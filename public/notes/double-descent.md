---
title_en: Double Descent
title_de: Double Descent
entity_type: Concept
aliases:
- Double descent
- Deep double descent
- Interpolation threshold
sources:
- https://arxiv.org/abs/1812.11118
- https://arxiv.org/abs/1912.02292
- https://www.statlearning.com/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Double descent describes a test-error curve that first follows the classical U-shape of the [[bias-variance-tradeoff|bias-variance trade-off]], peaks around the "interpolation threshold" where a model can fit the training data exactly, and then falls a second time as capacity grows further, often below the earlier minimum (Belkin et al., 2019). Belkin et al. (2019) named it and showed it for random features, neural networks and random forests; Nakkiran et al. (2019) found it in modern deep networks such as ResNets and Transformers, not only as a function of model size but also of training epochs, and showed regimes where more training data hurts. It does not contradict the bias-variance trade-off: parameter count simply does not capture the real flexibility of interpolating models, and well-regularised models usually avoid the peak (James et al., 2023).

### How it works

```text
test error
  │╲              peak at interpolation threshold
  │ ╲      ╱╲     (training error reaches ~0)
  │  ╲__╱    ╲
  │  sweet     ╲_______  second descent: "modern" interpolating regime
  │  spot
  └──────────────┼──────────────────────→ capacity (parameters, width, epochs)
     classical   │  over-parameterised
     U-shape     n ≈ capacity
```

#### 1. The classical regime

Below the interpolation threshold, capacity behaves as textbooks predict: too little capacity under-fits, too much over-fits, and the best test error lies at a "sweet spot" in between ([[overfitting|overfitting]]; Belkin et al., 2019). The textbook corollary is that a model with zero training error is overfit and will generalise poorly (Belkin et al., 2019).

#### 2. The interpolation threshold

When capacity is just large enough to fit the n training points exactly, there is essentially one way to do it, and that solution can be wild: in James et al.'s example, a natural spline with 20 degrees of freedom on 20 points interpolates the data with large excursions, and test error is very high (James et al., 2023).

#### 3. The second descent

Beyond the threshold, many functions fit the training data perfectly, and the learning procedure picks a particular one. With a minimum-norm choice, the fit becomes smoother as capacity grows; the splines with 42 and 80 degrees of freedom are much less wild than the one with 20 (James et al., 2023). Belkin et al. (2019) explain the second descent as an inductive bias towards smooth, small-norm solutions, a form of Occam's razor, which gradient descent and averaging in random forests also provide.

#### 4. Deep double descent

Nakkiran et al. (2019) observed the peak for convolutional networks, ResNets and Transformers, both when varying model width ("model-wise") and when training longer ("epoch-wise"), most strongly with label noise but also in some settings without it. They define an effective model complexity, the largest number of samples a training procedure can fit to near-zero training error, and conjecture that test error behaves unpredictably when this complexity is close to the number of training samples; in that regime, more data can even hurt, as with Transformers on IWSLT'14 German–English translation (Nakkiran et al., 2019).

#### Origin and variants

Similar curves had been observed earlier, but Belkin et al. (2019) postulated the phenomenon in general and named it; they argue it was overlooked because classical statistics used fixed, small feature sets and regularisation masks the peak. Nakkiran et al. (2019), from Harvard University and [[openai|OpenAI]], extended it to deep learning. The textbook by James et al. (2023) explains it with splines and places it in the bias-variance framework.

### When to use it

- Explaining why very large [[neural-networks|neural networks]] trained to near-zero training error can still generalise well (Belkin et al., 2019).
- Diagnosing surprising behaviour: a test-error spike when model size, training time or data size crosses a critical point (Nakkiran et al., 2019).
- Not as a design target: in practice regularisation or early stopping usually gives good results without relying on the second descent (James et al., 2023).

### Strengths and limitations

**Strengths**
- Reconciles the classical U-shaped curve with the practice of training very large models to zero training error (Belkin et al., 2019).
- Observed across model families and datasets, from random features and random forests to ResNets and Transformers (Belkin et al., 2019; Nakkiran et al., 2019).

**Limitations**
- The deep-learning version rests on an informal hypothesis and empirical evidence, not a full theory (Nakkiran et al., 2019).
- The effect depends on how capacity is measured; parameter count is a poor proxy for flexibility (James et al., 2023).
- Optimal early stopping often removes the peak, although Nakkiran et al. (2019) found one setting where model-wise double descent remained.

### Comparison

| | Classical bias-variance view | Double descent |
|---|---|---|
| Shape of test error over capacity | U-shape | U-shape, peak at interpolation threshold, second descent |
| Zero training error | sign of overfitting | can generalise well beyond the threshold |
| Best model | at the sweet spot | often in the over-parameterised regime |
| Role of regularisation | controls variance | also smooths out the peak |

Sources: Belkin et al. (2019); James et al. (2023).

### In practice

When a model gets worse as it grows slightly, or as more data is added, check whether it sits near the interpolation threshold and whether the labels are noisy before drawing conclusions (Nakkiran et al., 2019). Tune regularisation and early stopping with validation data rather than relying on the second descent; James et al. (2023) note that a ridge-regularised spline would have beaten all interpolating fits in their example ([[regularisation-and-hyperparameters|regularisation and hyperparameters]], [[neural-network-evaluation|neural network evaluation]]).

### Key takeaway

Past the point where a model fits its training data exactly, test error can fall again; double descent refines, rather than refutes, the bias-variance trade-off.

### Sources

- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
- Nakkiran, P., Kaplun, G., Bansal, Y., Yang, T., Barak, B. & Sutskever, I. (2019). Deep Double Descent: Where Bigger Models and More Data Hurt. [arXiv:1912.02292](https://arxiv.org/abs/1912.02292)
- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, section 10.8. Springer. [statlearning.com](https://www.statlearning.com/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Double Descent beschreibt eine Kurve des Testfehlers, die zunächst der klassischen U-Form des [[bias-variance-tradeoff|Bias-Varianz-Dilemmas]] folgt, um die „Interpolationsschwelle“, an der ein Modell die Trainingsdaten exakt abbilden kann, einen Höhepunkt erreicht und dann bei weiter wachsender Kapazität ein zweites Mal sinkt, oft unter das frühere Minimum (Belkin et al., 2019). Belkin et al. (2019) gaben dem Phänomen seinen Namen und zeigten es für Random Features, neuronale Netze und Random Forests; Nakkiran et al. (2019) fanden es in modernen tiefen Netzen wie ResNets und Transformern, nicht nur in Abhängigkeit von der Modellgröße, sondern auch von der Zahl der Trainingsepochen, und zeigten Bereiche, in denen mehr Trainingsdaten schaden. Es widerspricht dem Bias-Varianz-Dilemma nicht: Die Zahl der Parameter erfasst die tatsächliche Flexibilität interpolierender Modelle schlicht nicht, und gut regularisierte Modelle vermeiden den Höhepunkt meist (James et al., 2023).

### Funktionsweise

```text
Testfehler
  │╲              Höhepunkt an der Interpolationsschwelle
  │ ╲      ╱╲     (Trainingsfehler erreicht ~0)
  │  ╲__╱    ╲
  │  Optimum   ╲_______  zweiter Abstieg: „moderner“ interpolierender Bereich
  │  (klassisch)
  └──────────────┼──────────────────────→ Kapazität (Parameter, Breite, Epochen)
     klassische  │  überparametrisiert
     U-Form      n ≈ Kapazität
```

#### 1. Der klassische Bereich

Unterhalb der Interpolationsschwelle verhält sich die Kapazität wie im Lehrbuch: Zu wenig Kapazität führt zu Underfitting, zu viel zu Overfitting, und der beste Testfehler liegt an einem Optimum dazwischen ([[overfitting|Overfitting]]; Belkin et al., 2019). Die Lehrbuchfolgerung lautet, dass ein Modell ohne Trainingsfehler überangepasst ist und schlecht generalisiert (Belkin et al., 2019).

#### 2. Die Interpolationsschwelle

Reicht die Kapazität gerade aus, um die n Trainingspunkte exakt abzubilden, gibt es dafür im Wesentlichen nur einen Weg, und diese Lösung kann stark ausschlagen: Im Beispiel von James et al. interpoliert ein natürlicher Spline mit 20 Freiheitsgraden die 20 Datenpunkte mit großen Ausschlägen, und der Testfehler ist sehr hoch (James et al., 2023).

#### 3. Der zweite Abstieg

Jenseits der Schwelle passen viele Funktionen perfekt zu den Trainingsdaten, und das Lernverfahren wählt eine bestimmte aus. Bei Wahl der Lösung mit minimaler Norm wird die Anpassung mit wachsender Kapazität glatter; die Splines mit 42 und 80 Freiheitsgraden schlagen viel weniger aus als der mit 20 (James et al., 2023). Belkin et al. (2019) erklären den zweiten Abstieg mit einer induktiven Verzerrung hin zu glatten Lösungen mit kleiner Norm, einer Form von Ockhams Rasiermesser, die auch das Gradientenverfahren und die Mittelung in Random Forests liefern.

#### 4. Deep Double Descent

Nakkiran et al. (2019) beobachteten den Höhepunkt bei Convolutional Networks, ResNets und Transformern, sowohl bei variierender Modellbreite („model-wise“) als auch bei längerem Training („epoch-wise“), am deutlichsten mit Label-Rauschen, in einigen Fällen aber auch ohne. Sie definieren eine effektive Modellkomplexität, die größte Zahl von Beispielen, die ein Trainingsverfahren mit nahezu null Trainingsfehler abbilden kann, und vermuten, dass sich der Testfehler unvorhersehbar verhält, wenn diese Komplexität nahe an der Zahl der Trainingsbeispiele liegt; in diesem Bereich können mehr Daten sogar schaden, etwa bei Transformern für die Übersetzung Deutsch–Englisch auf IWSLT'14 (Nakkiran et al., 2019).

#### Herkunft und Varianten

Ähnliche Kurven waren schon früher beobachtet worden, doch Belkin et al. (2019) formulierten das Phänomen allgemein und benannten es; sie vermuten, dass es übersehen wurde, weil die klassische Statistik mit festen, kleinen Merkmalsmengen arbeitete und Regularisierung den Höhepunkt verdeckt. Nakkiran et al. (2019) von der Harvard University und [[openai|OpenAI]] übertrugen es auf Deep Learning. Das Lehrbuch von James et al. (2023) erklärt es mit Splines und ordnet es in das Bias-Varianz-Dilemma ein.

### Wann einsetzen

- Um zu erklären, warum sehr große [[neural-networks|neuronale Netze]], die bis fast null Trainingsfehler trainiert werden, trotzdem gut generalisieren können (Belkin et al., 2019).
- Zur Diagnose überraschenden Verhaltens: ein Anstieg des Testfehlers, wenn Modellgröße, Trainingsdauer oder Datenmenge einen kritischen Punkt überschreiten (Nakkiran et al., 2019).
- Nicht als Entwurfsziel: In der Praxis liefern Regularisierung oder Early Stopping meist gute Ergebnisse, ohne sich auf den zweiten Abstieg zu verlassen (James et al., 2023).

### Stärken und Grenzen

**Stärken**
- Versöhnt die klassische U-Kurve mit der Praxis, sehr große Modelle bis null Trainingsfehler zu trainieren (Belkin et al., 2019).
- Über Modellfamilien und Datensätze hinweg beobachtet, von Random Features und Random Forests bis zu ResNets und Transformern (Belkin et al., 2019; Nakkiran et al., 2019).

**Grenzen**
- Die Deep-Learning-Variante beruht auf einer informellen Hypothese und empirischen Befunden, nicht auf einer vollständigen Theorie (Nakkiran et al., 2019).
- Der Effekt hängt davon ab, wie Kapazität gemessen wird; die Zahl der Parameter ist ein schlechtes Maß für Flexibilität (James et al., 2023).
- Optimales Early Stopping beseitigt den Höhepunkt oft, auch wenn Nakkiran et al. (2019) einen Fall fanden, in dem Double Descent über die Modellgröße bestehen blieb.

### Vergleich

| | Klassische Bias-Varianz-Sicht | Double Descent |
|---|---|---|
| Form des Testfehlers über der Kapazität | U-Form | U-Form, Höhepunkt an der Interpolationsschwelle, zweiter Abstieg |
| Kein Trainingsfehler | Zeichen für Overfitting | kann jenseits der Schwelle gut generalisieren |
| Bestes Modell | am Optimum der U-Kurve | oft im überparametrisierten Bereich |
| Rolle der Regularisierung | begrenzt die Varianz | glättet auch den Höhepunkt |

Quellen: Belkin et al. (2019); James et al. (2023).

### In der Praxis

Wird ein Modell schlechter, wenn es etwas wächst oder mehr Daten erhält, lohnt vor weiteren Schlüssen die Prüfung, ob es nahe der Interpolationsschwelle liegt und ob die Labels verrauscht sind (Nakkiran et al., 2019). Regularisierung und Early Stopping sollten mit Validierungsdaten abgestimmt werden, statt sich auf den zweiten Abstieg zu verlassen; James et al. (2023) merken an, dass in ihrem Beispiel ein mit Ridge regularisierter Spline alle interpolierenden Anpassungen geschlagen hätte ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]], [[neural-network-evaluation|Evaluation neuronaler Netze]]).

### Merksatz

Jenseits des Punkts, an dem ein Modell seine Trainingsdaten exakt abbildet, kann der Testfehler wieder sinken; Double Descent verfeinert das Bias-Varianz-Dilemma, statt es zu widerlegen.

### Quellen

- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
- Nakkiran, P., Kaplun, G., Bansal, Y., Yang, T., Barak, B. & Sutskever, I. (2019). Deep Double Descent: Where Bigger Models and More Data Hurt. [arXiv:1912.02292](https://arxiv.org/abs/1912.02292)
- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, Abschnitt 10.8. Springer. [statlearning.com](https://www.statlearning.com/)
