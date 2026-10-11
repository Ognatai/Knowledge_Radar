"""Source agent for Semantic Scholar: peer-reviewed papers from curated venues.

The arXiv search phrases from `sources.yaml` are searched in Semantic Scholar's
bulk search, restricted to an allowlist of venues (NeurIPS, ICLR, ACL, SIGIR,
TMLR, ...): without it, most results came from little-known journals. This also
covers the accepted papers of the OpenReview venues, whose API now requires a
login.

Semantic Scholar indexes conference papers weeks after they appear, so the search
looks back further than the weekly run (`lookback_days`); `seen.json` keeps
findings from repeating. A paper with an arXiv version gets its arXiv id, so it
is not proposed twice and the curator can read the full text.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime

from app.agents.monitoring import feeds
from app.agents.monitoring.findings import Finding

BULK_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,abstract,venue,publicationDate,year,authors,externalIds,url"
SOURCE_NAME = "Semantic Scholar"
REQUEST_SPACING_SECONDS = 1.5
# The unauthenticated pool is shared by all users and answers 429 when busy.
RETRY_WAITS_SECONDS = (5, 15, 30)
_last_request = 0.0


@dataclass(frozen=True)
class ScholarQuery:
    phrase: str
    venues: list[str]
    since: date
    max_results: int


def search_url(query: ScholarQuery) -> str:
    parameters = {
        # Quoted: unquoted, the words match separately ("model context protocol" found
        # papers on federated recommendation).
        "query": '"' + query.phrase.replace('"', "") + '"',
        "venue": ",".join(query.venues),
        "publicationDateOrYear": f"{query.since.isoformat()}:",
        "sort": "publicationDate:desc",
        "fields": FIELDS,
    }
    return f"{BULK_SEARCH}?{urllib.parse.urlencode(parameters)}"


def parse_results(body: str, *, query: str, max_results: int, fetched_at: datetime) -> list[Finding]:
    findings = []
    for paper in json.loads(body).get("data") or []:
        title = feeds._clean(paper.get("title"))
        if not title:
            continue
        ids = paper.get("externalIds") or {}
        arxiv_id = ids.get("ArXiv")
        doi = ids.get("DOI")
        if arxiv_id:
            identifier = f"arxiv:{arxiv_id}"
        else:
            identifier = f"s2:{paper.get('paperId')}"
        url = f"https://doi.org/{doi}" if doi else paper.get("url") or f"https://arxiv.org/abs/{arxiv_id}"
        published = feeds._date(paper.get("publicationDate")) or (date(paper["year"], 1, 1) if paper.get("year") else None)
        findings.append(
            Finding(
                id=identifier,
                source=SOURCE_NAME,
                category="conference",
                url=url,
                title=title,
                summary=feeds._clean(paper.get("abstract")),
                published=published,
                authors=[feeds._clean(author.get("name")) for author in paper.get("authors") or []],
                tier="peer_reviewed",
                source_kind="primary_research",
                fetched_at=fetched_at,
                query=query,
            )
        )
        if len(findings) == max_results:
            break
    return findings


def fetch_with_retry(
    url: str,
    fetch: Callable[[str], str] = feeds.fetch,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    global _last_request
    for attempt, wait in enumerate((0, *RETRY_WAITS_SECONDS)):
        sleep(max(wait, REQUEST_SPACING_SECONDS - (time.monotonic() - _last_request)))
        _last_request = time.monotonic()
        try:
            return fetch(url)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == len(RETRY_WAITS_SECONDS):
                raise
    raise AssertionError("unreachable")


def fetch_papers(query: ScholarQuery, fetch: Callable[[str], str] = feeds.fetch) -> list[Finding]:
    body = fetch_with_retry(search_url(query), fetch)
    return parse_results(body, query=query.phrase, max_results=query.max_results, fetched_at=datetime.now().astimezone())
