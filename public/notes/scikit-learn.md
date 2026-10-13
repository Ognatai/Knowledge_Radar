---
title_en: scikit-learn
title_de: scikit-learn
entity_type: Technology
aliases:
- sklearn
sources:
- https://www.jmlr.org/papers/v12/pedregosa11a.html
- https://arxiv.org/abs/1309.0238
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
scikit-learn is a Python library for classical machine learning: classification, regression, clustering, dimensionality reduction, preprocessing and model selection, built on NumPy and SciPy and distributed under the BSD licence (Pedregosa et al., 2011). Its defining feature is one consistent interface: every learning or processing step is an estimator with a `fit` method, so that steps can be chained into pipelines and tuned with cross-validation (Buitinck et al., 2013).

### Core concepts

#### 1. Estimators
The estimator is the central object. It is created with its hyperparameters, which are stored as public attributes, and learns from data in its `fit` method, which takes an input array and, for supervised problems, the labels. Learned parameters are exposed as attributes as well, such as the coefficients of a linear model (Pedregosa et al., 2011; Buitinck et al., 2013).

#### 2. Predictors and transformers
A predictor adds a `predict` method for new data and a `score` method that rates its performance on a batch of data. A transformer adds a `transform` method that modifies or filters data; preprocessing, feature selection, feature extraction and dimensionality reduction are all transformers (Buitinck et al., 2013).

#### 3. Composition
A `Pipeline` chains several estimators into one, and a `FeatureUnion` combines transformers in parallel; the result is itself an estimator and can be used wherever an estimator is expected (Buitinck et al., 2013).

#### 4. Model selection
`GridSearchCV` and `RandomizedSearchCV` are meta-estimators: for every hyperparameter combination and every train/validation split of the [[cross-validation|cross-validation]] scheme, they fit the base estimator on the training part and evaluate it on the validation part (Buitinck et al., 2013).

#### 5. Design principles
The API follows five principles: consistency (all objects share a small set of methods), inspection (parameters are public attributes), non-proliferation of classes (only learning algorithms get their own classes; data are NumPy arrays or SciPy sparse matrices), composition, and sensible defaults for every parameter (Buitinck et al., 2013).

### Common usage

A typical workflow splits the data, chains preprocessing and a model in a pipeline and evaluates or tunes it with cross-validation:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
search = GridSearchCV(pipeline, {"model__C": [0.1, 1, 10]}, cv=10)
search.fit(X_train, y_train)          # scaling is fitted inside every fold
print(search.best_params_, search.score(X_test, y_test))
```

Because the scaler is part of the pipeline, it is fitted on the training folds only, which keeps information from the validation folds out of the model ([[ml-preprocessing|ML Preprocessing]]; [[cross-validation|Cross-validation]]). The library wraps compiled code where speed matters, for example LibSVM and LibLinear for [[support-vector-machines|support vector machines]] and linear models (Pedregosa et al., 2011).

### When to use it
- Classical machine learning on tabular data: [[classification|classification]], regression, [[clustering|clustering]], [[decision-trees|decision trees]], [[k-nearest-neighbours|k-nearest neighbours]] ([[classical-machine-learning|Classical Machine Learning]]).
- Preprocessing, [[feature-engineering|feature engineering]] and dimensionality reduction as reusable steps ([[ml-preprocessing|ML Preprocessing]]; Buitinck et al., 2013).
- Model selection and evaluation with cross-validation and hyperparameter search (Buitinck et al., 2013; [[regularisation-and-hyperparameters|Regularisation and Hyperparameters]]).
- In teaching and for non-specialists: the library aims to bring machine learning to non-specialists in a general-purpose language (Pedregosa et al., 2011).

### Strengths and limitations

**Strengths**
- One consistent interface for all algorithms, so models can be swapped without changing the surrounding code (Buitinck et al., 2013).
- Pipelines and meta-estimators make whole workflows, including tuning, a single object (Buitinck et al., 2013).
- Emphasis on ease of use, performance, documentation and API consistency; minimal dependencies and a BSD licence that allows academic and commercial use (Pedregosa et al., 2011).
- Code quality is enforced with unit tests and style guidelines (Pedregosa et al., 2011; Buitinck et al., 2013).

**Limitations**
- In 2013 the authors listed [[neural-networks|neural networks]], bagging and subsampling ensembles, and missing-value completion as not yet supported; structured prediction and reinforcement learning were out of scope, because they need different data representations and APIs (Buitinck et al., 2013). For deep learning, frameworks such as [[keras-and-tensorflow|Keras and TensorFlow]] are used.
- Data must fit the array model: inputs are NumPy arrays or SciPy sparse matrices (Buitinck et al., 2013).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| scikit-learn | Ready-made algorithms behind one estimator interface, with pipelines and model selection (Buitinck et al., 2013) | Classical ML, preprocessing, evaluation |
| NumPy and SciPy | The array, linear algebra and sparse matrix layer scikit-learn builds on (Pedregosa et al., 2011) | Numerical code written by hand |
| [[keras-and-tensorflow\|Keras and TensorFlow]] | Deep learning frameworks; neural networks were outside scikit-learn's scope in 2013 (Buitinck et al., 2013) | Neural networks, large unstructured data |

### In practice
scikit-learn is usually the first library for a baseline: a simple model and a tree ensemble compared with cross-validation before more complex models are tried ([[classical-machine-learning|Classical Machine Learning]]; [[model-comparison|Model Comparison]]). Putting every data-dependent step into a pipeline avoids leaking information from the test data; experiments and their parameters are worth recording ([[experiment-tracking|Experiment Tracking]]). It is part of the scientific [[python|Python]] stack around NumPy and SciPy (Pedregosa et al., 2011).

### Key takeaway
scikit-learn's value lies less in any single algorithm than in its uniform estimator interface: fit, predict and transform make models interchangeable and whole workflows composable and tunable.

### Sources
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research 12. [JMLR](https://www.jmlr.org/papers/v12/pedregosa11a.html)
- Buitinck, L. et al. (2013). *API design for machine learning software: experiences from the scikit-learn project.* [arXiv:1309.0238](https://arxiv.org/abs/1309.0238)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
scikit-learn ist eine Python-Bibliothek für klassisches maschinelles Lernen: Klassifikation, Regression, Clustering, Dimensionsreduktion, Vorverarbeitung und Modellauswahl, aufgebaut auf NumPy und SciPy und unter der BSD-Lizenz verbreitet (Pedregosa et al., 2011). Kennzeichnend ist eine einheitliche Schnittstelle: Jeder Lern- oder Verarbeitungsschritt ist ein Estimator mit einer `fit`-Methode, sodass sich Schritte zu Pipelines verketten und per Kreuzvalidierung abstimmen lassen (Buitinck et al., 2013).

### Kernkonzepte

#### 1. Estimators
Der Estimator ist das zentrale Objekt. Er wird mit seinen Hyperparametern angelegt, die als öffentliche Attribute gespeichert werden, und lernt in seiner `fit`-Methode aus Daten, die ein Eingabe-Array und bei überwachten Problemen die Labels erhält. Gelernte Parameter sind ebenfalls als Attribute zugänglich, etwa die Koeffizienten eines linearen Modells (Pedregosa et al., 2011; Buitinck et al., 2013).

#### 2. Predictors und Transformers
Ein Predictor ergänzt eine `predict`-Methode für neue Daten und eine `score`-Methode, die seine Leistung auf einem Datenstapel bewertet. Ein Transformer ergänzt eine `transform`-Methode, die Daten verändert oder filtert; Vorverarbeitung, Merkmalsauswahl, Merkmalsextraktion und Dimensionsreduktion sind allesamt Transformer (Buitinck et al., 2013).

#### 3. Komposition
Eine `Pipeline` verkettet mehrere Estimators zu einem, und eine `FeatureUnion` kombiniert Transformer parallel; das Ergebnis ist selbst ein Estimator und überall einsetzbar, wo ein Estimator erwartet wird (Buitinck et al., 2013).

#### 4. Modellauswahl
`GridSearchCV` und `RandomizedSearchCV` sind Meta-Estimators: Für jede Hyperparameter-Kombination und jede Trainings-/Validierungsaufteilung des [[cross-validation|Kreuzvalidierungs]]-Schemas passen sie den Basis-Estimator auf dem Trainingsteil an und bewerten ihn auf dem Validierungsteil (Buitinck et al., 2013).

#### 5. Designprinzipien
Die API folgt fünf Prinzipien: Konsistenz (alle Objekte teilen wenige Methoden), Inspektion (Parameter sind öffentliche Attribute), keine Klassenflut (nur Lernalgorithmen erhalten eigene Klassen; Daten sind NumPy-Arrays oder dünnbesetzte SciPy-Matrizen), Komposition und sinnvolle Voreinstellungen für jeden Parameter (Buitinck et al., 2013).

### Typische Verwendung

Ein typischer Ablauf teilt die Daten, verkettet Vorverarbeitung und Modell in einer Pipeline und bewertet oder stimmt sie per Kreuzvalidierung ab:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
search = GridSearchCV(pipeline, {"model__C": [0.1, 1, 10]}, cv=10)
search.fit(X_train, y_train)          # die Skalierung wird in jedem Fold neu angepasst
print(search.best_params_, search.score(X_test, y_test))
```

Weil der Scaler Teil der Pipeline ist, wird er nur auf den Trainings-Folds angepasst; so gelangen keine Informationen aus den Validierungs-Folds ins Modell ([[ml-preprocessing|ML-Vorverarbeitung]]; [[cross-validation|Kreuzvalidierung]]). Wo Geschwindigkeit zählt, bindet die Bibliothek kompilierten Code ein, etwa LibSVM und LibLinear für [[support-vector-machines|Support Vector Machines]] und lineare Modelle (Pedregosa et al., 2011).

### Wann einsetzen
- Klassisches maschinelles Lernen auf tabellarischen Daten: [[classification|Klassifikation]], Regression, [[clustering|Clustering]], [[decision-trees|Entscheidungsbäume]], [[k-nearest-neighbours|k-Nächste-Nachbarn]] ([[classical-machine-learning|Klassisches Machine Learning]]).
- Vorverarbeitung, [[feature-engineering|Feature Engineering]] und Dimensionsreduktion als wiederverwendbare Schritte ([[ml-preprocessing|ML-Vorverarbeitung]]; Buitinck et al., 2013).
- Modellauswahl und Evaluation mit Kreuzvalidierung und Hyperparameter-Suche (Buitinck et al., 2013; [[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]).
- In der Lehre und für Nicht-Fachleute: Die Bibliothek soll maschinelles Lernen in einer allgemeinen Programmiersprache für Nicht-Fachleute zugänglich machen (Pedregosa et al., 2011).

### Stärken und Grenzen

**Stärken**
- Eine einheitliche Schnittstelle für alle Algorithmen; Modelle lassen sich austauschen, ohne den umgebenden Code zu ändern (Buitinck et al., 2013).
- Pipelines und Meta-Estimators machen ganze Abläufe einschließlich Abstimmung zu einem Objekt (Buitinck et al., 2013).
- Schwerpunkt auf Bedienbarkeit, Leistung, Dokumentation und API-Konsistenz; wenige Abhängigkeiten und eine BSD-Lizenz, die akademische und kommerzielle Nutzung erlaubt (Pedregosa et al., 2011).
- Codequalität wird mit Unit-Tests und Stilrichtlinien gesichert (Pedregosa et al., 2011; Buitinck et al., 2013).

**Grenzen**
- 2013 nannten die Autoren [[neural-networks|neuronale Netze]], Bagging- und Subsampling-Ensembles sowie das Auffüllen fehlender Werte als noch nicht unterstützt; strukturierte Vorhersage und Reinforcement Learning lagen außerhalb des Projektumfangs, weil sie andere Datenrepräsentationen und APIs erfordern (Buitinck et al., 2013). Für Deep Learning werden Frameworks wie [[keras-and-tensorflow|Keras und TensorFlow]] verwendet.
- Die Daten müssen ins Array-Modell passen: Eingaben sind NumPy-Arrays oder dünnbesetzte SciPy-Matrizen (Buitinck et al., 2013).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| scikit-learn | Fertige Algorithmen hinter einer Estimator-Schnittstelle, mit Pipelines und Modellauswahl (Buitinck et al., 2013) | Klassisches ML, Vorverarbeitung, Evaluation |
| NumPy und SciPy | Die Schicht für Arrays, lineare Algebra und dünnbesetzte Matrizen, auf der scikit-learn aufbaut (Pedregosa et al., 2011) | Selbst geschriebener numerischer Code |
| [[keras-and-tensorflow\|Keras und TensorFlow]] | Deep-Learning-Frameworks; neuronale Netze lagen 2013 außerhalb des Umfangs von scikit-learn (Buitinck et al., 2013) | Neuronale Netze, große unstrukturierte Daten |

### In der Praxis
scikit-learn ist meist die erste Bibliothek für eine Baseline: Ein einfaches Modell und ein Baum-Ensemble werden per Kreuzvalidierung verglichen, bevor komplexere Modelle versucht werden ([[classical-machine-learning|Klassisches Machine Learning]]; [[model-comparison|Modellvergleich]]). Wer jeden datenabhängigen Schritt in eine Pipeline legt, verhindert, dass Informationen aus den Testdaten durchsickern; Experimente und ihre Parameter sollten festgehalten werden ([[experiment-tracking|Experiment Tracking]]). Die Bibliothek gehört zum wissenschaftlichen [[python|Python]]-Stack rund um NumPy und SciPy (Pedregosa et al., 2011).

### Merksatz
Der Wert von scikit-learn liegt weniger in einem einzelnen Algorithmus als in der einheitlichen Estimator-Schnittstelle: fit, predict und transform machen Modelle austauschbar und ganze Abläufe kombinier- und abstimmbar.

### Quellen
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research 12. [JMLR](https://www.jmlr.org/papers/v12/pedregosa11a.html)
- Buitinck, L. et al. (2013). *API design for machine learning software: experiences from the scikit-learn project.* [arXiv:1309.0238](https://arxiv.org/abs/1309.0238)
