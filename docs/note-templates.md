# Note templates

Every public note follows one of two templates, chosen by area
(`template` in `migration/vault-mapping.yaml`): **regulatory** for legal
topics, **technical** for methods, concepts, and technologies. Both share the
repository's note format: YAML frontmatter, a `## EN` and a `## DE` section
with identical structure, and an optional `## Original Source Text (DE)`.
Sub-sections use `###`, details `####`.

Common rules:

- Factual, reference style; no personal opinion, no first person.
- Every claim is covered by an entry in `sources`. Primary sources first
  (official journal, original paper, official documentation).
- Links to other notes are `[[slug]]` / `[[slug|label]]` wikilinks, placed in
  the sentence where the relation matters, not in a trailing link list.
  Related notes and backlinks are shown automatically from the graph.
  Inside Markdown tables, escape the pipe: `[[graphrag\|GraphRAG]]`.
- Links may point to notes that are planned but not written yet (IDs in
  `migration/vault-mapping.yaml`); give them a label, because they render as
  plain text until the target exists.
- Cite sources in the text as "Author et al. (year)" and list them in the
  closing sources section; the frontmatter `sources` holds the same URLs.
- EN and DE carry the same content; headings are translated.
- German text keeps established English technical terms instead of translating
  them: *Dense Retrieval*, *Sparse Retrieval*, *Cosine Similarity*, *Recall*,
  *Inverted Index*, *Approximate Nearest Neighbor Search*, *Faithfulness*.
  Translate only where an established German term exists (e.g. *Vektordatenbank*,
  *Wissensgraph*); legal terms follow the official German text.
- No manual table of contents: the site generates one from the `###`/`####`
  headings and shows it right after the TL;DR.
  Long outlines collapse to the top level.
- Every note opens with a short notice that it is LLM-generated (regulatory
  notes additionally state that it is not legal advice).

---

## Regulatory template

Based on the EU AI Act note, plus the "relevance for AI development" section
that 25 of 27 vault notes already have.

```markdown
---
title_en: "General Data Protection Regulation (GDPR)"
title_de: "Datenschutz-Grundverordnung (DSGVO)"
entity_type: Regulation
jurisdiction: EU                 # EU | DE | International
instrument: regulation           # regulation | directive | national-law | guideline | standard
status: in-force                 # proposed | adopted | in-force | partially-applicable | repealed
official_reference: "Regulation (EU) 2016/679"
consolidated_version: 2016-05-04 # date of the text the summary is based on
sources:
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/deu
---

## EN

> **Important notice:** LLM-generated summary; may be incomplete, outdated or
> wrong. Not legal advice; only the texts published in the official journal
> are authentic.

### TL;DR
What the act regulates, for whom, and its core mechanism (1–2 paragraphs).

### Key facts
| | |
|---|---|
| Official reference | … |
| Type / jurisdiction | … |
| In force / applies from | … |
| Competent authorities | … |
| Version summarised | consolidated text of … |

### Scope
Who and what is covered (personal, material, territorial scope); main exemptions.

### Chapter I — … / ### Part 1 — …  (structure and key provisions)
One `###` per chapter/part, titled as in the act, and one `####` per article
(or §) with its own summary, as in the EU AI Act note. There is no wrapping
"Structure" heading, so that chapters and articles both appear in the
generated table of contents. Acts without articles (e.g. BCBS 239,
guidelines) follow their own numbered principles or sections.

### Timeline
Adoption, entry into force, staged application dates, pending amendments.

### Enforcement and penalties
Supervision, fines, liability, remedies.

### Relationship to other acts
lex specialis / implementing law / overlaps, each with a wikilink,
e.g. [[tdddg]] implements [[eprivacy-directive]] in Germany.

### Relevance for AI development
Concrete consequences for building and operating AI systems, each linked to the
technical note concerned, e.g. Art. 17 GDPR → deletion favours keeping personal
data in a [[retrieval-augmented-generation|retrieval index]] rather than model weights.

### Recitals (optional)
### Annexes (optional)

### Official sources
Official journal (EN/DE), consolidated versions, amending acts.

## DE
(same structure: TL;DR · Eckdaten · Anwendungsbereich · Aufbau und
zentrale Regelungen · Zeitplan · Durchsetzung und Sanktionen · Verhältnis zu
anderen Rechtsakten · Bedeutung für die KI-Entwicklung · Erwägungsgründe ·
Anhänge · Amtliche Quellen)

## Original Source Text (DE)
Optional: verbatim key passages from the German official text, never translated.
```

**Depth:** every regulatory note covers its act article by article, in two
levels:

- **Standard:** every article gets a short summary of one to three sentences:
  what it regulates and for whom, with key numbers and dates in bold.
- **Detailed:** only for *important* articles, i.e. those that
  - create prohibitions, core obligations or rights of affected persons,
  - decide whether or how the act applies (scope, definitions that set the
    scope, classification rules, application dates), or
  - matter directly for building or operating AI systems (they are the ones
    linked from "Relevance for AI development").

  A detailed article uses `#####` sub-sections, as in Article 4 of the EU AI
  Act note: *What is it about?* · *What does the article require?* · *Who is
  affected?* · *What is not specified?* · *What could this mean in practice?*
  (clearly marked as possible implementation, not legal requirement) ·
  *When does it apply?* Sub-sections without content are left out.

Long acts therefore exceed the length guideline of the technical template;
that is intended.

---

## Technical template

Synthesises the recurring vault sections (Grundidee, Vorteile/Grenzen,
Vergleich, Merksatz, Regulatorischer Kontext) into one fixed order.

```markdown
---
title_en: "Retrieval-Augmented Generation"
title_de: "Retrieval-Augmented Generation"
entity_type: Method              # Method | Concept | Technology
aliases: [RAG]
sources:
  - https://arxiv.org/abs/2005.11401
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be
> incomplete, outdated or wrong.

### TL;DR
Definition in 2–3 sentences: what it is and which problem it solves.

### How it works
The core of every technical note: the mechanism, explained technically and
step by step in the order data actually flows. Start with a one-paragraph
overview and a small `text` diagram of the pipeline/architecture, then one
`####` per step, covering for each: what goes in and out, the algorithm or
data structure used, the important design choices and their trade-offs,
formulas where they define the step (as inline code). End with
`#### Origin and variants` (original paper, later variants).
Example: retrieval-augmented-generation (chunking → embedding → indexing →
query processing → retrieval → reranking → context construction → generation).

### When to use it
Typical use cases and the conditions under which the approach fits.

### Strengths and limitations
Two short lists.

### Comparison
Table against the closest alternatives, each a wikilink,
e.g. [[rag-vs-fine-tuning]], [[graphrag]].

### In practice (optional)
Evaluation, typical failure modes, pitfalls, parameter choices.

### Regulatory context (optional)
Only where a legal note says something concrete about this topic, e.g.
[[gdpr]] Art. 22 for automated decisions. Mirrors "Relevance for AI
development" in the regulatory notes.

### Key takeaway
One sentence.

### Sources
Original paper(s), authoritative documentation, surveys.

## DE
(same structure, opening with the notice "Hinweis: LLM-generierte
Zusammenfassung …": TL;DR · Funktionsweise · Wann einsetzen · Stärken und
Grenzen · Vergleich · In der Praxis · Regulatorischer Kontext · Merksatz · Quellen)
```

**Variant for `Technology`** notes (Python, Docker, LangGraph, …): "How it
works" becomes **Core concepts**, and **Common usage** (key commands/APIs as a
short table or code block) follows it. "Comparison" contrasts with alternative
tools.

**Length guideline:** driven by "How it works": roughly 1,000–2,500 words per
language for a method with a multi-step mechanism, less for narrow concepts.
An overview note explains every step at the depth needed to understand the
whole mechanism; sub-notes go deeper into single steps, as the vault already
does for RAG ([[rag-retrieval]], [[rag-chunking]], …).
