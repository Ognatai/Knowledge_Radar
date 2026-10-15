---
title_en: Temperature Scaling
title_de: Temperature Scaling
entity_type: Method
aliases:
- Temperature scaling
- Softmax temperature
sources:
- https://arxiv.org/abs/1706.04599
- https://arxiv.org/abs/1503.02531
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Temperature scaling calibrates a trained classification network by dividing its logits by a single scalar T > 0 before the softmax; T is fitted by minimising the negative log-likelihood on a validation set, and because it does not change which class has the highest score, accuracy stays the same (Guo et al., 2017). Guo et al. (2017) found that modern deep networks are overconfident and that this one-parameter variant of [[platt-scaling|Platt scaling]] was the most effective post-hoc calibration method on the vision datasets they tested, beating [[isotonic-regression|isotonic regression]], histogram binning and more general matrix and vector scaling. The same temperature-softened softmax is used in [[knowledge-distillation|knowledge distillation]] to produce soft targets (Hinton et al., 2015).

### How it works

```text
trained network → logits z (one per class)
  softmax(z / T):  T = 1 → original probabilities
                   T > 1 → softer, higher entropy (less confident)
                   T → ∞ → uniform 1/K;   T → 0 → all mass on the top class
fit T on validation set by minimising NLL (1-D convex problem)
argmax unchanged → same predictions, calibrated confidences
```

#### 1. Why modern networks need it

A network is calibrated when its confidence matches the probability of being correct; Guo et al. (2017) showed that a 5-layer LeNet on CIFAR-100 was well calibrated, while a 110-layer [[resnet|ResNet]] was more accurate but substantially overconfident. Depth, width, weight decay and batch normalisation influence calibration, and networks can overfit the negative log-likelihood without [[overfitting|overfitting]] the 0/1 loss: on CIFAR-100, test error kept falling from 29% to 27% while NLL already overfitted (Guo et al., 2017).

#### 2. The temperature

The softmax computes q_i = exp(z_i/T) / Σ_j exp(z_j/T) from the logits z; T is normally 1, and a higher T gives a softer distribution over classes (Hinton et al., 2015). For calibration, the new confidence is the maximum of softmax(z/T); with T > 1 the output entropy rises, as T grows without bound the probability approaches 1/K for K classes, and as T approaches 0 it collapses to a point mass (Guo et al., 2017).

#### 3. Fitting on held-out data

T is optimised with respect to NLL on a validation set that can be the same set used for hyperparameter tuning; it is a one-dimensional convex problem that a conjugate gradient solver solves in about ten iterations (Guo et al., 2017). In Torch7, the authors implemented it as a constant multiplication of the logits by 1/T, set to 1 during training and fitted afterwards (Guo et al., 2017).

#### 4. Family of scaling methods

Matrix scaling applies a linear transformation Wz + b to the logits and vector scaling restricts W to a diagonal matrix; temperature scaling, the simplest extension of Platt scaling, uses one scalar for all classes (Guo et al., 2017). Vector scaling learned nearly constant entries and thus essentially recovered temperature scaling, which suggests that network miscalibration is intrinsically low-dimensional (Guo et al., 2017).

#### Origin and variants

Hinton et al. (2015) raised the softmax temperature to transfer knowledge from a large model to a small one. Guo et al. (2017), from Cornell University, proposed using a single temperature for calibration and reported no prior use of temperature scaling for calibrating probabilistic models. In language models, a temperature parameter also controls how random sampling is ([[large-language-models|large language models]]), which is a different use of the same softmax.

### When to use it

- Calibrating the confidence of a trained multiclass [[neural-networks|neural network]] when predictions feed into decisions, for example handing control to a human when confidence is low (Guo et al., 2017).
- When only a small validation set is available, since one parameter is unlikely to overfit (Guo et al., 2017).
- Not to fix accuracy problems: the predicted class does not change (Guo et al., 2017).

### Strengths and limitations

**Strengths**
- One parameter, the fastest of the methods tested, and simple to add between logits and softmax (Guo et al., 2017).
- Leaves accuracy untouched because the argmax does not change (Guo et al., 2017).
- Most effective on the vision tasks tested: for a 110-layer ResNet on CIFAR-100, expected calibration error fell from 16.53% to 1.26% (Guo et al., 2017).

**Limitations**
- Uses the same temperature for all classes; vector and matrix scaling add per-class parameters but did not do better in the experiments (Guo et al., 2017).
- Comparable to, not better than, other methods on the NLP datasets tested, and it did not improve the already well-calibrated Reuters model (Guo et al., 2017).
- Like all post-hoc methods, it needs a hold-out validation set (Guo et al., 2017; [[neural-network-evaluation|neural network evaluation]]).

### Comparison

| Method | Parameters | Changes predictions? | ECE, ResNet-110 on CIFAR-100 |
|---|---|---|---|
| Uncalibrated | – | – | 16.53% |
| Histogram binning | one value per bin | can change them | 2.66% |
| Isotonic regression | non-parametric | can change them | 4.99% |
| Temperature scaling | 1 | no | 1.26% |
| Matrix scaling | K² + K | yes | 25.49% |

Source: Guo et al. (2017), Table 1 (ECE with 15 bins).

### In practice

Fit T once after training on the validation split and store it with the model; check the result with a reliability diagram and expected calibration error, which averages the gap between accuracy and confidence over bins (Guo et al., 2017; [[classification-metrics|classification metrics]]). Because accuracy does not change, temperature scaling can be added to an existing model without retraining or re-evaluating its accuracy ([[classification|classification]], [[ml-preprocessing|ML preprocessing]]).

### Key takeaway

Dividing the logits by one fitted temperature makes overconfident deep networks calibrated without changing their predictions; for neural classifiers it is usually the first calibration method to try.

### Sources

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- Hinton, G., Vinyals, O. & Dean, J. (2015). Distilling the Knowledge in a Neural Network. [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Temperature Scaling kalibriert ein trainiertes Klassifikationsnetz, indem seine Logits vor der Softmax durch einen einzigen Skalar T > 0 geteilt werden; T wird durch Minimieren der negativen Log-Likelihood auf einer Validierungsmenge angepasst, und weil sich nicht ändert, welche Klasse den höchsten Wert hat, bleibt die Accuracy gleich (Guo et al., 2017). Guo et al. (2017) stellten fest, dass moderne tiefe Netze zu selbstsicher sind und dass diese Variante von [[platt-scaling|Platt Scaling]] mit einem Parameter auf den getesteten Bilddatensätzen das wirksamste nachträgliche Kalibrierungsverfahren war, besser als [[isotonic-regression|isotone Regression]], Histogram Binning und die allgemeineren Verfahren Matrix und Vector Scaling. Dieselbe durch eine Temperatur abgeschwächte Softmax wird bei der [[knowledge-distillation|Knowledge Distillation]] genutzt, um weiche Zielwerte zu erzeugen (Hinton et al., 2015).

### Funktionsweise

```text
trainiertes Netz → Logits z (eins je Klasse)
  softmax(z / T):  T = 1 → ursprüngliche Wahrscheinlichkeiten
                   T > 1 → weicher, höhere Entropie (weniger selbstsicher)
                   T → ∞ → gleichverteilt 1/K;   T → 0 → gesamte Masse auf der besten Klasse
T auf Validierungsmenge durch Minimieren der NLL anpassen (eindimensionales konvexes Problem)
argmax unverändert → gleiche Vorhersagen, kalibrierte Konfidenzen
```

#### 1. Warum moderne Netze es brauchen

Ein Netz ist kalibriert, wenn seine Konfidenz der Wahrscheinlichkeit entspricht, richtig zu liegen; Guo et al. (2017) zeigten, dass ein LeNet mit 5 Schichten auf CIFAR-100 gut kalibriert war, während ein [[resnet|ResNet]] mit 110 Schichten genauer, aber deutlich zu selbstsicher war. Tiefe, Breite, Weight Decay und Batch Normalization beeinflussen die Kalibrierung, und Netze können sich an die negative Log-Likelihood überanpassen, ohne sich an den 0/1-Verlust überanzupassen: Auf CIFAR-100 sank der Testfehler weiter von 29 % auf 27 %, während die NLL bereits überangepasst war (Guo et al., 2017).

#### 2. Die Temperatur

Die Softmax berechnet q_i = exp(z_i/T) / Σ_j exp(z_j/T) aus den Logits z; T ist normalerweise 1, und ein höheres T ergibt eine weichere Verteilung über die Klassen (Hinton et al., 2015). Zur Kalibrierung ist die neue Konfidenz das Maximum von softmax(z/T); mit T > 1 steigt die Entropie der Ausgabe, wächst T unbegrenzt, nähert sich die Wahrscheinlichkeit 1/K für K Klassen, und geht T gegen 0, fällt sie auf eine Punktmasse zusammen (Guo et al., 2017).

#### 3. Anpassung auf zurückgehaltenen Daten

T wird bezüglich der NLL auf einer Validierungsmenge optimiert, die dieselbe sein kann wie für die Abstimmung der Hyperparameter; es ist ein eindimensionales konvexes Problem, das ein Conjugate-Gradient-Verfahren in etwa zehn Iterationen löst (Guo et al., 2017). In Torch7 setzten die Autoren es als konstante Multiplikation der Logits mit 1/T um, beim Training auf 1 gesetzt und danach angepasst (Guo et al., 2017).

#### 4. Familie der Skalierungsverfahren

Matrix Scaling wendet eine lineare Transformation Wz + b auf die Logits an, und Vector Scaling beschränkt W auf eine Diagonalmatrix; Temperature Scaling, die einfachste Erweiterung von Platt Scaling, nutzt einen Skalar für alle Klassen (Guo et al., 2017). Vector Scaling lernte nahezu konstante Einträge und fand damit im Wesentlichen Temperature Scaling wieder, was darauf hindeutet, dass die Fehlkalibrierung von Netzen von Natur aus niedrigdimensional ist (Guo et al., 2017).

#### Herkunft und Varianten

Hinton et al. (2015) erhöhten die Softmax-Temperatur, um Wissen von einem großen auf ein kleines Modell zu übertragen. Guo et al. (2017) von der Cornell University schlugen vor, eine einzige Temperatur zur Kalibrierung zu nutzen, und kannten keine frühere Verwendung von Temperature Scaling zur Kalibrierung probabilistischer Modelle. Bei Sprachmodellen steuert ein Temperaturparameter außerdem, wie zufällig das Sampling ist ([[large-language-models|große Sprachmodelle]]), eine andere Verwendung derselben Softmax.

### Wann einsetzen

- Zur Kalibrierung der Konfidenz eines trainierten [[neural-networks|neuronalen Netzes]] für mehrere Klassen, wenn Vorhersagen in Entscheidungen einfließen, etwa die Übergabe an einen Menschen bei geringer Konfidenz (Guo et al., 2017).
- Wenn nur eine kleine Validierungsmenge vorliegt, da ein einzelner Parameter kaum überanpasst (Guo et al., 2017).
- Nicht, um Probleme mit der Accuracy zu beheben: Die vorhergesagte Klasse ändert sich nicht (Guo et al., 2017).

### Stärken und Grenzen

**Stärken**
- Ein Parameter, das schnellste der getesteten Verfahren und einfach zwischen Logits und Softmax einzufügen (Guo et al., 2017).
- Lässt die Accuracy unberührt, weil sich das argmax nicht ändert (Guo et al., 2017).
- Am wirksamsten bei den getesteten Bildaufgaben: Für ein ResNet mit 110 Schichten auf CIFAR-100 sank der erwartete Kalibrierungsfehler von 16,53 % auf 1,26 % (Guo et al., 2017).

**Grenzen**
- Nutzt für alle Klassen dieselbe Temperatur; Vector und Matrix Scaling ergänzen Parameter je Klasse, schnitten in den Experimenten aber nicht besser ab (Guo et al., 2017).
- Auf den getesteten NLP-Datensätzen vergleichbar mit, aber nicht besser als andere Verfahren, und das bereits gut kalibrierte Reuters-Modell verbesserte es nicht (Guo et al., 2017).
- Wie alle nachträglichen Verfahren braucht es eine zurückgehaltene Validierungsmenge (Guo et al., 2017; [[neural-network-evaluation|Evaluation neuronaler Netze]]).

### Vergleich

| Verfahren | Parameter | Ändert Vorhersagen? | ECE, ResNet-110 auf CIFAR-100 |
|---|---|---|---|
| Unkalibriert | – | – | 16,53 % |
| Histogram Binning | ein Wert je Bin | kann sie ändern | 2,66 % |
| Isotone Regression | nichtparametrisch | kann sie ändern | 4,99 % |
| Temperature Scaling | 1 | nein | 1,26 % |
| Matrix Scaling | K² + K | ja | 25,49 % |

Quelle: Guo et al. (2017), Tabelle 1 (ECE mit 15 Bins).

### In der Praxis

T wird einmal nach dem Training auf der Validierungsmenge angepasst und mit dem Modell gespeichert; das Ergebnis wird mit einem Reliability-Diagramm und dem erwarteten Kalibrierungsfehler geprüft, der die Lücke zwischen Accuracy und Konfidenz über Bins mittelt (Guo et al., 2017; [[classification-metrics|Klassifikationsmetriken]]). Weil sich die Accuracy nicht ändert, lässt sich Temperature Scaling einem bestehenden Modell hinzufügen, ohne es neu zu trainieren oder seine Accuracy neu zu evaluieren ([[classification|Klassifikation]], [[ml-preprocessing|ML-Vorverarbeitung]]).

### Merksatz

Teilt man die Logits durch eine angepasste Temperatur, werden zu selbstsichere tiefe Netze kalibriert, ohne dass sich ihre Vorhersagen ändern; für neuronale Klassifikatoren ist es meist das erste Kalibrierungsverfahren, das sich lohnt.

### Quellen

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- Hinton, G., Vinyals, O. & Dean, J. (2015). Distilling the Knowledge in a Neural Network. [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
