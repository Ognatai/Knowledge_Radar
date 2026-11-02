---
title_en: Hyperparameter Optimisation
title_de: Hyperparameter-Optimierung
entity_type: Method
aliases:
- Hyperparameter optimisation
- Hyperparameter optimization
- Hyperparameter tuning
- Hyperparameter search
- Grid search
- Random search
- Bayesian optimisation
- Hyperband
- Successive halving
sources:
- https://www.jmlr.org/papers/v13/bergstra12a.html
- https://arxiv.org/abs/1206.2944
- https://arxiv.org/abs/1603.06560
- https://arxiv.org/abs/1907.10902
- https://scikit-learn.org/stable/modules/grid_search.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Hyperparameter optimisation searches for the settings that a learning algorithm does not learn itself, such as the learning rate, regularisation strength or tree depth, by training models with different settings and comparing them on validation data ([[scikit-learn|scikit-learn]]). Grid search tries every combination of given values; random search samples combinations and is more efficient because usually only a few hyperparameters matter (Bergstra & Bengio, 2012). Bayesian optimisation models the validation score as a function of the hyperparameters and picks the next trial where improvement is most likely (Snoek et al., 2012), and Hyperband and successive halving stop poor configurations early to spend the budget on promising ones (Li et al., 2018).

### How it works

```text
define search space (ranges or distributions per hyperparameter) + budget
   ▼
loop:
    propose configuration     grid │ random │ Bayesian model (GP, TPE) │ bandit (Hyperband)
    train model, score on validation folds (cross-validation)
    (optional) stop unpromising trials early   ← successive halving / pruning
   ▼
best configuration ──► refit on all training data ──► evaluate once on held-out test data
```

#### 1. What is searched

A search consists of an estimator, a parameter space, a method for searching or sampling candidates, a cross-validation scheme and a score function (scikit-learn). Hyperparameters differ from model parameters, which training learns from data ([[regularisation-and-hyperparameters|regularisation and hyperparameters]]). Typically a small subset of hyperparameters has a large impact on performance while the others can stay at their defaults (scikit-learn; Bergstra & Bengio, 2012).

#### 2. Grid search

`GridSearchCV` exhaustively evaluates all combinations of given values with [[cross-validation|cross-validation]] (scikit-learn). Its cost grows exponentially with the number of hyperparameters, and if only some of them matter, most trials repeat the same values of the important ones (Bergstra & Bengio, 2012).

#### 3. Random search

Random search samples each configuration from distributions over the hyperparameters. Bergstra and Bengio (2012) showed empirically and theoretically that this is more efficient than a grid: the function from hyperparameters to validation performance has low effective dimensionality, so random trials cover the important dimensions with more distinct values. Compared with pure grid search for [[neural-networks|neural networks]], random search found models as good or better in a small fraction of the computation time; for deep belief networks in a 32-dimensional space, it matched a careful manual-plus-grid configuration on four of seven data sets and beat it on one (Bergstra & Bengio, 2012). In scikit-learn, `RandomizedSearchCV` lets the budget be chosen independently of the number of parameters, and adding irrelevant parameters does not reduce its efficiency (scikit-learn).

#### 4. Bayesian optimisation

Bayesian optimisation treats the validation score as a sample from a Gaussian process; its posterior uses all previous trials to choose the next configuration, for example by maximising expected improvement (Snoek et al., 2012). Snoek et al. (2012) showed that the choice of prior and inference procedure strongly affects success, added methods that account for the varying duration of experiments and for parallel runs, and reached or exceeded expert-level tuning for latent Dirichlet allocation, structured SVMs and convolutional networks. Other frameworks use a tree-structured Parzen estimator (TPE) instead of a Gaussian process (Akiba et al., 2019).

#### 5. Early stopping of trials: successive halving and Hyperband

Successive halving gives a budget to many configurations, evaluates them, discards the worst half and repeats with more resources for the survivors; the resource can be training iterations, data samples or features (Li et al., 2018; scikit-learn). Because it requires choosing the number of configurations in advance, Hyperband runs successive halving with several trade-offs between many cheap and few expensive trials; it gave over an order-of-magnitude speed-up over Bayesian optimisation methods on deep learning and kernel problems (Li et al., 2018). scikit-learn offers `HalvingGridSearchCV` and `HalvingRandomSearchCV` (scikit-learn), and Optuna combines searching with pruning of unpromising trials and a define-by-run API that builds the search space dynamically (Akiba et al., 2019).

#### Origin and variants

Grid search and manual search were long the most widely used strategies (Bergstra & Bengio, 2012). Random search (Bergstra & Bengio, 2012), Gaussian-process Bayesian optimisation as in Spearmint (Snoek et al., 2012; Akiba et al., 2019), Hyperband (Li et al., 2018) and frameworks such as Optuna (Akiba et al., 2019) followed.

### When to use it

- Every model with hyperparameters whose good values are unknown, from [[ridge-and-lasso|ridge and lasso]] penalties to neural network learning rates ([[gradient-descent|gradient descent]]).
- Grid search for one or two hyperparameters with few values; random search for more (Bergstra & Bengio, 2012).
- Bayesian optimisation when each trial is expensive and the number of trials small (Snoek et al., 2012).
- Hyperband or successive halving when partial training gives a useful early signal (Li et al., 2018).

### Strengths and limitations

**Strengths**
- Random search is simple, parallel and robust to irrelevant hyperparameters (Bergstra & Bengio, 2012; scikit-learn).
- Model-based and early-stopping methods find good settings with far fewer full trainings (Snoek et al., 2012; Li et al., 2018).

**Limitations**
- Each trial trains a model, so search can dominate compute cost.
- Tuning on the same data used to report results overestimates performance; scikit-learn recommends nested cross-validation for evaluating a model with grid search (scikit-learn; [[cross-validation|cross-validation]]).
- Bayesian optimisation is sensitive to its own modelling choices (Snoek et al., 2012).
- Early stopping can mislead when configurations need a long time before their quality differs, for example when training converges slowly; Hyperband hedges by mixing aggressive and conservative brackets (Li et al., 2018).

### Comparison

| Method | How it picks trials | Uses earlier results | Strength |
|---|---|---|---|
| Grid search | all combinations | no | exhaustive for few parameters |
| Random search | random samples | no | efficient, parallel |
| Bayesian optimisation | surrogate model + acquisition | yes | few expensive trials |
| Successive halving / Hyperband | many cheap, few expensive | yes (early stopping) | large speed-ups |

Sources: Bergstra & Bengio (2012), Snoek et al. (2012), Li et al. (2018).

### In practice

Define distributions on sensible scales, for example log-uniform for learning rates and regularisation strengths, start with random search or successive halving, refit the best configuration on all training data and evaluate it once on a test set that played no part in the search (scikit-learn; Bergstra & Bengio, 2012). Logging every trial makes the search reproducible ([[experiment-tracking|experiment tracking]]).

### Key takeaway

Hyperparameter optimisation compares trained models across settings on validation data; random search beats grids because few hyperparameters matter, and Bayesian optimisation and Hyperband save further budget.

### Sources

- Bergstra, J. & Bengio, Y. (2012). *Random Search for Hyper-Parameter Optimization.* Journal of Machine Learning Research 13, 281–305. [jmlr.org](https://www.jmlr.org/papers/v13/bergstra12a.html)
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms.* NeurIPS 2012. [arXiv:1206.2944](https://arxiv.org/abs/1206.2944)
- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2018). *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization.* Journal of Machine Learning Research 18. [arXiv:1603.06560](https://arxiv.org/abs/1603.06560)
- Akiba, T., Sano, S., Yanase, T., Ohta, T. & Koyama, M. (2019). *Optuna: A Next-generation Hyperparameter Optimization Framework.* KDD 2019. [arXiv:1907.10902](https://arxiv.org/abs/1907.10902)
- scikit-learn developers. *Tuning the hyper-parameters of an estimator.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/grid_search.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Hyperparameter-Optimierung sucht die Einstellungen, die ein Lernverfahren nicht selbst lernt, etwa Lernrate, Regularisierungsstärke oder Baumtiefe, indem sie Modelle mit verschiedenen Einstellungen trainiert und auf Validierungsdaten vergleicht ([[scikit-learn|scikit-learn]]). Grid Search probiert jede Kombination vorgegebener Werte; Random Search zieht Kombinationen zufällig und ist effizienter, weil meist nur wenige Hyperparameter wichtig sind (Bergstra & Bengio, 2012). Bayes'sche Optimierung modelliert den Validierungs-Score als Funktion der Hyperparameter und wählt den nächsten Versuch dort, wo eine Verbesserung am wahrscheinlichsten ist (Snoek et al., 2012), und Hyperband und Successive Halving brechen schlechte Konfigurationen früh ab, um das Budget für vielversprechende einzusetzen (Li et al., 2018).

### Funktionsweise

```text
Suchraum festlegen (Bereiche oder Verteilungen pro Hyperparameter) + Budget
   ▼
Schleife:
    Konfiguration vorschlagen   Raster │ zufällig │ Bayes-Modell (GP, TPE) │ Bandit (Hyperband)
    Modell trainieren, auf Validierungs-Folds bewerten (Kreuzvalidierung)
    (optional) wenig aussichtsreiche Versuche früh abbrechen   ← Successive Halving / Pruning
   ▼
beste Konfiguration ──► auf allen Trainingsdaten neu anpassen ──► einmal auf zurückgehaltenen Testdaten bewerten
```

#### 1. Was gesucht wird

Eine Suche besteht aus einem Schätzer, einem Parameterraum, einem Verfahren zum Suchen oder Ziehen von Kandidaten, einem Kreuzvalidierungsschema und einer Score-Funktion (scikit-learn). Hyperparameter unterscheiden sich von Modellparametern, die das Training aus den Daten lernt ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]). Typischerweise hat eine kleine Teilmenge der Hyperparameter großen Einfluss auf die Leistung, während die übrigen auf ihren Voreinstellungen bleiben können (scikit-learn; Bergstra & Bengio, 2012).

#### 2. Grid Search

`GridSearchCV` bewertet alle Kombinationen vorgegebener Werte erschöpfend mit [[cross-validation|Kreuzvalidierung]] (scikit-learn). Der Aufwand wächst exponentiell mit der Zahl der Hyperparameter, und wenn nur einige davon wichtig sind, wiederholen die meisten Versuche dieselben Werte der wichtigen (Bergstra & Bengio, 2012).

#### 3. Random Search

Random Search zieht jede Konfiguration aus Verteilungen über die Hyperparameter. Bergstra und Bengio (2012) zeigten empirisch und theoretisch, dass dies effizienter ist als ein Raster: Die Funktion von den Hyperparametern zur Validierungsleistung hat eine geringe effektive Dimension, sodass zufällige Versuche die wichtigen Dimensionen mit mehr verschiedenen Werten abdecken. Gegenüber reiner Grid Search für [[neural-networks|neuronale Netze]] fand Random Search ebenso gute oder bessere Modelle in einem kleinen Bruchteil der Rechenzeit; bei Deep Belief Networks in einem 32-dimensionalen Raum erreichte es auf vier von sieben Datensätzen die Leistung einer sorgfältigen Kombination aus manueller Suche und Raster und übertraf sie auf einem (Bergstra & Bengio, 2012). In scikit-learn lässt `RandomizedSearchCV` das Budget unabhängig von der Zahl der Parameter wählen, und zusätzliche irrelevante Parameter verringern seine Effizienz nicht (scikit-learn).

#### 4. Bayes'sche Optimierung

Die Bayes'sche Optimierung behandelt den Validierungs-Score als Stichprobe aus einem Gauß-Prozess; dessen Posterior nutzt alle bisherigen Versuche, um die nächste Konfiguration zu wählen, etwa durch Maximieren der erwarteten Verbesserung (Snoek et al., 2012). Snoek et al. (2012) zeigten, dass die Wahl des Priors und des Inferenzverfahrens den Erfolg stark beeinflusst, ergänzten Verfahren, die die unterschiedliche Dauer von Experimenten und parallele Läufe berücksichtigen, und erreichten oder übertrafen das Tuning durch Fachleute für Latent Dirichlet Allocation, strukturierte SVMs und Convolutional Networks. Andere Frameworks nutzen statt eines Gauß-Prozesses einen Tree-structured Parzen Estimator (TPE) (Akiba et al., 2019).

#### 5. Frühes Abbrechen von Versuchen: Successive Halving und Hyperband

Successive Halving gibt vielen Konfigurationen ein Budget, bewertet sie, verwirft die schlechtere Hälfte und wiederholt mit mehr Ressourcen für die verbleibenden; die Ressource können Trainingsiterationen, Datenbeispiele oder Merkmale sein (Li et al., 2018; scikit-learn). Weil dafür die Zahl der Konfigurationen vorab gewählt werden muss, führt Hyperband Successive Halving mit mehreren Abwägungen zwischen vielen günstigen und wenigen teuren Versuchen aus; es brachte gegenüber Verfahren der Bayes'schen Optimierung bei Deep-Learning- und Kernel-Problemen mehr als eine Größenordnung Beschleunigung (Li et al., 2018). scikit-learn bietet `HalvingGridSearchCV` und `HalvingRandomSearchCV` an (scikit-learn), und Optuna verbindet die Suche mit dem Beschneiden wenig aussichtsreicher Versuche und einer Define-by-Run-API, die den Suchraum dynamisch aufbaut (Akiba et al., 2019).

#### Ursprung und Varianten

Grid Search und manuelle Suche waren lange die am weitesten verbreiteten Strategien (Bergstra & Bengio, 2012). Es folgten Random Search (Bergstra & Bengio, 2012), Bayes'sche Optimierung mit Gauß-Prozessen wie in Spearmint (Snoek et al., 2012; Akiba et al., 2019), Hyperband (Li et al., 2018) und Frameworks wie Optuna (Akiba et al., 2019).

### Wann einsetzen

- Bei jedem Modell mit Hyperparametern, deren gute Werte unbekannt sind, von Straftermen bei [[ridge-and-lasso|Ridge und Lasso]] bis zu Lernraten neuronaler Netze ([[gradient-descent|Gradientenabstieg]]).
- Grid Search für ein oder zwei Hyperparameter mit wenigen Werten; Random Search für mehr (Bergstra & Bengio, 2012).
- Bayes'sche Optimierung, wenn jeder Versuch teuer und die Zahl der Versuche klein ist (Snoek et al., 2012).
- Hyperband oder Successive Halving, wenn ein teilweises Training ein brauchbares frühes Signal liefert (Li et al., 2018).

### Stärken und Grenzen

**Stärken**
- Random Search ist einfach, parallelisierbar und robust gegenüber irrelevanten Hyperparametern (Bergstra & Bengio, 2012; scikit-learn).
- Modellbasierte Verfahren und frühes Abbrechen finden gute Einstellungen mit weit weniger vollständigen Trainings (Snoek et al., 2012; Li et al., 2018).

**Grenzen**
- Jeder Versuch trainiert ein Modell, sodass die Suche die Rechenkosten dominieren kann.
- Auf denselben Daten zu tunen, mit denen Ergebnisse berichtet werden, überschätzt die Leistung; scikit-learn empfiehlt verschachtelte Kreuzvalidierung, um ein Modell mit Grid Search zu bewerten (scikit-learn; [[cross-validation|Kreuzvalidierung]]).
- Die Bayes'sche Optimierung reagiert empfindlich auf ihre eigenen Modellierungsentscheidungen (Snoek et al., 2012).
- Frühes Abbrechen kann in die Irre führen, wenn Konfigurationen lange brauchen, bis sich ihre Qualität unterscheidet, etwa bei langsam konvergierendem Training; Hyperband sichert sich ab, indem es aggressive und vorsichtige Brackets mischt (Li et al., 2018).

### Vergleich

| Verfahren | Wie es Versuche wählt | Nutzt frühere Ergebnisse | Stärke |
|---|---|---|---|
| Grid Search | alle Kombinationen | nein | erschöpfend bei wenigen Parametern |
| Random Search | zufällige Stichproben | nein | effizient, parallel |
| Bayes'sche Optimierung | Ersatzmodell + Akquisitionsfunktion | ja | wenige teure Versuche |
| Successive Halving / Hyperband | viele günstige, wenige teure | ja (frühes Abbrechen) | große Beschleunigung |

Quellen: Bergstra & Bengio (2012), Snoek et al. (2012), Li et al. (2018).

### In der Praxis

Verteilungen auf sinnvollen Skalen festlegen, etwa log-gleichverteilt für Lernraten und Regularisierungsstärken, mit Random Search oder Successive Halving beginnen, die beste Konfiguration auf allen Trainingsdaten neu anpassen und einmal auf einer Testmenge bewerten, die an der Suche nicht beteiligt war (scikit-learn; Bergstra & Bengio, 2012). Jeden Versuch zu protokollieren macht die Suche reproduzierbar ([[experiment-tracking|Experiment Tracking]]).

### Merksatz

Die Hyperparameter-Optimierung vergleicht trainierte Modelle über Einstellungen hinweg auf Validierungsdaten; Random Search schlägt Raster, weil nur wenige Hyperparameter wichtig sind, und Bayes'sche Optimierung und Hyperband sparen weiteres Budget.

### Quellen

- Bergstra, J. & Bengio, Y. (2012). *Random Search for Hyper-Parameter Optimization.* Journal of Machine Learning Research 13, 281–305. [jmlr.org](https://www.jmlr.org/papers/v13/bergstra12a.html)
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms.* NeurIPS 2012. [arXiv:1206.2944](https://arxiv.org/abs/1206.2944)
- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2018). *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization.* Journal of Machine Learning Research 18. [arXiv:1603.06560](https://arxiv.org/abs/1603.06560)
- Akiba, T., Sano, S., Yanase, T., Ohta, T. & Koyama, M. (2019). *Optuna: A Next-generation Hyperparameter Optimization Framework.* KDD 2019. [arXiv:1907.10902](https://arxiv.org/abs/1907.10902)
- scikit-learn developers. *Tuning the hyper-parameters of an estimator.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/grid_search.html)
