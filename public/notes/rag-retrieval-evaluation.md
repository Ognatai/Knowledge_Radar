---
title_en: 'RAG: Retrieval Evaluation'
title_de: 'RAG: Evaluation des Retrievals'
entity_type: Method
aliases:
- Precision@k
- Recall@k
- Normalized discounted cumulative gain (nDCG)
- nDCG
- Mean reciprocal rank (MRR)
- MRR
sources:
- https://nlp.stanford.edu/IR-book/pdf/08eval.pdf
- https://arxiv.org/abs/2104.08663
- https://arxiv.org/abs/1611.09268
- https://doi.org/10.1145/582415.582418
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Retrieval evaluation measures how well the [[rag-retrieval|retrieval component]] of a [[retrieval-augmented-generation|RAG]] system finds and ranks the passages a query needs. It follows the test-collection method of [[information-retrieval|information retrieval]]: a document collection, a set of information needs expressed as queries, and relevance judgments for query-document pairs (Manning et al., 2008, ch. 8). Set-based measures (precision, recall, F) and ranked measures (Precision@k, Recall@k, MAP, R-precision, MRR, nDCG) summarise the comparison; BEIR reports nDCG@10 because it handles binary and graded relevance (Thakur et al., 2021). Relevance judgments are almost always incomplete, which can penalise retrievers that differ from those used to build the judgments (Thakur et al., 2021).

### How it works

```text
document collection + information needs (≥ 50) + relevance judgments (pooled, binary or graded)
 ▼
retriever ─▶ ranked list per query
 ▼
per query: Precision@k · Recall@k · average precision · reciprocal rank · nDCG@k
 ▼
mean over queries ─▶ system score (tune on a development set, report on the test set)
```

#### 1. Test collections and relevance judgments

A test collection consists of documents, a test suite of information needs and relevance judgments, usually binary. Relevance is judged against the information need, not the query: a document is relevant if it addresses the need, not because it contains all query words. Results vary strongly across information needs, so about 50 needs are a usual minimum. Parameters must be tuned on a separate development test collection; tuning on the test collection overstates performance (Manning et al., 2008, ch. 8).

For large collections, relevance is judged only on a pool: the top k documents returned by several systems, plus other sources such as Boolean searches (Manning et al., 2008, ch. 8). MS MARCO, built from 1,010,916 questions sampled from Bing's query logs and 8,841,823 passages from 3,563,535 web documents, marks as relevant the passages that editors used to compose an answer; its authors note that this annotation is incomplete, so other passages may also contain the answer (Bajaj et al., 2016).

Judges disagree. Agreement is measured with the kappa statistic, which corrects observed agreement for chance; in TREC it was normally "fair" (0.67–0.8). The choice of judge changes absolute scores considerably but has little impact on the relative ranking of systems (Manning et al., 2008, ch. 8).

#### 2. Set-based measures

Precision is the fraction of retrieved documents that are relevant, recall the fraction of relevant documents that are retrieved. Accuracy is unsuitable, because usually over 99.9% of documents are nonrelevant, so returning nothing scores well. The two trade off: returning every document gives recall 1. Web searchers want high precision on the first page, while professional searchers such as paralegals want high recall. The F measure is the weighted harmonic mean of precision and recall; the harmonic mean stays close to the smaller value, so a system cannot score well by maximising only one of them (Manning et al., 2008, ch. 8). The same measures are used for classifiers ([[classification-metrics|Classification Metrics]]).

#### 3. Ranked measures

For ranked results, the top k documents form the retrieved set. Precision@k, such as Precision at 10, needs no estimate of how many documents are relevant, but it is the least stable common measure and averages poorly, because the number of relevant documents per query strongly influences it. R-precision is the precision of the top |Rel| results, where |Rel| is the number of relevant documents; it equals the break-even point of precision and recall and correlates highly with MAP. Precision-recall curves have a saw-tooth shape and are usually smoothed with interpolated precision, the highest precision at any recall level at or above the given one; the early TREC evaluations averaged it at 11 recall levels (Manning et al., 2008, ch. 8).

Mean Average Precision (MAP) averages, for each query, the precision after each relevant document is retrieved (0 for relevant documents not retrieved) and then averages over queries. It weights every information need equally and has especially good discrimination and stability; within one system it can vary between 0.1 and 0.7 across information needs (Manning et al., 2008, ch. 8). Mean Reciprocal Rank (MRR) averages 1/rank of the first relevant result. Like MAP it is rank-aware but binary, so neither can evaluate graded relevance judgments (Thakur et al., 2021).

#### 4. nDCG

Normalised discounted cumulative gain is designed for graded relevance and evaluated over the top k results. A common form sums (2^rel − 1) / log2(1 + rank) over the top k and normalises by the score of a perfect ranking, so a perfect ranking scores 1 (Manning et al., 2008, ch. 8). Järvelin and Kekäläinen (2002) introduced cumulated gain: their original definition adds the graded relevance itself and discounts it by log_b(rank) from rank b onwards. BEIR argues that precision and recall are rank-unaware and MRR and MAP binary, and uses nDCG@10 as a single metric comparable across tasks with binary and graded judgments (Thakur et al., 2021).

#### 5. Annotation selection bias

Because unjudged documents are assumed to be nonrelevant, a new system that retrieves different documents than the systems that formed the pool is penalised. Many BEIR datasets have a lexical bias: candidates for annotation were retrieved with TF-IDF or BM25. On TREC-COVID, the share of unjudged documents in the top 10 (Hole@10) was 6.4% for [[bm25|BM25]] but 14.4% for the dense retriever ANCE and 31.8% for TAS-B. After annotating these holes, ANCE rose from 0.654 to 0.735 nDCG@10, 6.7 points above BM25, while lexical systems barely changed (Thakur et al., 2021).

#### 6. Beyond relevance

Standard judgments treat each document's relevance as independent, but a highly relevant document can be redundant with documents already seen; marginal relevance rewards diversity and novelty, and duplicates are very common on the web ([[near-duplicate-detection|Near-Duplicate Detection]]). Relevance is only a proxy for user utility, which user studies, rates of return or, in deployed systems, A/B tests with clickthrough analysis measure more directly (Manning et al., 2008, ch. 8).

#### Origin and variants

Recall and precision were first used by Kent et al. (1955), and the F measure was introduced by van Rijsbergen (1979). The Cranfield collection of the late 1950s, with 1,398 abstracts, 225 queries and exhaustive judgments, enabled the first precise quantitative measurements; NIST has run TREC since 1992, and NTCIR and CLEF focus on Asian, European and cross-language retrieval (Manning et al., 2008, ch. 8). BEIR combines 18 English datasets from 9 retrieval tasks for zero-shot evaluation (Thakur et al., 2021).

### When to use it

- Choosing between retrieval set-ups (embedding model, chunking, hybrid search, re-ranker) on a system's own test queries, with parameters tuned on a separate development set (Manning et al., 2008, ch. 8).
- [[regression-testing|Regression testing]]: re-running the same queries after every change to the index or the models.
- Checking whether a retriever generalises to new domains with a heterogeneous benchmark such as BEIR (Thakur et al., 2021).
- Locating failures: if the relevant passage is not in the top k, the problem lies in retrieval, not in generation ([[rag-failure-modes|RAG: Failure Modes]]).

### Strengths and limitations

**Strengths**
- A fixed test collection allows cheap, repeatable comparisons and clearer diagnosis than user studies (Manning et al., 2008, ch. 8).
- Relative system rankings stay largely stable even though judges disagree (Manning et al., 2008, ch. 8).
- nDCG handles both binary and graded judgments (Thakur et al., 2021).

**Limitations**
- Relevance judgments are expensive, and for large collections they cover only a pool; unjudged documents count as nonrelevant, which biases results toward the systems that built the pool (Manning et al., 2008, ch. 8; Thakur et al., 2021).
- Judgments are subjective, mostly binary and treat documents as independent, ignoring redundancy (Manning et al., 2008, ch. 8).
- Results depend heavily on the collection, queries and judgments and may not transfer to other domains or user groups (Manning et al., 2008, ch. 8).
- Retrieval scores do not show how the retrieved passages affect the generated answer ([[rag-generation-evaluation|RAG: Generation Evaluation]]).

### Comparison

| Metric | Measures | Note |
|--------|----------|------|
| Precision@k | Share of relevant results in the top k | Least stable; depends on number of relevant documents |
| Recall@k | Share of relevant documents in the top k | Needs all relevant documents to be known |
| R-precision | Precision at rank \|Rel\| | Equals break-even point; correlates with MAP |
| MAP | Precision across all recall levels | Good discrimination and stability; binary |
| MRR | Rank of the first relevant result | Binary |
| nDCG@k | Graded gain discounted by rank | Binary and graded judgments |

Sources: Manning et al. (2008, ch. 8); Thakur et al. (2021).

### In practice

A RAG generator only sees the passages passed to it, so Recall@k at that k shows whether the needed information reaches the model, and nDCG@k shows how well it is ordered. Because judgments are incomplete, unjudged passages in a new retriever's top results should be checked before concluding that it is worse than [[bm25|BM25]] (Thakur et al., 2021). Retrieval evaluation is one half of [[rag-evaluation|RAG evaluation]]; re-rankers such as [[cross-encoder|cross-encoders]] are evaluated with the same measures (Thakur et al., 2021).

### Key takeaway

Retrieval evaluation compares ranked results with relevance judgments for information needs; nDCG@10, MAP and Recall@k summarise ranking quality, but incomplete, pooled judgments can make new retrievers look worse than they are.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Evaluation in information retrieval.* Introduction to Information Retrieval, Chapter 8. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/08eval.pdf)
- Thakur, N. et al. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Evaluation des Retrievals misst, wie gut die [[rag-retrieval|Retrieval-Komponente]] eines [[retrieval-augmented-generation|RAG]]-Systems die Passagen findet und ordnet, die eine Anfrage braucht. Sie folgt der Testkollektions-Methode des [[information-retrieval|Information Retrieval]]: eine Dokumentsammlung, eine Menge von Informationsbedürfnissen, als Anfragen formuliert, und Relevanzurteile für Anfrage-Dokument-Paare (Manning et al., 2008, Kap. 8). Mengenbasierte Maße (Precision, Recall, F) und Ranglistenmaße (Precision@k, Recall@k, MAP, R-Precision, MRR, nDCG) fassen den Vergleich zusammen; BEIR berichtet nDCG@10, weil es binäre und abgestufte Relevanz abdeckt (Thakur et al., 2021). Relevanzurteile sind fast immer unvollständig, was Retriever benachteiligen kann, die sich von denen unterscheiden, mit denen die Urteile erstellt wurden (Thakur et al., 2021).

### Funktionsweise

```text
Dokumentsammlung + Informationsbedürfnisse (≥ 50) + Relevanzurteile (gepoolt, binär oder abgestuft)
 ▼
Retriever ─▶ Rangliste pro Anfrage
 ▼
pro Anfrage: Precision@k · Recall@k · Average Precision · reziproker Rang · nDCG@k
 ▼
Mittel über die Anfragen ─▶ Systemwert (auf Entwicklungsmenge abstimmen, auf Testmenge berichten)
```

#### 1. Testkollektionen und Relevanzurteile

Eine Testkollektion besteht aus Dokumenten, einer Menge von Informationsbedürfnissen und Relevanzurteilen, meist binär. Relevanz wird am Informationsbedürfnis gemessen, nicht an der Anfrage: Ein Dokument ist relevant, wenn es das Bedürfnis bedient, nicht weil es alle Anfragewörter enthält. Die Ergebnisse schwanken stark zwischen Informationsbedürfnissen, daher gelten etwa 50 als übliches Minimum. Parameter müssen auf einer getrennten Entwicklungs-Testkollektion abgestimmt werden; Abstimmen auf der Testkollektion überschätzt die Leistung (Manning et al., 2008, Kap. 8).

Bei großen Sammlungen wird Relevanz nur auf einem Pool beurteilt: den Top-k-Dokumenten mehrerer Systeme, ergänzt um weitere Quellen wie boolesche Suchen (Manning et al., 2008, Kap. 8). MS MARCO, aufgebaut aus 1.010.916 Fragen aus den Suchprotokollen von Bing und 8.841.823 Passagen aus 3.563.535 Webdokumenten, markiert die Passagen als relevant, die Redakteurinnen und Redakteure für eine Antwort verwendet haben; die Autoren weisen darauf hin, dass diese Annotation unvollständig ist und weitere Passagen die Antwort enthalten können (Bajaj et al., 2016).

Beurteilende sind sich uneinig. Übereinstimmung wird mit der Kappa-Statistik gemessen, die die beobachtete Übereinstimmung um Zufallsübereinstimmung bereinigt; bei TREC lag sie meist im „ordentlichen“ Bereich (0,67–0,8). Die Wahl der beurteilenden Person verändert absolute Werte deutlich, die relative Rangfolge der Systeme aber kaum (Manning et al., 2008, Kap. 8).

#### 2. Mengenbasierte Maße

Precision ist der Anteil relevanter Dokumente unter den gefundenen, Recall der Anteil gefundener Dokumente unter den relevanten. Accuracy eignet sich nicht, weil meist über 99,9 % der Dokumente nicht relevant sind und ein leeres Ergebnis daher gut abschneiden würde. Beide Maße stehen im Zielkonflikt: Wer alle Dokumente zurückgibt, erreicht Recall 1. Websuchende wollen hohe Precision auf der ersten Seite, professionell Suchende wie Rechtsanwaltsfachangestellte hohen Recall. Das F-Maß ist das gewichtete harmonische Mittel aus Precision und Recall; das harmonische Mittel bleibt nahe am kleineren Wert, sodass ein System nicht gut abschneidet, wenn es nur eines von beiden maximiert (Manning et al., 2008, Kap. 8). Dieselben Maße dienen auch für Klassifikatoren ([[classification-metrics|Klassifikationsmetriken]]).

#### 3. Ranglistenmaße

Bei Ranglisten bilden die Top-k-Dokumente die gefundene Menge. Precision@k, etwa Precision at 10, braucht keine Schätzung, wie viele Dokumente relevant sind, ist aber das am wenigsten stabile gängige Maß und lässt sich schlecht mitteln, weil die Zahl relevanter Dokumente pro Anfrage es stark beeinflusst. R-Precision ist die Precision der Top-|Rel|-Ergebnisse, wobei |Rel| die Zahl der relevanten Dokumente ist; sie entspricht dem Break-even-Punkt von Precision und Recall und korreliert stark mit MAP. Precision-Recall-Kurven verlaufen sägezahnförmig und werden meist mit interpolierter Precision geglättet, der höchsten Precision auf einem beliebigen Recall-Niveau ab dem gegebenen; die frühen TREC-Evaluationen mittelten sie über 11 Recall-Niveaus (Manning et al., 2008, Kap. 8).

Mean Average Precision (MAP) mittelt für jede Anfrage die Precision nach jedem gefundenen relevanten Dokument (0 für nicht gefundene relevante Dokumente) und dann über die Anfragen. Sie gewichtet jedes Informationsbedürfnis gleich und unterscheidet besonders gut und stabil; innerhalb eines Systems kann sie zwischen Informationsbedürfnissen von 0,1 bis 0,7 schwanken (Manning et al., 2008, Kap. 8). Mean Reciprocal Rank (MRR) mittelt 1/Rang des ersten relevanten Ergebnisses. Wie MAP berücksichtigt er die Reihenfolge, ist aber binär, daher können beide keine abgestuften Relevanzurteile auswerten (Thakur et al., 2021).

#### 4. nDCG

Normalised Discounted Cumulative Gain ist für abgestufte Relevanz gedacht und wird über die Top-k-Ergebnisse berechnet. Eine gängige Form summiert (2^rel − 1) / log2(1 + Rang) über die Top k und normiert mit dem Wert einer perfekten Rangfolge, sodass diese 1 erreicht (Manning et al., 2008, Kap. 8). Järvelin und Kekäläinen (2002) führten den kumulierten Gewinn ein: Ihre ursprüngliche Definition addiert die abgestufte Relevanz selbst und dämpft sie ab Rang b mit log_b(Rang). BEIR argumentiert, dass Precision und Recall die Reihenfolge nicht berücksichtigen und MRR und MAP binär sind, und verwendet nDCG@10 als einheitliche Metrik, die über Aufgaben mit binären und abgestuften Urteilen vergleichbar ist (Thakur et al., 2021).

#### 5. Verzerrung durch die Auswahl der Annotationen

Weil nicht beurteilte Dokumente als nicht relevant gelten, wird ein neues System benachteiligt, das andere Dokumente findet als die Systeme, aus denen der Pool stammt. Viele BEIR-Datensätze haben eine lexikalische Verzerrung: Die Kandidaten für die Annotation wurden mit TF-IDF oder BM25 gesucht. Auf TREC-COVID lag der Anteil nicht beurteilter Dokumente in den Top 10 (Hole@10) bei 6,4 % für [[bm25|BM25]], aber bei 14,4 % für den Dense Retriever ANCE und 31,8 % für TAS-B. Nach der Annotation dieser Lücken stieg ANCE von 0,654 auf 0,735 nDCG@10, 6,7 Punkte über BM25, während sich lexikalische Systeme kaum veränderten (Thakur et al., 2021).

#### 6. Über Relevanz hinaus

Übliche Urteile behandeln die Relevanz jedes Dokuments als unabhängig, doch ein sehr relevantes Dokument kann gegenüber bereits gesehenen redundant sein; marginale Relevanz belohnt Vielfalt und Neuheit, und Duplikate sind im Web sehr häufig ([[near-duplicate-detection|Erkennung von Beinahe-Duplikaten]]). Relevanz ist nur ein Stellvertreter für den Nutzen für die Nutzenden, den Nutzerstudien, Wiederkehrraten oder bei laufenden Systemen A/B-Tests mit Klickanalyse direkter messen (Manning et al., 2008, Kap. 8).

#### Herkunft und Varianten

Recall und Precision verwendeten zuerst Kent et al. (1955), das F-Maß führte van Rijsbergen (1979) ein. Die Cranfield-Kollektion der späten 1950er-Jahre mit 1.398 Abstracts, 225 Anfragen und vollständigen Urteilen ermöglichte die ersten genauen quantitativen Messungen; NIST veranstaltet TREC seit 1992, NTCIR und CLEF konzentrieren sich auf asiatische, europäische und sprachübergreifende Suche (Manning et al., 2008, Kap. 8). BEIR vereint 18 englische Datensätze aus 9 Retrieval-Aufgaben für die Zero-Shot-Evaluation (Thakur et al., 2021).

### Wann einsetzen

- Auswahl zwischen Retrieval-Varianten (Embedding-Modell, Chunking, hybride Suche, Re-Ranker) anhand der eigenen Testanfragen, mit auf einer getrennten Entwicklungsmenge abgestimmten Parametern (Manning et al., 2008, Kap. 8).
- [[regression-testing|Regressionstests]]: dieselben Anfragen nach jeder Änderung am Index oder an den Modellen erneut ausführen.
- Prüfen, ob ein Retriever auf neue Domänen verallgemeinert, mit einem heterogenen Benchmark wie BEIR (Thakur et al., 2021).
- Fehler eingrenzen: Liegt die relevante Passage nicht in den Top k, liegt das Problem im Retrieval, nicht in der Generierung ([[rag-failure-modes|RAG: Fehlermuster]]).

### Stärken und Grenzen

**Stärken**
- Eine feste Testkollektion erlaubt günstige, wiederholbare Vergleiche und eine klarere Diagnose als Nutzerstudien (Manning et al., 2008, Kap. 8).
- Die relative Rangfolge von Systemen bleibt weitgehend stabil, obwohl Beurteilende uneinig sind (Manning et al., 2008, Kap. 8).
- nDCG kommt mit binären und abgestuften Urteilen zurecht (Thakur et al., 2021).

**Grenzen**
- Relevanzurteile sind teuer und decken bei großen Sammlungen nur einen Pool ab; nicht beurteilte Dokumente zählen als nicht relevant, was die Ergebnisse zugunsten der Systeme verzerrt, aus denen der Pool stammt (Manning et al., 2008, Kap. 8; Thakur et al., 2021).
- Urteile sind subjektiv, meist binär und behandeln Dokumente als unabhängig, ohne Redundanz zu berücksichtigen (Manning et al., 2008, Kap. 8).
- Ergebnisse hängen stark von Sammlung, Anfragen und Urteilen ab und übertragen sich nicht unbedingt auf andere Domänen oder Nutzergruppen (Manning et al., 2008, Kap. 8).
- Retrieval-Werte zeigen nicht, wie die gefundenen Passagen die erzeugte Antwort beeinflussen ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]).

### Vergleich

| Metrik | Misst | Hinweis |
|--------|-------|---------|
| Precision@k | Anteil relevanter Ergebnisse in den Top k | Am wenigsten stabil; abhängig von der Zahl relevanter Dokumente |
| Recall@k | Anteil der relevanten Dokumente in den Top k | Alle relevanten Dokumente müssen bekannt sein |
| R-Precision | Precision auf Rang \|Rel\| | Entspricht dem Break-even-Punkt; korreliert mit MAP |
| MAP | Precision über alle Recall-Niveaus | Gute Trennschärfe und Stabilität; binär |
| MRR | Rang des ersten relevanten Ergebnisses | Binär |
| nDCG@k | Abgestufter Gewinn, nach Rang gedämpft | Binäre und abgestufte Urteile |

Quellen: Manning et al. (2008, Kap. 8); Thakur et al. (2021).

### In der Praxis

Ein RAG-Generator sieht nur die Passagen, die er erhält; Recall@k bei diesem k zeigt daher, ob die nötige Information beim Modell ankommt, und nDCG@k, wie gut sie geordnet ist. Weil Urteile unvollständig sind, sollten nicht beurteilte Passagen in den Top-Ergebnissen eines neuen Retrievers geprüft werden, bevor man schließt, dass er schlechter ist als [[bm25|BM25]] (Thakur et al., 2021). Die Retrieval-Evaluation ist eine Hälfte der [[rag-evaluation|RAG-Evaluation]]; Re-Ranker wie [[cross-encoder|Cross-Encoder]] werden mit denselben Maßen bewertet (Thakur et al., 2021).

### Merksatz

Die Evaluation des Retrievals vergleicht Ranglisten mit Relevanzurteilen zu Informationsbedürfnissen; nDCG@10, MAP und Recall@k fassen die Rangqualität zusammen, doch unvollständige, gepoolte Urteile können neue Retriever schlechter aussehen lassen, als sie sind.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Evaluation in information retrieval.* Introduction to Information Retrieval, Chapter 8. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/08eval.pdf)
- Thakur, N. et al. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)
