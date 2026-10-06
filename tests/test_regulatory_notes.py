from app.agents import regulatory_notes as rn
from app.agents.legal_text import Heading, Section

SECTION = Section(
    number="Article 83", title="General conditions for imposing administrative fines",
    text="4. Infringements shall be subject to fines up to 10 000 000 EUR, or up to 2 % of turnover.",
    path=(Heading(1, "CHAPTER VIII", "REMEDIES, LIABILITY AND PENALTIES"),),
)


def test_summary_problems_accepts_one_short_sentence():
    assert rn.summary_problems("Sets out the conditions for administrative fines of up to 2 % of turnover.", SECTION) == []


def test_summary_problems_flags_typical_model_errors():
    assert "starts with the provision number" in rn.summary_problems("Article 83 sets out fines.", SECTION)
    assert "paragraph or point numbers" in rn.summary_problems("Sets out fines. (1) Fines apply", SECTION)
    assert "more than one sentence" in rn.summary_problems("Sets out fines. It applies to all.", SECTION)
    assert "numbers not in the source" in rn.summary_problems("Sets out fines of up to 5 % of turnover.", SECTION)
    assert any("longer than" in p for p in rn.summary_problems("Sets out " + "many " * 45 + "fines.", SECTION))
    assert rn.summary_problems("", SECTION) == ["empty"]


def test_clean_summary_removes_bold_and_echoed_heading():
    raw = "Sets out **fines** for infringements. Article 83 General conditions for imposing administrative fines"
    assert rn.clean_summary(raw, SECTION) == "Sets out fines for infringements."


def test_heading_title_sentence_cases_capitals_but_keeps_acronyms():
    assert rn.heading_title("REMEDIES, LIABILITY AND PENALTIES") == "Remedies, liability and penalties"
    assert rn.heading_title("RULES FOR AI SYSTEMS IN THE EU") == "Rules for AI systems in the EU"
    assert rn.heading_title("Gemeinsame Bestimmungen") == "Gemeinsame Bestimmungen"


def test_provisions_block_groups_by_structure():
    data = {"en": {
        "1": {"number": "§ 1", "title": "Scope", "summary": "Defines the scope.", "problems": [],
              "path": [[1, "Part 1", "Common provisions"], [2, "Chapter 1", "Scope"]]},
        "2": {"number": "§ 2", "title": "Definitions", "summary": "Defines terms.", "problems": [],
              "path": [[1, "Part 1", "Common provisions"], [2, "Chapter 1", "Scope"]]},
        "26": {"number": "§ 26", "title": "Employment", "summary": "Governs employee data.", "problems": [],
               "path": [[1, "Part 2", "Implementing provisions"]]},
    }}
    block = rn.Builder.provisions_block(None, data, "en")

    assert block.splitlines() == [
        "### Part 1 — Common provisions", "",
        "**Chapter 1 — Scope**", "",
        "#### § 1 — Scope", "", "Defines the scope.", "",
        "#### § 2 — Definitions", "", "Defines terms.", "",
        "### Part 2 — Implementing provisions", "",
        "#### § 26 — Employment", "", "Governs employee data.",
    ]


def test_apply_corrections_replaces_summary_and_retranslates_other_language(tmp_path, monkeypatch):
    import json

    corrections = tmp_path / "corrections"
    corrections.mkdir()
    (corrections / "law.yaml").write_text('de:\n  "1": Regelt den Vorrang anderer Gesetze.\n', encoding="utf-8")
    monkeypatch.setattr(rn, "CORRECTIONS", corrections)
    calls = []
    monkeypatch.setattr(rn, "translate", lambda text, source, target: calls.append(text) or "Governs precedence.")

    builder = rn.Builder.__new__(rn.Builder)
    builder.drafts = tmp_path
    builder.specs = {"law": {"source": "gesetze"}}
    item = {"number": "§ 1", "title": "x", "summary": "falsch", "problems": ["check: wrong"], "path": []}
    (tmp_path / "law").mkdir()
    (tmp_path / "law" / "summaries.json").write_text(json.dumps({"de": {"1": dict(item)}, "en": {"1": dict(item)}}))

    builder.apply_corrections("law")
    builder.apply_corrections("law")  # second run: nothing to translate again

    data = json.loads((tmp_path / "law" / "summaries.json").read_text())
    assert data["de"]["1"]["summary"] == "Regelt den Vorrang anderer Gesetze."
    assert data["de"]["1"]["problems"] == []
    assert data["en"]["1"]["summary"] == "Governs precedence."
    assert calls == ["Regelt den Vorrang anderer Gesetze."]


def test_corrections_of_the_translation_never_overwrite_the_source_language(tmp_path, monkeypatch):
    import json

    corrections = tmp_path / "corrections"
    corrections.mkdir()
    (corrections / "law.yaml").write_text(
        'en:\n  "38":\n    title: Data protection officers of non-public bodies\n    summary: Requires a DPO.\n',
        encoding="utf-8")
    monkeypatch.setattr(rn, "CORRECTIONS", corrections)
    monkeypatch.setattr(rn, "translate", lambda *args: (_ for _ in ()).throw(AssertionError("no translation")))

    builder = rn.Builder.__new__(rn.Builder)
    builder.drafts = tmp_path
    builder.specs = {"law": {"source": "gesetze"}}
    item = {"number": "§ 38", "title": "x", "summary": "Verpflichtet.", "problems": [], "path": []}
    (tmp_path / "law").mkdir()
    (tmp_path / "law" / "summaries.json").write_text(json.dumps({"de": {"38": dict(item)}, "en": {"38": dict(item)}}))

    builder.apply_corrections("law")

    data = json.loads((tmp_path / "law" / "summaries.json").read_text())
    assert data["de"]["38"]["summary"] == "Verpflichtet."
    assert (data["en"]["38"]["title"], data["en"]["38"]["summary"]) == ("Data protection officers of non-public bodies", "Requires a DPO.")
