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
query
 ├─▶ sparse: BM25 over an inverted index ──────┐
 └─▶ dense: bi-encoder ─▶ ANN search (HNSW) ───┤
                                               ▼
                      fusion of both lists (RRF)
                                               ▼
                      reranking (cross-encoder)
                                               ▼
                      top-n passages ─▶ prompt
variants: late interaction (ColBERT), zero-shot query expansion (HyDE)
```

#### 1. Sparse Retrieval (BM25)

BM25 is a ranking function from the probabilistic relevance framework, described comprehensively by Robertson & Zaragoza (2009). It computes document relevance scores using term-frequency saturation (`tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avg_dl))`), inverse document frequency (IDF, typically `log((N - n + 0.5) / (n + 0.5))`), and document-length normalization (`(1 - b + b * |d| / avg_dl)` with `b` ≈ 0.75). The inverted index data structure maps each term to a list of document identifiers and term frequencies, enabling efficient term-based lookup. Inputs are a query and a document collection; outputs are a ranked list of documents. Design choices include TF saturation to avoid over-weighting highly frequent terms, IDF to emphasize discriminative terms, and length normalization to reduce bias toward longer documents. The inverted index makes query processing fast because only documents containing a query term are scored. BM25 excels with precise terminology such as names, identifiers or article numbers but does not match synonyms or paraphrases.

#### 2. Dense Retrieval with Bi-Encoders

Dense retrieval with bi-encoders encodes queries and passages independently into embeddings, either with two separate encoders (as in the dual-encoder of Karpukhin et al., 2020) or with one shared encoder trained in a siamese set-up (as in Sentence-BERT), so that no model call per query-passage pair is needed. Passage embeddings are precomputed offline and stored in a vector index (e.g., [[vector-databases|Vector Databases]]), enabling efficient similarity search at query time. Inputs are a query string and a knowledge base of passages; outputs are top-k passages ranked by similarity. The algorithm computes cosine similarity or inner product between the query embedding and all precomputed passage embeddings. This design choice prioritizes scalability: at query time only one encoder call plus a nearest-neighbour search is needed instead of one model call per passage, at the cost of storing all passage vectors and encoding the corpus in advance. Reimers & Gurevych (2019) report that finding the most similar pair among 10,000 sentences takes about 65 hours with pairwise BERT inference and about 5 seconds with sentence embeddings, while Karpukhin et al. (2020) showed that a learned dense retriever outperforms BM25 by 9-19 percentage points in top-20 passage retrieval accuracy on open-domain QA benchmarks.

#### 3. Vector Indexing (HNSW)

Vector indexing for approximate nearest neighbor (ANN) search replaces exhaustive comparison of query embeddings against all database vectors with a hierarchical graph structure. The HNSW (Hierarchical NSW) algorithm, introduced by Malkov & Yashunin (2016), constructs a multi-layer graph where each layer represents a nested subset of the data. Elements are assigned to layers with exponentially decaying probability, enabling scale separation between layers. Search begins at the top layer and uses greedy traversal to the nearest neighbor until reaching the base layer, achieving logarithmic complexity. This eliminates the need for auxiliary search structures required by other proximity graph methods. The input consists of high-dimensional embedding vectors (from [[embeddings|Embeddings]]), and the output is a ranked list of top-k nearest neighbors. The recall-speed trade-off is controlled by index parameters: increasing the number of connections per node improves recall at the cost of slower search. HNSW's fully graph-based design enables efficient large-scale vector search, making it suitable for real-time retrieval in systems like [[vector-databases|Vector Databases]].

#### 4. Hybrid Search Fusion (RRF)

Hybrid Search Fusion (RRF) combines parallel sparse (e.g., [[information-retrieval|Information Retrieval]]) and dense retrieval (using [[embeddings|Embeddings]]) results. Inputs are two ranked document lists from each method. Instead of fusing incommensurate scores (e.g., BM25 scores vs. cosine similarities), RRF uses ranks: for a document ranked `r_s` in sparse and `r_d` in dense, the score is `1/(k + r_s) + 1/(k + r_d)` with `k = 60` (Cormack et al., 2009). This avoids score normalization and leverages relative ordering within each method. The output is a single fused list sorted by total score. Design choices prioritize efficiency: ranks require no scale adjustment, and fixed `k=60` balances top-result influence. Trade-offs include losing score magnitude details (only rank order matters) but enabling robust fusion without cross-validation. RRF outperformed Condorcet Fuse and CombMNZ (Cormack et al., 2009) by effectively combining complementary retrieval signals.

#### 5. Reranking with Cross-Encoders

Reranking with cross-encoders refines relevance ordering by jointly processing query-passage pairs. The input concatenates the query and passage with [CLS] and [SEP] tokens (e.g., `[CLS] query [SEP] passage [SEP]`), processed by a BERT-based model. The [CLS] token's output embedding generates a relevance probability via a linear layer, yielding a score for each candidate pair. This step operates on a first-stage candidate list (e.g., BM25 top 1000), reordering candidates by refined relevance. The two-stage design employs a computationally cheap retriever (e.g., BM25) for high recall, producing a large candidate pool, followed by a precision-focused cross-encoder reranker. This trade-off is essential: cross-encoders require per-pair inference (O(N) complexity), making them infeasible for full corpus retrieval but optimal for small candidate sets. The candidate list size `k` directly balances latency and precision—smaller `k` reduces computation but risks discarding relevant passages, while larger `k` increases cost without proportional gains. This architecture leverages the efficiency of sparse retrieval for broad coverage while achieving higher precision through deep contextual modeling.

#### 6. Late Interaction (ColBERT)

ColBERT (Khattab & Zaharia, 2020) implements a late interaction architecture that independently encodes queries and documents into token-level embeddings using BERT, enabling precomputation of document representations for efficient offline storage. At query time, the query is encoded, and a lightweight interaction step scores the document: for every query token the maximum similarity to any document token is taken, and these maxima are summed (MaxSim). This positions ColBERT between bi-encoders (which use scalar similarity on whole-document embeddings) and cross-encoders (which process full query-document pairs). The design achieves competitive accuracy with cross-encoders while maintaining efficiency: document embeddings require only one-off computation, and the interaction step avoids per-pair neural processing during retrieval. Khattab & Zaharia (2020) report that ColBERT is competitive with BERT-based ranking models while executing two orders of magnitude faster and requiring four orders of magnitude fewer FLOPs per query. This approach balances expressiveness (through token-level interaction) with computational feasibility (via precomputed document embeddings).

#### 7. Zero-Shot Dense Retrieval (HyDE)

Zero-Shot Dense Retrieval via Hypothetical Document Embeddings (HyDE) generates a hypothetical document from a query using an instruction-following language model (e.g., InstructGPT), which is then embedded by a contrastive encoder (e.g., Contriever) without relevance labels. The embedding of this hypothetical document, not of the query itself, is used to retrieve the nearest real documents via vector similarity in a precomputed index (e.g., [[vector-databases|Vector Database]]). Inputs are a query and a pre-embedded document corpus; outputs are top-k relevant documents. The contrastive encoder's unsupervised training aligns the embedding space with the corpus, filtering inaccuracies from the generated document while preserving semantic intent. This design eliminates the need for labeled data but relies on the language model's ability to generate semantically relevant text. Gao et al. (2022) report that HyDE significantly outperforms the unsupervised dense retriever Contriever and is comparable to fine-tuned retrievers across various tasks and languages.

#### Origin and variants

Traditional retrieval relied on term-based sparse methods like BM25 [[information-retrieval|Information Retrieval]], which scores documents using term frequency and inverse document frequency. The shift to dense retrieval, demonstrated by Karpukhin et al. (2020), replaced sparse vectors with learned embeddings, enabling semantic matching without exact term overlap. Modern pipelines standardly employ two stages: candidate retrieval and reranking. Candidate retrieval generates an initial pool using fast methods—dense retrieval (e.g., dual-encoder models [[embeddings|Embeddings]]) or sparse methods (BM25)—often combined via fusion techniques like Reciprocal Rank Fusion (RRF), which computes `score = sum(1 / (k + rank))` per document across rankings (k=60, per Cormack et al., 2009). The top-k candidates (e.g., k=100) are then reranked by a cross-encoder (e.g., Nogueira & Cho, 2019), which jointly processes query-document pairs for higher precision but at significant computational cost. This design balances recall (from efficient candidate generation) with precision (via reranking), though reranking increases latency and is restricted to small candidate sets. Trade-offs include dense retrieval's reduced reliance on exact terms versus sparse methods' interpretability, and fusion's recall gains versus added complexity.

### When to use it

- Queries phrased differently from the documents (paraphrases, synonyms, natural-language questions): dense retrieval with [[embeddings|embeddings]].
- Queries with exact identifiers, names, codes or article numbers: sparse retrieval with BM25, usually combined with dense retrieval in a hybrid set-up.
- Large corpora with latency requirements: a cheap first stage (BM25, bi-encoder with an ANN index) followed by reranking only a short candidate list.
- No labelled training data for the domain: zero-shot approaches such as HyDE.

### Strengths and limitations

**Strengths**
- Dense retrieval with dual-encoders (Karpukhin et al. (2020)) achieves 9%-19% absolute improvement in top-20 passage retrieval accuracy over BM25 on open-domain QA benchmarks.
- Sentence-BERT (Reimers & Gurevych (2019)) reduces semantic similarity search time from ~65 hours (BERT) to ~5 seconds for 10,000 sentences while maintaining BERT-level accuracy.
- ColBERT (Khattab & Zaharia (2020)) matches BERT-based effectiveness with four orders of magnitude fewer FLOPs per query and two orders of magnitude faster execution.

**Limitations**
- Cross-encoder reranking with BERT needs one model call per query-passage pair and is therefore orders of magnitude more expensive than first-stage retrieval (Khattab & Zaharia, 2020); it can only be applied to short candidate lists.
- Fully zero-shot dense retrieval without relevance labels remains challenging (Gao et al. (2022)), necessitating additional techniques like HyDE for embedding grounding.
- Dense retrieval depends on the embedding model and its training data; quality can drop in domains the model was not trained on, and failures are harder to interpret than missing keyword matches.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Sparse retrieval (BM25) | Lexical term matching over an inverted index; no embedding model | Exact terms, identifiers, legal citations |
| Dense retrieval (bi-encoder) | Independent embeddings, nearest-neighbour search; matches meaning without shared words | Paraphrased and natural-language queries |
| Hybrid retrieval (RRF) | Runs both and fuses the ranked lists by rank | Mixed query types; the usual default |
| Cross-encoder reranking | Reads query and passage jointly; most precise, one model call per pair | Reordering a short candidate list |
| Late interaction (ColBERT) | Token-level embeddings, cheap MaxSim interaction | Precision close to cross-encoders at lower cost |

Dense retrieval typically relies on precomputed embeddings (see [[embeddings|Embeddings]]), while sparse methods use term-based indexing (see [[information-retrieval|Information Retrieval]]).

### In practice

Evaluation of retrieval effectiveness typically uses top-20 passage retrieval accuracy (Karpukhin et al., 2020) or MRR@10 (Nogueira & Cho, 2019); see [[rag-retrieval-evaluation|retrieval evaluation]]. Typical failure modes include context pollution (retrieving irrelevant documents) and low recall (missing relevant documents), degrading LLM response quality [[rag-failure-modes|Failure Modes]]. Parameter choices include top-k (typically 3–10), with smaller values reducing token count and LLM cost but risking missing information, while larger values increase recall at the cost of context pollution; embedding models (e.g., SBERT) and vector indexes (e.g., HNSW) are selected for efficiency and accuracy [[vector-databases|Vector Databases]].

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

Retrieval in RAG wählt relevante Kontextpassagen aus einer Wissensbasis für ein Sprachmodell aus. Es löst das Problem, dass Sprachmodelle keinen Zugriff auf externe Informationen haben, die über ihre Trainingsdaten hinausgehen, was für das Generieren präziser Antworten auf Abfragen entscheidend ist, die aktuelle oder domain-spezifische Kenntnisse erfordern.

### Funktionsweise

RAG-Retrieval verwendet einen mehrstufigen Prozess: Sparse Retrieval mithilfe von BM25 [[information-retrieval|BM25]] identifiziert Kandidatenpassagen über lexikale Übereinstimmung, während Dense Retrieval mit bi-Encodern semantische Embeddings generiert. Vektorindexierung über HNSW [[vector-databases|HNSW]] ermöglicht effiziente Ähnlichkeitssuche, und Hybridfusion kombiniert sparse und dense Ergebnisse mithilfe von Reciprocal Rank Fusion (RRF). Anschließend wird die Reranking-Phase mit Cross-Encodern durchgeführt, um die besten Kandidaten zu verfeinern, und fortgeschrittene Varianten umfassen späte Interaktion (ColBERT) und zero-shot Retrieval (HyDE).

```text
Abfrage
 ├─▶ sparse: BM25 über einen Inverted Index ──────┐
 └─▶ dense: bi-encoder ─▶ ANN-Suche (HNSW) ───┤
                                               ▼
                      Fusion beider Listen (RRF)
                                               ▼
                      Reranking (cross-encoder)
                                               ▼
                      top-n Passagen ─▶ Prompt
Varianten: späte Interaktion (ColBERT), zero-shot Abfrageerweiterung (HyDE)
```

#### 1. Sparse Retrieval (BM25)

BM25 ist eine Bewertungsfunktion aus dem probabilistischen Relevanzrahmen, umfassend beschrieben von Robertson & Zaragoza (2009). Sie berechnet Dokumentrelevanzscores mithilfe der Term Frequency Saturation (`tf * (k1 + 1) / (tf + k1 * (1 - b + b * |d| / avg_dl))`), der Inverse Document Frequency (IDF, typischerweise `log((N - n + 0.5) / (n + 0.5))`) und der Dokumentlängennormalisierung (`(1 - b + b * |d| / avg_dl)` mit `b` ≈ 0.75). Die Datenstruktur des Inverted Index ordnet jedem Begriff eine Liste von Dokumentidentifikatoren und Termausprägungen zu, was eine effiziente Begriffssuche ermöglicht. Eingaben sind eine Abfrage und eine Dokumentensammlung; Ausgaben sind eine nach Relevanz sortierte Liste von Dokumenten. Gestaltungsentscheidungen umfassen die TF-Sättigung, um hochfrequente Begriffe nicht zu stark zu gewichten, die IDF, um diskriminierende Begriffe zu betonen, und die Längennormalisierung, um den Vorteil längerer Dokumente zu verringern. Der Inverted Index macht die Abfrageverarbeitung schnell, da nur Dokumente, die einen Abfragebegriff enthalten, bewertet werden. BM25 ist besonders effektiv bei präziser Terminologie wie Namen, Identifikatoren oder Artikelnummern, passt aber keine Synonyme oder Paraphrasen an.

#### 2. Dichter Retrieval mit Bi-Encodern

Dichter Retrieval mit Bi-Encodern kodiert Abfragen und Passagen unabhängig in Embeddings, entweder mit zwei separaten Encodern (wie bei dem Dual-Encoder von Karpukhin et al., 2020) oder mit einem gemeinsamen Encoder, der in einer siamesischen Konfiguration trainiert wird (wie bei Sentence-BERT), so dass keine Modellaufrufe pro Abfrage-Passage-Paar notwendig sind. Passage-Embeddings werden offline vorab berechnet und in einem Vektorindex gespeichert (z. B. [[vector-databases|Vektordatenbank]], was eine effiziente Ähnlichkeitssuche bei der Abfrage ermöglicht. Die Eingaben sind eine Abfragezeichenfolge und eine Wissensbasis aus Passagen; die Ausgaben sind die top-k Passagen, die nach Ähnlichkeit sortiert sind. Der Algorithmus berechnet die Kosinusähnlichkeit oder das Skalarprodukt zwischen dem Abfrage-Embedding und allen vorab berechneten Passage-Embeddings. Diese Gestaltung entspricht der Priorisierung der Skalierbarkeit: bei der Abfrage ist nur ein Encoder-Aufruf plus eine Nachbarschaftssuche erforderlich, anstatt einen Modellauftrag pro Passage, wobei der Preis dafür besteht, alle Passage-Vektoren zu speichern und den Korpus im Voraus zu kodieren. Reimers & Gurevych (2019) berichten, dass das Finden des ähnlichsten Paares unter 10.000 Sätzen etwa 65 Stunden mit paarweiser BERT-Interferenz und etwa 5 Sekunden mit Satz-Embeddings dauert, während Karpukhin et al. (2020) zeigten, dass ein gelernter dichter Retriever bei der top-20-Passage-Retrievalgenauigkeit auf offenen Domain QA-Benchmarks BM25 um 9–19 Prozentpunkte übertrifft.

#### 3. Vektorindexierung (HNSW)

Die Vektorindexierung für Approximate Nearest Neighbor (ANN)-Suche ersetzt die umfassende Vergleichung von Abfrage-Embeddings mit allen Datenbankvektoren durch eine hierarchische Graphstruktur. Der HNSW-Algorithmus (Hierarchical NSW), eingeführt von Malkov & Yashunin (2016), erstellt einen mehrschichtigen Graphen, wobei jede Schicht eine verschachtelte Teilmenge der Daten darstellt. Elemente werden mit exponentiell abnehmender Wahrscheinlichkeit Schichten zugewiesen, was eine Skalentrennung zwischen Schichten ermöglicht. Die Suche beginnt in der obersten Schicht und nutzt eine gierige Traversierung zum nächsten Nachbarn, bis die Grundschicht erreicht ist, wodurch eine logarithmische Komplexität erreicht wird. Dies beseitigt den Bedarf an Hilfsstrukturen, die von anderen Verfahren für Nähegraphen erforderlich sind. Die Eingabe besteht aus hochdimensionalen Embedding-Vektoren (aus [[embeddings|Embeddings]]), und die Ausgabe ist eine rangierte Liste der top-k nächsten Nachbarn. Der Kompromiss zwischen Erinnerungsfähigkeit und Geschwindigkeit wird durch Indexparameter gesteuert: eine Erhöhung der Anzahl der Verbindungen pro Knoten verbessert die Erinnerungsfähigkeit, allerdings auf Kosten einer langsameren Suche. Der vollständig graphbasierte Entwurf von HNSW ermöglicht effiziente großskalige Vektor-Suche, wodurch es für Echtzeit-Retrieval in Systemen wie [[vector-databases|Vektordatenbanken]] geeignet ist.

#### 4. Hybrid Search Fusion (RRF)

Hybrid Search Fusion (RRF) kombiniert parallele sparse (z. B. [[information-retrieval|Information Retrieval]]) und dense Retrieval (mit [[embeddings|Embeddings]]) Ergebnisse. Eingaben sind zwei rangierte Dokumentlisten aus jedem Verfahren. Anstatt inkompatible Scores zu kombinieren (z. B. BM25 Scores vs. Kosinusähnlichkeiten) verwendet RRF Ränge: für ein Dokument, das im sparse Verfahren den Rang `r_s` und im dense Verfahren den Rang `r_d` hat, ist der Score `1/(k + r_s) + 1/(k + r_d)` mit `k = 60` (Cormack et al., 2009). Dies vermeidet die Score-Normalisierung und nutzt die relative Ordnung innerhalb jedes Verfahrens. Das Ergebnis ist eine einzelne zusammengeführte Liste, die nach Gesamtscore sortiert ist. Designentscheidungen priorisieren Effizienz: Ränge benötigen keine Skalierung, und der festgelegte Wert `k=60` balanciert den Einfluss der besten Ergebnisse. Kompromisse umfassen den Verlust von Details der Score-Magnitude (nur die Rangordnung zählt) aber ermöglichen eine robuste Kombination ohne Kreuzvalidierung. RRF übertraf Condorcet Fuse und CombMNZ (Cormack et al., 2009), indem es komplementäre Retrieval-Signale effektiv kombinierte.

#### 5. Reranking mit Cross-Encodern

Das Reranking mit Cross-Encodern verfeinert die Relevanzreihenfolge durch gemeinsame Verarbeitung von Abfrage-Passage-Paaren. Die Eingabe verknüpft die Abfrage und Passage mit [CLS]- und [SEP]-Token (z. B. `[CLS] query [SEP] passage [SEP]`), die von einem BERT-basierten Modell verarbeitet werden. Das Ausgabeverbundenebene des [CLS]-Tokens erzeugt eine Relevanzwahrscheinlichkeit über eine lineare Schicht, wodurch ein Score für jedes Kandidatenpaar erzeugt wird. Dieser Schritt wird auf einer ersten Stufe Kandidatenliste (z. B. BM25 Top 1000) durchgeführt, wobei die Kandidaten nach verfeinerter Relevanz neu geordnet werden. Das zweistufige Design verwendet einen rechenleichten Retriever (z. B. BM25) für eine hohe Recall, der eine große Kandidatenpool erzeugt, gefolgt von einem präzisionsorientierten Cross-Encoder-Reranker. Dieser Kompromiss ist entscheidend: Cross-Encoder erfordern eine Paarweise Inferenz (O(N) Komplexität), wodurch sie für die vollständige Korpus-Retrieval nicht umsetzbar sind, aber optimal für kleine Kandidatenmengen. Die Größe der Kandidatenliste `k` gleicht direkt Latenz und Präzision aus – ein kleineres `k` reduziert die Rechenleistung, birgt aber das Risiko, relevante Passagen zu verwerfen, während ein größeres `k` die Kosten erhöht, ohne proportionale Vorteile. Diese Architektur nutzt die Effizienz der sparsamen Retrieval-Methoden für eine breite Abdeckung, während sie durch tiefgehende kontextuelle Modellierung eine höhere Präzision erzielt.

#### 6. Späte Wechselwirkung (ColBERT)

ColBERT (Khattab & Zaharia, 2020) implementiert eine Architektur mit späterer Wechselwirkung, die Abfragen und Dokumente unabhängig in Token-Embeddings kodiert, wobei BERT verwendet wird. Dies ermöglicht die vorab Berechnung von Dokumentrepräsentationen für eine effiziente Offline-Speicherung. Bei der Abfrage wird diese kodiert und ein leichtgewichtiger Wechselwirkungsschritt bewertet das Dokument: Für jedes Abfragetoken wird die maximale Ähnlichkeit zu jedem Dokumententoken ermittelt, und diese Maxima werden summiert (MaxSim). Dies positioniert ColBERT zwischen Bi-Encodern (die skalare Ähnlichkeit auf gesamtdokumentbasierten Embeddings verwenden) und Cross-Encodern (die vollständige Abfrage-Dokument-Paare verarbeiten). Das Design erzielt eine wettbewerbsfähige Genauigkeit im Vergleich zu Cross-Encodern, während Effizienz gewahrt bleibt: Dokumenteinbettungen erfordern nur eine einmalige Berechnung, und der Wechselwirkungsschritt vermeidet während der Retrieval-Phase die neuronale Verarbeitung pro Paar. Khattab & Zaharia (2020) berichten, dass ColBERT mit BERT-basierten Rangiermodellen wettbewerbsfähig ist, während es um zwei Größenordnungen schneller ausführt und pro Abfrage um vier Größenordnungen weniger FLOPs benötigt. Dieser Ansatz balanciert Ausdruckskraft (durch Token-basierte Wechselwirkung) mit rechnerischer Umsetzbarkeit (durch vorberechnete Dokumenteinbettungen).

#### 7. Zero-Shot Dense Retrieval (HyDE)

Zero-Shot Dense Retrieval über hypothetische Dokument-Embeddings (HyDE) generiert ein hypothetisches Dokument aus einer Anfrage mithilfe eines Sprachmodells, das Anweisungen folgt (z. B. InstructGPT), das anschließend von einem kontrastiven Encoder (z. B. Contriever) eingebettet wird, ohne dass relevante Etiketten vorhanden sind. Die Einbettung dieses hypothetischen Dokuments, nicht die der Anfrage selbst, wird verwendet, um über Vektorsimilarität in einem vorberechneten Index (z. B. [[vector-databases|Vektordatenbank]]) die nächsten realen Dokumente abzurufen. Eingaben sind eine Anfrage und ein vorab eingebetteter Dokumentenkorpus; Ausgaben sind die top-k relevanten Dokumente. Die unsupervisede Schulung des kontrastiven Encoders ordnet den Einbettungsraum dem Korpus zu, filtert Ungenauigkeiten aus dem generierten Dokument, während die semantische Absicht beibehalten wird. Dieses Design beseitigt den Bedarf an etikettierten Daten, hängt jedoch von der Fähigkeit des Sprachmodells ab, semantisch relevanten Text zu generieren. Gao et al. (2022) berichten, dass HyDE den unsuperviseden dichten Retriever Contriever deutlich übertrifft und in verschiedenen Aufgaben und Sprachen mit feinabgestimmten Retrievern vergleichbar ist.

#### Ursprung und Varianten

Traditionelle Retrieval-Methoden basierten auf sparsen, termbasierten Verfahren wie BM25 [[information-retrieval|Information Retrieval]], die Dokumente anhand der Termhäufigkeit und Inverse Document Frequency bewerten. Der Übergang zu Dense Retrieval, wie von Karpukhin et al. (2020) gezeigt, ersetzte sparsene Vektoren durch gelernte Embeddings, was semantisches Matching ohne exakte Termübereinstimmung ermöglichte. Moderne Pipelines verwenden standardmäßig zwei Stufen: Kandidatenretrieval und Reranking. Das Kandidatenretrieval erzeugt eine erste Menge von Kandidaten mithilfe schneller Methoden – Dense Retrieval (z. B. Dual-Encoder-Modelle [[embeddings|Embeddings]]) oder sparsene Methoden (BM25) – oft kombiniert durch Techniken wie Reciprocal Rank Fusion (RRF), die `score = sum(1 / (k + rank))` pro Dokument über die Ranglisten berechnet (k=60, gemäß Cormack et al., 2009). Die Top-k Kandidaten (z. B. k=100) werden anschließend durch einen Cross-Encoder (z. B. Nogueira & Cho, 2019) reranked, der Abfragen und Dokumente gemeinsam verarbeitet, um eine höhere Präzision zu erzielen, allerdings mit erheblichem Rechenaufwand. Dieses Design balanciert Recall (durch effiziente Kandidatengenerierung) mit Präzision (durch Reranking), wobei Reranking die Latenz erhöht und auf kleine Kandidatenmengen beschränkt ist. Kompromisse umfassen die reduzierte Abhängigkeit des Dense Retrievals von exakten Begriffen im Vergleich zur Interpretierbarkeit sparsener Methoden sowie die Recall-Verbesserungen durch Fusion im Vergleich zur zusätzlichen Komplexität.

### Wann einsetzen

- Abweichende Formulierungen der Abfragen im Vergleich zu den Dokumenten (Paraphrasen, Synonyme, natürliche Sprachfragen): dichter Retrieval mit [[embeddings|Embedding]].
- Abfragen mit exakten Identifiern, Namen, Codes oder Artikelnummern: spärlicher Retrieval mit BM25, meist in Kombination mit Dense Retrieval in einer hybriden Anordnung.
- Große Corpora mit Latenzanforderungen: billige erste Stufe (BM25, bi-Encoder mit einem ANN-Index), gefolgt von einem Reranking nur einer kurzen Kandidatenliste.
- Keine etikettierten Trainingsdaten für den Bereich: zero-shot Ansätze wie HyDE.

### Stärken und Grenzen

**Stärken**
- Dense Retrieval mit Dual-Encodern (Karpukhin et al. (2020)) erzielt eine absolute Verbesserung um 9%-19 % bei der Genauigkeit der top-20-Passage-Retrieval auf offenen Domain QA-Benchmarks im Vergleich zu BM25.
- Sentence-BERT (Reimers & Gurevych (2019)) reduziert die Zeit für semantische Ähnlichkeitssuche von ~65 Stunden (BERT) auf ~5 Sekunden für 10.000 Sätze, während die BERT-Niveau Genauigkeit beibehalten wird.
- ColBERT (Khattab & Zaharia (2020)) erreicht die gleiche Effektivität wie BERT-basierte Modelle mit vier Größenordnungen weniger FLOPs pro Abfrage und zwei Größenordnungen schnellerer Ausführung.

**Einschränkungen**
- Cross-Encoder-Reranking mit BERT benötigt eine Modellaufruf pro Abfrage-Passage-Paar und ist daher um Größenordnungen teurer als die erste Stufe Retrieval (Khattab & Zaharia, 2020); es kann nur auf kurzen Kandidatenlisten angewendet werden.
- Vollständig zero-shot Dense Retrieval ohne Relevanzlabels bleibt herausfordernd (Gao et al. (2022)), was zusätzliche Techniken wie HyDE zur Einbettungsgrounding erforderlich macht.
- Dense Retrieval hängt vom Embedding-Modell und dessen Trainingsdaten ab; die Qualität kann in Bereichen sinken, in denen das Modell nicht trainiert wurde, und Fehler sind schwerer zu interpretieren als fehlende Schlüsselwortübereinstimmungen.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Sparse Retrieval (BM25) | Lexikalische Begriffssuche über einen Inverted Index; kein Embedding-Modell | Genauere Begriffe, Identifikatoren, rechtliche Zitierungen |
| Dense Retrieval (bi-Encoder) | Unabhängige Embeddings, Approximate Nearest Neighbor Search; passt Bedeutung ohne gemeinsame Wörter | Paraphrasierte und natürliche Sprachabfragen |
| Hybrid Retrieval (RRF) | Führt beide durch und verschmilzt die rangierten Listen nach Rang | Gemischte Abfragetypen; die übliche Voreinstellung |
| Cross-Encoder Reranking | Liest Abfrage und Passage gemeinsam; präziseste, eine Modellaufruf pro Paar | Umordnen einer kurzen Kandidatenliste |
| Late Interaction (ColBERT) | Token-basierte Embeddings, günstige MaxSim-Interaktion | Präzision nahe bei Cross-Encodern zu geringerem Kosten |

Dense Retrieval basiert typischerweise auf vorgerechneten Embeddings (siehe [[embeddings|Embeddings]]), während sparse Methoden term-basierte Indexierung verwenden (siehe [[information-retrieval|Information Retrieval]]).

### In der Praxis

Die Bewertung der Retrieval-Effektivität erfolgt typischerweise mithilfe der top-20 Passage-Retrieval-Genauigkeit (Karpukhin et al., 2020) oder des MRR@10 (Nogueira & Cho, 2019); siehe [[rag-retrieval-evaluation|Retrieval-Bewertung]]. Typische Fehlmodi umfassen Kontextverschmutzung (Retrieval von irrelevanten Dokumenten) und geringe Recall (fehlende relevante Dokumente), was die Qualität der LLM-Antworten verschlechtert [[rag-failure-modes|Fehlmodi]]. Parameterauswahl umfasst top-k (typischerweise 3–10), wobei kleinere Werte die Tokenanzahl und die LLM-Kosten reduzieren, aber das Risiko von fehlender Information erhöhen, während größere Werte die Recall erhöhen, jedoch zu Kosten in Form von Kontextverschmutzung führen; Embedding-Modelle (z. B. SBERT) und Vektordatenbanken (z. B. HNSW) werden aus Gründen der Effizienz und Genauigkeit ausgewählt [[vector-databases|Vektordatenbanken]].

### Merksatz

Die Retrieval-Methoden in RAG balancieren die lexikalische Präzision und rechnerische Effizienz der sparsamen [[information-retrieval|Information Retrieval]]-Methoden gegenüber der semantischen Genauigkeit der dichten [[embeddings|Embeddings]]-Methoden, wobei kürzliche Fortschritte den Effizienzunterschied verringert haben.

### Quellen

- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Gao, L. et al. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
