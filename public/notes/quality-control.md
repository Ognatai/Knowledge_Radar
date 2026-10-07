---
title_en: Quality Control
title_de: Qualitätskontrolle
entity_type: Method
sources:
- https://doi.org/10.1109/BigData.2017.8258038
- https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- https://doi.org/10.1109/ICSE-SEIP.2019.00042
- https://arxiv.org/abs/1810.03993
- https://arxiv.org/abs/1803.09010
- https://arxiv.org/abs/2005.04118
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Quality control is the systematic checking and assurance of quality in data, models, retrieval and generation across the whole lifecycle of an ML or LLM system, not a one-off test before launch. Real-world ML systems incur large ongoing maintenance costs because they depend on data and on the world around them (Sculley et al., 2015), so quality control combines tests for data, models and infrastructure with monitoring in production (Breck et al., 2017), documentation of models and datasets (Mitchell et al., 2018; Gebru et al., 2018) and behavioural tests beyond aggregate accuracy (Ribeiro et al., 2020).

### How it works

#### 1. Quality across the lifecycle

```text
data quality → development and offline evaluation → staged rollout → monitoring in production
     ↑                                                                        │
     └──────────────────────────── feedback ──────────────────────────────────┘
```

Teams at Microsoft described a nine-stage ML workflow from model requirements, data collection, cleaning and labelling through feature engineering, training and evaluation to deployment and monitoring, integrated into agile software processes (Amershi et al., 2019); quality checks belong to every stage.

#### 2. Areas to check

- **Data:** completeness and currency of the source documents, correct metadata and versions, and bias in the corpora ([[vector-databases|Vector Databases]]; [[bias-in-nlp|Bias in NLP]]). Datasheets document a dataset's motivation, composition, collection process and recommended uses (Gebru et al., 2018).
- **Retrieval:** Recall@k, Precision@k, MRR and nDCG, and checks for retrieval and ranking failures ([[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]; [[rag-failure-modes|RAG: Failure Modes]]).
- **Prompts:** systematic comparisons instead of ad-hoc changes, with prompts versioned as part of the configuration ([[prompt-comparison|Prompt Comparison]]).
- **Answers:** correctness, faithfulness, completeness and citation correctness ([[rag-generation-evaluation|RAG: Generation Evaluation]]).
- **Robustness and consistency:** stable behaviour under slightly varied inputs and across repeated runs ([[llm-evaluation|LLM Evaluation]]).

#### 3. A rubric for production readiness

The ML Test Score lists 28 tests and monitoring needs in four groups: features and data, model development, ML infrastructure and monitoring, and scores how ready a system is for production (Breck et al., 2017).

#### 4. Behavioural testing

CheckList adapts behavioural testing from software engineering to NLP: a matrix of linguistic capabilities and test types guides which tests to write, and a tool generates many test cases (Ribeiro et al., 2020). Practitioners using it created twice as many tests and found almost three times as many bugs, and a team found new bugs in an extensively tested commercial model (Ribeiro et al., 2020).

#### 5. Documentation

Model cards accompany trained models with their intended use and with evaluation results across conditions such as demographic groups (Mitchell et al., 2018); datasheets do the same for datasets (Gebru et al., 2018). Both make the limits of a system visible to the people who deploy it.

#### Origin and variants

Quality assurance comes from software engineering. For ML, the hidden technical debt of production systems (Sculley et al., 2015), rubrics such as the ML Test Score (Breck et al., 2017) and experience reports from industry (Amershi et al., 2019) defined what has to be tested beyond code; documentation standards (Mitchell et al., 2018; Gebru et al., 2018) and behavioural testing (Ribeiro et al., 2020) extended this to models and data.

### When to use it

- Always for systems in production; the depth depends on how critical errors are.
- Before every release, with a checklist: evaluation set passed, no regression against the previous version, citations validated automatically, critical cases checked manually, known edge cases re-tested ([[regression-testing|Regression Testing]]).
- With additional expert review where automated checks cannot establish correctness, such as legal correctness in [[legal-ai|Legal AI]].

### Strengths and limitations

**Strengths**
- Finds problems in data, retrieval or generation before users do.
- Error categories locate causes that an aggregate score hides ([[llm-evaluation|LLM Evaluation]]).
- Behavioural tests find bugs that held-out accuracy misses (Ribeiro et al., 2020).

**Limitations**
- Testing ML systems is hard because their prediction behaviour is difficult to specify in advance (Breck et al., 2017).
- Changes in the external world and hidden feedback loops can degrade a system without any code change (Sculley et al., 2015), so offline checks need monitoring in production.
- Automated judges and metrics only approximate correctness and need calibration against human judgement ([[llm-as-a-judge|LLM-as-a-Judge]]).

### Comparison

| Level | How it differs | Used for |
|----------|----------------|------------|
| Automated metrics | Deterministic checks, such as whether a cited norm exists | Every change |
| LLM-as-a-judge | Semantic ratings at scale ([[llm-as-a-judge|LLM-as-a-Judge]]) | Every change, larger samples |
| Expert review | Domain experts check critical cases | Critical test cases, samples |
| User feedback | Signals from real use | Continuously in production |

### In practice

Failed answers are sorted into categories, such as retrieval failure, missing information in the corpus, hallucination, interpretation error and formatting error, to find the component to fix ([[rag-failure-modes|RAG: Failure Modes]]). Each change to prompt, model, retriever or chunking runs against a fixed test set before rollout ([[regression-testing|Regression Testing]]), experiments are tracked ([[experiment-tracking|Experiment Tracking]]), and monitoring in production complements the checks before release ([[mlops-and-deployment|MLOps and Deployment]]). For RAG systems, the evaluation methods are collected in [[rag-evaluation|RAG: Evaluation]]; for contract review in [[contract-intelligence|Contract Intelligence]]; the underlying system is described in [[retrieval-augmented-generation|Retrieval-Augmented Generation]]. For the code itself, readability, reviews and refactoring are covered in [[clean-code|Clean Code]].

### Key takeaway

Quality control for ML and LLM systems is a continuous process: tests for data, models and infrastructure, behavioural tests, documentation and monitoring in production, with expert review where correctness cannot be checked automatically.

### Sources

- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* IEEE BigData 2017. [doi:10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
- Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B. & Zimmermann, T. (2019). *Software Engineering for Machine Learning: A Case Study.* ICSE-SEIP 2019. [doi:10.1109/ICSE-SEIP.2019.00042](https://doi.org/10.1109/ICSE-SEIP.2019.00042)
- Mitchell, M. et al. (2018). *Model Cards for Model Reporting.* FAT* 2019. [arXiv:1810.03993](https://arxiv.org/abs/1810.03993)
- Gebru, T. et al. (2018). *Datasheets for Datasets.* Communications of the ACM 2021. [arXiv:1803.09010](https://arxiv.org/abs/1803.09010)
- Ribeiro, M. T. et al. (2020). *Beyond Accuracy: Behavioral Testing of NLP models with CheckList.* ACL 2020. [arXiv:2005.04118](https://arxiv.org/abs/2005.04118)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Qualitätskontrolle ist die systematische Prüfung und Sicherung der Qualität von Daten, Modellen, Retrieval und Generierung über den gesamten Lebenszyklus eines ML- oder LLM-Systems, kein einmaliger Test vor dem Start. Reale ML-Systeme verursachen hohe laufende Wartungskosten, weil sie von Daten und ihrer Umgebung abhängen (Sculley et al., 2015); Qualitätskontrolle verbindet deshalb Tests für Daten, Modelle und Infrastruktur mit Monitoring im Betrieb (Breck et al., 2017), Dokumentation von Modellen und Datensätzen (Mitchell et al., 2018; Gebru et al., 2018) und Verhaltenstests jenseits aggregierter Genauigkeit (Ribeiro et al., 2020).

### Funktionsweise

#### 1. Qualität über den Lebenszyklus

```text
Datenqualität → Entwicklung und Offline-Evaluation → gestufter Rollout → Monitoring im Betrieb
     ↑                                                                          │
     └──────────────────────────── Feedback ────────────────────────────────────┘
```

Teams bei Microsoft beschrieben einen neunstufigen ML-Workflow von Modellanforderungen, Datensammlung, Bereinigung und Annotation über Feature Engineering, Training und Evaluation bis zu Deployment und Monitoring, eingebettet in agile Softwareprozesse (Amershi et al., 2019); Qualitätsprüfungen gehören in jede Stufe.

#### 2. Prüfbereiche

- **Daten:** Vollständigkeit und Aktualität der Quelldokumente, korrekte Metadaten und Versionen sowie Bias in den Korpora ([[vector-databases|Vektordatenbanken]]; [[bias-in-nlp|Bias in NLP]]). Datasheets dokumentieren Motivation, Zusammensetzung, Erhebungsprozess und empfohlene Nutzung eines Datensatzes (Gebru et al., 2018).
- **Retrieval:** Recall@k, Precision@k, MRR und nDCG sowie Prüfung auf Retrieval- und Ranking-Fehler ([[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]; [[rag-failure-modes|RAG: Typische Fehlerarten]]).
- **Prompts:** systematische Vergleiche statt Ad-hoc-Änderungen, Prompts versioniert als Teil der Konfiguration ([[prompt-comparison|Prompt-Vergleiche]]).
- **Antworten:** Korrektheit, Faithfulness, Vollständigkeit und Zitationskorrektheit ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]).
- **Robustheit und Konsistenz:** stabiles Verhalten bei leicht variierten Eingaben und über wiederholte Durchläufe ([[llm-evaluation|LLM-Evaluation]]).

#### 3. Ein Bewertungsraster für die Produktionsreife

Der ML Test Score umfasst 28 Tests und Monitoring-Anforderungen in vier Gruppen, Features und Daten, Modellentwicklung, ML-Infrastruktur und Monitoring, und bewertet, wie produktionsreif ein System ist (Breck et al., 2017).

#### 4. Verhaltenstests

CheckList überträgt Verhaltenstests aus der Softwareentwicklung auf NLP: Eine Matrix aus sprachlichen Fähigkeiten und Testtypen leitet an, welche Tests zu schreiben sind, und ein Werkzeug erzeugt viele Testfälle (Ribeiro et al., 2020). Fachleute, die es nutzten, schrieben doppelt so viele Tests und fanden fast dreimal so viele Fehler, und ein Team fand neue Fehler in einem bereits umfassend getesteten kommerziellen Modell (Ribeiro et al., 2020).

#### 5. Dokumentation

Model Cards begleiten trainierte Modelle mit ihrem vorgesehenen Einsatzzweck und Evaluationsergebnissen unter verschiedenen Bedingungen, etwa für demografische Gruppen (Mitchell et al., 2018); Datasheets leisten dasselbe für Datensätze (Gebru et al., 2018). Beide machen die Grenzen eines Systems für diejenigen sichtbar, die es einsetzen.

#### Ursprung und Varianten

Qualitätssicherung stammt aus der Softwareentwicklung. Für ML legten die versteckten technischen Schulden produktiver Systeme (Sculley et al., 2015), Bewertungsraster wie der ML Test Score (Breck et al., 2017) und Erfahrungsberichte aus der Industrie (Amershi et al., 2019) fest, was über den Code hinaus geprüft werden muss; Dokumentationsstandards (Mitchell et al., 2018; Gebru et al., 2018) und Verhaltenstests (Ribeiro et al., 2020) erweiterten dies auf Modelle und Daten.

### Wann einsetzen

- Immer bei Systemen im Betrieb; die Tiefe richtet sich danach, wie folgenreich Fehler sind.
- Vor jedem Release mit einer Checkliste: Evaluationsset bestanden, keine Regression gegenüber der Vorversion, Zitate automatisch validiert, kritische Fälle manuell geprüft, bekannte Grenzfälle erneut getestet ([[regression-testing|Regressionstests]]).
- Mit zusätzlicher fachlicher Prüfung, wo automatische Prüfungen die Richtigkeit nicht feststellen können, etwa die rechtliche Richtigkeit in [[legal-ai|Legal AI]].

### Stärken und Grenzen

**Stärken**
- Findet Probleme in Daten, Retrieval oder Generierung, bevor Nutzende sie finden.
- Fehlerkategorien lokalisieren Ursachen, die ein aggregierter Score verdeckt ([[llm-evaluation|LLM-Evaluation]]).
- Verhaltenstests finden Fehler, die die Genauigkeit auf zurückgehaltenen Daten übersieht (Ribeiro et al., 2020).

**Einschränkungen**
- ML-Systeme sind schwer zu testen, weil sich ihr Vorhersageverhalten kaum im Voraus spezifizieren lässt (Breck et al., 2017).
- Veränderungen in der Umgebung und versteckte Rückkopplungsschleifen können ein System ohne jede Codeänderung verschlechtern (Sculley et al., 2015); Offline-Prüfungen brauchen deshalb Monitoring im Betrieb.
- Automatische Bewertungen und Metriken nähern Korrektheit nur an und müssen an menschlichen Urteilen kalibriert werden ([[llm-as-a-judge|LLM-as-a-Judge]]).

### Vergleich

| Ebene | Unterschiede | Einsatz |
|----------|----------------|------------|
| Automatische Metriken | Deterministische Prüfungen, etwa ob eine zitierte Norm existiert | Jede Änderung |
| LLM-as-a-Judge | Semantische Bewertungen im großen Umfang ([[llm-as-a-judge|LLM-as-a-Judge]]) | Jede Änderung, größere Stichproben |
| Fachliche Prüfung | Fachleute prüfen kritische Fälle | Kritische Testfälle, Stichproben |
| Feedback der Nutzenden | Signale aus der realen Nutzung | Laufend im Betrieb |

### In der Praxis

Fehlerhafte Antworten werden in Kategorien sortiert, etwa Retrieval-Fehler, fehlende Information im Korpus, Halluzination, Interpretationsfehler und Formatierungsfehler, um die zu verbessernde Komponente zu finden ([[rag-failure-modes|RAG: Typische Fehlerarten]]). Jede Änderung an Prompt, Modell, Retriever oder Chunking läuft vor dem Rollout gegen ein festes Testset ([[regression-testing|Regressionstests]]), Experimente werden protokolliert ([[experiment-tracking|Experiment Tracking]]), und Monitoring im Betrieb ergänzt die Prüfungen vor dem Release ([[mlops-and-deployment|MLOps und Deployment]]). Für RAG-Systeme sind die Evaluationsmethoden in [[rag-evaluation|RAG: Evaluation]] gebündelt, für die Vertragsprüfung in [[contract-intelligence|Contract Intelligence]]; das zugrunde liegende System beschreibt [[retrieval-augmented-generation|Retrieval-Augmented Generation]]. Für den Code selbst behandelt [[clean-code|Clean Code]] Lesbarkeit, Reviews und Refactoring.

### Merksatz

Qualitätskontrolle für ML- und LLM-Systeme ist ein laufender Prozess: Tests für Daten, Modelle und Infrastruktur, Verhaltenstests, Dokumentation und Monitoring im Betrieb, ergänzt durch fachliche Prüfung, wo sich Korrektheit nicht automatisch prüfen lässt.

### Quellen

- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* IEEE BigData 2017. [doi:10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
- Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B. & Zimmermann, T. (2019). *Software Engineering for Machine Learning: A Case Study.* ICSE-SEIP 2019. [doi:10.1109/ICSE-SEIP.2019.00042](https://doi.org/10.1109/ICSE-SEIP.2019.00042)
- Mitchell, M. et al. (2018). *Model Cards for Model Reporting.* FAT* 2019. [arXiv:1810.03993](https://arxiv.org/abs/1810.03993)
- Gebru, T. et al. (2018). *Datasheets for Datasets.* Communications of the ACM 2021. [arXiv:1803.09010](https://arxiv.org/abs/1803.09010)
- Ribeiro, M. T. et al. (2020). *Beyond Accuracy: Behavioral Testing of NLP models with CheckList.* ACL 2020. [arXiv:2005.04118](https://arxiv.org/abs/2005.04118)
