"""Build regulatory notes: provision summaries from the official text plus hand-written frame.

A regulatory note (docs/note-templates.md) consists of frame sections written
by a person (TL;DR, key facts, scope, timeline, enforcement, relationship to
other acts, relevance for AI development, official sources) and one summary
per article or section of the act. Each summary is one checked sentence that
the local model drafts from the official text in the source language (English
for EU acts, German for German federal law); the other language is a
translation of it, with the official headings where they exist.

    python -m app.agents.regulatory_notes summaries data-protection [--notes gdpr]
    python -m app.agents.regulatory_notes details   data-protection [--notes gdpr]
    python -m app.agents.regulatory_notes assemble  data-protection [--notes gdpr]
    python -m app.agents.regulatory_notes accept    data-protection --notes gdpr

Corrections from the review: migration/regulatory/corrections/<note>.yaml
({language: {key: summary}}), applied by `assemble`.
Frames: migration/regulatory/frames/<note>.en.md and <note>.de.md, with the
line <!-- PROVISIONS --> where the chapters and articles go. German law needs
a written German frame (German is the authentic text). For EU acts without a
written German frame, it is translated once and kept in the drafts folder.
Drafts: .knowledge-radar/drafts/regulatory/ (untracked).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from string import Template

import yaml

from app.agents import eurlex, gesetze, llm
from app.agents.legal_text import Heading, Section
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory
from app.backend.knowledge_radar.templates import REGULATORY_REQUIRED, check_template

MIGRATION = REPOSITORY_ROOT / "migration"
FRAMES = MIGRATION / "regulatory" / "frames"
CORRECTIONS = MIGRATION / "regulatory" / "corrections"
DETAILS = MIGRATION / "regulatory" / "details"
WRITER_MODEL = os.environ.get("KNOWLEDGE_RADAR_WRITER_MODEL", "qwen3:30b-a3b")
DETAIL_HEADINGS = {  # same sub-sections as the EU AI Act note (docs/note-templates.md, "Depth")
    ("en", "article"): ("What is it about?", "What does the article require?", "Who is affected?",
                        "What is not specified?", "What could this mean in practice?", "When does it apply?"),
    ("de", "article"): ("Worum geht es?", "Was verlangt der Artikel?", "Wer ist betroffen?",
                        "Was ist nicht ausdrücklich geregelt?", "Was könnte das in der Praxis bedeuten?",
                        "Ab wann gilt der Artikel?"),
    ("en", "section"): ("What is it about?", "What does the section require?", "Who is affected?",
                        "What is not specified?", "What could this mean in practice?", "When does it apply?"),
    ("de", "section"): ("Worum geht es?", "Was verlangt die Vorschrift?", "Wer ist betroffen?",
                        "Was ist nicht ausdrücklich geregelt?", "Was könnte das in der Praxis bedeuten?",
                        "Ab wann gilt die Vorschrift?"),
}
PRACTICE_RULES = {
    "en": "Start the practice sub-section with '**Possible implementation – not a legally prescribed checklist:**'.",
    "de": "Beginne den Praxis-Abschnitt mit "
          "'**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**'.",
}
PARAGRAPH_LABELS = {"en": 'e.g. "**Paragraph 3** – ..."', "de": 'z. B. "**Absatz 3** – ..."'}
DRAFTS = REPOSITORY_ROOT / ".knowledge-radar" / "drafts" / "regulatory"
PROMPTS = Path(__file__).parent / "prompts"
PROVISIONS_MARKER = "<!-- PROVISIONS -->"
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
ACRONYMS = {"AI", "EU", "GPAI", "IT", "ICT", "IKT", "KI", "EWR", "EEA", "UN"}
LANGUAGE_NAMES = {"en": "English", "de": "German"}
LANGUAGE_RULES = {
    "en": "Use the terms of the official English text of the act.",
    "de": "Verwende genau die Begriffe des amtlichen deutschen Textes; übersetze nichts ins Englische.",
}
START_RULES = {
    "en": "Start with a verb in the third person, without a subject, e.g. \"Defines ...\", \"Sets out ...\", "
          "\"Requires providers to ...\", \"Gives users the right to ...\".",
    "de": "Beginne mit einem Verb ohne Subjekt, z. B. \"Regelt ...\", \"Legt fest, ...\", "
          "\"Verpflichtet die Anbieter, ...\", \"Gibt den Nutzern das Recht, ...\".",
}
MAX_SUMMARY_WORDS = 40
PROVISION_WORD = re.compile(r"^(Article|Artikel|Art\.|§|Paragraph|Section)\s*\d", re.I)
FRAGMENT = re.compile(r"\(\d+\)|(?:^|\s)\d+\.(?:\s|$)|(?:^|\s)[a-z]\)\s")
LEGAL_TERM_HINT = {
    "de": "For data protection law e.g. controller = Verantwortlicher, processor = Auftragsverarbeiter, data subject = betroffene Person, supervisory authority = Aufsichtsbehörde.",
    "en": "For German law use established English renderings, e.g. Verantwortlicher = controller, Aufsichtsbehörde = supervisory authority.",
}
GERMAN_UNIT_LABELS = {"Teil": "Part", "Kapitel": "Chapter", "Abschnitt": "Division", "Unterabschnitt": "Subdivision"}


def render(name: str, **values: str) -> str:
    return Template((PROMPTS / name).read_text(encoding="utf-8")).substitute(values)


def load_package(package: str) -> dict[str, dict]:
    return yaml.safe_load((MIGRATION / "regulatory" / f"{package}.yaml").read_text(encoding="utf-8"))["notes"]


def provisions(spec: dict, language: str) -> list[Section]:
    """Articles/sections of the act in one language (German law: always the German text)."""
    if spec["source"] == "eurlex":
        return eurlex.parse_structure(eurlex.fetch(spec["urls"][language], language))
    return gesetze.load(spec["slug"]).sections


def summary_numbers_ok(summary: str, section: Section) -> bool:
    allowed = set(NUMBER.findall(section.text + " " + section.number + " " + section.title))
    return set(NUMBER.findall(summary)) <= allowed


def clean_summary(summary: str, section: Section) -> str:
    """Normalise a model summary: no bold (the model bolds at random), no echoed heading."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", summary)
    text = re.sub(r"\s+", " ", text).strip()
    echo = f"{section.number} {section.title}".strip()
    if echo and text.endswith(echo):
        text = text[: -len(echo)].rstrip(" .") + "."
    return text


def summary_problems(summary: str, section: Section) -> list[str]:
    """Checks for the one-sentence provision summary; empty list means accepted."""
    problems = []
    if not summary:
        return ["empty"]
    if len(summary.split()) > MAX_SUMMARY_WORDS:
        problems.append(f"longer than {MAX_SUMMARY_WORDS} words")
    if PROVISION_WORD.match(summary):
        problems.append("starts with the provision number")
    if FRAGMENT.search(summary):
        problems.append("paragraph or point numbers")
    if len(re.findall(r"[.!?](?:\s|$)", summary)) > 1:
        problems.append("more than one sentence")
    if not summary_numbers_ok(summary, section):
        problems.append("numbers not in the source")
    return problems


def check_summary(summary: str, section: Section) -> list[str]:
    """Second pass: the model compares the sentence with the official text."""
    prompt = render("provision_check.md", number=section.number, title=section.title,
                    summary=summary, text=section.text[:24000])
    try:
        answer = json.loads(llm.generate(prompt, temperature=0, json_output=True, max_tokens=300,
                                         model=llm.translation_model_name()))
    except json.JSONDecodeError:
        return ["check failed"]
    if answer.get("correct") is True:
        return []
    return [f"check: {answer.get('reason') or 'incorrect'}"]


def summarise(spec: dict, section: Section, language: str) -> tuple[str, list[str]]:
    """(summary, remaining problems) for one provision, from the official text in that language.

    Up to three attempts with rising temperature; the attempt with the fewest problems wins.
    """
    prompt = render(
        "provision_summary.md", act=spec["act"], language=LANGUAGE_NAMES[language],
        language_rules=LANGUAGE_RULES[language], start_rule=START_RULES[language],
        number=section.number, title=section.title, text=section.text[:24000],
    )
    best: tuple[str, list[str]] | None = None
    for temperature in (0.2, 0.5, 0.8):
        summary = clean_summary(
            llm.generate(prompt, temperature=temperature, max_tokens=300, model=llm.translation_model_name()), section)
        problems = summary_problems(summary, section)
        if not problems:
            problems = check_summary(summary, section)
        if best is None or len(problems) < len(best[1]):
            best = (summary, problems)
        if not problems:
            break
    return best


def translate(text: str, source: str, target: str) -> str:
    return llm.generate(
        render("translate_legal.md", source_language=LANGUAGE_NAMES[source], target_language=LANGUAGE_NAMES[target],
               term_hint=LEGAL_TERM_HINT[target], text=text),
        temperature=0.2, max_tokens=4000 + 3 * len(text.split()), model=llm.translation_model_name(),
        context_tokens=32768,
    ).strip()


def translate_titles(titles: list[str]) -> list[str]:
    """Translate German headings to English in one call; falls back to the German titles."""
    prompt = (
        "Translate these German statutory headings into English as used in official English renderings "
        "of German law. Return JSON {\"titles\": [...]} with the same number of items in the same order.\n\n"
        + json.dumps(titles, ensure_ascii=False)
    )
    answer = json.loads(llm.generate(prompt, temperature=0, json_output=True, model=llm.translation_model_name(),
                                     max_tokens=60 * len(titles) + 200, context_tokens=32768))
    translated = answer.get("titles", [])
    return translated if len(translated) == len(titles) else titles


def heading_title(title: str) -> str:
    """Sentence case for headings that the source writes in capitals, keeping acronyms."""
    if not title.isupper():
        return title
    words = title.lower().split()
    words = [w.upper() if w.upper().strip(",;:()") in ACRONYMS else w for w in words]
    text = " ".join(words)
    return text[:1].upper() + text[1:]


def heading_label(label: str) -> str:
    return " ".join(part if re.fullmatch(r"[IVXLC]+|\d+\w?", part) else part.capitalize() for part in label.split())


def item_key(item: dict) -> str:
    """Key of a provision ("26" for "§ 26", "5" for "Article 5")."""
    return item["number"].split()[-1].rstrip(".")


def detail_body(text: str) -> str:
    """Body of a detailed section: everything after an optional `####` heading line."""
    text = text.strip()
    if text.startswith("#### "):
        text = text.split("\n", 1)[1] if "\n" in text else ""
    return text.strip()


def load_details(note: str, language: str, directory: Path | None = None) -> dict[str, str]:
    """Reviewed detailed sections: migration/regulatory/details/<note>/<key>.<language>.md."""
    folder = (directory or DETAILS) / note
    return {
        path.name[: -len(f".{language}.md")]: detail_body(path.read_text(encoding="utf-8"))
        for path in sorted(folder.glob(f"*.{language}.md"))
    } if folder.is_dir() else {}


def fix_heading_terms(data: dict, terms: dict | None) -> dict:
    """Copy of the summaries with term fixes applied to the English provision and unit titles."""
    if not terms:
        return data

    def fix(text: str) -> str:
        for wrong, right in terms.items():
            text = text.replace(wrong, right)
        return text

    english = {
        key: {**item, "title": fix(item["title"]),
              "path": [[level, label, fix(title)] for level, label, title in item["path"]]}
        for key, item in data["en"].items()
    }
    return {**data, "en": english}


def template_headings(english_frame: str, german_frame: str) -> str:
    """Use the template's German headings: the n-th `###` of the German frame gets the
    German counterpart of the n-th English heading, whatever the model made of it."""
    names = dict(REGULATORY_REQUIRED)
    english = re.findall(r"^### (.+?)\s*$", english_frame, flags=re.M)
    german_headings = iter(english)

    def replace(match: re.Match) -> str:
        source = next(german_headings, None)
        return f"### {names[source]}" if source in names else match.group(0)

    if len(re.findall(r"^### ", german_frame, flags=re.M)) != len(english):
        return german_frame  # structure differs; the template check will report it
    return re.sub(r"^### .+$", replace, german_frame, flags=re.M)


class Builder:
    def __init__(self, package: str, notes_directory: Path, drafts: Path = DRAFTS):
        self.package = package
        self.specs = load_package(package)
        self.notes_directory = notes_directory
        self.drafts = drafts
        mapping = yaml.safe_load((MIGRATION / "vault-mapping.yaml").read_text(encoding="utf-8"))["notes"]
        self.mapping = {entry["id"]: entry for entry in mapping.values() if not entry.get("hub")}

    def summaries_path(self, note: str) -> Path:
        return self.drafts / note / "summaries.json"

    # -- step 1: provision summaries ------------------------------------------------
    def summaries(self, note: str, force: bool = False) -> None:
        spec = self.specs[note]
        path = self.summaries_path(note)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() and not force else {"en": {}, "de": {}}
        german_law = spec["source"] == "gesetze"
        source_language = "de" if german_law else "en"
        started = time.time()

        def save() -> None:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

        # Summaries come from an authentic text: for EU acts both language versions are
        # authentic, so each language is summarised from its own text. German law exists
        # only in German; its English summaries are translations, reviewed afterwards.
        languages = [source_language] if german_law or spec.get("german_summaries") == "translate" else ["en", "de"]
        for language in languages:
            for section in provisions(spec, language):
                if section.key in data[language]:
                    continue
                summary, problems = summarise(spec, section, language)
                data[language][section.key] = {
                    "number": section.number, "title": section.title, "summary": summary,
                    "problems": problems, "path": [[h.level, h.label, h.title] for h in section.path],
                }
                save()

        if german_law:
            self.english_from_german(data)
        elif "de" not in languages:
            self.german_from_english(spec, data, save)
        save()
        flagged = [f"{lang}:{key} ({', '.join(item['problems'])})"
                   for lang in data for key, item in data[lang].items() if item["problems"]]
        print(f"{note}: {len(data[source_language])} provisions in {time.time() - started:.0f}s; "
              f"flagged: {flagged or '-'}", flush=True)

    def german_from_english(self, spec: dict, data: dict, save) -> None:
        """German summaries for an EU act: translated English summary, official German headings."""
        for section in provisions(spec, "de"):
            english = data["en"].get(section.key)
            if english is None or section.key in data["de"]:
                continue
            summary = re.sub(r"\s+", " ", translate(english["summary"], "en", "de"))
            problems = list(english["problems"])
            if set(NUMBER.findall(summary)) != set(NUMBER.findall(english["summary"])):
                problems.append("numbers changed in translation")
            data["de"][section.key] = {
                "number": section.number, "title": section.title, "summary": summary,
                "problems": problems, "path": [[h.level, h.label, h.title] for h in section.path],
            }
            save()

    def english_from_german(self, data: dict) -> None:
        german = data["de"]
        missing = [key for key in german if key not in data["en"]]
        if not missing:
            return
        heading_titles = sorted({title for key in missing for _, _, title in german[key]["path"]})
        section_titles = [german[key]["title"] for key in missing]
        translated = translate_titles(heading_titles + section_titles)
        heading_map = dict(zip(heading_titles, translated[: len(heading_titles)]))
        for key, title in zip(missing, translated[len(heading_titles):]):
            item = german[key]
            summary = re.sub(r"\s+", " ", translate(item["summary"], "de", "en"))
            problems = list(item["problems"])
            if set(NUMBER.findall(summary)) != set(NUMBER.findall(item["summary"])):
                problems.append("numbers changed in translation")
            data["en"][key] = {
                "number": item["number"], "title": title, "summary": summary, "problems": problems,
                "path": [[level, " ".join(GERMAN_UNIT_LABELS.get(p, p) for p in label.split()), heading_map.get(t, t)]
                         for level, label, t in item["path"]],
            }

    def apply_corrections(self, note: str) -> None:
        """Apply reviewed corrections (migration/regulatory/corrections/<note>.yaml) to the summaries.

        A corrected summary replaces the model's text and its problems; the other
        language is re-translated from it unless the file corrects that one too.
        Applied corrections are remembered, so a second run does not translate again.
        """
        corrections_file = CORRECTIONS / f"{note}.yaml"
        if not corrections_file.exists():
            return
        corrections = yaml.safe_load(corrections_file.read_text(encoding="utf-8")) or {}
        spec = self.specs[note]
        source_language = "de" if spec["source"] == "gesetze" else "en"
        # Only a language that was produced by translation follows corrections of the other one;
        # for EU acts summarised from both official texts, each language stands on its own.
        translated_counterpart = spec["source"] == "gesetze" or spec.get("german_summaries") == "translate"
        path = self.summaries_path(note)
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = 0
        for language, entries in corrections.items():
            other = "de" if language == "en" else "en"
            for key, entry in (entries or {}).items():
                key = str(key)
                item = data[language][key]
                # An entry is the corrected summary, or {summary, title} to fix a translated heading too.
                summary = entry["summary"] if isinstance(entry, dict) else entry
                title = entry.get("title") if isinstance(entry, dict) else None
                if item.get("reviewed") and item["summary"] == summary and (not title or item["title"] == title):
                    continue
                if title:
                    item["title"] = title
                item.update(summary=summary, problems=[], reviewed=True)
                # Translate only from the source language, never into it.
                if (translated_counterpart and language == source_language
                        and key not in {str(k) for k in (corrections.get(other) or {})}):
                    translated = re.sub(r"\s+", " ", translate(summary, language, other))
                    data[other][key].update(summary=translated, reviewed=True, problems=(
                        [] if set(NUMBER.findall(translated)) == set(NUMBER.findall(summary))
                        else ["numbers changed in translation"]))
                changed += 1
                path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{note}: {changed} corrections applied", flush=True)

    # -- detailed sections of important provisions ------------------------------------
    def details(self, note: str, keys: list[str] | None = None, force: bool = False) -> None:
        """Draft detailed sections in the source language only, from the official text.

        Drafts go to the drafts folder; after review, the final sections (both
        languages) are stored in migration/regulatory/details/<note>/<key>.<lang>.md.
        """
        from app.agents import regulatory_articles

        spec = self.specs[note]
        language = "de" if spec["source"] == "gesetze" else "en"
        unit = "section" if spec["source"] == "gesetze" else "article"
        headings = DETAIL_HEADINGS[(language, unit)]
        data = json.loads(self.summaries_path(note).read_text(encoding="utf-8"))
        sections = {s.key: s for s in provisions(spec, language)}
        ai_act = (self.notes_directory / "eu-ai-act.md").read_text(encoding="utf-8")
        example = regulatory_articles.article_sections(ai_act, regulatory_articles.LANGUAGES[language])["4"]
        example = example.split("\n", 1)[1]
        target_folder = self.drafts / note / "details"
        target_folder.mkdir(parents=True, exist_ok=True)

        for key in keys or [str(k) for k in spec["detailed"]]:
            target = target_folder / f"{key}.{language}.md"
            if target.exists() and not force:
                continue
            section, item = sections[key], data[language][key]
            dash = " — " if language == "en" else " – "
            prompt = render(
                "regulatory_article.md",
                act_context=spec["act"], provision=section.number, language=LANGUAGE_NAMES[language],
                heading_requires=headings[1], heading_open=headings[3], heading_applies=headings[5],
                paragraph_label=PARAGRAPH_LABELS[language],
                title=f"#### {item['number']}{dash}{item['title']}",
                headings="\n".join(f"##### {heading}" for heading in headings),
                practice_rule=PRACTICE_RULES[language], application=spec["detailed"][key],
                language_rules=LANGUAGE_RULES[language] + " Keep established English technical terms "
                               "of AI and IT untranslated in German text.",
                example=example, existing=item["summary"], official=section.text,
            )
            started = time.time()
            draft = llm.generate(prompt, temperature=0.6, sampling={"top_p": 0.95, "top_k": 20}, think=True,
                                 max_tokens=12000, context_tokens=32768, model=WRITER_MODEL, timeout=1800)
            draft = re.sub(r"^```(?:markdown)?\n|\n```$", "", draft.strip()).strip() + "\n"
            target.write_text(draft, encoding="utf-8")
            missing = [h for h in headings if f"##### {h}" not in draft]
            body = detail_body(draft).split(f"##### {headings[5]}")[0]
            allowed = set(NUMBER.findall(section.text + " " + section.number))
            numbers = sorted({n for n in NUMBER.findall(body) if n not in allowed})
            print(f"{note} {section.number} ({language}): {len(draft.split())} words in "
                  f"{time.time() - started:.0f}s | missing sub-headings: {missing or '-'} | "
                  f"numbers not in source: {numbers or '-'}", flush=True)

    # -- step 2: assemble the note --------------------------------------------------
    def provisions_block(self, data: dict, language: str, details: dict[str, str] | None = None) -> str:
        """Chapters and provisions; a reviewed detailed section replaces the one-sentence summary."""
        dash = " — " if language == "en" else " – "
        lines: list[str] = []
        current: list[tuple] = []
        for item in data[language].values():
            path = [tuple(p) for p in item["path"]]
            for depth, (level, label, title) in enumerate(path):
                if depth < len(current) and current[depth] == (level, label, title):
                    continue
                heading = f"{heading_label(label)}{dash}{heading_title(title)}" if title else heading_label(label)
                lines.append(f"### {heading}" if depth == 0 else f"**{heading}**")
                lines.append("")
            current = path
            title = f"{dash}{item['title']}" if item["title"] else ""
            body = (details or {}).get(item_key(item)) or item["summary"]
            lines += [f"#### {item['number']}{title}", "", body, ""]
        return "\n".join(lines).strip()

    def german_frame(self, note: str, english_frame: str, force: bool = False) -> str:
        written = FRAMES / f"{note}.de.md"
        if written.exists():
            # Written German frame (required for German law, where German is the authentic text).
            return written.read_text(encoding="utf-8")
        if self.specs[note]["source"] == "gesetze":
            raise ValueError(f"{note}: German law needs a written German frame ({written.name}), not a translation")
        target = self.drafts / note / "frame.de.md"
        if target.exists() and not force:
            return template_headings(english_frame, target.read_text(encoding="utf-8"))
        parts = re.split(r"(?=^### )", english_frame, flags=re.M)
        german = "\n\n".join(
            part if not part.strip() or part.strip() == PROVISIONS_MARKER else translate(part, "en", "de")
            for part in parts
        )
        german = re.sub(r"^> \*\*Important notice:\*\*.*$", (
            "> **Wichtiger Hinweis:** Diese Seite ist eine LLM-generierte Zusammenfassung. Sie kann unvollständig, "
            "veraltet oder falsch sein. Sie ist keine Rechtsberatung und entfaltet keine rechtliche Wirkung; "
            "maßgeblich sind allein die amtlich veröffentlichten Texte."), german, count=1, flags=re.M)
        target.write_text(german, encoding="utf-8")
        return template_headings(english_frame, german)

    def assemble(self, note: str) -> Path:
        spec = self.specs[note]
        entry = self.mapping[note]
        self.apply_corrections(note)
        data = json.loads(self.summaries_path(note).read_text(encoding="utf-8"))
        english_frame = (FRAMES / f"{note}.en.md").read_text(encoding="utf-8")
        german_frame = self.german_frame(note, english_frame)
        frontmatter = {
            "title_en": entry["title_en"], "title_de": entry["title_de"], "entity_type": entry["entity_type"],
            **spec["frontmatter"], "sources": spec["sources"],
        }
        english = english_frame.replace(PROVISIONS_MARKER, self.provisions_block(
            fix_heading_terms(data, spec.get("english_heading_terms")), "en", load_details(note, "en")))
        german = german_frame.replace(PROVISIONS_MARKER, self.provisions_block(data, "de", load_details(note, "de")))
        note_text = (
            "---\n" + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False) + "---\n\n"
            f"## EN\n\n{english.strip()}\n\n## DE\n\n{german.strip()}\n"
        )
        target = self.drafts / f"{note}.md"
        target.write_text(note_text, encoding="utf-8")
        problems = check_template(note_text)
        print(f"{note}: assembled, {len(problems)} template problems", flush=True)
        for problem in problems:
            print(f"    - {problem}")
        return target

    def accept(self, note: str) -> list[str]:
        draft = self.drafts / f"{note}.md"
        problems = check_template(draft.read_text(encoding="utf-8"))
        if not problems:
            shutil.copyfile(draft, self.notes_directory / f"{note}.md")
            print(f"{note}: accepted into {self.notes_directory}")
        return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["summaries", "details", "assemble", "accept"])
    parser.add_argument("package")
    parser.add_argument("--notes", help="comma-separated subset")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    builder = Builder(args.package, configured_notes_directory())
    notes = args.notes.split(",") if args.notes else list(builder.specs)
    if args.command == "accept" and not args.notes:
        parser.error("accept needs --notes: accept only reviewed notes")
    try:
        problems = []
        for note in notes:
            if args.command == "summaries":
                builder.summaries(note, args.force)
            elif args.command == "details":
                if builder.specs[note].get("detailed"):
                    builder.details(note, force=args.force)
            elif args.command == "assemble":
                builder.assemble(note)
            else:
                problems += [f"{note}: {p}" for p in builder.accept(note)]
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1 if problems else 0
    except (llm.LLMError, eurlex.EurLexError, gesetze.GesetzeError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
