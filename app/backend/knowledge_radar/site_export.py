"""Export the public notes and graph as static JSON for the GitHub Pages site.

The export reads only `public/`: the notes and the versioned graph files in
`public/graph/` (see `graph.py`). It needs no database and no LLM, so it runs in
the cloud build. It produces the two-layer graph model: `Note` nodes, `Entity`
nodes, `DISCUSSES` and `RELATED_TO` edges, and entity-to-entity relations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from app.backend.knowledge_radar.graph import (
    DEFAULT_GRAPH_DIRECTORY,
    GraphError,
    load_graph,
    public_relation_types,
)
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import (
    REPOSITORY_ROOT,
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)

DEFAULT_OUTPUT_DIRECTORY = REPOSITORY_ROOT / "app" / "site" / "public" / "data"
OUTPUT_FILE_NAME = "site-data.json"
EXPORT_FORMAT_VERSION = 1


def build_site_data(notes: list[NoteDetail], graph_directory: Path | None) -> dict[str, Any]:
    graph = load_graph(graph_directory, notes)
    nodes: list[dict[str, Any]] = [
        {
            "id": f"note:{note.slug}",
            "kind": "note",
            "slug": note.slug,
            "title_en": note.title_en,
            "title_de": note.title_de,
        }
        for note in notes
    ]
    nodes += [
        {
            "id": f"entity:{entity.id}",
            "kind": "entity",
            "entity_type": entity.type,
            "name_en": entity.name_en,
            "name_de": entity.name_de,
            "note": entity.note,
        }
        for entity in sorted(graph.entities.values(), key=lambda entity: entity.id)
    ]

    edges: list[dict[str, Any]] = []
    for note_slug, entity in sorted(graph.discusses):
        edges.append({"source": f"note:{note_slug}", "target": f"entity:{entity}", "type": "DISCUSSES"})
    for note in notes:
        for linked_slug in note.links:
            edges.append({"source": f"note:{note.slug}", "target": f"note:{linked_slug}", "type": "RELATED_TO"})
    # Several notes may support the same relation; the site shows it once.
    symmetric_types = {name for name, definition in public_relation_types().items() if definition.symmetric}
    for source, relation_type, target in sorted({(r.source, r.type, r.target) for r in graph.relations}):
        edge: dict[str, Any] = {"source": f"entity:{source}", "target": f"entity:{target}", "type": relation_type}
        if relation_type in symmetric_types:
            edge["undirected"] = True
        edges.append(edge)

    return {
        "version": EXPORT_FORMAT_VERSION,
        "notes": [note.model_dump() for note in notes],
        "graph": {"nodes": nodes, "edges": edges},
    }


def export_site_data(notes_directory: Path, graph_directory: Path | None, output_directory: Path) -> Path:
    data = build_site_data(load_notes(notes_directory), graph_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / OUTPUT_FILE_NAME
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notes-dir", type=Path, default=configured_notes_directory())
    parser.add_argument("--graph-dir", type=Path, default=DEFAULT_GRAPH_DIRECTORY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_DIRECTORY)
    args = parser.parse_args()

    try:
        output_path = export_site_data(args.notes_dir, args.graph_dir, args.out)
    except (NoteRepositoryError, GraphError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
