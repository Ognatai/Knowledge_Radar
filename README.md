# Knowledge Radar

Knowledge Radar is a local-first knowledge base for machine-learning and
regulatory topics. Monitoring agents extend it with new developments; the
resulting knowledge graph is published as a static, bilingual (EN/DE) site.

**Setup and running locally: see [SETUP.md](SETUP.md).** The default setup is
free and Ollama-only; no API key is required.

## Repository layout

| Path | Contents |
| --- | --- |
| `public/notes/` | Public Markdown notes (MIT, like the code) |
| `public/graph/` | Versioned knowledge graph: `entities.yaml` (entities without a note, with aliases) and `extractions/<note>.yaml` (entities and relations per note, with evidence quotes) |
| `schema.yaml` | Entity/relation schema, `visibility: public/private` per type |
| `app/site/` | Static public site (React, GitHub Pages): graph + text view, DE/EN, client-side search |
| `app/backend/` | Python package: note loading/validation, static-site export, local app API (FastAPI) |
| `app/agents/` | Agent pipeline (currently: note validation) |
| `app/mcp/` | MCP servers |
| `app/frontend/` | Local app UI: chat + Review Dashboard (planned) |
| `scripts/` | Private-data check, weekly monitoring run, Task Scheduler registration |
| `scheduled_task.xml` | Windows Task Scheduler definition (template) for the weekly run |

## Note format

Every note requires `title_en`, `title_de`, an `entity_type` that is a public
entity type in `schema.yaml`, and a non-empty list of absolute HTTP(S) URLs
under `sources`. Content is split into `## EN` and `## DE` sections.
`## Original Source Text (DE)` is optional for source text that must remain
untranslated. Links to other notes are written as `[[wikilinks]]`
(`[[slug]]`, `[[slug|label]]`); they become `RELATED_TO` edges in the graph.

## Public/private boundary

This repository never contains private data. The private data lives in a
separate repository checked out *next to* this one; its location is set in an
untracked `local-config.yaml` (see `local-config.example.yaml`). Three safety
nets guard the boundary: physically separate checkouts, a pre-commit hook, and
a GitHub Actions check on every push (see SETUP.md).

## License

[MIT](LICENSE): code and notes alike.
