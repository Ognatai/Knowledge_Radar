# Agent utilities

Run from the repository root.

- `validate_notes.py`: checks every public note against the note contract and
  the note templates (`docs/note-templates.md`). Runs in CI.

  ```powershell
  python -m app.agents.validate_notes
  ```

Building blocks for the agent pipeline that will write new notes:

- `llm.py`: minimal client for the local Ollama server (`OLLAMA_BASE_URL`,
  `KNOWLEDGE_RADAR_MODEL`).
- `sources.py`: source metadata and citations; arXiv entries are verified
  against an expected title fragment and cached under `.knowledge-radar/cache/arxiv/`.
- `eurlex.py`: EUR-Lex fetching via a headless Edge/Chrome, because EUR-Lex
  blocks plain HTTP clients (`KNOWLEDGE_RADAR_BROWSER` overrides the browser
  path; cache in `.knowledge-radar/cache/eurlex/`), and splitting into articles.
- `cellar.py`: legal status of EU acts (consolidated versions, amendments,
  repeals) from the CELLAR SPARQL endpoint.
- `gesetze.py`: German federal law from gesetze-im-internet.de (official XML),
  split into sections.
- `legal_text.py`: source-independent structure of legal texts, shared by
  `eurlex` and `gesetze`.

Monitoring pipeline (milestone 3), in `monitoring/`:

- `run_sources.py`: the source agents. Fetches arXiv (curated search phrases)
  and the curated feeds from `sources.yaml`, keeps findings that are new, and
  writes them to `.knowledge-radar/monitoring/runs/findings-<time>.jsonl` for the
  relevance agent. `seen.json` next to it remembers what earlier runs handed on.

  ```powershell
  python -m app.agents.monitoring.run_sources --dry-run   # counts only, writes nothing
  python -m app.agents.monitoring.run_sources             # last 7 days
  ```

- `feeds.py`: arXiv API and RSS 2.0 / Atom / RSS 1.0 parsing (defusedxml).
- `config.py`: validation of `sources.yaml`.
- `findings.py`: the `Finding` record shared by all sources.

The tools of the one-off migration of the Obsidian vault into public notes
(completed on 7 October 2026) were removed afterwards; they remain in the Git
history.
