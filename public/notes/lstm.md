---
title_en: Long Short-Term Memory (LSTM)
title_de: Long Short-Term Memory (LSTM)
entity_type: Method
aliases:
- LSTM
- Long short-term memory
- LSTM network
- BiLSTM-CRF
- Bidirectional LSTM
sources:
- https://doi.org/10.1162/neco.1997.9.8.1735
- https://arxiv.org/abs/1503.04069
- https://arxiv.org/abs/1308.0850
- https://arxiv.org/abs/1508.01991
- https://arxiv.org/abs/1609.08144
- https://arxiv.org/abs/1706.03762
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Long Short-Term Memory (LSTM) is a [[recurrent-neural-networks|recurrent neural network]] architecture whose memory cells keep the error signal constant over time, so that it can learn dependencies across more than 1,000 time steps, where earlier recurrent networks failed because gradients vanished or exploded (Hochreiter & Schmidhuber, 1997). Multiplicative gates decide what is written into a cell, what is kept or forgotten, and what is read out. The vanilla LSTM with input, forget and output gates became the standard model for sequence tasks such as speech and handwriting recognition, sequence tagging and [[machine-translation|machine translation]] (Greff et al., 2017; Wu et al., 2016), until Transformers replaced recurrence with attention in most language tasks (Vaswani et al., 2017).

### How it works

```text
x_t, y_{t-1}, c_{t-1}
   │
   ├─ block input   z_t = tanh(W_z x_t + R_z y_{t-1} + b_z)
   ├─ input gate    i_t = σ(W_i x_t + R_i y_{t-1} + p_i ⊙ c_{t-1} + b_i)
   ├─ forget gate   f_t = σ(W_f x_t + R_f y_{t-1} + p_f ⊙ c_{t-1} + b_f)
   ▼
cell state  c_t = z_t ⊙ i_t + c_{t-1} ⊙ f_t          (constant error carousel)
   │
   ├─ output gate   o_t = σ(W_o x_t + R_o y_{t-1} + p_o ⊙ c_t + b_o)
   ▼
block output  y_t = tanh(c_t) ⊙ o_t   → next time step and next layer
```

An LSTM layer replaces the simple hidden units of a recurrent network with memory blocks. Each block holds a cell state that is carried from step to step, and three gates with sigmoid activations between 0 and 1 that scale what flows into the cell, what stays in it and what leaves it (Greff et al., 2017).

#### 1. The problem: decaying error flow

With back-propagation through time or real-time recurrent learning, error signals flowing backwards in time either blow up or vanish, because their size depends exponentially on the weights; exploding errors make weights oscillate, vanishing errors make learning over long time lags take prohibitively long or fail entirely (Hochreiter & Schmidhuber, 1997). This is the vanishing and exploding gradient problem described in [[recurrent-neural-networks|recurrent neural networks]] and [[back-propagation|back-propagation]].

#### 2. Memory cell and constant error carousel

The core of each memory cell is a linear unit with a fixed self-connection of weight 1.0, the constant error carousel (CEC): an error signal inside it can flow back indefinitely without being scaled (Hochreiter & Schmidhuber, 1997). In the vanilla formulation, the new cell state is the gated block input plus the old cell state scaled by the forget gate, `c_t = z_t ⊙ i_t + c_{t-1} ⊙ f_t` (Greff et al., 2017). Because the old state enters additively rather than through a squashing non-linearity, information and gradients can survive many steps.

#### 3. Gates

- **Input gate:** protects the stored content from perturbation by irrelevant inputs; the network learns when to write (Hochreiter & Schmidhuber, 1997).
- **Output gate:** protects other units from perturbation by currently irrelevant memory content; the network learns when to read (Hochreiter & Schmidhuber, 1997).
- **Forget gate:** added later by Gers et al. so that the cell can reset its own state, which made continual tasks learnable (Greff et al., 2017).
- **Peephole connections:** connections from the cell to the gates, added by Gers and Schmidhuber to learn precise timings (Greff et al., 2017).

Gate activations use the logistic sigmoid, block input and output activations usually tanh, and `⊙` is element-wise multiplication (Greff et al., 2017).

#### 4. Training

The original LSTM truncated the gradient outside the cells and trained with a mix of real-time recurrent learning and back-propagation through time; its update cost per weight and time step was O(1), like BPTT, but local in space and time (Hochreiter & Schmidhuber, 1997). Graves and Schmidhuber introduced full back-propagation through time for LSTM, which also allowed gradients to be checked with finite differences; this vanilla LSTM is the most commonly used setup (Greff et al., 2017). In practice, gradients are often clipped for numerical stability: Graves (2013) clipped LSTM derivatives to ranges such as [-1, 1] and found clipping the output gradients vital for stable training.

#### 5. Stacking, bidirectionality and output layers

LSTM layers are stacked and combined with task-specific output layers. A bidirectional LSTM runs one layer forwards and one backwards in time, so each position sees past and future context (Greff et al., 2017). For sequence tagging, Huang et al. (2015) put a conditional random field on top of a bidirectional LSTM (BiLSTM-CRF), which uses both past and future features and sentence-level tag information and reached state-of-the-art or near state-of-the-art accuracy on part-of-speech tagging, chunking and named entity recognition. [[google|Google]]'s neural machine translation system used 8 encoder layers (one bidirectional, seven unidirectional) and 8 decoder layers with attention; residual connections between layers were needed, because simple stacked LSTMs worked well up to 4 layers, barely with 6 and very poorly beyond 8 (Wu et al., 2016).

#### Origin and variants

Sepp Hochreiter and Jürgen Schmidhuber published LSTM in Neural Computation in 1997 (Hochreiter & Schmidhuber, 1997). The original version had input and output gates but no forget gate and no peepholes (Greff et al., 2017). Variants include the projection layer of Sak et al., which reduces the number of parameters, and the Gated Recurrent Unit (GRU) of Cho et al., which drops peepholes and the output activation and couples input and forget gate into an update gate (Greff et al., 2017).

### When to use it

- Sequence data with long-range dependencies where order matters: speech, handwriting, music, sensor and [[time-series-analysis|time series]] data (Greff et al., 2017).
- Sequence labelling such as [[part-of-speech-tagging|part-of-speech tagging]] and [[entity-extraction|named entity recognition]] with a BiLSTM-CRF (Huang et al., 2015).
- Generating sequences one step at a time, for example text or online handwriting (Graves, 2013).
- Settings with streaming input, where a model must update its state step by step instead of attending to a whole sequence at once.

### Strengths and limitations

**Strengths**
- Bridges time lags of more than 1,000 steps, also with noisy, distributed and continuous inputs (Hochreiter & Schmidhuber, 1997).
- Unlike finite state automata or [[hidden-markov-models|hidden Markov models]], it needs no prior choice of a finite number of states (Hochreiter & Schmidhuber, 1997).
- Robust to hyperparameters: in 5,400 runs, hyperparameters were nearly independent, so the learning rate can be tuned first on a small network (Greff et al., 2017).

**Limitations**
- Computation is sequential over time steps, which limits parallel training; the Transformer was proposed as more parallelisable and faster to train (Vaswani et al., 2017).
- Gradient-based training cannot count discrete time steps precisely, for example whether a signal occurred 99 or 100 steps ago (Hochreiter & Schmidhuber, 1997).
- Some non-decomposable problems such as strongly delayed XOR are hard for the truncated algorithm (Hochreiter & Schmidhuber, 1997).
- Deep stacks need residual connections to train (Wu et al., 2016).

### Comparison

| Model | Memory mechanism | Parallel over time | Typical use |
|---|---|---|---|
| Simple RNN ([[recurrent-neural-networks\|RNN]]) | hidden state through a non-linearity | no | short dependencies |
| LSTM | gated cell state with additive update | no | long dependencies in sequences |
| GRU | coupled update gate, no separate output activation | no | like LSTM with fewer parameters |
| [[attention-and-transformers\|Transformer]] | attention over all positions | yes | language modelling, translation |
| [[hidden-markov-models\|HMM]] | finite set of discrete states | no | tagging with small labelled data |

Sources: Greff et al. (2017), Hochreiter & Schmidhuber (1997), Vaswani et al. (2017).

### In practice

Greff et al. (2017) compared the vanilla LSTM with eight variants on [[automatic-speech-recognition|speech recognition]], handwriting recognition and music modelling, with hyperparameters found by [[hyperparameter-optimisation|random search]]. None of the variants improved significantly on the vanilla LSTM; removing the forget gate or the output activation hurt on all three tasks, while coupling input and forget gate or dropping peepholes made the model simpler without significant loss. The learning rate was the most important hyperparameter, followed by network size, and momentum mattered little (Greff et al., 2017). Today LSTMs still appear in sequence labelling and forecasting pipelines and in earlier architectures such as the sparsely-gated [[mixture-of-experts|mixture-of-experts]] layer placed between LSTM layers, while large language models are built on Transformers ([[large-language-models|large language models]]).

### Key takeaway

An LSTM keeps a cell state that is updated additively and guarded by learned gates, which lets gradients survive long sequences; the forget gate and the output activation are its most critical parts.

### Sources

- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8), 1735–1780. [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
- Greff, K., Srivastava, R. K., Koutník, J., Steunebrink, B. R. & Schmidhuber, J. (2017). *LSTM: A Search Space Odyssey.* IEEE Transactions on Neural Networks and Learning Systems. [arXiv:1503.04069](https://arxiv.org/abs/1503.04069)
- Graves, A. (2013). *Generating Sequences With Recurrent Neural Networks.* [arXiv:1308.0850](https://arxiv.org/abs/1308.0850)
- Huang, Z., Xu, W. & Yu, K. (2015). *Bidirectional LSTM-CRF Models for Sequence Tagging.* [arXiv:1508.01991](https://arxiv.org/abs/1508.01991)
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation.* [arXiv:1609.08144](https://arxiv.org/abs/1609.08144)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Long Short-Term Memory (LSTM) ist eine Architektur [[recurrent-neural-networks|rekurrenter neuronaler Netze]], deren Speicherzellen das Fehlersignal über die Zeit konstant halten, sodass sie Abhängigkeiten über mehr als 1.000 Zeitschritte lernen kann, an denen frühere rekurrente Netze scheiterten, weil Gradienten verschwanden oder explodierten (Hochreiter & Schmidhuber, 1997). Multiplikative Gates entscheiden, was in eine Zelle geschrieben, was behalten oder vergessen und was ausgelesen wird. Die Vanilla-LSTM mit Input-, Forget- und Output-Gate wurde zum Standardmodell für Sequenzaufgaben wie Sprach- und Handschrifterkennung, Sequence Labelling und [[machine-translation|maschinelle Übersetzung]] (Greff et al., 2017; Wu et al., 2016), bis Transformer in den meisten Sprachaufgaben Rekurrenz durch Attention ersetzten (Vaswani et al., 2017).

### Funktionsweise

```text
x_t, y_{t-1}, c_{t-1}
   │
   ├─ Block-Input    z_t = tanh(W_z x_t + R_z y_{t-1} + b_z)
   ├─ Input-Gate     i_t = σ(W_i x_t + R_i y_{t-1} + p_i ⊙ c_{t-1} + b_i)
   ├─ Forget-Gate    f_t = σ(W_f x_t + R_f y_{t-1} + p_f ⊙ c_{t-1} + b_f)
   ▼
Zellzustand  c_t = z_t ⊙ i_t + c_{t-1} ⊙ f_t          (Constant Error Carousel)
   │
   ├─ Output-Gate    o_t = σ(W_o x_t + R_o y_{t-1} + p_o ⊙ c_t + b_o)
   ▼
Block-Output  y_t = tanh(c_t) ⊙ o_t   → nächster Zeitschritt und nächste Schicht
```

Eine LSTM-Schicht ersetzt die einfachen verborgenen Einheiten eines rekurrenten Netzes durch Speicherblöcke. Jeder Block hält einen Zellzustand, der von Schritt zu Schritt weitergegeben wird, und drei Gates mit Sigmoid-Aktivierung zwischen 0 und 1, die skalieren, was in die Zelle hineinfließt, was in ihr bleibt und was sie verlässt (Greff et al., 2017).

#### 1. Das Problem: abklingender Fehlerfluss

Bei Backpropagation Through Time oder Real-Time Recurrent Learning explodieren oder verschwinden Fehlersignale, die rückwärts durch die Zeit fließen, weil ihre Größe exponentiell von den Gewichten abhängt; explodierende Fehler lassen Gewichte oszillieren, verschwindende Fehler machen das Lernen über lange Zeitabstände extrem langsam oder unmöglich (Hochreiter & Schmidhuber, 1997). Das ist das Problem verschwindender und explodierender Gradienten, das in [[recurrent-neural-networks|rekurrenten neuronalen Netzen]] und bei der [[back-propagation|Backpropagation]] beschrieben ist.

#### 2. Speicherzelle und Constant Error Carousel

Kern jeder Speicherzelle ist eine lineare Einheit mit einer festen Selbstverbindung vom Gewicht 1,0, das Constant Error Carousel (CEC): Ein Fehlersignal darin kann unbegrenzt zurückfließen, ohne skaliert zu werden (Hochreiter & Schmidhuber, 1997). In der Vanilla-Formulierung ist der neue Zellzustand der gegatete Block-Input plus der alte Zellzustand, skaliert mit dem Forget-Gate, `c_t = z_t ⊙ i_t + c_{t-1} ⊙ f_t` (Greff et al., 2017). Weil der alte Zustand additiv statt über eine stauchende Nichtlinearität eingeht, können Information und Gradienten viele Schritte überdauern.

#### 3. Gates

- **Input-Gate:** schützt den gespeicherten Inhalt vor Störung durch irrelevante Eingaben; das Netz lernt, wann geschrieben wird (Hochreiter & Schmidhuber, 1997).
- **Output-Gate:** schützt andere Einheiten vor Störung durch gerade irrelevanten Speicherinhalt; das Netz lernt, wann gelesen wird (Hochreiter & Schmidhuber, 1997).
- **Forget-Gate:** später von Gers et al. ergänzt, damit die Zelle ihren eigenen Zustand zurücksetzen kann, wodurch kontinuierliche Aufgaben lernbar wurden (Greff et al., 2017).
- **Peephole-Verbindungen:** Verbindungen von der Zelle zu den Gates, von Gers und Schmidhuber ergänzt, um präzise Zeitabstände zu lernen (Greff et al., 2017).

Gate-Aktivierungen nutzen die logistische Sigmoidfunktion, Block-Input und -Output meist tanh, und `⊙` ist die elementweise Multiplikation (Greff et al., 2017).

#### 4. Training

Die ursprüngliche LSTM schnitt den Gradienten außerhalb der Zellen ab und trainierte mit einer Mischung aus Real-Time Recurrent Learning und Backpropagation Through Time; ihr Aufwand pro Gewicht und Zeitschritt war O(1) wie bei BPTT, aber lokal in Raum und Zeit (Hochreiter & Schmidhuber, 1997). Graves und Schmidhuber führten volle Backpropagation Through Time für LSTM ein, wodurch sich Gradienten auch mit finiten Differenzen prüfen ließen; diese Vanilla-LSTM ist das am häufigsten genutzte Setup (Greff et al., 2017). In der Praxis werden Gradienten für die numerische Stabilität oft begrenzt (Gradient Clipping): Graves (2013) begrenzte LSTM-Ableitungen auf Bereiche wie [-1, 1] und fand das Begrenzen der Output-Gradienten entscheidend für stabiles Training.

#### 5. Stapeln, Bidirektionalität und Ausgabeschichten

LSTM-Schichten werden gestapelt und mit aufgabenspezifischen Ausgabeschichten kombiniert. Eine bidirektionale LSTM lässt eine Schicht vorwärts und eine rückwärts durch die Zeit laufen, sodass jede Position vergangenen und zukünftigen Kontext sieht (Greff et al., 2017). Für Sequence Labelling setzten Huang et al. (2015) ein Conditional Random Field auf eine bidirektionale LSTM (BiLSTM-CRF), die vergangene und zukünftige Merkmale sowie Tag-Information auf Satzebene nutzt und auf Part-of-Speech-Tagging, Chunking und Named Entity Recognition den Stand der Technik erreichte oder ihm nahekam. Googles neuronales Übersetzungssystem nutzte 8 Encoder-Schichten (eine bidirektionale, sieben unidirektionale) und 8 Decoder-Schichten mit Attention; Residualverbindungen zwischen den Schichten waren nötig, weil einfach gestapelte LSTMs bis 4 Schichten gut, mit 6 kaum und jenseits von 8 sehr schlecht funktionierten (Wu et al., 2016).

#### Ursprung und Varianten

Sepp Hochreiter und Jürgen Schmidhuber veröffentlichten LSTM 1997 in Neural Computation (Hochreiter & Schmidhuber, 1997). Die ursprüngliche Version hatte Input- und Output-Gates, aber kein Forget-Gate und keine Peepholes (Greff et al., 2017). Zu den Varianten gehören die Projektionsschicht von Sak et al., die die Zahl der Parameter verringert, und die Gated Recurrent Unit (GRU) von Cho et al., die Peepholes und die Output-Aktivierung weglässt und Input- und Forget-Gate zu einem Update-Gate koppelt (Greff et al., 2017).

### Wann einsetzen

- Sequenzdaten mit weitreichenden Abhängigkeiten, bei denen die Reihenfolge zählt: Sprache, Handschrift, Musik, Sensor- und [[time-series-analysis|Zeitreihendaten]] (Greff et al., 2017).
- Sequence Labelling wie [[part-of-speech-tagging|Part-of-Speech-Tagging]] und [[entity-extraction|Named Entity Recognition]] mit einer BiLSTM-CRF (Huang et al., 2015).
- Erzeugen von Sequenzen Schritt für Schritt, etwa Text oder Online-Handschrift (Graves, 2013).
- Anwendungen mit Streaming-Eingaben, in denen ein Modell seinen Zustand Schritt für Schritt aktualisieren muss, statt eine ganze Sequenz auf einmal per Attention zu betrachten.

### Stärken und Grenzen

**Stärken**
- Überbrückt Zeitabstände von mehr als 1.000 Schritten, auch bei verrauschten, verteilten und kontinuierlichen Eingaben (Hochreiter & Schmidhuber, 1997).
- Anders als endliche Automaten oder [[hidden-markov-models|Hidden-Markov-Modelle]] braucht sie keine vorab festgelegte endliche Zahl von Zuständen (Hochreiter & Schmidhuber, 1997).
- Robust gegenüber Hyperparametern: In 5.400 Läufen waren die Hyperparameter nahezu unabhängig, sodass sich die Lernrate zuerst an einem kleinen Netz einstellen lässt (Greff et al., 2017).

**Grenzen**
- Die Berechnung läuft sequenziell über die Zeitschritte, was paralleles Training einschränkt; der Transformer wurde als besser parallelisierbar und schneller zu trainieren vorgeschlagen (Vaswani et al., 2017).
- Gradientenbasiertes Training kann diskrete Zeitschritte nicht genau zählen, etwa ob ein Signal vor 99 oder vor 100 Schritten auftrat (Hochreiter & Schmidhuber, 1997).
- Manche nicht zerlegbaren Probleme wie das Strongly Delayed XOR sind für den abgeschnittenen Algorithmus schwer (Hochreiter & Schmidhuber, 1997).
- Tiefe Stapel brauchen Residualverbindungen, um trainierbar zu sein (Wu et al., 2016).

### Vergleich

| Modell | Speichermechanismus | Parallel über die Zeit | Typischer Einsatz |
|---|---|---|---|
| Einfaches RNN ([[recurrent-neural-networks\|RNN]]) | verborgener Zustand durch eine Nichtlinearität | nein | kurze Abhängigkeiten |
| LSTM | gegateter Zellzustand mit additivem Update | nein | lange Abhängigkeiten in Sequenzen |
| GRU | gekoppeltes Update-Gate, keine eigene Output-Aktivierung | nein | wie LSTM mit weniger Parametern |
| [[attention-and-transformers\|Transformer]] | Attention über alle Positionen | ja | Sprachmodellierung, Übersetzung |
| [[hidden-markov-models\|HMM]] | endliche Menge diskreter Zustände | nein | Tagging mit wenig annotierten Daten |

Quellen: Greff et al. (2017), Hochreiter & Schmidhuber (1997), Vaswani et al. (2017).

### In der Praxis

Greff et al. (2017) verglichen die Vanilla-LSTM mit acht Varianten auf Spracherkennung, Handschrifterkennung und Musikmodellierung, mit per [[hyperparameter-optimisation|Random Search]] gefundenen Hyperparametern. Keine Variante verbesserte die Vanilla-LSTM signifikant; das Entfernen des Forget-Gates oder der Output-Aktivierung verschlechterte alle drei Aufgaben, während das Koppeln von Input- und Forget-Gate oder das Weglassen der Peepholes das Modell ohne signifikanten Verlust vereinfachte. Die Lernrate war der wichtigste Hyperparameter, gefolgt von der Netzgröße, und Momentum spielte kaum eine Rolle (Greff et al., 2017). Heute finden sich LSTMs noch in Pipelines für Sequence Labelling und Prognosen sowie in früheren Architekturen wie der Sparsely-Gated-[[mixture-of-experts|Mixture-of-Experts]]-Schicht zwischen LSTM-Schichten, während große Sprachmodelle auf Transformern beruhen ([[large-language-models|große Sprachmodelle]]).

### Merksatz

Eine LSTM hält einen Zellzustand, der additiv aktualisiert und von gelernten Gates bewacht wird, wodurch Gradienten lange Sequenzen überdauern; Forget-Gate und Output-Aktivierung sind ihre wichtigsten Bestandteile.

### Quellen

- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8), 1735–1780. [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
- Greff, K., Srivastava, R. K., Koutník, J., Steunebrink, B. R. & Schmidhuber, J. (2017). *LSTM: A Search Space Odyssey.* IEEE Transactions on Neural Networks and Learning Systems. [arXiv:1503.04069](https://arxiv.org/abs/1503.04069)
- Graves, A. (2013). *Generating Sequences With Recurrent Neural Networks.* [arXiv:1308.0850](https://arxiv.org/abs/1308.0850)
- Huang, Z., Xu, W. & Yu, K. (2015). *Bidirectional LSTM-CRF Models for Sequence Tagging.* [arXiv:1508.01991](https://arxiv.org/abs/1508.01991)
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation.* [arXiv:1609.08144](https://arxiv.org/abs/1609.08144)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
