---
title_en: Language Models for Information Retrieval (Query Likelihood)
title_de: Sprachmodelle für Information Retrieval (Query Likelihood)
entity_type: Method
aliases:
- Query likelihood model
- Language modeling approach to IR
- Jelinek-Mercer smoothing
- Bayesian smoothing
- Language modelling approach to IR
sources:
- https://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The language modelling approach to retrieval builds a small probabilistic language model from each document and ranks documents by the probability that this model generates the query, P(q | M_d) (Manning et al., 2008, ch. 12). With a unigram model, this is the product of each query term's frequency in the document, smoothed with its frequency in the whole collection; smoothing avoids zero probabilities and, more importantly, implements much of the term weighting, with an effect similar to idf (Manning et al., 2008, ch. 12). The classic language models here are simple word distributions, not [[large-language-models|large language models]].

### How it works

```text
each document d ─► unigram model M_d (term counts / length), mixed with collection model M_c
query q = t1 t2 … ─► score(d) = P(d) · Π_t [ λ·P(t|M_d) + (1−λ)·P(t|M_c) ]
rank documents by score
```

#### 1. Ranking by query likelihood

The goal is to rank by P(d | q); by Bayes' rule this is P(q | d)·P(d) / P(q). P(q) is the same for all documents, and the prior P(d) is often uniform, though it could encode authority, length, genre, recency or popularity. Ranking therefore uses P(q | M_d), the probability of the query under the document's model: the user is assumed to have a prototype document in mind and to choose words from it (Manning et al., 2008, ch. 12).

#### 2. The unigram document model

The most common model is a multinomial unigram model, equivalent to a [[naive-bayes|multinomial Naive Bayes]] model with each document as its own class. The maximum likelihood estimate of a term's probability is its count in the document divided by the document's length, so P(q | M_d) = Π_t tf_t,d / L_d (Manning et al., 2008, ch. 12).

#### 3. Why smoothing is essential

A term missing from a document would get probability zero, making retrieval strictly conjunctive, and terms seen once are overestimated. Smoothing gives unseen terms some probability, but no more than expected by chance from the collection, and discounts seen ones (Manning et al., 2008, ch. 12):
- **Linear interpolation (Jelinek-Mercer):** `P(t|d) = λ·P_mle(t|M_d) + (1 − λ)·P_mle(t|M_c)`, a mixture of the document and the collection model.
- **Bayesian smoothing:** `P(t|d) = (tf_t,d + α·P(t|M_c)) / (L_d + α)`, the collection model as prior.
Both perform well; a small λ or a large α means more smoothing. Less smoothing, a more conjunctive search, suits short queries, more smoothing suits long ones. Smoothing turned out to be essential not only for estimation: it implements major parts of the term weighting (Manning et al., 2008, ch. 12).

#### 4. Relation to tf-idf

Term frequency appears directly, and mixing document and collection probabilities works a little like idf: terms that are rare in the collection but common in a document weigh more. Like tf-idf models, it treats terms as independent, but its intuitions are probabilistic rather than geometric and the model is more principled (Manning et al., 2008, ch. 12; [[information-retrieval|Information Retrieval]]).

#### 5. Extensions

A document likelihood model instead generates the document from a query model, which makes [[query-expansion|relevance feedback]] easy to add; the relevance model of Lavrenko and Croft builds pseudo relevance feedback into it with strong results. Comparing query and document models with the Kullback-Leibler divergence outperformed both directions in Lafferty and Zhai's experiments, though its scores are not comparable across queries. Translation models generate query words not in the document, addressing synonymy (Manning et al., 2008, ch. 12).

#### Origin and variants

Ponte and Croft (1998) introduced the approach, hoping that a probabilistic foundation would improve term weights; it has achieved very good retrieval results (Manning et al., 2008, ch. 12).

### When to use it

- As a principled alternative to tf-idf and [[bm25|BM25]] for ranked keyword retrieval over an [[inverted-index|inverted index]] (Manning et al., 2008, ch. 12).
- When collection statistics should enter the ranking as part of the model rather than as a heuristic (Manning et al., 2008, ch. 12).
- With document priors, such as authority or recency, that should multiply the query likelihood (Manning et al., 2008, ch. 12).

### Strengths and limitations

**Strengths**
- Mathematically precise, conceptually simple, computationally tractable and intuitive (Manning et al., 2008, ch. 12).
- Collection statistics are an integral part of the model (Manning et al., 2008, ch. 12).
- Extensible with priors, feedback and translation models (Manning et al., 2008, ch. 12).

**Limitations**
- Treating documents and information needs as the same kind of object is unrealistic (Manning et al., 2008, ch. 12).
- Unigram models ignore phrases and word order (Manning et al., 2008, ch. 12).
- Without an explicit notion of relevance, relevance feedback and user preferences are hard to integrate in the basic model (Manning et al., 2008, ch. 12).

### Comparison

| Model | Ranks by | Source |
|-------|----------|--------|
| Vector space with tf-idf | Cosine of weighted term vectors | [[information-retrieval\|Information Retrieval]] |
| [[bm25\|BM25]] | Probabilistic relevance weights | [[bm25\|BM25]] |
| Query likelihood | P(q \| M_d) with smoothing | Manning et al. (2008, ch. 12) |
| KL divergence | Distance between query and document models | Manning et al. (2008, ch. 12) |

### In practice

The smoothing parameter matters most and is tuned, for example by line search; it need not be constant and can depend on query length (Manning et al., 2008, ch. 12). The full ranking is P(d) times the product over the query terms of the smoothed probabilities (Manning et al., 2008, ch. 12).

### Key takeaway

The query likelihood model ranks documents by how probably their smoothed unigram model generates the query; smoothing with the collection model supplies the idf-like weighting.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Language models for information retrieval.* Introduction to Information Retrieval, Chapter 12. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der Sprachmodell-Ansatz im Retrieval baut aus jedem Dokument ein kleines probabilistisches Sprachmodell und rankt Dokumente nach der Wahrscheinlichkeit, dass dieses Modell die Anfrage erzeugt, P(q | M_d) (Manning et al., 2008, Kap. 12). Mit einem Unigramm-Modell ist das das Produkt der Häufigkeiten der Anfrageterme im Dokument, geglättet mit ihrer Häufigkeit in der ganzen Sammlung; die Glättung vermeidet Nullwahrscheinlichkeiten und setzt, noch wichtiger, einen großen Teil der Termgewichtung um, mit einer Wirkung ähnlich wie idf (Manning et al., 2008, Kap. 12). Die klassischen Sprachmodelle hier sind einfache Wortverteilungen, keine [[large-language-models|Large Language Models]].

### Funktionsweise

```text
jedes Dokument d ─► Unigramm-Modell M_d (Termzahlen / Länge), gemischt mit Sammlungsmodell M_c
Anfrage q = t1 t2 … ─► score(d) = P(d) · Π_t [ λ·P(t|M_d) + (1−λ)·P(t|M_c) ]
Dokumente nach score ranken
```

#### 1. Ranking nach Query Likelihood

Ziel ist das Ranking nach P(d | q); nach dem Satz von Bayes ist das P(q | d)·P(d) / P(q). P(q) ist für alle Dokumente gleich, und die A-priori-Wahrscheinlichkeit P(d) ist oft gleichverteilt, könnte aber Autorität, Länge, Genre, Aktualität oder Beliebtheit abbilden. Das Ranking nutzt daher P(q | M_d), die Wahrscheinlichkeit der Anfrage unter dem Modell des Dokuments: Angenommen wird, dass der Nutzer ein Musterdokument im Kopf hat und Wörter daraus wählt (Manning et al., 2008, Kap. 12).

#### 2. Das Unigramm-Dokumentmodell

Das häufigste Modell ist ein multinomiales Unigramm-Modell, gleichbedeutend mit einem multinomialen Naive-Bayes-Modell, in dem jedes Dokument seine eigene Klasse ist. Die Maximum-Likelihood-Schätzung der Wahrscheinlichkeit eines Terms ist seine Anzahl im Dokument geteilt durch die Dokumentlänge, also P(q | M_d) = Π_t tf_t,d / L_d (Manning et al., 2008, Kap. 12).

#### 3. Warum Glättung unverzichtbar ist

Ein im Dokument fehlender Term bekäme die Wahrscheinlichkeit null, was das Retrieval streng konjunktiv macht, und einmal gesehene Terme werden überschätzt. Glättung gibt ungesehenen Termen etwas Wahrscheinlichkeit, aber nicht mehr, als nach der Sammlung zufällig zu erwarten ist, und senkt gesehene ab (Manning et al., 2008, Kap. 12):
- **Lineare Interpolation (Jelinek-Mercer):** `P(t|d) = λ·P_mle(t|M_d) + (1 − λ)·P_mle(t|M_c)`, eine Mischung aus Dokument- und Sammlungsmodell.
- **Bayessche Glättung:** `P(t|d) = (tf_t,d + α·P(t|M_c)) / (L_d + α)`, mit dem Sammlungsmodell als A-priori-Verteilung.
Beide funktionieren gut; ein kleines λ oder ein großes α bedeutet mehr Glättung. Weniger Glättung, also eine konjunktivere Suche, passt zu kurzen Anfragen, mehr Glättung zu langen. Glättung erwies sich nicht nur für die Schätzung als wesentlich: Sie setzt große Teile der Termgewichtung um (Manning et al., 2008, Kap. 12).

#### 4. Bezug zu tf-idf

Die Termhäufigkeit geht direkt ein, und die Mischung aus Dokument- und Sammlungswahrscheinlichkeit wirkt ein wenig wie idf: Terme, die in der Sammlung selten, in einem Dokument aber häufig sind, wiegen mehr. Wie tf-idf-Modelle behandelt es Terme als unabhängig, seine Intuitionen sind aber probabilistisch statt geometrisch, und das Modell ist prinzipientreuer (Manning et al., 2008, Kap. 12; [[information-retrieval|Information Retrieval]]).

#### 5. Erweiterungen

Ein Document-Likelihood-Modell erzeugt stattdessen das Dokument aus einem Anfragemodell, was [[query-expansion|Relevance Feedback]] leicht einbinden lässt; das Relevanzmodell von Lavrenko und Croft baut darin Pseudo Relevance Feedback mit starken Ergebnissen ein. Anfrage- und Dokumentmodell mit der Kullback-Leibler-Divergenz zu vergleichen übertraf in den Experimenten von Lafferty und Zhai beide Richtungen, allerdings sind die Werte nicht über Anfragen hinweg vergleichbar. Übersetzungsmodelle erzeugen Anfragewörter, die nicht im Dokument stehen, und gehen so Synonyme an (Manning et al., 2008, Kap. 12).

#### Herkunft und Varianten

Ponte und Croft (1998) führten den Ansatz ein, in der Hoffnung, dass eine probabilistische Grundlage die Termgewichte verbessert; er hat sehr gute Retrieval-Ergebnisse erzielt (Manning et al., 2008, Kap. 12).

### Wann einsetzen

- Als prinzipientreue Alternative zu tf-idf und [[bm25|BM25]] für gerankte Stichwortsuche über einem [[inverted-index|Inverted Index]] (Manning et al., 2008, Kap. 12).
- Wenn Sammlungsstatistiken als Teil des Modells statt als Heuristik in das Ranking eingehen sollen (Manning et al., 2008, Kap. 12).
- Mit A-priori-Gewichten für Dokumente, etwa Autorität oder Aktualität, die die Query Likelihood multiplizieren sollen (Manning et al., 2008, Kap. 12).

### Stärken und Grenzen

**Stärken**
- Mathematisch präzise, konzeptionell einfach, gut berechenbar und intuitiv (Manning et al., 2008, Kap. 12).
- Sammlungsstatistiken sind fester Bestandteil des Modells (Manning et al., 2008, Kap. 12).
- Erweiterbar um A-priori-Gewichte, Feedback und Übersetzungsmodelle (Manning et al., 2008, Kap. 12).

**Grenzen**
- Dokumente und Informationsbedarf als gleichartige Objekte zu behandeln ist unrealistisch (Manning et al., 2008, Kap. 12).
- Unigramm-Modelle ignorieren Phrasen und Wortreihenfolge (Manning et al., 2008, Kap. 12).
- Ohne ausdrücklichen Relevanzbegriff lassen sich Relevance Feedback und Nutzerpräferenzen im Grundmodell schwer einbinden (Manning et al., 2008, Kap. 12).

### Vergleich

| Modell | Rankt nach | Quelle |
|--------|------------|--------|
| Vektorraum mit tf-idf | Cosinus gewichteter Termvektoren | [[information-retrieval\|Information Retrieval]] |
| [[bm25\|BM25]] | Probabilistische Relevanzgewichte | [[bm25\|BM25]] |
| Query Likelihood | P(q \| M_d) mit Glättung | Manning et al. (2008, Kap. 12) |
| KL-Divergenz | Abstand zwischen Anfrage- und Dokumentmodell | Manning et al. (2008, Kap. 12) |

### In der Praxis

Der Glättungsparameter ist am wichtigsten und wird abgestimmt, etwa per Line Search; er muss nicht konstant sein und kann von der Anfragelänge abhängen (Manning et al., 2008, Kap. 12). Das vollständige Ranking ist P(d) mal dem Produkt der geglätteten Wahrscheinlichkeiten über die Anfrageterme (Manning et al., 2008, Kap. 12).

### Merksatz

Das Query-Likelihood-Modell rankt Dokumente danach, wie wahrscheinlich ihr geglättetes Unigramm-Modell die Anfrage erzeugt; die Glättung mit dem Sammlungsmodell liefert die idf-ähnliche Gewichtung.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Language models for information retrieval.* Introduction to Information Retrieval, Chapter 12. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf)
