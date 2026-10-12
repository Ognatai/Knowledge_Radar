"""Read the private repository: private notes and company folders for interview prep.

The private repository is a sibling checkout (`private_repo_path` in the untracked
`local-config.yaml`) that holds data only; its README fixes the layout and the
Markdown-with-frontmatter formats read here:

    notes/*.md
    companies/<company>/company.md
    companies/<company>/_research/*.md        (research.py: company and interviewers)
    companies/<company>/<role>/job_posting.md
    companies/<company>/<role>/round-<n>/{round,interviewers,prep,retro}.md
    companies/<company>/<role>/round-<n>/notes/*.md

From the folders and frontmatter alone, without a language model, this module builds
the structural part of the private graph: companies, postings, rounds, retros and
interviewers, connected by POSTED_BY, FOR_POSTING, INTERVIEWED_BY and RETRO_OF, plus
IDENTIFIED_GAP_IN for retro gaps that name a known topic. Gaps that name no known
topic stay open: they are what the monitoring run should look for.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from app.backend.knowledge_radar.graph import Entity, entity_keys, normalize_name
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import FRONTMATTER_PATTERN

ROUND_FOLDER = re.compile(r"^round-(\d+)$")
# Written by research.py; not a slug, so never a role folder.
RESEARCH_FOLDER = "_research"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROUND_FILES = {"round.md": "round", "interviewers.md": "interviewers", "prep.md": "prep", "retro.md": "retro"}
REQUIRED = {"company": ["name"], "job_posting": ["title"], "round": ["round_number"]}
RETRO_LISTS = ["questions_asked", "struggled_with", "personal_improvement", "kb_gaps_identified"]
# Entity types a retro gap can point to (schema: IDENTIFIED_GAP_IN).
TOPIC_TYPES = frozenset({"Method", "Concept", "Technology", "Regulation", "Dataset"})


class PrivateRepoError(ValueError):
    """Raised when a private file does not follow the documented layout or format."""


@dataclass(frozen=True)
class PrivateDocument:
    id: str  # the path without .md, relative to the private repository
    kind: str  # note, company, research, job_posting, round, interviewers, prep, retro, round_note
    path: Path
    frontmatter: dict[str, Any]
    body: str
    company: str | None = None
    role: str | None = None
    round: int | None = None


def read_document(path: Path, root: Path, kind: str, **place: Any) -> PrivateDocument:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(text)
    frontmatter: dict[str, Any] = {}
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            raise PrivateRepoError(f"{path}: invalid frontmatter: {exc}") from exc
        if not isinstance(frontmatter, dict):
            raise PrivateRepoError(f"{path}: the frontmatter must be a mapping.")
    body = text[match.end():] if match else text
    missing = [key for key in REQUIRED.get(kind, []) if not str(frontmatter.get(key, "")).strip()]
    if missing:
        raise PrivateRepoError(f"{path}: missing frontmatter field(s): {', '.join(missing)}.")
    if kind == "retro":
        for key in RETRO_LISTS:
            if key in frontmatter and not isinstance(frontmatter[key], list):
                raise PrivateRepoError(f"{path}: '{key}' must be a list.")
    document_id = path.relative_to(root).with_suffix("").as_posix()
    return PrivateDocument(document_id, kind, path, frontmatter, body.strip(), **place)


def _slug(folder: Path) -> str:
    if not SLUG.match(folder.name):
        raise PrivateRepoError(f"{folder}: folder names must be lowercase slugs (e.g. 'acme-gmbh').")
    return folder.name


def load_documents(root: Path) -> list[PrivateDocument]:
    """Every document of the private repository, in a stable order."""
    documents: list[PrivateDocument] = []
    for path in sorted((root / "notes").glob("*.md")):
        documents.append(read_document(path, root, "note"))
    companies = root / "companies"
    for company_dir in sorted(p for p in companies.iterdir() if p.is_dir()) if companies.is_dir() else []:
        company = _slug(company_dir)
        if not (company_dir / "company.md").is_file():
            raise PrivateRepoError(f"{company_dir}: company.md is missing.")
        documents.append(read_document(company_dir / "company.md", root, "company", company=company))
        for path in sorted((company_dir / RESEARCH_FOLDER).glob("*.md")):
            documents.append(read_document(path, root, "research", company=company))
        for role_dir in sorted(p for p in company_dir.iterdir() if p.is_dir() and p.name != RESEARCH_FOLDER):
            role = _slug(role_dir)
            if (role_dir / "job_posting.md").is_file():
                documents.append(read_document(role_dir / "job_posting.md", root, "job_posting", company=company, role=role))
            for round_dir in sorted(p for p in role_dir.iterdir() if p.is_dir()):
                number = ROUND_FOLDER.match(round_dir.name)
                if not number:
                    raise PrivateRepoError(f"{round_dir}: round folders are named 'round-<n>'.")
                place = {"company": company, "role": role, "round": int(number.group(1))}
                for name, kind in ROUND_FILES.items():
                    if (round_dir / name).is_file():
                        documents.append(read_document(round_dir / name, root, kind, **place))
                for path in sorted((round_dir / "notes").glob("*.md")):
                    documents.append(read_document(path, root, "round_note", **place))
    return documents


def parse_interviewers(body: str) -> list[dict[str, str]]:
    """`## Name` sections with `- key: value` lines."""
    people: list[dict[str, str]] = []
    for section in re.split(r"^## ", body, flags=re.MULTILINE)[1:]:
        lines = section.strip().splitlines()
        person = {"name": lines[0].strip()}
        for line in lines[1:]:
            match = re.match(r"^\s*-\s*([\w ]+?)\s*:\s*(.+?)\s*$", line)
            if match:
                person[match.group(1).strip().lower()] = match.group(2)
        people.append(person)
    return people


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def document_slug(document: PrivateDocument) -> str:
    return "private-" + slugify(document.id)


KIND_LABELS = {"company": "Company", "research": "Research", "job_posting": "Job posting", "round": "Interview round", "interviewers": "Interviewers",
               "prep": "Preparation", "retro": "Retro", "round_note": "Round note", "note": "Note"}
FIELD_LABELS = {"questions_asked": "Questions asked", "struggled_with": "Struggled with",
                "personal_improvement": "Personal improvement", "kb_gaps_identified": "Knowledge-base gaps",
                "round_number": "Round", "url": "URL"}


def document_text(document: PrivateDocument) -> str:
    """The body with the frontmatter's facts in front: a retro's questions and gaps, a
    round's date, are what the chat is asked about."""
    lines: list[str] = []
    for key, value in document.frontmatter.items():
        if key in ("title", "name"):
            continue
        label = FIELD_LABELS.get(key, key.replace("_", " ").capitalize())
        if isinstance(value, list):
            if value:
                lines += [f"{label}:", *(f"- {item}" for item in value)]
        elif value not in (None, ""):
            lines.append(f"{label}: {_iso(value)}")
    if document.body:
        lines += ["", document.body] if lines else [document.body]
    return "\n".join(lines)


def document_titles(documents: list[PrivateDocument]) -> dict[str, str]:
    """Readable titles: "Retro: ACME GmbH – ML Engineer – round 1"."""
    companies = {d.company: str(d.frontmatter.get("name") or d.company) for d in documents if d.kind == "company"}
    roles = {(d.company, d.role): str(d.frontmatter.get("title") or d.role) for d in documents if d.kind == "job_posting"}
    titles: dict[str, str] = {}
    for document in documents:
        own = str(document.frontmatter.get("title") or document.frontmatter.get("name") or "")
        if document.company is None:
            titles[document.id] = own or document.id
            continue
        parts = [companies.get(document.company, document.company)]
        if document.role:
            parts.append(roles.get((document.company, document.role), document.role))
        if document.round:
            parts.append(f"round {document.round}")
        title = f"{KIND_LABELS.get(document.kind, document.kind)}: {' – '.join(parts)}"
        titles[document.id] = f"{title}: {own}" if document.kind in ("round_note", "research") and own else title
    return titles


def as_note(document: PrivateDocument, title: str | None = None) -> NoteDetail:
    """The document in the shape the extraction agent and the index read."""
    title = title or str(document.frontmatter.get("title") or document.frontmatter.get("name") or document.id)
    return NoteDetail.model_construct(
        slug=document_slug(document), title_en=title, title_de=title, entity_type="Concept",
        aliases=[], content_en=document_text(document), content_de="", sources=[], links=[],
    )


@dataclass
class StructuralGraph:
    entities: list[dict[str, Any]] = field(default_factory=list)
    relations: list[dict[str, str]] = field(default_factory=list)
    # Retro gaps naming no known topic: candidates for the monitoring watchlist.
    open_gaps: list[dict[str, str]] = field(default_factory=list)

    def to_yaml(self) -> str:
        data = {"version": 1, "entities": self.entities, "relations": self.relations, "open_gaps": self.open_gaps}
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)


def _iso(value: Any) -> str | None:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    return str(value) if value else None


def structural_graph(documents: list[PrivateDocument], known: dict[str, Entity]) -> StructuralGraph:
    """The graph the folders and frontmatter describe. `known` are the public and private
    entities that interviewers and retro gaps are resolved against."""
    graph = StructuralGraph()
    by_key: dict[tuple[str, str], str] = {}
    for entity in known.values():
        for key in entity_keys(entity):
            by_key.setdefault((entity.type, key), entity.id)

    def resolve(name: str, types: frozenset[str]) -> str | None:
        key = normalize_name(name)
        return next((by_key[(entity_type, key)] for entity_type in sorted(types) if (entity_type, key) in by_key), None)

    def add_entity(entity_id: str, entity_type: str, name: str, **properties: Any) -> None:
        if any(entry["id"] == entity_id for entry in graph.entities):
            return
        entry = {"id": entity_id, "type": entity_type, "name_en": name, "name_de": name}
        entry.update({key: value for key, value in properties.items() if value not in (None, [], "")})
        graph.entities.append(entry)

    def relate(source: str, relation_type: str, target: str, document: PrivateDocument) -> None:
        graph.relations.append({"from": source, "type": relation_type, "to": target, "source": document.id})

    postings = {(d.company, d.role) for d in documents if d.kind == "job_posting"}
    rounds_seen: set[tuple[str, str, int]] = set()

    def ensure_round(document: PrivateDocument) -> str:
        """Every round with any document is a node, whether or not round.md exists."""
        round_id = f"round-{document.company}-{document.role}-{document.round}"
        key = (document.company, document.role, document.round)
        if key not in rounds_seen:
            rounds_seen.add(key)
            round_doc = next((d for d in documents if d.kind == "round" and (d.company, d.role, d.round) == key), None)
            date = _iso(round_doc.frontmatter.get("date")) if round_doc else None
            add_entity(round_id, "InterviewRound", f"{document.company} {document.role} round {document.round}",
                       round_number=document.round, date=date)
            if (document.company, document.role) in postings:
                relate(round_id, "FOR_POSTING", f"posting-{document.company}-{document.role}", round_doc or document)
        return round_id

    for document in documents:
        if document.round is not None:
            ensure_round(document)
        if document.kind == "company":
            fm = document.frontmatter
            add_entity(f"company-{document.company}", "Company", fm["name"], industry=fm.get("industry"), aliases=fm.get("aliases") or [])
        elif document.kind == "job_posting":
            posting = f"posting-{document.company}-{document.role}"
            add_entity(posting, "JobPosting", document.frontmatter["title"], date=_iso(document.frontmatter.get("date")), url=document.frontmatter.get("url"))
            relate(posting, "POSTED_BY", f"company-{document.company}", document)
        elif document.kind == "interviewers":
            round_id = f"round-{document.company}-{document.role}-{document.round}"
            for person in parse_interviewers(document.body):
                person_id = resolve(person["name"], frozenset({"Person"})) or f"person-{slugify(person['name'])}"
                if person_id not in known:
                    add_entity(person_id, "Person", person["name"], role=person.get("role"), focus=person.get("focus"))
                relate(round_id, "INTERVIEWED_BY", person_id, document)
        elif document.kind == "retro":
            round_id = f"round-{document.company}-{document.role}-{document.round}"
            retro_id = f"retro-{document.company}-{document.role}-{document.round}"
            fm = document.frontmatter
            add_entity(retro_id, "InterviewRetro", f"Retro {document.company} {document.role} round {document.round}",
                       date=_iso(fm.get("date")), **{key: fm.get(key) or [] for key in RETRO_LISTS})
            relate(retro_id, "RETRO_OF", round_id, document)
            for gap in fm.get("kb_gaps_identified") or []:
                topic = resolve(str(gap), TOPIC_TYPES)
                if topic:
                    relate(retro_id, "IDENTIFIED_GAP_IN", topic, document)
                else:
                    graph.open_gaps.append({"retro": retro_id, "topic": str(gap)})
    return graph
