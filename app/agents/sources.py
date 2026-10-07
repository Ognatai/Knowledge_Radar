"""Source metadata for note drafting: arXiv lookups and citation formatting.

A source entry is either an arXiv paper
(`arxiv: 2004.04906`, verified against an expected title fragment) or any
other URL with a hand-written citation. arXiv metadata comes from the official
API, is cached under `.knowledge-radar/cache/arxiv/`, and requests are spaced
as arXiv's API guidelines ask.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

CACHE_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "cache" / "arxiv"
API_URL = "https://export.arxiv.org/api/query?id_list={id}"
REQUEST_SPACING_SECONDS = 3.0
ATOM = {"atom": "http://www.w3.org/2005/Atom"}
_last_request = 0.0


class SourceError(ValueError):
    """Raised when a source cannot be resolved or does not match its expectation."""


@dataclass(frozen=True)
class Source:
    url: str
    citation: str  # Markdown, e.g. "Lewis, P. et al. (2020). *Title.* NeurIPS 2020. [arXiv:…](…)"
    short: str  # in-text form, e.g. "Lewis et al. (2020)"
    summary: str  # abstract or excerpt given to the model as evidence


def _fetch_arxiv(arxiv_id: str, cache_directory: Path) -> dict:
    global _last_request
    cache_directory.mkdir(parents=True, exist_ok=True)
    cached = cache_directory / f"{arxiv_id.replace('/', '_')}.json"
    if cached.is_file():
        return json.loads(cached.read_text(encoding="utf-8"))

    wait = REQUEST_SPACING_SECONDS - (time.monotonic() - _last_request)
    if wait > 0:
        time.sleep(wait)
    with urllib.request.urlopen(API_URL.format(id=arxiv_id), timeout=60) as response:
        feed = ET.fromstring(response.read())
    _last_request = time.monotonic()

    entry = feed.find("atom:entry", ATOM)
    title = entry.findtext("atom:title", default="", namespaces=ATOM) if entry is not None else ""
    if entry is None or not title.strip() or title.strip() == "Error":
        raise SourceError(f"arXiv:{arxiv_id} not found.")
    metadata = {
        "id": arxiv_id,
        "title": re.sub(r"\s+", " ", title).strip(),
        "authors": [
            author.findtext("atom:name", default="", namespaces=ATOM).strip()
            for author in entry.findall("atom:author", ATOM)
        ],
        "year": entry.findtext("atom:published", default="", namespaces=ATOM)[:4],
        "summary": re.sub(r"\s+", " ", entry.findtext("atom:summary", default="", namespaces=ATOM)).strip(),
    }
    cached.write_text(json.dumps(metadata, ensure_ascii=False, indent=1), encoding="utf-8")
    return metadata


def _surname(name: str) -> str:
    return name.split()[-1] if name.split() else name


def _initials(name: str) -> str:
    return " ".join(f"{part[0]}." for part in name.split()[:-1] if part)


def format_authors(authors: list[str]) -> tuple[str, str]:
    """(citation form, in-text form): "Lewis, P. et al." / "Lewis et al."."""
    if not authors:
        return "Anonymous", "Anonymous"
    first = f"{_surname(authors[0])}, {_initials(authors[0])}".rstrip(", ")
    if len(authors) == 1:
        return first, _surname(authors[0])
    if len(authors) == 2:
        second = f"{_surname(authors[1])}, {_initials(authors[1])}".rstrip(", ")
        return f"{first} & {second}", f"{_surname(authors[0])} & {_surname(authors[1])}"
    return f"{first} et al.", f"{_surname(authors[0])} et al."


def resolve(entry: dict, cache_directory: Path = CACHE_DIRECTORY) -> Source:
    """Turn a package-config source entry into a verified Source."""
    if "arxiv" in entry:
        arxiv_id = str(entry["arxiv"])
        metadata = _fetch_arxiv(arxiv_id, cache_directory)
        expected = entry.get("expect")
        if not expected:
            raise SourceError(f"arXiv:{arxiv_id}: an 'expect' title fragment is required.")
        if expected.casefold() not in metadata["title"].casefold():
            raise SourceError(
                f"arXiv:{arxiv_id} is {metadata['title']!r}, which does not contain {expected!r}."
            )
        authors, short_authors = format_authors(metadata["authors"])
        year = str(entry.get("year", metadata["year"]))
        venue = f" {entry['venue']}." if entry.get("venue") else ""
        url = f"https://arxiv.org/abs/{arxiv_id}"
        title = metadata["title"].rstrip(".")
        title += "" if title.endswith(("?", "!")) else "."
        return Source(
            url=url,
            citation=f"{authors} ({year}). *{title}*{venue} [arXiv:{arxiv_id}]({url})",
            short=f"{short_authors} ({year})",
            summary=metadata["summary"],
        )
    for key in ("url", "citation", "short"):
        if not entry.get(key):
            raise SourceError(f"non-arXiv source needs '{key}': {entry}")
    return Source(
        url=entry["url"],
        citation=f"{entry['citation']} [{entry.get('link_label', 'Link')}]({entry['url']})",
        short=entry["short"],
        summary=entry.get("summary", ""),
    )
