import json

import yaml

from app.agents import llm

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
        # Once the scripted answers are used up (e.g. by the relation pass), find nothing.
        return remaining.pop(0) if remaining else json.dumps({"new_entities": [], "discusses": [], "relations": []})

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
            "new_entities": [{"id": "microsoft", "type": "Organization", "name_en": "MS", "name_de": "MS"}],
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


def test_failed_model_call_counts_as_an_attempt(tmp_path):
    *_, graph, alpha = load(tmp_path)
    calls = []

    def flaky(prompt, **options):
        calls.append(options)
        if len(calls) == 1:
            raise llm.LLMError("timed out")
        return json.dumps({"new_entities": [], "discusses": ["microsoft"], "relations": []})

    result = extract_note(alpha, known_entities(graph), generate=flaky)

    assert result.discusses == ["microsoft"] and result.dropped == []
    assert calls[0]["max_tokens"] and calls[0]["timeout"]


def test_new_entity_without_german_name_uses_the_english_name(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm_answer = fake_llm(
        {
            "new_entities": [{"id": "openai", "type": "Organization", "name_en": "OpenAI", "name_de": ""}],
            "discusses": ["openai"],
            "relations": [],
        }
    )

    result = extract_note(alpha, known_entities(graph), generate=llm_answer)

    assert [(e.id, e.name_de) for e in result.new_entities] == [("openai", "OpenAI")]
    assert result.dropped == []


def test_prompt_lists_only_entities_mentioned_in_the_chunk(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm_answer = fake_llm({"new_entities": [], "discusses": [], "relations": []})

    extract_note(alpha, known_entities(graph), generate=llm_answer)

    table = llm_answer.prompts[0].split("<known_entities>")[1].split("</known_entities>")[0]
    assert "microsoft | Organization" in table  # named in the text
    assert "beta | Method" in table  # linked from the text
    assert "knowledge-graph |" not in table  # not mentioned


def test_new_entity_matching_a_known_name_is_resolved_to_it(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm_answer = fake_llm(
        {
            "new_entities": [{"id": "microsoft-research", "type": "Organization", "name_en": "Microsoft Research", "name_de": ""}],
            "discusses": ["microsoft-research"],
            "relations": [
                {"from": "alpha", "type": "DEVELOPED_BY", "to": "microsoft-research", "evidence": "Alpha was developed by Microsoft"}
            ],
        }
    )

    result = extract_note(alpha, known_entities(graph), generate=llm_answer)

    assert result.new_entities == []
    assert result.discusses == ["microsoft"]
    assert [(r["from"], r["to"]) for r in result.relations] == [("alpha", "microsoft")]


def test_new_entity_is_not_merged_with_a_known_entity_of_another_type(tmp_path):
    *_, graph, alpha = load(tmp_path)
    answer = {
        "new_entities": [{"id": "microsoft", "type": "Method", "name_en": "Microsoft", "name_de": ""}],
        "discusses": [],
        "relations": [],
    }
    llm_answer = fake_llm(answer, answer)

    result = extract_note(alpha, known_entities(graph), generate=llm_answer, max_attempts=2)

    assert result.new_entities == []
    assert "already used by" in result.dropped[0]
    assert "already used by" in llm_answer.prompts[1]


def test_worked_examples_follow_the_rules():
    from app.agents.extraction import EXAMPLES_PATH, check_answer, example_note
    from app.backend.knowledge_radar.graph import Entity

    examples = yaml.safe_load(EXAMPLES_PATH.read_text(encoding="utf-8"))["examples"]
    assert examples
    for example in examples:
        note = example_note(example)
        known = {
            note.slug: Entity(id=note.slug, type=note.entity_type, name_en=note.title_en, name_de=note.title_en, note=note.slug),
            **{k["id"]: Entity(id=k["id"], type=k["type"], name_en=k["name_en"], name_de=k["name_en"]) for k in example["known"]},
        }

        checked = check_answer(json.dumps(example["answer"]), note, known)

        assert checked.problems == [], example["note"]
        assert len(checked.relations) == len(example["answer"]["relations"])


def test_prompt_contains_the_worked_examples(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm_answer = fake_llm({"new_entities": [], "discusses": [], "relations": []})

    extract_note(alpha, known_entities(graph), generate=llm_answer)

    assert "Helm packages Kubernetes applications as charts" in llm_answer.prompts[0]


def test_acronyms_match_only_in_their_exact_spelling():
    from app.agents.extraction import mentioned_entities
    from app.backend.knowledge_radar.graph import Entity

    dora = Entity(id="dora", type="Regulation", name_en="Digital Operational Resilience Act (DORA)", name_de="DORA", aliases=["DORA"])

    assert mentioned_entities("DoRA decomposes each weight matrix.", {"dora": dora}) == {}
    assert "dora" in mentioned_entities("DORA requires ICT risk management.", {"dora": dora})
    assert "dora" in mentioned_entities("the digital operational resilience act applies", {"dora": dora})


def test_relation_pass_finds_relations_the_entity_pass_missed(tmp_path):
    *_, graph, alpha = load(tmp_path)
    llm_answer = fake_llm(
        {"new_entities": [], "discusses": ["microsoft", "beta"], "relations": []},
        {
            "new_entities": [],
            "discusses": [],
            "relations": [{"from": "alpha", "type": "DEVELOPED_BY", "to": "microsoft", "evidence": "Alpha was developed by Microsoft"}],
        },
    )

    result = extract_note(alpha, known_entities(graph), generate=llm_answer)

    assert [(r["from"], r["type"], r["to"]) for r in result.relations] == [("alpha", "DEVELOPED_BY", "microsoft")]
    assert "Find every relation" in llm_answer.prompts[1]
    assert "microsoft | Organization" in llm_answer.prompts[1]


def test_entities_only_referenced_by_a_link_in_parentheses_are_not_discussed(tmp_path):
    *_, graph, alpha = load(tmp_path)
    note = alpha.model_copy(update={"content_en": "Alpha was developed by Microsoft; see also ([[beta|Beta]])."})
    llm_answer = fake_llm({"new_entities": [], "discusses": ["microsoft", "beta"], "relations": []})

    result = extract_note(note, known_entities(graph), generate=llm_answer)

    assert result.discusses == ["microsoft"]


def test_relation_pass_can_run_without_reasoning(tmp_path):
    *_, graph, alpha = load(tmp_path)
    calls = []

    def recording(prompt, **options):
        calls.append(options["think"])
        return json.dumps({"new_entities": [], "discusses": ["microsoft"], "relations": []})

    extract_note(alpha, known_entities(graph), generate=recording, think=True, relation_think=False)

    assert calls == [True, False]
