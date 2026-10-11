"""MCP server for the curated RSS/Atom feeds of `sources.yaml`.

Built on the official MCP Python SDK; the tools are read-only and reuse the
monitoring agents' feed parser, so an MCP client sees the same items, with the
same keyword filters, as the weekly run:

- `list_feeds`: the curated feeds, optionally of one category
- `get_feed_items`: recent items of one feed
- `search_feed_items`: recent items of all feeds that contain every search word

Run it over stdio, e.g. as an MCP server in Claude Desktop or Claude Code:

    python -m app.mcp.rss_server
"""

from __future__ import annotations

import time
from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from app.agents.monitoring import feeds
from app.agents.monitoring.config import FeedConfig, load_sources_config
from app.agents.monitoring.findings import Finding
from app.agents.monitoring.run_sources import _matches_any

CACHE_SECONDS = 600
MAX_LIMIT = 100


class FeedReader:
    """Fetches and filters the configured feeds; bodies are cached for a few minutes."""

    def __init__(
        self,
        feeds_config: list[FeedConfig],
        fetch_feed: Callable[[FeedConfig], list[Finding]] = feeds.fetch_feed,
        today: Callable[[], date] = date.today,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.feeds = {feed.name: feed for feed in feeds_config}
        self.fetch_feed = fetch_feed
        self.today = today
        self.clock = clock
        self._cache: dict[str, tuple[float, list[Finding]]] = {}

    def list_feeds(self, category: str | None = None) -> list[dict[str, Any]]:
        return [
            {"name": feed.name, "category": feed.category, "source_kind": feed.source_kind, "tier": feed.tier, "url": feed.url}
            for feed in self.feeds.values()
            if category is None or feed.category == category
        ]

    def _items(self, feed: FeedConfig) -> list[Finding]:
        cached = self._cache.get(feed.name)
        if cached and self.clock() - cached[0] < CACHE_SECONDS:
            return cached[1]
        items = [
            item
            for item in self.fetch_feed(feed)
            if (not feed.include_keywords or _matches_any(item, feed.include_keywords))
            and not _matches_any(item, feed.exclude_keywords)
        ]
        self._cache[feed.name] = (self.clock(), items)
        return items

    def _recent(self, items: list[Finding], days: int) -> list[Finding]:
        since = self.today() - timedelta(days=max(days, 0))
        recent = [item for item in items if item.published is None or item.published >= since]
        return sorted(recent, key=lambda item: item.published or date.min, reverse=True)

    def get_feed_items(self, feed: str, days: int = 7, limit: int = 20) -> list[dict[str, Any]]:
        if feed not in self.feeds:
            raise ValueError(f"Unknown feed {feed!r}; list_feeds names the configured feeds.")
        items = self._recent(self._items(self.feeds[feed]), days)
        return [item_json(item) for item in items[: _limit(limit)]]

    def search_feed_items(self, query: str, days: int = 14, category: str | None = None, limit: int = 20) -> dict[str, Any]:
        words = [word.casefold() for word in query.split()]
        if not words:
            raise ValueError("The query needs at least one word.")
        matches: list[Finding] = []
        errors: list[str] = []
        for feed in self.feeds.values():
            if category is not None and feed.category != category:
                continue
            try:
                items = self._items(feed)
            except Exception as exc:  # one unreachable feed must not fail the search
                errors.append(f"{feed.name}: {exc}")
                continue
            for item in self._recent(items, days):
                text = f"{item.title} {item.summary}".casefold()
                if all(word in text for word in words):
                    matches.append(item)
        matches.sort(key=lambda item: item.published or date.min, reverse=True)
        return {"items": [item_json(item) for item in matches[: _limit(limit)]], "errors": errors}


def _limit(limit: int) -> int:
    return min(max(limit, 1), MAX_LIMIT)


def item_json(item: Finding) -> dict[str, Any]:
    return {
        "feed": item.source,
        "title": item.title,
        "url": item.url,
        "published": item.published.isoformat() if item.published else None,
        "summary": item.summary,
        "category": item.category,
        "source_kind": item.source_kind,
        "tier": item.tier,
    }


READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)


def build_server(reader: FeedReader | None = None) -> MCPServer:
    reader = reader or FeedReader(load_sources_config().rss)
    server = MCPServer(
        name="knowledge-radar-rss",
        instructions=(
            "Curated RSS/Atom feeds on AI research, lab news, AI law and regulation. "
            "Call list_feeds first to see the feed names and categories."
        ),
    )

    @server.tool(annotations=READ_ONLY)
    def list_feeds(category: str | None = None) -> dict[str, Any]:
        """List the curated feeds. Categories: lab_blog, video, conference, newsletter, regulatory."""
        return {"feeds": reader.list_feeds(category)}

    @server.tool(annotations=READ_ONLY)
    def get_feed_items(feed: str, days: int = 7, limit: int = 20) -> dict[str, Any]:
        """Items of one feed (by its name from list_feeds) published in the last `days` days, newest first."""
        return {"items": reader.get_feed_items(feed, days, limit)}

    @server.tool(annotations=READ_ONLY)
    def search_feed_items(query: str, days: int = 14, category: str | None = None, limit: int = 20) -> dict[str, Any]:
        """Items of all feeds (or of one category) from the last `days` days whose title or summary
        contains every word of `query`, newest first; unreachable feeds are listed under errors."""
        return reader.search_feed_items(query, days, category, limit)

    return server


def main() -> None:
    build_server().run("stdio")


if __name__ == "__main__":
    main()
