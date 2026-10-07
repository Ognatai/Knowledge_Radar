---
title_en: Decision Trees
title_de: Entscheidungsbäume
entity_type: Method
sources:
- https://doi.org/10.1007/BF00116251
- https://hastie.su.domains/ElemStatLearn/
- https://doi.org/10.1023/A:1010933404324
- https://jmlr.org/papers/v12/pedregosa11a.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A decision tree predicts by passing an example through a sequence of tests on its features, from the root to a leaf that holds the prediction. Trees are grown top-down by repeatedly choosing the split that best separates the training examples (Quinlan, 1986) and then pruned to avoid overfitting (Hastie et al., 2009). They are easy to interpret but have high variance, which random forests reduce by combining many trees (Breiman, 2001).

### How it works

Starting with all training data at the root, the algorithm searches for the feature test that best separates the examples, splits the data accordingly and repeats this in each part. Each leaf predicts the majority class or the mean value of its examples.

```text
1. Top-down induction
▼
2. Recursive binary splitting (CART)
▼
3. Pruning
▼
4. Interpretability and variance
▼
5. Implementation
```

#### 1. Top-down induction

ID3 (Quinlan, 1986) builds a decision tree top-down: at each node it chooses the attribute that best splits the training examples according to an information-based criterion derived from entropy, and then continues with each subset. The paper also discusses how to handle noisy data and unknown attribute values.

#### 2. Recursive binary splitting (CART)

In the CART approach, the feature space is split recursively into two parts at a time (Hastie et al., 2009). For classification, the quality of a split is measured with a node impurity measure such as the Gini index or cross-entropy; for regression, with the squared error. The split that reduces impurity most is chosen.

#### 3. Pruning

A tree grown until its leaves are pure fits the training data too closely. CART therefore grows a large tree and prunes it back by cost-complexity pruning, which trades off tree size against fit; the pruning strength is chosen by cross-validation (Hastie et al., 2009).

#### 4. Interpretability and variance

Trees are interpretable, because each prediction can be traced as a path of simple tests. However, they have high variance: small changes in the training data can produce a very different tree (Hastie et al., 2009). Random forests reduce this variance by growing many trees on bootstrap samples, each considering a random subset of features at each split, and aggregating their predictions (Breiman, 2001; [[ensemble-methods|Ensemble Methods]]).

#### 5. Implementation

Decision trees and random forests are available in common libraries such as scikit-learn (Pedregosa et al., 2011).

#### Origin and variants

ID3 (Quinlan, 1986) and CART-style trees (Hastie et al., 2009) are the classical tree-building methods. Random forests (Breiman, 2001) and boosting build ensembles of trees, which are among the strongest methods for tabular data ([[classical-machine-learning|Classical Machine Learning]]).

### When to use it

- When the model must be explainable as a set of simple rules (Hastie et al., 2009).
- When a quick, interpretable baseline for tabular data is needed (Quinlan, 1986; Hastie et al., 2009).
- When higher accuracy is needed, as the base learner of a random forest or boosting ensemble (Breiman, 2001).

### Strengths and limitations

**Strengths**
- Interpretable: each prediction follows a path of simple tests (Hastie et al., 2009).
- Handles both classification and regression with the same procedure (Hastie et al., 2009).
- Serves as the base learner for powerful ensembles (Breiman, 2001).

**Limitations**
- High variance: small changes in the data can change the tree substantially (Hastie et al., 2009).
- Large trees overfit unless they are pruned (Hastie et al., 2009).
- A single tree is usually less accurate than an ensemble of trees (Breiman, 2001).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| ID3 | Top-down, entropy-based choice of attributes (Quinlan, 1986) | Categorical attributes, rule extraction |
| CART | Binary splits, Gini or squared error, cost-complexity pruning (Hastie et al., 2009) | Classification and regression |
| Random forest | Many trees on bootstrap samples with random feature subsets (Breiman, 2001) | Higher accuracy, lower variance |

### In practice

Tree depth and pruning strength are chosen by cross-validation (Hastie et al., 2009). If interpretability is the main goal, a small pruned tree is used; if accuracy matters more, an ensemble of trees is usually preferred (Breiman, 2001), and its decisions can be explained with dedicated methods ([[explainable-ai|Explainable AI]]).

### Key takeaway

Decision trees are interpretable models built from simple feature tests, but they vary strongly with the data, which is why they are usually pruned or combined into ensembles.

### Sources

- Quinlan, J. R. (1986). *Induction of Decision Trees.* Machine Learning 1(1). [doi:10.1007/BF00116251](https://doi.org/10.1007/BF00116251)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Breiman, L. (2001). *Random Forests.* Machine Learning 45(1). [doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Entscheidungsbaum trifft Vorhersagen, indem er ein Beispiel durch eine Folge von Tests auf seinen Merkmalen leitet, von der Wurzel bis zu einem Blatt, das die Vorhersage enthält. Bäume werden von oben nach unten aufgebaut, indem wiederholt die Aufteilung gewählt wird, die die Trainingsbeispiele am besten trennt (Quinlan, 1986), und anschließend beschnitten, um Überanpassung zu vermeiden (Hastie et al., 2009). Sie sind leicht zu interpretieren, haben aber eine hohe Varianz, die Random Forests durch die Kombination vieler Bäume verringern (Breiman, 2001).

### Funktionsweise

Ausgehend von allen Trainingsdaten an der Wurzel sucht der Algorithmus den Merkmalstest, der die Beispiele am besten trennt, teilt die Daten entsprechend auf und wiederholt das in jedem Teil. Jedes Blatt sagt die Mehrheitsklasse oder den Mittelwert seiner Beispiele voraus.

```text
1. Aufbau von oben nach unten
▼
2. Rekursive binäre Aufteilung (CART)
▼
3. Pruning
▼
4. Interpretierbarkeit und Varianz
▼
5. Implementierung
```

#### 1. Aufbau von oben nach unten

ID3 (Quinlan, 1986) baut einen Entscheidungsbaum von oben nach unten auf: An jedem Knoten wählt es das Attribut, das die Trainingsbeispiele nach einem informationsbasierten, aus der Entropie abgeleiteten Kriterium am besten trennt, und fährt dann mit jeder Teilmenge fort. Der Artikel behandelt auch den Umgang mit verrauschten Daten und unbekannten Attributwerten.

#### 2. Rekursive binäre Aufteilung (CART)

Beim CART-Ansatz wird der Merkmalsraum rekursiv in jeweils zwei Teile zerlegt (Hastie et al., 2009). Bei der Klassifikation wird die Güte einer Aufteilung mit einem Unreinheitsmaß wie dem Gini-Index oder der Kreuzentropie gemessen, bei der Regression mit dem quadratischen Fehler. Gewählt wird die Aufteilung, die die Unreinheit am stärksten verringert.

#### 3. Pruning

Ein Baum, der wächst, bis seine Blätter rein sind, passt sich den Trainingsdaten zu eng an. CART lässt daher einen großen Baum wachsen und beschneidet ihn per Cost-Complexity-Pruning, das Baumgröße gegen Anpassungsgüte abwägt; die Stärke des Prunings wird per Kreuzvalidierung bestimmt (Hastie et al., 2009).

#### 4. Interpretierbarkeit und Varianz

Bäume sind interpretierbar, weil sich jede Vorhersage als Pfad einfacher Tests nachvollziehen lässt. Sie haben aber eine hohe Varianz: Kleine Änderungen der Trainingsdaten können einen ganz anderen Baum ergeben (Hastie et al., 2009). Random Forests verringern diese Varianz, indem sie viele Bäume auf Bootstrap-Stichproben wachsen lassen, die an jeder Aufteilung nur eine zufällige Teilmenge der Merkmale berücksichtigen, und deren Vorhersagen zusammenführen (Breiman, 2001; [[ensemble-methods|Ensemble-Methoden]]).

#### 5. Implementierung

Entscheidungsbäume und Random Forests sind in gängigen Bibliotheken wie scikit-learn verfügbar (Pedregosa et al., 2011).

#### Ursprung und Varianten

ID3 (Quinlan, 1986) und Bäume nach dem CART-Ansatz (Hastie et al., 2009) sind die klassischen Verfahren zum Baumaufbau. Random Forests (Breiman, 2001) und Boosting bilden Ensembles aus Bäumen, die zu den stärksten Verfahren für tabellarische Daten gehören ([[classical-machine-learning|Klassische ML-Verfahren]]).

### Wann einsetzen

- Wenn das Modell als Menge einfacher Regeln erklärbar sein muss (Hastie et al., 2009).
- Wenn eine schnelle, interpretierbare Baseline für tabellarische Daten gebraucht wird (Quinlan, 1986; Hastie et al., 2009).
- Wenn höhere Genauigkeit nötig ist, als Basismodell eines Random Forest oder Boosting-Ensembles (Breiman, 2001).

### Stärken und Grenzen

**Stärken**
- Interpretierbar: Jede Vorhersage folgt einem Pfad einfacher Tests (Hastie et al., 2009).
- Klassifikation und Regression mit demselben Verfahren (Hastie et al., 2009).
- Dient als Basismodell leistungsfähiger Ensembles (Breiman, 2001).

**Einschränkungen**
- Hohe Varianz: Kleine Änderungen der Daten können den Baum stark verändern (Hastie et al., 2009).
- Große Bäume überanpassen, wenn sie nicht beschnitten werden (Hastie et al., 2009).
- Ein einzelner Baum ist meist ungenauer als ein Ensemble aus Bäumen (Breiman, 2001).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| ID3 | Aufbau von oben nach unten, entropiebasierte Attributwahl (Quinlan, 1986) | Kategoriale Attribute, Regelextraktion |
| CART | Binäre Aufteilungen, Gini oder quadratischer Fehler, Cost-Complexity-Pruning (Hastie et al., 2009) | Klassifikation und Regression |
| Random Forest | Viele Bäume auf Bootstrap-Stichproben mit zufälligen Merkmalsteilmengen (Breiman, 2001) | Höhere Genauigkeit, geringere Varianz |

### In der Praxis

Baumtiefe und Pruning-Stärke werden per Kreuzvalidierung gewählt (Hastie et al., 2009). Steht die Interpretierbarkeit im Vordergrund, wird ein kleiner beschnittener Baum verwendet; zählt die Genauigkeit mehr, wird meist ein Baum-Ensemble bevorzugt (Breiman, 2001), dessen Entscheidungen sich mit eigenen Verfahren erklären lassen ([[explainable-ai|Erklärbare KI (XAI)]]).

### Merksatz

Entscheidungsbäume sind interpretierbare Modelle aus einfachen Merkmalstests, schwanken aber stark mit den Daten und werden deshalb meist beschnitten oder zu Ensembles kombiniert.

### Quellen

- Quinlan, J. R. (1986). *Induction of Decision Trees.* Machine Learning 1(1). [doi:10.1007/BF00116251](https://doi.org/10.1007/BF00116251)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Breiman, L. (2001). *Random Forests.* Machine Learning 45(1). [doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
