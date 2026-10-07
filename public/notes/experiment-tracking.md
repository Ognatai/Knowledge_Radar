---
title_en: Experiment Tracking
title_de: Experiment Tracking
entity_type: Method
sources:
- https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf
- https://mlflow.org/docs/latest/ml/tracking/
- https://arxiv.org/abs/2003.12206
- https://arxiv.org/abs/1909.03004
- https://arxiv.org/abs/2103.03098
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Experiment tracking is the systematic logging of ML training runs: hyperparameters, metrics, data and code versions and output files, so that results can be traced, compared and reproduced later. ML development revolves around constant experimentation with datasets, models, libraries and parameters, and keeping track of these inputs is one of the challenges that distinguishes it from traditional software development (Zaharia et al., 2018). Tools such as MLflow Tracking log parameters, code versions, metrics and artifacts per run and show them in a UI for comparison (MLflow Tracking docs).

### How it works

#### 1. What to track

```text
configuration → hyperparameters, model architecture, random seed
data          → version of the training and validation data
code          → Git commit that produced the run
metrics       → training and validation curves over time, not only the final value
artifacts     → trained weights, plots, example outputs
environment   → library versions, hardware (GPU type and count)
```

The code version links a run to its commit ([[git|Git]]), and the environment can be fixed with virtual environments and containers ([[python|Python]]; [[docker|Docker]]).

#### 2. Runs and experiments

MLflow Tracking is organised around runs, single executions of data science code such as one training script; each run records metadata, such as metrics, parameters and start and end times, and artifacts, such as model weights or images, and runs are grouped into experiments (MLflow Tracking docs).

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    for epoch in range(epochs):
        loss, val_acc = train_one_epoch()  # placeholder for the training step
        mlflow.log_metric("train_loss", loss, step=epoch)
        mlflow.log_metric("val_accuracy", val_acc, step=epoch)
    mlflow.log_artifact("confusion_matrix.png")
```

#### 3. Comparing runs

The value lies in comparison: runs are shown side by side with their hyperparameters and metrics. Conclusions need care, because variance from data sampling, parameter initialisation and hyperparameter choice affects benchmark results markedly (Bouthillier et al., 2021), and a difference of a few thousandths between two runs can lie within that variance ([[statistics-fundamentals|Statistics Fundamentals]]; [[model-comparison|Model Comparison]]).

#### 4. Hyperparameter search and reporting

Grid search, random search and Bayesian optimisation create many runs at once, each logged as its own run. Reporting test scores alone is insufficient: expected validation performance as a function of the computation budget, such as the number of hyperparameter trials, shows whether a comparison would change with more or less search (Dodge et al., 2019).

#### 5. From experiment to production

A model registry adds a hand-over to production: a catalogue of model versions and their status, such as staging, production or archived. MLflow logs and registers trained models in this way (MLflow Tracking docs). Experiment tracking answers which configuration led to which result during development; model versioning answers which model version is running after development ([[mlops-and-deployment|MLOps and Deployment]]).

#### Origin and variants

Results were long recorded in notebooks and spreadsheets. MLflow was introduced as an open-source platform for experimentation, reproducibility and deployment with generic APIs that work with any ML library (Zaharia et al., 2018); other tools such as Weights & Biases, Neptune or TensorBoard emphasise visualisation, collaboration or training curves. In research, the NeurIPS reproducibility program with a code submission policy, a reproducibility challenge and a checklist raised the standards for reporting (Pineau et al., 2020).

### When to use it

- From the first experiments onwards, as soon as more than a handful of runs exist.
- When several people work on the same models or hyperparameter searches create many runs.
- When results must be reproduced or audited later.

### Strengths and limitations

**Strengths**
- Every result can be traced to its parameters, code, data and artifacts (MLflow Tracking docs).
- Systematic comparison shows which hyperparameters actually matter.
- Supports reproducibility and the hand-over to production (Zaharia et al., 2018).

**Limitations**
- Logging is not reproducibility: seeds must be fixed, the exact data version must be referenceable and the environment reproducible, and some GPU operations stay non-deterministic unless determinism is enforced.
- Single-run comparisons ignore variance from data sampling, initialisation and hyperparameters (Bouthillier et al., 2021).
- Results depend on the computation budget spent on tuning, which must be reported to make comparisons fair (Dodge et al., 2019).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Spreadsheet or notes | Manual, quickly inconsistent | Very few runs |
| MLflow | Open source, self-hostable, with model registry (MLflow Tracking docs) | Teams that want to host their own tracking |
| Hosted tracking services | Managed service with rich visualisation | Teams without their own infrastructure |
| TensorBoard | Visualises training curves, not a full tracking system ([[keras-and-tensorflow|Keras and TensorFlow]]) | Monitoring a single training run |

### In practice

Each training script logs parameters, the Git commit, the data version and metrics automatically, and seeds are logged together with the results. Before conclusions are drawn, the best configurations are re-run with several seeds and the spread is reported (Bouthillier et al., 2021); the reproducibility checklist from NeurIPS is a useful guide (Pineau et al., 2020). For LLM and RAG systems, prompt versions, retrieval settings and evaluation scores are tracked in the same way, linking experiments to [[quality-control|Quality Control]] and [[regression-testing|Regression Testing]], for example in [[legal-ai|Legal AI]] and [[contract-intelligence|Contract Intelligence]].

### Key takeaway

Experiment tracking records every run with its configuration, code, data, metrics and artifacts, which makes results comparable and traceable; reproducibility additionally needs fixed seeds, versioned data, a fixed environment and comparisons that account for variance.

### Sources

- Zaharia, M., Chen, A., Davidson, A., Ghodsi, A., Hong, S. A., Konwinski, A., Murching, S., Nykodym, T., Ogilvie, P., Parkhe, M., Xie, F. & Zumar, C. (2018). *Accelerating the Machine Learning Lifecycle with MLflow.* IEEE Data Engineering Bulletin 41(4). [PDF](https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf)
- MLflow. *MLflow Tracking.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/ml/tracking/)
- Pineau, J. et al. (2020). *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program).* JMLR 2021. [arXiv:2003.12206](https://arxiv.org/abs/2003.12206)
- Dodge, J. et al. (2019). *Show Your Work: Improved Reporting of Experimental Results.* EMNLP 2019. [arXiv:1909.03004](https://arxiv.org/abs/1909.03004)
- Bouthillier, X. et al. (2021). *Accounting for Variance in Machine Learning Benchmarks.* MLSys 2021. [arXiv:2103.03098](https://arxiv.org/abs/2103.03098)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Experiment Tracking ist das systematische Protokollieren von ML-Trainingsläufen: Hyperparameter, Metriken, Daten- und Codeversionen sowie Ausgabedateien, damit sich Ergebnisse später nachvollziehen, vergleichen und reproduzieren lassen. ML-Entwicklung besteht aus ständigem Experimentieren mit Datensätzen, Modellen, Bibliotheken und Parametern, und den Überblick über diese Eingaben zu behalten, ist eine der Herausforderungen, die sie von klassischer Softwareentwicklung unterscheiden (Zaharia et al., 2018). Werkzeuge wie MLflow Tracking protokollieren Parameter, Codeversionen, Metriken und Artefakte je Lauf und zeigen sie zum Vergleich in einer Oberfläche (MLflow Tracking docs).

### Funktionsweise

#### 1. Was protokolliert wird

```text
Konfiguration → Hyperparameter, Modellarchitektur, Zufalls-Seed
Daten         → Version der Trainings- und Validierungsdaten
Code          → Git-Commit, der den Lauf erzeugt hat
Metriken      → Trainings- und Validierungsverläufe über die Zeit, nicht nur der Endwert
Artefakte     → trainierte Gewichte, Plots, Beispielausgaben
Umgebung      → Bibliotheksversionen, Hardware (GPU-Typ und Anzahl)
```

Die Codeversion verknüpft einen Lauf mit seinem Commit ([[git|Git]]), und die Umgebung lässt sich mit virtuellen Umgebungen und Containern festhalten ([[python|Python]]; [[docker|Docker]]).

#### 2. Runs und Experimente

MLflow Tracking ist um Runs organisiert, einzelne Ausführungen von Data-Science-Code wie ein Trainingsskript; jeder Run speichert Metadaten wie Metriken, Parameter sowie Start- und Endzeit und Artefakte wie Modellgewichte oder Bilder, und Runs werden zu Experimenten gruppiert (MLflow Tracking docs).

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    for epoch in range(epochs):
        loss, val_acc = train_one_epoch()  # Platzhalter für den Trainingsschritt
        mlflow.log_metric("train_loss", loss, step=epoch)
        mlflow.log_metric("val_accuracy", val_acc, step=epoch)
    mlflow.log_artifact("confusion_matrix.png")
```

#### 3. Läufe vergleichen

Der Nutzen liegt im Vergleich: Läufe werden mit ihren Hyperparametern und Metriken nebeneinander dargestellt. Schlüsse brauchen Sorgfalt, denn die Varianz durch Datenauswahl, Parameterinitialisierung und Hyperparameterwahl beeinflusst Benchmark-Ergebnisse deutlich (Bouthillier et al., 2021), und ein Unterschied von wenigen Tausendsteln zwischen zwei Läufen kann innerhalb dieser Varianz liegen ([[statistics-fundamentals|Statistik-Grundlagen]]; [[model-comparison|Modellvergleiche]]).

#### 4. Hyperparametersuche und Berichterstattung

Grid Search, Random Search und Bayessche Optimierung erzeugen viele Läufe auf einmal, jeder davon als eigener Run protokolliert. Nur Testergebnisse zu berichten, reicht nicht: Die erwartete Validierungsleistung in Abhängigkeit vom Rechenbudget, etwa der Zahl der Hyperparameter-Versuche, zeigt, ob sich ein Vergleich mit mehr oder weniger Suche umkehren würde (Dodge et al., 2019).

#### 5. Vom Experiment in den Betrieb

Eine Model Registry ergänzt eine Übergabe an den Betrieb: einen Katalog der Modellversionen und ihres Status, etwa Staging, Production oder Archived. MLflow protokolliert und registriert trainierte Modelle auf diese Weise (MLflow Tracking docs). Experiment Tracking beantwortet während der Entwicklung, welche Konfiguration zu welchem Ergebnis führte; Modellversionierung beantwortet danach, welche Modellversion gerade läuft ([[mlops-and-deployment|MLOps und Deployment]]).

#### Ursprung und Varianten

Ergebnisse wurden lange in Notizbüchern und Tabellen festgehalten. MLflow wurde als Open-Source-Plattform für Experimente, Reproduzierbarkeit und Deployment mit generischen APIs vorgestellt, die mit jeder ML-Bibliothek funktionieren (Zaharia et al., 2018); andere Werkzeuge wie Weights & Biases, Neptune oder TensorBoard betonen Visualisierung, Zusammenarbeit oder Trainingsverläufe. In der Forschung hob das Reproduzierbarkeitsprogramm der NeurIPS mit einer Richtlinie zur Code-Einreichung, einer Reproduzierbarkeits-Challenge und einer Checkliste die Standards für die Berichterstattung (Pineau et al., 2020).

### Wann einsetzen

- Ab den ersten Experimenten, sobald es mehr als eine Handvoll Läufe gibt.
- Wenn mehrere Personen an denselben Modellen arbeiten oder Hyperparametersuchen viele Läufe erzeugen.
- Wenn Ergebnisse später reproduziert oder auditiert werden müssen.

### Stärken und Grenzen

**Stärken**
- Jedes Ergebnis lässt sich auf seine Parameter, seinen Code, seine Daten und Artefakte zurückführen (MLflow Tracking docs).
- Systematische Vergleiche zeigen, welche Hyperparameter tatsächlich zählen.
- Unterstützt Reproduzierbarkeit und die Übergabe in den Betrieb (Zaharia et al., 2018).

**Einschränkungen**
- Protokollieren ist noch keine Reproduzierbarkeit: Seeds müssen fixiert, die genaue Datenversion referenzierbar und die Umgebung reproduzierbar sein, und manche GPU-Operationen bleiben nicht deterministisch, solange Determinismus nicht erzwungen wird.
- Vergleiche einzelner Läufe ignorieren die Varianz durch Datenauswahl, Initialisierung und Hyperparameter (Bouthillier et al., 2021).
- Ergebnisse hängen vom Rechenbudget für das Tuning ab, das für faire Vergleiche berichtet werden muss (Dodge et al., 2019).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Tabelle oder Notizen | Manuell, schnell inkonsistent | Sehr wenige Läufe |
| MLflow | Open Source, selbst hostbar, mit Model Registry (MLflow Tracking docs) | Teams, die ihr Tracking selbst betreiben |
| Gehostete Tracking-Dienste | Verwalteter Dienst mit umfangreicher Visualisierung | Teams ohne eigene Infrastruktur |
| TensorBoard | Visualisiert Trainingsverläufe, kein vollständiges Tracking-System ([[keras-and-tensorflow|Keras und TensorFlow]]) | Beobachtung eines einzelnen Trainingslaufs |

### In der Praxis

Jedes Trainingsskript protokolliert Parameter, Git-Commit, Datenversion und Metriken automatisch, und Seeds werden zusammen mit den Ergebnissen gespeichert. Bevor Schlüsse gezogen werden, laufen die besten Konfigurationen mit mehreren Seeds erneut, und die Streuung wird berichtet (Bouthillier et al., 2021); die Reproduzierbarkeits-Checkliste der NeurIPS ist eine nützliche Orientierung (Pineau et al., 2020). Bei LLM- und RAG-Systemen werden Prompt-Versionen, Retrieval-Einstellungen und Evaluationsergebnisse ebenso protokolliert, was Experimente mit [[quality-control|Qualitätskontrolle]] und [[regression-testing|Regressionstests]] verbindet, etwa in [[legal-ai|Legal AI]] und [[contract-intelligence|Contract Intelligence]].

### Merksatz

Experiment Tracking hält jeden Lauf mit Konfiguration, Code, Daten, Metriken und Artefakten fest und macht Ergebnisse vergleichbar und nachvollziehbar; Reproduzierbarkeit braucht zusätzlich fixierte Seeds, versionierte Daten, eine feste Umgebung und Vergleiche, die die Varianz berücksichtigen.

### Quellen

- Zaharia, M., Chen, A., Davidson, A., Ghodsi, A., Hong, S. A., Konwinski, A., Murching, S., Nykodym, T., Ogilvie, P., Parkhe, M., Xie, F. & Zumar, C. (2018). *Accelerating the Machine Learning Lifecycle with MLflow.* IEEE Data Engineering Bulletin 41(4). [PDF](https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf)
- MLflow. *MLflow Tracking.* MLflow documentation. [mlflow.org](https://mlflow.org/docs/latest/ml/tracking/)
- Pineau, J. et al. (2020). *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program).* JMLR 2021. [arXiv:2003.12206](https://arxiv.org/abs/2003.12206)
- Dodge, J. et al. (2019). *Show Your Work: Improved Reporting of Experimental Results.* EMNLP 2019. [arXiv:1909.03004](https://arxiv.org/abs/1909.03004)
- Bouthillier, X. et al. (2021). *Accounting for Variance in Machine Learning Benchmarks.* MLSys 2021. [arXiv:2103.03098](https://arxiv.org/abs/2103.03098)
