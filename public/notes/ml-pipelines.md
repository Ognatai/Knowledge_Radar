---
title_en: ML Pipelines and Orchestration
title_de: ML-Pipelines und Orchestrierung
entity_type: Method
aliases:
- ML pipelines
- ML pipeline
- ML pipeline orchestration
- Continuous training
- ML-Pipelines
- ML-Pipeline
sources:
- https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- https://docs.zenml.io/getting-started/core-concepts
- https://www.kubeflow.org/docs/components/pipelines/overview/
- https://mlflow.org/docs/latest/ml/model-registry/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

An ML pipeline turns the steps of model development, from data extraction and validation through training and evaluation to registration, into an automated, versioned workflow that can be rerun on new data. Google describes this as the step from a manual, notebook-driven process (MLOps level 0) to continuous training (level 1) and finally to CI/CD for the pipelines themselves (level 2) (Google Cloud). Orchestration frameworks such as ZenML and Kubeflow Pipelines define pipelines as [[python|Python]] code, run each step in a container on a chosen infrastructure, store every intermediate artifact and record metadata for lineage and caching (ZenML; Kubeflow). A model registry such as [[mlflow|MLflow]]'s holds the resulting model versions and the aliases that decide which version is served (MLflow).

### How it works

```text
trigger: schedule, new data, drift alert, code change, manual
 ▼
data extraction → data validation (schema and value skew) → data preparation
 ▼
training → evaluation → model validation (against baseline and data segments)
 ▼
model registry: new version + metadata + lineage to the run
 ▼
deployment of the approved version (alias) → monitoring → next trigger
 (every step: containerised, inputs/outputs stored as artefacts, run metadata recorded)
```

#### 1. From manual process to continuous training

At MLOps level 0, every step from data analysis to validation is manual, often in notebooks; data scientists hand a trained model to engineers, models change only a few times a year, and predictions are rarely logged, so degradation goes unnoticed (Google Cloud). Level 1 automates the pipeline to achieve continuous training: the same pipeline code runs in experimentation, pre-production and production ("experimental-operational symmetry"), components are modular and ideally containerised, and what is deployed is the training pipeline that keeps producing models rather than a single model (Google Cloud). Level 2 adds CI/CD so that new pipeline components are built, tested and deployed automatically; see [[ci-cd|CI/CD]].

#### 2. Steps, artefacts and the DAG

A pipeline is a directed acyclic graph of steps. In ZenML, steps are Python functions with the `@step` decorator and typed inputs and outputs, and a pipeline is a function that calls them; a step only starts when the steps it depends on have finished (ZenML). Data passes between steps as artefacts: datasets, models, metrics, prompts or evaluation results are written to storage after a step and loaded by the next, not passed in memory, and materialisers define how each type is serialised (ZenML). In Kubeflow Pipelines, each component execution corresponds to a single container execution, and the compiled pipeline is an intermediate-representation YAML file that a conformant backend runs (Kubeflow). Storing artefacts makes caching possible: a step whose inputs have not changed is not run again (ZenML; Kubeflow).

#### 3. Validation gates

Two checks guard the pipeline (Google Cloud). Data validation before training stops the run when incoming data does not match the expected schema (schema skew) and signals retraining when its statistics shift significantly (value skew). Model validation after training compares the new model with the current one on a test set, checks quality on important data segments and confirms compatibility with the serving infrastructure; online validation follows with canary releases or A/B tests. Drift and quality monitoring are covered in [[monitoring-and-alerting|monitoring and alerting]].

#### 4. Infrastructure abstraction: stacks and backends

Orchestration frameworks separate pipeline code from where it runs. ZenML calls the execution environment a stack: a set of components of which an orchestrator, which decides which steps run when, and an artefact store, which holds all inputs and outputs, are required; flavours implement each component for a specific tool, and the stack can be switched without changing pipeline code (ZenML). Kubeflow Pipelines aims at portable pipelines that run on Kubernetes ([[kubernetes|Kubernetes]]); the same compiled pipeline can be submitted to the open-source KFP backend or to Google Cloud's Vertex AI Pipelines (Kubeflow), renamed Agent Platform Pipelines in April 2026 ([[cloud-ai-platforms|cloud AI platforms]]). General-purpose data orchestrators such as Airflow, described in [[data-pipelines|data pipelines]], schedule data workflows; ML orchestrators add artefact typing, model tracking and ML-specific integrations.

#### 5. Metadata, lineage and the model registry

Metadata management records, for every run, the pipeline and component versions, start time, parameters, artefact locations, earlier models for rollback and evaluation metrics; this enables lineage, reproducibility and resuming failed runs (Google Cloud). ZenML stores step parameters so that a run can be reproduced exactly and keeps immutable snapshots of a pipeline's graph, code, configuration and container images (ZenML). Trained models go into a registry: in MLflow, a registered model has a unique name and numbered versions, each linked to the run that produced it, and mutable aliases such as `champion` point to the version that serves production, so promoting or rolling back means moving the alias (MLflow). Run-level tracking is covered in [[experiment-tracking|experiment tracking]].

#### 6. Triggers and serving

Pipelines run on demand, on a schedule, when new training data arrives, when model performance degrades or when the data distribution shifts (Google Cloud). An optional feature store serves the same feature definitions for training and serving, which prevents training-serving skew (Google Cloud). ZenML can also expose a pipeline as a long-running [[http|HTTP]] service, where each request creates a new run (ZenML). Serving strategies are described in [[mlops-and-deployment|MLOps and deployment]].

#### Origin and variants

Google's MLOps maturity levels describe the move from manual work to automated pipelines (Google Cloud). Kubeflow Pipelines builds on Kubernetes and containers; ZenML describes itself as "a unified, extensible, open-source MLOps framework for creating portable, production-ready MLOps pipelines" and extends the same concepts to AI agents and their evaluation (Kubeflow; ZenML). Managed services such as Vertex AI Pipelines run the same pipeline format on a cloud platform (Kubeflow), see [[cloud-ai-platforms|cloud AI platforms]].

### When to use it

- Models must be retrained regularly on new data, or degrade as the data changes (Google Cloud).
- Several people develop pipeline components and need reproducible runs and shared artefacts (ZenML).
- The same workflow has to run locally during development and on cloud or Kubernetes infrastructure in production (ZenML; Kubeflow).

### Strengths and limitations

**Strengths**
- Reproducibility and lineage: every model can be traced to its code, data, parameters and run (Google Cloud; MLflow).
- Caching of unchanged steps and parallel execution save compute (Kubeflow).
- Rollback is a matter of pointing an alias back to an earlier version (MLflow).

**Limitations**
- Level 1 automation alone does not test or deploy new pipeline code; teams that try many new ideas need level 2 CI/CD (Google Cloud).
- Data and model analysis remain manual even at level 2 (Google Cloud).
- Each orchestrator brings its own abstractions and infrastructure to operate, from a ZenML server to a Kubernetes cluster (ZenML; Kubeflow).

### Comparison

| Tool | Focus | Pipeline definition | Runs on |
|---|---|---|---|
| ZenML | MLOps framework with switchable stacks | Python `@step` / `@pipeline` | local, cloud orchestrators, Kubernetes |
| Kubeflow Pipelines | containerised ML workflows | KFP Python SDK, compiled to YAML | KFP backend on Kubernetes, Vertex AI Pipelines |
| Airflow ([[data-pipelines\|data pipelines]]) | general data workflows | Python DAGs | scheduler and workers |
| MLflow ([[experiment-tracking\|experiment tracking]]) | tracking and registry, not orchestration | logging API | tracking server |

Sources: ZenML; Kubeflow; MLflow.

### In practice

Pipelines are tested like other code, with unit tests for feature logic and integration tests between components ([[software-testing|software testing]]). Google suggests promoting pipelines semi-automatically: automatic deployment to a test environment, semi-automatic deployment to pre-production after review, and manual deployment to production after several successful pre-production runs (Google Cloud). On [[databricks|Databricks]], the MLflow registry is integrated with Unity Catalog, where model versions require a signature (MLflow); see [[data-lakehouse|data lakehouse]].

### Key takeaway

ML pipelines turn data validation, training, evaluation and registration into a containerised, versioned graph of steps that runs on triggers, with artefacts, metadata and a model registry making every model reproducible and every deployment reversible.

### Sources

- Google Cloud. *MLOps: Continuous delivery and automation pipelines in machine learning.* Cloud Architecture Center. [docs.cloud.google.com](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- ZenML. *Core concepts.* ZenML documentation. [docs.zenml.io](https://docs.zenml.io/getting-started/core-concepts)
- Kubeflow. *Overview of Kubeflow Pipelines.* [kubeflow.org](https://www.kubeflow.org/docs/components/pipelines/overview/)
- MLflow. *MLflow Model Registry.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/ml/model-registry/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine ML-Pipeline macht aus den Schritten der Modellentwicklung, von Datenextraktion und Validierung über Training und Evaluation bis zur Registrierung, einen automatisierten, versionierten Ablauf, der auf neuen Daten erneut ausgeführt werden kann. Google beschreibt das als Weg von einem manuellen, notebookgetriebenen Prozess (MLOps-Stufe 0) zu Continuous Training (Stufe 1) und schließlich zu CI/CD für die Pipelines selbst (Stufe 2) (Google Cloud). Orchestrierungs-Frameworks wie ZenML und Kubeflow Pipelines definieren Pipelines als Python-Code, führen jeden Schritt in einem Container auf einer gewählten Infrastruktur aus, speichern jedes Zwischenartefakt und erfassen Metadaten für Lineage und Caching (ZenML; Kubeflow). Eine Model Registry wie die von [[mlflow|MLflow]] hält die entstehenden Modellversionen und die Aliase, die bestimmen, welche Version ausgeliefert wird (MLflow).

### Funktionsweise

```text
Trigger: Zeitplan, neue Daten, Drift-Alarm, Codeänderung, manuell
 ▼
Datenextraktion → Datenvalidierung (Schema- und Werteabweichung) → Datenaufbereitung
 ▼
Training → Evaluation → Modellvalidierung (gegen Baseline und Datensegmente)
 ▼
Model Registry: neue Version + Metadaten + Lineage zum Lauf
 ▼
Deployment der freigegebenen Version (Alias) → Monitoring → nächster Trigger
 (jeder Schritt: containerisiert, Ein- und Ausgaben als Artefakte gespeichert, Laufmetadaten erfasst)
```

#### 1. Vom manuellen Prozess zu Continuous Training

Auf MLOps-Stufe 0 ist jeder Schritt von der Datenanalyse bis zur Validierung manuell, oft in Notebooks; Data Scientists übergeben ein trainiertes Modell an Engineers, Modelle ändern sich nur wenige Male im Jahr, und Vorhersagen werden selten protokolliert, sodass Verschlechterungen unbemerkt bleiben (Google Cloud). Stufe 1 automatisiert die Pipeline, um Continuous Training zu erreichen: Derselbe Pipeline-Code läuft in Experiment, Vorproduktion und Produktion („experimental-operational symmetry“), Komponenten sind modular und idealerweise containerisiert, und ausgeliefert wird die Trainingspipeline, die laufend Modelle erzeugt, statt eines einzelnen Modells (Google Cloud). Stufe 2 ergänzt CI/CD, sodass neue Pipeline-Komponenten automatisch gebaut, getestet und ausgeliefert werden; siehe [[ci-cd|CI/CD]].

#### 2. Schritte, Artefakte und der DAG

Eine Pipeline ist ein gerichteter azyklischer Graph aus Schritten. In ZenML sind Schritte Python-Funktionen mit dem Decorator `@step` und typisierten Ein- und Ausgaben, und eine Pipeline ist eine Funktion, die sie aufruft; ein Schritt startet erst, wenn die Schritte, von denen er abhängt, fertig sind (ZenML). Daten wandern als Artefakte zwischen den Schritten: Datensätze, Modelle, Metriken, Prompts oder Evaluationsergebnisse werden nach einem Schritt gespeichert und vom nächsten geladen, nicht im Speicher weitergereicht, und Materializer legen fest, wie jeder Typ serialisiert wird (ZenML). In Kubeflow Pipelines entspricht jede Ausführung einer Komponente der Ausführung eines einzelnen Containers, und die kompilierte Pipeline ist eine YAML-Datei in einer Zwischenrepräsentation, die ein konformes Backend ausführt (Kubeflow). Gespeicherte Artefakte ermöglichen Caching: Ein Schritt, dessen Eingaben sich nicht geändert haben, läuft nicht erneut (ZenML; Kubeflow).

#### 3. Validierungsschranken

Zwei Prüfungen sichern die Pipeline ab (Google Cloud). Die Datenvalidierung vor dem Training stoppt den Lauf, wenn eingehende Daten nicht zum erwarteten Schema passen (Schema Skew), und signalisiert ein Neutraining, wenn sich ihre Statistik deutlich verschiebt (Value Skew). Die Modellvalidierung nach dem Training vergleicht das neue Modell auf einem Testset mit dem aktuellen, prüft die Qualität auf wichtigen Datensegmenten und bestätigt die Kompatibilität mit der Serving-Infrastruktur; online folgen Canary Releases oder A/B-Tests. Drift- und Qualitätsüberwachung behandelt [[monitoring-and-alerting|Monitoring und Alerting]].

#### 4. Abstraktion der Infrastruktur: Stacks und Backends

Orchestrierungs-Frameworks trennen den Pipeline-Code davon, wo er läuft. ZenML nennt die Ausführungsumgebung einen Stack: eine Menge von Komponenten, von denen ein Orchestrator, der entscheidet, welche Schritte wann laufen, und ein Artifact Store, der alle Ein- und Ausgaben hält, Pflicht sind; Flavors implementieren jede Komponente für ein bestimmtes Werkzeug, und der Stack lässt sich wechseln, ohne den Pipeline-Code zu ändern (ZenML). Kubeflow Pipelines zielt auf portable Pipelines, die auf Kubernetes laufen ([[kubernetes|Kubernetes]]); dieselbe kompilierte Pipeline kann an das Open-Source-Backend von KFP oder an Vertex AI Pipelines von Google Cloud übergeben werden (Kubeflow), seit April 2026 Agent Platform Pipelines ([[cloud-ai-platforms|Cloud-KI-Plattformen]]). Allgemeine Orchestratoren für Daten wie Airflow, beschrieben in [[data-pipelines|Datenpipelines]], planen Datenabläufe; ML-Orchestratoren ergänzen typisierte Artefakte, Modell-Tracking und ML-spezifische Integrationen.

#### 5. Metadaten, Lineage und die Model Registry

Das Metadatenmanagement hält für jeden Lauf die Versionen von Pipeline und Komponenten, Startzeit, Parameter, Speicherorte der Artefakte, frühere Modelle für ein Rollback und Evaluationsmetriken fest; das ermöglicht Lineage, Reproduzierbarkeit und das Fortsetzen fehlgeschlagener Läufe (Google Cloud). ZenML speichert Schrittparameter, damit sich ein Lauf exakt reproduzieren lässt, und hält unveränderliche Snapshots von Graph, Code, Konfiguration und Container-Images einer Pipeline (ZenML). Trainierte Modelle kommen in eine Registry: In MLflow hat ein registriertes Modell einen eindeutigen Namen und nummerierte Versionen, die jeweils mit dem erzeugenden Lauf verknüpft sind, und veränderliche Aliase wie `champion` zeigen auf die Version, die die Produktion bedient; Freigabe oder Rollback heißt, den Alias zu verschieben (MLflow). Tracking auf Ebene einzelner Läufe behandelt [[experiment-tracking|Experiment Tracking]].

#### 6. Trigger und Serving

Pipelines laufen bei Bedarf, nach Zeitplan, wenn neue Trainingsdaten eintreffen, wenn sich die Modellleistung verschlechtert oder wenn sich die Datenverteilung verschiebt (Google Cloud). Ein optionaler Feature Store stellt Training und Serving dieselben Feature-Definitionen bereit und verhindert so Abweichungen zwischen beiden (Google Cloud). ZenML kann eine Pipeline zudem als dauerhaft laufenden HTTP-Dienst bereitstellen, bei dem jede Anfrage einen neuen Lauf erzeugt (ZenML). Serving-Strategien beschreibt [[mlops-and-deployment|MLOps und Deployment]].

#### Herkunft und Varianten

Googles MLOps-Reifegrade beschreiben den Weg von manueller Arbeit zu automatisierten Pipelines (Google Cloud). Kubeflow Pipelines baut auf Kubernetes und Containern auf; ZenML beschreibt sich als „a unified, extensible, open-source MLOps framework for creating portable, production-ready MLOps pipelines“ und überträgt dieselben Konzepte auf KI-Agenten und deren Evaluation (Kubeflow; ZenML). Verwaltete Dienste wie Vertex AI Pipelines führen dasselbe Pipeline-Format auf einer Cloud-Plattform aus (Kubeflow), siehe [[cloud-ai-platforms|Cloud-KI-Plattformen]].

### Wann einsetzen

- Modelle müssen regelmäßig auf neuen Daten nachtrainiert werden oder verschlechtern sich, wenn sich die Daten ändern (Google Cloud).
- Mehrere Personen entwickeln Pipeline-Komponenten und brauchen reproduzierbare Läufe und gemeinsame Artefakte (ZenML).
- Derselbe Ablauf muss in der Entwicklung lokal und in der Produktion auf Cloud- oder Kubernetes-Infrastruktur laufen (ZenML; Kubeflow).

### Stärken und Grenzen

**Stärken**
- Reproduzierbarkeit und Lineage: Jedes Modell lässt sich auf Code, Daten, Parameter und Lauf zurückführen (Google Cloud; MLflow).
- Caching unveränderter Schritte und parallele Ausführung sparen Rechenleistung (Kubeflow).
- Ein Rollback besteht darin, einen Alias auf eine frühere Version zurückzusetzen (MLflow).

**Grenzen**
- Automatisierung nach Stufe 1 allein testet und liefert keinen neuen Pipeline-Code aus; Teams, die viele neue Ideen ausprobieren, brauchen CI/CD nach Stufe 2 (Google Cloud).
- Daten- und Modellanalyse bleiben auch auf Stufe 2 manuell (Google Cloud).
- Jeder Orchestrator bringt eigene Abstraktionen und zu betreibende Infrastruktur mit, vom ZenML-Server bis zum Kubernetes-Cluster (ZenML; Kubeflow).

### Vergleich

| Werkzeug | Schwerpunkt | Definition der Pipeline | Läuft auf |
|---|---|---|---|
| ZenML | MLOps-Framework mit austauschbaren Stacks | [[python\|Python]] `@step` / `@pipeline` | lokal, Cloud-Orchestratoren, Kubernetes |
| Kubeflow Pipelines | containerisierte ML-Abläufe | KFP Python SDK, kompiliert zu YAML | KFP-Backend auf Kubernetes, Vertex AI Pipelines |
| Airflow ([[data-pipelines\|Datenpipelines]]) | allgemeine Datenabläufe | Python-DAGs | Scheduler und Worker |
| MLflow ([[experiment-tracking\|Experiment Tracking]]) | Tracking und Registry, keine Orchestrierung | Logging-API | Tracking-Server |

Quellen: ZenML; Kubeflow; MLflow.

### In der Praxis

Pipelines werden wie anderer Code getestet, mit Unit-Tests für die Feature-Logik und Integrationstests zwischen Komponenten ([[software-testing|Softwaretests]]). Google schlägt eine gestufte Freigabe von Pipelines vor: automatisches Deployment in eine Testumgebung, halbautomatisches Deployment in die Vorproduktion nach einem Review und manuelles Deployment in die Produktion nach mehreren erfolgreichen Läufen in der Vorproduktion (Google Cloud). Auf [[databricks|Databricks]] ist die MLflow-Registry in Unity Catalog integriert, wo Modellversionen eine Signatur brauchen (MLflow); siehe [[data-lakehouse|Data Lakehouse]].

### Merksatz

ML-Pipelines machen aus Datenvalidierung, Training, Evaluation und Registrierung einen containerisierten, versionierten Graphen aus Schritten, der auf Trigger reagiert; Artefakte, Metadaten und eine Model Registry machen jedes Modell reproduzierbar und jedes Deployment umkehrbar.

### Quellen

- Google Cloud. *MLOps: Continuous delivery and automation pipelines in machine learning.* Cloud Architecture Center. [docs.cloud.google.com](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- ZenML. *Core concepts.* ZenML-Dokumentation. [docs.zenml.io](https://docs.zenml.io/getting-started/core-concepts)
- Kubeflow. *Overview of Kubeflow Pipelines.* [kubeflow.org](https://www.kubeflow.org/docs/components/pipelines/overview/)
- MLflow. *MLflow Model Registry.* MLflow-Dokumentation. [mlflow.org](https://mlflow.org/docs/latest/ml/model-registry/)
