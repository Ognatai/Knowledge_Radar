"""Measure the extraction agent against the hand-labelled gold standard.

Runs the agent on the gold notes into a fresh graph directory (or rescores an
existing run with `--predictions`) and reports precision, recall and F1 for

- entities: the (note, entity) pairs of `discusses`;
- relations: (from, type, to) triples, symmetric types in either direction;
- untyped relations: which entity pairs are connected, ignoring type and direction.

The agent names new entities itself, so predicted entities are aligned to gold
entities by id, name or alias before scoring (case, spaces and punctuation ignored).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from app.agents import llm
from app.agents.extraction import extract_notes
from app.backend.knowledge_radar.graph import (
    Entity,
    GraphError,
    KnowledgeGraph,
    load_graph,
    public_relation_types,
)
from app.backend.knowledge_radar.notes import (
    REPOSITORY_ROOT,
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)

GOLD_DIRECTORY = REPOSITORY_ROOT / "eval" / "gold"
RUNS_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "eval-runs"


def prf(predicted: set, gold: set) -> dict[str, Any]:
    tp, fp, fn = len(predicted & gold), len(predicted - gold), len(gold - predicted)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def _normalize(text: str) -> str:
    return re.sub(r"[^0-9a-z]", "", text.casefold())


def _keys(entity: Entity) -> set[str]:
    names = [entity.id, entity.name_en, entity.name_de, *entity.aliases]
    keys: set[str] = set()
    for name in names:
        keys.add(_normalize(name))
        # "World Wide Web Consortium (W3C)" also matches "World Wide Web Consortium" and "W3C".
        outside = re.sub(r"\([^)]*\)", "", name)
        keys.add(_normalize(outside))
        keys.update(_normalize(inside) for inside in re.findall(r"\(([^)]*)\)", name))
    keys.discard("")
    return keys


def align_entities(predicted: dict[str, Entity], gold: dict[str, Entity]) -> dict[str, str]:
    """Map predicted entity ids to gold entity ids where they mean the same entity."""
    gold_by_key: dict[str, str] = {}
    for entity in gold.values():
        for key in _keys(entity):
            gold_by_key.setdefault(key, entity.id)
    alignment: dict[str, str] = {}
    for entity in predicted.values():
        if entity.id in gold:
            alignment[entity.id] = entity.id
            continue
        for key in sorted(_keys(entity)):
            if key in gold_by_key:
                alignment[entity.id] = gold_by_key[key]
                break
    return alignment


def score(predicted: KnowledgeGraph, gold: KnowledgeGraph, slugs: list[str]) -> dict[str, Any]:
    alignment = align_entities(predicted.entities, gold.entities)
    symmetric = {name for name, definition in public_relation_types().items() if definition.symmetric}

    def mapped(entity_id: str) -> str:
        return alignment.get(entity_id, f"predicted:{entity_id}")

    def triple(source: str, relation_type: str, target: str) -> tuple[str, str, str]:
        if relation_type in symmetric and target < source:
            source, target = target, source
        return (source, relation_type, target)

    totals: dict[str, tuple[set, set]] = {"entities": (set(), set()), "relations": (set(), set()), "untyped_relations": (set(), set())}
    notes: dict[str, Any] = {}
    for slug in slugs:
        predicted_entities = {(slug, mapped(e)) for s, e in predicted.discusses if s == slug and e != slug}
        gold_entities = {(slug, e) for s, e in gold.discusses if s == slug and e != slug}
        predicted_relations = {
            (slug, *triple(mapped(r.source), r.type, mapped(r.target))) for r in predicted.relations if r.note == slug
        }
        gold_relations = {(slug, *triple(r.source, r.type, r.target)) for r in gold.relations if r.note == slug}
        predicted_pairs = {(slug, frozenset((s, t))) for _, s, _, t in predicted_relations}
        gold_pairs = {(slug, frozenset((s, t))) for _, s, _, t in gold_relations}
        for name, (p, g) in {
            "entities": (predicted_entities, gold_entities),
            "relations": (predicted_relations, gold_relations),
            "untyped_relations": (predicted_pairs, gold_pairs),
        }.items():
            totals[name][0].update(p)
            totals[name][1].update(g)
        notes[slug] = {
            "entities": prf(predicted_entities, gold_entities),
            "relations": prf(predicted_relations, gold_relations),
            "missed_entities": sorted(e for _, e in gold_entities - predicted_entities),
            "extra_entities": sorted(e for _, e in predicted_entities - gold_entities),
            "missed_relations": sorted(" ".join(r[1:]) for r in gold_relations - predicted_relations),
            "false_positive_relations": sorted(" ".join(r[1:]) for r in predicted_relations - gold_relations),
        }
    report: dict[str, Any] = {name: prf(p, g) for name, (p, g) in totals.items()}
    report["notes"] = notes
    report["alignment"] = {key: value for key, value in sorted(alignment.items()) if key != value}
    return report


def _format(report: dict[str, Any]) -> str:
    lines = ["metric               precision  recall    f1     tp   fp   fn"]
    for name in ("entities", "relations", "untyped_relations"):
        m = report[name]
        lines.append(
            f"{name:<20} {m['precision']:>9.3f} {m['recall']:>7.3f} {m['f1']:>6.3f} "
            f"{m['tp']:>5} {m['fp']:>4} {m['fn']:>4}"
        )
    lines.append("")
    lines.append("per note                                 entities F1  relations F1")
    for slug, note in report["notes"].items():
        lines.append(f"{slug:<40} {note['entities']['f1']:>11.3f} {note['relations']['f1']:>13.3f}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notes", nargs="*", help="Gold notes to evaluate (default: all).")
    parser.add_argument("--model", default=None)
    parser.add_argument("--think", action="store_true")
    parser.add_argument("--predictions", type=Path, help="Score an existing run directory instead of extracting.")
    parser.add_argument("--notes-dir", type=Path, default=configured_notes_directory())
    args = parser.parse_args()

    try:
        notes = load_notes(args.notes_dir)
        gold = load_graph(GOLD_DIRECTORY, notes, args.notes_dir)
        gold_slugs = sorted({slug for slug, _ in gold.discusses if (GOLD_DIRECTORY / "extractions" / f"{slug}.yaml").is_file()})
        slugs = args.notes or gold_slugs
        if args.predictions:
            run_directory = args.predictions
        else:
            model = args.model or llm.model_name()
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            run_directory = RUNS_DIRECTORY / f"{stamp}-{model.replace(':', '-')}{'-think' if args.think else ''}"
            extract_notes(slugs, args.notes_dir, run_directory, model=model, think=args.think)
        predicted = load_graph(run_directory, notes, args.notes_dir)
    except (NoteRepositoryError, GraphError, llm.LLMError) as exc:
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 1

    report = score(predicted, gold, slugs)
    (run_directory / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(_format(report))
    print(f"\nReport: {run_directory / 'report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
