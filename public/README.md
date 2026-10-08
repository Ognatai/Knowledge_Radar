# Public content

`notes/` contains bilingual, factual Markdown notes with YAML frontmatter and
at least one source URL; notes link to each other via `[[wikilinks]]`.
`graph/` is the versioned knowledge graph: `entities.yaml` registers entities
without a note of their own (with aliases), and `extractions/<note>.yaml` lists
the entities each note discusses and the relations it supports, each with a
verbatim evidence quote from the note. Only this directory feeds
the public site export; nothing here may come from the private repository.
