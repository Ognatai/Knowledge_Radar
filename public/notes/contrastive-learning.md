---
title_en: Contrastive Learning
title_de: Contrastive Learning
entity_type: Method
aliases:
- Contrastive learning
- Contrastive loss
- InfoNCE
- NT-Xent
- SimCLR
- MoCo
- SimCSE
- Self-supervised contrastive learning
sources:
- https://arxiv.org/abs/1807.03748
- https://arxiv.org/abs/2002.05709
- https://arxiv.org/abs/1911.05722
- https://arxiv.org/abs/2103.00020
- https://arxiv.org/abs/2104.08821
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Contrastive learning trains an encoder so that representations of matching pairs (two views of the same image, an image and its caption, a question and its passage) are close and representations of non-matching pairs are far apart (Chen et al., 2020; Radford et al., 2021). It needs no class labels: positive pairs come from data augmentation or naturally paired data, and the other examples in a batch serve as negatives. The usual loss is a softmax cross-entropy over similarities, called InfoNCE or NT-Xent (van den Oord et al., 2018; Chen et al., 2020). It produced self-supervised image representations matching supervised ones (Chen et al., 2020; He et al., 2020), [[clip|CLIP]]'s joint image–text space (Radford et al., 2021) and state-of-the-art sentence [[embeddings|embeddings]] (Gao et al., 2021).

### How it works

```text
batch of N examples
   ▼  build positives: two augmentations of each example  │  natural pairs (image, caption) / (query, passage)
encoder f(·) ──► representation h ──► projection head g(·) ──► z (L2-normalised)
   ▼
similarity  sim(z_i, z_j) = cosine;   divide by temperature τ
   ▼
loss for positive (i, j):  −log [ exp(sim(z_i, z_j)/τ) / Σ_{k≠i} exp(sim(z_i, z_k)/τ) ]     (InfoNCE / NT-Xent)
   ▼
after training: keep encoder f, drop projection head g; use h for downstream tasks
```

#### 1. Positive and negative pairs

SimCLR samples a minibatch of N images, creates two augmented views of each and treats the two views of the same image as a positive pair and the other 2(N − 1) views in the batch as negatives, without sampling negatives explicitly (Chen et al., 2020). The composition of augmentations, for example random cropping with colour distortion, plays a critical role in defining a useful prediction task (Chen et al., 2020). In text, SimCSE passes the same sentence twice through [[bert|BERT]] with different dropout masks, so dropout acts as minimal augmentation; without it, representations collapse (Gao et al., 2021). With natural pairs, CLIP uses each image and its caption as a positive pair and the other N² − N combinations in the batch as negatives (Radford et al., 2021).

#### 2. The InfoNCE / NT-Xent loss

The loss for a positive pair is the negative log of the softmax of its similarity among all candidates: `ℓ_ij = −log exp(sim(z_i, z_j)/τ) / Σ_{k≠i} exp(sim(z_i, z_k)/τ)`, with [[cosine-similarity|cosine similarity]] and a temperature τ (Chen et al., 2020). It is a [[cross-entropy|cross-entropy]] over which candidate is the positive, and Chen et al. (2020) call it NT-Xent, the normalised temperature-scaled cross-entropy loss. van den Oord et al. (2018) introduced it as InfoNCE in Contrastive Predictive Coding, where it maximises a lower bound on the mutual information between a context and future observations, and used it for speech, images, text and reinforcement learning. Normalised embeddings and a well-chosen temperature matter (Chen et al., 2020; [[softmax|softmax]]).

#### 3. Many negatives: large batches or a queue

More negatives make the task harder and the representations better. SimCLR varied the batch size from 256 to 8,192, which gives 16,382 negatives per positive pair, used the LARS optimiser to keep training stable, and aggregated batch normalisation statistics over all devices so that the model could not exploit information leaking within one device (Chen et al., 2020). MoCo instead keeps a queue of encoded keys from previous minibatches as a large dictionary and encodes keys with a momentum encoder, a slowly updated moving average of the query encoder, so that the dictionary stays consistent (He et al., 2020).

#### 4. Projection head

SimCLR showed that a learnable non-linear projection between the representation and the contrastive loss substantially improves the representation; after training the head is discarded and the encoder output is used (Chen et al., 2020). CLIP, with its very large data set, used only a linear projection and saw no difference in training efficiency (Radford et al., 2021).

#### 5. Results

A linear classifier on SimCLR's self-supervised ResNet-50 features reached 76.5% top-1 accuracy on ImageNet, matching a supervised ResNet-50, and fine-tuned on 1% of the labels it reached 85.8% top-5 accuracy (Chen et al., 2020; [[imagenet|ImageNet]]). MoCo's representations outperformed supervised pre-training on 7 detection and segmentation tasks (He et al., 2020). CLIP, trained on 400 million image–text pairs from the internet, matched the original ResNet-50 on ImageNet zero-shot without using any of its 1.28 million training images (Radford et al., 2021; [[multimodal-models|multimodal models]]). SimCSE reached 76.3% (unsupervised) and 81.6% (supervised, with natural language inference pairs: entailment as positives, contradiction as hard negatives) average Spearman correlation on semantic textual similarity, and made the anisotropic space of pre-trained embeddings more uniform (Gao et al., 2021; [[natural-language-inference|natural language inference]]).

#### Origin and variants

Contrastive Predictive Coding (van den Oord et al., 2018) introduced InfoNCE; MoCo (He et al., 2020) and SimCLR (Chen et al., 2020) made contrastive self-supervision competitive in vision; CLIP (Radford et al., 2021) applied it to image–text pairs and SimCSE (Gao et al., 2021) to sentences. Dense retrievers such as [[dense-passage-retrieval|DPR]] train question and passage encoders with the same in-batch negative principle.

### When to use it

- Learning representations from unlabelled data, then training a light classifier or fine-tuning with few labels (Chen et al., 2020).
- Aligning two modalities or two kinds of text, such as images and captions, or queries and documents ([[semantic-retrieval|semantic retrieval]]; Radford et al., 2021).
- Training sentence embeddings for similarity search and [[clustering|clustering]] ([[sentence-bert|Sentence-BERT]]; Gao et al., 2021).

### Strengths and limitations

**Strengths**
- No manual labels needed; supervision comes from augmentations or natural pairs (Chen et al., 2020; Radford et al., 2021).
- Representations transfer well, sometimes better than supervised pre-training (He et al., 2020).
- Joint embedding spaces enable zero-shot [[classification|classification]] and cross-modal retrieval (Radford et al., 2021).

**Limitations**
- Needs many negatives, hence large batches or extra machinery such as a queue (Chen et al., 2020; He et al., 2020).
- Quality depends on the augmentations, which encode what the model should be invariant to (Chen et al., 2020).

### Comparison

| Method | Positives | Negatives | Domain |
|---|---|---|---|
| CPC (InfoNCE) | context and future observation | other samples | speech, images, text, RL |
| SimCLR | two augmentations of an image | rest of the batch | images |
| MoCo | two augmentations | queue of past keys | images |
| CLIP | image and its caption | other pairs in the batch | image–text |
| SimCSE | same sentence, two dropout masks (or entailment) | batch (or contradiction) | sentences |

Sources: van den Oord et al. (2018), Chen et al. (2020), He et al. (2020), Radford et al. (2021), Gao et al. (2021).

### In practice

Batch size, temperature and augmentations are the main levers (Chen et al., 2020). Representations are usually evaluated with a linear classifier on frozen features or by fine-tuning on a downstream task (Chen et al., 2020). For retrieval, embeddings trained contrastively are compared with cosine similarity, matching their training objective ([[cosine-similarity|cosine similarity]]).

### Key takeaway

Contrastive learning pulls matching pairs together and pushes the rest of the batch apart with a temperature-scaled softmax loss, which learns transferable representations without labels and underlies CLIP and modern sentence embeddings.

### Sources

- van den Oord, A., Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding.* [arXiv:1807.03748](https://arxiv.org/abs/1807.03748)
- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations.* ICML 2020. [arXiv:2002.05709](https://arxiv.org/abs/2002.05709)
- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). *Momentum Contrast for Unsupervised Visual Representation Learning.* CVPR 2020. [arXiv:1911.05722](https://arxiv.org/abs/1911.05722)
- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
- Gao, T., Yao, X. & Chen, D. (2021). *SimCSE: Simple Contrastive Learning of Sentence Embeddings.* EMNLP 2021. [arXiv:2104.08821](https://arxiv.org/abs/2104.08821)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Contrastive Learning trainiert einen Encoder so, dass die Repräsentationen zusammengehöriger Paare (zwei Ansichten desselben Bildes, ein Bild und seine Bildunterschrift, eine Frage und ihre Passage) nah beieinander und die Repräsentationen nicht zusammengehöriger Paare weit voneinander entfernt liegen (Chen et al., 2020; Radford et al., 2021). Es braucht keine Klassenlabels: Positive Paare entstehen durch Datenaugmentierung oder aus natürlich gepaarten Daten, und die übrigen Beispiele im Batch dienen als Negative. Der übliche Verlust ist eine Softmax-Cross-Entropy über Ähnlichkeiten, genannt InfoNCE oder NT-Xent (van den Oord et al., 2018; Chen et al., 2020). Er brachte selbstüberwachte Bildrepräsentationen hervor, die mit überwachten mithalten (Chen et al., 2020; He et al., 2020), den gemeinsamen Bild-Text-Raum von [[clip|CLIP]] (Radford et al., 2021) und Satz-[[embeddings|Embeddings]] auf dem Stand der Technik (Gao et al., 2021).

### Funktionsweise

```text
Batch mit N Beispielen
   ▼  Positive bilden: zwei Augmentierungen jedes Beispiels  │  natürliche Paare (Bild, Bildunterschrift) / (Anfrage, Passage)
Encoder f(·) ──► Repräsentation h ──► Projektionskopf g(·) ──► z (L2-normalisiert)
   ▼
Ähnlichkeit  sim(z_i, z_j) = Kosinus;   durch Temperatur τ teilen
   ▼
Verlust für Positivpaar (i, j):  −log [ exp(sim(z_i, z_j)/τ) / Σ_{k≠i} exp(sim(z_i, z_k)/τ) ]     (InfoNCE / NT-Xent)
   ▼
nach dem Training: Encoder f behalten, Projektionskopf g verwerfen; h für nachgelagerte Aufgaben nutzen
```

#### 1. Positive und negative Paare

SimCLR zieht einen Minibatch aus N Bildern, erzeugt von jedem zwei augmentierte Ansichten und behandelt die beiden Ansichten desselben Bildes als Positivpaar und die übrigen 2(N − 1) Ansichten im Batch als Negative, ohne Negative ausdrücklich zu ziehen (Chen et al., 2020). Die Kombination der Augmentierungen, etwa zufälliges Zuschneiden mit Farbverzerrung, ist entscheidend dafür, eine nützliche Vorhersageaufgabe zu definieren (Chen et al., 2020). Bei Text gibt SimCSE denselben Satz zweimal mit unterschiedlichen Dropout-Masken durch [[bert|BERT]], sodass Dropout als minimale Augmentierung wirkt; ohne sie kollabieren die Repräsentationen (Gao et al., 2021). Bei natürlichen Paaren nutzt CLIP jedes Bild und seine Bildunterschrift als Positivpaar und die übrigen N² − N Kombinationen im Batch als Negative (Radford et al., 2021).

#### 2. Der Verlust InfoNCE / NT-Xent

Der Verlust für ein Positivpaar ist der negative Logarithmus der Softmax seiner Ähnlichkeit unter allen Kandidaten: `ℓ_ij = −log exp(sim(z_i, z_j)/τ) / Σ_{k≠i} exp(sim(z_i, z_k)/τ)`, mit [[cosine-similarity|Cosine Similarity]] und einer Temperatur τ (Chen et al., 2020). Er ist eine [[cross-entropy|Cross-Entropy]] darüber, welcher Kandidat der positive ist, und Chen et al. (2020) nennen ihn NT-Xent, die normalisierte, temperaturskalierte Cross-Entropy. van den Oord et al. (2018) führten ihn als InfoNCE im Contrastive Predictive Coding ein, wo er eine untere Schranke der Transinformation zwischen einem Kontext und künftigen Beobachtungen maximiert, und nutzten ihn für Sprache, Bilder, Text und Reinforcement Learning. Normalisierte Embeddings und eine gut gewählte Temperatur sind wichtig (Chen et al., 2020; [[softmax|Softmax]]).

#### 3. Viele Negative: große Batches oder eine Warteschlange

Mehr Negative machen die Aufgabe schwerer und die Repräsentationen besser. SimCLR variierte die Batch-Größe von 256 bis 8.192, was 16.382 Negative pro Positivpaar ergibt, nutzte den LARS-Optimierer für ein stabiles Training und aggregierte die Statistiken der Batch-Normalisierung über alle Geräte, damit das Modell keine Information ausnutzen konnte, die innerhalb eines Geräts durchsickert (Chen et al., 2020). MoCo hält stattdessen eine Warteschlange kodierter Keys aus früheren Minibatches als großes Wörterbuch und kodiert Keys mit einem Momentum-Encoder, einem langsam aktualisierten gleitenden Mittel des Query-Encoders, damit das Wörterbuch konsistent bleibt (He et al., 2020).

#### 4. Projektionskopf

SimCLR zeigte, dass eine lernbare nichtlineare Projektion zwischen Repräsentation und kontrastivem Verlust die Repräsentation deutlich verbessert; nach dem Training wird der Kopf verworfen und die Ausgabe des Encoders genutzt (Chen et al., 2020). CLIP nutzte bei seinem sehr großen Datensatz nur eine lineare Projektion und sah keinen Unterschied in der Trainingseffizienz (Radford et al., 2021).

#### 5. Ergebnisse

Ein linearer Klassifikator auf den selbstüberwachten ResNet-50-Merkmalen von SimCLR erreichte 76,5 % Top-1-Genauigkeit auf ImageNet, so viel wie ein überwachtes ResNet-50, und mit Fine-Tuning auf 1 % der Labels 85,8 % Top-5-Genauigkeit (Chen et al., 2020; [[imagenet|ImageNet]]). Die Repräsentationen von MoCo übertrafen überwachtes Vortraining bei 7 Erkennungs- und Segmentierungsaufgaben (He et al., 2020). CLIP, trainiert auf 400 Millionen Bild-Text-Paaren aus dem Internet, erreichte zero-shot die Genauigkeit des ursprünglichen ResNet-50 auf ImageNet, ohne eines von dessen 1,28 Millionen Trainingsbildern zu nutzen (Radford et al., 2021; [[multimodal-models|multimodale Modelle]]). SimCSE erreichte im Mittel 76,3 % (unüberwacht) und 81,6 % (überwacht, mit Paaren zur Natural Language Inference: Entailment als Positive, Contradiction als harte Negative) Spearman-Korrelation bei semantischer Textähnlichkeit und machte den anisotropen Raum vortrainierter Embeddings gleichmäßiger (Gao et al., 2021; [[natural-language-inference|Natural Language Inference]]).

#### Ursprung und Varianten

Contrastive Predictive Coding (van den Oord et al., 2018) führte InfoNCE ein; MoCo (He et al., 2020) und SimCLR (Chen et al., 2020) machten kontrastive Selbstüberwachung im Bildbereich konkurrenzfähig; CLIP (Radford et al., 2021) übertrug sie auf Bild-Text-Paare und SimCSE (Gao et al., 2021) auf Sätze. Dense Retriever wie [[dense-passage-retrieval|DPR]] trainieren Frage- und Passagen-Encoder nach demselben Prinzip der In-Batch-Negative.

### Wann einsetzen

- Repräsentationen aus ungelabelten Daten lernen und danach einen leichten Klassifikator trainieren oder mit wenigen Labels nachtrainieren (Chen et al., 2020).
- Zwei Modalitäten oder zwei Arten von Text aufeinander abbilden, etwa Bilder und Bildunterschriften oder Anfragen und Dokumente ([[semantic-retrieval|semantisches Retrieval]]; Radford et al., 2021).
- Satz-Embeddings für Ähnlichkeitssuche und [[clustering|Clustering]] trainieren ([[sentence-bert|Sentence-BERT]]; Gao et al., 2021).

### Stärken und Grenzen

**Stärken**
- Keine manuellen Labels nötig; die Überwachung stammt aus Augmentierungen oder natürlichen Paaren (Chen et al., 2020; Radford et al., 2021).
- Die Repräsentationen übertragen sich gut, manchmal besser als nach überwachtem Vortraining (He et al., 2020).
- Gemeinsame Embedding-Räume ermöglichen Zero-Shot-Klassifikation und modalitätsübergreifendes Retrieval (Radford et al., 2021).

**Grenzen**
- Braucht viele Negative, also große Batches oder zusätzliche Mechanismen wie eine Warteschlange (Chen et al., 2020; He et al., 2020).
- Die Qualität hängt von den Augmentierungen ab, die festlegen, wogegen das Modell invariant sein soll (Chen et al., 2020).

### Vergleich

| Verfahren | Positive | Negative | Bereich |
|---|---|---|---|
| CPC (InfoNCE) | Kontext und künftige Beobachtung | andere Stichproben | Sprache, Bilder, Text, RL |
| SimCLR | zwei Augmentierungen eines Bildes | Rest des Batches | Bilder |
| MoCo | zwei Augmentierungen | Warteschlange früherer Keys | Bilder |
| CLIP | Bild und seine Bildunterschrift | andere Paare im Batch | Bild-Text |
| SimCSE | derselbe Satz, zwei Dropout-Masken (oder Entailment) | Batch (oder Contradiction) | Sätze |

Quellen: van den Oord et al. (2018), Chen et al. (2020), He et al. (2020), Radford et al. (2021), Gao et al. (2021).

### In der Praxis

Batch-Größe, Temperatur und Augmentierungen sind die wichtigsten Stellschrauben (Chen et al., 2020). Repräsentationen werden meist mit einem linearen Klassifikator auf eingefrorenen Merkmalen oder durch Fine-Tuning auf einer nachgelagerten Aufgabe bewertet (Chen et al., 2020). Für Retrieval werden kontrastiv trainierte Embeddings mit Cosine Similarity verglichen, passend zu ihrem Trainingsziel ([[cosine-similarity|Cosine Similarity]]).

### Merksatz

Contrastive Learning zieht zusammengehörige Paare zusammen und drückt den Rest des Batches mit einem temperaturskalierten Softmax-Verlust weg; so entstehen ohne Labels übertragbare Repräsentationen, auf denen CLIP und moderne Satz-Embeddings beruhen.

### Quellen

- van den Oord, A., Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding.* [arXiv:1807.03748](https://arxiv.org/abs/1807.03748)
- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations.* ICML 2020. [arXiv:2002.05709](https://arxiv.org/abs/2002.05709)
- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). *Momentum Contrast for Unsupervised Visual Representation Learning.* CVPR 2020. [arXiv:1911.05722](https://arxiv.org/abs/1911.05722)
- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML 2021. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
- Gao, T., Yao, X. & Chen, D. (2021). *SimCSE: Simple Contrastive Learning of Sentence Embeddings.* EMNLP 2021. [arXiv:2104.08821](https://arxiv.org/abs/2104.08821)
