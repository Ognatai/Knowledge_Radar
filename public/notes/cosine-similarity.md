---
title_en: Cosine Similarity
title_de: Cosine Similarity
entity_type: Concept
aliases:
- Cosine similarity
- Cosine
- Cosine-similarity
sources:
- https://web.stanford.edu/~jurafsky/slp3/5.pdf
- https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html
- https://nlp.stanford.edu/IR-book/html/htmledition/queries-as-vectors-1.html
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/2403.05440
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Cosine similarity measures how similar two vectors are by the cosine of the angle between them: their dot product divided by the product of their lengths (Jurafsky & Martin, 2026). Because it ignores vector length, a long document and a short one with the same distribution of words count as similar, which is why it became the standard score of the vector space model in [[information-retrieval|information retrieval]] (Manning et al., 2008) and the default way to compare word and sentence [[embeddings|embeddings]] (Jurafsky & Martin, 2026; Reimers & Gurevych, 2019). For learned embeddings it can, however, give arbitrary results when the model was trained on the unnormalised dot product (Steck et al., 2024).

### How it works

```text
vectors v, w (same dimension N)
   │
   ├─ dot product      v · w = Σ v_i w_i
   ├─ lengths          |v| = √Σ v_i² ,  |w| = √Σ w_i²
   ▼
cos(v, w) = (v · w) / (|v| |w|)          range −1 … 1 (0 … 1 for non-negative vectors)
   │
   └─ equivalently: normalise both to unit length, then take the dot product
```

#### 1. From dot product to cosine

The dot product is high when two vectors have large values in the same dimensions and 0 for orthogonal vectors, but it favours long vectors: frequent words have longer co-occurrence vectors and would look similar to everything (Jurafsky & Martin, 2026). Dividing by both lengths gives the normalised dot product, which equals the cosine of the angle θ between the vectors, since `a · b = |a| |b| cos θ` (Jurafsky & Martin, 2026). In retrieval the same argument applies to documents: two documents with the same relative term distribution can have a large vector difference just because one is longer (Manning et al., 2008).

#### 2. Range and interpretation

The cosine is 1 for vectors pointing in the same direction, 0 for orthogonal vectors and −1 for opposite directions; for count or [[tf-idf|tf-idf]] vectors, which have no negative entries, it lies between 0 and 1 (Jurafsky & Martin, 2026). Cosine similarity is invariant to scaling a vector by a positive constant (Jurafsky & Martin, 2026).

#### 3. Unit vectors and fast search

If all vectors are normalised to length 1 in advance, the cosine reduces to the dot product (Jurafsky & Martin, 2026; Manning et al., 2008). Search systems use this: document vectors are normalised once when indexed, and a query is scored by dot products. In the vector space model the score of document d for query q is `cos(q, d)`, computed term at a time over an [[inverted-index|inverted index]] because only shared terms contribute (Manning et al., 2008). The same shortcut serves dense embeddings stored in [[vector-databases|vector databases]].

#### 4. Worked examples

With raw co-occurrence counts over the context words *pie*, *data* and *computer*, `cos(cherry, information) = 0.018` and `cos(digital, information) = 0.996`, so *information* is much closer to *digital* (Jurafsky & Martin, 2026). In the vector space model, the query *jealous gossip* ranks *Wuthering Heights* first with a score of 0.509, far ahead of *Pride and Prejudice* (0.085) (Manning et al., 2008).

#### 5. Cosine over learned embeddings

Sentence-BERT fine-tunes [[bert|BERT]] in a siamese network so that sentence embeddings can be compared with cosine similarity; finding the most similar pair among 10,000 sentences drops from about 65 hours with BERT as a [[cross-encoder|cross-encoder]] to about 5 seconds for the embeddings plus 0.01 seconds for the cosines (Reimers & Gurevych, 2019). Averaged BERT token embeddings, by contrast, did poorly with cosine similarity on semantic textual similarity tasks, worse than averaged [[glove|GloVe]] vectors, because cosine treats all dimensions equally (Reimers & Gurevych, 2019). Steck et al. (2024) show analytically for regularised matrix factorisation models that when training is defined on the unnormalised dot product, the learned embeddings have a degree of freedom (a rescaling of latent dimensions) that leaves the dot products unchanged but changes the cosine similarities, which can then be arbitrary and even non-unique.

#### Origin and variants

Cosine scoring is the core of the vector space model of retrieval, where queries are treated as short documents (Manning et al., 2008). Related measures are the raw dot product, Euclidean distance and, for sets, the Jaccard coefficient ([[text-similarity-metrics|text similarity metrics]]). Sentence-BERT reported roughly the same results with negative Manhattan and Euclidean distance as with cosine (Reimers & Gurevych, 2019).

### When to use it

- Ranking documents by a query in the vector space model with [[tf-idf|tf-idf]] weights (Manning et al., 2008).
- Finding similar words, sentences or passages with embeddings ([[semantic-retrieval|semantic retrieval]], [[sentence-bert|Sentence-BERT]]).
- [[clustering|Clustering]] and deduplicating texts by meaning (Reimers & Gurevych, 2019).
- Measuring associations in embedding spaces, for example in bias studies ([[bias-in-nlp|bias in NLP]]).

### Strengths and limitations

**Strengths**
- Independent of vector length, so frequency and document length do not dominate (Jurafsky & Martin, 2026; Manning et al., 2008).
- Cheap: one dot product on pre-normalised vectors.
- Bounded and easy to compare across pairs.

**Limitations**
- Only meaningful if the representation was built for it; averaged BERT embeddings and dot-product-trained embeddings can give poor or arbitrary cosines (Reimers & Gurevych, 2019; Steck et al., 2024).
- Treats all dimensions equally, unlike a trained classifier (Reimers & Gurevych, 2019).
- Discards length, which can carry information, for example about popularity in recommender embeddings (Steck et al., 2024).
- A high cosine shows relatedness, not truth or relevance; similar but wrong passages score high as well ([[rag-failure-modes|RAG failure modes]]).

### Comparison

| Measure | Formula | Length-sensitive | Typical use |
|---|---|---|---|
| Cosine similarity | `v·w / (‖v‖ ‖w‖)` | no | tf-idf retrieval, sentence embeddings |
| Dot product | `Σ v_i w_i` | yes | models trained on inner products |
| Euclidean distance | `√Σ (v_i − w_i)²` | yes | k-means, [[k-nearest-neighbours\|k-NN]] |
| Jaccard coefficient | size of A ∩ B divided by size of A ∪ B | not applicable (sets) | [[near-duplicate-detection\|near-duplicate detection]] |

Sources: Jurafsky & Martin (2026), Manning et al. (2008), Steck et al. (2024).

### In practice

Embedding models state which similarity they were trained for; using cosine on a model trained for the dot product, or the reverse, can change rankings (Steck et al., 2024). Steck et al. (2024) suggest training directly with respect to cosine similarity, for example with layer normalisation, or projecting embeddings back into the original space before taking cosines. In [[bias-in-nlp|bias research]], cosines between word embeddings reproduced human implicit associations: African American names had higher GloVe cosine with unpleasant words and European American names with pleasant words, and debiasing reduces but does not eliminate such effects (Jurafsky & Martin, 2026).

### Key takeaway

Cosine similarity compares directions rather than magnitudes, which makes it the standard score for tf-idf vectors and sentence embeddings, but it is only as meaningful as the embedding's training makes it.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 5: Embeddings. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/5.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, section 6.3.1: Dot products. Cambridge University Press. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, section 6.3.2: Queries as vectors. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/queries-as-vectors-1.html)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Steck, H., Ekanadham, C. & Kallus, N. (2024). *Is Cosine-Similarity of Embeddings Really About Similarity?* WWW 2024 Companion. [arXiv:2403.05440](https://arxiv.org/abs/2403.05440)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Cosine Similarity misst die Ähnlichkeit zweier Vektoren über den Kosinus des Winkels zwischen ihnen: ihr Skalarprodukt geteilt durch das Produkt ihrer Längen (Jurafsky & Martin, 2026). Weil sie die Vektorlänge ignoriert, gelten ein langes und ein kurzes Dokument mit derselben Wortverteilung als ähnlich; deshalb wurde sie zum Standard-Score des Vektorraummodells im [[information-retrieval|Information Retrieval]] (Manning et al., 2008) und zum üblichen Weg, Wort- und Satz-[[embeddings|Embeddings]] zu vergleichen (Jurafsky & Martin, 2026; Reimers & Gurevych, 2019). Bei gelernten Embeddings kann sie allerdings beliebige Ergebnisse liefern, wenn das Modell auf das unnormalisierte Skalarprodukt trainiert wurde (Steck et al., 2024).

### Funktionsweise

```text
Vektoren v, w (gleiche Dimension N)
   │
   ├─ Skalarprodukt    v · w = Σ v_i w_i
   ├─ Längen           |v| = √Σ v_i² ,  |w| = √Σ w_i²
   ▼
cos(v, w) = (v · w) / (|v| |w|)          Bereich −1 … 1 (0 … 1 bei nichtnegativen Vektoren)
   │
   └─ gleichwertig: beide auf Länge 1 normalisieren, dann Skalarprodukt bilden
```

#### 1. Vom Skalarprodukt zum Kosinus

Das Skalarprodukt ist hoch, wenn zwei Vektoren in denselben Dimensionen große Werte haben, und 0 für orthogonale Vektoren, bevorzugt aber lange Vektoren: Häufige Wörter haben längere Kookkurrenzvektoren und sähen allem ähnlich (Jurafsky & Martin, 2026). Das Teilen durch beide Längen ergibt das normalisierte Skalarprodukt, das dem Kosinus des Winkels θ zwischen den Vektoren entspricht, da `a · b = |a| |b| cos θ` (Jurafsky & Martin, 2026). Im Retrieval gilt dasselbe Argument für Dokumente: Zwei Dokumente mit derselben relativen Termverteilung können einen großen Vektorabstand haben, nur weil eines länger ist (Manning et al., 2008).

#### 2. Wertebereich und Deutung

Der Kosinus ist 1 für gleich gerichtete Vektoren, 0 für orthogonale und −1 für entgegengesetzte; für Häufigkeits- oder [[tf-idf|TF-IDF]]-Vektoren ohne negative Einträge liegt er zwischen 0 und 1 (Jurafsky & Martin, 2026). Cosine Similarity ist invariant gegenüber dem Skalieren eines Vektors mit einer positiven Konstante (Jurafsky & Martin, 2026).

#### 3. Einheitsvektoren und schnelle Suche

Werden alle Vektoren vorab auf Länge 1 normalisiert, reduziert sich der Kosinus auf das Skalarprodukt (Jurafsky & Martin, 2026; Manning et al., 2008). Suchsysteme nutzen das: Dokumentvektoren werden beim Indexieren einmal normalisiert, und eine Anfrage wird über Skalarprodukte bewertet. Im Vektorraummodell ist der Score von Dokument d für Anfrage q `cos(q, d)`, Term für Term über einen [[inverted-index|Inverted Index]] berechnet, weil nur gemeinsame Terme beitragen (Manning et al., 2008). Derselbe Kurzweg dient dichten Embeddings in [[vector-databases|Vektordatenbanken]].

#### 4. Rechenbeispiele

Mit rohen Kookkurrenzhäufigkeiten über die Kontextwörter *pie*, *data* und *computer* ergibt sich `cos(cherry, information) = 0,018` und `cos(digital, information) = 0,996`; *information* liegt also viel näher an *digital* (Jurafsky & Martin, 2026). Im Vektorraummodell setzt die Anfrage *jealous gossip* *Wuthering Heights* mit einem Score von 0,509 auf Platz eins, weit vor *Pride and Prejudice* (0,085) (Manning et al., 2008).

#### 5. Kosinus über gelernte Embeddings

Sentence-BERT trainiert [[bert|BERT]] in einem siamesischen Netz nach, sodass sich Satz-Embeddings mit Cosine Similarity vergleichen lassen; das ähnlichste Paar unter 10.000 Sätzen zu finden dauert dann statt etwa 65 Stunden mit BERT als [[cross-encoder|Cross-Encoder]] etwa 5 Sekunden für die Embeddings plus 0,01 Sekunden für die Kosinuswerte (Reimers & Gurevych, 2019). Gemittelte BERT-Token-Embeddings schnitten dagegen mit Cosine Similarity bei Aufgaben zur semantischen Textähnlichkeit schlecht ab, schlechter als gemittelte GloVe-Vektoren, weil der Kosinus alle Dimensionen gleich behandelt (Reimers & Gurevych, 2019). Steck et al. (2024) zeigen analytisch für regularisierte Matrixfaktorisierungsmodelle: Ist das Training über das unnormalisierte Skalarprodukt definiert, haben die gelernten Embeddings einen Freiheitsgrad (eine Umskalierung der latenten Dimensionen), der die Skalarprodukte unverändert lässt, die Kosinus-Ähnlichkeiten aber verändert; diese können dann beliebig und sogar nicht eindeutig sein.

#### Ursprung und Varianten

Kosinus-Scoring ist der Kern des Vektorraummodells im Retrieval, in dem Anfragen als kurze Dokumente behandelt werden (Manning et al., 2008). Verwandte Maße sind das rohe Skalarprodukt, der euklidische Abstand und für Mengen der Jaccard-Koeffizient ([[text-similarity-metrics|Textähnlichkeitsmetriken]]). Sentence-BERT erzielte mit negativem Manhattan- und euklidischem Abstand etwa dieselben Ergebnisse wie mit dem Kosinus (Reimers & Gurevych, 2019).

### Wann einsetzen

- Dokumente im Vektorraummodell mit [[tf-idf|TF-IDF]]-Gewichten nach einer Anfrage ordnen (Manning et al., 2008).
- Ähnliche Wörter, Sätze oder Passagen mit Embeddings finden ([[semantic-retrieval|semantisches Retrieval]], [[sentence-bert|Sentence-BERT]]).
- Texte nach Bedeutung [[clustering|clustern]] und Duplikate erkennen (Reimers & Gurevych, 2019).
- Assoziationen in Embedding-Räumen messen, etwa in Bias-Studien ([[bias-in-nlp|Bias in NLP]]).

### Stärken und Grenzen

**Stärken**
- Unabhängig von der Vektorlänge, sodass Häufigkeit und Dokumentlänge nicht dominieren (Jurafsky & Martin, 2026; Manning et al., 2008).
- Günstig: ein Skalarprodukt auf vorab normalisierten Vektoren.
- Beschränkt und über Paare hinweg leicht vergleichbar.

**Grenzen**
- Nur aussagekräftig, wenn die Repräsentation dafür gebaut ist; gemittelte BERT-Embeddings und auf das Skalarprodukt trainierte Embeddings können schlechte oder beliebige Kosinuswerte liefern (Reimers & Gurevych, 2019; Steck et al., 2024).
- Behandelt alle Dimensionen gleich, anders als ein trainierter Klassifikator (Reimers & Gurevych, 2019).
- Verwirft die Länge, die Information tragen kann, etwa über Popularität in Recommender-Embeddings (Steck et al., 2024).
- Ein hoher Kosinus zeigt Verwandtschaft, nicht Wahrheit oder Relevanz; ähnliche, aber falsche Passagen erzielen ebenfalls hohe Werte ([[rag-failure-modes|RAG-Fehlermuster]]).

### Vergleich

| Maß | Formel | Längenabhängig | Typischer Einsatz |
|---|---|---|---|
| Cosine Similarity | `v·w / (‖v‖ ‖w‖)` | nein | TF-IDF-Retrieval, Satz-Embeddings |
| Skalarprodukt | `Σ v_i w_i` | ja | auf Skalarprodukte trainierte Modelle |
| Euklidischer Abstand | `√Σ (v_i − w_i)²` | ja | k-Means, [[k-nearest-neighbours\|k-NN]] |
| Jaccard-Koeffizient | Größe von A ∩ B geteilt durch Größe von A ∪ B | entfällt (Mengen) | [[near-duplicate-detection\|Erkennung von Beinahe-Duplikaten]] |

Quellen: Jurafsky & Martin (2026), Manning et al. (2008), Steck et al. (2024).

### In der Praxis

Embedding-Modelle geben an, für welche Ähnlichkeit sie trainiert wurden; der Kosinus auf einem für das Skalarprodukt trainierten Modell oder umgekehrt kann Rankings verändern (Steck et al., 2024). Steck et al. (2024) schlagen vor, direkt auf Cosine Similarity zu trainieren, etwa mit Layer Normalization, oder Embeddings vor dem Kosinus in den ursprünglichen Raum zurückzuprojizieren. In der [[bias-in-nlp|Bias-Forschung]] reproduzierten Kosinuswerte zwischen Wort-Embeddings menschliche implizite Assoziationen: Afroamerikanische Namen hatten einen höheren GloVe-Kosinus mit unangenehmen Wörtern und europäisch-amerikanische Namen mit angenehmen, und Debiasing verringert solche Effekte, beseitigt sie aber nicht (Jurafsky & Martin, 2026).

### Merksatz

Cosine Similarity vergleicht Richtungen statt Beträge und ist deshalb der Standard-Score für TF-IDF-Vektoren und Satz-Embeddings, aber nur so aussagekräftig, wie das Training des Embeddings es zulässt.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 5: Embeddings. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/5.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, Abschnitt 6.3.1: Dot products. Cambridge University Press. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*, Abschnitt 6.3.2: Queries as vectors. [nlp.stanford.edu](https://nlp.stanford.edu/IR-book/html/htmledition/queries-as-vectors-1.html)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Steck, H., Ekanadham, C. & Kallus, N. (2024). *Is Cosine-Similarity of Embeddings Really About Similarity?* WWW 2024 Companion. [arXiv:2403.05440](https://arxiv.org/abs/2403.05440)
