"""Build and update the local index: the knowledge graph plus note embeddings in Neo4j.

Each machine keeps its own index, built from the versioned files (see the
architecture document, "Public export vs. local index"). The index is derived
data and can be rebuilt from the files at any time.

- The graph (notes, entities, DISCUSSES, RELATED_TO, entity relations) is
  synchronised in full on every run: it is small, and a full sync leaves nothing
  stale behind.
- Embeddings are the expensive part, so only notes whose content changed are
  embedded again. Changes are detected by content hash rather than `git diff`,
  which also covers uncommitted edits, rewritten history and a wiped database.
  A different embedding model or chunker version triggers a full rebuild.

    python -m app.backend.knowledge_radar.index            # incremental update
    python -m app.backend.knowledge_radar.index rebuild    # rebuild from scratch
    python -m app.backend.knowledge_radar.index search "How does LoRA work?"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.graph import (
    DEFAULT_GRAPH_DIRECTORY,
    GraphError,
    KnowledgeGraph,
    load_graph,
    note_sha256,
)
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import (
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
    public_entity_types,
)

# Bump when chunking changes, so existing embeddings are rebuilt.
CHUNKER_VERSION = 1
MAX_CHUNK_CHARACTERS = 2000
# Reference lists add noise to retrieval; the sources are in the frontmatter.
SKIPPED_HEADINGS = frozenset({"sources", "quellen"})
HEADING_PATTERN = re.compile(r"^(#{3,6})\s+(.+?)\s*$")
VECTOR_INDEX_NAME = "chunk_embedding"
RELATION_TYPE_PATTERN = re.compile(r"^[A-Z][A-Z_]*$")
ENTITY_TYPE_PATTERN = re.compile(r"^[A-Z][A-Za-z]*$")
KEYRING_SERVICE = "knowledge-radar"
KEYRING_USER = "neo4j"


@dataclass(frozen=True)
class Chunk:
    id: str
    note: str
    language: str
    title: str
    heading: str
    text: str

    @property
    def embedding_text(self) -> str:
        """The note title and heading give a short passage its context."""
        context = f"{self.title} > {self.heading}" if self.heading else self.title
        return f"{context}\n\n{self.text}"


def _split_long(text: str, max_characters: int) -> list[str]:
    parts: list[str] = []
    current = ""
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        while len(paragraph) > max_characters:
            if current:
                parts.append(current)
                current = ""
            parts.append(paragraph[:max_characters])
            paragraph = paragraph[max_characters:].strip()
        if not paragraph:
            continue
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= max_characters:
            current = candidate
        else:
            parts.append(current)
            current = paragraph
    if current:
        parts.append(current)
    return parts


def _sections(markdown: str) -> list[tuple[str, str]]:
    """(heading, text) per heading of level 3 or deeper; text before the first heading has ""."""
    sections: list[tuple[str, list[str]]] = [("", [])]
    skipping_level: int | None = None
    for line in markdown.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            level, heading = len(match.group(1)), match.group(2)
            if skipping_level is not None and level > skipping_level:
                continue
            skipping_level = level if heading.casefold() in SKIPPED_HEADINGS else None
            if skipping_level is None:
                sections.append((heading, []))
            continue
        if skipping_level is None:
            sections[-1][1].append(line)
    return [(heading, "\n".join(lines).strip()) for heading, lines in sections]


def chunk_note(note: NoteDetail, max_characters: int = MAX_CHUNK_CHARACTERS) -> list[Chunk]:
    """Passages of a note's EN and DE sections, split at headings and, if long, at paragraphs."""
    chunks: list[Chunk] = []
    for language, title, content in (("en", note.title_en, note.content_en), ("de", note.title_de, note.content_de)):
        number = 0
        for heading, text in _sections(content):
            for part in _split_long(text, max_characters) if text else []:
                chunks.append(
                    Chunk(
                        id=f"{note.slug}:{language}:{number}",
                        note=note.slug,
                        language=language,
                        title=title,
                        heading=heading,
                        text=part,
                    )
                )
                number += 1
    return chunks


@dataclass(frozen=True)
class IndexState:
    model: str
    chunker_version: int
    # Content hash of each note as last embedded.
    note_hashes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class UpdatePlan:
    embed: list[str]
    delete: list[str]
    full_rebuild: bool


def plan_update(
    current_hashes: dict[str, str],
    state: IndexState | None,
    *,
    model: str,
    rebuild: bool = False,
) -> UpdatePlan:
    """Which notes to embed and which to remove from the index."""
    full_rebuild = rebuild or state is None or state.model != model or state.chunker_version != CHUNKER_VERSION
    if full_rebuild:
        return UpdatePlan(embed=sorted(current_hashes), delete=[], full_rebuild=True)
    assert state is not None
    return UpdatePlan(
        embed=sorted(slug for slug, digest in current_hashes.items() if state.note_hashes.get(slug) != digest),
        delete=sorted(set(state.note_hashes) - set(current_hashes)),
        full_rebuild=False,
    )


class IndexStore(Protocol):
    def read_state(self) -> IndexState | None: ...
    def clear(self) -> None: ...
    def sync_graph(self, notes: list[NoteDetail], graph: KnowledgeGraph) -> None: ...
    def ensure_schema(self, dimensions: int) -> None: ...
    def replace_chunks(self, slug: str, content_hash: str, chunks: list[Chunk], vectors: list[list[float]]) -> None: ...
    def delete_chunks(self, slugs: list[str]) -> None: ...
    def write_state(self, state: IndexState) -> None: ...


@dataclass(frozen=True)
class UpdateResult:
    embedded: list[str]
    deleted: list[str]
    full_rebuild: bool


def update_index(
    store: IndexStore,
    notes: list[NoteDetail],
    graph: KnowledgeGraph,
    notes_directory: Path,
    *,
    embed: Callable[[list[str]], list[list[float]]],
    model: str,
    rebuild: bool = False,
    progress: Callable[[str], None] = lambda message: None,
) -> UpdateResult:
    hashes = {note.slug: note_sha256(notes_directory / f"{note.slug}.md") for note in notes}
    state = store.read_state()
    plan = plan_update(hashes, state, model=model, rebuild=rebuild)
    if plan.full_rebuild:
        store.clear()
    store.delete_chunks(plan.delete)
    store.sync_graph(notes, graph)

    by_slug = {note.slug: note for note in notes}
    schema_ready = False
    for position, slug in enumerate(plan.embed, start=1):
        chunks = chunk_note(by_slug[slug])
        vectors = embed([chunk.embedding_text for chunk in chunks]) if chunks else []
        if vectors and not schema_ready:
            store.ensure_schema(len(vectors[0]))
            schema_ready = True
        store.replace_chunks(slug, hashes[slug], chunks, vectors)
        progress(f"[{position}/{len(plan.embed)}] {slug}: {len(chunks)} chunks")

    store.write_state(IndexState(model=model, chunker_version=CHUNKER_VERSION, note_hashes=hashes))
    return UpdateResult(embedded=plan.embed, deleted=plan.delete, full_rebuild=plan.full_rebuild)


def neo4j_password(keyring_lookup: Callable[[str, str], str | None] | None = None) -> str:
    """NEO4J_PASSWORD (set for the Docker container), else the Windows Credential Manager."""
    password = os.environ.get("NEO4J_PASSWORD")
    if password:
        return password
    if keyring_lookup is None:
        import keyring

        keyring_lookup = keyring.get_password
    password = keyring_lookup(KEYRING_SERVICE, KEYRING_USER)
    if not password:
        raise RuntimeError(
            "No Neo4j password found. Store it once with "
            f"`python -m keyring set {KEYRING_SERVICE} {KEYRING_USER}` or set NEO4J_PASSWORD."
        )
    return password


class Neo4jStore:
    """The local index in Neo4j Community: graph nodes and edges plus `Chunk` nodes with embeddings."""

    def __init__(self, driver: Any, database: str | None = None) -> None:
        self.driver = driver
        self.database = database

    def _run(self, query: str, **parameters: Any) -> list[Any]:
        records, _, _ = self.driver.execute_query(query, parameters, database_=self.database)
        return records

    def read_state(self) -> IndexState | None:
        records = self._run("MATCH (s:IndexState {id: 'state'}) RETURN s.model AS model, s.chunker_version AS version")
        if not records:
            return None
        hashes = self._run("MATCH (n:Note) WHERE n.content_hash IS NOT NULL RETURN n.slug AS slug, n.content_hash AS hash")
        return IndexState(
            model=records[0]["model"],
            chunker_version=records[0]["version"],
            note_hashes={record["slug"]: record["hash"] for record in hashes},
        )

    def clear(self) -> None:
        # The vector index is dropped too: a new model may have other dimensions.
        self._run(f"DROP INDEX {VECTOR_INDEX_NAME} IF EXISTS")
        self._run("MATCH (c:Chunk) DETACH DELETE c")
        self._run("MATCH (n:Note) REMOVE n.content_hash")
        self._run("MATCH (s:IndexState) DELETE s")

    def ensure_schema(self, dimensions: int) -> None:
        self._run(
            f"CREATE VECTOR INDEX {VECTOR_INDEX_NAME} IF NOT EXISTS FOR (c:Chunk) ON c.embedding "
            "OPTIONS {indexConfig: {`vector.dimensions`: $dimensions, `vector.similarity_function`: 'cosine'}}",
            dimensions=dimensions,
        )

    def sync_graph(self, notes: list[NoteDetail], graph: KnowledgeGraph) -> None:
        for label, key in (("Note", "slug"), ("Entity", "id"), ("Chunk", "id")):
            self._run(f"CREATE CONSTRAINT {label.lower()}_{key} IF NOT EXISTS FOR (n:{label}) REQUIRE n.{key} IS UNIQUE")

        note_rows = [
            {"slug": note.slug, "title_en": note.title_en, "title_de": note.title_de, "entity_type": note.entity_type}
            for note in notes
        ]
        entity_rows = [
            {
                "id": entity.id,
                "type": entity.type,
                "name_en": entity.name_en,
                "name_de": entity.name_de,
                "aliases": entity.aliases,
                "note": entity.note,
            }
            for entity in graph.entities.values()
        ]
        discusses = [{"note": note, "entity": entity} for note, entity in sorted(graph.discusses)]
        related = [{"source": note.slug, "target": target} for note in notes for target in note.links]
        relations: dict[str, dict[tuple[str, str], dict[str, list[str]]]] = defaultdict(dict)
        for relation in graph.relations:
            entry = relations[relation.type].setdefault((relation.source, relation.target), {"notes": [], "evidence": []})
            entry["notes"].append(relation.note)
            entry["evidence"].append(relation.evidence)

        def write(tx: Any) -> None:
            tx.run(
                "UNWIND $rows AS row MERGE (n:Note {slug: row.slug}) "
                "SET n.title_en = row.title_en, n.title_de = row.title_de, "
                "n.entity_type = row.entity_type, n.visibility = 'public'",
                rows=note_rows,
            )
            tx.run(
                "MATCH (n:Note) WHERE NOT n.slug IN $slugs "
                "OPTIONAL MATCH (c:Chunk)-[:PART_OF]->(n) DETACH DELETE c, n",
                slugs=[row["slug"] for row in note_rows],
            )
            tx.run(
                "UNWIND $rows AS row MERGE (e:Entity {id: row.id}) "
                "SET e.type = row.type, e.name_en = row.name_en, e.name_de = row.name_de, "
                "e.aliases = row.aliases, e.note = row.note",
                rows=entity_rows,
            )
            tx.run("MATCH (e:Entity) WHERE NOT e.id IN $ids DETACH DELETE e", ids=[row["id"] for row in entity_rows])
            # The entity type is also a label (MATCH (d:Dataset)); labels cannot be parameters.
            type_labels = sorted(public_entity_types())
            if not all(ENTITY_TYPE_PATTERN.match(label) for label in type_labels):
                raise GraphError(f"Unexpected entity type in {type_labels}.")
            tx.run(f"MATCH (e:Entity) REMOVE e:{':'.join(type_labels)}")
            for label in type_labels:
                tx.run(f"MATCH (e:Entity {{type: $type}}) SET e:{label}", type=label)
            tx.run("MATCH (:Note)-[r:DISCUSSES|RELATED_TO]->() DELETE r")
            tx.run("MATCH (:Entity)-[r]->(:Entity) DELETE r")
            tx.run(
                "UNWIND $rows AS row MATCH (n:Note {slug: row.note}), (e:Entity {id: row.entity}) "
                "MERGE (n)-[:DISCUSSES]->(e)",
                rows=discusses,
            )
            tx.run(
                "UNWIND $rows AS row MATCH (a:Note {slug: row.source}), (b:Note {slug: row.target}) "
                "MERGE (a)-[:RELATED_TO]->(b)",
                rows=related,
            )
            for relation_type, pairs in relations.items():
                # Relationship types cannot be query parameters; they come from schema.yaml.
                if not RELATION_TYPE_PATTERN.match(relation_type):
                    raise GraphError(f"Unexpected relation type {relation_type!r}.")
                rows = [{"source": s, "target": t, **entry} for (s, t), entry in pairs.items()]
                tx.run(
                    f"UNWIND $rows AS row MATCH (a:Entity {{id: row.source}}), (b:Entity {{id: row.target}}) "
                    f"MERGE (a)-[r:{relation_type}]->(b) SET r.notes = row.notes, r.evidence = row.evidence",
                    rows=rows,
                )

        with self.driver.session(database=self.database) as session:
            session.execute_write(write)

    def replace_chunks(self, slug: str, content_hash: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        rows = [
            {"id": c.id, "language": c.language, "heading": c.heading, "text": c.text, "embedding": v}
            for c, v in zip(chunks, vectors, strict=True)
        ]

        def write(tx: Any) -> None:
            tx.run("MATCH (c:Chunk)-[:PART_OF]->(:Note {slug: $slug}) DETACH DELETE c", slug=slug)
            tx.run(
                "MATCH (n:Note {slug: $slug}) "
                "UNWIND $rows AS row CREATE (c:Chunk {id: row.id, language: row.language, heading: row.heading, "
                "text: row.text, embedding: row.embedding})-[:PART_OF]->(n)",
                slug=slug,
                rows=rows,
            )
            tx.run("MATCH (n:Note {slug: $slug}) SET n.content_hash = $hash", slug=slug, hash=content_hash)

        with self.driver.session(database=self.database) as session:
            session.execute_write(write)

    def delete_chunks(self, slugs: list[str]) -> None:
        if slugs:
            self._run("MATCH (c:Chunk)-[:PART_OF]->(n:Note) WHERE n.slug IN $slugs DETACH DELETE c", slugs=slugs)

    def write_state(self, state: IndexState) -> None:
        # Note hashes live on the Note nodes, so an interrupted run keeps its progress.
        self._run(
            "MERGE (s:IndexState {id: 'state'}) SET s.model = $model, s.chunker_version = $version",
            model=state.model,
            version=state.chunker_version,
        )

    def search(self, vector: list[float], limit: int = 5) -> list[dict[str, Any]]:
        """Nearest passages with their note and the entities that note discusses."""
        records = self._run(
            f"CALL db.index.vector.queryNodes('{VECTOR_INDEX_NAME}', $limit, $vector) YIELD node, score "
            "MATCH (node)-[:PART_OF]->(n:Note) "
            "OPTIONAL MATCH (n)-[:DISCUSSES]->(e:Entity) WHERE e.id <> n.slug "
            "RETURN n.slug AS note, node.language AS language, node.heading AS heading, node.text AS text, "
            "score, collect(e.name_en) AS entities ORDER BY score DESC",
            limit=limit,
            vector=vector,
        )
        return [dict(record) for record in records]


def connect() -> Any:
    from neo4j import GraphDatabase

    uri = os.environ.get("NEO4J_URI", "bolt://127.0.0.1:7687")
    user = os.environ.get("NEO4J_USER", KEYRING_USER)
    driver = GraphDatabase.driver(uri, auth=(user, neo4j_password()))
    driver.verify_connectivity()
    return driver


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="update", choices=["update", "rebuild", "search"])
    parser.add_argument("query", nargs="?", help="search text (for `search`)")
    parser.add_argument("-k", "--limit", type=int, default=5)
    parser.add_argument("--notes-dir", type=Path, default=configured_notes_directory())
    parser.add_argument("--graph-dir", type=Path, default=DEFAULT_GRAPH_DIRECTORY)
    args = parser.parse_args()

    try:
        driver = connect()
    except Exception as exc:  # the driver raises several unrelated exception types
        print(f"Could not connect to Neo4j: {exc}", file=sys.stderr)
        return 1
    with driver:
        store = Neo4jStore(driver)
        if args.command == "search":
            if not args.query:
                parser.error("search needs a query")
            vector = embeddings.embed([embeddings.query_text(args.query)])[0]
            for hit in store.search(vector, args.limit):
                print(f"{hit['score']:.3f}  {hit['note']} [{hit['language']}] {hit['heading']}")
                print(f"       {hit['text'][:160].replace(chr(10), ' ')}")
                if hit["entities"]:
                    print(f"       entities: {', '.join(hit['entities'][:8])}")
            return 0

        try:
            notes = load_notes(args.notes_dir)
            graph = load_graph(args.graph_dir, notes, args.notes_dir)
        except (NoteRepositoryError, GraphError) as exc:
            print(f"Index update failed: {exc}", file=sys.stderr)
            return 1
        if graph.stale_extractions:
            print(f"Warning: extractions older than their notes: {', '.join(graph.stale_extractions)}", file=sys.stderr)
        result = update_index(
            store,
            notes,
            graph,
            args.notes_dir,
            embed=embeddings.embed,
            model=embeddings.model_name(),
            rebuild=args.command == "rebuild",
            progress=print,
        )
    kind = "Rebuilt" if result.full_rebuild else "Updated"
    print(f"{kind} index: {len(result.embedded)} notes embedded, {len(result.deleted)} removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
