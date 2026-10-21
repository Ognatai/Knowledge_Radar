# Tests

The pytest suite, one file per module (`test_<module>.py`). Language models,
embeddings and network access are replaced by fakes, so the tests run offline
and without Ollama.

```powershell
python -m pytest
python -m pytest tests/test_notes_api.py    # one file
```

Some tests check data rather than code: `test_gold_set.py` validates the gold
standard in `eval/gold/` and fails when a labelled note has changed since it was
labelled.

`test_index_neo4j.py` runs against a real Neo4j instance and **wipes it**. It is
skipped unless `KNOWLEDGE_RADAR_NEO4J_TEST_URI` (and
`KNOWLEDGE_RADAR_NEO4J_TEST_PASSWORD`) name a throwaway instance; never point it
at the local index.

CI runs the whole suite on every push (`.github/workflows/ci.yml`).
