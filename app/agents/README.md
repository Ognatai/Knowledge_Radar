# Agent pipeline

The agents that check, extend and connect the knowledge base. All language-model
calls go to a local Ollama server (`llm.py`; `OLLAMA_BASE_URL`,
`KNOWLEDGE_RADAR_MODEL`). Run everything from the repository root.

## Notes and graph

- `validate_notes.py`: checks every public note against the note contract, the
  note templates (`docs/note-templates.md`) and the graph files in
  `public/graph/` against `schema.yaml`. Runs in CI.

  ```powershell
  python -m app.agents.validate_notes
  ```

- `extraction.py`: the extraction agent. Reads a note and proposes the entities it
  discusses and the relations it supports, each with an evidence quote, following
  `docs/extraction-guidelines.md`. Output is constrained to the types in
  `schema.yaml` and validated; invalid relations go back to the model for correction.
- `entity_resolution.py`: decides whether a newly extracted entity is one the
  graph already knows under another name (embedding shortlist, then confirmation
  by the model). A match becomes an alias of the known entity.
- `linking.py`: adds `[[wikilinks]]` where a note mentions another note's title or
  alias without linking it. Algorithmic; an embedding check makes sure the mention
  means the same thing. Lasting rejections go to `public/link-exclusions.yaml`.

  ```powershell
  python -m app.agents.linking                         # report the suggestions
  python -m app.agents.linking --target gpt --apply    # links to one note
  python -m app.agents.linking --source gpt --apply    # links inside one note
  ```

- `evaluate_extraction.py`, `evaluate_resolution.py`: score the agents against the
  gold standards in `eval/` (see `eval/README.md`).

## Sources for writing notes

- `sources.py`: source metadata and citations; arXiv entries are verified against
  an expected title fragment and cached under `.knowledge-radar/cache/arxiv/`.
- `eurlex.py`: fetches EUR-Lex documents with a headless Edge/Chrome (EUR-Lex
  blocks plain HTTP clients; `KNOWLEDGE_RADAR_BROWSER` overrides the browser path)
  and splits them into articles.
- `cellar.py`: legal status of EU acts (consolidated versions, amendments,
  repeals) from the CELLAR SPARQL endpoint.

  ```powershell
  python -m app.agents.cellar 32023R2854
  ```

- `gesetze.py`: German federal law from gesetze-im-internet.de (official XML),
  split into sections.
- `legal_text.py`: the source-independent structure of legal texts shared by
  `eurlex` and `gesetze`.

## Weekly monitoring (`monitoring/`)

The weekly run finds new developments and turns them into proposals for review.
`weekly.py` runs all steps in order as a LangGraph state graph
(`docs/weekly-run.md`):

1. validate the public notes;
2. update the local index (Neo4j must be running);
3. update the private checkout and its structure (`private_sync.py`, optional);
4. source agents: new findings of the last 7 days (`run_sources.py`);
5. relevance agent: proposals (`relevance.py`, `promotion.py`);
6. curator: drafts with review reports (`curator.py`);
7. inbox: findings on open knowledge gaps, as a branch in the private repository
   (`inbox.py`, optional);
8. the drafts on a local branch `proposals/<run>` (`propose.py`), never pushed.

```powershell
python -m app.agents.monitoring.weekly             # the whole run
python -m app.agents.monitoring.weekly --diagram   # the run as a Mermaid diagram
```

The steps can also be run on their own:

- `run_sources.py`: fetches Semantic Scholar, arXiv, Hugging Face Daily Papers
  and the feeds from `sources.yaml` and keeps what earlier runs have not seen.
  Findings go to `.knowledge-radar/monitoring/runs/findings-<time>.jsonl`.

  ```powershell
  python -m app.agents.monitoring.run_sources --dry-run   # counts only
  python -m app.agents.monitoring.run_sources --days 14
  ```

- `relevance.py`: compares each finding with the closest notes in the local index
  and decides `irrelevant`, `duplicate`, `update` or `new_topic`; keeps at most
  `max_proposals_per_week` proposals.
- `promotion.py`: registry entities discussed by more than three notes, as
  candidates for a note of their own.
- `curator.py`: drafts an update entry or a new note for each proposal, with
  quality gates (`quality.py`: originality and faithfulness to the sources).
  Drafts land in `.knowledge-radar/monitoring/drafts/<run>/`, never in `public/`.
  Full texts come from `source_texts.py`, foundational works from
  `foundations.py` (OpenAlex).
- `propose.py`: puts a run's drafts on the local branch `proposals/<run>`, so that
  `git diff main proposals/<run>` shows the proposal.
- `inbox.py`: proposes private reading lists for knowledge-gap topics as a branch
  in the private repository.
- `evaluate_relevance.py`: scores the relevance agent against
  `eval/relevance/gold.yaml`.
- Building blocks: `feeds.py` (arXiv, Hugging Face, RSS/Atom parsing),
  `semantic_scholar.py`, `config.py` (validation of `sources.yaml`),
  `findings.py` (the shared `Finding` record and the store of seen findings).

## Private repository

These modules work on the separate private repository (location in
`local-config.yaml`), use only the local model, and write their results into the
private repository, never into this one.

- `private_ingest.py`: builds the structural graph of the private repository from
  its folders and frontmatter.
- `private_extract.py`: entities and relations from private documents, and the
  requirements of job postings matched to knowledge-base notes.
- `posting_topics.py`: splits a posting into topics to study and finds the note
  on each.
- `private_refresh.py`: brings the private side up to date after the local app
  wrote to it (structure, index, requirements, extraction).
- `private_sync.py`: fast-forwards the private checkout before the weekly run and
  rebuilds its structure.
