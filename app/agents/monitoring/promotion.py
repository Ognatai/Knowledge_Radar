"""Promotion: registry entities that deserve a note of their own.

The registry (`public/graph/entities.yaml`) lists entities without a note; an
entity gets its own note once more than 3 notes discuss it. Candidates are taken
most-discussed first. Organisations and persons stay registry entries: the
knowledge base explains methods, concepts, technologies and laws, not who works
on them.

Each candidate is checked once by the local model, with reasoning, against the
notes with the most similar titles: a dedicated note may already explain it under
another name (e.g. "precision" in an evaluation note), or it may not be worth an
article. Declined candidates are remembered with their discussion count and only
checked again once more notes discuss them.

The weekly relevance run fills the room left under `max_proposals_per_week` with
at most `promotions_per_week` promotions; the curator drafts them like new topics,
from foundational sources, with the discussing notes offered as links.

    python -m app.agents.monitoring.promotion               # list the candidates
    python -m app.agents.monitoring.promotion --limit 5     # check the top 5, write a report for the curator
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.agents import llm
from app.agents.monitoring.findings import RUNS_DIRECTORY, STATE_DIRECTORY
from app.agents.monitoring.relevance import SCOPE, TOPIC_CHECK_NOTES, TopicVerdict, _similarity, topic_verdict_schema
from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.graph import Entity, KnowledgeGraph, load_graph
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory, load_notes

GRAPH_DIRECTORY = REPOSITORY_ROOT / "public" / "graph"
DECLINED_PATH = STATE_DIRECTORY / "promotions-declined.json"
MIN_DISCUSSING_NOTES = 4  # "more than 3 notes"
NOT_PROMOTED_TYPES = frozenset({"Organization", "Person"})


@dataclass(frozen=True)
class PromotionCandidate:
    entity: Entity
    notes: list[str]  # slugs of the notes that discuss it

    @property
    def search_name(self) -> str:
        """The name without a parenthesised expansion: "Sentence-BERT (SBERT)" -> "Sentence-BERT"."""
        return re.sub(r"\s*\([^)]*\)", "", self.entity.name_en).strip() or self.entity.name_en


def promotion_candidates(graph: KnowledgeGraph) -> list[PromotionCandidate]:
    """Registry entities discussed by more than 3 notes, most-discussed first."""
    counts = Counter(entity for _, entity in graph.discusses if graph.entities[entity].note is None)
    candidates = []
    for entity_id, count in counts.items():
        entity = graph.entities[entity_id]
        if count < MIN_DISCUSSING_NOTES or entity.type in NOT_PROMOTED_TYPES:
            continue
        notes = sorted(note for note, discussed in graph.discusses if discussed == entity_id)
        candidates.append(PromotionCandidate(entity, notes))
    return sorted(candidates, key=lambda candidate: (-len(candidate.notes), candidate.entity.id))


def build_promotion_prompt(candidate: PromotionCandidate, titles: dict[str, str], similar: list[tuple[str, str]]) -> str:
    entity = candidate.entity
    aliases = f" (also: {', '.join(entity.aliases)})" if entity.aliases else ""
    discussing = "\n".join(f"- {titles.get(slug, slug)}" for slug in candidate.notes)
    listed = "\n".join(f"[{slug}] {title}" for slug, title in similar)
    return f"""You maintain a reference knowledge base: factual articles, one per method, concept,
technology or law, like an encyclopedia. Its scope: {SCOPE}.

"{entity.name_en}"{aliases} ({entity.type}) has no article of its own, but these articles discuss it:
{discussing}

Existing articles with similar titles:
{listed}

Answer:
- "name": the subject as a short English noun phrase, e.g. "bm25".
- "dedicated_note": the slug (without brackets) of the article whose main subject is exactly
  this subject, possibly under another name, or null. An article that only uses or mentions
  it does not count.
- "worth_article": would a reader of these articles need a separate article explaining it:
  an established subject within the scope, more than a product name or a single number?
Answer with JSON only."""


def verify_promotion(
    candidate: PromotionCandidate,
    titles: dict[str, str],
    similar: list[tuple[str, str]],
    generate: Callable[..., str] = llm.generate,
) -> TopicVerdict:
    slugs = [slug for slug, _ in similar]
    answer = json.loads(
        generate(
            build_promotion_prompt(candidate, titles, similar),
            json_schema=topic_verdict_schema(slugs),
            temperature=0.0,
            think=True,
        )
    )
    dedicated = str(answer.get("dedicated_note") or "").strip("[] ") or None
    return TopicVerdict(
        name=str(answer.get("name") or candidate.entity.name_en).strip().lower(),
        dedicated_note=dedicated if dedicated in slugs else None,
        worth_article=bool(answer.get("worth_article")),
    )


def load_declined(path: Path = DECLINED_PATH) -> dict[str, dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_declined(declined: dict[str, dict[str, Any]], path: Path = DECLINED_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(declined, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def select_promotions(
    candidates: list[PromotionCandidate],
    notes: list[tuple[str, str]],
    limit: int,
    declined: dict[str, dict[str, Any]],
    embed: Callable[[list[str]], list[list[float]]],
    verify: Callable[[PromotionCandidate, dict[str, str], list[tuple[str, str]]], TopicVerdict] = verify_promotion,
    today: dt.date | None = None,
) -> list[dict[str, Any]]:
    """Up to `limit` verified promotions as curator proposals; newly declined candidates
    are added to `declined`."""
    if limit <= 0:
        return []
    titles = dict(notes)
    open_candidates = [
        c for c in candidates if len(c.notes) > declined.get(c.entity.id, {}).get("discussing_notes", 0)
    ]
    if not open_candidates:
        return []
    names = [c.entity.name_en for c in open_candidates]
    vectors = embed(names + [title for _, title in notes])
    name_vectors, title_vectors = vectors[: len(names)], vectors[len(names) :]

    proposals = []
    for candidate, vector in zip(open_candidates, name_vectors):
        ranked = sorted(range(len(notes)), key=lambda i: -_similarity(vector, title_vectors[i]))
        verdict = verify(candidate, titles, [notes[i] for i in ranked[:TOPIC_CHECK_NOTES]])
        if verdict.dedicated_note or not verdict.worth_article:
            declined[candidate.entity.id] = {
                "discussing_notes": len(candidate.notes),
                "dedicated_note": verdict.dedicated_note,
                "worth_article": verdict.worth_article,
                "checked": (today or dt.date.today()).isoformat(),
            }
            continue
        proposals.append(promotion_proposal(candidate, titles))
        if len(proposals) == limit:
            break
    return proposals


def promotion_proposal(candidate: PromotionCandidate, titles: dict[str, str]) -> dict[str, Any]:
    entity = candidate.entity
    return {
        "decision": "promotion",
        "entity": asdict(entity),
        "topic": candidate.search_name,
        "reason": f"registry entity discussed by {len(candidate.notes)} notes",
        "candidates": [{"note": slug, "title": titles.get(slug, slug)} for slug in candidate.notes],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--limit", type=int, default=0, help="check candidates and propose up to N promotions")
    args = parser.parse_args()

    notes = load_notes(configured_notes_directory())
    graph = load_graph(GRAPH_DIRECTORY, notes)
    candidates = promotion_candidates(graph)
    declined = load_declined()
    for candidate in candidates:
        status = " (declined)" if candidate.entity.id in declined else ""
        print(f"{len(candidate.notes):3}  {candidate.entity.id:40} {candidate.entity.type}{status}")
    if not args.limit:
        return 0

    note_titles = [(note.slug, note.title_en) for note in notes]
    proposals = select_promotions(candidates, note_titles, args.limit, declined, embeddings.embed)
    save_declined(declined)
    report_path = RUNS_DIRECTORY / f"promotion-{dt.datetime.now():%Y-%m-%d_%H%M%S}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({"proposals": proposals, "decisions": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    for proposal in proposals:
        print(f"Promote: {proposal['entity']['id']} ({proposal['reason']})")
    print(f"Report for the curator: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
