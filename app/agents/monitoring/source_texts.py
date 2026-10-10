"""Source texts for the curator: full text where available, else the abstract.

arXiv papers are read from their HTML version (arxiv.org/html/<id>, LaTeXML):
the article body without bibliography and appendix, formulas as their LaTeX
`alttext`. Other findings and papers without an HTML version fall back to the
summary the source agent stored. Texts are cached under
`.knowledge-radar/cache/fulltext/`.

The text comes from outside and goes into prompts; prompts mark it as data, and
the faithfulness gate plus the review catch text that does not belong.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from app.agents.monitoring import feeds
from app.agents.monitoring.findings import Finding
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

CACHE_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "cache" / "fulltext"
ARXIV_HTML = "https://arxiv.org/html/{id}"
MAX_CHARACTERS = 60_000
PASSAGE_CHARACTERS = 1200
SKIPPED_CLASSES = ("ltx_bibliography", "ltx_appendix", "ltx_authors", "ltx_page_logo", "ltx_role_footnote")
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK_TAGS = {"p", "div", "section", "h1", "h2", "h3", "h4", "h5", "li", "tr", "figcaption", "table"}


@dataclass(frozen=True)
class SourceText:
    finding_id: str
    url: str
    short: str  # in-text citation, e.g. "Doe et al. (2026)"
    title: str
    text: str
    full_text: bool


class _ArticleText(HTMLParser):
    """Text of the LaTeXML <article>, without skipped sections and MathML internals."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.in_article = 0
        self.skip_depth = 0
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in VOID_TAGS:
            if self.in_article and not self.skip_depth and tag == "br":
                self.parts.append("\n")
            return
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        self.depth += 1
        if tag == "article" and "ltx_document" in classes:
            self.in_article = self.depth
        if not self.in_article:
            return
        if self.skip_depth:
            return
        if any(name in classes for name in SKIPPED_CLASSES):
            self.skip_depth = self.depth
            return
        if tag == "math":
            self.parts.append(f" {attributes.get('alttext') or ''} ")
            self.skip_depth = self.depth
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if self.skip_depth == self.depth:
            self.skip_depth = 0
        if self.in_article == self.depth:
            self.in_article = 0
        self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.in_article and not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\s*\n\s*", "\n", text)
        return re.sub(r"\n{2,}", "\n", text).strip()


def arxiv_article_text(html: str) -> str:
    parser = _ArticleText()
    parser.feed(html)
    return parser.text()


def short_citation(finding: Finding) -> str:
    year = finding.published.year if finding.published else ""
    if not finding.authors:
        return f"{finding.source} ({year})"
    surname = finding.authors[0].split()[-1]
    if len(finding.authors) == 1:
        return f"{surname} ({year})"
    if len(finding.authors) == 2:
        return f"{surname} & {finding.authors[1].split()[-1]} ({year})"
    return f"{surname} et al. ({year})"


def source_text(finding: Finding, fetch=feeds.fetch, cache_directory: Path = CACHE_DIRECTORY) -> SourceText:
    text, full = "", False
    if finding.id.startswith("arxiv:"):
        arxiv_id = finding.id.removeprefix("arxiv:")
        cache = cache_directory / f"{arxiv_id.replace('/', '_')}.txt"
        if cache.is_file():
            text = cache.read_text(encoding="utf-8")
        else:
            try:
                text = arxiv_article_text(fetch(ARXIV_HTML.format(id=arxiv_id)))
            except Exception:  # no HTML version, or network trouble: fall back to the abstract
                text = ""
            if text:
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(text, encoding="utf-8")
        full = bool(text)
    if not text:
        text = finding.summary
    return SourceText(
        finding_id=finding.id,
        url=finding.url,
        short=short_citation(finding),
        title=finding.title,
        text=text[:MAX_CHARACTERS],
        full_text=full,
    )


def passages(source: SourceText, size: int = PASSAGE_CHARACTERS) -> list[str]:
    """Paragraph-aligned passages of about `size` characters, each prefixed with its source."""
    chunks: list[str] = []
    current = ""
    for paragraph in source.text.split("\n"):
        if current and len(current) + len(paragraph) > size:
            chunks.append(current)
            current = ""
        current = f"{current}\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return [f"[{source.short}] {chunk}" for chunk in chunks]
