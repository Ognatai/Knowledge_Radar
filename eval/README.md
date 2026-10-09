# Evaluation

`gold/` is the hand-labelled gold standard for the extraction agent: 18 public
notes, labelled by the rules in `docs/extraction-guidelines.md`, in the same
format as `public/graph/` (`entities.yaml` plus `extractions/<slug>.yaml`).
The agent's output for these notes is scored against it (precision and recall
of discussed entities and of relations).

`gold/split.yaml` divides the notes into 9 development notes, used to tune
prompts, models and the pipeline, and 9 held-out test notes, used only for the
final numbers below.

`tests/test_gold_set.py` checks that the labels are valid against
`schema.yaml` and that no labelled note has changed since; if a note changes,
its gold labels must be reviewed again and the recorded hash updated.

```powershell
python -m app.agents.evaluate_extraction                 # development notes
python -m app.agents.evaluate_extraction --split test    # held-out notes
python -m app.agents.evaluate_extraction --predictions <run dir>   # rescore a run
```

## Metrics

- **Entities**: the (note, entity) pairs a note discusses. The agent names new
  entities itself, so predicted entities are aligned to gold entities by id,
  name or alias within the same type.
- **Relations**: (from, type, to) triples; symmetric types count in either
  direction.
- **Untyped relations**: which entity pairs are connected, ignoring type and
  direction.

## Results

### Final, held-out test notes

`qwen3:30b-a3b` with reasoning, entity pass, relation pass and
type-and-direction classifier (commit 381dc55), 2026-10-09:

| | Precision | Recall | F1 |
| --- | --- | --- | --- |
| Entities | 0.51 | 0.70 | **0.59** |
| Relations | 0.35 | 0.35 | **0.35** |
| Untyped relations | 0.42 | 0.42 | 0.42 |

The target was F1 0.75 for entities and 0.6 for relations. The local model
finds most entities and many of the right entity pairs, but often chooses the
wrong relation type or direction. Its output is therefore used as a proposal:
every extraction is reviewed against the note text and corrected before it
enters `public/graph/` (see "Provenance" below).

### Development notes, by iteration

F1 on the 9 development notes. Runs on the same configuration vary by several
points (only 58 gold relations; outputs also changed with the Ollama backend),
so small differences are not meaningful.

| Iteration | Entities | Relations | What changed |
| --- | --- | --- | --- |
| qwen3:14b, one call per chunk | 0.47 | 0.28 | baseline with reasoning (without: 0.24 / 0.13) |
| qwen3:30b-a3b | 0.48 | 0.40 | larger model: relation precision 0.88, recall 0.26 |
| + relation pass per window | 0.56 | 0.52 | recall of relations 0.26 → 0.41 |
| + example for concept lists, Vulkan backend | 0.58 | 0.46 | rescored with type-aware alignment |
| relation pass without reasoning | 0.55 | 0.36 | 3× faster, but relation precision 0.55 → 0.36 |
| relation pass may add entities, yes/no verifier | 0.60 | 0.03 | verifier rejected 38 of 39 relations (0.43 before it) |

Fixes that removed systematic errors along the way: a token cap and timeout
against repetition loops, tolerance for punctuation around evidence quotes, a
fallback for empty German names, case-sensitive acronyms (the method DoRA is not
the regulation DORA), and gold-derived examples removed from the prompt.

### Speed

On the Desktop (Radeon RX 7900 XT, 20 GB), decode speed under ROCm fell from
about 110 to 18 tokens/s as the context grew to 14k tokens; the Vulkan backend
keeps about 30 tokens/s (`scripts/start-ollama.ps1`). With reasoning, one
extraction call produces about 6,000 tokens. A development run takes about
50 minutes without the classifier and about three times as long with it.

## Provenance

`extracted_by` in each `public/graph/extractions/<slug>.yaml` records where an
extraction comes from:

- `claude (hand-labelled gold standard)`: one of the 18 gold notes.
- `qwen3:30b-a3b, reviewed by claude`: proposed by the local model, then
  checked against the note text and corrected (types, directions, missing and
  unsupported relations).
