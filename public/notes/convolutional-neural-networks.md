---
title_en: Convolutional Neural Networks (CNN)
title_de: Convolutional Neural Networks (CNN)
entity_type: Method
sources:
- https://doi.org/10.1109/5.726791
- https://doi.org/10.1145/3065386
- https://arxiv.org/abs/1409.1556
- https://arxiv.org/abs/1512.03385
- https://www.deeplearningbook.org/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Convolutional neural networks (CNNs) process grid-like data such as images by sliding small learned filters over the input, so that the same weights detect a pattern wherever it occurs (Goodfellow et al., 2016). Stacked convolution and pooling layers learn features from edges to objects. CNNs outperformed all other methods on handwritten digit recognition (LeCun et al., 1998), won ImageNet in 2012 (Krizhevsky et al., 2012), and became much deeper with small filters (Simonyan & Zisserman, 2014) and residual connections (He et al., 2015).

### How it works

Convolution layers apply a set of filters to the input and produce feature maps, pooling layers summarise neighbouring values, and after several such stages fully connected layers or a global pooling produce the prediction. All filters are learned with back-propagation.

```text
1. The convolution operation
▼
2. Channels, filters and shapes
▼
3. Pooling
▼
4. Typical architecture
▼
5. Going deeper
▼
6. Transfer learning
```

#### 1. The convolution operation

A convolution slides a small kernel (filter) over the input and computes a weighted sum at each position (Goodfellow et al., 2016). Compared with a fully connected layer, this gives sparse interactions (each output depends only on a small region), parameter sharing (the same filter is used everywhere) and equivariance to translation (a shifted input gives a shifted output). LeCun et al. (1998) designed convolutional networks to deal with the variability of 2D shapes, and they outperformed all other techniques on a standard handwritten digit recognition task.

#### 2. Channels, filters and shapes

Inputs and feature maps have several channels, for example red, green and blue for a colour image (Goodfellow et al., 2016). Each filter spans all input channels and produces one output channel, so the number of filters sets the depth of the next feature map. The stride, the step size of the filter, and padding at the borders determine the spatial size of the output.

#### 3. Pooling

Pooling replaces a region of a feature map with a summary statistic, such as its maximum (max pooling) (Goodfellow et al., 2016). This reduces the spatial size and makes the representation approximately invariant to small translations of the input.

#### 4. Typical architecture

A typical CNN alternates convolution layers with non-linear activations and pooling, and ends with fully connected layers and a softmax. Krizhevsky et al. (2012) trained such a network with 60 million parameters, five convolutional and three fully connected layers on 1.2 million ImageNet images; using ReLU activations, GPU training and dropout, it reached top-1 and top-5 error rates of 37.5% and 17.0%, and a variant won ILSVRC-2012 with 15.3% top-5 error versus 26.2% for the second-best entry.

#### 5. Going deeper

Simonyan & Zisserman (2014) showed that very small 3×3 filters allow networks of 16 to 19 weight layers that improve markedly on earlier configurations. Deeper networks are harder to train; residual networks reformulate layers to learn residual functions with respect to their inputs, which made networks up to 152 layers deep easier to optimise and more accurate; an ensemble reached 3.57% error on the ImageNet test set and won ILSVRC 2015 (He et al., 2015).

#### 6. Transfer learning

Representations learned on large datasets generalise to other tasks: VGG representations achieved state-of-the-art results on other datasets, and the authors released their models (Simonyan & Zisserman, 2014). In practice, a network pretrained on ImageNet is reused and only its last layers are retrained or fine-tuned on the new task ([[llm-adaptation|LLM Adaptation]] for the analogous idea in language models).

#### Origin and variants

LeNet-style networks (LeCun et al., 1998) established CNNs for document recognition, AlexNet (Krizhevsky et al., 2012) started the deep learning era in computer vision, and VGG (Simonyan & Zisserman, 2014) and ResNet (He et al., 2015) made networks much deeper. Vision Transformers later offered an attention-based alternative ([[attention-and-transformers|Attention and Transformers]]).

### When to use it

- When data has a grid structure with local patterns, such as images, spectrograms or some time series (Goodfellow et al., 2016).
- When little labelled data is available for a vision task, a pretrained CNN can be fine-tuned (Simonyan & Zisserman, 2014).
- When very deep models are needed, residual connections make them trainable (He et al., 2015).

### Strengths and limitations

**Strengths**
- Parameter sharing makes CNNs efficient and translation-equivariant (Goodfellow et al., 2016).
- They learn features directly from pixels with minimal preprocessing (LeCun et al., 1998).
- Pretrained representations transfer well to other datasets (Simonyan & Zisserman, 2014).

**Limitations**
- Large CNNs need large labelled datasets and GPU training (Krizhevsky et al., 2012).
- Very deep plain networks are hard to optimise without residual connections (He et al., 2015).
- Pooling discards precise positional information (Goodfellow et al., 2016).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Fully connected network | Every unit connected to every input; no weight sharing (Goodfellow et al., 2016) | Small tabular inputs |
| CNN | Local filters with shared weights, pooling (Goodfellow et al., 2016) | Images and other grid data |
| Residual network | Layers learn residuals, enabling very deep CNNs (He et al., 2015) | Large-scale image recognition |

### In practice

Inputs are normalised, data augmentation such as cropping and flipping is used to reduce overfitting, and pretrained backbones are fine-tuned rather than trained from scratch when data is limited (Krizhevsky et al., 2012; Simonyan & Zisserman, 2014). Filter sizes, strides and padding are chosen so that the feature-map shapes fit the architecture (Goodfellow et al., 2016).

### Key takeaway

CNNs learn small filters that are shared across the whole input, which makes them efficient for images; depth and residual connections drive their accuracy.

### Sources

- LeCun, Y., Bottou, L., Bengio, Y. & Haffner, P. (1998). *Gradient-based learning applied to document recognition.* Proceedings of the IEEE 86(11). [doi:10.1109/5.726791](https://doi.org/10.1109/5.726791)
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2017). *ImageNet classification with deep convolutional neural networks.* Communications of the ACM 60(6) (NeurIPS 2012). [doi:10.1145/3065386](https://doi.org/10.1145/3065386)
- Simonyan, K. & Zisserman, A. (2014). *Very Deep Convolutional Networks for Large-Scale Image Recognition.* ICLR 2015. [arXiv:1409.1556](https://arxiv.org/abs/1409.1556)
- He, K. et al. (2015). *Deep Residual Learning for Image Recognition.* CVPR 2016. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Convolutional Neural Networks (CNNs) verarbeiten gitterartige Daten wie Bilder, indem sie kleine gelernte Filter über die Eingabe schieben; so erkennen dieselben Gewichte ein Muster, wo immer es auftritt (Goodfellow et al., 2016). Gestapelte Faltungs- und Pooling-Schichten lernen Merkmale von Kanten bis zu Objekten. CNNs übertrafen bei der Erkennung handgeschriebener Ziffern alle anderen Verfahren (LeCun et al., 1998), gewannen 2012 ImageNet (Krizhevsky et al., 2012) und wurden mit kleinen Filtern (Simonyan & Zisserman, 2014) und Residualverbindungen (He et al., 2015) deutlich tiefer.

### Funktionsweise

Faltungsschichten wenden eine Reihe von Filtern auf die Eingabe an und erzeugen Feature Maps, Pooling-Schichten fassen benachbarte Werte zusammen, und nach mehreren solchen Stufen liefern vollständig verbundene Schichten oder ein globales Pooling die Vorhersage. Alle Filter werden mit Backpropagation gelernt.

```text
1. Die Faltungsoperation
▼
2. Kanäle, Filter und Shapes
▼
3. Pooling
▼
4. Typische Architektur
▼
5. Tiefere Netze
▼
6. Transfer Learning
```

#### 1. Die Faltungsoperation

Eine Faltung (Convolution) schiebt einen kleinen Kernel (Filter) über die Eingabe und berechnet an jeder Position eine gewichtete Summe (Goodfellow et al., 2016). Gegenüber einer vollständig verbundenen Schicht ergibt das dünnbesetzte Verbindungen (jede Ausgabe hängt nur von einem kleinen Bereich ab), geteilte Parameter (derselbe Filter wird überall verwendet) und Äquivarianz gegenüber Verschiebungen (eine verschobene Eingabe ergibt eine verschobene Ausgabe). LeCun et al. (1998) entwarfen konvolutionale Netze für die Variabilität zweidimensionaler Formen, und sie übertrafen bei einer Standardaufgabe zur Erkennung handgeschriebener Ziffern alle anderen Verfahren.

#### 2. Kanäle, Filter und Shapes

Eingaben und Feature Maps haben mehrere Kanäle, bei einem Farbbild etwa Rot, Grün und Blau (Goodfellow et al., 2016). Jeder Filter erstreckt sich über alle Eingabekanäle und erzeugt einen Ausgabekanal; die Zahl der Filter bestimmt daher die Tiefe der nächsten Feature Map. Die Schrittweite des Filters (Stride) und das Auffüllen der Ränder (Padding) bestimmen die räumliche Größe der Ausgabe.

#### 3. Pooling

Pooling ersetzt einen Bereich einer Feature Map durch eine zusammenfassende Kennzahl, etwa sein Maximum (Max Pooling) (Goodfellow et al., 2016). Das verkleinert die räumliche Größe und macht die Repräsentation näherungsweise unempfindlich gegenüber kleinen Verschiebungen der Eingabe.

#### 4. Typische Architektur

Ein typisches CNN wechselt Faltungsschichten mit nichtlinearen Aktivierungen und Pooling ab und endet mit vollständig verbundenen Schichten und einer Softmax-Ausgabe. Krizhevsky et al. (2012) trainierten ein solches Netz mit 60 Millionen Parametern, fünf Faltungs- und drei vollständig verbundenen Schichten auf 1,2 Millionen ImageNet-Bildern; mit ReLU-Aktivierungen, GPU-Training und Dropout erreichte es Top-1- und Top-5-Fehlerraten von 37,5 % und 17,0 %, und eine Variante gewann ILSVRC-2012 mit 15,3 % Top-5-Fehler gegenüber 26,2 % beim zweitbesten Beitrag.

#### 5. Tiefere Netze

Simonyan & Zisserman (2014) zeigten, dass sehr kleine 3×3-Filter Netze mit 16 bis 19 Gewichtsschichten ermöglichen, die frühere Konfigurationen deutlich übertreffen. Tiefere Netze sind schwerer zu trainieren; Residualnetze formulieren Schichten so um, dass sie Residualfunktionen bezüglich ihrer Eingaben lernen, wodurch Netze mit bis zu 152 Schichten leichter zu optimieren und genauer wurden; ein Ensemble erreichte 3,57 % Fehler auf der ImageNet-Testmenge und gewann ILSVRC 2015 (He et al., 2015).

#### 6. Transfer Learning

Auf großen Datensätzen gelernte Repräsentationen lassen sich auf andere Aufgaben übertragen: VGG-Repräsentationen erreichten auf anderen Datensätzen den Stand der Technik, und die Autoren veröffentlichten ihre Modelle (Simonyan & Zisserman, 2014). In der Praxis wird ein auf ImageNet vortrainiertes Netz wiederverwendet und nur seine letzten Schichten auf die neue Aufgabe neu trainiert oder feinabgestimmt ([[llm-adaptation|LLM-Anpassung]] für die entsprechende Idee bei Sprachmodellen).

#### Ursprung und Varianten

Netze im Stil von LeNet (LeCun et al., 1998) etablierten CNNs für die Dokumenterkennung, AlexNet (Krizhevsky et al., 2012) leitete die Deep-Learning-Ära in der Bildverarbeitung ein, und VGG (Simonyan & Zisserman, 2014) sowie ResNet (He et al., 2015) machten Netze deutlich tiefer. Vision Transformer boten später eine attention-basierte Alternative ([[attention-and-transformers|Attention und Transformer]]).

### Wann einsetzen

- Wenn Daten eine Gitterstruktur mit lokalen Mustern haben, etwa Bilder, Spektrogramme oder manche Zeitreihen (Goodfellow et al., 2016).
- Wenn für eine Bildaufgabe wenige gelabelte Daten vorliegen, lässt sich ein vortrainiertes CNN feinabstimmen (Simonyan & Zisserman, 2014).
- Wenn sehr tiefe Modelle nötig sind, machen Residualverbindungen sie trainierbar (He et al., 2015).

### Stärken und Grenzen

**Stärken**
- Geteilte Parameter machen CNNs effizient und verschiebungsäquivariant (Goodfellow et al., 2016).
- Sie lernen Merkmale direkt aus Pixeln mit minimaler Vorverarbeitung (LeCun et al., 1998).
- Vortrainierte Repräsentationen lassen sich gut auf andere Datensätze übertragen (Simonyan & Zisserman, 2014).

**Einschränkungen**
- Große CNNs brauchen große gelabelte Datensätze und GPU-Training (Krizhevsky et al., 2012).
- Sehr tiefe Netze ohne Residualverbindungen sind schwer zu optimieren (He et al., 2015).
- Pooling verwirft genaue Positionsinformation (Goodfellow et al., 2016).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Vollständig verbundenes Netz | Jede Einheit mit jeder Eingabe verbunden; keine geteilten Gewichte (Goodfellow et al., 2016) | Kleine tabellarische Eingaben |
| CNN | Lokale Filter mit geteilten Gewichten, Pooling (Goodfellow et al., 2016) | Bilder und andere Gitterdaten |
| Residualnetz | Schichten lernen Residuen, ermöglicht sehr tiefe CNNs (He et al., 2015) | Bilderkennung im großen Maßstab |

### In der Praxis

Eingaben werden normalisiert, Datenaugmentation wie Zuschneiden und Spiegeln verringert Overfitting, und bei wenigen Daten werden vortrainierte Netze feinabgestimmt statt von Grund auf trainiert (Krizhevsky et al., 2012; Simonyan & Zisserman, 2014). Filtergrößen, Strides und Padding werden so gewählt, dass die Shapes der Feature Maps zur Architektur passen (Goodfellow et al., 2016).

### Merksatz

CNNs lernen kleine Filter, die über die ganze Eingabe geteilt werden, und sind dadurch für Bilder effizient; Tiefe und Residualverbindungen treiben ihre Genauigkeit.

### Quellen

- LeCun, Y., Bottou, L., Bengio, Y. & Haffner, P. (1998). *Gradient-based learning applied to document recognition.* Proceedings of the IEEE 86(11). [doi:10.1109/5.726791](https://doi.org/10.1109/5.726791)
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2017). *ImageNet classification with deep convolutional neural networks.* Communications of the ACM 60(6) (NeurIPS 2012). [doi:10.1145/3065386](https://doi.org/10.1145/3065386)
- Simonyan, K. & Zisserman, A. (2014). *Very Deep Convolutional Networks for Large-Scale Image Recognition.* ICLR 2015. [arXiv:1409.1556](https://arxiv.org/abs/1409.1556)
- He, K. et al. (2015). *Deep Residual Learning for Image Recognition.* CVPR 2016. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
