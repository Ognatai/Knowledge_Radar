---
title_en: Training Neural Networks
title_de: Training neuronaler Netze
entity_type: Method
sources:
- https://www.deeplearningbook.org/
- https://proceedings.mlr.press/v9/glorot10a.html
- https://arxiv.org/abs/1502.01852
- https://arxiv.org/abs/1412.6980
- https://arxiv.org/abs/1711.05101
- https://arxiv.org/abs/1502.03167
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Training a neural network means adjusting its weights to minimise a loss function on training data. Back-propagation computes the gradients, and a gradient-based optimiser such as stochastic gradient descent or Adam updates the weights on small batches of data, pass after pass over the training set (Goodfellow et al., 2016; Kingma & Ba, 2014). Careful initialisation (Glorot & Bengio, 2010; He et al., 2015), normalisation (Ioffe & Szegedy, 2015) and the choice of learning rate decide whether deep networks train well.

### How it works

The training loop repeats four steps: compute predictions for a batch (forward pass), measure the error with the loss, compute the gradient of the loss with respect to every weight (backward pass), and update the weights with the optimiser. One pass over the whole training set is an epoch.

```text
1. Loss functions
▼
2. Back-propagation
▼
3. Stochastic gradient descent, batches and epochs
▼
4. Adaptive optimisers
▼
5. Initialisation and normalisation
▼
6. Learning rate and regularisation
```

#### 1. Loss functions

The loss measures how far predictions are from the targets and is chosen together with the output layer: cross-entropy for classification with a softmax output, mean squared error for regression (Goodfellow et al., 2016). Training minimises the average loss over the training data.

#### 2. Back-propagation

Back-propagation applies the chain rule backwards through the network to compute the gradient of the loss with respect to every parameter efficiently, reusing intermediate results from the forward pass (Goodfellow et al., 2016). Frameworks compute these gradients automatically ([[keras-and-tensorflow|Keras and TensorFlow]]).

#### 3. Stochastic gradient descent, batches and epochs

Gradient descent moves the weights a small step against the gradient. Stochastic gradient descent estimates the gradient on a minibatch of examples instead of the full training set, which makes each step cheap and adds noise that can help optimisation (Goodfellow et al., 2016). An iteration processes one batch; an epoch is one pass over the training set. Momentum accumulates past gradients to speed up progress along consistent directions.

#### 4. Adaptive optimisers

Adam (Kingma & Ba, 2014) adapts the step size for each parameter using running estimates of the first and second moments of the gradients. It is computationally efficient, needs little memory, suits large problems and noisy or sparse gradients, and its hyperparameters typically need little tuning. Loshchilov & Hutter (2017) showed that L2 regularisation and weight decay are not equivalent for adaptive methods such as Adam; decoupling the weight decay from the gradient update (AdamW) substantially improved Adam's generalisation, making it competitive with SGD with momentum on image classification.

#### 5. Initialisation and normalisation

Glorot & Bengio (2010) showed why deep networks trained from standard random initialisation did poorly, for example because sigmoid activations saturate, and proposed an initialisation scaled to the number of inputs and outputs of each layer, which converged substantially faster. He et al. (2015) derived an initialisation for rectifier (ReLU) networks that allows extremely deep models to be trained from scratch. Batch normalisation normalises layer inputs over each minibatch; it allows much higher learning rates, makes initialisation less critical and acts as a regulariser, and reached the same accuracy as the original image classification model with 14 times fewer training steps (Ioffe & Szegedy, 2015).

#### 6. Learning rate and regularisation

The learning rate is the most important hyperparameter: too high and training diverges, too low and it progresses slowly (Goodfellow et al., 2016). Validation error is monitored to detect overfitting, which is countered with regularisation such as weight decay, dropout and early stopping ([[regularization-and-hyperparameters|Regularization and Hyperparameters]]).

#### Origin and variants

Back-propagation with stochastic gradient descent is the classical training method (Goodfellow et al., 2016). Better initialisation (Glorot & Bengio, 2010; He et al., 2015), batch normalisation (Ioffe & Szegedy, 2015), Adam (Kingma & Ba, 2014) and AdamW (Loshchilov & Hutter, 2017) made very deep networks trainable in practice. Mixed precision reduces the memory and compute needed ([[mixed-precision-training|Mixed Precision Training]]).

### When to use it

- Whenever a neural network is fitted to data; the choices of loss, optimiser and learning rate are part of every training run (Goodfellow et al., 2016).
- When a quick, robust default optimiser is needed, Adam or AdamW work with little tuning (Kingma & Ba, 2014; Loshchilov & Hutter, 2017).
- When very deep networks fail to train, initialisation and normalisation are the first things to check (He et al., 2015; Ioffe & Szegedy, 2015).

### Strengths and limitations

**Strengths**
- Back-propagation computes all gradients efficiently (Goodfellow et al., 2016).
- Adam needs little tuning and handles noisy or sparse gradients (Kingma & Ba, 2014).
- Batch normalisation allows higher learning rates and fewer training steps (Ioffe & Szegedy, 2015).

**Limitations**
- Results depend strongly on the learning rate and other hyperparameters (Goodfellow et al., 2016).
- With standard initialisation, deep networks may train poorly (Glorot & Bengio, 2010).
- With Adam, L2 regularisation does not act as weight decay unless it is decoupled (Loshchilov & Hutter, 2017).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| SGD with momentum | Same step size for all parameters, accumulates past gradients (Goodfellow et al., 2016) | Well-tuned training, image classification |
| Adam | Per-parameter step sizes from gradient moments (Kingma & Ba, 2014) | Default choice, sparse or noisy gradients |
| AdamW | Adam with decoupled weight decay (Loshchilov & Hutter, 2017) | Regularised training with adaptive steps |

### In practice

A training run fixes the loss, optimiser, learning rate (often with a schedule), batch size and number of epochs, and logs training and validation curves (Goodfellow et al., 2016; [[experiment-tracking|Experiment Tracking]]). Initialisation schemes suited to the activation function are used by default in modern frameworks (He et al., 2015), and the model is evaluated on held-out data ([[neural-network-evaluation|Evaluating Neural Networks]]).

### Key takeaway

Training repeats forward pass, loss, back-propagation and weight update on small batches; good initialisation, normalisation, optimiser and learning rate decide whether it succeeds.

### Sources

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks.* AISTATS 2010. [PMLR](https://proceedings.mlr.press/v9/glorot10a.html)
- He, K. et al. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification.* ICCV 2015. [arXiv:1502.01852](https://arxiv.org/abs/1502.01852)
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization.* ICLR 2015. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift.* ICML 2015. [arXiv:1502.03167](https://arxiv.org/abs/1502.03167)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein neuronales Netz zu trainieren heißt, seine Gewichte so anzupassen, dass eine Verlustfunktion auf den Trainingsdaten minimal wird. Backpropagation berechnet die Gradienten, und ein gradientenbasierter Optimierer wie stochastischer Gradientenabstieg oder Adam aktualisiert die Gewichte auf kleinen Datenpaketen (Batches), Durchlauf für Durchlauf über die Trainingsmenge (Goodfellow et al., 2016; Kingma & Ba, 2014). Sorgfältige Initialisierung (Glorot & Bengio, 2010; He et al., 2015), Normalisierung (Ioffe & Szegedy, 2015) und die Wahl der Lernrate entscheiden, ob tiefe Netze gut trainieren.

### Funktionsweise

Die Trainingsschleife wiederholt vier Schritte: Vorhersagen für einen Batch berechnen (Vorwärtsdurchlauf), den Fehler mit der Verlustfunktion messen, den Gradienten des Verlusts nach jedem Gewicht berechnen (Rückwärtsdurchlauf) und die Gewichte mit dem Optimierer aktualisieren. Ein Durchlauf über die gesamte Trainingsmenge ist eine Epoche.

```text
1. Verlustfunktionen
▼
2. Backpropagation
▼
3. Stochastischer Gradientenabstieg, Batches und Epochen
▼
4. Adaptive Optimierer
▼
5. Initialisierung und Normalisierung
▼
6. Lernrate und Regularisierung
```

#### 1. Verlustfunktionen

Die Verlustfunktion misst, wie weit die Vorhersagen von den Zielwerten entfernt sind, und wird zusammen mit der Ausgabeschicht gewählt: Kreuzentropie für Klassifikation mit Softmax-Ausgabe, mittlerer quadratischer Fehler für Regression (Goodfellow et al., 2016). Das Training minimiert den durchschnittlichen Verlust über die Trainingsdaten.

#### 2. Backpropagation

Backpropagation wendet die Kettenregel rückwärts durch das Netz an, um den Gradienten des Verlusts nach jedem Parameter effizient zu berechnen, wobei Zwischenergebnisse des Vorwärtsdurchlaufs wiederverwendet werden (Goodfellow et al., 2016). Frameworks berechnen diese Gradienten automatisch ([[keras-and-tensorflow|Keras und TensorFlow]]).

#### 3. Stochastischer Gradientenabstieg, Batches und Epochen

Der Gradientenabstieg bewegt die Gewichte einen kleinen Schritt entgegen dem Gradienten. Stochastischer Gradientenabstieg schätzt den Gradienten auf einem Minibatch von Beispielen statt auf der ganzen Trainingsmenge; das macht jeden Schritt günstig und fügt Rauschen hinzu, das der Optimierung helfen kann (Goodfellow et al., 2016). Eine Iteration verarbeitet einen Batch, eine Epoche ist ein Durchlauf über die Trainingsmenge. Momentum sammelt frühere Gradienten und beschleunigt so den Fortschritt in gleichbleibende Richtungen.

#### 4. Adaptive Optimierer

Adam (Kingma & Ba, 2014) passt die Schrittweite für jeden Parameter anhand laufender Schätzungen des ersten und zweiten Moments der Gradienten an. Es ist recheneffizient, braucht wenig Speicher, eignet sich für große Probleme und verrauschte oder dünnbesetzte Gradienten, und seine Hyperparameter erfordern meist wenig Tuning. Loshchilov & Hutter (2017) zeigten, dass L2-Regularisierung und Weight Decay bei adaptiven Verfahren wie Adam nicht gleichwertig sind; wird der Weight Decay von der Gradientenaktualisierung entkoppelt (AdamW), generalisiert Adam deutlich besser und kann bei der Bildklassifikation mit SGD mit Momentum mithalten.

#### 5. Initialisierung und Normalisierung

Glorot & Bengio (2010) zeigten, warum tiefe Netze mit gewöhnlicher Zufallsinitialisierung schlecht trainierten, etwa weil Sigmoid-Aktivierungen sättigen, und schlugen eine Initialisierung vor, die an die Zahl der Ein- und Ausgänge jeder Schicht angepasst ist und deutlich schneller konvergierte. He et al. (2015) leiteten eine Initialisierung für Netze mit Rectifier-Aktivierung (ReLU) her, mit der sich auch sehr tiefe Modelle von Grund auf trainieren lassen. Batch Normalization normalisiert die Eingaben einer Schicht über jeden Minibatch; sie erlaubt deutlich höhere Lernraten, macht die Initialisierung weniger kritisch, wirkt regularisierend und erreichte die Genauigkeit des ursprünglichen Bildklassifikationsmodells mit 14-mal weniger Trainingsschritten (Ioffe & Szegedy, 2015).

#### 6. Lernrate und Regularisierung

Die Lernrate ist der wichtigste Hyperparameter: Ist sie zu hoch, divergiert das Training, ist sie zu niedrig, kommt es nur langsam voran (Goodfellow et al., 2016). Der Validierungsfehler wird beobachtet, um Overfitting zu erkennen, dem mit Regularisierung wie Weight Decay, Dropout und Early Stopping begegnet wird ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]).

#### Ursprung und Varianten

Backpropagation mit stochastischem Gradientenabstieg ist das klassische Trainingsverfahren (Goodfellow et al., 2016). Bessere Initialisierung (Glorot & Bengio, 2010; He et al., 2015), Batch Normalization (Ioffe & Szegedy, 2015), Adam (Kingma & Ba, 2014) und AdamW (Loshchilov & Hutter, 2017) machten sehr tiefe Netze in der Praxis trainierbar. Mixed Precision verringert Speicher- und Rechenbedarf ([[mixed-precision-training|Mixed Precision Training]]).

### Wann einsetzen

- Immer wenn ein neuronales Netz an Daten angepasst wird; Verlustfunktion, Optimierer und Lernrate gehören zu jedem Trainingslauf (Goodfellow et al., 2016).
- Wenn ein schneller, robuster Standardoptimierer gebraucht wird, funktionieren Adam oder AdamW mit wenig Tuning (Kingma & Ba, 2014; Loshchilov & Hutter, 2017).
- Wenn sehr tiefe Netze nicht trainieren, sind Initialisierung und Normalisierung das Erste, was zu prüfen ist (He et al., 2015; Ioffe & Szegedy, 2015).

### Stärken und Grenzen

**Stärken**
- Backpropagation berechnet alle Gradienten effizient (Goodfellow et al., 2016).
- Adam braucht wenig Tuning und kommt mit verrauschten oder dünnbesetzten Gradienten zurecht (Kingma & Ba, 2014).
- Batch Normalization erlaubt höhere Lernraten und weniger Trainingsschritte (Ioffe & Szegedy, 2015).

**Einschränkungen**
- Die Ergebnisse hängen stark von Lernrate und anderen Hyperparametern ab (Goodfellow et al., 2016).
- Mit gewöhnlicher Initialisierung trainieren tiefe Netze möglicherweise schlecht (Glorot & Bengio, 2010).
- Bei Adam wirkt L2-Regularisierung nur dann als Weight Decay, wenn sie entkoppelt wird (Loshchilov & Hutter, 2017).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| SGD mit Momentum | Gleiche Schrittweite für alle Parameter, sammelt frühere Gradienten (Goodfellow et al., 2016) | Gut abgestimmtes Training, Bildklassifikation |
| Adam | Schrittweite je Parameter aus Momenten der Gradienten (Kingma & Ba, 2014) | Standardwahl, dünnbesetzte oder verrauschte Gradienten |
| AdamW | Adam mit entkoppeltem Weight Decay (Loshchilov & Hutter, 2017) | Regularisiertes Training mit adaptiven Schritten |

### In der Praxis

Ein Trainingslauf legt Verlustfunktion, Optimierer, Lernrate (oft mit Zeitplan), Batchgröße und Epochenzahl fest und protokolliert Trainings- und Validierungskurven (Goodfellow et al., 2016; [[experiment-tracking|Experiment Tracking]]). Zur Aktivierungsfunktion passende Initialisierungen sind in modernen Frameworks voreingestellt (He et al., 2015), und das Modell wird auf zurückgehaltenen Daten evaluiert ([[neural-network-evaluation|Modellbewertung neuronaler Netze]]).

### Merksatz

Training wiederholt Vorwärtsdurchlauf, Verlust, Backpropagation und Gewichtsaktualisierung auf kleinen Batches; gute Initialisierung, Normalisierung, Optimierer und Lernrate entscheiden über den Erfolg.

### Quellen

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks.* AISTATS 2010. [PMLR](https://proceedings.mlr.press/v9/glorot10a.html)
- He, K. et al. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification.* ICCV 2015. [arXiv:1502.01852](https://arxiv.org/abs/1502.01852)
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization.* ICLR 2015. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift.* ICML 2015. [arXiv:1502.03167](https://arxiv.org/abs/1502.03167)
