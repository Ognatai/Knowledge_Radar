---
title_en: Contract Intelligence
title_de: Contract Intelligence
entity_type: Concept
sources:
- https://arxiv.org/abs/2103.06268
- https://arxiv.org/abs/2110.01799
- https://arxiv.org/abs/2110.00976
- https://arxiv.org/abs/2308.11462
- https://arxiv.org/abs/2405.20362
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Contract intelligence is the automated reading, structuring and checking of contracts: a pipeline classifies the contract type, finds relevant clauses, extracts values such as deadlines, amounts and parties, and compares the result with an internal playbook of standard clauses. It is a concrete application of [[legal-ai|Legal AI]] and [[information-extraction|Information Extraction]]. Expert-annotated datasets such as CUAD with over 13,000 annotations (Hendrycks et al., 2021) and ContractNLI with 607 contracts (Koreeda & Manning, 2021) make the task measurable and show that it is far from solved.

### How it works

#### 1. Pipeline

```text
Contract (PDF, scan, Word)
   → document preparation (OCR for scans, layout detection)
   → classification of the contract type (purchase, NDA, licence, …)
   → clause extraction (termination, liability, payment terms, …)
   → attribute extraction (deadlines, amounts, parties, dates)
   → deviation check against a playbook
   → structured output (review report, risk rating, database entry)
```

#### 2. Contract type classification

Different contract types have different relevant clauses, so systems often first determine the type, a text classification problem ([[classification|Classification]]).

#### 3. Clause extraction

Clause extraction assigns whole passages to predefined clause types, such as termination, limitation of liability, confidentiality, governing law, non-compete or change of control. CUAD frames this as highlighting the salient portions of a contract that a human should review; it was annotated by dozens of legal experts, and Transformer models showed nascent performance that depended strongly on model design and training set size (Hendrycks et al., 2021). Approaches range from keyword rules, which break on varied wording, through trained classifiers that need annotated data, to LLM-based extraction against a schema ([[information-extraction|Information Extraction]]).

#### 4. Checking statements against a contract

ContractNLI turns contract review into document-level natural language inference: given a hypothesis such as "Some obligations of Agreement may survive termination" and a contract, a system decides whether the contract entails, contradicts or does not mention it and identifies the evidence spans (Koreeda & Manning, 2021). Existing models failed badly; a stronger baseline treats evidence identification as multi-label classification over spans and segments long documents more carefully, and linguistic features of contracts such as negations by exceptions make the task hard (Koreeda & Manning, 2021).

#### 5. Attribute extraction and normalisation

After a clause is found, concrete values are extracted. Relative deadlines only become dates in the context of the contract:

```text
extracted:   "three months' notice to the end of a calendar year"
normalised:  notice must be received by 30 September to end the contract on 31 December
```

#### 6. Playbook check and redlining

A playbook defines standard clauses and acceptable deviations, for example a notice period between one and six months. Extracted values are compared with it, often with a traffic-light logic: green for standard clauses, yellow for deviations within tolerance, red for deviations that require legal review. More advanced systems suggest alternative wording for deviating clauses (redlining), which raises the requirements for explainable suggestions ([[explainable-ai|Explainable AI (XAI)]]).

#### Origin and variants

Contract review has long been handled with rules and supervised classifiers; public, expert-annotated benchmarks such as CUAD (Hendrycks et al., 2021) and ContractNLI (Koreeda & Manning, 2021) and broader legal benchmarks (Chalkidis et al., 2021; Guha et al., 2023) made systems comparable. LLMs now enable extraction with schemas and few annotated examples, and commercial tools combine them with retrieval.

### When to use it

- For due diligence, contract migration and portfolio analysis, where many contracts must be screened for the same clause types.
- When an organisation has a playbook of standard clauses against which deviations can be checked.
- When outputs can be verified: each extracted value points to the passage it came from.

### Strengths and limitations

**Strengths**
- Screens large contract portfolios consistently and prioritises the clauses that need human review.
- Evidence spans make each decision traceable to the contract text (Koreeda & Manning, 2021).
- Expert-annotated benchmarks allow measurable comparison of approaches (Hendrycks et al., 2021).

**Limitations**
- Performance depends strongly on model design and the amount of annotated training data, and there is substantial room for improvement (Hendrycks et al., 2021).
- Long documents and negations by exceptions remain hard (Koreeda & Manning, 2021).
- LLM-based tools can hallucinate; even commercial legal AI tools hallucinated on 17 to 33% of research queries (Magesh et al., 2024).
- Scans and complex layouts introduce errors before extraction starts ([[multimodal-models|Multimodal Models]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Keyword rules | Fast to build, fragile against varied wording | Narrow, well-known clause types |
| Trained clause classifiers | Need expert annotations such as those in CUAD (Hendrycks et al., 2021) | High-volume, stable clause taxonomies |
| Document-level NLI | Checks hypotheses against the contract and returns evidence spans (Koreeda & Manning, 2021) | Verifying specific obligations |
| LLM extraction with a schema | Few examples needed, but outputs must be verified (Magesh et al., 2024) | Varied contracts and changing taxonomies |

### In practice

The system identifies and prioritises, while lawyers take the final legal assessment, in line with human review as a basic principle of [[legal-ai|Legal AI]]. Clause detection is evaluated per clause type with precision and recall on annotated contracts ([[classification-metrics|Classification Metrics]]), and answers are checked for correct evidence ([[rag-generation-evaluation|RAG: Generation Evaluation]]). Extraction schemas, prompts and models are versioned and tested on a fixed set of contracts before changes go live ([[quality-control|Quality Control]]; [[regression-testing|Regression Testing]]; [[experiment-tracking|Experiment Tracking]]; [[mlops-and-deployment|MLOps and Deployment]]). Electronic signatures and seals fall under the [[eidas|eIDAS Regulation]], and using contracts as training data can raise questions of [[copyright-and-ai-training-data|Copyright and AI Training Data]].

### Key takeaway

Contract intelligence breaks contract review into classification, clause and value extraction and playbook checks; it speeds up screening, but evidence spans and human review remain necessary because the task is far from solved.

### Sources

- Hendrycks, D. et al. (2021). *CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2103.06268](https://arxiv.org/abs/2103.06268)
- Koreeda, Y. & Manning, C. D. (2021). *ContractNLI: A Dataset for Document-level Natural Language Inference for Contracts.* Findings of EMNLP 2021. [arXiv:2110.01799](https://arxiv.org/abs/2110.01799)
- Chalkidis, I. et al. (2021). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.* ACL 2022. [arXiv:2110.00976](https://arxiv.org/abs/2110.00976)
- Guha, N. et al. (2023). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models.* NeurIPS 2023 Datasets and Benchmarks. [arXiv:2308.11462](https://arxiv.org/abs/2308.11462)
- Magesh, V. et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.* Journal of Empirical Legal Studies 2025. [arXiv:2405.20362](https://arxiv.org/abs/2405.20362)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Contract Intelligence bezeichnet das automatisierte Lesen, Strukturieren und Prüfen von Verträgen: Eine Pipeline klassifiziert den Vertragstyp, findet relevante Klauseln, extrahiert Werte wie Fristen, Beträge und Parteien und vergleicht das Ergebnis mit einem internen Playbook aus Standardklauseln. Sie ist eine konkrete Anwendung von [[legal-ai|Legal AI]] und [[information-extraction|Informationsextraktion]]. Von Fachleuten annotierte Datensätze wie CUAD mit über 13.000 Annotationen (Hendrycks et al., 2021) und ContractNLI mit 607 Verträgen (Koreeda & Manning, 2021) machen die Aufgabe messbar und zeigen, dass sie längst nicht gelöst ist.

### Funktionsweise

#### 1. Pipeline

```text
Vertrag (PDF, Scan, Word)
   → Dokumentenaufbereitung (OCR bei Scans, Layout-Erkennung)
   → Klassifikation des Vertragstyps (Kaufvertrag, NDA, Lizenzvertrag, …)
   → Klausel-Extraktion (Kündigung, Haftung, Zahlungsbedingungen, …)
   → Attribut-Extraktion (Fristen, Beträge, Parteien, Datumsangaben)
   → Abweichungsprüfung gegen ein Playbook
   → strukturierte Ausgabe (Review-Bericht, Risikobewertung, Datenbankeintrag)
```

#### 2. Klassifikation des Vertragstyps

Verschiedene Vertragstypen haben unterschiedliche relevante Klauseln; Systeme bestimmen deshalb oft zuerst den Typ, ein Problem der Textklassifikation ([[classification|Klassifikation]]).

#### 3. Klausel-Extraktion

Die Klausel-Extraktion ordnet ganze Textabschnitte vordefinierten Klauseltypen zu, etwa Kündigung, Haftungsbeschränkung, Vertraulichkeit, anwendbares Recht, Wettbewerbsverbot oder Change of Control. CUAD fasst dies als Markieren der Vertragsstellen, die ein Mensch prüfen sollte; der Datensatz wurde von Dutzenden Fachleuten aus dem Recht annotiert, und Transformer-Modelle zeigten eine erst beginnende Leistung, die stark von Modellarchitektur und Umfang der Trainingsdaten abhing (Hendrycks et al., 2021). Die Verfahren reichen von Stichwortregeln, die an variierenden Formulierungen scheitern, über trainierte Klassifikatoren, die annotierte Daten brauchen, bis zur LLM-basierten Extraktion gegen ein Schema ([[information-extraction|Informationsextraktion]]).

#### 4. Aussagen gegen einen Vertrag prüfen

ContractNLI fasst die Vertragsprüfung als Natural Language Inference auf Dokumentebene: Zu einer Hypothese wie „Some obligations of Agreement may survive termination." und einem Vertrag entscheidet ein System, ob der Vertrag sie stützt, ihr widerspricht oder sie nicht erwähnt, und benennt die Belegstellen (Koreeda & Manning, 2021). Bestehende Modelle scheiterten deutlich; eine stärkere Baseline behandelt die Belegsuche als Multi-Label-Klassifikation über Textabschnitte und segmentiert lange Dokumente sorgfältiger, und sprachliche Eigenheiten von Verträgen wie Verneinungen durch Ausnahmen erschweren die Aufgabe (Koreeda & Manning, 2021).

#### 5. Attribut-Extraktion und Normalisierung

Nach dem Fund einer Klausel werden konkrete Werte extrahiert. Relative Fristen werden erst im Kontext des Vertrags zu Daten:

```text
extrahiert:    "Kündigungsfrist von drei Monaten zum Ende eines Kalenderjahres"
normalisiert:  Kündigung muss bis 30. September zugehen, damit der Vertrag am 31. Dezember endet
```

#### 6. Playbook-Prüfung und Redlining

Ein Playbook legt Standardklauseln und akzeptable Abweichungen fest, etwa eine Kündigungsfrist zwischen einem und sechs Monaten. Extrahierte Werte werden damit verglichen, oft mit einer Ampellogik: Grün für Standardklauseln, Gelb für Abweichungen innerhalb der Toleranz, Rot für Abweichungen, die eine juristische Prüfung erfordern. Weiter entwickelte Systeme schlagen für abweichende Klauseln alternative Formulierungen vor (Redlining), was die Anforderungen an nachvollziehbare Vorschläge erhöht ([[explainable-ai|Erklärbare KI (XAI)]]).

#### Ursprung und Varianten

Vertragsprüfung wurde lange mit Regeln und überwachten Klassifikatoren umgesetzt; öffentliche, von Fachleuten annotierte Benchmarks wie CUAD (Hendrycks et al., 2021) und ContractNLI (Koreeda & Manning, 2021) sowie breitere juristische Benchmarks (Chalkidis et al., 2021; Guha et al., 2023) machten Systeme vergleichbar. LLMs ermöglichen heute Extraktion mit Schemata und wenigen annotierten Beispielen, und kommerzielle Werkzeuge kombinieren sie mit Retrieval.

### Wann einsetzen

- Für Due Diligence, Vertragsmigration und Portfolioanalysen, bei denen viele Verträge auf dieselben Klauseltypen geprüft werden.
- Wenn eine Organisation ein Playbook mit Standardklauseln hat, gegen das Abweichungen geprüft werden können.
- Wenn Ausgaben überprüfbar sind: Jeder extrahierte Wert verweist auf die Stelle, aus der er stammt.

### Stärken und Grenzen

**Stärken**
- Prüft große Vertragsbestände einheitlich und priorisiert die Klauseln, die menschliche Prüfung brauchen.
- Belegstellen machen jede Entscheidung am Vertragstext nachvollziehbar (Koreeda & Manning, 2021).
- Von Fachleuten annotierte Benchmarks erlauben einen messbaren Vergleich der Ansätze (Hendrycks et al., 2021).

**Einschränkungen**
- Die Leistung hängt stark von der Modellarchitektur und der Menge annotierter Trainingsdaten ab, und es gibt viel Verbesserungsspielraum (Hendrycks et al., 2021).
- Lange Dokumente und Verneinungen durch Ausnahmen bleiben schwierig (Koreeda & Manning, 2021).
- LLM-basierte Werkzeuge können halluzinieren; selbst kommerzielle juristische KI-Werkzeuge halluzinierten bei 17 bis 33 % der Rechercheanfragen (Magesh et al., 2024).
- Scans und komplexe Layouts erzeugen Fehler, bevor die Extraktion beginnt ([[multimodal-models|Multimodale Modelle]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Stichwortregeln | Schnell gebaut, anfällig für variierende Formulierungen | Enge, bekannte Klauseltypen |
| Trainierte Klausel-Klassifikatoren | Brauchen Annotationen von Fachleuten wie in CUAD (Hendrycks et al., 2021) | Große Mengen, stabile Klauseltaxonomien |
| NLI auf Dokumentebene | Prüft Hypothesen gegen den Vertrag und liefert Belegstellen (Koreeda & Manning, 2021) | Prüfung konkreter Pflichten |
| LLM-Extraktion mit Schema | Wenige Beispiele nötig, Ausgaben müssen aber geprüft werden (Magesh et al., 2024) | Vielfältige Verträge, wechselnde Taxonomien |

### In der Praxis

Das System erkennt und priorisiert, die finale rechtliche Bewertung treffen Jurist:innen, entsprechend der menschlichen Prüfung als Grundprinzip von [[legal-ai|Legal AI]]. Die Klauselerkennung wird je Klauseltyp mit Precision und Recall auf annotierten Verträgen evaluiert ([[classification-metrics|Klassifikationsmetriken]]), Antworten werden auf korrekte Belege geprüft ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]). Extraktionsschemata, Prompts und Modelle werden versioniert und vor Änderungen an einem festen Vertragsset getestet ([[quality-control|Qualitätskontrolle]]; [[regression-testing|Regressionstests]]; [[experiment-tracking|Experiment Tracking]]; [[mlops-and-deployment|MLOps und Deployment]]). Elektronische Signaturen und Siegel fallen unter die [[eidas|eIDAS-Verordnung]], und die Nutzung von Verträgen als Trainingsdaten kann Fragen des [[copyright-and-ai-training-data|Urheberrechts an KI-Trainingsdaten]] aufwerfen.

### Merksatz

Contract Intelligence zerlegt die Vertragsprüfung in Klassifikation, Klausel- und Wertextraktion und Playbook-Abgleich; sie beschleunigt die Sichtung, doch Belegstellen und menschliche Prüfung bleiben nötig, weil die Aufgabe längst nicht gelöst ist.

### Quellen

- Hendrycks, D. et al. (2021). *CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review.* NeurIPS 2021 Datasets and Benchmarks. [arXiv:2103.06268](https://arxiv.org/abs/2103.06268)
- Koreeda, Y. & Manning, C. D. (2021). *ContractNLI: A Dataset for Document-level Natural Language Inference for Contracts.* Findings of EMNLP 2021. [arXiv:2110.01799](https://arxiv.org/abs/2110.01799)
- Chalkidis, I. et al. (2021). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.* ACL 2022. [arXiv:2110.00976](https://arxiv.org/abs/2110.00976)
- Guha, N. et al. (2023). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models.* NeurIPS 2023 Datasets and Benchmarks. [arXiv:2308.11462](https://arxiv.org/abs/2308.11462)
- Magesh, V. et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.* Journal of Empirical Legal Studies 2025. [arXiv:2405.20362](https://arxiv.org/abs/2405.20362)
