# Extraction guidelines

Rules for extracting entities and relations from a public note into
`public/graph/extractions/<slug>.yaml` (format: `app/backend/knowledge_radar/graph.py`).
The same rules apply to the hand-labelled gold standard in `eval/gold/` and to
the extraction agent, so that precision and recall measure the agent against a
fixed, explicit target.

## What is read

- Only the `## EN` section. The German section carries the same content, and
  evidence quotes must come from one language.
- Skipped: the LLM/legal notice, the closing sources list (`### Sources`,
  `### Official sources`), and Markdown tables that only repeat facts stated in
  the text.

## Entities (`discusses`)

A note **discusses** an entity if the entity is named in the text **and** the
text states at least one fact about it (what it is, does, is based on, who
developed it, how it compares). A bare mention, for example in an enumeration
of further reading, does not count.

- Use an existing entity if there is one: the entity of another note (its slug,
  e.g. `retrieval-augmented-generation`) or an entry in the registry
  (`public/graph/entities.yaml`). Match by meaning, not by spelling: "vector
  representations" is `embeddings`, "an LLM" is `large-language-models`.
- Otherwise register a new entity with a lowercase ASCII slug of its usual
  English name (`hipporag`, `personalized-pagerank`, `microsoft`).
- **Named** methods, systems, regulations, organisations, technologies and
  people are entities. **Generic** terms (an index, a prompt, LLM calls,
  documents) are not.
- **Concepts** are entities only if a note exists for them or the text defines
  or explains them; otherwise they stay plain text.
- **Named models and architectures** (BERT, GPT, Vision Transformer) are
  `Method` entities when the text describes them; models that only serve as an
  evaluation setting ("evaluated it on RoBERTa and GPT-3") are not discussed.
- **Components** that appear only in an enumeration of another method's parts
  ("it uses NF4, double quantization and paged optimizers") are not separate
  entities; a component that the text describes in its own sentence is.
- **People** are entities only when the text names them as actors ("developed
  by Geoffrey Hinton"). Citations such as "Edge et al. (2024)" are references,
  not entities.
- **Sources** (papers, articles) and their `MENTIONED_IN` / `PRESENTED_AT`
  relations are not extracted: a note's sources are already listed in its
  frontmatter.
- The note's own entity is always discussed and is not listed.

## Relations

- Only relations the text **states explicitly**. No background knowledge, no
  inference across sentences that the text does not draw itself.
- Every relation carries an `evidence` quote: a verbatim excerpt from the EN
  section (wikilinks as their label, emphasis removed) that supports it on its
  own. Keep it short, usually a clause.
- Both ends must be listed in `discusses` (or be the note's own entity).
- In relations of the note's own entity, the evidence may leave the subject
  implicit ("The Act implements the ePrivacy Directive" in the TDDDG note).
- Type constraints come from `schema.yaml`. If a stated relation fits no type,
  do not force it into one; record it as a proposal in `schema_proposals.md`.
- Each (from, type, to) triple appears at most once per note; pick the clearest
  evidence.

### Relation types in use

| Type | Meaning | Example evidence |
| --- | --- | --- |
| `BASED_ON` | builds on, extends, combines, uses as a component (also between technologies) | "GraphRAG extends retrieval-augmented generation"; "MCP builds on JSON-RPC" |
| `DEVELOPED_BY` | created or introduced by a person or organisation; for a regulation, the issuing body | "Microsoft's GraphRAG builds an entity graph"; "BCBS 239 is the Basel Committee's set of 14 principles" |
| `IMPLEMENTS` | a technology implements a method or concept; a national act transposes a directive or supplements a regulation | "transposes Directive (EU) 2016/943" |
| `IS_EXAMPLE_OF` | an instance or variant of a broader concept, method or technology | "BM25 is a ranking function" |
| `AMENDS` | a regulation amends, replaces or repeals another | "replaces the criminal provisions of sections 17 to 19 of the Act against Unfair Competition (UWG)" |
| `REGULATES` | a regulation or authority governs something | "protects trade secrets against unlawful acquisition" |
| `TAKES_PRECEDENCE_OVER` | a regulation prevails over another (lex specialis or an explicit precedence rule) | "the TDDDG (...) takes precedence over the BDSG" |
| `COMPLEMENTS` | each covers what the other does not, or they are explicitly combined; symmetric, so list each pair once in either order | "MCP is agent-to-tool, A2A agent-to-agent, and both are complementary" |
| `CONTRADICTS` | the text states the two are opposed or incompatible | |
