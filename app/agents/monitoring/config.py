"""The curated source list `sources.yaml`: arXiv search phrases and RSS feeds."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from app.agents.monitoring.findings import SOURCE_KINDS, TIERS
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

SOURCES_PATH = REPOSITORY_ROOT / "sources.yaml"
FEED_CATEGORIES = frozenset({"conference", "newsletter", "regulatory", "lab_blog"})


class ConfigError(ValueError):
    """Raised when sources.yaml is malformed."""


@dataclass(frozen=True)
class ArxivConfig:
    categories: list[str]
    queries: list[str]
    max_results_per_query: int = 25


@dataclass(frozen=True)
class FeedConfig:
    name: str
    url: str
    category: str
    source_kind: str
    tier: str | None = None
    # For broad feeds (official journals): keep only items whose title or
    # summary contains one of these, case-insensitively.
    include_keywords: list[str] = field(default_factory=list)
    # Items whose title or summary contains one of these are dropped (e.g. corrigenda).
    exclude_keywords: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SourcesConfig:
    max_proposals_per_week: int
    arxiv: ArxivConfig
    rss: list[FeedConfig]
    # Hugging Face Daily Papers: the most upvoted papers per day, found without
    # search phrases; 0 disables the source.
    daily_papers_top_per_day: int = 0


def _choice(value: object, allowed: frozenset[str], key: str, where: str, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if value not in allowed:
        raise ConfigError(f"{where}: {key} must be one of {', '.join(sorted(allowed))}, not {value!r}.")
    return str(value)


def _strings(value: object, key: str, where: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ConfigError(f"{where}: {key} must be a list of non-empty strings.")
    return [item.strip() for item in value]


def load_sources_config(path: Path = SOURCES_PATH) -> SourcesConfig:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"{path}: could not read: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: must be a YAML mapping.")

    arxiv_raw = raw.get("arxiv") or {}
    arxiv = ArxivConfig(
        categories=_strings(arxiv_raw.get("categories"), "arxiv.categories", str(path)),
        queries=_strings(arxiv_raw.get("queries"), "arxiv.queries", str(path)),
        max_results_per_query=int(arxiv_raw.get("max_results_per_query", 25)),
    )

    feeds: list[FeedConfig] = []
    for index, entry in enumerate(raw.get("rss") or []):
        where = f"{path}: rss[{index}]"
        if not isinstance(entry, dict) or not entry.get("name") or not entry.get("url"):
            raise ConfigError(f"{where}: each feed needs a name and a url.")
        feeds.append(
            FeedConfig(
                name=str(entry["name"]),
                url=str(entry["url"]),
                category=_choice(entry.get("category"), FEED_CATEGORIES, "category", where),
                source_kind=_choice(entry.get("source_kind"), SOURCE_KINDS, "source_kind", where),
                tier=_choice(entry.get("tier"), TIERS, "tier", where, optional=True),
                include_keywords=_strings(entry.get("include_keywords"), "include_keywords", where),
                exclude_keywords=_strings(entry.get("exclude_keywords"), "exclude_keywords", where),
            )
        )
    names = [feed.name for feed in feeds]
    if len(names) != len(set(names)):
        raise ConfigError(f"{path}: feed names must be unique.")

    return SourcesConfig(
        max_proposals_per_week=int(raw.get("max_proposals_per_week", 10)),
        arxiv=arxiv,
        rss=feeds,
        daily_papers_top_per_day=int((raw.get("huggingface_daily_papers") or {}).get("top_per_day", 0)),
    )
