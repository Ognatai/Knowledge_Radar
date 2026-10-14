---
title_en: BERT
title_de: BERT
entity_type: Method
aliases:
- Bidirectional Encoder Representations from Transformers
sources:
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/1706.03762
- https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/1910.01108
- https://arxiv.org/abs/1909.10351
- https://arxiv.org/abs/1901.04085
- https://arxiv.org/abs/2004.04906
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
BERT (Bidirectional Encoder Representations from Transformers) is a language model built from the encoder of the [[attention-and-transformers|Transformer]]. It is pre-trained on unlabelled text by predicting masked tokens from their left and right context, and then fine-tuned for a task with one additional output layer (Devlin et al., 2018). BERT set new results on eleven NLP tasks and became the standard starting point for [[classification|classification]], extraction and, through variants such as [[sentence-bert|Sentence-BERT]], for embeddings in search (Devlin et al., 2018; Reimers & Gurevych, 2019).

### How it works

BERT reads the whole input at once: every token attends to all other tokens, before and after it. The output is one vector per token plus a vector for the special [CLS] token at the start, which summarises the sequence.

```text
[CLS] the cat [MASK] on the mat [SEP] it was tired [SEP]
  │      │          │                                       token + segment + position embeddings
  ▼      ▼          ▼
 ┌────────────────────────────────────────────────┐
 │  Transformer encoder (bidirectional, L layers) │
 └────────────────────────────────────────────────┘
  │                 │
  C ─▶ is B the next sentence?      T₃ ─▶ masked token = "sat"
```

#### 1. Input representation
Text is split into WordPiece tokens with a 30,000-token vocabulary ([[tokenisation|Tokenisation]]). Every sequence starts with [CLS]; a pair of sentences is separated by [SEP], and a learned segment embedding marks whether a token belongs to sentence A or B. The input of each token is the sum of its token, segment and position embeddings (Devlin et al., 2018).

#### 2. Pre-training
BERT is pre-trained on BooksCorpus (800M words) and English Wikipedia (2,500M words) with two tasks (Devlin et al., 2018):
- **Masked language modelling (MLM):** 15% of the tokens are chosen for prediction; a chosen token is replaced by [MASK] 80% of the time, by a random token 10% of the time, and left unchanged 10% of the time. Mixing in random and unchanged tokens reduces the mismatch that [MASK] never appears during fine-tuning.
- **Next sentence prediction (NSP):** for sentences A and B, B is the actual next sentence half of the time and a random sentence otherwise; the model predicts which from the [CLS] vector. Removing NSP hurt performance on question answering and inference tasks in the authors' ablation.

#### 3. Fine-tuning
For a task, one output layer is added and all parameters are trained on labelled data: the [CLS] vector feeds classification (e.g. entailment, sentiment), the token vectors feed token-level tasks such as sequence tagging ([[entity-extraction|Entity Extraction]]) or the start and end of an answer span in question answering (Devlin et al., 2018).

#### 4. Model sizes
BERT-Base has 12 layers, hidden size 768 and 12 attention heads (110M parameters); it was chosen to match the size of [[gpt|GPT]]-1 for comparison. BERT-Large has 24 layers, hidden size 1,024 and 16 heads (340M parameters) (Devlin et al., 2018).

#### Origin and variants
BERT (Devlin et al., 2018) followed GPT-1 (Radford et al., 2018), which pre-trained a left-to-right Transformer decoder; BERT's masked objective allowed a deeply bidirectional model. Variants adapt it for other uses:
- **Sentence-BERT** fine-tunes BERT in a siamese network so that each sentence gets its own embedding that can be compared with cosine similarity (Reimers & Gurevych, 2019); see [[embeddings|Embeddings]].
- **BERT as re-ranker:** query and passage are fed in together, and the [CLS] vector scores relevance (Nogueira & Cho, 2019); see [[cross-encoder|Cross-encoder]].
- **[[dense-passage-retrieval|Dense Passage Retrieval]]** uses two independent BERT encoders for questions and passages (Karpukhin et al., 2020); see [[semantic-retrieval|Semantic Retrieval]].
- **[[distilbert|DistilBERT]]** and **TinyBERT** are smaller BERT models trained by [[knowledge-distillation|knowledge distillation]] (Sanh et al., 2019; Jiao et al., 2019).

### When to use it
- Text classification, such as sentiment or topic, and sentence-pair tasks such as entailment (Devlin et al., 2018).
- Token-level tasks: named entity recognition and extractive question answering (Devlin et al., 2018).
- As the encoder behind sentence embeddings, dense retrieval and re-ranking in search and [[retrieval-augmented-generation|retrieval-augmented generation]] (Reimers & Gurevych, 2019; Karpukhin et al., 2020; Nogueira & Cho, 2019).
- When a model must be fine-tuned and run at moderate cost: BERT-Base has 110M parameters (Devlin et al., 2018).

### Strengths and limitations

**Strengths**
- Each token representation uses context from both sides in all layers (Devlin et al., 2018).
- One pre-trained model serves many tasks with only one task-specific output layer (Devlin et al., 2018).
- Distilled versions keep most of the quality at a fraction of the cost: DistilBERT is 40% smaller and 60% faster while retaining 97% of BERT's language understanding (Sanh et al., 2019); TinyBERT with 4 layers reaches over 96.8% of BERT-Base on GLUE, being 7.5x smaller and 9.4x faster (Jiao et al., 2019).

**Limitations**
- BERT does not generate text; for generation, decoder models such as [[gpt|GPT]] are used.
- The [MASK] token appears in pre-training but not in fine-tuning, a mismatch the 80/10/10 rule only reduces (Devlin et al., 2018).
- The [CLS] output or the average of BERT's token vectors gives poor sentence embeddings, often worse than averaged [[glove|GloVe]] vectors (Reimers & Gurevych, 2019).
- Comparing sentence pairs by feeding both into BERT is slow: finding the most similar pair among 10,000 sentences takes about 50 million inference computations, roughly 65 hours on a V100 GPU (Reimers & Gurevych, 2019).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| BERT (encoder-only) | Bidirectional context, masked language modelling, fine-tuned per task (Devlin et al., 2018) | Classification, tagging, extractive QA |
| [[gpt\|GPT]] (decoder-only) | Left-to-right context, next-token prediction; generates text (Radford et al., 2018) | Generation and prompting |
| Sentence-BERT (bi-encoder) | Embeds each sentence separately, compared by cosine similarity; about 5 seconds instead of 65 hours for the 10,000-sentence example (Reimers & Gurevych, 2019) | Semantic search, clustering |
| BERT re-ranker ([[cross-encoder\|cross-encoder]]) | Reads query and passage together; more accurate, but one model pass per pair (Nogueira & Cho, 2019) | Re-ranking a short candidate list |

### In practice
BERT is rarely trained from scratch: a pre-trained checkpoint is fine-tuned for the task, which needs only one additional output layer (Devlin et al., 2018); where inference cost matters, distilled models such as DistilBERT are an option (Sanh et al., 2019). For search, the choice is between embedding texts separately ([[semantic-retrieval|Semantic Retrieval]], [[vector-databases|Vector Databases]]) and scoring query and text together ([[cross-encoder|Cross-encoder]]); retrieval pipelines often combine both ([[rag-retrieval|RAG: Retrieval]]). Similarity of BERT embeddings is evaluated with [[text-similarity-metrics|text similarity metrics]], and representations learned from web and book text can carry social biases ([[bias-in-nlp|Bias in NLP]]).

### Key takeaway
BERT learns to understand text by filling in masked words from both sides; it is the encoder counterpart to GPT and the base of most models that classify, extract or embed text.

### Sources
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Radford, A., Narasimhan, K., Salimans, T. & Sutskever, I. (2018). *Improving Language Understanding by Generative Pre-Training.* OpenAI. [PDF](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Sanh, V. et al. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)
- Jiao, X. et al. (2019). *TinyBERT: Distilling BERT for Natural Language Understanding.* Findings of EMNLP 2020. [arXiv:1909.10351](https://arxiv.org/abs/1909.10351)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
BERT (Bidirectional Encoder Representations from Transformers) ist ein Sprachmodell, das auf dem Encoder des [[attention-and-transformers|Transformers]] aufbaut. Es wird auf ungelabeltem Text vortrainiert, indem es maskierte Tokens aus ihrem linken und rechten Kontext vorhersagt, und dann mit einer zusätzlichen Ausgabeschicht für eine Aufgabe feinjustiert (Devlin et al., 2018). BERT erzielte neue Bestwerte in elf NLP-Aufgaben und wurde zum üblichen Ausgangspunkt für [[classification|Klassifikation]], Extraktion und, über Varianten wie [[sentence-bert|Sentence-BERT]], für Embeddings in der Suche (Devlin et al., 2018; Reimers & Gurevych, 2019).

### Funktionsweise

BERT liest die ganze Eingabe auf einmal: Jedes Token richtet Attention auf alle anderen Tokens davor und danach. Ausgegeben wird ein Vektor pro Token und ein Vektor für das Sondertoken [CLS] am Anfang, das die Sequenz zusammenfasst.

```text
[CLS] the cat [MASK] on the mat [SEP] it was tired [SEP]
  │      │          │                                       Token- + Segment- + Positions-Embeddings
  ▼      ▼          ▼
 ┌───────────────────────────────────────────────────┐
 │  Transformer-Encoder (bidirektional, L Schichten) │
 └───────────────────────────────────────────────────┘
  │                 │
  C ─▶ ist B der Folgesatz?      T₃ ─▶ maskiertes Token = "sat"
```

#### 1. Eingaberepräsentation
Text wird in WordPiece-Tokens mit einem Vokabular von 30.000 Tokens zerlegt ([[tokenisation|Tokenisierung]]). Jede Sequenz beginnt mit [CLS]; ein Satzpaar wird durch [SEP] getrennt, und ein gelerntes Segment-Embedding markiert, ob ein Token zu Satz A oder B gehört. Die Eingabe jedes Tokens ist die Summe aus Token-, Segment- und Positions-Embedding (Devlin et al., 2018).

#### 2. Vortraining
BERT wird auf BooksCorpus (800 Mio. Wörter) und der englischen Wikipedia (2.500 Mio. Wörter) mit zwei Aufgaben vortrainiert (Devlin et al., 2018):
- **Masked Language Modelling (MLM):** 15 % der Tokens werden zur Vorhersage ausgewählt; ein ausgewähltes Token wird in 80 % der Fälle durch [MASK] ersetzt, in 10 % durch ein zufälliges Token und in 10 % unverändert gelassen. Die Beimischung zufälliger und unveränderter Tokens verringert die Diskrepanz, dass [MASK] beim Fine-Tuning nie vorkommt.
- **Next Sentence Prediction (NSP):** Bei den Sätzen A und B ist B in der Hälfte der Fälle der tatsächliche Folgesatz, sonst ein zufälliger Satz; das Modell sagt aus dem [CLS]-Vektor vorher, welcher Fall vorliegt. In der Ablationsstudie der Autoren verschlechterte das Weglassen von NSP die Leistung bei Frage-Antwort- und Inferenzaufgaben.

#### 3. Fine-Tuning
Für eine Aufgabe wird eine Ausgabeschicht ergänzt, und alle Parameter werden auf gelabelten Daten trainiert: Der [CLS]-Vektor speist die Klassifikation (z. B. Entailment, Sentiment), die Token-Vektoren speisen Aufgaben auf Token-Ebene wie Sequence Tagging ([[entity-extraction|Entitätsextraktion]]) oder Anfang und Ende einer Antwortspanne beim Question Answering (Devlin et al., 2018).

#### 4. Modellgrößen
BERT-Base hat 12 Schichten, Hidden Size 768 und 12 Attention-Heads (110 Mio. Parameter); es wurde so gewählt, dass es für den Vergleich gleich groß wie [[gpt|GPT]]-1 ist. BERT-Large hat 24 Schichten, Hidden Size 1.024 und 16 Heads (340 Mio. Parameter) (Devlin et al., 2018).

#### Ursprung und Varianten
BERT (Devlin et al., 2018) folgte auf GPT-1 (Radford et al., 2018), das einen Transformer-Decoder von links nach rechts vortrainierte; das maskierte Trainingsziel ermöglichte BERT ein tief bidirektionales Modell. Varianten passen es an andere Zwecke an:
- **Sentence-BERT** justiert BERT in einem siamesischen Netz so nach, dass jeder Satz ein eigenes Embedding erhält, das sich per Kosinus-Ähnlichkeit vergleichen lässt (Reimers & Gurevych, 2019); siehe [[embeddings|Embeddings]].
- **BERT als Re-Ranker:** Anfrage und Passage werden gemeinsam eingegeben, und der [CLS]-Vektor bewertet die Relevanz (Nogueira & Cho, 2019); siehe [[cross-encoder|Cross-Encoder]].
- **[[dense-passage-retrieval|Dense Passage Retrieval]]** verwendet zwei unabhängige BERT-Encoder für Fragen und Passagen (Karpukhin et al., 2020); siehe [[semantic-retrieval|Semantisches Retrieval]].
- **[[distilbert|DistilBERT]]** und **TinyBERT** sind kleinere BERT-Modelle, die per [[knowledge-distillation|Knowledge Distillation]] trainiert wurden (Sanh et al., 2019; Jiao et al., 2019).

### Wann einsetzen
- Textklassifikation, etwa Sentiment oder Thema, und Aufgaben mit Satzpaaren wie Entailment (Devlin et al., 2018).
- Aufgaben auf Token-Ebene: Named Entity Recognition und extraktives Question Answering (Devlin et al., 2018).
- Als Encoder hinter Satz-Embeddings, Dense Retrieval und Re-Ranking in der Suche und bei [[retrieval-augmented-generation|Retrieval-Augmented Generation]] (Reimers & Gurevych, 2019; Karpukhin et al., 2020; Nogueira & Cho, 2019).
- Wenn ein Modell zu moderaten Kosten feinjustiert und betrieben werden soll: BERT-Base hat 110 Mio. Parameter (Devlin et al., 2018).

### Stärken und Grenzen

**Stärken**
- Jede Token-Repräsentation nutzt in allen Schichten Kontext von beiden Seiten (Devlin et al., 2018).
- Ein vortrainiertes Modell bedient viele Aufgaben mit nur einer aufgabenspezifischen Ausgabeschicht (Devlin et al., 2018).
- Destillierte Versionen behalten den Großteil der Qualität bei einem Bruchteil der Kosten: DistilBERT ist 40 % kleiner und 60 % schneller und behält 97 % des Sprachverständnisses von BERT (Sanh et al., 2019); TinyBERT mit 4 Schichten erreicht über 96,8 % der Leistung von BERT-Base auf GLUE und ist 7,5-mal kleiner und 9,4-mal schneller (Jiao et al., 2019).

**Grenzen**
- BERT erzeugt keinen Text; für Generierung werden Decoder-Modelle wie [[gpt|GPT]] eingesetzt.
- Das [MASK]-Token kommt im Vortraining vor, beim Fine-Tuning aber nicht; die 80/10/10-Regel verringert diese Diskrepanz nur (Devlin et al., 2018).
- Die [CLS]-Ausgabe oder der Durchschnitt der Token-Vektoren von BERT liefert schlechte Satz-Embeddings, oft schlechter als gemittelte GloVe-Vektoren (Reimers & Gurevych, 2019).
- Satzpaare zu vergleichen, indem beide Sätze in BERT eingegeben werden, ist langsam: Das ähnlichste Paar unter 10.000 Sätzen zu finden, erfordert etwa 50 Millionen Inferenzschritte, rund 65 Stunden auf einer V100-GPU (Reimers & Gurevych, 2019).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| BERT (Encoder-only) | Bidirektionaler Kontext, Masked Language Modelling, pro Aufgabe feinjustiert (Devlin et al., 2018) | Klassifikation, Tagging, extraktives QA |
| [[gpt\|GPT]] (Decoder-only) | Kontext von links nach rechts, Next-Token-Prediction; erzeugt Text (Radford et al., 2018) | Generierung und Prompting |
| Sentence-BERT (Bi-Encoder) | Bettet jeden Satz einzeln ein, Vergleich per Kosinus-Ähnlichkeit; etwa 5 Sekunden statt 65 Stunden im Beispiel mit 10.000 Sätzen (Reimers & Gurevych, 2019) | Semantische Suche, [[clustering\|Clustering]] |
| BERT-Re-Ranker ([[cross-encoder\|Cross-Encoder]]) | Liest Anfrage und Passage gemeinsam; genauer, aber ein Modelldurchlauf pro Paar (Nogueira & Cho, 2019) | Re-Ranking einer kurzen Kandidatenliste |

### In der Praxis
BERT wird selten von Grund auf trainiert: Ein vortrainierter Checkpoint wird für die Aufgabe feinjustiert, wofür nur eine zusätzliche Ausgabeschicht nötig ist (Devlin et al., 2018); wo die Inferenzkosten zählen, kommen destillierte Modelle wie DistilBERT in Frage (Sanh et al., 2019). Für die Suche besteht die Wahl zwischen getrennt eingebetteten Texten ([[semantic-retrieval|Semantisches Retrieval]], [[vector-databases|Vektordatenbanken]]) und gemeinsam bewerteten Anfrage-Text-Paaren ([[cross-encoder|Cross-Encoder]]); Retrieval-Pipelines kombinieren oft beides ([[rag-retrieval|RAG: Retrieval]]). Die Ähnlichkeit von BERT-Embeddings wird mit [[text-similarity-metrics|Textähnlichkeitsmetriken]] bewertet, und aus Web- und Buchtexten gelernte Repräsentationen können gesellschaftliche Verzerrungen tragen ([[bias-in-nlp|Bias in NLP]]).

### Merksatz
BERT lernt Textverständnis, indem es maskierte Wörter von beiden Seiten her ergänzt; es ist das Encoder-Gegenstück zu GPT und die Grundlage der meisten Modelle, die Text klassifizieren, extrahieren oder einbetten.

### Quellen
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Radford, A., Narasimhan, K., Salimans, T. & Sutskever, I. (2018). *Improving Language Understanding by Generative Pre-Training.* OpenAI. [PDF](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Sanh, V. et al. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* [arXiv:1910.01108](https://arxiv.org/abs/1910.01108)
- Jiao, X. et al. (2019). *TinyBERT: Distilling BERT for Natural Language Understanding.* Findings of EMNLP 2020. [arXiv:1909.10351](https://arxiv.org/abs/1909.10351)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
