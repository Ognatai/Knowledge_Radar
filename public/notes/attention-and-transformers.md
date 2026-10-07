---
title_en: Attention and Transformers
title_de: Attention und Transformer
entity_type: Method
sources:
- https://arxiv.org/abs/1409.3215
- https://arxiv.org/abs/1409.0473
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/2010.11929
- https://arxiv.org/abs/2205.14135
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Attention lets a model weigh all positions of an input when computing each output, instead of squeezing the input into one fixed-length vector (Bahdanau et al., 2014). The Transformer builds a whole architecture on attention alone, without recurrence or convolution, which makes it faster to train and better at translation (Vaswani et al., 2017). Its encoder, decoder or both underlie BERT, T5 and the GPT family (Urchs, 2025) and, applied to image patches, Vision Transformers (Dosovitskiy et al., 2020); self-attention's quadratic cost in sequence length is reduced in practice by IO-aware implementations (Dao et al., 2022).

### How it works

Each token is turned into a query, a key and a value. Attention compares a token's query with all keys, turns the similarities into weights and returns the weighted sum of the values. Stacking multi-head attention and feed-forward layers with residual connections gives the Transformer.

```text
1. Encoder-decoder and its bottleneck
▼
2. Attention
▼
3. Scaled dot-product and multi-head attention
▼
4. The Transformer layer
▼
5. Encoder, decoder and encoder-decoder models
▼
6. Beyond text and efficiency
```

#### 1. Encoder-decoder and its bottleneck

Sequence-to-sequence models encode an input sequence into a vector of fixed dimensionality with one LSTM and decode the output from it with another (Sutskever et al., 2014; [[recurrent-neural-networks|Recurrent Neural Networks and Time Series]]). Bahdanau et al. (2014) conjectured that this fixed-length vector is a bottleneck for translation performance.

#### 2. Attention

Bahdanau et al. (2014) let the decoder automatically (soft-)search for the parts of the source sentence that are relevant for predicting the next target word, instead of relying on one vector. This reached translation performance comparable to the existing state-of-the-art phrase-based system on English-to-French, and the learned soft alignments agreed well with intuition.

#### 3. Scaled dot-product and multi-head attention

The Transformer computes attention as softmax(QKᵀ / √d_k)V: the similarity of queries Q and keys K determines weights over the values V, scaled by the square root of the key dimension d_k (Urchs, 2025). Instead of one attention function, h heads with their own learned projections attend to different representation subspaces in parallel, and their outputs are concatenated and projected back (Urchs, 2025).

#### 4. The Transformer layer

The Transformer (Vaswani et al., 2017) is based solely on attention mechanisms and dispenses with recurrence and convolutions. Encoder and decoder each consist of N identical layers; an encoder layer contains multi-head self-attention and a position-wise feed-forward network, and a decoder layer adds cross-attention over the encoder outputs; every sub-layer is wrapped in a residual connection and layer normalisation (Urchs, 2025). Because all positions are processed in parallel, training is faster: the Transformer reached 28.4 BLEU on WMT 2014 English-to-German and 41.8 BLEU on English-to-French after 3.5 days on eight GPUs (Vaswani et al., 2017).

#### 5. Encoder, decoder and encoder-decoder models

Three families build on the architecture (Urchs, 2025). Encoder-only BERT conditions each token on its left and right context in all layers and is pretrained with masked language modelling, in which 15% of tokens are masked, and next sentence prediction; it is fine-tuned with one additional output layer and set new results on eleven NLP tasks (Devlin et al., 2018). The encoder-decoder T5 casts every task as text-to-text with a task prefix such as "summarize:". Decoder-only GPT models predict the next token autoregressively; GPT-3 with 175 billion parameters showed few-shot learning from prompts ([[large-language-models|Large Language Models]]).

#### 6. Beyond text and efficiency

A pure Transformer applied to sequences of image patches, the Vision Transformer, attained excellent image classification results compared with convolutional networks when pretrained on large data, while requiring substantially fewer computational resources to train (Dosovitskiy et al., 2020; [[multimodal-models|Multimodal Models]]). Self-attention's time and memory grow quadratically with sequence length. FlashAttention computes exact attention with tiling that reduces reads and writes between GPU memory levels, giving for example a 3× training speedup on GPT-2 with sequence length 1K and enabling longer contexts (Dao et al., 2022).

#### Origin and variants

Attention for neural machine translation (Bahdanau et al., 2014) extended sequence-to-sequence models (Sutskever et al., 2014), the Transformer (Vaswani et al., 2017) removed recurrence altogether, and BERT (Devlin et al., 2018), T5 and GPT models (Urchs, 2025), Vision Transformers (Dosovitskiy et al., 2020) and efficient attention kernels (Dao et al., 2022) followed.

### When to use it

- For language tasks, Transformers are the standard architecture, as encoders for understanding and decoders for generation (Urchs, 2025).
- For image tasks with large pretraining data, Vision Transformers are an alternative to CNNs (Dosovitskiy et al., 2020).
- For long inputs, efficient attention implementations reduce memory and time (Dao et al., 2022).

### Strengths and limitations

**Strengths**
- Every token can attend to every other token, capturing long-range dependencies (Vaswani et al., 2017).
- Parallel processing makes training faster than with recurrent models (Vaswani et al., 2017).
- One architecture serves understanding, generation and vision (Urchs, 2025; Dosovitskiy et al., 2020).

**Limitations**
- Self-attention's time and memory grow quadratically with sequence length (Dao et al., 2022).
- Vision Transformers rely on large-scale pretraining to excel (Dosovitskiy et al., 2020).
- Attention weights are not reliable explanations of predictions ([[explainable-ai|Explainable AI (XAI)]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| RNN encoder-decoder | Whole input in one fixed-length vector (Sutskever et al., 2014) | Short sequences, historical baseline |
| RNN with attention | Decoder attends over all encoder states (Bahdanau et al., 2014) | Translation with recurrent models |
| Transformer | Attention only, parallel over positions (Vaswani et al., 2017) | Language and many other modalities |
| Encoder-only (BERT) | Bidirectional context, fine-tuned per task (Devlin et al., 2018) | Classification, NER, extractive QA |
| Decoder-only (GPT) | Autoregressive next-token prediction (Urchs, 2025) | Text generation, prompting |

### In practice

Pretrained Transformer models are fine-tuned or prompted rather than trained from scratch ([[llm-adaptation|LLM Adaptation]]). Context length and attention implementation determine memory use (Dao et al., 2022), and inputs are tokenised into subwords before they reach the model ([[tokenization|Tokenization]]).

### Key takeaway

Attention lets every position draw information from every other position; the Transformer builds on it alone and is the basis of today's language and many vision models.

### Sources

- Sutskever, I. et al. (2014). *Sequence to Sequence Learning with Neural Networks.* NeurIPS 2014. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215)
- Bahdanau, D. et al. (2014). *Neural Machine Translation by Jointly Learning to Align and Translate.* ICLR 2015. [arXiv:1409.0473](https://arxiv.org/abs/1409.0473)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Attention erlaubt einem Modell, bei der Berechnung jeder Ausgabe alle Positionen einer Eingabe zu gewichten, statt die Eingabe in einen einzigen Vektor fester Länge zu pressen (Bahdanau et al., 2014). Der Transformer baut eine ganze Architektur allein auf Attention auf, ohne Rekurrenz oder Faltung; dadurch trainiert er schneller und übersetzt besser (Vaswani et al., 2017). Sein Encoder, sein Decoder oder beide liegen BERT, T5 und der GPT-Familie zugrunde (Urchs, 2025), auf Bildausschnitte angewendet den Vision Transformern (Dosovitskiy et al., 2020); die quadratischen Kosten der Self-Attention in der Sequenzlänge verringern in der Praxis speicherzugriffsbewusste Implementierungen (Dao et al., 2022).

### Funktionsweise

Jedes Token wird in eine Query, einen Key und einen Value umgewandelt. Attention vergleicht die Query eines Tokens mit allen Keys, macht aus den Ähnlichkeiten Gewichte und liefert die gewichtete Summe der Values. Gestapelte Multi-Head-Attention- und Feedforward-Schichten mit Residualverbindungen ergeben den Transformer.

```text
1. Encoder-Decoder und sein Engpass
▼
2. Attention
▼
3. Scaled Dot-Product und Multi-Head-Attention
▼
4. Die Transformer-Schicht
▼
5. Encoder-, Decoder- und Encoder-Decoder-Modelle
▼
6. Über Text hinaus und Effizienz
```

#### 1. Encoder-Decoder und sein Engpass

Sequence-to-Sequence-Modelle kodieren eine Eingabesequenz mit einem LSTM in einen Vektor fester Dimension und dekodieren daraus mit einem zweiten die Ausgabe (Sutskever et al., 2014; [[recurrent-neural-networks|RNN und Zeitreihen]]). Bahdanau et al. (2014) vermuteten, dass dieser Vektor fester Länge ein Engpass für die Übersetzungsqualität ist.

#### 2. Attention

Bahdanau et al. (2014) ließen den Decoder automatisch („weich“) nach den Teilen des Quellsatzes suchen, die für die Vorhersage des nächsten Zielworts relevant sind, statt sich auf einen Vektor zu verlassen. Damit erreichten sie bei Englisch-Französisch eine Übersetzungsqualität, die mit dem damals besten phrasenbasierten System vergleichbar war, und die gelernten weichen Zuordnungen entsprachen gut der Intuition.

#### 3. Scaled Dot-Product und Multi-Head-Attention

Der Transformer berechnet Attention als softmax(QKᵀ / √d_k)V: Die Ähnlichkeit von Queries Q und Keys K bestimmt Gewichte über die Values V, skaliert mit der Wurzel der Key-Dimension d_k (Urchs, 2025). Statt einer einzigen Attention-Funktion achten h Heads mit eigenen gelernten Projektionen parallel auf verschiedene Teilräume der Repräsentation; ihre Ausgaben werden verkettet und zurückprojiziert (Urchs, 2025).

#### 4. Die Transformer-Schicht

Der Transformer (Vaswani et al., 2017) beruht ausschließlich auf Attention-Mechanismen und verzichtet auf Rekurrenz und Faltungen. Encoder und Decoder bestehen jeweils aus N gleichartigen Schichten; eine Encoder-Schicht enthält Multi-Head-Self-Attention und ein positionsweises Feedforward-Netz, eine Decoder-Schicht zusätzlich Cross-Attention über die Encoder-Ausgaben; jede Teilschicht ist von einer Residualverbindung und Layer Normalization umgeben (Urchs, 2025). Da alle Positionen parallel verarbeitet werden, trainiert er schneller: Der Transformer erreichte 28,4 BLEU auf WMT 2014 Englisch-Deutsch und 41,8 BLEU auf Englisch-Französisch nach 3,5 Tagen auf acht GPUs (Vaswani et al., 2017).

#### 5. Encoder-, Decoder- und Encoder-Decoder-Modelle

Drei Modellfamilien bauen auf der Architektur auf (Urchs, 2025). Das reine Encoder-Modell BERT bezieht für jedes Token in allen Schichten den linken und rechten Kontext ein und wird mit Masked Language Modelling, bei dem 15 % der Token maskiert werden, und Next Sentence Prediction vortrainiert; es wird mit einer zusätzlichen Ausgabeschicht feinabgestimmt und erzielte neue Bestwerte bei elf NLP-Aufgaben (Devlin et al., 2018). Das Encoder-Decoder-Modell T5 formuliert jede Aufgabe als Text-zu-Text mit einem Aufgabenpräfix wie „summarize:“. Reine Decoder-Modelle der GPT-Familie sagen autoregressiv das nächste Token voraus; GPT-3 mit 175 Milliarden Parametern zeigte Few-Shot-Learning über Prompts ([[large-language-models|Large Language Models]]).

#### 6. Über Text hinaus und Effizienz

Ein reiner Transformer, angewendet auf Folgen von Bildausschnitten (Patches), der Vision Transformer, erzielte bei großem Vortraining hervorragende Ergebnisse in der Bildklassifikation im Vergleich zu konvolutionalen Netzen und brauchte dabei deutlich weniger Rechenaufwand für das Training (Dosovitskiy et al., 2020; [[multimodal-models|Multimodale Modelle]]). Zeit- und Speicherbedarf der Self-Attention wachsen quadratisch mit der Sequenzlänge. FlashAttention berechnet exakte Attention mit einer Kachelung, die Lese- und Schreibzugriffe zwischen den Speicherebenen der GPU verringert, und erreicht etwa eine dreifache Trainingsbeschleunigung bei GPT-2 mit Sequenzlänge 1K; zudem ermöglicht es längere Kontexte (Dao et al., 2022).

#### Ursprung und Varianten

Attention für neuronale maschinelle Übersetzung (Bahdanau et al., 2014) erweiterte Sequence-to-Sequence-Modelle (Sutskever et al., 2014), der Transformer (Vaswani et al., 2017) verzichtete ganz auf Rekurrenz, und es folgten BERT (Devlin et al., 2018), T5 und GPT-Modelle (Urchs, 2025), Vision Transformer (Dosovitskiy et al., 2020) und effiziente Attention-Kernel (Dao et al., 2022).

### Wann einsetzen

- Für Sprachaufgaben sind Transformer die Standardarchitektur, als Encoder für das Verstehen und als Decoder für die Generierung (Urchs, 2025).
- Für Bildaufgaben mit großen Vortrainingsdaten sind Vision Transformer eine Alternative zu CNNs (Dosovitskiy et al., 2020).
- Für lange Eingaben verringern effiziente Attention-Implementierungen Speicher- und Zeitbedarf (Dao et al., 2022).

### Stärken und Grenzen

**Stärken**
- Jedes Token kann auf jedes andere achten und so weitreichende Abhängigkeiten erfassen (Vaswani et al., 2017).
- Parallele Verarbeitung macht das Training schneller als bei rekurrenten Modellen (Vaswani et al., 2017).
- Eine Architektur dient Verstehen, Generierung und Bildverarbeitung (Urchs, 2025; Dosovitskiy et al., 2020).

**Einschränkungen**
- Zeit- und Speicherbedarf der Self-Attention wachsen quadratisch mit der Sequenzlänge (Dao et al., 2022).
- Vision Transformer brauchen großes Vortraining, um zu überzeugen (Dosovitskiy et al., 2020).
- Attention-Gewichte sind keine verlässlichen Erklärungen von Vorhersagen ([[explainable-ai|Erklärbare KI (XAI)]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| RNN-Encoder-Decoder | Ganze Eingabe in einem Vektor fester Länge (Sutskever et al., 2014) | Kurze Sequenzen, historische Baseline |
| RNN mit Attention | Decoder achtet auf alle Encoder-Zustände (Bahdanau et al., 2014) | Übersetzung mit rekurrenten Modellen |
| Transformer | Nur Attention, parallel über die Positionen (Vaswani et al., 2017) | Sprache und viele weitere Modalitäten |
| Reiner Encoder (BERT) | Bidirektionaler Kontext, je Aufgabe feinabgestimmt (Devlin et al., 2018) | Klassifikation, NER, extraktive Fragebeantwortung |
| Reiner Decoder (GPT) | Autoregressive Vorhersage des nächsten Tokens (Urchs, 2025) | Textgenerierung, Prompting |

### In der Praxis

Vortrainierte Transformer-Modelle werden feinabgestimmt oder gepromptet statt von Grund auf trainiert ([[llm-adaptation|LLM-Anpassung]]). Kontextlänge und Attention-Implementierung bestimmen den Speicherbedarf (Dao et al., 2022), und Eingaben werden vor dem Modell in Subwords tokenisiert ([[tokenization|Tokenisierung]]).

### Merksatz

Attention lässt jede Position Information aus jeder anderen Position ziehen; der Transformer baut allein darauf auf und ist die Grundlage heutiger Sprach- und vieler Bildmodelle.

### Quellen

- Sutskever, I. et al. (2014). *Sequence to Sequence Learning with Neural Networks.* NeurIPS 2014. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215)
- Bahdanau, D. et al. (2014). *Neural Machine Translation by Jointly Learning to Align and Translate.* ICLR 2015. [arXiv:1409.0473](https://arxiv.org/abs/1409.0473)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
