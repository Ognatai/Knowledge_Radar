---
title_en: Computer Vision
title_de: Computer Vision
entity_type: Concept
aliases:
- Computer vision
- Image classification
- Object detection
- Image segmentation
- Instance segmentation
- Semantic segmentation
- Bildverarbeitung
sources:
- https://arxiv.org/abs/1409.0575
- https://arxiv.org/abs/1506.02640
- https://arxiv.org/abs/1703.06870
- https://arxiv.org/abs/1505.04597
- https://arxiv.org/abs/2010.11929
- https://arxiv.org/abs/2103.00020
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Computer vision is the field of AI that extracts information from images and video. Its core tasks are image classification (what is in the image), object detection (where are which objects, as bounding boxes), segmentation (which pixels belong to which object or class) and keypoint or pose estimation; further tasks include OCR, tracking and visual question answering. Since the ImageNet challenge, deep learning has dominated: convolutional networks for classification, single-pass detectors such as YOLO, two-stage detectors with mask branches such as Mask R-CNN, encoder-decoder networks such as U-Net for segmentation, and Vision Transformers that treat images as sequences of patches (Russakovsky et al., 2015; Redmon et al., 2016; He et al., 2017; Ronneberger et al., 2015; Dosovitskiy et al., 2021). Models trained on image-text pairs such as CLIP recognise categories named in natural language without task-specific training (Radford et al., 2021).

### How it works

```text
image or video frame (pixels, H × W × 3)
 ▼
backbone: CNN or Vision Transformer → feature maps / patch embeddings
 ▼
task head:
  classification → class probabilities
  detection      → boxes + classes (one-stage like YOLO, two-stage like Faster/Mask R-CNN)
  segmentation   → per-pixel classes or per-object masks (U-Net, Mask R-CNN)
  image–text     → shared embedding space for zero-shot recognition (CLIP)
 ▼
post-processing, evaluation (accuracy, mAP, IoU) and deployment
```

#### 1. Classification and the ImageNet benchmark

The ImageNet Large Scale Visual Recognition Challenge (ILSVRC) ran annually from 2010 and covered object classification and detection across hundreds of categories and millions of images, with more than fifty participating institutions; the paper also compares machine and human accuracy on it (Russakovsky et al., 2015). Classification models built from convolutions, pooling and ever deeper architectures are described in [[convolutional-neural-networks|convolutional neural networks]]. A backbone pre-trained on such data is usually reused for other tasks through transfer learning.

#### 2. Object detection

Detection predicts a bounding box and a class for each object. Two-stage detectors first propose regions and then classify them; one-stage detectors predict everything in one pass. YOLO frames detection as a single regression problem from the full image to box coordinates and class probabilities, trained end to end; its base model ran at about 45 frames per second and Fast YOLO at about 155, it made more localisation errors than state-of-the-art systems but fewer false positives on background, and it generalised well from photos to artwork (Redmon et al., 2016). Detectors are evaluated with mean average [[classification-metrics|precision]] (mAP) over intersection-over-union thresholds.

#### 3. Segmentation

Semantic segmentation assigns a class to every pixel; instance segmentation additionally separates individual objects. U-Net combines a contracting path that captures context with a symmetric expanding path for precise localisation, trains end to end from very few images with heavy data augmentation, segments a 512×512 image in under a second on a GPU and won biomedical segmentation challenges (Ronneberger et al., 2015). Mask R-CNN extends the two-stage detector Faster R-CNN with a branch that predicts a mask for each detected object, runs at about 5 frames per second, also handles human pose estimation and achieved top results on the COCO instance segmentation, detection and keypoint tracks (He et al., 2017).

#### 4. Vision Transformers

The Vision Transformer (ViT) splits an image into 16×16 patches and feeds the sequence of patch embeddings to a standard Transformer without convolutions; pre-trained on large datasets and transferred to ImageNet, CIFAR-100 or VTAB, it matches state-of-the-art CNNs while needing substantially less compute to train (Dosovitskiy et al., 2021). The architecture is the same as in language models, see [[attention-and-transformers|attention and Transformers]].

#### 5. Vision and language

Standard vision models only know a fixed set of labelled categories. CLIP learns from 400 million image-text pairs from the internet with a contrastive objective that matches each image with its caption; afterwards, categories can be named in natural language, enabling zero-shot transfer: on ImageNet it matches the accuracy of the original ResNet-50 without using any of its 1.28 million training examples, and it was benchmarked on over 30 datasets including OCR, action recognition and geo-localisation (Radford et al., 2021). Models that combine vision with language generation are covered in [[multimodal-models|multimodal models]]; reading documents is covered in [[document-processing|document processing]].

#### Origin and variants

ILSVRC from 2010 provided the large labelled benchmark (Russakovsky et al., 2015); deep CNNs, real-time detectors (2015–2016), instance segmentation (2017), Vision Transformers (2020–2021) and image-text pre-training (2021) followed (Redmon et al., 2016; He et al., 2017; Dosovitskiy et al., 2021; Radford et al., 2021). Generative image models are covered in [[diffusion-models|diffusion models]] and [[autoencoders-and-gans|autoencoders and GANs]].

### When to use it

- Detecting, counting or tracking objects in images or video, where one-stage detectors allow real-time processing (Redmon et al., 2016).
- Medical imaging, where segmentation networks such as U-Net delineate structures with little training data (Ronneberger et al., 2015).
- Classifying or searching images by text descriptions without collecting labels, using image-text models such as CLIP (Radford et al., 2021).

### Strengths and limitations

**Strengths**
- Pre-trained backbones transfer to new tasks with comparatively little labelled data (Dosovitskiy et al., 2021; Ronneberger et al., 2015).
- Real-time detection is possible on video (Redmon et al., 2016).
- Zero-shot recognition through natural language removes the need for a fixed label set (Radford et al., 2021).

**Limitations**
- Supervised models only know their training categories (Radford et al., 2021).
- Vision Transformers need large pre-training datasets to compete with CNNs (Dosovitskiy et al., 2021).
- Speed and accuracy trade off: fast one-stage detectors localise less precisely (Redmon et al., 2016).

### Comparison

| Task | Output | Typical models | Metric |
|---|---|---|---|
| Classification | label(s) per image | [[convolutional-neural-networks\|CNNs]], ViT | accuracy, top-5 error |
| Object detection | boxes + labels | YOLO, Faster R-CNN | mAP |
| Semantic segmentation | class per pixel | U-Net | IoU |
| Instance segmentation | mask per object | Mask R-CNN | mask mAP |
| Zero-shot recognition | label from text prompts | CLIP | zero-shot accuracy |

Sources: Russakovsky et al. (2015); Redmon et al. (2016); He et al. (2017); Ronneberger et al. (2015); Dosovitskiy et al. (2021); Radford et al. (2021).

### In practice

Projects usually start from a pre-trained backbone and fine-tune it on labelled images from the target domain (Dosovitskiy et al., 2021); data augmentation helps when few labelled images exist (Ronneberger et al., 2015). Test images should come from the real deployment conditions, since models generalise unevenly across image styles (Redmon et al., 2016). Image data often shows people, so data protection applies ([[gdpr|GDPR]]).

### Regulatory context

The [[eu-ai-act|EU AI Act]] prohibits certain uses of biometric identification and classifies others as high risk; images of identifiable people are personal data under the [[gdpr|GDPR]].

### Key takeaway

Computer vision maps pixels to labels, boxes, masks or text-aligned embeddings with CNN or Transformer backbones and task-specific heads, and image-text pre-training now allows recognition of categories that were never labelled.

### Sources

- Russakovsky, O., Deng, J., Su, H. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge.* arXiv:1409.0575. [arXiv](https://arxiv.org/abs/1409.0575)
- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2016). *You Only Look Once: Unified, Real-Time Object Detection.* arXiv:1506.02640. [arXiv](https://arxiv.org/abs/1506.02640)
- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN.* arXiv:1703.06870. [arXiv](https://arxiv.org/abs/1703.06870)
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation.* MICCAI 2015. [arXiv](https://arxiv.org/abs/1505.04597)
- Dosovitskiy, A., Beyer, L., Kolesnikov, A. et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv](https://arxiv.org/abs/2010.11929)
- Radford, A., Kim, J. W., Hallacy, C. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* arXiv:2103.00020. [arXiv](https://arxiv.org/abs/2103.00020)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Computer Vision ist das Teilgebiet der KI, das Informationen aus Bildern und Videos gewinnt. Ihre Kernaufgaben sind Bildklassifikation (was ist im Bild), Objekterkennung (wo befinden sich welche Objekte, als Bounding Boxes), Segmentierung (welche Pixel gehören zu welchem Objekt oder welcher Klasse) sowie Keypoint- oder Posenschätzung; weitere Aufgaben sind OCR, Tracking und visuelle Fragebeantwortung. Seit der ImageNet-Challenge dominiert Deep Learning: Convolutional Networks für die [[classification|Klassifikation]], Detektoren mit einem Durchlauf wie YOLO, zweistufige Detektoren mit Maskenzweig wie Mask R-CNN, Encoder-Decoder-Netze wie U-Net für die Segmentierung und Vision Transformer, die Bilder als Folgen von Ausschnitten behandeln (Russakovsky et al., 2015; Redmon et al., 2016; He et al., 2017; Ronneberger et al., 2015; Dosovitskiy et al., 2021). Modelle, die auf Bild-Text-Paaren trainiert sind, wie CLIP, erkennen in natürlicher Sprache benannte Kategorien ohne aufgabenspezifisches Training (Radford et al., 2021).

### Funktionsweise

```text
Bild oder Videoframe (Pixel, H × W × 3)
 ▼
Backbone: CNN oder Vision Transformer → Feature Maps / Patch-Embeddings
 ▼
Aufgabenkopf:
  Klassifikation  → Klassenwahrscheinlichkeiten
  Objekterkennung → Boxen + Klassen (einstufig wie YOLO, zweistufig wie Faster/Mask R-CNN)
  Segmentierung   → Klasse je Pixel oder Maske je Objekt (U-Net, Mask R-CNN)
  Bild–Text       → gemeinsamer Embedding-Raum für Zero-Shot-Erkennung (CLIP)
 ▼
Nachbearbeitung, Evaluation (Accuracy, mAP, IoU) und Betrieb
```

#### 1. Klassifikation und der ImageNet-Benchmark

Die ImageNet Large Scale Visual Recognition Challenge (ILSVRC) lief ab 2010 jährlich und umfasste Objektklassifikation und -erkennung über Hunderte Kategorien und Millionen Bilder, mit mehr als fünfzig teilnehmenden Einrichtungen; das Paper vergleicht darauf auch die Genauigkeit von Maschinen und Menschen (Russakovsky et al., 2015). Klassifikationsmodelle aus Faltungen, Pooling und immer tieferen Architekturen beschreibt [[convolutional-neural-networks|Convolutional Neural Networks]]. Ein auf solchen Daten vortrainiertes Backbone wird meist per Transfer Learning für andere Aufgaben weiterverwendet.

#### 2. Objekterkennung

Objekterkennung sagt für jedes Objekt eine Bounding Box und eine Klasse voraus. Zweistufige Detektoren schlagen zuerst Regionen vor und klassifizieren sie dann; einstufige Detektoren sagen alles in einem Durchlauf voraus. YOLO fasst Erkennung als ein einziges Regressionsproblem vom ganzen Bild auf Boxkoordinaten und Klassenwahrscheinlichkeiten auf, Ende-zu-Ende trainiert; das Basismodell lief mit etwa 45 Bildern pro Sekunde und Fast YOLO mit etwa 155, es machte mehr Lokalisierungsfehler als die besten Systeme, aber weniger Fehlalarme im Hintergrund, und es verallgemeinerte gut von Fotos auf Kunstwerke (Redmon et al., 2016). Detektoren werden mit Mean Average [[classification-metrics|Precision]] (mAP) über Schwellen für Intersection over Union bewertet.

#### 3. Segmentierung

Semantische Segmentierung ordnet jedem Pixel eine Klasse zu; Instanzsegmentierung trennt zusätzlich einzelne Objekte. U-Net verbindet einen kontrahierenden Pfad, der Kontext erfasst, mit einem symmetrischen expandierenden Pfad für genaue Lokalisierung, lässt sich mit starker Datenaugmentierung aus sehr wenigen Bildern Ende-zu-Ende trainieren, segmentiert ein Bild mit 512×512 Pixeln in unter einer Sekunde auf einer GPU und gewann Wettbewerbe zur biomedizinischen Segmentierung (Ronneberger et al., 2015). Mask R-CNN erweitert den zweistufigen Detektor Faster R-CNN um einen Zweig, der für jedes erkannte Objekt eine Maske vorhersagt, läuft mit etwa 5 Bildern pro Sekunde, beherrscht auch Posenschätzung und erzielte Bestwerte in den COCO-Disziplinen Instanzsegmentierung, Objekterkennung und Keypoints (He et al., 2017).

#### 4. Vision Transformer

Der Vision Transformer (ViT) zerlegt ein Bild in Ausschnitte von 16×16 Pixeln und gibt die Folge der Patch-Embeddings ohne Faltungen an einen Standard-Transformer; auf großen Datensätzen vortrainiert und auf ImageNet, CIFAR-100 oder VTAB übertragen, erreicht er die besten CNNs und braucht dabei deutlich weniger Rechenaufwand für das Training (Dosovitskiy et al., 2021). Die Architektur ist dieselbe wie bei Sprachmodellen, siehe [[attention-and-transformers|Attention und Transformer]].

#### 5. Bild und Sprache

Herkömmliche Bildmodelle kennen nur eine feste Menge gelabelter Kategorien. CLIP lernt aus 400 Millionen Bild-Text-Paaren aus dem Internet mit einem kontrastiven Ziel, das jedes Bild seiner Bildunterschrift zuordnet; danach lassen sich Kategorien in natürlicher Sprache benennen, was Zero-Shot-Übertragung ermöglicht: Auf ImageNet erreicht es die Genauigkeit des ursprünglichen ResNet-50, ohne eines seiner 1,28 Millionen Trainingsbeispiele zu nutzen, und es wurde auf über 30 Datensätzen getestet, darunter OCR, Aktionserkennung und Geolokalisierung (Radford et al., 2021). Modelle, die Bilder mit Sprachgenerierung verbinden, behandelt [[multimodal-models|Multimodale Modelle]]; das Lesen von Dokumenten behandelt [[document-processing|Dokumentenverarbeitung]].

#### Herkunft und Varianten

Die ILSVRC ab 2010 lieferte den großen gelabelten Benchmark (Russakovsky et al., 2015); es folgten tiefe CNNs, Echtzeitdetektoren (2015–2016), Instanzsegmentierung (2017), Vision Transformer (2020–2021) und Bild-Text-Pre-Training (2021) (Redmon et al., 2016; He et al., 2017; Dosovitskiy et al., 2021; Radford et al., 2021). Generative Bildmodelle behandeln [[diffusion-models|Diffusionsmodelle]] und [[autoencoders-and-gans|Autoencoder und GANs]].

### Wann einsetzen

- Objekte in Bildern oder Videos erkennen, zählen oder verfolgen, wobei einstufige Detektoren Echtzeitverarbeitung erlauben (Redmon et al., 2016).
- Medizinische Bildgebung, wo Segmentierungsnetze wie U-Net Strukturen mit wenigen Trainingsdaten abgrenzen (Ronneberger et al., 2015).
- Bilder nach Textbeschreibungen klassifizieren oder durchsuchen, ohne Labels zu sammeln, mit Bild-Text-Modellen wie CLIP (Radford et al., 2021).

### Stärken und Grenzen

**Stärken**
- Vortrainierte Backbones lassen sich mit vergleichsweise wenigen gelabelten Daten auf neue Aufgaben übertragen (Dosovitskiy et al., 2021; Ronneberger et al., 2015).
- Echtzeiterkennung auf Video ist möglich (Redmon et al., 2016).
- Zero-Shot-Erkennung über natürliche Sprache macht eine feste Label-Menge überflüssig (Radford et al., 2021).

**Grenzen**
- Überwachte Modelle kennen nur ihre Trainingskategorien (Radford et al., 2021).
- Vision Transformer brauchen große Datensätze zum Vortraining, um mit CNNs mitzuhalten (Dosovitskiy et al., 2021).
- Geschwindigkeit und Genauigkeit stehen im Zielkonflikt: Schnelle einstufige Detektoren lokalisieren weniger genau (Redmon et al., 2016).

### Vergleich

| Aufgabe | Ausgabe | Typische Modelle | Metrik |
|---|---|---|---|
| Klassifikation | Label(s) je Bild | [[convolutional-neural-networks\|CNNs]], ViT | Accuracy, Top-5-Fehler |
| Objekterkennung | Boxen + Labels | YOLO, Faster R-CNN | mAP |
| Semantische Segmentierung | Klasse je Pixel | U-Net | IoU |
| Instanzsegmentierung | Maske je Objekt | Mask R-CNN | Masken-mAP |
| Zero-Shot-Erkennung | Label aus Text-Prompts | CLIP | Zero-Shot-Accuracy |

Quellen: Russakovsky et al. (2015); Redmon et al. (2016); He et al. (2017); Ronneberger et al. (2015); Dosovitskiy et al. (2021); Radford et al. (2021).

### In der Praxis

Projekte starten meist mit einem vortrainierten Backbone und trainieren es auf gelabelten Bildern aus der Zieldomäne nach (Dosovitskiy et al., 2021); Datenaugmentierung hilft, wenn es wenige gelabelte Bilder gibt (Ronneberger et al., 2015). Testbilder sollten aus den echten Einsatzbedingungen stammen, weil Modelle unterschiedlich gut über Bildstile verallgemeinern (Redmon et al., 2016). Bilddaten zeigen oft Menschen, daher gilt der Datenschutz ([[gdpr|DSGVO]]).

### Regulatorischer Kontext

Der [[eu-ai-act|EU AI Act]] verbietet bestimmte Formen biometrischer Identifizierung und stuft andere als hochriskant ein; Bilder erkennbarer Personen sind personenbezogene Daten nach der [[gdpr|DSGVO]].

### Merksatz

Computer Vision bildet Pixel mit CNN- oder Transformer-Backbones und aufgabenspezifischen Köpfen auf Labels, Boxen, Masken oder an Text ausgerichtete [[embeddings|Embeddings]] ab, und Bild-Text-Pre-Training erlaubt inzwischen, Kategorien zu erkennen, die nie gelabelt wurden.

### Quellen

- Russakovsky, O., Deng, J., Su, H. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge.* arXiv:1409.0575. [arXiv](https://arxiv.org/abs/1409.0575)
- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2016). *You Only Look Once: Unified, Real-Time Object Detection.* arXiv:1506.02640. [arXiv](https://arxiv.org/abs/1506.02640)
- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN.* arXiv:1703.06870. [arXiv](https://arxiv.org/abs/1703.06870)
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation.* MICCAI 2015. [arXiv](https://arxiv.org/abs/1505.04597)
- Dosovitskiy, A., Beyer, L., Kolesnikov, A. et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv](https://arxiv.org/abs/2010.11929)
- Radford, A., Kim, J. W., Hallacy, C. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* arXiv:2103.00020. [arXiv](https://arxiv.org/abs/2103.00020)
