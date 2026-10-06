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

RAG generation evaluation assesses response faithfulness, correctness, and completeness by decomposing outputs into atomic claims, validating each claim against retrieved context, verifying citation correctness, scoring via [[llm-as-a-judge|LLM-as-a-Judge]], and computing the hallucination rate as `hallucination_rate = (unsupported_claims) / (total_claims)`. Claim-level checking underlies both FActScore (Min et al., 2023), which scores the share of supported atomic facts, and the faithfulness metric of Ragas (Es et al., 2023); automated versions of these checks reduce the need for human annotation but do not remove it entirely. Generation evaluation is one half of [[rag-evaluation|RAG evaluation]].

```text
question + context + generated answer
 ▼
split answer into atomic claims
 ▼
check each claim against the context ─▶ supported / unsupported
check each citation ─▶ cited passage supports the claim?
 ▼
scores: faithfulness, hallucination rate, citation quality
(optional: LLM judge for correctness and completeness)
```

#### 1. Decomposing responses into atomic claims

FACTSCORE decomposes a generated response into atomic claims by segmenting the text into independent factual assertions, typically as simple declarative statements or subject-predicate-object triples. The decomposition is usually done by a language model prompted to rewrite each sentence into short, self-contained facts. Each fact is then checked for support against a reliable knowledge source (for RAG: the retrieved context); the automated FActScore estimator combines retrieval with a strong language model for this check. The primary metric is the support ratio: `support_ratio = (number of supported claims) / (total claims)`. This decomposition enables granular evaluation of factuality, capturing partial support (e.g., 80% of claims supported) and avoiding limitations of binary judgments. Min et al. (2023) obtained FActScores through extensive human evaluation and introduced an automated estimator that reproduces them with less than a 2% error rate. A key trade-off is that complex assertions may fragment into oversimplified claims, potentially misrepresenting nuanced statements, though this is offset by the scalability of reference-free assessment. The approach requires only the generation and a knowledge source, eliminating human annotation costs while providing actionable insights into factual accuracy.

#### 2. Context-based claim validation

Context-based claim validation decomposes the generated response into atomic claims and verifies each against provided context passages to assess groundedness. Inputs include the response string and context passages; outputs are claim-level support assessments (e.g., supported/not supported) or a faithfulness score. The algorithm typically employs a model-based approach where a lightweight language model judge [[llm-as-a-judge|LLM-as-a-Judge]] evaluates claim-context alignment via a prompt like "Does the context support the claim? [claim] [context]". Saad-Falcon et al. (2023) demonstrate this using fine-tuned judges trained on synthetic data to minimize human annotation needs. Design choices involve trade-offs between rule-based checks (computationally efficient but semantically shallow) and model-based methods (more accurate for nuanced context claims but requiring model training and introducing potential bias). The model-based approach captures semantic relationships critical for groundedness but increases computational overhead and risks model-specific scoring inconsistencies compared to simpler rule-based alternatives.

#### 3. Citation correctness verification

Citation correctness verification ensures generated citations are valid and contextually supported. Inputs include the LLM response with citations, retrieved context passages, and the original query. The process checks four aspects: (1) source existence (cited source exists in a knowledge base), (2) context inclusion (source was present in retrieved passages), (3) semantic support (context semantically validates the claim), and (4) precision (citation points to exact relevant source segment). Deterministic checks (existence and context inclusion) use string matching against retrieved passages; semantic support employs a natural language inference model or [[llm-as-a-judge|LLM-as-a-Judge]]; precision requires anchor matching (e.g., paragraph numbers). Outputs are per-citation verification results (valid/invalid) and a composite metric. Design choices prioritize deterministic checks for efficiency (low latency, no model cost), deferring semantic support to a model to balance accuracy and resource use. This trades off potential false negatives in semantic checks for scalability. Gao et al. (2023) quantified the challenge, reporting that top models lack complete citation support 50% of the time on the ELI5 dataset, underscoring the need for rigorous verification.

#### 4. LLM-as-a-Judge scoring

LLM-as-a-Judge scoring employs lightweight language models to automate semantic evaluation of RAG generations. Inputs consist of a query, retrieved context, and generated answer; outputs are scalar scores for correctness (factual accuracy), faithfulness (contextual grounding), and completeness (coverage of query requirements). The algorithm typically involves training a lightweight judge model on synthetic data generated via the RAG pipeline, followed by prediction-powered inference (PPI) using a small human-annotated validation set (e.g., hundreds of examples) to correct errors, as implemented in ARES (Saad-Falcon et al. (2023)). This design minimizes human annotation needs while maintaining cross-domain robustness. The alternative is prompting a strong general-purpose LLM as judge: Zheng et al. (2023) found that strong LLM judges such as GPT-4 agree with human preferences in over 80% of cases, the same level as agreement between humans, but also documented position, verbosity and self-enhancement biases and limited reasoning ability. Lightweight fine-tuned judges are cheaper to run; strong prompted judges need no training data. Either way, judge scores should be calibrated against a sample of human judgements.

#### 5. Hallucination rate calculation

Hallucination rate is defined as the ratio of unsupported claims to the total claims examined, computed as `hallucination_rate = unsupported_claims / total_claims`. Unsupported claims are assertions in the generated response not verifiable from the provided context. Three hallucination types are distinguished: (1) citation hallucination, where a claim references a non-existent or misattributed source; (2) grounding hallucination, where a claim lacks contextual support despite an existing source; and (3) unsupported claim, the general category of claims without contextual evidence. Inputs are the generated response and retrieved context. The algorithm processes the response by splitting it into atomic claims (e.g., via fact extraction as in FACTSCORE (Min et al. (2023))), then checks each claim against the context using semantic matching (e.g., LLM-based verification via natural language inference). Design choices prioritize robustness against paraphrasing (semantic matching) over speed (string matching), accepting higher computational cost to reduce false negatives. This trade-off is justified for accurate hallucination detection, as demonstrated in reference-free evaluation frameworks [[rag-evaluation|reference-free evaluation]], which avoid human annotation through automated claim verification as implemented in Ragas (Es et al. (2023)) and FACTSCORE (Min et al. (2023)).

#### Origin and variants

Ragas (Es et al. 2023) computes faithfulness by decomposing the generated answer into claims and verifying each against the retrieved context using LLM-based natural language inference. FACTSCORE (Min et al. 2023) breaks responses into atomic facts and scores support percentage via retrieval against a knowledge source, using an automated model with <2% error. ALCE (Gao et al. 2023) evaluates citation correctness through end-to-end system outputs, measuring fluency, correctness, and citation quality against a curated benchmark. ARES (Saad-Falcon et al. 2023) finetunes lightweight LM judges on synthetic data and applies prediction-powered inference (PPI) with a few hundred human annotations, remaining effective across domain shifts. These approaches reduce, but do not eliminate, human evaluation; their weak points are the biases of LLM-based judges and the dependence on the knowledge source or context used for checking.

### When to use it

- Checking whether answers stay faithful to the retrieved context, e.g. after changing the prompt or the model.
- Evaluating systems that cite sources, where every citation must actually support its claim (Gao et al., 2023).
- Long answers that mix supported and unsupported statements, where a single right/wrong label is too coarse (Min et al., 2023).
- Isolating generation from retrieval by evaluating with a fixed, correct context.

### Strengths and limitations

**Strengths**
- Enables reference-free generation evaluation without human annotations, reducing evaluation cost and time (Es et al. 2023; [[rag-evaluation|Evaluation]]).
- Achieves high accuracy (e.g., <2% error rate) and scales to large-scale generation sets (e.g., 6,500 generations) (Min et al. 2023).
- Requires only a few hundred human annotations for cross-domain validation across retrieval-augmented tasks (Saad-Falcon et al. 2023).

**Limitations**
- Automated estimates still deviate from human judgements and depend on the quality of the judging model and the knowledge source; a human-annotated sample remains necessary for calibration.
- Current systems exhibit significant gaps in citation support (e.g., 50% lack of complete citations on ELI5 dataset (Gao et al. 2023)).
- LLM judges show position, verbosity and self-enhancement biases and limited reasoning ability (Zheng et al. 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Reference-free suite of metrics for RAG-specific dimensions (faithfulness, answer relevance) evaluated on a controlled context. | Automated, large-scale RAG system development and testing without human annotations. |
| FACTSCORE (Min et al. 2023) | Evaluates factuality by decomposing into atomic facts and checking against a knowledge source; not RAG-specific. | General factuality assessment of LLM generations, including RAG outputs, when knowledge source access is available. |
| ARES (Saad-Falcon et al. 2023) | Uses synthetic data and fine-tuned LM judges with minimal human annotations (few hundred) for prediction-powered inference. | RAG evaluation in contexts with limited human annotation resources, robust across domain shifts. |

Ragas differs from [[llm-as-a-judge|LLM-as-a-Judge]] by providing RAG-specific metrics rather than general response evaluation, while FACTSCORE focuses on atomic fact verification without RAG pipeline context. ARES requires minimal human calibration but targets broader RAG component assessment.

### In practice

For evaluation, FACTSCORE computes factuality as the percentage of atomic facts supported by a reliable knowledge source (e.g., 58% for ChatGPT on biographies, Min et al. (2023)), while Ragas uses LLM-as-a-judge for faithfulness assessment (Es et al. (2023)). Typical failure modes include unsupported claims (42% of atomic facts in ChatGPT, Min et al. (2023)) and incomplete citation support (50% lack of complete citation support in top models, Gao et al. (2023)), documented in [[rag-failure-modes|failure modes]]. Parameter choices include the judging model, the prompt or rubric used for claim checking, and the size of the human-annotated calibration set; ARES needs a few hundred annotations for prediction-powered inference (Saad-Falcon et al. (2023)), see also [[llm-as-a-judge|LLM-as-a-judge]].

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

RAG-Generierungsbewertung bewertet die Zuverlässigkeit, Richtigkeit und Vollständigkeit der LLM-Antworten im Vergleich zum abgerufenen Kontext, ohne menschliche Annotationen zu benötigen. Sie löst das Problem langsamer und kostspieliger menschlicher Bewertung, indem sie eine automatisierte, referenzfreie Bewertung durch Frameworks wie Ragas (Es et al. (2023)) und FACTSCORE (Min et al. (2023)) ermöglicht.

### Funktionsweise

RAG-Generierungsbewertung bewertet die Antworttreue, Richtigkeit und Vollständigkeit, indem sie die Ausgaben in atomare Aussagen zerlegt, jede Aussage anhand des abgerufenen Kontexts validiert, die Richtigkeit der Zitierungen überprüft, mittels [[llm-as-a-judge|LLM-as-a-Judge]] bewertet und die Halluzinationsrate berechnet als `hallucination_rate = (unsupported_claims) / (total_claims)`. Die Prüfung auf Ebene der Aussagen bildet die Grundlage sowohl für FActScore (Min et al., 2023), der den Anteil der unterstützten atomaren Fakten bewertet, als auch für den Treue-Metrik von Ragas (Es et al., 2023); automatisierte Versionen dieser Prüfungen reduzieren den Bedarf an menschlicher Annotation, entfernen sie jedoch nicht vollständig. Die Generierungsbewertung ist die eine Hälfte von [[rag-evaluation|RAG-Bewertung]].

```text
Frage + Kontext + generierte Antwort
 ▼
Antwort in atomare Aussagen aufteilen
 ▼
jede Aussage mit dem Kontext prüfen ─▶ unterstützt / nicht unterstützt
jede Zitierung prüfen ─▶ zitiertes Passagen unterstützt die Aussage?
 ▼
Bewertungen: Treue, Halluzinationsrate, Zitierqualität
(wahlweise: LLM-Judge zur Prüfung von Richtigkeit und Vollständigkeit)
```

#### 1. Zerlegung von Antworten in atomare Aussagen

FACTSCORE zerlegt eine generierte Antwort in atomare Aussagen, indem der Text in unabhängige faktische Aussagen unterteilt wird, typischerweise als einfache deklarative Aussagen oder Subjekt-Prädikat-Objekt-Tripel. Die Zerlegung erfolgt in der Regel durch ein Sprachmodell, das angewiesen wird, jeden Satz in kurze, selbstständige Fakten umzuformulieren. Jeder Fakt wird anschließend auf Unterstützung durch eine zuverlässige Wissensquelle überprüft (bei RAG: den abgerufenen Kontext); der automatisierte FActScore-Schätzer kombiniert dabei Retrieval mit einem starken Sprachmodell. Der primäre Metrikwert ist der Unterstützungssatz: `support_ratio = (Anzahl der unterstützten Aussagen) / (Gesamtzahl der Aussagen)`. Diese Zerlegung ermöglicht eine feine Bewertung der Faktualität, wodurch teilweise Unterstützung (z. B. 80 % der Aussagen unterstützt) erfasst wird und die Grenzen binärer Urteile vermieden werden. Min et al. (2023) erhielten FActScores durch umfangreiche menschliche Bewertung und führten einen automatisierten Schätzer ein, der sie mit einem Fehleranteil von weniger als 2 % reproduziert. Ein entscheidender Kompromiss besteht darin, dass komplexe Aussagen in übervereinfachte Aussagen zerfallen können, was zu einer möglichen Fehldarstellung nuancierter Aussagen führen kann, wobei dies durch die Skalierbarkeit der referenzfreien Bewertung ausgeglichen wird. Der Ansatz benötigt nur die Generierung und eine Wissensquelle, wodurch Kosten für menschliche Annotationen eliminiert werden, während gleichzeitig wertvolle Erkenntnisse über die faktische Genauigkeit bereitgestellt werden.

#### 2. Kontextbasierte Aussagevalidierung

Die kontextbasierte Aussagevalidierung zerlegt die generierte Antwort in atomare Aussagen und überprüft jede einzelne Aussage anhand der bereitgestellten Kontextpassagen, um die Verankerung zu bewerten. Die Eingaben umfassen die Antwortzeichenfolge und die Kontextpassagen; die Ausgaben sind Bewertungen der Aussageebene (z. B. unterstützt/nicht unterstützt) oder ein Faithfulness-Score. Der Algorithmus verwendet typischerweise einen modellbasierten Ansatz, bei dem ein leichtgewichtiges Sprachmodell [[llm-as-a-judge|LLM-as-a-Judge]] die Übereinstimmung zwischen Aussage und Kontext über einen Prompt wie „Unterstützt der Kontext die Aussage? [Aussage] [Kontext]“ bewertet. Saad-Falcon et al. (2023) demonstrieren dies mithilfe von feinabgestimmten Richtern, die auf synthetischen Daten trainiert wurden, um den Bedarf an menschlicher Annotation zu minimieren. Die Gestaltungswahl beinhaltet Kompromisse zwischen regelbasierten Prüfungen (rechenintensiv, aber semantisch flach) und modellbasierten Methoden (genauer bei nuancierten Kontextaussagen, erfordert aber Modelltraining und kann potenzielle Verzerrungen einführen). Der modellbasierte Ansatz erfasst semantische Beziehungen, die für die Verankerung entscheidend sind, erhöht aber die rechnerische Belastung und birgt im Vergleich zu einfachen regelbasierten Alternativen das Risiko von modellabhängigen Bewertungsinkonsistenzen.

#### 3. Überprüfung der Zitatabsicherung

Die Überprüfung der Zitatabsicherung stellt sicher, dass generierte Zitierungen gültig und kontextuell unterstützt sind. Die Eingaben umfassen die LLM-Antwort mit Zitierungen, die abgerufenen Kontextpassagen und die ursprüngliche Anfrage. Der Prozess überprüft vier Aspekte: (1) Existenz der Quelle (die zitierte Quelle existiert in einer Wissensdatenbank), (2) Einbeziehung des Kontexts (die Quelle war in den abgerufenen Passagen vorhanden), (3) semantische Unterstützung (der Kontext validiert die Aussage semantisch) und (4) Präzision (die Zitierung verweist auf den exakt relevanten Quellabschnitt). Deterministische Überprüfungen (Existenz und Einbeziehung des Kontexts) verwenden Zeichenkettenvergleiche mit den abgerufenen Passagen; die semantische Unterstützung nutzt ein Modell für natürliche Sprachinferenz oder [[llm-as-a-judge|LLM-as-a-Judge]]. Präzision erfordert Ankererkennung (z. B. Absatznummern). Die Ausgaben sind Ergebnisse der Überprüfung pro Zitierung (gültig/ungültig) und ein Gesamtmesswert. Die Gestaltungswahl priorisiert deterministische Überprüfungen für Effizienz (geringe Latenz, kein Modellkosten), wobei die semantische Unterstützung einem Modell überlassen wird, um Genauigkeit und Ressourcennutzung auszugleichen. Dieser Ansatz opfert potenzielle Fehlalarme bei semantischen Überprüfungen für Skalierbarkeit. Gao et al. (2023) haben das Problem quantifiziert und berichtet, dass die besten Modelle in 50 % der Fälle auf dem ELI5-Datensatz keine vollständige Zitierunterstützung besitzen, was die Notwendigkeit einer strengen Überprüfung unterstreicht.

#### 4. LLM-as-a-Judge-Bewertung

Die LLM-as-a-Judge-Bewertung nutzt leichte Sprachmodelle, um die semantische Bewertung von RAG-Erzeugungen zu automatisieren. Die Eingaben bestehen aus einer Anfrage, einem abgerufenen Kontext und einer generierten Antwort; die Ausgaben sind Skalarscores für Richtigkeit (fakтиsche Genauigkeit), Glaubwürdigkeit (kontextuelle Verankerung) und Vollständigkeit (Abdeckung der Anforderungen der Anfrage). Der Algorithmus besteht typischerweise aus dem Training eines leichten Richtermodells auf synthetischen Daten, die über den RAG-Pipeline generiert wurden, gefolgt von einer Vorhersagegestützten Inferenz (PPI) mithilfe einer kleinen, von Menschen annotierten Validierungsstichprobe (z. B. einige hundert Beispiele), um Fehler zu korrigieren, wie in ARES implementiert (Saad-Falcon et al. (2023)). Dieses Design minimiert die Notwendigkeit für menschliche Annotationen, während es die robustheit über verschiedene Domänen hinweg beibehält. Die Alternative besteht darin, ein starkes allgemeines LLM als Richter zu prompten: Zheng et al. (2023) fanden heraus, dass starke LLM-Richter wie GPT-4 in über 80 % der Fälle mit menschlichen Präferenzen übereinstimmen, auf demselben Niveau wie die Übereinstimmung zwischen Menschen, dokumentierten jedoch auch Position, Lautstärke und Selbstverstärkungsviaseiten sowie begrenzte Fähigkeiten zum Denken. Leicht feinabgestimmte Richter sind günstiger in der Ausführung; starke promptierte Richter benötigen keine Trainingsdaten. Auf jeden Fall sollten Richterscores anhand einer Stichprobe menschlicher Bewertungen kalibriert werden.

#### 5. Berechnung der Halluzinationsrate

Die Halluzinationsrate wird als Verhältnis der nicht unterstützten Aussagen zur Gesamtzahl der untersuchten Aussagen definiert und berechnet sich wie folgt: `hallucination_rate = unsupported_claims / total_claims`. Nicht unterstützte Aussagen sind Aussagen im generierten Antworttext, die sich nicht aus dem bereitgestellten Kontext verifizieren lassen. Drei Arten von Halluzinationen werden unterschieden: (1) Zitathalluzination, bei der eine Aussage sich auf eine nicht existierende oder falsch zugeordnete Quelle bezieht; (2) Grundierungshalluzination, bei der eine Aussage trotz vorhandener Quelle keine kontextuelle Unterstützung aufweist; und (3) nicht unterstützte Aussage, die allgemeine Kategorie von Aussagen ohne kontextuelle Beweise. Die Eingaben sind der generierte Antworttext und der abgerufene Kontext. Der Algorithmus verarbeitet die Antwort, indem er sie in atomare Aussagen aufteilt (z. B. durch Faktextraktion wie in FACTSCORE (Min et al. (2023))), und überprüft anschließend jede Aussage im Kontext mithilfe semantischer Übereinstimmung (z. B. durch LLM-basierte Verifikation über natürliche Sprachinferenz). Die Gestaltungswahl priorisiert Robustheit gegenüber Paraphrasierung (semantische Übereinstimmung) gegenüber Geschwindigkeit (Zeichenkettenübereinstimmung), wobei ein höherer Rechenaufwand akzeptiert wird, um Falschnegative zu reduzieren. Dieser Kompromiss wird durch die genaue Halluzinationserkennung gerechtfertigt, wie in referenzfreien Bewertungsframeworks [[rag-evaluation|referenzfreie Bewertung]] gezeigt, die durch automatisierte Aussagenverifikation wie in Ragas (Es et al. (2023)) und FACTSCORE (Min et al. (2023)) menschliche Annotation vermeiden.

#### Ursprung und Varianten

Ragas (Es et al. 2023) berechnet die Treue, indem es die generierte Antwort in Aussagen zerlegt und jede Aussage mithilfe von LLM-basiertem natürlichen Sprachschluss gegen den abgerufenen Kontext überprüft. FACTSCORE (Min et al. 2023) zerlegt Antworten in atomare Fakten und bewertet den Unterstützungsprozentsatz mithilfe von Retrieval gegen eine Wissensquelle, wobei ein automatisiertes Modell mit weniger als 2 % Fehler verwendet wird. ALCE (Gao et al. 2023) bewertet die Richtigkeit von Zitaten durch End-to-End-Systemausgaben, indem Fluß, Richtigkeit und Zitatsqualität anhand eines kurierten Benchmarks gemessen werden. ARES (Saad-Falcon et al. 2023) feinabstimmte leichte LM-Beurteiler auf synthetischen Daten und wendet Vorhersagegestützte Schlussfolgerung (PPI) mit einigen hundert menschlichen Annotationen an, bleibt aber effektiv bei Domain-Shifts. Diese Ansätze reduzieren, eliminieren aber nicht, die menschliche Bewertung; ihre Schwachstellen sind die Voreingenommenheit der LLM-basierten Beurteiler und die Abhängigkeit von der Wissensquelle oder dem Kontext, der für die Überprüfung verwendet wird.

### Wann einsetzen

- Prüfen, ob Antworten dem abgerufenen Kontext treu bleiben, z. B. nach Änderung des Prompts oder des Modells.
- Bewertung von Systemen, die Quellen zitieren, wobei jedes Zitat tatsächlich die Aussage unterstützen muss (Gao et al., 2023).
- Längere Antworten, die unterstützte und nicht unterstützte Aussagen mischen, wobei eine einzelne Kennzeichnung als richtig/falsch zu grob ist (Min et al., 2023).
- Trennen der Generierung von der Retrieval-Phase durch die Bewertung mit einem festen, korrekten Kontext.

### Stärken und Grenzen

**Stärken**
- Ermöglicht die generationsbasierte Bewertung ohne Referenzen und ohne menschliche Annotationen, wodurch Kosten und Zeit für die Bewertung reduziert werden (Es et al. 2023; [[rag-evaluation|Bewertung]]).
- Erreicht eine hohe Genauigkeit (z. B. <2 % Fehlerrate) und skaliert auf große Generationsmengen (z. B. 6.500 Generierungen) (Min et al. 2023).
- Erfordert nur einige hundert menschliche Annotationen für die Kreuzdomänenumvalidierung über Aufgaben mit Retrieval-Erweiterung (Saad-Falcon et al. 2023).

**Einschränkungen**
- Automatisierte Schätzungen weichen weiterhin von menschlichen Urteilen ab und hängen von der Qualität des Urteilsmodells und der Wissensquelle ab; eine mit menschlichen Annotationen versehene Stichprobe bleibt für die Kalibrierung erforderlich.
- Aktuelle Systeme weisen erhebliche Lücken in der Unterstützung von Zitaten auf (z. B. 50 % fehlender vollständiger Zitierungen im ELI5 Datensatz (Gao et al. 2023)).
- LLM-Urteile zeigen Position-, Verbose- und Selbstverbesserungs-Voreingenommenheit sowie begrenzte Fähigkeiten im logischen Denken (Zheng et al. 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Ragas (Es et al. 2023) | Referenzfreie Metrikensuite für RAG-spezifische Dimensionen (Faithfulness, Antwortrelevanz), bewertet auf einem kontrollierten Kontext. | Automatisierte, großskalige Entwicklung und Testung von RAG-Systemen ohne menschliche Annotationen. |
| FACTSCORE (Min et al. 2023) | Bewertet Faktizität durch Zerlegung in atomare Fakten und Überprüfung gegen eine Wissensquelle; nicht RAG-spezifisch. | Allgemeine Faktizitätsbewertung von LLM-Generierungen, einschließlich RAG-Ausgaben, wenn Zugriff auf eine Wissensquelle besteht. |
| ARES (Saad-Falcon et al. 2023) | Nutzt synthetische Daten und feinabgestimmte LM-Beurteiler mit minimalen menschlichen Annotationen (hunderte) für prädiktionsgestützte Inferenz. | RAG-Bewertung in Kontexten mit begrenzten Ressourcen für menschliche Annotationen, robust gegenüber Domain-Shifts. |

Ragas unterscheidet sich von [[llm-as-a-judge|LLM-as-a-Judge]], indem es RAG-spezifische Metriken anstelle allgemeiner Antwortbewertungen bereitstellt, während FACTSCORE sich auf die Verifikation von atomaren Fakten ohne Kontext des RAG-Pipelines konzentriert. ARES benötigt minimale menschliche Kalibrierung, zielt jedoch auf eine umfassendere Bewertung von RAG-Komponenten ab.

### In der Praxis

Für die Bewertung berechnet FACTSCORE Faktualität als den Prozentsatz der atomaren Fakten, die durch eine zuverlässige Wissensquelle unterstützt werden (z. B. 58 % bei ChatGPT für Biografien, Min et al. (2023)), während Ragas Faithfulness-Prüfung mit LLM-as-a-judge durchführt (Es et al. (2023)). Typische Fehlermodi umfassen nicht unterstützte Aussagen (42 % der atomaren Fakten bei ChatGPT, Min et al. (2023)) und unvollständige Zitierunterstützung (50 % fehlender vollständiger Zitierunterstützung bei den besten Modellen, Gao et al. (2023)), dies wird in [[rag-failure-modes|Fehlermodi]] dokumentiert. Parameterauswahlen beinhalten das beurteilende Modell, den Prompt oder Rubric, der für die Prüfung von Aussagen verwendet wird, und die Größe der menschlich annotierten Kalibrierungsmenge; ARES benötigt einige hundert Annotationen für die prädiktionsgestützte Inferenz (Saad-Falcon et al. (2023)), siehe auch [[llm-as-a-judge|LLM-as-a-judge]].

### Merksatz

RAG-Generierungsbewertung ermöglicht eine skalierbare, referenzfreie Bewertung von Zuverlässigkeit, Richtigkeit und Vollständigkeit durch [[llm-as-a-judge|LLM-as-a-Judge]]-Frameworks, aber ihre domain-spezifische Genauigkeit erfordert menschliche Validierung.

### Quellen

- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.* [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
- Gao, T. et al. (2023). *Enabling Large Language Models to Generate Text with Citations.* [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Saad-Falcon, J. et al. (2023). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* [arXiv:2311.09476](https://arxiv.org/abs/2311.09476)
