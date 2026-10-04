"""Draft, review and merge detailed article sections of a regulatory note.

Detailed sections (docs/note-templates.md, "Depth") are drafted by the local
LLM from the official article text, checked deterministically, reviewed by a
human and only then merged into the note. Per act, a config file in
`migration/regulatory/<note>.yaml` lists the source URLs, the important
articles and their application dates.

    python -m app.agents.regulatory_articles draft  eu-ai-act [--articles 5,6] [--lang en,de]
    python -m app.agents.regulatory_articles review eu-ai-act
    python -m app.agents.regulatory_articles merge  eu-ai-act

Drafts are written to `.knowledge-radar/drafts/<note>/` (untracked).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from string import Template

import yaml

from app.agents import eurlex, llm
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory
from app.backend.knowledge_radar.templates import check_template

CONFIG_DIRECTORY = REPOSITORY_ROOT / "migration" / "regulatory"
DRAFT_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "drafts"
PROMPTS = Path(__file__).parent / "prompts"
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    section: str  # "EN" / "DE" part of the note
    article_word: str
    headings: tuple[str, ...]  # what · requires · who · open · practice · applies
    paragraph_label: str
    practice_rule: str
    rules: str


LANGUAGES = {
    "en": Language(
        "en", "English", "EN", "Article",
        ("What is it about?", "What does the article require?", "Who is affected?",
         "What is not specified?", "What could this mean in practice?", "When does it apply?"),
        'e.g. "**Paragraph 3** – ..."',
        "Start the practice sub-section with "
        "'**Possible implementation – not a legally prescribed checklist:**'.",
        "",
    ),
    "de": Language(
        "de", "German", "DE", "Artikel",
        ("Worum geht es?", "Was verlangt der Artikel?", "Wer ist betroffen?",
         "Was ist nicht ausdrücklich geregelt?", "Was könnte das in der Praxis bedeuten?",
         "Ab wann gilt der Artikel?"),
        'z. B. "**Absatz 3** – ..."',
        "Beginne den Praxis-Abschnitt mit "
        "'**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**'.",
        "Use the legal terms exactly as in the official German text. Keep established English "
        "technical terms untranslated (e.g. Machine Learning, Logging, Prompt). Write dates in "
        "German form (e.g. 2. Dezember 2027).",
    ),
}


@dataclass(frozen=True)
class ActConfig:
    note: str
    act_context: str
    sources: dict[str, str]
    style_example: str
    detailed_articles: dict[str, str]

    @classmethod
    def load(cls, note: str, directory: Path = CONFIG_DIRECTORY) -> ActConfig:
        raw = yaml.safe_load((directory / f"{note}.yaml").read_text(encoding="utf-8"))
        return cls(
            note=raw["note"],
            act_context=raw["act_context"],
            sources=raw["sources"],
            style_example=str(raw["style_example"]),
            detailed_articles={str(key): value for key, value in raw["detailed_articles"].items()},
        )


def language_part(note_text: str, language: Language) -> str:
    english, german = note_text.split("\n## DE\n", 1)
    return english if language.section == "EN" else german


def article_sections(note_text: str, language: Language) -> dict[str, str]:
    """Existing `#### Article N — Title` sections (heading line + body) of one language."""
    pattern = (
        rf"^#### {language.article_word} (\d+[a-z]?) [—–-][^\n]*\n.*?(?=^#{{2,4}} |\Z)"
    )
    part = language_part(note_text, language)
    return {
        match.group(1): match.group(0).strip()
        for match in re.finditer(pattern, part, re.M | re.S)
    }


def render(template_name: str, **values: str) -> str:
    return Template((PROMPTS / template_name).read_text(encoding="utf-8")).substitute(values)


def draft_prompt(config: ActConfig, article: str, language: Language, official: str,
                 existing: str, example: str) -> str:
    headings = language.headings
    return render(
        "regulatory_article.md",
        act_context=config.act_context,
        article=article,
        language=language.name,
        heading_requires=headings[1],
        heading_open=headings[3],
        heading_applies=headings[5],
        paragraph_label=language.paragraph_label,
        title=existing.splitlines()[0],
        headings="\n".join(f"##### {heading}" for heading in headings),
        practice_rule=language.practice_rule,
        application=config.detailed_articles[article],
        language_rules=language.rules,
        example=example,
        existing=existing,
        official=official,
    )


def clean_draft(answer: str) -> str:
    return re.sub(r"^```(?:markdown)?\n|\n```$", "", answer.strip()).strip() + "\n"


def unknown_numbers(draft: str, official: str, language: Language, allowed_extra: str = "") -> list[str]:
    """Numbers in the draft (outside the application sub-section) absent from the source."""
    body = draft.split(f"##### {language.headings[5]}")[0]
    if body.startswith("#### "):
        body = body.split("\n", 1)[1] if "\n" in body else ""  # the heading carries the article number
    allowed = set(NUMBER.findall(official)) | set(NUMBER.findall(allowed_extra))
    return sorted({number for number in NUMBER.findall(body) if number not in allowed}, key=len)


def missing_headings(draft: str, language: Language) -> list[str]:
    return [heading for heading in language.headings if f"##### {heading}" not in draft]


def factual_issues(draft: str, check: dict, language: Language) -> list[dict]:
    """LLM-check issues located in the factual sub-sections (what · requires · who)."""
    parts = re.split(r"^##### ", draft, flags=re.M)[1:]
    factual = "\n".join(
        part.partition("\n")[2] for part in parts if part.partition("\n")[0].strip() in language.headings[:3]
    )
    return [
        issue for issue in check.get("issues", [])
        if isinstance(issue, dict) and issue.get("statement", "")[:40] in factual
    ]


class Workspace:
    def __init__(self, config: ActConfig, notes_directory: Path, drafts_root: Path = DRAFT_DIRECTORY):
        self.config = config
        self.note_path = notes_directory / f"{config.note}.md"
        self.drafts = drafts_root / config.note

    def draft_path(self, article: str, language: Language) -> Path:
        return self.drafts / f"art{article}.{language.code}.md"

    def check_path(self, article: str, language: Language) -> Path:
        return self.drafts / f"art{article}.{language.code}.check.json"

    def official_articles(self, language: Language) -> dict[str, str]:
        return eurlex.split_articles(eurlex.fetch_html(self.config.sources[language.code]))

    def draft(self, articles: list[str], languages: list[Language], force: bool = False) -> None:
        self.drafts.mkdir(parents=True, exist_ok=True)
        note_text = self.note_path.read_text(encoding="utf-8")
        for language in languages:
            official = self.official_articles(language)
            sections = article_sections(note_text, language)
            example = sections[self.config.style_example].split("\n", 1)[1]
            for article in articles:
                target = self.draft_path(article, language)
                if target.exists() and not force:
                    continue
                started = time.time()
                answer = llm.generate(draft_prompt(
                    self.config, article, language, official[article], sections[article], example,
                ))
                target.write_text(clean_draft(answer), encoding="utf-8")
                check = llm.generate(
                    render("faithfulness_check.md", official=official[article], draft=answer),
                    temperature=0,
                    json_output=True,
                )
                self.check_path(article, language).write_text(check, encoding="utf-8")
                print(f"article {article} {language.code}: drafted in {time.time() - started:.0f}s", flush=True)

    def review(self, languages: list[Language]) -> bool:
        """Print a review table; return True if no deterministic check failed."""
        clean = True
        for language in languages:
            official = self.official_articles(language)
            for article in self.config.detailed_articles:
                path = self.draft_path(article, language)
                if not path.exists():
                    print(f"article {article:>4} {language.code}: no draft")
                    clean = False
                    continue
                draft = path.read_text(encoding="utf-8")
                numbers = unknown_numbers(draft, official[article], language, self.config.act_context)
                headings = missing_headings(draft, language)
                try:
                    check = json.loads(self.check_path(article, language).read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    check = {}
                issues = factual_issues(draft, check, language)
                clean &= not numbers and not headings
                print(
                    f"article {article:>4} {language.code}: {len(draft.split()):4} words"
                    f" | numbers not in source: {numbers or '-'}"
                    f" | missing sub-headings: {headings or '-'}"
                    f" | LLM issues in factual parts: {len(issues)}"
                )
                for issue in issues:
                    print(f"      - {issue.get('statement', '')[:160]}")
        return clean

    def merge(self, languages: list[Language]) -> list[str]:
        """Replace the article sections with the reviewed drafts; return template problems."""
        note_text = self.note_path.read_text(encoding="utf-8")
        english, german = note_text.split("\n## DE\n", 1)
        parts = {"EN": english, "DE": german}
        for language in languages:
            sections = article_sections(note_text, language)
            for article in self.config.detailed_articles:
                path = self.draft_path(article, language)
                if not path.exists():
                    continue
                draft = path.read_text(encoding="utf-8").strip()
                old = sections[article]
                if draft.splitlines()[0] != old.splitlines()[0]:
                    raise SystemExit(f"{path.name}: heading line differs from the note: {draft.splitlines()[0]!r}")
                parts[language.section] = parts[language.section].replace(old, draft, 1)
        merged = parts["EN"] + "\n## DE\n" + parts["DE"]
        self.note_path.write_text(merged, encoding="utf-8", newline="\n")
        return check_template(merged)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["draft", "review", "merge"])
    parser.add_argument("note", help="note slug with a config in migration/regulatory/")
    parser.add_argument("--articles", help="comma-separated subset (default: all configured)")
    parser.add_argument("--lang", default="en,de")
    parser.add_argument("--force", action="store_true", help="redraft existing drafts")
    args = parser.parse_args()

    config = ActConfig.load(args.note)
    workspace = Workspace(config, configured_notes_directory())
    languages = [LANGUAGES[code] for code in args.lang.split(",")]
    articles = args.articles.split(",") if args.articles else list(config.detailed_articles)
    unknown = [article for article in articles if article not in config.detailed_articles]
    if unknown:
        parser.error(f"articles not configured as detailed: {', '.join(unknown)}")

    try:
        if args.command == "draft":
            workspace.draft(articles, languages, args.force)
        elif args.command == "review":
            return 0 if workspace.review(languages) else 1
        else:
            problems = workspace.merge(languages)
            for problem in problems:
                print(f"template: {problem}", file=sys.stderr)
            return 1 if problems else 0
    except (llm.LLMError, eurlex.EurLexError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
