---
title_en: ImageNet
title_de: ImageNet
entity_type: Dataset
aliases:
- ImageNet
- ILSVRC
- ImageNet Large Scale Visual Recognition Challenge
- ImageNet-1k
sources:
- https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf
- https://arxiv.org/abs/1409.0575
- https://arxiv.org/abs/1912.07726
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

ImageNet is a large image database organised by the noun hierarchy of WordNet, introduced in 2009 with the aim of illustrating most of WordNet's roughly 80,000 noun synsets with 500 to 1,000 clean, full-resolution images each; the first version had 3.2 million images in 5,247 synsets, labelled through Amazon Mechanical Turk with about 99.7% precision (Deng et al., 2009). Its best-known subset is the ImageNet Large Scale Visual Recognition Challenge (ILSVRC), run annually from 2010, whose [[classification|classification]] task uses 1,000 categories with about 1.2 million training images (Russakovsky et al., 2015). The challenge became the standard benchmark for large-scale object recognition: after a deep [[convolutional-neural-networks|convolutional network]] won in 2012 with 16.4% top-5 error, error fell to 6.7% by 2014, close to an estimated human error of 5.1% (Russakovsky et al., 2015). Later analysis of its person categories showed many offensive or non-visual labels and unequal representation of demographic groups (Yang et al., 2020).

### How it works

```text
WordNet noun synsets (e.g. mammal → … → dog → husky)
  └─ candidate images from web image search, queries = synonyms (also in other languages)   ~10K per synset
       └─ Amazon Mechanical Turk: "Is this a <synset>?" several workers per image,
          adaptive agreement threshold per synset                                  ~500–1,000 clean images
ILSVRC subset: 1,000 classes, ~1.2M train / 50K val / 100K test; metric: top-5 error
```

#### 1. A hierarchy borrowed from WordNet

ImageNet uses WordNet's synonym sets ("synsets") as categories, so each image is attached to a node in a semantic tree, for example mammal → placental → carnivore → canine → dog → working dog → husky (Deng et al., 2009). The 2009 version covered twelve subtrees such as mammal, bird, vehicle, furniture, tool, flower and fruit, with 5,247 synsets and 3.2 million images, and was planned to grow to about 50 million images (Deng et al., 2009).

#### 2. Collecting and cleaning images

Because only about 10% of results from web image search are accurate, ImageNet first collected a large pool of candidates per synset by querying several search engines with the WordNet synonyms, giving over 10,000 images per synset after removing duplicates (Deng et al., 2009). Workers on Amazon Mechanical Turk then verified whether each image showed the synset, with several votes per image and a confidence threshold that adapts to how hard the synset is; on 80 sampled synsets, the cleaned data reached an average precision of 99.7% (Deng et al., 2009).

#### 3. The ILSVRC benchmark

ILSVRC ran annually from 2010 with tasks in image classification, single-object localisation and object detection (Russakovsky et al., 2015). The classification data has 1,000 object classes, about 1.2 million training, 50,000 validation and 100,000 test images, including fine-grained classes such as 120 dog breeds; test labels are withheld and submissions are scored by a server (Russakovsky et al., 2015). Since 2012 the main metric has been top-5 error: a prediction counts as correct if the true class is among the model's five guesses (Russakovsky et al., 2015).

#### 4. From hand-crafted features to deep learning

Early winners used hand-crafted features such as SIFT with linear or kernel classifiers. In 2012 the SuperVision team trained a large convolutional neural network with 60 million parameters on GPUs with dropout and reduced classification error to 16.4%; GoogLeNet reached 6.7% in 2014 on the unchanged dataset (Russakovsky et al., 2015). On a sample of 1,500 test images, a trained human annotator had an estimated error of 5.1% (Russakovsky et al., 2015). Later architectures such as [[resnet|ResNet]] and the [[vision-transformer|Vision Transformer]] were also evaluated on ImageNet.

#### Origin and variants

Jia Deng, Li Fei-Fei and colleagues at Princeton presented ImageNet at CVPR 2009 (Deng et al., 2009). The ILSVRC paper describes the 1,000-class subset that is today often called ImageNet-1k (Russakovsky et al., 2015). Yang et al. (2020) examined the 2,832 people categories in the person subtree of the full ImageNet: 1,593 were potentially offensive labels to be removed, only 158 of the remaining 1,239 were visual, and crowdsourced annotations showed unequal representation by gender, skin colour and age.

### When to use it

- Benchmarking image classification models, and pre-training backbones that are then fine-tuned for other vision tasks ([[computer-vision|computer vision]], [[convolutional-neural-networks|convolutional neural networks]]).
- Studying the history of deep learning, since ILSVRC results trace the shift from hand-crafted features to [[neural-networks|neural networks]] (Russakovsky et al., 2015).
- Not as a fair or representative sample of people: its person categories have known problems (Yang et al., 2020).

### Strengths and limitations

**Strengths**
- Large scale, broad diversity and high label precision for its time (Deng et al., 2009).
- A hierarchical label space that allows fine-grained and coarse evaluation (Deng et al., 2009).
- A stable benchmark: the classification dataset has not changed since 2012, so results are comparable across years (Russakovsky et al., 2015).

**Limitations**
- Labels come from WordNet's vocabulary, which includes offensive and non-imageable concepts for people (Yang et al., 2020).
- Images collected from web search and labelled by crowdworkers inherit their biases, including unequal demographic representation (Yang et al., 2020).
- One label per image in the classification task ignores scenes with several objects; top-5 error tolerates such ambiguity (Russakovsky et al., 2015).
- Results on a widely reused test set become optimistic over time ([[overfitting|overfitting]]).

### Comparison

| Dataset | Classes | Images |
|---|---|---|
| PASCAL VOC 2012 | 20 | 21,738 |
| ILSVRC 2012 | 1,000 | 1,431,167 annotated |
| COCO | 91 | more than 328,000, with 2.5 million segmented instances |

Source: Russakovsky et al. (2015).

### In practice

Pre-trained ImageNet models are the usual starting point for transfer learning in vision, while new models are increasingly pre-trained on far larger datasets, as with the Vision Transformer ([[vision-transformer|Vision Transformer]]). When a model is meant to recognise or describe people, check its training data for problematic categories and demographic imbalance, and evaluate across groups ([[fairness-metrics|fairness metrics]]).

### Key takeaway

ImageNet turned WordNet's hierarchy into millions of crowd-verified images; its 1,000-class ILSVRC benchmark drove the rise of deep convolutional networks, while its person categories show how dataset construction carries bias.

### Sources

- Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K. & Fei-Fei, L. (2009). ImageNet: A Large-Scale Hierarchical Image Database. *CVPR 2009*. [PDF](https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf)
- Russakovsky, O., Deng, J. et al. (2015). ImageNet Large Scale Visual Recognition Challenge. *International Journal of Computer Vision*. [arXiv:1409.0575](https://arxiv.org/abs/1409.0575)
- Yang, K., Qinami, K., Fei-Fei, L. & Deng, J. (2020). Towards Fairer Datasets: Filtering and Balancing the Distribution of the People Subtree in the ImageNet Hierarchy. *FAT* 2020*. [arXiv:1912.07726](https://arxiv.org/abs/1912.07726)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

ImageNet ist eine große Bilddatenbank, die nach der Substantiv-Hierarchie von WordNet geordnet ist; sie wurde 2009 mit dem Ziel vorgestellt, die meisten der rund 80 000 Substantiv-Synsets von WordNet mit je 500 bis 1 000 sauberen Bildern in voller Auflösung zu illustrieren; die erste Version umfasste 3,2 Millionen Bilder in 5 247 Synsets, gelabelt über Amazon Mechanical Turk mit rund 99,7 % Präzision (Deng et al., 2009). Die bekannteste Teilmenge ist die ImageNet Large Scale Visual Recognition Challenge (ILSVRC), die ab 2010 jährlich stattfand und deren Klassifikationsaufgabe 1 000 Kategorien mit rund 1,2 Millionen Trainingsbildern nutzt (Russakovsky et al., 2015). Die Challenge wurde zum Standard-Benchmark für Objekterkennung im großen Maßstab: Nachdem 2012 ein tiefes [[convolutional-neural-networks|Convolutional Neural Network]] mit 16,4 % Top-5-Fehler gewann, sank der Fehler bis 2014 auf 6,7 %, nahe am geschätzten menschlichen Fehler von 5,1 % (Russakovsky et al., 2015). Spätere Analysen der Personenkategorien zeigten viele beleidigende oder nicht visuelle Labels und eine ungleiche Repräsentation demografischer Gruppen (Yang et al., 2020).

### Funktionsweise

```text
WordNet-Substantiv-Synsets (z. B. mammal → … → dog → husky)
  └─ Kandidatenbilder aus der Websuche, Anfragen = Synonyme (auch in anderen Sprachen)   ~10 000 je Synset
       └─ Amazon Mechanical Turk: "Zeigt das Bild ein <Synset>?" mehrere Personen je Bild,
          adaptive Zustimmungsschwelle je Synset                                       ~500–1 000 saubere Bilder
ILSVRC-Teilmenge: 1 000 Klassen, ~1,2 Mio. Training / 50 000 Validierung / 100 000 Test; Metrik: Top-5-Fehler
```

#### 1. Eine von WordNet übernommene Hierarchie

ImageNet nutzt die Synonymgruppen („Synsets“) von WordNet als Kategorien, sodass jedes Bild an einem Knoten eines semantischen Baums hängt, etwa mammal → placental → carnivore → canine → dog → working dog → husky (Deng et al., 2009). Die Version von 2009 umfasste zwölf Teilbäume wie Säugetiere, Vögel, Fahrzeuge, Möbel, Werkzeuge, Blumen und Früchte mit 5 247 Synsets und 3,2 Millionen Bildern und sollte auf rund 50 Millionen Bilder wachsen (Deng et al., 2009).

#### 2. Bilder sammeln und bereinigen

Weil nur etwa 10 % der Ergebnisse einer Bildsuche im Web zutreffen, sammelte ImageNet zunächst einen großen Kandidatenpool je Synset, indem mehrere Suchmaschinen mit den WordNet-Synonymen abgefragt wurden; nach Entfernen von Duplikaten blieben über 10 000 Bilder je Synset (Deng et al., 2009). Beschäftigte auf Amazon Mechanical Turk prüften dann, ob jedes Bild das Synset zeigt, mit mehreren Stimmen je Bild und einer Konfidenzschwelle, die sich an die Schwierigkeit des Synsets anpasst; bei 80 Stichproben-Synsets erreichten die bereinigten Daten eine durchschnittliche Präzision von 99,7 % (Deng et al., 2009).

#### 3. Der Benchmark ILSVRC

Die ILSVRC lief ab 2010 jährlich mit Aufgaben zur Bildklassifikation, Lokalisierung einzelner Objekte und Objektdetektion (Russakovsky et al., 2015). Die Klassifikationsdaten umfassen 1 000 Objektklassen, rund 1,2 Millionen Trainings-, 50 000 Validierungs- und 100 000 Testbilder, darunter feine Klassen wie 120 Hunderassen; die Testlabels werden zurückgehalten, und Einreichungen bewertet ein Server (Russakovsky et al., 2015). Seit 2012 ist die Hauptmetrik der Top-5-Fehler: Eine Vorhersage gilt als richtig, wenn die wahre Klasse unter den fünf Vorschlägen des Modells ist (Russakovsky et al., 2015).

#### 4. Von handgefertigten Merkmalen zu Deep Learning

Frühe Gewinner nutzten handgefertigte Merkmale wie SIFT mit linearen oder Kernel-Klassifikatoren. 2012 trainierte das Team SuperVision ein großes Convolutional Neural Network mit 60 Millionen Parametern auf GPUs mit Dropout und senkte den Klassifikationsfehler auf 16,4 %; GoogLeNet erreichte 2014 auf dem unveränderten Datensatz 6,7 % (Russakovsky et al., 2015). Auf einer Stichprobe von 1 500 Testbildern hatte ein geschulter menschlicher Annotator einen geschätzten Fehler von 5,1 % (Russakovsky et al., 2015). Spätere Architekturen wie [[resnet|ResNet]] und der [[vision-transformer|Vision Transformer]] wurden ebenfalls auf ImageNet evaluiert.

#### Herkunft und Varianten

Jia Deng, Li Fei-Fei und Kolleginnen und Kollegen in Princeton stellten ImageNet auf der CVPR 2009 vor (Deng et al., 2009). Das ILSVRC-Paper beschreibt die Teilmenge mit 1 000 Klassen, die heute oft ImageNet-1k heißt (Russakovsky et al., 2015). Yang et al. (2020) untersuchten die 2 832 Personenkategorien im Personen-Teilbaum des vollständigen ImageNet: 1 593 waren potenziell beleidigende Labels, die entfernt werden sollten, nur 158 der verbleibenden 1 239 waren visuell, und Crowdsourcing-Annotationen zeigten eine ungleiche Repräsentation nach Geschlecht, Hautfarbe und Alter.

### Wann einsetzen

- Benchmarking von Bildklassifikationsmodellen und Vortraining von Backbones, die dann für andere Bildaufgaben feinabgestimmt werden ([[computer-vision|Computer Vision]], [[convolutional-neural-networks|Convolutional Neural Networks]]).
- Untersuchung der Geschichte des Deep Learning, da die ILSVRC-Ergebnisse den Wechsel von handgefertigten Merkmalen zu neuronalen Netzen zeigen (Russakovsky et al., 2015).
- Nicht als faire oder repräsentative Stichprobe von Menschen: Die Personenkategorien haben bekannte Probleme (Yang et al., 2020).

### Stärken und Grenzen

**Stärken**
- Großer Umfang, breite Vielfalt und für seine Zeit hohe Labelpräzision (Deng et al., 2009).
- Ein hierarchischer Labelraum, der feine und grobe Evaluation erlaubt (Deng et al., 2009).
- Ein stabiler Benchmark: Der Klassifikationsdatensatz ist seit 2012 unverändert, sodass Ergebnisse über die Jahre vergleichbar sind (Russakovsky et al., 2015).

**Grenzen**
- Die Labels stammen aus dem Vokabular von WordNet, das bei Personen beleidigende und nicht bildlich darstellbare Begriffe enthält (Yang et al., 2020).
- Aus der Websuche gesammelte und von Crowdworkern gelabelte Bilder übernehmen deren Verzerrungen, einschließlich ungleicher demografischer Repräsentation (Yang et al., 2020).
- Ein Label je Bild in der Klassifikationsaufgabe ignoriert Szenen mit mehreren Objekten; der Top-5-Fehler toleriert diese Mehrdeutigkeit (Russakovsky et al., 2015).
- Ergebnisse auf einer viel wiederverwendeten Testmenge werden mit der Zeit zu optimistisch ([[overfitting|Overfitting]]).

### Vergleich

| Datensatz | Klassen | Bilder |
|---|---|---|
| PASCAL VOC 2012 | 20 | 21 738 |
| ILSVRC 2012 | 1 000 | 1 431 167 annotiert |
| COCO | 91 | mehr als 328 000, mit 2,5 Millionen segmentierten Instanzen |

Quelle: Russakovsky et al. (2015).

### In der Praxis

Auf ImageNet vortrainierte Modelle sind der übliche Ausgangspunkt für Transfer Learning in der Bildverarbeitung, während neue Modelle zunehmend auf weit größeren Datensätzen vortrainiert werden, wie beim Vision Transformer ([[vision-transformer|Vision Transformer]]). Soll ein Modell Menschen erkennen oder beschreiben, sind seine Trainingsdaten auf problematische Kategorien und demografisches Ungleichgewicht zu prüfen und Evaluationen über Gruppen hinweg vorzunehmen ([[fairness-metrics|Fairness-Metriken]]).

### Merksatz

ImageNet machte aus der Hierarchie von WordNet Millionen von der Crowd geprüfte Bilder; sein ILSVRC-Benchmark mit 1 000 Klassen trieb den Aufstieg tiefer Convolutional Networks voran, während seine Personenkategorien zeigen, wie die Konstruktion eines Datensatzes Bias weiterträgt.

### Quellen

- Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K. & Fei-Fei, L. (2009). ImageNet: A Large-Scale Hierarchical Image Database. *CVPR 2009*. [PDF](https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf)
- Russakovsky, O., Deng, J. et al. (2015). ImageNet Large Scale Visual Recognition Challenge. *International Journal of Computer Vision*. [arXiv:1409.0575](https://arxiv.org/abs/1409.0575)
- Yang, K., Qinami, K., Fei-Fei, L. & Deng, J. (2020). Towards Fairer Datasets: Filtering and Balancing the Distribution of the People Subtree in the ImageNet Hierarchy. *FAT* 2020*. [arXiv:1912.07726](https://arxiv.org/abs/1912.07726)
