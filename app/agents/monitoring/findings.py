"""Findings: items the source agents fetched, before the relevance agent sees them.

Every source (arXiv, RSS, later OpenReview, Semantic Scholar, YouTube) produces the
same `Finding`. The `SeenStore` remembers which findings earlier runs already
handed on, so a weekly run only passes on what is new.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path

from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

STATE_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "monitoring"
SEEN_PATH = STATE_DIRECTORY / "seen.json"
RUNS_DIRECTORY = STATE_DIRECTORY / "runs"

# source_kind and tier are orthogonal (architecture document, "Source Diversity").
SOURCE_KINDS = frozenset({"primary_research", "secondary_commentary"})
TIERS = frozenset({"peer_reviewed", "preprint"})


@dataclass(frozen=True)
class Finding:
    # Stable across runs: "arxiv:<id without version>" or "rss:<hash of guid or link>".
    id: str
    source: str  # the arXiv API or the name of a curated feed
    category: str  # arxiv | conference | newsletter | regulatory | lab_blog
    url: str
    title: str
    summary: str
    published: date | None
    authors: list[str]
    tier: str | None
    source_kind: str
    fetched_at: datetime
    query: str | None = None  # the arXiv search phrase that found it

    def to_json(self) -> dict:
        data = asdict(self)
        data["published"] = self.published.isoformat() if self.published else None
        data["fetched_at"] = self.fetched_at.isoformat()
        return data


class SeenStore:
    """Finding ids already handed on, with the date they were first seen, and the
    sources fetched at least once (see `collect_findings` on undated items)."""

    def __init__(self, path: Path = SEEN_PATH) -> None:
        self.path = path
        self._seen: dict[str, str] = {}
        self._sources: set[str] = set()
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            self._seen = data.get("findings", {})
            self._sources = set(data.get("sources", []))

    def knows_source(self, name: str) -> bool:
        return name in self._sources

    def add_sources(self, names: list[str]) -> None:
        self._sources.update(names)

    def contains(self, finding_id: str) -> bool:
        return finding_id in self._seen

    def add(self, findings: list[Finding], when: datetime) -> None:
        for finding in findings:
            self._seen.setdefault(finding.id, when.date().isoformat())

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"sources": sorted(self._sources), "findings": dict(sorted(self._seen.items()))}
        self.path.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")


def write_run(findings: list[Finding], when: datetime, directory: Path = RUNS_DIRECTORY) -> Path:
    """One JSON object per line, the input of the relevance agent."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"findings-{when:%Y-%m-%d_%H%M%S}.jsonl"
    path.write_text(
        "".join(json.dumps(finding.to_json(), ensure_ascii=False) + "\n" for finding in findings),
        encoding="utf-8",
    )
    return path
