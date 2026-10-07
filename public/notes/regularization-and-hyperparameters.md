---
title_en: Regularization and Hyperparameters
title_de: Regularisierung und Hyperparameter
entity_type: Method
sources:
- https://doi.org/10.1080/00401706.1970.10488634
- https://doi.org/10.1111/j.2517-6161.1996.tb02080.x
- https://jmlr.org/papers/v15/srivastava14a.html
- https://doi.org/10.1007/3-540-49430-8_3
- https://jmlr.org/papers/v13/bergstra12a.html
- https://arxiv.org/abs/1206.2944
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Regularisation reduces overfitting by constraining a model, for example with an L2 penalty (ridge regression, Hoerl & Kennard, 1970), an L1 penalty (lasso, Tibshirani, 1996), dropout (Srivastava et al., 2014) or early stopping (Prechelt, 1998). Hyperparameters such as the penalty strength are not learned from the training data but chosen by search on validation data, where random search (Bergstra & Bengio, 2012) and Bayesian optimisation (Snoek et al., 2012) are more efficient than trying a grid.

### How it works

A model is trained with a constraint or penalty that discourages overly complex solutions. The strength of this constraint and other settings are hyperparameters, chosen by training several configurations and comparing them on validation data.

```text
1. Parameters and hyperparameters
▼
2. L2 regularisation (ridge)
▼
3. L1 regularisation (lasso)
▼
4. Dropout
▼
5. Early stopping
▼
6. Hyperparameter search
```

#### 1. Parameters and hyperparameters

Parameters, such as the weights of a model, are learned from the training data. Hyperparameters, such as regularisation terms and optimisation settings, are set before training and must be tuned; this tuning is often a "black art" requiring expert experience, unwritten rules of thumb or brute-force search (Snoek et al., 2012).

#### 2. L2 regularisation (ridge)

Least-squares estimates have a high probability of being unsatisfactory when the predictors are not orthogonal, i.e. correlated (Hoerl & Kennard, 1970). Ridge regression adds small positive quantities to the diagonal of X′X, which gives biased estimates with a smaller mean squared error; the ridge trace shows how the estimates change with the penalty. Equivalently, large coefficients are penalised by their squared size.

#### 3. L1 regularisation (lasso)

The lasso minimises the residual sum of squares subject to the sum of the absolute values of the coefficients being below a constant (Tibshirani, 1996). Because of this constraint, some coefficients become exactly zero, which yields interpretable models like subset selection while keeping the stability of ridge regression.

#### 4. Dropout

Dropout randomly drops units, together with their connections, from a neural network during training, which prevents units from co-adapting too much (Srivastava et al., 2014). At test time, a single network with scaled-down weights approximates the average of the many thinned networks seen during training. Dropout reduced overfitting and improved results on benchmarks in vision, speech recognition, document classification and computational biology ([[neural-network-training|Neural Network Training]]).

#### 5. Early stopping

Early stopping ends training when the error on a validation set starts to increase, before the model overfits (Prechelt, 1998). Comparing stopping criteria empirically, Prechelt found that slower criteria, which stop later, give slightly better generalisation at the cost of considerably longer training.

#### 6. Hyperparameter search

Bergstra & Bengio (2012) showed empirically and theoretically that randomly chosen trials are more efficient for hyperparameter optimisation than trials on a grid, because for most datasets only a few hyperparameters really matter, and random search tries more distinct values of these. Bayesian optimisation models the generalisation performance as a sample from a Gaussian process and uses the results of previous trials to choose the next setting; with careful choices, it exceeded expert-level tuning (Snoek et al., 2012).

#### Origin and variants

Ridge regression (Hoerl & Kennard, 1970) and the lasso (Tibshirani, 1996) come from statistics; early stopping criteria (Prechelt, 1998) and dropout (Srivastava et al., 2014) from neural network training. Random search (Bergstra & Bengio, 2012) and Bayesian optimisation (Snoek et al., 2012) made hyperparameter tuning more systematic.

### When to use it

- When a model fits the training data much better than validation data, regularisation is needed (Prechelt, 1998).
- When only a few of many features are expected to matter, the lasso selects them (Tibshirani, 1996).
- When predictors are strongly correlated, ridge regression stabilises the estimates (Hoerl & Kennard, 1970).
- When several hyperparameters must be tuned, random search or Bayesian optimisation is more efficient than a grid (Bergstra & Bengio, 2012; Snoek et al., 2012).

### Strengths and limitations

**Strengths**
- Ridge reduces mean squared error when predictors are correlated (Hoerl & Kennard, 1970).
- The lasso produces sparse, interpretable models (Tibshirani, 1996).
- Random search finds good settings with fewer trials than grid search (Bergstra & Bengio, 2012).

**Limitations**
- Regularisation introduces bias in the estimates (Hoerl & Kennard, 1970).
- Early stopping trades better generalisation against longer training, depending on the criterion (Prechelt, 1998).
- Bayesian optimisation depends on choices of the Gaussian process prior and inference procedure (Snoek et al., 2012).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| L2 (ridge) | Shrinks all coefficients; none become zero (Hoerl & Kennard, 1970) | Correlated predictors |
| L1 (lasso) | Sets some coefficients exactly to zero (Tibshirani, 1996) | Feature selection, sparse models |
| Dropout | Randomly removes units during training (Srivastava et al., 2014) | Neural networks |
| Early stopping | Stops when validation error rises (Prechelt, 1998) | Iteratively trained models |
| Random search / Bayesian optimisation | Random or model-guided choice of trials (Bergstra & Bengio, 2012; Snoek et al., 2012) | Tuning several hyperparameters |

### In practice

Hyperparameters are tuned with cross-validation or a separate validation set, and the test set is used only for the final evaluation ([[ml-preprocessing|ML Preprocessing]]). Logging all tried configurations and their results makes tuning reproducible ([[experiment-tracking|Experiment Tracking]]).

### Key takeaway

Regularisation constrains models to generalise better, and its strength, like other hyperparameters, is chosen on validation data, preferably with random search or Bayesian optimisation rather than a grid.

### Sources

- Hoerl, A. E. & Kennard, R. W. (1970). *Ridge Regression: Biased Estimation for Nonorthogonal Problems.* Technometrics 12(1). [doi:10.1080/00401706.1970.10488634](https://doi.org/10.1080/00401706.1970.10488634)
- Tibshirani, R. (1996). *Regression Shrinkage and Selection via the Lasso.* Journal of the Royal Statistical Society, Series B 58(1). [doi:10.1111/j.2517-6161.1996.tb02080.x](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x)
- Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I. & Salakhutdinov, R. (2014). *Dropout: A Simple Way to Prevent Neural Networks from Overfitting.* JMLR 15. [JMLR](https://jmlr.org/papers/v15/srivastava14a.html)
- Prechelt, L. (1998). *Early Stopping - But When?* In Neural Networks: Tricks of the Trade, LNCS 1524. [doi:10.1007/3-540-49430-8_3](https://doi.org/10.1007/3-540-49430-8_3)
- Bergstra, J. & Bengio, Y. (2012). *Random Search for Hyper-Parameter Optimization.* JMLR 13. [JMLR](https://jmlr.org/papers/v13/bergstra12a.html)
- Snoek, J. et al. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms.* NeurIPS 2012. [arXiv:1206.2944](https://arxiv.org/abs/1206.2944)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Regularisierung verringert Überanpassung, indem sie ein Modell einschränkt, etwa mit einem L2-Strafterm (Ridge-Regression, Hoerl & Kennard, 1970), einem L1-Strafterm (Lasso, Tibshirani, 1996), Dropout (Srivastava et al., 2014) oder Early Stopping (Prechelt, 1998). Hyperparameter wie die Stärke des Strafterms werden nicht aus den Trainingsdaten gelernt, sondern durch Suche auf Validierungsdaten gewählt; Random Search (Bergstra & Bengio, 2012) und Bayes'sche Optimierung (Snoek et al., 2012) sind dabei effizienter als ein Raster.

### Funktionsweise

Ein Modell wird mit einer Einschränkung oder einem Strafterm trainiert, der übermäßig komplexe Lösungen erschwert. Die Stärke dieser Einschränkung und weitere Einstellungen sind Hyperparameter, die gewählt werden, indem mehrere Konfigurationen trainiert und auf Validierungsdaten verglichen werden.

```text
1. Parameter und Hyperparameter
▼
2. L2-Regularisierung (Ridge)
▼
3. L1-Regularisierung (Lasso)
▼
4. Dropout
▼
5. Early Stopping
▼
6. Hyperparametersuche
```

#### 1. Parameter und Hyperparameter

Parameter wie die Gewichte eines Modells werden aus den Trainingsdaten gelernt. Hyperparameter wie Regularisierungsterme und Optimierungseinstellungen werden vor dem Training festgelegt und müssen abgestimmt werden; dieses Tuning ist oft eine „schwarze Kunst“, die Expertenerfahrung, ungeschriebene Faustregeln oder Brute-Force-Suche erfordert (Snoek et al., 2012).

#### 2. L2-Regularisierung (Ridge)

Kleinste-Quadrate-Schätzer sind mit hoher Wahrscheinlichkeit unbefriedigend, wenn die Prädiktoren nicht orthogonal, also korreliert sind (Hoerl & Kennard, 1970). Die Ridge-Regression addiert kleine positive Werte zur Diagonale von X′X und erhält so verzerrte Schätzer mit kleinerem mittlerem quadratischem Fehler; der Ridge Trace zeigt, wie sich die Schätzer mit dem Strafterm verändern. Gleichbedeutend werden große Koeffizienten nach ihrer quadrierten Größe bestraft.

#### 3. L1-Regularisierung (Lasso)

Das Lasso minimiert die Residuenquadratsumme unter der Nebenbedingung, dass die Summe der Absolutbeträge der Koeffizienten unter einer Konstanten bleibt (Tibshirani, 1996). Wegen dieser Nebenbedingung werden manche Koeffizienten exakt null; so entstehen interpretierbare Modelle wie bei der Teilmengenauswahl, bei gleichzeitiger Stabilität der Ridge-Regression.

#### 4. Dropout

Dropout entfernt während des Trainings zufällig Einheiten samt ihrer Verbindungen aus einem neuronalen Netz und verhindert so, dass sich Einheiten zu stark aufeinander einstellen (Srivastava et al., 2014). Zur Testzeit nähert ein einzelnes Netz mit herunterskalierten Gewichten den Mittelwert der vielen ausgedünnten Netze aus dem Training an. Dropout verringerte Überanpassung und verbesserte Ergebnisse auf Benchmarks in Bildverarbeitung, Spracherkennung, Dokumentklassifikation und Bioinformatik ([[neural-network-training|Training neuronaler Netze]]).

#### 5. Early Stopping

Early Stopping beendet das Training, sobald der Fehler auf einer Validierungsmenge zu steigen beginnt, bevor das Modell überanpasst (Prechelt, 1998). Prechelt verglich Abbruchkriterien empirisch und fand, dass langsamere Kriterien, die später abbrechen, etwas bessere Generalisierung bringen, um den Preis deutlich längeren Trainings.

#### 6. Hyperparametersuche

Bergstra & Bengio (2012) zeigten empirisch und theoretisch, dass zufällig gewählte Versuche für die Hyperparameteroptimierung effizienter sind als Versuche auf einem Raster, weil bei den meisten Datensätzen nur wenige Hyperparameter wirklich zählen und Random Search mehr unterschiedliche Werte dieser wichtigen Hyperparameter ausprobiert. Bayes'sche Optimierung modelliert die Generalisierungsleistung als Stichprobe aus einem Gauß-Prozess und nutzt die Ergebnisse früherer Versuche, um die nächste Einstellung zu wählen; bei sorgfältiger Wahl übertraf sie das Tuning durch Fachleute (Snoek et al., 2012).

#### Ursprung und Varianten

Ridge-Regression (Hoerl & Kennard, 1970) und Lasso (Tibshirani, 1996) stammen aus der Statistik, Abbruchkriterien für Early Stopping (Prechelt, 1998) und Dropout (Srivastava et al., 2014) aus dem Training neuronaler Netze. Random Search (Bergstra & Bengio, 2012) und Bayes'sche Optimierung (Snoek et al., 2012) machten das Hyperparameter-Tuning systematischer.

### Wann einsetzen

- Wenn ein Modell die Trainingsdaten deutlich besser abbildet als die Validierungsdaten, ist Regularisierung nötig (Prechelt, 1998).
- Wenn von vielen Merkmalen nur wenige relevant sein dürften, wählt das Lasso sie aus (Tibshirani, 1996).
- Wenn Prädiktoren stark korreliert sind, stabilisiert die Ridge-Regression die Schätzer (Hoerl & Kennard, 1970).
- Wenn mehrere Hyperparameter abgestimmt werden müssen, sind Random Search oder Bayes'sche Optimierung effizienter als ein Raster (Bergstra & Bengio, 2012; Snoek et al., 2012).

### Stärken und Grenzen

**Stärken**
- Ridge verringert den mittleren quadratischen Fehler bei korrelierten Prädiktoren (Hoerl & Kennard, 1970).
- Das Lasso erzeugt dünnbesetzte, interpretierbare Modelle (Tibshirani, 1996).
- Random Search findet gute Einstellungen mit weniger Versuchen als eine Rastersuche (Bergstra & Bengio, 2012).

**Einschränkungen**
- Regularisierung führt eine Verzerrung (Bias) in die Schätzer ein (Hoerl & Kennard, 1970).
- Early Stopping wägt je nach Kriterium bessere Generalisierung gegen längeres Training ab (Prechelt, 1998).
- Bayes'sche Optimierung hängt von der Wahl des Gauß-Prozess-Priors und des Inferenzverfahrens ab (Snoek et al., 2012).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| L2 (Ridge) | Schrumpft alle Koeffizienten; keiner wird null (Hoerl & Kennard, 1970) | Korrelierte Prädiktoren |
| L1 (Lasso) | Setzt manche Koeffizienten exakt auf null (Tibshirani, 1996) | Merkmalsauswahl, dünnbesetzte Modelle |
| Dropout | Entfernt während des Trainings zufällig Einheiten (Srivastava et al., 2014) | Neuronale Netze |
| Early Stopping | Bricht ab, wenn der Validierungsfehler steigt (Prechelt, 1998) | Iterativ trainierte Modelle |
| Random Search / Bayes'sche Optimierung | Zufällige oder modellgesteuerte Wahl der Versuche (Bergstra & Bengio, 2012; Snoek et al., 2012) | Abstimmung mehrerer Hyperparameter |

### In der Praxis

Hyperparameter werden per Kreuzvalidierung oder auf einer separaten Validierungsmenge abgestimmt, und die Testmenge dient nur der abschließenden Evaluation ([[ml-preprocessing|Preprocessing für Machine Learning]]). Wer alle ausprobierten Konfigurationen und ihre Ergebnisse protokolliert, macht das Tuning reproduzierbar ([[experiment-tracking|Experiment Tracking]]).

### Merksatz

Regularisierung schränkt Modelle ein, damit sie besser generalisieren, und ihre Stärke wird wie andere Hyperparameter auf Validierungsdaten gewählt, am besten mit Random Search oder Bayes'scher Optimierung statt mit einem Raster.

### Quellen

- Hoerl, A. E. & Kennard, R. W. (1970). *Ridge Regression: Biased Estimation for Nonorthogonal Problems.* Technometrics 12(1). [doi:10.1080/00401706.1970.10488634](https://doi.org/10.1080/00401706.1970.10488634)
- Tibshirani, R. (1996). *Regression Shrinkage and Selection via the Lasso.* Journal of the Royal Statistical Society, Series B 58(1). [doi:10.1111/j.2517-6161.1996.tb02080.x](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x)
- Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I. & Salakhutdinov, R. (2014). *Dropout: A Simple Way to Prevent Neural Networks from Overfitting.* JMLR 15. [JMLR](https://jmlr.org/papers/v15/srivastava14a.html)
- Prechelt, L. (1998). *Early Stopping - But When?* In Neural Networks: Tricks of the Trade, LNCS 1524. [doi:10.1007/3-540-49430-8_3](https://doi.org/10.1007/3-540-49430-8_3)
- Bergstra, J. & Bengio, Y. (2012). *Random Search for Hyper-Parameter Optimization.* JMLR 13. [JMLR](https://jmlr.org/papers/v13/bergstra12a.html)
- Snoek, J. et al. (2012). *Practical Bayesian Optimization of Machine Learning Algorithms.* NeurIPS 2012. [arXiv:1206.2944](https://arxiv.org/abs/1206.2944)
