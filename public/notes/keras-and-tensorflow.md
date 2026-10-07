---
title_en: Keras and TensorFlow
title_de: Keras und TensorFlow
entity_type: Technology
sources:
- https://arxiv.org/abs/1603.04467
- https://keras.io/guides/sequential_model/
- https://keras.io/guides/functional_api/
- https://keras.io/guides/training_with_built_in_methods/
- https://arxiv.org/abs/1912.01703
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

TensorFlow is a system for expressing machine learning computations and executing them on hardware ranging from phones to large GPU clusters (Abadi et al., 2016). Keras is a high-level API for building and training neural networks: models are defined as a sequence of layers or as a graph of layers, configured with compile() and trained with fit() (Keras Sequential guide; Keras Functional API guide; Keras training guide). PyTorch is the main alternative, with an imperative, Pythonic style (Paszke et al., 2019).

### Core concepts

- **Computation graphs and devices:** A TensorFlow computation can run with little or no change on heterogeneous systems, from mobile devices to distributed systems with thousands of GPUs, and is used for both research and production (Abadi et al., 2016).
- **Layers and models:** Keras models are built from layers. A Sequential model is a plain stack of layers in which each layer has exactly one input and one output tensor (Keras Sequential guide).
- **Functional API:** Most deep learning models are directed acyclic graphs of layers; the functional API builds such graphs and supports non-linear topologies, shared layers and multiple inputs or outputs. Models can also be written by subclassing the Model class (Keras Functional API guide).
- **compile() and fit():** compile() specifies the loss function, the optimizer and optional metrics; fit() then trains the model on data for a number of epochs with a batch size, evaluate() measures performance and predict() produces outputs (Keras training guide; [[neural-network-training|Training Neural Networks]]).
- **Backends:** The Keras developer guides cover training with JAX, TensorFlow and PyTorch as backends (Keras Sequential guide).

### Common usage

A simple classifier is defined as a Sequential model of Dense layers, compiled with an optimizer, a loss and an accuracy metric, and trained with fit() on training data while validation data is held out (Keras Sequential guide; Keras training guide). For sequence data, recurrent layers such as LSTM are stacked in the same way ([[recurrent-neural-networks|Recurrent Neural Networks and Time Series]]); for images, convolution and pooling layers are combined ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]). Models with several inputs, outputs or skip connections use the functional API (Keras Functional API guide). Callbacks such as early stopping and model checkpoints hook into fit() (Keras training guide).

```python
import keras
from keras import layers

model = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)
```

### When to use it

- When standard architectures should be built and trained with little code, Keras's Sequential and functional APIs fit (Keras Sequential guide; Keras Functional API guide).
- When models must be deployed across devices, from mobile to distributed systems, the TensorFlow ecosystem helps (Abadi et al., 2016).
- When research code needs full control in plain Python and easy debugging, PyTorch is a common alternative (Paszke et al., 2019).

### Strengths and limitations

**Strengths**
- compile() and fit() cover the standard training loop with very little code (Keras training guide).
- The functional API supports complex topologies with shared layers and multiple inputs and outputs (Keras Functional API guide).
- TensorFlow runs the same computation on very different hardware (Abadi et al., 2016).

**Limitations**
- The Sequential model does not support multiple inputs or outputs, shared layers or non-linear topology (Keras Sequential guide).
- Non-standard training procedures require customising fit() or writing a custom training loop (Keras training guide).
- For research that favours an imperative style, PyTorch is often preferred (Paszke et al., 2019).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Keras Sequential API | Linear stack of layers (Keras Sequential guide) | Simple feedforward, CNN or RNN models |
| Keras functional API | Graph of layers with shared layers and multiple inputs and outputs (Keras Functional API guide) | Multi-input models, skip connections |
| Model subclassing | Model logic written as a Python class (Keras Functional API guide) | Custom architectures |
| PyTorch | Imperative, Pythonic library where every model is a regular Python program (Paszke et al., 2019) | Research and custom training loops |

### In practice

Training runs log their configuration and metrics ([[experiment-tracking|Experiment Tracking]]) and use callbacks for early stopping and checkpoints (Keras training guide). Saved models are reloaded for evaluation and deployment ([[mlops-and-deployment|MLOps and Deployment]]).

### Key takeaway

Keras builds and trains neural networks with a few high-level calls on top of backends such as TensorFlow; the functional API covers models that are more than a simple stack of layers.

### Sources

- Abadi, M. et al. (2016). *TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems.* Whitepaper. [arXiv:1603.04467](https://arxiv.org/abs/1603.04467)
- Keras team. *The Sequential model.* Keras developer guide. [keras.io](https://keras.io/guides/sequential_model/)
- Keras team. *The Functional API.* Keras developer guide. [keras.io](https://keras.io/guides/functional_api/)
- Keras team. *Training & evaluation with the built-in methods.* Keras developer guide. [keras.io](https://keras.io/guides/training_with_built_in_methods/)
- Paszke, A. et al. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library.* NeurIPS 2019. [arXiv:1912.01703](https://arxiv.org/abs/1912.01703)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

TensorFlow ist ein System, um Berechnungen des maschinellen Lernens auszudrücken und auf Hardware vom Smartphone bis zum großen GPU-Cluster auszuführen (Abadi et al., 2016). Keras ist eine High-Level-API zum Aufbauen und Trainieren neuronaler Netze: Modelle werden als Folge von Schichten oder als Graph aus Schichten definiert, mit compile() konfiguriert und mit fit() trainiert (Keras Sequential guide; Keras Functional API guide; Keras training guide). PyTorch ist die wichtigste Alternative mit einem imperativen, pythonischen Stil (Paszke et al., 2019).

### Kernkonzepte

- **Berechnungsgraphen und Geräte:** Eine TensorFlow-Berechnung läuft mit wenigen oder keinen Änderungen auf heterogenen Systemen, von Mobilgeräten bis zu verteilten Systemen mit Tausenden GPUs, und wird in Forschung und Produktivbetrieb eingesetzt (Abadi et al., 2016).
- **Schichten und Modelle:** Keras-Modelle bestehen aus Schichten. Ein Sequential-Modell ist ein einfacher Stapel von Schichten, bei dem jede Schicht genau einen Eingabe- und einen Ausgabetensor hat (Keras Sequential guide).
- **Functional API:** Die meisten Deep-Learning-Modelle sind gerichtete azyklische Graphen aus Schichten; die Functional API baut solche Graphen und unterstützt nichtlineare Topologien, geteilte Schichten und mehrere Ein- oder Ausgaben. Modelle lassen sich auch durch Ableiten der Model-Klasse schreiben (Keras Functional API guide).
- **compile() und fit():** compile() legt Verlustfunktion, Optimierer und optionale Metriken fest; fit() trainiert das Modell dann über eine Zahl von Epochen mit einer Batchgröße, evaluate() misst die Leistung und predict() erzeugt Ausgaben (Keras training guide; [[neural-network-training|Training neuronaler Netze]]).
- **Backends:** Die Keras-Entwicklerleitfäden behandeln das Training mit JAX, TensorFlow und PyTorch als Backend (Keras Sequential guide).

### Typische Verwendung

Ein einfacher Klassifikator wird als Sequential-Modell aus Dense-Schichten definiert, mit einem Optimierer, einer Verlustfunktion und einer Accuracy-Metrik kompiliert und mit fit() auf Trainingsdaten trainiert, während Validierungsdaten zurückgehalten werden (Keras Sequential guide; Keras training guide). Für Sequenzdaten werden rekurrente Schichten wie LSTM auf dieselbe Weise gestapelt ([[recurrent-neural-networks|RNN und Zeitreihen]]); für Bilder werden Faltungs- und Pooling-Schichten kombiniert ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]). Modelle mit mehreren Ein- oder Ausgaben oder Skip-Verbindungen nutzen die Functional API (Keras Functional API guide). Callbacks wie Early Stopping und Modell-Checkpoints klinken sich in fit() ein (Keras training guide).

```python
import keras
from keras import layers

model = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)
```

### Wann einsetzen

- Wenn Standardarchitekturen mit wenig Code aufgebaut und trainiert werden sollen, passen die Sequential- und die Functional-API von Keras (Keras Sequential guide; Keras Functional API guide).
- Wenn Modelle auf verschiedenen Geräten bis hin zu verteilten Systemen eingesetzt werden müssen, hilft das TensorFlow-Ökosystem (Abadi et al., 2016).
- Wenn Forschungscode volle Kontrolle in reinem Python und einfaches Debugging braucht, ist PyTorch eine verbreitete Alternative (Paszke et al., 2019).

### Stärken und Grenzen

**Stärken**
- compile() und fit() decken die übliche Trainingsschleife mit sehr wenig Code ab (Keras training guide).
- Die Functional API unterstützt komplexe Topologien mit geteilten Schichten und mehreren Ein- und Ausgaben (Keras Functional API guide).
- TensorFlow führt dieselbe Berechnung auf sehr unterschiedlicher Hardware aus (Abadi et al., 2016).

**Einschränkungen**
- Das Sequential-Modell unterstützt keine mehrfachen Ein- oder Ausgaben, keine geteilten Schichten und keine nichtlineare Topologie (Keras Sequential guide).
- Ungewöhnliche Trainingsverfahren erfordern ein angepasstes fit() oder eine eigene Trainingsschleife (Keras training guide).
- Für Forschung, die einen imperativen Stil bevorzugt, wird oft PyTorch gewählt (Paszke et al., 2019).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Keras-Sequential-API | Linearer Stapel von Schichten (Keras Sequential guide) | Einfache Feedforward-, CNN- oder RNN-Modelle |
| Keras-Functional-API | Graph aus Schichten mit geteilten Schichten und mehreren Ein- und Ausgaben (Keras Functional API guide) | Modelle mit mehreren Eingaben, Skip-Verbindungen |
| Ableiten der Model-Klasse | Modelllogik als Python-Klasse (Keras Functional API guide) | Eigene Architekturen |
| PyTorch | Imperative, pythonische Bibliothek, in der jedes Modell ein gewöhnliches Python-Programm ist (Paszke et al., 2019) | Forschung und eigene Trainingsschleifen |

### In der Praxis

Trainingsläufe protokollieren ihre Konfiguration und Metriken ([[experiment-tracking|Experiment Tracking]]) und nutzen Callbacks für Early Stopping und Checkpoints (Keras training guide). Gespeicherte Modelle werden für Evaluation und Bereitstellung wieder geladen ([[mlops-and-deployment|MLOps und Deployment]]).

### Merksatz

Keras baut und trainiert neuronale Netze mit wenigen High-Level-Aufrufen auf Backends wie TensorFlow; die Functional API deckt Modelle ab, die mehr sind als ein einfacher Schichtstapel.

### Quellen

- Abadi, M. et al. (2016). *TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems.* Whitepaper. [arXiv:1603.04467](https://arxiv.org/abs/1603.04467)
- Keras team. *The Sequential model.* Keras developer guide. [keras.io](https://keras.io/guides/sequential_model/)
- Keras team. *The Functional API.* Keras developer guide. [keras.io](https://keras.io/guides/functional_api/)
- Keras team. *Training & evaluation with the built-in methods.* Keras developer guide. [keras.io](https://keras.io/guides/training_with_built_in_methods/)
- Paszke, A. et al. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library.* NeurIPS 2019. [arXiv:1912.01703](https://arxiv.org/abs/1912.01703)
