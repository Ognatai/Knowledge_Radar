"""Relevance agent: decide what each finding means for the knowledge base.

For every finding of a source run, embedding search against the local index
names the closest notes; the local model then decides:

- `irrelevant`: outside the knowledge base's scope, or not substantive
  (customer stories, product marketing, personnel news);
- `duplicate`: already covered by a note, adds nothing worth recording;
- `update`: adds something substantive to an existing note;
- `new_topic`: substantive and in scope, but no note covers it.

`irrelevant` is a fourth outcome next to the three in the architecture document:
the curated feeds bring much noise, and on real findings the similarity scores of
noise and of relevant work overlapped (0.73-0.76 vs. 0.74), so similarity alone
cannot separate them. It only names candidate notes; findings below
`MIN_SIMILARITY` are dropped without a model call.

The model answers narrow questions (kind of item, scope, which note has the topic
as its main subject, landmark or not) and the decision follows from them; asked
for a decision directly, it called nearly every new paper an update.

New topics are proposed per topic, not per finding: a topic qualifies when a
finding was judged new or when it recurs in several substantive findings, and the
model then checks it once, with reasoning, against the notes with the most similar
titles. Updates and new topics are proposals; at most `max_proposals_per_week`
(sources.yaml) are kept, ranked by importance, then tier, source kind and upvotes.
Recurring new topics outside the arXiv search phrases suggest new search phrases.

    python -m app.agents.monitoring.relevance                    # latest source run
    python -m app.agents.monitoring.relevance --run <findings.jsonl> --limit 10
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from app.agents import llm
from app.agents.monitoring.config import load_sources_config
from app.agents.monitoring.findings import RUNS_DIRECTORY, Finding
from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.index import _sections
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes

DECISIONS = ("irrelevant", "duplicate", "update", "new_topic")
PROPOSAL_DECISIONS = frozenset({"update", "new_topic"})
CANDIDATE_NOTES = 3
SEARCH_PASSAGES = 20
# Below this, a finding is unrelated to everything in the knowledge base.
MIN_SIMILARITY = 0.70
# Topic labels at least this similar count as the same topic.
SAME_TOPIC_SIMILARITY = 0.85
RECURRING_TOPIC_FINDINGS = 3
# Notes with the most similar titles shown when checking a candidate topic.
TOPIC_CHECK_NOTES = 5
FINDING_INSTRUCTION = "Given a new publication, retrieve knowledge base passages about the same topic"
SCOPE = (
    "AI and machine learning methods, NLP and large language models, agents, retrieval-augmented "
    "generation, knowledge graphs, evaluation, fairness and bias, explainability, MLOps and software "
    "engineering for AI systems, and the EU and German law on AI, data, data protection, IT security, "
    "digital services and financial-sector IT"
)


@dataclass(frozen=True)
class Candidate:
    note: str
    title: str
    score: float
    summary: str


@dataclass(frozen=True)
class Decision:
    finding: Finding
    decision: str
    note: str | None
    topic: str
    importance: int  # 1-5, how much it matters for a reference knowledge base
    reason: str
    candidates: list[Candidate] = field(default_factory=list)
    # Other findings on the same topic, for a new-topic proposal.
    related: list[str] = field(default_factory=list)

    @property
    def is_proposal(self) -> bool:
        return self.decision in PROPOSAL_DECISIONS

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["finding"] = self.finding.to_json()
        return data


def finding_from_json(data: dict[str, Any]) -> Finding:
    data = dict(data)
    data["published"] = date.fromisoformat(data["published"]) if data.get("published") else None
    data["fetched_at"] = datetime.fromisoformat(data["fetched_at"])
    return Finding(**data)


def note_summaries(notes: list[NoteDetail]) -> dict[str, tuple[str, str]]:
    """Title and TL;DR (or the first section) of every note, for the prompt."""
    summaries = {}
    for note in notes:
        sections = [(heading, text) for heading, text in _sections(note.content_en) if text]
        tldr = next((text for heading, text in sections if heading.casefold() == "tl;dr"), "")
        summaries[note.slug] = (note.title_en, (tldr or (sections[0][1] if sections else ""))[:800])
    return summaries


def finding_text(finding: Finding) -> str:
    return f"{finding.title}\n{finding.summary[:1500]}"


def candidates_from_hits(hits: list[dict[str, Any]], summaries: dict[str, tuple[str, str]]) -> list[Candidate]:
    """The best-scoring notes among the nearest passages."""
    best: dict[str, float] = {}
    for hit in hits:
        best[hit["note"]] = max(best.get(hit["note"], 0.0), hit["score"])
    ranked = sorted(best.items(), key=lambda item: -item[1])[:CANDIDATE_NOTES]
    return [
        Candidate(note=slug, title=summaries.get(slug, (slug, ""))[0], score=round(score, 3), summary=summaries.get(slug, ("", ""))[1])
        for slug, score in ranked
    ]


ITEM_KINDS = (
    "new_method",  # a research contribution: method, model, architecture, algorithm
    "empirical_study",  # an analysis, evaluation or benchmark of existing methods
    "legal_development",  # an adopted or amended act, a court ruling, an official guideline
    "enforcement_decision",  # a fine or decision of an authority in a single case
    "product_or_company_news",  # releases, customer stories, partnerships, marketing, events
    "opinion_or_anecdote",  # commentary, personal experiments, predictions
    "tutorial_or_tooling",  # how-tos, tool tips, software releases
)
NOT_SUBSTANTIVE = frozenset({"product_or_company_news", "opinion_or_anecdote", "tutorial_or_tooling"})

def decision_schema(candidate_slugs: list[str]) -> dict[str, Any]:
    """`covered_by` may only name one of the candidate notes shown to the model."""
    return {
        "type": "object",
        "properties": {
            "main_topic": {"type": "string"},
            "kind": {"type": "string", "enum": list(ITEM_KINDS)},
            "in_scope": {"type": "boolean"},
            "covered_by": {"enum": [*candidate_slugs, None]},
            "established_topic": {"type": "boolean"},
            "landmark": {"type": "boolean"},
            "importance": {"type": "integer", "minimum": 1, "maximum": 5},
            "reason": {"type": "string"},
        },
        "required": ["main_topic", "kind", "in_scope", "covered_by", "established_topic", "landmark", "importance", "reason"],
    }


def build_prompt(finding: Finding, candidates: list[Candidate]) -> str:
    notes = "\n\n".join(
        f"[{candidate.note}] {candidate.title}\n{candidate.summary}" for candidate in candidates
    ) or "(none)"
    tier = finding.tier or "none"
    return f"""You maintain a reference knowledge base: factual articles, one per method, concept,
technology or law, like an encyclopedia. Its scope: {SCOPE}.

New item from {finding.source} ({finding.category}; {finding.source_kind}; tier: {tier}):
Title: {finding.title}
Summary: {finding.summary[:1500] or "(no summary)"}

Closest existing articles:
{notes}

Answer these questions about the item:
- "main_topic": its main topic as a short English noun phrase (2-5 words, lowercase), naming
  the general subject (e.g. "prompt injection", "low-rank adaptation"), not the item's own name.
- "kind": one of {", ".join(ITEM_KINDS)}.
- "in_scope": does the main topic belong to the scope above? Applying AI to an unrelated
  domain (medicine, chip design, energy, geography, speech) is not in scope by itself.
- "covered_by": the slug (without brackets) of the article whose main subject is the item's
  main topic, or null. An article that only mentions the topic among others does not cover it.
- "established_topic": is the general subject of the main topic (not the item's own variant
  of it) an established subject that many works and practitioners discuss? false if it is
  mainly this item's own proposal.
- "landmark": would an encyclopedia article on this topic, written a year from now, cite this
  specific item? Almost all new papers, studies, fines and products: false. true only for a
  method that became a widely used standard, a major result that changed practice, an adopted
  or amended law, or a landmark ruling.
- "importance": 1-5, how much a reader of the knowledge base would miss the item.
- "reason": one short sentence.
Answer with JSON only."""


def derive_decision(answer: dict[str, Any], candidate_slugs: set[str]) -> tuple[str, str | None]:
    """The decision follows from the model's answers to the narrower questions."""
    covered_by = str(answer.get("covered_by") or "").strip("[] ") or None
    if covered_by not in candidate_slugs:
        covered_by = None
    if not answer.get("in_scope") or answer.get("kind") in NOT_SUBSTANTIVE:
        return "irrelevant", None
    if covered_by:
        return ("update" if answer.get("landmark") else "duplicate"), covered_by
    return ("new_topic" if answer.get("established_topic") else "irrelevant"), None


def classify(
    finding: Finding,
    candidates: list[Candidate],
    generate: Callable[..., str] = llm.generate,
    think: bool = False,
) -> Decision:
    slugs = [candidate.note for candidate in candidates]
    answer = json.loads(generate(build_prompt(finding, candidates), json_schema=decision_schema(slugs), temperature=0.0, think=think))
    if answer.get("kind") not in ITEM_KINDS:
        raise llm.LLMError(f"unknown item kind {answer.get('kind')!r}")
    decision, note = derive_decision(answer, {candidate.note for candidate in candidates})
    return Decision(
        finding=finding,
        decision=decision,
        note=note,
        topic=str(answer.get("main_topic", "")).strip().lower(),
        importance=min(5, max(1, int(answer.get("importance", 1)))),
        reason=f"{answer.get('kind')}: {str(answer.get('reason', '')).strip()}",
        candidates=candidates,
    )


def priority(decision: Decision) -> tuple[float, ...]:
    """Higher first: importance, then peer review, primary research, community votes."""
    finding = decision.finding
    tier = {"peer_reviewed": 2, None: 1, "preprint": 0}.get(finding.tier, 0)
    kind = 1 if finding.source_kind == "primary_research" else 0
    return (decision.importance, tier, kind, finding.upvotes or 0)


def select_proposals(decisions: list[Decision], limit: int) -> list[Decision]:
    proposals = [decision for decision in decisions if decision.is_proposal]
    return sorted(proposals, key=priority, reverse=True)[:limit]


def _similarity(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def group_topics(vectors: list[list[float]], threshold: float = SAME_TOPIC_SIMILARITY) -> list[list[int]]:
    """Greedy grouping: each topic joins the first group whose first topic is similar enough."""
    groups: list[list[int]] = []
    for index, vector in enumerate(vectors):
        for group in groups:
            if _similarity(vector, vectors[group[0]]) >= threshold:
                group.append(index)
                break
        else:
            groups.append([index])
    return groups


@dataclass(frozen=True)
class TopicVerdict:
    name: str  # the general subject, e.g. "prompt injection" for "indirect prompt injection"
    dedicated_note: str | None  # a note whose main subject is exactly this topic
    worth_article: bool


def topic_verdict_schema(note_slugs: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "dedicated_note": {"enum": [*note_slugs, None]},
            "worth_article": {"type": "boolean"},
        },
        "required": ["name", "dedicated_note", "worth_article"],
    }


def build_topic_prompt(labels: list[str], titles: list[str], notes: list[tuple[str, str]]) -> str:
    listed_labels = "\n".join(f"- {label}" for label in labels[:8])
    listed_titles = "\n".join(f"- {title}" for title in titles[:5])
    listed_notes = "\n".join(f"[{slug}] {title}" for slug, title in notes)
    return f"""You maintain a reference knowledge base: factual articles, one per method, concept,
technology or law, like an encyclopedia. Its scope: {SCOPE}.

New items share a topic. Their topic labels:
{listed_labels}
Some of their titles:
{listed_titles}

Existing articles with similar titles:
{listed_notes}

Answer:
- "name": the general subject of these items as a short English noun phrase (lowercase), e.g.
  "prompt injection" for "indirect prompt injection" and "staged prompt injection".
- "dedicated_note": the slug (without brackets) of the article whose main subject is exactly
  this topic, or null. An article on a related or broader subject that only mentions the
  topic does not count.
- "worth_article": would the knowledge base need a separate article on this topic: an
  established subject within the scope, clearly distinct from the existing articles? false
  for one-off items (a corrigendum, a single event) and for subtopics an existing article
  covers well.
Answer with JSON only."""


def verify_topic(
    labels: list[str],
    titles: list[str],
    notes: list[tuple[str, str]],
    generate: Callable[..., str] = llm.generate,
) -> TopicVerdict:
    slugs = [slug for slug, _ in notes]
    answer = json.loads(
        # Reasoning first: without it, the model names a note for almost every topic. There are
        # only a few candidate topics per run, so the slower mode is affordable here.
        generate(
            build_topic_prompt(labels, titles, notes),
            json_schema=topic_verdict_schema(slugs),
            temperature=0.0,
            think=True,
        )
    )
    dedicated = str(answer.get("dedicated_note") or "").strip("[] ") or None
    return TopicVerdict(
        name=str(answer.get("name", labels[0])).strip().lower() or labels[0],
        dedicated_note=dedicated if dedicated in slugs else None,
        worth_article=bool(answer.get("worth_article")),
    )


def merge_subtopics(topics: dict[str, list[Decision]]) -> dict[str, list[Decision]]:
    """A topic whose name contains another topic's name as whole words joins that more
    general topic: "indirect prompt injection" goes to "prompt injection"."""
    merged: dict[str, list[Decision]] = {}
    for name in sorted(topics, key=len):
        general = next((other for other in merged if re.search(rf"\b{re.escape(other)}\b", name)), None)
        merged.setdefault(general or name, []).extend(topics[name])
    return merged


def topic_proposals(
    decisions: list[Decision],
    notes: list[tuple[str, str]],
    embed: Callable[[list[str]], list[list[float]]],
    verify: Callable[[list[str], list[str], list[tuple[str, str]]], TopicVerdict] = verify_topic,
    min_findings: int = RECURRING_TOPIC_FINDINGS,
) -> list[Decision]:
    """One new-topic proposal per topic, not per finding.

    Candidate topics are the topics of findings judged new, and topics that recur
    in at least `min_findings` substantive findings: a single paper is weak
    evidence of a missing note, a topic many findings share is strong evidence.
    Each candidate is verified once by the model against the notes with the most
    similar titles (similar words are not the same subject: "prompt injection" vs.
    "Prompt Engineering"); candidates with the same general name are merged.
    """
    pool = [d for d in decisions if d.decision != "irrelevant" and d.topic]
    if not pool:
        return []
    labels = [d.topic for d in pool]
    titles = [title for _, title in notes]
    vectors = embed(labels + titles)
    topic_vectors, title_vectors = vectors[: len(labels)], vectors[len(labels) :]

    merged: dict[str, list[Decision]] = {}
    for group in group_topics(topic_vectors):
        members = [pool[index] for index in group]
        if not (any(m.decision == "new_topic" for m in members) or len(members) >= min_findings):
            continue
        ranked = sorted(range(len(notes)), key=lambda i: -_similarity(topic_vectors[group[0]], title_vectors[i]))
        verdict = verify(
            [m.topic for m in members],
            [m.finding.title for m in members],
            [notes[i] for i in ranked[:TOPIC_CHECK_NOTES]],
        )
        if verdict.dedicated_note is None and verdict.worth_article:
            merged.setdefault(verdict.name, []).extend(members)

    topics = merge_subtopics(merged)
    # Findings left out of every group whose topic names a proposed topic join it
    # ("staged prompt injection" joins "prompt injection").
    grouped = {id(member) for members in topics.values() for member in members}
    for decision in pool:
        if id(decision) in grouped:
            continue
        for name, members in topics.items():
            if re.search(rf"\b{re.escape(name)}\b", decision.topic):
                members.append(decision)
                break

    proposals = []
    for name, members in topics.items():
        representative = max(members, key=priority)
        proposals.append(
            Decision(
                finding=representative.finding,
                decision="new_topic",
                note=None,
                topic=name,
                importance=max(member.importance for member in members),
                reason=f"topic without a note of its own ({len(members)} findings)",
                candidates=representative.candidates,
                related=[member.finding.id for member in members if member is not representative],
            )
        )
    return proposals


def suggest_search_phrases(
    decisions: list[Decision],
    existing_phrases: list[str],
    embed: Callable[[list[str]], list[list[float]]],
    min_occurrences: int = 2,
) -> list[dict[str, Any]]:
    """Recurring new topics found outside the arXiv search phrases: candidates for sources.yaml."""
    topics = [d for d in decisions if d.decision == "new_topic" and d.finding.query is None and d.topic]
    if not topics:
        return []
    labels = [d.topic for d in topics]
    vectors = embed(labels + existing_phrases)
    topic_vectors, phrase_vectors = vectors[: len(labels)], vectors[len(labels) :]

    suggestions = []
    for group in group_topics(topic_vectors):
        if len(group) < min_occurrences:
            continue
        if any(_similarity(topic_vectors[group[0]], phrase) >= SAME_TOPIC_SIMILARITY for phrase in phrase_vectors):
            continue
        suggestions.append(
            {
                "phrase": labels[group[0]],
                "occurrences": len(group),
                "examples": [topics[index].finding.title for index in group][:3],
            }
        )
    return sorted(suggestions, key=lambda suggestion: -suggestion["occurrences"])


def latest_run(directory: Path = RUNS_DIRECTORY) -> Path:
    runs = sorted(directory.glob("findings-*.jsonl"))
    if not runs:
        raise FileNotFoundError(f"No source run in {directory}; run app.agents.monitoring.run_sources first.")
    return runs[-1]


def main() -> int:
    from app.backend.knowledge_radar.index import Neo4jStore, connect

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", type=Path, help="findings file (default: the latest source run)")
    parser.add_argument("--limit", type=int, help="classify only the first N findings (for trials)")
    args = parser.parse_args()

    run_path = args.run or latest_run()
    findings = [finding_from_json(json.loads(line)) for line in run_path.read_text(encoding="utf-8").splitlines() if line]
    if args.limit:
        findings = findings[: args.limit]
    config = load_sources_config()
    notes = load_notes(configured_notes_directory())
    summaries = note_summaries(notes)
    vectors = embeddings.embed([embeddings.query_text(finding_text(f), FINDING_INSTRUCTION) for f in findings])

    decisions: list[Decision] = []
    errors: list[str] = []
    with connect() as driver:
        store = Neo4jStore(driver)
        for position, (finding, vector) in enumerate(zip(findings, vectors), start=1):
            candidates = candidates_from_hits(store.search(vector, SEARCH_PASSAGES), summaries)
            if not candidates or candidates[0].score < MIN_SIMILARITY:
                decision = Decision(finding, "irrelevant", None, "", 1, "unrelated to every note (embedding similarity)", candidates)
            else:
                try:
                    decision = classify(finding, candidates)
                except (llm.LLMError, json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"{finding.id}: {exc}")
                    continue
            decisions.append(decision)
            target = f" -> {decision.note}" if decision.note else ""
            print(f"[{position}/{len(findings)}] {decision.decision:10} {decision.importance} {finding.title[:70]}{target}")

    topics = topic_proposals(decisions, [(note.slug, note.title_en) for note in notes], embeddings.embed)
    updates = [decision for decision in decisions if decision.decision == "update"]
    proposals = select_proposals(updates + topics, config.max_proposals_per_week)
    suggestions = suggest_search_phrases(decisions, config.arxiv.queries, embeddings.embed)
    report = {
        "findings_file": str(run_path),
        "proposals": [decision.to_json() for decision in proposals],
        "search_phrase_suggestions": suggestions,
        "errors": errors,
        "decisions": [decision.to_json() for decision in decisions],
    }
    report_path = run_path.with_name(run_path.name.replace("findings-", "relevance-").replace(".jsonl", ".json"))
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    counts = {name: sum(1 for d in decisions if d.decision == name) for name in DECISIONS}
    print(", ".join(f"{count} {name}" for name, count in counts.items()))
    print(f"Proposals ({len(proposals)} of {len(updates) + len(topics)}):")
    for decision in proposals:
        target = decision.note or "new note"
        label = decision.finding.title if decision.decision == "update" else f"{decision.topic} ({decision.reason})"
        print(f"  {decision.importance}  {decision.decision:9} {target:35} {label[:90]}")
    for suggestion in suggestions:
        print(f"Suggested search phrase: {suggestion['phrase']!r} ({suggestion['occurrences']} findings)")
    for error in errors:
        print(f"Error: {error}", file=sys.stderr)
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
