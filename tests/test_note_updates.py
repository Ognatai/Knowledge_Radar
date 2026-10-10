from datetime import date

import pytest

from app.backend.knowledge_radar.note_updates import NoteUpdate, add_update, needs_rewrite, update_count
from app.backend.knowledge_radar.templates import check_template
from tests.test_templates import SOURCE, technical

NEW_SOURCE = "https://arxiv.org/abs/2610.05163"


def update(day=date(2026, 10, 12), source=NEW_SOURCE):
    return NoteUpdate(
        day=day,
        title_en="Staged prompt injection",
        body_en=f"Agents can be attacked across several steps (Doe et al., 2026; [arXiv]({source})).",
        title_de="Gestaffelte Prompt Injection",
        body_de=f"Agenten lassen sich über mehrere Schritte angreifen (Doe et al., 2026; [arXiv]({source})).",
        source=source,
    )


def test_first_update_creates_the_section_in_both_languages():
    text = add_update(technical(), update())

    assert "### Updates\n\n#### 2026-10-12 — Staged prompt injection\nAgents can be attacked" in text
    assert "### Aktualisierungen\n\n#### 2026-10-12 — Gestaffelte Prompt Injection\nAgenten lassen" in text
    assert text.index("### Updates") > text.index("### Sources")
    assert text.index("### Aktualisierungen") > text.index("### Quellen")
    assert check_template(text) == []


def test_the_source_is_added_to_the_frontmatter_once():
    text = add_update(technical(), update())

    assert f"  - {SOURCE}\n  - {NEW_SOURCE}\n" in text
    assert add_update(text, update(day=date(2026, 11, 1))).count(f"- {NEW_SOURCE}\n") == 1


def test_later_updates_are_appended_in_order():
    text = add_update(add_update(technical(), update()), update(day=date(2026, 11, 2)))

    assert text.index("#### 2026-10-12") < text.index("#### 2026-11-02")
    assert update_count(text) == 2
    assert check_template(text) == []


def test_the_updates_section_must_come_last():
    text = add_update(technical(), update()).replace("### Sources\n", "### Moved\n", 1)
    text = text.replace("### Updates\n", "### Updates\n\n### Sources\nText.\n", 1)

    assert any("Updates" in problem for problem in check_template(text))


def test_a_note_without_updates_needs_no_rewrite():
    assert needs_rewrite(technical(), today=date(2027, 1, 1)) is None


def test_more_than_three_updates_trigger_a_rewrite():
    text = technical()
    for day in (date(2026, 10, 1), date(2026, 10, 8), date(2026, 10, 15)):
        text = add_update(text, update(day=day))
    assert needs_rewrite(text, today=date(2026, 10, 20)) is None

    text = add_update(text, update(day=date(2026, 10, 22)))

    assert needs_rewrite(text, today=date(2026, 10, 23)) == "4 updates since the last rewrite"


@pytest.mark.parametrize("last_rewrite, expected", [(date(2026, 1, 1), True), (date(2026, 6, 1), False)])
def test_six_months_since_the_last_rewrite_trigger_a_rewrite(last_rewrite, expected):
    text = technical().replace("entity_type: Method\n", f"entity_type: Method\nlast_rewrite_date: {last_rewrite}\n")
    text = add_update(text, update())

    reason = needs_rewrite(text, today=date(2026, 10, 12))

    assert (reason is not None) == expected
    if expected:
        assert reason == "last rewrite on 2026-01-01, more than 6 months ago"
