import pytest

from app.agents.evaluate_extraction import align_entities, prf, score
from app.backend.knowledge_radar.graph import Entity, KnowledgeGraph, Relation


def entity(entity_id, name, entity_type="Method", aliases=(), note=None):
    return Entity(id=entity_id, type=entity_type, name_en=name, name_de=name, aliases=list(aliases), note=note)


def graph(entities, discusses, relations):
    return KnowledgeGraph(
        entities={e.id: e for e in entities},
        discusses=set(discusses),
        relations=[Relation(source=s, type=t, target=o, note="alpha", evidence="") for s, t, o in relations],
        stale_extractions=[],
    )


ALPHA = entity("alpha", "Alpha", note="alpha")


def test_prf_handles_empty_sets():
    assert prf(set(), set()) == {"precision": 1.0, "recall": 1.0, "f1": 1.0, "tp": 0, "fp": 0, "fn": 0}
    assert prf({1, 2}, {2, 3})["precision"] == 0.5


def test_entities_align_by_id_name_or_alias():
    gold = {
        "alpha": ALPHA,
        "hipporag": entity("hipporag", "HippoRAG"),
        "w3c": entity("w3c", "World Wide Web Consortium (W3C)", "Organization", aliases=["W3C"]),
    }
    predicted = {
        "alpha": ALPHA,
        "hippo-rag": entity("hippo-rag", "Hippo RAG"),
        "world-wide-web-consortium": entity("world-wide-web-consortium", "W3C", "Organization"),
        "openai": entity("openai", "OpenAI", "Organization"),
    }

    assert align_entities(predicted, gold) == {
        "alpha": "alpha",
        "hippo-rag": "hipporag",
        "world-wide-web-consortium": "w3c",
    }


def test_score_maps_predictions_to_gold_and_ignores_symmetric_direction():
    gold = graph(
        [ALPHA, entity("beta", "Beta", note="beta"), entity("hipporag", "HippoRAG")],
        [("alpha", "alpha"), ("alpha", "beta"), ("alpha", "hipporag")],
        [("alpha", "BASED_ON", "beta"), ("alpha", "COMPLEMENTS", "hipporag")],
    )
    predicted = graph(
        [ALPHA, entity("beta", "Beta", note="beta"), entity("hippo-rag", "HippoRAG"), entity("openai", "OpenAI")],
        [("alpha", "alpha"), ("alpha", "beta"), ("alpha", "hippo-rag"), ("alpha", "openai")],
        # COMPLEMENTS is symmetric: stored as (hippo-rag, alpha) after id sorting.
        [("alpha", "BASED_ON", "beta"), ("alpha", "COMPLEMENTS", "hippo-rag"), ("alpha", "DEVELOPED_BY", "openai")],
    )

    report = score(predicted, gold, ["alpha"])

    assert report["entities"]["tp"] == 2 and report["entities"]["fp"] == 1 and report["entities"]["fn"] == 0
    assert report["relations"]["tp"] == 2 and report["relations"]["fp"] == 1
    assert report["relations"]["recall"] == pytest.approx(1.0)
    assert report["notes"]["alpha"]["false_positive_relations"] == ["alpha DEVELOPED_BY predicted:openai"]


def test_entities_align_across_singular_and_plural():
    gold = {"random-forest": entity("random-forest", "Random forest")}
    predicted = {"random-forests": entity("random-forests", "Random forests")}

    assert align_entities(predicted, gold) == {"random-forests": "random-forest"}


def test_entities_align_only_within_the_same_type():
    gold = {
        "dora": entity("dora", "Digital Operational Resilience Act (DORA)", "Regulation", aliases=["DORA"], note="dora"),
        "weight-decomposed-low-rank-adaptation": entity(
            "weight-decomposed-low-rank-adaptation", "DoRA (Weight-Decomposed Low-Rank Adaptation)", aliases=["DoRA"]
        ),
    }
    predicted = {"dora-method": entity("dora-method", "DoRA")}

    assert align_entities(predicted, gold) == {"dora-method": "weight-decomposed-low-rank-adaptation"}
