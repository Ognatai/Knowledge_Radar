"""Score the relevance agent against the gold labels in `eval/relevance/gold.yaml`.

- Proposals: precision and recall of the findings the agent proposes (update or
  new_topic). This is what matters: proposals cost the user review time, missed
  proposals cost coverage.
- Accuracy over the four decisions, and how often an update names the right note.

    python -m app.agents.monitoring.evaluate_relevance                # dev split
    python -m app.agents.monitoring.evaluate_relevance --split test   # held-out items
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.agents.monitoring.relevance import (
    FINDING_INSTRUCTION,
    MIN_SIMILARITY,
    PROPOSAL_DECISIONS,
    SEARCH_PASSAGES,
    candidates_from_hits,
    classify,
    finding_from_json,
    finding_text,
    note_summaries,
)
from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory, load_notes

GOLD_PATH = REPOSITORY_ROOT / "eval" / "relevance" / "gold.yaml"


@dataclass(frozen=True)
class Scores:
    proposal_precision: float
    proposal_recall: float
    proposal_f1: float
    accuracy: float
    update_note_accuracy: float | None
    confusion: dict[tuple[str, str], int]


def score(gold: list[tuple[str, str | None]], predicted: list[tuple[str, str | None]]) -> Scores:
    """Each item is (decision, note); both lists in the same order."""
    gold_proposals = {i for i, (decision, _) in enumerate(gold) if decision in PROPOSAL_DECISIONS}
    predicted_proposals = {i for i, (decision, _) in enumerate(predicted) if decision in PROPOSAL_DECISIONS}
    hits = len(gold_proposals & predicted_proposals)
    precision = hits / len(predicted_proposals) if predicted_proposals else 1.0
    recall = hits / len(gold_proposals) if gold_proposals else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = sum(g[0] == p[0] for g, p in zip(gold, predicted)) / len(gold)
    updates = [(g, p) for g, p in zip(gold, predicted) if g[0] == "update" and p[0] == "update"]
    note_accuracy = sum(g[1] == p[1] for g, p in updates) / len(updates) if updates else None
    confusion = Counter((g[0], p[0]) for g, p in zip(gold, predicted))
    return Scores(precision, recall, f1, accuracy, note_accuracy, dict(confusion))


def main() -> int:
    from app.backend.knowledge_radar.index import Neo4jStore, connect

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--split", choices=["dev", "test", "all"], default="dev")
    parser.add_argument("--out", type=Path, help="write the predictions here as JSON")
    parser.add_argument("--think", action="store_true", help="let the model reason first (slower)")
    args = parser.parse_args()

    items = yaml.safe_load(GOLD_PATH.read_text(encoding="utf-8"))["items"]
    items = [item for item in items if args.split == "all" or item["split"] == args.split]
    findings = [finding_from_json(item["finding"]) for item in items]
    summaries = note_summaries(load_notes(configured_notes_directory()))
    vectors = embeddings.embed([embeddings.query_text(finding_text(f), FINDING_INSTRUCTION) for f in findings])

    predicted: list[tuple[str, str | None]] = []
    rows = []
    with connect() as driver:
        store = Neo4jStore(driver)
        for item, finding, vector in zip(items, findings, vectors):
            candidates = candidates_from_hits(store.search(vector, SEARCH_PASSAGES), summaries)
            if not candidates or candidates[0].score < MIN_SIMILARITY:
                decision, note, reason = "irrelevant", None, "below similarity threshold"
            else:
                result = classify(finding, candidates, think=args.think)
                decision, note, reason = result.decision, result.note, result.reason
            predicted.append((decision, note))
            mark = "  " if decision == item["decision"] else "XX"
            print(f"{mark} gold {item['decision']:10} got {decision:10} {finding.title[:60]}  ({reason[:80]})")
            rows.append({"id": finding.id, "gold": item["decision"], "predicted": decision, "note": note, "reason": reason})

    scores = score([(item["decision"], item["note"]) for item in items], predicted)
    print(
        f"\n{args.split}: proposals P {scores.proposal_precision:.2f} R {scores.proposal_recall:.2f} "
        f"F1 {scores.proposal_f1:.2f}; accuracy {scores.accuracy:.2f}"
    )
    for (gold, got), count in sorted(scores.confusion.items()):
        print(f"  gold {gold:10} -> {got:10} {count}")
    if args.out:
        args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
