---
title_en: Semantic Retrieval
title_de: Semantisches Retrieval
entity_type: Method
sources:
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/2004.04906
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/1901.04085
- https://arxiv.org/abs/2212.10496
- https://arxiv.org/abs/2104.08663
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Semantic retrieval finds documents by meaning rather than by shared words: queries and documents are encoded as vectors, and documents whose vectors are close to the query vector are returned (Reimers & Gurevych, 2019; Karpukhin et al., 2020). Dense retrievers outperformed BM25 on open-domain question answering, late-interaction models and cross-encoder re-rankers add precision (Khattab & Zaharia, 2020; Nogueira & Cho, 2019), and hypothetical document embeddings work without relevance labels (Gao et al., 2022). On diverse benchmarks, however, BM25 remains a robust baseline, so semantic and lexical retrieval are often combined (Thakur et al., 2021).

### How it works

An encoder turns every document into an embedding in advance, and the embeddings are stored in an index. At query time, the query is encoded the same way, the nearest document embeddings are retrieved, and optionally a more expensive model re-ranks the top candidates.

```text
1. From lexical to semantic matching
▼
2. Bi-encoders and sentence embeddings
▼
3. Dense passage retrieval
▼
4. Late interaction and re-ranking
▼
5. Retrieval without labelled data
▼
6. Generalisation across domains
```

#### 1. From lexical to semantic matching

Lexical retrieval with BM25 or tf-idf matches the words of the query ([[information-retrieval|Information Retrieval]]). It misses relevant documents that use different words for the same meaning; semantic retrieval addresses this by comparing learned representations of meaning ([[embeddings|Embeddings]]).

#### 2. Bi-encoders and sentence embeddings

Scoring every query-document pair jointly with BERT is too expensive for search: finding the most similar pair among 10,000 sentences takes about 65 hours (Reimers & Gurevych, 2019). Sentence-BERT encodes each text separately into an embedding compared with cosine similarity, which reduces this to about 5 seconds while keeping BERT's accuracy; document embeddings can be computed once and stored in a vector index ([[vector-databases|Vector Databases]]).

#### 3. Dense passage retrieval

Karpukhin et al. (2020) showed that retrieval for open-domain question answering can be implemented with dense representations alone, learned from a small number of questions and passages by a dual-encoder framework. Their dense retriever outperformed a strong Lucene-BM25 system by 9% to 19% absolute in top-20 passage retrieval accuracy.

#### 4. Late interaction and re-ranking

ColBERT encodes query and document separately with BERT but keeps an embedding per token and computes a cheap late-interaction score between them; it was competitive with BERT-based ranking models while running two orders of magnitude faster and needing four orders of magnitude fewer FLOPs per query (Khattab & Zaharia, 2020). A cross-encoder re-ranker processes query and passage together and is the most accurate but most expensive option, so it is applied only to the top candidates; a BERT re-ranker improved the previous state of the art on MS MARCO passage retrieval by 27% relative in MRR@10 (Nogueira & Cho, 2019).

#### 5. Retrieval without labelled data

Without relevance labels, it is hard to train an effective dense retriever. HyDE first lets an instruction-following language model write a hypothetical answer document for the query and then retrieves real documents whose embeddings are close to it; the encoder's dense bottleneck filters out false details of the generated document (Gao et al., 2022). HyDE significantly outperformed the unsupervised dense retriever Contriever and was comparable to fine-tuned retrievers across tasks and languages.

#### 6. Generalisation across domains

BEIR evaluated 10 retrieval systems on 18 datasets from diverse domains in a zero-shot setting (Thakur et al., 2021). BM25 proved a robust baseline; re-ranking and late-interaction models achieved the best average zero-shot results at high computational cost, while dense retrievers were efficient but often underperformed, showing considerable room for improvement in their generalisation.

#### Origin and variants

Sentence-BERT (Reimers & Gurevych, 2019) made sentence embeddings practical for search, dense passage retrieval (Karpukhin et al., 2020) showed their value for question answering, ColBERT (Khattab & Zaharia, 2020) and cross-encoder re-ranking (Nogueira & Cho, 2019) improved precision, HyDE (Gao et al., 2022) removed the need for labels, and BEIR (Thakur et al., 2021) tested generalisation.

### When to use it

- When queries and relevant documents use different wording, as in natural-language questions (Karpukhin et al., 2020).
- When retrieval feeds a RAG system and must find passages by meaning ([[rag-retrieval|RAG: Retrieval]]).
- When exact terms matter or the domain differs strongly from the training data, semantic retrieval should be combined with BM25 (Thakur et al., 2021).

### Strengths and limitations

**Strengths**
- Finds relevant passages with different wording; outperformed BM25 on open-domain QA (Karpukhin et al., 2020).
- Document embeddings are precomputed, so search is fast (Reimers & Gurevych, 2019).
- Re-ranking and late interaction raise precision on the top results (Nogueira & Cho, 2019; Khattab & Zaharia, 2020).

**Limitations**
- Dense retrievers often generalise poorly to new domains, where BM25 is a robust baseline (Thakur et al., 2021).
- Training effective dense retrievers usually needs relevance labels (Gao et al., 2022).
- Cross-encoder re-ranking is computationally expensive (Thakur et al., 2021).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| BM25 | Lexical term matching ([[information-retrieval|Information Retrieval]]) | Exact terms, robust baseline |
| Bi-encoder / dense retrieval | One embedding per text, nearest-neighbour search (Reimers & Gurevych, 2019; Karpukhin et al., 2020) | Fast semantic search |
| Late interaction (ColBERT) | Token-level embeddings with cheap interaction (Khattab & Zaharia, 2020) | Higher precision at moderate cost |
| Cross-encoder re-ranker | Query and passage scored jointly (Nogueira & Cho, 2019) | Re-ranking the top candidates |
| HyDE | Retrieval via a generated hypothetical document (Gao et al., 2022) | No relevance labels available |

### In practice

A common pipeline combines BM25 and dense retrieval (hybrid search), then re-ranks the top candidates with a cross-encoder (Thakur et al., 2021; Nogueira & Cho, 2019). Retrieval quality is measured on queries from the target domain with recall@k and nDCG ([[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]).

### Key takeaway

Semantic retrieval compares meaning through embeddings, which finds differently worded passages, but it is usually combined with lexical search and re-ranking to be robust.

### Sources

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Gao, L. et al. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* ACL 2023. [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Semantisches Retrieval findet Dokumente nach ihrer Bedeutung statt nach gemeinsamen Wörtern: Anfragen und Dokumente werden als Vektoren kodiert, und Dokumente, deren Vektoren nahe am Anfragevektor liegen, werden zurückgegeben (Reimers & Gurevych, 2019; Karpukhin et al., 2020). Dense Retriever übertrafen BM25 bei Open-Domain-Fragebeantwortung, Late-Interaction-Modelle und Cross-Encoder-Reranker erhöhen die Präzision (Khattab & Zaharia, 2020; Nogueira & Cho, 2019), und hypothetische Dokument-Embeddings funktionieren ohne Relevanzlabels (Gao et al., 2022). Auf vielfältigen Benchmarks bleibt BM25 aber eine robuste Baseline, weshalb semantisches und lexikalisches Retrieval oft kombiniert werden (Thakur et al., 2021).

### Funktionsweise

Ein Encoder wandelt jedes Dokument vorab in ein Embedding um, und die Embeddings werden in einem Index gespeichert. Zur Anfragezeit wird die Anfrage ebenso kodiert, die nächstgelegenen Dokument-Embeddings werden abgerufen, und optional bringt ein aufwendigeres Modell die besten Kandidaten in eine neue Rangfolge.

```text
1. Von lexikalischem zu semantischem Abgleich
▼
2. Bi-Encoder und Satz-Embeddings
▼
3. Dense Passage Retrieval
▼
4. Late Interaction und Reranking
▼
5. Retrieval ohne gelabelte Daten
▼
6. Generalisierung über Domänen
```

#### 1. Von lexikalischem zu semantischem Abgleich

Lexikalisches Retrieval mit BM25 oder tf-idf gleicht die Wörter der Anfrage ab ([[information-retrieval|Information Retrieval]]). Es übersieht relevante Dokumente, die für dieselbe Bedeutung andere Wörter verwenden; semantisches Retrieval begegnet dem, indem es gelernte Bedeutungsrepräsentationen vergleicht ([[embeddings|Embeddings]]).

#### 2. Bi-Encoder und Satz-Embeddings

Jedes Paar aus Anfrage und Dokument gemeinsam mit BERT zu bewerten ist für die Suche zu teuer: Das ähnlichste Paar unter 10.000 Sätzen zu finden dauert etwa 65 Stunden (Reimers & Gurevych, 2019). Sentence-BERT kodiert jeden Text einzeln in ein Embedding, das mit Kosinusähnlichkeit verglichen wird; das senkt den Aufwand auf etwa 5 Sekunden bei gleicher Genauigkeit wie BERT, und Dokument-Embeddings lassen sich einmal berechnen und in einem Vektorindex speichern ([[vector-databases|Vektordatenbanken]]).

#### 3. Dense Passage Retrieval

Karpukhin et al. (2020) zeigten, dass sich Retrieval für Open-Domain-Fragebeantwortung allein mit dichten Repräsentationen umsetzen lässt, die ein Dual-Encoder aus einer kleinen Zahl von Fragen und Passagen lernt. Ihr Dense Retriever übertraf ein starkes Lucene-BM25-System bei der Top-20-Genauigkeit des Passage-Retrievals um 9 bis 19 Prozentpunkte.

#### 4. Late Interaction und Reranking

ColBERT kodiert Anfrage und Dokument getrennt mit BERT, behält aber ein Embedding je Token und berechnet zwischen ihnen eine günstige späte Interaktion; es war mit BERT-basierten Ranking-Modellen konkurrenzfähig, lief dabei zwei Größenordnungen schneller und brauchte vier Größenordnungen weniger FLOPs je Anfrage (Khattab & Zaharia, 2020). Ein Cross-Encoder-Reranker verarbeitet Anfrage und Passage gemeinsam und ist die genaueste, aber teuerste Option; er wird daher nur auf die besten Kandidaten angewendet. Ein BERT-Reranker verbesserte den bisherigen Bestwert beim Passage-Retrieval auf MS MARCO um relativ 27 % im MRR@10 (Nogueira & Cho, 2019).

#### 5. Retrieval ohne gelabelte Daten

Ohne Relevanzlabels lässt sich ein wirksamer Dense Retriever schwer trainieren. HyDE lässt zunächst ein anweisungsbefolgendes Sprachmodell ein hypothetisches Antwortdokument zur Anfrage schreiben und ruft dann echte Dokumente ab, deren Embeddings diesem nahe sind; der dichte Engpass des Encoders filtert falsche Details des erzeugten Dokuments heraus (Gao et al., 2022). HyDE übertraf den unüberwachten Dense Retriever Contriever deutlich und war über Aufgaben und Sprachen hinweg mit feinabgestimmten Retrievern vergleichbar.

#### 6. Generalisierung über Domänen

BEIR evaluierte 10 Retrieval-Systeme auf 18 Datensätzen aus vielfältigen Domänen ohne vorheriges Training darauf (Thakur et al., 2021). BM25 erwies sich als robuste Baseline; Reranking- und Late-Interaction-Modelle erzielten im Mittel die besten Zero-Shot-Ergebnisse bei hohem Rechenaufwand, während Dense Retriever effizient waren, aber oft schlechter abschnitten, was großen Verbesserungsbedarf bei ihrer Generalisierung zeigt.

#### Ursprung und Varianten

Sentence-BERT (Reimers & Gurevych, 2019) machte Satz-Embeddings für die Suche praktikabel, Dense Passage Retrieval (Karpukhin et al., 2020) zeigte ihren Nutzen für die Fragebeantwortung, ColBERT (Khattab & Zaharia, 2020) und Cross-Encoder-Reranking (Nogueira & Cho, 2019) erhöhten die Präzision, HyDE (Gao et al., 2022) kam ohne Labels aus, und BEIR (Thakur et al., 2021) prüfte die Generalisierung.

### Wann einsetzen

- Wenn Anfragen und relevante Dokumente unterschiedlich formuliert sind, etwa bei Fragen in natürlicher Sprache (Karpukhin et al., 2020).
- Wenn das Retrieval ein RAG-System speist und Passagen nach Bedeutung finden muss ([[rag-retrieval|RAG: Retrieval]]).
- Wenn exakte Begriffe zählen oder die Domäne stark von den Trainingsdaten abweicht, sollte semantisches Retrieval mit BM25 kombiniert werden (Thakur et al., 2021).

### Stärken und Grenzen

**Stärken**
- Findet relevante Passagen mit anderer Formulierung; übertraf BM25 bei Open-Domain-QA (Karpukhin et al., 2020).
- Dokument-Embeddings werden vorab berechnet, die Suche ist daher schnell (Reimers & Gurevych, 2019).
- Reranking und Late Interaction erhöhen die Präzision bei den besten Treffern (Nogueira & Cho, 2019; Khattab & Zaharia, 2020).

**Einschränkungen**
- Dense Retriever generalisieren oft schlecht auf neue Domänen, wo BM25 eine robuste Baseline ist (Thakur et al., 2021).
- Wirksame Dense Retriever zu trainieren erfordert meist Relevanzlabels (Gao et al., 2022).
- Cross-Encoder-Reranking ist rechenaufwendig (Thakur et al., 2021).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| BM25 | Lexikalischer Termabgleich ([[information-retrieval|Information Retrieval]]) | Exakte Begriffe, robuste Baseline |
| Bi-Encoder / Dense Retrieval | Ein Embedding je Text, Nächste-Nachbarn-Suche (Reimers & Gurevych, 2019; Karpukhin et al., 2020) | Schnelle semantische Suche |
| Late Interaction (ColBERT) | Embeddings je Token mit günstiger Interaktion (Khattab & Zaharia, 2020) | Höhere Präzision bei moderatem Aufwand |
| Cross-Encoder-Reranker | Anfrage und Passage gemeinsam bewertet (Nogueira & Cho, 2019) | Neues Ranking der besten Kandidaten |
| HyDE | Retrieval über ein erzeugtes hypothetisches Dokument (Gao et al., 2022) | Keine Relevanzlabels verfügbar |

### In der Praxis

Eine verbreitete Pipeline kombiniert BM25 und Dense Retrieval (Hybrid Search) und bringt die besten Kandidaten dann mit einem Cross-Encoder in eine neue Rangfolge (Thakur et al., 2021; Nogueira & Cho, 2019). Die Retrieval-Qualität wird an Anfragen aus der Zieldomäne mit Recall@k und nDCG gemessen ([[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]).

### Merksatz

Semantisches Retrieval vergleicht Bedeutung über Embeddings und findet so anders formulierte Passagen, wird für Robustheit aber meist mit lexikalischer Suche und Reranking kombiniert.

### Quellen

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Gao, L. et al. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* ACL 2023. [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
