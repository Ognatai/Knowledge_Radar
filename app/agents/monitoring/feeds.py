"""Source agents for arXiv and RSS/Atom feeds: pure fetching and parsing, no LLM.

arXiv is searched with the curated phrases from `sources.yaml` (title or abstract,
within the configured categories), spaced as arXiv's API guidelines ask. Feeds may
be RSS 2.0, Atom or RSS 1.0 (RDF). XML is parsed with defusedxml, since feed
content comes from outside.
"""

from __future__ import annotations

import gzip
import hashlib
import html
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from xml.etree.ElementTree import Element

from defusedxml.ElementTree import fromstring

from app.agents.monitoring.config import FeedConfig
from app.agents.monitoring.findings import Finding

ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_REQUEST_SPACING_SECONDS = 3.0
USER_AGENT = "KnowledgeRadar/0.1 (+https://github.com/Ognatai/Knowledge_Radar)"
MAX_SUMMARY_CHARACTERS = 2000
ATOM = "{http://www.w3.org/2005/Atom}"
RSS1 = "{http://purl.org/rss/1.0/}"
DC = "{http://purl.org/dc/elements/1.1/}"
RDF = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
ARXIV_ID = re.compile(r"arxiv\.org/abs/(.+?)(?:v\d+)?$")
_last_arxiv_request = 0.0


@dataclass(frozen=True)
class ArxivQuery:
    phrase: str
    categories: list[str]
    max_results: int


def decode_body(body: bytes) -> str:
    """Some servers send gzip even when it was not requested."""
    if body[:2] == b"\x1f\x8b":
        body = gzip.decompress(body)
    return body.decode("utf-8", errors="replace")


def fetch(url: str, timeout: float = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return decode_body(response.read())


def _clean(text: str | None) -> str:
    """Plain text from a feed field that may contain (escaped) HTML."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text[:MAX_SUMMARY_CHARACTERS]


def _date(text: str | None) -> date | None:
    if not text:
        return None
    text = text.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    try:
        return parsedate_to_datetime(text).date()
    except (TypeError, ValueError):
        return None


def arxiv_query_url(query: ArxivQuery) -> str:
    phrase = query.phrase.replace('"', "")
    search = f'(ti:"{phrase}" OR abs:"{phrase}")'
    if query.categories:
        search += " AND (" + " OR ".join(f"cat:{category}" for category in query.categories) + ")"
    parameters = {
        "search_query": search,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": query.max_results,
    }
    return f"{ARXIV_API}?{urllib.parse.urlencode(parameters)}"


def parse_arxiv(body: str, *, query: str, fetched_at: datetime) -> list[Finding]:
    findings = []
    for entry in fromstring(body).iter(f"{ATOM}entry"):
        match = ARXIV_ID.search((entry.findtext(f"{ATOM}id") or "").strip())
        if not match:
            continue
        arxiv_id = match.group(1)
        findings.append(
            Finding(
                id=f"arxiv:{arxiv_id}",
                source="arXiv",
                category="arxiv",
                url=f"https://arxiv.org/abs/{arxiv_id}",
                title=_clean(entry.findtext(f"{ATOM}title")),
                summary=_clean(entry.findtext(f"{ATOM}summary")),
                published=_date(entry.findtext(f"{ATOM}published")),
                authors=[_clean(author.findtext(f"{ATOM}name")) for author in entry.iter(f"{ATOM}author")],
                tier="preprint",
                source_kind="primary_research",
                fetched_at=fetched_at,
                query=query,
            )
        )
    return findings


def fetch_arxiv(query: ArxivQuery) -> list[Finding]:
    global _last_arxiv_request
    wait = ARXIV_REQUEST_SPACING_SECONDS - (time.monotonic() - _last_arxiv_request)
    if wait > 0:
        time.sleep(wait)
    try:
        body = fetch(arxiv_query_url(query), timeout=60)
    finally:
        _last_arxiv_request = time.monotonic()
    return parse_arxiv(body, query=query.phrase, fetched_at=datetime.now().astimezone())


def _atom_link(entry: Element) -> str:
    for link in entry.iter(f"{ATOM}link"):
        if link.get("rel", "alternate") == "alternate" and link.get("href"):
            return link.get("href", "")
    return ""


def _items(root: Element) -> list[dict[str, str | None]]:
    """Title, link, guid, date and summary of every item, whatever the feed format."""
    items: list[dict[str, str | None]] = []
    for item in root.iter("item"):  # RSS 2.0
        items.append(
            {
                "title": item.findtext("title"),
                "link": item.findtext("link"),
                "guid": item.findtext("guid"),
                "date": item.findtext("pubDate") or item.findtext(f"{DC}date"),
                "summary": item.findtext("description"),
            }
        )
    for entry in root.iter(f"{ATOM}entry"):
        items.append(
            {
                "title": entry.findtext(f"{ATOM}title"),
                "link": _atom_link(entry),
                "guid": entry.findtext(f"{ATOM}id"),
                "date": entry.findtext(f"{ATOM}published") or entry.findtext(f"{ATOM}updated"),
                "summary": entry.findtext(f"{ATOM}summary") or entry.findtext(f"{ATOM}content"),
            }
        )
    for item in root.iter(f"{RSS1}item"):  # RSS 1.0 (RDF)
        items.append(
            {
                "title": item.findtext(f"{RSS1}title"),
                "link": item.findtext(f"{RSS1}link") or item.get(f"{RDF}about"),
                "guid": item.get(f"{RDF}about"),
                "date": item.findtext(f"{DC}date"),
                "summary": item.findtext(f"{RSS1}description"),
            }
        )
    return items


def parse_feed(
    body: str,
    *,
    feed_name: str,
    category: str,
    source_kind: str,
    tier: str | None,
    fetched_at: datetime,
) -> list[Finding]:
    findings = []
    for item in _items(fromstring(body)):
        link = (item["link"] or "").strip()
        key = (item["guid"] or link).strip()
        if not link or not key:
            continue
        findings.append(
            Finding(
                id="rss:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16],
                source=feed_name,
                category=category,
                url=link,
                title=_clean(item["title"]),
                summary=_clean(item["summary"]),
                published=_date(item["date"]),
                authors=[],
                tier=tier,
                source_kind=source_kind,
                fetched_at=fetched_at,
            )
        )
    return findings


def fetch_feed(feed: FeedConfig) -> list[Finding]:
    return parse_feed(
        fetch(feed.url),
        feed_name=feed.name,
        category=feed.category,
        source_kind=feed.source_kind,
        tier=feed.tier,
        fetched_at=datetime.now().astimezone(),
    )
