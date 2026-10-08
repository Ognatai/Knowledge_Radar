import json

import yaml

from app.agents.extraction import (
    chunk_text,
    extract_note,
    known_entities,
    reading_text,
    write_extraction,
)
from app.backend.knowledge_radar.graph import load_graph, note_sha256
from app.backend.knowledge_radar.notes import load_notes
from tests.test_graph import setup_repo


def fake_llm(*answers):
    """An LLM stand-in returning the given answers in order and recording prompts."""
    prompts = []
    remaining = [json.dumps(answer) for answer in answers]

    def generate(prompt, **_options):
        prompts.append(prompt)
        return remaining.pop(0)

    generate.prompts = prompts
    return generate


def load(tmp_path):
    notes_dir, graph_dir, _ = setup_repo(tmp_path)
    notes = load_notes(notes_dir)
    graph = load_graph(graph_dir, notes, notes_dir)
    alpha = next(note for note in notes if note.slug == "alpha")
    return notes_dir, graph_dir, notes, graph, alpha


def test_reading_text_drops_notice_code_and_sources():
    markdown = """> **Note:** LLM-generated summary.

### TL;DR

Alpha builds on beta.

```text
1. Outline
```

### Sources

- Someone (2020).
"""

    assert reading_text(markdown) == "### TL;DR\n\nAlpha builds on beta."


def test_chunk_text_splits_at_sections_and_keeps_short_texts_whole():
    text = "### A\n\n" + "a " * 30 + "\n\n### B\n\n" + "b " * 30

    assert chunk_text(text, max_chars=1000) == [text]
    chunks = chunk_text(text, max_chars=80)
    assert len(chunks) == 2
    assert chunks[0].startswith("### A") and chunks[1].startswith("### B")


def test_chunk_text_splits_oversized_sections_at_paragraphs():
    text = "### A\n\n" + "\n\n".join("word " * 10 for _ in range(4))

    chunks = chunk_text(text, max_chars=120)

    assert len(chunks) > 1
    assert all(len(chunk) <= 120 for chunk in chunks)


def test_extract_note_accepts_valid_output_and_registers_new_entities(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm = fake_llm(
        {
            "new_entities": [
                {"id": "openai", "type": "Organization", "name_en": "OpenAI", "name_de": "OpenAI"}
            ],
            "discusses": ["microsoft", "beta"],
            "relations": [
                {"from": "alpha", "type": "DEVELOPED_BY", "to": "microsoft", "evidence": "Alpha was developed by Microsoft"},
                {"from": "alpha", "type": "BASED_ON", "to": "beta", "evidence": "builds on Beta"},
            ],
        }
    )

    result = extract_note(alpha, known_entities(graph), generate=llm)

    assert result.discusses == ["microsoft", "beta"]
    assert [(r["from"], r["type"], r["to"]) for r in result.relations] == [
        ("alpha", "DEVELOPED_BY", "microsoft"),
        ("alpha", "BASED_ON", "beta"),
    ]
    # Registered but not discussed: only discussed new entities are kept.
    assert result.new_entities == []
    assert result.dropped == []
    assert "Alpha was developed by **Microsoft**" in llm.prompts[0]
    assert "microsoft | Organization | Microsoft" in llm.prompts[0]


def test_extract_note_asks_for_corrections_and_drops_what_stays_invalid(tmp_path):
    *_, graph, alpha = load(tmp_path)
    invented = {"from": "alpha", "type": "DEVELOPED_BY", "to": "microsoft", "evidence": "Alpha was invented by Microsoft"}
    llm = fake_llm(
        {"new_entities": [], "discusses": ["microsoft"], "relations": [invented]},
        {"new_entities": [], "discusses": ["microsoft"], "relations": [invented]},
    )

    result = extract_note(alpha, known_entities(graph), generate=llm, max_attempts=2)

    assert result.relations == []
    assert len(result.dropped) == 1 and "evidence" in result.dropped[0]
    assert "not a verbatim quote" in llm.prompts[1]


def test_extract_note_adds_relation_endpoints_to_discusses(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm = fake_llm(
        {
            "new_entities": [],
            "discusses": [],
            "relations": [{"from": "alpha", "type": "BASED_ON", "to": "beta", "evidence": "builds on Beta"}],
        }
    )

    result = extract_note(alpha, known_entities(graph), generate=llm)

    assert result.discusses == ["beta"]


def test_new_entity_with_a_known_id_refers_to_the_known_entity(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm = fake_llm(
        {
            "new_entities": [{"id": "microsoft", "type": "Concept", "name_en": "MS", "name_de": "MS"}],
            "discusses": ["microsoft"],
            "relations": [],
        }
    )

    result = extract_note(alpha, known_entities(graph), generate=llm)

    assert result.new_entities == [] and result.discusses == ["microsoft"]


def test_write_extraction_produces_a_valid_graph(tmp_path):
    notes_dir, graph_dir, notes, graph, alpha = load(tmp_path)
    llm = fake_llm(
        {
            "new_entities": [{"id": "openai", "type": "Organization", "name_en": "OpenAI", "name_de": "OpenAI"}],
            "discusses": ["openai", "microsoft"],
            "relations": [{"from": "alpha", "type": "DEVELOPED_BY", "to": "microsoft", "evidence": "Alpha was developed by Microsoft"}],
        }
    )
    result = extract_note(alpha, known_entities(graph), generate=llm)

    write_extraction(graph_dir, notes_dir / "alpha.md", alpha, result, extracted_by="test-model")

    reloaded = load_graph(graph_dir, notes, notes_dir)
    assert reloaded.entities["openai"].name_en == "OpenAI"
    assert ("alpha", "openai") in reloaded.discusses
    assert reloaded.stale_extractions == []
    data = yaml.safe_load((graph_dir / "extractions" / "alpha.yaml").read_text(encoding="utf-8"))
    assert data["extracted_by"] == "test-model"
    assert data["note_sha256"] == note_sha256(notes_dir / "alpha.md")
