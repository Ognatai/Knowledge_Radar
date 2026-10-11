"""The private local index: the private repository in its own Neo4j database.

Public and private stay physically separate in every index (decided 2026-10-11): the
private repository is indexed into a separate Neo4j container (`neo4j-private`, own
volume, own password, bolt port 7688), never into the public index that the monitoring
pipeline queries. Only the chat and /prep read it. Public entities that private
documents refer to are copied in as plain nodes, so that a retro can point to the
knowledge-base topic it found lacking; nothing flows the other way.

    python -m app.backend.knowledge_radar.private_index             # incremental update
    python -m app.backend.knowledge_radar.private_index rebuild
    python -m app.backend.knowledge_radar.private_index search "What did they ask about RAG?"
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.config import LocalConfigError, load_local_config
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, Entity, KnowledgeGraph, Relation, load_graph
from app.backend.knowledge_radar.index import KEYRING_SERVICE, Neo4jStore, update_index
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes
from app.backend.knowledge_radar.private_repo import (
    PrivateDocument,
    PrivateRepoError,
    as_note,
    document_slug,
    document_text,
    document_titles,
    load_documents,
)

PRIVATE_URI = "bolt://127.0.0.1:7688"
KEYRING_USER = "neo4j-private"
PUBLIC_URI = "bolt://127.0.0.1:7687"


def private_uri() -> str:
    """The private index's address; it must never be the public index's."""
    uri = os.environ.get("NEO4J_PRIVATE_URI", PRIVATE_URI)
    if uri == os.environ.get("NEO4J_URI", PUBLIC_URI):
        raise RuntimeError(f"The private index must not use the public index's address ({uri}).")
    return uri


def private_password(keyring_lookup: Callable[[str, str], str | None] | None = None) -> str:
    password = os.environ.get("NEO4J_PRIVATE_PASSWORD")
    if password:
        return password
    if keyring_lookup is None:
        import keyring

        keyring_lookup = keyring.get_password
    password = keyring_lookup(KEYRING_SERVICE, KEYRING_USER)
    if not password:
        raise RuntimeError(f"No private index password. Store it once with `python -m keyring set {KEYRING_SERVICE} {KEYRING_USER}`.")
    return password


def connect_private() -> Any:
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(private_uri(), auth=("neo4j", private_password()), notifications_min_severity="OFF")
    driver.verify_connectivity()
    return driver


def _read(path: Path) -> dict[str, Any]:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


def _entity(entry: dict[str, Any]) -> Entity:
    return Entity(entry["id"], entry["type"], entry["name_en"], entry.get("name_de", entry["name_en"]), list(entry.get("aliases") or []))


def private_graph(root: Path, documents: list[PrivateDocument], public_entities: dict[str, Entity]) -> KnowledgeGraph:
    """Registry, structure, requirements and extractions of the private repository as one graph."""
    graph_directory = root / "graph"
    entities: dict[str, Entity] = {}
    relations: list[Relation] = []
    for name in ("entities.yaml", "structure.yaml", "requirements.yaml"):
        data = _read(graph_directory / name)
        entities.update({entry["id"]: _entity(entry) for entry in data.get("entities") or []})
        relations += [
            Relation(r["from"], r["type"], r["to"], note=str(r.get("source", name)), evidence="")
            for r in data.get("relations") or []
        ]
    slugs = {document_slug(document) for document in documents}
    discusses: set[tuple[str, str]] = set()
    for path in sorted((graph_directory / "extractions").glob("*.yaml")):
        if path.stem not in slugs:
            continue
        data = _read(path)
        discusses |= {(path.stem, entity) for entity in data.get("discusses") or []}
        relations += [Relation(r["from"], r["type"], r["to"], note=path.stem, evidence=r.get("evidence", "")) for r in data.get("relations") or []]
    # Public entities the private documents refer to come along as plain nodes.
    referenced = {entity for _, entity in discusses} | {r.source for r in relations} | {r.target for r in relations}
    for entity_id in referenced - set(entities):
        if entity_id in public_entities:
            entities[entity_id] = public_entities[entity_id]
    relations = [r for r in relations if r.source in entities and r.target in entities]
    discusses = {(note, entity) for note, entity in discusses if entity in entities}
    return KnowledgeGraph(entities=entities, discusses=discusses, relations=relations, stale_extractions=[])


def private_notes(documents: list[PrivateDocument]) -> tuple[list[NoteDetail], dict[str, Path]]:
    """Documents with text (body or frontmatter facts), as notes with readable titles, and the file behind each."""
    titles = document_titles(documents)
    with_text = [document for document in documents if document_text(document).strip()]
    return [as_note(d, titles[d.id]) for d in with_text], {document_slug(d): d.path for d in with_text}


def update_private_index(store: Neo4jStore, root: Path, public_entities: dict[str, Entity], *, rebuild: bool = False,
                         progress: Callable[[str], None] = print):
    """Embed what changed in the private repository and sync its graph."""
    documents = load_documents(root)
    notes, paths = private_notes(documents)
    return update_index(
        store, notes, private_graph(root, documents, public_entities), root,
        embed=embeddings.embed, model=embeddings.model_name(), rebuild=rebuild, progress=progress, paths=paths,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="update", choices=["update", "rebuild", "search"])
    parser.add_argument("query", nargs="?")
    parser.add_argument("-k", "--limit", type=int, default=5)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        config = load_local_config()
    except LocalConfigError as exc:
        print(exc, file=sys.stderr)
        return 1
    if not config.has_private_repo:
        print("No private_repo_path in local-config.yaml; there is no private index to build.", file=sys.stderr)
        return 1
    try:
        driver = connect_private()
    except Exception as exc:  # the driver raises several unrelated exception types
        print(f"Could not connect to the private index: {exc}", file=sys.stderr)
        return 1
    with driver:
        store = Neo4jStore(driver, visibility="private")
        if args.command == "search":
            if not args.query:
                parser.error("search needs a query")
            for hit in store.search(embeddings.embed([embeddings.query_text(args.query)])[0], args.limit):
                print(f"{hit['score']:.3f}  {hit['note']} {hit['heading']}\n       {hit['text'][:160].replace(chr(10), ' ')}")
            return 0
        notes_directory = configured_notes_directory()
        public = load_graph(DEFAULT_GRAPH_DIRECTORY, load_notes(notes_directory), notes_directory)
        try:
            result = update_private_index(store, config.private_repo_path, public.entities, rebuild=args.command == "rebuild")
        except PrivateRepoError as exc:
            print(f"Private index update failed: {exc}", file=sys.stderr)
            return 1
    print(f"{'Rebuilt' if result.full_rebuild else 'Updated'} private index: {len(result.embedded)} documents embedded, {len(result.deleted)} removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
