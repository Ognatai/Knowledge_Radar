# Evaluation

`gold/` is the hand-labelled gold standard for the extraction agent: 18 public
notes, labelled by the rules in `docs/extraction-guidelines.md`, in the same
format as `public/graph/` (`entities.yaml` plus `extractions/<slug>.yaml`).
The agent's output for these notes is scored against it (precision and recall
of discussed entities and of relations).

`tests/test_gold_set.py` checks that the labels are valid against
`schema.yaml` and that no labelled note has changed since; if a note changes,
its gold labels must be reviewed again and the recorded hash updated.
