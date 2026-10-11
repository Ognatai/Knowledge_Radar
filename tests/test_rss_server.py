import asyncio
import json
from datetime import date

import pytest

from app.agents.monitoring.config import FeedConfig
from app.mcp.rss_server import FeedReader, build_server
from tests.test_monitoring_sources import finding

FEEDS = [
    FeedConfig(name="Lab", url="u1", category="lab_blog", source_kind="primary_research"),
    FeedConfig(name="Journal", url="u2", category="regulatory", source_kind="primary_research", include_keywords=["AI"]),
]
ITEMS = {
    "Lab": [
        finding("rss:new", published=date(2026, 10, 9), title="Agents with memory", source="Lab"),
        finding("rss:old", published=date(2026, 9, 1), title="Agents in 2025", source="Lab"),
    ],
    "Journal": [
        finding("rss:ai", published=date(2026, 10, 8), title="Regulation on AI agents", source="Journal"),
        finding("rss:fish", published=date(2026, 10, 8), title="Fishing quotas", source="Journal"),
    ],
}


def reader(fetch=None, clock=lambda: 0.0):
    calls = []

    def fetch_feed(feed):
        calls.append(feed.name)
        return ITEMS[feed.name]

    return FeedReader(FEEDS, fetch or fetch_feed, today=lambda: date(2026, 10, 10), clock=clock), calls


def test_feeds_are_listed_with_their_category():
    feeds, _ = reader()

    assert [f["name"] for f in feeds.list_feeds()] == ["Lab", "Journal"]
    assert [f["name"] for f in feeds.list_feeds("regulatory")] == ["Journal"]


def test_feed_items_are_recent_filtered_and_newest_first():
    feeds, _ = reader()

    assert [i["title"] for i in feeds.get_feed_items("Lab", days=7)] == ["Agents with memory"]
    assert [i["title"] for i in feeds.get_feed_items("Journal", days=7)] == ["Regulation on AI agents"]
    with pytest.raises(ValueError, match="Unknown feed"):
        feeds.get_feed_items("Nope")


def test_search_needs_every_word_and_reports_unreachable_feeds():
    def fetch(feed):
        if feed.name == "Journal":
            raise OSError("timeout")
        return ITEMS[feed.name]

    feeds, _ = reader(fetch)
    result = feeds.search_feed_items("agents MEMORY", days=7)

    assert [i["title"] for i in result["items"]] == ["Agents with memory"]
    assert result["errors"] == ["Journal: timeout"]


def test_feeds_are_cached_for_a_few_minutes():
    now = [0.0]
    feeds, calls = reader(clock=lambda: now[0])

    feeds.get_feed_items("Lab")
    feeds.get_feed_items("Lab")
    now[0] = 601.0
    feeds.get_feed_items("Lab")

    assert calls == ["Lab", "Lab"]


def test_the_server_offers_three_read_only_tools():
    feeds, _ = reader()
    server = build_server(feeds)

    tools = asyncio.run(server.list_tools())

    assert sorted(t.name for t in tools) == ["get_feed_items", "list_feeds", "search_feed_items"]
    assert all(t.annotations.read_only_hint for t in tools)


def test_a_tool_call_returns_the_items():
    feeds, _ = reader()
    server = build_server(feeds)

    result = asyncio.run(server.call_tool("get_feed_items", {"feed": "Lab", "days": 7}))

    (block,) = result.content
    assert [item["title"] for item in json.loads(block.text)["items"]] == ["Agents with memory"]
