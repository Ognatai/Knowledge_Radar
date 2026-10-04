import io
import json

import pytest

from app.agents import eurlex, llm, regulatory_articles as ra

PAGE = """<html><body>
<div id="cpt_I"><p>CHAPTER I GENERAL PROVISIONS</p>
<div class="eli-subdivision" id="art_1"><p>Article 1 Subject matter</p><p>&#9660;M1 1. This Regulation lays down rules. 2. It applies from 2025.</p></div>
<div class="eli-subdivision" id="art_4a"><p>Article 4a Bias</p><p>1. Processing is allowed for 3 purposes.</p></div>
</div>
<div id="cpt_II"><p>CHAPTER II</p>
<div class="eli-subdivision" id="art_5"><p>Article 5 Prohibitions</p><p>1. Fines up to EUR 35 000 000.</p></div>
</div>
<div class="eli-subdivision" id="fnp_1"><p>Done at Brussels.</p></div>
<div id="anx_I"><p>ANNEX I</p></div>
</body></html>"""

NOTE = """---
title_en: Act
title_de: Gesetz
entity_type: Regulation
sources:
  - https://example.org/act
---

## EN

### Chapter I — General

#### Article 1 — Subject matter

Old summary of Article 1.

#### Article 4a — Bias

##### What is it about?
Style example.

### Chapter II — Prohibitions

#### Article 5 — Prohibitions

Old summary of Article 5.

## DE

### Kapitel I – Allgemeines

#### Artikel 1 – Gegenstand

Alte Zusammenfassung.

#### Artikel 4a – Bias

##### Worum geht es?
Stilbeispiel.

#### Artikel 5 – Verbote

Alte Zusammenfassung von Artikel 5.
"""


def test_split_articles_stops_at_structural_units_and_drops_markers():
    articles = eurlex.split_articles(PAGE)

    assert list(articles) == ["1", "4a", "5"]
    assert articles["1"] == "Article 1 Subject matter 1. This Regulation lays down rules. 2. It applies from 2025."
    assert "CHAPTER II" not in articles["4a"]
    assert "Brussels" not in articles["5"] and "ANNEX" not in articles["5"]


def test_split_articles_rejects_pages_without_articles():
    with pytest.raises(eurlex.EurLexError):
        eurlex.split_articles("<html>blocked</html>")


def test_article_sections_per_language():
    en = ra.article_sections(NOTE, ra.LANGUAGES["en"])
    de = ra.article_sections(NOTE, ra.LANGUAGES["de"])

    assert list(en) == ["1", "4a", "5"]
    assert en["4a"].startswith("#### Article 4a — Bias") and "Style example." in en["4a"]
    assert de["5"] == "#### Artikel 5 – Verbote\n\nAlte Zusammenfassung von Artikel 5."


def test_unknown_numbers_ignore_the_application_section():
    language = ra.LANGUAGES["en"]
    draft = (
        "#### Article 5 — X\n##### What does the article require?\nFines up to **EUR 35 000 000**"
        " or 7 %.\n##### When does it apply?\nFrom **2 February 2025**.\n"
    )

    assert ra.unknown_numbers(draft, "Fines up to EUR 35 000 000.", language) == ["7"]


def test_factual_issues_only_cover_factual_subsections():
    language = ra.LANGUAGES["en"]
    draft = (
        "#### Article 1 — X\n##### What is it about?\nThe article covers banks only.\n"
        "##### What is not specified?\nNo format is prescribed.\n"
    )
    check = {"issues": [
        {"statement": "The article covers banks only.", "problem": "not in text"},
        {"statement": "No format is prescribed.", "problem": "not stated"},
    ]}

    assert [issue["statement"] for issue in ra.factual_issues(draft, check, language)] == [
        "The article covers banks only."
    ]


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "act.md").write_text(NOTE, encoding="utf-8")
    config = ra.ActConfig(
        note="act",
        act_context="the Example Act (Regulation (EU) 2099/1)",
        sources={"en": "https://example.org/en", "de": "https://example.org/de"},
        style_example="4a",
        detailed_articles={"5": "1 January 2030", "1": "1 January 2030"},
    )
    monkeypatch.setattr(eurlex, "fetch_html", lambda url, **_: PAGE)
    return ra.Workspace(config, notes, tmp_path / "drafts")


def test_draft_review_and_merge(workspace, monkeypatch):
    prompts = []

    def fake_generate(prompt, **kwargs):
        prompts.append(prompt)
        if kwargs.get("json_output"):
            return json.dumps({"issues": [], "supported": True})
        heading = "#### Article 5 — Prohibitions" if "Article 5 in English" in prompt else "#### Artikel 5 – Verbote"
        return f"```markdown\n{heading}\n\n##### What is it about?\nFines up to **EUR 35 000 000**.\n```"

    monkeypatch.setattr(llm, "generate", fake_generate)
    workspace.draft(["5"], [ra.LANGUAGES["en"], ra.LANGUAGES["de"]])

    draft_prompt = prompts[0]
    assert "Article 5 Prohibitions 1. Fines up to EUR 35 000 000." in draft_prompt
    assert "In \"When does it apply?\" state: 1 January 2030." in draft_prompt
    assert "Style example." in draft_prompt and "$" not in draft_prompt.split("OFFICIAL ARTICLE TEXT")[0]
    assert workspace.draft_path("5", ra.LANGUAGES["en"]).read_text(encoding="utf-8").startswith(
        "#### Article 5 — Prohibitions\n"
    )

    workspace.merge([ra.LANGUAGES["en"], ra.LANGUAGES["de"]])
    merged = workspace.note_path.read_text(encoding="utf-8")
    assert "Old summary of Article 5." not in merged
    assert merged.count("Fines up to **EUR 35 000 000**.") == 2
    assert "Old summary of Article 1." in merged  # no draft, unchanged


def test_merge_refuses_changed_headings(workspace):
    language = ra.LANGUAGES["en"]
    workspace.drafts.mkdir(parents=True)
    workspace.draft_path("5", language).write_text("#### Article 5 — Renamed\nText\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="heading line differs"):
        workspace.merge([language])


def test_llm_generate_sends_model_and_disables_thinking(monkeypatch):
    sent = {}

    def fake_urlopen(request, timeout):
        sent.update(json.loads(request.data))
        return io.BytesIO(json.dumps({"response": " answer "}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("KNOWLEDGE_RADAR_MODEL", "test-model")

    assert llm.generate("hello", json_output=True) == "answer"
    assert sent["model"] == "test-model" and sent["think"] is False and sent["format"] == "json"


def test_llm_errors_are_wrapped(monkeypatch):
    def failing_urlopen(request, timeout):
        raise OSError("connection refused")

    monkeypatch.setattr(llm.urllib.request, "urlopen", failing_urlopen)

    with pytest.raises(llm.LLMError, match="connection refused"):
        llm.generate("hello")
