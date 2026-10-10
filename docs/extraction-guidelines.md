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
  (`public/graph/entities.yaml`). Match by meaning, not by spelling: a
  paraphrase, abbreviation or plural of a known entity refers to it.
- Otherwise register a new entity with a lowercase ASCII slug of its usual
  English name (`bm25`, `openai`).
- **Named** methods, systems, regulations, organisations, technologies and
  people are entities. **Generic** terms (an index, a prompt, LLM calls,
  documents) are not.
- **Concepts** are entities only if a note exists for them or the text defines
  or explains them; otherwise they stay plain text.
- **Named models and architectures** are `Method` entities when the text
  describes them; models that only serve as an evaluation setting ("evaluated
  on model X and model Y") are not discussed.
- **Datasets** (benchmarks and corpora such as GLUE or MS MARCO) are `Dataset`
  entities when the text says what they contain or measure; a bare name in a
  list of results is not enough.
- **Components** that appear only in an enumeration of another method's parts
  ("it uses A, B and C") are not separate
  entities; a component that the text describes in its own sentence is.
- **People** are entities only when the text names them as actors ("developed
  by Geoffrey Hinton"). Citations such as "Author et al. (2024)" are references,
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
  implicit ("The Act implements Directive D" in the note about that act).
- Type constraints come from `schema.yaml`. If a stated relation fits no type,
  do not force it into one; record it as a proposal in `schema_proposals.md`.
- Each (from, type, to) triple appears at most once per note; pick the clearest
  evidence.
- Relations between **any** two discussed entities count, not only those of
  the note's own entity: in a note about X, "Y builds on Z" gives `Y BASED_ON Z`.
- **Direction**: the subject (`from`) is the more specific, newer or dependent
  side. A method that the note lists as an example of the note's topic is the
  subject of `IS_EXAMPLE_OF`; the topic is not `BASED_ON` its examples.
- Choose the most specific type: a technology that realises a method or concept
  `IMPLEMENTS` it (not `BASED_ON`); a regulation that governs something
  `REGULATES` it (not `IMPLEMENTS`); `IMPLEMENTS` between regulations only for
  transposition or supplementing; a regulation never `IMPLEMENTS` a method or
  concept. An act that builds on another act's framework without transposing
  or changing it is `BASED_ON` it.
- `COMPLEMENTS` only when the text says so explicitly (complement, combine, used
  together, each covers what the other does not). Being related, mentioned in
  the same section or linked is not enough.

### Relation types in use

Examples use placeholders; A, B are entities discussed in the note.

| Type | Meaning (from → to) | Typical wording |
| --- | --- | --- |
| `BASED_ON` | A builds on, extends, combines or uses B as a component (also between technologies, and between regulations that build on another act's framework) | "A extends B", "A combines B and C", "A builds on B" |
| `DEVELOPED_BY` | A was created or introduced by person or organisation B; for a regulation, B issued it | "B's A", "A, introduced by B", "B published A" |
| `IMPLEMENTS` | technology A realises method or concept B; national act A transposes directive B or supplements regulation B | "A is an implementation of B", "A transposes B" |
| `IS_EXAMPLE_OF` | A is an instance or variant of the broader concept, method or technology B (a concept can be an example of a broader concept) | "A is a B", "Bs such as A" |
| `AMENDS` | regulation A amends, replaces or repeals regulation B | "A replaces B", "A amended B", "B is repealed" |
| `EVALUATES` | dataset or evaluation method A measures method, concept or technology B | "A measures B", "A is a benchmark for B" |
| `REGULATES` | regulation or authority A governs B | "A protects B", "A requires B", "A supervises B" |
| `TAKES_PRECEDENCE_OVER` | regulation A prevails over regulation B (lex specialis or an explicit precedence rule) | "A takes precedence over B" |
| `COMPLEMENTS` | A and B cover each other's gaps or are explicitly combined; symmetric, list each pair once | "A and B are complementary", "A is combined with B" |
| `CONTRADICTS` | the text states that A and B are opposed or incompatible | "A contradicts B" |
