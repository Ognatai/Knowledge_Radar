---
title_en: MLOps and Deployment
title_de: MLOps und Deployment
entity_type: Method
sources:
- https://arxiv.org/abs/2205.02302
- https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- https://arxiv.org/abs/2011.09926
- https://arxiv.org/abs/1810.11953
- https://doi.org/10.1109/BigData.2017.8258038
- https://doi.org/10.1109/ICSE-SEIP.2019.00042
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MLOps transfers DevOps principles such as automation, versioning, continuous integration and monitoring to the lifecycle of ML models, with the goal of bringing ML products into production and operating them reliably (Kreuzberger et al., 2022). Unlike classical software, an ML system depends not only on code but also on data and trained weights, which change independently; real-world ML systems therefore incur massive ongoing maintenance costs (Sculley et al., 2015), and practitioners face issues at every stage of deployment (Paleyes et al., 2020). A model that was evaluated well once does not stay good: data and user behaviour change, and ML systems tend to fail silently (Rabanser et al., 2018).

### How it works

#### 1. The ML lifecycle

```text
collect data → preprocessing → training → evaluation → deployment → monitoring
     ↑                                                                    │
     └──────────────────────────── retraining ────────────────────────────┘
```

Teams at Microsoft described a nine-stage workflow from model requirements and data work through training and evaluation to deployment and monitoring, integrated into agile software processes (Amershi et al., 2019). The cycle never really ends, because both the data and the requirements change ([[ml-preprocessing|Preprocessing for Machine Learning]]; [[neural-network-evaluation|Evaluating Neural Networks]]; [[llm-evaluation|LLM Evaluation]]).

#### 2. Model serving

- **Batch inference:** predictions are computed in advance for large amounts of data, for example a nightly risk rating of all open cases.
- **Real-time inference:** predictions are computed per request, as in a [[retrieval-augmented-generation|Retrieval-Augmented Generation]] system or an agent ([[agentic-ai|Agentic AI]]); latency and scalability matter here.

Models are usually packaged as container images and run on orchestration platforms ([[docker|Docker]]; [[kubernetes|Kubernetes]]).

#### 3. Versioning code, data and model

Code, data and trained weights must be versioned together; otherwise it can no longer be traced which model was trained with which data and which code ([[git|Git]]; [[experiment-tracking|Experiment Tracking]]). The same applies to embedding models and vector indexes in RAG systems ([[embeddings|Embeddings]]; [[vector-databases|Vector Databases]]). The ML Test Score asks for reproducible training and for model specifications that are reviewed and checked into a repository (Breck et al., 2017).

#### 4. CI/CD for ML

```text
commit code change → unit tests → retrain / run regression tests → check quality on a fixed evaluation set → deploy if no regression
```

The ML-specific steps check data and model quality, not only code ([[regression-testing|Regression Testing]]). MLOps combines such pipelines with roles, components and workflows for the whole lifecycle (Kreuzberger et al., 2022).

#### 5. Deployment strategies

- **Shadow deployment:** the new model runs alongside the old one; its predictions are logged but not shown to users.
- **Canary release:** the new model first receives a small share of requests, for example 5%, which grows step by step if no problems occur. The ML Test Score asks that models are tested via a canary process before they enter production serving (Breck et al., 2017).
- **Blue-green deployment:** two complete production environments run in parallel, and switching between them is a single step that can be undone immediately.

#### 6. Monitoring and rollback

- **Data drift:** the distribution of inputs moves away from the training data. For detecting such dataset shift, two-sample tests on representations from pretrained classifiers performed best in an empirical comparison (Rabanser et al., 2018).
- **Concept drift:** the relationship between input and correct output itself changes, for example through new user behaviour, market conditions or legal rules.
- **Rollback:** for every strategy, a defined way back to the last known good model version exists; the ML Test Score lists the ability to roll back serving models and monitoring of dependencies, data invariants, training–serving skew, staleness and prediction quality (Breck et al., 2017).

#### Origin and variants

The term MLOps grew out of DevOps and the experience that ML systems accumulate hidden technical debt (Sculley et al., 2015). Rubrics for production readiness (Breck et al., 2017), industry case studies (Amershi et al., 2019; Paleyes et al., 2020) and overviews of principles, components and roles (Kreuzberger et al., 2022) shaped the field; LLM systems add prompts, retrieval indexes and hosted models as further components to version and monitor.

### When to use it

- As soon as a model is used in production and must be updated, monitored or audited.
- When several people or teams train, deploy and operate models.
- To a lighter degree for prototypes: versioning and tracking from the start make later production much easier.

### Strengths and limitations

**Strengths**
- Reproducible results through joint versioning of code, data and model.
- Safer releases through automated quality gates, staged rollouts and rollback.
- Problems in production are detected through monitoring instead of user complaints (Rabanser et al., 2018).

**Limitations**
- MLOps is still a vague term, and many ML projects fail to deliver on their expectations because automating and operationalising them is hard (Kreuzberger et al., 2022).
- Practitioners face challenges at every stage of the deployment workflow (Paleyes et al., 2020).
- Entanglement, hidden feedback loops and undeclared consumers make ML systems hard to change safely (Sculley et al., 2015).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Shadow deployment | New model invisible to users, predictions only logged | Observing a model under real traffic without risk |
| Canary release | New model visible to a growing share of requests (Breck et al., 2017) | Gradual, measurable rollout |
| Blue-green deployment | Two complete environments, instant switch | Fast, reversible changeover |
| Batch vs. real-time inference | Precomputed vs. per-request predictions | Reports vs. interactive applications |

### In practice

A typical setup versions code in Git, data and models with their identifiers, tracks every training run, packages models in containers and deploys them through a pipeline that runs regression tests and quality checks first ([[git|Git]]; [[experiment-tracking|Experiment Tracking]]; [[docker|Docker]]; [[quality-control|Quality Control]]). In production, input distributions, quality metrics and costs are monitored, and a rollback path is tested regularly. For [[legal-ai|Legal AI]] and [[contract-intelligence|Contract Intelligence]], model and corpus versions also document which state of the law and which model produced an answer. Data shared between connected products and services can fall under the [[data-act|Data Act]].

### Key takeaway

MLOps keeps ML systems reliable after the first deployment: code, data and model are versioned together, changes pass automated quality gates and staged rollouts, and monitoring with rollback catches drift that offline tests cannot see.

### Sources

- Kreuzberger, D. et al. (2022). *Machine Learning Operations (MLOps): Overview, Definition, and Architecture.* IEEE Access 2023. [arXiv:2205.02302](https://arxiv.org/abs/2205.02302)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
- Paleyes, A. et al. (2020). *Challenges in Deploying Machine Learning: a Survey of Case Studies.* ACM Computing Surveys 2022. [arXiv:2011.09926](https://arxiv.org/abs/2011.09926)
- Rabanser, S. et al. (2018). *Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift.* NeurIPS 2019. [arXiv:1810.11953](https://arxiv.org/abs/1810.11953)
- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* IEEE BigData 2017. [doi:10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038)
- Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B. & Zimmermann, T. (2019). *Software Engineering for Machine Learning: A Case Study.* ICSE-SEIP 2019. [doi:10.1109/ICSE-SEIP.2019.00042](https://doi.org/10.1109/ICSE-SEIP.2019.00042)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MLOps überträgt DevOps-Prinzipien wie Automatisierung, Versionierung, kontinuierliche Integration und Monitoring auf den Lebenszyklus von ML-Modellen, mit dem Ziel, ML-Produkte in den Betrieb zu bringen und zuverlässig zu betreiben (Kreuzberger et al., 2022). Anders als klassische Software hängt ein ML-System nicht nur vom Code ab, sondern auch von Daten und trainierten Gewichten, die sich unabhängig voneinander ändern; reale ML-Systeme verursachen deshalb hohe laufende Wartungskosten (Sculley et al., 2015), und in jeder Phase des Deployments treten Probleme auf (Paleyes et al., 2020). Ein einmal gut evaluiertes Modell bleibt nicht gut: Daten und Nutzungsverhalten ändern sich, und ML-Systeme scheitern oft unbemerkt (Rabanser et al., 2018).

### Funktionsweise

#### 1. Der ML-Lebenszyklus

```text
Daten sammeln → Preprocessing → Training → Evaluation → Deployment → Monitoring
     ↑                                                                      │
     └──────────────────────────── Retraining ──────────────────────────────┘
```

Teams bei Microsoft beschrieben einen neunstufigen Workflow von Modellanforderungen und Datenarbeit über Training und Evaluation bis zu Deployment und Monitoring, eingebettet in agile Softwareprozesse (Amershi et al., 2019). Der Zyklus endet nie wirklich, weil sich Daten und Anforderungen ändern ([[ml-preprocessing|Preprocessing für Machine Learning]]; [[neural-network-evaluation|Modellbewertung neuronaler Netze]]; [[llm-evaluation|LLM-Evaluation]]).

#### 2. Model Serving

- **Batch-Inferenz:** Vorhersagen werden für große Datenmengen im Voraus berechnet, etwa eine nächtliche Risikobewertung aller offenen Fälle.
- **Echtzeit-Inferenz:** Vorhersagen werden pro Anfrage berechnet, etwa in einem [[retrieval-augmented-generation|Retrieval-Augmented-Generation]]-System oder bei einem Agenten ([[agentic-ai|Agentic AI]]); hier zählen Latenz und Skalierbarkeit.

Modelle werden meist als Container-Images verpackt und auf Orchestrierungsplattformen betrieben ([[docker|Docker]]; [[kubernetes|Kubernetes]]).

#### 3. Code, Daten und Modell versionieren

Code, Daten und trainierte Gewichte müssen gemeinsam versioniert werden; sonst lässt sich nicht mehr nachvollziehen, welches Modell mit welchen Daten und welchem Code trainiert wurde ([[git|Git]]; [[experiment-tracking|Experiment Tracking]]). Dasselbe gilt für Embedding-Modelle und Vektorindizes in RAG-Systemen ([[embeddings|Embeddings]]; [[vector-databases|Vektordatenbanken]]). Der ML Test Score verlangt reproduzierbares Training und Modellspezifikationen, die geprüft und in ein Repository eingecheckt werden (Breck et al., 2017).

#### 4. CI/CD für ML

```text
Codeänderung committen → Unit-Tests → neu trainieren / Regressionstests → Qualität auf festem Evaluationsset prüfen → ausrollen, falls keine Regression
```

Die ML-spezifischen Schritte prüfen Daten- und Modellqualität, nicht nur Code ([[regression-testing|Regressionstests]]). MLOps verbindet solche Pipelines mit Rollen, Komponenten und Workflows für den gesamten Lebenszyklus (Kreuzberger et al., 2022).

#### 5. Deployment-Strategien

- **Shadow Deployment:** Das neue Modell läuft neben dem alten mit; seine Vorhersagen werden protokolliert, aber nicht an Nutzende ausgeliefert.
- **Canary Release:** Das neue Modell erhält zunächst einen kleinen Anteil der Anfragen, etwa 5 %, der schrittweise wächst, wenn keine Probleme auftreten. Der ML Test Score verlangt, dass Modelle in einem Canary-Prozess getestet werden, bevor sie in den produktiven Betrieb gehen (Breck et al., 2017).
- **Blue-Green Deployment:** Zwei vollständige Produktionsumgebungen laufen parallel, und das Umschalten ist ein einzelner, sofort umkehrbarer Schritt.

#### 6. Monitoring und Rollback

- **Data Drift:** Die Verteilung der Eingaben entfernt sich von den Trainingsdaten. Zum Erkennen solcher Verteilungsverschiebungen schnitten in einem empirischen Vergleich Zwei-Stichproben-Tests auf Repräsentationen vortrainierter Klassifikatoren am besten ab (Rabanser et al., 2018).
- **Concept Drift:** Der Zusammenhang zwischen Eingabe und korrekter Ausgabe ändert sich selbst, etwa durch neues Nutzungsverhalten, Marktbedingungen oder rechtliche Vorgaben.
- **Rollback:** Für jede Strategie gibt es einen festgelegten Rückweg zur letzten bekannt guten Modellversion; der ML Test Score nennt die Möglichkeit, ausgerollte Modelle zurückzurollen, sowie Monitoring von Abhängigkeiten, Dateninvarianten, Abweichungen zwischen Training und Betrieb, Veralterung und Vorhersagequalität (Breck et al., 2017).

#### Ursprung und Varianten

Der Begriff MLOps entstand aus DevOps und der Erfahrung, dass ML-Systeme versteckte technische Schulden anhäufen (Sculley et al., 2015). Bewertungsraster für die Produktionsreife (Breck et al., 2017), Fallstudien aus der Industrie (Amershi et al., 2019; Paleyes et al., 2020) und Überblicke über Prinzipien, Komponenten und Rollen (Kreuzberger et al., 2022) prägten das Feld; LLM-Systeme fügen Prompts, Retrieval-Indizes und gehostete Modelle als weitere zu versionierende und zu überwachende Komponenten hinzu.

### Wann einsetzen

- Sobald ein Modell im Betrieb genutzt wird und aktualisiert, überwacht oder auditiert werden muss.
- Wenn mehrere Personen oder Teams Modelle trainieren, ausrollen und betreiben.
- In leichterer Form schon bei Prototypen: Versionierung und Tracking von Anfang an erleichtern den späteren Betrieb deutlich.

### Stärken und Grenzen

**Stärken**
- Reproduzierbare Ergebnisse durch gemeinsame Versionierung von Code, Daten und Modell.
- Sicherere Releases durch automatische Qualitätsschranken, gestufte Rollouts und Rollback.
- Probleme im Betrieb werden durch Monitoring erkannt statt durch Beschwerden der Nutzenden (Rabanser et al., 2018).

**Einschränkungen**
- MLOps ist noch ein unscharfer Begriff, und viele ML-Projekte erfüllen die Erwartungen nicht, weil Automatisierung und Betrieb schwierig sind (Kreuzberger et al., 2022).
- In jeder Phase des Deployment-Workflows treten Herausforderungen auf (Paleyes et al., 2020).
- Verflechtung, versteckte Rückkopplungsschleifen und nicht deklarierte Nutzer von Modellausgaben erschweren sichere Änderungen an ML-Systemen (Sculley et al., 2015).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Shadow Deployment | Neues Modell für Nutzende unsichtbar, Vorhersagen nur protokolliert | Modell unter realem Verkehr ohne Risiko beobachten |
| Canary Release | Neues Modell für einen wachsenden Anteil der Anfragen sichtbar (Breck et al., 2017) | Schrittweiser, messbarer Rollout |
| Blue-Green Deployment | Zwei vollständige Umgebungen, sofortiges Umschalten | Schneller, umkehrbarer Wechsel |
| Batch- vs. Echtzeit-Inferenz | Vorab berechnete vs. pro Anfrage berechnete Vorhersagen | Berichte vs. interaktive Anwendungen |

### In der Praxis

Ein typisches Setup versioniert Code in Git, Daten und Modelle mit ihren Kennungen, protokolliert jeden Trainingslauf, verpackt Modelle in Container und rollt sie über eine Pipeline aus, die zuerst Regressionstests und Qualitätsprüfungen ausführt ([[git|Git]]; [[experiment-tracking|Experiment Tracking]]; [[docker|Docker]]; [[quality-control|Qualitätskontrolle]]). Im Betrieb werden Eingabeverteilungen, Qualitätsmetriken und Kosten überwacht, und der Rückweg wird regelmäßig getestet. Bei [[legal-ai|Legal AI]] und [[contract-intelligence|Contract Intelligence]] dokumentieren Modell- und Korpusversionen zusätzlich, welcher Rechtsstand und welches Modell eine Antwort erzeugt haben. Daten, die zwischen vernetzten Produkten und Diensten geteilt werden, können unter die [[data-act|Datenverordnung (Data Act)]] fallen.

### Merksatz

MLOps hält ML-Systeme nach dem ersten Deployment zuverlässig: Code, Daten und Modell werden gemeinsam versioniert, Änderungen durchlaufen automatische Qualitätsschranken und gestufte Rollouts, und Monitoring mit Rollback fängt Drift ab, die Offline-Tests nicht sehen.

### Quellen

- Kreuzberger, D. et al. (2022). *Machine Learning Operations (MLOps): Overview, Definition, and Architecture.* IEEE Access 2023. [arXiv:2205.02302](https://arxiv.org/abs/2205.02302)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
- Paleyes, A. et al. (2020). *Challenges in Deploying Machine Learning: a Survey of Case Studies.* ACM Computing Surveys 2022. [arXiv:2011.09926](https://arxiv.org/abs/2011.09926)
- Rabanser, S. et al. (2018). *Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift.* NeurIPS 2019. [arXiv:1810.11953](https://arxiv.org/abs/1810.11953)
- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* IEEE BigData 2017. [doi:10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038)
- Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B. & Zimmermann, T. (2019). *Software Engineering for Machine Learning: A Case Study.* ICSE-SEIP 2019. [doi:10.1109/ICSE-SEIP.2019.00042](https://doi.org/10.1109/ICSE-SEIP.2019.00042)
