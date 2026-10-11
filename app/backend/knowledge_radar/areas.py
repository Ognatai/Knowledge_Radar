"""Subject areas of the notes and the "new and updated" list, for the site.

`public/areas.yaml` assigns every note to exactly one main area (`notes`), in which
it is listed and counted; cross-cutting notes can also appear in up to two further
areas (`also`). The order in the file is the display order.

"New and updated" lists notes added after the initial migration (date of the
commit that added the file) and dated update entries (`### Updates`), newest
first.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, NoteRepositoryError

AREAS_PATH = REPOSITORY_ROOT / "public" / "areas.yaml"
MAX_SECONDARY_AREAS = 2
# The notes migrated from the old vault were added up to 2026-10-07; they are not news.
NEWS_SINCE = dt.date(2026, 10, 8)
NEWS_LIMIT = 12
UPDATE_ENTRY = re.compile(r"^#### (\d{4}-\d{2}-\d{2})\s+[—–-]\s+(.+?)\s*$", re.MULTILINE)
UPDATES_HEADINGS = {"en": "### Updates", "de": "### Aktualisierungen"}


class AreaError(NoteRepositoryError):
    """Raised when areas.yaml does not assign every note correctly."""


@dataclass(frozen=True)
class Area:
    id: str
    name_en: str
    name_de: str
    notes: list[str]
    also: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {"id": self.id, "name_en": self.name_en, "name_de": self.name_de, "notes": self.notes, "also": self.also}


def areas_path(notes_directory: Path) -> Path:
    """`areas.yaml` sits next to the notes directory (`public/areas.yaml`)."""
    return notes_directory.parent / "areas.yaml"


def load_areas(note_slugs: set[str], path: Path = AREAS_PATH) -> list[Area]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise AreaError(f"{path}: could not read: {exc}") from exc
    areas = []
    for index, entry in enumerate(raw.get("areas") or []):
        where = f"{path}: areas[{index}]"
        if not isinstance(entry, dict) or not all(str(entry.get(key, "")).strip() for key in ("id", "name_en", "name_de")):
            raise AreaError(f"{where}: each area needs id, name_en and name_de.")
        areas.append(
            Area(
                id=str(entry["id"]),
                name_en=str(entry["name_en"]),
                name_de=str(entry["name_de"]),
                notes=[str(slug) for slug in entry.get("notes") or []],
                also=[str(slug) for slug in entry.get("also") or []],
            )
        )

    main: dict[str, str] = {}
    secondary: dict[str, list[str]] = {}
    for area in areas:
        for slug in area.notes:
            if slug in main:
                raise AreaError(f"{path}: '{slug}' has two main areas, '{main[slug]}' and '{area.id}'.")
            main[slug] = area.id
        for slug in area.also:
            secondary.setdefault(slug, []).append(area.id)
    for slug, area_ids in secondary.items():
        if main.get(slug) in area_ids:
            raise AreaError(f"{path}: '{slug}' is listed under 'also' in its own main area '{main[slug]}'.")
        if len(area_ids) > MAX_SECONDARY_AREAS:
            raise AreaError(f"{path}: '{slug}' appears in more than {MAX_SECONDARY_AREAS} further areas.")
    unknown = sorted((set(main) | set(secondary)) - note_slugs)
    if unknown:
        raise AreaError(f"{path}: unknown notes: {', '.join(unknown)}.")
    missing = sorted(note_slugs - set(main))
    if missing:
        raise AreaError(f"{path}: notes without a main area: {', '.join(missing)}.")
    return areas


def added_dates(notes_directory: Path) -> dict[str, dt.date]:
    """The date of the commit that added each note file; empty without Git history."""
    try:
        log = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%x00%as", "--name-only", "--", "."],
            cwd=notes_directory,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {}
    dates: dict[str, dt.date] = {}
    for block in log.split("\x00")[1:]:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        day = dt.date.fromisoformat(lines[0])
        for name in lines[1:]:
            if name.endswith(".md"):
                # The log runs newest first; the last date seen is when the file was added.
                dates[Path(name).stem] = day
    return dates


def update_entries(content: str, language: str) -> list[tuple[dt.date, str]]:
    start = content.find(f"{UPDATES_HEADINGS[language]}\n")
    if start < 0:
        return []
    return [(dt.date.fromisoformat(day), title) for day, title in UPDATE_ENTRY.findall(content[start:])]


def news(
    notes: list[NoteDetail],
    added: dict[str, dt.date],
    since: dt.date = NEWS_SINCE,
    limit: int = NEWS_LIMIT,
) -> list[dict[str, Any]]:
    """New notes and update entries since `since`, newest first."""
    items: list[dict[str, Any]] = []
    for note in notes:
        day = added.get(note.slug)
        if day and day >= since:
            items.append({"kind": "new", "slug": note.slug, "date": day.isoformat()})
        german = dict(update_entries(note.content_de, "de"))
        for day, title in update_entries(note.content_en, "en"):
            if day >= since:
                items.append(
                    {"kind": "update", "slug": note.slug, "date": day.isoformat(), "title_en": title, "title_de": german.get(day, title)}
                )
    items.sort(key=lambda item: (item["date"], item["kind"] == "new", item["slug"]), reverse=True)
    return items[:limit]
