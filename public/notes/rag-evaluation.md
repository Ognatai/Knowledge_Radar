---
title_en: 'RAG: Evaluation'
title_de: 'RAG: Evaluation'
entity_type: Method
sources:
- https://arxiv.org/abs/2309.15217
- https://arxiv.org/abs/2311.09476
- https://arxiv.org/abs/2405.07437
- https://arxiv.org/abs/2312.10997
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RAG evaluation assesses retrieval and generation components in RAG systems, addressing the challenge of requiring extensive human annotations for multi-dimensional assessment. Frameworks like Ragas (Es et al. 2023) provide reference-free metrics, while ARES (Saad-Falcon et al. 2023) uses only a few hundred human annotations to enable efficient evaluation.

### How it works

RAG evaluation systematically assesses retrieval and generation components through a test set containing queries, relevant documents, and expected answers; retrieval performance is measured via rank-based metrics like Recall@k (see [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]), while generation quality is evaluated with a fixed, correct context to isolate the generation module (see [[rag-generation-evaluation|RAG: Generation Evaluation]]), utilizing reference-free frameworks (Ragas) or LM judge-based methods (ARES) for scalable assessment without extensive human annotation.

```text
test set: questions, relevant documents, expected answers
 ├─▶ retrieval evaluation: Recall@k, Precision@k, MRR, nDCG
 └─▶ generation evaluation with fixed correct context
                    ▼
     scoring: human judgement | reference-free metrics (Ragas)
              | trained LM judges + small human set (ARES)
```

#### 1. Test Set Construction

Test set construction defines a structured dataset for RAG evaluation, comprising per-instance fields: `question`, `expected_relevant_documents` (a list of document identifiers or text snippets expected to be retrieved), `expected_answer` (ground-truth answer text), and optional `metadata` (e.g., domain, difficulty level, edge-case flags). The test set is typically constructed via human annotation of question-answer pairs with supporting context or synthetic generation using domain knowledge bases. Human annotation ensures high fidelity but incurs high cost and slow iteration (e.g., ARES uses a few hundred human-annotated examples for prediction-powered inference (PPI) (Saad-Falcon et al. 2023)). Synthetic methods scale efficiently but risk artifacts. The data structure is a list of records enabling systematic metric computation: retrieval quality via recall@k or nDCG, and generation faithfulness via reference-free metrics like Ragas (Es et al. 2023). Metadata supports targeted failure analysis (e.g., domain-specific edge cases) and regression testing. Trade-offs center on annotation cost versus the artefacts of synthetic data.

#### 2. Retrieval Evaluation Metrics

Recall@k, Precision@k, Mean Reciprocal Rank (MRR), and normalized Discounted Cumulative Gain (nDCG) evaluate retrieval quality against ground truth. Inputs comprise a query, a ranked list of retrieved passages (top k), and a set of expected relevant documents. Recall@k measures the proportion of relevant documents retrieved within top k: `recall@k = |relevant ∩ top_k| / |relevant|`. Precision@k quantifies relevant passages among retrieved results: `precision@k = |relevant ∩ top_k| / k`. MRR averages the reciprocal of the rank of the first relevant passage across queries: `mrr = (1 / |queries|) * sum(1 / rank_i)`. nDCG@k normalizes Discounted Cumulative Gain (DCG) by the ideal ranking (IDCG): `nDCG@k = DCG@k / IDCG@k`, where `DCG@k = sum_{i=1}^{k} (rel_i / log2(i+1))` and `IDCG@k` is the DCG for the optimal ranking. These metrics balance precision and recall trade-offs; higher k values improve recall but may reduce precision. They require a test set with query-relevant document pairs and are computed using ranked lists and ground truth. [[rag-retrieval-evaluation|Retrieval Evaluation]] details implementation considerations for RAG pipelines.

#### 3. Generation Evaluation with Controlled Context

Generation evaluation with controlled context isolates the LLM's generation quality by providing pre-specified correct context passages, bypassing retrieval errors. Inputs include a question, a verified context (derived from the test set's `relevant_documents`), and an expected answer. The LLM generates a response using this context, and outputs are compared against the expected answer via reference-free metrics for faithfulness (groundedness) and correctness. The algorithm computes `faithfulness_score = 1 - (number of unsupported claims / total claims)`, where unsupported claims are identified through semantic matching between the generated answer and context. Design choices prioritize isolation of generation from retrieval; the scoring itself can be done by people, by reference metrics against the expected answer, or by reference-free metrics. Trade-offs include necessitating a curated test set with correctly aligned context (which may not reflect retrieval failures) and sacrificing real-world retrieval dynamics for evaluation purity. This method is implemented in frameworks like Ragas (Es et al. 2023) and complements retrieval evaluation [[rag-retrieval-evaluation|Retrieval Evaluation]].

#### 4. Reference-Free Evaluation Frameworks (Ragas)

Reference-free evaluation frameworks such as Ragas (Es et al. 2023) assess RAG pipelines without ground-truth human annotations. Ragas addresses three dimensions: whether the retrieval system finds relevant and focused context passages, whether the LLM uses these passages faithfully, and the quality of the generated answer itself. Inputs are the question, the retrieved context and the generated answer; the metrics are computed with the help of an LLM, for example by breaking the answer into statements and checking each against the context. Design choices prioritize scalability and speed by eliminating annotation costs, but trade off precision for nuanced errors—such as subtle context misinterpretations—that human evaluation might detect. This enables faster evaluation cycles during development. The reference-free approach accelerates iteration but may miss domain-specific nuances, making it complementary to, not a replacement for, targeted human evaluation in high-stakes applications.

#### 5. LM Judge-Based Evaluation (ARES)

ARES trains lightweight language model (LM) judges on synthetic data to evaluate three dimensions: context relevance (retrieved context's alignment with query), answer faithfulness (answer groundedness in context), and answer relevance (answer's pertinence to query). ARES creates its own synthetic training data and fine-tunes lightweight LM judges on it; at evaluation time, the judges score query-context-answer triples on each dimension. To mitigate the judges' prediction errors, ARES uses prediction-powered inference (PPI) with a small set of human-annotated datapoints (a few hundred). This minimizes reliance on extensive human annotations while maintaining accuracy across diverse benchmarks (KILT, SuperGLUE, AIS), as validated by Saad-Falcon et al. (2023). The trade-off prioritizes efficiency (low annotation cost) over potential synthetic label inaccuracies, mitigated by PPI's minimal human input requirement. Saad-Falcon et al. (2023) also report that the judges remain effective after domain shifts in queries and documents.

#### 6. Origin and variants

Evaluating RAG systems grew out of separate traditions: ranking metrics from information retrieval and answer-quality judgements from question answering. Ragas (Es et al. 2023) introduced a reference-free framework for RAG pipelines that scores context relevance, faithfulness and answer quality with an LLM, without ground-truth annotations. ARES (Saad-Falcon et al. 2023) evolved this by introducing synthetic data generation for lightweight LM judges, using only a few hundred human annotations for prediction-powered inference (PPI) to balance cost and accuracy across domain shifts. The survey by Yu et al. (2024) organises RAG evaluation as a unified process (Auepora), compares metrics such as relevance, accuracy and faithfulness across current benchmarks and discusses their limitations. Key trade-offs involve Ragas’ annotation-free efficiency versus ARES’ minimal human input cost versus Auepora’s holistic but less automated approach, reflecting the tension between scalability and precision in isolating retrieval [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] and generation [[rag-generation-evaluation|RAG: Generation Evaluation]] failures.

### When to use it

- When ground truth human annotations are unavailable but retrieval and generation components require assessment (Es et al. 2023).  
- When minimal human annotations (a few hundred) suffice for cross-domain evaluation of RAG systems (Saad-Falcon et al. 2023).  
- To isolate failure causes between retrieval and generation modules via [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] and [[rag-generation-evaluation|RAG: Generation Evaluation]].

### Strengths and limitations

**Strengths**  
- Reference-free evaluation eliminates ground truth human annotations, enabling faster assessment cycles (Es et al. 2023).  
- ARES achieves high accuracy using only hundreds of human annotations via synthetic data and prediction-powered inference (Saad-Falcon et al. 2023).  
- Multi-dimensional metrics cover retrieval relevance (e.g., context relevance), generation faithfulness, and answer relevance (Yu et al. 2024).  

**Limitations**  
- Reference-free metrics cannot fully replace domain-specific human evaluation in critical contexts (e.g., legal, medical), as required by [[rag-generation-evaluation|RAG: Generation Evaluation]].  
- LLM-based judges and metrics can themselves be wrong or biased; automated scores need spot checks by people, see [[llm-as-a-judge|LLM-as-a-Judge]].  
- Yu et al. (2024) discuss limitations of current RAG benchmarks; the hybrid structure of RAG systems and their dynamic knowledge sources make evaluation hard, see also [[rag-failure-modes|RAG: Failure Modes]].

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Reference-free evaluation, eliminating human annotation needs entirely. | Rapid iteration of RAG pipelines where annotation costs are prohibitive. |
| ARES (Saad-Falcon et al. 2023) | Fine-tunes lightweight judges on synthetic data; a few hundred human annotations correct their errors via PPI. | Repeated evaluation where a small human-labelled set is available. |
| Human evaluation | Experts judge relevance and correctness directly. | Small, high-stakes test sets; calibrating automated metrics. |
| Reference metrics (e.g. exact match) | Compare the answer with an expected answer. | Questions with short, unambiguous answers. |

Ragas enables fully automated assessment, while ARES integrates [[llm-as-a-judge|LLM-as-a-Judge]]-based scoring with minimal human input for cross-domain reliability.

### In practice

The survey by Gao et al. (2023) covers the evaluation of RAG along both retrieval and generation quality; evaluating both separately helps to locate failures. Typical failure modes include retrieval failure (missing relevant documents), poor ranking (relevant documents ranked low), LLM misinterpretation of correct context, generation of unsupported claims, and incorrect or misleading citations. Parameter choices critical for retrieval include embedding model, chunk size, top-k, metadata filters, and reranker configuration; see [[rag-retrieval-evaluation|Retrieval Evaluation]]. For generation, controlled context input is essential to avoid confounding retrieval errors with generation errors; see [[rag-generation-evaluation|Generation Evaluation]].

### Key takeaway

RAG evaluation enables comprehensive multi-dimensional assessment of retrieval and generation components through reference-free metrics or minimal human annotation, avoiding the extensive annotation burden.

### Sources

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)
- Yu, H. et al. (2024). *Evaluation of Retrieval-Augmented Generation: A Survey.* [arXiv:2405.07437](https://arxiv.org/abs/2405.07437)
- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

RAG-Bewertung bewertet die Retrieval- und GenerierungsKomponenten in RAG-Systemen und befasst sich mit der Herausforderung, umfangreiche menschliche Annotationen für eine mehrdimensionale Bewertung zu benötigen. Frameworks wie Ragas (Es et al. 2023) stellen metrische Ansätze ohne Referenzen bereit, während ARES (Saad-Falcon et al. 2023) nur einige hundert menschliche Annotationen verwendet, um eine effiziente Bewertung zu ermöglichen.

### Funktionsweise

RAG-Bewertung bewertet systematisch die Retrieval- und Generierungsbausteine mithilfe eines Testdatensatzes, der Fragen, relevante Dokumente und erwartete Antworten enthält; die Retrieval-Leistung wird mit rangbasierten Metriken wie Recall@k gemessen (siehe [[rag-retrieval-evaluation|RAG: Retrieval-Bewertung]]), während die Generierungsqualität mit einem festen, korrekten Kontext bewertet wird, um den Generierungsmodul zu isolieren (siehe [[rag-generation-evaluation|RAG: Generierungs-Bewertung]]), wobei referenzfreie Frameworks (Ragas) oder LM-judge-basierte Methoden (ARES) für eine skalierbare Bewertung ohne umfangreiche menschliche Annotation genutzt werden.

```text
test set: Fragen, relevante Dokumente, erwartete Antworten
 ├─▶ Retrieval-Bewertung: Recall@k, Precision@k, MRR, nDCG
 └─▶ Generierungs-Bewertung mit festem korrektem Kontext
                    ▼
     Bewertung: menschliche Beurteilung | referenzfreie Metriken (Ragas)
              | trainierte LM-Judges + kleiner menschlicher Datensatz (ARES)
```

#### 1. Testset-Construction

Die Testset-Construction definiert ein strukturiertes Datenset zur RAG-Bewertung, das pro Instanz folgende Felder umfasst: `Frage`, `erwartete_relevante_Dokumente` (eine Liste von Dokument-Identifiern oder Textausschnitten, die erwartet werden, abgerufen zu werden), `erwartete_Anwort` (wahrer Antworttext) und optional `Metadaten` (z. B. Domain, Schwierigkeitsgrad, Flags für Randfälle). Der Testset wird typischerweise durch menschliche Annotation von Frage-Antwort-Paaren mit unterstützenden Kontexten oder synthetische Erzeugung mithilfe von Domänkenntnisbanken konstruiert. Die menschliche Annotation gewährleistet eine hohe Genauigkeit, birgt aber hohe Kosten und verlangsamt die Iteration (z. B. verwendet ARES einige hundert menschlich annotierte Beispiele für die prädiktionsgestützte Inferenz (PPI) (Saad-Falcon et al. 2023)). Synthetische Methoden sind effizient skalierbar, bergen aber das Risiko von Artefakten. Die Datenstruktur ist eine Liste von Datensätzen, die systematische Metrikberechnung ermöglicht: Retrieval-Qualität über Recall@k oder nDCG und Generationsfaithfulness über referenzfreie Metriken wie Ragas (Es et al. 2023). Metadaten unterstützen gezielte Fehleranalyse (z. B. domänenspezifische Randfälle) und Regressionstests. Kompromisse konzentrieren sich auf Annotationskosten im Vergleich zu Artefakten synthetischer Daten.

#### 2. Retrieval-Evaluationsmetriken

Recall@k, Precision@k, Mean Reciprocal Rank (MRR) und normalized Discounted Cumulative Gain (nDCG) bewerten die Qualität der Retrieval-Operationen im Vergleich zur Ground Truth. Die Eingaben umfassen eine Abfrage, eine nach Rang geordnete Liste der abgerufenen Abschnitte (Top k) und eine Menge erwarteter relevanter Dokumente. Recall@k misst den Anteil der abgerufenen relevanten Dokumente innerhalb der Top k: `recall@k = |relevant ∩ top_k| / |relevant|`. Precision@k quantifiziert die Anzahl der relevanten Abschnitte unter den abgerufenen Ergebnissen: `precision@k = |relevant ∩ top_k| / k`. MRR berechnet den Durchschnitt des Reziproks des Rangs des ersten relevanten Abschnitts über alle Abfragen: `mrr = (1 / |queries|) * sum(1 / rank_i)`. nDCG@k normalisiert den Discounted Cumulative Gain (DCG) durch die ideale Rangordnung (IDCG): `nDCG@k = DCG@k / IDCG@k`, wobei `DCG@k = sum_{i=1}^{k} (rel_i / log2(i+1))` und `IDCG@k` der DCG für die optimale Rangordnung ist. Diese Metriken balancieren den Kompromiss zwischen Präzision und Recall; höhere k-Werte verbessern Recall, können aber Präzision verringern. Sie benötigen eine Testmenge mit Paaren von Abfragen und relevanten Dokumenten und werden mithilfe von nach Rang geordneten Listen und Ground Truth berechnet. [[rag-retrieval-evaluation|Retrieval-Evaluation]] enthält weitere Informationen zur Implementierung von RAG-Pipelines.

#### 3. Generationsbewertung mit kontrolliertem Kontext

Die Generationsbewertung mit kontrolliertem Kontext isoliert die Generationsqualität des LLM, indem vorgegebene korrekte Kontextpassagen bereitgestellt werden, wodurch Fehler bei der Retrieval-Phase umgangen werden. Die Eingaben umfassen eine Frage, einen verifizierten Kontext (abgeleitet aus dem Testdatensatz `relevant_documents`) und eine erwartete Antwort. Das LLM generiert eine Antwort mithilfe dieses Kontexts, und die Ausgaben werden mithilfe referenzfreier Metriken zur Bewertung der Glaubwürdigkeit (Verankerung) und Richtigkeit mit der erwarteten Antwort verglichen. Der Algorithmus berechnet `faithfulness_score = 1 - (Anzahl der nicht unterstützten Aussagen / Gesamtzahl der Aussagen)`, wobei nicht unterstützte Aussagen durch semantische Übereinstimmung zwischen der generierten Antwort und dem Kontext identifiziert werden. Die Gestaltungswahl priorisiert die Isolation der Generierung von der Retrieval-Phase; die Bewertung selbst kann durch Menschen erfolgen, durch referenzbasierte Metriken im Vergleich zur erwarteten Antwort oder durch referenzfreie Metriken. Kompromisse umfassen die Notwendigkeit eines kurierten Testdatensatzes mit korrekt ausgerichteten Kontexten (der möglicherweise nicht die Retrieval-Fehler widerspiegelt) und den Verzicht auf reale Retrieval-Dynamiken für die Bewertungsgenauigkeit. Dieser Ansatz wird in Frameworks wie Ragas (Es et al. 2023) umgesetzt und ergänzt die Retrieval-Bewertung [[rag-retrieval-evaluation|Retrieval-Bewertung]].

#### 4. Referenzfreie Bewertungsrahmen (Ragas)

Referenzfreie Bewertungsrahmen wie Ragas (Es et al. 2023) bewerten RAG-Pipelines ohne wahrheitsgemäße menschliche Annotationen. Ragas adressiert drei Dimensionen: ob das Retrieval-System relevante und fokussierte Kontextpassagen findet, ob das Sprachmodell diese Passagen treu verwendet und die Qualität der generierten Antwort selbst. Die Eingaben sind die Frage, der abgerufene Kontext und die generierte Antwort; die Metriken werden mit Hilfe eines Sprachmodells berechnet, beispielsweise indem die Antwort in Aussagen unterteilt und jede Aussage mit dem Kontext überprüft wird. Designentscheidungen priorisieren Skalierbarkeit und Geschwindigkeit, indem Kosten für Annotationen eliminiert werden, geben jedoch Präzision für nuancierte Fehler auf – wie subtile Kontextmissinterpretationen, die menschliche Bewertung erkennen könnte. Dies ermöglicht schnellere Bewertungsrunden während der Entwicklung. Der referenzfreie Ansatz beschleunigt die Iteration, könnte jedoch spezifische Nuancen eines Bereichs übersehen und ist daher ergänzend, nicht als Ersatz für gezielte menschliche Bewertung in hochriskanten Anwendungen.

#### 5. LM-Judge-basierte Bewertung (ARES)

ARES trainiert leichte Sprachmodelle (LM) als Richter anhand synthetischer Daten, um drei Dimensionen zu bewerten: Kontextrelevanz (Übereinstimmung des abgerufenen Kontexts mit der Anfrage), Antworttreue (Grundlage der Antwort im Kontext) und Antwortrelevanz (Relevanz der Antwort für die Anfrage). ARES erstellt eigene synthetische Trainingsdaten und feinabstimmte leichte LM-Richter darauf; bei der Bewertung bewerten die Richter die Tripel aus Anfrage, Kontext und Antwort in jeder Dimension. Um die Vorhersagefehler der Richter zu minimieren, verwendet ARES eine Vorhersagegesteuerte Inferenz (PPI) mit einer kleinen Menge an von Menschen annotierten Datensätzen (ein paar hundert). Dies minimiert den Bedarf an umfangreichen menschlichen Annotationen, während die Genauigkeit über verschiedene Benchmarks (KILT, SuperGLUE, AIS) gewährleistet bleibt, wie von Saad-Falcon et al. (2023) validiert. Der Kompromiss priorisiert Effizienz (niedrige Annotationskosten) gegenüber potenziellen Ungenauigkeiten synthetischer Labels, die durch den geringen menschlichen Eingriff bei PPI gemindert werden. Saad-Falcon et al. (2023) berichten auch, dass die Richter weiterhin effektiv bleiben, wenn sich die Domänen der Anfragen und Dokumente verändern.

#### 6. Ursprung und Varianten

Die Bewertung von RAG-Systemen entstand aus getrennten Traditionen: Ranking-Metriken aus der Informationsrecherche und Beurteilungen der Antwortqualität aus der Fragebeantwortung. Ragas (Es et al. 2023) führte ein referenzfreies Framework für RAG-Pipelines ein, das mit einem Sprachmodell (LLM) den Kontextrelevanz, die Treue und die Antwortqualität bewertet, ohne annotierte Referenzdaten. ARES (Saad-Falcon et al. 2023) entwickelte dies weiter, indem es synthetische Datengeneration für leichte LM-Judges einführte, wobei nur einige hundert menschliche Annotationen für die prädiktionsgestützte Inferenz (PPI) verwendet wurden, um Kosten und Genauigkeit über Domain-Shifts auszugleichen. Die Übersicht von Yu et al. (2024) organisiert die RAG-Bewertung als einheitlichen Prozess (Auepora), vergleicht Metriken wie Relevanz, Genauigkeit und Treue über aktuelle Benchmarks und diskutiert ihre Grenzen. Wichtige Kompromisse betreffen die annotierungsfreie Effizienz von Ragas im Vergleich zur minimalen menschlichen Eingabe-Kosten von ARES im Vergleich zum umfassenderen, aber weniger automatisierten Ansatz von Auepora, was den Spannungsbogen zwischen Skalierbarkeit und Präzision bei der Isolierung von Retrieval [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und Generationsfehlern [[rag-generation-evaluation|RAG: Generation Evaluation]] widerspiegelt.

### Wann einsetzen

- Wenn keine menschlichen Annotationsdaten zur Verfügung stehen, aber die Retrieval- und Generierungsbausteine bewertet werden müssen (Es et al. 2023).  
- Wenn minimale menschliche Annotationen (ein paar hundert) für die über-domainübergreifende Bewertung von RAG-Systemen ausreichen (Saad-Falcon et al. 2023).  
- Um die Ursachen von Fehlern zwischen Retrieval- und Generierungsmodulen mithilfe von [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und [[rag-generation-evaluation|RAG: Generation Evaluation]] zu isolieren.

### Stärken und Grenzen

**Vorteile**  
- Die referenzfreie Bewertung beseitigt die Notwendigkeit menschlicher Annotationen als Grundwahrheit und ermöglicht schnellere Bewertungsrunden (Es et al. 2023).  
- ARES erreicht eine hohe Genauigkeit mit nur hunderten menschlicher Annotationen durch synthetische Daten und prädiktionsgestützte Inferenz (Saad-Falcon et al. 2023).  
- Mehrdimensionale Metriken erfassen die Relevanz der Retrieval-Ergebnisse (z. B. Kontextrelevanz), die Glaubwürdigkeit der Generierung und die Relevanz der Antwort (Yu et al. 2024).  

**Einschränkungen**  
- Referenzfreie Metriken können in kritischen Kontexten (z. B. rechtlich, medizinisch) nicht vollständig den menschlichen, domain-spezifischen Bewertungen ersetzen, wie es von [[rag-generation-evaluation|RAG: Generation Evaluation]] gefordert wird.  
- LLM-basierte Richter und Metriken können selbst falsch oder voreingenommen sein; automatisierte Scores benötigen manuelle Prüfungen durch Menschen, siehe auch [[llm-as-a-judge|LLM-as-a-Judge]].  
- Yu et al. (2024) diskutieren die Grenzen der aktuellen RAG-Benchmarks; die hybride Struktur von RAG-Systemen und ihre dynamischen Wissensquellen machen die Bewertung schwierig, siehe auch [[rag-failure-modes|RAG: Failure Modes]].

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Referenzfreie Bewertung, die den Bedarf an menschlicher Annotation vollständig eliminiert. | Schnelle Iteration von RAG-Pipelines, bei denen Kosten für Annotationen prohibitiv sind. |
| ARES (Saad-Falcon et al. 2023) | Feinabstimmung leichtgewichtiger Richter auf synthetischen Daten; ein paar hundert menschliche Annotationen korrigieren ihre Fehler über PPI. | Wiederholte Bewertung, bei der eine kleine, menschlich annotierte Menge verfügbar ist. |
| Menschliche Bewertung | Experten beurteilen Relevanz und Richtigkeit direkt. | Kleine, hochriskante Testmengen; Kalibrierung automatisierter Metriken. |
| Referenzmetriken (z. B. exakter Treffer) | Vergleicht die Antwort mit einer erwarteten Antwort. | Fragen mit kurzen, eindeutigen Antworten. |

Ragas ermöglicht eine vollständig automatisierte Bewertung, während ARES [[llm-as-a-judge|LLM-as-a-Judge]]-basierte Bewertung mit minimaler menschlicher Eingabe für eine zuverlässige Überprüfung über verschiedene Domänen integriert.

### In der Praxis

Die Umfrage von Gao et al. (2023) behandelt die Bewertung von RAG sowohl hinsichtlich der Retrieval-Qualität als auch der Generationsqualität; die separate Bewertung hilft dabei, Fehler zu identifizieren. Typische Fehlermodi umfassen Retrieval-Fehler (fehlende relevante Dokumente), schlechte Rangierung (relevante Dokumente werden niedrig gerangiert), Fehlinterpretation des korrekten Kontexts durch das LLM, Erstellung von nicht unterstützten Aussagen und falsche oder irreführende Zitierungen. Kritische Parameter für das Retrieval sind das Embedding-Modell, die Chunk-Größe, top-k, Metadaten-Filter und die Reranker-Konfiguration; siehe [[rag-retrieval-evaluation|Retrieval-Bewertung]]. Bei der Generierung ist eine kontrollierte Kontexteingabe entscheidend, um Retrieval-Fehler mit Generationsfehlern nicht zu verwechseln; siehe [[rag-generation-evaluation|Generationsbewertung]].

### Merksatz

RAG-Bewertung ermöglicht eine umfassende mehrdimensionale Bewertung der Retrieval- und GenerierungsKomponenten durch referenzfreie Metriken oder minimale menschliche Annotation, um die umfangreiche Annotationsschwere zu vermeiden.

### Quellen

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)
- Yu, H. et al. (2024). *Evaluation of Retrieval-Augmented Generation: A Survey.* [arXiv:2405.07437](https://arxiv.org/abs/2405.07437)
- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
