# Public content

Everything published on the site comes from this folder, and only from it.
Nothing here may come from the private repository.

| Path | Contents |
| --- | --- |
| `notes/` | Bilingual (EN/DE), factual Markdown notes with YAML frontmatter and at least one source URL; notes link to each other via `[[wikilinks]]`. Format and templates: `docs/note-templates.md` |
| `graph/entities.yaml` | The entity registry: entities without a note of their own, with aliases and a short sourced text |
| `graph/extractions/<note>.yaml` | The entities each note discusses and the relations it supports, each with a verbatim evidence quote from the note |
| `areas.yaml` | Subject areas in display order; every note belongs to exactly one |
| `redirects.yaml` | Renamed notes and entities (old → new), so that old addresses keep working |
| `link-exclusions.yaml` | Mentions the linking agent must not turn into links, with the reason |

Notes, graph and areas are checked by `python -m app.agents.validate_notes`.
The site export (`python -m app.backend.knowledge_radar.site_export`) checks the
redirects and turns everything into `public/data/site-data.json`, which is
generated and not committed.
