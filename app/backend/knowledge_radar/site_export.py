"""Export the public notes as static JSON for the GitHub Pages site.

The export reads only `public/notes/`. It produces the two-layer graph model:
`Note` nodes, the `Entity` node each note describes (`DISCUSSES`), and note-to-note
`RELATED_TO` edges from [[wikilinks]]. Once the Kuzu public index exists, this
module becomes its export step; the JSON shape stays the same.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

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


def entity_id(entity_type: str, name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return f"entity:{entity_type}:{slug}"


def build_site_data(notes: list[NoteDetail]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    entities: dict[str, dict[str, Any]] = {}

    for note in notes:
        note_id = f"note:{note.slug}"
        nodes.append(
            {
                "id": note_id,
                "kind": "note",
                "slug": note.slug,
                "title_en": note.title_en,
                "title_de": note.title_de,
            }
        )
        # Until the extraction agent exists, each note contributes the entity it describes.
        described_id = entity_id(note.entity_type, note.title_en)
        entity = entities.setdefault(
            described_id,
            {
                "id": described_id,
                "kind": "entity",
                "entity_type": note.entity_type,
                "name_en": note.title_en,
                "name_de": note.title_de,
                "note": note.slug,
            },
        )
        edges.append({"source": note_id, "target": entity["id"], "type": "DISCUSSES"})
        for linked_slug in note.links:
            edges.append(
                {"source": note_id, "target": f"note:{linked_slug}", "type": "RELATED_TO"}
            )

    return {
        "version": EXPORT_FORMAT_VERSION,
        "notes": [note.model_dump() for note in notes],
        "graph": {"nodes": nodes + list(entities.values()), "edges": edges},
    }


def export_site_data(notes_directory: Path, output_directory: Path) -> Path:
    data = build_site_data(load_notes(notes_directory))
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
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_DIRECTORY)
    args = parser.parse_args()

    try:
        output_path = export_site_data(args.notes_dir, args.out)
    except NoteRepositoryError as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
