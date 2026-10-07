---
title_en: k-Nearest Neighbors
title_de: k-Nearest Neighbors
entity_type: Method
sources:
- https://doi.org/10.1109/TIT.1967.1053964
- https://doi.org/10.1007/3-540-49257-7_15
- https://hastie.su.domains/ElemStatLearn/
- https://jmlr.org/papers/v12/pedregosa11a.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

k-nearest neighbours (k-NN) predicts for a new point by looking at the k closest training points and taking a majority vote for classification or an average for regression (Hastie et al., 2009). It needs no training beyond storing the data, and even the simplest version has an error of at most twice the Bayes error in large samples (Cover & Hart, 1967). Its results depend on feature scaling and the choice of k, and nearest neighbours become less meaningful in high dimensions (Beyer et al., 1999).

### How it works

The training data is stored. For a new point, the distances to all stored points are computed, the k closest are selected, and their labels or values are aggregated.

```text
1. Nearest neighbour rule
▼
2. k neighbours and prediction
▼
3. Feature scaling
▼
4. Curse of dimensionality
▼
5. Implementation
```

#### 1. Nearest neighbour rule

The nearest neighbour rule assigns an unclassified point the class of the nearest previously classified point (Cover & Hart, 1967). It makes no assumptions about the underlying distribution. In large samples, its probability of error is bounded above by twice the Bayes error, the minimum achievable error, for any number of classes; in this sense, half of the classification information in an infinite sample is contained in the nearest neighbour (Cover & Hart, 1967).

#### 2. k neighbours and prediction

k-NN generalises the rule to the k closest training points: the prediction is the majority class among them or the average of their values (Hastie et al., 2009). k controls the bias-variance trade-off: a small k follows the training data closely, with low bias and high variance, while a large k smooths the prediction. Because all computation happens at prediction time, the method is called lazy learning.

#### 3. Feature scaling

Distances depend on the units of the features, so a feature with large values dominates the distance. Features therefore need to be standardised before k-NN is applied (Hastie et al., 2009; [[ml-preprocessing|ML Preprocessing]]).

#### 4. Curse of dimensionality

Beyer et al. (1999) showed that under broad conditions, as dimensionality increases, the distance to the nearest data point approaches the distance to the farthest data point. Nearest-neighbour queries can then become meaningless, which limits k-NN in high-dimensional spaces (Hastie et al., 2009).

#### 5. Implementation

k-NN is available in common libraries such as scikit-learn (Pedregosa et al., 2011). The same idea of finding the nearest points underlies similarity search over embeddings ([[vector-databases|Vector Databases]]).

#### Origin and variants

The nearest neighbour rule and its error bound go back to Cover & Hart (1967). Beyer et al. (1999) analysed when nearest-neighbour search remains meaningful in high dimensions, and textbook treatments cover k-NN for classification and regression (Hastie et al., 2009).

### When to use it

- When a simple, assumption-free baseline is needed for low-dimensional data (Cover & Hart, 1967; Hastie et al., 2009).
- When the model must adapt to new training data immediately, since no training step is needed (Hastie et al., 2009).
- When the number of features is small or has been reduced, because distances lose meaning in high dimensions (Beyer et al., 1999).

### Strengths and limitations

**Strengths**
- No distributional assumptions; error at most twice the Bayes error in large samples (Cover & Hart, 1967).
- No training phase; new data can be added directly (Hastie et al., 2009).
- Works for classification and regression (Hastie et al., 2009).

**Limitations**
- Sensitive to feature scaling (Hastie et al., 2009).
- Nearest neighbours become less meaningful as dimensionality grows (Beyer et al., 1999).
- Prediction requires comparing with the stored training data, which is costly for large datasets (Hastie et al., 2009).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| 1-nearest neighbour | Class of the single closest point (Cover & Hart, 1967) | Very simple baselines |
| k-NN | Vote or average over k neighbours; k sets the bias-variance trade-off (Hastie et al., 2009) | Low-dimensional data |
| Model-based classifiers | Learn a model once, prediction without the training data (Hastie et al., 2009) | Large datasets, fast prediction |

### In practice

Features are standardised and k is chosen by cross-validation (Hastie et al., 2009). For high-dimensional data, the dimensionality is often reduced first, for example with [[principal-component-analysis|Principal Component Analysis]], because nearest neighbours lose meaning otherwise (Beyer et al., 1999).

### Key takeaway

k-NN predicts from the k closest training points; it is simple and assumption-free but depends on scaling, the choice of k and low dimensionality.

### Sources

- Cover, T. & Hart, P. (1967). *Nearest Neighbor Pattern Classification.* IEEE Transactions on Information Theory 13(1). [doi:10.1109/TIT.1967.1053964](https://doi.org/10.1109/TIT.1967.1053964)
- Beyer, K., Goldstein, J., Ramakrishnan, R. & Shaft, U. (1999). *When Is "Nearest Neighbor" Meaningful?* ICDT 1999. [doi:10.1007/3-540-49257-7_15](https://doi.org/10.1007/3-540-49257-7_15)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

k-Nearest Neighbors (k-NN) sagt für einen neuen Punkt etwas voraus, indem es die k nächstgelegenen Trainingspunkte betrachtet und bei Klassifikation per Mehrheitsentscheid, bei Regression per Mittelwert entscheidet (Hastie et al., 2009). Es braucht kein Training außer dem Speichern der Daten, und schon die einfachste Variante hat bei großen Stichproben höchstens den doppelten Bayes-Fehler (Cover & Hart, 1967). Die Ergebnisse hängen von der Skalierung der Merkmale und der Wahl von k ab, und in hohen Dimensionen verlieren nächste Nachbarn an Aussagekraft (Beyer et al., 1999).

### Funktionsweise

Die Trainingsdaten werden gespeichert. Für einen neuen Punkt werden die Abstände zu allen gespeicherten Punkten berechnet, die k nächsten ausgewählt und ihre Labels oder Werte zusammengefasst.

```text
1. Nächster-Nachbar-Regel
▼
2. k Nachbarn und Vorhersage
▼
3. Skalierung der Merkmale
▼
4. Fluch der Dimensionalität
▼
5. Implementierung
```

#### 1. Nächster-Nachbar-Regel

Die Nächster-Nachbar-Regel weist einem unklassifizierten Punkt die Klasse des nächstgelegenen bereits klassifizierten Punktes zu (Cover & Hart, 1967). Sie trifft keine Annahmen über die zugrunde liegende Verteilung. Bei großen Stichproben ist ihre Fehlerwahrscheinlichkeit für jede Anzahl von Klassen nach oben durch den doppelten Bayes-Fehler, den kleinstmöglichen Fehler, beschränkt; in diesem Sinne steckt die Hälfte der Klassifikationsinformation einer unendlichen Stichprobe im nächsten Nachbarn (Cover & Hart, 1967).

#### 2. k Nachbarn und Vorhersage

k-NN verallgemeinert die Regel auf die k nächstgelegenen Trainingspunkte: Vorhergesagt wird die Mehrheitsklasse unter ihnen oder der Mittelwert ihrer Werte (Hastie et al., 2009). k steuert die Bias-Varianz-Abwägung: Ein kleines k folgt den Trainingsdaten eng, mit geringem Bias und hoher Varianz, ein großes k glättet die Vorhersage. Weil die gesamte Berechnung erst bei der Vorhersage stattfindet, spricht man von Lazy Learning.

#### 3. Skalierung der Merkmale

Abstände hängen von den Einheiten der Merkmale ab, sodass ein Merkmal mit großen Werten den Abstand dominiert. Die Merkmale müssen daher vor der Anwendung von k-NN standardisiert werden (Hastie et al., 2009; [[ml-preprocessing|Preprocessing für Machine Learning]]).

#### 4. Fluch der Dimensionalität

Beyer et al. (1999) zeigten, dass sich unter breiten Bedingungen mit wachsender Dimension der Abstand zum nächsten Datenpunkt dem Abstand zum entferntesten annähert. Nächste-Nachbarn-Abfragen können dann bedeutungslos werden, was k-NN in hochdimensionalen Räumen begrenzt (Hastie et al., 2009).

#### 5. Implementierung

k-NN ist in gängigen Bibliotheken wie scikit-learn verfügbar (Pedregosa et al., 2011). Dieselbe Idee, die nächstgelegenen Punkte zu finden, liegt der Ähnlichkeitssuche über Embeddings zugrunde ([[vector-databases|Vektordatenbanken]]).

#### Ursprung und Varianten

Die Nächster-Nachbar-Regel und ihre Fehlerschranke gehen auf Cover & Hart (1967) zurück. Beyer et al. (1999) untersuchten, wann die Suche nach nächsten Nachbarn in hohen Dimensionen sinnvoll bleibt, und Lehrbücher behandeln k-NN für Klassifikation und Regression (Hastie et al., 2009).

### Wann einsetzen

- Wenn eine einfache Baseline ohne Verteilungsannahmen für niedrigdimensionale Daten gebraucht wird (Cover & Hart, 1967; Hastie et al., 2009).
- Wenn sich das Modell sofort an neue Trainingsdaten anpassen soll, da kein Trainingsschritt nötig ist (Hastie et al., 2009).
- Wenn die Zahl der Merkmale klein ist oder reduziert wurde, weil Abstände in hohen Dimensionen an Aussagekraft verlieren (Beyer et al., 1999).

### Stärken und Grenzen

**Stärken**
- Keine Verteilungsannahmen; bei großen Stichproben höchstens doppelter Bayes-Fehler (Cover & Hart, 1967).
- Keine Trainingsphase; neue Daten lassen sich direkt hinzufügen (Hastie et al., 2009).
- Funktioniert für Klassifikation und Regression (Hastie et al., 2009).

**Einschränkungen**
- Empfindlich gegenüber der Skalierung der Merkmale (Hastie et al., 2009).
- Nächste Nachbarn verlieren mit wachsender Dimension an Aussagekraft (Beyer et al., 1999).
- Die Vorhersage erfordert den Vergleich mit den gespeicherten Trainingsdaten, was bei großen Datensätzen aufwendig ist (Hastie et al., 2009).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Nächster Nachbar (1-NN) | Klasse des einen nächstgelegenen Punktes (Cover & Hart, 1967) | Sehr einfache Baselines |
| k-NN | Abstimmung oder Mittelwert über k Nachbarn; k bestimmt die Bias-Varianz-Abwägung (Hastie et al., 2009) | Niedrigdimensionale Daten |
| Modellbasierte Klassifikatoren | Lernen einmal ein Modell, Vorhersage ohne Trainingsdaten (Hastie et al., 2009) | Große Datensätze, schnelle Vorhersage |

### In der Praxis

Die Merkmale werden standardisiert, und k wird per Kreuzvalidierung gewählt (Hastie et al., 2009). Bei hochdimensionalen Daten wird die Dimension oft vorher reduziert, etwa mit der [[principal-component-analysis|Hauptkomponentenanalyse (PCA)]], weil nächste Nachbarn sonst an Aussagekraft verlieren (Beyer et al., 1999).

### Merksatz

k-NN sagt aus den k nächstgelegenen Trainingspunkten voraus; es ist einfach und kommt ohne Annahmen aus, hängt aber von der Skalierung, der Wahl von k und einer niedrigen Dimension ab.

### Quellen

- Cover, T. & Hart, P. (1967). *Nearest Neighbor Pattern Classification.* IEEE Transactions on Information Theory 13(1). [doi:10.1109/TIT.1967.1053964](https://doi.org/10.1109/TIT.1967.1053964)
- Beyer, K., Goldstein, J., Ramakrishnan, R. & Shaft, U. (1999). *When Is "Nearest Neighbor" Meaningful?* ICDT 1999. [doi:10.1007/3-540-49257-7_15](https://doi.org/10.1007/3-540-49257-7_15)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
