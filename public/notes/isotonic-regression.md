---
title_en: Isotonic Regression
title_de: Isotone Regression
entity_type: Method
aliases:
- Isotonic regression
- Isotonic calibration
- Pair-adjacent violators algorithm
- PAV algorithm
sources:
- https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf
- https://scikit-learn.org/stable/modules/isotonic.html
- https://scikit-learn.org/stable/modules/calibration.html
- https://arxiv.org/abs/1706.04599
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Isotonic regression fits the non-decreasing function that is closest to the targets in squared error; the only assumption is monotonicity (scikit-learn developers, 2026a). In machine learning it is best known as a calibration method: it maps a classifier's scores to probabilities with a stepwise constant, monotonically increasing function, fitted on held-out data with the pair-adjacent violators (PAV) algorithm (Niculescu-Mizil & Caruana, 2005). Because it can correct any monotonic distortion, it is more flexible than [[platt-scaling|Platt scaling]], but it overfits more easily: with fewer than about 200 to 1,000 calibration cases, Platt scaling did better for all nine learning methods tested (Niculescu-Mizil & Caruana, 2005). For modern [[neural-networks|neural networks]], the simpler [[temperature-scaling|temperature scaling]] usually calibrates better (Guo et al., 2017).

### How it works

```text
held-out calibration set: (score f_i, label y_i)
  └─ sort by f_i
       └─ PAV: start with m_i = y_i; whenever a neighbour pair violates order (m_left > m_right),
          merge them into a block with their weighted mean; repeat until non-decreasing
            └─ stepwise constant, non-decreasing map m(f) → calibrated probability
```

#### 1. The optimisation problem

Given predictions f_i and true targets y_i, isotonic regression assumes y_i = m(f_i) + ε_i for some monotonically increasing function m and finds the m that minimises the squared error over the training pairs (Niculescu-Mizil & Caruana, 2005). In general form it fits a non-decreasing real function to one-dimensional data, optionally with sample weights, and can be set to fit a non-increasing function instead (scikit-learn developers, 2026a).

#### 2. The pair-adjacent violators algorithm

The PAV algorithm (Ayer et al., 1955, as presented by Niculescu-Mizil & Caruana, 2005) sorts the examples by score, starts with each label as its own value and, whenever two adjacent blocks are out of order, replaces them with their weighted average. The result is a stepwise constant function (Niculescu-Mizil & Caruana, 2005); scikit-learn interpolates between the fitted points, so its predictions for unseen inputs are piecewise linear (scikit-learn developers, 2026a).

#### 3. Calibration on independent data

If the same data is used to train the model and the isotonic function, the calibration is biased, so an independent validation set is used (Niculescu-Mizil & Caruana, 2005). In scikit-learn, `CalibratedClassifierCV(method="isotonic")` fits the calibrator on held-out folds of a cross-validation (scikit-learn developers, 2026b).

#### 4. Binary and multiclass use

Like Platt scaling, the method is designed for binary classification; multiclass problems are usually split into one-vs-rest binary problems whose calibrated outputs are recombined (Niculescu-Mizil & Caruana, 2005; scikit-learn developers, 2026b). Guo et al. (2017) describe isotonic regression as a strict generalisation of histogram binning in which bin boundaries and bin values are optimised jointly.

#### Origin and variants

Zadrozny and Elkan used isotonic regression to calibrate SVMs, [[naive-bayes|naive Bayes]], boosted naive Bayes and [[decision-trees|decision trees]]; Niculescu-Mizil and Caruana (2005) compared it systematically with Platt scaling across ten learning methods. Guo et al. (2017) call it arguably the most common non-parametric calibration method and compare it with histogram binning, Bayesian Binning into Quantiles and temperature scaling for deep networks.

### When to use it

- Calibrating classifiers whose distortion is monotonic but not sigmoid-shaped, for example naive Bayes, which pushes probabilities towards 0 and 1 (Niculescu-Mizil & Caruana, 2005).
- When enough calibration data is available: with more than about 1,000 samples, isotonic calibration performs as well as or better than the sigmoid method (scikit-learn developers, 2026b).
- Not when ranking must be preserved exactly, since its ties can change ROC-AUC, and not as the first choice for deep networks (scikit-learn developers, 2026b; Guo et al., 2017).

### Strengths and limitations

**Strengths**
- Corrects any monotonic distortion, with no assumption about its shape (Niculescu-Mizil & Caruana, 2005).
- After calibration, boosted trees, random forests and SVMs gave the best probabilities among the ten methods tested (Niculescu-Mizil & Caruana, 2005).
- Simple, fast algorithm and standard library support (scikit-learn developers, 2026a).

**Limitations**
- More prone to [[overfitting|overfitting]] than Platt scaling on small calibration sets (Niculescu-Mizil & Caruana, 2005).
- Introduces ties in predicted probabilities, so ranking metrics such as ROC-AUC can change (scikit-learn developers, 2026b).
- On deep networks it was beaten by temperature scaling and, on most datasets, even by plain histogram binning: for a 110-layer [[resnet|ResNet]] on CIFAR-100, expected calibration error fell from 16.53% to 4.99% with isotonic regression and to 1.26% with temperature scaling (Guo et al., 2017).

### Comparison

| Method | Calibration map | Parameters | Data needed |
|---|---|---|---|
| Platt scaling | sigmoid | 2 | works with small calibration sets |
| Isotonic regression | monotonic step function | non-parametric | about 1,000 cases or more |
| Temperature scaling | softmax with one temperature | 1 | small validation set; keeps the predicted class |

Sources: Niculescu-Mizil & Caruana (2005); scikit-learn developers (2026b); Guo et al. (2017).

### In practice

Check calibration with a reliability diagram, which plots the mean predicted value against the observed fraction of positives per bin, before and after calibration (Niculescu-Mizil & Caruana, 2005). Fit the isotonic map on data not used for training, and keep it disjoint from the test data ([[cross-validation|cross-validation]], [[classification-metrics|classification metrics]]). If predicted probabilities feed into decisions, calibration belongs into model selection, not only accuracy ([[classification|classification]]).

### Key takeaway

Isotonic regression learns any monotonic mapping from scores to probabilities; it is the flexible calibration choice when calibration data is plentiful, while Platt or temperature scaling is safer when data is scarce or the model is a deep network.

### Sources

- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting Good Probabilities With Supervised Learning. *Proceedings of ICML 2005*. [PDF](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf)
- scikit-learn developers (2026a). *User Guide 1.15: Isotonic regression*. [scikit-learn.org](https://scikit-learn.org/stable/modules/isotonic.html)
- scikit-learn developers (2026b). *User Guide 1.16: Probability calibration*. [scikit-learn.org](https://scikit-learn.org/stable/modules/calibration.html)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die isotone Regression passt die nicht fallende Funktion an, die den Zielwerten im quadratischen Fehler am nächsten kommt; die einzige Annahme ist Monotonie (scikit-learn developers, 2026a). Im maschinellen Lernen ist sie vor allem als Kalibrierungsverfahren bekannt: Sie bildet die Scores eines Klassifikators mit einer stückweise konstanten, monoton steigenden Funktion auf Wahrscheinlichkeiten ab, angepasst auf zurückgehaltenen Daten mit dem Pair-Adjacent-Violators-Algorithmus (PAV) (Niculescu-Mizil & Caruana, 2005). Weil sie jede monotone Verzerrung korrigieren kann, ist sie flexibler als [[platt-scaling|Platt Scaling]], neigt aber eher zur Überanpassung: Mit weniger als etwa 200 bis 1 000 Kalibrierungsfällen schnitt Platt Scaling bei allen neun getesteten Lernverfahren besser ab (Niculescu-Mizil & Caruana, 2005). Für moderne [[neural-networks|neuronale Netze]] kalibriert das einfachere [[temperature-scaling|Temperature Scaling]] meist besser (Guo et al., 2017).

### Funktionsweise

```text
zurückgehaltene Kalibrierungsmenge: (Score f_i, Label y_i)
  └─ nach f_i sortieren
       └─ PAV: Start mit m_i = y_i; verletzt ein Nachbarpaar die Ordnung (m_links > m_rechts),
          beide zu einem Block mit gewichtetem Mittel zusammenfassen; wiederholen bis nicht fallend
            └─ stückweise konstante, nicht fallende Abbildung m(f) → kalibrierte Wahrscheinlichkeit
```

#### 1. Das Optimierungsproblem

Zu Vorhersagen f_i und wahren Zielwerten y_i nimmt die isotone Regression y_i = m(f_i) + ε_i für eine monoton steigende Funktion m an und sucht das m, das den quadratischen Fehler über die Trainingspaare minimiert (Niculescu-Mizil & Caruana, 2005). Allgemein passt sie eine nicht fallende reelle Funktion an eindimensionale Daten an, optional mit Gewichten je Beispiel, und lässt sich auch auf eine nicht steigende Funktion umstellen (scikit-learn developers, 2026a).

#### 2. Der Pair-Adjacent-Violators-Algorithmus

Der PAV-Algorithmus (Ayer et al., 1955, dargestellt bei Niculescu-Mizil & Caruana, 2005) sortiert die Beispiele nach Score, beginnt mit jedem Label als eigenem Wert und ersetzt zwei benachbarte Blöcke durch ihren gewichteten Mittelwert, sobald sie in falscher Reihenfolge stehen. Ergebnis ist eine stückweise konstante Funktion (Niculescu-Mizil & Caruana, 2005); scikit-learn interpoliert zwischen den angepassten Punkten, sodass seine Vorhersagen für neue Eingaben stückweise linear sind (scikit-learn developers, 2026a).

#### 3. Kalibrierung auf unabhängigen Daten

Werden dieselben Daten für das Modell und die isotone Funktion verwendet, ist die Kalibrierung verzerrt; deshalb wird eine unabhängige Validierungsmenge genutzt (Niculescu-Mizil & Caruana, 2005). In scikit-learn passt `CalibratedClassifierCV(method="isotonic")` den Kalibrator auf zurückgehaltenen Folds einer Kreuzvalidierung an (scikit-learn developers, 2026b).

#### 4. Binäre und Mehrklassen-Anwendung

Wie Platt Scaling ist das Verfahren für binäre Klassifikation gedacht; Mehrklassenprobleme werden meist in binäre One-vs-Rest-Probleme zerlegt, deren kalibrierte Ausgaben wieder zusammengeführt werden (Niculescu-Mizil & Caruana, 2005; scikit-learn developers, 2026b). Guo et al. (2017) beschreiben die isotone Regression als strikte Verallgemeinerung des Histogram Binning, bei der Bin-Grenzen und Bin-Werte gemeinsam optimiert werden.

#### Herkunft und Varianten

Zadrozny und Elkan nutzten die isotone Regression, um SVMs, [[naive-bayes|Naive Bayes]], Boosted Naive Bayes und [[decision-trees|Entscheidungsbäume]] zu kalibrieren; Niculescu-Mizil und Caruana (2005) verglichen sie systematisch mit Platt Scaling über zehn Lernverfahren. Guo et al. (2017) nennen sie das wohl verbreitetste nichtparametrische Kalibrierungsverfahren und vergleichen sie für tiefe Netze mit Histogram Binning, Bayesian Binning into Quantiles und Temperature Scaling.

### Wann einsetzen

- Zur Kalibrierung von Klassifikatoren, deren Verzerrung monoton, aber nicht sigmoidförmig ist, etwa Naive Bayes, das Wahrscheinlichkeiten in Richtung 0 und 1 drückt (Niculescu-Mizil & Caruana, 2005).
- Wenn genug Kalibrierungsdaten vorliegen: Ab etwa 1 000 Beispielen ist die isotone Kalibrierung gleich gut oder besser als das Sigmoid-Verfahren (scikit-learn developers, 2026b).
- Nicht, wenn die Rangfolge exakt erhalten bleiben muss, da ihre Gleichstände die ROC-AUC verändern können, und nicht als erste Wahl für tiefe Netze (scikit-learn developers, 2026b; Guo et al., 2017).

### Stärken und Grenzen

**Stärken**
- Korrigiert jede monotone Verzerrung ohne Annahme über deren Form (Niculescu-Mizil & Caruana, 2005).
- Nach der Kalibrierung lieferten Boosted Trees, Random Forests und SVMs die besten Wahrscheinlichkeiten unter den zehn getesteten Verfahren (Niculescu-Mizil & Caruana, 2005).
- Einfacher, schneller Algorithmus mit Unterstützung in Standardbibliotheken (scikit-learn developers, 2026a).

**Grenzen**
- Auf kleinen Kalibrierungsmengen anfälliger für [[overfitting|Overfitting]] als Platt Scaling (Niculescu-Mizil & Caruana, 2005).
- Erzeugt Gleichstände bei den vorhergesagten Wahrscheinlichkeiten, sodass sich Rangmetriken wie die ROC-AUC ändern können (scikit-learn developers, 2026b).
- Bei tiefen Netzen wurde sie von Temperature Scaling und auf den meisten Datensätzen sogar vom einfachen Histogram Binning übertroffen: Für ein [[resnet|ResNet]] mit 110 Schichten auf CIFAR-100 sank der erwartete Kalibrierungsfehler mit isotoner Regression von 16,53 % auf 4,99 %, mit Temperature Scaling auf 1,26 % (Guo et al., 2017).

### Vergleich

| Verfahren | Kalibrierungsabbildung | Parameter | Benötigte Daten |
|---|---|---|---|
| Platt Scaling | Sigmoid | 2 | funktioniert mit kleinen Kalibrierungsmengen |
| Isotone Regression | monotone Stufenfunktion | nichtparametrisch | etwa 1 000 Fälle oder mehr |
| Temperature Scaling | Softmax mit einer Temperatur | 1 | kleine Validierungsmenge; vorhergesagte Klasse bleibt gleich |

Quellen: Niculescu-Mizil & Caruana (2005); scikit-learn developers (2026b); Guo et al. (2017).

### In der Praxis

Die Kalibrierung wird vor und nach dem Verfahren mit einem Reliability-Diagramm geprüft, das je Bin den mittleren vorhergesagten Wert gegen den beobachteten Anteil positiver Fälle aufträgt (Niculescu-Mizil & Caruana, 2005). Die isotone Abbildung wird auf Daten angepasst, die nicht zum Training dienten, und bleibt von den Testdaten getrennt ([[cross-validation|Kreuzvalidierung]], [[classification-metrics|Klassifikationsmetriken]]). Fließen vorhergesagte Wahrscheinlichkeiten in Entscheidungen ein, gehört die Kalibrierung in die Modellauswahl, nicht nur die Accuracy ([[classification|Klassifikation]]).

### Merksatz

Die isotone Regression lernt jede monotone Abbildung von Scores auf Wahrscheinlichkeiten; sie ist die flexible Wahl bei reichlich Kalibrierungsdaten, während Platt oder Temperature Scaling sicherer sind, wenn Daten knapp sind oder das Modell ein tiefes Netz ist.

### Quellen

- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting Good Probabilities With Supervised Learning. *Proceedings of ICML 2005*. [PDF](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf)
- scikit-learn developers (2026a). *User Guide 1.15: Isotonic regression*. [scikit-learn.org](https://scikit-learn.org/stable/modules/isotonic.html)
- scikit-learn developers (2026b). *User Guide 1.16: Probability calibration*. [scikit-learn.org](https://scikit-learn.org/stable/modules/calibration.html)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
