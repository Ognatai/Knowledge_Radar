"""Ingest the private repository: the structural graph of the company folders.

Reads the private checkout configured in `local-config.yaml`, builds the graph its
folders and frontmatter describe (`private_repo.structural_graph`) and writes it to
`graph/structure.yaml` in the private repository, never into this public one. Retro
gaps that name no known topic are printed: they are candidates for the monitoring
run's watchlist.

    python -m app.agents.private_ingest
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from app.backend.knowledge_radar.config import LocalConfigError, load_local_config
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, Entity, load_graph
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory, load_notes
from app.backend.knowledge_radar.private_repo import PrivateRepoError, StructuralGraph, load_documents, structural_graph

STRUCTURE_FILE = Path("graph") / "structure.yaml"
REGISTRY_FILE = Path("graph") / "entities.yaml"


def private_registry(root: Path) -> dict[str, Entity]:
    path = root / REGISTRY_FILE
    if not path.is_file():
        return {}
    entries = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("entities") or []
    return {
        entry["id"]: Entity(entry["id"], entry["type"], entry["name_en"], entry.get("name_de", entry["name_en"]), list(entry.get("aliases") or []))
        for entry in entries
    }


def write_structure(root: Path, graph: StructuralGraph, public_root: Path = REPOSITORY_ROOT) -> Path:
    """Write the structural graph into the private repository; refuse any path in the public one."""
    path = (root / STRUCTURE_FILE).resolve()
    if path.is_relative_to(public_root.resolve()):
        raise PrivateRepoError(f"Refusing to write private data into the public repository: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(graph.to_yaml(), encoding="utf-8")
    return path


def ingest(root: Path, known: dict[str, Entity]) -> tuple[StructuralGraph, Path]:
    graph = structural_graph(load_documents(root), {**known, **private_registry(root)})
    return graph, write_structure(root, graph)


def main() -> int:
    try:
        config = load_local_config()
    except LocalConfigError as exc:
        print(exc, file=sys.stderr)
        return 1
    if not config.has_private_repo:
        print("No private_repo_path in local-config.yaml; nothing to ingest.", file=sys.stderr)
        return 1
    notes_directory = configured_notes_directory()
    public = load_graph(DEFAULT_GRAPH_DIRECTORY, load_notes(notes_directory), notes_directory)
    try:
        graph, path = ingest(config.private_repo_path, public.entities)
    except PrivateRepoError as exc:
        print(f"Ingestion failed: {exc}", file=sys.stderr)
        return 1
    print(f"{len(graph.entities)} entities, {len(graph.relations)} relations -> {path}")
    for gap in graph.open_gaps:
        print(f"Open gap ({gap['retro']}): {gap['topic']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
