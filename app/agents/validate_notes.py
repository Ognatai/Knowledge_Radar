"""Validate public Markdown notes before they enter the agent pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app.backend.knowledge_radar.notes import (
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=configured_notes_directory(),
        help="Public Markdown directory to validate.",
    )
    args = parser.parse_args()

    try:
        notes = load_notes(args.notes_dir)
    except NoteRepositoryError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Validated {len(notes)} public note(s) in {args.notes_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
