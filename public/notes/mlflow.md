---
title_en: MLflow
title_de: MLflow
entity_type: Technology
aliases:
- MLflow
- MLflow Tracking
- MLflow Model Registry
sources:
- https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf
- https://mlflow.org/docs/latest/ml/tracking/
- https://mlflow.org/docs/latest/ml/model-registry/
- https://mlflow.org/docs/latest/genai/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MLflow is an open-source platform for the machine learning lifecycle, launched by [[databricks|Databricks]] in June 2018 to address experimentation, reproducibility and model deployment "using generic APIs that work with any ML library, algorithm and programming language" (Zaharia et al., 2018). Its core components are Tracking for logging runs, Projects for packaging reproducible code, Models for packaging models in several "flavors", and a Model Registry for versioning and promoting models (Zaharia et al., 2018; MLflow, n.d.-b). It has since grown into a platform for LLM and agent applications with tracing, evaluation and prompt management, and is part of the Linux Foundation (MLflow, n.d.-c).

### Core concepts

```text
Tracking:  experiment ─┬─ run (params, metrics, tags, artifacts, code version)
                       └─ logged model
Projects:  MLproject file → environment + entry points → reproducible run
Models:    MLmodel file + "flavors" → REST container, Spark UDF, cloud serving
Registry:  registered model → versions 1, 2, 3 … (linked to runs) → aliases (@champion)
GenAI:     tracing (OpenTelemetry) · evaluation with LLM judges · prompt management · AI Gateway
```

#### Tracking

MLflow Tracking is "an API and UI for logging parameters, code versions, metrics, and output files" when running ML code (MLflow, n.d.-a). It is organised around runs, single executions of data science code that record metadata and artifacts, and experiments that group runs and models for a task; by default it logs to a local `mlruns` directory, or to a shared tracking server so teams can compare results (MLflow, n.d.-a; Zaharia et al., 2018). `mlflow.autolog()` logs metrics, parameters and models for libraries such as [[scikit-learn|scikit-learn]], XGBoost, PyTorch, Keras and Spark without explicit log statements (MLflow, n.d.-a).

#### Projects and Models

An MLflow Project is a directory or [[git|Git]] repository with an `MLproject` YAML file that specifies its environment, entry points and parameters; when run through MLflow, the Git commit is recorded so the run can be re-executed (Zaharia et al., 2018). An MLflow Model is a directory with an `MLmodel` file and one or more "flavors", so the same model can be served as a [[docker|Docker]] container for REST, as an [[apache-spark|Apache Spark]] user-defined function for batch inference or on cloud serving platforms (Zaharia et al., 2018).

#### Model Registry

The Model Registry is "a centralized model store, set of APIs and a UI" for managing a model's lifecycle, with versioning, lineage to the run that produced each version, aliases such as `@champion`, tags and annotations (MLflow, n.d.-b; [[ml-pipelines|ML pipelines]]).

#### Origin and variants

Zaharia et al. (2018) at Databricks designed MLflow around an "open interface design", in contrast to internal platforms such as Facebook's FBLearner, Uber's Michelangelo and Google's TFX, which restrict the libraries developers may use. The first version offered APIs for [[python|Python]], Java and R and had over 50 contributors shortly after launch (Zaharia et al., 2018). The current documentation is split into a machine learning section and an LLM and agents section (MLflow, n.d.-c).

### Common usage

```python
import mlflow

mlflow.autolog()                     # or log explicitly:
with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    # ... train the model ...
    mlflow.log_metric("val_loss", val_loss)
```

Source: MLflow (n.d.-a).

### When to use it

- Tracking parameters, metrics and artifacts of training runs so that results can be compared and reproduced ([[experiment-tracking|experiment tracking]]).
- Handing models over to production through versioned, aliased registry entries (MLflow, n.d.-b).
- Tracing and evaluating LLM and agent applications, including LLM-as-a-judge metrics ([[llm-observability-and-tracing|LLM observability and tracing]], [[llm-as-a-judge|LLM as a judge]]; MLflow, n.d.-c).

### Strengths and limitations

**Strengths**
- Library-agnostic: works with any ML library and lets users bring their own training code, metrics and inference logic (Zaharia et al., 2018).
- Runs locally without a server and scales to a shared tracking server (MLflow, n.d.-a).
- Open source under the Linux Foundation; its tracing is compatible with OpenTelemetry, which reduces vendor lock-in (MLflow, n.d.-c).

**Limitations**
- Role-based access control for the registry depends on the backend, such as Databricks or a managed MLflow service (MLflow, n.d.-b).
- Tracking only records what is logged; data versions and environments must be captured deliberately ([[experiment-tracking|experiment tracking]]).

### Comparison

| | MLflow | Internal ML platforms (FBLearner, Michelangelo, TFX) |
|---|---|---|
| Libraries | any ML library, algorithm and language | restricted to supported libraries |
| Interfaces | open: Python functions, REST APIs, Docker containers | platform-specific APIs |
| Availability | open source | internal to one company (at the time) |

Source: Zaharia et al. (2018).

### In practice

Log every training run, including data version and Git commit, and promote models through registry aliases instead of copying files; managed MLflow is built into Databricks, where models can be governed with Unity Catalog ([[databricks|Databricks]], [[data-governance|data governance]]). For LLM applications, MLflow traces capture prompts, retrievals, tool calls and responses (MLflow, n.d.-c).

### Key takeaway

MLflow gives ML and LLM projects a common, library-independent way to track runs, package and version models and, increasingly, trace and evaluate agents.

### Sources

- Zaharia, M., Chen, A., Davidson, A., Ghodsi, A., Hong, S. A., Konwinski, A., Murching, S., Nykodym, T., Ogilvie, P., Parkhe, M., Xie, F. & Zumar, C. (2018). *Accelerating the Machine Learning Lifecycle with MLflow.* IEEE Data Engineering Bulletin 41(4). [PDF](https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf)
- MLflow (n.d.-a). *MLflow Tracking.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/ml/tracking/)
- MLflow (n.d.-b). *MLflow Model Registry.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/ml/model-registry/)
- MLflow (n.d.-c). *MLflow: AI Engineering Platform for LLMs and Agents.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/genai/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MLflow ist eine Open-Source-Plattform für den Lebenszyklus des maschinellen Lernens, im Juni 2018 von [[databricks|Databricks]] vorgestellt, um Experimentieren, Reproduzierbarkeit und Modellbereitstellung „using generic APIs that work with any ML library, algorithm and programming language“ zu unterstützen (Zaharia et al., 2018). Seine Kernkomponenten sind Tracking zum Protokollieren von Läufen, Projects zum Paketieren reproduzierbaren Codes, Models zum Paketieren von Modellen in mehreren „Flavors“ und eine Model Registry zum Versionieren und Freigeben von Modellen (Zaharia et al., 2018; MLflow, n.d.-b). Inzwischen ist es zu einer Plattform für LLM- und Agentenanwendungen mit Tracing, Evaluation und Prompt-Verwaltung gewachsen und gehört zur Linux Foundation (MLflow, n.d.-c).

### Kernkonzepte

```text
Tracking:  Experiment ─┬─ Run (Parameter, Metriken, Tags, Artefakte, Codeversion)
                       └─ protokolliertes Modell
Projects:  MLproject-Datei → Umgebung + Einstiegspunkte → reproduzierbarer Lauf
Models:    MLmodel-Datei + „Flavors“ → REST-Container, Spark-UDF, Cloud-Serving
Registry:  registriertes Modell → Versionen 1, 2, 3 … (mit Runs verknüpft) → Aliase (@champion)
GenAI:     Tracing (OpenTelemetry) · Evaluation mit LLM-Judges · Prompt-Verwaltung · AI Gateway
```

#### Tracking

MLflow Tracking ist „an API and UI for logging parameters, code versions, metrics, and output files“ beim Ausführen von ML-Code (MLflow, n.d.-a). Es ist um Runs organisiert, einzelne Ausführungen von Data-Science-Code, die Metadaten und Artefakte festhalten, und um Experimente, die Runs und Modelle für eine Aufgabe bündeln; standardmäßig protokolliert es in ein lokales Verzeichnis `mlruns` oder an einen gemeinsamen Tracking-Server, sodass Teams Ergebnisse vergleichen können (MLflow, n.d.-a; Zaharia et al., 2018). `mlflow.autolog()` protokolliert Metriken, Parameter und Modelle für Bibliotheken wie [[scikit-learn|scikit-learn]], XGBoost, PyTorch, Keras und Spark ohne explizite Log-Anweisungen (MLflow, n.d.-a).

#### Projects und Models

Ein MLflow Project ist ein Verzeichnis oder Git-Repository mit einer YAML-Datei `MLproject`, die Umgebung, Einstiegspunkte und Parameter festlegt; beim Ausführen über MLflow wird der Git-Commit gespeichert, sodass der Lauf wiederholt werden kann (Zaharia et al., 2018). Ein MLflow Model ist ein Verzeichnis mit einer Datei `MLmodel` und einem oder mehreren „Flavors“, sodass dasselbe Modell als Docker-Container für REST, als benutzerdefinierte Funktion in [[apache-spark|Apache Spark]] für Batch-Inferenz oder auf Cloud-Plattformen bereitgestellt werden kann (Zaharia et al., 2018).

#### Model Registry

Die Model Registry ist „a centralized model store, set of APIs and a UI“ zur Verwaltung des Lebenszyklus eines Modells, mit Versionierung, Lineage zum erzeugenden Run jeder Version, Aliasen wie `@champion`, Tags und Anmerkungen (MLflow, n.d.-b; [[ml-pipelines|ML-Pipelines]]).

#### Herkunft und Varianten

Zaharia et al. (2018) bei Databricks entwarfen MLflow mit einem „open interface design“, im Gegensatz zu internen Plattformen wie FBLearner von Facebook, Michelangelo von Uber und TFX von Google, die die nutzbaren Bibliotheken einschränken. Die erste Version bot APIs für [[python|Python]], Java und R und hatte kurz nach dem Start über 50 Mitwirkende (Zaharia et al., 2018). Die aktuelle Dokumentation ist in einen Bereich für maschinelles Lernen und einen für LLMs und Agenten geteilt (MLflow, n.d.-c).

### Typische Verwendung

```python
import mlflow

mlflow.autolog()                     # oder explizit protokollieren:
with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    # ... Modell trainieren ...
    mlflow.log_metric("val_loss", val_loss)
```

Quelle: MLflow (n.d.-a).

### Wann einsetzen

- Um Parameter, Metriken und Artefakte von Trainingsläufen festzuhalten, damit Ergebnisse vergleichbar und reproduzierbar sind ([[experiment-tracking|Experiment Tracking]]).
- Um Modelle über versionierte Registry-Einträge mit Aliasen in den Betrieb zu übergeben (MLflow, n.d.-b).
- Zum Tracing und zur Evaluation von LLM- und Agentenanwendungen, auch mit LLM-as-a-Judge-Metriken ([[llm-observability-and-tracing|LLM-Observability und Tracing]], [[llm-as-a-judge|LLM as a Judge]]; MLflow, n.d.-c).

### Stärken und Grenzen

**Stärken**
- Bibliotheksunabhängig: funktioniert mit jeder ML-Bibliothek, und eigener Trainingscode, eigene Metriken und Inferenzlogik lassen sich einbringen (Zaharia et al., 2018).
- Läuft lokal ohne Server und skaliert auf einen gemeinsamen Tracking-Server (MLflow, n.d.-a).
- Open Source unter der Linux Foundation; sein Tracing ist mit OpenTelemetry kompatibel, was die Bindung an Anbieter verringert (MLflow, n.d.-c).

**Grenzen**
- Rollenbasierte Zugriffskontrolle für die Registry hängt vom Backend ab, etwa Databricks oder einem verwalteten MLflow-Dienst (MLflow, n.d.-b).
- Tracking hält nur fest, was protokolliert wird; Datenversionen und Umgebungen müssen bewusst erfasst werden ([[experiment-tracking|Experiment Tracking]]).

### Vergleich

| | MLflow | Interne ML-Plattformen (FBLearner, Michelangelo, TFX) |
|---|---|---|
| Bibliotheken | jede ML-Bibliothek, jeder Algorithmus, jede Sprache | auf unterstützte Bibliotheken beschränkt |
| Schnittstellen | offen: Python-Funktionen, REST-APIs, Docker-Container | plattformspezifische APIs |
| Verfügbarkeit | Open Source | (damals) intern bei einem Unternehmen |

Quelle: Zaharia et al. (2018).

### In der Praxis

Jeder Trainingslauf wird protokolliert, einschließlich Datenversion und Git-Commit, und Modelle werden über Registry-Aliase freigegeben statt Dateien zu kopieren; verwaltetes MLflow ist in Databricks integriert, wo Modelle mit Unity Catalog gesteuert werden können ([[databricks|Databricks]], [[data-governance|Data Governance]]). Für LLM-Anwendungen erfassen MLflow-Traces Prompts, Retrieval-Schritte, Tool-Aufrufe und Antworten (MLflow, n.d.-c).

### Merksatz

MLflow gibt ML- und LLM-Projekten einen gemeinsamen, bibliotheksunabhängigen Weg, Läufe festzuhalten, Modelle zu paketieren und zu versionieren und zunehmend Agenten zu tracen und zu evaluieren.

### Quellen

- Zaharia, M., Chen, A., Davidson, A., Ghodsi, A., Hong, S. A., Konwinski, A., Murching, S., Nykodym, T., Ogilvie, P., Parkhe, M., Xie, F. & Zumar, C. (2018). *Accelerating the Machine Learning Lifecycle with MLflow.* IEEE Data Engineering Bulletin 41(4). [PDF](https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf)
- MLflow (n.d.-a). *MLflow Tracking.* MLflow-Dokumentation. [mlflow.org](https://mlflow.org/docs/latest/ml/tracking/)
- MLflow (n.d.-b). *MLflow Model Registry.* MLflow-Dokumentation. [mlflow.org](https://mlflow.org/docs/latest/ml/model-registry/)
- MLflow (n.d.-c). *MLflow: AI Engineering Platform for LLMs and Agents.* MLflow-Dokumentation. [mlflow.org](https://mlflow.org/docs/latest/genai/)
