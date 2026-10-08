"""Load and validate the versioned knowledge graph in `public/graph/`.

The graph's source of truth is files, not a database:

- every public note describes one entity, whose id is the note's slug;
- `entities.yaml` registers further entities that have no note of their own;
- `extractions/<slug>.yaml` lists the entities a note discusses (`DISCUSSES`) and the
  entity-to-entity relations it supports, each with a verbatim evidence quote from
  the note's English section.

Everything is checked against `schema.yaml`, so a malformed extraction fails loudly
instead of reaching the site or a database index.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

import yaml

from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import (
    REPOSITORY_ROOT,
    SCHEMA_PATH,
    public_entity_types,
)

DEFAULT_GRAPH_DIRECTORY = REPOSITORY_ROOT / "public" / "graph"
REGISTRY_FILE_NAME = "entities.yaml"
EXTRACTIONS_DIRECTORY_NAME = "extractions"
FORMAT_VERSION = 1
# Relations a note's text can support; DISCUSSES and RELATED_TO are derived, not extracted.
DERIVED_RELATION_TYPES = frozenset({"DISCUSSES", "RELATED_TO"})
ENTITY_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WIKILINK_LABEL_PATTERN = re.compile(r"\[\[([^\[\]|#\\]+)(?:#[^\[\]|\\]*)?(?:\\?\|([^\[\]]*))?\]\]")


class GraphError(ValueError):
    """Raised when the versioned graph files do not follow the graph contract."""


@dataclass(frozen=True)
class Entity:
    id: str
    type: str
    name_en: str
    name_de: str
    aliases: list[str] = field(default_factory=list)
    note: str | None = None


@dataclass(frozen=True)
class Relation:
    source: str
    type: str
    target: str
    note: str
    evidence: str


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity]
    # (note slug, entity id)
    discusses: set[tuple[str, str]]
    relations: list[Relation]
    # Notes changed since their extraction; they need to be extracted again.
    stale_extractions: list[str]


@cache
def public_relation_types(schema_path: Path = SCHEMA_PATH) -> dict[str, tuple[frozenset[str], frozenset[str]]]:
    """Extractable public relation types with their allowed (from, to) entity types."""
    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    relation_types: dict[str, tuple[frozenset[str], frozenset[str]]] = {}
    for name, definition in schema.get("relation_types", {}).items():
        if definition.get("visibility") != "public" or name in DERIVED_RELATION_TYPES:
            continue
        relation_types[name] = (frozenset(definition["from"]), frozenset(definition["to"]))
    return relation_types


def note_sha256(path: Path) -> str:
    """Hash of a note's content; line endings are normalised, since Git checks
    notes out with CRLF on Windows and LF elsewhere."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def plain_text(markdown: str) -> str:
    """Note text as a reader sees it: wikilink labels, no emphasis, single spaces."""
    text = WIKILINK_LABEL_PATTERN.sub(lambda match: match.group(2) or match.group(1), markdown)
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def _read_yaml(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GraphError(f"{path}: could not read YAML: {exc}") from exc
    if not isinstance(value, dict) or value.get("version") != FORMAT_VERSION:
        raise GraphError(f"{path}: expected a mapping with 'version: {FORMAT_VERSION}'.")
    return value


def _text(entry: dict, key: str, where: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise GraphError(f"{where}: '{key}' must be a non-empty string.")
    return value.strip()


def _string_list(value: object, key: str, where: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise GraphError(f"{where}: '{key}' must be a list of non-empty strings.")
    return [item.strip() for item in value]


def _load_registry(path: Path, entities: dict[str, Entity]) -> None:
    if not path.is_file():
        return
    entries = _read_yaml(path).get("entities") or []
    if not isinstance(entries, list):
        raise GraphError(f"{path}: 'entities' must be a list.")
    allowed_types = public_entity_types()
    for entry in entries:
        if not isinstance(entry, dict):
            raise GraphError(f"{path}: each entity must be a mapping.")
        entity_id = _text(entry, "id", str(path))
        where = f"{path}: entity '{entity_id}'"
        if not ENTITY_ID_PATTERN.match(entity_id):
            raise GraphError(f"{where}: id must be a lowercase ASCII slug.")
        if entity_id in entities:
            owner = entities[entity_id].note
            reason = f"the note '{owner}' already describes it" if owner else "it is registered twice"
            raise GraphError(f"{where}: duplicate id, {reason}.")
        entity_type = _text(entry, "type", where)
        if entity_type not in allowed_types:
            raise GraphError(
                f"{where}: type '{entity_type}' is not a public entity type "
                f"({', '.join(sorted(allowed_types))})."
            )
        entities[entity_id] = Entity(
            id=entity_id,
            type=entity_type,
            name_en=_text(entry, "name_en", where),
            name_de=_text(entry, "name_de", where),
            aliases=_string_list(entry.get("aliases"), "aliases", where),
        )


def _load_extraction(
    path: Path,
    note: NoteDetail,
    notes_directory: Path | None,
    graph: KnowledgeGraph,
) -> None:
    data = _read_yaml(path)
    where = str(path)
    recorded_hash = _text(data, "note_sha256", where)
    _text(data, "extracted_by", where)
    if notes_directory is not None:
        current_hash = note_sha256(notes_directory / f"{note.slug}.md")
        if recorded_hash != current_hash:
            graph.stale_extractions.append(note.slug)

    discussed = {note.slug}
    for entity_id in _string_list(data.get("discusses"), "discusses", where):
        if entity_id not in graph.entities:
            raise GraphError(f"{where}: discusses unknown entity '{entity_id}'.")
        discussed.add(entity_id)
    graph.discusses.update((note.slug, entity_id) for entity_id in discussed)

    relations = data.get("relations") or []
    if not isinstance(relations, list):
        raise GraphError(f"{where}: 'relations' must be a list.")
    allowed = public_relation_types()
    note_text = plain_text(note.content_en)
    for entry in relations:
        if not isinstance(entry, dict):
            raise GraphError(f"{where}: each relation must be a mapping.")
        source = _text(entry, "from", where)
        relation_type = _text(entry, "type", where)
        target = _text(entry, "to", where)
        label = f"{where}: relation {source} {relation_type} {target}"
        if relation_type not in allowed:
            raise GraphError(
                f"{label}: '{relation_type}' is not an extractable public relation type "
                f"({', '.join(sorted(allowed))})."
            )
        for endpoint in (source, target):
            if endpoint not in discussed:
                raise GraphError(f"{label}: '{endpoint}' is not listed in 'discusses'.")
        from_types, to_types = allowed[relation_type]
        source_type = graph.entities[source].type
        target_type = graph.entities[target].type
        if source_type not in from_types or target_type not in to_types:
            raise GraphError(
                f"{label}: {relation_type} does not allow {source_type} -> {target_type} "
                f"(schema: {sorted(from_types)} -> {sorted(to_types)})."
            )
        evidence = _text(entry, "evidence", label)
        if plain_text(evidence) not in note_text:
            raise GraphError(f"{label}: evidence is not a verbatim quote from the EN section: {evidence!r}.")
        graph.relations.append(
            Relation(source=source, type=relation_type, target=target, note=note.slug, evidence=evidence)
        )


def load_graph(
    graph_directory: Path | None,
    notes: list[NoteDetail],
    notes_directory: Path | None = None,
) -> KnowledgeGraph:
    """Combine note entities, the registry, and per-note extractions into one graph.

    `notes_directory` enables the staleness check (note changed after extraction);
    without it, recorded hashes are not compared.
    """
    graph = KnowledgeGraph(
        entities={
            note.slug: Entity(
                id=note.slug,
                type=note.entity_type,
                name_en=note.title_en,
                name_de=note.title_de,
                note=note.slug,
            )
            for note in notes
        },
        discusses={(note.slug, note.slug) for note in notes},
        relations=[],
        stale_extractions=[],
    )
    if graph_directory is None or not graph_directory.is_dir():
        return graph

    _load_registry(graph_directory / REGISTRY_FILE_NAME, graph.entities)
    notes_by_slug = {note.slug: note for note in notes}
    extractions_directory = graph_directory / EXTRACTIONS_DIRECTORY_NAME
    paths = sorted(extractions_directory.rglob("*.yaml")) if extractions_directory.is_dir() else []
    for path in paths:
        slug = path.relative_to(extractions_directory).with_suffix("").as_posix()
        note = notes_by_slug.get(slug)
        if note is None:
            raise GraphError(f"{path}: there is no public note '{slug}'.")
        _load_extraction(path, note, notes_directory, graph)
    return graph
