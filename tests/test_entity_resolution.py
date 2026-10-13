import json

import yaml

from app.agents import llm
from app.agents.entity_resolution import NameIndex, Resolution, apply, confirm, mention, resolve
from app.agents.extraction import NoteExtraction, write_extraction
from app.backend.knowledge_radar.graph import Entity
from tests.test_notes_api import write_note


def entity(identifier, name, type_="Method", aliases=()):
    return Entity(identifier, type_, name, name, aliases=list(aliases))


KNOWN = {
    "bm25": entity("bm25", "BM25", aliases=["Okapi BM25"]),
    "bm25f": entity("bm25f", "BM25F"),
    "ecb": entity("ecb", "European Central Bank", "Organisation"),
}


def fake_embed(texts):
    """Same vector for names sharing their first two letters, orthogonal otherwise."""
    prefixes = sorted({text[:2].lower() for text in texts} | {"bm", "eu", "ok", "ze"})
    return [[1.0 if text[:2].lower() == prefix else 0.0 for prefix in prefixes] for text in texts]


def answering(same_as):
    def generate(prompt, json_schema, **options):
        assert options["think"] is True
        return json.dumps({"same_as": same_as, "reason": "test"})

    return generate


def test_the_shortlist_holds_only_entities_of_the_same_type():
    index = NameIndex(KNOWN, fake_embed)

    nearest = index.nearest(entity("bm-okapi", "BM-Okapi"))

    assert [e.id for e in nearest] == ["bm25", "bm25f"]
    assert index.nearest(entity("euro-data", "Eurodata", "Dataset")) == []


def test_mention_finds_the_sentence_naming_the_entity():
    text = "Lexical search is old. Okapi weighting (Robertson, 2009) is common. Dense search is new."

    assert mention(text, ["Okapi weighting"]) == "Okapi weighting (Robertson, 2009) is common."
    assert mention(text, ["SPLADE"]) == ""


def test_a_confirmed_match_merges_and_records_the_new_name_as_alias():
    index = NameIndex(KNOWN, fake_embed)
    new = entity("okapi-weighting", "Okapi weighting")

    resolution = resolve([new], "Okapi weighting ranks documents.", index, lambda e: "", answering("bm25"))

    assert resolution.merged == {"okapi-weighting": "bm25"}
    assert resolution.aliases == {"bm25": ["Okapi weighting"]}


def test_an_unconfirmed_entity_stays_new_and_joins_the_index():
    index = NameIndex(KNOWN, fake_embed)
    new = entity("bm25-plus", "BM25+")

    resolution = resolve([new], "", index, lambda e: "", answering(None))

    assert resolution.merged == {}
    assert "bm25-plus" in index.entities


def test_a_failed_model_call_keeps_the_entity():
    def failing(prompt, json_schema, **options):
        raise llm.LLMError("timeout")

    resolution = resolve([entity("bm-x", "BM-X")], "", NameIndex(KNOWN, fake_embed), lambda e: "", failing)

    assert resolution.merged == {}


def test_without_candidates_the_model_is_not_asked():
    def generate(prompt, json_schema, **options):
        raise AssertionError("must not be called")

    resolution = resolve([entity("zeta", "Zeta", "Dataset")], "", NameIndex(KNOWN, fake_embed), lambda e: "", generate)

    assert resolution.merged == {}


def test_confirm_accepts_only_offered_ids_and_explains_what_is_not_the_same():
    def generate(prompt, json_schema, **options):
        assert "BM25F is not BM25" in prompt and "in use: ranks documents" in prompt
        assert json_schema["properties"]["same_as"]["enum"] == ["bm25", None]
        return json.dumps({"same_as": "ecb", "reason": "x"})

    assert confirm(entity("x", "X"), "", [(KNOWN["bm25"], "ranks documents")], generate) is None


def test_apply_replaces_merged_ids_and_drops_relations_that_collapse():
    resolution = Resolution(merged={"okapi": "bm25"})
    relations = [
        {"from": "okapi", "type": "BASED_ON", "to": "prf", "evidence": "a"},
        {"from": "bm25", "type": "BASED_ON", "to": "prf", "evidence": "b"},
        {"from": "okapi", "type": "COMPLEMENTS", "to": "bm25", "evidence": "c"},
    ]

    discusses, merged = apply(resolution, ["okapi", "bm25", "prf"], relations, "note")

    assert discusses == ["bm25", "prf"]
    assert merged == [{"from": "bm25", "type": "BASED_ON", "to": "prf", "evidence": "a"}]


def test_confirmed_aliases_are_written_to_the_registry(tmp_path):
    graph_dir = tmp_path / "graph"
    graph_dir.mkdir()
    (graph_dir / "entities.yaml").write_text(
        "version: 1\nentities:\n- id: bm25\n  type: Method\n  name_en: BM25\n  name_de: BM25\n", encoding="utf-8"
    )
    notes_dir = tmp_path / "notes"
    note_path = write_note(notes_dir, name="alpha.md")
    from app.backend.knowledge_radar.notes import load_notes

    note = load_notes(notes_dir)[0]
    write_extraction(graph_dir, note_path, note, NoteExtraction(aliases={"bm25": ["Okapi weighting"]}), extracted_by="test")

    registry = yaml.safe_load((graph_dir / "entities.yaml").read_text(encoding="utf-8"))
    assert registry["entities"][0]["aliases"] == ["Okapi weighting"]


def test_an_acronym_shortlists_the_entities_it_abbreviates():
    known = {**KNOWN, "dga": entity("data-governance-act", "Data Governance Act", "Organisation")}
    index = NameIndex(known, fake_embed)

    nearest = index.nearest(entity("dga-new", "DGA", "Organisation"))

    assert nearest[0].id == "data-governance-act"
