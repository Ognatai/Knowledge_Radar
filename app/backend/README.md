# Backend package

- `notes.py`: loads and validates public notes (frontmatter, sources, EN/DE
  sections, entity types from `schema.yaml`, `[[wikilinks]]`).
- `site_export.py`: exports notes and the two-layer graph (notes, entities,
  `DISCUSSES`, `RELATED_TO`) as JSON for the static site:
  `python -m app.backend.knowledge_radar.site_export`.
- `index.py`: the local index in Neo4j (graph plus embedded note passages),
  updated incrementally: `python -m app.backend.knowledge_radar.index`
  (see SETUP.md, "Local index").
- `embeddings.py`: embeddings from Ollama (`qwen3-embedding:0.6b`).
- `config.py`: reads the untracked `local-config.yaml` (private repo location).
- `api.py`: read-only FastAPI app, the starting point of the local app backend.
  It reads `public/notes/` by default; `KNOWLEDGE_RADAR_NOTES_DIR` may point at
  another **public-only** directory.

```powershell
uvicorn app.backend.knowledge_radar.api:app --reload
```
