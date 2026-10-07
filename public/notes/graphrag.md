---
title_en: GraphRAG
title_de: GraphRAG
entity_type: Method
sources:
- https://arxiv.org/abs/2404.16130
- https://arxiv.org/abs/2408.08921
- https://arxiv.org/abs/2405.14831
- https://arxiv.org/abs/2410.05779
- https://arxiv.org/abs/2306.08302
- https://arxiv.org/abs/2005.11401
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

GraphRAG extends retrieval-augmented generation ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]) with graph structure: entities and relations are extracted into a knowledge graph, and retrieval follows the graph instead of only matching text chunks (Peng et al., 2024). Microsoft's GraphRAG builds an entity graph with an LLM and pregenerates summaries of communities of related entities, which answers global questions about a whole corpus much better than conventional RAG (Edge et al., 2024). Other approaches use graphs for multi-hop retrieval (Gutiérrez et al., 2024) or combine graph and vector retrieval (Guo et al., 2024).

### How it works

During indexing, an LLM extracts entities and relationships from the documents and builds a graph, often with summaries of groups of entities. At query time, the system retrieves relevant nodes, paths or community summaries and passes them, together with source text, to the LLM, which generates the answer.

```text
1. Why plain RAG falls short
▼
2. Graph-based indexing
▼
3. Communities and global questions
▼
4. Graph-guided retrieval
▼
5. Combining graphs and vectors
▼
6. Graph-enhanced generation
```

#### 1. Why plain RAG falls short

RAG retrieves passages from an external source to ground a model's answer (Lewis et al., 2020). It fails on global questions directed at an entire corpus, such as "What are the main themes in the dataset?", because these are query-focused summarisation tasks rather than retrieval tasks (Edge et al., 2024). Flat chunk retrieval also struggles to capture relations between entities spread across documents (Peng et al., 2024; Guo et al., 2024).

#### 2. Graph-based indexing

Peng et al. (2024) formalise the GraphRAG workflow in three stages: graph-based indexing, graph-guided retrieval and graph-enhanced generation. For indexing, an LLM extracts entities and relationships from the source documents to derive an entity knowledge graph (Edge et al., 2024); duplicate mentions of the same entity must be resolved, otherwise the graph fragments ([[entity-extraction|Entity Extraction]], [[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### 3. Communities and global questions

Edge et al. (2024) group closely related entities into communities and pregenerate a summary for each. For a question, each community summary produces a partial answer, and the partial answers are summarised into a final response. For global sensemaking questions over datasets in the range of 1 million tokens, this substantially improved the comprehensiveness and diversity of answers over a conventional RAG baseline.

#### 4. Graph-guided retrieval

HippoRAG, inspired by the hippocampal indexing theory of human memory, combines an LLM, a knowledge graph and the Personalized PageRank algorithm (Gutiérrez et al., 2024). On multi-hop question answering it outperformed state-of-the-art methods by up to 20%, and single-step retrieval with HippoRAG matched or beat iterative retrieval such as IRCoT while being 10 to 30 times cheaper and 6 to 13 times faster.

#### 5. Combining graphs and vectors

LightRAG incorporates graph structures into text indexing and retrieval with a dual-level retrieval system for low-level details and high-level knowledge, and combines graph structures with vector representations to retrieve related entities and their relationships efficiently (Guo et al., 2024). An incremental update algorithm integrates new data without rebuilding the index ([[vector-databases|Vector Databases]]).

#### 6. Graph-enhanced generation

Retrieved graph elements, community summaries and the underlying text passages are formatted into the prompt for generation (Peng et al., 2024; [[structured-context-construction|Structured Context Construction]]). Knowledge graphs give LLMs explicit external knowledge for inference and interpretability, which Pan et al. (2023) describe as knowledge-graph-enhanced LLMs.

#### Origin and variants

RAG (Lewis et al., 2020) retrieved text passages; GraphRAG (Edge et al., 2024) introduced community summaries for global questions, HippoRAG (Gutiérrez et al., 2024) graph-based multi-hop retrieval and LightRAG (Guo et al., 2024) dual-level graph-vector retrieval. Peng et al. (2024) survey the field, and Pan et al. (2023) place it within the broader combination of LLMs and knowledge graphs.

### When to use it

- When users ask global questions about a whole corpus, such as main themes or trends (Edge et al., 2024).
- When answers require connecting facts across several documents (multi-hop questions) (Gutiérrez et al., 2024).
- When the domain is strongly relational, as with norms, cases and parties in law ([[legal-ai|Legal AI]]).

### Strengths and limitations

**Strengths**
- Much more comprehensive and diverse answers to global questions than conventional RAG (Edge et al., 2024).
- Better multi-hop retrieval at lower cost than iterative retrieval (Gutiérrez et al., 2024).
- Explicit relations make retrieved context more interpretable (Pan et al., 2023).

**Limitations**
- Building the graph requires many LLM calls during indexing (Edge et al., 2024).
- Extraction errors and unresolved duplicates propagate into retrieval ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).
- Keeping the graph current needs incremental updates (Guo et al., 2024).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Conventional RAG | Retrieves similar text chunks (Lewis et al., 2020) | Local, factual questions |
| GraphRAG with community summaries | Entity graph plus pregenerated community summaries (Edge et al., 2024) | Global sensemaking questions |
| HippoRAG | Knowledge graph plus Personalized PageRank (Gutiérrez et al., 2024) | Multi-hop questions |
| LightRAG | Dual-level graph and vector retrieval with incremental updates (Guo et al., 2024) | Changing corpora |

### In practice

Classic RAG remains the default for local questions; GraphRAG is added when evaluation shows failures on global or multi-hop questions (Edge et al., 2024; [[rag-failure-modes|RAG: Failure Modes]]). Answers are evaluated for comprehensiveness and faithfulness ([[rag-evaluation|RAG: Evaluation]]), and graph quality is monitored, since errors in entities and relations directly affect retrieval (Peng et al., 2024).

### Key takeaway

GraphRAG turns documents into an entity graph and retrieves along it, which helps with global and multi-hop questions that plain chunk retrieval misses.

### Sources

- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Peng, B. et al. (2024). *Graph Retrieval-Augmented Generation: A Survey.* [arXiv:2408.08921](https://arxiv.org/abs/2408.08921)
- Gutiérrez, B. J. et al. (2024). *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models.* NeurIPS 2024. [arXiv:2405.14831](https://arxiv.org/abs/2405.14831)
- Guo, Z. et al. (2024). *LightRAG: Simple and Fast Retrieval-Augmented Generation.* [arXiv:2410.05779](https://arxiv.org/abs/2410.05779)
- Pan, S. et al. (2023). *Unifying Large Language Models and Knowledge Graphs: A Roadmap.* IEEE TKDE 2024. [arXiv:2306.08302](https://arxiv.org/abs/2306.08302)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

GraphRAG erweitert Retrieval-Augmented Generation ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]) um Graphstruktur: Entitäten und Beziehungen werden in einen Wissensgraphen extrahiert, und das Retrieval folgt dem Graphen, statt nur Textabschnitte abzugleichen (Peng et al., 2024). GraphRAG von Microsoft baut mit einem LLM einen Entitätengraphen auf und erzeugt vorab Zusammenfassungen von Gemeinschaften verwandter Entitäten; damit beantwortet es globale Fragen über ein ganzes Korpus deutlich besser als herkömmliches RAG (Edge et al., 2024). Andere Ansätze nutzen Graphen für Multi-Hop-Retrieval (Gutiérrez et al., 2024) oder kombinieren Graph- und Vektor-Retrieval (Guo et al., 2024).

### Funktionsweise

Bei der Indexierung extrahiert ein LLM Entitäten und Beziehungen aus den Dokumenten und baut einen Graphen auf, oft mit Zusammenfassungen von Gruppen von Entitäten. Zur Anfragezeit ruft das System relevante Knoten, Pfade oder Gemeinschaftszusammenfassungen ab und übergibt sie zusammen mit Quelltext dem LLM, das die Antwort erzeugt.

```text
1. Warum einfaches RAG nicht genügt
▼
2. Graphbasierte Indexierung
▼
3. Gemeinschaften und globale Fragen
▼
4. Graphgesteuertes Retrieval
▼
5. Graphen und Vektoren kombinieren
▼
6. Graphgestützte Generierung
```

#### 1. Warum einfaches RAG nicht genügt

RAG ruft Passagen aus einer externen Quelle ab, um die Antwort eines Modells zu fundieren (Lewis et al., 2020). Es scheitert an globalen Fragen an ein ganzes Korpus, etwa „Was sind die Hauptthemen im Datensatz?“, weil das Aufgaben der anfragebezogenen Zusammenfassung sind und keine Retrieval-Aufgaben (Edge et al., 2024). Auch Beziehungen zwischen Entitäten, die über Dokumente verstreut sind, erfasst flaches Chunk-Retrieval nur schwer (Peng et al., 2024; Guo et al., 2024).

#### 2. Graphbasierte Indexierung

Peng et al. (2024) formalisieren den GraphRAG-Ablauf in drei Stufen: graphbasierte Indexierung, graphgesteuertes Retrieval und graphgestützte Generierung. Für die Indexierung extrahiert ein LLM Entitäten und Beziehungen aus den Quelldokumenten, um einen Entitäten-Wissensgraphen abzuleiten (Edge et al., 2024); doppelte Erwähnungen derselben Entität müssen aufgelöst werden, sonst zerfällt der Graph ([[entity-extraction|Entitätsextraktion]], [[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### 3. Gemeinschaften und globale Fragen

Edge et al. (2024) fassen eng verwandte Entitäten zu Gemeinschaften (Communities) zusammen und erzeugen für jede vorab eine Zusammenfassung. Für eine Frage liefert jede Gemeinschaftszusammenfassung eine Teilantwort, und die Teilantworten werden zu einer Gesamtantwort zusammengefasst. Bei globalen Sensemaking-Fragen über Datensätze im Bereich von 1 Million Token verbesserte das Vollständigkeit und Vielfalt der Antworten gegenüber einer herkömmlichen RAG-Baseline deutlich.

#### 4. Graphgesteuertes Retrieval

HippoRAG, angeregt von der Hippocampus-Indexierungstheorie des menschlichen Gedächtnisses, verbindet ein LLM, einen Wissensgraphen und den Personalized-PageRank-Algorithmus (Gutiérrez et al., 2024). Bei Multi-Hop-Fragebeantwortung übertraf es die besten Verfahren um bis zu 20 %, und einstufiges Retrieval mit HippoRAG erreichte oder übertraf iteratives Retrieval wie IRCoT bei 10- bis 30-mal geringeren Kosten und 6- bis 13-mal höherer Geschwindigkeit.

#### 5. Graphen und Vektoren kombinieren

LightRAG bezieht Graphstrukturen in Indexierung und Retrieval von Text ein, mit einem zweistufigen Retrieval für Detailwissen und übergeordnetes Wissen, und kombiniert Graphstrukturen mit Vektorrepräsentationen, um verwandte Entitäten und ihre Beziehungen effizient abzurufen (Guo et al., 2024). Ein inkrementeller Aktualisierungsalgorithmus nimmt neue Daten auf, ohne den Index neu aufzubauen ([[vector-databases|Vektordatenbanken]]).

#### 6. Graphgestützte Generierung

Abgerufene Graphelemente, Gemeinschaftszusammenfassungen und die zugrunde liegenden Textpassagen werden für die Generierung in den Prompt eingebaut (Peng et al., 2024; [[structured-context-construction|Strukturierte Kontextbildung]]). Wissensgraphen geben LLMs ausdrückliches externes Wissen für Inferenz und Nachvollziehbarkeit, was Pan et al. (2023) als durch Wissensgraphen verbesserte LLMs beschreiben.

#### Ursprung und Varianten

RAG (Lewis et al., 2020) rief Textpassagen ab; GraphRAG (Edge et al., 2024) führte Gemeinschaftszusammenfassungen für globale Fragen ein, HippoRAG (Gutiérrez et al., 2024) graphbasiertes Multi-Hop-Retrieval und LightRAG (Guo et al., 2024) zweistufiges Graph-Vektor-Retrieval. Peng et al. (2024) geben einen Überblick über das Gebiet, und Pan et al. (2023) ordnen es in die allgemeinere Verbindung von LLMs und Wissensgraphen ein.

### Wann einsetzen

- Wenn Nutzende globale Fragen an ein ganzes Korpus stellen, etwa nach Hauptthemen oder Trends (Edge et al., 2024).
- Wenn Antworten Fakten aus mehreren Dokumenten verbinden müssen (Multi-Hop-Fragen) (Gutiérrez et al., 2024).
- Wenn das Fachgebiet stark relational ist, etwa Normen, Entscheidungen und Beteiligte im Recht ([[legal-ai|Legal AI]]).

### Stärken und Grenzen

**Stärken**
- Deutlich vollständigere und vielfältigere Antworten auf globale Fragen als herkömmliches RAG (Edge et al., 2024).
- Besseres Multi-Hop-Retrieval bei geringeren Kosten als iteratives Retrieval (Gutiérrez et al., 2024).
- Ausdrückliche Beziehungen machen den abgerufenen Kontext nachvollziehbarer (Pan et al., 2023).

**Einschränkungen**
- Der Aufbau des Graphen erfordert bei der Indexierung viele LLM-Aufrufe (Edge et al., 2024).
- Extraktionsfehler und nicht aufgelöste Dubletten pflanzen sich ins Retrieval fort ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).
- Den Graphen aktuell zu halten erfordert inkrementelle Aktualisierungen (Guo et al., 2024).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Herkömmliches RAG | Ruft ähnliche Textabschnitte ab (Lewis et al., 2020) | Lokale Faktenfragen |
| GraphRAG mit Gemeinschaftszusammenfassungen | Entitätengraph plus vorab erzeugte Zusammenfassungen (Edge et al., 2024) | Globale Sensemaking-Fragen |
| HippoRAG | Wissensgraph plus Personalized PageRank (Gutiérrez et al., 2024) | Multi-Hop-Fragen |
| LightRAG | Zweistufiges Graph- und Vektor-Retrieval mit inkrementellen Aktualisierungen (Guo et al., 2024) | Sich ändernde Korpora |

### In der Praxis

Klassisches RAG bleibt für lokale Fragen der Standard; GraphRAG kommt hinzu, wenn die Evaluation Schwächen bei globalen oder Multi-Hop-Fragen zeigt (Edge et al., 2024; [[rag-failure-modes|RAG: Typische Fehlerarten]]). Antworten werden auf Vollständigkeit und Treue zur Quelle evaluiert ([[rag-evaluation|RAG: Evaluation]]), und die Graphqualität wird überwacht, da Fehler bei Entitäten und Beziehungen das Retrieval direkt beeinträchtigen (Peng et al., 2024).

### Merksatz

GraphRAG macht aus Dokumenten einen Entitätengraphen und ruft entlang dieses Graphen ab; das hilft bei globalen und Multi-Hop-Fragen, die einfaches Chunk-Retrieval verfehlt.

### Quellen

- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Peng, B. et al. (2024). *Graph Retrieval-Augmented Generation: A Survey.* [arXiv:2408.08921](https://arxiv.org/abs/2408.08921)
- Gutiérrez, B. J. et al. (2024). *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models.* NeurIPS 2024. [arXiv:2405.14831](https://arxiv.org/abs/2405.14831)
- Guo, Z. et al. (2024). *LightRAG: Simple and Fast Retrieval-Augmented Generation.* [arXiv:2410.05779](https://arxiv.org/abs/2410.05779)
- Pan, S. et al. (2023). *Unifying Large Language Models and Knowledge Graphs: A Roadmap.* IEEE TKDE 2024. [arXiv:2306.08302](https://arxiv.org/abs/2306.08302)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
