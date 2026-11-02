---
title_en: Gradient Descent
title_de: Gradientenabstieg
entity_type: Method
aliases:
- Gradient descent
- Stochastic gradient descent
- SGD
- Mini-batch gradient descent
- Batch gradient descent
- Gradientenabstieg
- Stochastischer Gradientenabstieg
sources:
- https://web.stanford.edu/~jurafsky/slp3/4.pdf
- https://arxiv.org/abs/1609.04747
- https://scikit-learn.org/stable/modules/sgd.html
- https://arxiv.org/abs/1711.05101
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Gradient descent finds parameters that minimise a loss function by repeatedly computing the gradient, the direction in which the loss rises most steeply, and taking a step in the opposite direction, scaled by a learning rate (Jurafsky & Martin, 2026). Stochastic gradient descent (SGD) estimates the gradient from a single example or a small mini-batch instead of the whole training set, which makes each step cheap and is how [[logistic-regression|logistic regression]] and [[neural-networks|neural networks]] are usually trained (Jurafsky & Martin, 2026; Ruder, 2016). Momentum and adaptive methods such as [[adam-optimiser|Adam]] modify the basic update to converge faster and more reliably (Ruder, 2016).

### How it works

```text
initialise θ (zeros or small random values)
repeat until converged or validation loss stops improving:
    shuffle training data
    for each mini-batch B of size m:
        loss  L(θ) = (1/m) Σ_{(x,y)∈B} L(f(x; θ), y)
        grad  g = ∇θ L(θ)                (back-propagation in neural networks)
        step  θ ← θ − η · g              (η = learning rate)
```

#### 1. Objective and gradient

Training chooses the parameters θ that minimise the average loss over the training examples, for example the [[cross-entropy|cross-entropy]] loss (Jurafsky & Martin, 2026). The gradient ∇L is the vector of partial derivatives of the loss with respect to every parameter; it points in the direction of greatest increase, so the update `θ_{t+1} = θ_t − η ∇L(f(x; θ), y)` moves downhill (Jurafsky & Martin, 2026). For logistic regression with cross-entropy, the derivative for one weight is simply `(ŷ − y) · x_j`, the prediction error times the feature value (Jurafsky & Martin, 2026). In neural networks the gradient is computed by [[back-propagation|back-propagation]].

#### 2. Batch, stochastic and mini-batch

- **Batch gradient descent** computes the gradient over the whole data set for each update; it gives an accurate direction but is slow, impossible for data that does not fit in memory and cannot learn online (Ruder, 2016; Jurafsky & Martin, 2026).
- **Stochastic gradient descent** updates after each randomly chosen example; updates are frequent and noisy, which lets it jump to new minima but also keeps it overshooting, unless the learning rate is slowly decreased (Ruder, 2016).
- **Mini-batch gradient descent** averages the gradient over m examples, which reduces the variance of updates and lets hardware process the batch in parallel; m = 1 is SGD and m = data set size is batch gradient descent (Jurafsky & Martin, 2026). Ruder (2016) names 50 to 256 as common sizes, Jurafsky and Martin (2026) give 512 or 1024 as examples, and the term SGD is commonly used for mini-batch training too.

#### 3. Learning rate

The learning rate η is a hyperparameter: too high and steps overshoot the minimum or diverge, too low and training takes very long (Jurafsky & Martin, 2026; Ruder, 2016). It is common to start with a higher rate and decrease it over iterations; such schedules must be fixed in advance and cannot adapt to the data set (Ruder, 2016). For logistic regression the loss is convex, so gradient descent can reach the single minimum from any starting point; neural network losses are non-convex and have local minima and saddle points, where gradients are close to zero in all directions (Jurafsky & Martin, 2026; Ruder, 2016).

#### 4. Momentum and adaptive methods

- **Momentum** adds a fraction γ (usually about 0.9) of the previous update to the current one, `v_t = γ v_{t−1} + η ∇J(θ)`, `θ = θ − v_t`, which speeds up movement along consistent directions and damps oscillation in ravines (Ruder, 2016).
- **Nesterov accelerated gradient** evaluates the gradient at the approximate future position `θ − γ v_{t−1}` (Ruder, 2016).
- **Adagrad** scales the step of each parameter by the root of the sum of its past squared gradients, which suits sparse features but makes the learning rate shrink towards zero over time (Ruder, 2016).
- **RMSprop and Adadelta** replace that sum with a decaying average of squared gradients (Ruder, 2016).
- **Adam** combines a decaying average of gradients (momentum) with RMSprop-style scaling and bias correction ([[adam-optimiser|Adam]]; Ruder, 2016).

#### 5. Stopping

The algorithm stops when the gradient norm falls below a threshold or when progress halts, for example when the loss on a held-out set starts rising ([[regularisation-and-hyperparameters|early stopping]]; Jurafsky & Martin, 2026). Training data is shuffled in each epoch (Ruder, 2016; [[scikit-learn|scikit-learn]]).

#### Origin and variants

Gradient descent is a general first-order optimisation method; scikit-learn notes that SGD has been used in machine learning for a long time but gained attention more recently for large-scale learning (scikit-learn). Ruder (2016) surveys the variants above and parallel versions such as Hogwild! and Downpour SGD; averaged SGD keeps the average of the parameters over updates (scikit-learn).

### When to use it

- Training any differentiable model, from [[logistic-regression|logistic regression]] and [[linear-regression|linear regression]] to deep networks ([[neural-network-training|neural network training]]).
- Large or sparse data such as text [[classification|classification]], where scikit-learn's SGD classifiers scale to more than 10^5 examples and 10^5 features (scikit-learn).
- Online learning, where the model must update as new examples arrive (Ruder, 2016).

### Strengths and limitations

**Strengths**
- Each step only needs first-order gradients, cheap for millions of parameters.
- Mini-batches use parallel hardware efficiently (Jurafsky & Martin, 2026).
- Simple and efficient to implement (scikit-learn).

**Limitations**
- Needs several hyperparameters: learning rate, schedule, batch size, number of iterations and regularisation (scikit-learn; Ruder, 2016).
- Sensitive to feature scaling, so inputs are usually standardised (scikit-learn; Jurafsky & Martin, 2026).
- On non-convex losses it can stall in saddle points or local minima (Ruder, 2016).
- One learning rate for all parameters suits features of very different frequency poorly, which adaptive methods address (Ruder, 2016).

### Comparison

| Variant | Gradient computed on | Update | Typical use |
|---|---|---|---|
| Batch GD | whole data set | `θ − η∇J` | small convex problems |
| SGD | one example | noisy, frequent | online learning |
| Mini-batch SGD | m examples | lower variance, parallel | neural networks |
| SGD + momentum | mini-batch | accumulated velocity | ravines, [[computer-vision\|image classification]] |
| [[adam-optimiser\|Adam]] | mini-batch | per-parameter adaptive step | sparse data, fast convergence of deep networks |

Sources: Jurafsky & Martin (2026), Ruder (2016), Loshchilov & Hutter (2019).

### In practice

scikit-learn recommends shuffling the data, standardising features unless they have an intrinsic scale such as word frequencies, tuning the regularisation term by search over values from 10^-1 to 10^-6, and setting the number of iterations to about `10^6 / n`, since SGD converged after seeing roughly 10^6 samples in their experience (scikit-learn). Ruder (2016) suggests adaptive methods for sparse data and for fast convergence of deep networks, while noting that many papers use plain SGD with an annealing schedule, which finds a minimum but more slowly and depends more on initialisation. Monitoring a validation set and stopping early is a cheap safeguard against [[overfitting|overfitting]] (Ruder, 2016).

### Key takeaway

Gradient descent repeatedly steps against the gradient of the loss; in practice it runs on shuffled mini-batches with a tuned learning rate, often with momentum or an adaptive method such as Adam.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Ruder, S. (2016). *An overview of gradient descent optimization algorithms.* [arXiv:1609.04747](https://arxiv.org/abs/1609.04747)
- scikit-learn developers. *Stochastic Gradient Descent.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/sgd.html)
- Loshchilov, I. & Hutter, F. (2019). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der Gradientenabstieg findet Parameter, die eine Verlustfunktion minimieren, indem er wiederholt den Gradienten berechnet, also die Richtung, in der der Verlust am steilsten steigt, und einen Schritt in die Gegenrichtung macht, skaliert mit einer Lernrate (Jurafsky & Martin, 2026). Der stochastische Gradientenabstieg (SGD) schätzt den Gradienten aus einem einzelnen Beispiel oder einem kleinen Mini-Batch statt aus dem ganzen Trainingsdatensatz; das macht jeden Schritt günstig und ist der übliche Weg, [[logistic-regression|logistische Regression]] und [[neural-networks|neuronale Netze]] zu trainieren (Jurafsky & Martin, 2026; Ruder, 2016). Momentum und adaptive Verfahren wie [[adam-optimiser|Adam]] verändern das Grund-Update, damit es schneller und zuverlässiger konvergiert (Ruder, 2016).

### Funktionsweise

```text
θ initialisieren (Nullen oder kleine Zufallswerte)
wiederholen, bis konvergiert oder der Validierungsverlust nicht mehr sinkt:
    Trainingsdaten mischen
    für jeden Mini-Batch B der Größe m:
        Verlust   L(θ) = (1/m) Σ_{(x,y)∈B} L(f(x; θ), y)
        Gradient  g = ∇θ L(θ)              (Backpropagation in neuronalen Netzen)
        Schritt   θ ← θ − η · g            (η = Lernrate)
```

#### 1. Zielfunktion und Gradient

Das Training wählt die Parameter θ, die den mittleren Verlust über die Trainingsbeispiele minimieren, etwa den [[cross-entropy|Cross-Entropy]]-Verlust (Jurafsky & Martin, 2026). Der Gradient ∇L ist der Vektor der partiellen Ableitungen des Verlusts nach jedem Parameter; er zeigt in Richtung des stärksten Anstiegs, sodass das Update `θ_{t+1} = θ_t − η ∇L(f(x; θ), y)` bergab führt (Jurafsky & Martin, 2026). Bei logistischer Regression mit Cross-Entropy ist die Ableitung für ein Gewicht einfach `(ŷ − y) · x_j`, der Vorhersagefehler mal dem Merkmalswert (Jurafsky & Martin, 2026). In neuronalen Netzen wird der Gradient per [[back-propagation|Backpropagation]] berechnet.

#### 2. Batch, stochastisch und Mini-Batch

- **Batch-Gradientenabstieg** berechnet den Gradienten für jedes Update über den ganzen Datensatz; das liefert eine genaue Richtung, ist aber langsam, für Daten, die nicht in den Speicher passen, unmöglich und kann nicht online lernen (Ruder, 2016; Jurafsky & Martin, 2026).
- **Stochastischer Gradientenabstieg** aktualisiert nach jedem zufällig gewählten Beispiel; die Updates sind häufig und verrauscht, was Sprünge zu neuen Minima erlaubt, aber auch ständiges Überschießen verursacht, sofern die Lernrate nicht langsam gesenkt wird (Ruder, 2016).
- **Mini-Batch-Gradientenabstieg** mittelt den Gradienten über m Beispiele, was die Varianz der Updates senkt und die Hardware den Batch parallel verarbeiten lässt; m = 1 ist SGD, m = Datensatzgröße ist Batch-Gradientenabstieg (Jurafsky & Martin, 2026). Ruder (2016) nennt 50 bis 256 als übliche Größen, Jurafsky und Martin (2026) geben 512 oder 1024 als Beispiele, und der Begriff SGD wird üblicherweise auch für Mini-Batch-Training verwendet.

#### 3. Lernrate

Die Lernrate η ist ein Hyperparameter: Ist sie zu hoch, schießen Schritte über das Minimum hinaus oder divergieren, ist sie zu niedrig, dauert das Training sehr lange (Jurafsky & Martin, 2026; Ruder, 2016). Üblich ist, mit einer höheren Rate zu beginnen und sie über die Iterationen zu senken; solche Zeitpläne müssen vorab festgelegt werden und können sich nicht an den Datensatz anpassen (Ruder, 2016). Bei logistischer Regression ist der Verlust konvex, sodass der Gradientenabstieg das einzige Minimum von jedem Startpunkt aus erreichen kann; Verluste neuronaler Netze sind nicht konvex und haben lokale Minima und Sattelpunkte, an denen die Gradienten in allen Richtungen nahe null sind (Jurafsky & Martin, 2026; Ruder, 2016).

#### 4. Momentum und adaptive Verfahren

- **Momentum** addiert einen Anteil γ (meist etwa 0,9) des vorigen Updates zum aktuellen, `v_t = γ v_{t−1} + η ∇J(θ)`, `θ = θ − v_t`; das beschleunigt die Bewegung in gleichbleibende Richtungen und dämpft Oszillationen in Schluchten (Ruder, 2016).
- **Nesterov Accelerated Gradient** wertet den Gradienten an der ungefähren künftigen Position `θ − γ v_{t−1}` aus (Ruder, 2016).
- **Adagrad** skaliert den Schritt jedes Parameters mit der Wurzel der Summe seiner bisherigen quadrierten Gradienten; das passt zu dünn besetzten Merkmalen, lässt die Lernrate aber mit der Zeit gegen null schrumpfen (Ruder, 2016).
- **RMSprop und Adadelta** ersetzen diese Summe durch einen abklingenden Mittelwert der quadrierten Gradienten (Ruder, 2016).
- **Adam** kombiniert einen abklingenden Mittelwert der Gradienten (Momentum) mit einer Skalierung wie bei RMSprop und einer Bias-Korrektur ([[adam-optimiser|Adam]]; Ruder, 2016).

#### 5. Abbruch

Der Algorithmus endet, wenn die Norm des Gradienten unter eine Schwelle fällt oder der Fortschritt stockt, etwa wenn der Verlust auf zurückgehaltenen Daten zu steigen beginnt ([[regularisation-and-hyperparameters|Early Stopping]]; Jurafsky & Martin, 2026). Die Trainingsdaten werden in jeder Epoche gemischt (Ruder, 2016; [[scikit-learn|scikit-learn]]).

#### Ursprung und Varianten

Der Gradientenabstieg ist ein allgemeines Optimierungsverfahren erster Ordnung; scikit-learn merkt an, dass SGD im maschinellen Lernen schon lange genutzt wird, aber erst in jüngerer Zeit im Zusammenhang mit Lernen auf großen Datenmengen Beachtung fand (scikit-learn). Ruder (2016) gibt einen Überblick über die genannten Varianten und parallele Versionen wie Hogwild! und Downpour SGD; Averaged SGD behält den Mittelwert der Parameter über die Updates (scikit-learn).

### Wann einsetzen

- Training jedes differenzierbaren Modells, von [[logistic-regression|logistischer Regression]] und [[linear-regression|linearer Regression]] bis zu tiefen Netzen ([[neural-network-training|Training neuronaler Netze]]).
- Große oder dünn besetzte Daten wie bei der Textklassifikation, wo die SGD-Klassifikatoren von scikit-learn auf mehr als 10^5 Beispiele und 10^5 Merkmale skalieren (scikit-learn).
- Online-Lernen, bei dem das Modell sich mit neu eintreffenden Beispielen aktualisieren muss (Ruder, 2016).

### Stärken und Grenzen

**Stärken**
- Jeder Schritt braucht nur Gradienten erster Ordnung und ist auch für Millionen Parameter günstig.
- Mini-Batches nutzen parallele Hardware effizient (Jurafsky & Martin, 2026).
- Einfach und effizient zu implementieren (scikit-learn).

**Grenzen**
- Braucht mehrere Hyperparameter: Lernrate, Zeitplan, Batch-Größe, Zahl der Iterationen und Regularisierung (scikit-learn; Ruder, 2016).
- Empfindlich gegenüber der Skalierung der Merkmale, weshalb Eingaben meist standardisiert werden (scikit-learn; Jurafsky & Martin, 2026).
- Bei nicht konvexen Verlusten kann er in Sattelpunkten oder lokalen Minima steckenbleiben (Ruder, 2016).
- Eine Lernrate für alle Parameter passt schlecht zu Merkmalen sehr unterschiedlicher Häufigkeit, was adaptive Verfahren angehen (Ruder, 2016).

### Vergleich

| Variante | Gradient berechnet auf | Update | Typischer Einsatz |
|---|---|---|---|
| Batch-GD | ganzer Datensatz | `θ − η∇J` | kleine konvexe Probleme |
| SGD | einem Beispiel | verrauscht, häufig | Online-Lernen |
| Mini-Batch-SGD | m Beispielen | geringere Varianz, parallel | neuronale Netze |
| SGD + Momentum | Mini-Batch | aufsummierte Geschwindigkeit | Schluchten, Bildklassifikation |
| [[adam-optimiser\|Adam]] | Mini-Batch | adaptiver Schritt pro Parameter | dünn besetzte Daten, schnelle Konvergenz tiefer Netze |

Quellen: Jurafsky & Martin (2026), Ruder (2016), Loshchilov & Hutter (2019).

### In der Praxis

scikit-learn empfiehlt, die Daten zu mischen, Merkmale zu standardisieren, sofern sie keine eigene Skala wie Worthäufigkeiten haben, den Regularisierungsterm per Suche über Werte von 10^-1 bis 10^-6 einzustellen und die Zahl der Iterationen auf etwa `10^6 / n` zu setzen, da SGD nach ihrer Erfahrung nach etwa 10^6 gesehenen Beispielen konvergierte (scikit-learn). Ruder (2016) rät für dünn besetzte Daten und für schnelle Konvergenz tiefer Netze zu adaptiven Verfahren und merkt an, dass viele Arbeiten einfaches SGD mit abklingender Lernrate nutzen, das zwar ein Minimum findet, aber langsamer und stärker abhängig von der Initialisierung. Einen Validierungsdatensatz zu beobachten und früh abzubrechen ist ein günstiger Schutz vor [[overfitting|Overfitting]] (Ruder, 2016).

### Merksatz

Der Gradientenabstieg geht wiederholt gegen den Gradienten des Verlusts; in der Praxis läuft er auf gemischten Mini-Batches mit eingestellter Lernrate, oft mit Momentum oder einem adaptiven Verfahren wie Adam.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Ruder, S. (2016). *An overview of gradient descent optimization algorithms.* [arXiv:1609.04747](https://arxiv.org/abs/1609.04747)
- scikit-learn developers. *Stochastic Gradient Descent.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/sgd.html)
- Loshchilov, I. & Hutter, F. (2019). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
