# Knowledge Radar

Knowledge Radar is a local-first knowledge base for machine-learning and
regulatory topics. Monitoring agents extend it with new developments; the
resulting knowledge graph is published as a static, bilingual (EN/DE) site.

**Setup and running locally: see [SETUP.md](SETUP.md).** The default setup is
free and Ollama-only; no API key is required.

## Repository layout

Every folder has its own README with details.

| Path | Contents |
| --- | --- |
| `public/` | Published content: Markdown notes (`notes/`), the versioned knowledge graph (`graph/`), subject areas, redirects and link exclusions |
| `app/site/` | Static public site (React, GitHub Pages): graph + text view, DE/EN, client-side search |
| `app/backend/` | Python package `knowledge_radar`: notes and graph, static-site export, local index (Neo4j), local app API (FastAPI) |
| `app/frontend/` | Local app UI: chat, interview commands, Review Dashboard |
| `app/agents/` | Agent pipeline: validation, extraction, entity resolution, linking, weekly monitoring |
| `app/mcp/` | MCP servers |
| `docs/` | Note templates, extraction guidelines and examples, the weekly run as a graph |
| `eval/` | Gold standards and results for the extraction, relevance and resolution agents |
| `tests/` | Test suite (pytest) |
| `scripts/` | PowerShell helpers to set up and start the local app, the indices and Ollama; weekly run; private-data check |
| `.githooks/` | Git hooks that guard the public/private boundary |
| `schema.yaml` | Entity/relation schema, `visibility: public/private` per type |
| `sources.yaml` | Curated sources of the monitoring run (arXiv phrases, venues, feeds) |
| `local-config.example.yaml` | Template for the untracked per-machine configuration |
| `docker-compose*.yml` | Neo4j indices and the local app in Docker |
| `scheduled_task.xml` | Windows Task Scheduler definition (template) for the weekly run |

## Note format

Every note requires `title_en`, `title_de`, an `entity_type` that is a public
entity type in `schema.yaml`, and a non-empty list of absolute HTTP(S) URLs
under `sources`. Content is split into `## EN` and `## DE` sections.
`## Original Source Text (DE)` is optional for source text that must remain
untranslated. Links to other notes are written as `[[wikilinks]]`
(`[[slug]]`, `[[slug|label]]`); they become `RELATED_TO` edges in the graph.
The templates are described in [docs/note-templates.md](docs/note-templates.md).

## Public/private boundary

This repository never contains private data. The private data lives in a
separate repository checked out *next to* this one; its location is set in an
untracked `local-config.yaml` (see `local-config.example.yaml`). Three safety
nets guard the boundary: physically separate checkouts, a pre-commit hook, and
a GitHub Actions check on every push (see SETUP.md).

## Continuous integration

`.github/workflows/ci.yml` runs the private-data check, the note validation,
the tests and a build of the static site on every push. `.github/workflows/pages.yml` builds the static site
from `public/` and deploys it to GitHub Pages after every push to `main`.

## License

[MIT](LICENSE): code and notes alike.
