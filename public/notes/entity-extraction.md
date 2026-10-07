---
title_en: Entity Extraction
title_de: Entitätsextraktion
entity_type: Method
sources:
- https://aclanthology.org/W03-0419/
- https://arxiv.org/abs/1603.01360
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/2311.08526
- https://arxiv.org/abs/2304.10428
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Entity extraction, also called named entity recognition (NER), finds the spans in a text that name entities such as persons, locations and organisations and assigns each span a type (Tjong Kim Sang & De Meulder, 2003). Approaches have moved from hand-crafted features to neural sequence labelling (Lample et al., 2016), fine-tuned pretrained encoders (Devlin et al., 2018) and, more recently, extraction of arbitrary entity types with compact encoders or large language models (Zaratiana et al., 2023; Wang et al., 2023). Extracted entities are the building blocks of [[information-extraction|Information Extraction]] and [[knowledge-graphs|Knowledge Graphs]].

### How it works

A model reads a text and marks each entity span together with its type. Classical systems label every token; newer systems can take the wanted entity types as input or generate the marked-up text.

```text
1. Task and evaluation
▼
2. Neural sequence labelling
▼
3. Fine-tuned pretrained encoders
▼
4. Arbitrary entity types with a compact encoder
▼
5. NER with large language models
```

#### 1. Task and evaluation

The CoNLL-2003 shared task (Tjong Kim Sang & De Meulder, 2003) defined NER for English and German with four entity types: persons, locations, organisations and miscellaneous names. Systems were evaluated with precision, recall and F1 on exact entity matches, so a prediction only counts if both the span and the type are correct. The data set became a standard NER benchmark.

#### 2. Neural sequence labelling

Earlier NER systems relied heavily on hand-crafted features and domain-specific knowledge. Lample et al. (2016) introduced two neural architectures: a bidirectional LSTM combined with a conditional random field (CRF), which labels each token while taking the neighbouring labels into account, and a transition-based model inspired by shift-reduce parsers that constructs and labels segments. Both use character-based word representations learned from the annotated corpus and word representations learned without supervision from unannotated text. They reached state-of-the-art performance in four languages without language-specific resources such as gazetteers (Lample et al., 2016).

#### 3. Fine-tuned pretrained encoders

BERT (Devlin et al., 2018) pretrains deep bidirectional representations on unlabeled text and is then fine-tuned with just one additional output layer, without substantial task-specific architecture changes. For NER this means that a classification layer on top of the pretrained encoder predicts an entity label for each token, and the whole model is trained on the annotated data. This pretrain-then-fine-tune pattern replaced task-specific architectures for many NLP tasks ([[natural-language-processing|Natural Language Processing]]).

#### 4. Arbitrary entity types with a compact encoder

Traditional NER models are limited to the entity types they were trained on. Large language models can extract arbitrary types from natural language instructions, but their size and cost make them impractical in resource-limited scenarios (Zaratiana et al., 2023). GLiNER is a compact NER model built on a bidirectional transformer encoder and trained to identify any type of entity. It extracts entities in parallel rather than by slow sequential token generation, and in zero-shot evaluations on various NER benchmarks it outperformed both ChatGPT and fine-tuned LLMs (Zaratiana et al., 2023).

#### 5. NER with large language models

Out of the box, large language models performed significantly below supervised baselines on NER, because NER is a sequence labelling task and LLMs generate text (Wang et al., 2023). GPT-NER bridges this gap by turning labelling into generation: to find location entities in "Columbus is a city", the model generates "@@Columbus## is a city", where the special tokens mark the entity. Against the tendency of LLMs to label inputs without entities over-confidently as entities, a self-verification step asks the model whether each extracted entity really belongs to the label. On five widely used NER datasets GPT-NER achieved performance comparable to fully supervised baselines, and with very little training data it performed significantly better than supervised models (Wang et al., 2023).

#### Origin and variants

CoNLL-2003 (Tjong Kim Sang & De Meulder, 2003) set a common benchmark. Neural architectures (Lample et al., 2016) removed the need for hand-crafted features, pretrained encoders (Devlin et al., 2018) made fine-tuning the standard approach, and GLiNER (Zaratiana et al., 2023) and GPT-NER (Wang et al., 2023) opened NER to arbitrary entity types and low-resource settings.

### When to use it

- When the entity types are fixed and annotated training data is available, a fine-tuned encoder or neural sequence labeller fits (Lample et al., 2016; Devlin et al., 2018).
- When new entity types must be recognised without retraining, a compact open-type model such as GLiNER is an option (Zaratiana et al., 2023).
- When labelled data is very scarce, LLM-based NER with self-verification can outperform supervised models (Wang et al., 2023).

### Strengths and limitations

**Strengths**
- Neural models reach state-of-the-art performance without hand-crafted features or gazetteers (Lample et al., 2016).
- Compact open-type models extract arbitrary entity types in parallel and outperformed ChatGPT in zero-shot evaluations (Zaratiana et al., 2023).
- LLM-based NER works with very little training data (Wang et al., 2023).

**Limitations**
- Classical models only recognise the entity types they were trained on (Zaratiana et al., 2023).
- Large language models are costly to run, especially via APIs, which makes them impractical in resource-limited scenarios (Zaratiana et al., 2023).
- LLMs tend to label inputs without entities over-confidently as entities and need extra verification (Wang et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Neural sequence labelling (BiLSTM-CRF) | Labels each token, learned from annotated data with character and word representations (Lample et al., 2016) | Fixed entity types with annotated data |
| Fine-tuned pretrained encoder | Pretrained bidirectional encoder plus one output layer (Devlin et al., 2018) | Fixed entity types with annotated data |
| Open-type compact encoder (GLiNER) | Entity types are given as input; extraction in parallel (Zaratiana et al., 2023) | New entity types, limited resources |
| LLM generation (GPT-NER) | Entities marked in generated text, plus self-verification (Wang et al., 2023) | Very little labelled data |

### In practice

Systems are evaluated with precision, recall and F1 on exact entity matches (Tjong Kim Sang & De Meulder, 2003), ideally on data from the target domain, since performance on a benchmark does not transfer automatically to specialised texts. When LLMs are used, a verification step against the label definitions reduces false positives (Wang et al., 2023). The entity types themselves should follow the domain model, for example an ontology ([[ontology-design|Ontology Design]]), so that extracted entities can be linked and stored consistently ([[knowledge-graphs|Knowledge Graphs]]).

### Key takeaway

Entity extraction finds and types the named entities in a text; fine-tuned encoders work well for fixed types, while open-type encoders and LLMs handle new types and very small amounts of training data.

### Sources

- Tjong Kim Sang, E. F. & De Meulder, F. (2003). *Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition.* CoNLL 2003. [ACL Anthology](https://aclanthology.org/W03-0419/)
- Lample, G. et al. (2016). *Neural Architectures for Named Entity Recognition.* NAACL 2016. [arXiv:1603.01360](https://arxiv.org/abs/1603.01360)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Zaratiana, U. et al. (2023). *GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer.* NAACL 2024. [arXiv:2311.08526](https://arxiv.org/abs/2311.08526)
- Wang, S. et al. (2023). *GPT-NER: Named Entity Recognition via Large Language Models.* [arXiv:2304.10428](https://arxiv.org/abs/2304.10428)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Entitätsextraktion, auch Named Entity Recognition (NER), findet die Textstellen, die Entitäten wie Personen, Orte und Organisationen benennen, und weist jeder Stelle einen Typ zu (Tjong Kim Sang & De Meulder, 2003). Die Ansätze entwickelten sich von handgefertigten Merkmalen über neuronales Sequenz-Labeling (Lample et al., 2016) und feinabgestimmte vortrainierte Encoder (Devlin et al., 2018) bis zur Extraktion beliebiger Entitätstypen mit kompakten Encodern oder großen Sprachmodellen (Zaratiana et al., 2023; Wang et al., 2023). Extrahierte Entitäten sind die Bausteine der [[information-extraction|Informationsextraktion]] und von [[knowledge-graphs|Wissensgraphen]].

### Funktionsweise

Ein Modell liest einen Text und markiert jede Entität mit ihrem Typ. Klassische Systeme vergeben für jedes Token ein Label; neuere Systeme erhalten die gesuchten Entitätstypen als Eingabe oder erzeugen den markierten Text.

```text
1. Aufgabe und Evaluation
▼
2. Neuronales Sequenz-Labeling
▼
3. Feinabgestimmte vortrainierte Encoder
▼
4. Beliebige Entitätstypen mit einem kompakten Encoder
▼
5. NER mit großen Sprachmodellen
```

#### 1. Aufgabe und Evaluation

Der Shared Task CoNLL-2003 (Tjong Kim Sang & De Meulder, 2003) definierte NER für Englisch und Deutsch mit vier Entitätstypen: Personen, Orte, Organisationen und sonstige Namen. Systeme wurden mit Precision, Recall und F1 auf exakten Entitätstreffern bewertet; eine Vorhersage zählt also nur, wenn Textspanne und Typ stimmen. Der Datensatz wurde zu einem Standard-Benchmark für NER.

#### 2. Neuronales Sequenz-Labeling

Frühere NER-Systeme stützten sich stark auf handgefertigte Merkmale und Domänenwissen. Lample et al. (2016) stellten zwei neuronale Architekturen vor: ein bidirektionales LSTM mit Conditional Random Field (CRF), das jedes Token unter Berücksichtigung der benachbarten Labels klassifiziert, und ein transitionsbasiertes Modell nach dem Vorbild von Shift-Reduce-Parsern, das Segmente bildet und labelt. Beide nutzen zeichenbasierte Wortrepräsentationen, die aus dem annotierten Korpus gelernt werden, sowie Wortrepräsentationen, die unüberwacht aus nicht annotiertem Text gelernt werden. Sie erreichten den Stand der Technik in vier Sprachen, ohne sprachspezifische Ressourcen wie Gazetteers (Lample et al., 2016).

#### 3. Feinabgestimmte vortrainierte Encoder

BERT (Devlin et al., 2018) trainiert tiefe bidirektionale Repräsentationen auf nicht annotiertem Text vor und wird dann mit nur einer zusätzlichen Ausgabeschicht feinabgestimmt, ohne wesentliche aufgabenspezifische Änderungen der Architektur. Für NER heißt das: Eine Klassifikationsschicht auf dem vortrainierten Encoder sagt für jedes Token ein Entitätslabel voraus, und das ganze Modell wird auf den annotierten Daten trainiert. Dieses Muster aus Vortraining und Fine-Tuning löste bei vielen NLP-Aufgaben aufgabenspezifische Architekturen ab ([[natural-language-processing|Natural Language Processing]]).

#### 4. Beliebige Entitätstypen mit einem kompakten Encoder

Klassische NER-Modelle sind auf die Entitätstypen beschränkt, mit denen sie trainiert wurden. Große Sprachmodelle können beliebige Typen anhand von Anweisungen in natürlicher Sprache extrahieren, sind aber wegen ihrer Größe und Kosten in ressourcenbeschränkten Szenarien unpraktisch (Zaratiana et al., 2023). GLiNER ist ein kompaktes NER-Modell auf Basis eines bidirektionalen Transformer-Encoders, das darauf trainiert ist, Entitäten beliebigen Typs zu erkennen. Es extrahiert Entitäten parallel statt durch langsame sequenzielle Token-Generierung und übertraf in Zero-Shot-Evaluationen auf verschiedenen NER-Benchmarks sowohl ChatGPT als auch feinabgestimmte LLMs (Zaratiana et al., 2023).

#### 5. NER mit großen Sprachmodellen

Ohne Anpassung lagen große Sprachmodelle bei NER deutlich unter überwachten Baselines, weil NER eine Sequenz-Labeling-Aufgabe ist und LLMs Text erzeugen (Wang et al., 2023). GPT-NER überbrückt diese Lücke, indem es das Labeling in Generierung umwandelt: Um Ortsentitäten in „Columbus is a city“ zu finden, erzeugt das Modell „@@Columbus## is a city“, wobei die Sondertoken die Entität markieren. Gegen die Neigung von LLMs, Eingaben ohne Entitäten übermäßig selbstsicher als Entitäten zu labeln, fragt ein Selbstverifikationsschritt das Modell, ob jede extrahierte Entität wirklich zum Label gehört. Auf fünf verbreiteten NER-Datensätzen erreichte GPT-NER eine mit vollständig überwachten Baselines vergleichbare Leistung und war bei sehr wenigen Trainingsdaten deutlich besser als überwachte Modelle (Wang et al., 2023).

#### Ursprung und Varianten

CoNLL-2003 (Tjong Kim Sang & De Meulder, 2003) schuf einen gemeinsamen Benchmark. Neuronale Architekturen (Lample et al., 2016) machten handgefertigte Merkmale überflüssig, vortrainierte Encoder (Devlin et al., 2018) machten Fine-Tuning zum Standard, und GLiNER (Zaratiana et al., 2023) sowie GPT-NER (Wang et al., 2023) öffneten NER für beliebige Entitätstypen und Szenarien mit wenigen Daten.

### Wann einsetzen

- Wenn die Entitätstypen feststehen und annotierte Trainingsdaten vorliegen, eignet sich ein feinabgestimmter Encoder oder ein neuronales Sequenz-Labeling-Modell (Lample et al., 2016; Devlin et al., 2018).
- Wenn neue Entitätstypen ohne erneutes Training erkannt werden sollen, ist ein kompaktes Modell für beliebige Typen wie GLiNER eine Option (Zaratiana et al., 2023).
- Wenn annotierte Daten sehr knapp sind, kann LLM-basierte NER mit Selbstverifikation überwachte Modelle übertreffen (Wang et al., 2023).

### Stärken und Grenzen

**Stärken**
- Neuronale Modelle erreichen den Stand der Technik ohne handgefertigte Merkmale oder Gazetteers (Lample et al., 2016).
- Kompakte Modelle für beliebige Typen extrahieren Entitäten parallel und übertrafen ChatGPT in Zero-Shot-Evaluationen (Zaratiana et al., 2023).
- LLM-basierte NER funktioniert mit sehr wenigen Trainingsdaten (Wang et al., 2023).

**Einschränkungen**
- Klassische Modelle erkennen nur die Entitätstypen, mit denen sie trainiert wurden (Zaratiana et al., 2023).
- Große Sprachmodelle sind im Betrieb teuer, besonders über APIs, und daher in ressourcenbeschränkten Szenarien unpraktisch (Zaratiana et al., 2023).
- LLMs neigen dazu, Eingaben ohne Entitäten übermäßig selbstsicher als Entitäten zu labeln, und brauchen eine zusätzliche Prüfung (Wang et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Neuronales Sequenz-Labeling (BiLSTM-CRF) | Label für jedes Token, gelernt aus annotierten Daten mit Zeichen- und Wortrepräsentationen (Lample et al., 2016) | Feste Entitätstypen mit annotierten Daten |
| Feinabgestimmter vortrainierter Encoder | Vortrainierter bidirektionaler Encoder plus eine Ausgabeschicht (Devlin et al., 2018) | Feste Entitätstypen mit annotierten Daten |
| Kompakter Encoder für beliebige Typen (GLiNER) | Entitätstypen als Eingabe, parallele Extraktion (Zaratiana et al., 2023) | Neue Entitätstypen, begrenzte Ressourcen |
| LLM-Generierung (GPT-NER) | Entitäten im erzeugten Text markiert, plus Selbstverifikation (Wang et al., 2023) | Sehr wenige annotierte Daten |

### In der Praxis

Systeme werden mit Precision, Recall und F1 auf exakten Entitätstreffern evaluiert (Tjong Kim Sang & De Meulder, 2003), idealerweise auf Daten aus der Zieldomäne, da sich Benchmark-Ergebnisse nicht automatisch auf Fachtexte übertragen. Beim Einsatz von LLMs verringert ein Prüfschritt gegen die Label-Definitionen falsch positive Treffer (Wang et al., 2023). Die Entitätstypen selbst sollten dem Domänenmodell folgen, etwa einer Ontologie ([[ontology-design|Ontologie-Design]]), damit extrahierte Entitäten konsistent verknüpft und gespeichert werden können ([[knowledge-graphs|Wissensgraphen]]).

### Merksatz

Entitätsextraktion findet und typisiert die benannten Entitäten in einem Text; feinabgestimmte Encoder eignen sich für feste Typen, Encoder für beliebige Typen und LLMs für neue Typen und sehr wenige Trainingsdaten.

### Quellen

- Tjong Kim Sang, E. F. & De Meulder, F. (2003). *Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition.* CoNLL 2003. [ACL Anthology](https://aclanthology.org/W03-0419/)
- Lample, G. et al. (2016). *Neural Architectures for Named Entity Recognition.* NAACL 2016. [arXiv:1603.01360](https://arxiv.org/abs/1603.01360)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Zaratiana, U. et al. (2023). *GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer.* NAACL 2024. [arXiv:2311.08526](https://arxiv.org/abs/2311.08526)
- Wang, S. et al. (2023). *GPT-NER: Named Entity Recognition via Large Language Models.* [arXiv:2304.10428](https://arxiv.org/abs/2304.10428)
