---
title_en: Recurrent Neural Networks and Time Series
title_de: RNN und Zeitreihen
entity_type: Method
sources:
- https://www.deeplearningbook.org/
- https://doi.org/10.1109/72.279181
- https://doi.org/10.1162/neco.1997.9.8.1735
- https://arxiv.org/abs/1406.1078
- https://arxiv.org/abs/1409.3215
- https://otexts.com/fpp3/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Recurrent neural networks (RNNs) process sequences step by step and carry a hidden state that summarises what they have seen so far, sharing the same weights at every time step (Goodfellow et al., 2016). They are trained with back-propagation through time, but long-term dependencies are hard to learn because gradients vanish or explode over many steps (Bengio et al., 1994). Gated variants such as the LSTM (Hochreiter & Schmidhuber, 1997) and GRU (Cho et al., 2014) address this and powered sequence-to-sequence models for translation (Sutskever et al., 2014), before Transformers largely replaced them in language processing.

### How it works

At each time step, the RNN combines the current input with its previous hidden state to compute a new hidden state and, if required, an output. The same weights are reused at every step, so one network handles sequences of any length.

```text
1. Recurrence and hidden state
▼
2. Back-propagation through time
▼
3. Vanishing and exploding gradients
▼
4. Gated units: LSTM and GRU
▼
5. Sequence-to-sequence models
▼
6. RNNs for time series
```

#### 1. Recurrence and hidden state

An RNN processes a sequence one element at a time and updates a hidden state that serves as a summary of the past (Goodfellow et al., 2016). Because the parameters are shared across time steps, the model generalises across positions and sequence lengths, much as a CNN shares filters across positions in an image ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]).

#### 2. Back-propagation through time

To train an RNN, the network is unrolled over the sequence into a deep feedforward graph with one copy per time step, and back-propagation is applied to this unrolled graph; this is called back-propagation through time (Goodfellow et al., 2016; [[neural-network-training|Training Neural Networks]]).

#### 3. Vanishing and exploding gradients

Bengio et al. (1994) showed why gradient-based learning becomes increasingly difficult as the dependencies to be captured span longer intervals: gradients propagated back over many steps tend to vanish or explode. This exposes a trade-off between efficient learning by gradient descent and holding on to information over long periods.

#### 4. Gated units: LSTM and GRU

The long short-term memory (LSTM) introduces memory cells whose content is controlled by multiplicative gates; this keeps the error flow constant over long time lags and allows learning dependencies over more than 1000 time steps, where earlier RNNs failed (Hochreiter & Schmidhuber, 1997). Cho et al. (2014) proposed a simpler gated unit, today known as the GRU, as part of their RNN encoder-decoder.

#### 5. Sequence-to-sequence models

In an encoder-decoder, one RNN encodes an input sequence into a fixed-length vector and another decodes it into an output sequence; both are trained jointly to maximise the probability of the target sequence (Cho et al., 2014). Sutskever et al. (2014) used deep LSTMs this way for English-to-French translation on WMT'14 and reached a BLEU score of 34.8, compared with 33.3 for a phrase-based system; reversing the order of the source words markedly improved performance by introducing short-term dependencies. The fixed-length vector became a bottleneck that attention later removed ([[attention-and-transformers|Attention and Transformers]]).

#### 6. RNNs for time series

RNNs also model numerical time series, since they process observations in order and keep a state of the past (Goodfellow et al., 2016). For forecasting, neural networks compete with classical statistical models such as exponential smoothing and ARIMA, and forecasts must be evaluated on later data with time series cross-validation (Hyndman & Athanasopoulos, 2021; [[time-series-analysis|Time Series Analysis]]).

#### Origin and variants

Bengio et al. (1994) analysed why long-term dependencies are hard to learn, the LSTM (Hochreiter & Schmidhuber, 1997) addressed the problem, and the GRU-based encoder-decoder (Cho et al., 2014) and sequence-to-sequence LSTMs (Sutskever et al., 2014) made RNNs the standard for machine translation until attention-based Transformers took over.

### When to use it

- When data arrives as a sequence and the order matters, such as sensor data or text (Goodfellow et al., 2016).
- When dependencies span many steps, gated units such as LSTM or GRU are needed (Hochreiter & Schmidhuber, 1997; Cho et al., 2014).
- For forecasting numerical series, RNNs should be compared with statistical baselines (Hyndman & Athanasopoulos, 2021).

### Strengths and limitations

**Strengths**
- Handle sequences of any length with shared weights (Goodfellow et al., 2016).
- LSTMs learn dependencies over more than 1000 time steps (Hochreiter & Schmidhuber, 1997).
- Sequence-to-sequence LSTMs translated long sentences without difficulty (Sutskever et al., 2014).

**Limitations**
- Plain RNNs suffer from vanishing and exploding gradients (Bengio et al., 1994).
- Steps must be processed in order, which limits parallel training (Goodfellow et al., 2016).
- Encoding a whole input into one fixed-length vector is a bottleneck (Cho et al., 2014).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Plain RNN | Single hidden state updated each step (Goodfellow et al., 2016) | Short dependencies |
| LSTM | Gated memory cells keep error flow constant (Hochreiter & Schmidhuber, 1997) | Long dependencies |
| GRU | Simpler gated unit (Cho et al., 2014) | Long dependencies with fewer parameters |
| Encoder-decoder RNN | One RNN encodes, another decodes (Sutskever et al., 2014) | Sequence-to-sequence tasks such as translation |

### In practice

Gated units are the standard way to learn dependencies over long sequences, since plain RNNs suffer from vanishing and exploding gradients (Bengio et al., 1994; Hochreiter & Schmidhuber, 1997). For language tasks, Transformers have largely replaced RNNs ([[attention-and-transformers|Attention and Transformers]]); for time series, models are compared against simple statistical baselines on data split in time order (Hyndman & Athanasopoulos, 2021).

### Key takeaway

RNNs process sequences step by step with a shared state; gated units such as the LSTM make long dependencies learnable.

### Sources

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Bengio, Y., Simard, P. & Frasconi, P. (1994). *Learning long-term dependencies with gradient descent is difficult.* IEEE Transactions on Neural Networks 5(2). [doi:10.1109/72.279181](https://doi.org/10.1109/72.279181)
- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8). [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
- Cho, K. et al. (2014). *Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation.* EMNLP 2014. [arXiv:1406.1078](https://arxiv.org/abs/1406.1078)
- Sutskever, I. et al. (2014). *Sequence to Sequence Learning with Neural Networks.* NeurIPS 2014. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Rekurrente neuronale Netze (RNNs) verarbeiten Sequenzen Schritt für Schritt und führen einen verborgenen Zustand mit, der das bisher Gesehene zusammenfasst; dabei nutzen sie in jedem Zeitschritt dieselben Gewichte (Goodfellow et al., 2016). Sie werden mit Backpropagation Through Time trainiert, doch weitreichende Abhängigkeiten sind schwer zu lernen, weil Gradienten über viele Schritte verschwinden oder explodieren (Bengio et al., 1994). Gesteuerte Varianten wie das LSTM (Hochreiter & Schmidhuber, 1997) und die GRU (Cho et al., 2014) lösen das und trugen Sequence-to-Sequence-Modelle für Übersetzung (Sutskever et al., 2014), bevor Transformer sie in der Sprachverarbeitung weitgehend ablösten.

### Funktionsweise

In jedem Zeitschritt verbindet das RNN die aktuelle Eingabe mit seinem vorherigen verborgenen Zustand, berechnet daraus einen neuen Zustand und bei Bedarf eine Ausgabe. Dieselben Gewichte werden in jedem Schritt wiederverwendet, sodass ein Netz Sequenzen beliebiger Länge verarbeitet.

```text
1. Rekurrenz und verborgener Zustand
▼
2. Backpropagation Through Time
▼
3. Verschwindende und explodierende Gradienten
▼
4. Gesteuerte Einheiten: LSTM und GRU
▼
5. Sequence-to-Sequence-Modelle
▼
6. RNNs für Zeitreihen
```

#### 1. Rekurrenz und verborgener Zustand

Ein RNN verarbeitet eine Sequenz Element für Element und aktualisiert einen verborgenen Zustand, der als Zusammenfassung der Vergangenheit dient (Goodfellow et al., 2016). Da die Parameter über die Zeitschritte geteilt werden, generalisiert das Modell über Positionen und Sequenzlängen hinweg, ähnlich wie ein CNN Filter über die Positionen eines Bildes teilt ([[convolutional-neural-networks|Convolutional Neural Networks (CNN)]]).

#### 2. Backpropagation Through Time

Zum Training wird das Netz über die Sequenz zu einem tiefen Feedforward-Graphen mit einer Kopie je Zeitschritt aufgefaltet, und Backpropagation wird auf diesen aufgefalteten Graphen angewendet; das heißt Backpropagation Through Time (Goodfellow et al., 2016; [[neural-network-training|Training neuronaler Netze]]).

#### 3. Verschwindende und explodierende Gradienten

Bengio et al. (1994) zeigten, warum gradientenbasiertes Lernen immer schwieriger wird, je länger die zu erfassenden Abhängigkeiten sind: Über viele Schritte zurückpropagierte Gradienten neigen dazu zu verschwinden oder zu explodieren. Daraus ergibt sich ein Zielkonflikt zwischen effizientem Lernen per Gradientenabstieg und dem Festhalten von Information über lange Zeiträume.

#### 4. Gesteuerte Einheiten: LSTM und GRU

Das Long Short-Term Memory (LSTM) führt Speicherzellen ein, deren Inhalt durch multiplikative Gates gesteuert wird; das hält den Fehlerfluss über lange Zeitabstände konstant und erlaubt, Abhängigkeiten über mehr als 1000 Zeitschritte zu lernen, woran frühere RNNs scheiterten (Hochreiter & Schmidhuber, 1997). Cho et al. (2014) schlugen als Teil ihres RNN-Encoder-Decoders eine einfachere gesteuerte Einheit vor, die heute als GRU bekannt ist.

#### 5. Sequence-to-Sequence-Modelle

In einem Encoder-Decoder kodiert ein RNN eine Eingabesequenz in einen Vektor fester Länge, und ein anderes dekodiert ihn in eine Ausgabesequenz; beide werden gemeinsam so trainiert, dass die Wahrscheinlichkeit der Zielsequenz maximal wird (Cho et al., 2014). Sutskever et al. (2014) nutzten tiefe LSTMs so für die Übersetzung Englisch-Französisch auf WMT'14 und erreichten einen BLEU-Wert von 34,8 gegenüber 33,3 für ein phrasenbasiertes System; die Umkehr der Wortreihenfolge im Quelltext verbesserte die Leistung deutlich, weil sie kurze Abhängigkeiten zwischen Quelle und Ziel schuf. Der Vektor fester Länge wurde zu einem Engpass, den später Attention beseitigte ([[attention-and-transformers|Attention und Transformer]]).

#### 6. RNNs für Zeitreihen

RNNs modellieren auch numerische Zeitreihen, da sie Beobachtungen in ihrer Reihenfolge verarbeiten und einen Zustand der Vergangenheit führen (Goodfellow et al., 2016). Bei Prognosen konkurrieren neuronale Netze mit klassischen statistischen Modellen wie exponentieller Glättung und ARIMA, und Prognosen müssen auf späteren Daten mit Zeitreihen-Kreuzvalidierung bewertet werden (Hyndman & Athanasopoulos, 2021; [[time-series-analysis|Zeitreihenanalyse]]).

#### Ursprung und Varianten

Bengio et al. (1994) analysierten, warum weitreichende Abhängigkeiten schwer zu lernen sind, das LSTM (Hochreiter & Schmidhuber, 1997) löste das Problem, und der Encoder-Decoder mit GRU (Cho et al., 2014) sowie Sequence-to-Sequence-LSTMs (Sutskever et al., 2014) machten RNNs zum Standard der maschinellen Übersetzung, bis attention-basierte Transformer übernahmen.

### Wann einsetzen

- Wenn Daten als Sequenz vorliegen und die Reihenfolge zählt, etwa Sensordaten oder Text (Goodfellow et al., 2016).
- Wenn Abhängigkeiten viele Schritte überspannen, sind gesteuerte Einheiten wie LSTM oder GRU nötig (Hochreiter & Schmidhuber, 1997; Cho et al., 2014).
- Bei der Prognose numerischer Reihen sollten RNNs mit statistischen Baselines verglichen werden (Hyndman & Athanasopoulos, 2021).

### Stärken und Grenzen

**Stärken**
- Verarbeiten Sequenzen beliebiger Länge mit geteilten Gewichten (Goodfellow et al., 2016).
- LSTMs lernen Abhängigkeiten über mehr als 1000 Zeitschritte (Hochreiter & Schmidhuber, 1997).
- Sequence-to-Sequence-LSTMs übersetzten auch lange Sätze ohne Schwierigkeiten (Sutskever et al., 2014).

**Einschränkungen**
- Einfache RNNs leiden unter verschwindenden und explodierenden Gradienten (Bengio et al., 1994).
- Die Schritte müssen nacheinander verarbeitet werden, was paralleles Training begrenzt (Goodfellow et al., 2016).
- Eine ganze Eingabe in einen Vektor fester Länge zu kodieren ist ein Engpass (Cho et al., 2014).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Einfaches RNN | Ein verborgener Zustand, der in jedem Schritt aktualisiert wird (Goodfellow et al., 2016) | Kurze Abhängigkeiten |
| LSTM | Gesteuerte Speicherzellen halten den Fehlerfluss konstant (Hochreiter & Schmidhuber, 1997) | Lange Abhängigkeiten |
| GRU | Einfachere gesteuerte Einheit (Cho et al., 2014) | Lange Abhängigkeiten mit weniger Parametern |
| Encoder-Decoder-RNN | Ein RNN kodiert, ein anderes dekodiert (Sutskever et al., 2014) | Sequence-to-Sequence-Aufgaben wie Übersetzung |

### In der Praxis

Gesteuerte Einheiten sind der Standardweg, um Abhängigkeiten über lange Sequenzen zu lernen, da einfache RNNs unter verschwindenden und explodierenden Gradienten leiden (Bengio et al., 1994; Hochreiter & Schmidhuber, 1997). In der Sprachverarbeitung haben Transformer RNNs weitgehend abgelöst ([[attention-and-transformers|Attention und Transformer]]); bei Zeitreihen werden Modelle auf zeitlich geordnet aufgeteilten Daten gegen einfache statistische Baselines verglichen (Hyndman & Athanasopoulos, 2021).

### Merksatz

RNNs verarbeiten Sequenzen Schritt für Schritt mit einem geteilten Zustand; gesteuerte Einheiten wie das LSTM machen weitreichende Abhängigkeiten lernbar.

### Quellen

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning.* MIT Press. [online edition](https://www.deeplearningbook.org/)
- Bengio, Y., Simard, P. & Frasconi, P. (1994). *Learning long-term dependencies with gradient descent is difficult.* IEEE Transactions on Neural Networks 5(2). [doi:10.1109/72.279181](https://doi.org/10.1109/72.279181)
- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8). [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
- Cho, K. et al. (2014). *Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation.* EMNLP 2014. [arXiv:1406.1078](https://arxiv.org/abs/1406.1078)
- Sutskever, I. et al. (2014). *Sequence to Sequence Learning with Neural Networks.* NeurIPS 2014. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)
