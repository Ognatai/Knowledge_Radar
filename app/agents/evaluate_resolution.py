"""Score entity resolution against the cases in `eval/resolution/cases.yaml`.

Each case withholds part of the current registry and presents it as a new entity:

- `alias`: an alias of a known entity is removed and comes back as a new entity;
  the expected answer is that entity (a synonym the exact matching cannot find).
- `distinct`: an entity is removed whose name is close to another entity of the same
  type (WEAT and WEFAT, BM25 and BM25F); the expected answer is no match.

Precision matters most: a wrong merge corrupts the graph, a missed one only leaves a
duplicate for the review.

    python -m app.agents.evaluate_resolution --build          # write the cases from the registry
    python -m app.agents.evaluate_resolution                  # dev split
    python -m app.agents.evaluate_resolution --split test     # held-out cases
"""

from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import replace
from pathlib import Path
from typing import Any

import yaml

from app.agents import entity_resolution, llm
from app.agents.extraction import describe_entity, known_entities
from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, Entity, entity_keys, load_graph, normalize_name, plain_text
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT, configured_notes_directory, load_notes

CASES_PATH = REPOSITORY_ROOT / "eval" / "resolution" / "cases.yaml"
ALIAS_CASES = 40
DISTINCT_CASES = 40


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-") or "new"


def without_alias(entity: Entity, alias: str) -> Entity:
    return replace(entity, aliases=[a for a in entity.aliases if a != alias])


def build_cases(entities: dict[str, Entity], embed, seed: int = 7) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    alias_cases = []
    for entity in entities.values():
        for alias in entity.aliases:
            rest = without_alias(entity, alias)
            key = normalize_name(alias)
            # Only synonyms the exact matching cannot recover: not a name part, not a plural.
            if len(key) < 3 or key in entity_keys(rest) or key.isdigit():
                continue
            alias_cases.append({"kind": "alias", "entity": entity.id, "name": alias, "type": entity.type, "expected": entity.id})
    rng.shuffle(alias_cases)

    pool = list(entities.values())
    vectors = embed([entity.name_en for entity in pool])
    pairs = []
    for i, a in enumerate(pool):
        for j in range(i + 1, len(pool)):
            b = pool[j]
            if a.type == b.type:
                pairs.append((sum(x * y for x, y in zip(vectors[i], vectors[j])), a.id, b.id))
    pairs.sort(reverse=True)
    distinct_cases, used = [], set()
    for _, a, b in pairs:
        if a in used:
            continue
        used.add(a)
        distinct_cases.append({"kind": "distinct", "entity": a, "name": entities[a].name_en, "type": entities[a].type, "near": b, "expected": None})
        if len(distinct_cases) == DISTINCT_CASES:
            break

    cases = alias_cases[:ALIAS_CASES] + distinct_cases
    rng.shuffle(cases)
    for position, case in enumerate(cases):
        case["split"] = "dev" if position % 2 == 0 else "test"
    return cases


def run_case(case: dict[str, Any], entities: dict[str, Entity], graph, notes_by_slug, embed, generate) -> dict[str, Any]:
    known = dict(entities)
    if case["kind"] == "alias":
        known[case["entity"]] = without_alias(known[case["entity"]], case["name"])
        new = Entity(_slug(case["name"]), case["type"], case["name"], case["name"])
    else:
        withheld = known.pop(case["entity"])
        new = replace(withheld, id=f"new-{withheld.id}", note=None)
    index = entity_resolution.NameIndex(known, embed)
    candidates = index.nearest(new)
    shortlisted = case["expected"] in {c.id for c in candidates} if case["expected"] else None
    text = " ".join(plain_text(note.content_en) for note in notes_by_slug.values() if case["name"].casefold() in note.content_en.casefold())
    context = entity_resolution.mention(text, [case["name"]])
    answer = None
    if candidates:
        answer = entity_resolution.confirm(
            new, context, [(c, describe_entity(c, graph, notes_by_slug)) for c in candidates], generate
        )
    return {**case, "answer": answer, "shortlisted": shortlisted, "candidates": [c.id for c in candidates]}


def cached(embed):
    """Each case builds a new index over nearly the same names; embed every name once."""
    vectors: dict[str, list[float]] = {}

    def lookup(texts: list[str]) -> list[list[float]]:
        missing = list(dict.fromkeys(text for text in texts if text not in vectors))
        if missing:
            vectors.update(zip(missing, embed(missing)))
        return [vectors[text] for text in texts]

    return lookup


def score(results: list[dict[str, Any]]) -> dict[str, Any]:
    merges = [r for r in results if r["answer"]]
    correct = [r for r in merges if r["answer"] == r["expected"]]
    aliases = [r for r in results if r["kind"] == "alias"]
    return {
        "cases": len(results),
        "merges": len(merges),
        "precision": len(correct) / len(merges) if merges else 1.0,
        "recall": sum(r["answer"] == r["expected"] for r in aliases) / len(aliases) if aliases else 0.0,
        "shortlist_recall": sum(bool(r["shortlisted"]) for r in aliases) / len(aliases) if aliases else 0.0,
        "wrong_merges": [f"{r['name']} -> {r['answer']} (expected {r['expected']})" for r in merges if r["answer"] != r["expected"]],
        "missed": [f"{r['name']} (expected {r['expected']}, shortlist {r['candidates']})" for r in aliases if r["answer"] != r["expected"] and not r["answer"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--build", action="store_true", help="write the cases from the current registry")
    parser.add_argument("--split", default="dev", choices=["dev", "test", "all"])
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    notes_directory = configured_notes_directory()
    notes = load_notes(notes_directory)
    graph = load_graph(DEFAULT_GRAPH_DIRECTORY, notes, notes_directory)
    entities = known_entities(graph)
    if args.build:
        cases = build_cases(entities, embeddings.embed)
        CASES_PATH.parent.mkdir(parents=True, exist_ok=True)
        CASES_PATH.write_text(yaml.safe_dump({"version": 1, "cases": cases}, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"{len(cases)} cases written to {CASES_PATH}")
        return 0

    cases = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))["cases"]
    cases = [case for case in cases if args.split == "all" or case["split"] == args.split]
    by_slug = {note.slug: note for note in notes}
    embed = cached(embeddings.embed)
    generate = (lambda prompt, **options: llm.generate(prompt, **{**options, "model": args.model})) if args.model else llm.generate
    results = []
    for position, case in enumerate(cases, start=1):
        result = run_case(case, entities, graph, by_slug, embed, generate)
        results.append(result)
        mark = "ok " if result["answer"] == result["expected"] else "ERR"
        print(f"[{position}/{len(cases)}] {mark} {case['kind']:8} {case['name'][:40]:40} -> {result['answer']}", flush=True)
    report = score(results)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
