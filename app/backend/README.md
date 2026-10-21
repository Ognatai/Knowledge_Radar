# Backend package

The Python package `knowledge_radar` (in `knowledge_radar/`) and the Dockerfile
of the local app's API. Run modules from the repository root.

## Public knowledge base

- `notes.py`: loads and validates public notes (frontmatter, sources, EN/DE
  sections, entity types from `schema.yaml`, `[[wikilinks]]`).
- `templates.py`: checks notes against the templates in `docs/note-templates.md`.
- `graph.py`: loads and validates the versioned knowledge graph in
  `public/graph/` against `schema.yaml`.
- `areas.py`: subject areas (`public/areas.yaml`) and the "new and updated" list.
- `note_updates.py`: dated update entries in notes, and when a note is rewritten.
- `site_export.py`: exports notes and graph as JSON for the static site.

  ```powershell
  python -m app.backend.knowledge_radar.site_export
  ```

## Local index

- `index.py`: the local index in Neo4j (graph plus embedded note passages),
  updated incrementally by content hash.

  ```powershell
  python -m app.backend.knowledge_radar.index            # incremental update
  python -m app.backend.knowledge_radar.index rebuild    # from scratch
  python -m app.backend.knowledge_radar.index search "How does LoRA work?"
  ```

- `embeddings.py`: embeddings from Ollama (`qwen3-embedding:0.6b`).
- `private_index.py`: the private repository in its own, separate Neo4j database
  (same commands as `index.py`).

## Local app

- `api.py`: FastAPI app: read-only public notes, the chat and the endpoints of
  the interview commands and the Review Dashboard. It reads `public/notes/` by
  default; `KNOWLEDGE_RADAR_NOTES_DIR` may point at another **public-only**
  directory.

  ```powershell
  uvicorn app.backend.knowledge_radar.api:app --reload
  ```

- `chat.py`: chat over the public and the private index; the answer comes from
  the local model.
- `interviews.py`: the interview commands `/new-application`, `/new-round` and
  `/retro`, which write files into the private repository.
- `prep.py`: `/prep`, a briefing for one interview round.
- `study_guide.py`: a study guide for one round from the notes on the posting's
  topics.
- `research.py`: optional company and interviewer research with Claude and web
  search (needs an API key; only names leave the machine; monthly budget cap).
- `review.py`: the Review Dashboard: drafts of the weekly run and private inbox
  branches, with a decision per draft.
- `models.py`: typed data returned by the API and the site export.

## Configuration and private repository

- `config.py`: reads the untracked `local-config.yaml` (location of the private
  checkout, which must sit next to this repository, never inside it).
- `private_repo.py`: reads the private repository and builds its structural graph.
- `private_git.py`: git operations on the private checkout.
- `watchlist.py`: the only channel from the private repository to the monitoring
  run: the topic names of open knowledge gaps, nothing else.
