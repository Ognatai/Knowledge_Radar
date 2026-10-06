"""Draft technical notes from the vault with the local LLM, review, and accept.

Notes are migrated in packages (`migration/technical/<package>.yaml`), each
listing the notes and their sources. Per note, the local model first plans
the "How it works" steps specific to the topic, then writes the English body
part by part (vault note for topic coverage, source abstracts as evidence)
and translates it part by part into German; the sources sections are generated from verified metadata.
Drafts are checked against the template, links, citations, numbers and
originality, reviewed by a person and only then accepted into `public/notes/`.

    python -m app.agents.technical_notes outline rag   # plan; review/edit the .outline.md files
    python -m app.agents.technical_notes draft  rag [--notes rag-chunking,...] [--force]
    python -m app.agents.technical_notes review rag
    python -m app.agents.technical_notes accept rag --notes rag-chunking,...

Drafts are written to `.knowledge-radar/drafts/technical/` (untracked).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from string import Template

import yaml

from app.agents import llm, sources
from app.backend.knowledge_radar.config import load_local_config
from app.backend.knowledge_radar.notes import (
    REPOSITORY_ROOT,
    configured_notes_directory,
    planned_note_slugs,
    wikilink_targets,
)
from app.backend.knowledge_radar.templates import (
    TECHNICAL_OPTIONAL,
    TECHNICAL_REQUIRED,
    TECHNOLOGY_MECHANISM,
    check_language_part,
    check_template,
)

MIGRATION = REPOSITORY_ROOT / "migration"
DRAFTS = REPOSITORY_ROOT / ".knowledge-radar" / "drafts" / "technical"
PROMPTS = Path(__file__).parent / "prompts"
NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*(?![\w])")
SOURCES_HEADING = re.compile(r"^### (?:Sources|Quellen)\s*$", re.M)
# Only vault notes with their own regulatory section get a "Regulatory context" section.
REGULATION_HINT = re.compile(r"^#+\s*Regulatorischer Kontext", re.M)
SHINGLE = 6  # words per n-gram for the originality check
ORIGINALITY_LIMIT = 0.10  # share of a draft's 6-grams found verbatim in vault note or abstracts
# Qwen3's recommended non-thinking sampling; low temperatures cause repetition loops.
# Writing parts use the model's reasoning mode (KNOWLEDGE_RADAR_THINK=0 disables it):
# better content, and answers free of planning text. Qwen3's recommended thinking sampling.
THINK = os.environ.get("KNOWLEDGE_RADAR_THINK", "1") != "0"
# Writer: qwen3:30b-a3b with reasoning gave far fewer factual errors than qwen3:14b in the RAG pilot.
WRITER_MODEL = os.environ.get("KNOWLEDGE_RADAR_WRITER_MODEL", "qwen3:30b-a3b")
GLOSSARY = MIGRATION / "glossary-de.yaml"
WRITING_SAMPLING = {"top_p": 0.95, "top_k": 20} if THINK else {"top_p": 0.8, "top_k": 20, "presence_penalty": 1.5}
PART_TOKENS = 6000 if THINK else 900  # hard cap per part, including reasoning


@dataclass(frozen=True)
class NotePlan:
    id: str
    source_title: str
    title_en: str
    title_de: str
    entity_type: str
    links: list[str]
    sources: list[dict]


def load_package(package: str) -> list[NotePlan]:
    config = yaml.safe_load((MIGRATION / "technical" / f"{package}.yaml").read_text(encoding="utf-8"))
    mapping = yaml.safe_load((MIGRATION / "vault-mapping.yaml").read_text(encoding="utf-8"))["notes"]
    inventory = {
        note["id"]: note
        for note in yaml.safe_load((MIGRATION / "inventory.yaml").read_text(encoding="utf-8"))["notes"]
    }
    by_id = {entry["id"]: (title, entry) for title, entry in mapping.items() if not entry.get("hub")}
    plans = []
    for note_id, spec in config["notes"].items():
        source_title, entry = by_id[note_id]
        linked = inventory[note_id]["links_inline"] + inventory[note_id]["links_related_only"]
        package_members = [other for other in config["notes"] if other != note_id]
        links = list(dict.fromkeys(linked + package_members + spec.get("extra_links", [])))
        plans.append(NotePlan(
            id=note_id,
            source_title=source_title,
            title_en=entry["title_en"],
            title_de=entry["title_de"],
            entity_type=entry["entity_type"],
            links=links,
            sources=spec["sources"],
        ))
    return plans


def sections_for(entity_type: str, lang_index: int) -> tuple[list[str], list[str]]:
    """(required, optional) section headings of the technical template for one language."""
    required = TECHNICAL_REQUIRED
    if entity_type == "Technology":
        how = required.index(("How it works", "Funktionsweise"))
        required = required[:how] + TECHNOLOGY_MECHANISM + required[how + 1:]
    return [pair[lang_index] for pair in required], [pair[lang_index] for pair in TECHNICAL_OPTIONAL]


def mechanism_heading(entity_type: str) -> str:
    return "Core concepts" if entity_type == "Technology" else "How it works"


def render(name: str, **values: str) -> str:
    return Template((PROMPTS / name).read_text(encoding="utf-8")).substitute(values)


def source_block(resolved: list[sources.Source]) -> str:
    return "\n\n".join(f"{source.short}: {source.summary or '(no abstract)'}" for source in resolved)


def outline_prompt(plan: NotePlan, resolved: list[sources.Source], vault_text: str) -> str:
    return render(
        "technical_outline.md",
        mechanism_heading=mechanism_heading(plan.entity_type),
        title=plan.title_en,
        sources=source_block(resolved),
        vault=vault_text,
    )


def format_outline(outline: dict) -> str:
    lines = [str(outline.get("overview", ""))]
    for step in outline.get("steps", []):
        lines.append(f"#### {str(step.get('heading', '')).strip()}")
        lines += [f"  - {point}" for point in step.get("covers", [])]
        if step.get("sources"):
            lines.append(f"  - cite: {'; '.join(map(str, step['sources']))}")
    return "\n".join(line for line in lines if line)


def parse_outline(markdown: str) -> dict:
    """Read an outline file (as written by format_outline, possibly edited by hand)."""
    lines = markdown.splitlines()
    outline: dict = {"overview": "", "steps": []}
    for line in lines:
        if line.startswith("#### "):
            outline["steps"].append({"heading": line[5:].strip(), "covers": [], "sources": []})
        elif line.strip().startswith("- ") and outline["steps"]:
            item = line.strip()[2:].strip()
            step = outline["steps"][-1]
            if item.startswith("cite:"):
                step["sources"] += [name.strip() for name in item[5:].split(";") if name.strip()]
            else:
                step["covers"].append(item)
        elif line.strip() and not outline["steps"] and not line.startswith("#"):
            outline["overview"] = (outline["overview"] + " " + line.strip()).strip()
    return outline


SECTION_TASKS = {
    "TL;DR": "2-3 sentences: what it is and which problem it solves.",
    "When to use it": "A list of 3-6 bullet points: situations in which the approach fits, each with a short reason.",
    "Strengths and limitations": (
        'Two bold labels on their own lines, "**Strengths**" and "**Limitations**", each followed '
        "by a list of 3-6 precise bullet points."
    ),
    "Comparison": (
        "A Markdown table comparing the approach with its closest alternatives (columns e.g. "
        "Approach | How it differs | Suited for), followed by one or two sentences."
    ),
    "In practice": "A list of practical points: evaluation, typical failure modes, parameter choices.",
    "Regulatory context": (
        "Only what a regulation concretely requires for this specific topic, as stated in the vault "
        "note; one short paragraph."
    ),
    "Key takeaway": (
        "Exactly one sentence that summarises the whole note (what the topic is and its main "
        "trade-off). No citation, no link, not about a single paper or method variant."
    ),
    "Common usage": "Typical commands or API calls as a short Markdown table or code block, with one line of explanation each.",
}
NOTICE_EN = "> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong."
NOTICE_DE = (
    "> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; "
    "sie kann unvollst\u00e4ndig, veraltet oder falsch sein."
)


def cites(text: str, source: sources.Source) -> bool:
    """True if the text cites the source, tolerating "(Name et al., 2024)" style variants."""
    if source.short in text:
        return True
    surname = source.short.split()[0].rstrip(",")
    year = re.search(r"\d{4}", source.short)
    return bool(year) and re.search(rf"{re.escape(surname)}[^\n]{{0,40}}{year.group(0)}", text) is not None


def section_prompt(plan: NotePlan, part: str, task: str, required: list[sources.Source],
                   resolved: list[sources.Source], vault_text: str, context: str,
                   titles: dict[str, str]) -> str:
    citation_rule = ""
    if required:
        forms = ", ".join(f'"{source.short}"' for source in required)
        citation_rule = (
            f"Relevant sources for this part: {forms}. Cite a source only where it directly supports a "
            "specific statement (a finding, a number, the origin of a method), in exactly that form, and "
            "at most once in this part. Do not attach sources to general statements.\n"
        )
    return render(
        "technical_section.md",
        title=plan.title_en,
        part=part,
        task=task,
        citation_rule=citation_rule,
        example_short=resolved[0].short if resolved else "Author et al. (2020)",
        context=context or "(nothing yet)",
        links="\n".join(f"- {link}: {titles.get(link, link)}" for link in plan.links),
        sources=source_block(resolved),
        vault=vault_text,
    )


def unlink_citations(text: str, resolved: list[sources.Source]) -> str:
    """Turn citations the model wrote as wikilinks ([[Name et al. (2020)]]) back into plain text."""
    shorts = {source.short for source in resolved}

    def replace(match: re.Match) -> str:
        target = match.group(1).strip()
        return target if target in shorts else match.group(0)

    return re.sub(r"\[\[([^\[\]|]+)(?:\\?\|[^\[\]]*)?\]\]", replace, text)


def write_part(prompt: str) -> str:
    """Generate one part; the heading line is set by the pipeline.

    With reasoning mode the model can use up the token budget for thinking and return
    nothing; such a part is retried once with twice the budget.
    """
    text = ""
    for budget in (PART_TOKENS, 2 * PART_TOKENS):
        text = clean(llm.generate(prompt, temperature=0.6 if THINK else 0.7, sampling=WRITING_SAMPLING,
                                  max_tokens=budget, think=THINK, model=WRITER_MODEL,
                                  context_tokens=32768))
        text = re.sub(r"^#{3,4} .*\n+", "", text)  # the heading is set by the pipeline
        if text.strip():
            break
    return text


def apply_glossary(german: str, glossary_path: Path = GLOSSARY) -> str:
    """Restore established English technical terms the translation germanised."""
    if not glossary_path.is_file():
        return german
    for pattern, replacement in yaml.safe_load(glossary_path.read_text(encoding="utf-8"))["rules"]:
        german = re.sub(pattern, replacement, german)
    return german


def split_steps(body: str) -> list[str]:
    """Split a section body into its intro and one chunk per '####' step."""
    return [chunk for chunk in re.split(r"\n(?=#### )", body) if chunk.strip()]


def translate_section(body: str) -> str:
    """Translate a section; long sections step by step (whole blocks made the model loop)."""
    return "\n\n".join(apply_glossary(translate(chunk)) for chunk in split_steps(body))


def english_sections(english: str) -> list[tuple[str, str]]:
    """(heading, body) pairs of an English note part, without notice and sources."""
    parts = re.split(r"^### (.+)$", SOURCES_HEADING.split(english)[0], flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts) - 1, 2)]


def heading_count(text: str) -> int:
    return len(re.findall(r"^#### ", text, flags=re.M))


def translate(text: str) -> str:
    """Translate one part; retry once if the number of '####' headings changed."""
    german = ""
    for _ in range(2):
        german = clean(llm.generate(render("translate_de.md", english=text), temperature=0.3,
                                    model=llm.translation_model_name(),
                                    max_tokens=4000 + 3 * len(text.split()), context_tokens=32768))
        if heading_count(german) == heading_count(text):
            break
    return german


def clean(answer: str) -> str:
    text = answer.strip()
    # Unwrap an answer the model put entirely into a ```markdown block, but keep real code blocks.
    wrapped = re.fullmatch(r"```(?:markdown|md)?\n(.*)\n```", text, flags=re.S)
    if wrapped and "```" not in wrapped.group(1):
        text = wrapped.group(1).strip()
    # The sources section is generated; drop one the model may have added anyway.
    text = SOURCES_HEADING.split(text)[0].rstrip()
    if len(re.findall(r"^```", text, flags=re.M)) % 2:
        text += "\n```"  # close a code block the model left open
    return text


def sources_section(heading: str, resolved: list[sources.Source]) -> str:
    return f"### {heading}\n\n" + "\n".join(f"- {source.citation}" for source in resolved)


def assemble(plan: NotePlan, resolved: list[sources.Source], english: str, german: str) -> str:
    frontmatter = {
        "title_en": plan.title_en,
        "title_de": plan.title_de,
        "entity_type": plan.entity_type,
        "sources": [source.url for source in resolved],
    }
    return (
        "---\n" + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False) + "---\n\n"
        f"## EN\n\n{english}\n\n{sources_section('Sources', resolved)}\n\n"
        f"## DE\n\n{german}\n\n{sources_section('Quellen', resolved)}\n"
    )


def shingles(text: str) -> set[tuple[str, ...]]:
    words = re.findall(r"\w+", text.casefold())
    return {tuple(words[i:i + SHINGLE]) for i in range(len(words) - SHINGLE + 1)}


def originality_overlap(draft: str, references: list[str]) -> float:
    draft_shingles = shingles(draft)
    if not draft_shingles:
        return 0.0
    reference_shingles = set().union(*(shingles(text) for text in references)) if references else set()
    return len(draft_shingles & reference_shingles) / len(draft_shingles)


def unknown_numbers(text: str, evidence: list[str]) -> list[str]:
    body = SOURCES_HEADING.split(text)[0]
    body = re.sub(r"```.*?```", "", body, flags=re.S)  # diagrams number their steps
    body = re.sub(r"^#{3,4} .*$", "", body, flags=re.M)  # numbered step headings
    allowed = set().union(*(NUMBER.findall(text) for text in evidence)) if evidence else set()
    return sorted({n for n in NUMBER.findall(body) if n not in allowed and n not in {"0", "1", "2"}}, key=len)


def uncited(text: str, resolved: list[sources.Source]) -> list[sources.Source]:
    body = SOURCES_HEADING.split(text)[0]
    return [source for source in resolved if not cites(body, source)]


def label_bare_links(text: str, titles: dict[str, str]) -> str:
    """Give [[id]] links without a label the title of the target note as label."""
    return re.sub(
        r"\[\[([^\[\]|#\\]+)\]\]",
        lambda m: f"[[{m.group(1)}|{titles[m.group(1)]}]]" if m.group(1) in titles else m.group(0),
        text,
    )


LATEX = re.compile(r"\$[^$\n]+\$|\\(?:frac|mathbf|text|cdot|sum)\b")
DANGLING_LINKS = re.compile(r"[.!?:]\s*(?:\[\[[^\[\]]+\]\]\s*)+$", re.M)
CITATION_REPEAT_LIMIT = 4


def style_problems(text: str, resolved: list[sources.Source]) -> list[str]:
    """Formatting problems the template check does not cover (one language part)."""
    body = SOURCES_HEADING.split(text)[0]
    problems = []
    if LATEX.search(body):
        problems.append("LaTeX formula (the site does not render LaTeX; use inline code)")
    dangling = DANGLING_LINKS.findall(body)
    if dangling:
        problems.append(f"{len(dangling)} link(s) appended after the end of a sentence")
    if body.count("[[") != body.count("]]"):
        problems.append("unbalanced [[ ]] (broken link)")
    for heading, section in english_sections(text):
        last_line = section.strip().splitlines()[-1].strip() if section.strip() else ""
        if last_line and not last_line.startswith(("|", "```", "-", "*")) and not re.search(r"[.!?:)\]`*]$", last_line):
            problems.append(f"section '{heading}' ends mid-sentence (truncated?)")
        elif last_line.startswith("-") and not re.search(r"[.!?:)\]`*a-z0-9]$", last_line):
            problems.append(f"section '{heading}' ends mid-sentence (truncated?)")
    for source in resolved:
        surname = re.escape(source.short.split()[0].rstrip(","))
        year = source.short[-5:-1]
        count = len(re.findall(rf"{surname}[^\n]{{0,40}}{year}", body))
        if count > CITATION_REPEAT_LIMIT:
            problems.append(f"{source.short} cited {count} times")
    return problems


def link_problems(note: str, known: set[str]) -> list[str]:
    return [f"unknown link target: {target}" for target in wikilink_targets(note) if target not in known]


class Drafter:
    def __init__(self, notes_directory: Path, drafts: Path = DRAFTS):
        self.notes_directory = notes_directory
        self.drafts = drafts
        vault = load_local_config().vault_path
        if vault is None:
            raise SystemExit("Set 'vault_path' in local-config.yaml (see local-config.example.yaml).")
        self.vault = vault
        mapping = yaml.safe_load((MIGRATION / "vault-mapping.yaml").read_text(encoding="utf-8"))["notes"]
        self.titles = {entry["id"]: entry["title_en"] for entry in mapping.values() if not entry.get("hub")}

    def vault_text(self, plan: NotePlan) -> str:
        matches = list(self.vault.rglob(f"{plan.source_title}.md"))
        if len(matches) != 1:
            raise SystemExit(f"vault note {plan.source_title!r}: found {len(matches)} files")
        return matches[0].read_text(encoding="utf-8")

    def write_outline(self, plan: NotePlan, resolved: list[sources.Source], vault_text: str) -> Path:
        outline: dict = {}
        for _ in range(3):  # models sometimes echo the example or placeholders instead of planning
            outline = json.loads(llm.generate(
                outline_prompt(plan, resolved, vault_text), json_output=True, think=THINK,
                model=WRITER_MODEL, max_tokens=PART_TOKENS, context_tokens=32768,
            ))
            headings = [str(step.get("heading", "")) for step in outline.get("steps", [])]
            if len(headings) >= 3 and not any("<" in h or "dropout" in h.lower() for h in headings):
                break
        else:
            raise llm.LLMError(f"{plan.id}: no usable outline after 3 attempts")
        target = self.drafts / f"{plan.id}.outline.md"
        target.write_text(format_outline(outline) + "\n", encoding="utf-8")
        return target

    def outline(self, plans: list[NotePlan], force: bool = False) -> None:
        """Plan the "How it works" steps of each note, for review before drafting."""
        self.drafts.mkdir(parents=True, exist_ok=True)
        for plan in plans:
            if (self.drafts / f"{plan.id}.outline.md").exists() and not force:
                continue
            started = time.time()
            resolved = [sources.resolve(entry) for entry in plan.sources]
            self.write_outline(plan, resolved, self.vault_text(plan))
            print(f"{plan.id}: outline in {time.time() - started:.0f}s", flush=True)

    def draft(self, plans: list[NotePlan], force: bool = False, retranslate: bool = False) -> None:
        self.drafts.mkdir(parents=True, exist_ok=True)
        for plan in plans:
            target = self.drafts / f"{plan.id}.md"
            if retranslate and target.exists():
                self.retranslate(plan, target)
                continue
            if target.exists() and not force:
                continue
            started = time.time()
            resolved = [sources.resolve(entry) for entry in plan.sources]
            vault_text = self.vault_text(plan)

            outline_file = self.drafts / f"{plan.id}.outline.md"
            if not outline_file.exists():
                self.write_outline(plan, resolved, vault_text)
            outline = parse_outline(outline_file.read_text(encoding="utf-8"))
            english, german = self.write_parts(plan, resolved, vault_text, outline)

            english, german = unlink_citations(english, resolved), unlink_citations(german, resolved)
            note = assemble(plan, resolved, english, german)
            target.write_text(note, encoding="utf-8")
            report = self.check(plan, note, resolved, vault_text)
            (self.drafts / f"{plan.id}.review.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            print(f"{plan.id}: drafted in {time.time() - started:.0f}s, "
                  f"{len(report['template'])} template problems", flush=True)

    def retranslate(self, plan: NotePlan, target: Path) -> None:
        """Rebuild the German part of an existing draft from its English part."""
        started = time.time()
        resolved = [sources.resolve(entry) for entry in plan.sources]
        english = target.read_text(encoding="utf-8").split("\n## EN\n", 1)[1].split("\n## DE\n", 1)[0]
        english = SOURCES_HEADING.split(english)[0].strip()
        german = unlink_citations(self.german(plan, english_sections(english)), resolved)
        note = assemble(plan, resolved, english, german)
        target.write_text(note, encoding="utf-8")
        report = self.check(plan, note, resolved, self.vault_text(plan))
        (self.drafts / f"{plan.id}.review.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"{plan.id}: German part rebuilt in {time.time() - started:.0f}s, "
              f"{len(report['template'])} template problems", flush=True)

    def write_parts(self, plan: NotePlan, resolved: list[sources.Source], vault_text: str,
                    outline: dict) -> tuple[str, str]:
        """Write the note part by part (EN), then translate part by part (DE)."""
        by_short = {source.short: source for source in resolved}
        steps = [step for step in outline.get("steps", []) if str(step.get("heading", "")).strip()]
        assigned = {str(n) for step in steps for n in step.get("sources", []) if str(n) in by_short}
        leftover = [source for source in resolved if source.short not in assigned]
        mechanism = mechanism_heading(plan.entity_type)
        en_required, en_optional = sections_for(plan.entity_type, 0)
        de_required, de_optional = sections_for(plan.entity_type, 1)
        heading_de = dict(zip(en_required + en_optional, de_required + de_optional))
        order = [heading for heading in en_required if heading != "Sources"]
        optional = ["In practice"] + (["Regulatory context"] if REGULATION_HINT.search(vault_text) else [])
        position = order.index("Key takeaway")
        order[position:position] = optional

        written: list[tuple[str, str]] = []  # (heading, English body)
        context = ""
        for heading in order:
            if heading == mechanism:
                step_names = ", ".join(str(step["heading"]).strip() for step in steps)
                body = [write_part(section_prompt(
                    plan, f"### {heading} (introduction)",
                    "One paragraph overview of how it works, then a ```text``` flow diagram with arrows (▼, ─▶), lines at most "
                    f"72 characters) showing these steps in order: {step_names}.",
                    [], resolved, vault_text, context, self.titles,
                ))]
                for step in steps:
                    required = [by_short[str(n)] for n in step.get("sources", []) if str(n) in by_short]
                    covers = "; ".join(map(str, step.get("covers", [])))
                    text = write_part(section_prompt(
                        plan, f"#### {step['heading']}",
                        f"Explain this step precisely (100-250 words): {covers}. Cover inputs and outputs, "
                        "the algorithm or data structure, design choices and their trade-offs.",
                        required, resolved, vault_text, context, self.titles,
                    ))
                    body.append(f"#### {str(step['heading']).strip()}\n\n{text}")
                written.append((heading, "\n\n".join(body)))
            else:
                required = leftover if heading in ("Comparison", "In practice") else []
                text = write_part(section_prompt(
                    plan, f"### {heading}", SECTION_TASKS.get(heading, ""), required,
                    resolved, vault_text, context, self.titles,
                ))
                leftover = [source for source in leftover if not cites(text, source)]
                written.append((heading, text))
            if heading == "TL;DR":
                context = f"TL;DR: {written[-1][1]}\nSections of the note: " + ", ".join(order)

        written = [(h, label_bare_links(unlink_citations(b, resolved), self.titles)) for h, b in written]
        english = "\n\n".join([NOTICE_EN] + [f"### {h}\n\n{b}" for h, b in written])
        return english, self.german(plan, written)

    def german(self, plan: NotePlan, written: list[tuple[str, str]]) -> str:
        en_required, en_optional = sections_for(plan.entity_type, 0)
        de_required, de_optional = sections_for(plan.entity_type, 1)
        heading_de = dict(zip(en_required + en_optional, de_required + de_optional))
        return "\n\n".join(
            [NOTICE_DE] + [f"### {heading_de[h]}\n\n{translate_section(b)}" for h, b in written]
        )

    def check(self, plan: NotePlan, note: str, resolved: list[sources.Source], vault_text: str) -> dict:
        english = note.split("\n## EN\n", 1)[1].split("\n## DE\n", 1)[0]
        german = note.split("\n## DE\n", 1)[1]
        evidence = [source.summary for source in resolved] + [source.citation for source in resolved] + [vault_text]
        known = set(planned_note_slugs()) | {path.stem for path in self.notes_directory.glob("*.md")}
        return {
            "template": check_template(note),
            "links": link_problems(note, known),
            "uncited_sources": [source.short for source in uncited(english, resolved)],
            "style": style_problems(english, resolved),
            "empty_sections": [heading for heading, body in english_sections(english) if not body.strip()],
            "numbers_not_in_evidence": unknown_numbers(english, evidence),
            "overlap_en_with_abstracts": round(originality_overlap(english, [s.summary for s in resolved]), 3),
            "overlap_de_with_vault": round(originality_overlap(german, [vault_text]), 3),
            "words_en": len(re.findall(r"\w+", english)),
            "words_de": len(re.findall(r"\w+", german)),
        }

    def review(self, plans: list[NotePlan]) -> bool:
        clean_run = True
        for plan in plans:
            report_path = self.drafts / f"{plan.id}.review.json"
            if not report_path.exists():
                print(f"{plan.id}: no draft")
                clean_run = False
                continue
            report = json.loads(report_path.read_text(encoding="utf-8"))
            copied = max(report["overlap_en_with_abstracts"], report["overlap_de_with_vault"])
            blocking = report["template"] + report["links"] + [
                f"empty section: {heading}" for heading in report.get("empty_sections", [])
            ]
            clean_run &= not blocking and copied <= ORIGINALITY_LIMIT
            print(
                f"{plan.id}: EN {report['words_en']} / DE {report['words_de']} words"
                f" | template: {len(report['template'])} | links: {len(report['links'])}"
                f" | verbatim overlap: {copied:.0%}"
                f" | uncited: {report.get('uncited_sources') or '-'}"
                f" | style: {len(report.get('style', []))}"
                f" | numbers to verify: {report['numbers_not_in_evidence'] or '-'}"
            )
            for problem in blocking + report.get("style", []):
                print(f"    - {problem}")
        return clean_run

    def accept(self, plans: list[NotePlan]) -> list[str]:
        problems = []
        for plan in plans:
            draft = self.drafts / f"{plan.id}.md"
            found = check_template(draft.read_text(encoding="utf-8"))
            if found:
                problems += [f"{plan.id}: {problem}" for problem in found]
                continue
            shutil.copyfile(draft, self.notes_directory / f"{plan.id}.md")
            print(f"{plan.id}: accepted into {self.notes_directory}")
        return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["outline", "draft", "review", "accept"])
    parser.add_argument("package", help="package config in migration/technical/")
    parser.add_argument("--notes", help="comma-separated subset of the package")
    parser.add_argument("--force", action="store_true", help="redraft existing drafts")
    parser.add_argument("--retranslate", action="store_true", help="only rebuild the German part of drafts")
    args = parser.parse_args()

    plans = load_package(args.package)
    if args.notes:
        wanted = args.notes.split(",")
        unknown = sorted(set(wanted) - {plan.id for plan in plans})
        if unknown:
            parser.error(f"not in package {args.package}: {', '.join(unknown)}")
        plans = [plan for plan in plans if plan.id in wanted]
    elif args.command == "accept":
        parser.error("accept needs --notes: accept only drafts you have reviewed")

    drafter = Drafter(configured_notes_directory())
    try:
        if args.command == "outline":
            drafter.outline(plans, args.force)
        elif args.command == "draft":
            drafter.draft(plans, args.force, args.retranslate)
        elif args.command == "review":
            return 0 if drafter.review(plans) else 1
        else:
            problems = drafter.accept(plans)
            for problem in problems:
                print(problem, file=sys.stderr)
            return 1 if problems else 0
    except (llm.LLMError, sources.SourceError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
