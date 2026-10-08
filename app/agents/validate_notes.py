"""Validate public Markdown notes before they enter the agent pipeline.

Checks the basic note contract (frontmatter, sources, EN/DE sections, links),
the note templates (docs/note-templates.md), and the versioned graph files
(public/graph/) against schema.yaml.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, GraphError, load_graph
from app.backend.knowledge_radar.notes import (
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)
from app.backend.knowledge_radar.templates import check_template_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=configured_notes_directory(),
        help="Public Markdown directory to validate.",
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=DEFAULT_GRAPH_DIRECTORY,
        help="Versioned graph directory (entity registry and per-note extractions).",
    )
    args = parser.parse_args()

    try:
        notes = load_notes(args.notes_dir)
    except NoteRepositoryError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    failed = False
    for note in notes:
        problems = check_template_file(args.notes_dir / f"{note.slug}.md")
        if problems:
            failed = True
            print(f"{note.slug}: does not follow its note template:", file=sys.stderr)
            for problem in problems:
                print(f"  - {problem}", file=sys.stderr)
    if failed:
        return 1

    try:
        graph = load_graph(args.graph_dir, notes, args.notes_dir)
    except GraphError as exc:
        print(f"Graph validation failed: {exc}", file=sys.stderr)
        return 1
    # A stale extraction is still valid; the pipeline extracts the note again.
    for slug in graph.stale_extractions:
        print(f"Warning: {slug} changed since its extraction; extract it again.", file=sys.stderr)

    print(
        f"Validated {len(notes)} public note(s) in {args.notes_dir} and the graph "
        f"({len(graph.entities)} entities, {len(graph.relations)} relations)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
