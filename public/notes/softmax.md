---
title_en: Softmax
title_de: Softmax
entity_type: Concept
aliases:
- Softmax function
- Softmax layer
- Softargmax
- Normalised exponential
- Log-softmax
sources:
- https://web.stanford.edu/~jurafsky/slp3/4.pdf
- https://web.stanford.edu/~jurafsky/slp3/7.pdf
- https://www.deeplearningbook.org/contents/mlp.html
- https://www.deeplearningbook.org/contents/numerical.html
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/1503.02531
- https://arxiv.org/abs/1706.04599
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The softmax function turns a vector of K real-valued scores (logits) into a probability distribution: it exponentiates each score and divides by the sum of all exponentials, so every output lies between 0 and 1 and the outputs sum to 1 (Jurafsky & Martin, 2026). It generalises the sigmoid to more than two classes and is the standard output layer of classifiers and language models, where it gives the probability of every token in the vocabulary (Goodfellow et al., 2016; Jurafsky & Martin, 2026). Inside Transformers, a softmax over scaled dot products turns attention scores into weights (Vaswani et al., 2017), and dividing the logits by a temperature makes the distribution sharper or flatter (Jurafsky & Martin, 2026; Hinton et al., 2015).

### How it works

```text
logits z = [z₁ … z_K]              (any real numbers, e.g. z = W h + b)
   ▼  subtract max_j z_j            (numerical stability, result unchanged)
   ▼  exponentiate                  exp(z_i)
   ▼  normalise                     softmax(z)_i = exp(z_i) / Σ_j exp(z_j)
probabilities ŷ (each in (0,1), sum = 1)
   ▼
training: −log ŷ_correct  (cross-entropy)      inference: argmax, sampling, or attention weights
```

#### 1. Definition

For a vector `z` of K values, `softmax(z_i) = exp(z_i) / Σ_{j=1..K} exp(z_j)`; the denominator normalises the exponentials into probabilities (Jurafsky & Martin, 2026). Like the sigmoid it pushes the largest input towards 1 and suppresses smaller ones: in Jurafsky and Martin's example, `z = [0.6, 1.1, −1.5, 1.2, 3.2, −1.1]` becomes roughly `[0.05, 0.09, 0.01, 0.1, 0.74, 0.01]`. The inputs are called logits (Jurafsky & Martin, 2026). Goodfellow et al. (2016) note that the function is a softened, differentiable version of the arg max rather than of the max and would better be called "softargmax"; when one input is much larger than the others it becomes winner-take-all.

#### 2. Relation to the sigmoid

With two classes, defining `P(y = 1 | x) = σ(z)` is the same as a softmax over a two-dimensional z with one element fixed at 0 (Goodfellow et al., 2016). In general, K outputs that must sum to 1 need only K − 1 free parameters, but the overparametrised version with K logits is simpler and in practice rarely differs (Goodfellow et al., 2016). In [[logistic-regression|multinomial logistic regression]], each class has its own weight vector and `ŷ = softmax(Wx + b)` (Jurafsky & Martin, 2026).

#### 3. Training with the log-likelihood

The softmax pairs naturally with the [[cross-entropy|cross-entropy]] (negative log-likelihood) loss, because the log undoes the exponential: `log softmax(z)_i = z_i − log Σ_j exp(z_j)` (Goodfellow et al., 2016). The first term always contributes directly to the loss and cannot saturate, so learning continues even when the correct class has a very low probability; the second term, roughly `max_j z_j`, strongly penalises the most confident wrong prediction (Goodfellow et al., 2016). Losses without a log, such as squared error, can fail to train a softmax output when its inputs become very negative and the gradient vanishes (Goodfellow et al., 2016).

#### 4. Numerical stability

Computed naively, `exp(z)` overflows for large inputs and underflows to zero for very negative ones, which can make the denominator zero (Goodfellow et al., 2016). Since the softmax is unchanged when the same constant is added to all inputs, implementations compute `softmax(z − max_i z_i)`: the largest exponent is then 0 and at least one term in the denominator is 1 (Goodfellow et al., 2016). The log-softmax needs its own stable implementation instead of taking the log of the softmax output, which could give −∞ (Goodfellow et al., 2016).

#### 5. Softmax in language models and attention

At the top of a language model, the final hidden state is multiplied by the unembedding matrix to give one logit per vocabulary token, and a softmax turns these into the distribution from which the next token is chosen (Jurafsky & Martin, 2026; [[large-language-models|large language models]]). In scaled dot-product attention, `Attention(Q, K, V) = softmax(QKᵀ / √d_k) V`; the scaling by `1/√d_k` counteracts large dot products that would push the softmax into regions with extremely small gradients (Vaswani et al., 2017; [[attention-and-transformers|attention]]).

#### 6. Temperature

Dividing the logits by a temperature τ before the softmax, `softmax(u / τ)`, reshapes the distribution: τ < 1 sharpens it towards greedy choice, τ > 1 flattens it towards uniform (Jurafsky & Martin, 2026). With logits `[1.2, 0.9, 0.1, −0.5]`, the top probability is 0.44 at τ = 1, 0.59 at τ = 0.5 and 0.95 at τ = 0.1 (Jurafsky & Martin, 2026). [[knowledge-distillation|Knowledge distillation]] uses a high temperature to produce soft targets from a large model and trains the small model at the same temperature (Hinton et al., 2015); [[temperature-scaling|temperature scaling]], a single-parameter variant of Platt scaling, uses one temperature to calibrate a trained classifier and was surprisingly effective on most data sets Guo et al. (2017) tested.

#### Origin and variants

Goodfellow et al. (2016) relate the softmax's competition between units to lateral inhibition between neurons. Bridle (1990), cited by Goodfellow et al. (2016), showed that squared error is a poor loss for softmax units. Variants change how the logits are produced or scaled rather than the function itself, for example temperature and the attention scaling factor.

### When to use it

- As the output layer of a classifier over K mutually exclusive classes ([[neural-networks|neural networks]], [[classification|classification]]).
- To produce next-token probabilities in language models and decoding (Jurafsky & Martin, 2026).
- To normalise attention scores into weights (Vaswani et al., 2017).

### Strengths and limitations

**Strengths**
- Differentiable, turns any scores into a valid distribution (Goodfellow et al., 2016).
- Works well with the log-likelihood, which cancels the exponential and avoids saturation (Goodfellow et al., 2016).
- Temperature gives a simple control over sharpness (Jurafsky & Martin, 2026).

**Limitations**
- Saturates when input differences are extreme, so losses that do not undo the exponential learn poorly (Goodfellow et al., 2016).
- Needs stable implementation to avoid overflow and underflow (Goodfellow et al., 2016).
- Softmax outputs of modern neural networks are often poorly calibrated (Guo et al., 2017).
- A language model computes one logit per vocabulary token at every step (Jurafsky & Martin, 2026).

### Comparison

| Function | Input | Output | Use |
|---|---|---|---|
| Sigmoid | one score | probability of one class | binary or multi-label |
| Softmax | K scores | distribution over K classes | multi-class, next token, attention |
| Arg max | K scores | one-hot vector | final hard decision, not differentiable |
| Softmax with temperature τ | K scores / τ | sharper or flatter distribution | sampling, distillation, calibration |

Sources: Goodfellow et al. (2016), Jurafsky & Martin (2026), Hinton et al. (2015).

### In practice

Most users can rely on low-level libraries that provide numerically stable implementations of softmax and log-softmax (Goodfellow et al., 2016). Depth, width, weight decay and batch normalisation influence how well a network's softmax outputs are calibrated, so when these outputs drive decisions, calibration is checked on held-out data (Guo et al., 2017; [[classification-metrics|classification metrics]]).

### Key takeaway

Softmax exponentiates and normalises a score vector into probabilities; it is trained with the log-likelihood, implemented with the max-subtraction trick, and controlled at inference with a temperature.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 6: Deep Feedforward Networks. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 4: Numerical Computation. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/numerical.html)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Softmax-Funktion macht aus einem Vektor von K reellwertigen Scores (Logits) eine Wahrscheinlichkeitsverteilung: Sie potenziert jeden Score und teilt durch die Summe aller Exponentialwerte, sodass jede Ausgabe zwischen 0 und 1 liegt und die Ausgaben sich zu 1 summieren (Jurafsky & Martin, 2026). Sie verallgemeinert die Sigmoidfunktion auf mehr als zwei Klassen und ist die Standard-Ausgabeschicht von Klassifikatoren und Sprachmodellen, wo sie die Wahrscheinlichkeit jedes Tokens im Vokabular angibt (Goodfellow et al., 2016; Jurafsky & Martin, 2026). In Transformern macht eine Softmax über skalierte Skalarprodukte aus Attention-Scores Gewichte (Vaswani et al., 2017), und das Teilen der Logits durch eine Temperatur macht die Verteilung schärfer oder flacher (Jurafsky & Martin, 2026; Hinton et al., 2015).

### Funktionsweise

```text
Logits z = [z₁ … z_K]              (beliebige reelle Zahlen, z. B. z = W h + b)
   ▼  max_j z_j abziehen            (numerische Stabilität, Ergebnis unverändert)
   ▼  potenzieren                   exp(z_i)
   ▼  normalisieren                 softmax(z)_i = exp(z_i) / Σ_j exp(z_j)
Wahrscheinlichkeiten ŷ (jeweils in (0,1), Summe = 1)
   ▼
Training: −log ŷ_richtig  (Cross-Entropy)      Inferenz: Argmax, Sampling oder Attention-Gewichte
```

#### 1. Definition

Für einen Vektor `z` aus K Werten gilt `softmax(z_i) = exp(z_i) / Σ_{j=1..K} exp(z_j)`; der Nenner normalisiert die Exponentialwerte zu Wahrscheinlichkeiten (Jurafsky & Martin, 2026). Wie die Sigmoidfunktion drückt sie den größten Eingabewert Richtung 1 und unterdrückt kleinere: Im Beispiel von Jurafsky und Martin wird `z = [0,6, 1,1, −1,5, 1,2, 3,2, −1,1]` zu etwa `[0,05, 0,09, 0,01, 0,1, 0,74, 0,01]`. Die Eingaben heißen Logits (Jurafsky & Martin, 2026). Goodfellow et al. (2016) merken an, dass die Funktion eine geglättete, differenzierbare Version des Arg max ist, nicht des Max, und besser „Softargmax“ hieße; ist ein Eingabewert viel größer als die übrigen, wird sie zu einem Winner-take-all.

#### 2. Verhältnis zur Sigmoidfunktion

Bei zwei Klassen ist `P(y = 1 | x) = σ(z)` dasselbe wie eine Softmax über ein zweidimensionales z, dessen eines Element auf 0 festgelegt ist (Goodfellow et al., 2016). Allgemein brauchen K Ausgaben, die sich zu 1 summieren müssen, nur K − 1 freie Parameter, doch die überparametrisierte Version mit K Logits ist einfacher und unterscheidet sich in der Praxis selten (Goodfellow et al., 2016). In der [[logistic-regression|multinomialen logistischen Regression]] hat jede Klasse einen eigenen Gewichtsvektor, und `ŷ = softmax(Wx + b)` (Jurafsky & Martin, 2026).

#### 3. Training mit der Log-Likelihood

Die Softmax passt natürlich zum [[cross-entropy|Cross-Entropy]]-Verlust (negative Log-Likelihood), weil der Logarithmus die Exponentialfunktion aufhebt: `log softmax(z)_i = z_i − log Σ_j exp(z_j)` (Goodfellow et al., 2016). Der erste Term trägt immer direkt zum Verlust bei und kann nicht sättigen, sodass das Lernen weitergeht, auch wenn die richtige Klasse eine sehr kleine Wahrscheinlichkeit hat; der zweite Term, ungefähr `max_j z_j`, bestraft die selbstsicherste falsche Vorhersage stark (Goodfellow et al., 2016). Verluste ohne Logarithmus, etwa der quadratische Fehler, können eine Softmax-Ausgabe nicht trainieren, wenn ihre Eingaben sehr negativ werden und der Gradient verschwindet (Goodfellow et al., 2016).

#### 4. Numerische Stabilität

Naiv berechnet läuft `exp(z)` bei großen Eingaben über und bei sehr negativen auf null, was den Nenner null werden lassen kann (Goodfellow et al., 2016). Da die Softmax sich nicht ändert, wenn zu allen Eingaben dieselbe Konstante addiert wird, berechnen Implementierungen `softmax(z − max_i z_i)`: Der größte Exponent ist dann 0, und mindestens ein Term im Nenner ist 1 (Goodfellow et al., 2016). Die Log-Softmax braucht eine eigene stabile Implementierung, statt den Logarithmus der Softmax-Ausgabe zu nehmen, was −∞ ergeben könnte (Goodfellow et al., 2016).

#### 5. Softmax in Sprachmodellen und Attention

An der Spitze eines Sprachmodells wird der letzte verborgene Zustand mit der Unembedding-Matrix multipliziert, was einen Logit pro Token des Vokabulars ergibt, und eine Softmax macht daraus die Verteilung, aus der das nächste Token gewählt wird (Jurafsky & Martin, 2026; [[large-language-models|große Sprachmodelle]]). In der Scaled Dot-Product Attention gilt `Attention(Q, K, V) = softmax(QKᵀ / √d_k) V`; die Skalierung mit `1/√d_k` wirkt großen Skalarprodukten entgegen, die die Softmax in Bereiche mit extrem kleinen Gradienten drängen würden (Vaswani et al., 2017; [[attention-and-transformers|Attention]]).

#### 6. Temperatur

Teilt man die Logits vor der Softmax durch eine Temperatur τ, `softmax(u / τ)`, ändert sich die Form der Verteilung: τ < 1 schärft sie Richtung gieriger Auswahl, τ > 1 glättet sie Richtung Gleichverteilung (Jurafsky & Martin, 2026). Mit den Logits `[1,2, 0,9, 0,1, −0,5]` beträgt die höchste Wahrscheinlichkeit 0,44 bei τ = 1, 0,59 bei τ = 0,5 und 0,95 bei τ = 0,1 (Jurafsky & Martin, 2026). [[knowledge-distillation|Knowledge Distillation]] nutzt eine hohe Temperatur, um aus einem großen Modell weiche Zielwerte zu erzeugen, und trainiert das kleine Modell mit derselben Temperatur (Hinton et al., 2015); [[temperature-scaling|Temperature Scaling]], eine Variante des Platt Scaling mit einem einzigen Parameter, nutzt eine Temperatur, um einen trainierten Klassifikator zu kalibrieren, und war auf den meisten von Guo et al. (2017) getesteten Datensätzen überraschend wirksam.

#### Ursprung und Varianten

Goodfellow et al. (2016) vergleichen den Wettbewerb zwischen den Einheiten der Softmax mit der lateralen Hemmung zwischen Neuronen. Bridle (1990), zitiert bei Goodfellow et al. (2016), zeigte, dass der quadratische Fehler ein schlechter Verlust für Softmax-Einheiten ist. Varianten ändern meist, wie die Logits erzeugt oder skaliert werden, nicht die Funktion selbst, etwa die Temperatur und der Skalierungsfaktor der Attention.

### Wann einsetzen

- Als Ausgabeschicht eines Klassifikators über K sich gegenseitig ausschließende Klassen ([[neural-networks|neuronale Netze]], [[classification|Klassifikation]]).
- Um in Sprachmodellen und beim Decoding Wahrscheinlichkeiten für das nächste Token zu erzeugen (Jurafsky & Martin, 2026).
- Um Attention-Scores zu Gewichten zu normalisieren (Vaswani et al., 2017).

### Stärken und Grenzen

**Stärken**
- Differenzierbar, macht aus beliebigen Scores eine gültige Verteilung (Goodfellow et al., 2016).
- Passt gut zur Log-Likelihood, die die Exponentialfunktion aufhebt und Sättigung vermeidet (Goodfellow et al., 2016).
- Die Temperatur bietet eine einfache Steuerung der Schärfe (Jurafsky & Martin, 2026).

**Grenzen**
- Sättigt bei extremen Unterschieden der Eingaben, sodass Verluste, die die Exponentialfunktion nicht aufheben, schlecht lernen (Goodfellow et al., 2016).
- Braucht eine stabile Implementierung gegen Über- und Unterlauf (Goodfellow et al., 2016).
- Softmax-Ausgaben moderner neuronaler Netze sind oft schlecht kalibriert (Guo et al., 2017).
- Ein Sprachmodell berechnet in jedem Schritt einen Logit pro Token des Vokabulars (Jurafsky & Martin, 2026).

### Vergleich

| Funktion | Eingabe | Ausgabe | Einsatz |
|---|---|---|---|
| Sigmoid | ein Score | Wahrscheinlichkeit einer Klasse | binär oder Multi-Label |
| Softmax | K Scores | Verteilung über K Klassen | Mehrklassen, nächstes Token, Attention |
| Arg max | K Scores | One-hot-Vektor | finale harte Entscheidung, nicht differenzierbar |
| Softmax mit Temperatur τ | K Scores / τ | schärfere oder flachere Verteilung | Sampling, Distillation, Kalibrierung |

Quellen: Goodfellow et al. (2016), Jurafsky & Martin (2026), Hinton et al. (2015).

### In der Praxis

Die meisten Nutzenden können sich auf Low-Level-Bibliotheken verlassen, die numerisch stabile Implementierungen von Softmax und Log-Softmax bereitstellen (Goodfellow et al., 2016). Tiefe, Breite, Weight Decay und Batch Normalization beeinflussen, wie gut die Softmax-Ausgaben eines Netzes kalibriert sind; steuern diese Ausgaben Entscheidungen, wird die Kalibrierung daher auf zurückgehaltenen Daten geprüft (Guo et al., 2017; [[classification-metrics|Klassifikationsmetriken]]).

### Merksatz

Softmax potenziert und normalisiert einen Score-Vektor zu Wahrscheinlichkeiten; sie wird mit der Log-Likelihood trainiert, mit dem Abzug des Maximums stabil implementiert und bei der Inferenz über eine Temperatur gesteuert.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 6: Deep Feedforward Networks. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 4: Numerical Computation. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/numerical.html)
- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
