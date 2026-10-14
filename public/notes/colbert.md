---
title_en: ColBERT (Late Interaction Retrieval)
title_de: ColBERT (Late-Interaction-Retrieval)
entity_type: Method
aliases:
- ColBERT
- ColBERTv2
- Late interaction
- Late Interaction
sources:
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/2112.01488
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

ColBERT is a neural retrieval and ranking model that encodes the query and each document separately with [[bert|BERT]] into one vector per token and then scores them with a cheap "late interaction": for every query token it takes the maximum similarity to any document token and sums these maxima (Khattab & Zaharia, 2020). Because document vectors can be computed offline, ColBERT reached the effectiveness of BERT re-rankers on MS MARCO while running two orders of magnitude faster and using four orders of magnitude fewer FLOPs per query, and it can retrieve directly from millions of documents through a vector index (Khattab & Zaharia, 2020). ColBERTv2 reduces the large storage cost of token-level vectors by 6 to 10 times with residual compression (Santhanam et al., 2022).

### How it works

```text
offline: document → BERT("[D] d1 … dn") → linear layer → normalise → drop punctuation
         → bag of m-dimensional token vectors per document (m = 128), stored / indexed
online:  query → BERT("[Q] q1 … ql [mask] … [mask]")  (padded to Nq = 32) → token vectors
 ▼
late interaction: S(q, d) = Σ_i max_j  E_q,i · E_d,j        (MaxSim per query token, summed)
 ▼
re-rank a candidate list, or retrieve end to end via a FAISS index over all token vectors
```

#### 1. The efficiency problem of BERT rankers

Fine-tuned BERT rankers that feed every query-document pair through the network are very effective but expensive: re-ranking the top 1,000 [[bm25|BM25]] results per MS MARCO query with BERT-base took about 10.7 seconds and 97 trillion FLOPs (Khattab & Zaharia, 2020). Representation-based models encode query and document independently and are fast, but compress each text into a single vector. ColBERT sits between these extremes: independent encoding like a bi-encoder, fine-grained matching like a [[cross-encoder|cross-encoder]] (Khattab & Zaharia, 2020).

#### 2. Query and document encoders

One shared BERT model serves both sides; a special token [Q] or [D] after [CLS] marks queries and documents (Khattab & Zaharia, 2020). Queries are padded with BERT's [mask] tokens to a fixed length Nq of 32; this "query augmentation" lets BERT produce extra query [[embeddings|embeddings]] at the mask positions, a soft way of expanding the query with new terms or re-weighting existing ones, and it proved essential for effectiveness. A linear layer reduces each token vector to m dimensions (128 in the experiments), and vectors are normalised so that the dot product equals [[text-similarity-metrics|cosine similarity]]. Document embeddings for punctuation are filtered out to save space (Khattab & Zaharia, 2020).

#### 3. Late interaction (MaxSim)

The relevance score is `S(q,d) = Σ_i max_j E_q,i · E_d,j`: each query token finds its best-matching document token, and the maxima are summed (Khattab & Zaharia, 2020). The interaction step has no trainable parameters; the encoders are fine-tuned with a pairwise softmax cross-entropy loss on triples of query, positive and negative document. Compared with a single-vector [[dense-passage-retrieval|DPR]]-style retriever, the model keeps token-level matching; compared with a cross-encoder, BERT only processes the short query at query time (Khattab & Zaharia, 2020).

#### 4. Re-ranking and end-to-end retrieval

For re-ranking, the pre-computed document matrices of the k candidates are loaded to the GPU and scored in one batched operation; the cost is dominated by gathering and transferring the embeddings (Khattab & Zaharia, 2020). For end-to-end retrieval from a large collection, all document token vectors are put into a [[faiss|FAISS]] IVFPQ index (k-means partitions plus product quantisation); each of the Nq query vectors retrieves its nearest document tokens, the corresponding documents form a candidate set, and these are then scored exactly with MaxSim (Khattab & Zaharia, 2020). Index structures are explained in [[vector-databases|vector databases]].

#### 5. Results

On MS MARCO passage ranking, ColBERT re-ranking reached an [[rag-retrieval-evaluation|MRR]]@10 of 34.9 with 61 ms re-ranking latency, against 36.0 for a BERT-base re-ranker at 10,700 ms, and over 170 times speed-up overall (Khattab & Zaharia, 2020). End-to-end retrieval over 8.8 million passages reached MRR@10 36.0 and [[classification-metrics|Recall]]@1000 of 96.8%, against 18.7 MRR@10 and 85.7% recall for BM25 in Anserini, at 458 ms latency. Storage is the main cost: 286 GiB for 128-dimensional 32-bit vectors in the re-ranking setting, reducible to 27 GiB with 24-dimensional 16-bit vectors at a small loss in MRR@10 (Khattab & Zaharia, 2020).

#### Origin and variants

Omar Khattab and Matei Zaharia of Stanford presented ColBERT at SIGIR 2020 (Khattab & Zaharia, 2020). ColBERTv2 combines aggressive residual compression with denoised supervision, cutting the space footprint of late interaction by 6 to 10 times while reaching state-of-the-art quality both within and outside the training domain (Santhanam et al., 2022). ColBERT is evaluated on [[ms-marco|MS MARCO]] and, for zero-shot transfer, on [[beir|BEIR]].

### When to use it

- Retrieval or re-ranking that needs close to cross-encoder quality at much lower latency (Khattab & Zaharia, 2020).
- When storage for token-level vectors is affordable, or compressed as in ColBERTv2 (Santhanam et al., 2022).

### Strengths and limitations

**Strengths**
- Token-level matching with precomputed document representations (Khattab & Zaharia, 2020).
- Usable both as re-ranker and as end-to-end retriever (Khattab & Zaharia, 2020).
- Much higher recall than BM25 in end-to-end retrieval on MS MARCO (Khattab & Zaharia, 2020).

**Limitations**
- One vector per token makes the index roughly an order of magnitude larger than single-vector indexes (Santhanam et al., 2022).
- End-to-end retrieval needs a two-stage search over token vectors, with higher latency than BM25 (Khattab & Zaharia, 2020).
- Slightly below the best BERT re-rankers in MRR@10 (Khattab & Zaharia, 2020).

### Comparison

| | [[dense-passage-retrieval\|Bi-encoder (DPR)]] | ColBERT | [[cross-encoder\|Cross-encoder]] |
|---|---|---|---|
| Vectors per text | one | one per token | none (joint scoring) |
| Interaction | dot product of two vectors | sum of MaxSim over tokens | full attention over the pair |
| Documents precomputable | yes | yes | no |
| Cost driver | index size small | index size large | compute per pair |

Sources: Khattab & Zaharia (2020); Santhanam et al. (2022).

### In practice

ColBERT is used as a re-ranking stage after BM25 or a dense retriever, or as the first stage when its index fits in memory ([[rag-retrieval|RAG retrieval]]). The embedding dimension and bytes per dimension trade storage against quality (Khattab & Zaharia, 2020). The general concepts of dense retrieval are covered in [[semantic-retrieval|semantic retrieval]].

### Key takeaway

ColBERT keeps one vector per token, precomputes documents and scores with a sum of per-token maximum similarities, which brings ranking quality close to BERT cross-encoders at a fraction of the cost, paid for with large indexes that ColBERTv2 compresses.

### Sources

- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Santhanam, K., Khattab, O., Saad-Falcon, J., Potts, C. & Zaharia, M. (2022). *ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction.* NAACL 2022. [arXiv:2112.01488](https://arxiv.org/abs/2112.01488)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

ColBERT ist ein neuronales Modell für Retrieval und Ranking, das Anfrage und jedes Dokument getrennt mit [[bert|BERT]] in je einen Vektor pro Token kodiert und sie dann mit einer günstigen „Late Interaction“ bewertet: Für jedes Anfrage-Token nimmt es die maximale Ähnlichkeit zu einem Dokument-Token und summiert diese Maxima (Khattab & Zaharia, 2020). Weil sich Dokumentvektoren offline berechnen lassen, erreichte ColBERT auf MS MARCO die Wirksamkeit von BERT-Re-Rankern, lief dabei zwei Größenordnungen schneller und brauchte vier Größenordnungen weniger FLOPs pro Anfrage, und es kann über einen Vektorindex direkt aus Millionen Dokumenten abrufen (Khattab & Zaharia, 2020). ColBERTv2 verringert den großen Speicherbedarf der Token-Vektoren mit Residual Compression um das 6- bis 10-Fache (Santhanam et al., 2022).

### Funktionsweise

```text
offline: Dokument → BERT("[D] d1 … dn") → lineare Schicht → normalisieren → Satzzeichen entfernen
         → Menge m-dimensionaler Token-Vektoren je Dokument (m = 128), gespeichert / indexiert
online:  Anfrage → BERT("[Q] q1 … ql [mask] … [mask]")  (auf Nq = 32 aufgefüllt) → Token-Vektoren
 ▼
Late Interaction: S(q, d) = Σ_i max_j  E_q,i · E_d,j        (MaxSim je Anfrage-Token, summiert)
 ▼
Kandidatenliste neu ordnen oder Ende-zu-Ende über einen FAISS-Index aller Token-Vektoren abrufen
```

#### 1. Das Effizienzproblem von BERT-Rankern

Feinjustierte BERT-Ranker, die jedes Paar aus Anfrage und Dokument durch das Netz schicken, sind sehr wirksam, aber teuer: Das Neuordnen der 1.000 besten BM25-Ergebnisse je MS-MARCO-Anfrage mit BERT-base dauerte etwa 10,7 Sekunden und kostete 97 Billionen FLOPs (Khattab & Zaharia, 2020). Repräsentationsbasierte Modelle kodieren Anfrage und Dokument unabhängig und sind schnell, pressen aber jeden Text in einen einzigen Vektor. ColBERT liegt dazwischen: unabhängige Kodierung wie ein Bi-Encoder, feingranularer Abgleich wie ein [[cross-encoder|Cross-Encoder]] (Khattab & Zaharia, 2020).

#### 2. Encoder für Anfragen und Dokumente

Ein gemeinsames BERT-Modell dient beiden Seiten; ein besonderes Token [Q] oder [D] nach [CLS] kennzeichnet Anfragen und Dokumente (Khattab & Zaharia, 2020). Anfragen werden mit BERTs [mask]-Token auf eine feste Länge Nq von 32 aufgefüllt; diese „Query Augmentation“ lässt BERT an den Maskenpositionen zusätzliche Anfrage-Embeddings erzeugen, eine weiche Form, die Anfrage um neue Terme zu erweitern oder vorhandene neu zu gewichten, und sie erwies sich als entscheidend für die Wirksamkeit. Eine lineare Schicht reduziert jeden Token-Vektor auf m Dimensionen (128 in den Experimenten), und die Vektoren werden normalisiert, sodass das Skalarprodukt der [[text-similarity-metrics|Cosine Similarity]] entspricht. [[embeddings|Embeddings]] von Satzzeichen in Dokumenten werden herausgefiltert, um Platz zu sparen (Khattab & Zaharia, 2020).

#### 3. Late Interaction (MaxSim)

Der Relevanzwert lautet `S(q,d) = Σ_i max_j E_q,i · E_d,j`: Jedes Anfrage-Token sucht sein am besten passendes Dokument-Token, und die Maxima werden summiert (Khattab & Zaharia, 2020). Der Interaktionsschritt hat keine trainierbaren Parameter; die Encoder werden mit einem paarweisen Softmax-Cross-Entropy-Verlust auf Tripeln aus Anfrage, positivem und negativem Dokument feinjustiert. Gegenüber einem Retriever mit einem Vektor je Text wie [[dense-passage-retrieval|DPR]] bleibt der Abgleich auf Token-Ebene erhalten; gegenüber einem Cross-Encoder verarbeitet BERT zur Anfragezeit nur die kurze Anfrage (Khattab & Zaharia, 2020).

#### 4. Re-Ranking und Ende-zu-Ende-Retrieval

Beim Re-Ranking werden die vorberechneten Dokumentmatrizen der k Kandidaten auf die GPU geladen und in einer gebündelten Operation bewertet; die Kosten bestimmen das Sammeln und Übertragen der Embeddings (Khattab & Zaharia, 2020). Für Ende-zu-Ende-Retrieval aus einer großen Sammlung kommen alle Token-Vektoren der Dokumente in einen [[faiss|FAISS]]-Index vom Typ IVFPQ (k-Means-Partitionen plus Product Quantization); jeder der Nq Anfragevektoren ruft seine nächsten Dokument-Token ab, die zugehörigen Dokumente bilden eine Kandidatenmenge, und diese wird dann exakt mit MaxSim bewertet (Khattab & Zaharia, 2020). Indexstrukturen erklärt [[vector-databases|Vektordatenbanken]].

#### 5. Ergebnisse

Beim Passage Ranking auf MS MARCO erreichte ColBERT im Re-Ranking einen [[rag-retrieval-evaluation|MRR]]@10 von 34,9 bei 61 ms Latenz für das Re-Ranking, gegenüber 36,0 für einen BERT-base-Re-Ranker bei 10.700 ms, insgesamt über 170-mal schneller (Khattab & Zaharia, 2020). Ende-zu-Ende-Retrieval über 8,8 Millionen Passagen erreichte MRR@10 36,0 und [[classification-metrics|Recall]]@1000 von 96,8 %, gegenüber 18,7 MRR@10 und 85,7 % Recall für [[bm25|BM25]] in Anserini, bei 458 ms Latenz. Der Speicher ist der Hauptkostenfaktor: 286 GiB für 128-dimensionale 32-Bit-Vektoren im Re-Ranking, reduzierbar auf 27 GiB mit 24-dimensionalen 16-Bit-Vektoren bei geringem Verlust im MRR@10 (Khattab & Zaharia, 2020).

#### Herkunft und Varianten

Omar Khattab und Matei Zaharia von der Stanford University stellten ColBERT auf der SIGIR 2020 vor (Khattab & Zaharia, 2020). ColBERTv2 verbindet aggressive Residual Compression mit entrauschter Supervision, verringert den Speicherbedarf von Late Interaction um das 6- bis 10-Fache und erreicht Bestwerte innerhalb und außerhalb der Trainingsdomäne (Santhanam et al., 2022). ColBERT wird auf [[ms-marco|MS MARCO]] und für Zero-Shot-Übertragung auf [[beir|BEIR]] evaluiert.

### Wann einsetzen

- Retrieval oder Re-Ranking, das nahezu die Qualität eines Cross-Encoders bei deutlich geringerer Latenz braucht (Khattab & Zaharia, 2020).
- Wenn Speicher für Token-Vektoren bezahlbar ist oder komprimiert wird wie in ColBERTv2 (Santhanam et al., 2022).

### Stärken und Grenzen

**Stärken**
- Abgleich auf Token-Ebene mit vorberechneten Dokumentrepräsentationen (Khattab & Zaharia, 2020).
- Als Re-Ranker und als Ende-zu-Ende-Retriever nutzbar (Khattab & Zaharia, 2020).
- Deutlich höherer Recall als BM25 im Ende-zu-Ende-Retrieval auf MS MARCO (Khattab & Zaharia, 2020).

**Grenzen**
- Ein Vektor je Token macht den Index etwa eine Größenordnung größer als Indizes mit einem Vektor je Text (Santhanam et al., 2022).
- Ende-zu-Ende-Retrieval braucht eine zweistufige Suche über Token-Vektoren, mit höherer Latenz als BM25 (Khattab & Zaharia, 2020).
- Im MRR@10 leicht unter den besten BERT-Re-Rankern (Khattab & Zaharia, 2020).

### Vergleich

| | [[dense-passage-retrieval\|Bi-Encoder (DPR)]] | ColBERT | [[cross-encoder\|Cross-Encoder]] |
|---|---|---|---|
| Vektoren je Text | einer | einer je Token | keine (gemeinsame Bewertung) |
| Interaktion | Skalarprodukt zweier Vektoren | Summe der MaxSim über Token | volle Attention über das Paar |
| Dokumente vorab berechenbar | ja | ja | nein |
| Kostentreiber | kleiner Index | großer Index | Rechenaufwand je Paar |

Quellen: Khattab & Zaharia (2020); Santhanam et al. (2022).

### In der Praxis

ColBERT dient als Re-Ranking-Stufe nach BM25 oder einem Dense Retriever oder als erste Stufe, wenn sein Index in den Speicher passt ([[rag-retrieval|RAG: Retrieval]]). Embedding-Dimension und Bytes je Dimension wägen Speicher gegen Qualität ab (Khattab & Zaharia, 2020). Die allgemeinen Konzepte des Dense Retrieval behandelt [[semantic-retrieval|Semantisches Retrieval]].

### Merksatz

ColBERT behält einen Vektor je Token, berechnet Dokumente vorab und bewertet mit einer Summe der maximalen Ähnlichkeiten je Token; das bringt die Ranking-Qualität nahe an BERT-Cross-Encoder bei einem Bruchteil der Kosten, bezahlt mit großen Indizes, die ColBERTv2 komprimiert.

### Quellen

- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Santhanam, K., Khattab, O., Saad-Falcon, J., Potts, C. & Zaharia, M. (2022). *ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction.* NAACL 2022. [arXiv:2112.01488](https://arxiv.org/abs/2112.01488)
