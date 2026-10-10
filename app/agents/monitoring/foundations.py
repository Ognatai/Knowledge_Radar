"""Foundational sources for a new topic: the most cited works on it.

The findings that trigger a new-topic proposal are this week's papers, usually
narrow; a reference article also needs the works that established the topic
(for prompt injection: Greshake et al., 2023). OpenAlex (open, no API key) is
searched for the topic in titles, within computer science, sorted by citations.
Where an arXiv version exists, it is looked up by title so that the curator can
read the full text.
"""

from __future__ import annotations

import json
import re
import urllib.parse
from collections.abc import Callable
from datetime import date, datetime

from app.agents.monitoring import feeds
from app.agents.monitoring.findings import Finding

OPENALEX_WORKS = "https://api.openalex.org/works"
COMPUTER_SCIENCE_FIELD = 17
MIN_CITATIONS = 20
SOURCE_NAME = "OpenAlex"


def openalex_query_url(topic: str, candidates: int = 10) -> str:
    phrase = topic.replace('"', "").replace(",", " ")
    parameters = {
        "filter": f'title.search:"{phrase}",primary_topic.field.id:{COMPUTER_SCIENCE_FIELD},has_abstract:true',
        "sort": "cited_by_count:desc",
        "per_page": candidates,
        "select": "id,title,publication_year,cited_by_count,doi,authorships,abstract_inverted_index",
    }
    return f"{OPENALEX_WORKS}?{urllib.parse.urlencode(parameters)}"


def abstract_text(inverted_index: dict[str, list[int]] | None) -> str:
    """OpenAlex stores abstracts as word -> positions."""
    if not inverted_index:
        return ""
    words: dict[int, str] = {}
    for word, positions in inverted_index.items():
        for position in positions:
            words[position] = word
    return " ".join(words[position] for position in sorted(words))


def _normalise_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.casefold())


def arxiv_id_for_title(
    title: str,
    year: int | None = None,
    fetch: Callable[[str], str] = feeds.fetch,
) -> str | None:
    """The arXiv id of the paper with exactly this title and a matching year, if arXiv has
    it. The year guards generic titles: "Model compression" (Buciluǎ et al., 2006) is not
    the 2021 arXiv paper of the same name."""
    words = re.sub(r"[^\w\s-]", " ", title).split()
    query = urllib.parse.urlencode({"search_query": f'ti:"{" ".join(words)}"', "max_results": 5})
    for finding in feeds.parse_arxiv(fetch(f"{feeds.ARXIV_API}?{query}"), query=title, fetched_at=datetime.now()):
        if _normalise_title(finding.title) != _normalise_title(title):
            continue
        if year is not None and finding.published is not None and abs(finding.published.year - year) > 1:
            continue
        return finding.id.removeprefix("arxiv:")
    return None


def parse_works(body: str, limit: int, fetched_at: datetime) -> list[dict]:
    works = [w for w in json.loads(body).get("results", []) if (w.get("cited_by_count") or 0) >= MIN_CITATIONS]
    return [w for w in works if w.get("title") and w.get("abstract_inverted_index")][:limit]


def foundational_findings(
    topic: str,
    limit: int = 3,
    fetch: Callable[[str], str] = feeds.fetch,
    find_arxiv: Callable[[str, int | None], str | None] | None = None,
) -> list[Finding]:
    find_arxiv = find_arxiv or (lambda title, year: arxiv_id_for_title(title, year, fetch))
    fetched_at = datetime.now().astimezone()
    findings = []
    for work in parse_works(fetch(openalex_query_url(topic)), limit, fetched_at):
        title = re.sub(r"\s+", " ", work["title"]).strip()
        try:
            arxiv_id = find_arxiv(title, work.get("publication_year"))
        except Exception:  # arXiv unreachable: the abstract still serves
            arxiv_id = None
        year = work.get("publication_year")
        if arxiv_id:
            identifier, url = f"arxiv:{arxiv_id}", f"https://arxiv.org/abs/{arxiv_id}"
        else:
            identifier, url = f"openalex:{work['id'].rsplit('/', 1)[-1]}", work.get("doi") or work["id"]
        findings.append(
            Finding(
                id=identifier,
                source=SOURCE_NAME,
                category="foundation",
                url=url,
                title=title,
                summary=abstract_text(work.get("abstract_inverted_index")),
                published=date(year, 1, 1) if year else None,
                authors=[a["author"]["display_name"] for a in work.get("authorships", []) if a.get("author")],
                tier=None,
                source_kind="primary_research",
                fetched_at=fetched_at,
            )
        )
    return findings
