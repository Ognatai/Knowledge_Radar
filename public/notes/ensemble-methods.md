---
title_en: Ensemble Methods
title_de: Ensemble-Methoden
entity_type: Method
sources:
- https://doi.org/10.1007/BF00058655
- https://doi.org/10.1023/A:1010933404324
- https://doi.org/10.1006/jcss.1997.1504
- https://doi.org/10.1214/aos/1013203451
- https://doi.org/10.1016/S0893-6080%2805%2980023-1
- https://arxiv.org/abs/1603.02754
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Ensemble methods combine several models into one predictor that is usually more accurate than each individual model. Bagging and random forests average models trained on bootstrap samples to reduce variance (Breiman, 1996; Breiman, 2001), boosting trains models one after another so that each corrects the errors of its predecessors (Freund & Schapire, 1997; Friedman, 2001), and stacking trains a higher-level model on the base models' predictions (Wolpert, 1992).

### How it works

Several base models are trained, either independently on resampled data (parallel strategy) or sequentially on data reweighted by the previous models' errors (sequential strategy). Their predictions are combined by averaging, voting or a second-level model.

```text
1. Bagging
▼
2. Random forests
▼
3. AdaBoost
▼
4. Gradient boosting
▼
5. Stacking
```

#### 1. Bagging

Bagging (bootstrap aggregating) trains multiple versions of a predictor on bootstrap replicates of the training set, i.e. samples drawn with replacement, and aggregates them by averaging for regression or by plurality vote for classification (Breiman, 1996). It improves accuracy most when the base method is unstable, meaning that small changes in the training data change the predictor substantially, as with [[decision-trees|Decision Trees]].

#### 2. Random forests

Random forests grow many decision trees, each on a bootstrap sample and considering only a random subset of features at each split, and aggregate them by voting or averaging (Breiman, 2001). Their generalisation error depends on the strength of the individual trees and the correlation between them; the random feature selection lowers this correlation.

#### 3. AdaBoost

AdaBoost (Freund & Schapire, 1997) trains weak learners sequentially. After each round, the examples that were misclassified receive higher weights, so that the next learner focuses on them, and the final classifier is a weighted vote of all weak learners. Unlike earlier boosting algorithms, it needs no prior knowledge of how accurate the weak learners are.

#### 4. Gradient boosting

Friedman (2001) views boosting as numerical optimisation in function space: an additive model is built stagewise, and each new component is fitted to the negative gradient of an arbitrary loss function, such as least squares, least absolute deviation, Huber or multiclass logistic loss. Gradient boosting of regression trees gives competitive and robust procedures for regression and classification. XGBoost (Chen & Guestrin, 2016) is a scalable tree boosting system with a sparsity-aware algorithm for sparse data and a weighted quantile sketch for approximate tree learning, which scales beyond billions of examples.

#### 5. Stacking

Stacked generalisation (Wolpert, 1992) combines several base learners by training a higher-level learner on their predictions, made on data that was not used to train them. The higher-level learner thus learns how to correct and combine the base learners' outputs.

#### Origin and variants

Stacking (Wolpert, 1992), bagging (Breiman, 1996) and AdaBoost (Freund & Schapire, 1997) introduced the main ensemble strategies. Random forests (Breiman, 2001) and gradient boosting (Friedman, 2001) became the standard tree ensembles, and XGBoost (Chen & Guestrin, 2016) made boosting scale to very large datasets.

### When to use it

- When a single model, such as a decision tree, is unstable and its predictions vary strongly with the data, bagging or random forests reduce this variance (Breiman, 1996; Breiman, 2001).
- When the highest accuracy on tabular data is needed, gradient-boosted trees are a strong choice ([[classical-machine-learning|Classical Machine Learning]]; Chen & Guestrin, 2016).
- When several different models are available, stacking can combine their strengths (Wolpert, 1992).

### Strengths and limitations

**Strengths**
- Bagging reduces the variance of unstable predictors (Breiman, 1996).
- Gradient boosting works with arbitrary differentiable losses for regression and classification (Friedman, 2001).
- Boosting systems such as XGBoost scale beyond billions of examples (Chen & Guestrin, 2016).

**Limitations**
- Bagging helps little if the base method is already stable (Breiman, 1996).
- Random forests only help as long as the trees are not too strongly correlated (Breiman, 2001).
- An ensemble of many models is harder to interpret than a single model ([[explainable-ai|Explainable AI]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Bagging | Independent models on bootstrap samples, averaged or voted (Breiman, 1996) | Unstable base models |
| Random forest | Bagging plus random feature subsets per split (Breiman, 2001) | Robust default for tabular data |
| AdaBoost | Sequential, reweights misclassified examples (Freund & Schapire, 1997) | Combining weak classifiers |
| Gradient boosting | Sequential fit to the negative gradient of a loss (Friedman, 2001; Chen & Guestrin, 2016) | High accuracy on tabular data |
| Stacking | Higher-level model learns from base predictions (Wolpert, 1992) | Combining heterogeneous models |

### In practice

Random forests work well with little tuning and provide out-of-bag error estimates (Breiman, 2001). Gradient boosting usually needs more tuning of learning rate, number and depth of trees, chosen with cross-validation ([[regularization-and-hyperparameters|Regularization and Hyperparameters]]). For stacking, the base predictions used to train the higher-level model must come from data the base models were not trained on (Wolpert, 1992).

### Key takeaway

Ensembles combine many models into one: averaging independent models reduces variance, sequential boosting reduces errors step by step, and stacking learns how to combine different models.

### Sources

- Breiman, L. (1996). *Bagging Predictors.* Machine Learning 24(2). [doi:10.1007/BF00058655](https://doi.org/10.1007/BF00058655)
- Breiman, L. (2001). *Random Forests.* Machine Learning 45(1). [doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
- Freund, Y. & Schapire, R. E. (1997). *A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting.* Journal of Computer and System Sciences 55(1). [doi:10.1006/jcss.1997.1504](https://doi.org/10.1006/jcss.1997.1504)
- Friedman, J. H. (2001). *Greedy Function Approximation: A Gradient Boosting Machine.* The Annals of Statistics 29(5). [doi:10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)
- Wolpert, D. H. (1992). *Stacked Generalization.* Neural Networks 5(2). [doi:10.1016/S0893-6080(05)80023-1](https://doi.org/10.1016/S0893-6080%2805%2980023-1)
- Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.* KDD 2016. [arXiv:1603.02754](https://arxiv.org/abs/1603.02754)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ensemble-Methoden kombinieren mehrere Modelle zu einem Prädiktor, der meist genauer ist als jedes einzelne Modell. Bagging und Random Forests mitteln Modelle, die auf Bootstrap-Stichproben trainiert wurden, und verringern so die Varianz (Breiman, 1996; Breiman, 2001); Boosting trainiert Modelle nacheinander, sodass jedes die Fehler seiner Vorgänger korrigiert (Freund & Schapire, 1997; Friedman, 2001); Stacking trainiert ein übergeordnetes Modell auf den Vorhersagen der Basismodelle (Wolpert, 1992).

### Funktionsweise

Mehrere Basismodelle werden trainiert, entweder unabhängig voneinander auf neu gezogenen Stichproben (parallele Strategie) oder nacheinander auf Daten, die nach den Fehlern der vorherigen Modelle gewichtet sind (sequenzielle Strategie). Ihre Vorhersagen werden durch Mittelung, Abstimmung oder ein Modell zweiter Stufe kombiniert.

```text
1. Bagging
▼
2. Random Forests
▼
3. AdaBoost
▼
4. Gradient Boosting
▼
5. Stacking
```

#### 1. Bagging

Bagging (Bootstrap Aggregating) trainiert mehrere Versionen eines Prädiktors auf Bootstrap-Replikaten der Trainingsmenge, also auf Stichproben mit Zurücklegen, und fasst sie bei Regression durch Mittelung und bei Klassifikation durch Mehrheitsentscheid zusammen (Breiman, 1996). Am meisten hilft es, wenn das Basisverfahren instabil ist, kleine Änderungen der Trainingsdaten den Prädiktor also stark verändern, wie bei [[decision-trees|Entscheidungsbäumen]].

#### 2. Random Forests

Random Forests lassen viele Entscheidungsbäume wachsen, jeden auf einer Bootstrap-Stichprobe und mit nur einer zufälligen Teilmenge der Merkmale an jeder Aufteilung, und fassen sie durch Abstimmung oder Mittelung zusammen (Breiman, 2001). Ihr Generalisierungsfehler hängt von der Stärke der einzelnen Bäume und ihrer Korrelation untereinander ab; die zufällige Merkmalsauswahl senkt diese Korrelation.

#### 3. AdaBoost

AdaBoost (Freund & Schapire, 1997) trainiert schwache Lerner nacheinander. Nach jeder Runde erhalten falsch klassifizierte Beispiele ein höheres Gewicht, sodass sich der nächste Lerner auf sie konzentriert, und der endgültige Klassifikator ist eine gewichtete Abstimmung aller schwachen Lerner. Anders als frühere Boosting-Algorithmen braucht er kein Vorwissen darüber, wie genau die schwachen Lerner sind.

#### 4. Gradient Boosting

Friedman (2001) versteht Boosting als numerische Optimierung im Funktionenraum: Ein additives Modell wird schrittweise aufgebaut, und jede neue Komponente wird an den negativen Gradienten einer beliebigen Verlustfunktion angepasst, etwa kleinste Quadrate, kleinste absolute Abweichung, Huber- oder multinomialer logistischer Verlust. Gradient Boosting mit Regressionsbäumen ergibt konkurrenzfähige und robuste Verfahren für Regression und Klassifikation. XGBoost (Chen & Guestrin, 2016) ist ein skalierbares System für Tree Boosting mit einem Algorithmus für dünnbesetzte Daten und einem gewichteten Quantile Sketch für approximatives Baumlernen, das über Milliarden von Beispielen hinaus skaliert.

#### 5. Stacking

Stacked Generalization (Wolpert, 1992) kombiniert mehrere Basislerner, indem ein übergeordneter Lerner auf ihren Vorhersagen trainiert wird, die auf Daten entstanden, mit denen die Basislerner nicht trainiert wurden. Der übergeordnete Lerner lernt so, die Ausgaben der Basislerner zu korrigieren und zu kombinieren.

#### Ursprung und Varianten

Stacking (Wolpert, 1992), Bagging (Breiman, 1996) und AdaBoost (Freund & Schapire, 1997) führten die wichtigsten Ensemble-Strategien ein. Random Forests (Breiman, 2001) und Gradient Boosting (Friedman, 2001) wurden zu den Standard-Baum-Ensembles, und XGBoost (Chen & Guestrin, 2016) machte Boosting für sehr große Datensätze skalierbar.

### Wann einsetzen

- Wenn ein einzelnes Modell wie ein Entscheidungsbaum instabil ist und seine Vorhersagen stark mit den Daten schwanken, verringern Bagging oder Random Forests diese Varianz (Breiman, 1996; Breiman, 2001).
- Wenn höchste Genauigkeit auf tabellarischen Daten gefragt ist, sind Gradient-Boosted Trees eine starke Wahl ([[classical-machine-learning|Klassische ML-Verfahren]]; Chen & Guestrin, 2016).
- Wenn mehrere unterschiedliche Modelle vorliegen, kann Stacking ihre Stärken verbinden (Wolpert, 1992).

### Stärken und Grenzen

**Stärken**
- Bagging verringert die Varianz instabiler Prädiktoren (Breiman, 1996).
- Gradient Boosting funktioniert mit beliebigen differenzierbaren Verlustfunktionen für Regression und Klassifikation (Friedman, 2001).
- Boosting-Systeme wie XGBoost skalieren über Milliarden von Beispielen hinaus (Chen & Guestrin, 2016).

**Einschränkungen**
- Bagging hilft wenig, wenn das Basisverfahren bereits stabil ist (Breiman, 1996).
- Random Forests helfen nur, solange die Bäume nicht zu stark korreliert sind (Breiman, 2001).
- Ein Ensemble aus vielen Modellen ist schwerer zu interpretieren als ein einzelnes Modell ([[explainable-ai|Erklärbare KI (XAI)]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Bagging | Unabhängige Modelle auf Bootstrap-Stichproben, gemittelt oder abgestimmt (Breiman, 1996) | Instabile Basismodelle |
| Random Forest | Bagging plus zufällige Merkmalsteilmengen je Aufteilung (Breiman, 2001) | Robuster Standard für Tabellendaten |
| AdaBoost | Sequenziell, gewichtet falsch klassifizierte Beispiele höher (Freund & Schapire, 1997) | Kombination schwacher Klassifikatoren |
| Gradient Boosting | Sequenzielle Anpassung an den negativen Gradienten eines Verlusts (Friedman, 2001; Chen & Guestrin, 2016) | Hohe Genauigkeit auf Tabellendaten |
| Stacking | Übergeordnetes Modell lernt aus den Basisvorhersagen (Wolpert, 1992) | Kombination unterschiedlicher Modelle |

### In der Praxis

Random Forests funktionieren mit wenig Tuning gut und liefern Out-of-Bag-Fehlerschätzungen (Breiman, 2001). Gradient Boosting braucht meist mehr Abstimmung von Lernrate, Anzahl und Tiefe der Bäume, die per Kreuzvalidierung gewählt werden ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]). Beim Stacking müssen die Basisvorhersagen, mit denen das übergeordnete Modell trainiert wird, aus Daten stammen, auf denen die Basismodelle nicht trainiert wurden (Wolpert, 1992).

### Merksatz

Ensembles kombinieren viele Modelle zu einem: Mitteln unabhängiger Modelle senkt die Varianz, sequenzielles Boosting verringert Fehler Schritt für Schritt, und Stacking lernt, unterschiedliche Modelle zu kombinieren.

### Quellen

- Breiman, L. (1996). *Bagging Predictors.* Machine Learning 24(2). [doi:10.1007/BF00058655](https://doi.org/10.1007/BF00058655)
- Breiman, L. (2001). *Random Forests.* Machine Learning 45(1). [doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
- Freund, Y. & Schapire, R. E. (1997). *A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting.* Journal of Computer and System Sciences 55(1). [doi:10.1006/jcss.1997.1504](https://doi.org/10.1006/jcss.1997.1504)
- Friedman, J. H. (2001). *Greedy Function Approximation: A Gradient Boosting Machine.* The Annals of Statistics 29(5). [doi:10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)
- Wolpert, D. H. (1992). *Stacked Generalization.* Neural Networks 5(2). [doi:10.1016/S0893-6080(05)80023-1](https://doi.org/10.1016/S0893-6080%2805%2980023-1)
- Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.* KDD 2016. [arXiv:1603.02754](https://arxiv.org/abs/1603.02754)
