# Agent utilities

Run from the repository root.

- `validate_notes.py`: checks every public note against the note contract and
  the note templates (`docs/note-templates.md`). Runs in CI.

  ```powershell
  python -m app.agents.validate_notes
  ```

- `regulatory_articles.py`: drafts the detailed article sections of a
  regulatory note with the local LLM, checks them and merges them after human
  review. Configuration per act: `migration/regulatory/<note>.yaml` (source
  URLs, important articles, application dates).

  ```powershell
  python -m app.agents.regulatory_articles draft  eu-ai-act   # Ollama, ~20-60 s per article and language
  python -m app.agents.regulatory_articles review eu-ai-act   # deterministic checks + LLM findings
  # read and correct the drafts in .knowledge-radar/drafts/eu-ai-act/
  python -m app.agents.regulatory_articles merge  eu-ai-act   # writes the note, runs the template check
  ```

  `review` flags numbers that do not occur in the official text and missing
  sub-headings. The local model's own faithfulness check is only advisory: it
  produces many false positives, so its findings are listed for the factual
  sub-sections only and must be judged by a person.

- `technical_notes.py`: migrates technical notes in packages
  (`migration/technical/<package>.yaml`: notes and their sources). Per note the
  local model plans the topic-specific "How it works" steps, writes the
  English note part by part (each step cites its sources; vault note only for
  topic coverage), then translates it part by part. Sources sections are
  generated from verified metadata (arXiv IDs are checked against an expected
  title). Needs `vault_path` in `local-config.yaml`.

  ```powershell
  python -m app.agents.technical_notes outline rag            # ~2 min per note; read/edit the .outline.md files
  python -m app.agents.technical_notes draft  rag             # ~20-25 min per note (overnight run)
  python -m app.agents.technical_notes review rag             # template, links, citations, numbers, originality
  python -m app.agents.technical_notes accept rag --notes rag-chunking   # after reading the draft
  ```

  Models: `qwen3:30b-a3b` writes with reasoning mode (`KNOWLEDGE_RADAR_WRITER_MODEL`),
  `qwen3:14b` translates (`KNOWLEDGE_RADAR_TRANSLATION_MODEL`). In the RAG pilot,
  qwen3:14b as writer produced fluent text with factual errors and invented
  attributions; the 30B model with reasoning did not. German terms are
  post-processed with `migration/glossary-de.yaml`.

- `vault_inventory.py`: structural inventory of the Obsidian vault for the
  migration (`migration/inventory.yaml`).

Shared modules: `llm.py` (Ollama client; `OLLAMA_BASE_URL`,
`KNOWLEDGE_RADAR_MODEL`), `eurlex.py` (EUR-Lex fetching via a headless
Edge/Chrome, because EUR-Lex blocks plain HTTP clients; `KNOWLEDGE_RADAR_BROWSER`
overrides the browser path; cache in `.knowledge-radar/cache/`), and the prompt
templates in `prompts/`.
