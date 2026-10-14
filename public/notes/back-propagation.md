---
title_en: Back-Propagation
title_de: Backpropagation
entity_type: Method
aliases:
- Back-propagation
- Backpropagation
- Backprop
- Reverse-mode automatic differentiation
sources:
- https://www.deeplearningbook.org/contents/mlp.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Back-propagation ("backprop") computes the gradient of a network's cost with respect to all its parameters by applying the chain rule backwards through the computational graph, from the cost to the inputs, while reusing intermediate results so that each partial derivative is computed only once (Goodfellow et al., 2016). It is only the method for computing gradients; an optimiser such as stochastic gradient descent then uses them to update the weights ([[neural-network-training|neural network training]]). Back-propagation is a special case of reverse-mode automatic differentiation and works for any differentiable function, not only multilayer networks (Goodfellow et al., 2016). Its popularisation by Rumelhart, Hinton and Williams in 1986 made training multilayer [[neural-networks|neural networks]] practical.

### How it works

```text
forward pass:  input x → layer by layer → prediction ŷ → scalar cost J(θ); store intermediate values
backward pass: start with ∂J/∂J = 1
               for each node in reverse order:
                 gradient w.r.t. its inputs = (gradient w.r.t. its output) × (local Jacobian)   [chain rule]
                 sum contributions from all paths that use the node
result: ∂J/∂θ for every weight → optimiser step (e.g. SGD: θ ← θ − η ∂J/∂θ)
```

#### 1. Forward propagation and the cost

In a feedforward network, the input provides initial information that propagates through the hidden units of each layer and produces an output ŷ; during training this forward propagation continues until it produces a scalar cost J(θ) (Goodfellow et al., 2016). Writing down an analytical expression for the gradient of J is straightforward, but evaluating it naively is computationally expensive, because many subexpressions repeat. Back-propagation evaluates it with a simple and inexpensive procedure (Goodfellow et al., 2016).

#### 2. Computational graphs

To describe the algorithm precisely, the computation is written as a graph in which each node is a variable, such as a scalar, vector, matrix or tensor, and each operation is a simple function of one or more variables (Goodfellow et al., 2016). More complex functions are composed of these operations. The same graph language covers multilayer perceptrons, convolutional and recurrent networks and the Transformer blocks of [[large-language-models|large language models]].

#### 3. The chain rule, applied backwards

The chain rule of calculus gives the derivative of a composition of functions from the derivatives of its parts. For a scalar cost and a graph of operations, back-propagation starts at the cost and moves backwards, multiplying each node's gradient by the Jacobian of the operation that produced it and summing over all paths through which a variable influences the cost (Goodfellow et al., 2016). The same idea applies to tensors of any shape: conceptually, tensors are flattened into vectors, a gradient is computed and reshaped back (Goodfellow et al., 2016).

#### 4. Dynamic programming: storing intermediate results

The key to efficiency is that each node stores its gradient in a table once it is computed; filling this table in order avoids recomputing common subexpressions, a strategy called dynamic programming (Goodfellow et al., 2016). Back-propagation visits each edge of the graph once and performs on the order of one Jacobian product per node, so its cost is proportional to that of the forward pass. The price is memory: intermediate values from the forward pass must be kept. Recomputing some of them instead of storing them trades run time for memory, as in gradient checkpointing (Goodfellow et al., 2016).

#### 5. An example: training a multilayer perceptron

For a network with one hidden layer, `H = max{0, X W⁽¹⁾}` with a ReLU, followed by an output layer and a cross-entropy cost plus weight decay, the backward pass computes the gradient with respect to the output weights from the hidden activations, passes the gradient through the output weights to the hidden layer, zeroes it where the ReLU was inactive, and then computes the gradient with respect to the first-layer weights (Goodfellow et al., 2016). Minibatch stochastic gradient descent then updates both weight matrices.

#### Origin and variants

The chain rule dates back to Leibniz (1676) and L'Hôpital (1696), and gradient descent to Cauchy (1847) (Goodfellow et al., 2016). Efficient chain-rule computations based on dynamic programming appeared in the 1960s and 1970s for control and sensitivity analysis; Werbos (1981) proposed applying them to neural networks, and the idea was independently rediscovered and put into practice by LeCun (1985), Parker (1985) and Rumelhart, Hinton and Williams (1986), whose work started a very active period of research on multilayer networks (Goodfellow et al., 2016). The core ideas, back-propagation plus gradient descent, have not changed substantially since the 1980s; most later gains came from larger datasets and larger networks (Goodfellow et al., 2016). Modern frameworks implement back-propagation as reverse-mode automatic differentiation ([[keras-and-tensorflow|Keras and TensorFlow]]).

### When to use it

- Training any differentiable model with gradient-based optimisation, from logistic regression to Transformers ([[neural-network-training|neural network training]]).
- Computing gradients of a scalar output with respect to many inputs, where reverse mode is far cheaper than computing each derivative separately (Goodfellow et al., 2016).
- Gradient-based explanation methods that need derivatives of a prediction with respect to the input ([[explainable-ai|explainable AI]]).

### Strengths and limitations

**Strengths**
- Computes all gradients at a cost comparable to one forward pass (Goodfellow et al., 2016).
- General: works for any differentiable computational graph (Goodfellow et al., 2016).
- Implemented automatically by deep learning frameworks.

**Limitations**
- Needs memory for the intermediate values of the forward pass, which limits batch size and model size (Goodfellow et al., 2016).
- Gives only gradients; whether training succeeds depends on the optimiser, initialisation and architecture, for example vanishing gradients in very deep networks ([[resnet|ResNet]]).
- Not applicable to non-differentiable operations without approximations.

### Comparison

| Approach | Computes | Cost for many parameters |
|---|---|---|
| Symbolic differentiation | analytical expression | expression can blow up with repeated subexpressions |
| Numerical differences | approximation per parameter | one extra evaluation per parameter |
| Back-propagation (reverse mode) | exact gradients of a scalar | about one backward pass |

Source: Goodfellow et al. (2016).

### In practice

Gradient problems show up as vanishing or exploding gradients; normalisation, careful initialisation and residual connections address them ([[neural-network-training|neural network training]], [[resnet|ResNet]]). When memory runs short, gradient checkpointing recomputes activations during the backward pass, and mixed precision reduces the size of stored values ([[mixed-precision-training|mixed precision training]]).

### Key takeaway

Back-propagation applies the chain rule backwards through the computational graph and stores intermediate results, computing all gradients of a scalar cost at about the cost of one forward pass; optimisers then use these gradients to train the network.

### Sources

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 6: Deep Feedforward Networks (sections 6.5–6.6). MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Backpropagation („Backprop“) berechnet den Gradienten der Kostenfunktion eines Netzes nach allen seinen Parametern, indem es die Kettenregel rückwärts durch den Rechengraphen anwendet, von den Kosten zu den Eingaben, und dabei Zwischenergebnisse wiederverwendet, sodass jede partielle Ableitung nur einmal berechnet wird (Goodfellow et al., 2016). Es ist nur das Verfahren zur Berechnung der Gradienten; ein Optimierer wie der stochastische Gradientenabstieg nutzt sie dann, um die Gewichte anzupassen ([[neural-network-training|Training neuronaler Netze]]). Backpropagation ist ein Spezialfall der automatischen Differentiation im Rückwärtsmodus und funktioniert für jede differenzierbare Funktion, nicht nur für mehrschichtige Netze (Goodfellow et al., 2016). Seine Verbreitung durch Rumelhart, Hinton und Williams 1986 machte das Training mehrschichtiger [[neural-networks|neuronaler Netze]] praktikabel.

### Funktionsweise

```text
Vorwärtsdurchlauf:  Eingabe x → Schicht für Schicht → Vorhersage ŷ → skalare Kosten J(θ); Zwischenwerte speichern
Rückwärtsdurchlauf: beginnen mit ∂J/∂J = 1
                    für jeden Knoten in umgekehrter Reihenfolge:
                      Gradient nach seinen Eingaben = (Gradient nach seiner Ausgabe) × (lokale Jacobi-Matrix)   [Kettenregel]
                      Beiträge aller Pfade aufsummieren, die den Knoten nutzen
Ergebnis: ∂J/∂θ für jedes Gewicht → Optimierungsschritt (z. B. SGD: θ ← θ − η ∂J/∂θ)
```

#### 1. Vorwärtsdurchlauf und Kosten

In einem Feedforward-Netz liefert die Eingabe die Anfangsinformation, die sich durch die verborgenen Einheiten jeder Schicht fortpflanzt und eine Ausgabe ŷ erzeugt; im Training läuft dieser Vorwärtsdurchlauf weiter, bis er skalare Kosten J(θ) ergibt (Goodfellow et al., 2016). Einen analytischen Ausdruck für den Gradienten von J aufzuschreiben, ist einfach, ihn naiv auszuwerten aber rechenaufwendig, weil sich viele Teilausdrücke wiederholen. Backpropagation wertet ihn mit einem einfachen und günstigen Verfahren aus (Goodfellow et al., 2016).

#### 2. Rechengraphen

Um den Algorithmus genau zu beschreiben, wird die Berechnung als Graph geschrieben, in dem jeder Knoten eine Variable ist, etwa ein Skalar, Vektor, eine Matrix oder ein Tensor, und jede Operation eine einfache Funktion einer oder mehrerer Variablen (Goodfellow et al., 2016). Komplexere Funktionen setzen sich aus diesen Operationen zusammen. Dieselbe Graphsprache erfasst mehrschichtige Perzeptrons, Convolutional und rekurrente Netze sowie die Transformer-Blöcke [[large-language-models|großer Sprachmodelle]].

#### 3. Die Kettenregel, rückwärts angewendet

Die Kettenregel der Analysis liefert die Ableitung einer Verkettung von Funktionen aus den Ableitungen ihrer Teile. Bei skalaren Kosten und einem Graphen aus Operationen beginnt Backpropagation bei den Kosten und geht rückwärts, multipliziert den Gradienten jedes Knotens mit der Jacobi-Matrix der Operation, die ihn erzeugt hat, und summiert über alle Pfade, über die eine Variable die Kosten beeinflusst (Goodfellow et al., 2016). Dieselbe Idee gilt für Tensoren beliebiger Form: Gedanklich werden Tensoren zu Vektoren abgeflacht, ein Gradient berechnet und zurückgeformt (Goodfellow et al., 2016).

#### 4. Dynamische Programmierung: Zwischenergebnisse speichern

Der Schlüssel zur Effizienz ist, dass jeder Knoten seinen Gradienten nach der Berechnung in einer Tabelle ablegt; das Füllen dieser Tabelle in der richtigen Reihenfolge vermeidet das erneute Berechnen gemeinsamer Teilausdrücke, eine Strategie, die dynamische Programmierung heißt (Goodfellow et al., 2016). Backpropagation besucht jede Kante des Graphen einmal und führt in der Größenordnung ein Produkt mit einer Jacobi-Matrix je Knoten aus, sodass ihr Aufwand dem des Vorwärtsdurchlaufs entspricht. Der Preis ist Speicher: Zwischenwerte des Vorwärtsdurchlaufs müssen aufbewahrt werden. Einige davon neu zu berechnen statt zu speichern, tauscht Laufzeit gegen Speicher, wie beim Gradient Checkpointing (Goodfellow et al., 2016).

#### 5. Ein Beispiel: Training eines mehrschichtigen Perzeptrons

Für ein Netz mit einer verborgenen Schicht, `H = max{0, X W⁽¹⁾}` mit ReLU, gefolgt von einer Ausgabeschicht und Cross-Entropy-Kosten plus Weight Decay, berechnet der Rückwärtsdurchlauf den Gradienten nach den Ausgabegewichten aus den verborgenen Aktivierungen, gibt den Gradienten über die Ausgabegewichte an die verborgene Schicht weiter, setzt ihn dort auf null, wo die ReLU inaktiv war, und berechnet dann den Gradienten nach den Gewichten der ersten Schicht (Goodfellow et al., 2016). Stochastischer Gradientenabstieg mit Minibatches passt dann beide Gewichtsmatrizen an.

#### Herkunft und Varianten

Die Kettenregel geht auf Leibniz (1676) und L'Hôpital (1696) zurück, der Gradientenabstieg auf Cauchy (1847) (Goodfellow et al., 2016). Effiziente Anwendungen der Kettenregel auf Basis dynamischer Programmierung erschienen in den 1960er- und 1970er-Jahren für Regelungstechnik und Sensitivitätsanalyse; Werbos (1981) schlug vor, sie auf neuronale Netze anzuwenden, und die Idee wurde unabhängig von LeCun (1985), Parker (1985) sowie Rumelhart, Hinton und Williams (1986) wiederentdeckt und praktisch umgesetzt, deren Arbeit eine sehr aktive Forschungsphase zu mehrschichtigen Netzen auslöste (Goodfellow et al., 2016). Die Kernideen, Backpropagation plus Gradientenabstieg, haben sich seit den 1980er-Jahren kaum verändert; die meisten späteren Fortschritte kamen von größeren Datensätzen und größeren Netzen (Goodfellow et al., 2016). Moderne Frameworks setzen Backpropagation als automatische Differentiation im Rückwärtsmodus um ([[keras-and-tensorflow|Keras und TensorFlow]]).

### Wann einsetzen

- Training jedes differenzierbaren Modells mit gradientenbasierter Optimierung, von logistischer Regression bis zu Transformern ([[neural-network-training|Training neuronaler Netze]]).
- Berechnung der Gradienten einer skalaren Ausgabe nach vielen Eingaben, wo der Rückwärtsmodus weit günstiger ist als jede Ableitung einzeln zu berechnen (Goodfellow et al., 2016).
- Gradientenbasierte Erklärungsverfahren, die Ableitungen einer Vorhersage nach der Eingabe brauchen ([[explainable-ai|Explainable AI]]).

### Stärken und Grenzen

**Stärken**
- Berechnet alle Gradienten mit einem Aufwand vergleichbar einem Vorwärtsdurchlauf (Goodfellow et al., 2016).
- Allgemein: funktioniert für jeden differenzierbaren Rechengraphen (Goodfellow et al., 2016).
- Wird von Deep-Learning-Frameworks automatisch umgesetzt.

**Grenzen**
- Braucht Speicher für die Zwischenwerte des Vorwärtsdurchlaufs, was Batch- und Modellgröße begrenzt (Goodfellow et al., 2016).
- Liefert nur Gradienten; ob das Training gelingt, hängt von Optimierer, Initialisierung und Architektur ab, etwa bei verschwindenden Gradienten in sehr tiefen Netzen ([[resnet|ResNet]]).
- Ohne Näherungen nicht auf nicht differenzierbare Operationen anwendbar.

### Vergleich

| Ansatz | Berechnet | Aufwand bei vielen Parametern |
|---|---|---|
| Symbolische Differentiation | analytischen Ausdruck | Ausdruck kann durch wiederholte Teilausdrücke explodieren |
| Numerische Differenzen | Näherung je Parameter | eine zusätzliche Auswertung je Parameter |
| Backpropagation (Rückwärtsmodus) | exakte Gradienten eines Skalars | etwa ein Rückwärtsdurchlauf |

Quelle: Goodfellow et al. (2016).

### In der Praxis

Gradientenprobleme zeigen sich als verschwindende oder explodierende Gradienten; Normalisierung, sorgfältige Initialisierung und Residualverbindungen wirken dagegen ([[neural-network-training|Training neuronaler Netze]], [[resnet|ResNet]]). Wird der Speicher knapp, berechnet Gradient Checkpointing Aktivierungen im Rückwärtsdurchlauf neu, und Mixed Precision verkleinert die gespeicherten Werte ([[mixed-precision-training|Mixed-Precision-Training]]).

### Merksatz

Backpropagation wendet die Kettenregel rückwärts durch den Rechengraphen an und speichert Zwischenergebnisse; so berechnet es alle Gradienten skalarer Kosten mit etwa dem Aufwand eines Vorwärtsdurchlaufs, und Optimierer nutzen diese Gradienten, um das Netz zu trainieren.

### Quellen

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 6: Deep Feedforward Networks (Abschnitte 6.5–6.6). MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)
