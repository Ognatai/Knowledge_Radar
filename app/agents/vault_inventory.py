"""Build a structural inventory of the Obsidian vault for the migration.

Reads every Markdown note of the vault directory and records what exists and how
it is linked, not the text itself (notes are rewritten, not imported):
headings, word count, and wikilinks resolved to the new English IDs from
`migration/vault-mapping.yaml`. Links under "Verwandte Themen" are kept apart
from links in the running text, and overview notes (hubs) become topic groups.

    python -m app.agents.vault_inventory "<path to vault>/Wissensdatenbank"

The vault path is a command-line argument and never written to the output.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

MIGRATION_DIRECTORY = REPOSITORY_ROOT / "migration"
DEFAULT_MAPPING = MIGRATION_DIRECTORY / "vault-mapping.yaml"
DEFAULT_OUTPUT = MIGRATION_DIRECTORY / "inventory.yaml"
RELATED_SECTION = "Verwandte Themen"
REGULATORY_AREAS = {"legal"}

CODE_BLOCK = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
# [[target]], [[target|label]], [[target#heading]], ![[embed]]
WIKILINK = re.compile(r"!?\[\[([^\[\]|#^]*)(?:[#^][^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")


@dataclass
class ParsedNote:
    title: str | None = None
    sections: list[str] = field(default_factory=list)
    words: int = 0
    # (target, enclosing level-2 section or None)
    links: list[tuple[str, str | None]] = field(default_factory=list)


def parse_note(text: str) -> ParsedNote:
    """Extract headings, word count, and wikilinks with their level-2 section."""
    body = CODE_BLOCK.sub("", text)
    parsed = ParsedNote(words=len(re.findall(r"\w+", body)))
    section: str | None = None
    for line in body.splitlines():
        heading = HEADING.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            if level == 1 and parsed.title is None:
                parsed.title = title
            elif level == 1 or level == 2:
                section = title
                parsed.sections.append(title)
            continue
        for match in WIKILINK.finditer(line):
            target = match.group(1).strip()
            if target:
                parsed.links.append((target, section))
    return parsed


def load_mapping(path: Path) -> dict[str, Any]:
    mapping = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict) or not isinstance(mapping.get("notes"), dict):
        raise ValueError(f"{path}: expected a mapping with a 'notes' section.")
    ids = [entry["id"] for entry in mapping["notes"].values() if not entry.get("hub")]
    duplicates = sorted(identifier for identifier, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"{path}: duplicate IDs: {', '.join(duplicates)}")
    return mapping


def build_inventory(vault: Path, mapping: dict[str, Any]) -> dict[str, Any]:
    entries: dict[str, dict[str, Any]] = mapping["notes"]
    areas: dict[str, str] = mapping.get("areas", {})

    paths = sorted(
        path for path in vault.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(vault).parts)
    )
    by_name = {path.stem: path for path in paths}
    unmapped = sorted(name for name in by_name if name not in entries)
    missing = sorted(name for name in entries if name not in by_name)
    if unmapped or missing:
        raise ValueError(
            "Mapping and vault differ. Unmapped notes: "
            f"{unmapped or 'none'}; mapped but missing: {missing or 'none'}."
        )

    def resolve(target: str) -> str | None:
        name = target.removesuffix(".md").rsplit("/", 1)[-1]
        return name if name in by_name else None

    notes: list[dict[str, Any]] = []
    hubs: list[dict[str, Any]] = []
    unresolved: list[dict[str, str]] = []
    linked_from: Counter[str] = Counter()

    for path in paths:
        name = path.stem
        entry = entries[name]
        parsed = parse_note(path.read_text(encoding="utf-8"))
        folder = path.relative_to(vault).parent.as_posix()
        area = areas.get(folder, folder or "root")

        inline: list[str] = []
        related: list[str] = []
        groups: dict[str, list[str]] = {}
        for target, section in parsed.links:
            resolved = resolve(target)
            if resolved is None:
                unresolved.append({"note": name, "target": target})
                continue
            target_entry = entries[resolved]
            if resolved == name or target_entry.get("hub"):
                continue  # self links and "back to overview" navigation
            target_id = target_entry["id"]
            if entry.get("hub"):
                group = groups.setdefault(section or "(intro)", [])
                if target_id not in group:
                    group.append(target_id)
                continue
            bucket = related if section == RELATED_SECTION else inline
            if target_id not in bucket:
                bucket.append(target_id)

        if entry.get("hub"):
            hubs.append({"source_title": name, "area": area, "groups": groups})
            continue

        for target_id in set(inline) | set(related):
            linked_from[target_id] += 1
        note: dict[str, Any] = {
            "id": entry["id"],
            "source_title": name,
            "area": area,
            "title_en": entry["title_en"],
            "title_de": entry["title_de"],
            "entity_type": entry["entity_type"],
            "template": entry.get(
                "template", "regulatory" if area in REGULATORY_AREAS else "technical"
            ),
        }
        if "jurisdiction" in entry:
            note["jurisdiction"] = entry["jurisdiction"]
        note.update(
            {
                "words": parsed.words,
                "sections": [s for s in parsed.sections if s != RELATED_SECTION],
                "links_inline": inline,
                "links_related_only": [t for t in related if t not in inline],
            }
        )
        notes.append(note)

    area_of = {note["id"]: note["area"] for note in notes}
    edges = {
        tuple(sorted((note["id"], target)))
        for note in notes
        for target in note["links_inline"] + note["links_related_only"]
    }
    directed = {
        (note["id"], target)
        for note in notes
        for target in note["links_inline"] + note["links_related_only"]
    }
    for note in notes:
        note["linked_from"] = linked_from[note["id"]]

    return {
        "version": 1,
        "source": f"Obsidian vault '{vault.name}'",
        "summary": {
            "notes": len(notes),
            "hubs": len(hubs),
            "words": sum(note["words"] for note in notes),
            "notes_per_area": dict(Counter(note["area"] for note in notes)),
            "notes_per_entity_type": dict(Counter(note["entity_type"] for note in notes)),
            "directed_links": len(directed),
            "connected_pairs": len(edges),
            "reciprocal_pairs": sum(1 for a, b in directed if (b, a) in directed) // 2,
            "cross_area_pairs": dict(
                Counter(
                    " <-> ".join(sorted({area_of[a], area_of[b]}))
                    for a, b in edges
                    if area_of[a] != area_of[b]
                )
            ),
            "most_linked": [
                {"id": identifier, "linked_from": count}
                for identifier, count in linked_from.most_common(15)
            ],
            "isolated": sorted(n["id"] for n in notes if not n["linked_from"]),
            "unresolved_links": unresolved,
        },
        "hubs": hubs,
        "notes": sorted(notes, key=lambda note: (note["area"], note["id"])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("vault", type=Path, help="vault directory to inventory")
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        inventory = build_inventory(args.vault, load_mapping(args.mapping))
    except (OSError, ValueError, KeyError) as exc:
        print(f"Inventory failed: {exc}", file=sys.stderr)
        return 1

    header = (
        "# Generated by `python -m app.agents.vault_inventory`; do not edit by hand.\n"
        "# Structure only (titles, sections, links); note texts are rewritten.\n"
    )
    args.out.write_text(
        header + yaml.safe_dump(inventory, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    summary = inventory["summary"]
    print(
        f"Wrote {args.out}: {summary['notes']} notes, {summary['hubs']} hubs, "
        f"{summary['connected_pairs']} connected pairs."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
