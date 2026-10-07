---
title_en: Information Retrieval
title_de: Information Retrieval
entity_type: Concept
sources:
- https://nlp.stanford.edu/IR-book/
- https://doi.org/10.1561/1500000019
- https://doi.org/10.1145/361219.361220
- https://doi.org/10.1016/0306-4573%2888%2990021-0
- https://arxiv.org/abs/2004.04906
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Information retrieval (IR) finds the documents in a large collection that are relevant to a query and ranks them (Manning et al., 2008). Classical systems use an inverted index and rank documents with term weights such as tf-idf (Salton & Buckley, 1988) or the probabilistic BM25 function (Robertson & Zaragoza, 2009). Dense retrieval compares learned query and passage [[embeddings|Embeddings]] instead and outperformed BM25 on open-domain question answering (Karpukhin et al., 2020). IR is the retrieval step of [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

### How it works

Documents are indexed in advance. At query time, the system looks up candidate documents, scores each by its similarity or estimated relevance to the query, and returns a ranked list, whose quality is measured against relevance judgements.

```text
1. Inverted index
▼
2. Vector space model
▼
3. Term weighting with tf-idf
▼
4. BM25
▼
5. Dense retrieval
▼
6. Evaluation
```

#### 1. Inverted index

An inverted index maps each term to the list of documents that contain it (Manning et al., 2008). To answer a query, the system only reads the lists of the query terms instead of scanning the whole collection. The index supports Boolean retrieval, where documents either match a combination of terms or not, and ranked retrieval, where the matching documents are scored.

#### 2. Vector space model

The vector space model (Salton et al., 1975) represents documents and queries as vectors of term weights in a common space, with one dimension per term. Documents are ranked by their similarity to the query vector; a common measure is the cosine similarity, the cosine of the angle between the two vectors, which does not depend on vector length (Manning et al., 2008).

#### 3. Term weighting with tf-idf

Not all terms are equally informative. Salton & Buckley (1988) systematically compared term-weighting schemes that combine term frequency (how often a term occurs in a document), inverse document frequency (how rare the term is in the collection) and length normalisation. Schemes based on term frequency times inverse document frequency, with normalisation, performed well. As a result, terms that are frequent in a document but rare overall get the highest weights.

#### 4. BM25

BM25 is a ranking function derived from the probabilistic relevance framework (Robertson & Zaragoza, 2009). For each query term it combines three components: inverse document frequency; term-frequency saturation, so that further occurrences of a term add less and less to the score; and document-length normalisation, so that long documents are not favoured just because they contain more words. A common form is

`score(D, Q) = Σ IDF(q) · f(q, D) · (k1 + 1) / (f(q, D) + k1 · (1 − b + b · |D| / avgdl))`

where f(q, D) is the frequency of query term q in document D, |D| the document length and avgdl the average document length. The parameter k1 controls saturation and b the strength of length normalisation (Robertson & Zaragoza, 2009).

#### 5. Dense retrieval

Sparse vector models such as tf-idf and BM25 were the de facto method for passage retrieval in open-domain question answering. Karpukhin et al. (2020) showed that retrieval can be implemented with dense representations alone: a dual encoder learns embeddings of questions and passages from a small number of questions and passages, and passages are retrieved by comparing their embeddings with the question embedding. The dense retriever outperformed a strong Lucene-BM25 system by 9% to 19% absolute in top-20 passage retrieval accuracy and helped the end-to-end system set new state-of-the-art results on several open-domain QA benchmarks ([[semantic-retrieval|Semantic Retrieval]]).

#### 6. Evaluation

Retrieval systems are evaluated against relevance judgements with precision (the share of retrieved documents that are relevant), recall (the share of relevant documents that are retrieved) and measures for ranked lists (Manning et al., 2008). How these measures are applied to RAG retrievers is described in [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]].

#### Origin and variants

The vector space model (Salton et al., 1975) and the comparison of term-weighting schemes (Salton & Buckley, 1988) shaped classical ranked retrieval. BM25 grew out of the probabilistic relevance framework (Robertson & Zaragoza, 2009), and dense passage retrieval (Karpukhin et al., 2020) replaced sparse term vectors with learned embeddings. Manning et al. (2008) give a textbook overview of the classical methods.

### When to use it

- When a query has to be answered from a large document collection, an inverted index avoids scanning all documents (Manning et al., 2008).
- When exact terms matter, such as names, identifiers or legal citations, lexical ranking with BM25 matches them directly (Robertson & Zaragoza, 2009).
- When queries and relevant passages use different wording, as is common in question answering, dense retrieval tends to find more relevant passages (Karpukhin et al., 2020).

### Strengths and limitations

**Strengths**
- The inverted index makes lookup efficient without scanning the collection (Manning et al., 2008).
- BM25 needs no training data and accounts for term-frequency saturation and document length (Robertson & Zaragoza, 2009).
- Dense retrieval outperformed BM25 by 9% to 19% absolute in top-20 accuracy on open-domain QA (Karpukhin et al., 2020).

**Limitations**
- Term-based models only match the words that occur in the query; different wording for the same meaning is not matched (Salton et al., 1975).
- Dense retrievers need training data of questions and passages (Karpukhin et al., 2020).
- Ranking quality depends on weighting choices that have to be compared empirically (Salton & Buckley, 1988).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Boolean retrieval | Documents match a combination of terms or not; no ranking (Manning et al., 2008) | Precise filtering, for example in legal or patent search |
| Vector space model with tf-idf | Ranking by similarity of term-weight vectors (Salton et al., 1975; Salton & Buckley, 1988) | Ranked keyword search |
| BM25 | Probabilistic ranking with term-frequency saturation and length normalisation (Robertson & Zaragoza, 2009) | Strong lexical baseline without training |
| Dense passage retrieval | Learned question and passage embeddings (Karpukhin et al., 2020) | Questions phrased differently from the text |

### In practice

BM25 is a strong baseline that should be measured before more complex methods are introduced, since it requires no training (Robertson & Zaragoza, 2009). Lexical and dense retrieval are often combined, because they fail in different situations ([[rag-retrieval|RAG: Retrieval]]). Retrieval quality is measured on a set of queries with relevance judgements from the target domain (Manning et al., 2008; [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]).

### Key takeaway

Information retrieval ranks documents for a query, classically with an inverted index and term weights such as tf-idf or BM25, and increasingly with learned dense embeddings, which match meaning rather than exact words.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Salton, G., Wong, A. & Yang, C. S. (1975). *A Vector Space Model for Automatic Indexing.* Communications of the ACM 18(11). [doi:10.1145/361219.361220](https://doi.org/10.1145/361219.361220)
- Salton, G. & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval.* Information Processing & Management 24(5). [doi:10.1016/0306-4573(88)90021-0](https://doi.org/10.1016/0306-4573%2888%2990021-0)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Information Retrieval (IR) findet die Dokumente einer großen Sammlung, die für eine Anfrage relevant sind, und bringt sie in eine Rangfolge (Manning et al., 2008). Klassische Systeme nutzen einen invertierten Index und ranken Dokumente mit Termgewichten wie tf-idf (Salton & Buckley, 1988) oder mit der probabilistischen Funktion BM25 (Robertson & Zaragoza, 2009). Dense Retrieval vergleicht stattdessen gelernte [[embeddings|Embeddings]] von Anfrage und Passage und übertraf BM25 bei Open-Domain-Fragebeantwortung (Karpukhin et al., 2020). IR ist der Retrieval-Schritt von [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

### Funktionsweise

Dokumente werden vorab indexiert. Zur Anfragezeit sucht das System Kandidatendokumente heraus, bewertet jedes nach Ähnlichkeit oder geschätzter Relevanz zur Anfrage und liefert eine Rangliste, deren Qualität an Relevanzurteilen gemessen wird.

```text
1. Invertierter Index
▼
2. Vektorraummodell
▼
3. Termgewichtung mit tf-idf
▼
4. BM25
▼
5. Dense Retrieval
▼
6. Evaluation
```

#### 1. Invertierter Index

Ein invertierter Index ordnet jedem Term die Liste der Dokumente zu, die ihn enthalten (Manning et al., 2008). Um eine Anfrage zu beantworten, liest das System nur die Listen der Anfrageterme, statt die ganze Sammlung zu durchsuchen. Der Index unterstützt boolesches Retrieval, bei dem Dokumente eine Termkombination erfüllen oder nicht, und Ranked Retrieval, bei dem die gefundenen Dokumente bewertet werden.

#### 2. Vektorraummodell

Das Vektorraummodell (Salton et al., 1975) stellt Dokumente und Anfragen als Vektoren von Termgewichten in einem gemeinsamen Raum dar, mit einer Dimension je Term. Dokumente werden nach ihrer Ähnlichkeit zum Anfragevektor gerankt; ein gängiges Maß ist die Kosinusähnlichkeit, der Kosinus des Winkels zwischen den beiden Vektoren, der nicht von der Vektorlänge abhängt (Manning et al., 2008).

#### 3. Termgewichtung mit tf-idf

Nicht alle Terme sind gleich aussagekräftig. Salton & Buckley (1988) verglichen systematisch Gewichtungsschemata, die Termhäufigkeit (wie oft ein Term in einem Dokument vorkommt), inverse Dokumenthäufigkeit (wie selten der Term in der Sammlung ist) und Längennormalisierung kombinieren. Schemata auf Basis von Termhäufigkeit mal inverser Dokumenthäufigkeit mit Normalisierung schnitten gut ab. Die höchsten Gewichte erhalten damit Terme, die in einem Dokument häufig, in der Sammlung insgesamt aber selten sind.

#### 4. BM25

BM25 ist eine Ranking-Funktion, die aus dem probabilistischen Relevanzmodell abgeleitet ist (Robertson & Zaragoza, 2009). Für jeden Anfrageterm kombiniert sie drei Komponenten: die inverse Dokumenthäufigkeit; eine Sättigung der Termhäufigkeit, sodass weitere Vorkommen eines Terms immer weniger zum Wert beitragen; und eine Normalisierung der Dokumentlänge, damit lange Dokumente nicht allein deshalb bevorzugt werden, weil sie mehr Wörter enthalten. Eine gängige Form ist

`score(D, Q) = Σ IDF(q) · f(q, D) · (k1 + 1) / (f(q, D) + k1 · (1 − b + b · |D| / avgdl))`

Dabei ist f(q, D) die Häufigkeit des Anfrageterms q im Dokument D, |D| die Dokumentlänge und avgdl die durchschnittliche Dokumentlänge. Der Parameter k1 steuert die Sättigung, b die Stärke der Längennormalisierung (Robertson & Zaragoza, 2009).

#### 5. Dense Retrieval

Dünnbesetzte (sparse) Vektormodelle wie tf-idf und BM25 waren die übliche Methode für das Passage-Retrieval bei Open-Domain-Fragebeantwortung. Karpukhin et al. (2020) zeigten, dass sich Retrieval allein mit dichten Repräsentationen umsetzen lässt: Ein Dual Encoder lernt aus einer kleinen Zahl von Fragen und Passagen Embeddings für beide, und Passagen werden abgerufen, indem ihre Embeddings mit dem Embedding der Frage verglichen werden. Der Dense Retriever übertraf ein starkes Lucene-BM25-System bei der Top-20-Genauigkeit des Passage-Retrievals um 9 bis 19 Prozentpunkte und verhalf dem Gesamtsystem zu neuen Bestwerten auf mehreren Open-Domain-QA-Benchmarks ([[semantic-retrieval|Semantisches Retrieval]]).

#### 6. Evaluation

Retrieval-Systeme werden gegen Relevanzurteile mit Precision (Anteil der gefundenen Dokumente, die relevant sind), Recall (Anteil der relevanten Dokumente, die gefunden werden) und Maßen für Ranglisten evaluiert (Manning et al., 2008). Wie diese Maße auf RAG-Retriever angewendet werden, beschreibt [[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]].

#### Ursprung und Varianten

Das Vektorraummodell (Salton et al., 1975) und der Vergleich von Termgewichtungsschemata (Salton & Buckley, 1988) prägten das klassische Ranked Retrieval. BM25 entstand aus dem probabilistischen Relevanzmodell (Robertson & Zaragoza, 2009), und Dense Passage Retrieval (Karpukhin et al., 2020) ersetzte dünnbesetzte Termvektoren durch gelernte Embeddings. Manning et al. (2008) geben einen Lehrbuchüberblick über die klassischen Verfahren.

### Wann einsetzen

- Wenn eine Anfrage aus einer großen Dokumentsammlung beantwortet werden muss, erspart ein invertierter Index das Durchsuchen aller Dokumente (Manning et al., 2008).
- Wenn es auf exakte Begriffe ankommt, etwa Namen, Kennungen oder juristische Zitate, trifft lexikalisches Ranking mit BM25 diese direkt (Robertson & Zaragoza, 2009).
- Wenn Anfragen und relevante Passagen unterschiedlich formuliert sind, wie bei der Fragebeantwortung üblich, findet Dense Retrieval tendenziell mehr relevante Passagen (Karpukhin et al., 2020).

### Stärken und Grenzen

**Stärken**
- Der invertierte Index macht die Suche effizient, ohne die Sammlung zu durchlaufen (Manning et al., 2008).
- BM25 braucht keine Trainingsdaten und berücksichtigt Sättigung der Termhäufigkeit und Dokumentlänge (Robertson & Zaragoza, 2009).
- Dense Retrieval übertraf BM25 bei Open-Domain-QA um 9 bis 19 Prozentpunkte in der Top-20-Genauigkeit (Karpukhin et al., 2020).

**Einschränkungen**
- Termbasierte Modelle treffen nur die Wörter, die in der Anfrage vorkommen; andere Formulierungen derselben Bedeutung werden nicht gefunden (Salton et al., 1975).
- Dense Retriever brauchen Trainingsdaten aus Fragen und Passagen (Karpukhin et al., 2020).
- Die Ranking-Qualität hängt von Gewichtungsentscheidungen ab, die empirisch verglichen werden müssen (Salton & Buckley, 1988).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Boolesches Retrieval | Dokumente erfüllen eine Termkombination oder nicht; keine Rangfolge (Manning et al., 2008) | Präzises Filtern, etwa in juristischer oder Patentrecherche |
| Vektorraummodell mit tf-idf | Ranking nach Ähnlichkeit von Termgewichtsvektoren (Salton et al., 1975; Salton & Buckley, 1988) | Gerankte Stichwortsuche |
| BM25 | Probabilistisches Ranking mit Sättigung der Termhäufigkeit und Längennormalisierung (Robertson & Zaragoza, 2009) | Starke lexikalische Baseline ohne Training |
| Dense Passage Retrieval | Gelernte Embeddings für Fragen und Passagen (Karpukhin et al., 2020) | Fragen, die anders formuliert sind als der Text |

### In der Praxis

BM25 ist eine starke Baseline, die gemessen werden sollte, bevor aufwendigere Verfahren eingeführt werden, da sie kein Training erfordert (Robertson & Zaragoza, 2009). Lexikalisches und Dense Retrieval werden oft kombiniert, weil sie in unterschiedlichen Situationen versagen ([[rag-retrieval|RAG: Retrieval]]). Die Retrieval-Qualität wird an einer Menge von Anfragen mit Relevanzurteilen aus der Zieldomäne gemessen (Manning et al., 2008; [[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]).

### Merksatz

Information Retrieval bringt Dokumente für eine Anfrage in eine Rangfolge, klassisch mit invertiertem Index und Termgewichten wie tf-idf oder BM25, zunehmend mit gelernten dichten Embeddings, die Bedeutung statt exakter Wörter vergleichen.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Salton, G., Wong, A. & Yang, C. S. (1975). *A Vector Space Model for Automatic Indexing.* Communications of the ACM 18(11). [doi:10.1145/361219.361220](https://doi.org/10.1145/361219.361220)
- Salton, G. & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval.* Information Processing & Management 24(5). [doi:10.1016/0306-4573(88)90021-0](https://doi.org/10.1016/0306-4573%2888%2990021-0)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
