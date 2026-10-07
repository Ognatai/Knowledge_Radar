---
title_en: Natural Language Processing
title_de: Natural Language Processing
entity_type: Concept
sources:
- https://web.stanford.edu/~jurafsky/slp3/
- https://arxiv.org/abs/1301.3781
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/2005.14165
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Natural language processing (NLP) builds systems that analyse, understand and generate human language, for tasks such as part-of-speech tagging, named entity recognition, parsing, information extraction, question answering and machine translation (Jurafsky & Martin (SLP3)). Modern NLP represents text as tokens and learned vectors and models it with neural networks, today mostly Transformer-based pretrained language models that are fine-tuned or prompted for a task ([[large-language-models|Large Language Models]]).

### How it works

Text is first normalised and split into tokens. Tokens are mapped to learned vectors, a neural network (today usually a Transformer) computes context-dependent representations, and the model is either fine-tuned on labelled data for a task or, in the case of large language models, given the task and a few examples as text.

```text
1. Text normalisation and tokenization
▼
2. Word vectors
▼
3. Transformer architecture
▼
4. Pretraining and fine-tuning
▼
5. Few-shot learning with large language models
```

#### 1. Text normalisation and tokenization

Before any modelling, text is normalised and split into tokens, the units that later steps operate on (Jurafsky & Martin (SLP3)). Modern systems mostly use subword tokens, which keep the vocabulary small while still representing rare words ([[tokenization|Tokenization]]). On top of tokens, the field addresses tasks such as part-of-speech tagging, named entity recognition ([[entity-extraction|Entity Extraction]]), parsing, information extraction ([[information-extraction|Information Extraction]]), question answering and machine translation (Jurafsky & Martin (SLP3)).

#### 2. Word vectors

Mikolov et al. (2013) proposed two model architectures (word2vec) that learn continuous vector representations of words from very large data sets. The quality of the vectors was measured on word similarity tasks, where they gave large improvements in accuracy at much lower computational cost than earlier neural approaches: high-quality vectors could be learned from a 1.6 billion word data set in less than a day. Such vectors place words with similar meaning close together and are the starting point for [[embeddings|Embeddings]] in general.

#### 3. Transformer architecture

The Transformer (Vaswani et al., 2017) is a sequence model based solely on attention mechanisms, dispensing with recurrence and convolutions. This makes it more parallelizable and faster to train than the recurrent and convolutional models it replaced. On machine translation it reached 28.4 BLEU on WMT 2014 English-to-German, more than 2 BLEU above the previous best results including ensembles, and 41.8 BLEU on English-to-French as a single model after 3.5 days of training on eight GPUs. The Transformer is the basis of today's pretrained language models.

#### 4. Pretraining and fine-tuning

BERT (Devlin et al., 2018) pretrains deep bidirectional representations from unlabeled text by conditioning on both left and right context in all layers. The pretrained model is then fine-tuned with just one additional output layer, without substantial task-specific architecture changes. This gave new state-of-the-art results on eleven NLP tasks, among them a GLUE score of 80.5% (7.7 points absolute improvement) and SQuAD v1.1 question answering Test F1 of 93.2 (Devlin et al., 2018).

#### 5. Few-shot learning with large language models

GPT-3 (Brown et al., 2020) is an autoregressive language model with 175 billion parameters. Tasks and a few demonstrations are given purely as text, without any gradient updates or fine-tuning. Scaling up language models greatly improved such task-agnostic few-shot performance, sometimes reaching the level of earlier fine-tuned state-of-the-art approaches. The authors also identified datasets on which GPT-3's few-shot learning still struggles and datasets with methodological issues related to training on large web corpora (Brown et al., 2020). How to prompt such models is covered in [[prompt-engineering|Prompt Engineering]].

#### Origin and variants

Jurafsky & Martin (SLP3) give a textbook overview of both classical and neural methods. The neural line traced here runs from learned word vectors (Mikolov et al., 2013) to the Transformer (Vaswani et al., 2017), the pretrain-then-fine-tune approach of BERT (Devlin et al., 2018) and few-shot prompting of large models such as GPT-3 (Brown et al., 2020).

### When to use it

- When text has to be analysed or generated automatically at a scale that manual work cannot handle, for example in translation, extraction or question answering (Jurafsky & Martin (SLP3)).
- When labelled data for a task is available, a pretrained encoder fine-tuned with one additional output layer is a strong starting point (Devlin et al., 2018).
- When little or no labelled data exists, a large language model can be given the task and a few examples as text (Brown et al., 2020).

### Strengths and limitations

**Strengths**
- Learned word vectors capture word similarity and can be trained on billions of words in less than a day (Mikolov et al., 2013).
- One pretrained model can be adapted to many tasks with only an additional output layer (Devlin et al., 2018).
- Large language models can perform new tasks from a few examples without gradient updates (Brown et al., 2020).

**Limitations**
- Few-shot learning still struggles on some datasets (Brown et al., 2020).
- Training on large web corpora raises methodological issues for evaluation (Brown et al., 2020), and models can reproduce social biases from their training data ([[bias-in-nlp|Bias in NLP]]).
- Models with 175 billion parameters are expensive to train and run (Brown et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Word vectors | One static vector per word, learned from large corpora (Mikolov et al., 2013) | Word similarity and lightweight features |
| Pretrained encoder with fine-tuning | Bidirectional context, one additional output layer per task (Devlin et al., 2018) | Classification, labelling and extractive question answering with labelled data |
| Large autoregressive model with few-shot prompting | Task and examples given as text, no gradient updates (Brown et al., 2020) | Tasks with little labelled data and generation tasks |

### In practice

Tasks are evaluated with task-specific benchmarks and metrics, for example BLEU for translation (Vaswani et al., 2017; [[text-similarity-metrics|Text Similarity Metrics]]), GLUE and SQuAD for understanding and question answering (Devlin et al., 2018), and word similarity tests for word vectors (Mikolov et al., 2013). Because large models are trained on web data, benchmark results can be affected by overlap with the training data (Brown et al., 2020), so evaluation on held-out, task-specific data remains necessary ([[llm-evaluation|LLM Evaluation]]).

### Key takeaway

Modern NLP turns text into tokens and learned vectors and models it with Transformer-based pretrained models, which are adapted to a task either by fine-tuning or by prompting with a few examples.

### Sources

- Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd ed. draft). [online draft](https://web.stanford.edu/~jurafsky/slp3/)
- Mikolov, T. et al. (2013). *Efficient Estimation of Word Representations in Vector Space.* [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Natural Language Processing (NLP) entwickelt Systeme, die menschliche Sprache analysieren, verstehen und erzeugen, etwa für Wortartenerkennung (Part-of-Speech-Tagging), Named Entity Recognition, Parsing, Informationsextraktion, Fragebeantwortung und maschinelle Übersetzung (Jurafsky & Martin (SLP3)). Modernes NLP stellt Text als Token und gelernte Vektoren dar und modelliert ihn mit neuronalen Netzen, heute meist mit vortrainierten Sprachmodellen auf Transformer-Basis, die für eine Aufgabe feinabgestimmt oder gepromptet werden ([[large-language-models|Large Language Models]]).

### Funktionsweise

Der Text wird zunächst normalisiert und in Token aufgeteilt. Token werden auf gelernte Vektoren abgebildet, ein neuronales Netz (heute meist ein Transformer) berechnet kontextabhängige Repräsentationen, und das Modell wird entweder mit annotierten Daten für eine Aufgabe feinabgestimmt oder erhält, bei großen Sprachmodellen, die Aufgabe und einige Beispiele als Text.

```text
1. Textnormalisierung und Tokenisierung
▼
2. Wortvektoren
▼
3. Transformer-Architektur
▼
4. Vortraining und Fine-Tuning
▼
5. Few-Shot-Learning mit großen Sprachmodellen
```

#### 1. Textnormalisierung und Tokenisierung

Vor jeder Modellierung wird der Text normalisiert und in Token zerlegt, die Einheiten, mit denen die folgenden Schritte arbeiten (Jurafsky & Martin (SLP3)). Moderne Systeme verwenden meist Subword-Token, die das Vokabular klein halten und trotzdem seltene Wörter darstellen können ([[tokenization|Tokenisierung]]). Auf Basis der Token bearbeitet das Fachgebiet Aufgaben wie Wortartenerkennung, Named Entity Recognition ([[entity-extraction|Entitätsextraktion]]), Parsing, Informationsextraktion ([[information-extraction|Informationsextraktion]]), Fragebeantwortung und maschineller Übersetzung (Jurafsky & Martin (SLP3)).

#### 2. Wortvektoren

Mikolov et al. (2013) schlugen zwei Modellarchitekturen (word2vec) vor, die kontinuierliche Vektorrepräsentationen von Wörtern aus sehr großen Datensätzen lernen. Die Qualität der Vektoren wurde anhand von Aufgaben zur Wortähnlichkeit gemessen, bei denen sie die Genauigkeit gegenüber früheren neuronalen Ansätzen deutlich verbesserten, bei weit geringeren Rechenkosten: Hochwertige Vektoren konnten aus einem Datensatz mit 1,6 Milliarden Wörtern in weniger als einem Tag gelernt werden. Solche Vektoren platzieren Wörter mit ähnlicher Bedeutung nahe beieinander und sind der Ausgangspunkt für [[embeddings|Embeddings]] im Allgemeinen.

#### 3. Transformer-Architektur

Der Transformer (Vaswani et al., 2017) ist ein Sequenzmodell, das ausschließlich auf Attention-Mechanismen beruht und auf Rekurrenz und Faltungen verzichtet. Dadurch lässt er sich besser parallelisieren und schneller trainieren als die rekurrenten und konvolutionalen Modelle, die er ablöste. In der maschinellen Übersetzung erreichte er 28,4 BLEU auf WMT 2014 Englisch-Deutsch, mehr als 2 BLEU über den bisher besten Ergebnissen einschließlich Ensembles, und 41,8 BLEU bei Englisch-zu-Französisch als Einzelmodell nach 3,5 Tagen Training auf acht GPUs. Der Transformer bildet die Grundlage der heutigen vortrainierten Sprachmodelle.

#### 4. Vortraining und Fine-Tuning

BERT (Devlin et al., 2018) trainiert tiefe bidirektionale Repräsentationen auf nicht annotiertem Text vor, indem es in allen Schichten sowohl den linken als auch den rechten Kontext berücksichtigt. Das vortrainierte Modell wird dann mit nur einer zusätzlichen Ausgabeschicht feinabgestimmt, ohne wesentliche aufgabenspezifische Änderungen der Architektur. Das ergab neue Bestwerte bei elf NLP-Aufgaben, darunter einen GLUE-Score von 80,5 % (7,7 Punkte absolute Verbesserung) und einen Test-F1-Wert von 93,2 bei der Fragebeantwortung auf SQuAD v1.1 (Devlin et al., 2018).

#### 5. Few-Shot-Learning mit großen Sprachmodellen

GPT-3 (Brown et al., 2020) ist ein autoregressives Sprachmodell mit 175 Milliarden Parametern. Aufgaben und einige Demonstrationsbeispiele werden rein als Text übergeben, ohne Gradienten-Updates oder Fine-Tuning. Das Skalieren von Sprachmodellen verbesserte diese aufgabenunabhängige Few-Shot-Leistung erheblich und erreichte teils das Niveau früherer feinabgestimmter Spitzenansätze. Die Autoren fanden auch Datensätze, bei denen das Few-Shot-Learning von GPT-3 weiterhin Schwierigkeiten hat, sowie Datensätze mit methodischen Problemen, die mit dem Training auf großen Web-Korpora zusammenhängen (Brown et al., 2020). Wie man solche Modelle promptet, behandelt [[prompt-engineering|Prompt Engineering]].

#### Ursprung und Varianten

Jurafsky & Martin (SLP3) geben einen Lehrbuchüberblick über klassische und neuronale Methoden. Die hier nachgezeichnete neuronale Entwicklungslinie führt von gelernten Wortvektoren (Mikolov et al., 2013) über den Transformer (Vaswani et al., 2017) und das Vortrainieren mit anschließendem Fine-Tuning bei BERT (Devlin et al., 2018) zum Few-Shot-Prompting großer Modelle wie GPT-3 (Brown et al., 2020).

### Wann einsetzen

- Wenn Text automatisch in einem Umfang analysiert oder generiert werden muss, den manuelle Arbeit nicht bewältigen kann, beispielsweise bei Übersetzung, Extraktion oder bei Fragebeantwortung (Jurafsky & Martin (SLP3)).
- Wenn für eine Aufgabe annotierte Daten vorliegen, ist ein vortrainierter Encoder, der mit einer zusätzlichen Ausgabeschicht feinabgestimmt wird, ein starker Ausgangspunkt (Devlin et al., 2018).
- Wenn kaum oder keine annotierten Daten vorhanden sind, kann man einem großen Sprachmodell die Aufgabe und einige Beispiele als Text übergeben (Brown et al., 2020).

### Stärken und Grenzen

**Stärken**
- Gelernte Wortvektoren erfassen die Ähnlichkeit zwischen Wörtern und lassen sich in weniger als einem Tag auf Milliarden von Wörtern trainieren (Mikolov et al., 2013).
- Ein vortrainiertes Modell kann mit nur einer zusätzlichen Ausgabeschicht an viele Aufgaben angepasst werden (Devlin et al., 2018).
- Große Sprachmodelle können neue Aufgaben aus wenigen Beispielen ohne Gradientenupdates ausführen (Brown et al., 2020).

**Einschränkungen**
- Few-Shot-Learning hat auf einigen Datensätzen weiterhin Schwierigkeiten (Brown et al., 2020).
- Das Training auf großen Webkorpora wirft methodische Probleme für die Evaluierung auf (Brown et al., 2020), und Modelle können soziale Verzerrungen aus ihren Trainingsdaten reproduzieren ([[bias-in-nlp|Bias in NLP]]).
- Modelle mit 175 Milliarden Parametern sind teuer im Training und im Betrieb (Brown et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Wortvektoren | Ein statischer Vektor pro Wort, gelernt aus großen Korpora (Mikolov et al., 2013) | Wortähnlichkeit und einfache Merkmale |
| Vortrainierter Encoder mit Fine-Tuning | Bidirektionaler Kontext, eine zusätzliche Ausgabeschicht pro Aufgabe (Devlin et al., 2018) | Klassifikation, Sequenz-Labeling und extraktive Fragebeantwortung mit annotierten Daten |
| Großes autoregressives Modell mit Few-Shot-Prompting | Aufgabe und Beispiele als Text, keine Gradienten-Updates (Brown et al., 2020) | Aufgaben mit wenig annotierten Daten und Generierungsaufgaben |

### In der Praxis

Aufgaben werden mit aufgabenspezifischen Benchmarks und Metriken evaluiert, beispielsweise BLEU für die Übersetzung (Vaswani et al., 2017; [[text-similarity-metrics|Textähnlichkeitsmetriken]]), GLUE und SQuAD für das Verständnis und das Beantworten von Fragen (Devlin et al., 2018) sowie Wortähnlichkeitstests für Wortvektoren (Mikolov et al., 2013). Da große Modelle auf Webdaten trainiert werden, können Benchmark-Ergebnisse durch Überschneidungen mit den Trainingsdaten beeinflusst werden (Brown et al., 2020), weshalb eine Evaluation auf zurückgehaltenen, aufgabenspezifischen Daten weiterhin notwendig ist ([[llm-evaluation|LLM-Evaluation]]).

### Merksatz

Modernes NLP verwandelt Text in Token und gelernte Vektoren und modelliert ihn mit vortrainierten Transformer-Modellen, die entweder durch Fine-Tuning oder durch Prompting mit einigen Beispielen an eine Aufgabe angepasst werden.

### Quellen

- Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd ed. draft). [online draft](https://web.stanford.edu/~jurafsky/slp3/)
- Mikolov, T. et al. (2013). *Efficient Estimation of Word Representations in Vector Space.* [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
