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

- `vault_inventory.py`: structural inventory of the Obsidian vault for the
  migration (`migration/inventory.yaml`).

Shared modules: `llm.py` (Ollama client; `OLLAMA_BASE_URL`,
`KNOWLEDGE_RADAR_MODEL`), `eurlex.py` (EUR-Lex fetching via a headless
Edge/Chrome, because EUR-Lex blocks plain HTTP clients; `KNOWLEDGE_RADAR_BROWSER`
overrides the browser path; cache in `.knowledge-radar/cache/`), and the prompt
templates in `prompts/`.
