---
title_en: Vision Transformer (ViT)
title_de: Vision Transformer (ViT)
entity_type: Method
aliases:
- Vision Transformer
- ViT
sources:
- https://arxiv.org/abs/2010.11929
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The Vision Transformer (ViT) applies a standard Transformer encoder, almost unchanged from NLP, directly to images: the image is cut into fixed-size patches, for example 16×16 pixels, each patch is flattened and linearly embedded like a word token, position [[embeddings|embeddings]] are added, and a learnable class token collects the representation used for [[classification|classification]] (Dosovitskiy et al., 2021). Without the built-in assumptions of convolutional networks, ViT does worse than comparable ResNets when trained on mid-sized datasets such as [[imagenet|ImageNet]], but pre-trained on 14 to 300 million images it matched or beat state-of-the-art CNNs on image classification benchmarks with substantially less pre-training compute (Dosovitskiy et al., 2021). In short: "large scale training trumps inductive bias".

### How it works

```text
image x ∈ R^(H×W×C)
 ▼ split into N = HW / P² patches of P×P pixels, flatten each to P²·C values
 ▼ linear projection E → patch embeddings of size D
 ▼ prepend learnable [class] token; add learnable 1D position embeddings
z₀ = [x_class; x¹E; …; xᴺE] + E_pos
 ▼ L Transformer encoder layers: z′ = MSA(LN(z)) + z;  z = MLP(LN(z′)) + z′
 ▼ y = LN(z_L at [class] position) → classification head (MLP in pre-training, linear in fine-tuning)
```

#### 1. Images as sequences of patches

A Transformer expects a 1D sequence of token embeddings. ViT reshapes an image of H×W pixels with C channels into N = HW/P² flattened patches of P×P pixels, maps each with a trainable linear projection to the model width D, and treats the resulting patch embeddings as tokens (Dosovitskiy et al., 2021). With P = 16 on a 224×224 image, this gives 196 tokens; the name of the paper, "An Image is Worth 16x16 Words", refers to this. A model name such as ViT-L/16 denotes the "Large" variant with 16×16 patches.

#### 2. Class token, position embeddings and encoder

As in [[bert|BERT]], a learnable classification token is prepended; its output state after the last layer serves as the image representation, followed by an MLP head during pre-training and a single linear layer during fine-tuning (Dosovitskiy et al., 2021). Learnable 1D position embeddings are added to keep positional information; 2D-aware variants brought no significant gain. The encoder alternates multi-head self-attention and MLP blocks with layer normalisation before and residual connections after each block, as in the original Transformer ([[attention-and-transformers|attention and Transformers]]).

#### 3. Inductive bias and data

Convolutional networks build locality, two-dimensional neighbourhood structure and translation equivariance into every layer ([[convolutional-neural-networks|convolutional neural networks]]). In ViT, only the MLP layers are local; self-attention is global from the first layer, and all spatial relations between patches must be learned (Dosovitskiy et al., 2021). Consequently, on mid-sized datasets such as ImageNet without strong regularisation, ViT was a few percentage points below ResNets of similar size and overfitted more on small subsets, but on 90 million or more pre-training images it outperformed them; the authors conclude that the convolutional inductive bias helps on smaller datasets while large datasets make learning the patterns directly sufficient (Dosovitskiy et al., 2021).

#### 4. Pre-training and fine-tuning

ViT is pre-trained on large datasets, ImageNet-21k (14 million images) or the in-house JFT-300M, and then fine-tuned on smaller benchmarks (Dosovitskiy et al., 2021). Fine-tuning often uses a higher resolution than pre-training; the patch size stays the same, so the sequence gets longer, and the pre-trained position embeddings are interpolated in 2D to the new grid, one of the few places where image structure is injected by hand (Dosovitskiy et al., 2021).

#### 5. Results and analysis

The largest model, ViT-H/14 pre-trained on JFT-300M, reached 88.55% on ImageNet, 90.72% on ImageNet-ReaL, 94.55% on CIFAR-100 and 77.63% on the 19-task VTAB suite, outperforming ResNet-based baselines while needing 2,500 TPUv3-core-days of pre-training against 9,900 for the best ResNet baseline (Dosovitskiy et al., 2021). Analysing attention distance, comparable to receptive field size, showed some heads attending to most of the image already in the lowest layers while others stayed local, with attention distance growing with depth. A preliminary self-supervised variant with masked patch prediction reached 79.9% on ImageNet with ViT-B/16 (Dosovitskiy et al., 2021).

#### Origin and variants

Alexey Dosovitskiy and colleagues at Google Research presented ViT at ICLR 2021 and released code and pre-trained models (Dosovitskiy et al., 2021). A hybrid variant feeds CNN feature maps instead of raw patches into the Transformer. Image-text models such as CLIP use ViT image encoders ([[multimodal-models|multimodal models]], [[computer-vision|computer vision]]).

### When to use it

- Image classification and transfer learning when a model pre-trained on a large dataset is available (Dosovitskiy et al., 2021).
- Multimodal systems that need an image encoder compatible with Transformer language models ([[multimodal-models|multimodal models]]).
- Large training budgets and datasets, where ViT scales more cheaply than comparable CNNs (Dosovitskiy et al., 2021).

### Strengths and limitations

**Strengths**
- Uses the standard Transformer and its efficient implementations almost unchanged (Dosovitskiy et al., 2021).
- Global attention from the first layer (Dosovitskiy et al., 2021).
- Better accuracy per pre-training compute than ResNet baselines at large scale (Dosovitskiy et al., 2021).

**Limitations**
- Needs large pre-training datasets; on mid-sized datasets it underperforms comparable CNNs (Dosovitskiy et al., 2021).
- Overfits more than ResNets of comparable cost on small datasets (Dosovitskiy et al., 2021).
- Self-attention cost grows with the square of the number of patches, so higher resolutions mean much longer sequences ([[attention-and-transformers|attention and Transformers]]).

### Comparison

| | [[resnet\|ResNet (CNN)]] | ViT |
|---|---|---|
| Built-in assumptions | locality, translation equivariance | almost none |
| Receptive field | grows with depth | global from the first layer |
| Data needs | works on mid-sized data | needs large-scale pre-training |
| Best case in the paper | BiT-L 87.54% ImageNet, 9.9k TPUv3-core-days | ViT-H/14 88.55%, 2.5k TPUv3-core-days |

Source: Dosovitskiy et al. (2021).

### In practice

ViT is almost always used as a pre-trained backbone and fine-tuned, not trained from scratch on small data (Dosovitskiy et al., 2021). Patch size trades accuracy against sequence length and compute.

### Key takeaway

The Vision Transformer treats an image as a sequence of 16×16 patch tokens and processes it with a standard Transformer encoder; lacking the inductive biases of convolutions, it needs large-scale pre-training, but then matches or beats CNNs at lower pre-training cost.

### Sources

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J. & Houlsby, N. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der Vision Transformer (ViT) wendet einen gewöhnlichen Transformer-Encoder, nahezu unverändert aus dem NLP übernommen, direkt auf Bilder an: Das Bild wird in Ausschnitte fester Größe zerlegt, etwa 16×16 Pixel, jeder Ausschnitt wird wie ein Wort-Token abgeflacht und linear eingebettet, Positions-Embeddings werden ergänzt, und ein lernbares Klassen-Token sammelt die Repräsentation für die [[classification|Klassifikation]] (Dosovitskiy et al., 2021). Ohne die eingebauten Annahmen von Convolutional Networks schneidet ViT beim Training auf mittelgroßen Datensätzen wie [[imagenet|ImageNet]] schlechter ab als vergleichbare ResNets, erreichte oder übertraf aber nach Vortraining auf 14 bis 300 Millionen Bildern die besten CNNs bei Benchmarks zur Bildklassifikation, mit deutlich weniger Rechenaufwand im Vortraining (Dosovitskiy et al., 2021). Kurz: „large scale training trumps inductive bias“.

### Funktionsweise

```text
Bild x ∈ R^(H×W×C)
 ▼ in N = HW / P² Ausschnitte zu P×P Pixeln zerlegen, jeden zu P²·C Werten abflachen
 ▼ lineare Projektion E → Patch-Embeddings der Größe D
 ▼ lernbares [class]-Token voranstellen; lernbare 1D-Positions-Embeddings addieren
z₀ = [x_class; x¹E; …; xᴺE] + E_pos
 ▼ L Transformer-Encoder-Schichten: z′ = MSA(LN(z)) + z;  z = MLP(LN(z′)) + z′
 ▼ y = LN(z_L an der [class]-Position) → Klassifikationskopf (MLP im Vortraining, linear im Fine-Tuning)
```

#### 1. Bilder als Folgen von Ausschnitten

Ein Transformer erwartet eine 1D-Folge von Token-Embeddings. ViT formt ein Bild mit H×W Pixeln und C Kanälen in N = HW/P² abgeflachte Ausschnitte zu P×P Pixeln um, bildet jeden mit einer trainierbaren linearen Projektion auf die Modellbreite D ab und behandelt die entstehenden Patch-Embeddings als Token (Dosovitskiy et al., 2021). Mit P = 16 ergibt ein Bild mit 224×224 Pixeln 196 Token; der Titel des Papers, „An Image is Worth 16x16 Words“, spielt darauf an. Ein Modellname wie ViT-L/16 bezeichnet die Variante „Large“ mit Ausschnitten von 16×16 Pixeln.

#### 2. Klassen-Token, Positions-Embeddings und Encoder

Wie bei [[bert|BERT]] wird ein lernbares Klassifikations-Token vorangestellt; sein Ausgabezustand nach der letzten Schicht dient als Bildrepräsentation, gefolgt von einem MLP-Kopf im Vortraining und einer einzelnen linearen Schicht beim Fine-Tuning (Dosovitskiy et al., 2021). Lernbare 1D-Positions-Embeddings werden addiert, um die Positionsinformation zu erhalten; Varianten, die die 2D-Struktur berücksichtigen, brachten keinen deutlichen Gewinn. Der Encoder wechselt Multi-Head-Self-Attention und MLP-Blöcke ab, mit Layer-Normalisierung vor und Residualverbindungen nach jedem Block, wie im ursprünglichen Transformer ([[attention-and-transformers|Attention und Transformer]]).

#### 3. Inductive Bias und Daten

Convolutional Networks bauen Lokalität, zweidimensionale Nachbarschaft und Translationsäquivarianz in jede Schicht ein ([[convolutional-neural-networks|Convolutional Neural Networks]]). Bei ViT sind nur die MLP-Schichten lokal; Self-Attention ist schon ab der ersten Schicht global, und alle räumlichen Beziehungen zwischen Ausschnitten müssen gelernt werden (Dosovitskiy et al., 2021). Folglich lag ViT auf mittelgroßen Datensätzen wie ImageNet ohne starke Regularisierung einige Prozentpunkte unter ResNets ähnlicher Größe und überanpasste auf kleinen Teilmengen stärker, übertraf sie aber ab 90 Millionen Vortrainingsbildern; die Autoren folgern, dass der Inductive Bias von Faltungen bei kleineren Datensätzen hilft, während bei großen Datensätzen das direkte Lernen der Muster genügt (Dosovitskiy et al., 2021).

#### 4. Vortraining und Fine-Tuning

ViT wird auf großen Datensätzen vortrainiert, ImageNet-21k (14 Millionen Bilder) oder dem internen JFT-300M, und dann auf kleineren Benchmarks feinjustiert (Dosovitskiy et al., 2021). Das Fine-Tuning nutzt oft eine höhere Auflösung als das Vortraining; die Ausschnittgröße bleibt gleich, die Folge wird also länger, und die vortrainierten Positions-Embeddings werden in 2D auf das neue Raster interpoliert, eine der wenigen Stellen, an denen Bildstruktur von Hand eingebracht wird (Dosovitskiy et al., 2021).

#### 5. Ergebnisse und Analyse

Das größte Modell, ViT-H/14 vortrainiert auf JFT-300M, erreichte 88,55 % auf ImageNet, 90,72 % auf ImageNet-ReaL, 94,55 % auf CIFAR-100 und 77,63 % auf der VTAB-Suite mit 19 Aufgaben, übertraf ResNet-basierte Baselines und brauchte 2.500 TPUv3-Kern-Tage Vortraining gegenüber 9.900 für die beste ResNet-Baseline (Dosovitskiy et al., 2021). Die Analyse der Attention-Distanz, vergleichbar mit der Größe des rezeptiven Felds, zeigte, dass manche Köpfe schon in den untersten Schichten den Großteil des Bilds beachten, während andere lokal bleiben, und dass die Attention-Distanz mit der Tiefe wächst. Eine vorläufige selbstüberwachte Variante mit Vorhersage maskierter Ausschnitte erreichte mit ViT-B/16 79,9 % auf ImageNet (Dosovitskiy et al., 2021).

#### Herkunft und Varianten

Alexey Dosovitskiy und Kolleginnen und Kollegen bei Google Research stellten ViT auf der ICLR 2021 vor und veröffentlichten Code und vortrainierte Modelle (Dosovitskiy et al., 2021). Eine Hybridvariante gibt CNN-Feature-Maps statt roher Ausschnitte in den Transformer. Bild-Text-Modelle wie CLIP nutzen ViT als Bild-Encoder ([[multimodal-models|Multimodale Modelle]], [[computer-vision|Computer Vision]]).

### Wann einsetzen

- Bildklassifikation und Transfer Learning, wenn ein auf großen Daten vortrainiertes Modell verfügbar ist (Dosovitskiy et al., 2021).
- Multimodale Systeme, die einen mit Transformer-Sprachmodellen kompatiblen Bild-Encoder brauchen ([[multimodal-models|Multimodale Modelle]]).
- Große Trainingsbudgets und Datensätze, bei denen ViT günstiger skaliert als vergleichbare CNNs (Dosovitskiy et al., 2021).

### Stärken und Grenzen

**Stärken**
- Nutzt den gewöhnlichen Transformer und seine effizienten Implementierungen fast unverändert (Dosovitskiy et al., 2021).
- Globale Attention ab der ersten Schicht (Dosovitskiy et al., 2021).
- Im großen Maßstab bessere Genauigkeit je Vortrainingsaufwand als ResNet-Baselines (Dosovitskiy et al., 2021).

**Grenzen**
- Braucht große Vortrainingsdatensätze; auf mittelgroßen Datensätzen schneidet es schlechter ab als vergleichbare CNNs (Dosovitskiy et al., 2021).
- Überanpasst auf kleinen Datensätzen stärker als ResNets mit vergleichbarem Aufwand (Dosovitskiy et al., 2021).
- Der Aufwand der Self-Attention wächst quadratisch mit der Zahl der Ausschnitte, höhere Auflösungen bedeuten also deutlich längere Folgen ([[attention-and-transformers|Attention und Transformer]]).

### Vergleich

| | [[resnet\|ResNet (CNN)]] | ViT |
|---|---|---|
| Eingebaute Annahmen | Lokalität, Translationsäquivarianz | nahezu keine |
| Rezeptives Feld | wächst mit der Tiefe | global ab der ersten Schicht |
| Datenbedarf | funktioniert mit mittelgroßen Daten | braucht Vortraining im großen Maßstab |
| Bestwert im Paper | BiT-L 87,54 % ImageNet, 9,9k TPUv3-Kern-Tage | ViT-H/14 88,55 %, 2,5k TPUv3-Kern-Tage |

Quelle: Dosovitskiy et al. (2021).

### In der Praxis

ViT wird fast immer als vortrainiertes Backbone genutzt und feinjustiert, nicht auf kleinen Daten von Grund auf trainiert (Dosovitskiy et al., 2021). Die Ausschnittgröße wägt Genauigkeit gegen Folgenlänge und Rechenaufwand ab.

### Merksatz

Der Vision Transformer behandelt ein Bild als Folge von Token aus Ausschnitten zu 16×16 Pixeln und verarbeitet es mit einem gewöhnlichen Transformer-Encoder; ohne den Inductive Bias von Faltungen braucht er Vortraining im großen Maßstab, erreicht oder übertrifft dann aber CNNs bei geringerem Vortrainingsaufwand.

### Quellen

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J. & Houlsby, N. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
