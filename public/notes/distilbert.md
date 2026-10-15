---
title_en: DistilBERT
title_de: DistilBERT
entity_type: Method
aliases:
- DistilBERT
sources:
- https://arxiv.org/abs/1910.01108
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

DistilBERT is a smaller version of [[bert|BERT]] created by [[knowledge-distillation|knowledge distillation]] during pre-training: a 6-layer student learns from the 12-layer BERT-base teacher and keeps 97% of its language understanding performance on [[glue|GLUE]] with 40% fewer parameters and 60% faster inference (Sanh et al., 2019). Its training objective combines three losses: matching the teacher's soft output distribution, the usual masked language modelling loss and a cosine loss that aligns the student's hidden states with the teacher's (Sanh et al., 2019). Released by Hugging Face in 2019, it is a general-purpose model that can be fine-tuned like BERT and is small enough for on-device use.

### How it works

```text
teacher: BERT-base (12 layers, 110 M parameters)
student: same architecture with 6 layers, no token-type embeddings, no pooler (66 M parameters)
 ▼ initialise student from teacher: take one layer out of two
 ▼ pre-train on English Wikipedia + Toronto Book Corpus with
    L = L_ce (soft targets of the teacher, temperature T)
      + L_mlm (masked language modelling)
      + L_cos (cosine between student and teacher hidden states)
 ▼ fine-tune on the downstream task like BERT (optionally with a second distillation step)
```

#### 1. Distillation during pre-training

Most earlier work distilled BERT for one specific task after fine-tuning; DistilBERT applies knowledge distillation during pre-training instead, producing a general-purpose model that can then be fine-tuned on many tasks (Sanh et al., 2019). In distillation, a compact student is trained to reproduce the behaviour of a larger teacher; the teacher's full output distribution, including the small probabilities of wrong classes, carries more information than one-hot labels (Sanh et al., 2019). For a masked token in "I think this is the beginning of a beautiful [MASK]", BERT puts high probability on "day" and "life" and spreads the rest over valid alternatives such as "future" or "story".

#### 2. The triple loss

The distillation loss `L_ce = Σ_i t_i · log(s_i)` compares the teacher's probabilities t with the student's s, both softened with the same temperature T in the softmax `p_i = exp(z_i/T) / Σ_j exp(z_j/T)`; at inference T is set to 1 (Sanh et al., 2019). It is combined linearly with the masked language modelling loss of BERT and a cosine embedding loss that aligns the directions of student and teacher hidden-state vectors. In the ablation, the two distillation losses accounted for most of the performance, while removing the masked language modelling loss had little impact (Sanh et al., 2019).

#### 3. Student architecture and initialisation

The student keeps BERT's general architecture but halves the number of layers and removes the token-type [[embeddings|embeddings]] and the pooler; the authors reduced depth rather than width because changes to the hidden size affected efficiency less than the number of layers (Sanh et al., 2019). Because teacher and student share the hidden dimension, the student is initialised by taking one of every two teacher layers; random initialisation cost 3.69 points on the GLUE macro-score in the ablation (Sanh et al., 2019).

#### 4. Training setup

Following RoBERTa's practices, DistilBERT was trained with very large batches of up to 4,000 examples via gradient accumulation, dynamic masking and without next-sentence prediction, on the same corpus as BERT, English Wikipedia and the Toronto Book Corpus (Sanh et al., 2019). Training took about 90 hours on 8 V100 GPUs with 16 GB each.

#### 5. Results

On the GLUE dev sets, DistilBERT scored 77.0 against 79.5 for BERT-base and 68.7 for the ELMo baseline (Sanh et al., 2019). On IMDb sentiment classification it reached 92.82% accuracy against 93.46%, and on SQuAD 1.1 77.7/85.8 EM/F1 against 81.2/88.5, improving to 79.1/86.9 with a second distillation step during fine-tuning. With 66 million instead of 110 million parameters, a full pass over the STS-B task on CPU took 410 instead of 668 seconds; on an iPhone 7 Plus, a question answering model was 71% faster than one based on BERT-base and weighed 207 MB (Sanh et al., 2019).

#### Origin and variants

Victor Sanh, Lysandre Debut, Julien Chaumond and Thomas Wolf of Hugging Face presented DistilBERT at the EMC² workshop at NeurIPS 2019 and released it in the transformers library (Sanh et al., 2019). Other ways to shrink BERT include pruning attention heads and quantisation ([[model-compression|model compression]], [[quantisation|quantisation]]).

### When to use it

- Text classification, extraction or question answering where BERT-level quality is needed under tight latency, memory or cost limits (Sanh et al., 2019).
- On-device or edge inference (Sanh et al., 2019).
- As a baseline encoder before trying larger models ([[classification|classification]]).

### Strengths and limitations

**Strengths**
- 40% smaller and 60% faster than BERT-base while keeping 97% of GLUE performance (Sanh et al., 2019).
- General-purpose: fine-tuned like BERT for many tasks (Sanh et al., 2019).
- Much cheaper to pre-train than training a large model from scratch (Sanh et al., 2019).

**Limitations**
- A few points below BERT-base, more on some tasks such as [[natural-language-inference|RTE]] and SQuAD (Sanh et al., 2019).
- Pre-training still needs the teacher and substantial compute, about 90 hours on 8 V100 GPUs (Sanh et al., 2019).
- English only in the original release (Sanh et al., 2019 train on English Wikipedia and Toronto Books).

### Comparison

| Model | Parameters | GLUE (dev) | Inference time STS-B (CPU) |
|---|---|---|---|
| ELMo | 180 M | 68.7 | 895 s |
| [[bert\|BERT-base]] | 110 M | 79.5 | 668 s |
| DistilBERT | 66 M | 77.0 | 410 s |

Source: Sanh et al. (2019).

### In practice

DistilBERT fits steps that must run cheaply, for example classification or filtering before a larger model ([[llm-cost-optimisation|LLM cost optimisation]]). The gap to BERT varies by task, from about 0.6 points on IMDb to about 9 points on RTE, so quality should be checked on the target task (Sanh et al., 2019).

### Key takeaway

DistilBERT halves BERT's depth and learns from BERT during pre-training with a triple loss of soft targets, masked language modelling and hidden-state alignment, keeping 97% of its performance at 60% of its size and with 60% faster inference.

### Sources

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* EMC² Workshop at NeurIPS 2019. [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

DistilBERT ist eine kleinere Fassung von [[bert|BERT]], erzeugt durch [[knowledge-distillation|Knowledge Distillation]] während des Vortrainings: Ein Schülermodell mit 6 Schichten lernt vom Lehrermodell BERT-base mit 12 Schichten und behält 97 % seiner Leistung beim Sprachverstehen auf [[glue|GLUE]], bei 40 % weniger Parametern und 60 % schnellerer Inferenz (Sanh et al., 2019). Seine Zielfunktion verbindet drei Verluste: die weiche Ausgabeverteilung des Lehrers nachbilden, den üblichen Masked-Language-Modelling-Verlust und einen Cosine-Verlust, der die verborgenen Zustände des Schülers an die des Lehrers angleicht (Sanh et al., 2019). 2019 von Hugging Face veröffentlicht, ist es ein Allzweckmodell, das sich wie BERT feinjustieren lässt und klein genug für den Einsatz auf Endgeräten ist.

### Funktionsweise

```text
Lehrer: BERT-base (12 Schichten, 110 Mio. Parameter)
Schüler: gleiche Architektur mit 6 Schichten, ohne Token-Type-Embeddings, ohne Pooler (66 Mio. Parameter)
 ▼ Schüler aus dem Lehrer initialisieren: jede zweite Schicht übernehmen
 ▼ Vortraining auf englischer Wikipedia + Toronto Book Corpus mit
    L = L_ce (weiche Zielwerte des Lehrers, Temperatur T)
      + L_mlm (Masked Language Modelling)
      + L_cos (Cosine zwischen verborgenen Zuständen von Schüler und Lehrer)
 ▼ Fine-Tuning auf die Zielaufgabe wie bei BERT (optional mit zweitem Distillationsschritt)
```

#### 1. Distillation während des Vortrainings

Die meisten früheren Arbeiten destillierten BERT nach dem Fine-Tuning für eine bestimmte Aufgabe; DistilBERT wendet Knowledge Distillation stattdessen während des Vortrainings an und erzeugt so ein Allzweckmodell, das anschließend für viele Aufgaben feinjustiert werden kann (Sanh et al., 2019). Bei der Distillation wird ein kompakter Schüler darauf trainiert, das Verhalten eines größeren Lehrers nachzubilden; die vollständige Ausgabeverteilung des Lehrers, einschließlich der kleinen Wahrscheinlichkeiten falscher Klassen, trägt mehr Information als One-Hot-Labels (Sanh et al., 2019). Für ein maskiertes Token in „I think this is the beginning of a beautiful [MASK]“ vergibt BERT hohe Wahrscheinlichkeit an „day“ und „life“ und verteilt den Rest auf gültige Alternativen wie „future“ oder „story“.

#### 2. Der dreifache Verlust

Der Distillationsverlust `L_ce = Σ_i t_i · log(s_i)` vergleicht die Wahrscheinlichkeiten t des Lehrers mit denen s des Schülers, beide mit derselben Temperatur T im Softmax `p_i = exp(z_i/T) / Σ_j exp(z_j/T)` geglättet; bei der Inferenz ist T = 1 (Sanh et al., 2019). Er wird linear mit dem Masked-Language-Modelling-Verlust von BERT und einem Cosine-Embedding-Verlust kombiniert, der die Richtungen der verborgenen Zustandsvektoren von Schüler und Lehrer angleicht. In der Ablation trugen die beiden Distillationsverluste den größten Teil der Leistung, während das Weglassen des Masked-Language-Modelling-Verlusts wenig ausmachte (Sanh et al., 2019).

#### 3. Architektur und Initialisierung des Schülers

Der Schüler behält den allgemeinen Aufbau von BERT, halbiert aber die Zahl der Schichten und entfernt Token-Type-Embeddings und Pooler; die Autoren verringerten die Tiefe statt der Breite, weil Änderungen der verborgenen Dimension die Effizienz weniger beeinflussten als die Zahl der Schichten (Sanh et al., 2019). Weil Lehrer und Schüler dieselbe verborgene Dimension haben, wird der Schüler initialisiert, indem jede zweite Schicht des Lehrers übernommen wird; zufällige Initialisierung kostete in der Ablation 3,69 Punkte im GLUE-Makrowert (Sanh et al., 2019).

#### 4. Trainingsaufbau

Nach den Praktiken von RoBERTa wurde DistilBERT mit sehr großen Batches von bis zu 4.000 Beispielen per Gradientenakkumulation, dynamischer Maskierung und ohne Next-Sentence-Prediction trainiert, auf demselben Korpus wie BERT, englischer Wikipedia und dem Toronto Book Corpus (Sanh et al., 2019). Das Training dauerte etwa 90 Stunden auf 8 V100-GPUs mit je 16 GB.

#### 5. Ergebnisse

Auf den Dev-Sets von GLUE erreichte DistilBERT 77,0 gegenüber 79,5 für BERT-base und 68,7 für die ELMo-Baseline (Sanh et al., 2019). Bei der Sentimentklassifikation auf IMDb erreichte es 92,82 % Accuracy gegenüber 93,46 %, auf SQuAD 1.1 77,7/85,8 EM/F1 gegenüber 81,2/88,5, mit einem zweiten Distillationsschritt beim Fine-Tuning 79,1/86,9. Mit 66 statt 110 Millionen Parametern dauerte ein vollständiger Durchlauf über die STS-B-Aufgabe auf der CPU 410 statt 668 Sekunden; auf einem iPhone 7 Plus war ein Modell zur Fragebeantwortung 71 % schneller als eines auf Basis von BERT-base und wog 207 MB (Sanh et al., 2019).

#### Herkunft und Varianten

Victor Sanh, Lysandre Debut, Julien Chaumond und Thomas Wolf von Hugging Face stellten DistilBERT im EMC²-Workshop der NeurIPS 2019 vor und veröffentlichten es in der transformers-Bibliothek (Sanh et al., 2019). Weitere Wege, BERT zu verkleinern, sind das Entfernen von Attention-Köpfen und Quantisierung ([[model-compression|Modellkompression]], [[quantisation|Quantisierung]]).

### Wann einsetzen

- Textklassifikation, Extraktion oder Fragebeantwortung, wenn Qualität auf BERT-Niveau unter engen Grenzen für Latenz, Speicher oder Kosten nötig ist (Sanh et al., 2019).
- Inferenz auf Endgeräten oder am Netzrand (Sanh et al., 2019).
- Als Baseline-Encoder, bevor größere Modelle ausprobiert werden ([[classification|Klassifikation]]).

### Stärken und Grenzen

**Stärken**
- 40 % kleiner und 60 % schneller als BERT-base bei 97 % der GLUE-Leistung (Sanh et al., 2019).
- Allzweckmodell: wie BERT für viele Aufgaben feinjustierbar (Sanh et al., 2019).
- Deutlich günstiger vorzutrainieren als ein großes Modell von Grund auf (Sanh et al., 2019).

**Grenzen**
- Einige Punkte unter BERT-base, bei manchen Aufgaben wie [[natural-language-inference|RTE]] und SQuAD mehr (Sanh et al., 2019).
- Das Vortraining braucht weiterhin den Lehrer und erhebliche Rechenleistung, etwa 90 Stunden auf 8 V100-GPUs (Sanh et al., 2019).
- In der ursprünglichen Fassung nur Englisch (Sanh et al., 2019 trainieren auf englischer Wikipedia und Toronto Books).

### Vergleich

| Modell | Parameter | GLUE (Dev) | Inferenzzeit STS-B (CPU) |
|---|---|---|---|
| ELMo | 180 Mio. | 68,7 | 895 s |
| [[bert\|BERT-base]] | 110 Mio. | 79,5 | 668 s |
| DistilBERT | 66 Mio. | 77,0 | 410 s |

Quelle: Sanh et al. (2019).

### In der Praxis

DistilBERT passt zu Schritten, die günstig laufen müssen, etwa Klassifikation oder Filtern vor einem größeren Modell ([[llm-cost-optimisation|LLM-Kostenoptimierung]]). Der Abstand zu BERT schwankt je Aufgabe, von etwa 0,6 Punkten auf IMDb bis etwa 9 Punkten auf RTE, daher sollte die Qualität auf der Zielaufgabe geprüft werden (Sanh et al., 2019).

### Merksatz

DistilBERT halbiert die Tiefe von BERT und lernt während des Vortrainings mit einem dreifachen Verlust aus weichen Zielwerten, Masked Language Modelling und Angleichung der verborgenen Zustände von BERT; es behält 97 % der Leistung bei 60 % der Größe und 60 % schnellerer Inferenz.

### Quellen

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* EMC²-Workshop auf der NeurIPS 2019. [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)
