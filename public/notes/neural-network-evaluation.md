---
title_en: Evaluating Neural Networks
title_de: Modellbewertung neuronaler Netze
entity_type: Method
sources:
- https://www.deeplearningbook.org/
- https://arxiv.org/abs/1611.03530
- https://arxiv.org/abs/1812.11118
- https://arxiv.org/abs/1706.04599
- https://aclanthology.org/P02-1040/
- https://doi.org/10.1016/j.ijforecast.2006.03.001
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Evaluating a neural network means measuring how well it performs on data it was not trained on, with metrics that match the task: classification metrics, error measures such as MAE and RMSE for regression (Hyndman & Koehler, 2006), and overlap metrics such as BLEU for generated text (Papineni et al., 2002). Comparing training and validation error reveals underfitting and overfitting (Goodfellow et al., 2016), although large networks can fit even random labels and still generalise on real data (Zhang et al., 2016). Predicted probabilities of modern networks are often poorly calibrated (Guo et al., 2017).

### How it works

The network is trained on a training set, monitored on a validation set during development and evaluated once on a held-out test set. Task-specific metrics are computed on each set, and the gap between training and validation results shows whether the model underfits or overfits.

```text
1. Metrics for classification
▼
2. Metrics for regression
▼
3. Metrics for generated text
▼
4. Underfitting and overfitting
▼
5. Generalisation of large networks
▼
6. Calibration
```

#### 1. Metrics for classification

The metric should match the goal of the application: accuracy for balanced problems with equal error costs, precision and recall when one kind of error matters more, and coverage when a system may abstain from deciding (Goodfellow et al., 2016). Confusion-matrix metrics and threshold-free curves are described in [[classification-metrics|Classification Metrics]].

#### 2. Metrics for regression

For numerical predictions, scale-dependent measures such as the mean absolute error (MAE) and the root mean squared error (RMSE) are common; RMSE penalises large errors more strongly (Hyndman & Koehler, 2006). Percentage errors such as MAPE are scale-free but can be infinite or misleading when actual values are zero or close to zero; the mean absolute scaled error (MASE) avoids this by scaling errors by those of a naive forecast.

#### 3. Metrics for generated text

For generated text, such as translations, outputs are compared with reference texts. BLEU computes clipped n-gram precision up to length four, combines it by a geometric mean and applies a brevity penalty; it correlates with human judgements at corpus level (Papineni et al., 2002). Further lexical and embedding-based metrics are covered in [[text-similarity-metrics|Text Similarity Metrics]], and the evaluation of large language models in [[llm-evaluation|LLM Evaluation]].

#### 4. Underfitting and overfitting

A model underfits when its training error is too high, and overfits when the gap between training error and test error is too large (Goodfellow et al., 2016). Both relate to the model's capacity: too little capacity leads to underfitting, too much to overfitting. Monitoring the validation error during training reveals overfitting and allows early stopping ([[regularization-and-hyperparameters|Regularization and Hyperparameters]]).

#### 5. Generalisation of large networks

Zhang et al. (2016) showed that state-of-the-art convolutional networks for image classification easily fit a random labelling of the training data, even with explicit regularisation and even when the images are replaced by random noise. Traditional explanations based on model family or regularisation therefore do not explain why large networks generalise well. Belkin et al. (2018) reconcile this with the bias-variance trade-off through a "double descent" curve: test error first follows the classical U shape, but decreases again when capacity grows beyond the point where the model fits the training data exactly.

#### 6. Calibration

Calibration means that predicted probabilities reflect the true likelihood of being correct. Modern neural networks, unlike those from a decade ago, are poorly calibrated; depth, width, weight decay and batch normalisation influence this (Guo et al., 2017). On most datasets, temperature scaling, a single-parameter variant of Platt scaling, was surprisingly effective at correcting it ([[ml-preprocessing|ML Preprocessing]]).

#### Origin and variants

Goodfellow et al. (2016) describe the classical view of generalisation and practical methodology for deep learning. Zhang et al. (2016) and Belkin et al. (2018) revised the understanding of generalisation in large networks, Guo et al. (2017) showed their miscalibration, and task metrics such as BLEU (Papineni et al., 2002) and MASE (Hyndman & Koehler, 2006) come from translation and forecasting.

### When to use it

- Throughout training, to detect underfitting and overfitting from training and validation curves (Goodfellow et al., 2016).
- When predicted probabilities are used for decisions, to check and correct calibration (Guo et al., 2017).
- When errors on numerical targets must be compared across series or scales, with scale-free measures (Hyndman & Koehler, 2006).

### Strengths and limitations

**Strengths**
- Training and validation curves give a simple diagnosis of underfitting and overfitting (Goodfellow et al., 2016).
- Temperature scaling corrects calibration with one parameter (Guo et al., 2017).
- Standard metrics such as BLEU make systems comparable at corpus level (Papineni et al., 2002).

**Limitations**
- Classical capacity arguments do not explain the generalisation of large networks (Zhang et al., 2016; Belkin et al., 2018).
- Percentage error measures can be undefined or misleading (Hyndman & Koehler, 2006).
- High accuracy does not imply calibrated probabilities (Guo et al., 2017).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Classification metrics | Count correct and incorrect class decisions (Goodfellow et al., 2016) | Classification tasks |
| MAE / RMSE | Absolute or squared deviations in the target's units (Hyndman & Koehler, 2006) | Regression on one scale |
| MASE | Errors scaled by a naive forecast (Hyndman & Koehler, 2006) | Comparing across scales |
| BLEU | n-gram overlap with references (Papineni et al., 2002) | Machine translation |
| Calibration measures | Agreement of confidence with accuracy (Guo et al., 2017) | Probabilities used for decisions |

### In practice

The test set is used only once, at the end; all choices are made on validation data ([[ml-preprocessing|ML Preprocessing]]). Learning curves for training and validation are plotted to diagnose underfitting and overfitting (Goodfellow et al., 2016), and results are compared between models with appropriate statistical tests ([[model-comparison|Model Comparison]]).

### Key takeaway

Neural networks are evaluated with task-appropriate metrics on held-out data, training and validation curves show under- and overfitting, and predicted probabilities need a separate calibration check.

### Sources

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Zhang, C. et al. (2016). *Understanding deep learning requires rethinking generalization.* ICLR 2017. [arXiv:1611.03530](https://arxiv.org/abs/1611.03530)
- Belkin, M. et al. (2018). *Reconciling modern machine learning practice and the bias-variance trade-off.* PNAS 2019. [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [ACL Anthology](https://aclanthology.org/P02-1040/)
- Hyndman, R. J. & Koehler, A. B. (2006). *Another look at measures of forecast accuracy.* International Journal of Forecasting 22(4). [doi:10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein neuronales Netz zu evaluieren heißt zu messen, wie gut es auf Daten abschneidet, mit denen es nicht trainiert wurde, und zwar mit Metriken, die zur Aufgabe passen: Klassifikationsmetriken, Fehlermaße wie MAE und RMSE für Regression (Hyndman & Koehler, 2006) und Überlappungsmetriken wie BLEU für generierten Text (Papineni et al., 2002). Der Vergleich von Trainings- und Validierungsfehler zeigt Underfitting und Overfitting (Goodfellow et al., 2016), wobei große Netze sogar zufällige Labels auswendig lernen und auf echten Daten trotzdem generalisieren können (Zhang et al., 2016). Die vorhergesagten Wahrscheinlichkeiten moderner Netze sind oft schlecht kalibriert (Guo et al., 2017).

### Funktionsweise

Das Netz wird auf einer Trainingsmenge trainiert, während der Entwicklung auf einer Validierungsmenge beobachtet und einmalig auf einer zurückgehaltenen Testmenge evaluiert. Auf jeder Menge werden aufgabenspezifische Metriken berechnet, und der Abstand zwischen Trainings- und Validierungsergebnissen zeigt, ob das Modell unter- oder überangepasst ist.

```text
1. Metriken für Klassifikation
▼
2. Metriken für Regression
▼
3. Metriken für generierten Text
▼
4. Underfitting und Overfitting
▼
5. Generalisierung großer Netze
▼
6. Kalibrierung
```

#### 1. Metriken für Klassifikation

Die Metrik sollte zum Ziel der Anwendung passen: Accuracy bei ausgewogenen Problemen mit gleichen Fehlerkosten, Precision und Recall, wenn eine Fehlerart mehr zählt, und Coverage, wenn ein System auf eine Entscheidung verzichten darf (Goodfellow et al., 2016). Metriken auf Basis der Konfusionsmatrix und schwellenwertfreie Kurven beschreibt [[classification-metrics|Klassifikationsmetriken]].

#### 2. Metriken für Regression

Für numerische Vorhersagen sind skalenabhängige Maße wie der mittlere absolute Fehler (MAE) und die Wurzel aus dem mittleren quadratischen Fehler (RMSE) üblich; RMSE bestraft große Fehler stärker (Hyndman & Koehler, 2006). Prozentuale Fehler wie MAPE sind skalenfrei, können aber unendlich oder irreführend werden, wenn tatsächliche Werte null oder nahe null sind; der Mean Absolute Scaled Error (MASE) vermeidet das, indem er die Fehler durch die einer naiven Prognose skaliert.

#### 3. Metriken für generierten Text

Bei generiertem Text, etwa Übersetzungen, werden die Ausgaben mit Referenztexten verglichen. BLEU berechnet eine n-Gramm-Präzision mit Clipping bis zur Länge vier, kombiniert sie über das geometrische Mittel und wendet eine Längenstrafe an; auf Korpusebene korreliert BLEU mit menschlichen Urteilen (Papineni et al., 2002). Weitere lexikalische und Embedding-basierte Metriken behandelt [[text-similarity-metrics|Textähnlichkeitsmetriken]], die Evaluation großer Sprachmodelle [[llm-evaluation|LLM-Evaluation]].

#### 4. Underfitting und Overfitting

Ein Modell ist unteranpasst (Underfitting), wenn sein Trainingsfehler zu hoch ist, und überangepasst (Overfitting), wenn der Abstand zwischen Trainings- und Testfehler zu groß ist (Goodfellow et al., 2016). Beides hängt mit der Kapazität des Modells zusammen: Zu wenig Kapazität führt zu Underfitting, zu viel zu Overfitting. Wird der Validierungsfehler während des Trainings beobachtet, lässt sich Overfitting erkennen und früh abbrechen ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]).

#### 5. Generalisierung großer Netze

Zhang et al. (2016) zeigten, dass aktuelle konvolutionale Netze für Bildklassifikation eine zufällige Zuordnung der Trainingslabels problemlos lernen, auch mit expliziter Regularisierung und selbst dann, wenn die Bilder durch Zufallsrauschen ersetzt werden. Klassische Erklärungen über Modellfamilie oder Regularisierung erklären daher nicht, warum große Netze gut generalisieren. Belkin et al. (2018) bringen dies mit der Bias-Varianz-Abwägung über eine „Double Descent“-Kurve in Einklang: Der Testfehler folgt zunächst der klassischen U-Form, sinkt aber wieder, wenn die Kapazität über den Punkt hinaus wächst, an dem das Modell die Trainingsdaten exakt abbildet.

#### 6. Kalibrierung

Kalibrierung bedeutet, dass vorhergesagte Wahrscheinlichkeiten die tatsächliche Trefferwahrscheinlichkeit widerspiegeln. Moderne neuronale Netze sind anders als die von vor zehn Jahren schlecht kalibriert; Tiefe, Breite, Weight Decay und Batch Normalization beeinflussen das (Guo et al., 2017). Auf den meisten Datensätzen korrigierte Temperature Scaling, eine Variante von Platt Scaling mit einem einzigen Parameter, dies überraschend wirksam ([[ml-preprocessing|Preprocessing für Machine Learning]]).

#### Ursprung und Varianten

Goodfellow et al. (2016) beschreiben die klassische Sicht auf Generalisierung und die praktische Methodik des Deep Learning. Zhang et al. (2016) und Belkin et al. (2018) revidierten das Verständnis der Generalisierung großer Netze, Guo et al. (2017) zeigten ihre Fehlkalibrierung, und Aufgabenmetriken wie BLEU (Papineni et al., 2002) und MASE (Hyndman & Koehler, 2006) stammen aus Übersetzung und Prognose.

### Wann einsetzen

- Während des gesamten Trainings, um Underfitting und Overfitting anhand von Trainings- und Validierungskurven zu erkennen (Goodfellow et al., 2016).
- Wenn vorhergesagte Wahrscheinlichkeiten in Entscheidungen einfließen, um die Kalibrierung zu prüfen und zu korrigieren (Guo et al., 2017).
- Wenn Fehler bei numerischen Zielgrößen über Reihen oder Skalen hinweg verglichen werden sollen, mit skalenfreien Maßen (Hyndman & Koehler, 2006).

### Stärken und Grenzen

**Stärken**
- Trainings- und Validierungskurven liefern eine einfache Diagnose von Underfitting und Overfitting (Goodfellow et al., 2016).
- Temperature Scaling korrigiert die Kalibrierung mit einem Parameter (Guo et al., 2017).
- Standardmetriken wie BLEU machen Systeme auf Korpusebene vergleichbar (Papineni et al., 2002).

**Einschränkungen**
- Klassische Kapazitätsargumente erklären die Generalisierung großer Netze nicht (Zhang et al., 2016; Belkin et al., 2018).
- Prozentuale Fehlermaße können undefiniert oder irreführend sein (Hyndman & Koehler, 2006).
- Hohe Accuracy bedeutet keine kalibrierten Wahrscheinlichkeiten (Guo et al., 2017).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Klassifikationsmetriken | Zählen richtige und falsche Klassenentscheidungen (Goodfellow et al., 2016) | Klassifikationsaufgaben |
| MAE / RMSE | Absolute oder quadrierte Abweichungen in den Einheiten der Zielgröße (Hyndman & Koehler, 2006) | Regression auf einer Skala |
| MASE | Fehler skaliert durch eine naive Prognose (Hyndman & Koehler, 2006) | Vergleich über Skalen hinweg |
| BLEU | n-Gramm-Überlappung mit Referenzen (Papineni et al., 2002) | Maschinelle Übersetzung |
| Kalibrierungsmaße | Übereinstimmung von Konfidenz und Trefferquote (Guo et al., 2017) | Wahrscheinlichkeiten für Entscheidungen |

### In der Praxis

Die Testmenge wird nur einmal am Ende verwendet; alle Entscheidungen fallen auf Validierungsdaten ([[ml-preprocessing|Preprocessing für Machine Learning]]). Lernkurven für Training und Validierung werden aufgetragen, um Underfitting und Overfitting zu erkennen (Goodfellow et al., 2016), und Ergebnisse werden zwischen Modellen mit geeigneten statistischen Tests verglichen ([[model-comparison|Modellvergleiche]]).

### Merksatz

Neuronale Netze werden mit aufgabengerechten Metriken auf zurückgehaltenen Daten evaluiert, Trainings- und Validierungskurven zeigen Unter- und Überanpassung, und vorhergesagte Wahrscheinlichkeiten brauchen eine eigene Kalibrierungsprüfung.

### Quellen

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Zhang, C. et al. (2016). *Understanding deep learning requires rethinking generalization.* ICLR 2017. [arXiv:1611.03530](https://arxiv.org/abs/1611.03530)
- Belkin, M. et al. (2018). *Reconciling modern machine learning practice and the bias-variance trade-off.* PNAS 2019. [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [ACL Anthology](https://aclanthology.org/P02-1040/)
- Hyndman, R. J. & Koehler, A. B. (2006). *Another look at measures of forecast accuracy.* International Journal of Forecasting 22(4). [doi:10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)
