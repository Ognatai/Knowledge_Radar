---
title_en: Multimodal Models
title_de: Multimodale Modelle
entity_type: Concept
sources:
- https://arxiv.org/abs/2103.00020
- https://arxiv.org/abs/2010.11929
- https://arxiv.org/abs/2204.14198
- https://arxiv.org/abs/2301.12597
- https://arxiv.org/abs/2304.08485
- https://arxiv.org/abs/2112.10752
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Multimodal models process more than one kind of data, most often images and text. Contrastive models such as CLIP learn a shared embedding space in which matching images and captions lie close together, enabling zero-shot image classification (Radford et al., 2021). Vision-language models connect a vision encoder to a large language model, so that they can answer questions about images and follow visual instructions (Alayrac et al., 2022; Li et al., 2023; Liu et al., 2023), and diffusion models generate images from text (Rombach et al., 2021).

### How it works

Each modality is first turned into vectors by a suitable encoder, for example a Vision Transformer for images (Dosovitskiy et al., 2020). The vectors are then either aligned in a shared space by contrastive training or fed into a language model through a connecting module, and the model is trained on paired image-text data.

```text
1. A shared embedding space
▼
2. Contrastive learning with CLIP
▼
3. Connecting vision encoders to language models
▼
4. Visual instruction tuning
▼
5. Generating images from text
```

#### 1. A shared embedding space

To relate images and text, both must be represented in comparable vectors ([[embeddings|Embeddings]]). A Vision Transformer splits an image into patches and processes them as a sequence of tokens with a standard Transformer, which works well when pretrained on large data (Dosovitskiy et al., 2020; [[attention-and-transformers|Attention and Transformers]]).

#### 2. Contrastive learning with CLIP

Radford et al. (2021) trained image and text encoders on 400 million image-text pairs collected from the internet with the simple task of predicting which caption goes with which image. Afterwards, natural language can name visual concepts, which allows zero-shot transfer: the model was benchmarked on over 30 computer vision datasets, was often competitive with fully supervised baselines without dataset-specific training, and matched the accuracy of the original ResNet-50 on ImageNet zero-shot without using any of its 1.28 million training examples.

#### 3. Connecting vision encoders to language models

Flamingo bridges pretrained vision-only and language-only models, handles arbitrarily interleaved sequences of images and text, and accepts images or videos as input (Alayrac et al., 2022). Trained on large-scale multimodal web corpora, a single Flamingo model reached new state-of-the-art results with few-shot prompting on many tasks, outperforming models fine-tuned on thousands of times more task-specific data. BLIP-2 keeps both the image encoder and the language model frozen and bridges them with a lightweight Querying Transformer pretrained in two stages; it outperformed Flamingo80B by 8.7% on zero-shot VQAv2 with 54 times fewer trainable parameters (Li et al., 2023).

#### 4. Visual instruction tuning

LLaVA used language-only GPT-4 to generate multimodal instruction-following data and instruction-tuned a model that connects a vision encoder with a large language model (Liu et al., 2023). It showed multimodal chat abilities, reached an 85.1% relative score compared with GPT-4 on a synthetic multimodal instruction-following dataset, and, combined with GPT-4, a new state-of-the-art accuracy of 92.53% on Science QA.

#### 5. Generating images from text

In the other direction, latent diffusion models generate images conditioned on text: cross-attention layers connect the denoising network to a text representation, and diffusion runs in the latent space of an autoencoder to keep computation manageable (Rombach et al., 2021; [[diffusion-models|Diffusion Models]]).

#### Origin and variants

Vision Transformers (Dosovitskiy et al., 2020) brought the Transformer to images, CLIP (Radford et al., 2021) aligned images and text contrastively, Flamingo (Alayrac et al., 2022), BLIP-2 (Li et al., 2023) and LLaVA (Liu et al., 2023) connected vision encoders to language models, and latent diffusion (Rombach et al., 2021) enabled text-to-image generation.

### When to use it

- When images should be classified or retrieved by free-text descriptions without task-specific training, contrastive models such as CLIP fit (Radford et al., 2021).
- When questions about images or documents with images must be answered in natural language, vision-language models fit (Alayrac et al., 2022; Liu et al., 2023).
- When images should be generated from text, latent diffusion models fit (Rombach et al., 2021).

### Strengths and limitations

**Strengths**
- Zero-shot transfer to many vision tasks via natural language (Radford et al., 2021).
- Few-shot adaptation by prompting with examples (Alayrac et al., 2022).
- Frozen encoders and language models make training efficient (Li et al., 2023).

**Limitations**
- Contrastive pretraining needs hundreds of millions of image-text pairs from the web (Radford et al., 2021).
- Instruction data generated by another model inherits that model's behaviour (Liu et al., 2023).
- Vision Transformers rely on large-scale pretraining (Dosovitskiy et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Contrastive dual encoder (CLIP) | Separate encoders aligned in one embedding space (Radford et al., 2021) | Zero-shot classification, image-text retrieval |
| Vision-language model (Flamingo, BLIP-2) | Vision encoder feeds a language model (Alayrac et al., 2022; Li et al., 2023) | Visual question answering, captioning |
| Instruction-tuned VLM (LLaVA) | Trained on visual instruction-following data (Liu et al., 2023) | Multimodal chat assistants |
| Text-to-image diffusion | Text conditions an image generator (Rombach et al., 2021) | Image generation |

### In practice

Multimodal models are evaluated per task, for example with visual question answering, captioning and zero-shot classification benchmarks (Radford et al., 2021; Alayrac et al., 2022). For retrieval over images and text, CLIP-style embeddings are stored in a vector index ([[vector-databases|Vector Databases]]).

### Key takeaway

Multimodal models align or connect encoders for different data types, so that language can describe, query and generate images.

### Sources

- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
- Alayrac, J. et al. (2022). *Flamingo: a Visual Language Model for Few-Shot Learning.* NeurIPS 2022. [arXiv:2204.14198](https://arxiv.org/abs/2204.14198)
- Li, J. et al. (2023). *BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models.* ICML 2023. [arXiv:2301.12597](https://arxiv.org/abs/2301.12597)
- Liu, H. et al. (2023). *Visual Instruction Tuning.* NeurIPS 2023. [arXiv:2304.08485](https://arxiv.org/abs/2304.08485)
- Rombach, R. et al. (2021). *High-Resolution Image Synthesis with Latent Diffusion Models.* CVPR 2022. [arXiv:2112.10752](https://arxiv.org/abs/2112.10752)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Multimodale Modelle verarbeiten mehr als eine Art von Daten, meist Bilder und Text. Kontrastive Modelle wie CLIP lernen einen gemeinsamen Embedding-Raum, in dem zusammengehörige Bilder und Bildunterschriften nahe beieinander liegen, was Zero-Shot-Bildklassifikation ermöglicht (Radford et al., 2021). Vision-Language-Modelle verbinden einen Bild-Encoder mit einem großen Sprachmodell, sodass sie Fragen zu Bildern beantworten und visuellen Anweisungen folgen können (Alayrac et al., 2022; Li et al., 2023; Liu et al., 2023), und Diffusionsmodelle erzeugen Bilder aus Text (Rombach et al., 2021).

### Funktionsweise

Jede Modalität wird zunächst von einem passenden Encoder in Vektoren umgewandelt, etwa von einem Vision Transformer für Bilder (Dosovitskiy et al., 2020). Die Vektoren werden dann entweder durch kontrastives Training in einem gemeinsamen Raum ausgerichtet oder über ein Verbindungsmodul in ein Sprachmodell eingespeist, und das Modell wird auf Bild-Text-Paaren trainiert.

```text
1. Ein gemeinsamer Embedding-Raum
▼
2. Kontrastives Lernen mit CLIP
▼
3. Bild-Encoder mit Sprachmodellen verbinden
▼
4. Visual Instruction Tuning
▼
5. Bilder aus Text erzeugen
```

#### 1. Ein gemeinsamer Embedding-Raum

Um Bilder und Text aufeinander zu beziehen, müssen beide in vergleichbaren Vektoren dargestellt werden ([[embeddings|Embeddings]]). Ein Vision Transformer zerlegt ein Bild in Ausschnitte (Patches) und verarbeitet sie als Folge von Token mit einem gewöhnlichen Transformer, was bei großem Vortraining gut funktioniert (Dosovitskiy et al., 2020; [[attention-and-transformers|Attention und Transformer]]).

#### 2. Kontrastives Lernen mit CLIP

Radford et al. (2021) trainierten Bild- und Text-Encoder auf 400 Millionen Bild-Text-Paaren aus dem Internet mit der einfachen Aufgabe vorherzusagen, welche Bildunterschrift zu welchem Bild gehört. Danach lassen sich visuelle Konzepte in natürlicher Sprache benennen, was Zero-Shot-Transfer erlaubt: Das Modell wurde auf über 30 Datensätzen der Bildverarbeitung getestet, war ohne datensatzspezifisches Training oft mit vollständig überwachten Baselines konkurrenzfähig und erreichte auf ImageNet zero-shot die Genauigkeit des ursprünglichen ResNet-50, ohne eines von dessen 1,28 Millionen Trainingsbeispielen zu nutzen.

#### 3. Bild-Encoder mit Sprachmodellen verbinden

Flamingo verbindet vortrainierte reine Bild- und reine Sprachmodelle, verarbeitet beliebig verschachtelte Folgen von Bildern und Text und nimmt Bilder oder Videos als Eingabe (Alayrac et al., 2022). Auf großen multimodalen Webkorpora trainiert, erzielte ein einziges Flamingo-Modell mit Few-Shot-Prompting bei vielen Aufgaben neue Bestwerte und übertraf Modelle, die mit tausendfach mehr aufgabenspezifischen Daten feinabgestimmt waren. BLIP-2 lässt sowohl den Bild-Encoder als auch das Sprachmodell eingefroren und verbindet sie mit einem leichten Querying Transformer, der in zwei Stufen vortrainiert wird; es übertraf Flamingo80B bei zero-shot VQAv2 um 8,7 % mit 54-mal weniger trainierbaren Parametern (Li et al., 2023).

#### 4. Visual Instruction Tuning

LLaVA nutzte das rein sprachliche GPT-4, um multimodale Daten zum Befolgen von Anweisungen zu erzeugen, und stimmte damit ein Modell ab, das einen Bild-Encoder mit einem großen Sprachmodell verbindet (Liu et al., 2023). Es zeigte multimodale Chat-Fähigkeiten, erreichte auf einem synthetischen multimodalen Datensatz zum Befolgen von Anweisungen 85,1 % der Bewertung von GPT-4 und zusammen mit GPT-4 eine neue Bestgenauigkeit von 92,53 % auf Science QA.

#### 5. Bilder aus Text erzeugen

In der Gegenrichtung erzeugen Latent-Diffusion-Modelle Bilder, die durch Text bedingt sind: Cross-Attention-Schichten verbinden das Entrauschungsnetz mit einer Textrepräsentation, und die Diffusion läuft im latenten Raum eines Autoencoders, um den Rechenaufwand beherrschbar zu halten (Rombach et al., 2021; [[diffusion-models|Diffusionsmodelle]]).

#### Ursprung und Varianten

Vision Transformer (Dosovitskiy et al., 2020) übertrugen den Transformer auf Bilder, CLIP (Radford et al., 2021) richtete Bilder und Text kontrastiv aus, Flamingo (Alayrac et al., 2022), BLIP-2 (Li et al., 2023) und LLaVA (Liu et al., 2023) verbanden Bild-Encoder mit Sprachmodellen, und Latent Diffusion (Rombach et al., 2021) ermöglichte die Erzeugung von Bildern aus Text.

### Wann einsetzen

- Wenn Bilder ohne aufgabenspezifisches Training anhand freier Textbeschreibungen klassifiziert oder gesucht werden sollen, passen kontrastive Modelle wie CLIP (Radford et al., 2021).
- Wenn Fragen zu Bildern oder zu Dokumenten mit Bildern in natürlicher Sprache beantwortet werden müssen, passen Vision-Language-Modelle (Alayrac et al., 2022; Liu et al., 2023).
- Wenn Bilder aus Text erzeugt werden sollen, passen Latent-Diffusion-Modelle (Rombach et al., 2021).

### Stärken und Grenzen

**Stärken**
- Zero-Shot-Transfer auf viele Bildaufgaben über natürliche Sprache (Radford et al., 2021).
- Few-Shot-Anpassung durch Prompting mit Beispielen (Alayrac et al., 2022).
- Eingefrorene Encoder und Sprachmodelle machen das Training effizient (Li et al., 2023).

**Einschränkungen**
- Kontrastives Vortraining braucht Hunderte Millionen Bild-Text-Paare aus dem Web (Radford et al., 2021).
- Von einem anderen Modell erzeugte Anweisungsdaten übernehmen dessen Verhalten (Liu et al., 2023).
- Vision Transformer sind auf großes Vortraining angewiesen (Dosovitskiy et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Kontrastiver Dual Encoder (CLIP) | Getrennte Encoder, in einem Embedding-Raum ausgerichtet (Radford et al., 2021) | Zero-Shot-Klassifikation, Bild-Text-Suche |
| Vision-Language-Modell (Flamingo, BLIP-2) | Bild-Encoder speist ein Sprachmodell (Alayrac et al., 2022; Li et al., 2023) | Visuelle Fragebeantwortung, Bildbeschreibung |
| Anweisungsabgestimmtes VLM (LLaVA) | Trainiert auf visuellen Anweisungsdaten (Liu et al., 2023) | Multimodale Chat-Assistenten |
| Text-zu-Bild-Diffusion | Text bedingt einen Bildgenerator (Rombach et al., 2021) | Bilderzeugung |

### In der Praxis

Multimodale Modelle werden je Aufgabe evaluiert, etwa mit Benchmarks für visuelle Fragebeantwortung, Bildbeschreibung und Zero-Shot-Klassifikation (Radford et al., 2021; Alayrac et al., 2022). Für die Suche über Bilder und Text werden Embeddings im Stil von CLIP in einem Vektorindex gespeichert ([[vector-databases|Vektordatenbanken]]).

### Merksatz

Multimodale Modelle richten Encoder für verschiedene Datenarten aneinander aus oder verbinden sie, sodass Sprache Bilder beschreiben, abfragen und erzeugen kann.

### Quellen

- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
- Alayrac, J. et al. (2022). *Flamingo: a Visual Language Model for Few-Shot Learning.* NeurIPS 2022. [arXiv:2204.14198](https://arxiv.org/abs/2204.14198)
- Li, J. et al. (2023). *BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models.* ICML 2023. [arXiv:2301.12597](https://arxiv.org/abs/2301.12597)
- Liu, H. et al. (2023). *Visual Instruction Tuning.* NeurIPS 2023. [arXiv:2304.08485](https://arxiv.org/abs/2304.08485)
- Rombach, R. et al. (2021). *High-Resolution Image Synthesis with Latent Diffusion Models.* CVPR 2022. [arXiv:2112.10752](https://arxiv.org/abs/2112.10752)
