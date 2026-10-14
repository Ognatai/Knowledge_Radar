---
title_en: Reciprocal Rank Fusion (RRF)
title_de: Reciprocal Rank Fusion (RRF)
entity_type: Method
aliases:
- Reciprocal rank fusion
- RRF
- Rank fusion
sources:
- https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
- https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Reciprocal Rank Fusion (RRF) merges several ranked result lists into one by giving each document the sum of `1 / (k + rank)` over all lists in which it appears, with `k = 60` (Cormack et al., 2009). Because it uses only ranks, not scores, it can combine systems whose scores are on incompatible scales, such as BM25 and vector similarity, which makes it a common way to merge results in hybrid search, for example in Azure AI Search (Microsoft Learn). In the original experiments, RRF beat every individual system it combined and the established fusion methods Condorcet Fuse and CombMNZ, without any training (Cormack et al., 2009).

### How it works

```text
query → system 1 (e.g. BM25)     → ranking r₁
      → system 2 (e.g. dense)    → ranking r₂
      → …                        → ranking rₙ
 ▼
for each document d:  RRF(d) = Σ_r  1 / (k + r(d))      (k = 60; documents missing from a list add nothing)
 ▼
sort by RRF(d) → fused ranking (optionally reranked afterwards)
```

#### 1. The formula

Given a set of documents D and a set of rankings R, RRF computes `RRFscore(d) = Σ_{r ∈ R} 1 / (k + r(d))` and sorts by this score (Cormack et al., 2009). The intuition is that highly ranked documents matter more, but the importance of lower ranks does not vanish as it would with an exponential weighting; the constant k dampens the influence of a very high rank from a single outlier system. Cormack et al. (2009) fixed `k = 60` in a pilot experiment, where values between about 10 and 100 performed almost equally well and the choice was not critical. The formula needs no voting algorithm or global information: ranks can be computed and summed one system at a time (Cormack et al., 2009).

#### 2. Why ranks instead of scores

Different retrieval methods produce scores with different ranges: BM25 has no upper limit, [[text-similarity-metrics|cosine similarity]] of vectors lies within a fixed range, and rerankers use their own scales (Microsoft Learn). Combining raw scores therefore needs normalisation and weights, whereas RRF ignores the arbitrary scores and only uses positions, like Condorcet Fuse (Cormack et al., 2009). One or two systems that rank a document highly can lift it considerably, which Cormack et al. (2009) suspect is why RRF exploits the diversity of the input rankings better than Condorcet, where a majority of weak preferences can overrule stronger ones.

#### 3. Hybrid search

In Azure AI Search, RRF is applied whenever several queries run in parallel, for example a full-text BM25 query plus one or more vector queries; each produces a ranked list, each document gets `1/(rank + k)` per list, and the sums give the fused ranking (Microsoft Learn). The fused score is bounded by the number of lists, each contributing at most about `1/k`. Individual vector queries can be weighted, and a semantic reranker can reorder the fused results afterwards (Microsoft Learn). The same pattern is used in RAG pipelines that combine [[bm25|BM25]] with [[dense-passage-retrieval|dense retrieval]], see [[rag-retrieval|RAG retrieval]].

#### 4. Evidence

In pilot runs combining 30 configurations of one search engine on TREC collections and in fusions of real TREC submissions, RRF outperformed Condorcet, CombMNZ and the best individual system by 4 to 5% on average in mean average [[classification-metrics|precision]]; it beat Condorcet in all seven tests and the best automatic system in every case (Cormack et al., 2009). On the LETOR 3 learning-to-rank benchmark, fusing the supplied learning-to-rank baselines with RRF beat every individual method, by 0.02 MAP (4%) over the best, giving the best result reported on that dataset at the time; CombMNZ was slightly but not significantly better than RRF there (Cormack et al., 2009).

#### Origin and variants

Gordon Cormack, Charles Clarke and Stefan Büttcher proposed RRF at SIGIR 2009 originally as a baseline for learning-to-rank experiments, and found it hard to beat (Cormack et al., 2009). Variants weight the contribution of each list, as Azure AI Search does for vector queries (Microsoft Learn).

### When to use it

- Combining lexical and vector search in hybrid retrieval, where scores are not comparable (Microsoft Learn).
- Merging results from several query formulations or several vector fields ([[query-expansion|query expansion]], Microsoft Learn).
- Any metasearch setting without training data for a learned combination (Cormack et al., 2009).

### Strengths and limitations

**Strengths**
- Simple, unsupervised and robust to the choice of k (Cormack et al., 2009).
- Independent of score scales (Cormack et al., 2009; Microsoft Learn).
- Consistently at least as good as the best input ranking in the original experiments (Cormack et al., 2009).

**Limitations**
- Ignores score magnitudes, so a document that one system finds clearly better is treated like any other at the same rank (Cormack et al., 2009).
- The fused score is not a calibrated relevance estimate; its upper bound depends on the number of lists (Microsoft Learn).
- A fused list still benefits from a reranker for the final ordering ([[cross-encoder|cross-encoders]]).

### Comparison

| Method | Input | Combination | Training |
|---|---|---|---|
| RRF | ranks | sum of 1/(k + rank) | none |
| Condorcet Fuse | ranks | pairwise majority vote | none |
| CombMNZ | scores | sum of scores × number of systems returning the document | none, but scores must be comparable |
| Learning to rank | features | learned model | labelled data |

Source: Cormack et al. (2009).

### In practice

Each retriever is asked for more candidates than the final cut-off, so that documents found by only one system can still enter the fused list; in Azure AI Search, the full-text side can contribute up to 1,000 matches and the top 50 fused results are returned by default (Microsoft Learn). The fused list is often passed to a [[cross-encoder|cross-encoder]] reranker before the top passages go to the LLM ([[retrieval-augmented-generation|RAG]]).

### Key takeaway

RRF fuses rankings by summing 1/(60 + rank) per document, needs no training or score normalisation, and reliably matches or beats the best single system, which makes it a common choice for hybrid lexical and vector search.

### Sources

- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [plg.uwaterloo.ca](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- Microsoft Learn. *Hybrid search scoring (RRF).* Azure AI Search documentation. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Reciprocal Rank Fusion (RRF) führt mehrere Ergebnislisten zu einer zusammen, indem jedes Dokument die Summe von `1 / (k + Rang)` über alle Listen erhält, in denen es vorkommt, mit `k = 60` (Cormack et al., 2009). Weil es nur Ränge und keine Scores nutzt, kann es Systeme kombinieren, deren Scores auf unvereinbaren Skalen liegen, etwa BM25 und Vektorähnlichkeit; deshalb ist es ein verbreitetes Verfahren, um Ergebnisse in der hybriden Suche zusammenzuführen, etwa in Azure AI Search (Microsoft Learn). In den ursprünglichen Experimenten übertraf RRF jedes einzelne kombinierte System und die etablierten Fusionsverfahren Condorcet Fuse und CombMNZ, ohne jedes Training (Cormack et al., 2009).

### Funktionsweise

```text
Anfrage → System 1 (z. B. BM25)   → Ranking r₁
        → System 2 (z. B. dicht)  → Ranking r₂
        → …                       → Ranking rₙ
 ▼
für jedes Dokument d:  RRF(d) = Σ_r  1 / (k + r(d))      (k = 60; fehlt d in einer Liste, trägt sie nichts bei)
 ▼
nach RRF(d) sortieren → fusioniertes Ranking (optional danach Reranking)
```

#### 1. Die Formel

Für eine Menge von Dokumenten D und eine Menge von Rankings R berechnet RRF `RRFscore(d) = Σ_{r ∈ R} 1 / (k + r(d))` und sortiert nach diesem Wert (Cormack et al., 2009). Die Idee: Hoch platzierte Dokumente zählen mehr, doch die Bedeutung niedrigerer Ränge verschwindet nicht, wie es bei exponentieller Gewichtung der Fall wäre; die Konstante k dämpft den Einfluss eines sehr hohen Rangs aus einem einzelnen Ausreißer-System. Cormack et al. (2009) legten `k = 60` in einem Vorversuch fest, in dem Werte zwischen etwa 10 und 100 nahezu gleich gut abschnitten und die Wahl nicht entscheidend war. Die Formel braucht keinen Abstimmungsalgorithmus und keine globalen Informationen: Ränge lassen sich System für System berechnen und aufsummieren (Cormack et al., 2009).

#### 2. Warum Ränge statt Scores

Verschiedene Retrieval-Verfahren liefern Scores mit unterschiedlichen Wertebereichen: BM25 hat keine Obergrenze, die [[text-similarity-metrics|Cosine Similarity]] von Vektoren liegt in einem festen Bereich, und Reranker nutzen eigene Skalen (Microsoft Learn). Rohscores zu kombinieren, erfordert daher Normalisierung und Gewichte, während RRF wie Condorcet Fuse die willkürlichen Scores ignoriert und nur Positionen nutzt (Cormack et al., 2009). Ein oder zwei Systeme, die ein Dokument hoch einstufen, können es deutlich nach oben bringen; Cormack et al. (2009) vermuten, dass RRF deshalb die Vielfalt der Eingangsrankings besser nutzt als Condorcet, bei dem eine Mehrheit schwacher Präferenzen stärkere überstimmen kann.

#### 3. Hybride Suche

In Azure AI Search kommt RRF zum Einsatz, sobald mehrere Abfragen parallel laufen, etwa eine Volltextabfrage mit BM25 und eine oder mehrere Vektorabfragen; jede liefert eine geordnete Liste, jedes Dokument erhält je Liste `1/(rank + k)`, und die Summen ergeben das fusionierte Ranking (Microsoft Learn). Der fusionierte Score ist durch die Zahl der Listen begrenzt, von denen jede höchstens etwa `1/k` beiträgt. Einzelne Vektorabfragen lassen sich gewichten, und ein semantischer Reranker kann die fusionierten Ergebnisse danach neu ordnen (Microsoft Learn). Dasselbe Muster nutzen RAG-Pipelines, die [[bm25|BM25]] mit [[dense-passage-retrieval|Dense Retrieval]] kombinieren, siehe [[rag-retrieval|RAG: Retrieval]].

#### 4. Belege

In Vorversuchen, die 30 Konfigurationen einer Suchmaschine auf TREC-Sammlungen kombinierten, und bei der Fusion echter TREC-Einreichungen übertraf RRF Condorcet, CombMNZ und das beste einzelne System im Mittel um 4 bis 5 % in der Mean Average [[classification-metrics|Precision]]; es schlug Condorcet in allen sieben Tests und das beste automatische System in jedem Fall (Cormack et al., 2009). Auf dem Learning-to-Rank-Benchmark LETOR 3 übertraf die RRF-Fusion der mitgelieferten Learning-to-Rank-Baselines jede einzelne Methode, um 0,02 MAP (4 %) gegenüber der besten, und lieferte das damals beste berichtete Ergebnis auf diesem Datensatz; CombMNZ war dort knapp, aber nicht signifikant besser als RRF (Cormack et al., 2009).

#### Herkunft und Varianten

Gordon Cormack, Charles Clarke und Stefan Büttcher schlugen RRF auf der SIGIR 2009 ursprünglich als Baseline für Learning-to-Rank-Experimente vor und stellten fest, dass es schwer zu schlagen war (Cormack et al., 2009). Varianten gewichten den Beitrag jeder Liste, wie Azure AI Search bei Vektorabfragen (Microsoft Learn).

### Wann einsetzen

- Lexikalische und Vektorsuche im hybriden Retrieval kombinieren, wenn die Scores nicht vergleichbar sind (Microsoft Learn).
- Ergebnisse mehrerer Anfrageformulierungen oder mehrerer Vektorfelder zusammenführen ([[query-expansion|Query Expansion]], Microsoft Learn).
- Jede Metasuche ohne Trainingsdaten für eine gelernte Kombination (Cormack et al., 2009).

### Stärken und Grenzen

**Stärken**
- Einfach, unüberwacht und robust gegenüber der Wahl von k (Cormack et al., 2009).
- Unabhängig von den Skalen der Scores (Cormack et al., 2009; Microsoft Learn).
- In den ursprünglichen Experimenten durchweg mindestens so gut wie das beste Eingangsranking (Cormack et al., 2009).

**Grenzen**
- Ignoriert die Höhe der Scores, sodass ein Dokument, das ein System klar besser findet, wie jedes andere auf demselben Rang behandelt wird (Cormack et al., 2009).
- Der fusionierte Score ist keine kalibrierte Relevanzschätzung; seine Obergrenze hängt von der Zahl der Listen ab (Microsoft Learn).
- Eine fusionierte Liste profitiert für die endgültige Reihenfolge weiterhin von einem Reranker ([[cross-encoder|Cross-Encoder]]).

### Vergleich

| Verfahren | Eingabe | Kombination | Training |
|---|---|---|---|
| RRF | Ränge | Summe von 1/(k + Rang) | keines |
| Condorcet Fuse | Ränge | paarweise Mehrheitsentscheidung | keines |
| CombMNZ | Scores | Summe der Scores × Zahl der Systeme, die das Dokument liefern | keines, aber Scores müssen vergleichbar sein |
| Learning to Rank | Merkmale | gelerntes Modell | gelabelte Daten |

Quelle: Cormack et al. (2009).

### In der Praxis

Jeder Retriever liefert mehr Kandidaten als der endgültige Schnitt, damit auch Dokumente, die nur ein System findet, in die fusionierte Liste gelangen; in Azure AI Search kann die Volltextseite bis zu 1.000 Treffer beitragen, und standardmäßig werden die besten 50 fusionierten Ergebnisse zurückgegeben (Microsoft Learn). Die fusionierte Liste geht oft noch an einen [[cross-encoder|Cross-Encoder]]-Reranker, bevor die besten Passagen das LLM erreichen ([[retrieval-augmented-generation|RAG]]).

### Merksatz

RRF fusioniert Rankings, indem es je Dokument 1/(60 + Rang) aufsummiert, braucht weder Training noch Normalisierung der Scores und erreicht oder übertrifft zuverlässig das beste Einzelsystem; deshalb ist es eine verbreitete Wahl für hybride lexikalische und Vektorsuche.

### Quellen

- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [plg.uwaterloo.ca](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- Microsoft Learn. *Hybrid search scoring (RRF).* Azure AI Search documentation. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking)
