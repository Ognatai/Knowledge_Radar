---
title_en: Bias-Variance Trade-off
title_de: Bias-Varianz-Dilemma
entity_type: Concept
aliases:
- Bias-variance trade-off
- Bias-variance tradeoff
- Bias-variance decomposition
- Bias-Varianz-Zerlegung
sources:
- https://www.statlearning.com/
- https://www.deeplearningbook.org/contents/ml.html
- https://arxiv.org/abs/1812.11118
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The expected test error of a model at a point can be split into three parts: the variance of the model's prediction across training sets, its squared bias, and the irreducible error from noise (James et al., 2023). Variance is how much the fitted model would change on a different training set; bias is the error from approximating a complicated problem with a simpler model. More flexible methods generally have lower bias and higher variance, so the test error first falls and then rises with flexibility, the familiar U-shape (James et al., 2023). Balancing the two is the bias-variance trade-off; in practice it is usually negotiated with cross-validation (Goodfellow et al., 2016). Heavily overparameterised models can show a second descent of the test error beyond the point where they fit the training data exactly ("double descent", Belkin et al., 2019).

### How it works

```text
expected test MSE at x₀ = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε)
                            variance       squared bias   irreducible error

flexibility ↑  →  bias ↓ , variance ↑
test error = sum of both (+ noise floor) → U-shape, minimum at intermediate flexibility
```

#### 1. The decomposition

For a given input x₀, the expected test mean squared error, averaged over many training sets drawn from the same distribution, equals the variance of the prediction f̂(x₀), plus its squared bias, plus the variance of the error term ε (James et al., 2023). Both variance and squared bias are non-negative, so the expected test error can never fall below Var(ε), the irreducible error (James et al., 2023). For estimators of a parameter, the same relationship reads MSE = Bias² + Var (Goodfellow et al., 2016).

#### 2. Variance

Variance is the amount by which the fitted model would change if it were estimated on a different training set (James et al., 2023). A flexible curve that follows the observations closely has high variance, because changing a single data point can change the estimate considerably; a least-squares line is inflexible and has low variance (James et al., 2023).

#### 3. Bias

Bias is the error introduced by approximating a real-life problem, which may be very complicated, with a much simpler model (James et al., 2023). Linear regression assumes a linear relationship; if the true function is strongly non-linear, no amount of training data makes the linear estimate accurate (James et al., 2023).

#### 4. The trade-off

As flexibility increases, bias usually decreases faster than variance increases at first, so the test error falls; at some point more flexibility barely reduces bias but strongly increases variance, and the test error rises (James et al., 2023). It is easy to get very low bias with high variance, for example with a curve through every training point, or very low variance with high bias, for example with a horizontal line; the challenge is to make both low (James et al., 2023). The relationship mirrors capacity, underfitting and [[overfitting|overfitting]]: increasing capacity tends to increase variance and decrease bias (Goodfellow et al., 2016).

#### 5. Example: k in k-nearest neighbours

With K = 1, a k-nearest-neighbours classifier has zero training error, low bias and very high variance; with K = 100 its decision boundary is close to linear, with low variance and high bias (James et al., 2023). In the book's simulated example, test error is U-shaped in 1/K with a minimum around K = 10 ([[k-nearest-neighbours|k-nearest neighbours]]).

#### Origin and variants

The trade-off also applies to evaluation procedures: in k-fold [[cross-validation|cross-validation]], leave-one-out has low bias but high variance because its training sets overlap almost completely, which is why k = 5 or k = 10 is typical (James et al., 2023). Belkin et al. (2019) argued that the classical trade-off seems at odds with modern practice, in which very rich models such as [[neural-networks|neural networks]] interpolate the training data and still reach high test accuracy, and proposed a "double descent" curve that subsumes the U-shape: beyond the interpolation threshold, more capacity improves performance again. James et al. (2023) show double descent with minimum-norm natural splines and stress that it does not contradict the trade-off: the number of parameters does not capture the true flexibility of interpolating models, and regularised methods typically do not interpolate and do not show double descent.

### When to use it

- Choosing model flexibility or hyperparameters such as k, tree depth or regularisation strength ([[regularisation-and-hyperparameters|regularisation and hyperparameters]]).
- Explaining why a more complex model does not automatically beat a simpler one: if the true function is linear, linear regression has no bias and is hard to beat (James et al., 2023).
- Designing evaluation: the choice of k in cross-validation is itself a bias-variance trade-off (James et al., 2023).

### Strengths and limitations

**Strengths**
- Gives a clear vocabulary for the two sources of error and the noise floor (James et al., 2023).
- Explains the U-shaped test error curve and why validation data is needed (Goodfellow et al., 2016).

**Limitations**
- In real problems the true function is unknown, so bias and variance cannot be computed explicitly (James et al., 2023).
- The clean decomposition holds for squared error; for other losses it is less direct.
- Model size measured in parameters is a poor proxy for flexibility in overparameterised models, where double descent appears (Belkin et al., 2019; James et al., 2023).

### Comparison

| | High bias | High variance |
|---|---|---|
| Typical model | too simple, e.g. a straight line for a curved relation | too flexible, e.g. K = 1 nearest neighbour |
| Training error | high | very low |
| Test error | high | high |
| Symptom | [[overfitting|underfitting]] | [[overfitting|overfitting]] |

Source: James et al. (2023).

### In practice

Cross-validation is the most common way to negotiate the trade-off (Goodfellow et al., 2016). Regularisation lowers variance at the price of some bias; James et al. (2023) note that ridge-regularised splines with a well-chosen penalty would have given lower test error than the interpolating fits in their double-descent example. Learning curves that compare training and validation error show on which side of the trade-off a model sits ([[neural-network-evaluation|neural network evaluation]]).

### Key takeaway

Expected test error is variance plus squared bias plus irreducible noise; more flexibility lowers bias and raises variance, so the best model sits in between, and overparameterised models that interpolate are a special case worth knowing.

### Sources

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, sections 2.2.2, 5.1.4 and 10.8. Springer. [statlearning.com](https://www.statlearning.com/)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 5, section 5.4.4. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/ml.html)
- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der erwartete Testfehler eines Modells an einem Punkt lässt sich in drei Teile zerlegen: die Varianz der Vorhersage über verschiedene Trainingsmengen, den quadrierten Bias und den nicht reduzierbaren Fehler durch Rauschen (James et al., 2023). Varianz beschreibt, wie stark sich das angepasste Modell bei einer anderen Trainingsmenge ändern würde; Bias ist der Fehler, der entsteht, wenn ein kompliziertes Problem durch ein einfacheres Modell angenähert wird. Flexiblere Verfahren haben in der Regel weniger Bias und mehr Varianz, sodass der Testfehler mit wachsender Flexibilität erst sinkt und dann steigt, die bekannte U-Form (James et al., 2023). Beides auszubalancieren, ist das Bias-Varianz-Dilemma; in der Praxis wird es meist mit Kreuzvalidierung gelöst (Goodfellow et al., 2016). Stark überparametrisierte Modelle können jenseits des Punkts, an dem sie die Trainingsdaten exakt abbilden, einen zweiten Abfall des Testfehlers zeigen („Double Descent“, Belkin et al., 2019).

### Funktionsweise

```text
erwarteter Test-MSE an x₀ = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε)
                              Varianz        quadr. Bias      nicht reduzierbarer Fehler

Flexibilität ↑  →  Bias ↓ , Varianz ↑
Testfehler = Summe aus beidem (+ Rauschuntergrenze) → U-Form, Minimum bei mittlerer Flexibilität
```

#### 1. Die Zerlegung

Für eine Eingabe x₀ ist der erwartete mittlere quadratische Testfehler, gemittelt über viele Trainingsmengen aus derselben Verteilung, gleich der Varianz der Vorhersage f̂(x₀) plus ihrem quadrierten Bias plus der Varianz des Fehlerterms ε (James et al., 2023). Varianz und quadrierter Bias sind nicht negativ, daher kann der erwartete Testfehler nie unter Var(ε) fallen, den nicht reduzierbaren Fehler (James et al., 2023). Für Schätzer eines Parameters lautet derselbe Zusammenhang MSE = Bias² + Var (Goodfellow et al., 2016).

#### 2. Varianz

Varianz ist das Ausmaß, in dem sich das angepasste Modell ändern würde, wenn es auf einer anderen Trainingsmenge geschätzt würde (James et al., 2023). Eine flexible Kurve, die den Beobachtungen eng folgt, hat hohe Varianz, weil schon die Änderung eines einzelnen Datenpunkts die Schätzung stark verändern kann; eine Kleinste-Quadrate-Gerade ist unflexibel und hat geringe Varianz (James et al., 2023).

#### 3. Bias

Bias ist der Fehler, der entsteht, wenn ein reales, möglicherweise sehr kompliziertes Problem durch ein viel einfacheres Modell angenähert wird (James et al., 2023). Lineare Regression nimmt einen linearen Zusammenhang an; ist die wahre Funktion stark nichtlinear, macht keine noch so große Datenmenge die lineare Schätzung genau (James et al., 2023).

#### 4. Das Dilemma

Mit wachsender Flexibilität sinkt der Bias anfangs meist schneller, als die Varianz steigt, sodass der Testfehler fällt; ab einem Punkt verringert mehr Flexibilität den Bias kaum noch, erhöht aber die Varianz deutlich, und der Testfehler steigt (James et al., 2023). Sehr geringen Bias bei hoher Varianz erreicht man leicht, etwa mit einer Kurve durch jeden Trainingspunkt, ebenso sehr geringe Varianz bei hohem Bias, etwa mit einer horizontalen Linie; die Herausforderung ist, beides niedrig zu halten (James et al., 2023). Der Zusammenhang entspricht Kapazität, Underfitting und [[overfitting|Overfitting]]: Mehr Kapazität erhöht tendenziell die Varianz und senkt den Bias (Goodfellow et al., 2016).

#### 5. Beispiel: k bei k-nächsten Nachbarn

Mit K = 1 hat ein k-Nächste-Nachbarn-Klassifikator null Trainingsfehler, geringen Bias und sehr hohe Varianz; mit K = 100 ist seine Entscheidungsgrenze nahezu linear, mit geringer Varianz und hohem Bias (James et al., 2023). Im simulierten Beispiel des Buchs ist der Testfehler in 1/K U-förmig mit einem Minimum um K = 10 ([[k-nearest-neighbours|k-nächste Nachbarn]]).

#### Herkunft und Varianten

Das Dilemma gilt auch für Evaluationsverfahren: Bei der k-fachen [[cross-validation|Kreuzvalidierung]] hat Leave-one-out geringen Bias, aber hohe Varianz, weil sich seine Trainingsmengen fast vollständig überschneiden; deshalb sind k = 5 oder k = 10 üblich (James et al., 2023). Belkin et al. (2019) argumentierten, dass das klassische Dilemma im Widerspruch zur modernen Praxis zu stehen scheint, in der sehr ausdrucksstarke Modelle wie [[neural-networks|neuronale Netze]] die Trainingsdaten interpolieren und trotzdem eine hohe Testgenauigkeit erreichen, und schlugen eine „Double Descent“-Kurve vor, die die U-Form einschließt: Jenseits der Interpolationsschwelle verbessert mehr Kapazität die Leistung wieder. James et al. (2023) zeigen Double Descent mit Minimum-Norm-Natural-Splines und betonen, dass es dem Dilemma nicht widerspricht: Die Zahl der Parameter erfasst die tatsächliche Flexibilität interpolierender Modelle nicht, und regularisierte Verfahren interpolieren typischerweise nicht und zeigen kein Double Descent.

### Wann einsetzen

- Wahl der Modellflexibilität oder von Hyperparametern wie k, Baumtiefe oder Regularisierungsstärke ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]).
- Erklären, warum ein komplexeres Modell ein einfacheres nicht automatisch schlägt: Ist die wahre Funktion linear, hat lineare Regression keinen Bias und ist schwer zu schlagen (James et al., 2023).
- Gestaltung der Evaluation: Die Wahl von k bei der Kreuzvalidierung ist selbst eine Bias-Varianz-Abwägung (James et al., 2023).

### Stärken und Grenzen

**Stärken**
- Liefert ein klares Vokabular für die beiden Fehlerquellen und die Rauschuntergrenze (James et al., 2023).
- Erklärt die U-förmige Testfehlerkurve und warum Validierungsdaten nötig sind (Goodfellow et al., 2016).

**Grenzen**
- Bei realen Problemen ist die wahre Funktion unbekannt, daher lassen sich Bias und Varianz nicht explizit berechnen (James et al., 2023).
- Die saubere Zerlegung gilt für den quadratischen Fehler; für andere Verlustfunktionen ist sie weniger direkt.
- Die Zahl der Parameter ist bei überparametrisierten Modellen, bei denen Double Descent auftritt, ein schlechtes Maß für Flexibilität (Belkin et al., 2019; James et al., 2023).

### Vergleich

| | Hoher Bias | Hohe Varianz |
|---|---|---|
| Typisches Modell | zu einfach, z. B. eine Gerade für einen gekrümmten Zusammenhang | zu flexibel, z. B. K = 1 nächster Nachbar |
| Trainingsfehler | hoch | sehr niedrig |
| Testfehler | hoch | hoch |
| Symptom | [[overfitting|Underfitting]] | [[overfitting|Overfitting]] |

Quelle: James et al. (2023).

### In der Praxis

Kreuzvalidierung ist der gängigste Weg, das Dilemma aufzulösen (Goodfellow et al., 2016). Regularisierung senkt die Varianz um den Preis von etwas Bias; James et al. (2023) merken an, dass mit Ridge regularisierte Splines mit gut gewähltem Strafterm in ihrem Double-Descent-Beispiel einen niedrigeren Testfehler erreicht hätten als die interpolierenden Anpassungen. Lernkurven, die Trainings- und Validierungsfehler vergleichen, zeigen, auf welcher Seite des Dilemmas ein Modell liegt ([[neural-network-evaluation|Evaluation neuronaler Netze]]).

### Merksatz

Der erwartete Testfehler ist Varianz plus quadrierter Bias plus nicht reduzierbares Rauschen; mehr Flexibilität senkt den Bias und erhöht die Varianz, daher liegt das beste Modell dazwischen, und interpolierende überparametrisierte Modelle sind ein Sonderfall, den man kennen sollte.

### Quellen

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, Abschnitte 2.2.2, 5.1.4 und 10.8. Springer. [statlearning.com](https://www.statlearning.com/)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 5, Abschnitt 5.4.4. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/ml.html)
- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
