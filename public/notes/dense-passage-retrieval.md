---
title_en: Dense Passage Retrieval (DPR)
title_de: Dense Passage Retrieval (DPR)
entity_type: Method
aliases:
- Dense passage retrieval
- DPR
- Dense Passage Retriever
sources:
- https://arxiv.org/abs/2004.04906
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Dense Passage Retrieval (DPR) retrieves text passages for a question by comparing dense vectors instead of matching keywords: one BERT encoder embeds the question, a second embeds every passage, and relevance is the dot product of the two vectors (Karpukhin et al., 2020). Trained only on question-passage pairs with in-batch negatives plus one hard BM25 negative, DPR beat a strong BM25 baseline by 9 to 19 percentage points in top-20 retrieval accuracy on open-domain question answering datasets and improved end-to-end answer accuracy (Karpukhin et al., 2020). Its dual-encoder design, contrastive training and FAISS index became the standard recipe for dense retrieval in [[retrieval-augmented-generation|retrieval-augmented generation]].

### How it works

```text
offline: passages (Wikipedia, 100-word blocks, title prepended)
 ▼ passage encoder E_P (BERT-base, [CLS] vector, d = 768)
 ▼ FAISS index over all passage vectors
online: question
 ▼ question encoder E_Q (separate BERT-base)
 ▼ sim(q, p) = E_Q(q)ᵀ E_P(p)  →  top-k passages by maximum inner product
 ▼ reader model extracts the answer span
```

#### 1. Task and passages

Open-domain question answering answers factoid questions from a large corpus in two stages: a retriever selects a small set of passages, then a reader extracts the answer (Karpukhin et al., 2020). DPR splits the English Wikipedia dump of December 2018 into disjoint blocks of 100 words, 21,015,324 passages in total, each prefixed with the article title; fixed-length passages worked better than natural paragraphs, and overlapping passages brought no advantage (Karpukhin et al., 2020). Retrievers are evaluated on top-k accuracy, the share of questions for which one of the k retrieved passages contains the answer. Chunking choices for RAG are covered in [[rag-chunking|RAG chunking]].

#### 2. Dual encoder and similarity

DPR uses two independent BERT-base encoders, one for passages and one for questions, and takes the [CLS] representation as a 768-dimensional vector (Karpukhin et al., 2020). Similarity is the dot product `sim(q, p) = E_Q(q)ᵀ E_P(p)`. More expressive models with cross-attention exist, but the similarity must be decomposable so that all passage vectors can be computed in advance; in ablations, L2 distance performed comparably to the dot product and both beat cosine (Karpukhin et al., 2020). Encoders of this type are called bi-encoders; the contrast with joint encoding is described in [[cross-encoder|cross-encoders]] and [[semantic-retrieval|semantic retrieval]], the underlying model in [[bert|BERT]].

#### 3. Training with in-batch negatives

Training is metric learning: the loss is the negative log-likelihood of the positive passage against n negatives, `L = −log( e^{sim(q,p⁺)} / (e^{sim(q,p⁺)} + Σ_j e^{sim(q,p⁻_j)}) )` (Karpukhin et al., 2020). Negatives can be random passages, top BM25 passages that do not contain the answer, or gold passages of other questions. With in-batch negatives, the B questions and B positive passages of a mini-batch form a B×B similarity matrix, so each question uses the other B−1 positives as negatives at no extra cost. The best model used batch size 128, in-batch negatives and one additional BM25 hard negative per question; adding a second BM25 negative did not help further (Karpukhin et al., 2020).

#### 4. Indexing and search

All passages are encoded offline and indexed with FAISS, "an extremely efficient, open-source library for similarity search and [[clustering|clustering]] of dense vectors" ([[faiss|FAISS]]); at query time only the question is encoded (Karpukhin et al., 2020). With an in-memory FAISS index, DPR processed 995 questions per second returning the top 100 passages, compared with 23.7 questions per second per CPU thread for BM25 in Lucene. Building the index is the expensive part: embedding 21 million passages took about 8.8 hours on 8 GPUs and building the FAISS index another 8.5 hours on one server, against about 30 minutes for a Lucene [[inverted-index|inverted index]] (Karpukhin et al., 2020). Index structures are compared in [[vector-databases|vector databases]].

#### 5. Results

On Natural Questions, DPR reached 78.4% top-20 accuracy against 59.1% for BM25, and 65.2% against 42.9% top-5 accuracy; the end-to-end system reached 41.5% exact-match accuracy against 33.3% for the earlier dense retriever ORQA (Karpukhin et al., 2020). Only 1,000 training examples were enough to outperform BM25. DPR lost on [[squad|SQuAD]], whose questions were written while looking at the passage and therefore share many words with it, which favours BM25. A linear combination of BM25 and DPR scores improved results on some datasets, and DPR trained only on Natural Questions lost 3 to 5 points on other datasets but still clearly beat BM25 (Karpukhin et al., 2020). BM25 remains better at highly selective keywords, DPR at paraphrases and semantic relations, such as matching "bad guy" with "villain".

#### Origin and variants

Before DPR, dense retrieval had only beaten BM25 with ORQA, which needed an expensive inverse cloze pre-training task; DPR showed that fine-tuning BERT on existing question-passage pairs suffices (Karpukhin et al., 2020). The authors released code and models. Later work adds token-level late interaction ([[colbert|ColBERT]]), combines dense and sparse results ([[reciprocal-rank-fusion|reciprocal rank fusion]], [[rag-retrieval|RAG retrieval]]) and tests zero-shot generalisation across domains ([[beir|BEIR]]).

### When to use it

- Retrieval over a fixed corpus where questions are phrased differently from the text, so keyword matching misses relevant passages (Karpukhin et al., 2020).
- Applications with labelled question-passage pairs, even a few thousand, to fine-tune the encoders (Karpukhin et al., 2020).
- As the first stage of a RAG pipeline, followed by a reranker or reader ([[retrieval-augmented-generation|RAG]]).

### Strengths and limitations

**Strengths**
- Matches synonyms and paraphrases that share no tokens with the question (Karpukhin et al., 2020).
- Fast at query time with an approximate nearest neighbour index (Karpukhin et al., 2020).
- Simple training without extra pre-training (Karpukhin et al., 2020).

**Limitations**
- Weaker than BM25 when questions share many words with the text, as on SQuAD (Karpukhin et al., 2020).
- Encoding and indexing a large corpus is far more expensive than building an inverted index (Karpukhin et al., 2020).
- Performance drops when applied to datasets it was not trained on (Karpukhin et al., 2020).

### Comparison

| | [[bm25\|BM25]] | DPR | [[cross-encoder\|Cross-encoder]] |
|---|---|---|---|
| Representation | sparse term weights | dense 768-d vectors | joint encoding of query and passage |
| Precomputable | yes (inverted index) | yes (passage vectors) | no |
| Strength | exact, rare keywords | paraphrases, semantics | most accurate scoring |
| Typical role | first stage | first stage | reranking |

Source: Karpukhin et al. (2020).

### In practice

The quality of a dense retriever depends heavily on the hard negatives used in training (Karpukhin et al., 2020). Many systems run BM25 and dense retrieval in parallel and fuse the results ([[rag-retrieval|RAG retrieval]]). Retrieval quality is measured separately from answer quality ([[rag-retrieval-evaluation|RAG retrieval evaluation]]).

### Key takeaway

DPR encodes questions and passages with two BERT models, ranks passages by dot product, learns from in-batch and BM25 hard negatives and clearly beat BM25 for open-domain question answering, establishing the standard dense retrieval recipe.

### Sources

- Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D. & Yih, W. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Dense Passage Retrieval (DPR) findet Textpassagen zu einer Frage, indem es dichte Vektoren vergleicht statt Schlüsselwörter abzugleichen: Ein BERT-Encoder bettet die Frage ein, ein zweiter jede Passage, und die Relevanz ist das Skalarprodukt der beiden Vektoren (Karpukhin et al., 2020). Nur mit Frage-Passage-Paaren, In-Batch-Negativen und einem schwierigen BM25-Negativbeispiel trainiert, übertraf DPR eine starke BM25-Baseline bei der Top-20-Retrieval-Genauigkeit auf Datensätzen zur Open-Domain-Fragebeantwortung um 9 bis 19 Prozentpunkte und verbesserte die Genauigkeit der Antworten (Karpukhin et al., 2020). Sein Dual-Encoder-Aufbau, das kontrastive Training und der FAISS-Index wurden zum Standardrezept für Dense Retrieval in [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

### Funktionsweise

```text
offline: Passagen (Wikipedia, Blöcke zu 100 Wörtern, Titel vorangestellt)
 ▼ Passagen-Encoder E_P (BERT-base, [CLS]-Vektor, d = 768)
 ▼ FAISS-Index über alle Passagenvektoren
online: Frage
 ▼ Frage-Encoder E_Q (eigenes BERT-base)
 ▼ sim(q, p) = E_Q(q)ᵀ E_P(p)  →  Top-k-Passagen per Maximum Inner Product Search
 ▼ Reader-Modell extrahiert die Antwortspanne
```

#### 1. Aufgabe und Passagen

Open-Domain-Fragebeantwortung beantwortet Faktenfragen aus einem großen Korpus in zwei Stufen: Ein Retriever wählt wenige Passagen aus, dann extrahiert ein Reader die Antwort (Karpukhin et al., 2020). DPR zerlegt den englischen Wikipedia-Dump vom Dezember 2018 in disjunkte Blöcke zu 100 Wörtern, insgesamt 21.015.324 Passagen, jeweils mit vorangestelltem Artikeltitel; Passagen fester Länge funktionierten besser als natürliche Absätze, und überlappende Passagen brachten keinen Vorteil (Karpukhin et al., 2020). Retriever werden über die Top-k-Genauigkeit bewertet, den Anteil der Fragen, bei denen eine der k gefundenen Passagen die Antwort enthält. Chunking-Entscheidungen für RAG behandelt [[rag-chunking|RAG: Chunking]].

#### 2. Dual Encoder und Ähnlichkeit

DPR nutzt zwei unabhängige BERT-base-Encoder, einen für Passagen und einen für Fragen, und verwendet die Repräsentation des [CLS]-Tokens als 768-dimensionalen Vektor (Karpukhin et al., 2020). Die Ähnlichkeit ist das Skalarprodukt `sim(q, p) = E_Q(q)ᵀ E_P(p)`. Ausdrucksstärkere Modelle mit Cross-Attention gibt es, doch die Ähnlichkeit muss zerlegbar sein, damit sich alle Passagenvektoren vorab berechnen lassen; in Ablationen schnitt die L2-Distanz vergleichbar zum Skalarprodukt ab, und beide waren besser als [[text-similarity-metrics|Cosine Similarity]] (Karpukhin et al., 2020). Encoder dieser Art heißen Bi-Encoder; den Unterschied zur gemeinsamen Kodierung beschreiben [[cross-encoder|Cross-Encoder]] und [[semantic-retrieval|Semantisches Retrieval]], das zugrunde liegende Modell [[bert|BERT]].

#### 3. Training mit In-Batch-Negativen

Das Training ist Metric Learning: Der Verlust ist die negative Log-Likelihood der positiven Passage gegenüber n Negativen, `L = −log( e^{sim(q,p⁺)} / (e^{sim(q,p⁺)} + Σ_j e^{sim(q,p⁻_j)}) )` (Karpukhin et al., 2020). Negative können zufällige Passagen sein, Top-Passagen aus BM25, die die Antwort nicht enthalten, oder die korrekten Passagen anderer Fragen. Bei In-Batch-Negativen bilden die B Fragen und B positiven Passagen eines Mini-Batches eine B×B-Ähnlichkeitsmatrix, sodass jede Frage die übrigen B−1 positiven Passagen ohne Zusatzkosten als Negative nutzt. Das beste Modell nutzte eine Batchgröße von 128, In-Batch-Negative und ein zusätzliches schwieriges BM25-Negativ je Frage; ein zweites BM25-Negativ half nicht weiter (Karpukhin et al., 2020).

#### 4. Indexierung und Suche

Alle Passagen werden offline kodiert und mit FAISS indexiert, „an extremely efficient, open-source library for similarity search and [[clustering|clustering]] of dense vectors“ ([[faiss|FAISS]]); zur Anfragezeit wird nur die Frage kodiert (Karpukhin et al., 2020). Mit einem FAISS-Index im Arbeitsspeicher verarbeitete DPR 995 Fragen pro Sekunde mit jeweils den 100 besten Passagen, gegenüber 23,7 Fragen pro Sekunde und CPU-Thread für BM25 in Lucene. Teuer ist der Indexaufbau: Das Einbetten von 21 Millionen Passagen dauerte etwa 8,8 Stunden auf 8 GPUs und der Aufbau des FAISS-Index weitere 8,5 Stunden auf einem Server, gegenüber etwa 30 Minuten für einen Inverted Index in Lucene (Karpukhin et al., 2020). Indexstrukturen vergleicht [[vector-databases|Vektordatenbanken]].

#### 5. Ergebnisse

Auf Natural Questions erreichte DPR 78,4 % Top-20-Genauigkeit gegenüber 59,1 % für BM25 und 65,2 % gegenüber 42,9 % Top-5-Genauigkeit; das Gesamtsystem erreichte 41,5 % Exact Match gegenüber 33,3 % für den früheren Dense Retriever ORQA (Karpukhin et al., 2020). Schon 1.000 Trainingsbeispiele reichten, um BM25 zu übertreffen. Auf [[squad|SQuAD]] unterlag DPR, weil die Fragen mit Blick auf die Passage geschrieben wurden und daher viele Wörter mit ihr teilen, was BM25 begünstigt. Eine Linearkombination der Scores von BM25 und DPR verbesserte die Ergebnisse auf manchen Datensätzen, und ein nur auf Natural Questions trainiertes DPR verlor auf anderen Datensätzen 3 bis 5 Punkte, übertraf BM25 aber weiterhin deutlich (Karpukhin et al., 2020). BM25 bleibt bei sehr selektiven Schlüsselwörtern besser, DPR bei Umschreibungen und semantischen Beziehungen, etwa wenn „bad guy“ zu „villain“ passen muss.

#### Herkunft und Varianten

Vor DPR hatte Dense Retrieval BM25 nur mit ORQA geschlagen, das eine aufwendige Inverse-Cloze-Vortrainingsaufgabe brauchte; DPR zeigte, dass Fine-Tuning von BERT auf vorhandenen Frage-Passage-Paaren genügt (Karpukhin et al., 2020). Die Autorinnen und Autoren veröffentlichten Code und Modelle. Spätere Arbeiten ergänzen Late Interaction auf Token-Ebene ([[colbert|ColBERT]]), kombinieren dichte und spärliche Ergebnisse ([[reciprocal-rank-fusion|Reciprocal Rank Fusion]], [[rag-retrieval|RAG: Retrieval]]) und prüfen die Zero-Shot-Verallgemeinerung über Domänen ([[beir|BEIR]]).

### Wann einsetzen

- Retrieval über einen festen Korpus, bei dem Fragen anders formuliert sind als der Text, sodass Schlüsselwortsuche relevante Passagen verfehlt (Karpukhin et al., 2020).
- Anwendungen mit gelabelten Frage-Passage-Paaren, schon einige Tausend, um die Encoder nachzutrainieren (Karpukhin et al., 2020).
- Als erste Stufe einer RAG-Pipeline, gefolgt von einem Reranker oder Reader ([[retrieval-augmented-generation|RAG]]).

### Stärken und Grenzen

**Stärken**
- Findet Synonyme und Umschreibungen, die keine Token mit der Frage teilen (Karpukhin et al., 2020).
- Schnell zur Anfragezeit mit einem Index für Approximate Nearest Neighbor Search (Karpukhin et al., 2020).
- Einfaches Training ohne zusätzliches Vortraining (Karpukhin et al., 2020).

**Grenzen**
- Schwächer als BM25, wenn Fragen viele Wörter mit dem Text teilen, wie bei SQuAD (Karpukhin et al., 2020).
- Kodieren und Indexieren eines großen Korpus ist weit teurer als der Aufbau eines Inverted Index (Karpukhin et al., 2020).
- Die Leistung sinkt auf Datensätzen, auf denen nicht trainiert wurde (Karpukhin et al., 2020).

### Vergleich

| | [[bm25\|BM25]] | DPR | [[cross-encoder\|Cross-Encoder]] |
|---|---|---|---|
| Repräsentation | spärliche Termgewichte | dichte 768-d-Vektoren | gemeinsame Kodierung von Anfrage und Passage |
| Vorab berechenbar | ja (Inverted Index) | ja (Passagenvektoren) | nein |
| Stärke | exakte, seltene Schlüsselwörter | Umschreibungen, Semantik | genaueste Bewertung |
| Typische Rolle | erste Stufe | erste Stufe | Reranking |

Quelle: Karpukhin et al. (2020).

### In der Praxis

Die Qualität eines Dense Retrievers hängt stark von den schwierigen Negativen im Training ab (Karpukhin et al., 2020). Viele Systeme führen BM25 und Dense Retrieval parallel aus und fusionieren die Ergebnisse ([[rag-retrieval|RAG: Retrieval]]). Die Retrieval-Qualität wird getrennt von der Antwortqualität gemessen ([[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]).

### Merksatz

DPR kodiert Fragen und Passagen mit zwei BERT-Modellen, ordnet Passagen nach Skalarprodukt, lernt aus In-Batch- und schwierigen BM25-Negativen und übertraf BM25 bei der Open-Domain-Fragebeantwortung deutlich; damit setzte es das Standardrezept für Dense Retrieval.

### Quellen

- Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D. & Yih, W. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
