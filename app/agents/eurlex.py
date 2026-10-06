"""Fetch EUR-Lex documents and split them into articles.

EUR-Lex answers plain HTTP clients with an empty bot-protection response, so
documents are rendered with a local headless Chromium-based browser (Edge or
Chrome) and cached under `.knowledge-radar/cache/eurlex/`.
"""

from __future__ import annotations

import hashlib
import html
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from app.agents.legal_text import Heading, Section
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

CACHE_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "cache" / "eurlex"
WINDOWS_BROWSERS = [
    ("ProgramFiles(x86)", "Microsoft/Edge/Application/msedge.exe"),
    ("ProgramFiles", "Microsoft/Edge/Application/msedge.exe"),
    ("ProgramFiles", "Google/Chrome/Application/chrome.exe"),
]
BROWSER_COMMANDS = ["msedge", "google-chrome", "chromium", "chromium-browser"]
# Every structural unit (chapter, article, annex) starts a part; only articles are kept,
# so an article never runs into a following chapter title or annex.
ARTICLE_START = re.compile(r'(?=<div (?:class="eli-subdivision" )?id="(?:art|cpt|anx|enc|fnp)_)')
ARTICLE_ID = re.compile(r'<div class="eli-subdivision" id="art_([0-9a-z]+)"')
# Consolidation markers such as "▼M1", "►B" or "◄".
AMENDMENT_MARKER = re.compile("[\u25bc\u25ba\u25c4]\\s*(?:[A-Z]\\d*)?\\s*")


class EurLexError(RuntimeError):
    """Raised when a document cannot be fetched or contains no articles."""


def find_browser() -> str:
    configured = os.environ.get("KNOWLEDGE_RADAR_BROWSER")
    windows = [
        str(Path(os.environ[variable]) / relative)
        for variable, relative in WINDOWS_BROWSERS
        if os.environ.get(variable)
    ]
    for candidate in ([configured] if configured else []) + windows + BROWSER_COMMANDS:
        if Path(candidate).is_file() or shutil.which(candidate):
            return candidate
    raise EurLexError(
        "No Chromium-based browser found; set KNOWLEDGE_RADAR_BROWSER to Edge or Chrome."
    )


def fetch_html(url: str, cache_directory: Path = CACHE_DIRECTORY, refresh: bool = False) -> str:
    """Return the rendered HTML of a EUR-Lex page, from cache when available."""
    cache_directory.mkdir(parents=True, exist_ok=True)
    cached = cache_directory / f"{hashlib.sha256(url.encode()).hexdigest()[:16]}.html"
    if cached.is_file() and not refresh:
        return cached.read_text(encoding="utf-8")

    # The bot protection does not always let the first attempt through; retry with more time.
    page, returncode = "", 0
    for budget in (25000, 40000, 60000):
        with tempfile.TemporaryDirectory() as profile:
            result = subprocess.run(
                [
                    find_browser(), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
                    f"--virtual-time-budget={budget}", "--dump-dom", url,
                ],
                capture_output=True,
                timeout=240,
                check=False,
            )
        page, returncode = result.stdout.decode("utf-8", errors="replace"), result.returncode
        if "eli-subdivision" in page or "title-article-norm" in page:
            break
    else:
        raise EurLexError(f"No legal text received from {url} (browser exit code {returncode}).")
    cached.write_text(page, encoding="utf-8")
    return page


def html_to_text(fragment: str) -> str:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = AMENDMENT_MARKER.sub(" ", html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def split_articles(page: str) -> dict[str, str]:
    """Map article numbers ("5", "4a") to their plain text."""
    articles = {}
    for part in ARTICLE_START.split(page):
        match = ARTICLE_ID.match(part)
        if match:
            articles[match.group(1)] = html_to_text(part)
    if not articles:
        raise EurLexError("The page contains no articles.")
    return articles


UNIT_ID = re.compile(r'<div (?:class="eli-subdivision" )?id="(art|cpt|anx|enc|fnp)_([^"]+)"')
TITLE = re.compile(r'<p class="([a-z0-9-]+)"[^>]*>(.*?)</p>', re.S)


def parse_structure(page: str) -> list[Section]:
    """Articles with number, title and text, and the chapters/sections enclosing them."""
    sections: list[Section] = []
    path: list[Heading] = []
    for part in ARTICLE_START.split(page):
        unit = UNIT_ID.match(part)
        if not unit:
            continue
        kind, ident = unit.groups()
        titles = {cls: html_to_text(body) for cls, body in TITLE.findall(part[:3000])}
        if kind == "cpt":
            level = ident.count(".") + 1  # cpt_III -> 1, cpt_III.sct_1 -> 2
            heading = Heading(level, titles.get("title-division-1", ""), titles.get("title-division-2", ""))
            path = [h for h in path if h.level < level] + [heading]
        elif kind == "art":
            number = titles.get("title-article-norm", f"Article {ident}")
            title = titles.get("stitle-article-norm", "").strip(" '’")  # drop amendment-marker remnants
            text = html_to_text(part)
            prefix = f"{number} {title}".strip()
            if text.startswith(prefix):
                text = text[len(prefix):].lstrip(" '’")
            sections.append(Section(number=number, title=title, text=text, path=tuple(path)))
        elif kind in ("anx", "fnp"):
            path = []
    if not sections:
        sections = _parse_flat(page)
    if not sections:
        raise EurLexError("The page contains no articles.")
    return sections


FLAT_ARTICLE = re.compile(r'(?=<p class="title-article-norm")')


def _parse_flat(page: str) -> list[Section]:
    """Older consolidated texts mark article titles but have no article containers."""
    sections = []
    parts = FLAT_ARTICLE.split(page)[1:]
    for part in parts:
        part = re.split(r'<div id="anx_|<p class="title-annex', part)[0]
        titles = {cls: html_to_text(body) for cls, body in TITLE.findall(part[:3000])}
        number = titles.get("title-article-norm", "")
        title = titles.get("stitle-article-norm", "").strip(" '’")
        text = html_to_text(part)
        for prefix in (number, titles.get("stitle-article-norm", "")):
            if prefix and text.startswith(prefix):
                text = text[len(prefix):].lstrip(" '’")
        sections.append(Section(number=number, title=title, text=text, path=()))
    return sections
