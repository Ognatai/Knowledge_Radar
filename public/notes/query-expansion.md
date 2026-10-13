---
title_en: Query Expansion and Relevance Feedback
title_de: Query Expansion und Relevance Feedback
entity_type: Method
aliases:
- Relevance feedback
- Pseudo relevance feedback
- Rocchio algorithm
sources:
- https://nlp.stanford.edu/IR-book/pdf/09expand.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Users often describe the same thing with different words than the documents, so a query misses relevant documents. Query expansion and relevance feedback reformulate the query: global methods add related terms independently of the results, for example from a thesaurus, while local methods adjust the query to the documents that the first search returned, as in the Rocchio algorithm, pseudo relevance feedback and implicit feedback from clicks (Manning et al., 2008, ch. 9). They mostly help recall.

### How it works

```text
query ─► search ─► top results ─► feedback: user marks relevant (explicit)
                                          / assume top k relevant (pseudo)
                                          / clicks (implicit)
            ▲                                │
            └── reweighted, expanded query ◄─┘   (local methods)
query ─► + synonyms / related terms from a thesaurus ─► search   (global methods)
```

#### 1. Relevance feedback

The user issues a short query, the system returns results, the user marks some documents as relevant or not, the system computes a better representation of the information need and shows revised results; this can repeat. It works because it is hard to write a good query without knowing the collection, but easy to judge particular documents (Manning et al., 2008, ch. 9).

#### 2. The Rocchio algorithm

In the [[information-retrieval|vector space model]], the query that best separates relevant from non-relevant documents is the difference between their centroids, but the relevant set is unknown. Rocchio's algorithm, popularised by Salton's SMART system around 1970, therefore moves the original query towards the centroid of the known relevant documents and away from the known non-relevant ones: `q_m = α·q_0 + β·centroid(D_r) − γ·centroid(D_nr)`, setting negative term weights to zero. Positive feedback is worth much more than negative, so systems choose γ < β; reasonable values are α = 1, β = 0.75 and γ = 0.15, and many systems use only positive feedback (γ = 0) (Manning et al., 2008, ch. 9).

#### 3. Pseudo relevance feedback

Pseudo (blind) relevance feedback automates the user's part: it assumes the top k results of an ordinary search are relevant and runs relevance feedback on them. It mostly works and has improved results in the TREC ad hoc task, but it can drift: for a query about copper mines whose top results are all about mines in Chile, the expanded query drifts towards Chile (Manning et al., 2008, ch. 9).

#### 4. Implicit feedback

Implicit feedback uses indirect evidence such as clicks: DirectHit ranked pages higher that users chose to look at more often. It is less reliable than explicit feedback but more useful than pseudo relevance feedback, and easy to collect in large quantities in high-volume systems such as web search (Manning et al., 2008, ch. 9).

#### 5. Global methods: thesauri

Global methods expand query terms independently of the results: by showing users which terms were dropped or stemmed and suggesting terms, by a manual thesaurus or controlled vocabulary, or by an automatically generated thesaurus. An automatic thesaurus can be built from word co-occurrence, for example as the term-term similarity matrix C = A·Aᵀ of a length-normalised term-document matrix A, or from grammatical relations, which is more accurate but depends on the parser. Ambiguity introduces errors: a query for Apple computer may expand to Apple red fruit computer (Manning et al., 2008, ch. 9).

#### Origin and variants

Rocchio's algorithm dates from around 1970 (Manning et al., 2008, ch. 9). Dimensionality reduction with [[latent-semantic-indexing|latent semantic indexing]] can refine automatically derived thesauri (Manning et al., 2008, ch. 9).

### When to use it

- When recall matters and users are willing to review results and iterate, the setting in which relevance feedback has been most useful (Manning et al., 2008, ch. 9).
- Pseudo relevance feedback to improve ranked retrieval without user interaction, for example on top of [[bm25|BM25]] (Manning et al., 2008, ch. 9).
- A domain-specific thesaurus when users and documents use different vocabularies (Manning et al., 2008, ch. 9).

### Strengths and limitations

**Strengths**
- Improves recall, and with good feedback also precision (Manning et al., 2008, ch. 9).
- Pseudo relevance feedback needs no user interaction (Manning et al., 2008, ch. 9).
- Implicit feedback can be collected in large quantities (Manning et al., 2008, ch. 9).

**Limitations**
- Relevance feedback cannot fix misspellings, cross-language queries or a mismatch between the user's and the collection's vocabulary, such as laptop versus notebook computer (Manning et al., 2008, ch. 9).
- Rocchio treats the relevant documents as one cluster; it works poorly when they form several clusters, as with Burma versus Myanmar or disjunctive answers (Manning et al., 2008, ch. 9).
- Pseudo feedback can drift, explicit feedback is onerous for users, and manual thesauri are costly to build and maintain (Manning et al., 2008, ch. 9).

### Comparison

| Method | Input | Risk |
|--------|-------|------|
| Explicit relevance feedback | User judges results (Manning et al., 2008, ch. 9) | Effort for users |
| Pseudo relevance feedback | Top k results assumed relevant (Manning et al., 2008, ch. 9) | Query drift |
| Implicit feedback | Clicks and other behaviour (Manning et al., 2008, ch. 9) | Clicks reflect snippets, not relevance |
| Thesaurus expansion | Synonyms and related terms (Manning et al., 2008, ch. 9) | Ambiguous expansions |

### In practice

Relevance feedback needs queries whose set of relevant documents is medium to large; in many cases other forms of interactive retrieval improve relevance about as much with less work (Manning et al., 2008, ch. 9). Beyond ad hoc search, it serves to follow a changing information need, to maintain information filters such as news feeds, and in active learning (Manning et al., 2008, ch. 9).

### Key takeaway

Query expansion adds related terms to a query, and relevance feedback moves the query towards documents known or assumed to be relevant; both raise recall but can drift when the feedback or the expansion is wrong.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Relevance feedback and query expansion.* Introduction to Information Retrieval, Chapter 9. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/09expand.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Nutzer beschreiben dieselbe Sache oft mit anderen Wörtern als die Dokumente, sodass eine Anfrage relevante Dokumente verfehlt. Query Expansion und Relevance Feedback formulieren die Anfrage um: Globale Methoden ergänzen verwandte Terme unabhängig von den Ergebnissen, etwa aus einem Thesaurus, lokale Methoden passen die Anfrage an die Dokumente an, die die erste Suche geliefert hat, wie der Rocchio-Algorithmus, Pseudo Relevance Feedback und implizites Feedback aus Klicks (Manning et al., 2008, Kap. 9). Sie helfen vor allem dem Recall.

### Funktionsweise

```text
Anfrage ─► Suche ─► Top-Ergebnisse ─► Feedback: Nutzer markiert relevante (explizit)
                                              / Top k gelten als relevant (pseudo)
                                              / Klicks (implizit)
            ▲                                    │
            └── neu gewichtete, erweiterte Anfrage ◄┘   (lokale Methoden)
Anfrage ─► + Synonyme / verwandte Terme aus einem Thesaurus ─► Suche   (globale Methoden)
```

#### 1. Relevance Feedback

Der Nutzer stellt eine kurze Anfrage, das System liefert Ergebnisse, der Nutzer markiert einige Dokumente als relevant oder nicht, das System berechnet daraus eine bessere Darstellung des Informationsbedarfs und zeigt überarbeitete Ergebnisse; das kann sich wiederholen. Es funktioniert, weil es schwer ist, ohne Kenntnis der Sammlung eine gute Anfrage zu formulieren, aber leicht, einzelne Dokumente zu beurteilen (Manning et al., 2008, Kap. 9).

#### 2. Der Rocchio-Algorithmus

Im Vektorraummodell ist die Anfrage, die relevante und nicht relevante Dokumente am besten trennt, die Differenz ihrer Zentroide, doch die relevante Menge ist unbekannt. Rocchios Algorithmus, um 1970 durch Saltons SMART-System bekannt geworden, verschiebt daher die ursprüngliche Anfrage zum Zentroid der bekannten relevanten Dokumente hin und von dem der bekannten nicht relevanten weg: `q_m = α·q_0 + β·Zentroid(D_r) − γ·Zentroid(D_nr)`, wobei negative Termgewichte auf null gesetzt werden. Positives Feedback ist viel wertvoller als negatives, daher wählen Systeme γ < β; sinnvolle Werte sind α = 1, β = 0,75 und γ = 0,15, und viele Systeme nutzen nur positives Feedback (γ = 0) (Manning et al., 2008, Kap. 9).

#### 3. Pseudo Relevance Feedback

Pseudo (Blind) Relevance Feedback automatisiert den Teil des Nutzers: Es nimmt an, dass die Top-k-Ergebnisse einer normalen Suche relevant sind, und führt darauf Relevance Feedback aus. Das funktioniert meist und hat die Ergebnisse in der TREC-Ad-hoc-Aufgabe verbessert, kann aber abdriften: Handeln bei einer Anfrage zu Kupferminen alle Top-Ergebnisse von Minen in Chile, driftet die erweiterte Anfrage Richtung Chile (Manning et al., 2008, Kap. 9).

#### 4. Implizites Feedback

Implizites Feedback nutzt indirekte Hinweise wie Klicks: DirectHit rankte Seiten höher, die Nutzer häufiger aufriefen. Es ist weniger verlässlich als explizites Feedback, aber nützlicher als Pseudo Relevance Feedback und in Systemen mit vielen Anfragen wie der Websuche leicht in großen Mengen zu sammeln (Manning et al., 2008, Kap. 9).

#### 5. Globale Methoden: Thesauri

Globale Methoden erweitern Anfrageterme unabhängig von den Ergebnissen: indem sie Nutzern zeigen, welche Terme weggelassen oder gestemmt wurden, und Terme vorschlagen, über einen manuellen Thesaurus oder ein kontrolliertes Vokabular oder über einen automatisch erzeugten Thesaurus. Ein automatischer Thesaurus lässt sich aus dem gemeinsamen Vorkommen von Wörtern bauen, etwa als Term-Term-Ähnlichkeitsmatrix C = A·Aᵀ einer längennormierten Term-Dokument-Matrix A, oder aus grammatischen Relationen, was genauer ist, aber vom Parser abhängt. Mehrdeutigkeit führt zu Fehlern: Eine Anfrage nach Apple computer kann zu Apple red fruit computer erweitert werden (Manning et al., 2008, Kap. 9).

#### Herkunft und Varianten

Rocchios Algorithmus stammt aus der Zeit um 1970 (Manning et al., 2008, Kap. 9). Dimensionsreduktion mit [[latent-semantic-indexing|Latent Semantic Indexing]] kann automatisch abgeleitete Thesauri verfeinern (Manning et al., 2008, Kap. 9).

### Wann einsetzen

- Wenn der Recall wichtig ist und Nutzer bereit sind, Ergebnisse zu prüfen und nachzufassen, das Szenario, in dem Relevance Feedback am nützlichsten war (Manning et al., 2008, Kap. 9).
- Pseudo Relevance Feedback, um gerankte Suche ohne Nutzerinteraktion zu verbessern, etwa auf Basis von [[bm25|BM25]] (Manning et al., 2008, Kap. 9).
- Einen domänenspezifischen Thesaurus, wenn Nutzer und Dokumente unterschiedliche Vokabulare verwenden (Manning et al., 2008, Kap. 9).

### Stärken und Grenzen

**Stärken**
- Verbessert den Recall und bei gutem Feedback auch die Precision (Manning et al., 2008, Kap. 9).
- Pseudo Relevance Feedback braucht keine Nutzerinteraktion (Manning et al., 2008, Kap. 9).
- Implizites Feedback lässt sich in großen Mengen sammeln (Manning et al., 2008, Kap. 9).

**Grenzen**
- Relevance Feedback hilft nicht bei Tippfehlern, sprachübergreifenden Anfragen oder einem Unterschied zwischen dem Vokabular des Nutzers und der Sammlung, etwa laptop gegenüber notebook computer (Manning et al., 2008, Kap. 9).
- Rocchio behandelt die relevanten Dokumente als einen Cluster; es funktioniert schlecht, wenn sie mehrere Cluster bilden, etwa bei Burma und Myanmar oder disjunktiven Antworten (Manning et al., 2008, Kap. 9).
- Pseudo Feedback kann abdriften, explizites Feedback ist für Nutzer mühsam, und manuelle Thesauri sind teuer in Aufbau und Pflege (Manning et al., 2008, Kap. 9).

### Vergleich

| Methode | Eingabe | Risiko |
|---------|---------|--------|
| Explizites Relevance Feedback | Nutzer bewertet Ergebnisse (Manning et al., 2008, Kap. 9) | Aufwand für Nutzer |
| Pseudo Relevance Feedback | Top-k-Ergebnisse gelten als relevant (Manning et al., 2008, Kap. 9) | Abdriften der Anfrage |
| Implizites Feedback | Klicks und anderes Verhalten (Manning et al., 2008, Kap. 9) | Klicks spiegeln Snippets, nicht Relevanz |
| Thesaurus-Erweiterung | Synonyme und verwandte Terme (Manning et al., 2008, Kap. 9) | Mehrdeutige Erweiterungen |

### In der Praxis

Relevance Feedback braucht Anfragen mit einer mittleren bis großen Menge relevanter Dokumente; in vielen Fällen verbessern andere Formen interaktiver Suche die Relevanz ähnlich stark mit weniger Aufwand (Manning et al., 2008, Kap. 9). Über die Ad-hoc-Suche hinaus dient es dazu, einem sich ändernden Informationsbedarf zu folgen, Informationsfilter wie Newsfeeds zu pflegen und beim Active Learning (Manning et al., 2008, Kap. 9).

### Merksatz

Query Expansion ergänzt eine Anfrage um verwandte Terme, Relevance Feedback verschiebt sie zu Dokumenten, die als relevant bekannt sind oder angenommen werden; beide erhöhen den Recall, können aber abdriften, wenn Feedback oder Erweiterung falsch sind.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Relevance feedback and query expansion.* Introduction to Information Retrieval, Chapter 9. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/09expand.pdf)
