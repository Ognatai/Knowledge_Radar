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

The tools of the one-off migration of the Obsidian vault into public notes
(completed on 7 October 2026) were removed afterwards; they remain in the Git
history.
