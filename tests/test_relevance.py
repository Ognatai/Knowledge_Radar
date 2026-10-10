import json
from datetime import date, datetime, timezone

import pytest

from app.agents.llm import LLMError
from app.agents.monitoring.evaluate_relevance import score
from app.agents.monitoring.findings import Finding
from app.agents.monitoring.relevance import (
    Candidate,
    Decision,
    candidates_from_hits,
    classify,
    derive_decision,
    finding_from_json,
    select_proposals,
    suggest_search_phrases,
    TopicVerdict,
    merge_subtopics,
    topic_proposals,
    verify_topic,
)

NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
CANDIDATES = [Candidate("lora", "LoRA", 0.88, "Low-rank adapters."), Candidate("llm-adaptation", "LLM adaptation", 0.84, "")]


def finding(identifier="arxiv:1", tier="preprint", source_kind="primary_research", query=None, upvotes=None, title="A paper"):
    return Finding(
        id=identifier,
        source="arXiv",
        category="arxiv",
        url="https://arxiv.org/abs/1",
        title=title,
        summary="Summary.",
        published=date(2026, 10, 8),
        authors=[],
        tier=tier,
        source_kind=source_kind,
        fetched_at=NOW,
        query=query,
        upvotes=upvotes,
    )


def answer(**overrides):
    base = {
        "main_topic": "low-rank adaptation",
        "kind": "new_method",
        "in_scope": True,
        "covered_by": "lora",
        "established_topic": True,
        "landmark": False,
        "importance": 2,
        "reason": "An incremental variant.",
    }
    return {**base, **overrides}


@pytest.mark.parametrize(
    "overrides, expected",
    [
        ({}, ("duplicate", "lora")),
        ({"landmark": True}, ("update", "lora")),
        ({"in_scope": False, "landmark": True}, ("irrelevant", None)),
        ({"kind": "product_or_company_news", "landmark": True}, ("irrelevant", None)),
        ({"kind": "opinion_or_anecdote"}, ("irrelevant", None)),
        ({"covered_by": None}, ("new_topic", None)),
        ({"covered_by": None, "established_topic": False}, ("irrelevant", None)),
        ({"covered_by": "[lora]", "landmark": True}, ("update", "lora")),
        ({"covered_by": "unknown-note"}, ("new_topic", None)),
    ],
)
def test_decision_follows_from_the_answers(overrides, expected):
    assert derive_decision(answer(**overrides), {"lora", "llm-adaptation"}) == expected


def test_classify_offers_only_candidate_notes_and_records_the_kind():
    seen = {}

    def generate(prompt, json_schema, **options):
        seen["schema"] = json_schema
        seen["prompt"] = prompt
        return json.dumps(answer(landmark=True, importance=4))

    decision = classify(finding(), CANDIDATES, generate=generate)

    assert (decision.decision, decision.note, decision.importance) == ("update", "lora", 4)
    assert decision.topic == "low-rank adaptation"
    assert decision.reason.startswith("new_method: ")
    assert seen["schema"]["properties"]["covered_by"]["enum"] == ["lora", "llm-adaptation", None]
    assert "[lora] LoRA" in seen["prompt"]


def test_classify_rejects_unknown_item_kinds():
    with pytest.raises(LLMError):
        classify(finding(), CANDIDATES, generate=lambda prompt, **options: json.dumps(answer(kind="poem")))


def test_candidates_keep_the_best_passage_per_note():
    hits = [{"note": "lora", "score": 0.8}, {"note": "lora", "score": 0.9}, {"note": "rag", "score": 0.85}]

    candidates = candidates_from_hits(hits, {"lora": ("LoRA", "Adapters."), "rag": ("RAG", "")})

    assert [(c.note, c.score) for c in candidates] == [("lora", 0.9), ("rag", 0.85)]
    assert candidates[0].title == "LoRA" and candidates[0].summary == "Adapters."


def decision(kind, importance=3, **finding_options):
    return Decision(finding(**finding_options), kind, None, "topic", importance, "", [])


def test_proposals_are_capped_and_ranked_by_importance_then_tier():
    decisions = [
        decision("duplicate", 5, identifier="d"),
        decision("update", 3, identifier="preprint", tier="preprint"),
        decision("update", 3, identifier="reviewed", tier="peer_reviewed"),
        decision("new_topic", 4, identifier="important"),
        decision("update", 1, identifier="minor"),
    ]

    proposals = select_proposals(decisions, limit=3)

    assert [d.finding.id for d in proposals] == ["important", "reviewed", "preprint"]


def test_upvotes_break_ties():
    decisions = [decision("update", 3, identifier="few", upvotes=5), decision("update", 3, identifier="many", upvotes=90)]

    assert [d.finding.id for d in select_proposals(decisions, limit=2)] == ["many", "few"]


def fake_embed(texts):
    """Same vector for texts that share their first word, orthogonal otherwise."""
    words = sorted({text.split()[0] for text in texts})
    return [[1.0 if text.split()[0] == word else 0.0 for word in words] for text in texts]


def topic_decision(topic, query=None, kind="new_topic", title="t"):
    return Decision(finding(query=query, title=title), kind, None, topic, 3, "", [])


def test_recurring_new_topics_outside_the_search_phrases_become_suggestions():
    decisions = [
        topic_decision("diffusion language models", title="one"),
        topic_decision("diffusion language models", title="two"),
        topic_decision("watermarking", title="once"),
        topic_decision("prompt injection", query="prompt injection"),
        topic_decision("prompt injection", query="prompt injection"),
        topic_decision("diffusion language models", kind="duplicate"),
    ]

    suggestions = suggest_search_phrases(decisions, ["dense retrieval"], fake_embed)

    assert suggestions == [{"phrase": "diffusion language models", "occurrences": 2, "examples": ["one", "two"]}]


def test_topics_matching_an_existing_phrase_are_not_suggested():
    decisions = [topic_decision("dense passage retrieval"), topic_decision("dense retrievers")]

    assert suggest_search_phrases(decisions, ["dense retrieval"], fake_embed) == []


def test_findings_round_trip_through_json():
    original = finding(upvotes=12)

    assert finding_from_json(json.loads(json.dumps(original.to_json()))) == original


def test_scores_focus_on_proposals():
    gold = [("update", "lora"), ("duplicate", "lora"), ("irrelevant", None), ("new_topic", None)]
    predicted = [("update", "llm-adaptation"), ("update", "lora"), ("irrelevant", None), ("duplicate", "lora")]

    scores = score(gold, predicted)

    assert scores.proposal_precision == 0.5
    assert scores.proposal_recall == 0.5
    assert scores.accuracy == 0.5
    assert scores.update_note_accuracy == 0.0
    assert scores.confusion[("new_topic", "duplicate")] == 1


NOTES = [("lora", "low-rank adaptation (LoRA)"), ("prompt-engineering", "prompt engineering")]


def verdict(name, dedicated=None, worth=True):
    return lambda labels, titles, notes: TopicVerdict(name, dedicated, worth)


def test_a_topic_judged_new_becomes_one_proposal_with_its_related_findings():
    decisions = [
        topic_decision("prompt injection attacks", kind="duplicate", title="a"),
        topic_decision("prompt injection", kind="new_topic", title="b"),
        topic_decision("low-rank adaptation", kind="duplicate", title="c"),
    ]

    proposals = topic_proposals(decisions, NOTES, fake_embed, verify=verdict("prompt injection"))

    assert len(proposals) == 1
    assert proposals[0].decision == "new_topic" and proposals[0].topic == "prompt injection"
    assert len(proposals[0].related) == 1


def test_recurring_topics_are_checked_against_the_most_similar_note_titles():
    decisions = [topic_decision("prompt injection", kind="duplicate", title=str(i)) for i in range(3)]
    decisions += [topic_decision("watermarking", kind="duplicate", title="once")]
    checked = []

    def verify(labels, titles, notes):
        checked.append((labels, notes))
        return TopicVerdict("prompt injection", None, True)

    proposals = topic_proposals(decisions, NOTES, fake_embed, verify=verify)

    assert [p.topic for p in proposals] == ["prompt injection"]
    assert proposals[0].reason == "topic without a note of its own (3 findings)"
    assert len(checked) == 1 and checked[0][1][0] == ("prompt-engineering", "prompt engineering")


@pytest.mark.parametrize("dedicated, worth", [("lora", True), (None, False)])
def test_topics_with_a_note_or_not_worth_an_article_are_dropped(dedicated, worth):
    decisions = [topic_decision("low-rank adaptation", kind="new_topic")]

    assert topic_proposals(decisions, NOTES, fake_embed, verify=verdict("low-rank adaptation", dedicated, worth)) == []


def test_groups_with_the_same_general_name_are_merged():
    decisions = [topic_decision("indirect injection", kind="new_topic", title="a")]
    decisions += [topic_decision("staged injection", kind="new_topic", title="b")]

    proposals = topic_proposals(decisions, NOTES, fake_embed, verify=verdict("prompt injection"))

    assert len(proposals) == 1 and len(proposals[0].related) == 1


def test_irrelevant_findings_do_not_make_a_topic_recur():
    decisions = [topic_decision("crypto prices", kind="irrelevant") for _ in range(5)]

    assert topic_proposals(decisions, NOTES, fake_embed, verify=verdict("crypto")) == []


def test_verify_topic_only_accepts_offered_notes():
    def generate(prompt, json_schema, **options):
        assert json_schema["properties"]["dedicated_note"]["enum"] == ["lora", "prompt-engineering", None]
        return json.dumps({"name": " Prompt Injection ", "dedicated_note": "[other]", "worth_article": True})

    result = verify_topic(["prompt injection"], ["A paper"], NOTES, generate=generate)

    assert result == TopicVerdict("prompt injection", None, True)


def test_subtopics_join_the_more_general_topic():
    a, b, c = topic_decision("x", title="a"), topic_decision("x", title="b"), topic_decision("x", title="c")

    merged = merge_subtopics({"indirect prompt injection": [a], "prompt injection": [b], "injection molding": [c]})

    assert merged == {"prompt injection": [b, a], "injection molding": [c]}


def test_findings_naming_a_proposed_topic_join_it():
    decisions = [topic_decision("prompt injection", kind="new_topic", title="a")]
    decisions += [topic_decision("staged prompt injection", kind="duplicate", title="b")]
    decisions += [topic_decision("skill routing", kind="duplicate", title="c")]

    proposals = topic_proposals(decisions, NOTES, fake_embed, verify=verdict("prompt injection"))

    assert len(proposals) == 1 and len(proposals[0].related) == 1
