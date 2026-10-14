---
title_en: Overfitting
title_de: Overfitting
entity_type: Concept
aliases:
- Overfitting
- Over-fitting
- Überanpassung
sources:
- https://www.deeplearningbook.org/contents/ml.html
- https://arxiv.org/abs/1812.11118
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A model overfits when the gap between its training error and its test error is too large: it has memorised properties of the training set that do not help on new data. It underfits when it cannot reach a sufficiently low error even on the training set (Goodfellow et al., 2016). Both depend on the model's capacity, its ability to fit a wide variety of functions: too little capacity leads to underfitting, too much to overfitting, and generalisation error typically follows a U-shaped curve as capacity grows (Goodfellow et al., 2016). Overfitting is detected by comparing training and validation error and reduced by regularisation, more data or a smaller hypothesis space ([[regularisation-and-hyperparameters|regularisation and hyperparameters]]). Very large modern models complicate the picture: they can fit the training data exactly and still generalise well ("double descent", Belkin et al., 2019).

### How it works

```text
                error
                  │  underfitting zone │ overfitting zone
                  │╲                   │        ╱ generalisation (test) error
                  │ ╲                  │      ╱
                  │  ╲________________ │ ___╱    ← generalisation gap grows
                  │    ╲               │
                  │      ╲_____________│_______ training error
                  └────────────────────┴─────────→ capacity
                                optimal capacity
```

#### 1. Training error, test error and generalisation

Training a model minimises an error on the training set, which by itself is only an optimisation problem; machine learning additionally wants a low generalisation error, the expected error on new inputs, which is estimated on a separately collected test set (Goodfellow et al., 2016). Under the i.i.d. assumptions, training and test examples are drawn independently from the same distribution. Because the parameters are chosen to reduce the training error, the expected test error is greater than or equal to the expected training error (Goodfellow et al., 2016). A model therefore has to do two things: make the training error small, and make the gap between training and test error small; failing at the first is underfitting, failing at the second is overfitting (Goodfellow et al., 2016).

#### 2. Capacity

Capacity can be controlled by choosing the hypothesis space, the set of functions the learning algorithm may select from (Goodfellow et al., 2016). In the textbook example, data generated from a quadratic function is fitted by a linear model, which underfits because it cannot capture the curvature, a quadratic model, which generalises well, and a degree-9 polynomial, which passes exactly through all training points but has more parameters than training examples and picks one of infinitely many such solutions, which generalises poorly (Goodfellow et al., 2016). Nonparametric models such as nearest-neighbour regression grow with the training set and can reach minimal training error ([[k-nearest-neighbours|k-nearest neighbours]]).

#### 3. Effect of the amount of data

Expected generalisation error cannot increase as the number of training examples grows; a model with optimal capacity can still show a large gap between training and test error, and more training data can then reduce it (Goodfellow et al., 2016). Even an oracle that knows the true distribution has some error, the Bayes error, because of noise; training error can fall below it only by memorising the training set (Goodfellow et al., 2016).

#### 4. Regularisation

Regularisation is "any modification we make to a learning algorithm that is intended to reduce its generalization error but not its training error" (Goodfellow et al., 2016). Weight decay, for example, adds a penalty λ‖w‖² to the training error: with a very large λ, a degree-9 polynomial underfits, with a medium λ it recovers the right general shape, and with λ close to zero it overfits (Goodfellow et al., 2016). Dropout and early stopping are common further options ([[regularisation-and-hyperparameters|regularisation and hyperparameters]]).

#### 5. Validation sets

Hyperparameters that control capacity, such as the polynomial degree or λ, cannot be learned on the training set, because they would always choose maximum capacity and overfit (Goodfellow et al., 2016). They are tuned on a validation set split off from the training data, typically about 20 percent; the test set must not be used for any decision about the model ([[cross-validation|cross-validation]]).

#### Origin and variants

The idea of preferring the simplest explanation goes back to the principle of parsimony known as Occam's razor; statistical learning theory (Vapnik and Chervonenkis, from 1971) formalised capacity, for example as the VC dimension, and showed that the gap between training and generalisation error is bounded by a quantity that grows with capacity and shrinks with more training examples (Goodfellow et al., 2016). These bounds are rarely used for deep learning because they are loose and capacity is hard to determine (Goodfellow et al., 2016). Belkin et al. (2019) observed that very rich models such as [[neural-networks|neural networks]] are trained to fit the data exactly yet often reach high test accuracy, and proposed the "double descent" curve: beyond the point of interpolation, increasing capacity improves performance again ([[bias-variance-tradeoff|bias-variance trade-off]]).

### When to use it

- Diagnosing a model with learning curves: high training error points to underfitting, a large gap to validation error points to overfitting ([[neural-network-evaluation|neural network evaluation]]).
- Choosing capacity, regularisation strength and the amount of data needed for a task ([[regularisation-and-hyperparameters|regularisation and hyperparameters]]).
- Judging reported results: a test set reused for many decisions gives optimistic estimates (Goodfellow et al., 2016).

### Strengths and limitations

**Strengths**
- A simple, measurable diagnosis from training and validation error (Goodfellow et al., 2016).
- Links directly to practical levers: capacity, regularisation, data.

**Limitations**
- The classical U-shaped picture does not fully describe heavily overparameterised models, which can interpolate the training data and still generalise (Belkin et al., 2019).
- Learning-theory bounds on the generalisation gap are often too loose for deep learning (Goodfellow et al., 2016).
- A good validation score only holds for data from the same distribution; it says nothing about distribution shift.

### Comparison

| | Underfitting | Good fit | Overfitting |
|---|---|---|---|
| Training error | high | low | very low |
| Gap to test error | small | small | large |
| Typical remedy | more capacity, better features | — | regularisation, more data, less capacity |

Source: Goodfellow et al. (2016).

### In practice

The same test set used over many years and by many teams yields optimistic results as well, so benchmarks become stale (Goodfellow et al., 2016). Validation error is monitored during training to stop before the model overfits ([[neural-network-training|neural network training]]). When comparing models, repeated cross-validation and suitable statistical tests reduce the risk of reading noise as progress ([[model-comparison|model comparison]]).

### Key takeaway

A model overfits when its test error is much higher than its training error and underfits when even its training error is too high; capacity, regularisation and data size decide where it lands, and only held-out data shows it.

### Sources

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 5: Machine Learning Basics (sections 5.2–5.3). MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/ml.html)
- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Modell ist überangepasst (Overfitting), wenn der Abstand zwischen Trainingsfehler und Testfehler zu groß ist: Es hat Eigenschaften der Trainingsdaten auswendig gelernt, die bei neuen Daten nicht helfen. Es ist unterangepasst (Underfitting), wenn es schon auf den Trainingsdaten keinen ausreichend niedrigen Fehler erreicht (Goodfellow et al., 2016). Beides hängt von der Kapazität des Modells ab, seiner Fähigkeit, sehr unterschiedliche Funktionen abzubilden: Zu wenig Kapazität führt zu Underfitting, zu viel zu Overfitting, und der Generalisierungsfehler folgt mit wachsender Kapazität typischerweise einer U-Kurve (Goodfellow et al., 2016). Overfitting wird durch den Vergleich von Trainings- und Validierungsfehler erkannt und durch Regularisierung, mehr Daten oder einen kleineren Hypothesenraum verringert ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]). Sehr große moderne Modelle machen das Bild komplizierter: Sie können die Trainingsdaten exakt abbilden und trotzdem gut generalisieren („Double Descent“, Belkin et al., 2019).

### Funktionsweise

```text
                Fehler
                  │  Underfitting-Zone │ Overfitting-Zone
                  │╲                   │        ╱ Generalisierungs-(Test-)Fehler
                  │ ╲                  │      ╱
                  │  ╲________________ │ ___╱    ← Generalisierungslücke wächst
                  │    ╲               │
                  │      ╲_____________│_______ Trainingsfehler
                  └────────────────────┴─────────→ Kapazität
                                optimale Kapazität
```

#### 1. Trainingsfehler, Testfehler und Generalisierung

Beim Training wird ein Fehler auf den Trainingsdaten minimiert, was für sich genommen nur ein Optimierungsproblem ist; maschinelles Lernen will zusätzlich einen niedrigen Generalisierungsfehler, den erwarteten Fehler bei neuen Eingaben, der auf einer getrennt erhobenen Testmenge geschätzt wird (Goodfellow et al., 2016). Unter den i.i.d.-Annahmen werden Trainings- und Testbeispiele unabhängig aus derselben Verteilung gezogen. Weil die Parameter so gewählt werden, dass der Trainingsfehler sinkt, ist der erwartete Testfehler größer oder gleich dem erwarteten Trainingsfehler (Goodfellow et al., 2016). Ein Modell muss daher zweierlei leisten: einen kleinen Trainingsfehler erreichen und den Abstand zwischen Trainings- und Testfehler klein halten; scheitert es am Ersten, liegt Underfitting vor, scheitert es am Zweiten, Overfitting (Goodfellow et al., 2016).

#### 2. Kapazität

Die Kapazität lässt sich über die Wahl des Hypothesenraums steuern, der Menge an Funktionen, aus denen der Lernalgorithmus wählen darf (Goodfellow et al., 2016). Im Lehrbuchbeispiel werden Daten aus einer quadratischen Funktion mit einem linearen Modell angepasst, das unterangepasst ist, weil es die Krümmung nicht erfasst, mit einem quadratischen Modell, das gut generalisiert, und mit einem Polynom 9. Grades, das genau durch alle Trainingspunkte geht, aber mehr Parameter als Trainingsbeispiele hat und eine von unendlich vielen solchen Lösungen wählt, die schlecht generalisiert (Goodfellow et al., 2016). Nichtparametrische Modelle wie die Nächste-Nachbarn-Regression wachsen mit der Trainingsmenge und können einen minimalen Trainingsfehler erreichen ([[k-nearest-neighbours|k-nächste Nachbarn]]).

#### 3. Einfluss der Datenmenge

Der erwartete Generalisierungsfehler kann mit mehr Trainingsbeispielen nicht steigen; auch ein Modell mit optimaler Kapazität kann eine große Lücke zwischen Trainings- und Testfehler zeigen, die mehr Trainingsdaten dann verkleinern können (Goodfellow et al., 2016). Selbst ein Orakel, das die wahre Verteilung kennt, macht wegen Rauschen Fehler, den Bayes-Fehler; der Trainingsfehler kann nur durch Auswendiglernen der Trainingsdaten darunter fallen (Goodfellow et al., 2016).

#### 4. Regularisierung

Regularisierung ist jede Änderung am Lernalgorithmus, die den Generalisierungsfehler senken soll, nicht aber den Trainingsfehler (Goodfellow et al., 2016). Weight Decay etwa addiert einen Strafterm λ‖w‖² zum Trainingsfehler: Mit sehr großem λ ist ein Polynom 9. Grades unterangepasst, mit mittlerem λ findet es die richtige Grundform, mit λ nahe null ist es überangepasst (Goodfellow et al., 2016). Dropout und Early Stopping sind weitere übliche Optionen ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]).

#### 5. Validierungsmengen

Hyperparameter, die die Kapazität steuern, etwa der Polynomgrad oder λ, können nicht auf den Trainingsdaten gelernt werden, weil sie dann immer die maximale Kapazität wählen und überanpassen würden (Goodfellow et al., 2016). Sie werden auf einer Validierungsmenge abgestimmt, die von den Trainingsdaten abgetrennt wird, typischerweise etwa 20 Prozent; die Testmenge darf für keine Entscheidung über das Modell genutzt werden ([[cross-validation|Kreuzvalidierung]]).

#### Herkunft und Varianten

Die Idee, die einfachste Erklärung vorzuziehen, geht auf das Sparsamkeitsprinzip zurück, das als Ockhams Rasiermesser bekannt ist; die statistische Lerntheorie (Vapnik und Chervonenkis, ab 1971) formalisierte die Kapazität, etwa als VC-Dimension, und zeigte, dass der Abstand zwischen Trainings- und Generalisierungsfehler durch eine Größe beschränkt ist, die mit der Kapazität wächst und mit mehr Trainingsbeispielen schrumpft (Goodfellow et al., 2016). Für Deep Learning werden diese Schranken selten genutzt, weil sie locker sind und sich die Kapazität schwer bestimmen lässt (Goodfellow et al., 2016). Belkin et al. (2019) beobachteten, dass sehr ausdrucksstarke Modelle wie [[neural-networks|neuronale Netze]] so trainiert werden, dass sie die Daten exakt abbilden, und dennoch oft eine hohe Testgenauigkeit erreichen, und schlugen die „Double Descent“-Kurve vor: Jenseits des Interpolationspunkts verbessert mehr Kapazität die Leistung wieder ([[bias-variance-tradeoff|Bias-Varianz-Dilemma]]).

### Wann einsetzen

- Diagnose eines Modells mit Lernkurven: Ein hoher Trainingsfehler deutet auf Underfitting, ein großer Abstand zum Validierungsfehler auf Overfitting ([[neural-network-evaluation|Evaluation neuronaler Netze]]).
- Wahl von Kapazität, Regularisierungsstärke und der für eine Aufgabe nötigen Datenmenge ([[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]]).
- Bewertung berichteter Ergebnisse: Eine für viele Entscheidungen wiederverwendete Testmenge liefert zu optimistische Schätzungen (Goodfellow et al., 2016).

### Stärken und Grenzen

**Stärken**
- Eine einfache, messbare Diagnose aus Trainings- und Validierungsfehler (Goodfellow et al., 2016).
- Führt direkt zu praktischen Stellschrauben: Kapazität, Regularisierung, Daten.

**Grenzen**
- Das klassische U-förmige Bild beschreibt stark überparametrisierte Modelle nicht vollständig, die die Trainingsdaten interpolieren und trotzdem generalisieren können (Belkin et al., 2019).
- Schranken der Lerntheorie für die Generalisierungslücke sind für Deep Learning oft zu locker (Goodfellow et al., 2016).
- Ein guter Validierungswert gilt nur für Daten aus derselben Verteilung; über Verteilungsverschiebungen sagt er nichts aus.

### Vergleich

| | Underfitting | Gute Anpassung | Overfitting |
|---|---|---|---|
| Trainingsfehler | hoch | niedrig | sehr niedrig |
| Abstand zum Testfehler | klein | klein | groß |
| Typische Abhilfe | mehr Kapazität, bessere Merkmale | — | Regularisierung, mehr Daten, weniger Kapazität |

Quelle: Goodfellow et al. (2016).

### In der Praxis

Auch dieselbe Testmenge, die über viele Jahre und von vielen Teams genutzt wird, liefert zu optimistische Ergebnisse, sodass Benchmarks veralten (Goodfellow et al., 2016). Der Validierungsfehler wird während des Trainings beobachtet, um vor dem Overfitting abzubrechen ([[neural-network-training|Training neuronaler Netze]]). Beim Vergleich von Modellen verringern wiederholte Kreuzvalidierung und geeignete statistische Tests das Risiko, Rauschen für Fortschritt zu halten ([[model-comparison|Modellvergleich]]).

### Merksatz

Ein Modell ist überangepasst, wenn sein Testfehler viel höher ist als sein Trainingsfehler, und unterangepasst, wenn schon der Trainingsfehler zu hoch ist; Kapazität, Regularisierung und Datenmenge entscheiden, wo es landet, und nur zurückgehaltene Daten zeigen es.

### Quellen

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 5: Machine Learning Basics (Abschnitte 5.2–5.3). MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/ml.html)
- Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019). Reconciling modern machine-learning practice and the classical bias–variance trade-off. *PNAS*, 116(32). [arXiv:1812.11118](https://arxiv.org/abs/1812.11118)
