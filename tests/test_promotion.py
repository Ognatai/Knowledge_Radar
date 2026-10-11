import datetime as dt
import json

from app.agents.monitoring.curator import with_entity_names
from app.agents.monitoring.promotion import (
    PromotionCandidate,
    promotion_candidates,
    select_promotions,
    verify_promotion,
)
from app.agents.monitoring.relevance import TopicVerdict
from app.backend.knowledge_radar.graph import Entity, KnowledgeGraph

NOTES = [("bert-note", "Transformers"), ("evaluation", "Retrieval evaluation"), ("rag", "RAG")]


def entity(identifier, type_="Method", name=None, note=None):
    return Entity(identifier, type_, name or identifier.upper(), name or identifier.upper(), note=note)


def graph(counts, types=None):
    """Registry entities discussed by the given number of notes."""
    types = types or {}
    entities = {"rag": entity("rag", note="rag")}
    discusses = {("rag", "rag")}
    for identifier, count in counts.items():
        entities[identifier] = entity(identifier, types.get(identifier, "Method"))
        discusses |= {(f"note-{i}", identifier) for i in range(count)}
    return KnowledgeGraph(entities, discusses, [], [])


def candidate(identifier, count=4, name=None):
    return PromotionCandidate(entity(identifier, name=name), [f"note-{i}" for i in range(count)])


def fake_embed(texts):
    """Same vector for texts that share their first letter, orthogonal otherwise."""
    letters = sorted({text[0].lower() for text in texts})
    return [[1.0 if text[0].lower() == letter else 0.0 for letter in letters] for text in texts]


def test_candidates_are_discussed_by_more_than_three_notes_most_discussed_first():
    found = promotion_candidates(graph({"bm25": 4, "gpt": 11, "bert": 9, "faiss": 3}))

    assert [(c.entity.id, len(c.notes)) for c in found] == [("gpt", 11), ("bert", 9), ("bm25", 4)]


def test_organisations_and_persons_stay_registry_entries():
    found = promotion_candidates(graph({"ecb": 6, "someone": 5, "bm25": 4}, {"ecb": "Organization", "someone": "Person"}))

    assert [c.entity.id for c in found] == ["bm25"]


def test_entities_with_a_note_are_not_candidates():
    g = graph({"bm25": 4})
    g.discusses |= {(f"note-{i}", "rag") for i in range(6)}

    assert [c.entity.id for c in promotion_candidates(g)] == ["bm25"]


def test_search_name_drops_the_parenthesised_expansion():
    assert candidate("sbert", name="Sentence-BERT (SBERT)").search_name == "Sentence-BERT"


def test_promotions_stop_at_the_limit_and_remember_declined_candidates():
    candidates = [candidate("gpt", 11), candidate("precision", 5), candidate("bert", 9), candidate("bm25", 4)]

    def verify(c, titles, similar):
        if c.entity.id == "precision":
            return TopicVerdict("precision", "evaluation", True)
        return TopicVerdict(c.entity.id, None, True)

    declined = {}
    proposals = select_promotions(candidates, NOTES, 2, declined, fake_embed, verify, today=dt.date(2026, 10, 11))

    assert [p["entity"]["id"] for p in proposals] == ["gpt", "bert"]
    assert proposals[0]["decision"] == "promotion"
    assert proposals[0]["candidates"][0] == {"note": "note-0", "title": "note-0"}
    assert declined == {
        "precision": {"discussing_notes": 5, "dedicated_note": "evaluation", "worth_article": True, "checked": "2026-10-11"}
    }


def test_declined_candidates_are_checked_again_only_when_more_notes_discuss_them():
    checked = []

    def verify(c, titles, similar):
        checked.append(c.entity.id)
        return TopicVerdict(c.entity.id, None, True)

    declined = {"bm25": {"discussing_notes": 4}, "bert": {"discussing_notes": 4}}
    select_promotions([candidate("bm25", 4), candidate("bert", 5)], NOTES, 3, declined, fake_embed, verify)

    assert checked == ["bert"]


def test_no_room_under_the_cap_means_no_check():
    def verify(c, titles, similar):
        raise AssertionError("must not be called")

    assert select_promotions([candidate("gpt")], NOTES, 0, {}, fake_embed, verify) == []


def test_verify_promotion_shows_the_discussing_notes_and_accepts_only_offered_notes():
    def generate(prompt, json_schema, **options):
        assert "- Transformers" in prompt and options["think"] is True
        assert json_schema["properties"]["dedicated_note"]["enum"] == ["evaluation", None]
        return json.dumps({"name": "BERT", "dedicated_note": "[other]", "worth_article": True})

    c = PromotionCandidate(entity("bert"), ["bert-note"])
    verdict = verify_promotion(c, dict(NOTES), [("evaluation", "Retrieval evaluation")], generate=generate)

    assert verdict == TopicVerdict("bert", None, True)


def test_promoted_notes_keep_the_registry_names_and_type():
    draft = "---\ntitle_en: Bm25 ranking\ntitle_de: BM25-Ranking\nentity_type: Concept\naliases:\n- Okapi\nsources:\n- https://x\n---\n\n## EN\n"
    registry = {"id": "bm25", "type": "Method", "name_en": "BM25", "name_de": "BM25", "aliases": ["Okapi BM25"], "note": None}

    text = with_entity_names(draft, registry)

    assert text.startswith(
        "---\ntitle_en: BM25\ntitle_de: BM25\nentity_type: Method\naliases:\n- Okapi BM25\n- Okapi\nsources:\n- https://x\n---\n"
    )
    assert text.endswith("\n## EN\n")
