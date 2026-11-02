---
title_en: TF-IDF
title_de: TF-IDF
entity_type: Method
aliases:
- tf-idf
- Tf-idf
- tf–idf
- Term frequency–inverse document frequency
- Inverse document frequency
- IDF
sources:
- https://web.stanford.edu/~jurafsky/slp3/11.pdf
- https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html
- https://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html
- https://scikit-learn.org/stable/modules/feature_extraction.html
- https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

TF-IDF (term frequency–inverse document frequency) weights a word in a document by how often it occurs there (term frequency) and how rare it is across the collection (inverse document frequency), so that words which occur often in few documents get high weights and words that occur everywhere get weights near zero (Manning et al., 2008). Documents and queries become sparse vectors with one dimension per vocabulary word, and the classic vector space model ranks documents by the [[cosine-similarity|cosine]] between the tf-idf vectors of query and document (Jurafsky & Martin, 2026). TF-IDF is also a standard feature weighting for text [[classification|classification]] and [[clustering|clustering]] (scikit-learn), and [[bm25|BM25]] is a variant of it.

### How it works

```text
documents ──► tokenise ──► count(t, d)  ──► tf(t, d)   = 1 + log10 count(t, d)   (0 if count is 0)
                     └──► df(t)         ──► idf(t)     = log10(N / df(t))
                                             ▼
                              weight(t, d) = tf(t, d) · idf(t)
                                             ▼
                     document vector (|V| dimensions, mostly zeros) ──► normalise to length 1
                                             ▼
          query vector (same weighting) ──► score(q, d) = cos(q, d) ──► ranked list
```

#### 1. Term frequency

Raw counts overstate repetition: a word that appears 100 times is not 100 times more indicative of the document's content (Jurafsky & Martin, 2026). The usual sublinear scaling uses `tf(t,d) = 1 + log10 count(t,d)` for counts above zero and 0 otherwise, which gives 1 for one occurrence, 2 for ten and 3 for a hundred (Jurafsky & Martin, 2026; Manning et al., 2008). Maximum tf normalisation divides by the largest term frequency in the document instead, which counters the higher frequencies in long documents but is unstable when the stop word list changes or a single outlier term dominates (Manning et al., 2008).

#### 2. Inverse document frequency

The document frequency `df(t)` is the number of documents that contain t; the inverse document frequency, which goes back to Spärck Jones (1972), is `idf(t) = log10(N / df(t))` for a collection of N documents (Jurafsky & Martin, 2026). Document frequency is preferred to collection frequency (the total number of occurrences), because it is a document-level statistic and better separates documents: in the Reuters collection, *try* and *insurance* occur about equally often overall but in very different numbers of documents (Manning et al., 2008). A word that occurs in every document gets idf 0, which acts like a soft stop word list; in Jurafsky and Martin's Shakespeare example, *Romeo* (one play) has idf 1.57, while *good* and *sweet* (all 37 plays) have 0 (Jurafsky & Martin, 2026). The base of the logarithm does not change the ranking (Manning et al., 2008).

#### 3. Combining and normalising

The weight of term t in document d is the product `tf-idf(t,d) = tf(t,d) · idf(t)`. It is highest when t occurs many times in few documents, lower when it occurs less often or in many documents, and lowest when it occurs in almost all documents (Manning et al., 2008). Each document is then a vector over the whole vocabulary, almost all of whose entries are zero; normalising it to unit length removes the advantage of long documents (Manning et al., 2008; [[inverted-index|inverted index]]).

#### 4. Scoring queries

The query is treated as a very short document and weighted the same way; the score of a document is the cosine between query and document vector, a sum over the terms they share (Manning et al., 2008). In Jurafsky and Martin's example, for the query *sweet love*, the document "Sweet sweet nurse! Love?" scores 0.747 and "Sweet sorrow" 0.0779, because the first contains both terms (Jurafsky & Martin, 2026). Many variants exist and are written in SMART notation `ddd.qqq` (term frequency, document frequency and normalisation component for document and query); a standard scheme is `lnc.ltc`, with log tf and cosine normalisation on both sides but idf only on the query (Manning et al., 2008). Dropping the idf for the document sometimes improves results (Jurafsky & Martin, 2026).

#### 5. Library defaults

Implementations differ from the textbook formula. scikit-learn's `TfidfTransformer` and `TfidfVectorizer` use raw counts as tf by default, compute `idf(t) = log((1 + n) / (1 + df(t))) + 1` with `smooth_idf=True` (as if one extra document contained every term once, which prevents division by zero) and `log(n / df(t)) + 1` without smoothing, and normalise each row with the L2 norm; `sublinear_tf=True` replaces tf with `1 + log(tf)` (scikit-learn API reference). Because of the "+1", terms that occur in every document are not ignored entirely (scikit-learn). Weights from different libraries are therefore not directly comparable.

#### Origin and variants

The idf weight was introduced by Spärck Jones in 1972 (Jurafsky & Martin, 2026); the SMART notation for weighting variants is named after an early text retrieval system (Manning et al., 2008). [[bm25|BM25]] is a tf-idf variant with a saturating term frequency (parameter k) and document length normalisation (parameter b) (Jurafsky & Martin, 2026). Pivoted document length normalisation corrects cosine normalisation's bias against long documents (Manning et al., 2008).

### When to use it

- Keyword search over a document collection, for a baseline or the lexical side of hybrid retrieval ([[information-retrieval|information retrieval]], [[rag-retrieval|RAG retrieval]]).
- Features for text classification and clustering, for example with [[naive-bayes|Naive Bayes]], logistic regression or k-means (scikit-learn; [[classification|classification]]).
- Finding characteristic words of a document or of a group of documents.
- Input to dimensionality reduction such as [[latent-semantic-indexing|latent semantic indexing]].

### Strengths and limitations

**Strengths**
- Needs no training, only counts over the collection, and is fast with an inverted index (Manning et al., 2008).
- Easy to interpret: each dimension is a word with a visible weight.
- Down-weights uninformative frequent words without a hand-made stop word list (Jurafsky & Martin, 2026).

**Limitations**
- Bag of words: word order is lost, so "Mary is quicker than John" and "John is quicker than Mary" get the same vector (Manning et al., 2008).
- Matches only exact terms; synonyms and paraphrases are missed, which dense [[embeddings|embeddings]] address ([[semantic-retrieval|semantic retrieval]]).
- Term frequency grows without bound and length normalisation is crude; BM25 handles both better (Jurafsky & Martin, 2026).
- Vectors are as wide as the vocabulary, so they are stored sparsely (scikit-learn).

### Comparison

| Method | Representation | Term frequency | Length handling | Training |
|---|---|---|---|---|
| TF-IDF + cosine | sparse word vector | log or raw count | cosine normalisation | none |
| [[bm25\|BM25]] | sparse word vector | saturating, parameter k | parameter b | none |
| [[query-likelihood-model\|Query likelihood]] | document language model | probability | smoothing | none |
| [[dense-passage-retrieval\|Dense retrieval]] | dense learned vector | implicit | implicit | encoder training |

Sources: Jurafsky & Martin (2026), Manning et al. (2008).

### In practice

The choices that most change results are tokenisation and lower-casing, whether tf is raw or logarithmic, whether idf is smoothed and whether vectors are normalised; they should be fixed together with the vocabulary on training data and reused unchanged at query time (scikit-learn). For retrieval, BM25 is usually preferred over plain tf-idf, and lexical scores are often fused with dense retrieval, for example with [[reciprocal-rank-fusion|reciprocal rank fusion]].

### Key takeaway

TF-IDF multiplies a dampened term frequency by the log of how rare a term is across documents, giving sparse, interpretable vectors that are compared with the cosine and remain the baseline for lexical search and text features.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, section 6.2: Tf-idf weighting. Cambridge University Press. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, section 6.4: Document and query weighting schemes. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html)
- scikit-learn developers. *Feature extraction: Tf–idf term weighting.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/feature_extraction.html)
- scikit-learn developers. *TfidfTransformer.* scikit-learn API reference. [scikit-learn.org](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

TF-IDF (Term Frequency–Inverse Document Frequency) gewichtet ein Wort in einem Dokument danach, wie oft es dort vorkommt (Term Frequency) und wie selten es in der Sammlung ist (Inverse Document Frequency), sodass Wörter, die in wenigen Dokumenten häufig vorkommen, hohe Gewichte erhalten und Wörter, die überall vorkommen, Gewichte nahe null (Manning et al., 2008). Dokumente und Anfragen werden zu dünn besetzten Vektoren mit einer Dimension pro Wort des Vokabulars, und das klassische Vektorraummodell ordnet Dokumente nach dem [[cosine-similarity|Kosinus]] zwischen den TF-IDF-Vektoren von Anfrage und Dokument (Jurafsky & Martin, 2026). TF-IDF ist auch eine Standardgewichtung für Merkmale in der Text-[[classification|Klassifikation]] und beim [[clustering|Clustering]] (scikit-learn), und [[bm25|BM25]] ist eine Variante davon.

### Funktionsweise

```text
Dokumente ──► Tokenisierung ──► count(t, d) ──► tf(t, d)  = 1 + log10 count(t, d)   (0 bei Anzahl 0)
                          └──► df(t)        ──► idf(t)    = log10(N / df(t))
                                                 ▼
                                  Gewicht(t, d) = tf(t, d) · idf(t)
                                                 ▼
                 Dokumentvektor (|V| Dimensionen, fast nur Nullen) ──► auf Länge 1 normalisieren
                                                 ▼
          Anfragevektor (gleiche Gewichtung) ──► score(q, d) = cos(q, d) ──► Rangliste
```

#### 1. Term Frequency

Rohe Häufigkeiten überbewerten Wiederholungen: Ein Wort, das 100-mal vorkommt, sagt nicht 100-mal mehr über den Inhalt des Dokuments aus (Jurafsky & Martin, 2026). Die übliche sublineare Skalierung nutzt `tf(t,d) = 1 + log10 count(t,d)` für Häufigkeiten über null und sonst 0, was 1 für ein Vorkommen, 2 für zehn und 3 für hundert ergibt (Jurafsky & Martin, 2026; Manning et al., 2008). Die Maximum-tf-Normalisierung teilt stattdessen durch die größte Term Frequency im Dokument; sie gleicht die höheren Häufigkeiten in langen Dokumenten aus, ist aber instabil, wenn sich die Stoppwortliste ändert oder ein einzelner Ausreißer-Term dominiert (Manning et al., 2008).

#### 2. Inverse Document Frequency

Die Document Frequency `df(t)` ist die Zahl der Dokumente, die t enthalten; die Inverse Document Frequency, die auf Spärck Jones (1972) zurückgeht, ist `idf(t) = log10(N / df(t))` für eine Sammlung von N Dokumenten (Jurafsky & Martin, 2026). Die Document Frequency wird der Collection Frequency (Gesamtzahl der Vorkommen) vorgezogen, weil sie eine Statistik auf Dokumentebene ist und Dokumente besser trennt: In der Reuters-Sammlung kommen *try* und *insurance* insgesamt etwa gleich oft vor, aber in sehr unterschiedlich vielen Dokumenten (Manning et al., 2008). Ein Wort, das in jedem Dokument vorkommt, erhält idf 0, was wie eine weiche Stoppwortliste wirkt; im Shakespeare-Beispiel von Jurafsky und Martin hat *Romeo* (ein Stück) idf 1,57, *good* und *sweet* (alle 37 Stücke) dagegen 0 (Jurafsky & Martin, 2026). Die Basis des Logarithmus ändert das Ranking nicht (Manning et al., 2008).

#### 3. Kombinieren und Normalisieren

Das Gewicht von Term t in Dokument d ist das Produkt `tf-idf(t,d) = tf(t,d) · idf(t)`. Es ist am höchsten, wenn t in wenigen Dokumenten oft vorkommt, niedriger, wenn es seltener oder in vielen Dokumenten vorkommt, und am niedrigsten, wenn es in fast allen Dokumenten steht (Manning et al., 2008). Jedes Dokument ist dann ein Vektor über das ganze Vokabular, dessen Einträge fast alle null sind; die Normalisierung auf Einheitslänge beseitigt den Vorteil langer Dokumente (Manning et al., 2008; [[inverted-index|Inverted Index]]).

#### 4. Anfragen bewerten

Die Anfrage wird wie ein sehr kurzes Dokument behandelt und genauso gewichtet; der Score eines Dokuments ist der Kosinus zwischen Anfrage- und Dokumentvektor, eine Summe über die gemeinsamen Terme (Manning et al., 2008). Im Beispiel von Jurafsky und Martin erzielt für die Anfrage *sweet love* das Dokument „Sweet sweet nurse! Love?“ 0,747 und „Sweet sorrow“ 0,0779, weil das erste beide Terme enthält (Jurafsky & Martin, 2026). Es gibt viele Varianten, die in der SMART-Notation `ddd.qqq` geschrieben werden (Komponente für Term Frequency, Document Frequency und Normalisierung jeweils für Dokument und Anfrage); ein Standardschema ist `lnc.ltc` mit logarithmischer tf und Kosinus-Normalisierung auf beiden Seiten, aber idf nur auf der Anfrage (Manning et al., 2008). Das Weglassen der idf für das Dokument verbessert die Ergebnisse manchmal (Jurafsky & Martin, 2026).

#### 5. Voreinstellungen in Bibliotheken

Implementierungen weichen von der Lehrbuchformel ab. `TfidfTransformer` und `TfidfVectorizer` von scikit-learn nutzen standardmäßig rohe Häufigkeiten als tf, berechnen `idf(t) = log((1 + n) / (1 + df(t))) + 1` mit `smooth_idf=True` (als enthielte ein zusätzliches Dokument jeden Term einmal, was Division durch null verhindert) und `log(n / df(t)) + 1` ohne Glättung und normalisieren jede Zeile mit der L2-Norm; `sublinear_tf=True` ersetzt tf durch `1 + log(tf)` (scikit-learn-API-Referenz). Wegen des „+1“ werden Terme, die in jedem Dokument vorkommen, nicht ganz ignoriert (scikit-learn). Gewichte aus verschiedenen Bibliotheken sind daher nicht direkt vergleichbar.

#### Ursprung und Varianten

Die idf-Gewichtung führte Spärck Jones 1972 ein (Jurafsky & Martin, 2026); die SMART-Notation für Gewichtungsvarianten ist nach einem frühen Text-Retrieval-System benannt (Manning et al., 2008). [[bm25|BM25]] ist eine TF-IDF-Variante mit sättigender Term Frequency (Parameter k) und Normalisierung der Dokumentlänge (Parameter b) (Jurafsky & Martin, 2026). Die Pivoted Document Length Normalization korrigiert die Benachteiligung langer Dokumente durch die Kosinus-Normalisierung (Manning et al., 2008).

### Wann einsetzen

- Stichwortsuche über eine Dokumentsammlung, als Baseline oder als lexikalische Seite einer hybriden Suche ([[information-retrieval|Information Retrieval]], [[rag-retrieval|RAG-Retrieval]]).
- Merkmale für Textklassifikation und Clustering, etwa mit [[naive-bayes|Naive Bayes]], logistischer Regression oder k-Means (scikit-learn; [[classification|Klassifikation]]).
- Charakteristische Wörter eines Dokuments oder einer Dokumentgruppe finden.
- Eingabe für Dimensionsreduktion wie [[latent-semantic-indexing|Latent Semantic Indexing]].

### Stärken und Grenzen

**Stärken**
- Braucht kein Training, nur Zählungen über die Sammlung, und ist mit einem Inverted Index schnell (Manning et al., 2008).
- Leicht interpretierbar: Jede Dimension ist ein Wort mit sichtbarem Gewicht.
- Gewichtet uninformative häufige Wörter ohne handgemachte Stoppwortliste herunter (Jurafsky & Martin, 2026).

**Grenzen**
- Bag of Words: Die Wortreihenfolge geht verloren, sodass „Mary is quicker than John“ und „John is quicker than Mary“ denselben Vektor erhalten (Manning et al., 2008).
- Trifft nur exakte Terme; Synonyme und Paraphrasen werden verfehlt, was dichte [[embeddings|Embeddings]] angehen ([[semantic-retrieval|semantisches Retrieval]]).
- Die Term Frequency wächst unbegrenzt, und die Längennormalisierung ist grob; BM25 behandelt beides besser (Jurafsky & Martin, 2026).
- Die Vektoren sind so breit wie das Vokabular und werden daher dünn besetzt gespeichert (scikit-learn).

### Vergleich

| Verfahren | Repräsentation | Term Frequency | Umgang mit Länge | Training |
|---|---|---|---|---|
| TF-IDF + Kosinus | dünn besetzter Wortvektor | logarithmisch oder roh | Kosinus-Normalisierung | keins |
| [[bm25\|BM25]] | dünn besetzter Wortvektor | sättigend, Parameter k | Parameter b | keins |
| [[query-likelihood-model\|Query Likelihood]] | Sprachmodell pro Dokument | Wahrscheinlichkeit | Glättung | keins |
| [[dense-passage-retrieval\|Dense Retrieval]] | dichter gelernter Vektor | implizit | implizit | Encoder-Training |

Quellen: Jurafsky & Martin (2026), Manning et al. (2008).

### In der Praxis

Am stärksten verändern Tokenisierung und Kleinschreibung die Ergebnisse, außerdem die Wahl zwischen roher und logarithmischer tf, ob idf geglättet wird und ob Vektoren normalisiert werden; diese Entscheidungen werden zusammen mit dem Vokabular auf den Trainingsdaten festgelegt und zur Anfragezeit unverändert wiederverwendet (scikit-learn). Für Retrieval wird meist BM25 statt reinem TF-IDF genutzt, und lexikalische Scores werden oft mit Dense Retrieval fusioniert, etwa mit [[reciprocal-rank-fusion|Reciprocal Rank Fusion]].

### Merksatz

TF-IDF multipliziert eine gedämpfte Term Frequency mit dem Logarithmus der Seltenheit eines Terms über die Dokumente und liefert dünn besetzte, interpretierbare Vektoren, die mit dem Kosinus verglichen werden und die Baseline für lexikalische Suche und Textmerkmale bleiben.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, Abschnitt 6.2: Tf-idf weighting. Cambridge University Press. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, Abschnitt 6.4: Document and query weighting schemes. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html)
- scikit-learn developers. *Feature extraction: Tf–idf term weighting.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/feature_extraction.html)
- scikit-learn developers. *TfidfTransformer.* scikit-learn-API-Referenz. [scikit-learn.org](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html)
