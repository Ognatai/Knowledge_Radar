---
title_en: Latent Semantic Indexing (LSI)
title_de: Latent Semantic Indexing (LSI)
entity_type: Method
aliases:
- LSI
- Latent semantic analysis
- LSA
- Truncated SVD
sources:
- https://nlp.stanford.edu/IR-book/pdf/18lsi.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Latent semantic indexing approximates the term-document matrix by a matrix of low rank k, computed with the singular value decomposition (SVD), and compares queries and documents in the resulting k-dimensional space instead of the space of individual terms (Manning et al., 2008, ch. 18). Terms that co-occur are brought together, which can address synonymy; with k in the low hundreds it increased recall and sometimes precision in TREC experiments, but the SVD is expensive and the dense representation loses Boolean operators and negation (Manning et al., 2008, ch. 18).

### How it works

```text
term-document matrix C (M terms × N documents)
   ─► SVD: C = U Σ Vᵀ   (singular values σ1 ≥ σ2 ≥ …)
   ─► keep the k largest: C_k = U Σ_k Vᵀ
   ─► documents as k-dim vectors; query q_k = Σ_k⁻¹ U_kᵀ q
   ─► cosine similarity in the k-dim space
```

#### 1. The problem: synonymy and polysemy

The vector space model gives each term its own dimension. Synonyms such as car and automobile are therefore unrelated, so similarity between a query and a document is underestimated; a polysemous term such as charge has several meanings, so similarity is overestimated. LSI uses co-occurrences of terms to capture latent semantic associations (Manning et al., 2008, ch. 18).

#### 2. Singular value decomposition

The SVD factors the term-document matrix C into U Σ Vᵀ, where Σ holds the singular values in decreasing order; U is the term matrix and Vᵀ the document matrix. Zeroing all but the k largest singular values gives C_k. By the Eckart-Young theorem, C_k is the best rank-k approximation of C, with Frobenius error σ_(k+1) (Manning et al., 2008, ch. 18).

#### 3. Mapping queries and new documents

A query vector q is mapped into the k-dimensional space as q_k = Σ_k⁻¹ U_kᵀ q, and cosine similarity then compares queries, documents or terms. The same formula folds new documents into an existing LSI space without recomputing the SVD, but folded-in documents add neither their co-occurrences nor new terms, so quality degrades and the SVD must eventually be recomputed (Manning et al., 2008, ch. 18).

#### 4. Why it can help

Forced into k dimensions, the SVD brings together terms with similar co-occurrences, so retrieval should not suffer much and may improve. k is typically chosen in the low hundreds, far below the original rank of tens of thousands (Manning et al., 2008, ch. 18).

#### 5. What experiments showed

Dumais ran LSI on TREC data in the early 1990s; computing the SVD for tens of thousands of documents took about a day, precision was at or above the median TREC participant, the system was top on about 20 % of topics and slightly better on average than standard vector spaces at about 350 dimensions. Later work confirmed: reducing k tends to increase recall; k in the low hundreds can increase precision on some benchmarks, suggesting it addresses synonymy; LSI works best when queries and documents share few words (Manning et al., 2008, ch. 18).

#### Origin and variants

Deerwester et al. (1990) connected information retrieval with low-rank approximations of the term-document matrix; outside retrieval the method is called latent semantic analysis (LSA), and Hofmann (1999) gave a probabilistic extension (Manning et al., 2008, ch. 18). Learned dense vectors from neural models are covered in [[embeddings|Embeddings]].

### When to use it

- When queries and documents use different words for the same things, so that term overlap is low (Manning et al., 2008, ch. 18).
- For cross-language retrieval, where documents in several languages are indexed and a query in one language should find documents in others (Manning et al., 2008, ch. 18).
- As a soft clustering, reading each dimension as a cluster and a document's value on it as its fractional membership (Manning et al., 2008, ch. 18; [[clustering|Clustering]]).

### Strengths and limitations

**Strengths**
- Optimal low-rank approximation in the Frobenius norm (Manning et al., 2008, ch. 18).
- Can raise recall and, for suitable k, precision (Manning et al., 2008, ch. 18).
- New documents can be folded in without recomputation, for a while (Manning et al., 2008, ch. 18).

**Limitations**
- The SVD is computationally expensive; the authors knew of no successful experiment with over a million documents, the main obstacle to adoption (Manning et al., 2008, ch. 18).
- Sparse query vectors become dense in the reduced space, which costs much more to process (Manning et al., 2008, ch. 18).
- Like vector space retrieval, there is no good way to express negation or Boolean conditions (Manning et al., 2008, ch. 18).

### Comparison

| Representation | Dimensions | Handles synonymy |
|----------------|-----------|------------------|
| Vector space (tf-idf) | One per term ([[information-retrieval\|Information Retrieval]]) | No |
| LSI | k, low hundreds (Manning et al., 2008, ch. 18) | Partly, via co-occurrence |

### In practice

One way around the cost of the SVD is to compute it on a random sample of the collection and fold in the remaining documents (Manning et al., 2008, ch. 18). The low-rank matrix C_k is dense and can contain negative entries, unlike the original counts (Manning et al., 2008, ch. 18).

### Key takeaway

LSI replaces term dimensions with the k strongest dimensions of an SVD of the term-document matrix, so co-occurring terms are matched; it can improve recall but is costly and loses Boolean operators.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Matrix decompositions and latent semantic indexing.* Introduction to Information Retrieval, Chapter 18. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/18lsi.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Latent Semantic Indexing nähert die Term-Dokument-Matrix durch eine Matrix niedrigen Rangs k an, berechnet mit der Singulärwertzerlegung (SVD), und vergleicht Anfragen und Dokumente im entstehenden k-dimensionalen Raum statt im Raum der einzelnen Terme (Manning et al., 2008, Kap. 18). Terme, die gemeinsam vorkommen, rücken zusammen, was Synonymie angehen kann; mit k im niedrigen dreistelligen Bereich stiegen in TREC-Experimenten der Recall und teils die Precision, doch die SVD ist teuer, und die dichte Darstellung verliert boolesche Operatoren und Negation (Manning et al., 2008, Kap. 18).

### Funktionsweise

```text
Term-Dokument-Matrix C (M Terme × N Dokumente)
   ─► SVD: C = U Σ Vᵀ   (Singulärwerte σ1 ≥ σ2 ≥ …)
   ─► die k größten behalten: C_k = U Σ_k Vᵀ
   ─► Dokumente als k-dim. Vektoren; Anfrage q_k = Σ_k⁻¹ U_kᵀ q
   ─► Cosine Similarity im k-dim. Raum
```

#### 1. Das Problem: Synonymie und Polysemie

Das Vektorraummodell gibt jedem Term eine eigene Dimension. Synonyme wie car und automobile sind daher unverbunden, sodass die Ähnlichkeit zwischen Anfrage und Dokument unterschätzt wird; ein mehrdeutiger Term wie charge hat mehrere Bedeutungen, sodass die Ähnlichkeit überschätzt wird. LSI nutzt das gemeinsame Vorkommen von Termen, um latente semantische Zusammenhänge zu erfassen (Manning et al., 2008, Kap. 18).

#### 2. Singulärwertzerlegung

Die SVD zerlegt die Term-Dokument-Matrix C in U Σ Vᵀ, wobei Σ die Singulärwerte in absteigender Reihenfolge enthält; U ist die Term-Matrix und Vᵀ die Dokument-Matrix. Alle außer den k größten Singulärwerten auf null zu setzen ergibt C_k. Nach dem Satz von Eckart und Young ist C_k die beste Approximation von C mit Rang k, mit dem Frobenius-Fehler σ_(k+1) (Manning et al., 2008, Kap. 18).

#### 3. Anfragen und neue Dokumente abbilden

Ein Anfragevektor q wird als q_k = Σ_k⁻¹ U_kᵀ q in den k-dimensionalen Raum abgebildet, und Cosine Similarity vergleicht dann Anfragen, Dokumente oder Terme. Mit derselben Formel lassen sich neue Dokumente ohne neue SVD in einen bestehenden LSI-Raum einfügen („Folding-in“), doch eingefügte Dokumente tragen weder ihre Kookkurrenzen noch neue Terme bei, sodass die Qualität sinkt und die SVD irgendwann neu berechnet werden muss (Manning et al., 2008, Kap. 18).

#### 4. Warum es helfen kann

In k Dimensionen gezwungen, bringt die SVD Terme mit ähnlichen Kookkurrenzen zusammen, sodass das Retrieval kaum leiden und sich sogar verbessern sollte. k wird typischerweise im niedrigen dreistelligen Bereich gewählt, weit unter dem ursprünglichen Rang von Zehntausenden (Manning et al., 2008, Kap. 18).

#### 5. Was Experimente zeigten

Dumais setzte LSI Anfang der 1990er-Jahre auf TREC-Daten ein; die SVD für Zehntausende Dokumente dauerte etwa einen Tag, die Precision lag auf oder über dem Median der TREC-Teilnehmer, das System war bei etwa 20 % der Themen das beste und im Mittel bei etwa 350 Dimensionen etwas besser als normale Vektorräume. Spätere Arbeiten bestätigten: Ein kleineres k erhöht tendenziell den Recall; k im niedrigen dreistelligen Bereich kann auf manchen Benchmarks die Precision erhöhen, was darauf hindeutet, dass es Synonymie angeht; LSI funktioniert am besten, wenn Anfragen und Dokumente wenige Wörter teilen (Manning et al., 2008, Kap. 18).

#### Herkunft und Varianten

Deerwester et al. (1990) verbanden Information Retrieval mit Niedrigrang-Approximationen der Term-Dokument-Matrix; außerhalb des Retrievals heißt das Verfahren Latent Semantic Analysis (LSA), und Hofmann (1999) lieferte eine probabilistische Erweiterung (Manning et al., 2008, Kap. 18). Gelernte dichte Vektoren aus neuronalen Modellen behandelt [[embeddings|Embeddings]].

### Wann einsetzen

- Wenn Anfragen und Dokumente unterschiedliche Wörter für dieselben Dinge nutzen, sodass die Termüberlappung gering ist (Manning et al., 2008, Kap. 18).
- Für sprachübergreifendes Retrieval, bei dem Dokumente in mehreren Sprachen indexiert sind und eine Anfrage in einer Sprache Dokumente in anderen finden soll (Manning et al., 2008, Kap. 18).
- Als weiches Clustering, bei dem jede Dimension als Cluster und der Wert eines Dokuments darauf als seine anteilige Zugehörigkeit gelesen wird (Manning et al., 2008, Kap. 18; [[clustering|Clustering]]).

### Stärken und Grenzen

**Stärken**
- Optimale Niedrigrang-Approximation in der Frobenius-Norm (Manning et al., 2008, Kap. 18).
- Kann den Recall und bei passendem k die Precision erhöhen (Manning et al., 2008, Kap. 18).
- Neue Dokumente lassen sich eine Zeit lang ohne Neuberechnung einfügen (Manning et al., 2008, Kap. 18).

**Grenzen**
- Die SVD ist rechenaufwendig; den Autoren war kein erfolgreiches Experiment mit über einer Million Dokumenten bekannt, das größte Hindernis für die Verbreitung (Manning et al., 2008, Kap. 18).
- Dünn besetzte Anfragevektoren werden im reduzierten Raum dicht, was deutlich teurer zu verarbeiten ist (Manning et al., 2008, Kap. 18).
- Wie beim Vektorraum-Retrieval gibt es keinen guten Weg, Negation oder boolesche Bedingungen auszudrücken (Manning et al., 2008, Kap. 18).

### Vergleich

| Darstellung | Dimensionen | Erfasst Synonymie |
|-------------|------------|-------------------|
| Vektorraum (tf-idf) | Eine pro Term ([[information-retrieval\|Information Retrieval]]) | Nein |
| LSI | k, niedriger dreistelliger Bereich (Manning et al., 2008, Kap. 18) | Teilweise, über Kookkurrenz |

### In der Praxis

Ein Weg um die Kosten der SVD ist, sie auf einer Zufallsstichprobe der Sammlung zu berechnen und die übrigen Dokumente einzufügen (Manning et al., 2008, Kap. 18). Die Niedrigrang-Matrix C_k ist dicht und kann, anders als die ursprünglichen Zählungen, negative Einträge enthalten (Manning et al., 2008, Kap. 18).

### Merksatz

LSI ersetzt die Term-Dimensionen durch die k stärksten Dimensionen einer SVD der Term-Dokument-Matrix, sodass gemeinsam vorkommende Terme zusammenfinden; es kann den Recall verbessern, ist aber teuer und verliert boolesche Operatoren.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Matrix decompositions and latent semantic indexing.* Introduction to Information Retrieval, Chapter 18. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/18lsi.pdf)
