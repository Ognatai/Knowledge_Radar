---
title_en: 'RAG: Failure Modes'
title_de: 'RAG: Typische Fehlerarten'
entity_type: Concept
sources:
- https://arxiv.org/abs/2401.05856
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2401.14887
- https://arxiv.org/abs/2305.14627
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RAG failure modes define the distinct failure points within the RAG pipeline (retrieval, ranking, context construction, generation) that cause erroneous outputs, such as retrieval failures or context pollution. This framework enables systematic error diagnosis to identify root causes, improving system robustness and reducing hallucinations beyond reliance on LLM generation alone.

### How it works

The framework for diagnosing RAG failures employs a sequential diagnostic process across six failure modes, each corresponding to a specific pipeline stage (e.g., [[rag-retrieval|Retrieval]] for retrieval failures and [[rag-generation-evaluation|Generation Evaluation]] for generation-related failures), to isolate root causes without conflating symptoms. Barnett et al. (2024), reporting on three RAG case studies, conclude that a RAG system can only really be validated during operation, so the diagnosis has to be repeated on real queries.

```text
pipeline stage        failure mode            typical check
retrieval        ─▶  passage not retrieved   hit rate / Recall@k
ranking          ─▶  ranked below cut-off    MRR, nDCG, reranking
context          ─▶  context pollution       top-k, filters, order
generation       ─▶  citation hallucination  citation check
generation       ─▶  grounding hallucination claim-level NLI
generation       ─▶  interpretation error    LLM judge, experts
```

#### 1. Retrieval Failure Detection

A retrieval failure means the passage needed for the answer is not among the retrieved results at all. It is measured with the hit rate (also success@k): the fraction of queries for which at least one relevant document appears in the top k, `hit_rate@k = (1 / N) * sum_i [relevant document in top k for query i]`; Recall@k additionally counts how many of all relevant documents were found. This binary metric prioritizes recall to minimize retrieval failures, though it ignores rank position within top k. Query expansion analysis tests the impact of adding terms (e.g., synonyms) to queries on retrieval performance. Inputs include original queries and expansion terms; outputs are performance metrics comparing expanded vs. base queries. The algorithm typically generates expansions via thesauri or corpus analysis and re-runs retrieval, with design choices balancing expansion depth to avoid over-expansion that reduces precision. Embedding model validation assesses the model's semantic alignment by correlating embedding similarity with relevance. Inputs are labeled query-document pairs; outputs are validation metrics (e.g., MRR). Design choices include using task-specific validation data, which requires labeled data but ensures model alignment with retrieval goals [[embeddings|Embedding Validation]] and is foundational for [[rag-retrieval-evaluation|Retrieval Evaluation]].

#### 2. Ranking Failure Analysis

Ranking failure occurs when relevant documents are retrieved but ranked below the top-k threshold, preventing their inclusion in the final context. Cross-Encoder reranking refines initial retrieval results by processing query-document pairs through a transformer model (e.g., `cross_encoder(query, document)`), producing more accurate relevance scores than initial retrieval methods. Inputs are the query and candidate documents, outputs are refined relevance scores. This improves precision over sparse/dense retrieval alone but increases latency due to per-pair computation complexity. Cuconasu et al. (2024) demonstrated that irrelevant documents ranked highly degrade LLM performance, highlighting the need for precise ranking. Evaluation metrics MRR (Mean Reciprocal Rank) and nDCG (normalized Discounted Cumulative Gain) measure ranking quality by emphasizing top-position accuracy (MRR) and overall ranking structure (nDCG), standard in [[rag-retrieval-evaluation|retrieval evaluation]]. Hybrid retrieval fuses sparse and dense results, either by rank (reciprocal rank fusion) or by a weighted sum such as `score = w1 * bm25_score + w2 * embedding_score`, which requires normalising the two score scales and tuning the weights.

#### 3. Context Pollution Detection

Context pollution detection employs three core techniques: position-aware relevance analysis, top-k optimization, and metadata filtering validation. Position-aware analysis builds on Liu et al. (2023), who showed that model performance degrades when relevant information sits in the middle of a long context; the remedy is to order the context so that the most relevant chunks come first (or last) and to keep the context short. Top-k optimization determines an optimal k value via retrieval evaluation metrics (e.g., Recall@k) to balance relevance inclusion against pollution risk. Metadata filtering validation uses structured metadata (e.g., document type, date) to exclude irrelevant chunks before context construction, validated through [[rag-retrieval-evaluation|retrieval evaluation]] to maintain high context quality. Cuconasu et al. (2024) found that the retriever's highest-scoring documents that do not contain the answer reduce the LLM's effectiveness, while adding random documents to the prompt even improved accuracy in their experiments. Design trade-offs include smaller k versus missing evidence, and stricter metadata filtering that may reduce recall but significantly improve context relevance. Outputs include a filtered context with reduced pollution risk, while inputs comprise retrieved chunks, query, and metadata.

#### 4. Citation Hallucination Detection

Citation hallucination detection validates generated references against verifiable sources through three integrated steps. First, ALCE benchmark validation uses a standardized dataset of diverse questions and retrieval corpora to assess citation correctness via automatic metrics (fluency, correctness, citation quality), demonstrating that top models lack complete citation support 50% of the time on ELI5 [Gao et al. (2023)]. Second, source database cross-checking matches generated citations (e.g., `Art. 999 DSGVO`) against a pre-validated knowledge base (e.g., legal code repositories) to confirm existence. Third, structured citation output verification enforces a fixed schema (e.g., `{"source": "DSGVO", "article": "999"}`) and checks source presence in the retrieved context. The ALCE benchmark prioritizes reproducibility through end-to-end system evaluation but requires significant setup effort. Cross-checking ensures deterministic validation but depends on database coverage and domain specificity. Structured verification improves consistency and reduces false positives but sacrifices flexibility for natural-language citations, trading off adaptability against reliability in critical domains like legal AI. This approach eliminates LLM-as-a-judge reliance, directly addressing citation hallucination by grounding validation in external evidence.

#### 5. Grounding Hallucination Verification

Grounding hallucination verification ensures claims in generated responses are supported by retrieved context, distinct from citation hallucination (where sources are fabricated). This step employs claim-by-claim grounding: decomposing the response into atomic claims and validating each against context passages. Natural Language Inference (NLI) models compute entailment scores between a claim `c` and context passage `p`, outputting `score = NLI(c, p)` (entailment, contradiction, or neutral). Inputs include the claim set and context passages; outputs are per-claim validation results (grounded if max entailment score exceeds threshold). The algorithm aggregates the highest entailment score across passages for each claim. Design choices prioritize efficiency via NLI (avoiding LLM-as-a-judge) but face trade-offs: context pollution (irrelevant passages) may lower scores, while high recall increases false positives. This method is integrated with [[rag-generation-evaluation|generation evaluation]] to systematically assess grounding quality beyond surface-level citation checks, catching cases where the model attributes a statement to a valid source that does not actually support it.

#### 6. Interpretation Error Analysis

Interpretation error analysis employs LLM-as-a-Judge evaluation, where a secondary LLM assesses generated claims against retrieved context. Inputs include the response text and source context; outputs are binary correctness labels (e.g., `correct = 1`) or confidence scores derived from prompt-based validation. This method leverages the judge's reasoning capabilities but inherits its limitations, so judge verdicts should be spot-checked. Human-in-the-loop validation uses domain experts to review outputs, providing higher accuracy for complex cases like legal grounding hallucination but incurring significant cost and latency. The design trade-off centers on scalability versus precision: LLM-as-a-Judge enables continuous, automated evaluation, while human validation is reserved for critical applications requiring high reliability, as emphasized in grounding hallucination detection protocols [[rag-generation-evaluation|RAG: Generation Evaluation]].

#### Origin and variants

Barnett et al. (2024) derived seven failure points from three case studies in research, education and the biomedical domain: missing content (the answer is not in the corpus), missed top-ranked documents, documents retrieved but not in the context, the answer not extracted from the context, wrong format, incorrect specificity, and incomplete answers. Their two key takeaways are that a RAG system can only be validated during operation and that its robustness evolves rather than being designed in at the start. The failure modes in this note group these points by pipeline stage and add the hallucination types that matter for systems citing their sources (see [[rag-generation-evaluation|generation evaluation]]); Cuconasu et al. (2024) and Liu et al. (2023) add the effects of irrelevant passages and of position in the context.

### When to use it

- High-stakes domains (e.g., biomedical, legal) require failure mode diagnosis to address grounding hallucinations and reduce critical factual errors (Barnett et al. (2024)).
- After deployment, on real queries: Barnett et al. (2024) conclude that validation is only feasible during operation.
- Context pollution diagnosis requires isolating retrieval [[rag-retrieval|retrieval]] or ranking failures, particularly when irrelevant documents degrade output quality (Cuconasu et al. (2024)).
- When answers get worse as more context is added: check the position and number of passages (Liu et al., 2023; Cuconasu et al., 2024).

### Strengths and limitations

**Strengths**
- Enables precise localization of failure points to specific RAG pipeline stages (retrieval, ranking, context, generation), avoiding misattribution to LLM hallucination alone (Barnett et al. (2024)).
- Captures empirical evidence that non-relevant top-scoring documents degrade LLM performance (Cuconasu et al. (2024)), enabling targeted context composition fixes.
- Supports operational validation, in line with the finding that RAG robustness evolves during operation (Barnett et al. (2024)).

**Limitations**
- Some effects are counter-intuitive and not captured by simple relevance checks: adding random documents to the prompt improved LLM accuracy by up to 35% in the experiments of Cuconasu et al. (2024).
- Treats pipeline stages as independent, whereas failures cascade (e.g., retrieval failure causing context pollution via excessive top-k).
- A failure taxonomy names where things go wrong but does not measure how often; it needs the metrics of [[rag-evaluation|RAG evaluation]] to quantify each failure mode.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Stage-wise failure diagnosis | Assigns each wrong answer to the pipeline stage where it originates. | Finding the cause of errors and the component to fix. |
| End-to-end answer metrics | Score only the final answer (correctness, faithfulness). | Tracking overall quality over time. |
| Component metrics | Measure retrieval and generation separately (e.g. Recall@k, citation quality). | Comparing alternatives for one component, see [[rag-retrieval-evaluation|retrieval evaluation]]. |

This framework enables precise error localization across the pipeline, critical for distinguishing between retrieval failures (e.g., missing documents) and generation errors (e.g., citation hallucination), avoiding misdiagnosis of root causes.

### In practice

Evaluation must employ [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] and [[rag-generation-evaluation|RAG: Generation Evaluation]] metrics, with Gao et al. (2023) reporting that even state-of-the-art models lack complete citation support 50% of the time on ELI5. Context position critically affects performance: Liu et al. (2023) observed significant accuracy degradation when relevant information appears in the middle of long contexts, while beginning/end positions yield higher results. Parameter choices should prioritize context relevance: Cuconasu et al. (2024) found that highest-scoring non-relevant documents negatively impact LLM performance, though adding random documents improves accuracy by up to 35%, indicating context filtering must exclude non-relevant content while acknowledging potential benefits from irrelevant context. Top-k values should be optimized via retrieval evaluation to balance recall and relevance, avoiding context pollution.

### Key takeaway

RAG systems reduce hallucinations by grounding responses in retrieved documents but require systematic diagnosis of failure modes across the pipeline (retrieval, ranking, context construction, generation) to identify root causes.

### Sources

- Barnett, S. et al. (2024). *Seven Failure Points When Engineering a Retrieval Augmented Generation System.* [arXiv:2401.05856](https://arxiv.org/abs/2401.05856)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Cuconasu, F. et al. (2024). *The Power of Noise: Redefining Retrieval for RAG Systems.* [arXiv:2401.14887](https://arxiv.org/abs/2401.14887)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

RAG-Fehlermodi definieren die unterschiedlichen Fehlerpunkte innerhalb des RAG-Pipelines (Retrieval, Ranking, Kontextkonstruktion, Generierung), die fehlerhafte Ausgaben verursachen, wie z. B. Retrieval-Fehler oder Kontextverschmutzung. Dieses Framework ermöglicht eine systematische Fehlerdiagnose, um Ursachen zu identifizieren, die Systemrobustheit zu verbessern und Halluzinationen zu reduzieren, ohne allein auf die Generierung durch das Sprachmodell zu vertrauen.

### Funktionsweise

Das Framework zur Diagnose von RAG-Fehlern verwendet einen sequenziellen Diagnoseprozess über sechs Fehlermodi, wobei jeder Fehlermodus einem bestimmten Pipeline-Stadium entspricht (z. B. [[rag-retrieval|Retrieval]] für Retrieval-Fehler und [[rag-generation-evaluation|Generation Evaluation]] für generationbezogene Fehler), um Ursachen ohne Verwechslung von Symptomen zu isolieren. Barnett et al. (2024), die drei RAG-Fallstudien berichten, schlussfolgern, dass ein RAG-System erst während des Betriebs wirklich validiert werden kann, daher muss die Diagnose auf realen Abfragen wiederholt werden.

```text
Pipeline-Stadium        Fehlermodus             typischer Check
Retrieval           ─▶  Passage nicht abgerufen  Hit Rate / Recall@k
Ranking             ─▶  unter Schwellenwert gerankt  MRR, nDCG, Reranking
Kontext             ─▶  Kontextverschmutzung     top-k, Filter, Reihenfolge
Generierung         ─▶  Zitierhalluzination     Zitatscheck
Generierung         ─▶  Grundierungshalluzination  claim-level NLI
Generierung         ─▶  Interpretationsfehler   LLM-Judge, Experten
```

#### 1. Erkennung von Retrieval-Fehlern

Ein Retrieval-Fehler bedeutet, dass der benötigte Absatz für die Antwort überhaupt nicht unter den abgerufenen Ergebnissen enthalten ist. Er wird mit der Trefferquote (auch success@k) gemessen: den Bruchteil der Abfragen, bei denen mindestens ein relevanter Dokument in den Top k enthalten ist, `hit_rate@k = (1 / N) * sum_i [relevanter Dokument in Top k für Abfrage i]`; Recall@k zählt zusätzlich, wie viele der insgesamt relevanten Dokumente gefunden wurden. Dieses binäre Metrik priorisiert Recall, um Retrieval-Fehler zu minimieren, beachtet jedoch nicht die Position innerhalb der Top k. Die Analyse der Abfrageerweiterung testet den Einfluss des Hinzufügens von Begriffen (z. B. Synonymen) zu Abfragen auf die Retrieval-Leistung. Eingaben umfassen ursprüngliche Abfragen und Erweiterungsbegriffe; Ausgaben sind Leistungsmetriken, die erweiterte Abfragen mit Basisabfragen vergleichen. Der Algorithmus generiert typischerweise Erweiterungen über Wörterbücher oder Korpusanalyse und führt Retrieval erneut durch, wobei Gestaltungswahl die Erweiterungstiefe ausbalancieren, um Übererweiterung zu vermeiden, die die Präzision reduziert. Die Validierung des Embedding-Modells bewertet die semantische Übereinstimmung des Modells, indem die Korrelation zwischen Embedding-Ähnlichkeit und Relevanz hergestellt wird. Eingaben sind etikettierte Abfrage-Dokument-Paare; Ausgaben sind Validierungsmetriken (z. B. MRR). Gestaltungswahl umfasst die Verwendung von task-spezifischen Validierungsdaten, was zwar etikettierte Daten erfordert, aber sicherstellt, dass das Modell mit Retrieval-Zielen übereinstimmt [[embeddings|Embedding-Validierung]] und grundlegend für [[rag-retrieval-evaluation|Retrieval-Bewertung]] ist.

#### 2. Analyse von Ranking-Fehlern

Ein Ranking-Fehler tritt auf, wenn relevante Dokumente zwar abgerufen, aber unterhalb des Schwellenwerts der obersten k Ergebnisse rangiert werden, wodurch sie nicht in den finalen Kontext aufgenommen werden. Das Cross-Encoder-Reranking verfeinert die ursprünglichen Suchergebnisse, indem es Paare aus Abfrage und Dokument durch ein Transformer-Modell verarbeitet (z. B. `cross_encoder(query, document)`), wodurch präzisere Relevanzwerte als bei den ursprünglichen Retrieval-Methoden erzeugt werden. Die Eingaben sind die Abfrage und die Kandidatendokumente, die Ausgaben sind verfeinerte Relevanzwerte. Dies verbessert die Präzision im Vergleich zu Sparse/Dense Retrieval allein, erhöht aber aufgrund der Komplexität der pro-Paar-Berechnung die Latenz. Cuconasu et al. (2024) zeigten, dass Dokumente, die irrelevant sind, aber hoch rangiert werden, die Leistung von LLMs beeinträchtigen, was die Notwendigkeit präziser Rangierungen unterstreicht. Die Bewertungsmetriken MRR (Mean Reciprocal Rank) und nDCG (normalized Discounted Cumulative Gain) messen die Qualität des Rankings, indem sie die Genauigkeit der obersten Positionen (MRR) und die Gesamtrangstruktur (nDCG) betonen, was in [[rag-retrieval-evaluation|retrieval evaluation]] Standard ist. Hybrid Retrieval kombiniert Sparse- und Dense-Ergebnisse, entweder durch Rang (reciprocal rank fusion) oder durch einen gewichteten Summenansatz wie `score = w1 * bm25_score + w2 * embedding_score`, was die Normalisierung der beiden Bewertungsskalen und die Anpassung der Gewichte erfordert.

#### 3. Erkennung von Kontextverschmutzung

Die Erkennung von Kontextverschmutzung verwendet drei Kernmethoden: positionsbasierte Relevanzanalyse, Top-k-Optimierung und Validierung durch Metadatenfilterung. Die positionsbasierte Analyse baut auf Liu et al. (2023) auf, die zeigten, dass die Modellleistung abnimmt, wenn relevante Informationen in der Mitte eines langen Kontextes liegen; die Lösung besteht darin, den Kontext so zu ordnen, dass die am relevantesten Teile zuerst (oder zuletzt) stehen und den Kontext kurz zu halten. Die Top-k-Optimierung bestimmt einen optimalen k-Wert über Retrieval-Evaluationsmetriken (z. B. Recall@k), um die Einbeziehung von Relevanz mit dem Risiko der Verschmutzung abzuwägen. Die Validierung durch Metadatenfilterung nutzt strukturierte Metadaten (z. B. Dokumenttyp, Datum), um irrelevante Abschnitte vor der Kontexterstellung zu filtern, wodurch [[rag-retrieval-evaluation|retrieval evaluation]] gewährleistet wird, um eine hohe Kontextqualität zu erhalten. Cuconasu et al. (2024) fanden heraus, dass die vom Retriever erzielten Dokumente mit der höchsten Bewertung, die die Antwort nicht enthalten, die Effektivität des LLM verringern, während das Hinzufügen zufälliger Dokumente im Prompt in ihren Experimenten sogar die Genauigkeit verbesserte. Design-Kompromisse umfassen ein kleineres k im Vergleich zum Verlust von Beweisen und strengere Metadatenfilterung, die zwar Recall reduzieren können, aber die Kontextrelevanz erheblich verbessern. Die Ausgaben umfassen einen gefilterten Kontext mit reduziertem Risiko der Verschmutzung, während die Eingaben aus den abgerufenen Abschnitten, der Abfrage und den Metadaten bestehen.

#### 4. Zitierhalluzinationserkennung

Die Erkennung von Zitierhalluzinationen überprüft generierte Quellenangaben anhand überprüfbare Quellen durch drei integrierte Schritte. Erstens erfolgt die ALCE-Benchmark-Validierung mit einer standardisierten Datensammlung aus unterschiedlichen Fragen und Retrieval-Korpora, um die Richtigkeit der Zitierungen mithilfe automatischer Metriken (Flüssigkeit, Richtigkeit, Zitierqualität) zu bewerten. Dabei zeigt sich, dass die besten Modelle in 50 % der Fälle auf ELI5 keine vollständige Zitierunterstützung besitzen [Gao et al. (2023)]. Zweitens erfolgt die Quellendatenbank-Überprüfung, bei der generierte Zitierungen (z. B. `Art. 999 DSGVO`) mit einer vorab validierten Wissensbasis (z. B. rechtliche Code-Repositories) abgeglichen werden, um ihre Existenz zu bestätigen. Drittens erfolgt die strukturierte Zitierausgabeverifikation, bei der ein fester Schema (z. B. `{"source": "DSGVO", "article": "999"}`) erzwungen wird und die Prüfung erfolgt, ob die Quelle im abgerufenen Kontext vorhanden ist. Der ALCE-Benchmark priorisiert Wiederherstellungsfähigkeit durch eine End-to-End-Systembewertung, erfordert aber erhebliche Aufwandskosten bei der Einrichtung. Die Überprüfung stellt deterministische Validierung sicher, hängt aber von der Datenbankabdeckung und der Domain-Spezifität ab. Die strukturierte Verifikation verbessert Konsistenz und reduziert Falschpositive, opfert aber Flexibilität bei natürlichsprachlichen Zitierungen und tauscht Anpassungsfähigkeit gegen Zuverlässigkeit in kritischen Bereichen wie rechtlicher KI. Dieser Ansatz beseitigt die Abhängigkeit von LLM-as-a-judge und adressiert direkt die Zitierhalluzination, indem die Validierung auf externem Beweis basiert.

#### 5. Verifikation von Halluzinationen durch Verankerung

Die Verifikation von Halluzinationen durch Verankerung stellt sicher, dass Aussagen in generierten Antworten durch abgerufene Kontexte unterstützt werden, was sich von der Zitier-Halluzination (bei der Quellen erfunden werden) unterscheidet. Dieser Schritt verwendet eine Verankerung pro Aussage: die Aufteilung der Antwort in atomare Aussagen und die Validierung jeder Aussage gegenüber Kontextpassagen. Modelle für natürliche Sprachinferenz (NLI) berechnen Schlussfolgerungsscores zwischen einer Aussage `c` und einer Kontextpassage `p`, wodurch `score = NLI(c, p)` (Implikation, Widerspruch oder neutral) ausgegeben wird. Die Eingaben umfassen die Menge der Aussagen und die Kontextpassagen; die Ausgaben sind Validierungsergebnisse pro Aussage (verankert, wenn der maximale Schlussfolgerungsscore den Schwellenwert überschreitet). Der Algorithmus aggregiert den höchsten Schlussfolgerungsscore über alle Passagen für jede Aussage. Die Gestaltungswahl priorisiert Effizienz durch NLI (Vermeidung von LLM-as-a-judge), trifft aber Kompromisse: Kontextverschmutzung (irrelevante Passagen) kann die Scores senken, während eine hohe Recall-Rate zu falsch positiven Ergebnissen führt. Dieses Verfahren wird mit [[rag-generation-evaluation|Generationsbewertung]] integriert, um die Qualität der Verankerung systematisch zu bewerten, überflächliche Zitierprüfungen hinausgehend, und Fälle zu erkennen, bei denen das Modell eine Aussage einem gültigen Quelltext zuordnet, der sie tatsächlich nicht unterstützt.

#### 6. Analyse von Interpretationsfehlern

Die Analyse von Interpretationsfehlern verwendet die LLM-as-a-Judge-Bewertung, bei der ein sekundäres LLM die generierten Aussagen anhand des abgerufenen Kontexts bewertet. Die Eingaben umfassen den Antworttext und den Quellkontext; die Ausgaben sind binäre Richtigkeitslabels (z. B. `correct = 1`) oder Konfidenzwerte, die aus promptbasierten Validierungen abgeleitet werden. Dieses Verfahren nutzt die Fähigkeit des Richters zum logischen Denken, erbt aber auch dessen Einschränkungen, weshalb die Urteile des Richters überprüft werden sollten. Die Validierung mit einem Menschen im Schleifenprozess verwendet Fachexperten, um die Ergebnisse zu prüfen, wodurch eine höhere Genauigkeit bei komplexen Fällen wie der Halluzination durch rechtliche Grundlagen gewährleistet wird, birgt aber erhebliche Kosten und Latenz. Der Design-Kompromiss konzentriert sich auf Skalierbarkeit versus Präzision: LLM-as-a-Judge ermöglicht eine kontinuierliche, automatisierte Bewertung, während die menschliche Validierung für kritische Anwendungen mit hoher Zuverlässigkeit reserviert ist, wie es in den Protokollen zur Halluzinationsdetektion bei der Grundierung betont wird [[rag-generation-evaluation|RAG: Generierungsbewertung]].

#### Ursprung und Varianten

Barnett et al. (2024) leiteten aus drei Fallstudien im Forschungs-, Bildungs- und Biomedizinbereich sieben Fehlerpunkte ab: fehlender Inhalt (die Antwort ist nicht im Corpus), übersehene, eigentlich hoch eingestufte Dokumente, Dokumente, die abgerufen wurden, aber nicht im Kontext enthalten sind, die Antwort wird nicht aus dem Kontext extrahiert, falsches Format, falsche Spezifität und unvollständige Antworten. Ihre beiden zentralen Erkenntnisse sind, dass ein RAG-System nur während des Betriebs validiert werden kann und dass seine Robustheit sich entwickelt, anstatt von vornherein entworfen zu werden. Die Fehlerarten in dieser Notiz gruppieren diese Punkte nach Verarbeitungsschritten und fügen die Halluzinationstypen hinzu, die für Systeme relevant sind, die ihre Quellen zitieren (siehe [[rag-generation-evaluation|Generierungsbewertung]]); Cuconasu et al. (2024) und Liu et al. (2023) fügen die Effekte von irrelevanten Passagen und der Position im Kontext hinzu.

### Wann einsetzen

- Hochrisko-Bereiche (z. B. biomedizinisch, rechtlich) erfordern die Diagnose von Fehlern im Fehlverhalten, um Halluzinationen bei der Verankerung zu beheben und kritische Faktenfehler zu reduzieren (Barnett et al. (2024)).
- Nach der Bereitstellung bei echten Abfragen: Barnett et al. (2024) schlussfolgern, dass die Validierung nur während des Betriebs durchführbar ist.
- Die Diagnose von Kontextverschmutzung erfordert die Isolierung von [[rag-retrieval|retrieval]]- oder Rangfolgefehlern, insbesondere wenn irrelevante Dokumente die Ausgabegüte verringern (Cuconasu et al. (2024)).
- Wenn Antworten schlechter werden, wenn mehr Kontext hinzugefügt wird: prüfen Sie die Position und Anzahl der Abschnitte (Liu et al., 2023; Cuconasu et al., 2024).

### Stärken und Grenzen

**Stärken**
- Ermöglicht die präzise Lokalisierung von Fehlern auf spezifische Stufen des RAG-Pipelines (retrieval, ranking, context, generation), vermeidet falsche Zuordnungen aufgrund von Halluzinationen des LLM allein (Barnett et al. (2024)).
- Erfasst empirische Beweise, dass nicht relevante, hoch bewertete Dokumente die Leistung des LLM beeinträchtigen (Cuconasu et al. (2024)), ermöglicht gezielte Korrekturen bei der Kontextzusammensetzung.
- Unterstützt die operativen Validierung, im Einklang mit der Erkenntnis, dass die Robustheit von RAG während des Betriebs zunimmt (Barnett et al. (2024)).

**Einschränkungen**
- Einige Effekte sind nicht intuitiv und werden nicht durch einfache Relevanzchecks erfasst: das Hinzufügen zufälliger Dokumente zum Prompt verbesserte die Genauigkeit des LLM in den Experimenten von Cuconasu et al. (2024) um bis zu 35 %.
- Behandelt die Pipeline-Stufen als unabhängig, während Fehler sich kaskadieren (z. B. Retrieval-Fehler führen durch zu großes top-k zur Kontaminierung des Kontexts).
- Eine Fehlerklassifizierung benennt, wo Dinge schiefgehen, misst jedoch nicht, wie häufig; sie benötigt die Metriken von [[rag-evaluation|RAG evaluation]], um jeden Fehlermodus zu quantifizieren.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Stufenweises Fehlerspezifizierung | Weist jede falsche Antwort dem Schritt im Pipeline zu, aus dem sie stammt. | Ursachen von Fehlern und den zu reparierenden Komponenten zu finden. |
| End-to-end-Antwermetriken | Bewertet nur die finale Antwort (Richtigkeit, Faithfulness). | Die Gesamtqualität im Laufe der Zeit zu verfolgen. |
| Komponentenmetriken | Messen Retrieval und Generierung getrennt (z. B. Recall@k, Zitierqualität). | Alternativen für eine Komponente zu vergleichen, siehe [[rag-retrieval-evaluation|Retrieval-Bewertung]]. |

Dieses Framework ermöglicht eine präzise Lokalisierung von Fehlern im Pipeline, was entscheidend ist, um zwischen Retrieval-Fehlern (z. B. fehlende Dokumente) und Generierungsfehlern (z. B. Zitierhalluzinationen) zu unterscheiden und Fehldiagnosen der Ursachen zu vermeiden.

### In der Praxis

Die Bewertung muss [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und [[rag-generation-evaluation|RAG: Generation Evaluation]]-Metriken verwenden. Gao et al. (2023) berichten, dass selbst state-of-the-art-Modelle 50 % der Zeit auf ELI5 keine vollständige Zitierunterstützung besitzen. Die Position des Kontexts beeinflusst die Leistung entscheidend: Liu et al. (2023) beobachteten eine erhebliche Genauigkeitsverschlechterung, wenn relevante Informationen in der Mitte langer Kontexte auftreten, während Positionen am Anfang oder Ende bessere Ergebnisse liefern. Parameterauswahlen sollten die Kontextrelevanz priorisieren: Cuconasu et al. (2024) fanden heraus, dass Dokumente mit der höchsten Bewertung, die nicht relevant sind, die Leistung von LLM negativ beeinflussen, obwohl das Hinzufügen zufälliger Dokumente die Genauigkeit um bis zu 35 % verbessert, was darauf hindeutet, dass das Kontextfiltern nicht-relevante Inhalte ausschließen muss, während mögliche Vorteile aus irrelevantem Kontext berücksichtigt werden. Top-k-Werte sollten über Retrieval-Bewertungen optimiert werden, um Erinnerung und Relevanz zu balancieren und Kontextverschmutzung zu vermeiden.

### Merksatz

RAG-Systeme reduzieren Halluzinationen, indem sie Antworten in abgerufenen Dokumenten verankern, erfordern jedoch eine systematische Diagnose von Fehlern im gesamten Pipeline-Prozess (Abfrage, Rangfolge, Kontextkonstruktion, Generierung), um Ursachen zu identifizieren.

### Quellen

- Barnett, S. et al. (2024). *Seven Failure Points When Engineering a Retrieval Augmented Generation System.* [arXiv:2401.05856](https://arxiv.org/abs/2401.05856)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Cuconasu, F. et al. (2024). *The Power of Noise: Redefining Retrieval for RAG Systems.* [arXiv:2401.14887](https://arxiv.org/abs/2401.14887)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
