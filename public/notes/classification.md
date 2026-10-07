---
title_en: Classification
title_de: Klassifikation
entity_type: Concept
sources:
- https://doi.org/10.1111/j.2517-6161.1958.tb00292.x
- https://doi.org/10.1111/j.1469-1809.1936.tb02137.x
- https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html
- https://hastie.su.domains/ElemStatLearn/
- https://doi.org/10.1145/1102351.1102430
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Classification predicts a discrete class from input features. Classical methods are logistic regression (Cox, 1958), naive Bayes and discriminant analysis (Fisher, 1936; Hastie et al., 2009). Discriminative models such as logistic regression model the class probability directly, while generative models such as naive Bayes model how the features are distributed in each class (Ng & Jordan, 2001). Predicted probabilities are often distorted and need calibration (Niculescu-Mizil & Caruana, 2005).

### How it works

A model is fitted to labelled examples and returns, for a new example, a class or a probability for each class. The class is then chosen by a decision threshold, and the quality is measured with suitable metrics ([[classification-metrics|Classification Metrics]]).

```text
1. Logistic regression
▼
2. Naive Bayes
▼
3. Discriminant analysis (LDA and QDA)
▼
4. Calibrated probabilities
```

#### 1. Logistic regression

Cox (1958) considered a sequence of 0s and 1s in which the chance that a trial is a 1 depends on one or more independent variables, and developed tests and estimates for this situation; this is an early foundation of logistic regression for binary outcomes. Logistic regression models the class probability directly as a function of the inputs, which makes it a discriminative model (Hastie et al., 2009).

#### 2. Naive Bayes

Naive Bayes is a generative classifier: it models the distribution of the features within each class, assuming that the features are independent given the class, and derives the class probability from that (Hastie et al., 2009). Ng & Jordan (2001) compared it with logistic regression: the discriminative model has the lower asymptotic error, but naive Bayes approaches its own, higher asymptotic error much faster, so with few training examples naive Bayes can perform better.

#### 3. Discriminant analysis (LDA and QDA)

Fisher (1936) introduced the linear discriminant function, a linear combination of several measurements chosen to separate groups as well as possible, illustrated with measurements of iris flowers. Linear discriminant analysis (LDA) assumes that all classes share one covariance matrix, which gives linear decision boundaries; quadratic discriminant analysis (QDA) allows a separate covariance matrix per class, which gives quadratic boundaries but requires more parameters (Hastie et al., 2009).

#### 4. Calibrated probabilities

Predicted probabilities do not always match true probabilities. Niculescu-Mizil & Caruana (2005) showed that boosted trees and stumps push predicted probabilities away from 0 and 1, naive Bayes pushes them toward 0 and 1, and neural nets and bagged trees are well calibrated. Platt scaling and isotonic regression correct these distortions; after calibration, boosted trees, random forests and SVMs predicted the best probabilities.

#### Origin and variants

Fisher (1936) introduced the linear discriminant and Cox (1958) the regression analysis of binary outcomes. Ng & Jordan (2001) compared generative and discriminative classifiers, and Niculescu-Mizil & Caruana (2005) studied the calibration of predicted probabilities. Tree ensembles, support vector machines and neural networks are further classifiers ([[ensemble-methods|Ensemble Methods]], [[support-vector-machines|Support Vector Machines]]).

### When to use it

- When an interpretable model of how inputs affect a binary outcome is needed, logistic regression fits (Cox, 1958; Hastie et al., 2009).
- When only few training examples are available, naive Bayes can outperform logistic regression (Ng & Jordan, 2001).
- When decisions depend on probabilities, for example on risk thresholds, the probabilities should be calibrated (Niculescu-Mizil & Caruana, 2005).

### Strengths and limitations

**Strengths**
- Logistic regression and LDA are simple and interpretable (Hastie et al., 2009).
- Naive Bayes learns quickly from few examples (Ng & Jordan, 2001).
- Calibration methods can turn distorted scores into usable probabilities (Niculescu-Mizil & Caruana, 2005).

**Limitations**
- Naive Bayes rests on an unrealistic independence assumption and pushes probabilities toward 0 and 1 (Niculescu-Mizil & Caruana, 2005).
- With more data, generative models end up with a higher asymptotic error than discriminative ones (Ng & Jordan, 2001).
- QDA needs a covariance matrix per class and therefore more data (Hastie et al., 2009).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Logistic regression | Discriminative; models the class probability directly (Cox, 1958; Hastie et al., 2009) | Interpretable models, larger datasets |
| Naive Bayes | Generative; features independent given the class (Ng & Jordan, 2001) | Few training examples, many features |
| LDA | Generative; shared covariance, linear boundaries (Fisher, 1936; Hastie et al., 2009) | Classes with similar spread |
| QDA | Generative; class-specific covariance, quadratic boundaries (Hastie et al., 2009) | Classes with different spread and enough data |

### In practice

Classifiers are compared with cross-validation on appropriate metrics ([[classification-metrics|Classification Metrics]], [[ml-preprocessing|ML Preprocessing]]). If predicted probabilities are used for decisions, their calibration is checked and, if needed, corrected with Platt scaling or isotonic regression on held-out data (Niculescu-Mizil & Caruana, 2005).

### Key takeaway

Classification predicts classes either by modelling the class probability directly or by modelling the features per class, and the predicted probabilities usually need to be checked for calibration.

### Sources

- Cox, D. R. (1958). *The Regression Analysis of Binary Sequences.* Journal of the Royal Statistical Society, Series B 20(2). [doi:10.1111/j.2517-6161.1958.tb00292.x](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x)
- Fisher, R. A. (1936). *The Use of Multiple Measurements in Taxonomic Problems.* Annals of Eugenics 7(2). [doi:10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x)
- Ng, A. Y. & Jordan, M. I. (2001). *On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes.* NIPS 14. [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Klassifikation sagt aus Eingabemerkmalen eine diskrete Klasse vorher. Klassische Verfahren sind die logistische Regression (Cox, 1958), Naive Bayes und die Diskriminanzanalyse (Fisher, 1936; Hastie et al., 2009). Diskriminative Modelle wie die logistische Regression modellieren die Klassenwahrscheinlichkeit direkt, generative Modelle wie Naive Bayes modellieren, wie die Merkmale in jeder Klasse verteilt sind (Ng & Jordan, 2001). Vorhergesagte Wahrscheinlichkeiten sind oft verzerrt und müssen kalibriert werden (Niculescu-Mizil & Caruana, 2005).

### Funktionsweise

Ein Modell wird an gelabelten Beispielen angepasst und liefert für ein neues Beispiel eine Klasse oder eine Wahrscheinlichkeit je Klasse. Die Klasse ergibt sich dann über einen Entscheidungsschwellenwert, und die Qualität wird mit geeigneten Metriken gemessen ([[classification-metrics|Klassifikationsmetriken]]).

```text
1. Logistische Regression
▼
2. Naive Bayes
▼
3. Diskriminanzanalyse (LDA und QDA)
▼
4. Kalibrierte Wahrscheinlichkeiten
```

#### 1. Logistische Regression

Cox (1958) betrachtete eine Folge von Nullen und Einsen, bei der die Wahrscheinlichkeit einer Eins von einer oder mehreren unabhängigen Variablen abhängt, und entwickelte Tests und Schätzer für diese Situation; das ist eine frühe Grundlage der logistischen Regression für binäre Zielgrößen. Die logistische Regression modelliert die Klassenwahrscheinlichkeit direkt als Funktion der Eingaben und ist damit ein diskriminatives Modell (Hastie et al., 2009).

#### 2. Naive Bayes

Naive Bayes ist ein generativer Klassifikator: Er modelliert die Verteilung der Merkmale innerhalb jeder Klasse unter der Annahme, dass die Merkmale bei gegebener Klasse unabhängig sind, und leitet daraus die Klassenwahrscheinlichkeit ab (Hastie et al., 2009). Ng & Jordan (2001) verglichen ihn mit der logistischen Regression: Das diskriminative Modell hat den geringeren asymptotischen Fehler, Naive Bayes erreicht seinen eigenen, höheren asymptotischen Fehler aber viel schneller und kann daher bei wenigen Trainingsbeispielen besser abschneiden.

#### 3. Diskriminanzanalyse (LDA und QDA)

Fisher (1936) führte die lineare Diskriminanzfunktion ein, eine Linearkombination mehrerer Messungen, die Gruppen möglichst gut trennt, veranschaulicht an Messungen von Schwertlilien. Die lineare Diskriminanzanalyse (LDA) nimmt eine gemeinsame Kovarianzmatrix für alle Klassen an und liefert lineare Entscheidungsgrenzen; die quadratische Diskriminanzanalyse (QDA) erlaubt je Klasse eine eigene Kovarianzmatrix, was quadratische Grenzen ergibt, aber mehr Parameter erfordert (Hastie et al., 2009).

#### 4. Kalibrierte Wahrscheinlichkeiten

Vorhergesagte Wahrscheinlichkeiten stimmen nicht immer mit den tatsächlichen überein. Niculescu-Mizil & Caruana (2005) zeigten, dass Boosted Trees und Stumps die Wahrscheinlichkeiten von 0 und 1 wegdrängen, Naive Bayes sie zu 0 und 1 hindrängt und neuronale Netze sowie Bagged Trees gut kalibriert sind. Platt Scaling und isotone Regression korrigieren diese Verzerrungen; nach der Kalibrierung lieferten Boosted Trees, Random Forests und SVMs die besten Wahrscheinlichkeiten.

#### Ursprung und Varianten

Fisher (1936) führte die lineare Diskriminanzfunktion ein, Cox (1958) die Regressionsanalyse binärer Zielgrößen. Ng & Jordan (2001) verglichen generative und diskriminative Klassifikatoren, Niculescu-Mizil & Caruana (2005) untersuchten die Kalibrierung vorhergesagter Wahrscheinlichkeiten. Baum-Ensembles, Support Vector Machines und neuronale Netze sind weitere Klassifikatoren ([[ensemble-methods|Ensemble-Methoden]], [[support-vector-machines|Support Vector Machines]]).

### Wann einsetzen

- Wenn ein interpretierbares Modell dafür gebraucht wird, wie Eingaben eine binäre Zielgröße beeinflussen, passt die logistische Regression (Cox, 1958; Hastie et al., 2009).
- Wenn nur wenige Trainingsbeispiele vorliegen, kann Naive Bayes die logistische Regression übertreffen (Ng & Jordan, 2001).
- Wenn Entscheidungen von Wahrscheinlichkeiten abhängen, etwa von Risikoschwellen, sollten diese kalibriert sein (Niculescu-Mizil & Caruana, 2005).

### Stärken und Grenzen

**Stärken**
- Logistische Regression und LDA sind einfach und interpretierbar (Hastie et al., 2009).
- Naive Bayes lernt schnell aus wenigen Beispielen (Ng & Jordan, 2001).
- Kalibrierungsverfahren machen aus verzerrten Werten brauchbare Wahrscheinlichkeiten (Niculescu-Mizil & Caruana, 2005).

**Einschränkungen**
- Naive Bayes beruht auf einer unrealistischen Unabhängigkeitsannahme und drängt Wahrscheinlichkeiten zu 0 und 1 (Niculescu-Mizil & Caruana, 2005).
- Mit mehr Daten erreichen generative Modelle einen höheren asymptotischen Fehler als diskriminative (Ng & Jordan, 2001).
- QDA braucht eine Kovarianzmatrix je Klasse und damit mehr Daten (Hastie et al., 2009).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Logistische Regression | Diskriminativ; modelliert die Klassenwahrscheinlichkeit direkt (Cox, 1958; Hastie et al., 2009) | Interpretierbare Modelle, größere Datensätze |
| Naive Bayes | Generativ; Merkmale bei gegebener Klasse unabhängig (Ng & Jordan, 2001) | Wenige Trainingsbeispiele, viele Merkmale |
| LDA | Generativ; gemeinsame Kovarianz, lineare Grenzen (Fisher, 1936; Hastie et al., 2009) | Klassen mit ähnlicher Streuung |
| QDA | Generativ; klassenspezifische Kovarianz, quadratische Grenzen (Hastie et al., 2009) | Klassen mit unterschiedlicher Streuung und genug Daten |

### In der Praxis

Klassifikatoren werden per Kreuzvalidierung mit geeigneten Metriken verglichen ([[classification-metrics|Klassifikationsmetriken]], [[ml-preprocessing|Preprocessing für Machine Learning]]). Werden vorhergesagte Wahrscheinlichkeiten für Entscheidungen genutzt, wird ihre Kalibrierung geprüft und bei Bedarf mit Platt Scaling oder isotoner Regression auf zurückgehaltenen Daten korrigiert (Niculescu-Mizil & Caruana, 2005).

### Merksatz

Klassifikation sagt Klassen voraus, indem sie entweder die Klassenwahrscheinlichkeit direkt oder die Merkmale je Klasse modelliert, und die vorhergesagten Wahrscheinlichkeiten müssen meist auf ihre Kalibrierung geprüft werden.

### Quellen

- Cox, D. R. (1958). *The Regression Analysis of Binary Sequences.* Journal of the Royal Statistical Society, Series B 20(2). [doi:10.1111/j.2517-6161.1958.tb00292.x](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x)
- Fisher, R. A. (1936). *The Use of Multiple Measurements in Taxonomic Problems.* Annals of Eugenics 7(2). [doi:10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x)
- Ng, A. Y. & Jordan, M. I. (2001). *On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes.* NIPS 14. [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)
