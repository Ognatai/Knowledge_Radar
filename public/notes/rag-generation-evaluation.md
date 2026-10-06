---
title_en: 'RAG: Generation Evaluation'
title_de: 'RAG: Evaluation der Generierung'
entity_type: Method
sources:
- https://arxiv.org/abs/2309.15217
- https://arxiv.org/abs/2305.14251
- https://arxiv.org/abs/2305.14627
- https://arxiv.org/abs/2306.05685
- https://arxiv.org/abs/2311.09476
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RAG generation evaluation assesses the faithfulness, correctness, and completeness of LLM responses relative to retrieved context without requiring human annotations. It solves the problem of slow and costly human evaluation by enabling automated reference-free assessment through frameworks like Ragas (Es et al. (2023)) and FACTSCORE (Min et al. (2023)).

### How it works

RAG generation evaluation assesses response faithfulness, correctness, and completeness by decomposing outputs into atomic claims, validating each claim against retrieved context, verifying citation correctness, scoring via [[llm-as-a-judge|LLM-as-a-Judge]], and computing the hallucination rate as `hallucination_rate = (unsupported_claims) / (total_claims)`. This automated reference-free framework, pioneered by Ragas (Es et al. (2023)) and FACTSCORE (Min et al. (2023)), eliminates human annotation requirements while supporting domain-specific validation through [[rag-evaluation|RAG Evaluation]].

```text
Decomposing responses into atomic claims ─▶
Context-based claim validation ─▶
Citation correctness verification ─▶
LLM-as-a-Judge scoring ─▶
Hallucination rate calculation
```

#### 1. Decomposing responses into atomic claims

FACTSCORE decomposes a generated response into atomic claims by segmenting the text into independent factual assertions, typically as simple declarative statements or subject-predicate-object triples. This segmentation is performed algorithmically using a rule-based extractor that splits the response into sentences and isolates core claims, ignoring conjunctions and contextual modifiers. Each claim is then evaluated for support against a reliable knowledge source (e.g., retrieved context or a knowledge base) via retrieval and natural language inference (NLI). The primary metric is the support ratio: `support_ratio = (number of supported claims) / (total claims)`. This decomposition enables granular evaluation of factuality, capturing partial support (e.g., 80% of claims supported) and avoiding limitations of binary judgments. Min et al. (2023) demonstrate this method achieves high correlation with human evaluation (less than 2% error rate in automated estimation). A key trade-off is that complex assertions may fragment into oversimplified claims, potentially misrepresenting nuanced statements, though this is offset by the scalability of reference-free assessment. The approach requires only the generation and a knowledge source, eliminating human annotation costs while providing actionable insights into factual accuracy.

#### 2. Context-based claim validation

Context-based claim validation decomposes the generated response into atomic claims and verifies each against provided context passages to assess groundedness. Inputs include the response string and context passages; outputs are claim-level support assessments (e.g., supported/not supported) or a faithfulness score. The algorithm typically employs a model-based approach where a lightweight language model judge [[llm-as-a-judge|LLM-as-a-Judge]] evaluates claim-context alignment via a prompt like "Does the context support the claim? [claim] [context]". Saad-Falcon et al. (2023) demonstrate this using fine-tuned judges trained on synthetic data to minimize human annotation needs. Design choices involve trade-offs between rule-based checks (computationally efficient but semantically shallow) and model-based methods (more accurate for nuanced context claims but requiring model training and introducing potential bias). The model-based approach captures semantic relationships critical for groundedness but increases computational overhead and risks model-specific scoring inconsistencies compared to simpler rule-based alternatives.

#### 3. Citation correctness verification

Citation correctness verification ensures generated citations are valid and contextually supported. Inputs include the LLM response with citations, retrieved context passages, and the original query. The process checks four aspects: (1) source existence (cited source exists in a knowledge base), (2) context inclusion (source was present in retrieved passages), (3) semantic support (context semantically validates the claim), and (4) precision (citation points to exact relevant source segment). Deterministic checks (existence and context inclusion) use string matching against retrieved passages; semantic support employs a natural language inference model or [[llm-as-a-judge|LLM-as-a-Judge]]; precision requires anchor matching (e.g., paragraph numbers). Outputs are per-citation verification results (valid/invalid) and a composite metric. Design choices prioritize deterministic checks for efficiency (low latency, no model cost), deferring semantic support to a model to balance accuracy and resource use. This trades off potential false negatives in semantic checks for scalability. Gao et al. (2023) quantified the challenge, reporting that top models lack complete citation support 50% of the time on the ELI5 dataset, underscoring the need for rigorous verification.

#### 4. LLM-as-a-Judge scoring

LLM-as-a-Judge scoring employs lightweight language models to automate semantic evaluation of RAG generations. Inputs consist of a query, retrieved context, and generated answer; outputs are scalar scores for correctness (factual accuracy), faithfulness (contextual grounding), and completeness (coverage of query requirements). The algorithm typically involves training a lightweight judge model on synthetic data generated via the RAG pipeline, followed by prediction-powered inference (PPI) using a small human-annotated validation set (e.g., hundreds of examples) to correct errors, as implemented in ARES (Saad-Falcon et al. (2023)). This design minimizes human annotation needs while maintaining cross-domain robustness. Key trade-offs include reduced computational cost and latency versus potential accuracy loss compared to strong LLM judges. Zheng et al. (2023) demonstrate that strong LLM judges achieve over 80% agreement with human preferences, justifying the lightweight approach for scalable reference-free evaluation. This method enables continuous integration testing without human annotation overhead, though it requires careful prompt engineering to avoid biases.

#### 5. Hallucination rate calculation

Hallucination rate is defined as the ratio of unsupported claims to the total claims examined, computed as `hallucination_rate = unsupported_claims / total_claims`. Unsupported claims are assertions in the generated response not verifiable from the provided context. Three hallucination types are distinguished: (1) citation hallucination, where a claim references a non-existent or misattributed source; (2) grounding hallucination, where a claim lacks contextual support despite an existing source; and (3) unsupported claim, the general category of claims without contextual evidence. Inputs are the generated response and retrieved context. The algorithm processes the response by splitting it into atomic claims (e.g., via fact extraction as in FACTSCORE (Min et al. (2023))), then checks each claim against the context using semantic matching (e.g., LLM-based verification via natural language inference). Design choices prioritize robustness against paraphrasing (semantic matching) over speed (string matching), accepting higher computational cost to reduce false negatives. This trade-off is justified for accurate hallucination detection, as demonstrated in reference-free evaluation frameworks [[rag-evaluation|reference-free evaluation]], which avoid human annotation through automated claim verification as implemented in Ragas (Es et al. (2023)) and FACTSCORE (Min et al. (2023)).

#### Origin and variants

Ragas (Es et al. 2023) computes faithfulness by decomposing the generated answer into claims and verifying each against the retrieved context using LLM-based natural language inference. FACTSCORE (Min et al. 2023) breaks responses into atomic facts and scores support percentage via retrieval against a knowledge source, using an automated model with <2% error. ALCE (Gao et al. 2023) evaluates citation correctness through end-to-end system outputs, measuring fluency, correctness, and citation quality against a curated benchmark. ARES (Saad-Falcon et al. 2023) finetunes lightweight LM judges on synthetic data and applies prediction-powered inference (PPI) with a small human-annotated set (hundreds of examples), reducing annotation needs while maintaining accuracy across domain shifts. All frameworks avoid full human evaluation but trade off against LLM bias (Ragas, ARES) or knowledge source dependency (FACTSCORE, ALCE), with ARES demonstrating robustness on diverse tasks [[rag-evaluation|reference-free evaluation]] and FACTSCORE enabling fine-grained fact verification [[llm-as-a-judge|LLM-as-a-Judge]].

### When to use it

- When avoiding human annotation for faithfulness assessment (Es et al. (2023)).
- When scaling completeness evaluation across large datasets (Gao et al. (2023)).
- When using automated factuality evaluation to avoid human annotation costs (Min et al. (2023)).
- When requiring verified context to isolate generation quality (Saad-Falcon et al. (2023)).

### Strengths and limitations

**Strengths**
- Enables reference-free generation evaluation without human annotations, reducing evaluation cost and time (Es et al. 2023; [[rag-evaluation|Evaluation]]).
- Achieves high accuracy (e.g., <2% error rate) and scales to large-scale generation sets (e.g., 6,500 generations) (Min et al. 2023).
- Requires only a few hundred human annotations for cross-domain validation across retrieval-augmented tasks (Saad-Falcon et al. 2023).

**Limitations**
- Does not fully replace human evaluation for fine-grained factuality assessment (e.g., ChatGPT factuality score of 58% on biographies (Min et al. 2023)).
- Current systems exhibit significant gaps in citation support (e.g., 50% lack of complete citations on ELI5 dataset (Gao et al. 2023)).
- LLM-as-a-judge approaches used in evaluation may introduce position, verbosity, and reasoning biases (Zheng et al. 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Reference-free suite of metrics for RAG-specific dimensions (faithfulness, answer relevance) evaluated on a controlled context. | Automated, large-scale RAG system development and testing without human annotations. |
| FACTSCORE (Min et al. 2023) | Evaluates factuality by decomposing into atomic facts and checking against a knowledge source; not RAG-specific. | General factuality assessment of LLM generations, including RAG outputs, when knowledge source access is available. |
| ARES (Saad-Falcon et al. 2023) | Uses synthetic data and fine-tuned LM judges with minimal human annotations (few hundred) for prediction-powered inference. | RAG evaluation in contexts with limited human annotation resources, robust across domain shifts. |

Ragas differs from [[llm-as-a-judge|LLM-as-a-Judge]] by providing RAG-specific metrics rather than general response evaluation, while FACTSCORE focuses on atomic fact verification without RAG pipeline context. ARES requires minimal human calibration but targets broader RAG component assessment.

### In practice

For evaluation, FACTSCORE computes factuality as the percentage of atomic facts supported by a reliable knowledge source (e.g., 58% for ChatGPT on biographies, Min et al. (2023)), while Ragas uses LLM-as-a-judge for faithfulness assessment (Es et al. (2023)). Typical failure modes include unsupported claims (42% of atomic facts in ChatGPT, Min et al. (2023)) and incomplete citation support (50% lack of complete citation support in top models, Gao et al. (2023)), documented in [[rag-failure-modes|failure modes]]. Parameter choices include using a few hundred human annotations for prediction-powered inference in ARES (Saad-Falcon et al. (2023)) and leveraging [[llm-as-a-judge|LLM-as-a-judge]] for automated evaluation with less than 2% error rate (Min et al. (2023)).

### Key takeaway

RAG generation evaluation enables scalable reference-free assessment of faithfulness, correctness, and completeness through [[llm-as-a-judge|LLM-as-a-Judge]] frameworks, but its domain-specific accuracy necessitates human validation.

### Sources

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.* [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

RAG-Generierungsbewertung bewertet die Glaubwürdigkeit, Richtigkeit und Vollständigkeit der LLM-Antworten im Vergleich zum abgerufenen Kontext, ohne menschliche Annotationen zu benötigen. Sie löst das Problem der langsamen und kostspieligen menschlichen Bewertung, indem sie eine automatisierte, referenzfreie Bewertung durch Frameworks wie Ragas (Es et al. (2023)) und FACTSCORE (Min et al. (2023)) ermöglicht.

### Funktionsweise

RAG-Generierungsbewertung bewertet die Antworttreue, Richtigkeit und Vollständigkeit, indem sie die Ausgaben in atomare Aussagen zerlegt, jede Aussage anhand des abgerufenen Kontexts validiert, die Zitatabschnitte auf Richtigkeit überprüft, mittels [[llm-as-a-judge|LLM-as-a-Judge]] bewertet und die Halluzinationsrate berechnet als `hallucination_rate = (unsupported_claims) / (total_claims)`. Dieses automatisierte, referenzfreie Framework, das von Ragas (Es et al. (2023)) und FACTSCORE (Min et al. (2023)) entwickelt wurde, eliminiert die Notwendigkeit menschlicher Annotationen, während es durch [[rag-evaluation|RAG Evaluation]] die Validierung für domänenspezifische Anwendungen ermöglicht.

```text
Antworten in atomare Aussagen zerlegen ─▶
Aussagen anhand des Kontexts validieren ─▶
Zitatabschnitte auf Richtigkeit überprüfen ─▶
LLM-as-a-Judge bewerten ─▶
Halluzinationsrate berechnen
```

#### 1. Antwort in atomare Aussagen zerlegen

FACTSCORE zerlegt eine generierte Antwort in atomare Aussagen, indem der Text in unabhängige fakтиsche Aussagen unterteilt wird, typischerweise als einfache deklarative Aussagen oder Subjekt-Prädikat-Objekt-Tripel. Diese Unterteilung erfolgt algorithmisch mithilfe eines regelbasierten Extractors, der die Antwort in Sätze unterteilt und die Kernaussagen isoliert, wobei Konjunktionen und kontextuelle Modifikatoren ignoriert werden. Jede Aussage wird anschließend anhand einer zuverlässigen Wissensquelle (z. B. abgerufener Kontext oder Wissensbank) mittels Retrieval und natürlicher Sprachinference (NLI) auf Unterstützung geprüft. Der primäre Metrik ist der Unterstützungssatz: `support_ratio = (number of supported claims) / (total claims)`. Diese Zerlegung ermöglicht eine feingranulare Bewertung der Faktenhaltigkeit, wodurch partielle Unterstützung (z. B. 80 % der Aussagen unterstützt) erfasst wird und die Einschränkungen binärer Urteile vermieden werden. Min et al. (2023) zeigen, dass dieser Ansatz eine hohe Korrelation mit menschlicher Bewertung erreicht (weniger als 2 % Fehlerquote bei automatischer Schätzung). Ein wichtiger Kompromiss besteht darin, dass komplexe Aussagen in übervereinfachte Aussagen zerlegt werden können, was potenziell nuanceureiche Aussagen falsch darstellen könnte, wobei dies durch die Skalierbarkeit der referenzfreien Bewertung ausgeglichen wird. Der Ansatz benötigt nur die Generierung und eine Wissensquelle, wodurch menschliche Annotationen vermieden werden, während er gleichzeitig wertvolle Erkenntnisse über die fakтиsche Genauigkeit liefert.

#### 2. Kontextbasierte Aussagenvalidierung

Die kontextbasierte Aussagenvalidierung zerlegt die generierte Antwort in atomare Aussagen und überprüft jede Aussage anhand der bereitgestellten Kontextpassagen, um die Grundlage zu bewerten. Die Eingaben umfassen die Antwortzeichenfolge und die Kontextpassagen; die Ausgaben sind Aussagenbezogene Unterstützungsbewertungen (z. B. unterstützt/nicht unterstützt) oder eine Treuebewertung. Der Algorithmus verwendet typischerweise einen modellbasierten Ansatz, bei dem ein leichtgewichtiges Sprachmodell [[llm-as-a-judge|LLM-as-a-Judge]] die Übereinstimmung zwischen Aussage und Kontext anhand eines Prompts wie „Unterstützt der Kontext die Aussage? [Aussage] [Kontext]“ bewertet. Saad-Falcon et al. (2023) zeigen dies mithilfe von feinabgestimmten Richtern, die auf synthetischen Daten trainiert wurden, um die Notwendigkeit menschlicher Annotationen zu minimieren. Die Gestaltungswahl beinhaltet Kompromisse zwischen regelbasierten Prüfungen (rechenintensiv, aber semantisch flach) und modellbasierten Methoden (genauer für nuanceureiche Kontextaussagen, aber Modelltraining erforderlich und potenzielle Verzerrungen einführend). Der modellbasierte Ansatz erfasst semantische Beziehungen, die für die Grundlage entscheidend sind, erhöht aber die rechnerische Überlastung und birgt Risiken für modellabhängige Bewertungsinkonstanz im Vergleich zu einfacheren regelbasierten Alternativen.

#### 3. Zitatabschnitte auf Richtigkeit überprüfen

Die Überprüfung der Zitatabschnitte auf Richtigkeit stellt sicher, dass generierte Zitierungen gültig und kontextuell unterstützt sind. Die Eingaben umfassen die LLM-Antwort mit Zitierungen, abgerufene Kontextpassagen und die ursprüngliche Anfrage. Der Prozess prüft vier Aspekte: (1) Quellbestand (die zitierte Quelle existiert in einer Wissensbank), (2) Kontexteinbindung (die Quelle war in den abgerufenen Passagen vorhanden), (3) semantische Unterstützung (der Kontext validiert die Aussage semantisch) und (4) Präzision (das Zitieren verweist auf den exakt relevanten Quellabschnitt). Deterministische Prüfungen (Bestand und Kontexteinbindung) verwenden Zeichenkettenvergleiche mit den abgerufenen Passagen; die semantische Unterstützung verwendet ein natürliche Sprachinference-Modell oder [[llm-as-a-judge|LLM-as-a-Judge]]; Präzision erfordert Anchormatching (z. B. Absatznummern). Die Ausgaben sind Ergebnisse der Zitierüberprüfung pro Zitierung (gültig/ungültig) und eine Gesamtmetrik. Gestaltungswahl priorisiert deterministische Prüfungen für Effizienz (niedrige Latenz, kein Modellkosten), wobei die semantische Unterstützung einem Modell überlassen wird, um Genauigkeit und Ressourcennutzung auszugleichen. Dieser Kompromiss birgt das Risiko von Fehlern in der semantischen Prüfung, um Skalierbarkeit zu ermöglichen. Gao et al. (2023) haben die Herausforderung quantifiziert, indem sie berichteten, dass die besten Modelle in 50 % der Fälle auf dem ELI5-Datensatz keine vollständige Zitierunterstützung besitzen, was die Notwendigkeit einer strengen Überprüfung unterstreicht.

#### 4. LLM-as-a-Judge-Bewertung

Die LLM-as-a-Judge-Bewertung verwendet leichte Sprachmodelle, um die semantische Bewertung von RAG-Generierungen zu automatisieren. Die Eingaben bestehen aus einer Anfrage, abgerufenem Kontext und der generierten Antwort; die Ausgaben sind Skalierungswerte für Richtigkeit (fakтиsche Genauigkeit), Treue (kontextuelle Grundlage) und Vollständigkeit (Abdeckung der Anforderungen der Anfrage). Der Algorithmus besteht typischerweise aus dem Training eines leichten Richtermodells auf synthetischen Daten, die über den RAG-Pipeline generiert wurden, gefolgt von Prädiktion-powered Inference (PPI) mithilfe einer kleinen, von Menschen annotierten Validierungsstichprobe (z. B. einige hundert Beispiele), um Fehler zu korrigieren, wie in ARES (Saad-Falcon et al. (2023)) implementiert. Dieses Design minimiert die Notwendigkeit menschlicher Annotationen, während es die robustheit über verschiedene Domänen hinweg beibehält. Wichtige Kompromisse bestehen in der Reduzierung der Rechenkosten und Latenz gegenüber potenziellen Genauigkeitsverlusten im Vergleich zu starken LLM-Richtern. Zheng et al. (2023) zeigen, dass starke LLM-Richter über 80 % Übereinstimmung mit menschlichen Präferenzen erreichen, was den leichten Ansatz für skalierbare referenzfreie Bewertung rechtfertigt. Dieser Ansatz ermöglicht kontinuierliche Integrationstests ohne menschliche Annotationsoverhead, erfordert jedoch sorgfältige Prompt-Engineering, um Verzerrungen zu vermeiden.

#### 5. Halluzinationsrate berechnen

Die Halluzinationsrate wird als Verhältnis der nicht unterstützten Aussagen zur Gesamtzahl der untersuchten Aussagen definiert und berechnet als `hallucination_rate = unsupported_claims / total_claims`. Nicht unterstützte Aussagen sind Aussagen in der generierten Antwort, die nicht aus dem bereitgestellten Kontext verifiziert werden können. Drei Halluzinationstypen werden unterschieden: (1) Zitierhalluzination, bei der eine Aussage eine nicht existierende oder falsch zugeordnete Quelle verweist; (2) Grundlagenhalluzination, bei der eine Aussage keine kontextuelle Unterstützung hat, obwohl eine Quelle vorhanden ist; und (3) nicht unterstützte Aussage, die allgemeine Kategorie von Aussagen ohne kontextuelle Beweise. Die Eingaben sind die generierte Antwort und der abgerufene Kontext. Der Algorithmus verarbeitet die Antwort, indem sie in atomare Aussagen unterteilt wird (z. B. über Faktenextraktion wie in FACTSCORE (Min et al. (2023))), und prüft jede Aussage anschließend anhand des Kontexts mit semantischem Matching (z. B. LLM-basierte Verifikation über natürliche Sprachinference). Gestaltungswahl priorisiert Robustheit gegenüber Paraphrasierung (semantisches Matching) gegenüber Geschwindigkeit (Zeichenkettenmatching), wobei ein höherer Rechenaufwand akzeptiert wird, um Falschnegative zu reduzieren. Dieser Kompromiss wird in referenzfreien Bewertungsframeworks [[rag-evaluation|referenzfreie Bewertung]] gerechtfertigt, die menschliche Annotationen durch automatisierte Aussagenverifikation vermeiden, wie in Ragas (Es et al. (2023)) und FACTSCORE (Min et al. (2023)) implementiert.

#### Ursprung und Varianten

Ragas (Es et al. 2023) berechnet Treue, indem die generierte Antwort in Aussagen zerlegt und jede Aussage anhand des abgerufenen Kontexts mithilfe LLM-basierter natürlicher Sprachinference validiert wird. FACTSCORE (Min et al. 2023) zerlegt Antworten in atomare Fakten und bewertet den Unterstützungssatzprozentual über Retrieval gegen eine Wissensquelle, wobei ein automatisiertes Modell mit <2 % Fehlerquote verwendet wird. ALCE (Gao et al. 2023) bewertet die Zitiergenauigkeit durch End-to-End-Systemausgaben, indem Flußigkeit, Richtigkeit und Zitierqualität anhand eines kurierten Benchmarks gemessen werden. ARES (Saad-Falcon et al. 2023) feinabstimmte leichte LM-Richter auf synthetischen Daten und wendet Prädiktion-powered Inference (PPI) mit einer kleinen, von Menschen annotierten Stichprobe (hunderte Beispiele) an, um die Notwendigkeit von Annotationen zu reduzieren, während Genauigkeit über Domain-Shifts beibehalten wird. Alle Frameworks vermeiden vollständige menschliche Bewertung, geben jedoch Kompromisse gegenüber LLM-Bias (Ragas, ARES) oder Abhängigkeit von Wissensquellen (FACTSCORE, ALCE) ab, wobei ARES Robustheit auf verschiedenen Aufgaben [[rag-evaluation|referenzfreie Bewertung]] und FACTSCORE feingranulare Faktenverifikation [[llm-as-a-judge|LLM-as-a-Judge]] demonstriert.

### Wann einsetzen

- Wenn die menschliche Annotation zur Bewertung der Glaubwürdigkeit vermieden wird (Es et al. (2023)).
- Wenn die Vollständigkeitsevaluation über große Datensätze skaliert wird (Gao et al. (2023)).
- Wenn eine automatisierte Faktenbewertung genutzt wird, um Kosten für menschliche Annotationen zu vermeiden (Min et al. (2023)).
- Wenn verifizierter Kontext benötigt wird, um die Qualität der Generierung zu isolieren (Saad-Falcon et al. (2023)).

### Stärken und Grenzen

**Vorteile**
- Ermöglicht die generationsbasierte Bewertung ohne Referenzen und ohne menschliche Annotationen, wodurch Kosten und Zeit für die Bewertung reduziert werden (Es et al. 2023; [[rag-evaluation|Bewertung]]).
- Erreicht eine hohe Genauigkeit (z. B. <2 % Fehlerrate) und skaliert auf große Generationsmengen (z. B. 6.500 Generierungen) (Min et al. 2023).
- Erfordert nur einige hundert menschliche Annotationen für die Überprüfung über verschiedene Retrieval-verstärkte Aufgaben hinweg (Saad-Falcon et al. 2023).

**Einschränkungen**
- Ersetzt die menschliche Bewertung nicht vollständig bei der feinkörnigen Faktualitätsbewertung (z. B. ChatGPT-Faktualitätsscore von 58 % bei Biografien (Min et al. 2023)).
- Die aktuellen Systeme weisen erhebliche Lücken bei der Unterstützung von Zitaten auf (z. B. 50 % fehlender vollständiger Zitierungen im ELI5-Datensatz (Gao et al. 2023)).
- Die in der Bewertung verwendeten LLM-as-a-judge-Methoden können Position, Umfang und Schlussfolgerungsbiases einführen (Zheng et al. 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Referenzfreie Metrikensuite für RAG-spezifische Dimensionen (Faithfulness, Antwortrelevanz), bewertet auf einem kontrollierten Kontext. | Automatisierte, großskalige RAG-Systementwicklung und -testung ohne menschliche Annotationen. |
| FACTSCORE (Min et al. 2023) | Bewertet Factualität durch Zerlegung in atomare Fakten und Überprüfung gegen eine Wissensquelle; nicht RAG-spezifisch. | Allgemeine Factualitätsbewertung von LLM-Generierungen, einschließlich RAG-Ausgaben, wenn Zugriff auf eine Wissensquelle besteht. |
| ARES (Saad-Falcon et al. 2023) | Verwendet synthetische Daten und feinabgestimmte LM-Beurteiler mit minimalen menschlichen Annotationen (hunderte) für prädiktionsgestützte Inferenz. | RAG-Bewertung in Kontexten mit begrenzten Ressourcen für menschliche Annotationen, robust gegenüber Domänenschifts. |

Ragas unterscheidet sich von [[llm-as-a-judge|LLM-as-a-Judge]], indem es RAG-spezifische Metriken anstelle allgemeiner Antwortbewertungen bereitstellt, während FACTSCORE sich auf die Verifikation von atomaren Fakten ohne Kontext des RAG-Pipelines konzentriert. ARES benötigt minimale menschliche Kalibrierung, zielt jedoch auf eine umfassendere Bewertung von RAG-Komponenten ab.

### In der Praxis

Für die Bewertung berechnet FACTSCORE die Factualität als Prozentsatz der atomaren Fakten, die von einer zuverlässigen Wissensquelle unterstützt werden (z. B. 58 % bei ChatGPT bei Biografien, Min et al. (2023)), während Ragas die Faithfulness mit LLM-as-a-judge bewertet (Es et al. (2023)). Typische Fehlmodi umfassen nicht unterstützte Aussagen (42 % der atomaren Fakten bei ChatGPT, Min et al. (2023)) und unvollständige Zitierunterstützung (50 % fehlender vollständiger Zitierunterstützung bei den besten Modellen, Gao et al. (2023)), wie in [[rag-failure-modes|Fehlmodi]] dokumentiert. Parameterauswahl umfasst die Verwendung einiger hundert menschlicher Annotationen für die prädiktionsgestützte Inferenz in ARES (Saad-Falcon et al. (2023)) und die Nutzung von [[llm-as-a-judge|LLM-as-a-judge]] für die automatisierte Bewertung mit weniger als 2 % Fehlerrate (Min et al. (2023)).

### Merksatz

RAG-Generierungsbewertung ermöglicht eine skalierbare, referenzfreie Bewertung von Zuverlässigkeit, Richtigkeit und Vollständigkeit durch [[llm-as-a-judge|LLM-as-a-Judge]]-Frameworks, aber ihre domain-spezifische Genauigkeit erfordert menschliche Validierung.

### Quellen

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.* [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)
