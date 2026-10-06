---
title_en: 'RAG: Retrieval'
title_de: 'RAG: Retrieval'
entity_type: Method
sources:
- https://arxiv.org/abs/2004.04906
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/2212.10496
- https://arxiv.org/abs/1901.04085
- https://arxiv.org/abs/1603.09320
- https://doi.org/10.1561/1500000019
- https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Retrieval in RAG selects relevant context passages from a knowledge base for a language model. It solves the problem that language models lack access to external information beyond their training data, which is critical for generating accurate responses to queries requiring up-to-date or domain-specific knowledge.

### How it works

RAG retrieval employs a multi-stage process: sparse retrieval using BM25 [[information-retrieval|BM25]] identifies candidate passages via lexical matching, while dense retrieval with bi-encoders generates semantic embeddings. Vector indexing via HNSW [[vector-databases|HNSW]] enables efficient similarity search, and hybrid fusion combines sparse and dense results using Reciprocal Rank Fusion (RRF). Subsequent reranking with cross-encoders refines top candidates, and advanced variants include late interaction (ColBERT) and zero-shot retrieval (HyDE).

```text
Sparse Retrieval (BM25) ─▶ Dense Retrieval (Bi-Encoders)
Vector Indexing (HNSW) ─▶ Hybrid Fusion (RRF)
Reranking (Cross-Encoders) ─▶ Late Interaction (ColBERT)
Zero-Shot (HyDE)
```

#### 1. Sparse Retrieval (BM25)

BM25 is a probabilistic relevance framework for information retrieval, introduced by Robertson & Zaragoza (2009). It computes document relevance scores using term-frequency saturation (`tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avg_dl))`), inverse document frequency (IDF, typically `log((N - n + 0.5) / (n + 0.5))`), and document-length normalization (`(1 - b + b * |d| / avg_dl)` with `b` ≈ 0.75). The inverted index data structure maps each term to a list of document identifiers and term frequencies, enabling efficient term-based lookup. Inputs are a query and a document collection; outputs are a ranked list of documents. Design choices include TF saturation to avoid over-weighting highly frequent terms, IDF to emphasize discriminative terms, and length normalization to reduce bias toward longer documents. The inverted index provides fast query processing at the cost of significant storage overhead. This approach excels with precise terminology but lacks semantic understanding, making it suitable for queries requiring exact keyword matching. [[information-retrieval|Information Retrieval]] establishes the foundational principles for this method.

#### 2. Dense Retrieval with Bi-Encoders

Dense retrieval with bi-encoders employs a dual-encoder framework where queries and passages are independently encoded into embeddings using a shared siamese network structure, eliminating the need for pairwise BERT inference. Passage embeddings are precomputed offline and stored in a vector index (e.g., [[vector-databases|Vector Databases]]), enabling efficient similarity search at query time. Inputs are a query string and a knowledge base of passages; outputs are top-k passages ranked by similarity. The algorithm computes cosine similarity or inner product between the query embedding and all precomputed passage embeddings. This design choice prioritizes scalability: precomputation reduces query-time complexity to O(1) after indexing (vs. O(N) for pairwise inference), but increases storage requirements and initial computation. Reimers & Gurevych (2019) demonstrated that siamese networks enable efficient semantic similarity search (reducing 10,000-pair computation from ~65 hours to ~5 seconds), while Karpukhin et al. (2020) showed this approach outperforms BM25 by 9%-19% absolute in top-20 passage retrieval accuracy on open-domain QA benchmarks.

#### 3. Vector Indexing (HNSW)

Vector indexing for approximate nearest neighbor (ANN) search replaces exhaustive comparison of query embeddings against all database vectors with a hierarchical graph structure. The HNSW (Hierarchical NSW) algorithm, introduced by Malkov & Yashunin (2016), constructs a multi-layer graph where each layer represents a nested subset of the data. Elements are assigned to layers with exponentially decaying probability, enabling scale separation between layers. Search begins at the top layer and uses greedy traversal to the nearest neighbor until reaching the base layer, achieving logarithmic complexity. This eliminates the need for auxiliary search structures required by other proximity graph methods. The input consists of high-dimensional embedding vectors (from [[embeddings|Embeddings]]), and the output is a ranked list of top-k nearest neighbors. The recall-speed trade-off is controlled by index parameters: increasing the number of connections per node improves recall at the cost of slower search. HNSW's fully graph-based design enables efficient large-scale vector search, making it suitable for real-time retrieval in systems like [[vector-databases|Vector Databases]].

#### 4. Hybrid Search Fusion (RRF)

Hybrid Search Fusion (RRF) combines parallel sparse (e.g., [[information-retrieval|Information Retrieval]]) and dense retrieval (using [[embeddings|Embeddings]]) results. Inputs are two ranked document lists from each method. Instead of fusing incommensurate scores (e.g., BM25 scores vs. cosine similarities), RRF uses ranks: for a document ranked `r_s` in sparse and `r_d` in dense, the score is `1/(k + r_s) + 1/(k + r_d)` with `k = 60` (Cormack et al., 2009). This avoids score normalization and leverages relative ordering within each method. The output is a single fused list sorted by total score. Design choices prioritize efficiency: ranks require no scale adjustment, and fixed `k=60` balances top-result influence. Trade-offs include losing score magnitude details (only rank order matters) but enabling robust fusion without cross-validation. RRF outperformed Condorcet Fuse and CombMNZ (Cormack et al., 2009) by effectively combining complementary retrieval signals.

#### 5. Reranking with Cross-Encoders

Reranking with cross-encoders refines relevance ordering by jointly processing query-passage pairs. The input concatenates the query and passage with [CLS] and [SEP] tokens (e.g., `[CLS] query [SEP] passage [SEP]`), processed by a BERT-based model. The [CLS] token's output embedding generates a relevance probability via a linear layer, yielding a score for each candidate pair. This step operates on a first-stage candidate list (e.g., BM25 top 1000), reordering candidates by refined relevance. The two-stage design employs a computationally cheap retriever (e.g., BM25) for high recall, producing a large candidate pool, followed by a precision-focused cross-encoder reranker. This trade-off is essential: cross-encoders require per-pair inference (O(N) complexity), making them infeasible for full corpus retrieval but optimal for small candidate sets. The candidate list size `k` directly balances latency and precision—smaller `k` reduces computation but risks discarding relevant passages, while larger `k` increases cost without proportional gains. This architecture leverages the efficiency of sparse retrieval for broad coverage while achieving higher precision through deep contextual modeling.

#### 6. Late Interaction (ColBERT)

ColBERT (Khattab & Zaharia, 2020) implements a late interaction architecture that independently encodes queries and documents into token-level embeddings using BERT, enabling precomputation of document representations for efficient offline storage. At query time, the query is encoded, and a lightweight interaction step computes the fine-grained similarity between query tokens and document tokens via element-wise dot products, aggregated (e.g., summed) to form a relevance score. This positions ColBERT between bi-encoders (which use scalar similarity on whole-document embeddings) and cross-encoders (which process full query-document pairs). The design achieves competitive accuracy with cross-encoders while maintaining efficiency: document embeddings require only one-off computation, and the interaction step avoids per-pair neural processing during retrieval. Consequently, ColBERT executes two orders-of-magnitude faster and requires four orders-of-magnitude fewer FLOPs per query than cross-encoders, making it suitable for large-scale retrieval systems. This approach balances expressiveness (through token-level interaction) with computational feasibility (via precomputed document embeddings).

#### 7. Zero-Shot Dense Retrieval (HyDE)

Zero-Shot Dense Retrieval via Hypothetical Document Embeddings (HyDE) generates a hypothetical document from a query using an instruction-following language model (e.g., InstructGPT), which is then embedded by a contrastive encoder (e.g., Contriever) without relevance labels. The query embedding retrieves the nearest real documents via vector similarity in a precomputed index (e.g., [[vector-databases|Vector Database]]). Inputs are a query and a pre-embedded document corpus; outputs are top-k relevant documents. The contrastive encoder's unsupervised training aligns the embedding space with the corpus, filtering inaccuracies from the generated document while preserving semantic intent. This design eliminates the need for labeled data but relies on the language model's ability to generate semantically relevant text. HyDE significantly outperforms unsupervised dense retrievers like Contriever and achieves performance comparable to fine-tuned retrievers across diverse tasks and languages [[embeddings|Embeddings]] Gao et al. (2022).

#### Origin and variants

Traditional retrieval relied on term-based sparse methods like BM25 [[information-retrieval|Information Retrieval]], which scores documents using term frequency and inverse document frequency. The shift to dense retrieval, demonstrated by Karpukhin et al. (2020), replaced sparse vectors with learned embeddings, enabling semantic matching without exact term overlap. Modern pipelines standardly employ two stages: candidate retrieval and reranking. Candidate retrieval generates an initial pool using fast methods—dense retrieval (e.g., dual-encoder models [[embeddings|Embeddings]]) or sparse methods (BM25)—often combined via fusion techniques like Reciprocal Rank Fusion (RRF), which computes `score = sum(1 / (k + rank))` per document across rankings (k=60, per Cormack et al., 2009). The top-k candidates (e.g., k=100) are then reranked by a cross-encoder (e.g., Nogueira & Cho, 2019), which jointly processes query-document pairs for higher precision but at significant computational cost. This design balances recall (from efficient candidate generation) with precision (via reranking), though reranking increases latency and is restricted to small candidate sets. Trade-offs include dense retrieval's reduced reliance on exact terms versus sparse methods' interpretability, and fusion's recall gains versus added complexity.

### When to use it

- For open-domain question answering requiring semantic understanding of paraphrased queries, dense retrieval using [[embeddings|Embeddings]] achieves 9%-

### Strengths and limitations

**Strengths**
- Dense retrieval with dual-encoders (Karpukhin et al. (2020)) achieves 9%-19% absolute improvement in top-20 passage retrieval accuracy over BM25 on open-domain QA benchmarks.
- Sentence-BERT (Reimers & Gurevych (2019)) reduces semantic similarity search time from ~65 hours (BERT) to ~5 seconds for 10,000 sentences while maintaining BERT-level accuracy.
- ColBERT (Khattab & Zaharia (2020)) matches BERT-based effectiveness with four orders of magnitude fewer FLOPs per query and two orders of magnitude faster execution.

**Limitations**
- BERT-based dense retrieval requires per-query-document pair processing, increasing computational cost by orders of magnitude over sparse methods (Khattab & Zaharia (2020)).
- Fully zero-shot dense retrieval without relevance labels remains challenging (Gao et al. (2022)), necessitating additional techniques like HyDE for embedding grounding.
- Performance sensitivity to embedding model quality and training data (Karpukhin et al. (2020); Nogueira & Cho (2019)) complicates deployment across diverse domains.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Dense Retrieval (dual-encoder) | Achieves 9-19% higher top-20 passage retrieval accuracy than BM25 (Karpukhin et al. (2020)) and reduces semantic search time from hours to seconds (Reimers & Gurevych (2019)) | Natural language queries requiring semantic understanding (e.g., paraphrasing, synonyms) |
| Sparse Retrieval (BM25) | Relies on lexical term matching without embedding computation, as standardized in information retrieval (Robertson & Zaragoza (2009)) | Queries requiring exact term matches (e.g., legal citations, technical specifications) |
Dense retrieval typically relies on precomputed embeddings (see [[embeddings|Embeddings]]), while sparse methods use term-based indexing (see [[information-retrieval|Information Retrieval]]).

### In practice

Evaluation of retrieval effectiveness typically uses top-20 passage retrieval accuracy (Karpukhin et al., 2020) or MRR@10 (Nogueira & Cho, 2019), where dense retrieval systems outperform sparse baselines by 9–19% absolute. Typical failure modes include context pollution (retrieving irrelevant documents) and low recall (missing relevant documents), degrading LLM response quality [[rag-failure-modes|Failure Modes]]. Parameter choices include top-k (typically 3–10), with smaller values reducing token count and LLM cost but risking missing information, while larger values increase recall at the cost of context pollution; embedding models (e.g., SBERT) and vector indexes (e.g., HNSW) are selected for efficiency and accuracy [[vector-databases|Vector Databases]].

### Key takeaway

Retrieval in RAG balances the lexical precision and computational efficiency of sparse [[information-retrieval|Information Retrieval]] methods against the semantic accuracy of dense [[embeddings|Embeddings]] methods, with recent advances reducing the efficiency gap.

### Sources

- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Gao, L. et al. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Retrieval in RAG wählt relevante Kontextpassagen aus einer Wissensbasis für ein Sprachmodell aus. Es löst das Problem, dass Sprachmodelle keinen Zugriff auf externe Informationen haben, die über ihre Trainingsdaten hinausgehen, was für die Generierung präziser Antworten auf Abfragen, die aktuelle oder domain-spezifische Kenntnisse erfordern, entscheidend ist.

### Funktionsweise

RAG-Retrieval verwendet einen mehrstufigen Prozess: Sparse Retrieval mit BM25 [[information-retrieval|BM25]] identifiziert Kandidatenpassagen über lexikalische Übereinstimmung, während Dense Retrieval mit Bi-Encodern semantische Embeddings erzeugt. Vektorindexierung über HNSW [[vector-databases|HNSW]] ermöglicht effiziente Ähnlichkeitssuche, und Hybrid Fusion kombiniert Sparse- und Dense-Ergebnisse mithilfe von Reciprocal Rank Fusion (RRF). Das anschließende Reranking mit Cross-Encodern verfeinert die besten Kandidaten, und fortgeschrittene Varianten umfassen späte Interaktion (ColBERT) und zero-shot Retrieval (HyDE).

```text
Sparse Retrieval (BM25) ─▶ Dense Retrieval (Bi-Encoders)
Vektorindexierung (HNSW) ─▶ Hybrid Fusion (RRF)
Reranking (Cross-Encoders) ─▶ Late Interaction (ColBERT)
Zero-Shot (HyDE)
```

#### 1. Sparse Retrieval (BM25)

BM25 ist ein probabilistisches Relevanzrahmenwerk für die Informationsrückgewinnung, eingeführt von Robertson & Zaragoza (2009). Es berechnet Dokumentrelevanzwerte mithilfe der Term Frequency Saturation (`tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avg_dl))`), der Inverse Document Frequency (IDF, typischerweise `log((N - n + 0.5) / (n + 0.5))`) und der Dokumentlängennormalisierung (`(1 - b + b * |d| / avg_dl)` mit `b` ≈ 0.75). Die Datenstruktur des inversen Indexes ordnet jedem Begriff eine Liste von Dokumentidentifikatoren und Termausprägungen zu, was eine effiziente Begriffsuche ermöglicht. Eingaben sind eine Abfrage und eine Dokumentensammlung; Ausgaben sind eine nach Relevanz sortierte Liste von Dokumenten. Gestaltungswahlmöglichkeiten umfassen die TF-Sättigung, um eine Überbewertung häufig vorkommender Begriffe zu vermeiden, die IDF, um diskriminierende Begriffe zu betonen, und die Längennormalisierung, um den Bias gegenüber längeren Dokumenten zu verringern. Der inverse Index ermöglicht schnelle Abfrageverarbeitung, wobei er erhebliche Speicherüberlastung verursacht. Dieser Ansatz ist bei präziser Terminologie besonders effektiv, verfügt jedoch nicht über semantisches Verständnis und eignet sich daher für Abfragen, die exakte Schlüsselwortübereinstimmung erfordern. [[information-retrieval|Information Retrieval]] legt die grundlegenden Prinzipien für diesen Ansatz fest.

#### 2. Dichter Retrieval mit Bi-Encodern

Dichter Retrieval mit Bi-Encodern verwendet ein Dual-Encoder-Framework, bei dem Abfragen und Passagen unabhängig in Embeddings kodiert werden, wobei ein gemeinsamer Siamese-Netzwerk-Struktur verwendet wird, wodurch das Paarweise-BERT-Verfahren überflüssig wird. Passagen-Embeddings werden offline vorberechnet und in einem Vektorindex (z. B. [[vector-databases|Vektordatenbank]] gespeichert, was eine effiziente Ähnlichkeitsuche zur Abfragezeit ermöglicht. Eingaben sind eine Abfragezeichenfolge und eine Wissensbasis von Passagen; Ausgaben sind die top-k Passagen, die nach Ähnlichkeit rangiert sind. Der Algorithmus berechnet die Kosinusähnlichkeit oder das Skalarprodukt zwischen dem Abfrage-Embedding und allen vorberechneten Passagen-Embeddings. Diese Designentscheidung priorisiert Skalierbarkeit: Vorverarbeitung reduziert die Komplexität zur Abfragezeit auf O(1) nach der Indizierung (gegenüber O(N) bei Paarweise-Verarbeitung), erhöht aber die Speicheranforderungen und die anfängliche Rechenleistung. Reimers & Gurevych (2019) zeigten, dass Siamese-Netzwerke effiziente semantische Ähnlichkeitsuche ermöglichen (die Berechnung von 10.000 Paaren reduziert sich von ~65 Stunden auf ~5 Sekunden), während Karpukhin et al. (2020) zeigten, dass dieser Ansatz bei offenen Domänen QA-Benchmarks die BM25-Genauigkeit um 9%-19% absolut in der top-20-Passagen-Retrieval-Genauigkeit übertrifft.

#### 3. Vektorindexierung (HNSW)

Die Vektorindexierung für Approximate Nearest Neighbor (ANN)-Suche ersetzt die umfassende Vergleichung der Abfragesitzungen mit allen Datenbankvektoren durch eine hierarchische Graphstruktur. Der HNSW-Algorithmus (Hierarchical NSW), eingeführt von Malkov & Yashunin (2016), erstellt einen mehrschichtigen Graphen, wobei jede Schicht eine verschachtelte Teilmenge der Daten darstellt. Elemente werden mit exponentiell abnehmender Wahrscheinlichkeit Schichten zugewiesen, was eine Skalentrennung zwischen Schichten ermöglicht. Die Suche beginnt in der obersten Schicht und nutzt eine gierige Traversierung zum nächsten Nachbarn, bis die Grundschicht erreicht ist, wodurch eine logarithmische Komplexität erreicht wird. Dies beseitigt den Bedarf an Hilfsstruktur für die Suche, die von anderen Proximitätsgraph-Methoden erforderlich ist. Die Eingabe besteht aus hochdimensionalen Embedding-Vektoren (aus [[embeddings|Embeddings]]), und die Ausgabe ist eine rangierte Liste der Top-k nächsten Nachbarn. Der Kompromiss zwischen Erinnerungsfähigkeit und Geschwindigkeit wird durch Indexparameter gesteuert: eine Erhöhung der Anzahl der Verbindungen pro Knoten verbessert die Erinnerungsfähigkeit, allerdings auf Kosten einer langsameren Suche. Der vollständig graphbasierte Entwurf von HNSW ermöglicht effiziente großskalige Vektorsuche, wodurch er für Echtzeit-Retrieval in Systemen wie [[vector-databases|Vektordatenbanken]] geeignet ist.

#### 4. Hybrid Search Fusion (RRF)

Hybrid Search Fusion (RRF) kombiniert parallele sparse (z. B. [[information-retrieval|Information Retrieval]]) und dense Retrieval (mit [[embeddings|Embeddings]]) Ergebnisse. Die Eingaben sind zwei rangierte Dokumentlisten aus jedem Verfahren. Anstatt inkompatible Scores zu kombinieren (z. B. BM25 Scores vs. Kosinusähnlichkeiten) verwendet RRF Ränge: für ein Dokument, das den Rang `r_s` in sparse und `r_d` in dense hat, ist der Score `1/(k + r_s) + 1/(k + r_d)` mit `k = 60` (Cormack et al., 2009). Dies vermeidet die Score-Standardisierung und nutzt die relative Ordnung innerhalb jedes Verfahrens. Das Ergebnis ist eine einzelne kombinierte Liste, die nach Gesamtscore sortiert ist. Die Gestaltungswahl priorisiert Effizienz: Ränge benötigen keine Skalenanpassung, und das feste `k=60` balanciert den Einfluss der Top-Ergebnisse. Kompromisse umfassen das Verlieren von Details der Score-Magnitude (nur die Rangreihenfolge zählt), aber ermöglichen eine robuste Kombination ohne Kreuzvalidierung. RRF übertraf Condorcet Fuse und CombMNZ (Cormack et al., 2009), indem es komplementäre Retrieval-Signale effektiv kombinierte.

#### 5. Reranking mit Cross-Encodern

Das Reranking mit Cross-Encodern verfeinert die Relevanzreihenfolge durch gemeinsame Verarbeitung von Abfrage-Passage-Paaren. Die Eingabe verknüpft die Abfrage und Passage mit [CLS] und [SEP]-Token (z. B. `[CLS] query [SEP] passage [SEP]`), die von einem BERT-basierten Modell verarbeitet werden. Das Ausgabeverbundenebene des [CLS]-Tokens erzeugt eine Relevanzwahrscheinlichkeit über eine lineare Schicht, wodurch ein Score für jedes Kandidatenpaar generiert wird. Dieser Schritt wird auf einer ersten Stufe Kandidatenliste (z. B. BM25 Top 1000) durchgeführt, wobei die Kandidaten nach verfeinerter Relevanz neu geordnet werden. Das zweistufige Design verwendet einen rechenleichten Retriever (z. B. BM25) für eine hohe Recall, der eine große Kandidatenmenge erzeugt, gefolgt von einem präzisionsorientierten Cross-Encoder-Reranker. Dieser Kompromiss ist entscheidend: Cross-Encoder erfordern Inferenz pro Paar (O(N) Komplexität), wodurch sie für die Retrieval eines gesamten Korpus ungeeignet sind, aber optimal für kleine Kandidatenmengen. Die Größe der Kandidatenliste `k` balanciert direkt Latenz und Präzision – ein kleineres `k` reduziert die Rechenleistung, birgt aber das Risiko, relevante Passagen zu verwerfen, während ein größeres `k` die Kosten erhöht, ohne proportionale Vorteile. Diese Architektur nutzt die Effizienz der Sparse Retrieval für eine breite Abdeckung, während sie durch tiefgehende kontextuelle Modellierung eine höhere Präzision erzielt.

#### 6. Späte Wechselwirkung (ColBERT)

ColBERT (Khattab & Zaharia, 2020) implementiert eine Architektur mit später Wechselwirkung, die Abfragen und Dokumente unabhängig in Token-Embeddings kodiert, wobei BERT verwendet wird. Dies ermöglicht die vorab Berechnung von Dokumentrepräsentationen für eine effiziente Offline-Speicherung. Bei der Abfrage wird diese kodiert, und ein leichtgewichtiger Wechselwirkungsschritt berechnet die feingranulare Ähnlichkeit zwischen Abfragetoken und Dokumenttoken über elementweise Skalarprodukte, die aggregiert (z. B. summiert) werden, um einen Relevanzscore zu bilden. Dies positioniert ColBERT zwischen Bi-Encodern (die skalare Ähnlichkeit auf gesamtdokumentbasierten Embeddings verwenden) und Cross-Encodern (die vollständige Abfrage-Dokument-Paare verarbeiten). Das Design erzielt eine wettbewerbsfähige Genauigkeit wie Cross-Encoder, während Effizienz gewahrt bleibt: Dokumenteinbettungen erfordern nur eine einmalige Berechnung, und der Wechselwirkungsschritt vermeidet während der Retrieval-Phase die neuronale Verarbeitung pro Paar. Folglich führt ColBERT zwei Größenordnungen schneller und benötigt vier Größenordnungen weniger FLOPs pro Abfrage als Cross-Encoder, wodurch es für großskalige Retrieval-Systeme geeignet ist. Dieser Ansatz balanciert Ausdruckskraft (durch Token-Ebene-Interaktion) mit rechnerischer Machbarkeit (über vorberechnete Dokumenteinbettungen).

#### 7. Zero-Shot Dense Retrieval (HyDE)

Zero-Shot Dense Retrieval via Hypothetical Document Embeddings (HyDE) generiert ein hypothetisches Dokument aus einer Abfrage mithilfe eines Sprachmodells, das Anweisungen folgt (z. B. InstructGPT), das dann von einem kontrastiven Encoder (z. B. Contriever) eingebettet wird, ohne dass relevante Labels vorhanden sind. Die Abfrageeingabe ruft die nächsten realen Dokumente über Vektorsimilarität in einem vorab berechneten Index (z. B. [[vector-databases|Vektordatenbank]]). Die Eingaben sind eine Abfrage und ein vorab eingebetteter Dokumentenkorpus; die Ausgaben sind die top-k relevanten Dokumente. Die unsupervised Training des kontrastiven Encoders aligniert den Embedding-Raum mit dem Korpus, filtert Ungenauigkeiten aus dem generierten Dokument, während die semantische Absicht beibehalten wird. Dieses Design eliminiert den Bedarf an gelabelten Daten, hängt aber von der Fähigkeit des Sprachmodells ab, semantisch relevanten Text zu generieren. HyDE übertrifft signifikant unsupervised dense Retriever wie Contriever und erreicht eine Leistung, die mit fine-tuned Retrievern vergleichbar ist, über verschiedene Aufgaben und Sprachen hinweg [[embeddings|Embeddings]] Gao et al. (2022).

#### Ursprung und Varianten

Traditionelle Retrieval-Methoden basierten auf sparsen, termbasierten Ansätzen wie BM25 [[information-retrieval|Information Retrieval]], die Dokumente anhand der Termfrequenz und Inverse Document Frequency bewerten. Der Übergang zu dense Retrieval, wie von Karpukhin et al. (2020) gezeigt, ersetzte sparsene Vektoren durch gelernte Embeddings und ermöglichte semantisches Matching ohne exakte Termübereinstimmung. Moderne Pipelines verwenden standardmäßig zwei Stufen: Kandidatenretrieval und Reranking. Das Kandidatenretrieval erzeugt eine erste Pool-Liste mithilfe schneller Methoden – dense Retrieval (z. B. Dual-Encoder-Modelle [[embeddings|Embeddings]]) oder sparsene Methoden (BM25) – oft kombiniert durch Techniken wie Reciprocal Rank Fusion (RRF), die `score = sum(1 / (k + rank))` pro Dokument über verschiedene Rankings berechnet (k=60, gemäß Cormack et al., 2009). Die Top-k Kandidaten (z. B. k=100) werden anschließend durch einen Cross-Encoder (z. B. Nogueira & Cho, 2019) reranked, der Abfrages-Dokument-Paare gemeinsam verarbeitet, um eine höhere Präzision zu erzielen, allerdings mit erheblichem Rechenaufwand. Dieses Design balanciert Recall (durch effiziente Kandidatengenerierung) mit Präzision (durch Reranking), wobei Reranking die Latenz erhöht und auf kleine Kandidatenmengen beschränkt ist. Kompromisse umfassen die reduzierte Abhängigkeit von exakten Begriffen bei dense Retrieval im Vergleich zur Interpretierbarkeit sparsener Methoden sowie die Recall-Verbesserungen durch Fusion im Vergleich zur erhöhten Komplexität.

### Wann einsetzen

- Für offene-domain-Fragebeantwortung, die eine semantische Verständnis von paraphrasierten Abfragen erfordert, erzielt der Dense Retrieval mit [[embeddings|Embedding]] 9%-

### Stärken und Grenzen

**Stärken**
- Dense Retrieval mit Dual-Encodern (Karpukhin et al. (2020)) erzielt eine absolute Verbesserung von 9 % bis 19 % bei der Genauigkeit der top-20-Passage-Retrieval auf offenen Domain QA-Benchmarks im Vergleich zu BM25.
- Sentence-BERT (Reimers & Gurevych (2019)) reduziert die Suchzeit für semantische Ähnlichkeitssuche von ~65 Stunden (BERT) auf ~5 Sekunden für 10.000 Sätze, während die Genauigkeit auf BERT-Niveau gehalten wird.
- ColBERT (Khattab & Zaharia (2020)) erreicht die gleiche Effektivität wie BERT-basierte Modelle mit vier Größenordnungen weniger FLOPs pro Abfrage und zwei Größenordnungen schnellerer Ausführung.

**Einschränkungen**
- BERT-basierte Dense Retrieval erfordert die Verarbeitung von Abfrage-Dokument-Paaren, was die Rechenkosten um Größenordnungen gegenüber sparsamen Methoden erhöht (Khattab & Zaharia (2020)).
- Vollständig zeroshot Dense Retrieval ohne Relevanzlabels bleibt herausfordernd (Gao et al. (2022)), wodurch zusätzliche Techniken wie HyDE zur Einbettungsgrounding erforderlich sind.
- Die Abhängigkeit der Leistung von der Qualität des Embedding-Modells und den Trainingsdaten (Karpukhin et al. (2020); Nogueira & Cho (2019)) macht die Bereitstellung in verschiedenen Domänen kompliziert.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Dense Retrieval (dual-encoder) | Erreicht 9–19 % höhere Genauigkeit bei der top-20-Passage-Rückgewinnung als BM25 (Karpukhin et al. (2020)) und reduziert die Zeit für semantische Suche von Stunden auf Sekunden (Reimers & Gurevych (2019)) | Natürliche Sprachanfragen, die semantisches Verständnis erfordern (z. B. Paraphrasen, Synonyme) |
| Sparse Retrieval (BM25) | Reliert auf lexikale Begriffsmatching ohne Embedding-Berechnung, wie in der Information Retrieval standardisiert (Robertson & Zaragoza (2009)) | Anfragen, die exakte Begriffsgenauigkeit erfordern (z. B. rechtliche Zitierungen, technische Spezifikationen) |
Dense Retrieval basiert typischerweise auf vorberechneten Embeddings (siehe [[embeddings|Embeddings]]), während sparse Methoden termbasierte Indexierung verwenden (siehe [[information-retrieval|Information Retrieval]]).

### In der Praxis

Die Bewertung der Retrieval-Effektivität erfolgt typischerweise mit der Genauigkeit des top-20 Passage Retrievals (Karpukhin et al., 2020) oder dem MRR@10 (Nogueira & Cho, 2019), wobei Dense Retrieval-Systeme die sparsen Baselines um 9–19 % absolut übertrumpfen. Typische Fehlermodi umfassen Kontextverschmutzung (das Retrieval irrelevanter Dokumente) und geringe Recall (fehlende relevante Dokumente), was die Qualität der LLM-Antworten verschlechtert [[rag-failure-modes|Fehlermodi]]. Parameterauswahl umfasst top-k (typischerweise 3–10), wobei kleinere Werte die Tokenanzahl und die LLM-Kosten reduzieren, aber das Risiko erhöhen, Informationen zu verpassen, während größere Werte die Recall erhöhen, allerdings mit dem Preis der Kontextverschmutzung; Embedding-Modelle (z. B. SBERT) und Vektorindizes (z. B. HNSW) werden aus Gründen der Effizienz und Genauigkeit ausgewählt [[vector-databases|Vektordatenbanken]].

### Merksatz

Die Retrieval-Methoden in RAG balancieren die lexikalische Präzision und rechnerische Effizienz der sparsamen [[information-retrieval|Information Retrieval]]-Methoden gegenüber der semantischen Genauigkeit der dichten [[embeddings|Embeddings]]-Methoden, wobei kürzliche Fortschritte den Effizienzunterschied reduziert haben.

### Quellen

- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Gao, L. et al. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
