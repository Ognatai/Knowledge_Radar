---
title_en: Collocations and Pointwise Mutual Information
title_de: Kollokationen und Pointwise Mutual Information
entity_type: Method
aliases:
- Collocation
- Collocation extraction
- Pointwise mutual information
- PMI
- PPMI
sources:
- https://nlp.stanford.edu/fsnlp/promo/colloc.pdf
- https://web.stanford.edu/~jurafsky/slp3/J.pdf
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A collocation is an expression of two or more words that corresponds to a conventional way of saying things, such as *strong tea*, *weapons of mass destruction* or *make up*; collocations are only partly compositional (Manning & Schütze, 1999). They are found in corpora by frequency with a part-of-speech filter, by the mean and variance of the distance between two words, by hypothesis tests (t test, χ² test, likelihood ratio) and by pointwise mutual information (PMI) (Manning & Schütze, 1999). PMI compares how often two words occur together with how often they would co-occur by chance; positive PMI (PPMI) also weights word-context matrices for word vectors (Jurafsky & Martin, 2026).

### How it works

```text
corpus ─► candidate bigrams (adjacent, or within a window of 3–4 words)
   ├─ frequency + part-of-speech filter (A N, N N, ...)        → fixed phrases
   ├─ mean and variance of the offset between two words         → flexible pairs (knock … door)
   ├─ hypothesis test against independence P(w1 w2) = P(w1)·P(w2)
   │     t test · χ² test · likelihood ratio                     → ranked candidates
   └─ PMI = log2 P(w1,w2) / (P(w1)·P(w2))                       → association strength
```

#### 1. What a collocation is

Collocations range from idioms such as *kick the bucket*, whose meaning has only an indirect historical relation to the parts, to milder cases such as *strong tea*, where *strong* means "rich in some active agent". Typical criteria are non-compositionality, non-substitutability (*yellow wine* cannot replace *white wine*) and non-modifiability (*to get a frog in one's throat* does not accept *ugly frog*). A practical test is translation: *make a decision* is *prendre une décision* in French, not word-by-word *faire une décision*. Subclasses include light verbs (*make a decision*, *do a favor*), phrasal verbs (*tell off*), proper names and terminological expressions (*hydraulic oil filter*). Words that are merely associated, such as *doctor – nurse*, are better called association or co-occurrence (Manning & Schütze, 1999).

#### 2. Frequency with a part-of-speech filter

The most frequent bigrams of a 14-million-word New York Times corpus are mostly pairs of function words (*of the*, *in the*); only *New York* stands out. Passing candidates through a part-of-speech filter that keeps patterns such as adjective-noun or noun-noun (Justeson & Katz) gives surprisingly good results: *New York*, *United States*, *Los Angeles*, with only a few compositional phrases like *last year* (Manning & Schütze, 1999).

#### 3. Mean and variance of the distance

Many collocations are not fixed phrases: *knocked on his door*, *knocked at the door*. Smadja's method computes the mean and standard deviation of the signed distance between two words within a window; a low standard deviation means the words usually occur at the same distance. *strong* relative to *opposition* has one clear peak at position −1 (σ = 0.67), relative to *for* it is spread out (σ = 2.15). Smadja reported about 80% accuracy for terminology extraction with this method (Manning & Schütze, 1999).

#### 4. Hypothesis tests

High frequency can be accidental when both words are frequent. Hypothesis tests take the null hypothesis that the words are independent, P(w1 w2) = P(w1)·P(w2):
- **t test**: *new companies* occurs 8 times; t ≈ 0.9999 is below the critical value 2.576, so independence cannot be rejected. For bigrams that each occur 20 times, the t test separates *Ayatollah Ruhollah* or *unsalted butter* from *first made* or *like people*, which frequency alone cannot. A t test of differences finds words that distinguish *strong* from *powerful* (*powerful computers*, *strong support*), useful in lexicography.
- **Pearson's χ² test** compares observed with expected counts in a 2×2 table and does not assume normally distributed probabilities; its top-20 bigrams matched those of the t test. It also identifies translation pairs in aligned corpora and measures corpus similarity.
- **Likelihood ratio** (Dunning) compares a hypothesis of independence with one of dependence; it is easier to interpret and more appropriate for sparse data than χ².
- **Relative frequency ratios** between two corpora find subject-specific collocations (Damerau).

Because language is very regular, 824 of 831 bigrams that occurred 20 times rejected independence; the tests are therefore mainly used to rank candidates, not for their significance level (Manning & Schütze, 1999).

#### 5. Pointwise mutual information

PMI (Fano, 1961) measures how much more often two events occur together than expected if they were independent: PMI(w, c) = log2 P(w, c) / (P(w) P(c)) (Jurafsky & Martin, 2026). Negative values are unreliable unless corpora are enormous, so positive PMI replaces them with zero: PPMI(w, c) = max(PMI(w, c), 0). PPMI is used instead of tf-idf in word-context matrices; because PMI is biased towards rare events, the context probability can be raised to the power α = 0.75 (Levy et al., 2015) or counts can be Laplace-smoothed (Jurafsky & Martin, 2026). As a collocation measure PMI is weak: among perfectly dependent bigrams it grows as they get rarer, bigrams seen once get inflated scores, and in the Canadian Hansard it preferred the wrong translation pair (*communes, house*) where χ² found *chambre, house*. It is a good measure of independence but a bad measure of dependence (Manning & Schütze, 1999).

#### Origin and variants

The tradition goes back to Firth's dictum that a word is characterised by the company it keeps; one of the first publications on discovering collocations was Church & Hanks (1989), who used them for computational lexicography (Manning & Schütze, 1999). Other measures include the z score and Fisher's exact test (Manning & Schütze, 1999).

### When to use it

- Natural language generation, so that output avoids mistakes like *powerful tea* (Manning & Schütze, 1999).
- Lexicography and terminology extraction, including consistent translation of terms (Manning & Schütze, 1999).
- Information retrieval, where matching on phrases instead of single words can improve accuracy (Manning & Schütze, 1999).
- PPMI for weighting word-context co-occurrence matrices (Jurafsky & Martin, 2026).

### Strengths and limitations

**Strengths**
- A simple quantitative method plus a little linguistic knowledge, such as parts of speech, goes a long way (Manning & Schütze, 1999).
- Hypothesis tests rank bigrams of equal frequency by how much of each word's occurrences fall into the bigram (Manning & Schütze, 1999).

**Limitations**
- None of the measures works very well for low-frequency events; PMI suffers most from sparse data (Manning & Schütze, 1999).
- The t test assumes normally distributed probabilities and χ² is inaccurate for small expected counts (Manning & Schütze, 1999).
- Machine-produced lists are of lower quality than manual collocation dictionaries such as the BBI Combinatory Dictionary (Manning & Schütze, 1999).

### Comparison

| Method | Finds | Caveat |
|--------|-------|--------|
| Frequency + POS filter | Fixed phrases, names | Not for flexible pairs |
| Mean and variance | Flexible pairs (*knock … door*) | Needs a window |
| t test | Ranked dependent bigrams | Assumes normality |
| χ² test | Dependence, translation pairs | Poor for small counts |
| Likelihood ratio | Dependence, including rare bigrams | – |
| PMI | Strength of association | Inflated for rare words |

All rows: Manning & Schütze (1999).

### In practice

The statistical tests are used to rank candidates rather than to test significance (Manning & Schütze, 1999). Collocations relate to the phrase handling of [[information-retrieval|Information Retrieval]], and PPMI weights the word-context co-occurrence matrices from which word vectors are built (Jurafsky & Martin, 2026); learned vectors are covered in [[embeddings|Embeddings]]. Background on hypothesis tests is in [[statistics-fundamentals|Statistics Fundamentals]]. In gender bias analysis of news corpora, the adjectives, nouns and verbs with the highest PMI per actor reveal thematic associations and stereotypical framing; differences between gender groups indicate bias (Urchs, 2025).

### Key takeaway

Collocations are conventional word combinations whose meaning is not fully predictable from their parts; they are found by frequency with POS filters, distance variance, hypothesis tests and PMI, of which PMI measures association but overrates rare pairs.

### Sources

- Manning, C. D. & Schütze, H. (1999). *Collocations.* Foundations of Statistical Natural Language Processing, Chapter 5. MIT Press. [stanford.edu](https://nlp.stanford.edu/fsnlp/promo/colloc.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Pointwise Mutual Information (PMI).* Speech and Language Processing, 3rd ed. draft, Appendix J. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/J.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine Kollokation ist ein Ausdruck aus zwei oder mehr Wörtern, der einer konventionellen Ausdrucksweise entspricht, etwa *strong tea*, *weapons of mass destruction* oder *make up*; Kollokationen sind nur teilweise kompositionell (Manning & Schütze, 1999). Sie werden in Korpora gefunden über Häufigkeit mit Wortartfilter, über Mittelwert und Varianz des Abstands zweier Wörter, über Hypothesentests (t-Test, χ²-Test, Likelihood-Quotient) und über Pointwise Mutual Information (PMI) (Manning & Schütze, 1999). PMI vergleicht, wie oft zwei Wörter gemeinsam auftreten, mit der zufällig erwarteten Häufigkeit; positive PMI (PPMI) gewichtet außerdem Wort-Kontext-Matrizen für Wortvektoren (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Korpus ─► Kandidaten-Bigramme (benachbart oder in einem Fenster von 3–4 Wörtern)
   ├─ Häufigkeit + Wortartfilter (A N, N N, ...)                → feste Wendungen
   ├─ Mittelwert und Varianz des Abstands zweier Wörter         → flexible Paare (knock … door)
   ├─ Hypothesentest gegen Unabhängigkeit P(w1 w2) = P(w1)·P(w2)
   │     t-Test · χ²-Test · Likelihood-Quotient                  → gerankte Kandidaten
   └─ PMI = log2 P(w1,w2) / (P(w1)·P(w2))                       → Assoziationsstärke
```

#### 1. Was eine Kollokation ist

Kollokationen reichen von Idiomen wie *kick the bucket*, deren Bedeutung nur noch historisch mit den Teilen zusammenhängt, bis zu milderen Fällen wie *strong tea*, in dem *strong* „reich an einem Wirkstoff“ bedeutet. Typische Kriterien sind Nicht-Kompositionalität, Nicht-Ersetzbarkeit (*yellow wine* kann *white wine* nicht ersetzen) und Nicht-Modifizierbarkeit (*to get a frog in one's throat* verträgt kein *ugly frog*). Ein praktischer Test ist die Übersetzung: *make a decision* heißt auf Französisch *prendre une décision*, nicht wörtlich *faire une décision*. Unterklassen sind Funktionsverben (*make a decision*, *do a favor*), Partikelverben (*tell off*), Eigennamen und Fachausdrücke (*hydraulic oil filter*). Wörter, die nur miteinander assoziiert sind, wie *doctor – nurse*, heißen besser Assoziation oder Kookkurrenz (Manning & Schütze, 1999).

#### 2. Häufigkeit mit Wortartfilter

Die häufigsten Bigramme eines New-York-Times-Korpus mit 14 Millionen Wörtern sind meist Paare von Funktionswörtern (*of the*, *in the*); nur *New York* fällt auf. Ein Wortartfilter, der Muster wie Adjektiv-Nomen oder Nomen-Nomen durchlässt (Justeson & Katz), liefert überraschend gute Ergebnisse: *New York*, *United States*, *Los Angeles*, mit nur wenigen kompositionellen Wendungen wie *last year* (Manning & Schütze, 1999).

#### 3. Mittelwert und Varianz des Abstands

Viele Kollokationen sind keine festen Wendungen: *knocked on his door*, *knocked at the door*. Smadjas Verfahren berechnet Mittelwert und Standardabweichung des vorzeichenbehafteten Abstands zweier Wörter in einem Fenster; eine kleine Standardabweichung bedeutet, dass die Wörter meist im gleichen Abstand stehen. *strong* hat relativ zu *opposition* einen klaren Gipfel bei Position −1 (σ = 0,67), relativ zu *for* ist die Verteilung breit (σ = 2,15). Smadja berichtete für die Terminologie-Extraktion mit diesem Verfahren etwa 80 % Genauigkeit (Manning & Schütze, 1999).

#### 4. Hypothesentests

Hohe Häufigkeit kann zufällig sein, wenn beide Wörter häufig sind. Hypothesentests nehmen als Nullhypothese an, dass die Wörter unabhängig sind, P(w1 w2) = P(w1)·P(w2):
- **t-Test**: *new companies* kommt 8-mal vor; t ≈ 0,9999 liegt unter dem kritischen Wert 2,576, also lässt sich Unabhängigkeit nicht verwerfen. Bei Bigrammen, die jeweils 20-mal vorkommen, trennt der t-Test *Ayatollah Ruhollah* oder *unsalted butter* von *first made* oder *like people*, was die Häufigkeit allein nicht kann. Ein t-Test für Unterschiede findet Wörter, die *strong* von *powerful* unterscheiden (*powerful computers*, *strong support*), nützlich für die Lexikographie.
- **Pearsons χ²-Test** vergleicht beobachtete mit erwarteten Häufigkeiten in einer 2×2-Tafel und setzt keine normalverteilten Wahrscheinlichkeiten voraus; seine Top-20-Bigramme stimmten mit denen des t-Tests überein. Er erkennt auch Übersetzungspaare in alignierten Korpora und misst Korpusähnlichkeit.
- **Likelihood-Quotient** (Dunning) vergleicht eine Hypothese der Unabhängigkeit mit einer der Abhängigkeit; er ist leichter zu deuten und für dünne Daten besser geeignet als χ².
- **Verhältnisse relativer Häufigkeiten** zwischen zwei Korpora finden themenspezifische Kollokationen (Damerau).

Weil Sprache sehr regelmäßig ist, verwarfen 824 von 831 Bigrammen mit 20 Vorkommen die Unabhängigkeit; die Tests dienen daher vor allem zum Ranking der Kandidaten, nicht wegen ihres Signifikanzniveaus (Manning & Schütze, 1999).

#### 5. Pointwise Mutual Information

PMI (Fano, 1961) misst, um wie viel häufiger zwei Ereignisse gemeinsam auftreten als bei Unabhängigkeit erwartet: PMI(w, c) = log2 P(w, c) / (P(w) P(c)) (Jurafsky & Martin, 2026). Negative Werte sind unzuverlässig, solange Korpora nicht riesig sind, daher ersetzt positive PMI sie durch null: PPMI(w, c) = max(PMI(w, c), 0). PPMI wird statt tf-idf in Wort-Kontext-Matrizen verwendet; weil PMI seltene Ereignisse bevorzugt, kann die Kontextwahrscheinlichkeit mit α = 0,75 potenziert (Levy et al., 2015) oder können die Zählungen mit Laplace geglättet werden (Jurafsky & Martin, 2026). Als Kollokationsmaß ist PMI schwach: Bei vollständig abhängigen Bigrammen steigt der Wert, je seltener sie sind, einmal gesehene Bigramme bekommen überhöhte Werte, und im kanadischen Hansard bevorzugte PMI das falsche Übersetzungspaar (*communes, house*), wo χ² *chambre, house* fand. PMI ist ein gutes Maß für Unabhängigkeit, aber ein schlechtes für Abhängigkeit (Manning & Schütze, 1999).

#### Herkunft und Varianten

Die Tradition geht auf Firths Diktum zurück, dass ein Wort durch seine Umgebung gekennzeichnet ist; eine der ersten Veröffentlichungen zum Finden von Kollokationen war Church & Hanks (1989), die sie für die computergestützte Lexikographie nutzten (Manning & Schütze, 1999). Weitere Maße sind der z-Score und Fishers exakter Test (Manning & Schütze, 1999).

### Wann einsetzen

- Textgenerierung, damit die Ausgabe Fehler wie *powerful tea* vermeidet (Manning & Schütze, 1999).
- Lexikographie und Terminologie-Extraktion, einschließlich einheitlicher Übersetzung von Fachbegriffen (Manning & Schütze, 1999).
- Information Retrieval, wo der Abgleich auf Wendungen statt Einzelwörtern die Genauigkeit verbessern kann (Manning & Schütze, 1999).
- PPMI zur Gewichtung von Wort-Kontext-Kookkurrenzmatrizen (Jurafsky & Martin, 2026).

### Stärken und Grenzen

**Stärken**
- Ein einfaches quantitatives Verfahren plus etwas linguistisches Wissen, etwa Wortarten, reicht weit (Manning & Schütze, 1999).
- Hypothesentests ordnen gleich häufige Bigramme danach, welcher Anteil der Vorkommen jedes Wortes in das Bigramm fällt (Manning & Schütze, 1999).

**Grenzen**
- Keines der Maße funktioniert für seltene Ereignisse gut; PMI leidet am stärksten unter dünnen Daten (Manning & Schütze, 1999).
- Der t-Test setzt normalverteilte Wahrscheinlichkeiten voraus, und χ² ist bei kleinen erwarteten Häufigkeiten ungenau (Manning & Schütze, 1999).
- Maschinell erzeugte Listen erreichen nicht die Qualität manueller Kollokationswörterbücher wie des BBI Combinatory Dictionary (Manning & Schütze, 1999).

### Vergleich

| Verfahren | Findet | Vorbehalt |
|-----------|--------|-----------|
| Häufigkeit + Wortartfilter | Feste Wendungen, Namen | Nicht für flexible Paare |
| Mittelwert und Varianz | Flexible Paare (*knock … door*) | Braucht ein Fenster |
| t-Test | Gerankte abhängige Bigramme | Setzt Normalverteilung voraus |
| χ²-Test | Abhängigkeit, Übersetzungspaare | Schwach bei kleinen Zahlen |
| Likelihood-Quotient | Abhängigkeit, auch seltene Bigramme | – |
| PMI | Stärke der Assoziation | Überhöht bei seltenen Wörtern |

Alle Zeilen: Manning & Schütze (1999).

### In der Praxis

Die statistischen Tests dienen eher dem Ranking der Kandidaten als dem Signifikanztest (Manning & Schütze, 1999). Kollokationen hängen mit der Behandlung von Wendungen im [[information-retrieval|Information Retrieval]] zusammen, und PPMI gewichtet die Wort-Kontext-Kookkurrenzmatrizen, aus denen Wortvektoren entstehen (Jurafsky & Martin, 2026); gelernte Vektoren behandelt [[embeddings|Embeddings]]. Grundlagen zu Hypothesentests stehen in [[statistics-fundamentals|Statistik-Grundlagen]]. In der Analyse von Gender-Bias in Nachrichtenkorpora zeigen die Adjektive, Nomen und Verben mit der höchsten PMI pro Akteur thematische Assoziationen und stereotype Rahmungen; Unterschiede zwischen Geschlechtergruppen weisen auf Bias hin (Urchs, 2025).

### Merksatz

Kollokationen sind konventionelle Wortverbindungen, deren Bedeutung sich nicht ganz aus den Teilen ergibt; man findet sie über Häufigkeit mit Wortartfilter, Abstandsvarianz, Hypothesentests und PMI, wobei PMI Assoziation misst, seltene Paare aber überschätzt.

### Quellen

- Manning, C. D. & Schütze, H. (1999). *Collocations.* Foundations of Statistical Natural Language Processing, Chapter 5. MIT Press. [stanford.edu](https://nlp.stanford.edu/fsnlp/promo/colloc.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Pointwise Mutual Information (PMI).* Speech and Language Processing, 3rd ed. draft, Appendix J. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/J.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
