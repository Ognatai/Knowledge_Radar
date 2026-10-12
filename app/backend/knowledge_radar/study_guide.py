"""The study guide for one interview round: every topic of the posting in one document.

Built without a language model from what is there, for reading on the phone (the app
saves it as PDF):

- Parts: the knowledge base's subject areas (public/areas.yaml), in their order.
- Chapters: one per note that covers a topic of the posting (graph/topics.yaml from
  posting_topics.py), with the posting's words and the note's text and sources.
- Not covered yet: topics without a note. A Claude session adds them through the
  new-note workflow (the user's choice on 2026-10-12: no automatic channel).
- Appendix, from the private repository: what is known about the company and the
  interviewers, the self-introduction and own questions from the saved prep.md, STAR
  stories from the user's notes (`### STAR: …` sections), questions from earlier
  rounds, and a checklist.

Headings get ids in the app by the same rule as `anchor` here, so the table of contents
links work.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.agents.posting_topics import read_topics
from app.backend.knowledge_radar.areas import Area
from app.backend.knowledge_radar.interviews import InterviewError, _frontmatter
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.prep import _body, _research
from app.backend.knowledge_radar.private_repo import RESEARCH_FOLDER, RETRO_LISTS, parse_interviewers, slugify

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
HEADING = re.compile(r"^(#{1,6})\s")
STAR_HEADING = re.compile(r"^###\s+STAR\b[:\s-]*(.*)$", re.IGNORECASE)
SKIPPED_SECTIONS = {"quellen", "sources"}
CHECKLIST = [
    "Lebenslauf und Anschreiben der Bewerbung noch einmal gelesen",
    "Kurzvorstellung laut geübt (etwa 60 Sekunden)",
    "Zu jeder Anforderung ein konkretes Beispiel aus eigener Arbeit parat",
    "Eigene Fragen notiert",
    "Technik geprüft (Kamera, Mikrofon, Link) oder Anfahrt geklärt",
    "Namen und Rollen der Gesprächspartner im Kopf",
]


def anchor(text: str) -> str:
    """The id of a heading; the app's heading renderer uses the same rule."""
    return re.sub(r"[\W_]+", "-", text.lower()).strip("-")


@dataclass
class Chapter:
    note: NoteDetail
    phrases: list[str] = field(default_factory=list)


def _note_text(note: NoteDetail, chapters: set[str]) -> str:
    """The note's German text (English if none) for a chapter: banner and sources removed,
    headings one level down, wikilinks to other chapters as links, others as plain text."""
    content = note.content_de or note.content_en
    lines, skipping, in_code = [], False, False
    for line in content.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if in_code or line.lstrip().startswith("```"):
            # "# comment" in a code block is no heading.
            if not skipping:
                lines.append(line)
            continue
        if line.startswith("> **"):
            continue
        heading = HEADING.match(line)
        if heading:
            skipping = line.lstrip("#").strip().casefold() in SKIPPED_SECTIONS
            if skipping:
                continue
            line = "#" + line
        if not skipping:
            lines.append(line)

    def link(match: re.Match[str]) -> str:
        label = match.group(2) or match.group(1)
        return label

    return WIKILINK.sub(link, "\n".join(lines)).strip()


def _section(text: str, title: str) -> str:
    """The body of `## title` in a Markdown text, without the heading."""
    match = re.search(rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _star_stories(root: Path) -> list[tuple[str, str]]:
    stories = []
    for path in sorted((root / "notes").glob("*.md")):
        title, lines = None, []
        for line in _body(path).splitlines() + ["### end"]:
            match = STAR_HEADING.match(line)
            if line.startswith("### ") and title is not None:
                stories.append((title, "\n".join(lines).strip()))
                title, lines = None, []
            if match:
                title = match.group(1).strip() or "STAR"
            elif title is not None:
                lines.append(line)
    return stories


def build(root: Path, company: str, role: str, round_number: int, notes: dict[str, NoteDetail], areas: list[Area]) -> str:
    role_dir = root / "companies" / company / role
    round_dir = role_dir / f"round-{round_number}"
    if not (round_dir / "round.md").is_file():
        raise InterviewError(f"Unknown round companies/{company}/{role}/round-{round_number}.")
    company_dir = role_dir.parent
    company_name = str(_frontmatter(company_dir / "company.md").get("name") or company) if (company_dir / "company.md").is_file() else company
    role_title = str(_frontmatter(role_dir / "job_posting.md").get("title") or role) if (role_dir / "job_posting.md").is_file() else role
    round_date = _frontmatter(round_dir / "round.md").get("date")
    topics = read_topics(root, f"companies/{company}/{role}/job_posting")

    chapters: dict[str, Chapter] = {}
    missing: list[dict[str, Any]] = []
    for topic in topics or []:
        if topic.get("note") in notes:
            chapters.setdefault(topic["note"], Chapter(notes[topic["note"]])).phrases.append(topic["phrase"])
        else:
            missing.append(topic)

    parts: list[tuple[str, list[Chapter]]] = []
    placed: set[str] = set()
    for area in areas:
        members = [chapters[slug] for slug in area.notes if slug in chapters]
        if members:
            parts.append((area.name_de, members))
            placed.update(chapter.note.slug for chapter in members)
    rest = [chapter for slug, chapter in chapters.items() if slug not in placed]
    if rest:
        parts.append(("Weitere Themen", rest))

    title = f"Lernunterlage: {company_name} – {role_title}"
    when = f"Runde {round_number}" + (f" am {round_date}" if round_date else "")
    toc, body = [], []
    number = 0
    for index, (part, members) in enumerate(parts, start=1):
        heading = f"Teil {index}: {part}"
        toc.append(f"- **[{heading}](#{anchor(heading)})**")
        body += ["", f"## {heading}"]
        for chapter in members:
            number += 1
            chapter_heading = f"{number} {chapter.note.title_de or chapter.note.title_en}"
            toc.append(f"  - [{chapter_heading}](#{anchor(chapter_heading)})")
            quoted = "; ".join(f"„{phrase}“" for phrase in dict.fromkeys(chapter.phrases))
            body += ["", f"### {chapter_heading}", "", f"_In der Anzeige: {quoted}_", "", _note_text(chapter.note, set(chapters))]
            if chapter.note.sources:
                body += ["", "**Quellen:** " + " · ".join(f"<{url}>" for url in chapter.note.sources)]

    if topics is None:
        body += ["", "## Themen", "", "Die Themen der Anzeige sind noch nicht ausgelesen. Die Aktualisierung nach "
                 "/new-application läuft noch oder ist fehlgeschlagen."]
    if missing:
        heading = "Noch nicht abgedeckt"
        toc.append(f"- **[{heading}](#{anchor(heading)})**")
        body += ["", f"## {heading}", "",
                 "Zu diesen Themen der Anzeige gibt es noch keine Notiz. In einer Claude-Sitzung ergänzen lassen: "
                 f"„Ergänze die fehlenden Themen der Lernunterlage für {company_name}.“", ""]
        body += [f"- **{t['name']}**: „{t['phrase']}“" + (" (im Graphen bekannt, noch ohne eigene Notiz)" if t.get("entity") else "")
                 for t in missing]

    appendix = _appendix(root, company_dir, round_dir, round_number)
    if appendix:
        toc.append("- **[Anhang](#anhang)**")
        for letter, (heading, _) in zip("ABCDEFGH", appendix):
            toc.append(f"  - [{letter} {heading}](#{anchor(f'{letter} {heading}')})")
        body += ["", "## Anhang"]
        for letter, (heading, text) in zip("ABCDEFGH", appendix):
            body += ["", f"### {letter} {heading}", "", text]

    lines = [f"# {title}", "", f"_{when} · {number} Kapitel · erstellt aus der Wissensbasis_", "", "## Inhalt", "", *toc, *body]
    return "\n".join(lines).strip() + "\n"


def _appendix(root: Path, company_dir: Path, round_dir: Path, round_number: int) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    company_parts = []
    own = _body(company_dir / "company.md")
    if own:
        company_parts.append(own)
    research = _research(company_dir / RESEARCH_FOLDER / "company.md")
    if research:
        company_parts.append("_Recherche mit Claude, aus öffentlichen Quellen; vor dem Gespräch prüfen._\n\n" + research.replace("\n### ", "\n#### "))
    interviewers_file = round_dir / "interviewers.md"
    for person in parse_interviewers(interviewers_file.read_text(encoding="utf-8")) if interviewers_file.is_file() else []:
        details = ", ".join(value for value in (person.get("role"), person.get("focus")) if value)
        text = f"#### {person['name']}" + (f" ({details})" if details else "")
        background = _research(company_dir / RESEARCH_FOLDER / f"{slugify(person['name'])}.md")
        company_parts.append(text + ("\n\n" + background.replace("### ", "##### ") if background else ""))
    if company_parts:
        sections.append(("Firmenwissen und Gesprächspartner", "\n\n".join(company_parts)))

    prep_text = _body(round_dir / "prep.md")
    pitch, questions = _section(prep_text, "Kurzvorstellung"), _section(prep_text, "Fragen an die Gesprächspartner")
    hint = "Noch keine gespeicherte Vorbereitung: /prep erzeugt sie."
    sections.append(("Kurzvorstellung", pitch or hint))
    sections.append(("Eigene Fragen", questions or hint))
    practice = _section(prep_text, "Übungsfragen")
    if practice:
        sections.append(("Übungsfragen", practice))

    stories = _star_stories(root)
    sections.append(("STAR-Geschichten", "\n\n".join(f"#### {title}\n\n{text}" for title, text in stories) or
                     "Noch keine: in einer Notiz unter notes/ als Abschnitte `### STAR: <Titel>` (Situation, Aufgabe, "
                     "Handlung, Ergebnis) anlegen."))

    asked = []
    for number in range(1, round_number):
        retro = round_dir.parent / f"round-{number}" / "retro.md"
        if retro.is_file():
            info = _frontmatter(retro)
            asked += [f"- Runde {number}: {item}" for item in info.get("questions_asked") or []]
    if asked:
        sections.append(("Fragen aus früheren Runden", "\n".join(asked)))
    sections.append(("Checkliste vor dem Gespräch", "\n".join(f"- [ ] {item}" for item in CHECKLIST)))
    return sections
