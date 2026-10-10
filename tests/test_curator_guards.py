import json

from app.agents.monitoring.curator import _nearest, clean_section, translate


def embed(texts):
    """Every passage is equally similar, so only the per-source cap decides."""
    return [[1.0] for _ in texts]


def test_nearest_takes_at_most_three_passages_per_source():
    pool = [f"[A (2026)] passage {i}" for i in range(6)] + ["[B (2023)] one", "[C (2024)] two"]

    selected = _nearest("query", pool, embed(pool), embed, count=5)

    assert [passage.split("]")[0] for passage in selected] == ["[A (2026)", "[A (2026)", "[A (2026)", "[B (2023)", "[C (2024)"]


def test_clean_section_drops_heading_lines_and_an_echo_of_the_heading():
    text = "2. Attack Surfaces and Propagation\n\n### Stray\nAttacks spread (Doe et al., 2026)."

    assert clean_section(text, "2. Attack surfaces and propagation") == "Attacks spread (Doe et al., 2026)."
    assert clean_section("First line stays.\nSecond.", "Other heading") == "First line stays.\nSecond."


def answers(*texts):
    replies = iter(texts)
    return lambda prompt, **options: json.dumps({"markdown": next(replies)})


def test_translation_keeps_a_normal_result():
    warnings = []

    assert translate(answers("Kurzer Text."), "Short text.", warnings) == "Kurzer Text."
    assert warnings == []


def test_a_translation_that_adds_content_is_retried_then_replaced_by_the_english_text():
    invented = "Text. " + "Erfundener Unterabschnitt mit vielen Worten. " * 20
    warnings = []

    assert translate(answers(invented, "Text."), "Text.", warnings) == "Text."
    assert warnings == []

    assert translate(answers(invented, invented), "Text.", warnings) == "Text."
    assert warnings == ["translation failed, English text kept: Text."]


def test_titles_are_translated_on_their_own_and_kept_when_the_answer_is_a_paragraph():
    from app.agents.monitoring.curator import translate_title

    def short(prompt, **options):
        return json.dumps({"title": "1. Mechanismus von Prompt Injection"})

    def paragraph(prompt, **options):
        return json.dumps({"title": "Prompt Injection ist ein Angriff, bei dem ... " * 5})

    assert translate_title(short, "1. Mechanism of Prompt Injection") == "1. Mechanismus von Prompt Injection"
    assert translate_title(paragraph, "1. Mechanism") == "1. Mechanism"
