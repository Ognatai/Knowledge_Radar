---
title_en: ResNet (Residual Network)
title_de: ResNet (Residual Network)
entity_type: Method
aliases:
- ResNet
- Residual network
- Residual networks
- Residual learning
- Residual connection
- Skip connection
sources:
- https://arxiv.org/abs/1512.03385
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Residual networks (ResNets) make very deep [[neural-networks|neural networks]] trainable by letting each block of layers learn a residual `F(x)` that is added to its input through a shortcut connection, so the block outputs `F(x) + x` instead of a new mapping from scratch (He et al., 2016). This solved the "degradation problem", in which deeper plain networks had higher training error than shallower ones, and allowed networks of 152 layers on [[imagenet|ImageNet]] and over 1,000 layers on CIFAR-10 (He et al., 2016). ResNets won the ILSVRC and COCO 2015 competitions with 3.57% top-5 error on ImageNet, and residual connections became a standard building block, including in every Transformer layer ([[attention-and-transformers|attention and Transformers]]).

### How it works

```text
x ──► [weight layer → BN → ReLU → weight layer → BN] = F(x) ──► (+) ──► ReLU ──► output
│                                                                ▲
└──────────────────── identity shortcut (no parameters) ────────┘
bottleneck block (ResNet-50/101/152): 1×1 conv (reduce) → 3×3 conv → 1×1 conv (restore) + shortcut
when dimensions change: zero-padding (A) or a 1×1 projection W_s·x (B)
```

#### 1. The degradation problem

Vanishing and exploding gradients had largely been addressed by normalised initialisation and batch normalisation, so networks with tens of layers could start converging (He et al., 2016). But as depth increased further, accuracy saturated and then degraded: a 56-layer plain network had higher training error, not just test error, than a 20-layer one on CIFAR-10, so the problem was not [[overfitting|overfitting]]. A deeper network could in principle copy the shallower one and add identity layers, so it should never be worse; that solvers fail to find such solutions shows that some networks are harder to optimise than others (He et al., 2016).

#### 2. Residual learning

Instead of letting a stack of layers fit a desired mapping `H(x)` directly, ResNet lets it fit the residual `F(x) = H(x) − x` and recovers the mapping as `F(x) + x` (He et al., 2016). The hypothesis is that the residual is easier to optimise: if the identity were optimal, the layers would only need to push F towards zero. In practice, learned residuals tend to be small, so the identity provides a useful starting point. The addition is implemented by a shortcut connection that skips one or more layers; identity shortcuts add neither parameters nor computation, and the network is still trained end to end with stochastic gradient descent and [[back-propagation|back-propagation]] (He et al., 2016).

#### 3. Shortcuts across dimension changes

When a block changes the number of channels or the spatial size, the shortcut must match it. He et al. (2016) compared three options: zero-padding for new dimensions (A), projection shortcuts with a 1×1 convolution only where dimensions change (B), and projections everywhere (C). All three were clearly better than plain networks, B slightly better than A and C marginally better than B; since the differences were small, projections are not essential, and identity shortcuts keep the models cheaper (He et al., 2016).

#### 4. Bottleneck blocks and depth

For the deeper ImageNet models, each two-layer block is replaced by a three-layer bottleneck: a 1×1 convolution reduces the number of channels, a 3×3 convolution works on the reduced representation, and another 1×1 convolution restores it (He et al., 2016). This gives ResNet-50, ResNet-101 and ResNet-152; even the 152-layer network, at 11.3 billion FLOPs, has lower complexity than VGG-16 and VGG-19 with 15.3 and 19.6 billion. Batch normalisation follows each convolution. On CIFAR-10, a 1,202-layer network trained without optimisation difficulty, but its test error of 7.93% was worse than that of a 110-layer network, which the authors attribute to overfitting on the small dataset (He et al., 2016).

#### 5. Results

An ensemble of ResNets reached 3.57% top-5 error on the ImageNet test set and won the ILSVRC 2015 classification task; the deep representations also won ImageNet detection and localisation and COCO detection and segmentation in 2015, with a 28% relative improvement on COCO object detection from depth alone (He et al., 2016). With Faster R-CNN on PASCAL VOC, replacing VGG-16 by ResNet-101 raised mAP from 73.2 to 76.4 on VOC 2007 (He et al., 2016). Detection and segmentation are covered in [[computer-vision|computer vision]].

#### Origin and variants

Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun at Microsoft Research presented ResNet at CVPR 2016, after posting it in December 2015 (He et al., 2016). Shortcut connections existed earlier, for example in highway networks with gated shortcuts; ResNet's shortcuts are parameter-free identities that are never closed, so information always passes (He et al., 2016). ResNets became a common backbone for vision models and a baseline for the [[vision-transformer|Vision Transformer]].

### When to use it

- Image classification, detection and segmentation backbones, typically pre-trained and fine-tuned ([[convolutional-neural-networks|convolutional neural networks]]).
- Any deep architecture that should stay trainable as layers are added, which is why residual connections appear in Transformers ([[neural-network-training|neural network training]]).
- Vision tasks with mid-sized datasets, where convolutional inductive biases help ([[vision-transformer|Vision Transformer]]).

### Strengths and limitations

**Strengths**
- Very deep networks become easy to optimise and gain accuracy from depth (He et al., 2016).
- Identity shortcuts cost no parameters or computation (He et al., 2016).
- Strong, well-studied backbone for many vision tasks (He et al., 2016).

**Limitations**
- Extremely deep models such as 1,202 layers can overfit small datasets without stronger regularisation (He et al., 2016).
- Deeper models cost more computation: from 3.6 billion FLOPs for ResNet-34 to 11.3 billion for ResNet-152 (He et al., 2016).
- Its convolutional design is compared with attention-based image models in [[vision-transformer|Vision Transformer]].

### Comparison

| Model | Depth | ImageNet complexity | Key idea |
|---|---|---|---|
| VGG-19 | 19 | 19.6 billion FLOPs | stacked 3×3 convolutions |
| Plain 34-layer | 34 | 3.6 billion FLOPs | no shortcuts, suffers degradation |
| ResNet-34 | 34 | 3.6 billion FLOPs | identity shortcuts |
| ResNet-152 | 152 | 11.3 billion FLOPs | bottleneck blocks |

Source: He et al. (2016).

### In practice

Pre-trained ResNets serve as starting points for transfer learning in vision ([[convolutional-neural-networks|convolutional neural networks]]). Identity shortcuts are preferred over projections, especially in bottleneck blocks, where a projection shortcut would double time complexity and model size (He et al., 2016).

### Key takeaway

ResNets let layers learn a residual that is added back to their input through identity shortcuts, which removed the degradation of very deep networks, enabled 152-layer models that won ImageNet 2015, and made residual connections a standard part of deep learning architectures.

### Sources

- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Deep Residual Learning for Image Recognition.* CVPR 2016. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Residual Networks (ResNets) machen sehr tiefe [[neural-networks|neuronale Netze]] trainierbar, indem jeder Block von Schichten ein Residuum `F(x)` lernt, das über eine Shortcut-Verbindung zu seiner Eingabe addiert wird, sodass der Block `F(x) + x` ausgibt statt einer völlig neuen Abbildung (He et al., 2016). Das löste das „Degradationsproblem“, bei dem tiefere einfache Netze einen höheren Trainingsfehler hatten als flachere, und ermöglichte Netze mit 152 Schichten auf [[imagenet|ImageNet]] und über 1.000 Schichten auf CIFAR-10 (He et al., 2016). ResNets gewannen 2015 die Wettbewerbe ILSVRC und COCO mit 3,57 % Top-5-Fehler auf ImageNet, und Residualverbindungen wurden zum Standardbaustein, auch in jeder Transformer-Schicht ([[attention-and-transformers|Attention und Transformer]]).

### Funktionsweise

```text
x ──► [Gewichtsschicht → BN → ReLU → Gewichtsschicht → BN] = F(x) ──► (+) ──► ReLU ──► Ausgabe
│                                                                     ▲
└──────────────────── Identitäts-Shortcut (ohne Parameter) ──────────┘
Bottleneck-Block (ResNet-50/101/152): 1×1-Faltung (verkleinern) → 3×3-Faltung → 1×1-Faltung (wiederherstellen) + Shortcut
bei Dimensionswechsel: Auffüllen mit Nullen (A) oder 1×1-Projektion W_s·x (B)
```

#### 1. Das Degradationsproblem

Verschwindende und explodierende Gradienten waren durch normalisierte Initialisierung und Batch-Normalisierung weitgehend gelöst, sodass Netze mit einigen Dutzend Schichten zu konvergieren begannen (He et al., 2016). Bei weiter wachsender Tiefe sättigte sich die Genauigkeit jedoch und sank dann: Ein einfaches Netz mit 56 Schichten hatte auf CIFAR-10 einen höheren Trainingsfehler, nicht nur Testfehler, als eines mit 20 Schichten; das Problem war also keine [[overfitting|Überanpassung]]. Ein tieferes Netz könnte im Prinzip das flachere kopieren und Identitätsschichten ergänzen und dürfte daher nie schlechter sein; dass Optimierer solche Lösungen nicht finden, zeigt, dass manche Netze schwerer zu optimieren sind als andere (He et al., 2016).

#### 2. Residuales Lernen

Statt eine Schichtfolge eine gewünschte Abbildung `H(x)` direkt lernen zu lassen, lässt ResNet sie das Residuum `F(x) = H(x) − x` lernen und gewinnt die Abbildung als `F(x) + x` zurück (He et al., 2016). Die Hypothese ist, dass das Residuum leichter zu optimieren ist: Wäre die Identität optimal, müssten die Schichten F nur gegen null treiben. In der Praxis sind die gelernten Residuen eher klein, sodass die Identität einen nützlichen Ausgangspunkt bietet. Die Addition setzt eine Shortcut-Verbindung um, die eine oder mehrere Schichten überspringt; Identitäts-Shortcuts fügen weder Parameter noch Rechenaufwand hinzu, und das Netz wird weiterhin Ende-zu-Ende mit stochastischem Gradientenabstieg und [[back-propagation|Backpropagation]] trainiert (He et al., 2016).

#### 3. Shortcuts bei Dimensionswechseln

Ändert ein Block die Zahl der Kanäle oder die räumliche Größe, muss der Shortcut angepasst werden. He et al. (2016) verglichen drei Varianten: Auffüllen neuer Dimensionen mit Nullen (A), Projektions-Shortcuts mit einer 1×1-Faltung nur dort, wo sich Dimensionen ändern (B), und Projektionen überall (C). Alle drei waren deutlich besser als einfache Netze, B etwas besser als A und C geringfügig besser als B; weil die Unterschiede klein waren, sind Projektionen nicht nötig, und Identitäts-Shortcuts halten die Modelle günstiger (He et al., 2016).

#### 4. Bottleneck-Blöcke und Tiefe

Für die tieferen ImageNet-Modelle wird jeder zweischichtige Block durch einen dreischichtigen Bottleneck ersetzt: Eine 1×1-Faltung verringert die Zahl der Kanäle, eine 3×3-Faltung arbeitet auf der verkleinerten Darstellung, und eine weitere 1×1-Faltung stellt sie wieder her (He et al., 2016). So entstehen ResNet-50, ResNet-101 und ResNet-152; selbst das Netz mit 152 Schichten hat mit 11,3 Milliarden FLOPs eine geringere Komplexität als VGG-16 und VGG-19 mit 15,3 und 19,6 Milliarden. Auf jede Faltung folgt eine Batch-Normalisierung. Auf CIFAR-10 ließ sich ein Netz mit 1.202 Schichten ohne Optimierungsschwierigkeiten trainieren, sein Testfehler von 7,93 % war aber schlechter als der eines Netzes mit 110 Schichten, was die Autoren auf Überanpassung an den kleinen Datensatz zurückführen (He et al., 2016).

#### 5. Ergebnisse

Ein Ensemble aus ResNets erreichte 3,57 % Top-5-Fehler auf dem ImageNet-Testset und gewann die Klassifikationsaufgabe der ILSVRC 2015; die tiefen Repräsentationen gewannen 2015 auch die ImageNet-Disziplinen Erkennung und Lokalisierung sowie bei COCO Erkennung und Segmentierung, mit einer relativen Verbesserung um 28 % bei der COCO-Objekterkennung allein durch Tiefe (He et al., 2016). Mit Faster R-CNN auf PASCAL VOC stieg der mAP auf VOC 2007 von 73,2 auf 76,4, wenn VGG-16 durch ResNet-101 ersetzt wurde (He et al., 2016). Erkennung und Segmentierung behandelt [[computer-vision|Computer Vision]].

#### Herkunft und Varianten

Kaiming He, Xiangyu Zhang, Shaoqing Ren und Jian Sun von Microsoft Research stellten ResNet auf der CVPR 2016 vor, nachdem sie es im Dezember 2015 veröffentlicht hatten (He et al., 2016). Shortcut-Verbindungen gab es schon früher, etwa in Highway Networks mit gesteuerten Shortcuts; die Shortcuts von ResNet sind parameterfreie Identitäten, die nie geschlossen sind, sodass Information immer durchgeht (He et al., 2016). ResNets wurden zu einem verbreiteten Backbone für Bildmodelle und zu einer Baseline für den [[vision-transformer|Vision Transformer]].

### Wann einsetzen

- Backbones für Bildklassifikation, Objekterkennung und Segmentierung, typischerweise vortrainiert und feinjustiert ([[convolutional-neural-networks|Convolutional Neural Networks]]).
- Jede tiefe Architektur, die beim Hinzufügen von Schichten trainierbar bleiben soll, weshalb Residualverbindungen in Transformern vorkommen ([[neural-network-training|Training neuronaler Netze]]).
- Bildaufgaben mit mittelgroßen Datensätzen, bei denen der Inductive Bias von Faltungen hilft ([[vision-transformer|Vision Transformer]]).

### Stärken und Grenzen

**Stärken**
- Sehr tiefe Netze werden leicht optimierbar und gewinnen durch Tiefe an Genauigkeit (He et al., 2016).
- Identitäts-Shortcuts kosten weder Parameter noch Rechenaufwand (He et al., 2016).
- Starkes, gut untersuchtes Backbone für viele Bildaufgaben (He et al., 2016).

**Grenzen**
- Extrem tiefe Modelle wie mit 1.202 Schichten können kleine Datensätze ohne stärkere Regularisierung überanpassen (He et al., 2016).
- Tiefere Modelle kosten mehr Rechenaufwand: von 3,6 Milliarden FLOPs für ResNet-34 bis 11,3 Milliarden für ResNet-152 (He et al., 2016).
- Den Vergleich des Faltungsentwurfs mit attentionbasierten Bildmodellen behandelt [[vision-transformer|Vision Transformer]].

### Vergleich

| Modell | Tiefe | Komplexität auf ImageNet | Kernidee |
|---|---|---|---|
| VGG-19 | 19 | 19,6 Mrd. FLOPs | gestapelte 3×3-Faltungen |
| Einfaches Netz, 34 Schichten | 34 | 3,6 Mrd. FLOPs | keine Shortcuts, leidet unter Degradation |
| ResNet-34 | 34 | 3,6 Mrd. FLOPs | Identitäts-Shortcuts |
| ResNet-152 | 152 | 11,3 Mrd. FLOPs | Bottleneck-Blöcke |

Quelle: He et al. (2016).

### In der Praxis

Vortrainierte ResNets dienen als Ausgangspunkt für Transfer Learning in der Bildverarbeitung ([[convolutional-neural-networks|Convolutional Neural Networks]]). Identitäts-Shortcuts sind Projektionen vorzuziehen, vor allem in Bottleneck-Blöcken, in denen ein Projektions-Shortcut Zeitaufwand und Modellgröße verdoppeln würde (He et al., 2016).

### Merksatz

ResNets lassen Schichten ein Residuum lernen, das über Identitäts-Shortcuts zur Eingabe zurückaddiert wird; das beseitigte die Degradation sehr tiefer Netze, ermöglichte Modelle mit 152 Schichten, die ImageNet 2015 gewannen, und machte Residualverbindungen zum festen Bestandteil von Deep-Learning-Architekturen.

### Quellen

- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Deep Residual Learning for Image Recognition.* CVPR 2016. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)
