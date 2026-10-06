---
title_en: 'RAG: Chunking'
title_de: 'RAG: Chunking'
entity_type: Method
sources:
- https://arxiv.org/abs/2312.10997
- https://arxiv.org/abs/2312.06648
- https://arxiv.org/abs/2409.04701
- https://arxiv.org/abs/2307.03172
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Chunking decomposes documents into smaller, contextually coherent units to enable precise retrieval and avoid context loss inherent in whole-document indexing. Chen et al. (2023) demonstrated that fine-grained units significantly outperform passage-level units in retrieval tasks, improving downstream QA performance. This approach addresses the precision and context preservation challenges in [[rag-retrieval|retrieval]].

### How it works

Chunking turns documents into the units that are embedded, indexed and later placed into the prompt. A splitting strategy (fixed-size, semantic, propositions or late chunking) is chosen per corpus; enrichment with metadata and overlap between neighbouring chunks are applied on top of it, and parent-child retrieval separates the unit that is searched from the unit that is shown to the model. Chunk size and the order of chunks in the prompt then determine how well the retrieved content can be used in [[rag-retrieval|retrieval]] and generation.

```text
document
 ▼
splitting strategy: fixed-size | semantic | propositions | late chunking
 ▼
+ overlap between neighbours, + metadata (context enrichment)
 ▼
chunks ─▶ embedding and index ─▶ retrieved chunks ─▶ prompt
   └─ optional: small child chunks linked to larger parent chunks
```

#### 1. Fixed-Size Chunking

Fixed-size chunking splits input text into uniform-length segments, typically defined by a fixed token count (e.g., 500 tokens) or character count. The algorithm processes text sequentially, dividing it into contiguous chunks of the target length without semantic analysis. This approach is computationally efficient, structure-agnostic, and requires minimal preprocessing. However, it risks fragmenting semantic units (e.g., splitting a sentence or concept across chunks), which can degrade embedding quality and retrieval precision. The optimal chunk size balances precision (smaller chunks) against context preservation (larger chunks), and is empirically tuned based on the embedding model [[embeddings|Embeddings]] and retrieval task constraints. There is no universal optimum; the size has to be evaluated for the corpus and the embedding model.

#### 2. Semantic Chunking

Semantic chunking places chunk boundaries where the content changes instead of after a fixed length. A common implementation embeds consecutive sentences and starts a new chunk where the similarity between neighbouring sentences drops below a threshold; structure-based variants split along headings, paragraphs or, in legal texts, articles. Chunks therefore vary in length but are more likely to contain one coherent topic, at the cost of an additional embedding pass and a threshold that needs tuning.

A finer-grained alternative uses propositions as retrieval units: Chen et al. (2023) define propositions as atomic expressions in a text, each a concise, self-contained statement of one factoid. Indexing a corpus by propositions significantly outperformed passage-level indexing in their retrieval experiments and, given a specific computation budget, prompts built from such fine-grained units improved downstream question answering. Proposition indexing produces many more units than passage indexing, which increases index size and the cost of creating the units.

#### 3. Context Enrichment

Context Enrichment appends domain-specific metadata (e.g., document title, section, article number) to each chunk to resolve semantic ambiguities when retrieved independently. Inputs are the chunk text and pre-extracted structural metadata (e.g., from document headers or sections). The output is a structured object containing the text and metadata fields (e.g., `{"text": "...", "metadata": {"title": "DSGVO", "article": "5", "section": "2"}}`). The algorithm stores metadata as key-value pairs without modifying the text, avoiding embedding overhead. Design choices prioritize minimal, high-value metadata (e.g., document identifier and section) to balance interpretability gains against token cost. Trade-offs include a small storage increase versus the critical prevention of retrieval ambiguity (e.g., resolving "Absatz 2" to "DSGVO Art. 5 para. 2"). This step is essential for structured documents (e.g., legal, technical) where isolated chunks lack referential context, as seen in domains requiring precise semantic grounding during [[rag-retrieval|retrieval]].

#### 4. Overlap

Overlap between adjacent chunks shares a fixed number of tokens (e.g., `o` tokens) between consecutive chunks to mitigate context loss at boundaries. Given a tokenized document and parameters `c` (chunk size) and `o` (overlap size), chunks are generated via a sliding window: chunk `i` spans tokens from `i*(c - o)` to `i*(c - o) + c`. This ensures semantically connected content (e.g., sentences spanning boundaries) remains contiguous within at least one chunk, preserving contextual coherence for retrieval. Trade-offs include increased storage due to redundant token representation (by `o` tokens per adjacent pair), higher computational cost for embedding generation, and potential retrieval of overlapping content. Typical overlaps are a small fraction of the chunk size; larger overlaps add redundancy without adding information.

#### 5. Late Chunking

Late chunking embeds the entire document as a single sequence through a long-context embedding model, generating token-level embeddings before applying chunking operations. This differs from early chunking (where documents are split before embedding) by preserving full contextual relationships during embedding. Inputs consist of raw text tokens, and outputs are chunk embeddings derived by grouping token embeddings into windows (e.g., fixed-size or sliding windows) followed by mean pooling. The algorithm leverages long-context models to avoid context loss at chunk boundaries—critical for capturing semantically interdependent elements like pronoun references or cross-chunk dependencies. Design trade-offs include higher computational cost for full-document embedding compared to early chunking, but this yields superior retrieval accuracy for tasks requiring document-wide coherence, as demonstrated by Günther et al. (2024). The method is model-agnostic and requires no additional training, making it compatible with existing [[embeddings|Embeddings]] pipelines while enhancing [[rag-retrieval|RAG: Retrieval]] robustness.

#### 6. Parent-Child Retrieval

Parent-Child Retrieval decouples the retrieval unit (child) from the context unit (parent). Children (e.g., sentences or short paragraphs) are embedded and indexed in a vector database for precise retrieval, while parents (e.g., document sections or full documents) provide contextual support for LLM generation. Inputs consist of document-level child-parent pairs and a query; outputs are top-k retrieved children with their linked parent contexts. The algorithm employs a two-level indexing structure: children are stored in the vector database and searched by embedding similarity, and each child record includes metadata (e.g., parent ID) for context retrieval. Design choices include child granularity (e.g., sentence vs. paragraph level) and linking method (e.g., document ID or section metadata). Trade-offs involve increased indexing complexity (due to metadata management) versus improved retrieval precision (smaller units minimize noise) and sufficient context (larger parents avoid isolated fragments). This resolves the inherent tension between fine-grained retrieval and contextual completeness, as critical in [[rag-retrieval|retrieval]] systems.

#### 7. Chunk Size and Position in the Context

Chunk size directly influences retrieval precision and context completeness: smaller chunks enhance precision by isolating atomic facts but risk incomplete context, while larger chunks preserve coherence at the cost of embedding over-compression and reduced retrieval accuracy. The number of chunks fitting within a model's context window (e.g., 8192 tokens) is constrained by `max_tokens / chunk_size`, limiting the retrievable context depth. Crucially, Liu et al. (2023) demonstrated that language models exhibit strong positional bias, with performance degrading significantly when relevant information resides in the middle of long contexts compared to the beginning or end. This necessitates ordering retrieved chunks to prioritize high-relevance content at sequence start/end, mitigating "lost-in-the-middle" effects. Design choices involve selecting chunk sizes that balance contextual integrity against context window limits, while structuring the chunk sequence to align with model behavior—typically via reranking to position key chunks early. This trade-off optimizes prompt efficiency and output quality in [[rag-retrieval|retrieval]]-augmented systems.

#### Origin and variants

Fixed-size splitting with overlap is the long-standing default of retrieval pipelines. Proposition-level indexing (Chen et al., 2023) moved the retrieval unit down to single factoids and outperformed passage-level indexing. Late chunking (Günther et al. 2024) processes entire documents as input, embedding them first using long-context models before applying chunking after embedding and before mean pooling. This preserves contextual relationships lost in conventional splitting, yielding embeddings where each chunk captures full contextual information. Variants include structure-based chunking (e.g., legal contracts split by clauses or articles), which leverages inherent document structures to form chunks aligned with semantic units. Proposition indexing improves retrieval precision but multiplies the number of units, while late chunking improves the context captured in each chunk embedding at the cost of encoding whole documents with a long-context model. Structure-based chunking maintains document semantics but requires format-specific parsers, limiting generality. These approaches optimize the [[embeddings|embedding]] process for retrieval efficiency and accuracy.

### When to use it

- When high precision in retrieval is critical: Fine-grained chunking (e.g., proposition-level) significantly outperforms passage-level indexing in retrieval tasks, as demonstrated by Chen et al. (2023) in [[rag-retrieval|retrieval]].
- When using dense vector-based retrieval: Shorter text segments minimize semantic over-compression in embeddings, improving retrieval effectiveness per Günther et al. (2024).
- When many chunks are placed into a long prompt: models use information at the beginning or end of a long context best, so chunk size and ordering should keep the most relevant chunks there (Liu et al., 2023).

### Strengths and limitations

**Strengths**
- Fine-grained chunking (e.g., propositions) significantly improves retrieval precision and downstream QA performance compared to passage-level units (Chen et al. (2023)).
- Late chunking preserves full contextual information by embedding the entire document before chunking, yielding superior retrieval results without additional training (Günther et al. (2024)).

**Limitations**
- Traditional fixed-size chunking fragments semantic units, causing context loss and sub-optimal embeddings (Günther et al. (2024)).
- Models use information in the middle of a long context markedly worse than at its beginning or end (Liu et al., 2023); many or long chunks therefore have to be ordered carefully, see [[rag-failure-modes|failure modes]].
- The best strategy depends on document structure and embedding model and has to be tuned per corpus.

### Comparison

| Approach             | How it differs                                      | Suited for |
|----------------------|-----------------------------------------------------|------------|
| Fixed-size           | Splits text by fixed token count (e.g., 500 tokens), potentially breaking semantic units and increasing context loss. | General use cases in [[rag-retrieval|retrieval]] systems where simplicity and speed are prioritized over context preservation. |
| Semantic-based       | Splits at semantic boundaries (e.g., propositions), capturing atomic facts and improving retrieval precision over passage-level indexing (Chen et al., 2023). | Documents requiring high context coherence; critical for fact-based QA tasks where fine-grained retrieval enhances downstream performance. |
| Late chunking        | Embeds entire document first using long-context models, then applies chunking, preserving full context in embeddings (Günther et al., 2024). | Systems using long-context embedding models (e.g., [[embeddings|embeddings]] pipelines) where context loss during embedding degrades retrieval quality. |

Semantic-based chunking minimizes context loss in retrieval compared to fixed-size methods, while late chunking eliminates embedding compression artifacts without additional training.

### In practice

Evaluation requires measuring retrieval metrics (e.g., recall@k) and downstream task accuracy (e.g., QA F1), as Chen et al. (2023) found indexing with fine-grained units (propositions) significantly outperforms passage-level indexing. Typical failure modes include context loss at chunk boundaries (Günther et al. (2024)) and performance degradation when relevant information is located in the middle of long contexts (Liu et al. (2023)). Parameter choices involve selecting chunk granularity (fine-grained units preferred for precision) and overlap size (to reduce boundary context loss), with optimal settings determined through [[rag-retrieval-evaluation|retrieval evaluation]] and documented in [[rag-failure-modes|failure modes]].

### Key takeaway

Chunking requires balancing retrieval precision against contextual coherence, as finer-grained units improve precision but risk context loss.

### Sources

- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Chen, T. et al. (2023). *Dense X Retrieval: What Retrieval Granularity Should We Use?* [arXiv:2312.06648](https://arxiv.org/abs/2312.06648)
- Günther, M. et al. (2024). *Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models.* [arXiv:2409.04701](https://arxiv.org/abs/2409.04701)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Chunking zerlegt Dokumente in kleinere, kontextuell zusammenhängende Einheiten, um präzise Retrieval zu ermöglichen und den inhärenten Kontextverlust bei der Indexierung ganzer Dokumente zu vermeiden. Chen et al. (2023) zeigten, dass feinkörnige Einheiten bei Retrieval-Aufgaben deutlich besser abschneiden als passagebasierte Einheiten, was die Leistung bei nachfolgenden QA-Aufgaben verbessert. Dieser Ansatz behebt die Herausforderungen bei Präzision und Kontexterhaltung im [[rag-retrieval|Retrieval]].

### Funktionsweise

Chunking verwandelt Dokumente in die Einheiten, die eingebettet, indiziert und später in den Prompt platziert werden. Eine Aufteilungsstrategie (fixed-size, semantic, propositions oder late chunking) wird pro Korpus gewählt; darauf aufbauend wird mit Metadaten-Enrichment und Überlappung zwischen benachbarten Chunks gearbeitet, und Parent-Child Retrieval trennt die Einheit, die gesucht wird, von der Einheit, die dem Modell gezeigt wird. Die Chunkgröße und die Reihenfolge der Chunks im Prompt bestimmen dann, wie gut der abgerufene Inhalt in [[rag-retrieval|retrieval]] und Generierung genutzt werden kann.

```text
Dokument
 ▼
Aufteilungsstrategie: fixed-size | semantic | propositions | late chunking
 ▼
+ Überlappung zwischen Nachbarn, + Metadaten (Kontext-Enrichment)
 ▼
Chunks ─▶ Einbettung und Index ─▶ abgerufene Chunks ─▶ Prompt
   └─ optional: kleine Kind-Chunks, die mit größeren Eltern-Chunks verknüpft sind
```

#### 1. Fixgröße Chunking

Fixgröße Chunking teilt den Eingabetext in Segmente gleicher Länge auf, typischerweise definiert durch eine feste Anzahl von Tokens (z. B. 500 Tokens) oder Zeichenanzahl. Der Algorithmus verarbeitet den Text sequenziell und teilt ihn in kontinuierliche Abschnitte der Zielgröße auf, ohne semantische Analyse. Dieser Ansatz ist rechenleistungseffizient, strukturunabhängig und benötigt minimale Vorverarbeitung. Allerdings besteht das Risiko, semantische Einheiten (z. B. das Aufteilen eines Satzes oder Konzepts über mehrere Abschnitte) zu zerstören, was die Qualität der Embeddings und die Präzision der Retrieval-Operationen beeinträchtigen kann. Die optimale Chunkgröße balanciert Präzision (kleinere Chunks) gegen Kontexterhaltung (größere Chunks) und wird empirisch anhand des Embedding-Modells [[embeddings|Embeddings]] und der Retrieval-Aufgabenanforderungen abgestimmt. Es gibt keinen universellen Optimum; die Größe muss für das Corpus und das Embedding-Modell bewertet werden.

#### 2. Semantisches Chunking

Beim semantischen Chunking werden Chunk-Grenzen dort gesetzt, wo sich der Inhalt ändert, anstatt nach einer festen Länge. Eine gängige Umsetzung besteht darin, aufeinanderfolgende Sätze zu embedden und einen neuen Chunk zu beginnen, sobald die Ähnlichkeit zwischen benachbarten Sätzen unter einen Schwellenwert fällt; strukturbezogene Varianten teilen entlang von Überschriften, Absätzen oder, bei rechtlichen Texten, Artikeln. Chunks variieren daher in ihrer Länge, enthalten aber wahrscheinlicher einen zusammenhängenden Thema, wobei dies den zusätzlichen Embedding-Vorgang und eine Schwellenwert-Einstellung erfordert.

Eine feiner granulierte Alternative verwendet Propositionen als Retrieval-Einheiten: Chen et al. (2023) definieren Propositionen als atomare Ausdrücke in einem Text, wobei jede Proposition eine präzise, eigenständige Aussage eines Fakts darstellt. Das Indizieren eines Corpora anhand von Propositionen übertraf in ihren Retrieval-Experimenten das Indizieren auf Passage-Ebene deutlich, und bei einem spezifischen Rechenbudget verbesserten Prompts, die aus solchen fein granulierten Einheiten bestanden, die downstream Fragebeantwortung. Propositions-Indizierung erzeugt deutlich mehr Einheiten als Passage-Indizierung, was die Indexgröße erhöht und den Aufwand für die Erstellung der Einheiten steigert.

#### 3. Kontextbereicherung

Die Kontextbereicherung fügt domänenspezifische Metadaten (z. B. Dokumenttitel, Abschnitt, Artikelnummer) jedem Chunk hinzu, um semantische Mehrdeutigkeiten zu lösen, wenn dieser unabhängig abgerufen wird. Die Eingaben sind der Chunk-Text und vorab extrahierte strukturelle Metadaten (z. B. aus Dokumentüberschriften oder Abschnitten). Das Ergebnis ist ein strukturierter Objekt, der den Text und Metadatenfelder enthält (z. B. `{"text": "...", "metadata": {"title": "DSGVO", "article": "5", "section": "2"}}`). Der Algorithmus speichert Metadaten als Schlüssel-Wert-Paare, ohne den Text zu verändern, um die Overhead durch Embedding zu vermeiden. Die Gestaltungswahl priorisiert minimale, hochwertige Metadaten (z. B. Dokumentidentifikator und Abschnitt), um den Gewinn an Interpretierbarkeit gegen den Token-Kosten zu balancieren. Kompromisse umfassen einen geringen Speicherbedarf gegenüber der kritischen Vermeidung von Retrieval-Mehrdeutigkeiten (z. B. Auflösen von „Absatz 2“ zu „DSGVO Art. 5 Abs. 2“). Dieser Schritt ist für strukturierte Dokumente (z. B. rechtliche, technische) entscheidend, bei denen isolierte Chunks referenziellen Kontext fehlen, wie er in Bereichen erforderlich ist, die präzise semantische Grundierung während [[rag-retrieval|Abfrage]] benötigen.

#### 4. Überlappung

Die Überlappung zwischen benachbarten Chunks teilt eine festgelegte Anzahl von Tokens (z. B. `o` Tokens) zwischen aufeinanderfolgenden Chunks auf, um den Verlust von Kontext an den Grenzen zu verringern. Gegeben ein tokenisiertes Dokument und die Parameter `c` (Chunk-Größe) und `o` (Überlappungsgröße), werden Chunks über einen Schiebemechanismus generiert: Chunk `i` erstreckt sich von Token `i*(c - o)` bis Token `i*(c - o) + c`. Dies stellt sicher, dass semantisch verbundener Inhalt (z. B. Sätze, die Grenzen überschreiten) in mindestens einem Chunk kontinuierlich bleibt, wodurch der kontextuelle Zusammenhang für die Retrieval-Operationen erhalten bleibt. Kompromisse umfassen erhöhten Speicherbedarf aufgrund der redundanten Darstellung von Tokens (durch `o` Tokens pro benachbarten Paar), höhere Rechenkosten für die Erstellung von Embeddings und das potenzielle Retrieval von überlappendem Inhalt. Typische Überlappungen sind ein kleiner Bruchteil der Chunk-Größe; größere Überlappungen führen zu Redundanz ohne zusätzliche Informationen.

#### 5. Late Chunking

Beim späten Chunking wird der gesamte Dokument als eine einzelne Sequenz durch ein Modell mit langer Kontextlänge eingebettet, wodurch tokenbasierte Embeddings generiert werden, bevor Chunking-Operationen angewendet werden. Dies unterscheidet sich vom frühen Chunking (wo Dokumente vor der Einbettung aufgeteilt werden), da während der Einbettung vollständige kontextuelle Beziehungen beibehalten werden. Die Eingaben bestehen aus Roh-Text-Tokens, und die Ausgaben sind Chunk-Embeddings, die durch Gruppieren der Token-Embeddings in Fenster (z. B. festgelegte Größe oder gleitende Fenster) gefolgt von Mittelwert-Pooling abgeleitet werden. Der Algorithmus nutzt Modelle mit langer Kontextlänge, um den Kontextverlust an Chunk-Grenzen zu vermeiden – kritisch für das Erfassen semantisch abhängiger Elemente wie Pronomen-Referenzen oder Abhängigkeiten über Chunk-Grenzen hinweg. Die Designkompromisse umfassen eine höhere Rechenkosten für die Einbettung des gesamten Dokuments im Vergleich zum frühen Chunking, aber dies führt zu einer besseren Retrievalgenauigkeit für Aufgaben, die Dokumentweite Kohärenz erfordern, wie von Günther et al. (2024) gezeigt. Die Methode ist modellagnostisch und erfordert keine zusätzliche Schulung, wodurch sie mit bestehenden [[embeddings|Embeddings]]-Pipelines kompatibel ist, während sie die Robustheit von [[rag-retrieval|RAG: Retrieval]] verbessert.

#### 6. Parent-Child Retrieval

Parent-Child Retrieval trennt die Retrieval-Einheit (Kind) von der Kontext-Einheit (Elternteil). Kinder (z. B. Sätze oder kurze Absätze) werden in einer Vektordatenbank eingefügt und indiziert, um präzise Retrieval-Ergebnisse zu ermöglichen, während Elternteile (z. B. Dokumentabschnitte oder vollständige Dokumente) den kontextuellen Hintergrund für die Generierung durch das Sprachmodell liefern. Eingaben bestehen aus kind-elternteil-Paaren auf Dokumentebene und einer Abfrage; Ausgaben sind die top-k abgerufenen Kinder mit ihren verknüpften Elternkontexten. Der Algorithmus verwendet eine zweistufige Indizierungsstruktur: Kinder werden in der Vektordatenbank gespeichert und über Ähnlichkeit der Embedding-Vektoren abgerufen, und jedes Kind-Record enthält Metadaten (z. B. Eltern-ID) zur Kontextabfrage. Designentscheidungen umfassen die Granularität der Kinder (z. B. Satzebene vs. Absatzebene) und die Verknüpfungsmethode (z. B. Dokument-ID oder Abschnittsmetadaten). Kompromisse bestehen zwischen erhöhter Indizierungscomplexität (aufgrund der Metadatenverwaltung) und verbesserter Retrieval-Präzision (kleinere Einheiten minimieren Rauschen) sowie ausreichendem Kontext (größere Elternteile vermeiden isolierte Fragmente). Dies löst die inhärente Spannung zwischen feinkörnigem Retrieval und kontextueller Vollständigkeit, wie sie in [[rag-retrieval|Retrieval]]-Systemen von zentraler Bedeutung ist.

#### 7. Chunkgröße und Position im Kontext

Die Chunkgröße beeinflusst direkt die Retrieval-Präzision und die Vollständigkeit des Kontexts: kleinere Chunks erhöhen die Präzision, indem sie atomare Fakten isolieren, bergen aber das Risiko einer unvollständigen Kontextinformation, während größere Chunks die Kohärenz bewahren, allerdings auf Kosten der Überkompression der Embedding-Verteilung und einer verringerten Retrievalgenauigkeit. Die Anzahl der Chunks, die in den Kontextfenster eines Modells (z. B. 8192 Token) passen, ist durch `max_tokens / chunk_size` begrenzt, was die tiefgehende Retrieval-Kontextinformation einschränkt. Entscheidend ist, dass Liu et al. (2023) zeigten, dass Sprachmodelle einen starken Positionsbiased aufweisen, wobei die Leistung deutlich abnimmt, wenn relevante Informationen sich in der Mitte langer Kontexte befinden, im Vergleich zum Anfang oder Ende. Dies erfordert eine Sortierung der abgerufenen Chunks, um hochrelevante Inhalte am Anfang/Ende der Sequenz zu priorisieren und so die „verloren in der Mitte“-Effekte zu verringern. Die Gestaltung entspricht der Wahl von Chunkgrößen, die den Kontextintegrität mit den Kontextfensterbeschränkungen abwägen, während die Chunksequenzstruktur dem Modellverhalten entsprechen soll – typischerweise durch Reranking, um Schlüsselchunks früh zu positionieren. Dieser Kompromiss optimiert die Prompteffizienz und die Ausgabegüte in [[rag-retrieval|retrieval]]-verstärkten Systemen.

#### Ursprung und Varianten

Die Aufteilung in festen Größen mit Überlappung ist die lange bestehende Standardmethode in Retrieval-Pipelines. Die Proposition-level-Indexierung (Chen et al., 2023) hat die Retrieval-Einheit auf einzelne Fakten herabgesetzt und übertraf die Passage-level-Indexierung. Late Chunking (Günther et al. 2024) verarbeitet ganze Dokumente als Eingabe, indem sie zuerst mit langen Kontextmodellen eingebettet werden und anschließend, nach dem Einbetten und vor dem Mittelwert-Pooling, aufgeteilt werden. Dies bewahrt die im konventionellen Aufteilen verlorenen kontextuellen Beziehungen und erzeugt Embeddings, bei denen jedes Chunk vollständige kontextuelle Informationen erfasst. Varianten umfassen struktur-basiertes Chunking (z. B. rechtliche Verträge werden anhand von Klauseln oder Artikeln aufgeteilt), das die inhärente Dokumentstruktur nutzt, um Chunks zu bilden, die mit semantischen Einheiten übereinstimmen. Proposition-Indexierung verbessert die Retrieval-Präzision, multipliziert jedoch die Anzahl der Einheiten, während Late Chunking die im Chunk-Embedding erfassten Kontexte verbessert, allerdings mit dem Nachteil, ganze Dokumente mit einem langen Kontextmodell zu kodieren. Struktur-basiertes Chunking bewahrt die Dokumentsemantik, erfordert jedoch format-spezifische Parser und beschränkt damit die Allgemeingültigkeit. Diese Ansätze optimieren den [[embeddings|Einbettungs]]-Prozess für die Retrieval-Effizienz und -Genauigkeit.

### Wann einsetzen

- Wenn hohe Präzision bei der Retrieval entscheidend ist: Feingranulares Chunking (z. B. auf Ebene der Propositionen) übertrifft deutlich das Passage-basierte Indexieren bei Retrieval-Aufgaben, wie Chen et al. (2023) in [[rag-retrieval|retrieval]] gezeigt haben.
- Wenn dichter Vektor-basierte Retrieval verwendet wird: Kürzere Textsegmente minimieren die semantische Überkompression in Embeddings und verbessern die Retrieval-Effectivität gemäß Günther et al. (2024).
- Wenn viele Chunks in einen langen Prompt gesetzt werden: Modelle nutzen Informationen am Anfang oder Ende eines langen Kontexts am besten, daher sollten Größe und Reihenfolge der Chunks die am relevantesten Chunks dort platzieren (Liu et al., 2023).

### Stärken und Grenzen

**Stärken**
- Feinkörniges Chunking (z. B. Propositionen) verbessert die Retrieval-Präzision und die Leistung bei nachfolgenden QA-Aufgaben erheblich im Vergleich zu passagebasierten Einheiten (Chen et al. (2023)).
- Late Chunking bewahrt die vollständige kontextuelle Information durch das Einbetten des gesamten Dokuments vor dem Chunking und erzielt dadurch überlegene Retrieval-Ergebnisse ohne zusätzliche Schulung (Günther et al. (2024)).

**Einschränkungen**
- Traditionelles, festgrößiges Chunking zerlegt semantische Einheiten und führt zu Kontextverlust und suboptimalen Embeddings (Günther et al. (2024)).
- Modelle nutzen Informationen in der Mitte eines langen Kontexts deutlich schlechter als am Anfang oder Ende (Liu et al., 2023); viele oder lange Chunks müssen daher sorgfältig geordnet werden, siehe [[rag-failure-modes|Fehlermodi]].
- Die beste Strategie hängt von der Dokumentstruktur und dem Embedding-Modell ab und muss pro Korpus abgestimmt werden.

### Vergleich

| Ansatz             | Unterschiede                                      | Geeignet für |
|----------------------|-----------------------------------------------------|------------|
| Fixgröße           | Teilt Text nach fester Tokenanzahl (z. B. 500 Tokens), kann semantische Einheiten zerstören und den Kontextverlust erhöhen. | Allgemeine Anwendungsfälle in [[rag-retrieval|retrieval]]-Systemen, bei denen Einfachheit und Geschwindigkeit gegenüber der Kontexterhaltung priorisiert werden. |
| Semantikbasiert      | Teilt an semantischen Grenzen (z. B. Propositionen), erfasst atomare Fakten und verbessert die Retrieval-Präzision gegenüber der Passagebasierten Indexierung (Chen et al., 2023). | Dokumente, die eine hohe Kontextkohärenz erfordern; kritisch für faktenbasierte QA-Aufgaben, bei denen feingranulare Retrieval-Methoden die Leistung im Nachbearbeitungsschritt verbessern. |
| Late Chunking      | Embeds das gesamte Dokument zunächst mithilfe von Modellen mit langer Kontextlänge, wendet dann Chunking an, wodurch der vollständige Kontext in den Embeddings erhalten bleibt (Günther et al., 2024). | Systeme, die Modelle mit langer Kontextlänge für Embeddings verwenden (z. B. [[embeddings|embeddings]]-Pipelines), bei denen der Kontextverlust während der Embedding-Phase die Retrieval-Qualität beeinträchtigt. |

Semantikbasiertes Chunking minimiert den Kontextverlust bei der Retrieval-Operation im Vergleich zu Methoden mit fester Größe, während Late Chunking die Kompressionseffekte der Embedding-Operation eliminiert, ohne zusätzliche Trainingsmaßnahmen.

### In der Praxis

Die Bewertung erfordert die Messung von Retrieval-Metriken (z. B. recall@k) und der Genauigkeit für downstream-Aufgaben (z. B. QA F1), wie Chen et al. (2023) feststellten, dass das Indizieren mit feingranularen Einheiten (Propositionen) deutlich besser abschneidet als das Indizieren auf Passage-Ebene. Typische Fehlermodi umfassen den Verlust von Kontext an Chunk-Grenzen (Günther et al. (2024)) und eine Leistungsschwächung, wenn relevante Informationen sich in der Mitte langer Kontexte befinden (Liu et al. (2023)). Die Parameterwahl beinhaltet die Auswahl der Chunk-Granularität (feingranulare Einheiten werden für Präzision bevorzugt) und der Überlappungsgröße (um den Verlust von Grenzkontext zu reduzieren), wobei die optimalen Einstellungen durch [[rag-retrieval-evaluation|Retrieval-Bewertung]] bestimmt und in [[rag-failure-modes|Fehlermodi]] dokumentiert werden.

### Merksatz

Chunking erfordert ein Gleichgewicht zwischen Retrieval-Präzision und kontextueller Kohärenz, da feiner granulierte Einheiten die Präzision verbessern, aber das Risiko von Kontextverlust erhöhen.

### Quellen

- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Chen, T. et al. (2023). *Dense X Retrieval: What Retrieval Granularity Should We Use?* [arXiv:2312.06648](https://arxiv.org/abs/2312.06648)
- Günther, M. et al. (2024). *Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models.* [arXiv:2409.04701](https://arxiv.org/abs/2409.04701)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
