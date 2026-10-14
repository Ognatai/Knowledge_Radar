---
title_en: Platt Scaling
title_de: Platt Scaling
entity_type: Method
aliases:
- Platt scaling
- Platt calibration
- Sigmoid calibration
sources:
- https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf
- https://scikit-learn.org/stable/modules/calibration.html
- https://arxiv.org/abs/1706.04599
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Platt scaling turns the scores of a binary classifier into calibrated probabilities by passing them through a sigmoid, P(y = 1 | f) = 1 / (1 + exp(A·f + B)), whose two parameters A and B are fitted by maximum likelihood on data that was not used to train the classifier (Niculescu-Mizil & Caruana, 2005). Platt proposed it in 1999 for the outputs of [[support-vector-machines|support vector machines]]. It works best when the distortion of the scores is sigmoid-shaped, as with SVMs and boosted trees, and needs little calibration data; isotonic regression is more flexible but overfits more easily on small calibration sets (Niculescu-Mizil & Caruana, 2005). Temperature scaling, a single-parameter variant, is a simple and effective way to calibrate modern [[neural-networks|neural networks]] (Guo et al., 2017).

### How it works

```text
trained classifier ─→ raw score f(x)  (e.g. SVM decision value, boosted-tree score)
                             │
calibration set (held out) ──┤  fit A, B by minimising log loss
                             ▼
             p = 1 / (1 + exp(A·f(x) + B))   →  calibrated probability in [0, 1]
check: reliability diagram (mean predicted value vs. fraction of positives per bin)
```

#### 1. Why calibration is needed

A classifier is well calibrated when, among the cases it gives a probability of about 0.8, about 80% actually belong to the positive class ([[scikit-learn|scikit-learn]] developers, 2026). Many applications need such probabilities, and good accuracy or area under the ROC curve is not sufficient (Niculescu-Mizil & Caruana, 2005). Maximum margin methods such as SVMs, boosted trees and boosted stumps push predicted probabilities away from 0 and 1, which produces a characteristic sigmoid-shaped distortion; naive Bayes pushes them towards 0 and 1 ([[naive-bayes|naive Bayes]]); neural networks, bagged trees and logistic regression were well calibrated in that study (Niculescu-Mizil & Caruana, 2005).

#### 2. The sigmoid fit

The classifier's output f(x) is passed through a sigmoid with parameters A and B, which are fitted by maximum likelihood, that is by minimising the log loss on a calibration set of pairs (fᵢ, yᵢ) (Niculescu-Mizil & Caruana, 2005). Because the sigmoid is strictly monotonic, it keeps the ranking of the predictions and therefore ranking metrics such as ROC-AUC (scikit-learn developers, 2026).

#### 3. An independent calibration set

If the calibrator is fitted on the same data the model was trained on, it is biased: a model that separates its training set perfectly would yield a sigmoid that outputs only 0 or 1 (Niculescu-Mizil & Caruana, 2005). An independent calibration set, or predictions from [[cross-validation|cross-validation]], is therefore needed; scikit-learn's `CalibratedClassifierCV` fits the calibrator on held-out folds (scikit-learn developers, 2026).

#### 4. Built-in overfitting control

To avoid [[overfitting|overfitting]] the sigmoid, Platt replaces the targets 1 and 0 by y₊ = (N₊ + 1)/(N₊ + 2) and y₋ = 1/(N₋ + 2), where N₊ and N₋ are the numbers of positive and negative examples (Niculescu-Mizil & Caruana, 2005).

#### Origin and variants

Platt (1999) proposed the method to turn SVM outputs into posterior probabilities; Niculescu-Mizil and Caruana (2005) showed that the sigmoid transformation is also justified for boosted trees and boosted stumps and compared it with isotonic regression, which fits any monotonically increasing step function. Both methods are designed for binary problems; multiclass problems are handled by calibrating one-vs-rest models and recombining them (Niculescu-Mizil & Caruana, 2005; scikit-learn developers, 2026). For deep networks, Guo et al. (2017) found that modern neural networks are poorly calibrated and that temperature scaling, a single-parameter variant of Platt scaling, was surprisingly effective on most datasets.

### When to use it

- Scores from SVMs, boosted trees or other maximum margin methods have to be used as probabilities (Niculescu-Mizil & Caruana, 2005).
- Little calibration data is available: with fewer than about 200 to 1,000 calibration cases, Platt scaling beat isotonic regression for all nine learning methods tested (Niculescu-Mizil & Caruana, 2005).
- The ranking of predictions must stay unchanged (scikit-learn developers, 2026).
- Probabilities feed into decisions, thresholds or risk scores ([[classification|classification]], [[ml-preprocessing|ML preprocessing]]).

### Strengths and limitations

**Strengths**
- Only two parameters, so it needs little data and rarely overfits (Niculescu-Mizil & Caruana, 2005).
- Keeps the order of predictions and thus ROC-AUC (scikit-learn developers, 2026).
- After calibration, boosted trees, random forests and SVMs predicted the best probabilities among ten methods in the study (Niculescu-Mizil & Caruana, 2005).

**Limitations**
- Assumes a sigmoid-shaped distortion; for naive Bayes, whose distortion is an inverted sigmoid, isotonic regression is the better choice (Niculescu-Mizil & Caruana, 2005).
- Works best when calibration errors are symmetrical, which can fail for highly imbalanced problems (scikit-learn developers, 2026).
- Can slightly worsen models that are already well calibrated, such as neural networks in the study, because the sigmoid has trouble fitting the tails (Niculescu-Mizil & Caruana, 2005).

### Comparison

| Method | Mapping | Data needed | Keeps ranking |
|---|---|---|---|
| Platt scaling | sigmoid, 2 parameters | small calibration sets | yes |
| Isotonic regression | monotonic step function | about 1,000 cases or more | ties possible |
| Temperature scaling | softmax with one temperature | small | yes |

Sources: Niculescu-Mizil & Caruana (2005); scikit-learn developers (2026); Guo et al. (2017).

### In practice

In scikit-learn, Platt scaling is `CalibratedClassifierCV(method="sigmoid")`; with enough data (more than about 1,000 samples), `method="isotonic"` performs as well or better (scikit-learn developers, 2026). Calibration is checked with reliability diagrams, which bin the predictions and plot the mean predicted value against the fraction of positives (Niculescu-Mizil & Caruana, 2005). Proper scoring rules such as the Brier score mix calibration with discriminative power and are of limited use for assessing calibration alone (scikit-learn developers, 2026); see [[neural-network-evaluation|neural network evaluation]] for calibration checks of neural networks.

### Key takeaway

Platt scaling fits a two-parameter sigmoid on held-out data to turn classifier scores into calibrated probabilities; it suits sigmoid-shaped distortions and small calibration sets, while isotonic regression is the more flexible choice when data is plentiful.

### Sources

- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting Good Probabilities With Supervised Learning. *Proceedings of ICML 2005*. [PDF](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf)
- scikit-learn developers (2026). *User Guide 1.16: Probability calibration* (version 1.9). [scikit-learn.org](https://scikit-learn.org/stable/modules/calibration.html)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Platt Scaling wandelt die Scores eines binären Klassifikators in kalibrierte Wahrscheinlichkeiten um, indem es sie durch eine Sigmoidfunktion schickt, P(y = 1 | f) = 1 / (1 + exp(A·f + B)), deren zwei Parameter A und B per Maximum Likelihood auf Daten angepasst werden, die nicht zum Training des Klassifikators genutzt wurden (Niculescu-Mizil & Caruana, 2005). Platt schlug das Verfahren 1999 für die Ausgaben von [[support-vector-machines|Support Vector Machines]] vor. Es funktioniert am besten, wenn die Verzerrung der Scores sigmoidförmig ist, wie bei SVMs und Boosted Trees, und braucht wenig Kalibrierungsdaten; isotone Regression ist flexibler, überanpasst sich aber leichter bei kleinen Kalibrierungsmengen (Niculescu-Mizil & Caruana, 2005). Temperature Scaling, eine Variante mit einem einzigen Parameter, ist ein einfacher und wirksamer Weg, moderne [[neural-networks|neuronale Netze]] zu kalibrieren (Guo et al., 2017).

### Funktionsweise

```text
trainierter Klassifikator ─→ Roh-Score f(x)  (z. B. SVM-Entscheidungswert, Boosted-Tree-Score)
                                    │
Kalibrierungsmenge (zurückgehalten) ┤  A, B durch Minimierung des Log Loss anpassen
                                    ▼
             p = 1 / (1 + exp(A·f(x) + B))   →  kalibrierte Wahrscheinlichkeit in [0, 1]
Prüfung: Reliability-Diagramm (mittlerer Vorhersagewert vs. Anteil Positiver je Bin)
```

#### 1. Warum Kalibrierung nötig ist

Ein Klassifikator ist gut kalibriert, wenn von den Fällen, denen er eine Wahrscheinlichkeit von etwa 0,8 gibt, etwa 80 % tatsächlich zur positiven Klasse gehören ([[scikit-learn|scikit-learn]] developers, 2026). Viele Anwendungen brauchen solche Wahrscheinlichkeiten, und eine gute Accuracy oder Fläche unter der ROC-Kurve reicht nicht aus (Niculescu-Mizil & Caruana, 2005). Maximum-Margin-Verfahren wie SVMs, Boosted Trees und Boosted Stumps drängen vorhergesagte Wahrscheinlichkeiten von 0 und 1 weg, was eine typische sigmoidförmige Verzerrung erzeugt; Naive Bayes drängt sie zu 0 und 1 hin ([[naive-bayes|Naive Bayes]]); neuronale Netze, Bagged Trees und logistische Regression waren in dieser Studie gut kalibriert (Niculescu-Mizil & Caruana, 2005).

#### 2. Die Sigmoid-Anpassung

Die Ausgabe f(x) des Klassifikators wird durch eine Sigmoidfunktion mit den Parametern A und B geschickt, die per Maximum Likelihood angepasst werden, also durch Minimierung des Log Loss auf einer Kalibrierungsmenge aus Paaren (fᵢ, yᵢ) (Niculescu-Mizil & Caruana, 2005). Da die Sigmoidfunktion streng monoton ist, bleibt die Rangfolge der Vorhersagen erhalten und damit auch Rangmetriken wie ROC-AUC (scikit-learn developers, 2026).

#### 3. Eine unabhängige Kalibrierungsmenge

Wird der Kalibrator auf denselben Daten angepasst, auf denen das Modell trainiert wurde, ist er verzerrt: Ein Modell, das seine Trainingsmenge perfekt trennt, ergäbe eine Sigmoidfunktion, die nur 0 oder 1 ausgibt (Niculescu-Mizil & Caruana, 2005). Daher braucht es eine unabhängige Kalibrierungsmenge oder Vorhersagen aus [[cross-validation|Kreuzvalidierung]]; `CalibratedClassifierCV` in scikit-learn passt den Kalibrator auf zurückgehaltenen Folds an (scikit-learn developers, 2026).

#### 4. Eingebauter Schutz vor Overfitting

Um eine [[overfitting|Überanpassung]] der Sigmoidfunktion zu vermeiden, ersetzt Platt die Zielwerte 1 und 0 durch y₊ = (N₊ + 1)/(N₊ + 2) und y₋ = 1/(N₋ + 2), wobei N₊ und N₋ die Zahl der positiven und negativen Beispiele sind (Niculescu-Mizil & Caruana, 2005).

#### Herkunft und Varianten

Platt (1999) schlug das Verfahren vor, um SVM-Ausgaben in A-posteriori-Wahrscheinlichkeiten umzuwandeln; Niculescu-Mizil und Caruana (2005) zeigten, dass die Sigmoid-Transformation auch für Boosted Trees und Boosted Stumps gerechtfertigt ist, und verglichen sie mit isotoner Regression, die eine beliebige monoton steigende Treppenfunktion anpasst. Beide Verfahren sind für binäre Probleme gedacht; Mehrklassenprobleme werden behandelt, indem One-vs-Rest-Modelle kalibriert und wieder zusammengeführt werden (Niculescu-Mizil & Caruana, 2005; scikit-learn developers, 2026). Für tiefe Netze stellten Guo et al. (2017) fest, dass moderne neuronale Netze schlecht kalibriert sind und Temperature Scaling, eine Variante von Platt Scaling mit einem einzigen Parameter, auf den meisten Datensätzen überraschend wirksam war.

### Wann einsetzen

- Scores von SVMs, Boosted Trees oder anderen Maximum-Margin-Verfahren sollen als Wahrscheinlichkeiten genutzt werden (Niculescu-Mizil & Caruana, 2005).
- Es gibt wenig Kalibrierungsdaten: Mit weniger als etwa 200 bis 1.000 Kalibrierungsfällen schlug Platt Scaling die isotone Regression bei allen neun getesteten Lernverfahren (Niculescu-Mizil & Caruana, 2005).
- Die Rangfolge der Vorhersagen muss unverändert bleiben (scikit-learn developers, 2026).
- Wahrscheinlichkeiten fließen in Entscheidungen, Schwellenwerte oder Risikoscores ein ([[classification|Klassifikation]], [[ml-preprocessing|ML-Vorverarbeitung]]).

### Stärken und Grenzen

**Stärken**
- Nur zwei Parameter, daher braucht es wenig Daten und überanpasst sich selten (Niculescu-Mizil & Caruana, 2005).
- Erhält die Reihenfolge der Vorhersagen und damit ROC-AUC (scikit-learn developers, 2026).
- Nach der Kalibrierung lieferten Boosted Trees, Random Forests und SVMs unter zehn Verfahren der Studie die besten Wahrscheinlichkeiten (Niculescu-Mizil & Caruana, 2005).

**Grenzen**
- Setzt eine sigmoidförmige Verzerrung voraus; für Naive Bayes, dessen Verzerrung einer umgekehrten Sigmoidfunktion folgt, ist isotone Regression die bessere Wahl (Niculescu-Mizil & Caruana, 2005).
- Funktioniert am besten bei symmetrischen Kalibrierungsfehlern, was bei stark unausgewogenen Problemen scheitern kann (scikit-learn developers, 2026).
- Kann bereits gut kalibrierte Modelle leicht verschlechtern, etwa neuronale Netze in der Studie, weil die Sigmoidfunktion die Ränder schlecht abbildet (Niculescu-Mizil & Caruana, 2005).

### Vergleich

| Verfahren | Abbildung | Benötigte Daten | Erhält Rangfolge |
|---|---|---|---|
| Platt Scaling | Sigmoid, 2 Parameter | kleine Kalibrierungsmengen | ja |
| Isotone Regression | monotone Treppenfunktion | etwa 1.000 Fälle oder mehr | Gleichstände möglich |
| Temperature Scaling | Softmax mit einer Temperatur | wenig | ja |

Quellen: Niculescu-Mizil & Caruana (2005); scikit-learn developers (2026); Guo et al. (2017).

### In der Praxis

In scikit-learn entspricht Platt Scaling `CalibratedClassifierCV(method="sigmoid")`; mit genug Daten (mehr als etwa 1.000 Beispiele) ist `method="isotonic"` gleich gut oder besser (scikit-learn developers, 2026). Die Kalibrierung wird mit Reliability-Diagrammen geprüft, die die Vorhersagen in Bins einteilen und den mittleren Vorhersagewert gegen den Anteil der Positiven auftragen (Niculescu-Mizil & Caruana, 2005). Strikt proper Scoring Rules wie der Brier Score vermischen Kalibrierung mit Trennschärfe und eignen sich nur begrenzt, um die Kalibrierung allein zu beurteilen (scikit-learn developers, 2026); zur Kalibrierungsprüfung neuronaler Netze siehe [[neural-network-evaluation|Evaluation neuronaler Netze]].

### Merksatz

Platt Scaling passt auf zurückgehaltenen Daten eine Sigmoidfunktion mit zwei Parametern an, um Klassifikator-Scores in kalibrierte Wahrscheinlichkeiten umzuwandeln; es eignet sich für sigmoidförmige Verzerrungen und kleine Kalibrierungsmengen, während isotone Regression bei vielen Daten die flexiblere Wahl ist.

### Quellen

- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting Good Probabilities With Supervised Learning. *Proceedings of ICML 2005*. [PDF](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf)
- scikit-learn developers (2026). *User Guide 1.16: Probability calibration* (Version 1.9). [scikit-learn.org](https://scikit-learn.org/stable/modules/calibration.html)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
