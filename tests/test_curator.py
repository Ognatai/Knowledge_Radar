import datetime as dt
import json
from datetime import date, datetime, timezone

from app.agents.monitoring.curator import (
    Draft,
    draft_new_note,
    draft_update,
    english_part,
    full_citation,
    remove_unknown_links,
    review_report,
    slugify,
)
from app.agents.monitoring.findings import Finding
from app.agents.monitoring.quality import ClaimCheck, OriginalityReport
from app.agents.monitoring.source_texts import SourceText
from app.backend.knowledge_radar.templates import check_template
from tests.test_templates import technical

NOW = datetime(2026, 10, 10, tzinfo=timezone.utc)


def finding(identifier="arxiv:2610.05163", authors=("Ada Lovelace", "Alan Turing", "Grace Hopper")):
    return Finding(
        id=identifier,
        source="arXiv",
        category="arxiv",
        url=f"https://arxiv.org/abs/{identifier.split(':')[1]}",
        title="Blocking at the Boundary.",
        summary="Abstract.",
        published=date(2026, 10, 7),
        authors=list(authors),
        tier="preprint",
        source_kind="primary_research",
        fetched_at=NOW,
    )


def source(identifier="arxiv:2610.05163"):
    return SourceText(
        identifier,
        f"https://arxiv.org/abs/{identifier.split(':')[1]}",
        "Lovelace et al. (2026)",
        "Blocking at the Boundary",
        "Prompt injection hides instructions in data.\nStaged attacks span several steps.",
        True,
    )


def embed(texts):
    return [[1.0, float(len(text) % 7)] for text in texts]


def test_slugs_are_lowercase_ascii_with_hyphens():
    assert slugify("Prompt Injection (LLMs)") == "prompt-injection-llms"


def test_unknown_wikilinks_become_plain_text():
    text = "See [[agentic-ai|agentic AI]], [[ghost-note|a ghost]] and [[ghost]]; tables use [[agentic-ai\\|agents]]."

    assert remove_unknown_links(text, {"agentic-ai"}) == (
        "See [[agentic-ai|agentic AI]], a ghost and ghost; tables use [[agentic-ai\\|agents]]."
    )


def test_full_citations_follow_the_notes_style():
    assert full_citation(source(), finding()) == (
        "Lovelace, A. et al. (2026). *Blocking at the Boundary.* [arXiv:2610.05163](https://arxiv.org/abs/2610.05163)"
    )
    feed = Finding(**{**finding(identifier="rss:1", authors=()).__dict__, "source": "OpenAI News", "url": "https://openai.com/x"})
    assert full_citation(source(), feed).startswith("OpenAI News (2026). *Blocking at the Boundary.* [Link](https://openai.com/x)")


def fake_generate(prompt, json_schema=None, **options):
    if json_schema and "steps" in json_schema["properties"]:
        return json.dumps(
            {
                "title_en": "Prompt Injection",
                "title_de": "Prompt Injection",
                "entity_type": "Concept",
                "aliases": ["PI"],
                "steps": ["1. Mechanism", "2. Defences"],
            }
        )
    if prompt.startswith("Translate"):
        return "Deutscher Text mit [[agentic-ai|Agenten]] und [[unknown|Unbekanntem]]."
    return "## Stray heading\nEnglish text (Lovelace et al., 2026) with [[agentic-ai|agents]] and [[unknown|nothing]]."


def test_new_note_drafts_follow_the_technical_template():
    text, outline = draft_new_note(
        "prompt injection",
        [finding()],
        [source()],
        [("agentic-ai", "Agentic AI")],
        {"agentic-ai"},
        embed,
        generate=fake_generate,
    )

    assert check_template(text) == []
    assert outline["entity_type"] == "Concept"
    assert "#### 1. Mechanism" in text and "### Funktionsweise" in text
    assert "[[unknown" not in text and "[[agentic-ai|agents]]" in text
    assert "Stray heading" not in text
    assert "aliases:\n- PI\n" in text
    assert "- Lovelace, A. et al. (2026). *Blocking at the Boundary.*" in english_part(text)


def test_update_drafts_append_a_dated_entry_with_a_link():
    def generate(prompt, json_schema=None, **options):
        if prompt.startswith("Translate"):
            return json.dumps({"title": "Gestaffelte Angriffe", "body": "Angriffe über mehrere Schritte (Lovelace et al., 2026)."})
        return json.dumps({"title": "Staged attacks", "body": "Attacks span several steps (Lovelace et al., 2026)."})

    text, english = draft_update(technical(), "Example", "Summary.", source(), dt.date(2026, 10, 12), embed, generate=generate)

    assert "#### 2026-10-12 — Staged attacks\nAttacks span several steps (Lovelace et al., 2026). [arXiv](https://arxiv.org/abs/2610.05163)" in text
    assert "#### 2026-10-12 — Gestaffelte Angriffe" in text
    assert english.endswith("[arXiv](https://arxiv.org/abs/2610.05163)")
    assert check_template(text) == []


def test_review_report_lists_problems_for_the_reviewer():
    draft = Draft("prompt-injection", "new_topic", "", [source()])
    draft.template_problems = ["EN: missing sections: Comparison."]
    draft.originality = OriginalityReport(0.2, ["prompt injection hides instructions in data that"])
    draft.checks = [ClaimCheck("Supported claim here.", True, "x"), ClaimCheck("It was invented in 1990.", False, "")]

    report = review_report(draft)

    assert "(full text)" in report
    assert "- EN: missing sections: Comparison." in report
    assert "## Originality: FAILED (20% copied 8-grams)" in report
    assert "## Faithfulness: 1 of 2 sentences unsupported\n- It was invented in 1990." in report
