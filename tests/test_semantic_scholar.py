import io
import json
import urllib.error
import urllib.parse
from datetime import date, datetime, timezone

import pytest

from app.agents.monitoring import semantic_scholar
from app.agents.monitoring.config import load_sources_config
from app.agents.monitoring.findings import SeenStore
from app.agents.monitoring.run_sources import collect_findings
from app.agents.monitoring.semantic_scholar import ScholarQuery, fetch_with_retry, parse_results, search_url
from tests.test_monitoring_sources import CONFIG, finding, write_config

NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
BODY = json.dumps(
    {
        "total": 2,
        "data": [
            {
                "paperId": "abc",
                "title": "Retrieval for  Long Documents",
                "abstract": "We propose <b>a</b> method.",
                "venue": "Annual Meeting of the Association for Computational Linguistics",
                "publicationDate": "2026-07-01",
                "year": 2026,
                "authors": [{"name": "Ada Lovelace"}],
                "externalIds": {"ArXiv": "2603.01234", "DOI": "10.18653/v1/x"},
                "url": "https://www.semanticscholar.org/paper/abc",
            },
            {
                "paperId": "def",
                "title": "A Journal Paper",
                "abstract": None,
                "venue": "Trans. Mach. Learn. Res.",
                "publicationDate": None,
                "year": 2026,
                "authors": [],
                "externalIds": {},
                "url": "https://www.semanticscholar.org/paper/def",
            },
        ],
    }
)


def test_search_url_restricts_to_venues_and_date():
    query = ScholarQuery('"prompt injection"', ["ACL", "TACL"], date(2026, 8, 1), 25)

    parameters = urllib.parse.parse_qs(urllib.parse.urlparse(search_url(query)).query)

    assert parameters["query"] == ['"prompt injection"']
    assert parameters["venue"] == ["ACL,TACL"]
    assert parameters["publicationDateOrYear"] == ["2026-08-01:"]
    assert parameters["sort"] == ["publicationDate:desc"]


def test_papers_become_peer_reviewed_findings_with_their_arxiv_id():
    papers = parse_results(BODY, query="retrieval", max_results=25, fetched_at=NOW)

    first, second = papers
    assert (first.id, first.url, first.tier, first.source) == (
        "arxiv:2603.01234",
        "https://doi.org/10.18653/v1/x",
        "peer_reviewed",
        "Semantic Scholar",
    )
    assert first.title == "Retrieval for Long Documents" and first.summary == "We propose a method."
    assert first.published == date(2026, 7, 1) and first.authors == ["Ada Lovelace"]
    assert (second.id, second.url, second.published, second.summary) == (
        "s2:def",
        "https://www.semanticscholar.org/paper/def",
        date(2026, 1, 1),
        "",
    )
    assert len(parse_results(BODY, query="retrieval", max_results=1, fetched_at=NOW)) == 1


def test_busy_responses_are_retried_after_a_wait():
    calls, waits = [], []

    def fetch(url):
        calls.append(url)
        if len(calls) < 3:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, io.BytesIO(b""))
        return "ok"

    assert fetch_with_retry("u", fetch, sleep=waits.append) == "ok"
    assert len(calls) == 3 and waits[1:] == [5, 15]


def test_other_errors_are_not_retried():
    def fetch(url):
        raise urllib.error.HTTPError(url, 400, "Bad Request", {}, io.BytesIO(b""))

    with pytest.raises(urllib.error.HTTPError):
        fetch_with_retry("u", fetch, sleep=lambda seconds: None)


SCHOLAR_CONFIG = CONFIG + """
semantic_scholar:
  lookback_days: 60
  venues: [ACL]
"""


def test_semantic_scholar_looks_back_further_and_wins_over_arxiv(tmp_path):
    config = load_sources_config(write_config(tmp_path, SCHOLAR_CONFIG))
    queries = []

    def fetch_scholar(query):
        queries.append(query)
        old = finding("arxiv:7", published=date(2026, 8, 20), source="Semantic Scholar")
        return [old, finding("s2:too-old", published=date(2026, 7, 1), source="Semantic Scholar")]

    def fetch_arxiv(query):
        return [finding("arxiv:7", source="arXiv")]

    result = collect_findings(
        config,
        SeenStore(tmp_path / "seen.json"),
        since=date(2026, 10, 3),
        today=date(2026, 10, 10),
        fetch_arxiv=fetch_arxiv,
        fetch_feed=lambda feed: [],
        fetch_scholar=fetch_scholar,
    )

    assert queries[0].since == date(2026, 8, 11) and queries[0].venues == ["ACL"]
    assert [(f.id, f.source) for f in result.findings] == [("arxiv:7", "Semantic Scholar")]


def test_without_venues_semantic_scholar_is_not_asked(tmp_path):
    def fetch_scholar(query):
        raise AssertionError("must not be called")

    collect_findings(
        load_sources_config(write_config(tmp_path)),
        SeenStore(tmp_path / "seen.json"),
        since=date(2026, 10, 3),
        fetch_arxiv=lambda query: [],
        fetch_feed=lambda feed: [],
        fetch_scholar=fetch_scholar,
    )
