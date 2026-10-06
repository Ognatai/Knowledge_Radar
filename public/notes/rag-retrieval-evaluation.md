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

RAG retrieval evaluation quantifies retrieval effectiveness through metrics derived from relevance judgments, including Recall@k (coverage of relevant documents in top-k), Precision@k (precision at rank k), MRR (mean reciprocal rank of first relevant result), and nDCG (normalized discounted cumulative gain), established in information retrieval frameworks [[rag-evaluation|evaluation framework]] [Järvelin & Kekäläinen (2002), Manning et al. (2008)].  
Relevance judgment data  
▼  
Recall@k calculation  
▼  
Precision@k calculation  
▼  
MRR calculation  
▼  
nDCG calculation  
▼  
Origin and variants

#### 1. Relevance judgment data

Human-annotated relevance labels for RAG retrieval evaluation are derived from the MS MARCO dataset (Bajaj et al. 2016), where passages are labeled relevant if they contain the answer to a question. The dataset structure consists of question-passage pairs, with each question (1,010,916 from Bing logs) associated with multiple passages (8,841,823 extracted from web documents) and a human-annotated answer. Inputs are question-passage pairs; outputs are binary relevance labels (true if passage contains answer). This design uses answerability as the sole relevance criterion, prioritizing scalability and real-world applicability over graded relevance assessment. Trade-offs include omitting contextual relevance nuances (e.g., partial relevance) and potentially mislabeling passages that support answers indirectly but lack exact text matches. The large-scale, query-log origin enables robust evaluation but limits relevance granularity. This structure directly supports metrics like Recall@k by providing ground-truth relevance for passage ranking, forming the basis for evaluating the [[rag-retrieval|retrieval]] component's effectiveness.

#### 2. Recall@k calculation

Recall@k quantifies the proportion of relevant documents retrieved within the top-k ranked results. Inputs consist of the ranked list of retrieved documents (typically from a vector database or retrieval system [[rag-retrieval|retrieval component]]) and ground-truth relevance labels identifying all relevant documents for a query. The output is a scalar value computed as `Recall@k = (relevant in top-k) / (total relevant)`, where `relevant in top-k` counts relevant documents within the top-k results, and `total relevant` is the total number of relevant documents for the query. The algorithm processes the ranked list, counts relevant documents in the top-k segment, and divides by the total relevant count. Design choices center on selecting k: a larger k increases recall but raises computational cost and may include irrelevant documents, while a smaller k reduces cost but risks omitting relevant items. This trade-off necessitates empirical tuning based on system constraints (e.g., token limits for downstream generation). The metric is standardized in information retrieval evaluation (Manning et al., 2008), enabling consistent assessment of retrieval coverage across systems.

#### 3. Precision@k calculation

Precision@k quantifies the proportion of relevant items within the top-k retrieved results for a query. Inputs consist of the ranked list of top-k results (e.g., document chunks) and binary relevance judgments for each item (indicating whether it pertains to the query). The output is a scalar value calculated as `Precision@k = (relevant in top-k) / k`, ranging from 0 to 1. The computation involves iterating through the top-k list, counting relevant items, and dividing by k. Design choices center on selecting k: a smaller k emphasizes precision (reducing irrelevant results but risking missed relevant items), while a larger k improves recall at the cost of lower precision. This metric is computationally efficient and widely adopted due to its simplicity, though it treats relevance as binary and ignores ranking position of relevant items beyond the top-k window. Manning et al. (2008) establish this as a standard metric in ranked retrieval evaluation. It complements Recall@k by focusing on the quality of the retrieved subset rather than coverage of all relevant items, directly informing retrieval component optimization for RAG systems [[rag-retrieval|retrieval component]].

#### 4. MRR calculation

Mean Reciprocal Rank (MRR) evaluates retrieval quality by measuring the position of the first relevant result across multiple queries. Inputs consist of ranked result lists for each query, where each result is labeled as relevant or not. For each query, the reciprocal rank is computed as `1 / rank`, where `rank` is the position of the first relevant document (0 if none found). The output is the arithmetic mean of these values across all queries, expressed as `MRR = average(1 / rank of first relevant)`. This metric prioritizes early retrieval of relevant content, making it ideal for scenarios where a single relevant result suffices (e.g., question answering). However, it discards all information about subsequent relevant results, a trade-off that simplifies computation but limits its ability to assess full ranking quality. Manning et al. (2008) formalized MRR as a standard measure for ranked retrieval evaluation, emphasizing its utility in tasks where top-k precision is less critical than early relevance. It is commonly used alongside [[rag-evaluation|retrieval evaluation]] metrics to assess retriever performance.

#### 5. nDCG calculation

nDCG@k evaluates ranking quality by incorporating graded relevance scores and position. It is defined as `nDCG@k = DCG@k / IDCG@k`, where `DCG@k` is the discounted cumulative gain for the top k results and `IDCG@k` is the ideal DCG for the optimal ranking. Inputs include a ranked list of retrieved items with per-item relevance scores (e.g., 0–3 for non-relevant to highly relevant) and a cutoff `k`. The DCG@k computation sums `(2^{rel_i} - 1) / log2(i+1)` for positions 1 to k, with `rel_i` as the relevance score at position i. The IDCG@k is derived by sorting all relevance scores in descending order and computing DCG for that list. Normalization ensures nDCG@k ranges from 0 (worst) to 1 (perfect). The logarithmic discount factor (`log2(i+1)`) models diminishing user attention for lower-ranked items, while the exponential relevance weighting (`2^{rel_i} - 1`) amplifies the impact of highly relevant items. This approach provides a more nuanced assessment than metrics like MRR (which only considers the first relevant item) but requires graded relevance labels and incurs higher computational overhead than Recall@k or Precision@k. The method was formalized by Järvelin & Kekäläinen (2002) for ranked retrieval evaluation.

#### Origin and variants

The BEIR benchmark (Thakur et al. (2021)) standardizes retrieval evaluation across 18 heterogeneous datasets spanning diverse text retrieval tasks and domains, addressing limitations of prior homogeneous benchmarks in assessing out-of-distribution generalization. It adopts standard metrics including nDCG, Recall@k, and Precision@k. Inputs comprise query-document pairs with ground-truth relevance judgments; outputs are system-level scores (e.g., nDCG@10) computed per dataset by applying the metrics to ranked results. The benchmark structures evaluations as ranked document lists per query, using relevance labels to compute scores. A key design trade-off involves dataset diversity: the 18 heterogeneous datasets enhance robustness for cross-domain generalization but increase computational overhead compared to single-dataset evaluations. This enables comprehensive assessment of model generalization capabilities while maintaining compatibility with established evaluation practices.

### When to use it

- When assessing retrieval model generalization across diverse domains and tasks, as validated by the BEIR benchmark (Thakur et al. (2021)).
- When evaluating passage ranking for question-answering systems requiring multiple relevant passages, as supported by the MS MARCO dataset (Bajaj et al. (2016)).
- When balancing computational cost against retrieval effectiveness for dense or re-ranking architectures (Thakur et al. (2021)).
- When downstream generation quality depends on the rank of retrieved context, necessitating metrics like `nDCG@k` (Järvelin & Kekäläinen (2002)).

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

nDCG is preferred over MRR for comprehensive retrieval evaluation (Järvelin & Kekäläinen, 2002), and the BEIR benchmark (Thakur et al., 2021) confirms its utility in assessing ranking quality for the [[rag-retrieval|retrieval component]].

### In practice

In practice, retrieval evaluation should leverage heterogeneous benchmarks like BEIR (Thakur et al., 2021) to assess generalization across diverse tasks, with BM25 serving as a robust baseline while re-ranking models achieve higher zero-shot performance at increased computational cost. Typical failure modes include poor out-of-distribution generalization (dense and sparse models often underperform, Thakur et al., 2021) and the recall-precision trade-off; see [[rag-failure-modes|failure modes]] for further details. Parameter choices for `k` must be empirically optimized, as larger `k` values increase recall but typically reduce precision.

### Key takeaway

RAG retrieval evaluation balances Recall@k and Precision@k, with increasing k typically improving recall at the expense of lower precision.

### Sources

- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die RAG-Retrievalbewertung verwendet Metriken wie Recall@k, Precision@k und nDCG, um die Relevanz und die Qualität der Rangierung des abgerufenen Kontextes für den Retrieval-Komponenten [[rag-retrieval|Retrieval-Komponente]] zu quantifizieren. Dies adressiert die Herausforderung, zu messen, wie effektiv der Retriever relevante Informationen identifiziert und rangiert, was direkt den Qualität der generierten Antworten in retrieval-verstärkten Systemen beeinflusst.

### Funktionsweise

RAG-Retrieverbewertung quantifiziert die Effektivität des Retrievers durch Metriken, die aus Relevanzurteilen abgeleitet werden, einschließlich Recall@k (Abdeckung relevanter Dokumente in den Top-k), Precision@k (Präzision bei Rang k), MRR (mittlerer reziproker Rang des ersten relevanten Ergebnisses) und nDCG (normalisierter abgezogener kumulierter Gewinn), die in Frameworks der Informationsretrieval etabliert wurden [[rag-evaluation|Bewertungsrahmen]] [Järvelin & Kekäläinen (2002), Manning et al. (2008)].  
Relevanzurteilsdaten  
▼  
Recall@k-Berechnung  
▼  
Precision@k-Berechnung  
▼  
MRR-Berechnung  
▼  
nDCG-Berechnung  
▼  
Ursprung und Varianten

#### 1. Relevanzurteilsdaten

Für die RAG-Retrieverbewertung stammen die menschlich annotierten Relevanzlabels aus dem MS MARCO Datensatz (Bajaj et al. 2016), bei dem Abschnitte als relevant markiert werden, wenn sie die Antwort auf eine Frage enthalten. Die Datensatzstruktur besteht aus Frage-Abschnittspaaren, wobei jede Frage (1.010.916 aus Bing-Protokollen) mit mehreren Abschnitten (8.841.823 aus Webdokumenten) und einer menschlich annotierten Antwort verbunden ist. Die Eingaben sind Frage-Abschnittspaare; die Ausgaben sind binäre Relevanzlabels (wahr, wenn der Abschnitt die Antwort enthält). Dieses Design verwendet die Beantwortbarkeit als einzigen Relevanzkriterium, wobei Skalierbarkeit und reale Anwendbarkeit gegenüber einer bewerteten Relevaszusammenstellung priorisiert werden. Kompromisse umfassen das Omission von kontextuellen Relevanznuancen (z. B. partielle Relevanz) und das potenzielle Fehlmarkieren von Abschnitten, die Antworten indirekt unterstützen, aber keine exakten Textübereinstimmungen aufweisen. Der großskalige, aus Abfragen-Protokollen stammende Ursprung ermöglicht eine robuste Bewertung, beschränkt aber die Relevanzgranularität. Diese Struktur unterstützt direkt Metriken wie Recall@k, indem sie die tatsächliche Relevanz für die Abschnittrangierung bereitstellt und bildet die Grundlage für die Bewertung der [[rag-retrieval|Retrieval]] Komponente.

#### 2. Recall@k-Berechnung

Recall@k quantifiziert den Anteil der relevanten Dokumente, die innerhalb der Top-k Ergebnisse abgerufen wurden. Die Eingaben bestehen aus der sortierten Liste der abgerufenen Dokumente (typischerweise aus einer Vektordatenbank oder einem Retrieval-System [[rag-retrieval|Retrievalkomponente]]) und den tatsächlichen Relevanzlabels, die alle relevanten Dokumente für eine Abfrage identifizieren. Das Ergebnis ist ein Skalarwert, der berechnet wird als `Recall@k = (relevant in top-k) / (total relevant)`, wobei `relevant in top-k` die Anzahl der relevanten Dokumente innerhalb der Top-k Ergebnisse zählt und `total relevant` die Gesamtzahl der relevanten Dokumente für die Abfrage ist. Der Algorithmus verarbeitet die sortierte Liste, zählt die relevanten Dokumente im Top-k-Bereich und teilt durch die Gesamtzahl der relevanten Dokumente. Die Gestaltungswahl konzentriert sich auf die Auswahl von k: ein größeres k erhöht Recall, erhöht aber den Rechenaufwand und kann irrelevanten Dokumenten beinhalten, während ein kleineres k den Aufwand reduziert, aber das Risiko besteht, relevante Elemente zu übersehen. Dieser Kompromiss erfordert empirische Anpassung basierend auf Systemeinschränkungen (z. B. Token-Limits für die nachfolgende Generierung). Die Metrik ist in der Informationsretrieval-Bewertung standardisiert (Manning et al., 2008), was eine konsistente Bewertung der Retrieval-Abdeckung über Systeme ermöglicht.

#### 3. Precision@k-Berechnung

Precision@k quantifiziert den Anteil der relevanten Elemente innerhalb der Top-k abgerufenen Ergebnisse für eine Abfrage. Die Eingaben bestehen aus der sortierten Liste der Top-k-Ergebnisse (z. B. Dokumentabschnitte) und binären Relevanzurteilen für jedes Element (wobei angegeben wird, ob es sich auf die Abfrage bezieht). Das Ergebnis ist ein Skalarwert, der berechnet wird als `Precision@k = (relevant in top-k) / k`, der zwischen 0 und 1 liegt. Die Berechnung umfasst das Durchlaufen der Top-k-Liste, das Zählen der relevanten Elemente und das Teilen durch k. Die Gestaltungswahl konzentriert sich auf die Auswahl von k: ein kleineres k betont Präzision (reduziert irrelevanten Ergebnisse, aber riskiert, relevante Elemente zu übersehen), während ein größeres k die Recall verbessert, aber die Präzision verringert. Diese Metrik ist rechenleicht und weit verbreitet aufgrund ihrer Einfachheit, beachtet aber Relevanz nur als binär und ignoriert die Position relevanter Elemente jenseits des Top-k-Fensters. Manning et al. (2008) etablieren dies als Standardmetrik in der Bewertung von sortiertem Retrieval. Sie ergänzt Recall@k, indem sie sich auf die Qualität der abgerufenen Untermenge konzentriert, anstatt die Abdeckung aller relevanten Elemente, und informiert direkt die Optimierung der Retrievalkomponente für RAG-Systeme [[rag-retrieval|Retrievalkomponente]].

#### 4. MRR-Berechnung

Der Mittlere Reziproke Rang (MRR) bewertet die Retrievalqualität, indem er die Position des ersten relevanten Ergebnisses über mehrere Abfragen misst. Die Eingaben bestehen aus sortierten Ergebnislisten für jede Abfrage, wobei jedes Ergebnis als relevant oder nicht markiert ist. Für jede Abfrage wird der reziproke Rang berechnet als `1 / rank`, wobei `rank` die Position des ersten relevanten Dokuments ist (0, wenn keines gefunden wurde). Das Ergebnis ist der arithmetische Mittelwert dieser Werte über alle Abfragen, ausgedrückt als `MRR = average(1 / rank of first relevant)`. Diese Metrik priorisiert die frühe Retrieval von relevantem Inhalt, wodurch sie ideal für Szenarien ist, bei denen ein einziges relevantes Ergebnis ausreicht (z. B. bei Fragebeantwortung). Allerdings wird alle Information über nachfolgende relevante Ergebnisse verworfen, ein Kompromiss, der die Berechnung vereinfacht, aber ihre Fähigkeit begrenzt, die vollständige Rangqualität zu bewerten. Manning et al. (2008) haben MRR als Standardmaß für die Bewertung von sortiertem Retrieval formalisiert, wobei ihre Nützlichkeit in Aufgaben betont wird, bei denen die Präzision im Top-k weniger kritisch ist als die frühe Relevanz. Sie wird häufig gemeinsam mit [[rag-evaluation|Retrievalbewertung]]-Metriken verwendet, um die Leistung des Retriever zu bewerten.

#### 5. nDCG-Berechnung

nDCG@k bewertet die Rangqualität, indem es bewertete Relevanzscores und Positionen einbezieht. Es wird definiert als `nDCG@k = DCG@k / IDCG@k`, wobei `DCG@k` der abgezogene kumulierte Gewinn für die Top-k-Ergebnisse ist und `IDCG@k` der ideale DCG für die optimale Rangierung. Die Eingaben umfassen eine sortierte Liste der abgerufenen Elemente mit pro-Element-Relevanzscores (z. B. 0–3 für nicht relevant bis hoch relevant) und einen Schwellenwert `k`. Die Berechnung von DCG@k summiert `(2^{rel_i} - 1) / log2(i+1)` für Positionen 1 bis k, wobei `rel_i` der Relevanzscore an Position i ist. Der IDCG@k wird durch Sortieren aller Relevanzscores in absteigender Reihenfolge und Berechnen des DCG für diese Liste abgeleitet. Die Normalisierung stellt sicher, dass nDCG@k zwischen 0 (schlechtest) und 1 (perfekt) liegt. Der logarithmische Abzugsfaktor (`log2(i+1)`) modelliert das abnehmende Aufmerksamkeitsniveau für Elemente mit niedrigerer Rangierung, während der exponentielle Relevanzgewichtungsfaktor (`2^{rel_i} - 1`) den Einfluss hoch relevanter Elemente verstärkt. Dieser Ansatz bietet eine präzisere Bewertung als Metriken wie MRR (die nur das erste relevante Element berücksichtigen), erfordert aber bewertete Relevanzlabels und hat einen höheren Rechenaufwand als Recall@k oder Precision@k. Der Ansatz wurde von Järvelin & Kekäläinen (2002) für die Bewertung von sortiertem Retrieval formalisiert.

#### Ursprung und Varianten

Der BEIR-Benchmark (Thakur et al. (2021)) standardisiert die Retrievalbewertung über 18 heterogene Datensätze, die diverse Textretrieval-Aufgaben und -Domainen abdecken, und adressiert die Einschränkungen früherer homogener Benchmarks bei der Bewertung der Generalisierung außerhalb der Verteilung. Er verwendet standardisierte Metriken wie nDCG, Recall@k und Precision@k. Die Eingaben bestehen aus Frage-Dokumentpaaren mit tatsächlichen Relevanzurteilen; die Ausgaben sind systemweite Scores (z. B. nDCG@10), die pro Datensatz durch Anwenden der Metriken auf sortierte Ergebnisse berechnet werden. Der Benchmark strukturiert die Bewertungen als sortierte Dokumentlisten pro Abfrage, wobei Relevanzlabels verwendet werden, um Scores zu berechnen. Ein zentraler Gestaltungskompromiss besteht in der Datensatzdiversität: die 18 heterogenen Datensätze erhöhen die Robustheit für die Generalisierung über verschiedene Domänen, erhöhen aber den Rechenaufwand im Vergleich zu Bewertungen mit einem einzigen Datensatz. Dies ermöglicht eine umfassende Bewertung der Fähigkeiten der Modellgeneralisierung, während die Kompatibilität mit etablierten Bewertungspraktiken gewahrt bleibt.

### Wann einsetzen

- Bei der Beurteilung der Generalisierungsfähigkeit von Retrieval-Modellen über verschiedene Domänen und Aufgaben, wie sie durch den BEIR-Benchmark (Thakur et al. (2021)) validiert wird.
- Bei der Bewertung der Passage-Rangierung für Frage-Antwort-Systeme, die mehrere relevante Passagen erfordern, wie sie durch den MS MARCO Datensatz (Bajaj et al. (2016)) unterstützt wird.
- Bei der Ausgewogenheit zwischen Rechenkosten und Retrieval-Effektivität für dichte oder Re-Ranking-Architekturen (Thakur et al. (2021)).
- Wenn die Qualität der nachfolgenden Generierung vom Rang des abgerufenen Kontexts abhängt und Metriken wie `nDCG@k` (Järvelin & Kekäläinen (2002)) erforderlich sind.

### Stärken und Grenzen

**Vorteile**  
- Der BEIR-Benchmark (Thakur et al. (2021)) ermöglicht eine standardisierte Bewertung über 18 heterogene Datensätze hinweg, wodurch sich zeigt, dass Re-Ranking-Modelle die beste Zero-Shot-Leistung erzielen, obwohl sie hohe rechnerische Kosten verursachen.  
- nDCG (Järvelin & Kekäläinen (2002)) berücksichtigt die gestufte Relevanz und die Gewichtung der Position, wodurch eine präzisere Bewertung als binäre Metriken wie Recall@k möglich ist.  
- Metriken wie Precision@k und Recall@k sind rechnerisch effizient und in der Information Retrieval gut etabliert (Manning et al. (2008)), was eine skalierbare Implementierung ermöglicht.  

**Einschränkungen**  
- Die Bewertung erfasst nicht den Einfluss der Retrieval-Operation auf die Qualität der nachfolgenden Generierung, weshalb eine separate [[rag-generation-evaluation|Generierungsbewertung]] erforderlich ist.  
- Etikettierte Relevanzdaten für Metriken (z. B. Recall@k) sind aufwendig zu erlangen, wie der Umfang von MS MARCO belegt (Bajaj et al. (2016)).  
- Hochleistungsfähige Modelle (z. B. Re-Ranking) verursachen erhebliche rechnerische Overhead-Kosten (Thakur et al. (2021)), was die Echtzeitanwendbarkeit einschränkt.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| nDCG | Berücksichtigt die Relevanz aller Dokumente in den Top-k, während MRR nur das erste relevante Dokument berücksichtigt. | Wenn mehrere relevante Dokumente vorhanden sind und ihre relative Reihenfolge kritisch ist, wie beispielsweise in RAG-Systemen, die mehrere Kontext-Blöcke benötigen. |
| Recall@k und Precision@k | Bieten komplementäre Maßzahlen für Abdeckung (Recall@k) und Qualität (Precision@k); die Verwendung nur einer davon erfasst nicht den Kompromiss zwischen Recall und Precision. | Wenn die Abdeckung aller relevanten Informationen (Recall@k) mit der Minimierung der irrelevanten Top-k-Ergebnisse (Precision@k) ausgewogen werden soll. |

nDCG wird gegenüber MRR bevorzugt, um die Retrieval-Evaluation umfassend zu bewerten (Järvelin & Kekäläinen, 2002), und der BEIR-Benchmark (Thakur et al., 2021) bestätigt seine Nützlichkeit bei der Bewertung der Reihenfolgequalität für die [[rag-retrieval|Retrieval-Komponente]].

### In der Praxis

In der Praxis sollte die Retrieval-Evaluation heterogene Benchmarks wie BEIR (Thakur et al., 2021) nutzen, um die Generalisierung über verschiedene Aufgaben zu bewerten, wobei BM25 als robuster Baseline dient, während Re-Ranking-Modelle eine höhere zero-shot-Leistung bei erhöhtem Rechenaufwand erzielen. Typische Fehlmodi umfassen eine schlechte Generalisierung außerhalb der Verteilung (dichte und spärliche Modelle leisten oft schlechter, Thakur et al., 2021) und den Recall-Precision-Trade-off; siehe [[rag-failure-modes|Fehlmodi]] für weitere Details. Die Parameterwahl für `k` muss empirisch optimiert werden, da größere `k`-Werte den Recall erhöhen, aber typischerweise die Precision verringern.

### Merksatz

RAG-Retriever-Bewertung ausgleicht Recall@k und Precision@k, wobei ein zunehmender k-Wert typischerweise die Erinnerung verbessert, auf Kosten der Präzision.

### Quellen

- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
- Bajaj, P. et al. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Järvelin, K. & Kekäläinen, J. (2002). *Cumulated gain-based evaluation of IR techniques.* ACM Transactions on Information Systems 20(4). [doi:10.1145/582415.582418](https://doi.org/10.1145/582415.582418)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press. [online edition](https://nlp.stanford.edu/IR-book/)
