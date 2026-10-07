---
title_en: Neural Networks
title_de: Neuronale Netze
entity_type: Method
sources:
- https://doi.org/10.1038/323533a0
- https://doi.org/10.1016/0893-6080%2889%2990020-8
- https://doi.org/10.1038/nature14539
- https://www.deeplearningbook.org/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A neural network is a model built from layers of simple units, each computing a weighted sum of its inputs plus a bias and passing it through a non-linear activation function (Goodfellow et al., 2016). Networks with a hidden layer can approximate any reasonable function given enough units (Hornik et al., 1989), and they learn their weights from data with back-propagation (Rumelhart et al., 1986). Deep networks with many layers learn representations at several levels of abstraction and are the basis of modern image, speech and language processing (LeCun et al., 2015).

### How it works

Inputs flow through the network layer by layer in a forward pass; each layer transforms its input into a new representation, and the output layer produces the prediction. Training then adjusts the weights so that the predictions move closer to the targets ([[neural-network-training|Training Neural Networks]]).

```text
1. Units, weights and bias
▼
2. Layers and architecture
▼
3. Activation functions
▼
4. Forward pass and output layer
▼
5. Learning the weights
▼
6. Depth and representation learning
```

#### 1. Units, weights and bias

Each unit computes a weighted sum of its inputs, adds a bias and applies an activation function (Goodfellow et al., 2016). The weights determine how strongly each input contributes, and the bias shifts the point at which the unit becomes active. The perceptron, a single such unit with a threshold, is the historical starting point; a single layer can only separate classes linearly.

#### 2. Layers and architecture

Units are arranged in layers: an input layer that receives the features, one or more hidden layers, and an output layer (Goodfellow et al., 2016). In a fully connected (dense) layer every unit receives every output of the previous layer. Hornik et al. (1989) proved that standard feedforward networks with as few as one hidden layer and squashing activation functions can approximate any Borel measurable function to any desired accuracy, provided there are enough hidden units. Specialised layer types exploit structure in the data, such as convolutions for images ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]) and recurrence for sequences ([[recurrent-neural-networks|Recurrent Neural Networks and Time Series]]).

#### 3. Activation functions

Without non-linear activation functions, a stack of layers would collapse into a single linear transformation. The rectified linear unit (ReLU), max(0, x), is the default recommendation for hidden units; sigmoid and tanh saturate for large inputs, which slows learning (Goodfellow et al., 2016).

#### 4. Forward pass and output layer

The forward pass computes the output from the input layer by layer (Goodfellow et al., 2016). The output layer and the loss are chosen together: for classification, a softmax output turns scores into class probabilities and is trained with cross-entropy; for regression, a linear output with squared error is common.

#### 5. Learning the weights

Rumelhart et al. (1986) described back-propagation: the weights are repeatedly adjusted to reduce the difference between the actual and the desired output, using gradients computed backwards through the network with the chain rule. As a result, hidden units come to represent important features of the task that were never specified explicitly.

#### 6. Depth and representation learning

Deep learning uses models with many processing layers that learn representations of data with multiple levels of abstraction (LeCun et al., 2015). Deep convolutional networks brought breakthroughs in images, video, speech and audio, and recurrent networks in sequential data such as text and speech; Transformers later became the standard for language ([[attention-and-transformers|Attention and Transformers]]).

#### Origin and variants

Back-propagation (Rumelhart et al., 1986) made multilayer networks trainable, the universal approximation theorem (Hornik et al., 1989) established their expressive power, and deep learning (LeCun et al., 2015) scaled them to many layers. Goodfellow et al. (2016) give a textbook treatment.

### When to use it

- When data is unstructured, such as images, audio or text, and features are hard to engineer by hand (LeCun et al., 2015).
- When large amounts of training data and compute are available (LeCun et al., 2015).
- For medium-sized tabular data, tree ensembles are often the stronger choice ([[classical-machine-learning|Classical Machine Learning Methods]]).

### Strengths and limitations

**Strengths**
- Can approximate any reasonable function given enough hidden units (Hornik et al., 1989).
- Learn useful internal features from data instead of hand-crafted ones (Rumelhart et al., 1986).
- Deep networks learn hierarchical representations (LeCun et al., 2015).

**Limitations**
- The approximation theorem says nothing about how many units are needed or how to find the weights (Hornik et al., 1989).
- Saturating activations slow learning (Goodfellow et al., 2016).
- Learned representations are hard to interpret ([[explainable-ai|Explainable AI (XAI)]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Perceptron | Single unit, linear decision boundary (Goodfellow et al., 2016) | Linearly separable problems |
| Multilayer perceptron | Hidden layers with non-linear activations (Hornik et al., 1989) | General function approximation |
| Deep networks | Many layers learning hierarchical representations (LeCun et al., 2015) | Images, speech, text |

### In practice

Architecture size, activation functions and the output layer are chosen to match the task (Goodfellow et al., 2016), and the network is trained and evaluated on separate data ([[neural-network-training|Training Neural Networks]], [[neural-network-evaluation|Evaluating Neural Networks]]). Frameworks such as Keras and PyTorch provide layers and automatic gradients ([[keras-and-tensorflow|Keras and TensorFlow]]).

### Key takeaway

A neural network stacks layers of weighted sums and non-linear activations; trained with back-propagation, it learns its own features from data.

### Sources

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). *Learning representations by back-propagating errors.* Nature 323. [doi:10.1038/323533a0](https://doi.org/10.1038/323533a0)
- Hornik, K., Stinchcombe, M. & White, H. (1989). *Multilayer feedforward networks are universal approximators.* Neural Networks 2(5). [doi:10.1016/0893-6080(89)90020-8](https://doi.org/10.1016/0893-6080%2889%2990020-8)
- LeCun, Y., Bengio, Y. & Hinton, G. (2015). *Deep learning.* Nature 521. [doi:10.1038/nature14539](https://doi.org/10.1038/nature14539)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein neuronales Netz ist ein Modell aus Schichten einfacher Einheiten, die jeweils eine gewichtete Summe ihrer Eingaben plus einen Bias berechnen und durch eine nichtlineare Aktivierungsfunktion leiten (Goodfellow et al., 2016). Netze mit einer verborgenen Schicht können bei genügend Einheiten jede vernünftige Funktion annähern (Hornik et al., 1989), und sie lernen ihre Gewichte mit Backpropagation aus Daten (Rumelhart et al., 1986). Tiefe Netze mit vielen Schichten lernen Repräsentationen auf mehreren Abstraktionsebenen und bilden die Grundlage moderner Bild-, Sprach- und Textverarbeitung (LeCun et al., 2015).

### Funktionsweise

Eingaben durchlaufen das Netz in einem Vorwärtsdurchlauf Schicht für Schicht; jede Schicht formt ihre Eingabe in eine neue Repräsentation um, und die Ausgabeschicht liefert die Vorhersage. Das Training passt anschließend die Gewichte so an, dass die Vorhersagen den Zielwerten näherkommen ([[neural-network-training|Training neuronaler Netze]]).

```text
1. Einheiten, Gewichte und Bias
▼
2. Schichten und Architektur
▼
3. Aktivierungsfunktionen
▼
4. Vorwärtsdurchlauf und Ausgabeschicht
▼
5. Lernen der Gewichte
▼
6. Tiefe und Repräsentationslernen
```

#### 1. Einheiten, Gewichte und Bias

Jede Einheit berechnet eine gewichtete Summe ihrer Eingaben, addiert einen Bias und wendet eine Aktivierungsfunktion an (Goodfellow et al., 2016). Die Gewichte bestimmen, wie stark jede Eingabe beiträgt, und der Bias verschiebt den Punkt, ab dem die Einheit aktiv wird. Das Perzeptron, eine einzelne solche Einheit mit Schwellenwert, ist der historische Ausgangspunkt; eine einzelne Schicht kann Klassen nur linear trennen.

#### 2. Schichten und Architektur

Einheiten sind in Schichten angeordnet: eine Eingabeschicht, die die Merkmale aufnimmt, eine oder mehrere verborgene Schichten und eine Ausgabeschicht (Goodfellow et al., 2016). In einer vollständig verbundenen (Dense-)Schicht erhält jede Einheit jede Ausgabe der vorherigen Schicht. Hornik et al. (1989) bewiesen, dass gewöhnliche Feedforward-Netze mit nur einer verborgenen Schicht und sättigenden Aktivierungsfunktionen jede Borel-messbare Funktion beliebig genau annähern können, sofern genügend verborgene Einheiten vorhanden sind. Spezialisierte Schichttypen nutzen Strukturen in den Daten, etwa Faltungen für Bilder ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]) und Rekurrenz für Sequenzen ([[recurrent-neural-networks|RNN und Zeitreihen]]).

#### 3. Aktivierungsfunktionen

Ohne nichtlineare Aktivierungsfunktionen fiele ein Stapel von Schichten in eine einzige lineare Transformation zusammen. Die Rectified Linear Unit (ReLU), max(0, x), ist die Standardempfehlung für verborgene Einheiten; Sigmoid und tanh sättigen bei großen Eingaben, was das Lernen verlangsamt (Goodfellow et al., 2016).

#### 4. Vorwärtsdurchlauf und Ausgabeschicht

Der Vorwärtsdurchlauf berechnet die Ausgabe aus der Eingabe Schicht für Schicht (Goodfellow et al., 2016). Ausgabeschicht und Verlustfunktion werden zusammen gewählt: Bei Klassifikation macht eine Softmax-Ausgabe aus Werten Klassenwahrscheinlichkeiten und wird mit Kreuzentropie trainiert; bei Regression ist eine lineare Ausgabe mit quadratischem Fehler üblich.

#### 5. Lernen der Gewichte

Rumelhart et al. (1986) beschrieben Backpropagation: Die Gewichte werden wiederholt so angepasst, dass der Unterschied zwischen tatsächlicher und gewünschter Ausgabe kleiner wird, mithilfe von Gradienten, die mit der Kettenregel rückwärts durch das Netz berechnet werden. Dadurch lernen verborgene Einheiten, wichtige Merkmale der Aufgabe darzustellen, die nie ausdrücklich vorgegeben wurden.

#### 6. Tiefe und Repräsentationslernen

Deep Learning nutzt Modelle mit vielen Verarbeitungsschichten, die Repräsentationen von Daten auf mehreren Abstraktionsebenen lernen (LeCun et al., 2015). Tiefe konvolutionale Netze brachten Durchbrüche bei Bildern, Video, Sprache und Audio, rekurrente Netze bei sequenziellen Daten wie Text und gesprochener Sprache; später wurden Transformer zum Standard für Sprache ([[attention-and-transformers|Attention und Transformer]]).

#### Ursprung und Varianten

Backpropagation (Rumelhart et al., 1986) machte mehrschichtige Netze trainierbar, das universelle Approximationstheorem (Hornik et al., 1989) belegte ihre Ausdruckskraft, und Deep Learning (LeCun et al., 2015) skalierte sie auf viele Schichten. Goodfellow et al. (2016) bieten eine Lehrbuchdarstellung.

### Wann einsetzen

- Wenn Daten unstrukturiert sind, etwa Bilder, Audio oder Text, und sich Merkmale schwer von Hand konstruieren lassen (LeCun et al., 2015).
- Wenn große Mengen an Trainingsdaten und Rechenleistung verfügbar sind (LeCun et al., 2015).
- Bei mittelgroßen tabellarischen Daten sind Baum-Ensembles oft die stärkere Wahl ([[classical-machine-learning|Klassische ML-Verfahren]]).

### Stärken und Grenzen

**Stärken**
- Können bei genügend verborgenen Einheiten jede vernünftige Funktion annähern (Hornik et al., 1989).
- Lernen nützliche interne Merkmale aus Daten statt handgefertigter Merkmale (Rumelhart et al., 1986).
- Tiefe Netze lernen hierarchische Repräsentationen (LeCun et al., 2015).

**Einschränkungen**
- Das Approximationstheorem sagt nichts darüber, wie viele Einheiten nötig sind oder wie man die Gewichte findet (Hornik et al., 1989).
- Sättigende Aktivierungsfunktionen verlangsamen das Lernen (Goodfellow et al., 2016).
- Gelernte Repräsentationen sind schwer zu interpretieren ([[explainable-ai|Erklärbare KI (XAI)]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Perzeptron | Einzelne Einheit, lineare Entscheidungsgrenze (Goodfellow et al., 2016) | Linear trennbare Probleme |
| Mehrschichtiges Perzeptron | Verborgene Schichten mit nichtlinearen Aktivierungen (Hornik et al., 1989) | Allgemeine Funktionsapproximation |
| Tiefe Netze | Viele Schichten, die hierarchische Repräsentationen lernen (LeCun et al., 2015) | Bilder, Sprache, Text |

### In der Praxis

Netzgröße, Aktivierungsfunktionen und Ausgabeschicht werden passend zur Aufgabe gewählt (Goodfellow et al., 2016), und das Netz wird auf getrennten Daten trainiert und evaluiert ([[neural-network-training|Training neuronaler Netze]], [[neural-network-evaluation|Modellbewertung neuronaler Netze]]). Frameworks wie Keras und PyTorch stellen Schichten und automatische Gradienten bereit ([[keras-and-tensorflow|Keras und TensorFlow]]).

### Merksatz

Ein neuronales Netz stapelt Schichten aus gewichteten Summen und nichtlinearen Aktivierungen; mit Backpropagation trainiert, lernt es seine Merkmale selbst aus den Daten.

### Quellen

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). *Learning representations by back-propagating errors.* Nature 323. [doi:10.1038/323533a0](https://doi.org/10.1038/323533a0)
- Hornik, K., Stinchcombe, M. & White, H. (1989). *Multilayer feedforward networks are universal approximators.* Neural Networks 2(5). [doi:10.1016/0893-6080(89)90020-8](https://doi.org/10.1016/0893-6080%2889%2990020-8)
- LeCun, Y., Bengio, Y. & Hinton, G. (2015). *Deep learning.* Nature 521. [doi:10.1038/nature14539](https://doi.org/10.1038/nature14539)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
