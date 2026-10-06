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

The framework for diagnosing RAG failures employs a sequential diagnostic process across six failure modes, each corresponding to a specific pipeline stage (e.g., [[rag-retrieval|Retrieval]] for retrieval failures and [[rag-generation-evaluation|Generation Evaluation]] for generation-related failures), to isolate root causes without conflating symptoms. This approach aligns with Barnett et al. (2024), who identified that RAG system validation requires operational analysis to trace errors from initial retrieval to final interpretation.

```text
Retrieval Failure Detection
─▶
Ranking Failure Analysis
─▶
Context Pollution Detection
─▶
Citation Hallucination Detection
─▶
Grounding Hallucination Verification
─▶
Interpretation Error Analysis
```

#### 1. Retrieval Failure Detection

Recall@k evaluation quantifies the fraction of queries for which at least one relevant document appears within the top k retrieved results. Inputs comprise a query set and ranked document lists per query; outputs are the Recall@k metric computed as `Recall@k = (1 / N) * sum_{i=1}^{N} (1 if relevant in top k else 0)`. This binary metric prioritizes recall to minimize retrieval failures, though it ignores rank position within top k. Query expansion analysis tests the impact of adding terms (e.g., synonyms) to queries on retrieval performance. Inputs include original queries and expansion terms; outputs are performance metrics comparing expanded vs. base queries. The algorithm typically generates expansions via thesauri or corpus analysis and re-runs retrieval, with design choices balancing expansion depth to avoid over-expansion that reduces precision. Embedding model validation assesses the model's semantic alignment by correlating embedding similarity with relevance. Inputs are labeled query-document pairs; outputs are validation metrics (e.g., MRR). Design choices include using task-specific validation data, which requires labeled data but ensures model alignment with retrieval goals [[embeddings|Embedding Validation]] and is foundational for [[rag-retrieval-evaluation|Retrieval Evaluation]].

#### 2. Ranking Failure Analysis

Ranking failure occurs when relevant documents are retrieved but ranked below the top-k threshold, preventing their inclusion in the final context. Cross-Encoder reranking refines initial retrieval results by processing query-document pairs through a transformer model (e.g., `cross_encoder(query, document)`), producing more accurate relevance scores than initial retrieval methods. Inputs are the query and candidate documents, outputs are refined relevance scores. This improves precision over sparse/dense retrieval alone but increases latency due to per-pair computation complexity. Cuconasu et al. (2024) demonstrated that irrelevant documents ranked highly degrade LLM performance, highlighting the need for precise ranking. Evaluation metrics MRR (Mean Reciprocal Rank) and nDCG (normalized Discounted Cumulative Gain) measure ranking quality by emphasizing top-position accuracy (MRR) and overall ranking structure (nDCG), standard in [[rag-retrieval-evaluation|retrieval evaluation]]. Hybrid retrieval scoring fuses multiple retrieval methods (e.g., sparse and dense) using weighted combinations like `score = w1 * bm25_score + w2 * embedding_score`, balancing recall and precision. Design choices prioritize robustness over speed but require careful hyperparameter tuning, trading computational cost for improved ranking accuracy.

#### 3. Context Pollution Detection

Context pollution detection employs three core techniques: position-aware relevance analysis, top-k optimization, and metadata filtering validation. Position-aware analysis (Liu et al. 2023) demonstrates that model performance degrades when relevant information is positioned centrally within long contexts, necessitating position-weighted scoring where `score = 1 / (k + rank)` to prioritize boundary chunks. Top-k optimization determines an optimal k value via retrieval evaluation metrics (e.g., Recall@k) to balance relevance inclusion against pollution risk. Metadata filtering validation uses structured metadata (e.g., document type, date) to exclude irrelevant chunks before context construction, validated through [[rag-retrieval-evaluation|retrieval evaluation]] to maintain high context quality. Design trade-offs include computational overhead for position weighting versus pollution reduction, and stricter metadata filtering that may reduce recall but significantly improve context relevance. Outputs include a filtered context with reduced pollution risk, while inputs comprise retrieved chunks, query, and metadata.

#### 4. Citation Hallucination Detection

Citation hallucination detection validates generated references against verifiable sources through three integrated steps. First, ALCE benchmark validation uses a standardized dataset of diverse questions and retrieval corpora to assess citation correctness via automatic metrics (fluency, correctness, citation quality), demonstrating that top models lack complete citation support 50% of the time on ELI5 [Gao et al. (2023)]. Second, source database cross-checking matches generated citations (e.g., `Art. 999 DSGVO`) against a pre-validated knowledge base (e.g., legal code repositories) to confirm existence. Third, structured citation output verification enforces a fixed schema (e.g., `{"source": "DSGVO", "article": "999"}`) and checks source presence in the retrieved context. The ALCE benchmark prioritizes reproducibility through end-to-end system evaluation but requires significant setup effort. Cross-checking ensures deterministic validation but depends on database coverage and domain specificity. Structured verification improves consistency and reduces false positives but sacrifices flexibility for natural-language citations, trading off adaptability against reliability in critical domains like legal AI. This approach eliminates LLM-as-a-judge reliance, directly addressing citation hallucination by grounding validation in external evidence.

#### 5. Grounding Hallucination Verification

Grounding hallucination verification ensures claims in generated responses are supported by retrieved context, distinct from citation hallucination (where sources are fabricated). This step employs claim-by-claim grounding: decomposing the response into atomic claims and validating each against context passages. Natural Language Inference (NLI) models compute entailment scores between a claim `c` and context passage `p`, outputting `score = NLI(c, p)` (entailment, contradiction, or neutral). Inputs include the claim set and context passages; outputs are per-claim validation results (grounded if max entailment score exceeds threshold). The algorithm aggregates the highest entailment score across passages for each claim. Design choices prioritize efficiency via NLI (avoiding LLM-as-a-judge) but face trade-offs: context pollution (irrelevant passages) may lower scores, while high recall increases false positives. This method is integrated with [[rag-generation-evaluation|generation evaluation]] to systematically assess grounding quality beyond surface-level citation checks, addressing limitations noted in RAG systems where LLMs may incorrectly attribute support even with valid sources (Barnett et al. 2024).

#### 6. Interpretation Error Analysis

Interpretation error analysis employs LLM-as-a-Judge evaluation, where a secondary LLM assesses generated claims against retrieved context. Inputs include the response text and source context; outputs are binary correctness labels (e.g., `correct = 1`) or confidence scores derived from prompt-based validation. This method leverages the LLM's reasoning capabilities but inherits its limitations, as Gao et al. (2023) demonstrated that state-of-the-art models lack complete citation support 50% of the time in ALCE benchmark tests. Human-in-the-loop validation uses domain experts to review outputs, providing higher accuracy for complex cases like legal grounding hallucination but incurring significant cost and latency. The design trade-off centers on scalability versus precision: LLM-as-a-Judge enables continuous, automated evaluation, while human validation is reserved for critical applications requiring high reliability, as emphasized in grounding hallucination detection protocols [[rag-generation-evaluation|RAG: Generation Evaluation]].

#### Origin and variants

Barnett et al. (2024) established a 7-point failure framework through case studies in research, education, and biomedical RAG deployments, analyzing the transformation of input queries and knowledge bases into generated outputs. The framework categorizes failures by pipeline stages (retrieval, ranking, context construction, generation), with key failure points including retrieval misses, ranking inaccuracies, and context pollution. A core finding is that robustness evolves through operational validation rather than initial design, requiring continuous monitoring of real-world usage. This approach prioritizes iterative refinement over static pre-deployment testing, trading upfront development efficiency for adaptability. For instance, context pollution often stems from suboptimal top-k retrieval thresholds (as in [[rag-retrieval|retrieval]]), where excessive context inclusion introduces noise that degrades generation quality. The framework's design choice acknowledges that failure modes are context-dependent and emerge during operation, making robustness a dynamic property rather than a fixed system attribute. Consequently, validation must occur in production environments, not during development.

### When to use it

- High-stakes domains (e.g., biomedical, legal) require failure mode diagnosis to address grounding hallucinations and reduce critical factual errors (Barnett et al. (2024)).
- Operational deployment necessitates continuous failure mode diagnosis, as validation is only feasible during real-world system operation (Barnett et al. (2024)).
- Context pollution diagnosis requires isolating retrieval [[rag-retrieval|retrieval]] or ranking failures, particularly when irrelevant documents degrade output quality (Cuconasu et al. (2024)).
- Long-context applications demand failure mode diagnosis to identify retrieval ranking failures causing performance degradation when relevant information is not positioned at context boundaries (Liu et al. (2023)).

### Strengths and limitations

**Strengths**
- Enables precise localization of failure points to specific RAG pipeline stages (retrieval, ranking, context, generation), avoiding misattribution to LLM hallucination alone (Barnett et al. (2024)).
- Captures empirical evidence that non-relevant top-scoring documents degrade LLM performance (Cuconasu et al. (2024)), enabling targeted context composition fixes.
- Facilitates operational validation by aligning with the finding that RAG robustness evolves during deployment, not design (Barnett et al. (2024)).

**Limitations**
- Does not account for counter-intuitive findings like random document addition improving LLM accuracy by up to 35% (Cuconasu et al. (2024)), suggesting gaps in failure mode coverage.
- Treats pipeline stages as independent, whereas failures cascade (e.g., retrieval failure causing context pollution via excessive top-k).
- Lacks integration of quantitative failure metrics (e.g., 50% citation support failure rate on ELI5, Gao et al. (2023)), requiring complementary evaluation frameworks.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| RAG Failure Modes Framework | Explicitly categorizes failures by pipeline stage (retrieval, ranking, context construction, generation), whereas LLM hallucination analysis (e.g., Gao et al. (2023)) attributes all errors to generation without pipeline context, and retrieval-centric analysis (e.g., Liu et al. (2023)) focuses only on retrieval and context position without addressing context construction or generation failures. | Systematic root cause diagnosis for improving RAG robustness, as failures often originate upstream (Barnett et al. (2024)). |
| LLM Hallucination Analysis | Attributes all errors to LLM generation hallucinations, ignoring upstream pipeline failures (e.g., Gao et al. (2023) found 50% of answers lack citation support, but did not diagnose retrieval failure). | Evaluating generation output for hallucination (e.g., [[rag-generation-evaluation|generation evaluation]]), but fails to identify upstream causes. |
| Retrieval-Centric Failure Analysis | Focuses exclusively on retrieval and ranking performance (e.g., Liu et al. (2023) showed LLMs degrade when relevant information is in the middle of context), ignoring context construction and generation errors. | Optimizing retrieval (e.g., [[rag-retrieval|retrieval evaluation]]), but misses failures in context composition or generation. |
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

RAG-Fehlermodi definieren die unterschiedlichen Fehlerpunkte innerhalb des RAG-Pipelines (Retrieval, Ranking, Kontextkonstruktion, Generierung), die fehlerhafte Ausgaben verursachen, wie z. B. Retrieval-Fehler oder Kontextverschmutzung. Dieses Framework ermöglicht eine systematische Fehlerdiagnose, um Ursachen zu identifizieren, die Systemrobustheit zu verbessern und Halluzinationen zu reduzieren, ohne allein auf die Generierung durch das Sprachmodell zu verlassen.

### Funktionsweise

Das Framework zur Diagnose von RAG-Fehlern verwendet einen sequenziellen diagnostischen Prozess über sechs Fehlermodi, wobei jeder Fehlermodus einem bestimmten Pipeline-Stadium entspricht (z. B. [[rag-retrieval|Retrieval]] für Retrieval-Fehler und [[rag-generation-evaluation|Generation Evaluation]] für generierungsbezogene Fehler), um Ursachen ohne Verwechslung von Symptomen zu isolieren. Dieser Ansatz entspricht Barnett et al. (2024), die feststellten, dass die Validierung von RAG-Systemen eine operatives Analyse erfordert, um Fehler von der ursprünglichen Retrieval-Phase bis zur finalen Interpretation nachzuverfolgen.

```text
Retrieval-Fehlererkennung
─▶
Ranking-Fehleranalyse
─▶
Kontextverschmutzungserkennung
─▶
Zitierhalluzinationserkennung
─▶
Grundierungshalluzinationssicherung
─▶
Interpretationsfehleranalyse
```

#### 1. Retrieval-Fehlererkennung

Die Recall@k-Bewertung quantifiziert den Anteil der Abfragen, bei denen mindestens ein relevanter Dokument innerhalb der Top-k-Ergebnisse vorkommt. Die Eingaben bestehen aus einer Abfragesammlung und sortierten Dokumentlisten pro Abfrage; die Ausgaben sind die Recall@k-Metrik, berechnet als `Recall@k = (1 / N) * sum_{i=1}^{N} (1 wenn relevant in top k sonst 0)`. Dieses binäre Metrikpriorisierungssystem fördert Recall, um Retrieval-Fehler zu minimieren, ignoriert jedoch die Position innerhalb der Top-k. Die Analyse der Abfrageerweiterung testet den Einfluss des Hinzufügens von Begriffen (z. B. Synonymen) auf die Retrieval-Leistung. Eingaben umfassen ursprüngliche Abfragen und Erweiterungsbegriffe; Ausgaben sind Leistungsmetriken, die erweiterte Abfragen mit Basiskriterien vergleichen. Der Algorithmus generiert in der Regel Erweiterungen über Wörterbücher oder Korpusanalysen und führt Retrieval erneut durch, wobei Gestaltungswahl die Erweiterungstiefe ausgewählt, um Übererweiterungen zu vermeiden, die die Präzision reduzieren. Die Validierung des Embedding-Modells bewertet die semantische Übereinstimmung des Modells, indem die Ähnlichkeit der Embedding-Embedding mit der Relevanz korreliert. Eingaben sind etikettierte Abfrage-Dokument-Paare; Ausgaben sind Validierungsmetriken (z. B. MRR). Gestaltungswahl umfasst die Verwendung von datenspezifischen Validierungsdaten, was zwar etikettierte Daten erfordert, aber sicherstellt, dass das Modell mit Retrieval-Zielen übereinstimmt [[embeddings|Embedding-Validierung]] und grundlegend für [[rag-retrieval-evaluation|Retrieval-Bewertung]] ist.

#### 2. Ranking-Fehleranalyse

Ein Ranking-Fehler tritt auf, wenn relevante Dokumente abgerufen werden, aber unter dem Top-k-Schwellenwert rangiert werden, wodurch sie nicht in den endgültigen Kontext aufgenommen werden. Das Cross-Encoder-Reranking verbessert die ursprünglichen Retrieval-Ergebnisse, indem es Abfrage-Dokument-Paare durch ein Transformer-Modell verarbeitet (z. B. `cross_encoder(query, document)`), wodurch präzisere Relevanzscores erzeugt werden als bei ursprünglichen Retrieval-Methoden. Eingaben sind die Abfrage und Kandidatendokumente; Ausgaben sind verfeinerte Relevanzscores. Dies verbessert die Präzision über Sparse/Dense Retrieval allein, erhöht aber aufgrund der Komplexität der pro-Paar-Berechnung die Latenz. Cuconasu et al. (2024) zeigten, dass Dokumente, die irrelevant sind, aber hoch rangiert werden, die Leistung von LLMs beeinträchtigen, was die Notwendigkeit präziser Ranking-Methoden unterstreicht. Die Bewertungsmetriken MRR (Mean Reciprocal Rank) und nDCG (normalized Discounted Cumulative Gain) messen die Qualität des Rankings, indem sie die Genauigkeit der obersten Position (MRR) und die allgemeine Struktur des Rankings (nDCG) betonen, was Standard in [[rag-retrieval-evaluation|Retrieval-Bewertung]] ist. Hybrid-Retrieval-Bewertung kombiniert mehrere Retrieval-Methoden (z. B. Sparse und Dense) mithilfe von gewichteten Kombinationen wie `score = w1 * bm25_score + w2 * embedding_score`, um Recall und Präzision auszugleichen. Gestaltungswahl priorisiert Robustheit gegenüber Geschwindigkeit, erfordert aber sorgfältige Hyperparameter-Feinabstimmung, wodurch der rechnerische Aufwand gegen verbesserte Rankinggenauigkeit getauscht wird.

#### 3. Kontextverschmutzungserkennung

Die Erkennung von Kontextverschmutzung verwendet drei Kernmethoden: positionsbewusste Relevanzanalyse, Top-k-Optimierung und Validierung der Metadatenfilterung. Die positionsbewusste Analyse (Liu et al. 2023) zeigt, dass die Modellleistung abnimmt, wenn relevante Informationen zentral in langen Kontexten positioniert sind, wodurch ein positionsgewichteter Score erforderlich ist, bei dem `score = 1 / (k + rank)` verwendet wird, um Randabschnitte zu priorisieren. Die Top-k-Optimierung bestimmt einen optimalen k-Wert über Retrieval-Bewertungsmetriken (z. B. Recall@k), um die Balance zwischen Relevanz und Verschmutzungsrisiko zu gewährleisten. Die Validierung der Metadatenfilterung verwendet strukturierte Metadaten (z. B. Dokumenttyp, Datum), um irrelevante Abschnitte vor der Kontextkonstruktion zu entfernen, wodurch [[rag-retrieval-evaluation|Retrieval-Bewertung]] validiert wird, um eine hohe Kontextqualität zu gewährleisten. Gestaltungskompromisse umfassen den rechnerischen Aufwand für Positionsgewichtung gegenüber der Reduktion von Verschmutzung und strengere Metadatenfilterung, die Recall reduzieren kann, aber die Kontextrelevanz erheblich verbessert. Ausgaben umfassen einen gefilterten Kontext mit reduziertem Verschmutzungsrisiko, während Eingaben aus abgerufenen Abschnitten, Abfragen und Metadaten bestehen.

#### 4. Zitierhalluzinationserkennung

Die Erkennung von Zitierhalluzinationen validiert generierte Referenzen anhand verifizierbarer Quellen durch drei integrierte Schritte. Erstens wird die ALCE-Benchmark-Validierung mit einem standardisierten Datensatz aus diversen Fragen und Retrieval-Korpora verwendet, um die Zitierkorrektheit über automatische Metriken (Flüssigkeit, Korrektheit, Zitierqualität) zu bewerten, wodurch gezeigt wird, dass die besten Modelle 50 % der Zeit auf ELI5 keine vollständige Zitierunterstützung haben [Gao et al. (2023)]. Zweitens wird die Quellendatenbank-Überprüfung verwendet, um generierte Zitierungen (z. B. `Art. 999 DSGVO`) mit einer vorab validierten Wissensbasis (z. B. rechtlichen Code-Repositories) zu übereinstimmen, um ihre Existenz zu bestätigen. Drittens wird die strukturierte Zitierausgabeverifikation verwendet, um einen festen Schema (z. B. `{"source": "DSGVO", "article": "999"}`) zu erzwingen und die Existenz der Quelle im abgerufenen Kontext zu prüfen. Die ALCE-Benchmark priorisiert Wiederherstellungsfähigkeit durch end-to-end-Systembewertung, erfordert aber erhebliche Aufwand. Die Überprüfung stellt deterministische Validierung sicher, hängt aber von Datenbankabdeckung und Domainspezifität ab. Die strukturierte Verifikation verbessert Konsistenz und reduziert Falschpositive, gibt aber Flexibilität für natürlichsprachliche Zitierungen auf, was in kritischen Bereichen wie rechtlicher KI zu einem Kompromiss zwischen Anpassungsfähigkeit und Zuverlässigkeit führt. Dieser Ansatz eliminiert die Abhängigkeit von LLM-as-a-Judge, indem die Validierung direkt auf externem Beweis basiert, um Zitierhalluzinationen direkt zu adressieren.

#### 5. Grundierungshalluzinationssicherung

Die Sicherung von Grundierungshalluzinationen stellt sicher, dass Aussagen in generierten Antworten durch den abgerufenen Kontext unterstützt werden, was sich von Zitierhalluzinationen (wo Quellen erfunden werden) unterscheidet. Dieser Schritt verwendet eine Aussage für Aussage Grundierung: die Aufteilung der Antwort in atomare Aussagen und die Validierung jeder Aussage gegen Kontextpassagen. Natürliche Sprachinferenz (NLI)-Modelle berechnen Schlussfolgerungsscores zwischen einer Aussage `c` und einer Kontextpassage `p`, wodurch `score = NLI(c, p)` (Schlussfolgerung, Widerspruch oder neutral) ausgegeben wird. Eingaben umfassen die Aussagemenge und Kontextpassagen; Ausgaben sind pro-Aussage-Validierungsergebnisse (grundiert, wenn der maximale Schlussfolgerungsscore den Schwellenwert überschreitet). Der Algorithmus aggregiert den höchsten Schlussfolgerungsscore über die Passagen für jede Aussage. Gestaltungswahl priorisiert Effizienz durch NLI (Vermeidung von LLM-as-a-Judge), aber es gibt Kompromisse: Kontextverschmutzung (irrelevante Passagen) kann die Scores senken, während hohe Recall-Falschpositive erhöhen. Dieser Ansatz wird mit [[rag-generation-evaluation|Generierungsbewertung]] integriert, um die Qualität der Grundierung systematisch zu bewerten, überflüssige Zitierprüfung hinaus, und adressiert die Einschränkungen, die in RAG-Systemen festgestellt wurden, wo LLMs falsche Unterstützung sogar mit gültigen Quellen zuweisen können (Barnett et al. 2024).

#### 6. Interpretationsfehleranalyse

Die Interpretationsfehleranalyse verwendet die LLM-as-a-Judge-Bewertung, bei der ein sekundäres LLM generierte Aussagen gegen den abgerufenen Kontext bewertet. Eingaben umfassen den Antworttext und die Quellkontexte; Ausgaben sind binäre Richtigkeitslabels (z. B. `correct = 1`) oder Konfidenzwerte, die aus promptbasierten Validierungen abgeleitet werden. Dieser Ansatz nutzt die Schlussfolgerungsfähigkeiten des LLMs, erbt aber seine Einschränkungen, wie Gao et al. (2023) gezeigt haben, dass führende Modelle in ALCE-Benchmark-Tests 50 % der Zeit keine vollständige Zitierunterstützung haben. Die menschliche Validierung im Loop verwendet Fachexperten, um Ausgaben zu überprüfen, was für komplexe Fälle wie rechtliche Grundierungshalluzinationen eine höhere Genauigkeit bietet, aber erhebliche Kosten und Latenz verursacht. Die Gestaltungskompromisse konzentrieren sich auf Skalierbarkeit versus Präzision: LLM-as-a-Judge ermöglicht kontinuierliche, automatisierte Bewertung, während menschliche Validierung für kritische Anwendungen mit hoher Zuverlässigkeit reserviert ist, wie in Protokollen zur Grundierungshalluzinationserkennung [[rag-generation-evaluation|RAG: Generierungsbewertung]] betont wird.

#### Ursprung und Varianten

Barnett et al. (2024) haben durch Fallstudien in Forschung, Bildung und biomedizinischen RAG-Bereitstellungen ein 7-Punkte-Fehlerframework etabliert, bei dem die Transformation von Eingabeabfragen und Wissensbasen in generierte Ausgaben analysiert wird. Das Framework kategorisiert Fehler nach Pipeline-Stufen (Retrieval, Ranking, Kontextkonstruktion, Generierung), wobei Schlüssel-Fehlerpunkte die Retrieval-Miss-Verfehlungen, Ranking-Unsicherheiten und Kontextverschmutzung umfassen. Eine zentrale Erkenntnis ist, dass Robustheit durch operatives Validierung statt durch ursprüngliches Design entsteht, was kontinuierliche Überwachung der realen Nutzung erfordert. Dieser Ansatz priorisiert iteratives Feinabstimmung über statische Vorab-Testung, wodurch Entwicklungseffizienz gegen Anpassungsfähigkeit getauscht wird. Zum Beispiel entsteht Kontextverschmutzung oft aus suboptimalen Top-k-Retrieval-Schwellenwerten (wie in [[rag-retrieval|Retrieval]], wobei übermäßige Kontexteinschließung Rauschen einführt, das die Generierungsgüte verringert. Die Gestaltungswahl des Frameworks erkennt an, dass Fehlermodi kontextabhängig sind und während der Operation auftreten, wodurch Robustheit eine dynamische Eigenschaft statt eine feste Systemeigenschaft ist. Daher muss die Validierung in Produktionsumgebungen statt während der Entwicklung stattfinden.

### Wann einsetzen

- Hochrisko-Bereiche (z. B. biomedizinisch, rechtlich) erfordern die Diagnose von Ausfallmodi, um Halluzinationen und kritische Fehlfunktionen zu beheben (Barnett et al. (2024)).
- Die operativen Bereitstellung erfordert eine kontinuierliche Diagnose von Ausfallmodi, da die Validierung nur während der realen Systembetriebs durchgeführt werden kann (Barnett et al. (2024)).
- Die Diagnose von Kontextverschmutzung erfordert die Isolierung von [[rag-retrieval|retrieval]]- oder Rangierungsfehlern, insbesondere wenn irrelevante Dokumente die Ausgabegüte beeinträchtigen (Cuconasu et al. (2024)).
- Anwendungen mit langen Kontexten erfordern die Diagnose von Ausfallmodi, um Rangierungsfehler im Retrieval zu identifizieren, die bei der Leistungsschwächung auftreten, wenn relevante Informationen nicht an Kontextgrenzen positioniert sind (Liu et al. (2023)).

### Stärken und Grenzen

**Stärken**
- Ermöglicht die präzise Lokalisierung von Fehlern auf spezifische RAG-Pipeline-Stufen (retrieval, ranking, context, generation), vermeidet falsche Zuordnungen aufgrund von LLM-Halluzinationen allein (Barnett et al. (2024)).
- Erfasst empirische Beweise, dass nicht relevante, hoch bewertete Dokumente die LLM-Performance beeinträchtigen (Cuconasu et al. (2024)), ermöglicht gezielte Korrekturen bei der Kontextzusammensetzung.
- Fördert die operativen Validierungen durch Übereinstimmung mit der Erkenntnis, dass die RAG-Robustheit während der Bereitstellung und nicht während des Designs entwickelt wird (Barnett et al. (2024)).

**Einschränkungen**
- Berücksichtigt nicht widersprüchliche Erkenntnisse wie die Verbesserung der LLM-Genauigkeit um bis zu 35 % durch die Addition zufälliger Dokumente (Cuconasu et al. (2024)), was Lücken in der Abdeckung von Fehlern zeigt.
- Behandelt die Pipeline-Stufen als unabhängig, obwohl Fehler sich kaskadieren (z. B. Retrieval-Fehler führen durch zu großes top-k zur Kontamination des Kontexts).
- Fehlt die Integration quantitativer Fehlermetriken (z. B. 50 % Fehlerrate bei der Zitatabdeckung auf ELI5, Gao et al. (2023)), was ergänzende Bewertungsrahmen erfordert.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| RAG-Fehlermodus-Framework | Kategorisiert Fehler explizit nach Pipeline-Stufen (Retrieval, Ranking, Kontextkonstruktion, Generierung), während die Analyse von LLM-Halluzinationen (z. B. Gao et al. (2023)) alle Fehler der Generierung zuschreibt, ohne den Pipeline-Kontext zu berücksichtigen, und die retrievalzentrierte Analyse (z. B. Liu et al. (2023)) sich nur auf Retrieval und Kontextposition konzentriert, ohne die Kontextkonstruktion oder Generierungsfehler zu berücksichtigen. | Systematische Ursachenanalyse zur Verbesserung der RAG-Robustheit, da Fehler oft upstream entstehen (Barnett et al. (2024)). |
| LLM-Halluzination-Analyse | Zuschreibt alle Fehler Halluzinationen der LLM-Generierung, ignoriert dabei Fehler in der upstream-Pipeline (z. B. fand Gao et al. (2023) heraus, dass 50 % der Antworten keine Zitierunterstützung haben, diagnostizierte aber keine Retrieval-Fehler). | Beurteilt die Generierung auf Halluzinationen (z. B. [[rag-generation-evaluation|Generierungsbewertung]], identifiziert aber keine Ursachen upstream. |
| Retrievalzentrierte Fehleranalyse | Konzentriert sich ausschließlich auf Retrieval- und Rankingleistung (z. B. zeigte Liu et al. (2023) nach, dass LLMs sich verschlechtern, wenn relevante Informationen in der Mitte des Kontexts stehen), ignoriert dabei Fehler in der Kontextkonstruktion und Generierung. | Optimiert Retrieval (z. B. [[rag-retrieval|Retrievalbewertung]], übersehen aber Fehler in der Kontextkomposition oder Generierung. |
Dieses Framework ermöglicht eine präzise Fehlerlokalisierung entlang der Pipeline, was entscheidend ist, um zwischen Retrieval-Fehlern (z. B. fehlende Dokumente) und Generierungsfehlern (z. B. Zitierhalluzinationen) zu unterscheiden und somit Fehldiagnosen der Ursachen zu vermeiden.

### In der Praxis

Die Evaluation muss [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]] und [[rag-generation-evaluation|RAG: Generation Evaluation]]-Metriken verwenden. Gao et al. (2023) berichteten, dass selbst state-of-the-art-Modelle nur zu 50 % der Zeit vollständige Zitierunterstützung auf ELI5 besitzen. Die Position des Kontexts beeinflusst die Leistung entscheidend: Liu et al. (2023) beobachteten einen erheblichen Rückgang der Genauigkeit, wenn relevante Informationen in der Mitte langer Kontexte auftreten, während Positionen am Anfang oder Ende bessere Ergebnisse liefern. Parameterauswahlen sollten die Kontextrelevanz priorisieren: Cuconasu et al. (2024) fanden heraus, dass Dokumente mit der höchsten Bewertung, die nicht relevant sind, die Leistung von LLM negativ beeinflussen, obwohl das Hinzufügen zufälliger Dokumente die Genauigkeit um bis zu 35 % verbessert, was darauf hindeutet, dass das Kontextfiltern irrelevanten Inhalt ausschließen muss, während mögliche Vorteile aus irrelevantem Kontext berücksichtigt werden sollten. Top-k-Werte sollten über Retrieval-Evaluation optimiert werden, um Recall und Relevanz zu balancieren und Kontextverschmutzung zu vermeiden.

### Merksatz

RAG-Systeme reduzieren Halluzinationen, indem sie Antworten in abgerufenen Dokumenten verankern, erfordern aber eine systematische Diagnose von Fehlern im gesamten Pipeline-Prozess (Abfrage, Rangfolge, Kontexterstellung, Generierung), um Ursachen zu identifizieren.

### Quellen

- Barnett, S. et al. (2024). *Seven Failure Points When Engineering a Retrieval Augmented Generation System.* [arXiv:2401.05856](https://arxiv.org/abs/2401.05856)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Cuconasu, F. et al. (2024). *The Power of Noise: Redefining Retrieval for RAG Systems.* [arXiv:2401.14887](https://arxiv.org/abs/2401.14887)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
