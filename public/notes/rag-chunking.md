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

The chunking process applies fixed-size or semantic segmentation to divide documents, then enriches context, adds overlap, and may employ late chunking or parent-child retrieval techniques, with chunk size and position being critical factors for retrieval effectiveness as analyzed in [[rag-retrieval|retrieval]] and [[rag-evaluation|evaluation]].

```text
Fixed-Size Chunking ─▶ Semantic Chunking ─▶ Context Enrichment
Overlap ─▶ Late Chunking
Parent-Child Retrieval ─▶ Chunk Size and Position
```

#### 1. Fixed-Size Chunking

Fixed-size chunking splits input text into uniform-length segments, typically defined by a fixed token count (e.g., 500 tokens) or character count. The algorithm processes text sequentially, dividing it into contiguous chunks of the target length without semantic analysis. This approach is computationally efficient, structure-agnostic, and requires minimal preprocessing. However, it risks fragmenting semantic units (e.g., splitting a sentence or concept across chunks), which can degrade embedding quality and retrieval precision. Chen et al. (2023) demonstrated that finer-grained units significantly outperform coarser passage-level units in retrieval tasks, implying that fixed-size chunks at larger granularities may reduce effectiveness. The optimal chunk size balances precision (smaller chunks) against context preservation (larger chunks), and is empirically tuned based on the embedding model [[embeddings|Embeddings]] and retrieval task constraints. Common sizes range from 250–1000 tokens, though no universal optimum exists.

#### 2. Semantic Chunking

Semantic chunking segments text into propositions—concise, self-contained natural language units each expressing a distinct atomic fact—by identifying semantic boundaries such as topic shifts or discrete fact expressions. Inputs are source documents; outputs are sequences of propositions, typically generated via natural language processing to detect these boundaries. This method, proposed by Chen et al. (2023), replaces fixed-size or passage-level chunking with fine-grained units. Design choices prioritize precision: propositions minimize context loss during retrieval by isolating single facts, improving downstream QA performance. However, this increases the number of chunks, raising storage and computational costs compared to coarser units. The trade-off is justified for knowledge-intensive tasks where precise fact retrieval outweighs efficiency concerns. The approach aligns with [[rag-retrieval|retrieval]] by enabling more targeted candidate passage selection while maintaining semantic coherence.

#### 3. Context Enrichment

Context Enrichment appends domain-specific metadata (e.g., document title, section, article number) to each chunk to resolve semantic ambiguities when retrieved independently. Inputs are the chunk text and pre-extracted structural metadata (e.g., from document headers or sections). The output is a structured object containing the text and metadata fields (e.g., `{"text": "...", "metadata": {"title": "DSGVO", "article": "5", "section": "2"}}`). The algorithm stores metadata as key-value pairs without modifying the text, avoiding embedding overhead. Design choices prioritize minimal, high-value metadata (e.g., document identifier and section) to balance interpretability gains against token cost. Trade-offs include a small storage increase versus the critical prevention of retrieval ambiguity (e.g., resolving "Absatz 2" to "DSGVO Art. 5 para. 2"). This step is essential for structured documents (e.g., legal, technical) where isolated chunks lack referential context, as seen in domains requiring precise semantic grounding during [[rag-retrieval|retrieval]].

#### 4. Overlap

Overlap between adjacent chunks shares a fixed number of tokens (e.g., `o` tokens) between consecutive chunks to mitigate context loss at boundaries. Given a tokenized document and parameters `c` (chunk size) and `o` (overlap size), chunks are generated via a sliding window: chunk `i` spans tokens from `i*(c - o)` to `i*(c - o) + c`. This ensures semantically connected content (e.g., sentences spanning boundaries) remains contiguous within at least one chunk, preserving contextual coherence for retrieval. Trade-offs include increased storage due to redundant token representation (by `o` tokens per adjacent pair), higher computational cost for embedding generation, and potential retrieval of overlapping content. Chen et al. (2023) demonstrated that retrieval unit granularity significantly impacts performance, and overlap is a technique to enhance unit coherence within fixed-size approaches. This aligns with [[rag-retrieval|retrieval]] strategies emphasizing contextual integrity while balancing precision and resource efficiency.

#### 5. Late Chunking

Late chunking embeds the entire document as a single sequence through a long-context embedding model, generating token-level embeddings before applying chunking operations. This differs from early chunking (where documents are split before embedding) by preserving full contextual relationships during embedding. Inputs consist of raw text tokens, and outputs are chunk embeddings derived by grouping token embeddings into windows (e.g., fixed-size or sliding windows) followed by mean pooling. The algorithm leverages long-context models to avoid context loss at chunk boundaries—critical for capturing semantically interdependent elements like pronoun references or cross-chunk dependencies. Design trade-offs include higher computational cost for full-document embedding compared to early chunking, but this yields superior retrieval accuracy for tasks requiring document-wide coherence, as demonstrated by Günther et al. (2024). The method is model-agnostic and requires no additional training, making it compatible with existing [[embeddings|Embeddings]] pipelines while enhancing [[rag-retrieval|RAG: Retrieval]] robustness. It particularly benefits from long-context models that retain middle-context information, mitigating the "lost-in-the-middle" effect observed in standard LLMs.

#### 6. Parent-Child Retrieval

Parent-Child Retrieval decouples the retrieval unit (child) from the context unit (parent). Children (e.g., sentences or short paragraphs) are embedded and indexed in a vector database for precise retrieval, while parents (e.g., document sections or full documents) provide contextual support for LLM generation. Inputs consist of document-level child-parent pairs and a query; outputs are top-k retrieved children with their linked parent contexts. The algorithm employs a two-level indexing structure: children are stored in the vector database for similarity search using `score = 1 / (k + rank)`, and each child record includes metadata (e.g., parent ID) for context retrieval. Design choices include child granularity (e.g., sentence vs. paragraph level) and linking method (e.g., document ID or section metadata). Trade-offs involve increased indexing complexity (due to metadata management) versus improved retrieval precision (smaller units minimize noise) and sufficient context (larger parents avoid isolated fragments). This resolves the inherent tension between fine-grained retrieval and contextual completeness, as critical in [[rag-retrieval|retrieval]] systems.

#### 7. Chunk Size and Position in the Context

Chunk size directly influences retrieval precision and context completeness: smaller chunks enhance precision by isolating atomic facts but risk incomplete context, while larger chunks preserve coherence at the cost of embedding over-compression and reduced retrieval accuracy. The number of chunks fitting within a model's context window (e.g., 8192 tokens) is constrained by `max_tokens / chunk_size`, limiting the retrievable context depth. Crucially, Liu et al. (2023) demonstrated that language models exhibit strong positional bias, with performance degrading significantly when relevant information resides in the middle of long contexts compared to the beginning or end. This necessitates ordering retrieved chunks to prioritize high-relevance content at sequence start/end, mitigating "lost-in-the-middle" effects. Design choices involve selecting chunk sizes that balance contextual integrity against context window limits, while structuring the chunk sequence to align with model behavior—typically via reranking to position key chunks early. This trade-off optimizes prompt efficiency and output quality in [[rag-retrieval|retrieval]]-augmented systems.

#### Origin and variants

Semantic chunking, introduced by Chen et al. (2023), defines fine-grained "propositions" as atomic factoids within text—each representing a distinct, self-contained unit of information. This method splits documents at natural semantic boundaries (e.g., topic shifts or discrete facts), producing contextually coherent chunks that outperform passage-level indexing in retrieval. Late chunking (Günther et al. 2024) processes entire documents as input, embedding them first using long-context models before applying chunking after embedding and before mean pooling. This preserves contextual relationships lost in conventional splitting, yielding embeddings where each chunk captures full contextual information. Variants include structure-based chunking (e.g., legal contracts split by clauses or articles), which leverages inherent document structures to form chunks aligned with semantic units. Inputs for semantic chunking are unstructured text; outputs are proposition-aligned chunks. Late chunking inputs are full documents; outputs are context-enriched chunk embeddings. Design choices involve trade-offs: semantic chunking improves retrieval precision but risks over-segmentation, while late chunking enhances context capture at higher computational cost. Structure-based chunking maintains document semantics but requires format-specific parsers, limiting generality. These approaches optimize the [[embeddings|embedding]] process for retrieval efficiency and accuracy.

### When to use it

- When high precision in retrieval is critical: Fine-grained chunking (e.g., proposition-level) significantly outperforms passage-level indexing in retrieval tasks, as demonstrated by Chen et al. (2023) in [[rag-retrieval|retrieval]].
- When using dense vector-based retrieval: Shorter text segments minimize semantic over-compression in embeddings, improving retrieval effectiveness per Günther et al. (2024).
- When mitigating "lost-in-the-middle" effects: Smaller chunks position relevant information at context boundaries, avoiding performance degradation in long-context tasks as observed by Liu et al. (2023).

### Strengths and limitations

**Strengths**
- Fine-grained chunking (e.g., propositions) significantly improves retrieval precision and downstream QA performance compared to passage-level units (Chen et al. (2023)).
- Late chunking preserves full contextual information by embedding the entire document before chunking, yielding superior retrieval results without additional training (Günther et al. (2024)).
- Using fine-grained units within a fixed computation budget enhances QA performance (Chen et al. (2023)).

**Limitations**
- Traditional fixed-size chunking fragments semantic units, causing context loss and sub-optimal embeddings (Günther et al. (2024)).
- The "lost-in-the-middle" effect (Liu et al. (2023)) degrades performance when relevant information falls within the middle of a chunk, a known failure mode in [[rag-failure-modes|failure modes]].
- Optimal chunking strategy varies significantly across document structures and embedding models, requiring task-specific tuning (Chen et al. (2023)).

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

Chunking zerlegt Dokumente in kleinere, kontextuell zusammenhängende Einheiten, um präzise Retrieval zu ermöglichen und den inhärenten Kontextverlust bei der Indexierung ganzer Dokumente zu vermeiden. Chen et al. (2023) zeigten, dass feinkörnige Einheiten bei Retrieval-Aufgaben deutlich besser abschneiden als Einheiten auf Passage-Ebene, was die Leistung bei nachfolgenden QA-Aufgaben verbessert. Dieser Ansatz behebt die Herausforderungen bei Präzision und Kontexterhaltung im [[rag-retrieval|Retrieval]].

### Funktionsweise

Der Chunking-Prozess wendet festgelegte Größen oder semantische Segmentierung an, um Dokumente zu teilen, und bereichert anschließend den Kontext, fügt Überlappungen hinzu und kann Techniken wie Late Chunking oder Parent-Child Retrieval anwenden. Die Größe und Position der Chunks sind entscheidende Faktoren für die Effektivität der Retrieval-Operationen, wie in [[rag-retrieval|retrieval]] und [[rag-evaluation|evaluation]] analysiert.

```text
Fixed-Size Chunking ─▶ Semantic Chunking ─▶ Context Enrichment
Overlap ─▶ Late Chunking
Parent-Child Retrieval ─▶ Chunk Size and Position
```

#### 1. Fixed-Size Chunking

Fixed-Size Chunking teilt den Eingabetext in gleichlange Segmente auf, typischerweise definiert durch eine feste Tokenanzahl (z. B. 500 Tokens) oder Zeichenanzahl. Der Algorithmus verarbeitet den Text sequenziell und teilt ihn in kontinuierliche Segmente der Zielgröße ohne semantische Analyse. Dieser Ansatz ist rechenleistungseffizient, strukturunabhängig und benötigt minimale Vorverarbeitung. Allerdings besteht das Risiko, semantische Einheiten (z. B. Satz oder Konzept über mehrere Chunks verteilt) zu zerstören, was die Qualität der Embeddings und die Retrievalgenauigkeit beeinträchtigen kann. Chen et al. (2023) zeigten, dass feiner granulierte Einheiten in Retrieval-Aufgaben deutlich besser abschneiden als gröbere Passage-Einheiten, was darauf hindeutet, dass feste Größen bei größeren Granularitäten die Effektivität reduzieren können. Die optimale Chunkgröße muss Präzision (kleine Chunks) mit Kontexterhaltung (große Chunks) abwägen und wird empirisch anhand des Embedding-Modells [[embeddings|Embeddings]] und der Retrieval-Aufgabenanforderungen abgestimmt. Typische Größen liegen zwischen 250–1000 Tokens, obwohl kein universeller Optimum existiert.

#### 2. Semantic Chunking

Semantic Chunking segmentiert den Text in Propositionen – prägnante, selbstständige natürliche Spracheneinheiten, die jeweils einen eindeutigen atomaren Fakt ausdrücken –, indem semantische Grenzen wie Themenwechsel oder diskrete Faktenausdrücke identifiziert werden. Die Eingaben sind Quelldokumente; die Ausgaben sind Sequenzen von Propositionen, typischerweise generiert durch natürliche Sprachverarbeitung, um diese Grenzen zu erkennen. Dieser Ansatz, vorgeschlagen von Chen et al. (2023), ersetzt feste Größen oder Passage-Einheiten durch feiner granulierte Einheiten. Die Gestaltungswahl priorisiert Präzision: Propositionen minimieren den Kontextverlust während der Retrieval-Operationen, indem sie einzelne Fakten isolieren und die Leistung der nachfolgenden QA-Aufgaben verbessern. Allerdings erhöht dies die Anzahl der Chunks und führt zu höheren Speicher- und Rechenkosten im Vergleich zu gröberen Einheiten. Der Kompromiss ist für kunststoffintensive Aufgaben gerechtfertigt, bei denen präzise Faktenerfassung die Effizienzprobleme überwiegt. Der Ansatz passt sich [[rag-retrieval|retrieval]] an, indem er die Auswahl von Kandidatenpassagen gezielter ermöglicht, während semantische Kohärenz gewahrt bleibt.

#### 3. Context Enrichment

Context Enrichment fügt domänenspezifische Metadaten (z. B. Dokumenttitel, Abschnitt, Artikelnummer) jedem Chunk hinzu, um semantische Ambiguitäten zu lösen, wenn dieser unabhängig abgerufen wird. Die Eingaben bestehen aus dem Chunk-Text und präextrahierten strukturellen Metadaten (z. B. aus Dokumentüberschriften oder Abschnitten). Das Ergebnis ist ein strukturierter Objekt, der den Text und Metadatenfelder enthält (z. B. `{"text": "...", "metadata": {"title": "DSGVO", "article": "5", "section": "2"}}`). Der Algorithmus speichert Metadaten als Schlüssel-Wert-Paare, ohne den Text zu verändern, um den Overhead der Embedding-Operationen zu vermeiden. Gestaltungswahl priorisiert minimale, hochwertige Metadaten (z. B. Dokumentidentifikator und Abschnitt), um den Gewinn an Interpretierbarkeit gegen Tokenkosten auszugleichen. Kompromisse umfassen einen geringen Speicherbedarf im Vergleich zur kritischen Vermeidung von Retrieval-Ambiguitäten (z. B. das Auflösen von "Absatz 2" zu "DSGVO Art. 5 Abs. 2"). Dieser Schritt ist für strukturierte Dokumente (z. B. rechtliche, technische) entscheidend, bei denen isolierte Chunks referenziellen Kontext fehlen, wie in Bereichen, die präzise semantische Grundierung während [[rag-retrieval|retrieval]] benötigen.

#### 4. Overlap

Overlap zwischen benachbarten Chunks teilt eine feste Anzahl von Tokens (z. B. `o` Tokens) zwischen aufeinanderfolgenden Chunks auf, um den Kontextverlust an Grenzen zu verringern. Gegeben ein tokenisiertes Dokument und Parameter `c` (Chunkgröße) und `o` (Überlappungsgröße), werden Chunks über einen Schiebebereich generiert: Chunk `i` erstreckt sich von `i*(c - o)` bis `i*(c - o) + c`. Dies stellt sicher, dass semantisch verbundene Inhalte (z. B. Sätze, die Grenzen überschreiten) in mindestens einem Chunk kontinuierlich bleiben und die kontextuelle Kohärenz für Retrieval erhalten bleibt. Kompromisse umfassen erhöhten Speicherbedarf aufgrund von redundanten Tokenrepräsentationen (um `o` Tokens pro benachbarten Paar), höheren Rechenkosten für Embedding-Generierung und potenzielle Retrieval von überlappendem Inhalt. Chen et al. (2023) zeigten, dass die Granularität der Retrieval-Einheit stark die Leistung beeinflusst, und Overlap ist eine Technik, um die Einheitengrenzen innerhalb von festgelegten Ansätzen zu erhöhen. Dies passt sich [[rag-retrieval|retrieval]]-Strategien an, die kontextuelle Integrität betonen, während Präzision und Ressourceneffizienz ausgewogen werden.

#### 5. Late Chunking

Late Chunking embeddet das gesamte Dokument als eine einzige Sequenz über ein langen-Kontext-Embedding-Modell, generiert Token-Level-Embeddings und wendet anschließend Chunking-Operationen an. Dies unterscheidet sich von Early Chunking (wo Dokumente vor dem Embedding geteilt werden), indem vollständige kontextuelle Beziehungen während des Embedding-Verfahrens erhalten bleiben. Eingaben bestehen aus Roh-Text-Token, und Ausgaben sind Chunk-Embeddings, die durch Gruppieren von Token-Embeddings in Fenster (z. B. feste Größe oder Schiebe-Fenster) gefolgt von Mittelwert-Pooling abgeleitet werden. Der Algorithmus nutzt langen-Kontext-Modelle, um den Kontextverlust an Chunk-Grenzen zu vermeiden – kritisch für das Erfassen semantisch abhängiger Elemente wie Pronomen-Referenzen oder über-Chunk-Abhängigkeiten. Gestaltungskompromisse umfassen höhere Rechenkosten für das vollständige Dokument-Embedding im Vergleich zu Early Chunking, was jedoch eine bessere Retrievalgenauigkeit für Aufgaben erzielt, die Dokumentweite Kohärenz benötigen, wie von Günther et al. (2024) gezeigt. Die Methode ist Modell-agnostisch und benötigt keine zusätzliche Schulung, was sie mit bestehenden [[embeddings|Embeddings]]-Pipelines kompatibel macht, während [[rag-retrieval|RAG: Retrieval]]-Robustheit erhöht wird. Sie profitiert besonders von langen-Kontext-Modellen, die mittleren Kontextinformationen beibehalten, und mildert den "lost-in-the-middle"-Effekt, der bei Standard-LLMs beobachtet wird.

#### 6. Parent-Child Retrieval

Parent-Child Retrieval trennt die Retrieval-Einheit (Kind) von der Kontext-Einheit (Elter). Kinder (z. B. Sätze oder kurze Absätze) werden in einer Vektordatenbank eingefügt und indiziert, um präzise Retrieval zu ermöglichen, während Eltern (z. B. Dokumentabschnitte oder vollständige Dokumente) den Kontext für LLM-Generierung bereitstellen. Eingaben bestehen aus Dokumentebenen-Kinder-Elter-Paaren und einer Abfrage; Ausgaben sind die top-k abgerufenen Kinder mit ihren verknüpften Elter-Kontexten. Der Algorithmus verwendet eine zweistufige Indizierungsstruktur: Kinder werden in der Vektordatenbank gespeichert, um mit `score = 1 / (k + rank)` Ähnlichkeitssuche durchzuführen, und jedes Kind-Record enthält Metadaten (z. B. Eltern-ID) für Kontext-Retrieval. Gestaltungswahl umfasst Kindergranularität (z. B. Satz vs. Absatz Ebene) und Verknüpfungsmethode (z. B. Dokument-ID oder Abschnittsmetadaten). Kompromisse umfassen erhöhte Indizierungs-Komplexität (aufgrund von Metadaten-Verwaltung) im Vergleich zu verbesserten Retrieval-Präzision (kleinere Einheiten minimieren Rauschen) und ausreichendem Kontext (größere Eltern vermeiden isolierte Fragmente). Dies löst die inhärente Spannung zwischen feiner granulierter Retrieval und kontextueller Vollständigkeit, wie in [[rag-retrieval|retrieval]]-Systemen kritisch.

#### 7. Chunk Größe und Position im Kontext

Die Chunkgröße beeinflusst direkt die Retrieval-Präzision und die Kontextvollständigkeit: kleinere Chunks erhöhen die Präzision, indem sie atomare Fakten isolieren, riskieren aber unvollständigen Kontext, während größere Chunks die Kohärenz bewahren, auf Kosten der Embedding-Überkompression und reduzierter Retrievalgenauigkeit. Die Anzahl der Chunks, die in den Kontextfenster eines Modells (z. B. 8192 Tokens) passen, ist durch `max_tokens / chunk_size` begrenzt, was die tiefgehende Retrieval-Kontextgrenze einschränkt. Entscheidend ist, dass Liu et al. (2023) zeigten, dass Sprachmodelle starke Positionsverzerrung aufweisen, wobei die Leistung deutlich abnimmt, wenn relevante Informationen in der Mitte von langen Kontexten liegen, im Vergleich zum Anfang oder Ende. Dies erfordert die Sortierung der abgerufenen Chunks, um hochrelevante Inhalte am Anfang/Ende der Sequenz zu priorisieren und den "lost-in-the-middle"-Effekt zu mildern. Gestaltungswahl umfasst die Auswahl von Chunkgrößen, die den Kontextintegrität gegen Kontextfenstergrenzen ausgewogen, während die Chunksequenzstruktur mit dem Modellverhalten übereinstimmt – typischerweise durch Reranking, um Schlüsselchunks früh zu positionieren. Dieser Kompromiss optimiert Prompteffizienz und Ausgabegüte in [[rag-retrieval|retrieval]]-ergänzten Systemen.

#### Ursprung und Varianten

Semantic Chunking, eingeführt von Chen et al. (2023), definiert feiner granulierte "Propositionen" als atomare Fakten innerhalb des Textes – jeweils eine selbstständige Informations-Einheit. Dieser Ansatz teilt Dokumente an natürlichen semantischen Grenzen (z. B. Themenwechsel oder diskrete Fakten) auf, wodurch kontextuell kohärente Chunks entstehen, die in der Retrieval-Operationen Passage-Level-Indizierung übertrifft. Late Chunking (Günther et al. 2024) verarbeitet ganze Dokumente als Eingabe, embeddet sie zuerst mit langen-Kontext-Modellen und wendet Chunking erst nach dem Embedding und vor dem Mittelwert-Pooling an. Dies bewahrt kontextuelle Beziehungen, die bei konventioneller Aufteilung verloren gehen, und erzeugt Embeddings, bei denen jeder Chunk vollständige kontextuelle Informationen erfasst. Varianten umfassen struktur-basiertes Chunking (z. B. rechtliche Verträge, die nach Klauseln oder Artikeln geteilt werden), das vorhandene Dokumentstrukturen nutzt, um Chunks mit semantischen Einheiten abzugleichen. Eingaben für Semantic Chunking sind unstrukturierter Text; Ausgaben sind propositionenbasierte Chunks. Eingaben für Late Chunking sind vollständige Dokumente; Ausgaben sind kontextverstärkte Chunk-Embeddings. Gestaltungswahl umfasst Kompromisse: Semantic Chunking verbessert Retrieval-Präzision, birgt aber das Risiko der Übersegmentierung, während Late Chunking die Kontexterfassung auf Kosten höherer Rechenkosten verbessert. Struktur-basiertes Chunking bewahrt Dokumentsemantik, erfordert aber format-spezifische Parser, was die Allgemeingültigkeit einschränkt. Diese Ansätze optimieren den [[embeddings|embedding]]-Prozess für Retrieval-Effizienz und -Genauigkeit.

### Wann einsetzen

- Wenn eine hohe Präzision bei der Retrieval entscheidend ist: Feinkörniges Chunking (z. B. auf Ebene der Proposition) übertrifft deutlich das Passage-basierte Indexieren bei Retrieval-Aufgaben, wie Chen et al. (2023) in [[rag-retrieval|Retrieval]] gezeigt haben.
- Wenn dichter, vektorbasierten Retrieval verwendet wird: Kürzere Textabschnitte minimieren die semantische Überkompression in Embeddings und verbessern die Retrieval-Effectivität gemäß Günther et al. (2024).
- Wenn „lost-in-the-middle“-Effekte gemindert werden sollen: Kleinere Chunk-Größen positionieren relevante Informationen an Kontextgrenzen und vermeiden Leistungsabbau bei langen Kontextaufgaben, wie Liu et al. (2023) beobachtet haben.

### Stärken und Grenzen

**Stärken**
- Feingranulares Chunking (z. B. Propositionen) verbessert die Retrieval-Präzision und die Leistung bei nachfolgenden QA-Aufgaben erheblich im Vergleich zu passagebasierten Einheiten (Chen et al. (2023)).
- Late Chunking bewahrt die vollständige kontextuelle Information, indem das gesamte Dokument vor dem Chunking eingebettet wird, was zu überlegenen Retrieval-Ergebnissen führt, ohne zusätzliche Trainingsdaten (Günther et al. (2024)).
- Das Verwenden feingranularer Einheiten innerhalb eines festen Rechenbudgets verbessert die QA-Leistung (Chen et al. (2023)).

**Einschränkungen**
- Traditionelles Chunking mit fester Größe zerlegt semantische Einheiten, was zu Verlust von Kontext und suboptimalen Embeddings führt (Günther et al. (2024)).
- Der „lost-in-the-middle“-Effekt (Liu et al. (2023)) verschlechtert die Leistung, wenn relevante Informationen in der Mitte eines Chunks liegen, ein bekannter Fehlermodus in [[rag-failure-modes|Fehlermodi]].
- Die optimale Chunking-Strategie variiert erheblich je nach Dokumentstruktur und Embedding-Modell und erfordert eine Aufgaben-spezifische Feinabstimmung (Chen et al. (2023)).

### Vergleich

| Ansatz             | Unterschiede                                       | Geeignet für |
|---------------------|----------------------------------------------------|--------------|
| Fixgröße           | Teilt den Text anhand einer festen Tokenanzahl (z. B. 500 Tokens) auf, was semantische Einheiten zerstören und den Kontextverlust erhöhen kann. | Allgemeine Anwendungsfälle in [[rag-retrieval|retrieval]]-Systemen, bei denen Einfachheit und Geschwindigkeit gegenüber der Kontexterhaltung priorisiert werden. |
| Semantikbasiert    | Teilt an semantischen Grenzen (z. B. Propositionen) auf, erfasst atomare Fakten und verbessert die Retrieval-Präzision gegenüber der Passage-Indexierung (Chen et al., 2023). | Dokumente, bei denen eine hohe Kontextkohärenz erforderlich ist; kritisch für faktenbasierte QA-Aufgaben, bei denen feingranulare Retrieval-Methoden die Leistung im Nachbearbeitungsschritt verbessern. |
| Late Chunking    | Embeds das gesamte Dokument zuerst mithilfe von Modellen mit langer Kontextlänge, wendet anschließend Chunking an und bewahrt so den vollen Kontext in den Embeddings (Günther et al., 2024). | Systeme, die Modelle mit langer Kontextlänge für Embeddings verwenden (z. B. [[embeddings|embeddings]]-Pipelines), bei denen der Kontextverlust während der Embedding-Phase die Retrieval-Qualität beeinträchtigt. |

Semantikbasiertes Chunking minimiert den Kontextverlust im Retrieval im Vergleich zu Methoden mit fester Größe, während Late Chunking die Artefakte der Embedding-Kompression eliminiert, ohne zusätzliche Schulung.

### In der Praxis

Die Bewertung erfordert die Messung von Retrieval-Metriken (z. B. recall@k) und der Genauigkeit bei downstream-Aufgaben (z. B. QA F1), wie Chen et al. (2023) feststellten, dass das Indizieren mit feingranularen Einheiten (Propositionen) deutlich besser abschneidet als das Indizieren auf Passage-Ebene. Typische Fehlermodi umfassen den Verlust von Kontext an Chunk-Grenzen (Günther et al. (2024)) und eine Leistungseinbuße, wenn relevante Informationen sich in der Mitte langer Kontexte befinden (Liu et al. (2023)). Die Parameterwahl beinhaltet die Auswahl der Chunk-Granularität (feingranulare Einheiten werden für Präzision bevorzugt) und der Überlappungsgröße (um den Verlust von Grenzkontext zu reduzieren), wobei die optimalen Einstellungen durch [[rag-retrieval-evaluation|Retrieval-Bewertung]] bestimmt und in [[rag-failure-modes|Fehlermodi]] dokumentiert werden.

### Merksatz

Chunking erfordert ein Gleichgewicht zwischen Retrieval-Präzision und kontextueller Kohärenz, da feiner granulierte Einheiten die Präzision verbessern, aber das Risiko von Kontextverlust erhöhen.

### Quellen

- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Chen, T. et al. (2023). *Dense X Retrieval: What Retrieval Granularity Should We Use?* [arXiv:2312.06648](https://arxiv.org/abs/2312.06648)
- Günther, M. et al. (2024). *Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models.* [arXiv:2409.04701](https://arxiv.org/abs/2409.04701)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
