---
title_en: Knowledge Distillation
title_de: Knowledge Distillation
entity_type: Method
sources:
- https://arxiv.org/abs/1503.02531
- https://arxiv.org/abs/1412.6550
- https://arxiv.org/abs/1910.01108
- https://arxiv.org/abs/1909.10351
- https://arxiv.org/abs/2006.05525
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Knowledge distillation trains a small student model to imitate a large teacher model or an ensemble, so that much of the teacher's performance becomes available at a fraction of the cost (Hinton et al., 2015). The student learns from the teacher's soft output probabilities, which carry more information than hard labels, and can also learn from intermediate representations (Romero et al., 2014). DistilBERT kept 97% of BERT's language understanding with 40% fewer parameters (Sanh et al., 2019), and TinyBERT reached over 96.8% of BERT-base with a model 7.5 times smaller (Jiao et al., 2019).

### How it works

The teacher is trained first. The student is then trained on the same or additional data with a loss that combines the true labels with the teacher's predictions, softened with a temperature so that the relative probabilities of wrong classes become visible; optionally, the student also matches the teacher's hidden representations.

```text
1. Compressing an ensemble or large model
▼
2. Soft targets and temperature
▼
3. Learning from intermediate representations
▼
4. Distilling pretrained language models
▼
5. Kinds of knowledge and schemes
```

#### 1. Compressing an ensemble or large model

Averaging the predictions of many models improves accuracy, but such an ensemble is cumbersome and may be too expensive to deploy to many users (Hinton et al., 2015). Building on earlier work showing that an ensemble's knowledge can be compressed into a single model, Hinton et al. distilled ensembles into single models, with surprising results on MNIST and a significant improvement of a heavily used commercial acoustic model.

#### 2. Soft targets and temperature

Hard labels say only which class is correct. The teacher's full output distribution also shows which wrong classes it considers similar, and this "dark knowledge" helps the student generalise (Hinton et al., 2015). Dividing the logits by a temperature above 1 before the softmax softens the distribution and makes these small probabilities visible. The student is trained on a weighted combination of the loss against these soft targets, computed at the same temperature, and the usual loss against the true labels.

#### 3. Learning from intermediate representations

FitNets extend distillation so that a student can be deeper and thinner than its teacher: besides the outputs, the student uses the teacher's intermediate representations as hints, with additional parameters mapping the student's smaller hidden layer to the teacher's (Romero et al., 2014). On CIFAR-10, a deep student with about 10.4 times fewer parameters outperformed a larger state-of-the-art teacher.

#### 4. Distilling pretrained language models

DistilBERT applies distillation during pretraining rather than for one task, with a triple loss combining language modelling, distillation and cosine-distance losses; it reduced BERT's size by 40% while retaining 97% of its language understanding and running 60% faster (Sanh et al., 2019). TinyBERT designs a distillation method for Transformer layers and applies it in both pretraining and task-specific fine-tuning; with 4 layers it reached more than 96.8% of BERT-base's performance on GLUE while being 7.5 times smaller and 9.4 times faster at inference (Jiao et al., 2019; [[large-language-models|Large Language Models]]).

#### 5. Kinds of knowledge and schemes

Knowledge distillation has become a representative technique of model compression and acceleration for deploying deep models on devices with limited resources (Gou et al., 2020). The survey organises the field by the kind of knowledge transferred, the distillation scheme and the teacher-student architecture.

#### Origin and variants

Distillation of ensembles and large networks with soft targets (Hinton et al., 2015) was extended to intermediate hints (Romero et al., 2014) and to pretrained language models with DistilBERT (Sanh et al., 2019) and TinyBERT (Jiao et al., 2019); Gou et al. (2020) survey the field.

### When to use it

- When a large model or ensemble is too expensive to deploy, a distilled student reduces cost and latency (Hinton et al., 2015).
- When a language model must run on devices or with tight inference budgets (Sanh et al., 2019; Jiao et al., 2019).
- When combined with quantization for further compression ([[quantization|Quantization]]).

### Strengths and limitations

**Strengths**
- Transfers most of a large model's or ensemble's performance into a much smaller model (Hinton et al., 2015).
- Distilled language models keep most of BERT's performance at a fraction of the size and latency (Sanh et al., 2019; Jiao et al., 2019).
- Hints allow students that are deeper and thinner than the teacher (Romero et al., 2014).

**Limitations**
- A trained teacher is required, which must first be built (Hinton et al., 2015).
- Students typically retain most but not all of the teacher's performance (Sanh et al., 2019).
- Hint-based methods need extra parameters to match differently sized layers (Romero et al., 2014).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Response-based distillation | Student matches the teacher's soft outputs (Hinton et al., 2015) | General model compression |
| Hint-based distillation (FitNets) | Student also matches intermediate representations (Romero et al., 2014) | Deep, thin students |
| Pretraining distillation (DistilBERT) | Distillation during general pretraining (Sanh et al., 2019) | Small general-purpose language models |
| Two-stage Transformer distillation (TinyBERT) | Layer-wise distillation in pretraining and fine-tuning (Jiao et al., 2019) | Task-specific compact language models |

### In practice

The student is evaluated against the teacher on the target task, and the temperature and the weighting of the soft and hard losses are tuned on validation data (Hinton et al., 2015). Distillation is one of several options for adapting and shrinking language models, alongside quantization and parameter-efficient fine-tuning ([[llm-adaptation|LLM Adaptation]]).

### Key takeaway

Knowledge distillation trains a small student on a large teacher's soft predictions, keeping most of the performance at a fraction of the cost.

### Sources

- Hinton, G. et al. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Romero, A. et al. (2014). *FitNets: Hints for Thin Deep Nets.* ICLR 2015. [arXiv:1412.6550](https://arxiv.org/abs/1412.6550)
- Sanh, V. et al. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)
- Jiao, X. et al. (2019). *TinyBERT: Distilling BERT for Natural Language Understanding.* Findings of EMNLP 2020. [arXiv:1909.10351](https://arxiv.org/abs/1909.10351)
- Gou, J. et al. (2020). *Knowledge Distillation: A Survey.* IJCV 2021. [arXiv:2006.05525](https://arxiv.org/abs/2006.05525)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Knowledge Distillation trainiert ein kleines Schülermodell darauf, ein großes Lehrermodell oder ein Ensemble nachzuahmen, sodass ein Großteil der Leistung des Lehrers zu einem Bruchteil der Kosten verfügbar wird (Hinton et al., 2015). Der Schüler lernt aus den weichen Ausgabewahrscheinlichkeiten des Lehrers, die mehr Information tragen als harte Labels, und kann zusätzlich aus Zwischenrepräsentationen lernen (Romero et al., 2014). DistilBERT behielt 97 % des Sprachverständnisses von BERT bei 40 % weniger Parametern (Sanh et al., 2019), und TinyBERT erreichte mehr als 96,8 % von BERT-base mit einem 7,5-mal kleineren Modell (Jiao et al., 2019).

### Funktionsweise

Zuerst wird der Lehrer trainiert. Danach wird der Schüler auf denselben oder zusätzlichen Daten mit einer Verlustfunktion trainiert, die die echten Labels mit den Vorhersagen des Lehrers verbindet; diese werden mit einer Temperatur geglättet, damit die relativen Wahrscheinlichkeiten falscher Klassen sichtbar werden. Optional bildet der Schüler auch die verborgenen Repräsentationen des Lehrers nach.

```text
1. Ensemble oder großes Modell komprimieren
▼
2. Soft Targets und Temperatur
▼
3. Lernen aus Zwischenrepräsentationen
▼
4. Destillation vortrainierter Sprachmodelle
▼
5. Arten von Wissen und Verfahren
```

#### 1. Ensemble oder großes Modell komprimieren

Die Vorhersagen vieler Modelle zu mitteln verbessert die Genauigkeit, doch ein solches Ensemble ist schwerfällig und für den Einsatz bei vielen Nutzenden womöglich zu teuer (Hinton et al., 2015). Aufbauend auf früheren Arbeiten, die zeigten, dass sich das Wissen eines Ensembles in ein einzelnes Modell komprimieren lässt, destillierten Hinton et al. Ensembles in Einzelmodelle, mit überraschenden Ergebnissen auf MNIST und einer deutlichen Verbesserung eines viel genutzten kommerziellen akustischen Modells.

#### 2. Soft Targets und Temperatur

Harte Labels sagen nur, welche Klasse richtig ist. Die vollständige Ausgabeverteilung des Lehrers zeigt zusätzlich, welche falschen Klassen er für ähnlich hält, und dieses „dunkle Wissen“ hilft dem Schüler zu generalisieren (Hinton et al., 2015). Werden die Logits vor der Softmax durch eine Temperatur größer als 1 geteilt, wird die Verteilung geglättet, und diese kleinen Wahrscheinlichkeiten werden sichtbar. Der Schüler wird auf einer gewichteten Kombination aus dem Verlust gegenüber diesen Soft Targets, berechnet bei derselben Temperatur, und dem üblichen Verlust gegenüber den echten Labels trainiert.

#### 3. Lernen aus Zwischenrepräsentationen

FitNets erweitern die Destillation so, dass ein Schüler tiefer und schmaler sein kann als sein Lehrer: Neben den Ausgaben nutzt der Schüler die Zwischenrepräsentationen des Lehrers als Hinweise (Hints), wobei zusätzliche Parameter die kleinere verborgene Schicht des Schülers auf die des Lehrers abbilden (Romero et al., 2014). Auf CIFAR-10 übertraf ein tiefer Schüler mit etwa 10,4-mal weniger Parametern einen größeren Lehrer auf dem damaligen Stand der Technik.

#### 4. Destillation vortrainierter Sprachmodelle

DistilBERT wendet die Destillation im Vortraining statt für eine einzelne Aufgabe an, mit einem dreiteiligen Verlust aus Sprachmodellierung, Destillation und Kosinusabstand; es verkleinerte BERT um 40 %, behielt 97 % seines Sprachverständnisses und war 60 % schneller (Sanh et al., 2019). TinyBERT entwickelt ein Destillationsverfahren für Transformer-Schichten und wendet es im Vortraining und im aufgabenspezifischen Fine-Tuning an; mit 4 Schichten erreichte es mehr als 96,8 % der Leistung von BERT-base auf GLUE, war 7,5-mal kleiner und bei der Inferenz 9,4-mal schneller (Jiao et al., 2019; [[large-language-models|Large Language Models]]).

#### 5. Arten von Wissen und Verfahren

Knowledge Distillation ist zu einer typischen Technik der Modellkompression und -beschleunigung geworden, um tiefe Modelle auf Geräten mit begrenzten Ressourcen einzusetzen (Gou et al., 2020). Die Übersichtsarbeit ordnet das Gebiet nach der Art des übertragenen Wissens, dem Destillationsverfahren und der Lehrer-Schüler-Architektur.

#### Ursprung und Varianten

Die Destillation von Ensembles und großen Netzen mit Soft Targets (Hinton et al., 2015) wurde auf Zwischenhinweise (Romero et al., 2014) und mit DistilBERT (Sanh et al., 2019) und TinyBERT (Jiao et al., 2019) auf vortrainierte Sprachmodelle erweitert; Gou et al. (2020) geben einen Überblick über das Gebiet.

### Wann einsetzen

- Wenn ein großes Modell oder Ensemble im Einsatz zu teuer ist, senkt ein destillierter Schüler Kosten und Latenz (Hinton et al., 2015).
- Wenn ein Sprachmodell auf Geräten oder mit knappem Inferenzbudget laufen muss (Sanh et al., 2019; Jiao et al., 2019).
- In Kombination mit Quantisierung für weitere Kompression ([[quantization|Quantisierung]]).

### Stärken und Grenzen

**Stärken**
- Überträgt den Großteil der Leistung eines großen Modells oder Ensembles in ein viel kleineres Modell (Hinton et al., 2015).
- Destillierte Sprachmodelle behalten den Großteil der Leistung von BERT bei einem Bruchteil von Größe und Latenz (Sanh et al., 2019; Jiao et al., 2019).
- Hints ermöglichen Schüler, die tiefer und schmaler als der Lehrer sind (Romero et al., 2014).

**Einschränkungen**
- Ein trainierter Lehrer ist nötig und muss erst gebaut werden (Hinton et al., 2015).
- Schüler behalten meist den Großteil, aber nicht die gesamte Leistung des Lehrers (Sanh et al., 2019).
- Hint-basierte Verfahren brauchen zusätzliche Parameter, um unterschiedlich große Schichten anzugleichen (Romero et al., 2014).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Ausgabebasierte Destillation | Schüler bildet die weichen Ausgaben des Lehrers nach (Hinton et al., 2015) | Allgemeine Modellkompression |
| Hint-basierte Destillation (FitNets) | Schüler bildet zusätzlich Zwischenrepräsentationen nach (Romero et al., 2014) | Tiefe, schmale Schüler |
| Destillation im Vortraining (DistilBERT) | Destillation während des allgemeinen Vortrainings (Sanh et al., 2019) | Kleine Allzweck-Sprachmodelle |
| Zweistufige Transformer-Destillation (TinyBERT) | Schichtweise Destillation in Vortraining und Fine-Tuning (Jiao et al., 2019) | Kompakte aufgabenspezifische Sprachmodelle |

### In der Praxis

Der Schüler wird auf der Zielaufgabe gegen den Lehrer evaluiert, und Temperatur sowie Gewichtung von weichem und hartem Verlust werden auf Validierungsdaten abgestimmt (Hinton et al., 2015). Destillation ist eine von mehreren Möglichkeiten, Sprachmodelle anzupassen und zu verkleinern, neben Quantisierung und parametereffizientem Fine-Tuning ([[llm-adaptation|LLM-Anpassung]]).

### Merksatz

Knowledge Distillation trainiert einen kleinen Schüler auf den weichen Vorhersagen eines großen Lehrers und erhält so den Großteil der Leistung zu einem Bruchteil der Kosten.

### Quellen

- Hinton, G. et al. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Romero, A. et al. (2014). *FitNets: Hints for Thin Deep Nets.* ICLR 2015. [arXiv:1412.6550](https://arxiv.org/abs/1412.6550)
- Sanh, V. et al. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)
- Jiao, X. et al. (2019). *TinyBERT: Distilling BERT for Natural Language Understanding.* Findings of EMNLP 2020. [arXiv:1909.10351](https://arxiv.org/abs/1909.10351)
- Gou, J. et al. (2020). *Knowledge Distillation: A Survey.* IJCV 2021. [arXiv:2006.05525](https://arxiv.org/abs/2006.05525)
