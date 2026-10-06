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
Test Set Construction
─▶ Retrieval Evaluation Metrics
─▶ Generation Evaluation with Controlled Context
─▶ Reference-Free Evaluation Frameworks (Ragas)
─▶ LM Judge-Based Evaluation (ARES)
─▶ Origin and variants
```

#### 1. Test Set Construction

Test set construction defines a structured dataset for RAG evaluation, comprising per-instance fields: `question`, `expected_relevant_documents` (a list of document identifiers or text snippets expected to be retrieved), `expected_answer` (ground-truth answer text), and optional `metadata` (e.g., domain, difficulty level, edge-case flags). The test set is typically constructed via human annotation of question-answer pairs with supporting context or synthetic generation using domain knowledge bases. Human annotation ensures high fidelity but incurs high cost and slow iteration (e.g., ARES uses a few hundred human-annotated examples for prediction-powered inference (PPI) (Saad-Falcon et al. 2023)). Synthetic methods scale efficiently but risk artifacts. The data structure is a list of records enabling systematic metric computation: retrieval quality via recall@k or nDCG, and generation faithfulness via reference-free metrics like Ragas (Es et al. 2023). Metadata supports targeted failure analysis (e.g., domain-specific edge cases) and regression testing [[rag-retrieval-evaluation|Retrieval Evaluation]] [[rag-generation-evaluation|Generation Evaluation]]. Trade-offs center on annotation cost versus synthetic bias.

#### 2. Retrieval Evaluation Metrics

Recall@k, Precision@k, Mean Reciprocal Rank (MRR), and normalized Discounted Cumulative Gain (nDCG) evaluate retrieval quality against ground truth. Inputs comprise a query, a ranked list of retrieved passages (top k), and a set of expected relevant documents. Recall@k measures the proportion of relevant documents retrieved within top k: `recall@k = |relevant ∩ top_k| / |relevant|`. Precision@k quantifies relevant passages among retrieved results: `precision@k = |relevant ∩ top_k| / k`. MRR averages the reciprocal of the rank of the first relevant passage across queries: `mrr = (1 / |queries|) * sum(1 / rank_i)`. nDCG@k normalizes Discounted Cumulative Gain (DCG) by the ideal ranking (IDCG): `nDCG@k = DCG@k / IDCG@k`, where `DCG@k = sum_{i=1}^{k} (rel_i / log2(i+1))` and `IDCG@k` is the DCG for the optimal ranking. These metrics balance precision and recall trade-offs; higher k values improve recall but may reduce precision. They require a test set with query-relevant document pairs and are computed using ranked lists and ground truth. [[rag-retrieval-evaluation|Retrieval Evaluation]] details implementation considerations for RAG pipelines.

#### 3. Generation Evaluation with Controlled Context

Generation evaluation with controlled context isolates the LLM's generation quality by providing pre-specified correct context passages, bypassing retrieval errors. Inputs include a question, a verified context (derived from the test set's `relevant_documents`), and an expected answer. The LLM generates a response using this context, and outputs are compared against the expected answer via reference-free metrics for faithfulness (groundedness) and correctness. The algorithm computes `faithfulness_score = 1 - (number of unsupported claims / total claims)`, where unsupported claims are identified through semantic matching between the generated answer and context. Design choices prioritize isolation of generation from retrieval, enabling automated, annotation-free assessment (Es et al. 2023). Trade-offs include necessitating a curated test set with correctly aligned context (which may not reflect retrieval failures) and sacrificing real-world retrieval dynamics for evaluation purity. This method is implemented in frameworks like Ragas (Es et al. 2023) and complements retrieval evaluation [[rag-retrieval-evaluation|Retrieval Evaluation]].

#### 4. Reference-Free Evaluation Frameworks (Ragas)

Reference-free evaluation frameworks, such as Ragas (Es et al. 2023), assess RAG systems using automated metrics without human annotations. Inputs include question-retrieved context pairs for retrieval evaluation (yielding metrics like `recall@k = |relevant ∩ retrieved| / |relevant|`) and question-context-answer triples for generation evaluation (yielding faithfulness scores via semantic alignment checks). The framework computes these metrics through algorithms that compare generated outputs against retrieved context without requiring reference answers, leveraging LLM-based semantic similarity or statistical methods. Design choices prioritize scalability and speed by eliminating annotation costs, but trade off precision for nuanced errors—such as subtle context misinterpretations—that human evaluation might detect. This enables rapid, continuous assessment during development cycles, as validated in [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] and [[rag-generation-evaluation|RAG: Generation Evaluation]]. The reference-free approach accelerates iteration but may miss domain-specific nuances, making it complementary to, not a replacement for, targeted human evaluation in high-stakes applications.

#### 5. LM Judge-Based Evaluation (ARES)

ARES trains lightweight language model (LM) judges on synthetic data to evaluate three dimensions: context relevance (retrieved context's alignment with query), answer faithfulness (answer groundedness in context), and answer relevance (answer's pertinence to query). Synthetic data is generated by constructing query-context-answer triples via a pre-trained LLM, with labels for each dimension derived from reference LLM outputs. Judges (e.g., DistilBERT variants) are fine-tuned on this data. During inference, judges process inputs (query, context, answer) to output dimension-specific scores. To correct synthetic data biases, ARES employs Prediction-Powered Inference (PPI) using a small human-annotated set (a few hundred examples) to recalibrate predictions via linear adjustment. This minimizes reliance on extensive human annotations while maintaining accuracy across diverse benchmarks (KILT, SuperGLUE, AIS), as validated by Saad-Falcon et al. (2023). The trade-off prioritizes efficiency (low annotation cost) over potential synthetic label inaccuracies, mitigated by PPI's minimal human input requirement. The approach isolates evaluation to individual RAG components, avoiding conflated end-to-end metrics [[rag-generation-evaluation|Generation Evaluation]].

#### 6. Origin and variants

Ragas (Es et al. 2023) pioneered reference-free evaluation for RAG, decomposing assessment into retrieval (context relevance) and generation (answer faithfulness) dimensions. Its input comprises query-retrieval pairs and generated answers, while outputs include metrics like `faithfulness_score = 1 - (number of unsupported claims / total claims)`. The framework leverages LLM-as-a-judge for automated scoring, eliminating human annotation needs but requiring careful prompt engineering to avoid bias. ARES (Saad-Falcon et al. 2023) evolved this by introducing synthetic data generation for lightweight LM judges, using only a few hundred human annotations for prediction-powered inference (PPI) to balance cost and accuracy across domain shifts. Auepora (Yu et al. 2024) later unified evaluation under a comprehensive process, analyzing retrieval (e.g., `recall@k`) and generation metrics (e.g., groundedness) across benchmarks, though it relies on existing evaluation frameworks rather than introducing new algorithms. Key trade-offs involve Ragas’ annotation-free efficiency versus ARES’ minimal human input cost versus Auepora’s holistic but less automated approach, reflecting the tension between scalability and precision in isolating retrieval [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] and generation [[rag-generation-evaluation|RAG: Generation Evaluation]] failures.

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
- ARES relies on small human-annotated sets for prediction-powered inference, limiting generalizability to edge cases (Saad-Falcon et al. 2023).  
- Current benchmarks lack comprehensive coverage of RAG failure modes across dynamic knowledge sources (Yu et al. 2024), as documented in [[rag-failure-modes|RAG: Failure Modes]].

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Reference-free evaluation, eliminating human annotation needs entirely. | Rapid iteration of RAG pipelines where annotation costs are prohibitive. |
| ARES (Saad-Falcon et al. 2023) | Uses a few hundred human annotations to train lightweight judges for domain-shift robustness. | Domain-adaptive evaluation requiring minimal human oversight. |
Ragas enables fully automated assessment, while ARES integrates [[llm-as-a-judge|LLM-as-a-Judge]]-based scoring with minimal human input for cross-domain reliability.

### In practice

Gao et al. (2023) propose a comprehensive evaluation framework that separates retrieval and generation evaluation to isolate failure modes. Typical failure modes include retrieval failure (missing relevant documents), poor ranking (relevant documents ranked low), LLM misinterpretation of correct context, generation of unsupported claims, and incorrect or misleading citations. Parameter choices critical for retrieval include embedding model, chunk size, top-k, metadata filters, and reranker configuration; see [[rag-retrieval-evaluation|Retrieval Evaluation]]. For generation, controlled context input is essential to avoid confounding retrieval errors with generation errors; see [[rag-generation-evaluation|Generation Evaluation]].

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

RAG-Bewertung bewertet die Retrieval- und Generierungscomponenten in RAG-Systemen und befasst sich mit der Herausforderung, umfangreiche menschliche Annotationen für eine multidimensionale Bewertung zu benötigen. Frameworks wie Ragas (Es et al. 2023) stellen metrische Ansätze ohne Referenzen bereit, während ARES (Saad-Falcon et al. 2023) lediglich einige hundert menschliche Annotationen verwendet, um eine effiziente Bewertung zu ermöglichen.

### Funktionsweise

RAG-Bewertung bewertet systematisch die Retrieval- und Generationskomponenten mithilfe eines Testsets, das Abfragen, relevante Dokumente und erwartete Antworten enthält; die Retrieval-Leistung wird durch rangbasierte Metriken wie Recall@k gemessen (siehe [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]], während die Generationsqualität mit einem festen, korrekten Kontext bewertet wird, um den Generationsmodul zu isolieren (siehe [[rag-generation-evaluation|RAG: Generation Evaluation]], wobei referenzfreie Frameworks (Ragas) oder LM-judge-basierte Methoden (ARES) für eine skalierbare Bewertung ohne umfangreiche menschliche Annotation genutzt werden.

```text
Testset-Konstruktion
─▶ Retrieval-Bewertungsmetriken
─▶ Generationsbewertung mit kontrolliertem Kontext
─▶ Referenzfreie Bewertungsframeworks (Ragas)
─▶ LM-Judge-basierte Bewertung (ARES)
─▶ Ursprung und Varianten
```

#### 1. Testset-Konstruktion

Die Testset-Konstruktion definiert ein strukturiertes Datenset für die RAG-Bewertung, das pro Instanz folgende Felder umfasst: `Frage`, `erwartete_relevante_Dokumente` (eine Liste von Dokumentidentifikatoren oder Textausschnitten, die erwartet werden, abgerufen zu werden), `erwartete_Antwort` (Ground-Truth-Antworttext) und optional `Metadaten` (z. B. Domain, Schwierigkeitsgrad, Edge-Case-Flaggen). Das Testset wird typischerweise durch menschliche Annotation von Frage-Antwort-Paaren mit unterstützenden Kontexten oder synthetische Erzeugung mithilfe von Domain-Wissensbanken erstellt. Menschliche Annotation gewährleistet eine hohe Genauigkeit, birgt aber hohe Kosten und langsame Iteration (z. B. verwendet ARES einige hundert menschlich annotierte Beispiele für prediction-powered inference (PPI) (Saad-Falcon et al. 2023)). Synthetische Methoden sind effizient skalierbar, bergen aber das Risiko von Artefakten. Die Datenstruktur ist eine Liste von Datensätzen, die systematische Metrikberechnung ermöglichen: Retrieval-Qualität über Recall@k oder nDCG und Generationsgenauigkeit über referenzfreie Metriken wie Ragas (Es et al. 2023). Metadaten unterstützen gezielte Fehleranalyse (z. B. domain-spezifische Edge Cases) und Regressionstests [[rag-retrieval-evaluation|Retrieval Evaluation]] [[rag-generation-evaluation|Generation Evaluation]]. Kompromisse stehen im Gegenstand der Annotationskosten versus synthetischer Verzerrung.

#### 2. Retrieval-Bewertungsmetriken

Recall@k, Precision@k, Mean Reciprocal Rank (MRR) und normalized Discounted Cumulative Gain (nDCG) bewerten die Retrieval-Qualität im Vergleich zur Ground Truth. Die Eingaben bestehen aus einer Abfrage, einer rangierten Liste der abgerufenen Passagen (Top k) und einer Menge erwarteter relevanter Dokumente. Recall@k misst den Anteil der relevanten Dokumente, die innerhalb der Top k abgerufen werden: `recall@k = |relevant ∩ top_k| / |relevant|`. Precision@k quantifiziert die relevanten Passagen unter den abgerufenen Ergebnissen: `precision@k = |relevant ∩ top_k| / k`. MRR berechnet den Durchschnitt des Reziproks des Rangs der ersten relevanten Passage über alle Abfragen: `mrr = (1 / |queries|) * sum(1 / rank_i)`. nDCG@k normalisiert Discounted Cumulative Gain (DCG) durch die ideale Rangfolge (IDCG): `nDCG@k = DCG@k / IDCG@k`, wobei `DCG@k = sum_{i=1}^{k} (rel_i / log2(i+1))` und `IDCG@k` der DCG für die optimale Rangfolge ist. Diese Metriken balancieren Präzision und Recall-Kompromisse; höhere k-Werte verbessern Recall, können aber Präzision verringern. Sie erfordern ein Testset mit Abfragen und relevanten Dokumentpaaren und werden mithilfe von rangierten Listen und Ground Truth berechnet. [[rag-retrieval-evaluation|Retrieval Evaluation]] beschreibt Implementierungskonsiderationen für RAG-Pipelines.

#### 3. Generationsbewertung mit kontrolliertem Kontext

Die Generationsbewertung mit kontrolliertem Kontext isoliert die Generationsqualität des LLMs, indem vorgegebene korrekte Kontextpassagen bereitgestellt werden, um Retrieval-Fehler zu umgehen. Eingaben umfassen eine Frage, einen verifizierten Kontext (abgeleitet aus dem Testsets `relevant_documents`) und eine erwartete Antwort. Das LLM generiert eine Antwort mithilfe dieses Kontexts, und die Ausgaben werden mit der erwarteten Antwort mithilfe referenzfreier Metriken für Genauigkeit (Groundedness) und Richtigkeit verglichen. Der Algorithmus berechnet `faithfulness_score = 1 - (Anzahl der nicht unterstützten Aussagen / Gesamtzahl der Aussagen)`, wobei nicht unterstützte Aussagen durch semantische Übereinstimmung zwischen der generierten Antwort und dem Kontext identifiziert werden. Designentscheidungen priorisieren die Isolation der Generierung von der Retrieval, was eine automatisierte, annotierungsfreie Bewertung ermöglicht (Es et al. 2023). Kompromisse umfassen die Notwendigkeit eines kurierten Testsets mit korrekt ausgerichteten Kontexten (was möglicherweise Retrieval-Fehler nicht widerspiegelt) und den Verzicht auf reale Retrieval-Dynamiken für die Bewertungsgenauigkeit. Dieser Ansatz wird in Frameworks wie Ragas (Es et al. 2023) implementiert und ergänzt die Retrieval-Bewertung [[rag-retrieval-evaluation|Retrieval Evaluation]].

#### 4. Referenzfreie Bewertungsframeworks (Ragas)

Referenzfreie Bewertungsframeworks, wie Ragas (Es et al. 2023), bewerten RAG-Systeme mithilfe automatisierter Metriken ohne menschliche Annotationen. Eingaben umfassen Frage-abgerufene Kontextpaare für die Retrieval-Bewertung (erzeugen Metriken wie `recall@k = |relevant ∩ retrieved| / |relevant|`) und Frage-Kontext-Antwort-Tripel für die Generationsbewertung (erzeugen Genauigkeitsbewertungen durch semantische Ausrichtungschecks). Das Framework berechnet diese Metriken mithilfe von Algorithmen, die generierte Ausgaben mit abgerufenem Kontext vergleichen, ohne Referenzantworten zu benötigen, wobei LLM-basierte semantische Ähnlichkeit oder statistische Methoden genutzt werden. Designentscheidungen priorisieren Skalierbarkeit und Geschwindigkeit durch das Entfernen von Annotationskosten, wobei Präzision für feine Fehler (z. B. subtile Kontextmissinterpretationen) gegen menschliche Bewertung getauscht wird. Dies ermöglicht schnelle, kontinuierliche Bewertung während der Entwicklungszyklen, wie in [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und [[rag-generation-evaluation|RAG: Generation Evaluation]] validiert. Der referenzfreie Ansatz beschleunigt Iterationen, kann aber domain-spezifische Nuancen verfehlen, wodurch er ergänzend, nicht als Ersatz für gezielte menschliche Bewertung in hochriskanten Anwendungen dienen sollte.

#### 5. LM-Judge-basierte Bewertung (ARES)

ARES trainiert leichte Sprachmodell (LM) Richter auf synthetischen Daten, um drei Dimensionen zu bewerten: Kontextrelevanz (Ausrichtung des abgerufenen Kontexts mit der Abfrage), Antwortgenauigkeit (Groundedness der Antwort im Kontext) und Antwortrelevanz (Relevanz der Antwort für die Abfrage). Synthetische Daten werden durch das Konstruieren von Frage-Kontext-Antwort-Tripeln mithilfe eines vortrainierten LLMs generiert, wobei Labels für jede Dimension aus Referenz-LLM-Ausgaben abgeleitet werden. Richter (z. B. DistilBERT-Varianten) werden auf dieser Datenbasis feinabgestimmt. Während der Inferenz verarbeiten Richter Eingaben (Frage, Kontext, Antwort), um dimensionspezifische Scores auszugeben. Um synthetische Datenverzerrungen zu korrigieren, verwendet ARES Prediction-Powered Inference (PPI) mithilfe einer kleinen, menschlich annotierten Menge (einige hundert Beispiele), um Vorhersagen durch lineare Anpassung zu rekalibrieren. Dies minimiert den Vertrauensbedarf auf umfangreiche menschliche Annotationen, während Genauigkeit über diverse Benchmarks (KILT, SuperGLUE, AIS) gewährleistet bleibt, wie von Saad-Falcon et al. (2023) validiert. Der Kompromiss priorisiert Effizienz (niedrige Annotationskosten) gegenüber potenziellen synthetischen Label-Ingenauigkeiten, die durch die minimale menschliche Eingabeanforderung von PPI gemildert werden. Der Ansatz isoliert die Bewertung auf individuelle RAG-Komponenten, vermeidet dabei zusammengefasste End-to-End-Metriken [[rag-generation-evaluation|Generation Evaluation]].

#### 6. Ursprung und Varianten

Ragas (Es et al. 2023) hat die referenzfreie Bewertung für RAG initiiert, indem die Bewertung in Retrieval (Kontextrelevanz) und Generierung (Antwortgenauigkeit) Dimensionen zerlegt. Seine Eingaben umfassen Frage-Retrieval-Paare und generierte Antworten, während die Ausgaben Metriken wie `faithfulness_score = 1 - (Anzahl der nicht unterstützten Aussagen / Gesamtzahl der Aussagen)` umfassen. Das Framework nutzt LLM-as-a-judge für automatische Bewertung, eliminiert menschliche Annotationen, erfordert aber sorgfältige Prompt-Engineering, um Bias zu vermeiden. ARES (Saad-Falcon et al. 2023) hat dies durch die Einführung synthetischer Daten für leichte LM-Richter weiterentwickelt, wobei nur wenige hundert menschliche Annotationen für prediction-powered inference (PPI) verwendet werden, um Kosten und Genauigkeit über Domain-Shifts auszugleichen. Auepora (Yu et al. 2024) hat später eine umfassende Bewertung unter einem einheitlichen Prozess vereint, indem Retrieval (z. B. `recall@k`) und Generationsmetriken (z. B. Groundedness) über Benchmarks analysiert werden, wobei es bestehende Bewertungsframeworks nutzt, statt neue Algorithmen einzuführen. Kritische Kompromisse umfassen Ragas’ annotierungsfreie Effizienz versus ARES’ minimale menschliche Eingabekosten versus Aueporas umfassenden, aber weniger automatisierten Ansatz, was den Spannungsbogen zwischen Skalierbarkeit und Präzision bei der Isolierung von Retrieval [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und Generations [[rag-generation-evaluation|RAG: Generation Evaluation]] Fehlern widerspiegelt.

### Wann einsetzen

- Wenn keine menschlichen Annotationen als Grundwahrheit vorliegen, aber die Komponenten für Retrieval und Generierung bewertet werden müssen (Es et al. 2023).  
- Wenn minimale menschliche Annotationen (ein paar hundert) für die cross-domain Bewertung von RAG-Systemen ausreichen (Saad-Falcon et al. 2023).  
- Um Ursachen für Fehlschläge zwischen Retrieval- und Generierungsmodulen über [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und [[rag-generation-evaluation|RAG: Generation Evaluation]] zu isolieren.

### Stärken und Grenzen

**Stärken**  
- Die referenzfreie Bewertung beseitigt menschliche Annotationen als Ground Truth, was schnelleren Bewertungszyklen ermöglicht (Es et al. 2023).  
- ARES erreicht eine hohe Genauigkeit mit nur hunderten menschlichen Annotationen durch synthetische Daten und prädiktionsgestützte Inferenz (Saad-Falcon et al. 2023).  
- Mehrdimensionale Metriken umfassen Retrieval-Relevanz (z. B. Kontextrelevanz), Generations-Treue und Antwortrelevanz (Yu et al. 2024).  

**Einschränkungen**  
- Referenzfreie Metriken können in kritischen Kontexten (z. B. rechtlich, medizinisch) nicht vollständig den domänenspezifischen menschlichen Bewertungen ersetzen, wie es von [[rag-generation-evaluation|RAG: Generation Evaluation]] gefordert wird.  
- ARES basiert auf kleinen, menschlich annotierten Datensätzen für prädiktionsgestützte Inferenz, was die Verallgemeinerbarkeit auf Randfälle begrenzt (Saad-Falcon et al. 2023).  
- Die aktuellen Benchmarks weisen keine umfassende Abdeckung der RAG-Fehlermodi über dynamische Wissensquellen auf (Yu et al. 2024), wie in [[rag-failure-modes|RAG: Failure Modes]] dokumentiert.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Referenzfreie Bewertung, die den Bedarf an menschlicher Annotation vollständig eliminiert. | Schnelle Iteration von RAG-Pipelines, bei denen die Kosten für Annotationen prohibitiv sind. |
| ARES (Saad-Falcon et al. 2023) | Verwendet einige hundert menschliche Annotationen, um leichte Richter für die Robustheit bei Domain-Shift zu trainieren. | Domain-adaptive Bewertung mit minimaler menschlicher Aufsicht. |
Ragas ermöglicht eine vollständig automatisierte Bewertung, während ARES [[llm-as-a-judge|LLM-as-a-Judge]]-basierte Bewertung mit minimaler menschlicher Eingabe für die Zuverlässigkeit über verschiedene Domänen hinweg integriert.

### In der Praxis

Gao et al. (2023) schlagen ein umfassendes Bewertungsfenster vor, das die Bewertung der Retrieval- und Generationsleistung trennt, um Fehlermodi zu isolieren. Typische Fehlermodi umfassen Retrieval-Fehler (fehlende relevante Dokumente), schlechte Rangierung (relevante Dokumente werden niedrig gerangiert), Fehlinterpretation des korrekten Kontextes durch das Sprachmodell, Erstellung von nicht unterstützten Aussagen und falsche oder irreführende Zitierungen. Kritische Parameter für das Retrieval umfassen das Embedding-Modell, die Chunk-Größe, top-k, Metadaten-Filter und die Reranker-Konfiguration; siehe [[rag-retrieval-evaluation|Retrieval-Bewertung]]. Bei der Generierung ist eine kontrollierte Kontexteingabe entscheidend, um Retrieval-Fehler mit Generationsfehlern nicht zu verwechseln; siehe [[rag-generation-evaluation|Generationsbewertung]].

### Merksatz

RAG-Bewertung ermöglicht eine umfassende mehrdimensionale Beurteilung der Retrieval- und Generierungsbausteine durch referenzfreie Metriken oder minimale menschliche Annotation, wodurch die umfangreiche Annotationsschwere vermieden wird.

### Quellen

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)
- Yu, H. et al. (2024). *Evaluation of Retrieval-Augmented Generation: A Survey.* [arXiv:2405.07437](https://arxiv.org/abs/2405.07437)
- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
