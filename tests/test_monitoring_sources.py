import gzip
import json
from datetime import date, datetime, timezone

import pytest

from app.agents.monitoring.config import ConfigError, load_sources_config
from app.agents.monitoring.feeds import (
    ArxivQuery,
    arxiv_query_url,
    decode_body,
    parse_arxiv,
    parse_feed,
)
from app.agents.monitoring.findings import Finding, SeenStore
from app.agents.monitoring.run_sources import collect_findings

NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)

ARXIV_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2610.01234v2</id>
    <published>2026-10-08T17:59:00Z</published>
    <updated>2026-10-09T10:00:00Z</updated>
    <title>Graph-Based Retrieval
      for Long Documents</title>
    <summary>  We propose a retrieval method.  </summary>
    <author><name>Ada Lovelace</name></author>
    <author><name>Alan Turing</name></author>
    <arxiv:primary_category term="cs.CL"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2601.00001v1</id>
    <published>2026-01-02T00:00:00Z</published>
    <title>Old paper</title>
    <summary>Old.</summary>
    <author><name>Someone</name></author>
  </entry>
</feed>"""

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Lab blog</title>
  <item>
    <title>New model release</title>
    <link>https://example.org/post-1</link>
    <guid>post-1</guid>
    <pubDate>Thu, 08 Oct 2026 09:00:00 GMT</pubDate>
    <description>&lt;p&gt;We release a &lt;b&gt;new&lt;/b&gt; model.&lt;/p&gt;</description>
  </item>
  <item>
    <title>Old post</title>
    <link>https://example.org/post-0</link>
    <pubDate>Mon, 01 Jun 2026 09:00:00 GMT</pubDate>
  </item>
</channel></rss>"""

ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Blog</title>
  <entry>
    <title>Agents in practice</title>
    <link rel="alternate" href="https://example.org/agents"/>
    <id>tag:example.org,2026:agents</id>
    <updated>2026-10-09T08:00:00+02:00</updated>
    <summary>Notes on agents.</summary>
  </entry>
</feed>"""

RDF = """<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
  <item rdf:about="https://example.org/talk">
    <title>A talk</title>
    <link>https://example.org/talk</link>
    <dc:date>2026-10-07T10:00:00Z</dc:date>
  </item>
</rdf:RDF>"""

CONFIG = """
max_proposals_per_week: 10
arxiv:
  categories: [cs.CL, cs.IR]
  max_results_per_query: 20
  queries:
    - retrieval-augmented generation
    - knowledge graph
rss:
  - name: Lab blog
    url: https://example.org/feed.xml
    category: lab_blog
    source_kind: primary_research
  - name: Official journal
    url: https://example.org/oj.xml
    category: regulatory
    source_kind: primary_research
    include_keywords: [artificial intelligence, Daten]
  - name: Proceedings
    url: https://example.org/pmlr.xml
    category: conference
    source_kind: primary_research
    tier: peer_reviewed
"""


def write_config(tmp_path, text=CONFIG):
    path = tmp_path / "sources.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_config_is_loaded_with_defaults(tmp_path):
    config = load_sources_config(write_config(tmp_path))

    assert config.max_proposals_per_week == 10
    assert config.arxiv.queries == ["retrieval-augmented generation", "knowledge graph"]
    assert [feed.name for feed in config.rss] == ["Lab blog", "Official journal", "Proceedings"]
    assert config.rss[0].tier is None
    assert config.rss[1].include_keywords == ["artificial intelligence", "Daten"]


@pytest.mark.parametrize(
    "old, new, message",
    [
        ("category: lab_blog", "category: podcast", "category"),
        ("source_kind: primary_research", "source_kind: opinion", "source_kind"),
        ("tier: peer_reviewed", "tier: excellent", "tier"),
    ],
)
def test_config_rejects_unknown_values(tmp_path, old, new, message):
    with pytest.raises(ConfigError, match=message):
        load_sources_config(write_config(tmp_path, CONFIG.replace(old, new, 1)))


def test_arxiv_query_searches_title_and_abstract_within_categories():
    url = arxiv_query_url(ArxivQuery(phrase="knowledge graph", categories=["cs.CL", "cs.IR"], max_results=20))

    assert "search_query=" in url
    assert "%22knowledge+graph%22" in url
    assert "cat%3Acs.CL+OR+cat%3Acs.IR" in url
    assert "sortBy=submittedDate" in url and "max_results=20" in url


def test_arxiv_entries_become_preprint_findings_without_version():
    findings = parse_arxiv(ARXIV_ATOM, query="graph retrieval", fetched_at=NOW)

    assert findings[0].id == "arxiv:2610.01234"
    assert findings[0].url == "https://arxiv.org/abs/2610.01234"
    assert findings[0].title == "Graph-Based Retrieval for Long Documents"
    assert findings[0].summary == "We propose a retrieval method."
    assert findings[0].authors == ["Ada Lovelace", "Alan Turing"]
    assert findings[0].published == date(2026, 10, 8)
    assert (findings[0].tier, findings[0].source_kind) == ("preprint", "primary_research")
    assert findings[0].source == "arXiv"


@pytest.mark.parametrize("body", [RSS, ATOM, RDF])
def test_rss_atom_and_rdf_feeds_are_parsed(body):
    findings = parse_feed(body, feed_name="Feed", category="lab_blog", source_kind="primary_research", tier=None, fetched_at=NOW)

    assert findings and all(finding.url.startswith("https://example.org/") for finding in findings)
    assert all(finding.id.startswith("rss:") for finding in findings)
    assert findings[0].published is not None


def test_rss_descriptions_lose_their_html():
    finding = parse_feed(RSS, feed_name="Feed", category="lab_blog", source_kind="primary_research", tier=None, fetched_at=NOW)[0]

    assert finding.summary == "We release a new model."
    assert finding.published == date(2026, 10, 8)


def test_compressed_bodies_are_decoded():
    assert decode_body(gzip.compress(RSS.encode("utf-8"))) == RSS
    assert decode_body(RSS.encode("utf-8")) == RSS


def finding(identifier, published=date(2026, 10, 8), title="Title", source="Feed"):
    return Finding(
        id=identifier,
        source=source,
        category="lab_blog",
        url=f"https://example.org/{identifier}",
        title=title,
        summary="",
        published=published,
        authors=[],
        tier=None,
        source_kind="primary_research",
        fetched_at=NOW,
    )


def test_seen_store_remembers_findings_across_runs(tmp_path):
    store = SeenStore(tmp_path / "seen.json")
    store.add([finding("rss:a")], NOW)
    store.add_sources(["Feed"])
    store.save()

    reloaded = SeenStore(tmp_path / "seen.json")

    assert reloaded.contains("rss:a") and not reloaded.contains("rss:b")
    assert reloaded.knows_source("Feed") and not reloaded.knows_source("Other")
    assert json.loads((tmp_path / "seen.json").read_text(encoding="utf-8")) == {
        "sources": ["Feed"],
        "findings": {"rss:a": "2026-10-10"},
    }


def test_collect_findings_filters_old_seen_duplicate_and_off_topic_items(tmp_path):
    config = load_sources_config(write_config(tmp_path))
    seen = SeenStore(tmp_path / "seen.json")
    seen.add([finding("rss:seen")], NOW)

    def fetch_arxiv(query):
        return [finding("arxiv:1", source="arXiv"), finding("arxiv:old", published=date(2026, 9, 1), source="arXiv")]

    def fetch_feed(feed):
        if feed.name == "Official journal":
            return [
                finding("rss:sanctions", title="Restrictive measures concerning Sudan", source=feed.name),
                finding("rss:ai", title="Regulation on Artificial Intelligence", source=feed.name),
            ]
        return [finding("rss:seen", source=feed.name), finding("rss:new", source=feed.name)]

    result = collect_findings(config, seen, since=date(2026, 10, 3), fetch_arxiv=fetch_arxiv, fetch_feed=fetch_feed)

    assert sorted(f.id for f in result.findings) == ["arxiv:1", "rss:ai", "rss:new"]
    assert result.errors == []


def test_collect_findings_reports_failing_sources_and_continues(tmp_path):
    config = load_sources_config(write_config(tmp_path))

    def fetch_feed(feed):
        if feed.name == "Lab blog":
            raise OSError("timeout")
        return []

    result = collect_findings(
        config, SeenStore(tmp_path / "seen.json"), since=date(2026, 10, 3), fetch_arxiv=lambda query: [], fetch_feed=fetch_feed
    )

    assert result.findings == []
    assert result.errors == ["Lab blog: timeout"]


def test_keywords_match_whole_words_or_marked_word_starts(tmp_path):
    config = load_sources_config(write_config(tmp_path, CONFIG.replace("[artificial intelligence, Daten]", "[AI, Daten*]")))

    def fetch_feed(feed):
        if feed.name != "Official journal":
            return []
        return [
            finding("rss:maintain", title="Rules to maintain stocks", source=feed.name),
            finding("rss:ai", title="Rules for AI systems", source=feed.name),
            finding("rss:daten", title="Gesetz zum Datenschutz", source=feed.name),
        ]

    result = collect_findings(
        config, SeenStore(tmp_path / "seen.json"), since=date(2026, 10, 3), fetch_arxiv=lambda query: [], fetch_feed=fetch_feed
    )

    assert sorted(f.id for f in result.findings) == ["rss:ai", "rss:daten"]


def test_undated_items_of_a_new_feed_become_the_baseline(tmp_path):
    config = load_sources_config(write_config(tmp_path))
    seen = SeenStore(tmp_path / "seen.json")

    def fetch_feed(feed):
        if feed.name == "Proceedings":
            return [finding("rss:volume-1", published=None, source=feed.name)]
        return []

    first = collect_findings(config, seen, since=date(2026, 10, 3), fetch_arxiv=lambda query: [], fetch_feed=fetch_feed)
    seen.add(first.baseline, NOW)
    seen.add_sources(first.fetched_sources)

    def fetch_feed_later(feed):
        if feed.name == "Proceedings":
            return [finding("rss:volume-1", published=None, source=feed.name), finding("rss:volume-2", published=None, source=feed.name)]
        return []

    second = collect_findings(config, seen, since=date(2026, 10, 3), fetch_arxiv=lambda query: [], fetch_feed=fetch_feed_later)

    assert first.findings == [] and [f.id for f in first.baseline] == ["rss:volume-1"]
    assert "Proceedings" in first.fetched_sources
    assert [f.id for f in second.findings] == ["rss:volume-2"]
