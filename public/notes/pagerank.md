---
title_en: PageRank and Link Analysis
title_de: PageRank und Linkanalyse
entity_type: Method
aliases:
- PageRank
- Link analysis
- HITS
- Hubs and authorities
- Topic-specific PageRank
sources:
- https://nlp.stanford.edu/IR-book/pdf/21link.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Link analysis treats a hyperlink from one page to another as an endorsement, much as citation analysis treats citations among scholarly articles (Manning et al., 2008, ch. 21). PageRank gives every page a score between 0 and 1: the fraction of time a random surfer spends on it while following links and occasionally teleporting to a random page; it is the steady state of a [[hidden-markov-models|Markov chain]] and is computed by power iteration. HITS instead computes, for each query, hub scores (pages that point to good authorities) and authority scores (pages pointed to by good hubs) (Manning et al., 2008, ch. 21).

### How it works

```text
web graph (adjacency matrix A)
   │  rows normalised, dead ends → teleport, mix with teleport probability α
   ▼
transition matrix P  ──power iteration──►  steady state π  =  PageRank of every page
query ─► root set ─► base set (+ in/out links) ─► hub and authority scores (HITS)
```

#### 1. Two intuitions

Link analysis rests on two ideas: the anchor text of a link to page B describes B well, and a link from A to B endorses B. Not every link is an endorsement, such as template links to a copyright notice on every page of a site, so implementations typically discount links within a site. Counting in-links alone is not robust, because people create pages that link to a target to boost it (link spam) (Manning et al., 2008, ch. 21).

#### 2. The random surfer with teleport

A random surfer starts at a page and at each step follows one of its out-links, chosen uniformly. Pages visited more often in this walk are more important. To handle pages without out-links, the surfer teleports to a page chosen uniformly from all N pages; at pages with out-links, it teleports with probability α and follows a link with probability 1 − α, with α typically about 0.1 (Manning et al., 2008, ch. 21).

#### 3. The Markov chain

The surfer is a Markov chain with one state per page. The transition matrix P is derived from the adjacency matrix A: a row without links becomes 1/N everywhere; otherwise each 1 is divided by the number of links in its row, the matrix is multiplied by 1 − α, and α/N is added to every entry. Teleporting makes the chain ergodic, and every ergodic chain has a unique steady-state distribution π, the principal left eigenvector of P with eigenvalue 1; π(v) is the PageRank of page v (Manning et al., 2008, ch. 21).

#### 4. Computing PageRank

Power iteration starts from any distribution x and multiplies it by P repeatedly; for large t, x·P^t settles into the steady state, independently of the start, and the iteration stops when the change falls below a threshold. Any other method for the principal eigenvector also works (Manning et al., 2008, ch. 21).

#### 5. Topic-specific and personalised PageRank

If the surfer teleports only to pages on one topic, such as a set of sports pages from a directory, the steady state is a topic-specific PageRank. A user with mixed interests, say 60 % sports and 40 % politics, gets a personalised PageRank that is the linear combination 0.6·π_sports + 0.4·π_politics of the topic-specific vectors, so no separate computation per user is needed (Manning et al., 2008, ch. 21).

#### 6. HITS: hubs and authorities

HITS (Hyperlink-Induced Topic Search) assigns two scores per query: a good hub points to many good authorities, and a good authority is pointed to by many good hubs. Starting from h = a = 1, the scores are updated alternately, which amounts to power iteration for the principal eigenvectors of A·Aᵀ (hubs) and Aᵀ·A (authorities). The subset of the web is built from a root set of about 200 pages matching the query, expanded to a base set with all pages linking to or linked from it; about five iterations give a good ordering of the top hubs and authorities (Manning et al., 2008, ch. 21).

#### Origin and variants

Link analysis has its roots in citation analysis and bibliometrics (Manning et al., 2008, ch. 21).

### When to use it

- As a query-independent quality signal in web search, combined with hundreds of other features such as [[text-similarity-metrics|cosine similarity]] and term proximity into one ranking score (Manning et al., 2008, ch. 21).
- To prioritise which pages a crawler fetches next ([[web-crawling|Web Crawling]]; Manning et al., 2008, ch. 21).
- HITS for broad informational topics, where authoritative pages may not even contain the query terms (Manning et al., 2008, ch. 21).

### Strengths and limitations

**Strengths**
- Links are prevalent and dependable enough to derive useful ranking signals from them (Manning et al., 2008, ch. 21).
- A unique, well-defined score thanks to the ergodic Markov chain (Manning et al., 2008, ch. 21).
- Personalised variants come from linear combinations of a few topic vectors (Manning et al., 2008, ch. 21).

**Limitations**
- Links do not always endorse, and link spam tries to inflate in-links (Manning et al., 2008, ch. 21).
- PageRank alone says nothing about relevance to a query; it is one feature among many (Manning et al., 2008, ch. 21).
- HITS must be computed per query on a base set built at query time (Manning et al., 2008, ch. 21).

### Comparison

| Method | Depends on the query | Output |
|--------|---------------------|--------|
| In-link count | No | Number of links; easy to spam (Manning et al., 2008, ch. 21) |
| PageRank | No | One score per page (Manning et al., 2008, ch. 21) |
| Topic-specific PageRank | Via the user's topics | One score per page and topic (Manning et al., 2008, ch. 21) |
| HITS | Yes | Hub and authority score per page (Manning et al., 2008, ch. 21) |

### In practice

Anchor text is indexed as terms of the target page, usually with a lower weight than in-page terms, which also makes it a target for abuse, such as derogatory anchor text pointing to a company (Manning et al., 2008, ch. 21). For HITS, exact scores are not needed, only the order of the top pages, so a few iterations suffice; because the web graph is sparse, with about ten links per page, the updates are done as additive sums rather than matrix products (Manning et al., 2008, ch. 21).

### Key takeaway

PageRank scores a page by how often a random surfer with occasional teleports visits it, computed as the steady state of a Markov chain; HITS separates hubs from authorities for a query.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Link analysis.* Introduction to Information Retrieval, Chapter 21. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/21link.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Linkanalyse behandelt einen Hyperlink von einer Seite auf eine andere als Empfehlung, so wie die Zitationsanalyse Zitate zwischen wissenschaftlichen Artikeln behandelt (Manning et al., 2008, Kap. 21). PageRank gibt jeder Seite einen Wert zwischen 0 und 1: den Anteil der Zeit, den ein zufälliger Surfer auf ihr verbringt, wenn er Links folgt und gelegentlich auf eine zufällige Seite springt; er ist der stationäre Zustand einer Markov-Kette und wird per Power Iteration berechnet. HITS berechnet stattdessen pro Anfrage Hub-Werte (Seiten, die auf gute Autoritäten verweisen) und Authority-Werte (Seiten, auf die gute Hubs verweisen) (Manning et al., 2008, Kap. 21).

### Funktionsweise

```text
Web-Graph (Adjazenzmatrix A)
   │  Zeilen normiert, Sackgassen → Teleport, Mischung mit Teleport-Wahrscheinlichkeit α
   ▼
Übergangsmatrix P  ──Power Iteration──►  stationärer Zustand π  =  PageRank jeder Seite
Anfrage ─► Root Set ─► Base Set (+ ein-/ausgehende Links) ─► Hub- und Authority-Werte (HITS)
```

#### 1. Zwei Annahmen

Linkanalyse beruht auf zwei Ideen: Der Ankertext eines Links auf Seite B beschreibt B gut, und ein Link von A auf B ist eine Empfehlung für B. Nicht jeder Link ist eine Empfehlung, etwa Vorlagen-Links auf einen Copyright-Hinweis auf jeder Seite einer Website, daher werten Implementierungen Links innerhalb einer Website meist ab. Nur eingehende Links zu zählen ist nicht robust, weil Leute Seiten anlegen, die auf ein Ziel verlinken, um es zu stärken (Link-Spam) (Manning et al., 2008, Kap. 21).

#### 2. Der zufällige Surfer mit Teleport

Ein zufälliger Surfer beginnt auf einer Seite und folgt in jedem Schritt einem ihrer ausgehenden Links, gleichverteilt gewählt. Seiten, die er dabei öfter besucht, sind wichtiger. Für Seiten ohne ausgehende Links springt der Surfer auf eine gleichverteilt gewählte Seite aus allen N Seiten; auf Seiten mit Links springt er mit Wahrscheinlichkeit α und folgt mit Wahrscheinlichkeit 1 − α einem Link, wobei α typischerweise etwa 0,1 ist (Manning et al., 2008, Kap. 21).

#### 3. Die Markov-Kette

Der Surfer ist eine Markov-Kette mit einem Zustand pro Seite. Die Übergangsmatrix P entsteht aus der Adjazenzmatrix A: Eine Zeile ohne Links wird überall 1/N; sonst wird jede 1 durch die Zahl der Links ihrer Zeile geteilt, die Matrix mit 1 − α multipliziert und zu jedem Eintrag α/N addiert. Der Teleport macht die Kette ergodisch, und jede ergodische Kette hat eine eindeutige stationäre Verteilung π, den linken Haupteigenvektor von P zum Eigenwert 1; π(v) ist der PageRank der Seite v (Manning et al., 2008, Kap. 21).

#### 4. PageRank berechnen

Power Iteration beginnt mit einer beliebigen Verteilung x und multipliziert sie wiederholt mit P; für großes t pendelt sich x·P^t unabhängig vom Start auf den stationären Zustand ein, und die Iteration endet, wenn die Änderung unter eine Schwelle fällt. Jedes andere Verfahren für den Haupteigenvektor funktioniert ebenfalls (Manning et al., 2008, Kap. 21).

#### 5. Themenspezifischer und personalisierter PageRank

Springt der Surfer nur auf Seiten zu einem Thema, etwa eine Menge von Sportseiten aus einem Verzeichnis, ist der stationäre Zustand ein themenspezifischer PageRank. Ein Nutzer mit gemischten Interessen, etwa 60 % Sport und 40 % Politik, erhält einen personalisierten PageRank als Linearkombination 0,6·π_Sport + 0,4·π_Politik der themenspezifischen Vektoren, sodass keine eigene Berechnung pro Nutzer nötig ist (Manning et al., 2008, Kap. 21).

#### 6. HITS: Hubs und Authorities

HITS (Hyperlink-Induced Topic Search) vergibt pro Anfrage zwei Werte: Ein guter Hub verweist auf viele gute Authorities, und eine gute Authority wird von vielen guten Hubs verlinkt. Ausgehend von h = a = 1 werden die Werte abwechselnd aktualisiert, was einer Power Iteration für die Haupteigenvektoren von A·Aᵀ (Hubs) und Aᵀ·A (Authorities) entspricht. Die Teilmenge des Webs entsteht aus einem Root Set von etwa 200 Seiten, die zur Anfrage passen, erweitert zu einem Base Set mit allen Seiten, die darauf verlinken oder von ihm verlinkt werden; etwa fünf Iterationen ergeben eine gute Reihenfolge der besten Hubs und Authorities (Manning et al., 2008, Kap. 21).

#### Herkunft und Varianten

Linkanalyse hat ihre Wurzeln in der Zitationsanalyse und Bibliometrie (Manning et al., 2008, Kap. 21).

### Wann einsetzen

- Als anfrageunabhängiges Qualitätssignal in der Websuche, kombiniert mit Hunderten anderer Merkmale wie [[text-similarity-metrics|Cosine Similarity]] und Termnähe zu einem Ranking-Wert (Manning et al., 2008, Kap. 21).
- Um zu priorisieren, welche Seiten ein Crawler als Nächstes holt ([[web-crawling|Web-Crawling]]; Manning et al., 2008, Kap. 21).
- HITS für breite Informationsthemen, bei denen maßgebliche Seiten die Anfrageterme vielleicht gar nicht enthalten (Manning et al., 2008, Kap. 21).

### Stärken und Grenzen

**Stärken**
- Links sind verbreitet und verlässlich genug, um daraus nützliche Ranking-Signale abzuleiten (Manning et al., 2008, Kap. 21).
- Ein eindeutiger, wohldefinierter Wert dank der ergodischen Markov-Kette (Manning et al., 2008, Kap. 21).
- Personalisierte Varianten entstehen aus Linearkombinationen weniger Themenvektoren (Manning et al., 2008, Kap. 21).

**Grenzen**
- Links empfehlen nicht immer, und Link-Spam versucht, eingehende Links aufzublähen (Manning et al., 2008, Kap. 21).
- PageRank allein sagt nichts über die Relevanz für eine Anfrage; er ist ein Merkmal unter vielen (Manning et al., 2008, Kap. 21).
- HITS muss pro Anfrage auf einem zur Anfragezeit gebauten Base Set berechnet werden (Manning et al., 2008, Kap. 21).

### Vergleich

| Verfahren | Hängt von der Anfrage ab | Ergebnis |
|-----------|-------------------------|----------|
| Zahl eingehender Links | Nein | Linkanzahl; leicht zu manipulieren (Manning et al., 2008, Kap. 21) |
| PageRank | Nein | Ein Wert pro Seite (Manning et al., 2008, Kap. 21) |
| Themenspezifischer PageRank | Über die Themen des Nutzers | Ein Wert pro Seite und Thema (Manning et al., 2008, Kap. 21) |
| HITS | Ja | Hub- und Authority-Wert pro Seite (Manning et al., 2008, Kap. 21) |

### In der Praxis

Ankertext wird als Term der Zielseite indexiert, meist schwächer gewichtet als Terme auf der Seite selbst, was ihn auch zum Ziel von Missbrauch macht, etwa abwertenden Ankertexten, die auf ein Unternehmen zeigen (Manning et al., 2008, Kap. 21). Für HITS braucht es keine exakten Werte, nur die Reihenfolge der besten Seiten, daher reichen wenige Iterationen; weil der Web-Graph dünn besetzt ist, mit etwa zehn Links pro Seite, werden die Aktualisierungen als Summen statt als Matrixprodukte berechnet (Manning et al., 2008, Kap. 21).

### Merksatz

PageRank bewertet eine Seite danach, wie oft ein zufälliger Surfer mit gelegentlichen Sprüngen sie besucht, berechnet als stationärer Zustand einer Markov-Kette; HITS trennt für eine Anfrage Hubs von Authorities.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Link analysis.* Introduction to Information Retrieval, Chapter 21. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/21link.pdf)
