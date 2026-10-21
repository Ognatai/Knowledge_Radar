# Evaluation

Gold standards for the agents that use the local model, the commands that score
the agents against them, and the latest results. Every gold set is split into
development items (to tune prompts, models and the pipeline) and held-out test
items (used only for the final numbers).

| Folder | Gold standard for |
| --- | --- |
| `gold/` | the extraction agent (`app/agents/extraction.py`) |
| `relevance/` | the relevance agent (`app/agents/monitoring/relevance.py`) |
| `resolution/` | entity resolution (`app/agents/entity_resolution.py`) |

## Extraction (`gold/`)

18 public notes, labelled by the rules in `docs/extraction-guidelines.md`, in the
same format as `public/graph/` (`entities.yaml` plus `extractions/<slug>.yaml`).
`gold/split.yaml` divides them into 9 development and 9 test notes.

`tests/test_gold_set.py` checks that the labels are valid against `schema.yaml`
and that no labelled note has changed since; if a note changes, its labels must
be reviewed again and the recorded hash updated.

```powershell
python -m app.agents.evaluate_extraction                 # development notes
python -m app.agents.evaluate_extraction --split test    # held-out notes
python -m app.agents.evaluate_extraction --predictions <run dir>   # rescore a run
```

Metrics:

- **Entities**: the (note, entity) pairs a note discusses. The agent names new
  entities itself, so predicted entities are aligned to gold entities by id,
  name or alias within the same type.
- **Relations**: (from, type, to) triples; symmetric types count in either
  direction.
- **Untyped relations**: which entity pairs are connected, ignoring type and
  direction.

Results on the held-out test notes, `qwen3:30b-a3b` with reasoning, entity pass,
relation pass and type-and-direction classifier:

| | Precision | Recall | F1 |
| --- | --- | --- | --- |
| Entities | 0.51 | 0.70 | **0.59** |
| Relations | 0.35 | 0.35 | **0.35** |
| Untyped relations | 0.42 | 0.42 | 0.42 |

The model finds most entities and many of the right entity pairs, but often
chooses the wrong relation type or direction. Its output is therefore a
proposal: every extraction is reviewed against the note text and corrected
before it enters `public/graph/`.

## Relevance (`relevance/`)

`relevance/gold.yaml`: 40 findings of a source run, from arXiv and the curated
feeds, each labelled `irrelevant`, `duplicate`, `update` or `new_topic`, split
into 20 development and 20 test items.

```powershell
python -m app.agents.monitoring.evaluate_relevance                # dev split
python -m app.agents.monitoring.evaluate_relevance --split test   # held-out items
```

What matters most is the precision and recall of proposals (`update` and
`new_topic`): proposals cost review time, missed proposals cost coverage. On the
test split the final variant makes no false proposals, at an accuracy of 0.70.
`duplicate` and `irrelevant` are often confused, which does not matter: both are
discarded.

## Entity resolution (`resolution/`)

`resolution/cases.yaml` holds 80 cases built from the entity registry, split
evenly into dev and test:

- 40 `alias` cases: an alias of a known entity that exact name matching cannot
  recover (abbreviations, translations, spellings, synonyms) is withheld and
  presented as a new entity; the expected answer is that entity.
- 40 `distinct` cases: an entity whose name is closest to another entity of the
  same type (WEAT and WEFAT, BM25 and BM25F, EDPS and EDPB) is withheld; the
  expected answer is no match.

```powershell
python -m app.agents.evaluate_resolution --build         # rebuild the cases from the registry
python -m app.agents.evaluate_resolution                 # dev split
python -m app.agents.evaluate_resolution --split test    # held-out cases
```

Precision is what matters: a wrong merge corrupts the graph silently, a missed
one leaves a duplicate for the review. `qwen3:30b-a3b` with reasoning and a
shortlist of 5:

| Split | Merges | Precision | Recall (aliases) | Shortlist recall | Distinct pairs kept apart |
| --- | --- | --- | --- | --- | --- |
| dev | 12 | 1.00 | 0.55 | 0.91 | 18 of 18 |
| test | 13 | 1.00 | 0.72 | 0.89 | 22 of 22 |

## Provenance

`extracted_by` in each `public/graph/extractions/<slug>.yaml` records where an
extraction comes from:

- `claude (hand-labelled gold standard)`: one of the 18 gold notes.
- `qwen3:30b-a3b, reviewed by claude`: proposed by the local model, then
  checked against the note text and corrected.
