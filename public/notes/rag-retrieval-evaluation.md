---
title_en: 'RAG: Retrieval Evaluation'
title_de: 'RAG: Evaluation des Retrievals'
entity_type: Method
sources:
- https://arxiv.org/abs/2104.08663
- https://arxiv.org/abs/1611.09268
- https://doi.org/10.1145/582415.582418
- https://nlp.stanford.edu/IR-book/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RAG retrieval evaluation employs metrics including Recall@k, Precision@k, and nDCG to quantify the relevance and ranking quality of retrieved context for the retrieval component [[rag-retrieval|retrieval component]]. This addresses the challenge of measuring how effectively the retriever identifies and ranks relevant information, directly impacting the quality of generated responses in retrieval-augmented systems.

### How it works

Retrieval evaluation compares the ranked list a retriever returns for each test query with relevance judgments, i.e. the known relevant documents for that query. From this comparison, standard information retrieval metrics are computed: Recall@k for coverage, Precision@k for the share of relevant results, MRR for the position of the first relevant result and nDCG for the quality of the whole ranking with graded relevance (Manning et al., 2008; Järvelin & Kekäläinen, 2002). It is one half of [[rag-evaluation|RAG evaluation]].

```text
test queries + relevance judgments
 ▼
retriever ─▶ ranked list per query (top k)
 ▼
per query: Recall@k, Precision@k, reciprocal rank, nDCG@k
 ▼
average over all queries ─▶ system scores
```

#### 1. Relevance judgment data

Retrieval evaluation needs relevance judgments: for each test query, the documents or passages that are relevant. They come from human annotation, from existing benchmarks or, for a RAG system's own corpus, from a curated test set. A large public example is MS MARCO (Bajaj et al. 2016), built from real Bing questions, where annotators marked the passages they used to write the answer. The dataset structure consists of question-passage pairs, with each question (1,010,916 from Bing logs) associated with multiple passages (8,841,823 extracted from web documents) and a human-annotated answer. Inputs are question-passage pairs; outputs are binary relevance labels (true if passage contains answer). This design uses answerability as the sole relevance criterion, prioritizing scalability and real-world applicability over graded relevance assessment. Trade-offs include omitting contextual relevance nuances (e.g., partial relevance) and potentially mislabeling passages that support answers indirectly but lack exact text matches. The large-scale, query-log origin enables robust evaluation but limits relevance granularity. This structure directly supports metrics like Recall@k by providing ground-truth relevance for passage ranking, forming the basis for evaluating the [[rag-retrieval|retrieval]] component's effectiveness.

#### 2. Recall@k calculation

Recall@k quantifies the proportion of relevant documents retrieved within the top-k ranked results. Inputs consist of the ranked list of retrieved documents (typically from a vector database or retrieval system [[rag-retrieval|retrieval component]]) and ground-truth relevance labels identifying all relevant documents for a query. The output is a scalar value computed as `Recall@k = (relevant in top-k) / (total relevant)`, where `relevant in top-k` counts relevant documents within the top-k results, and `total relevant` is the total number of relevant documents for the query. The algorithm processes the ranked list, counts relevant documents in the top-k segment, and divides by the total relevant count. Design choices center on selecting k: a larger k increases recall but raises computational cost and may include irrelevant documents, while a smaller k reduces cost but risks omitting relevant items. This trade-off necessitates empirical tuning based on system constraints (e.g., token limits for downstream generation). The metric is standardized in information retrieval evaluation (Manning et al., 2008), enabling consistent assessment of retrieval coverage across systems.

#### 3. Precision@k calculation

Precision@k quantifies the proportion of relevant items within the top-k retrieved results for a query. Inputs consist of the ranked list of top-k results (e.g., document chunks) and binary relevance judgments for each item (indicating whether it pertains to the query). The output is a scalar value calculated as `Precision@k = (relevant in top-k) / k`, ranging from 0 to 1. The computation involves iterating through the top-k list, counting relevant items, and dividing by k. Design choices center on selecting k: a smaller k emphasizes precision (reducing irrelevant results but risking missed relevant items), while a larger k improves recall at the cost of lower precision. This metric is computationally efficient and widely adopted due to its simplicity, though it treats relevance as binary and ignores ranking position of relevant items beyond the top-k window. Manning et al. (2008) establish this as a standard metric in ranked retrieval evaluation. It complements Recall@k by focusing on the quality of the retrieved subset rather than coverage of all relevant items, directly informing retrieval component optimization for RAG systems [[rag-retrieval|retrieval component]].

#### 4. MRR calculation

Mean Reciprocal Rank (MRR) evaluates retrieval quality by measuring the position of the first relevant result across multiple queries. Inputs consist of ranked result lists for each query, where each result is labeled as relevant or not. For each query, the reciprocal rank is computed as `1 / rank`, where `rank` is the position of the first relevant document; if no relevant document is retrieved, the reciprocal rank is 0. The output is the arithmetic mean of these values across all queries, expressed as `MRR = average(1 / rank of first relevant)`. This metric prioritizes early retrieval of relevant content, making it ideal for scenarios where a single relevant result suffices (e.g., question answering). However, it discards all information about subsequent relevant results, a trade-off that simplifies computation but limits its ability to assess full ranking quality. MRR became a standard measure in question-answering evaluation, where usually one correct passage suffices.

#### 5. nDCG calculation

nDCG@k evaluates ranking quality by incorporating graded relevance scores and position. It is defined as `nDCG@k = DCG@k / IDCG@k`, where `DCG@k` is the discounted cumulative gain for the top k results and `IDCG@k` is the ideal DCG for the optimal ranking. Inputs include a ranked list of retrieved items with per-item relevance scores (e.g., 0–3 for non-relevant to highly relevant) and a cutoff `k`. A widely used formulation computes DCG@k as the sum of `(2^rel_i - 1) / log2(i + 1)` over positions 1 to k, with `rel_i` as the relevance score at position i; the original definition by Järvelin & Kekäläinen (2002) adds the gain `rel_i` itself and discounts it by `log_b(i)` from rank b onwards. The IDCG@k is derived by sorting all relevance scores in descending order and computing DCG for that list. Normalization ensures nDCG@k ranges from 0 (worst) to 1 (perfect). The logarithmic discount factor (`log2(i+1)`) models diminishing user attention for lower-ranked items, while the exponential gain (`2^rel_i - 1`) of the common formulation amplifies the impact of highly relevant items. This approach provides a more nuanced assessment than metrics like MRR (which only considers the first relevant item) but requires graded relevance labels and incurs higher computational overhead than Recall@k or Precision@k. Cumulated gain measures, including DCG and nDCG, were introduced by Järvelin & Kekäläinen (2002).

#### Origin and variants

The BEIR benchmark (Thakur et al. (2021)) standardizes retrieval evaluation across 18 heterogeneous datasets spanning diverse text retrieval tasks and domains, addressing limitations of prior homogeneous benchmarks in assessing out-of-distribution generalization. It adopts standard metrics including nDCG, Recall@k, and Precision@k. Inputs comprise query-document pairs with ground-truth relevance judgments; outputs are system-level scores (e.g., nDCG@10) computed per dataset by applying the metrics to ranked results. The benchmark structures evaluations as ranked document lists per query, using relevance labels to compute scores. A key design trade-off involves dataset diversity: the 18 heterogeneous datasets enhance robustness for cross-domain generalization but increase computational overhead compared to single-dataset evaluations. This enables comprehensive assessment of model generalization capabilities while maintaining compatibility with established evaluation practices.

### When to use it

- Choosing between retrieval set-ups (embedding model, chunking, hybrid search, reranker) on the system's own test queries.
- Regression testing: re-running the same queries after every change to the index or the models.
- Checking whether a retriever generalises to new domains, e.g. with a heterogeneous benchmark such as BEIR (Thakur et al., 2021).
- Locating failures: if the relevant passage is not in the top k, the problem lies in retrieval, not in generation.

### Strengths and limitations

**Strengths**
- The BEIR benchmark (Thakur et al. (2021)) enables standardized evaluation across 18 heterogeneous datasets, revealing re-ranking models achieve the best zero-shot performance despite high computational costs.
- nDCG (Järvelin & Kekäläinen (2002)) accounts for graded relevance and position weighting, providing a more nuanced assessment than binary metrics like Recall@k.
- Metrics like Precision@k and Recall@k are computationally efficient and well-established in information retrieval (Manning et al. (2008)), supporting scalable deployment.

**Limitations**
- Evaluation does not capture retrieval's impact on downstream generation quality, requiring separate [[rag-generation-evaluation|generation evaluation]].
- Labeled relevance data for metrics (e.g., Recall@k) is expensive to obtain, as evidenced by MS MARCO’s scale (Bajaj et al. (2016)).
- High-performing models (e.g., re-ranking) incur significant computational overhead (Thakur et al. (2021)), limiting real-time applicability.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| nDCG | Incorporates relevance of all documents in top-k, whereas MRR considers only the first relevant document. | When multiple relevant documents exist and their relative ranking is critical, such as in RAG systems requiring multiple context chunks. |
| Recall@k and Precision@k | Provide complementary measures of coverage (Recall@k) and quality (Precision@k); using only one fails to capture the recall-precision trade-off. | When balancing retrieval of all relevant information (Recall@k) with minimization of irrelevant top-k results (Precision@k). |
| MRR | Only the rank of the first relevant result counts. | Tasks where one relevant passage is enough, e.g. factoid questions. |

For RAG, Recall@k at the k actually passed to the model is usually the most important number; nDCG adds sensitivity to the order within the top k, which BEIR (Thakur et al., 2021) reports as its main metric (nDCG@10).

### In practice

In practice, retrieval evaluation should leverage heterogeneous benchmarks like BEIR (Thakur et al., 2021) to assess generalization across diverse tasks, with BM25 serving as a robust baseline while re-ranking models achieve higher zero-shot performance at increased computational cost. Typical failure modes include poor out-of-distribution generalization (dense and sparse models often underperform, Thakur et al., 2021) and the recall-precision trade-off; see [[rag-failure-modes|failure modes]] for further details. Parameter choices for `k` must be empirically optimized, as larger `k` values increase recall but typically reduce precision.

### Key takeaway

Retrieval evaluation needs relevance judgments and complementary metrics: Recall@k shows whether the needed passages are retrieved at all, Precision@k, MRR and nDCG how well they are ranked.

### Sources

- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die RAG-Rückgewinnungsbewertung verwendet Metriken wie Recall@k, Precision@k und nDCG, um die Relevanz und die Qualität der Rangierung des zurückgewonnenen Kontextes für den Rückgewinnungskomponenten [[rag-retrieval|Rückgewinnungskomponente]] zu quantifizieren. Dies adressiert die Herausforderung, zu messen, wie effektiv der Rückgewinner relevante Informationen identifiziert und rangiert, was direkt die Qualität der generierten Antworten in systemen mit erweiterter Rückgewinnung beeinflusst.

### Funktionsweise

Retrieval-Bewertung vergleicht die nach Rang geordnete Liste, die ein Retrieval-System für jede Test-Abfrage zurückgibt, mit Relevanzurteilen, also den als relevant bekannten Dokumenten für diese Abfrage. Aus diesem Vergleich werden Standard-Metriken des Information Retrievals berechnet: Recall@k für die Abdeckung, Precision@k für den Anteil der relevanten Ergebnisse, MRR für die Position des ersten relevanten Ergebnisses und nDCG für die Qualität der gesamten Rangliste mit differenzierten Relevanzstufen (Manning et al., 2008; Järvelin & Kekäläinen, 2002). Es ist der eine Teil von [[rag-evaluation|RAG-Bewertung]].

```text
Test-Abfragen + Relevanzurteile
 ▼
Retrieval-System ─▶ nach Rang geordnete Liste pro Abfrage (Top k)
 ▼
pro Abfrage: Recall@k, Precision@k, reziproke Rang, nDCG@k
 ▼
Durchschnitt über alle Abfragen ─▶ Systembewertungen
```

#### 1. Relevanzurteilsdaten

Die Retrieval-Bewertung benötigt Relevanzurteile: für jede Testabfrage die Dokumente oder Abschnitte, die relevant sind. Sie stammen aus menschlicher Annotation, aus bestehenden Benchmarks oder, bei einem RAG-System eigenen Corpus, aus einem kurierten Testdatensatz. Ein großes öffentliches Beispiel ist MS MARCO (Bajaj et al. 2016), das aus echten Bing-Fragen erstellt wurde, wobei die Annotatoren die Abschnitte markierten, die sie zur Antworterstellung verwendet haben. Die Datensatzstruktur besteht aus Frage-Abschnitt-Paaren, wobei jede Frage (1.010.916 aus Bing-Protokollen) mit mehreren Abschnitten (8.841.823 aus Webdokumenten) und einer von Menschen annotierten Antwort verbunden ist. Die Eingaben sind Frage-Abschnitt-Paare; die Ausgaben sind binäre Relevanzlabels (wahr, wenn der Abschnitt die Antwort enthält). Dieses Design verwendet die Beantwortbarkeit als einzigen Relevanzkriterium, wobei Skalierbarkeit und reale Anwendbarkeit gegenüber einer bewerteten Relevanzanalyse priorisiert werden. Kompromisse umfassen das Auslassen von Kontextrelevanznuancen (z. B. partielle Relevanz) und das potenzielle Fehlzuordnen von Abschnitten, die Antworten indirekt unterstützen, aber keine exakten Textübereinstimmungen aufweisen. Die großskalige, aus Abfragen-Protokollen stammende Herkunft ermöglicht eine robuste Bewertung, beschränkt jedoch die Relevanzgranularität. Diese Struktur unterstützt direkt Metriken wie Recall@k, indem sie die tatsächliche Relevanz für die Abschnittrangierung bereitstellt und bildet die Grundlage für die Bewertung der [[rag-retrieval|Retrieval]]-Komponente.

#### 2. Recall@k-Berechnung

Recall@k quantifiziert den Anteil der relevanten Dokumente, die innerhalb der top-k rangierten Ergebnisse abgerufen wurden. Die Eingaben bestehen aus der rangierten Liste der abgerufenen Dokumente (typischerweise aus einer Vektordatenbank oder einem Retrieval-System [[rag-retrieval|Retrieval-Komponente]]) und den Ground-Truth-Relevanzlabels, die alle relevanten Dokumente für eine Abfrage identifizieren. Das Ergebnis ist ein skalares Wert, der als `Recall@k = (relevant in top-k) / (total relevant)` berechnet wird, wobei `relevant in top-k` die Anzahl der relevanten Dokumente innerhalb der top-k Ergebnisse zählt und `total relevant` die Gesamtzahl der relevanten Dokumente für die Abfrage ist. Der Algorithmus verarbeitet die rangierte Liste, zählt die relevanten Dokumente im top-k-Abschnitt und teilt diese durch die Gesamtzahl der relevanten Dokumente. Die Gestaltungswahl konzentriert sich auf die Auswahl von k: ein größeres k erhöht Recall, erhöht aber auch die Rechenkosten und kann irrelevanten Dokumenten beinhalten, während ein kleineres k die Kosten reduziert, aber das Risiko besteht, relevante Elemente zu übersehen. Dieser Kompromiss erfordert empirische Anpassung basierend auf Systembeschränkungen (z. B. Token-Limits für die nachfolgende Generierung). Der Metric ist in der Information Retrieval-Bewertung standardisiert (Manning et al., 2008), was eine konsistente Bewertung der Retrieval-Abdeckung über Systeme ermöglicht.

#### 3. Precision@k-Berechnung

Precision@k quantifiziert den Anteil der relevanten Elemente innerhalb der top-k-Ergebnisse, die für eine Abfrage abgerufen wurden. Die Eingaben bestehen aus der nach Rang geordneten Liste der top-k-Ergebnisse (z. B. Dokumentabschnitte) und binären Relevanzurteilen für jedes Element (die angeben, ob es sich auf die Abfrage bezieht). Das Ergebnis ist ein skalares Wert, der nach der Formel `Precision@k = (relevant in top-k) / k` berechnet wird und sich zwischen 0 und 1 bewegt. Die Berechnung erfolgt durch Iterieren durch die Liste der top-k-Ergebnisse, Zählen der relevanten Elemente und Dividieren durch k. Die Gestaltung entscheidet sich hauptsächlich für die Wahl von k: ein kleineres k betont die Präzision (indem irrelevanten Ergebnisse reduziert werden, aber das Risiko besteht, relevante Elemente zu verpassen), während ein größeres k die Erinnerung verbessert, allerdings auf Kosten der Präzision. Dieser Metrik kommt aufgrund ihrer Einfachheit eine hohe Relevanz zu und sie ist computationally effizient sowie weit verbreitet. Dennoch behandelt sie Relevanz als binär und ignoriert die Reihenfolge der relevanten Elemente außerhalb des top-k-Fensters. Manning et al. (2008) etablieren dies als Standardmetrik bei der Bewertung von ranked Retrieval. Sie ergänzt Recall@k, da sie sich auf die Qualität des abgerufenen Unterteils konzentriert, anstatt auf die Abdeckung aller relevanten Elemente, und informiert direkt die Optimierung von Retrieval-Komponenten für RAG-Systeme [[rag-retrieval|retrieval-Komponente]].

#### 4. MRR-Berechnung

Der Mittelwert des Reziproken Rangs (MRR) bewertet die Qualität der Retrieval-Operation, indem er die Position des ersten relevanten Ergebnisses über mehrere Abfragen hinweg misst. Die Eingaben bestehen aus rangierten Ergebnislisten für jede Abfrage, wobei jedes Ergebnis als relevant oder nicht relevant gekennzeichnet ist. Für jede Abfrage wird der Reziproke Rang als `1 / rank` berechnet, wobei `rank` die Position des ersten relevanten Dokuments ist; wenn kein relevantes Dokument abgerufen wird, ist der Reziproke Rang 0. Das Ergebnis ist der arithmetische Mittelwert dieser Werte über alle Abfragen, ausgedrückt als `MRR = average(1 / rank of first relevant)`. Dieser Metrik liegt der Vorrang des frühen Abrufens relevanter Inhalte zugrunde, wodurch sie ideal für Szenarien geeignet ist, bei denen ein einzelnes relevantes Ergebnis ausreicht (z. B. bei Frage-Antwort-Systemen). Allerdings wird dabei jede Information über nachfolgende relevante Ergebnisse verworfen, ein Kompromiss, der die Berechnung vereinfacht, aber die Fähigkeit zur Bewertung der gesamten Rangliste begrenzt. MRR wurde zu einem Standardmaß in der Evaluierung von Frage-Antwort-Systemen, bei denen in der Regel ein korrekter Abschnitt ausreicht.

#### 5. nDCG-Berechnung

nDCG@k bewertet die Qualität einer Sortierung, indem es bewertete Relevanzwerte und Positionen berücksichtigt. Es wird definiert als `nDCG@k = DCG@k / IDCG@k`, wobei `DCG@k` der abgezinsten kumulierten Gewinn für die Top-k-Ergebnisse und `IDCG@k` der ideale DCG für die optimale Sortierung ist. Die Eingaben umfassen eine sortierte Liste der abgerufenen Elemente mit pro-Element-Relevanzwerten (z. B. 0–3 für nicht relevant bis sehr relevant) und einen Schwellenwert `k`. Eine weit verbreitete Formulierung berechnet DCG@k als die Summe von `(2^rel_i - 1) / log2(i + 1)` über die Positionen 1 bis k, wobei `rel_i` der Relevanzwert an Position i ist; die ursprüngliche Definition von Järvelin & Kekäläinen (2002) fügt den Gewinn `rel_i` selbst hinzu und diskontiert ihn ab Rang b mit `log_b(i)`. Der IDCG@k wird durch Sortieren aller Relevanzwerte in absteigender Reihenfolge und Berechnen des DCG für diese Liste abgeleitet. Die Normalisierung stellt sicher, dass nDCG@k einen Wert zwischen 0 (schlechtest) und 1 (perfekt) annimmt. Der logarithmische Abzinsungsfaktor (`log2(i+1)`) modelliert den abnehmenden Aufmerksamkeitsgrad des Nutzers für weniger gut platzierte Elemente, während der exponentielle Gewinn (`2^rel_i - 1`) der üblichen Formulierung den Einfluss sehr relevanter Elemente verstärkt. Dieser Ansatz bietet eine präzisere Bewertung als Metriken wie MRR (die nur das erste relevante Element berücksichtigen), erfordert jedoch bewertete Relevanzlabels und verursacht höhere rechnerische Aufwände als Recall@k oder Precision@k. Kumulierte Gewinnmaße, einschließlich DCG und nDCG, wurden von Järvelin & Kekäläinen (2002) eingeführt.

#### Ursprung und Varianten

Der BEIR-Benchmark (Thakur et al. (2021)) standardisiert die Bewertung von Retrieval-Systemen über 18 heterogene Datensätze, die sich auf verschiedene Text-Retrieval-Aufgaben und -Domainen erstrecken, und adressiert dadurch die Einschränkungen früherer homogener Benchmarks bei der Bewertung der Generalisierungsfähigkeit außerhalb der Trainingsdatenverteilung. Er verwendet standardisierte Metriken wie nDCG, Recall@k und Precision@k. Die Eingaben bestehen aus Abfrage-Dokument-Paaren mit tatsächlichen Relevanzurteilen; die Ausgaben sind systemweite Scores (z. B. nDCG@10), die pro Datensatz berechnet werden, indem die Metriken auf die rangierten Ergebnisse angewendet werden. Der Benchmark strukturiert die Evaluierungen als rangierte Dokumentlisten pro Abfrage und verwendet Relevanzlabels, um die Scores zu berechnen. Ein zentraler Design-Kompromiss besteht in der Datensatzdiversität: die 18 heterogenen Datensätze erhöhen die Robustheit bei der Generalisierung über verschiedene Domänen, erhöhen aber im Vergleich zu Evaluierungen mit einem einzigen Datensatz den rechnerischen Aufwand. Dies ermöglicht eine umfassende Bewertung der Generalisierungsfähigkeit von Modellen, während die Kompatibilität mit etablierten Bewertungspraktiken gewahrt bleibt.

### Wann einsetzen

- Die Wahl zwischen Retrieval-Set-ups (Embedding-Modell, Chunking, hybride Suche, Reranker) anhand der eigenen Testabfragen des Systems.
- Regressionstests: Wiederholen der gleichen Abfragen nach jedem Änderung am Index oder den Modellen.
- Prüfen, ob ein Retriever auf neue Domänen generalisiert, z. B. mit einem heterogenen Benchmark wie BEIR (Thakur et al., 2021).
- Lokalisieren von Fehlern: Wenn der relevante Absatz nicht in den Top-k liegt, liegt das Problem im Retrieval und nicht in der Generierung.

### Stärken und Grenzen

**Stärken**
- Der BEIR-Benchmark (Thakur et al. (2021)) ermöglicht eine standardisierte Bewertung über 18 heterogene Datensätze, wodurch sich zeigt, dass Re-Ranking-Modelle die beste Zero-Shot-Leistung erzielen, obwohl sie mit hohen Rechenkosten verbunden sind.
- nDCG (Järvelin & Kekäläinen (2002)) berücksichtigt die graduelle Relevanz und die Positionsgewichtung, wodurch eine präzisere Bewertung als bei binären Metriken wie Recall@k möglich ist.
- Metriken wie Precision@k und Recall@k sind rechenleicht und etabliert in der Information Retrieval (Manning et al. (2008)), was eine skalierbare Bereitstellung ermöglicht.

**Einschränkungen**
- Die Bewertung erfasst nicht den Einfluss der Retrieval-Operation auf die Qualität der nachfolgenden Generierung, weshalb eine separate [[rag-generation-evaluation|Generierungsbewertung]] erforderlich ist.
- Etikettierte Relevanzdaten für Metriken (z. B. Recall@k) sind aufwendig zu erlangen, wie es beispielsweise bei der Skalierung von MS MARCO gezeigt wird (Bajaj et al. (2016)).
- Hochleistungsfähige Modelle (z. B. Re-Ranking) verursachen erhebliche Rechenkosten (Thakur et al. (2021)), was die Echtzeitanwendbarkeit einschränkt.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| nDCG | Berücksichtigt die Relevanz aller Dokumente in den Top-k, während MRR nur das erste relevante Dokument berücksichtigt. | Wenn mehrere relevante Dokumente vorhanden sind und deren relative Reihenfolge kritisch ist, wie z. B. in RAG-Systemen, die mehrere Kontextabschnitte benötigen. |
| Recall@k und Precision@k | Liefern komplementäre Maße für Abdeckung (Recall@k) und Qualität (Precision@k); die Verwendung nur eines davon kann den Kompromiss zwischen Recall und Precision nicht erfassen. | Wenn die Abdeckung aller relevanten Informationen (Recall@k) mit der Minimierung der irrelevanten Top-k-Ergebnisse (Precision@k) ausgewogen werden soll. |
| MRR | Nur die Reihenfolge des ersten relevanten Ergebnisses zählt. | Aufgaben, bei denen ein relevanter Absatz ausreicht, z. B. Faktenfragen. |

Für RAG ist Recall@k an der tatsächlich an das Modell übergebenen k in der Regel die wichtigste Zahl; nDCG fügt Empfindlichkeit für die Reihenfolge innerhalb der Top-k hinzu, was BEIR (Thakur et al., 2021) als seine Hauptmetrik berichtet (nDCG@10).

### In der Praxis

In der Praxis sollte die Retrieval-Evaluation heterogene Benchmarks wie BEIR (Thakur et al., 2021) nutzen, um die Generalisierung über verschiedene Aufgaben zu bewerten, wobei BM25 als robuster Baseline dient, während Re-Ranking-Modelle eine höhere zero-shot-Leistung bei erhöhtem Rechenaufwand erzielen. Typische Fehlmodi umfassen eine schlechte Generalisierung außerhalb der Verteilung (dichte und sparse Modelle leisten oft schlechter, Thakur et al., 2021) und den Recall-Precision-Trade-off; siehe [[rag-failure-modes|Fehlmodi]] für weitere Details. Die Parameterwahl für `k` muss empirisch optimiert werden, da höhere `k`-Werte den Recall erhöhen, aber typischerweise die Precision verringern.

### Merksatz

Die Retrieval-Evaluation benötigt Relevanzurteile und ergänzende Metriken: Recall@k zeigt, ob die benötigten Abschnitte überhaupt abgerufen werden, Precision@k, MRR und nDCG, wie gut sie rangiert sind.

### Quellen

- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)
