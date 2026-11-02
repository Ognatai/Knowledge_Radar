---
title_en: CLIP
title_de: CLIP
entity_type: Method
aliases:
- CLIP
- Contrastive Language-Image Pre-training
- Contrastive Language–Image Pre-training
sources:
- https://arxiv.org/abs/2103.00020
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

CLIP (Contrastive Language–Image Pre-training) is an [[openai|OpenAI]] model that learns image representations from natural language: an image encoder and a text encoder are trained jointly on 400 million image–text pairs from the internet to predict which caption belongs to which image (Radford et al., 2021). The result is a shared embedding space in which images and texts can be compared with [[cosine-similarity|cosine similarity]], so a new image classifier can be built zero-shot by writing class names as text prompts. Zero-shot CLIP matched the original ResNet-50 on ImageNet without using its training images and was much more robust to natural distribution shift, but it is weak on fine-grained, abstract and truly out-of-distribution tasks and learns social biases from its uncurated data (Radford et al., 2021).

### How it works

```text
pre-training (WIT: 400 M image–text pairs, 500,000 queries)
  batch of N pairs ──► image encoder (ResNet or ViT) ──► I_1…I_N ──► linear projection ──► L2-normalise
                   └─► text encoder (Transformer)    ──► T_1…T_N ──► linear projection ──► L2-normalise
  similarity matrix N × N (cosine · learned temperature) ──► symmetric cross-entropy: correct pair on the diagonal

zero-shot classification
  class names ──► prompts "A photo of a {label}." ──► text embeddings (ensemble of prompts, averaged)
  image ──► image embedding ──► cosine with each class embedding ──► softmax ──► predicted class
```

#### 1. Training data

Existing image–caption data sets were too small or too noisy, so the authors built WIT (WebImageText), 400 million (image, text) pairs from public internet sources, collected with 500,000 search queries and roughly class-balanced with up to 20,000 pairs per query; its total word count is similar to GPT-2's WebText (Radford et al., 2021).

#### 2. Contrastive objective

Predicting the exact words of a caption proved inefficient, so CLIP instead learns which of the N × N possible image–text pairings in a batch actually occurred: it maximises the cosine similarity of the N real pairs and minimises it for the N² − N wrong ones with a symmetric [[cross-entropy|cross-entropy loss]] ([[contrastive-learning|contrastive learning]]; Radford et al., 2021). Both encoders are trained from scratch and connected to the joint space by linear projections only (Radford et al., 2021).

#### 3. Encoders and scaling

The image encoder is either a modified ResNet or a Vision Transformer, the text encoder a Transformer of 63 million parameters in its base size; the authors trained five ResNets and three Vision Transformers, the best being ViT-L/14 at 336-pixel resolution (Radford et al., 2021; [[vision-transformer|Vision Transformer]], [[resnet|ResNet]]).

#### 4. Zero-shot classification and prompts

To classify, the class names are embedded as texts and the image is assigned to the class with the highest temperature-scaled cosine similarity; this prediction layer is equivalent to a multinomial [[logistic-regression|logistic regression]] with normalised inputs and weights and no bias (Radford et al., 2021). Bare class names are ambiguous (ImageNet contains both construction cranes and the birds), and captions are rarely single words, so the template "A photo of a {label}." improved ImageNet accuracy by 1.3%; task-specific prompts such as "a type of pet" and ensembles of prompts averaged in embedding space (80 for ImageNet) improved zero-shot accuracy by almost 5 points on average across 36 data sets (Radford et al., 2021; [[prompt-engineering|prompt engineering]]).

#### 5. Results and robustness

Zero-shot CLIP raised ImageNet accuracy from the 11.5% of an earlier zero-shot approach to 76.2%, matching the original ResNet-50 without any of its 1.28 million labelled examples (Radford et al., 2021; [[imagenet|ImageNet]]). On seven natural distribution shifts of ImageNet, zero-shot CLIP reduced the gap between ImageNet and shifted accuracy by up to 75%; adapting CLIP to ImageNet with a supervised classifier raised ImageNet accuracy by 9.2% but slightly reduced average robustness (Radford et al., 2021).

#### Origin and variants

Alec Radford and colleagues at OpenAI presented CLIP at ICML 2021, building on earlier work that learned visual concepts from text associated with images (Radford et al., 2021). Its image–text embedding space is used for image retrieval and search in both directions (Radford et al., 2021) and as a component of [[multimodal-models|multimodal models]].

### When to use it

- Zero-shot or few-label [[computer-vision|image classification]] where classes can be described in words (Radford et al., 2021).
- Text-to-image and image-to-text retrieval in one embedding space ([[semantic-retrieval|semantic retrieval]], [[vector-databases|vector databases]]).
- As a pretrained visual backbone with a linear classifier on its features (Radford et al., 2021).

### Strengths and limitations

**Strengths**
- New classifiers without retraining, defined by text (Radford et al., 2021).
- Much higher robustness to natural distribution shift than ImageNet-trained models (Radford et al., 2021).
- Scales with data that needs no manual labelling (Radford et al., 2021).

**Limitations**
- Weak on fine-grained [[classification|classification]] (car models, flower species, aircraft variants), abstract tasks such as counting objects, and specialised domains such as satellite images; near chance on novel tasks like estimating distance to the nearest car (Radford et al., 2021).
- Generalises poorly to truly out-of-distribution data: only 88% on handwritten MNIST digits, below logistic regression on raw pixels (Radford et al., 2021).
- Limited to choosing among the given class texts; it cannot generate new descriptions like a captioning model (Radford et al., 2021).
- Learns social biases from unfiltered internet pairs, and its open-ended classification can be misused, for example for surveillance (Radford et al., 2021; [[bias-in-nlp|bias]]).
- Moving from zero-shot to few-shot with a linear classifier on its features can at first lower performance (Radford et al., 2021).

### Comparison

| Approach | Supervision | New classes | Note |
|---|---|---|---|
| Supervised ImageNet model | 1.28 M labelled images, 1,000 classes | need retraining | strong in-distribution, less robust |
| CLIP zero-shot | 400 M image–text pairs | by writing prompts | robust, weak on fine-grained tasks |
| CLIP + linear probe | CLIP features + labelled data | need labels | higher accuracy, less robust |
| [[contrastive-learning\|SimCLR-style self-supervision]] | augmentations of unlabelled images | need labels for the classifier | no text interface |

Source: Radford et al. (2021).

### In practice

Prompt wording matters: adding context such as the type of object and averaging several prompts are cheap gains, and the averaged text [[embeddings|embeddings]] can be cached so ensembling costs nothing at prediction time (Radford et al., 2021). Before deployment, performance and bias have to be evaluated for the specific use, since general benchmarks do not reveal them (Radford et al., 2021).

### Key takeaway

CLIP aligns images and texts in one embedding space by contrastive training on 400 million web pairs, which turns any list of class names into a zero-shot classifier, robust but limited where the web data is thin.

### Sources

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

CLIP (Contrastive Language–Image Pre-training) ist ein Modell von [[openai|OpenAI]], das Bildrepräsentationen aus natürlicher Sprache lernt: Ein Bild- und ein Text-Encoder werden gemeinsam auf 400 Millionen Bild-Text-Paaren aus dem Internet darauf trainiert, vorherzusagen, welche Bildunterschrift zu welchem Bild gehört (Radford et al., 2021). Das Ergebnis ist ein gemeinsamer Embedding-Raum, in dem sich Bilder und Texte mit [[cosine-similarity|Cosine Similarity]] vergleichen lassen; ein neuer Bildklassifikator entsteht so zero-shot, indem Klassennamen als Text-Prompts formuliert werden. Zero-Shot-CLIP erreichte auf ImageNet die Genauigkeit des ursprünglichen ResNet-50, ohne dessen Trainingsbilder zu nutzen, und war gegenüber natürlichen Verteilungsverschiebungen deutlich robuster, ist aber schwach bei feinkörnigen, abstrakten und echt außerhalb der Verteilung liegenden Aufgaben und lernt gesellschaftliche Verzerrungen aus seinen ungefilterten Daten (Radford et al., 2021).

### Funktionsweise

```text
Vortraining (WIT: 400 Mio. Bild-Text-Paare, 500.000 Suchanfragen)
  Batch aus N Paaren ──► Bild-Encoder (ResNet oder ViT) ──► I_1…I_N ──► lineare Projektion ──► L2-normalisieren
                     └─► Text-Encoder (Transformer)     ──► T_1…T_N ──► lineare Projektion ──► L2-normalisieren
  Ähnlichkeitsmatrix N × N (Kosinus · gelernte Temperatur) ──► symmetrische Cross-Entropy: richtiges Paar auf der Diagonalen

Zero-Shot-Klassifikation
  Klassennamen ──► Prompts „A photo of a {label}.“ ──► Text-Embeddings (Ensemble von Prompts, gemittelt)
  Bild ──► Bild-Embedding ──► Kosinus mit jedem Klassen-Embedding ──► Softmax ──► vorhergesagte Klasse
```

#### 1. Trainingsdaten

Bestehende Datensätze aus Bildern und Bildunterschriften waren zu klein oder zu verrauscht; die Autoren bauten daher WIT (WebImageText), 400 Millionen (Bild, Text)-Paare aus öffentlichen Internetquellen, gesammelt mit 500.000 Suchanfragen und mit höchstens 20.000 Paaren pro Anfrage ungefähr nach Klassen ausgeglichen; die Gesamtzahl der Wörter entspricht etwa WebText von GPT-2 (Radford et al., 2021).

#### 2. Kontrastives Ziel

Die genauen Wörter einer Bildunterschrift vorherzusagen erwies sich als ineffizient; CLIP lernt stattdessen, welche der N × N möglichen Bild-Text-Paarungen eines Batches tatsächlich vorkamen: Es maximiert die Cosine Similarity der N echten Paare und minimiert sie für die N² − N falschen mit einem symmetrischen Cross-Entropy-Verlust ([[contrastive-learning|Contrastive Learning]]; Radford et al., 2021). Beide Encoder werden von Grund auf trainiert und nur über lineare Projektionen mit dem gemeinsamen Raum verbunden (Radford et al., 2021).

#### 3. Encoder und Skalierung

Der Bild-Encoder ist entweder ein angepasstes ResNet oder ein Vision Transformer, der Text-Encoder in der Grundgröße ein Transformer mit 63 Millionen Parametern; die Autoren trainierten fünf ResNets und drei Vision Transformer, am besten war ViT-L/14 bei 336 Pixeln Auflösung (Radford et al., 2021; [[vision-transformer|Vision Transformer]], [[resnet|ResNet]]).

#### 4. Zero-Shot-Klassifikation und Prompts

Zum Klassifizieren werden die Klassennamen als Texte eingebettet, und das Bild wird der Klasse mit der höchsten temperaturskalierten Cosine Similarity zugeordnet; diese Vorhersageschicht entspricht einer multinomialen [[logistic-regression|logistischen Regression]] mit normalisierten Eingaben und Gewichten ohne Bias (Radford et al., 2021). Bloße Klassennamen sind mehrdeutig (ImageNet enthält sowohl Baukräne als auch Kraniche), und Bildunterschriften bestehen selten aus einem Wort; die Vorlage „A photo of a {label}.“ verbesserte die ImageNet-Genauigkeit daher um 1,3 %, und aufgabenspezifische Prompts wie „a type of pet“ sowie im Embedding-Raum gemittelte Prompt-Ensembles (80 für ImageNet) verbesserten die Zero-Shot-Genauigkeit über 36 Datensätze im Mittel um fast 5 Punkte (Radford et al., 2021; [[prompt-engineering|Prompt Engineering]]).

#### 5. Ergebnisse und Robustheit

Zero-Shot-CLIP hob die ImageNet-Genauigkeit von den 11,5 % eines früheren Zero-Shot-Ansatzes auf 76,2 % und erreichte damit das ursprüngliche ResNet-50, ohne eines von dessen 1,28 Millionen gelabelten Beispielen (Radford et al., 2021; [[imagenet|ImageNet]]). Auf sieben natürlichen Verteilungsverschiebungen von ImageNet verringerte Zero-Shot-CLIP die Lücke zwischen ImageNet- und verschobener Genauigkeit um bis zu 75 %; die Anpassung von CLIP an ImageNet mit einem überwachten Klassifikator steigerte die ImageNet-Genauigkeit um 9,2 %, senkte aber die mittlere Robustheit leicht (Radford et al., 2021).

#### Ursprung und Varianten

Alec Radford und Kollegen bei OpenAI stellten CLIP auf der ICML 2021 vor, aufbauend auf früheren Arbeiten, die visuelle Konzepte aus Texten zu Bildern lernten (Radford et al., 2021). Sein Bild-Text-Embedding-Raum dient der Bildsuche in beide Richtungen (Radford et al., 2021) und als Baustein [[multimodal-models|multimodaler Modelle]].

### Wann einsetzen

- Zero-Shot-Bildklassifikation oder [[classification|Klassifikation]] mit wenigen Labels, wenn sich die Klassen in Worten beschreiben lassen (Radford et al., 2021).
- Text-zu-Bild- und Bild-zu-Text-Suche in einem Embedding-Raum ([[semantic-retrieval|semantisches Retrieval]], [[vector-databases|Vektordatenbanken]]).
- Als vortrainiertes visuelles Rückgrat mit einem linearen Klassifikator auf seinen Merkmalen (Radford et al., 2021).

### Stärken und Grenzen

**Stärken**
- Neue Klassifikatoren ohne neues Training, definiert durch Text (Radford et al., 2021).
- Deutlich robuster gegenüber natürlichen Verteilungsverschiebungen als auf ImageNet trainierte Modelle (Radford et al., 2021).
- Skaliert mit Daten, die keine manuellen Labels brauchen (Radford et al., 2021).

**Grenzen**
- Schwach bei feinkörniger Klassifikation (Automodelle, Blumenarten, Flugzeugvarianten), bei abstrakten Aufgaben wie dem Zählen von Objekten und in Spezialdomänen wie Satellitenbildern; nahe dem Zufall bei neuartigen Aufgaben wie dem Schätzen der Entfernung zum nächsten Auto (Radford et al., 2021).
- Generalisiert schlecht auf echt verteilungsfremde Daten: nur 88 % auf handgeschriebenen MNIST-Ziffern, weniger als eine logistische Regression auf rohen Pixeln (Radford et al., 2021).
- Auf die Auswahl unter den vorgegebenen Klassentexten beschränkt; es kann keine neuen Beschreibungen erzeugen wie ein Captioning-Modell (Radford et al., 2021).
- Lernt gesellschaftliche Verzerrungen aus ungefilterten Internetpaaren, und seine offene Klassifikation kann missbraucht werden, etwa zur Überwachung (Radford et al., 2021; [[bias-in-nlp|Bias]]).
- Der Übergang von Zero-Shot zu Few-Shot mit einem linearen Klassifikator auf seinen Merkmalen kann die Leistung zunächst senken (Radford et al., 2021).

### Vergleich

| Ansatz | Überwachung | Neue Klassen | Bemerkung |
|---|---|---|---|
| Überwachtes ImageNet-Modell | 1,28 Mio. gelabelte Bilder, 1.000 Klassen | brauchen neues Training | stark in der Verteilung, weniger robust |
| CLIP zero-shot | 400 Mio. Bild-Text-Paare | durch Formulieren von Prompts | robust, schwach bei feinkörnigen Aufgaben |
| CLIP + Linear Probe | CLIP-Merkmale + gelabelte Daten | brauchen Labels | höhere Genauigkeit, weniger robust |
| [[contrastive-learning\|Selbstüberwachung wie SimCLR]] | Augmentierungen ungelabelter Bilder | brauchen Labels für den Klassifikator | keine Textschnittstelle |

Quelle: Radford et al. (2021).

### In der Praxis

Die Formulierung der Prompts zählt: Kontext wie die Art des Objekts und das Mitteln mehrerer Prompts sind günstige Gewinne, und die gemittelten Text-Embeddings lassen sich zwischenspeichern, sodass das Ensemble bei der Vorhersage nichts kostet (Radford et al., 2021). Vor dem Einsatz müssen Leistung und Verzerrungen für den konkreten Zweck bewertet werden, da allgemeine Benchmarks sie nicht zeigen (Radford et al., 2021).

### Merksatz

CLIP bringt Bilder und Texte durch kontrastives Training auf 400 Millionen Web-Paaren in einen Embedding-Raum und macht so aus jeder Liste von Klassennamen einen Zero-Shot-Klassifikator, robust, aber begrenzt dort, wo die Webdaten dünn sind.

### Quellen

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
