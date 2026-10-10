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

Updates and new topics are proposals; at most `max_proposals_per_week` of them
(sources.yaml) are kept, ranked by the model's importance score, then tier and
source kind. New topics found outside the arXiv search phrases also suggest new
search phrases when they recur.

    python -m app.agents.monitoring.relevance                    # latest source run
    python -m app.agents.monitoring.relevance --run <findings.jsonl> --limit 10
"""

from __future__ import annotations

import argparse
import json
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

    def similarity(a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    groups: list[list[int]] = []
    for index, vector in enumerate(topic_vectors):
        for group in groups:
            if similarity(vector, topic_vectors[group[0]]) >= SAME_TOPIC_SIMILARITY:
                group.append(index)
                break
        else:
            groups.append([index])

    suggestions = []
    for group in groups:
        if len(group) < min_occurrences:
            continue
        if any(similarity(topic_vectors[group[0]], phrase) >= SAME_TOPIC_SIMILARITY for phrase in phrase_vectors):
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
    summaries = note_summaries(load_notes(configured_notes_directory()))
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

    proposals = select_proposals(decisions, config.max_proposals_per_week)
    suggestions = suggest_search_phrases(decisions, config.arxiv.queries, embeddings.embed)
    report = {
        "findings_file": str(run_path),
        "proposals": [decision.finding.id for decision in proposals],
        "search_phrase_suggestions": suggestions,
        "errors": errors,
        "decisions": [decision.to_json() for decision in decisions],
    }
    report_path = run_path.with_name(run_path.name.replace("findings-", "relevance-").replace(".jsonl", ".json"))
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    counts = {name: sum(1 for d in decisions if d.decision == name) for name in DECISIONS}
    print(", ".join(f"{count} {name}" for name, count in counts.items()))
    print(f"Proposals ({len(proposals)} of {counts['update'] + counts['new_topic']}):")
    for decision in proposals:
        target = decision.note or "new note"
        print(f"  {decision.importance}  {decision.decision:9} {target:35} {decision.finding.title[:70]}")
    for suggestion in suggestions:
        print(f"Suggested search phrase: {suggestion['phrase']!r} ({suggestion['occurrences']} findings)")
    for error in errors:
        print(f"Error: {error}", file=sys.stderr)
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
