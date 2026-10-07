---
title_en: Support Vector Machines
title_de: Support Vector Machines
entity_type: Method
sources:
- https://doi.org/10.1145/130385.130401
- https://doi.org/10.1007/BF00994018
- https://doi.org/10.1023/B:STCO.0000035301.49549.88
- https://hastie.su.domains/ElemStatLearn/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A support vector machine (SVM) classifies by finding the decision boundary with the largest margin to the nearest training points, the support vectors (Boser et al., 1992). A soft margin tolerates some training errors, and kernels make non-linear boundaries possible by working implicitly in a high-dimensional feature space (Cortes & Vapnik, 1995). The same ideas yield support vector regression (Smola & Schölkopf, 2004).

### How it works

Training solves an optimisation problem that places the boundary as far as possible from the closest examples of each class, while penalising points on the wrong side. Only these closest examples determine the boundary.

```text
1. Maximum margin
▼
2. Soft margin
▼
3. Kernel trick
▼
4. Support vector regression
```

#### 1. Maximum margin

Boser et al. (1992) presented a training algorithm that maximises the margin between the training patterns and the decision boundary. The solution is a linear combination of supporting patterns, the subset of training patterns closest to the boundary; all other training points do not influence it. The algorithm applies to a wide variety of classification functions, including perceptrons, polynomials and radial basis functions, and generalised well on optical character recognition.

#### 2. Soft margin

Real data is rarely perfectly separable. Cortes & Vapnik (1995) extended the method to non-separable training data with a soft margin, which allows training errors at a cost. The cost parameter C controls the trade-off between a wide margin and few training errors, and the approach corresponds to fitting a regularised hinge loss (Hastie et al., 2009; [[regularization-and-hyperparameters|Regularization and Hyperparameters]]).

#### 3. Kernel trick

Support-vector networks map the inputs non-linearly into a high-dimensional feature space and construct a linear decision surface there (Cortes & Vapnik, 1995). Kernels such as polynomial or radial basis kernels compute the required inner products in this enlarged space without constructing it explicitly, so non-linear boundaries can be learned at moderate cost (Hastie et al., 2009).

#### 4. Support vector regression

Support vector regression uses an epsilon-insensitive loss that ignores errors smaller than epsilon and keeps the function as flat as possible (Smola & Schölkopf, 2004). The problem is solved as a quadratic programme, and kernels again allow non-linear regression.

#### Origin and variants

Optimal margin classifiers (Boser et al., 1992) were extended to support-vector networks with soft margin and non-linear feature mappings (Cortes & Vapnik, 1995). Support vector regression (Smola & Schölkopf, 2004) carries the approach over to continuous targets.

### When to use it

- When a classifier with good generalisation is needed on data of moderate size, for example in character recognition (Boser et al., 1992; Cortes & Vapnik, 1995).
- When the boundary between classes is non-linear, kernels make SVMs flexible (Cortes & Vapnik, 1995).
- When a continuous target should be predicted with tolerance for small errors, support vector regression applies (Smola & Schölkopf, 2004).

### Strengths and limitations

**Strengths**
- The boundary depends only on the support vectors (Boser et al., 1992).
- Kernels allow non-linear boundaries without explicit feature construction (Hastie et al., 2009).
- The soft margin handles overlapping classes (Cortes & Vapnik, 1995).

**Limitations**
- The cost parameter C and the kernel must be chosen, usually by cross-validation (Hastie et al., 2009).
- SVMs output decision scores rather than probabilities; if probabilities are needed, they have to be calibrated separately ([[classification|Classification]]).
- The optimisation is a quadratic programme, which becomes expensive for very large datasets (Smola & Schölkopf, 2004).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Hard-margin SVM | Maximal margin, no training errors allowed (Boser et al., 1992) | Separable data |
| Soft-margin SVM | Training errors allowed at cost C (Cortes & Vapnik, 1995) | Overlapping classes |
| Kernel SVM | Linear boundary in an implicit feature space (Cortes & Vapnik, 1995; Hastie et al., 2009) | Non-linear class boundaries |
| Support vector regression | Epsilon-insensitive loss, flat function (Smola & Schölkopf, 2004) | Regression with tolerance |

### In practice

Features should be on comparable scales, since the margin is measured in feature space ([[ml-preprocessing|ML Preprocessing]]). C and the kernel parameters are tuned with cross-validation (Hastie et al., 2009). For large tabular datasets, tree ensembles are often the stronger and faster choice ([[ensemble-methods|Ensemble Methods]]).

### Key takeaway

An SVM places the decision boundary with maximal margin to the closest training points, tolerates errors through a soft margin and handles non-linear problems with kernels.

### Sources

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). *A Training Algorithm for Optimal Margin Classifiers.* COLT 1992. [doi:10.1145/130385.130401](https://doi.org/10.1145/130385.130401)
- Cortes, C. & Vapnik, V. (1995). *Support-Vector Networks.* Machine Learning 20(3). [doi:10.1007/BF00994018](https://doi.org/10.1007/BF00994018)
- Smola, A. J. & Schölkopf, B. (2004). *A Tutorial on Support Vector Regression.* Statistics and Computing 14(3). [doi:10.1023/B:STCO.0000035301.49549.88](https://doi.org/10.1023/B:STCO.0000035301.49549.88)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine Support Vector Machine (SVM) klassifiziert, indem sie die Entscheidungsgrenze mit dem größten Abstand (Margin) zu den nächstgelegenen Trainingspunkten findet, den Stützvektoren (Boser et al., 1992). Ein Soft Margin toleriert einige Trainingsfehler, und Kernel ermöglichen nichtlineare Grenzen, indem sie implizit in einem hochdimensionalen Merkmalsraum arbeiten (Cortes & Vapnik, 1995). Dieselben Ideen führen zur Support Vector Regression (Smola & Schölkopf, 2004).

### Funktionsweise

Das Training löst ein Optimierungsproblem, das die Grenze möglichst weit von den nächstgelegenen Beispielen jeder Klasse entfernt platziert und Punkte auf der falschen Seite bestraft. Nur diese nächstgelegenen Beispiele bestimmen die Grenze.

```text
1. Maximaler Margin
▼
2. Soft Margin
▼
3. Kernel-Trick
▼
4. Support Vector Regression
```

#### 1. Maximaler Margin

Boser et al. (1992) stellten einen Trainingsalgorithmus vor, der den Abstand zwischen den Trainingsmustern und der Entscheidungsgrenze maximiert. Die Lösung ist eine Linearkombination der Stützmuster, also der Trainingsmuster, die der Grenze am nächsten liegen; alle anderen Trainingspunkte beeinflussen sie nicht. Der Algorithmus lässt sich auf viele Klassifikationsfunktionen anwenden, darunter Perzeptrons, Polynome und radiale Basisfunktionen, und generalisierte bei der optischen Zeichenerkennung gut.

#### 2. Soft Margin

Echte Daten sind selten perfekt trennbar. Cortes & Vapnik (1995) erweiterten das Verfahren mit einem Soft Margin auf nicht trennbare Trainingsdaten, der Trainingsfehler gegen Kosten zulässt. Der Kostenparameter C steuert die Abwägung zwischen breitem Margin und wenigen Trainingsfehlern, und der Ansatz entspricht der Anpassung eines regularisierten Hinge-Loss (Hastie et al., 2009; [[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]).

#### 3. Kernel-Trick

Support-Vector-Netzwerke bilden die Eingaben nichtlinear in einen hochdimensionalen Merkmalsraum ab und konstruieren dort eine lineare Entscheidungsfläche (Cortes & Vapnik, 1995). Kernel wie polynomiale oder radiale Basisfunktions-Kernel berechnen die nötigen Skalarprodukte in diesem erweiterten Raum, ohne ihn explizit zu konstruieren; so lassen sich nichtlineare Grenzen mit moderatem Aufwand lernen (Hastie et al., 2009).

#### 4. Support Vector Regression

Die Support Vector Regression verwendet eine epsilon-insensitive Verlustfunktion, die Fehler unter epsilon ignoriert, und hält die Funktion so flach wie möglich (Smola & Schölkopf, 2004). Das Problem wird als quadratisches Programm gelöst, und Kernel ermöglichen auch hier nichtlineare Regression.

#### Ursprung und Varianten

Klassifikatoren mit optimalem Margin (Boser et al., 1992) wurden zu Support-Vector-Netzwerken mit Soft Margin und nichtlinearen Merkmalsabbildungen erweitert (Cortes & Vapnik, 1995). Die Support Vector Regression (Smola & Schölkopf, 2004) überträgt den Ansatz auf stetige Zielgrößen.

### Wann einsetzen

- Wenn ein gut generalisierender Klassifikator für Daten mittlerer Größe gebraucht wird, etwa bei der Zeichenerkennung (Boser et al., 1992; Cortes & Vapnik, 1995).
- Wenn die Grenze zwischen den Klassen nichtlinear ist, machen Kernel SVMs flexibel (Cortes & Vapnik, 1995).
- Wenn eine stetige Zielgröße mit Toleranz für kleine Fehler vorhergesagt werden soll, passt die Support Vector Regression (Smola & Schölkopf, 2004).

### Stärken und Grenzen

**Stärken**
- Die Grenze hängt nur von den Stützvektoren ab (Boser et al., 1992).
- Kernel ermöglichen nichtlineare Grenzen ohne explizite Merkmalskonstruktion (Hastie et al., 2009).
- Der Soft Margin kommt mit überlappenden Klassen zurecht (Cortes & Vapnik, 1995).

**Einschränkungen**
- Kostenparameter C und Kernel müssen gewählt werden, meist per Kreuzvalidierung (Hastie et al., 2009).
- SVMs liefern Entscheidungswerte statt Wahrscheinlichkeiten; werden Wahrscheinlichkeiten gebraucht, müssen sie gesondert kalibriert werden ([[classification|Klassifikation]]).
- Die Optimierung ist ein quadratisches Programm und wird bei sehr großen Datensätzen aufwendig (Smola & Schölkopf, 2004).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| SVM mit Hard Margin | Maximaler Margin, keine Trainingsfehler zulässig (Boser et al., 1992) | Trennbare Daten |
| SVM mit Soft Margin | Trainingsfehler gegen Kosten C zulässig (Cortes & Vapnik, 1995) | Überlappende Klassen |
| Kernel-SVM | Lineare Grenze in einem impliziten Merkmalsraum (Cortes & Vapnik, 1995; Hastie et al., 2009) | Nichtlineare Klassengrenzen |
| Support Vector Regression | Epsilon-insensitiver Verlust, flache Funktion (Smola & Schölkopf, 2004) | Regression mit Toleranz |

### In der Praxis

Merkmale sollten auf vergleichbaren Skalen liegen, da der Margin im Merkmalsraum gemessen wird ([[ml-preprocessing|Preprocessing für Machine Learning]]). C und die Kernel-Parameter werden per Kreuzvalidierung abgestimmt (Hastie et al., 2009). Bei großen tabellarischen Datensätzen sind Baum-Ensembles oft die stärkere und schnellere Wahl ([[ensemble-methods|Ensemble-Methoden]]).

### Merksatz

Eine SVM legt die Entscheidungsgrenze mit maximalem Abstand zu den nächstgelegenen Trainingspunkten, toleriert Fehler über einen Soft Margin und löst nichtlineare Probleme mit Kerneln.

### Quellen

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). *A Training Algorithm for Optimal Margin Classifiers.* COLT 1992. [doi:10.1145/130385.130401](https://doi.org/10.1145/130385.130401)
- Cortes, C. & Vapnik, V. (1995). *Support-Vector Networks.* Machine Learning 20(3). [doi:10.1007/BF00994018](https://doi.org/10.1007/BF00994018)
- Smola, A. J. & Schölkopf, B. (2004). *A Tutorial on Support Vector Regression.* Statistics and Computing 14(3). [doi:10.1023/B:STCO.0000035301.49549.88](https://doi.org/10.1023/B:STCO.0000035301.49549.88)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
