---
title_en: Adam Optimiser
title_de: Adam-Optimierer
entity_type: Method
aliases:
- Adam
- Adam optimizer
- Adaptive moment estimation
- AdamW
- Decoupled weight decay
- AMSGrad
sources:
- https://arxiv.org/abs/1412.6980
- https://arxiv.org/abs/1711.05101
- https://arxiv.org/abs/1904.09237
- https://arxiv.org/abs/1609.04747
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Adam (adaptive moment estimation) is a first-order optimisation method for stochastic objectives that keeps exponential moving averages of the gradient and of the squared gradient for every parameter and uses them to give each parameter its own step size (Kingma & Ba, 2015). It combines the momentum idea with the per-parameter scaling of AdaGrad and RMSProp, needs little memory and little tuning, and is a standard choice for training deep [[neural-networks|neural networks]] (Kingma & Ba, 2015; Ruder, 2016). AdamW decouples weight decay from the gradient update, which fixes the poor interaction of [[ridge-and-lasso|L2 regularisation]] with Adam (Loshchilov & Hutter, 2019).

### How it works

```text
m₀ = 0, v₀ = 0, t = 0                      defaults: α = 0.001, β₁ = 0.9, β₂ = 0.999, ε = 10⁻⁸
repeat:
    t ← t + 1
    g_t = ∇θ f_t(θ_{t−1})                   gradient on the current mini-batch
    m_t = β₁ m_{t−1} + (1 − β₁) g_t          1st moment: mean of gradients
    v_t = β₂ v_{t−1} + (1 − β₂) g_t²         2nd raw moment: mean of squared gradients
    m̂_t = m_t / (1 − β₁ᵗ),  v̂_t = v_t / (1 − β₂ᵗ)     bias correction
    θ_t = θ_{t−1} − α · m̂_t / (√v̂_t + ε)     element-wise update
```

#### 1. Moment estimates

Adam keeps two moving averages per parameter: m_t, an estimate of the mean of the gradients, and v_t, an estimate of their uncentred variance (Kingma & Ba, 2015). β₁ and β₂ set how fast they forget old gradients; m_t plays the role of momentum in [[gradient-descent|gradient descent]], and v_t the role of the squared-gradient average in RMSProp (Ruder, 2016).

#### 2. Bias correction

Because both averages start at zero, they are biased towards zero in the first steps, especially when β is close to 1; dividing by `1 − βᵗ` corrects this (Kingma & Ba, 2015). Kingma and Ba (2015) report that this correction helps Adam slightly outperform RMSProp towards the end of optimisation, when gradients become sparser (Ruder, 2016).

#### 3. The update and its step size

The update divides the corrected mean by the square root of the corrected second moment, so each parameter moves by roughly the step size α in the direction of its recent gradients (Kingma & Ba, 2015). The effective step is approximately bounded by α, which acts like a trust region and makes the right order of magnitude of α easier to choose; it is invariant to rescaling the gradients, and the ratio `m̂/√v̂`, which Kingma and Ba call a signal-to-noise ratio, shrinks near an optimum, giving a form of automatic annealing (Kingma & Ba, 2015). Parameters with rare but large gradients therefore get relatively larger updates than with plain SGD.

#### 4. Weight decay: Adam versus AdamW

For plain SGD, L2 regularisation and weight decay are equivalent once rescaled by the learning rate; for Adam they are not, because the L2 gradient is also divided by `√v̂`, so weights with large past gradients are regularised less (Loshchilov & Hutter, 2019). Common implementations nevertheless called L2 regularisation "weight decay". AdamW applies the decay directly to the weights, separately from the gradient-based step; this made the optimal weight decay independent of the learning rate and improved Adam's generalisation enough to compete with SGD with momentum on image classification, with a reported 15% relative improvement in test error (Loshchilov & Hutter, 2019; [[regularisation-and-hyperparameters|regularisation]]).

#### 5. Convergence issues and AMSGrad

Reddi et al. (2018) give a simple convex example in which Adam does not converge to the optimum and trace the problem to the exponential moving average, which can quickly forget large, informative gradients. Their variant AMSGrad keeps the maximum of all past second-moment estimates, `v̂_t = max(v̂_{t−1}, v_t)`, so the effective learning rate cannot increase; this fixes the convergence issue and often also improved empirical results (Reddi et al., 2018).

#### Origin and variants

Diederik Kingma and Jimmy Ba presented Adam at ICLR 2015, together with AdaMax, a variant based on the infinity norm (Kingma & Ba, 2015). Ruder (2016) also describes Nadam, which adds Nesterov momentum. AdamW (Loshchilov & Hutter, 2019) is implemented in TensorFlow and PyTorch.

### When to use it

- Training deep networks where fast convergence matters, and problems with noisy or sparse gradients (Kingma & Ba, 2015; Ruder, 2016).
- Large models with many parameters, since Adam needs only two extra values per parameter (Kingma & Ba, 2015).
- As a robust default when little time is available for tuning the learning rate (Ruder, 2016).

### Strengths and limitations

**Strengths**
- Per-parameter step sizes that adapt to gradient history (Kingma & Ba, 2015).
- Hyperparameters have intuitive meanings and usually need little tuning (Kingma & Ba, 2015).
- Invariant to diagonal rescaling of the gradients and suitable for non-stationary objectives (Kingma & Ba, 2015).

**Limitations**
- Can fail to converge in some settings because of its moving average (Reddi et al., 2018).
- With L2 regularisation instead of decoupled weight decay it generalised worse than SGD with momentum on image classification (Loshchilov & Hutter, 2019).
- Stores two moment vectors per parameter, one more than SGD with momentum (Kingma & Ba, 2015; Ruder, 2016); for very large models optimiser memory matters ([[mixed-precision-training|mixed-precision training]]).

### Comparison

| Optimiser | State per parameter | Step size | Note |
|---|---|---|---|
| SGD | none | global η | needs a schedule, robust generalisation |
| SGD + momentum | velocity | global η | dampens oscillation |
| RMSProp | squared-gradient average | per parameter | no momentum, no bias correction |
| Adam | mean and squared-gradient average | per parameter, bias-corrected | fast default |
| AdamW | as Adam | as Adam | weight decay decoupled from the step |
| AMSGrad | as Adam plus running maximum | non-increasing | convergence fix |

Sources: Kingma & Ba (2015), Ruder (2016), Loshchilov & Hutter (2019), Reddi et al. (2018).

### In practice

The defaults α = 0.001, β₁ = 0.9, β₂ = 0.999 and ε = 10⁻⁸ worked well on the problems Kingma and Ba (2015) tested. Loshchilov and Hutter (2019) found that the optimal weight decay depends on the total number of weight updates: the longer the training, the smaller the optimal decay. In frameworks, the choice between Adam with an L2 penalty and AdamW is therefore not a detail but changes regularisation ([[neural-network-training|neural network training]]).

### Key takeaway

Adam scales each parameter's step by running estimates of the mean and variance of its gradients, with bias correction; use AdamW when weight decay is wanted.

### Sources

- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization.* ICLR 2015. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
- Loshchilov, I. & Hutter, F. (2019). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
- Reddi, S. J., Kale, S. & Kumar, S. (2018). *On the Convergence of Adam and Beyond.* ICLR 2018. [arXiv:1904.09237](https://arxiv.org/abs/1904.09237)
- Ruder, S. (2016). *An overview of gradient descent optimization algorithms.* [arXiv:1609.04747](https://arxiv.org/abs/1609.04747)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Adam (Adaptive Moment Estimation) ist ein Optimierungsverfahren erster Ordnung für stochastische Zielfunktionen, das für jeden Parameter exponentiell gleitende Mittelwerte des Gradienten und des quadrierten Gradienten führt und damit jedem Parameter eine eigene Schrittweite gibt (Kingma & Ba, 2015). Es verbindet die Idee des Momentums mit der parameterweisen Skalierung von AdaGrad und RMSProp, braucht wenig Speicher und wenig Feinabstimmung und ist eine Standardwahl für das Training tiefer [[neural-networks|neuronaler Netze]] (Kingma & Ba, 2015; Ruder, 2016). AdamW entkoppelt den Weight Decay vom Gradienten-Update und behebt so das schlechte Zusammenspiel von L2-Regularisierung und Adam (Loshchilov & Hutter, 2019).

### Funktionsweise

```text
m₀ = 0, v₀ = 0, t = 0                      Standardwerte: α = 0,001, β₁ = 0,9, β₂ = 0,999, ε = 10⁻⁸
wiederholen:
    t ← t + 1
    g_t = ∇θ f_t(θ_{t−1})                   Gradient auf dem aktuellen Mini-Batch
    m_t = β₁ m_{t−1} + (1 − β₁) g_t          1. Moment: Mittel der Gradienten
    v_t = β₂ v_{t−1} + (1 − β₂) g_t²         2. Rohmoment: Mittel der quadrierten Gradienten
    m̂_t = m_t / (1 − β₁ᵗ),  v̂_t = v_t / (1 − β₂ᵗ)     Bias-Korrektur
    θ_t = θ_{t−1} − α · m̂_t / (√v̂_t + ε)     elementweises Update
```

#### 1. Momentschätzer

Adam führt pro Parameter zwei gleitende Mittelwerte: m_t, eine Schätzung des Mittels der Gradienten, und v_t, eine Schätzung ihrer unzentrierten Varianz (Kingma & Ba, 2015). β₁ und β₂ legen fest, wie schnell sie alte Gradienten vergessen; m_t übernimmt die Rolle des Momentums im [[gradient-descent|Gradientenabstieg]], v_t die Rolle des Mittels der quadrierten Gradienten in RMSProp (Ruder, 2016).

#### 2. Bias-Korrektur

Weil beide Mittelwerte bei null beginnen, sind sie in den ersten Schritten zur Null hin verzerrt, besonders wenn β nahe 1 liegt; das Teilen durch `1 − βᵗ` korrigiert das (Kingma & Ba, 2015). Nach Kingma und Ba (2015) hilft diese Korrektur Adam, RMSProp gegen Ende der Optimierung leicht zu übertreffen, wenn die Gradienten dünner besetzt werden (Ruder, 2016).

#### 3. Das Update und seine Schrittweite

Das Update teilt das korrigierte Mittel durch die Wurzel des korrigierten zweiten Moments, sodass jeder Parameter sich ungefähr um die Schrittweite α in Richtung seiner jüngsten Gradienten bewegt (Kingma & Ba, 2015). Der effektive Schritt ist näherungsweise durch α begrenzt, was wie eine Trust Region wirkt und die Wahl der richtigen Größenordnung von α erleichtert; er ist invariant gegenüber dem Umskalieren der Gradienten, und das Verhältnis `m̂/√v̂`, das Kingma und Ba als Signal-Rausch-Verhältnis bezeichnen, schrumpft nahe einem Optimum, was eine Art automatisches Annealing ergibt (Kingma & Ba, 2015). Parameter mit seltenen, aber großen Gradienten erhalten deshalb relativ größere Updates als mit einfachem SGD.

#### 4. Weight Decay: Adam und AdamW

Bei einfachem SGD sind L2-Regularisierung und Weight Decay nach Umskalierung mit der Lernrate gleichwertig; bei Adam nicht, weil auch der L2-Gradient durch `√v̂` geteilt wird, sodass Gewichte mit großen früheren Gradienten schwächer regularisiert werden (Loshchilov & Hutter, 2019). Verbreitete Implementierungen nannten L2-Regularisierung dennoch „Weight Decay“. AdamW wendet den Decay direkt auf die Gewichte an, getrennt vom gradientenbasierten Schritt; dadurch wurde der optimale Weight Decay unabhängig von der Lernrate, und Adams Generalisierung verbesserte sich so weit, dass es bei der Bildklassifikation mit SGD mit Momentum mithalten konnte, mit einer berichteten relativen Verbesserung des Testfehlers um 15 % (Loshchilov & Hutter, 2019; [[regularisation-and-hyperparameters|Regularisierung]]).

#### 5. Konvergenzprobleme und AMSGrad

Reddi et al. (2018) geben ein einfaches konvexes Beispiel, in dem Adam nicht zum Optimum konvergiert, und führen das Problem auf den exponentiell gleitenden Mittelwert zurück, der große, informative Gradienten schnell vergessen kann. Ihre Variante AMSGrad behält das Maximum aller bisherigen Schätzungen des zweiten Moments, `v̂_t = max(v̂_{t−1}, v_t)`, sodass die effektive Lernrate nicht steigen kann; das behebt das Konvergenzproblem und verbesserte oft auch die empirischen Ergebnisse (Reddi et al., 2018).

#### Ursprung und Varianten

Diederik Kingma und Jimmy Ba stellten Adam auf der ICLR 2015 vor, zusammen mit AdaMax, einer Variante auf Basis der Unendlichnorm (Kingma & Ba, 2015). Ruder (2016) beschreibt außerdem Nadam, das Nesterov-Momentum ergänzt. AdamW (Loshchilov & Hutter, 2019) ist in TensorFlow und PyTorch implementiert.

### Wann einsetzen

- Training tiefer Netze, bei dem schnelle Konvergenz zählt, und Probleme mit verrauschten oder dünn besetzten Gradienten (Kingma & Ba, 2015; Ruder, 2016).
- Große Modelle mit vielen Parametern, da Adam nur zwei zusätzliche Werte pro Parameter braucht (Kingma & Ba, 2015).
- Als robuste Voreinstellung, wenn wenig Zeit für das Einstellen der Lernrate bleibt (Ruder, 2016).

### Stärken und Grenzen

**Stärken**
- Schrittweiten pro Parameter, die sich an die Geschichte der Gradienten anpassen (Kingma & Ba, 2015).
- Hyperparameter mit anschaulicher Bedeutung, die meist wenig Abstimmung brauchen (Kingma & Ba, 2015).
- Invariant gegenüber diagonaler Umskalierung der Gradienten und geeignet für nicht stationäre Zielfunktionen (Kingma & Ba, 2015).

**Grenzen**
- Kann in manchen Situationen wegen seines gleitenden Mittelwerts nicht konvergieren (Reddi et al., 2018).
- Mit L2-Regularisierung statt entkoppeltem Weight Decay generalisierte es bei der Bildklassifikation schlechter als SGD mit Momentum (Loshchilov & Hutter, 2019).
- Speichert pro Parameter zwei Momentvektoren, einen mehr als SGD mit Momentum (Kingma & Ba, 2015; Ruder, 2016); bei sehr großen Modellen fällt der Speicher des Optimierers ins Gewicht ([[mixed-precision-training|Mixed-Precision-Training]]).

### Vergleich

| Optimierer | Zustand pro Parameter | Schrittweite | Bemerkung |
|---|---|---|---|
| SGD | keiner | globales η | braucht einen Zeitplan, robuste Generalisierung |
| SGD + Momentum | Geschwindigkeit | globales η | dämpft Oszillationen |
| RMSProp | Mittel der quadrierten Gradienten | pro Parameter | kein Momentum, keine Bias-Korrektur |
| Adam | Mittel und Mittel der quadrierten Gradienten | pro Parameter, bias-korrigiert | schnelle Voreinstellung |
| AdamW | wie Adam | wie Adam | Weight Decay vom Schritt entkoppelt |
| AMSGrad | wie Adam plus laufendes Maximum | nicht steigend | Konvergenzkorrektur |

Quellen: Kingma & Ba (2015), Ruder (2016), Loshchilov & Hutter (2019), Reddi et al. (2018).

### In der Praxis

Die Standardwerte α = 0,001, β₁ = 0,9, β₂ = 0,999 und ε = 10⁻⁸ funktionierten auf den von Kingma und Ba (2015) getesteten Problemen gut. Loshchilov und Hutter (2019) stellten fest, dass der optimale Weight Decay von der Gesamtzahl der Gewichts-Updates abhängt: Je länger das Training, desto kleiner der optimale Decay. In Frameworks ist die Wahl zwischen Adam mit L2-Strafterm und AdamW daher kein Detail, sondern verändert die Regularisierung ([[neural-network-training|Training neuronaler Netze]]).

### Merksatz

Adam skaliert den Schritt jedes Parameters mit laufenden Schätzungen von Mittel und Varianz seiner Gradienten, mit Bias-Korrektur; wird Weight Decay gebraucht, ist AdamW die richtige Wahl.

### Quellen

- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization.* ICLR 2015. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
- Loshchilov, I. & Hutter, F. (2019). *Decoupled Weight Decay Regularization.* ICLR 2019. [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
- Reddi, S. J., Kale, S. & Kumar, S. (2018). *On the Convergence of Adam and Beyond.* ICLR 2018. [arXiv:1904.09237](https://arxiv.org/abs/1904.09237)
- Ruder, S. (2016). *An overview of gradient descent optimization algorithms.* [arXiv:1609.04747](https://arxiv.org/abs/1609.04747)
