"""Dated update entries in notes, and the rule for when a note is rewritten.

An update does not touch a note's text: it is appended as a dated `####` entry under
a final `### Updates` / `### Aktualisierungen` section, and its source joins the
frontmatter `sources`. A note is rewritten from scratch (through the same quality
gates) once it has more than three updates, or when its `last_rewrite_date` lies
more than six months back (architecture document, "Agent Pipeline", curator).
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass

import yaml

from app.backend.knowledge_radar.notes import FRONTMATTER_PATTERN, SECTION_PATTERN

UPDATES_HEADINGS = {"EN": "Updates", "DE": "Aktualisierungen"}
MAX_UPDATES = 3
MAX_DAYS_SINCE_REWRITE = 183


@dataclass(frozen=True)
class NoteUpdate:
    day: dt.date
    title_en: str
    body_en: str
    title_de: str
    body_de: str
    source: str


def _add_source(frontmatter: str, url: str) -> str:
    """Append `url` to the sources list, keeping the list's own indentation."""
    match = re.search(r"^sources:\s*\n((?:[ \t]*-[^\n]*\n)+)", frontmatter, re.MULTILINE)
    if match is None:
        raise ValueError("the note has no 'sources' list")
    entries = match.group(1)
    if re.search(rf"^[ \t]*-\s*{re.escape(url)}\s*$", entries, re.MULTILINE):
        return frontmatter
    indent = re.match(r"[ \t]*", entries).group(0)
    return frontmatter[: match.end(1)] + f"{indent}- {url}\n" + frontmatter[match.end(1) :]


def _append_entry(section: str, heading: str, entry: str) -> str:
    body = section.rstrip("\n")
    if f"\n### {heading}\n" not in f"\n{body}\n":
        body += f"\n\n### {heading}"
    return f"{body}\n\n{entry}\n\n"


def add_update(text: str, update: NoteUpdate) -> str:
    """The note's file content with the update appended in both languages."""
    match = FRONTMATTER_PATTERN.match(text)
    if match is None:
        raise ValueError("the note has no frontmatter")
    frontmatter_end = match.end(1)
    head = _add_source(text[:frontmatter_end] + "\n", update.source).rstrip("\n")
    body = text[frontmatter_end:]

    headers = list(SECTION_PATTERN.finditer(body))
    parts = []
    position = 0
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(body)
        parts.append(body[position : header.end()])
        section = body[header.end() : end]
        lang = header.group(1)
        if lang in UPDATES_HEADINGS:
            title, entry_body = (update.title_en, update.body_en) if lang == "EN" else (update.title_de, update.body_de)
            section = _append_entry(section, UPDATES_HEADINGS[lang], f"#### {update.day.isoformat()} — {title}\n{entry_body}")
            if index + 1 == len(headers):
                section = section.rstrip("\n") + "\n"
        parts.append(section)
        position = end
    return head + "".join(parts)


def _updates_section(text: str) -> str:
    match = FRONTMATTER_PATTERN.match(text)
    body = text[match.end() :] if match else text
    headers = list(SECTION_PATTERN.finditer(body))
    for index, header in enumerate(headers):
        if header.group(1) == "EN":
            end = headers[index + 1].start() if index + 1 < len(headers) else len(body)
            section = body[header.end() : end]
            start = section.find(f"### {UPDATES_HEADINGS['EN']}\n")
            return section[start:] if start >= 0 else ""
    return ""


def update_count(text: str) -> int:
    return len(re.findall(r"^#### ", _updates_section(text), re.MULTILINE))


def needs_rewrite(text: str, today: dt.date) -> str | None:
    """Why the note should be rewritten from scratch, or None."""
    count = update_count(text)
    if count > MAX_UPDATES:
        return f"{count} updates since the last rewrite"
    match = FRONTMATTER_PATTERN.match(text)
    frontmatter = (yaml.safe_load(match.group(1)) or {}) if match else {}
    last_rewrite = frontmatter.get("last_rewrite_date")
    if count and isinstance(last_rewrite, dt.date) and (today - last_rewrite).days > MAX_DAYS_SINCE_REWRITE:
        return f"last rewrite on {last_rewrite.isoformat()}, more than 6 months ago"
    return None
