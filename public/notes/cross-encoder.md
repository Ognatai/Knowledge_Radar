---
title_en: Cross-encoder
title_de: Cross-Encoder
entity_type: Method
aliases:
- Cross-encoder re-ranker
- BERT re-ranker
sources:
- https://arxiv.org/abs/1905.01969
- https://arxiv.org/abs/1901.04085
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/2104.08663
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
A cross-encoder scores a pair of texts, such as a query and a passage, by feeding both together into one Transformer that performs full self-attention over the pair; a bi-encoder instead encodes each text separately (Humeau et al., 2019). Cross-encoders tend to be much more accurate, but every pair needs its own model pass, so in search they re-rank a short candidate list from a fast first-stage retriever (Humeau et al., 2019; Nogueira & Cho, 2019).

### How it works

```text
Bi-encoder                                   Cross-encoder
query ─▶ [encoder] ─▶ q ─┐                   [CLS] query [SEP] passage [SEP]
                         ├─▶ cos(q, p)                    │
passage ─▶ [encoder] ─▶ p ┘                    [Transformer, full attention]
 (p can be computed once and stored)                      │
                                                [CLS] ─▶ relevance score
```

#### 1. Joint encoding
Query and passage are concatenated with separator tokens and passed through a pre-trained Transformer such as [[bert|BERT]]. Because every token attends to every other token, words of the query interact with words of the passage in all layers (Humeau et al., 2019; Khattab & Zaharia, 2020).

#### 2. Scoring
Nogueira & Cho (2019) used BERT-Large as a binary classifier: the [CLS] vector goes into a single-layer network that outputs the probability that the passage is relevant. Queries were truncated to 64 tokens and query plus passage to 512 tokens. The model was fine-tuned on relevant and non-relevant passages among the top 1,000 that BM25 retrieved for each query.

#### 3. Re-ranking in a pipeline
A first stage, such as [[bm25|BM25]] or a dense retriever, retrieves candidates from the whole collection, for example a thousand documents; the cross-encoder then re-scores each query–candidate pair and the list is sorted by the new scores (Nogueira & Cho, 2019). Only the candidates are scored, since a cross-encoder cannot pre-compute anything for the collection.

#### 4. Why it is slow
A bi-encoder can encode all candidates once, cache them and compare them with each new input. A cross-encoder must recompute the encoding for every input and candidate, which makes it prohibitively slow for scoring large numbers of candidates (Humeau et al., 2019). Finding the most similar pair among 10,000 sentences with a BERT cross-encoder takes about 50 million inference computations, roughly 65 hours on a V100 GPU, against about 5 seconds with [[sentence-bert|Sentence-BERT]] embeddings (Reimers & Gurevych, 2019).

#### Origin and variants
Humeau et al. (2019) compared the two common architectures for scoring pairs, cross-encoders and bi-encoders, and proposed the poly-encoder in between, which is faster than a cross-encoder and more accurate than a bi-encoder. Nogueira & Cho (2019) applied BERT as a passage re-ranker. ColBERT (Khattab & Zaharia, 2020) delays the interaction: query and documents are encoded separately and compared token by token, so document representations can be pre-computed; see [[semantic-retrieval|Semantic Retrieval]].

### When to use it
- Re-ranking the top candidates of a first-stage retriever in search and [[retrieval-augmented-generation|retrieval-augmented generation]] (Nogueira & Cho, 2019; [[rag-retrieval|RAG: Retrieval]]).
- When precision at the top of the list matters more than latency (Humeau et al., 2019).
- When the retrieval domain differs from the training data: re-ranking models generalised well to out-of-distribution data in BEIR (Thakur et al., 2021).
- Scoring a small number of given sentence pairs, for example their semantic similarity, a sentence-pair task on which BERT set new state-of-the-art results (Reimers & Gurevych, 2019).

### Strengths and limitations

**Strengths**
- Higher accuracy than bi-encoders, since query and text interact in every layer (Humeau et al., 2019).
- A BERT re-ranker outperformed the previous state of the art on MS MARCO passage retrieval by 27% relative in MRR@10 (Nogueira & Cho, 2019).
- On BEIR, re-ranking BM25's top candidates with a cross-encoder (BM25+CE) gave the best zero-shot results and beat BM25 on 16 of 18 datasets (Thakur et al., 2021).

**Limitations**
- One model pass per query–candidate pair, nothing can be pre-computed for the collection: unusable for searching a whole collection (Humeau et al., 2019).
- High computational cost at query time, even when only re-ranking (Thakur et al., 2021).
- The result can only be as good as the candidate list: a relevant document the first stage misses is never re-ranked ([[rag-failure-modes|RAG: Failure Modes]]).
- Input length is limited; Nogueira & Cho (2019) truncated query and passage to 512 tokens.
- No independent sentence embeddings are computed, so the output cannot be stored, indexed or clustered (Reimers & Gurevych, 2019).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| Cross-encoder | Query and text together, full attention over the pair; accurate, slow (Humeau et al., 2019) | Re-ranking a short candidate list |
| Bi-encoder (e.g. Sentence-BERT) | Each text encoded separately, compared by [[text-similarity-metrics\|cosine similarity]]; embeddings can be stored (Reimers & Gurevych, 2019) | First-stage retrieval, [[clustering\|clustering]], [[vector-databases\|vector databases]] |
| Poly-encoder | Candidates encoded separately, input represented by several attention codes; between the two in speed and accuracy (Humeau et al., 2019) | Scoring many candidates with better accuracy than a bi-encoder |
| Late interaction (ColBERT) | Token-level comparison of separately encoded query and document; competitive with BERT re-rankers, two orders of magnitude faster (Khattab & Zaharia, 2020) | Re-ranking or retrieval at scale |
| [[bm25\|BM25]] | Lexical term matching, no model (Thakur et al., 2021) | Fast first stage |

### In practice
The usual pipeline is retrieve-then-re-rank: a cheap first stage with high recall, then a cross-encoder on the top candidates ([[rag-retrieval|RAG: Retrieval]]). How many candidates to re-rank is a trade-off between quality and latency, and the gain should be measured with ranking metrics on the final list ([[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]). Cross-encoders cannot fix recall: if the re-ranked list misses relevant documents, the first stage must change, for example by combining lexical and dense retrieval ([[rag-failure-modes|RAG: Failure Modes]]). For an overview of text representations, see [[embeddings|Embeddings]].

### Key takeaway
A cross-encoder reads query and text together and therefore judges relevance more accurately than comparing separate embeddings; because it has to run once per pair, it re-ranks a few candidates instead of searching the collection.

### Sources
- Humeau, S., Shuster, K., Lachaux, M.-A. & Weston, J. (2019). *Poly-encoders: Architectures and Pre-training Strategies for Fast and Accurate Multi-sentence Scoring.* ICLR 2020. [arXiv:1905.01969](https://arxiv.org/abs/1905.01969)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Ein Cross-Encoder bewertet ein Textpaar, etwa eine Anfrage und eine Passage, indem er beide gemeinsam in einen Transformer gibt, der vollständige Self-Attention über das Paar berechnet; ein Bi-Encoder kodiert dagegen jeden Text einzeln (Humeau et al., 2019). Cross-Encoder sind meist deutlich genauer, brauchen aber für jedes Paar einen eigenen Modelldurchlauf; in der Suche bewerten sie deshalb eine kurze Kandidatenliste neu, die ein schneller Retriever in der ersten Stufe liefert (Humeau et al., 2019; Nogueira & Cho, 2019).

### Funktionsweise

```text
Bi-Encoder                                   Cross-Encoder
Anfrage ─▶ [Encoder] ─▶ q ─┐                 [CLS] Anfrage [SEP] Passage [SEP]
                           ├─▶ cos(q, p)                  │
Passage ─▶ [Encoder] ─▶ p ─┘                  [Transformer, volle Attention]
 (p lässt sich einmal berechnen und speichern)            │
                                                [CLS] ─▶ Relevanz-Score
```

#### 1. Gemeinsame Kodierung
Anfrage und Passage werden mit Trenn-Tokens verbunden und durch einen vortrainierten Transformer wie [[bert|BERT]] geschickt. Da jedes Token Attention auf jedes andere richtet, interagieren Wörter der Anfrage in allen Schichten mit Wörtern der Passage (Humeau et al., 2019; Khattab & Zaharia, 2020).

#### 2. Bewertung
Nogueira & Cho (2019) nutzten BERT-Large als binären Klassifikator: Der [CLS]-Vektor geht in ein einschichtiges Netz, das die Wahrscheinlichkeit ausgibt, dass die Passage relevant ist. Anfragen wurden auf 64 Tokens gekürzt, Anfrage und Passage zusammen auf 512 Tokens. Das Modell wurde auf relevanten und nicht relevanten Passagen unter den Top 1.000 feinjustiert, die BM25 für jede Anfrage lieferte.

#### 3. Re-Ranking in einer Pipeline
Eine erste Stufe wie [[bm25|BM25]] oder ein Dense Retriever holt Kandidaten aus der gesamten Sammlung, etwa tausend Dokumente; der Cross-Encoder bewertet dann jedes Paar aus Anfrage und Kandidat neu, und die Liste wird nach den neuen Scores sortiert (Nogueira & Cho, 2019). Nur die Kandidaten werden bewertet, da ein Cross-Encoder für die Sammlung nichts vorab berechnen kann.

#### 4. Warum er langsam ist
Ein Bi-Encoder kann alle Kandidaten einmal kodieren, zwischenspeichern und mit jeder neuen Eingabe vergleichen. Ein Cross-Encoder muss die Kodierung für jede Eingabe und jeden Kandidaten neu berechnen, was ihn für das Bewerten großer Kandidatenmengen unerschwinglich langsam macht (Humeau et al., 2019). Das ähnlichste Paar unter 10.000 Sätzen mit einem BERT-Cross-Encoder zu finden, erfordert etwa 50 Millionen Inferenzschritte, rund 65 Stunden auf einer V100-GPU, gegenüber etwa 5 Sekunden mit Sentence-BERT-Embeddings (Reimers & Gurevych, 2019).

#### Ursprung und Varianten
Humeau et al. (2019) verglichen die beiden verbreiteten Architekturen zur Bewertung von Paaren, Cross-Encoder und Bi-Encoder, und schlugen dazwischen den Poly-Encoder vor, der schneller als ein Cross-Encoder und genauer als ein Bi-Encoder ist. Nogueira & Cho (2019) setzten BERT als Re-Ranker für Passagen ein. ColBERT (Khattab & Zaharia, 2020) verzögert die Interaktion: Anfrage und Dokumente werden getrennt kodiert und Token für Token verglichen, sodass sich die Dokumentrepräsentationen vorab berechnen lassen; siehe [[semantic-retrieval|Semantisches Retrieval]].

### Wann einsetzen
- Re-Ranking der besten Kandidaten eines Retrievers der ersten Stufe in der Suche und bei [[retrieval-augmented-generation|Retrieval-Augmented Generation]] (Nogueira & Cho, 2019; [[rag-retrieval|RAG: Retrieval]]).
- Wenn Präzision am Anfang der Liste wichtiger ist als Latenz (Humeau et al., 2019).
- Wenn die Retrieval-Domäne von den Trainingsdaten abweicht: Re-Ranking-Modelle verallgemeinerten in BEIR gut auf Daten außerhalb der Trainingsverteilung (Thakur et al., 2021).
- Bewertung einer kleinen Zahl gegebener Satzpaare, etwa ihrer semantischen Ähnlichkeit, einer Satzpaar-Aufgabe, bei der BERT neue Bestwerte erzielte (Reimers & Gurevych, 2019).

### Stärken und Grenzen

**Stärken**
- Höhere Genauigkeit als Bi-Encoder, da Anfrage und Text in jeder Schicht interagieren (Humeau et al., 2019).
- Ein BERT-Re-Ranker übertraf den bisherigen Stand der Technik beim MS-MARCO-Passage-Retrieval um 27 % relativ im MRR@10 (Nogueira & Cho, 2019).
- In BEIR lieferte das Re-Ranking der BM25-Kandidaten mit einem Cross-Encoder (BM25+CE) die besten Zero-Shot-Ergebnisse und schlug BM25 auf 16 von 18 Datensätzen (Thakur et al., 2021).

**Grenzen**
- Ein Modelldurchlauf pro Paar aus Anfrage und Kandidat, nichts lässt sich für die Sammlung vorab berechnen: für die Suche in einer ganzen Sammlung unbrauchbar (Humeau et al., 2019).
- Hoher Rechenaufwand zur Anfragezeit, auch wenn nur neu sortiert wird (Thakur et al., 2021).
- Das Ergebnis ist nur so gut wie die Kandidatenliste: Ein relevantes Dokument, das die erste Stufe verfehlt, wird nie neu bewertet ([[rag-failure-modes|RAG: Fehlermuster]]).
- Die Eingabelänge ist begrenzt; Nogueira & Cho (2019) kürzten Anfrage und Passage auf 512 Tokens.
- Es werden keine eigenständigen Satz-Embeddings berechnet; die Ausgabe lässt sich daher nicht speichern, indexieren oder clustern (Reimers & Gurevych, 2019).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Cross-Encoder | Anfrage und Text gemeinsam, volle Attention über das Paar; genau, langsam (Humeau et al., 2019) | Re-Ranking einer kurzen Kandidatenliste |
| Bi-Encoder (z. B. [[sentence-bert\|Sentence-BERT]]) | Jeder Text einzeln kodiert, Vergleich per Kosinus-Ähnlichkeit; Embeddings lassen sich speichern (Reimers & Gurevych, 2019) | Retrieval in der ersten Stufe, [[clustering\|Clustering]], [[vector-databases\|Vektordatenbanken]] |
| Poly-Encoder | Kandidaten getrennt kodiert, Eingabe durch mehrere Attention-Codes repräsentiert; bei Geschwindigkeit und Genauigkeit zwischen beiden (Humeau et al., 2019) | Bewertung vieler Kandidaten, genauer als ein Bi-Encoder |
| Late Interaction (ColBERT) | Vergleich auf Token-Ebene zwischen getrennt kodierter Anfrage und Dokument; mit BERT-Re-Rankern konkurrenzfähig, zwei Größenordnungen schneller (Khattab & Zaharia, 2020) | Re-Ranking oder Retrieval im großen Maßstab |
| [[bm25\|BM25]] | Lexikalischer Termabgleich, kein Modell (Thakur et al., 2021) | Schnelle erste Stufe |

### In der Praxis
Die übliche Pipeline ist Retrieve-then-Re-rank: eine günstige erste Stufe mit hohem Recall, danach ein Cross-Encoder auf den besten Kandidaten ([[rag-retrieval|RAG: Retrieval]]). Wie viele Kandidaten neu bewertet werden, ist eine Abwägung zwischen Qualität und Latenz, und der Gewinn sollte mit Ranking-Metriken auf der finalen Liste gemessen werden ([[rag-retrieval-evaluation|RAG: Retrieval-Evaluation]]). Cross-Encoder können fehlenden Recall nicht beheben: Fehlen relevante Dokumente in der neu sortierten Liste, muss die erste Stufe geändert werden, etwa durch die Kombination von lexikalischem und Dense Retrieval ([[rag-failure-modes|RAG: Fehlermuster]]). Einen Überblick über Textrepräsentationen gibt [[embeddings|Embeddings]].

### Merksatz
Ein Cross-Encoder liest Anfrage und Text gemeinsam und beurteilt Relevanz daher genauer als der Vergleich getrennter Embeddings; weil er einmal pro Paar laufen muss, sortiert er wenige Kandidaten neu, statt die Sammlung zu durchsuchen.

### Quellen
- Humeau, S., Shuster, K., Lachaux, M.-A. & Weston, J. (2019). *Poly-encoders: Architectures and Pre-training Strategies for Fast and Accurate Multi-sentence Scoring.* ICLR 2020. [arXiv:1905.01969](https://arxiv.org/abs/1905.01969)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
