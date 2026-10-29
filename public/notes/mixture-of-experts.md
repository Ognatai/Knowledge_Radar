---
title_en: Mixture-of-Experts
title_de: Mixture-of-Experts
entity_type: Method
aliases:
- MoE
- Sparsely-Gated Mixture-of-Experts
- Sparse Mixture of Experts
- SMoE
sources:
- https://arxiv.org/abs/1701.06538
- https://arxiv.org/abs/2006.16668
- https://arxiv.org/abs/2101.03961
- https://arxiv.org/abs/2202.08906
- https://arxiv.org/abs/2401.04088
- https://arxiv.org/abs/2401.06066
- https://arxiv.org/abs/2505.09388
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
A Mixture-of-Experts (MoE) layer replaces one large feed-forward block with many smaller ones, the experts, and a router that sends each token to only a few of them. The model therefore has far more parameters than it uses for any single token: capacity grows with the number of experts while the computation per token stays almost constant (Shazeer et al., 2017; Fedus et al., 2021). Mixtral 8x7B, for example, has 47B parameters but uses 13B per token and matched or outperformed [[llama|Llama 2 70B]] on the benchmarks its authors evaluated (Jiang et al., 2024); many current open [[large-language-models|large language models]], such as Qwen3-30B-A3B, are MoE models (Yang et al., 2025).

### How it works

In a [[attention-and-transformers|Transformer]], every block contains a feed-forward network that processes each token separately. An MoE layer keeps the attention part and replaces this feed-forward network with `n` experts of the same shape plus a small router. For every token, the router scores all experts, keeps the best `k`, and the layer returns the weighted sum of these experts' outputs; the other experts are not computed at all (Shazeer et al., 2017; Jiang et al., 2024).

```text
token x ─▶ router: scores x·W_g ─▶ keep top-k ─▶ softmax ─▶ gate weights
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
          expert 1 (FFN)          expert 3 (FFN)    ...   other experts: skipped
              └──── weighted sum of the k selected outputs ───┘
                                      ▼
                                  output y
```

#### 1. Experts
An expert is an ordinary feed-forward network; in Mixtral it is the same SwiGLU block that a dense Transformer would use (Jiang et al., 2024). The output of the layer is `y = Σ_i G(x)_i · E_i(x)`, where `E_i(x)` is the output of expert `i` and `G(x)` is the gate vector produced by the router. Wherever `G(x)_i = 0`, expert `i` need not be computed, which is where the savings come from (Shazeer et al., 2017). Models differ in where they place MoE layers: GShard replaced every other feed-forward layer with an MoE layer, Mixtral replaces all of them (Lepikhin et al., 2020; Jiang et al., 2024).

#### 2. Router
The router is a trainable linear layer: it multiplies the token representation by a weight matrix `W_g`, keeps the `k` largest scores, sets the rest to minus infinity and applies a softmax, so that the selected experts receive weights that sum to one: `G(x) = Softmax(TopK(x·W_g))` (Jiang et al., 2024). It is trained by [[back-propagation|back-propagation]] together with the rest of the model (Shazeer et al., 2017). Design choices:

- **Number of active experts `k`:** Shazeer et al. (2017) assumed that `k > 1` was needed for useful gradients to the router. The Switch Transformer routes each token to a single expert (`k = 1`), which reduces router computation and communication and preserved model quality (Fedus et al., 2021). GShard and Mixtral use two experts per token (Lepikhin et al., 2020; Jiang et al., 2024); Qwen3's MoE models activate 8 of 128 experts (Yang et al., 2025).
- **Noise:** the original layer added trainable Gaussian noise to the scores before the top-k selection, which helped to balance the load (Shazeer et al., 2017).
- **Second expert:** GShard sends a token to its second-best expert only with a probability proportional to that expert's weight, saving capacity when the second weight is small (Lepikhin et al., 2020).

#### 3. Expert capacity and dropped tokens
Hardware such as TPUs needs fixed tensor sizes, so each expert processes at most a fixed number of tokens per batch: `expert capacity = (tokens per batch / number of experts) × capacity factor`. A capacity factor above 1.0 leaves room for uneven routing. Tokens routed to an expert that is already full are dropped: the layer skips them and passes their representation on through the [[resnet|residual connection]]. A larger capacity factor drops fewer tokens but wastes computation and memory on empty slots; in the Switch Transformer experiments, typically fewer than 1% of tokens were dropped (Fedus et al., 2021). Implementations with specialised kernels such as Megablocks can instead handle a variable number of tokens per expert (Jiang et al., 2024); when all experts fit on one device, as in DeepSeekMoE's small validation models, no tokens are dropped (Dai et al., 2024).

#### 4. Load balancing
Left alone, the router tends to collapse onto a few experts: the favoured experts are trained faster and are then chosen even more often (Shazeer et al., 2017). An auxiliary loss counteracts this. In the Switch Transformer it is `α · N · Σ_i f_i · P_i`, where `f_i` is the fraction of tokens dispatched to expert `i`, `P_i` the fraction of router probability assigned to it, `N` the number of experts and `α = 10⁻²`; it is smallest when both are uniform (Fedus et al., 2021). DeepSeekMoE adds a device-level balance loss so that the computation is spread evenly across the devices that host the experts (Dai et al., 2024), and Qwen3 uses a balancing loss computed over the global batch to encourage expert specialisation (Yang et al., 2025).

#### 5. Training stability
The hard routing decisions make large sparse models prone to instability (Fedus et al., 2021). The Switch Transformer computes the router in float32 while the rest of the model runs in bfloat16 ("selective precision", a form of [[mixed-precision-training|mixed-precision training]]) and reduces the initialisation scale (Fedus et al., 2021). At larger scales this was not enough; ST-MoE adds the router z-loss, `(1/B) Σ_i (log Σ_j e^{x_j})²` over the router logits `x` of the `B` tokens in a batch, which penalises large logits and stabilised training without the loss of quality that tighter update clipping caused (Zoph et al., 2022).

#### 6. Total and active parameters
Increasing the number of experts `n` while keeping `k` fixed increases the total (sparse) parameter count at almost constant computation; the parameters actually used per token are the active parameters (Jiang et al., 2024). The compute per token is proportional to the active parameters, but the memory needed to serve the model is proportional to the total: Mixtral needs memory for 47B parameters although it computes with 13B (Jiang et al., 2024). Model names often state both: Qwen3-235B-A22B has 235B total and 22B activated parameters (Yang et al., 2025).

#### 7. Distribution across devices
Experts can be spread over many accelerators. In expert parallelism, each device holds some of the experts and tokens are sent to the device of their expert and back (Jiang et al., 2024). Shazeer et al. (2017) combined this with data parallelism: the ordinary layers are replicated, each expert exists once and receives the tokens routed to it from all data-parallel batches, so that adding devices adds experts without shrinking each expert's batch. The resulting communication is a central cost of MoE training; routing to a single expert, as in the Switch Transformer, reduces it (Fedus et al., 2021).

#### 8. Fine-grained and shared experts
With few, large experts, one expert has to hold very different kinds of knowledge ("knowledge hybridity"), and several experts may learn the same common knowledge ("knowledge redundancy"). DeepSeekMoE therefore splits each expert into several smaller ones and activates correspondingly more of them at the same cost (fine-grained expert segmentation), and it adds shared experts that every token passes through (shared expert isolation). DeepSeekMoE 16B routes each token to 2 shared and 6 of 64 routed experts, has 16.4B total and about 2.8B active parameters, and matched the dense DeepSeek 7B and LLaMA2 7B with about 40% of their computation (Dai et al., 2024). Qwen3 adopted fine-grained experts but dropped shared experts (Yang et al., 2025).

#### Origin and variants
Mixtures of experts date back to the early 1990s; in that early work the mixture was the whole model rather than a layer inside a deep network (Shazeer et al., 2017). Shazeer et al. (2017) introduced the sparsely-gated MoE layer with thousands of experts between LSTM layers, reaching up to 137B parameters in the MoE layer and better results than the state of the art in language modelling and [[machine-translation|machine translation]] at lower computational cost. GShard brought MoE into the Transformer and trained a 600B-parameter translation model from 100 languages to English on 2048 TPU v3 cores in 4 days (Lepikhin et al., 2020). The Switch Transformer simplified routing to one expert and scaled to 1.6 trillion parameters, with up to 7 times faster pre-training than a [[t5|T5]] model using the same computation (Fedus et al., 2021). ST-MoE addressed stability and fine-tuning (Zoph et al., 2022), Mixtral made a strong MoE model openly available under Apache 2.0 (Jiang et al., 2024), and DeepSeekMoE introduced fine-grained and shared experts (Dai et al., 2024).

### When to use it
- Training a larger model within a fixed compute budget: for the same computation per token, sparse models outperformed dense models per step and in wall-clock time in the Switch Transformer experiments (Fedus et al., 2021).
- Serving at large batch sizes: the routing overhead and the memory loads of several experts per device make MoE models better suited to batched workloads with high arithmetic intensity (Jiang et al., 2024).
- Running a capable open model with less computation per token than a dense model of similar quality, provided there is enough memory for all experts (Jiang et al., 2024; Yang et al., 2025).

### Strengths and limitations
Strengths:
- Capacity grows with the number of experts at almost constant computation per token (Shazeer et al., 2017; Jiang et al., 2024).
- Lower computation for comparable quality: Qwen3's MoE base models matched its dense base models with one fifth of the activated parameters (Yang et al., 2025).
- Gains also at small scale: models with as few as two experts improved over dense baselines (Fedus et al., 2021).

Limitations:
- Memory is set by the total parameter count, not the active one (Jiang et al., 2024).
- Training is more complex: load balancing, capacity limits, communication between devices and instability need extra losses and engineering (Fedus et al., 2021; Zoph et al., 2022).
- Sparse models overfit more easily when fine-tuned on small datasets; the Switch Transformer uses a higher dropout inside the experts ("expert dropout") (Fedus et al., 2021; Zoph et al., 2022).
- Experts do not necessarily specialise by topic: in Mixtral, expert assignment followed syntax rather than domain, and consecutive tokens often went to the same expert, which can overload single experts under expert parallelism (Jiang et al., 2024).

### Comparison
| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Dense [[attention-and-transformers\|Transformer]] | Every token uses all parameters; compute and memory grow together | Simple training and serving |
| [[knowledge-distillation\|Knowledge distillation]] | Trains a small dense model to imitate a large one; distilling a sparse Switch model into a dense one kept about 30% of its quality gain at 10 to 100 times smaller size (Fedus et al., 2021) | Deployment where memory is the bottleneck |
| [[quantisation\|Quantisation]] | Stores the same parameters with fewer bits; reduces memory, which MoE does not | Fitting a (possibly MoE) model into limited memory |
| [[ensemble-methods\|Ensemble methods]] | Run several complete models and combine all their predictions | Classical ML where every model is cheap |

### In practice
- Active and total parameters answer different questions: compute and latency follow the active parameters, memory follows the total (Jiang et al., 2024). For local use, the total size of an MoE model has to fit into memory even though each token touches only a fraction of it; [[quantisation|quantisation]] and [[model-compression|model compression]] address this side.
- The auxiliary balancing coefficient has to be large enough to balance the load but small enough not to dominate the training loss; Fedus et al. (2021) found `α = 10⁻²` to work across a sweep from `10⁻¹` to `10⁻⁵`.
- For fine-tuning, ST-MoE found that sparse and dense models need different protocols and that sparse models are robust to dropped tokens during fine-tuning (Zoph et al., 2022).
- Benchmarks of MoE models are usually compared at equal active parameters, as in Mixtral's comparison with Llama 2 (Jiang et al., 2024); [[llm-cost-optimisation|cost comparisons]] also need the memory and hardware utilisation, which this comparison leaves out.

### Regulatory context
The [[eu-ai-act|EU AI Act]] presumes high-impact capabilities, and thus systemic risk, for general-purpose AI models trained with more than 10²⁵ floating-point operations. The threshold refers to training compute, not to the number of parameters; for MoE models, the compute per token follows the active rather than the total parameters (Jiang et al., 2024), so the total parameter count alone does not show whether a model crosses it.

### Key takeaway
A Mixture-of-Experts model routes each token to a few of many experts, so it can have the knowledge capacity of a very large model at the computation cost of a much smaller one, but it still needs the memory of the large one.

### Sources
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer.* ICLR 2017. [arXiv:1701.06538](https://arxiv.org/abs/1701.06538)
- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding.* [arXiv:2006.16668](https://arxiv.org/abs/2006.16668)
- Fedus, W., Zoph, B. & Shazeer, N. (2021). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity.* JMLR 23 (2022). [arXiv:2101.03961](https://arxiv.org/abs/2101.03961)
- Zoph, B. et al. (2022). *ST-MoE: Designing Stable and Transferable Sparse Expert Models.* [arXiv:2202.08906](https://arxiv.org/abs/2202.08906)
- Jiang, A. Q. et al. (2024). *Mixtral of Experts.* [arXiv:2401.04088](https://arxiv.org/abs/2401.04088)
- Dai, D. et al. (2024). *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.* [arXiv:2401.06066](https://arxiv.org/abs/2401.06066)
- Yang, A. et al. (2025). *Qwen3 Technical Report.* [arXiv:2505.09388](https://arxiv.org/abs/2505.09388)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Eine Mixture-of-Experts-Schicht (MoE) ersetzt einen großen Feed-Forward-Block durch viele kleinere, die Experten, und einen Router, der jedes Token nur an wenige von ihnen schickt. Das Modell hat dadurch weit mehr Parameter, als es für ein einzelnes Token nutzt: Die Kapazität wächst mit der Zahl der Experten, während der Rechenaufwand je Token nahezu gleich bleibt (Shazeer et al., 2017; Fedus et al., 2021). Mixtral 8x7B etwa hat 47 Milliarden Parameter, nutzt aber 13 Milliarden je Token und erreichte oder übertraf [[llama|Llama 2 70B]] auf den von den Autoren untersuchten Benchmarks (Jiang et al., 2024); viele aktuelle offene [[large-language-models|große Sprachmodelle]] wie Qwen3-30B-A3B sind MoE-Modelle (Yang et al., 2025).

### Funktionsweise

In einem [[attention-and-transformers|Transformer]] enthält jeder Block ein Feed-Forward-Netz, das jedes Token einzeln verarbeitet. Eine MoE-Schicht behält den Attention-Teil und ersetzt dieses Feed-Forward-Netz durch `n` gleich aufgebaute Experten und einen kleinen Router. Für jedes Token bewertet der Router alle Experten, behält die besten `k`, und die Schicht gibt die gewichtete Summe der Ausgaben dieser Experten zurück; die übrigen Experten werden gar nicht berechnet (Shazeer et al., 2017; Jiang et al., 2024).

```text
Token x ─▶ Router: Scores x·W_g ─▶ Top-k behalten ─▶ Softmax ─▶ Gewichte
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
          Experte 1 (FFN)         Experte 3 (FFN)   ...   übrige Experten: übersprungen
              └──── gewichtete Summe der k gewählten Ausgaben ───┘
                                      ▼
                                  Ausgabe y
```

#### 1. Experten
Ein Experte ist ein gewöhnliches Feed-Forward-Netz; in Mixtral ist es derselbe SwiGLU-Block, den ein dichter Transformer verwenden würde (Jiang et al., 2024). Die Ausgabe der Schicht ist `y = Σ_i G(x)_i · E_i(x)`, wobei `E_i(x)` die Ausgabe von Experte `i` und `G(x)` der vom Router erzeugte Gewichtsvektor ist. Wo `G(x)_i = 0` gilt, muss Experte `i` nicht berechnet werden; daher kommt die Einsparung (Shazeer et al., 2017). Modelle unterscheiden sich darin, wo sie MoE-Schichten einsetzen: GShard ersetzte jede zweite Feed-Forward-Schicht durch eine MoE-Schicht, Mixtral ersetzt alle (Lepikhin et al., 2020; Jiang et al., 2024).

#### 2. Router
Der Router ist eine trainierbare lineare Schicht: Er multipliziert die Token-Repräsentation mit einer Gewichtsmatrix `W_g`, behält die `k` höchsten Scores, setzt die übrigen auf minus unendlich und wendet eine Softmax an, sodass die gewählten Experten Gewichte erhalten, die sich zu eins addieren: `G(x) = Softmax(TopK(x·W_g))` (Jiang et al., 2024). Er wird zusammen mit dem übrigen Modell per [[back-propagation|Backpropagation]] trainiert (Shazeer et al., 2017). Entwurfsentscheidungen:

- **Zahl der aktiven Experten `k`:** Shazeer et al. (2017) nahmen an, dass `k > 1` für brauchbare Gradienten zum Router nötig sei. Der Switch Transformer schickt jedes Token an einen einzigen Experten (`k = 1`), was Rechenaufwand und Kommunikation des Routers senkt und die Modellqualität erhielt (Fedus et al., 2021). GShard und Mixtral nutzen zwei Experten je Token (Lepikhin et al., 2020; Jiang et al., 2024); die MoE-Modelle von Qwen3 aktivieren 8 von 128 Experten (Yang et al., 2025).
- **Rauschen:** Die ursprüngliche Schicht addierte vor der Top-k-Auswahl trainierbares Gaußsches Rauschen zu den Scores, was die Last besser verteilte (Shazeer et al., 2017).
- **Zweiter Experte:** GShard schickt ein Token nur mit einer Wahrscheinlichkeit proportional zu dessen Gewicht an den zweitbesten Experten und spart so Kapazität, wenn das zweite Gewicht klein ist (Lepikhin et al., 2020).

#### 3. Expertenkapazität und verworfene Tokens
Hardware wie TPUs braucht feste Tensorgrößen, deshalb verarbeitet jeder Experte je Batch höchstens eine feste Zahl von Tokens: `Expertenkapazität = (Tokens je Batch / Zahl der Experten) × Kapazitätsfaktor`. Ein Kapazitätsfaktor über 1,0 lässt Spielraum für ungleichmäßiges Routing. Tokens, die an einen bereits vollen Experten gehen, werden verworfen: Die Schicht überspringt sie und reicht ihre Repräsentation über die Residualverbindung weiter. Ein größerer Kapazitätsfaktor verwirft weniger Tokens, verschwendet aber Rechenzeit und Speicher für leere Plätze; in den Experimenten zum Switch Transformer wurden typischerweise weniger als 1 % der Tokens verworfen (Fedus et al., 2021). Implementierungen mit spezialisierten Kernels wie Megablocks können stattdessen eine variable Zahl von Tokens je Experte verarbeiten (Jiang et al., 2024); passen alle Experten auf ein Gerät, wie bei den kleinen Validierungsmodellen von DeepSeekMoE, werden keine Tokens verworfen (Dai et al., 2024).

#### 4. Lastverteilung
Sich selbst überlassen, konzentriert sich der Router auf wenige Experten: Die bevorzugten Experten werden schneller trainiert und danach noch häufiger gewählt (Shazeer et al., 2017). Ein zusätzlicher Verlustterm wirkt dem entgegen. Im Switch Transformer lautet er `α · N · Σ_i f_i · P_i`, wobei `f_i` der Anteil der Tokens ist, die an Experte `i` gehen, `P_i` der Anteil der Router-Wahrscheinlichkeit, der auf ihn entfällt, `N` die Zahl der Experten und `α = 10⁻²`; er ist am kleinsten, wenn beide gleichverteilt sind (Fedus et al., 2021). DeepSeekMoE ergänzt einen Verlustterm auf Geräteebene, damit sich die Rechenlast gleichmäßig auf die Geräte verteilt, die die Experten beherbergen (Dai et al., 2024), und Qwen3 nutzt einen über den globalen Batch berechneten Balancing-Verlust, um die Spezialisierung der Experten zu fördern (Yang et al., 2025).

#### 5. Trainingsstabilität
Die harten Routing-Entscheidungen machen große dünn besetzte Modelle anfällig für Instabilität (Fedus et al., 2021). Der Switch Transformer berechnet den Router in float32, während der Rest des Modells in bfloat16 läuft („Selective Precision“, eine Form von [[mixed-precision-training|Mixed-Precision-Training]]), und verkleinert die Initialisierung (Fedus et al., 2021). Bei größeren Modellen reichte das nicht; ST-MoE ergänzt den Router-Z-Loss `(1/B) Σ_i (log Σ_j e^{x_j})²` über die Router-Logits `x` der `B` Tokens eines Batches, der große Logits bestraft und das Training stabilisierte, ohne den Qualitätsverlust, den engeres Update-Clipping verursachte (Zoph et al., 2022).

#### 6. Gesamt- und aktive Parameter
Erhöht man die Zahl der Experten `n` bei festem `k`, steigt die gesamte (dünn besetzte) Parameterzahl bei nahezu gleichem Rechenaufwand; die je Token tatsächlich genutzten Parameter sind die aktiven Parameter (Jiang et al., 2024). Der Rechenaufwand je Token ist proportional zu den aktiven Parametern, der Speicherbedarf für den Betrieb aber proportional zur Gesamtzahl: Mixtral braucht Speicher für 47 Milliarden Parameter, obwohl es mit 13 Milliarden rechnet (Jiang et al., 2024). Modellnamen nennen oft beides: Qwen3-235B-A22B hat 235 Milliarden Parameter insgesamt und 22 Milliarden aktive (Yang et al., 2025).

#### 7. Verteilung auf Geräte
Experten lassen sich auf viele Beschleuniger verteilen. Bei Expert Parallelism hält jedes Gerät einen Teil der Experten, und Tokens werden an das Gerät ihres Experten geschickt und zurück (Jiang et al., 2024). Shazeer et al. (2017) kombinierten dies mit Datenparallelität: Die gewöhnlichen Schichten werden repliziert, jeder Experte existiert nur einmal und erhält die an ihn gerouteten Tokens aus allen datenparallelen Batches, sodass zusätzliche Geräte zusätzliche Experten ermöglichen, ohne den Batch jedes Experten zu verkleinern. Die dabei entstehende Kommunikation ist ein zentraler Kostenfaktor des MoE-Trainings; Routing an nur einen Experten wie im Switch Transformer verringert sie (Fedus et al., 2021).

#### 8. Feinkörnige und geteilte Experten
Bei wenigen großen Experten muss ein Experte sehr unterschiedliches Wissen aufnehmen („Knowledge Hybridity“), und mehrere Experten lernen womöglich dasselbe allgemeine Wissen („Knowledge Redundancy“). DeepSeekMoE teilt deshalb jeden Experten in mehrere kleinere auf und aktiviert bei gleichem Aufwand entsprechend mehr davon (Fine-Grained Expert Segmentation), und es ergänzt geteilte Experten, die jedes Token durchläuft (Shared Expert Isolation). DeepSeekMoE 16B schickt jedes Token an 2 geteilte und 6 von 64 gerouteten Experten, hat 16,4 Milliarden Parameter insgesamt und rund 2,8 Milliarden aktive und erreichte mit etwa 40 % des Rechenaufwands die dichten Modelle DeepSeek 7B und LLaMA2 7B (Dai et al., 2024). Qwen3 übernahm feinkörnige Experten, verzichtet aber auf geteilte Experten (Yang et al., 2025).

#### Ursprung und Varianten
Mixtures of Experts gehen auf die frühen 1990er-Jahre zurück; in diesen frühen Arbeiten war die Mischung das ganze Modell und keine Schicht in einem tiefen Netz (Shazeer et al., 2017). Shazeer et al. (2017) führten die Sparsely-Gated-MoE-Schicht mit Tausenden von Experten zwischen LSTM-Schichten ein, erreichten bis zu 137 Milliarden Parameter in der MoE-Schicht und übertrafen bei Sprachmodellierung und [[machine-translation|maschineller Übersetzung]] den Stand der Technik mit geringerem Rechenaufwand. GShard brachte MoE in den Transformer und trainierte ein Übersetzungsmodell mit 600 Milliarden Parametern von 100 Sprachen ins Englische auf 2048 TPU-v3-Kernen in 4 Tagen (Lepikhin et al., 2020). Der Switch Transformer vereinfachte das Routing auf einen Experten und skalierte auf 1,6 Billionen Parameter, mit bis zu 7-mal schnellerem Pretraining als ein [[t5|T5]]-Modell bei gleichem Rechenaufwand (Fedus et al., 2021). ST-MoE befasste sich mit Stabilität und Fine-Tuning (Zoph et al., 2022), Mixtral machte ein starkes MoE-Modell unter Apache 2.0 offen verfügbar (Jiang et al., 2024), und DeepSeekMoE führte feinkörnige und geteilte Experten ein (Dai et al., 2024).

### Wann einsetzen
- Ein größeres Modell innerhalb eines festen Rechenbudgets trainieren: Bei gleichem Rechenaufwand je Token übertrafen dünn besetzte Modelle in den Experimenten zum Switch Transformer dichte Modelle je Trainingsschritt und in der Laufzeit (Fedus et al., 2021).
- Betrieb mit großen Batches: Der Routing-Aufwand und die Speicherzugriffe mehrerer Experten je Gerät machen MoE-Modelle besser geeignet für gebündelte Last mit hoher arithmetischer Intensität (Jiang et al., 2024).
- Ein leistungsfähiges offenes Modell mit weniger Rechenaufwand je Token betreiben als ein dichtes Modell ähnlicher Qualität, sofern genug Speicher für alle Experten vorhanden ist (Jiang et al., 2024; Yang et al., 2025).

### Stärken und Grenzen
Stärken:
- Die Kapazität wächst mit der Zahl der Experten bei nahezu gleichem Rechenaufwand je Token (Shazeer et al., 2017; Jiang et al., 2024).
- Weniger Rechenaufwand bei vergleichbarer Qualität: Die MoE-Basismodelle von Qwen3 erreichten die dichten Basismodelle mit einem Fünftel der aktivierten Parameter (Yang et al., 2025).
- Vorteile auch im Kleinen: Schon Modelle mit nur zwei Experten verbesserten sich gegenüber dichten Baselines (Fedus et al., 2021).

Grenzen:
- Der Speicherbedarf richtet sich nach der gesamten, nicht nach der aktiven Parameterzahl (Jiang et al., 2024).
- Das Training ist aufwendiger: Lastverteilung, Kapazitätsgrenzen, Kommunikation zwischen Geräten und Instabilität erfordern zusätzliche Verlustterme und technischen Aufwand (Fedus et al., 2021; Zoph et al., 2022).
- Dünn besetzte Modelle überanpassen sich beim Fine-Tuning auf kleinen Datensätzen leichter; der Switch Transformer nutzt deshalb eine höhere Dropout-Rate innerhalb der Experten („Expert Dropout“) (Fedus et al., 2021; Zoph et al., 2022).
- Experten spezialisieren sich nicht zwingend nach Themen: In Mixtral folgte die Zuweisung eher der Syntax als der Domäne, und aufeinanderfolgende Tokens gingen oft an denselben Experten, was bei Expert Parallelism einzelne Experten überlasten kann (Jiang et al., 2024).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Dichter [[attention-and-transformers\|Transformer]] | Jedes Token nutzt alle Parameter; Rechenaufwand und Speicher wachsen gemeinsam | Einfaches Training und einfacher Betrieb |
| [[knowledge-distillation\|Knowledge Distillation]] | Trainiert ein kleines dichtes Modell, ein großes nachzuahmen; die Destillation eines dünn besetzten Switch-Modells in ein dichtes behielt rund 30 % seines Qualitätsgewinns bei 10- bis 100-mal kleinerer Größe (Fedus et al., 2021) | Einsatz, bei dem der Speicher der Engpass ist |
| [[quantisation\|Quantisierung]] | Speichert dieselben Parameter mit weniger Bits; senkt den Speicherbedarf, was MoE nicht tut | Ein (auch MoE-)Modell in begrenzten Speicher bringen |
| [[ensemble-methods\|Ensemble-Methoden]] | Mehrere vollständige Modelle laufen lassen und alle Vorhersagen kombinieren | Klassisches ML, wenn jedes Modell günstig ist |

### In der Praxis
- Aktive und gesamte Parameter beantworten verschiedene Fragen: Rechenaufwand und Latenz folgen den aktiven Parametern, der Speicher der Gesamtzahl (Jiang et al., 2024). Für den lokalen Einsatz muss die volle Größe eines MoE-Modells in den Speicher passen, auch wenn jedes Token nur einen Bruchteil davon berührt; [[quantisation|Quantisierung]] und [[model-compression|Modellkompression]] setzen an dieser Seite an.
- Der Koeffizient des Balancing-Verlusts muss groß genug sein, um die Last zu verteilen, aber klein genug, um den Trainingsverlust nicht zu dominieren; Fedus et al. (2021) fanden `α = 10⁻²` in einem Bereich von `10⁻¹` bis `10⁻⁵` geeignet.
- Für das Fine-Tuning fand ST-MoE, dass dünn besetzte und dichte Modelle unterschiedliche Vorgehensweisen brauchen und dass dünn besetzte Modelle beim Fine-Tuning robust gegenüber verworfenen Tokens sind (Zoph et al., 2022).
- Benchmarks von MoE-Modellen werden meist bei gleichen aktiven Parametern verglichen, wie im Vergleich von Mixtral mit Llama 2 (Jiang et al., 2024); [[llm-cost-optimisation|Kostenvergleiche]] brauchen zusätzlich Speicher und Hardware-Auslastung, die dieser Vergleich auslässt.

### Regulatorischer Kontext
Die [[eu-ai-act|KI-Verordnung]] vermutet für KI-Modelle mit allgemeinem Verwendungszweck, die mit mehr als 10²⁵ Gleitkommaoperationen trainiert wurden, eine hohe Auswirkungskapazität und damit ein systemisches Risiko. Die Schwelle bezieht sich auf den Trainingsaufwand, nicht auf die Zahl der Parameter; bei MoE-Modellen folgt der Rechenaufwand je Token den aktiven und nicht den gesamten Parametern (Jiang et al., 2024), sodass die gesamte Parameterzahl allein nicht zeigt, ob ein Modell die Schwelle überschreitet.

### Merksatz
Ein Mixture-of-Experts-Modell schickt jedes Token an wenige von vielen Experten; es kann so die Wissenskapazität eines sehr großen Modells zum Rechenaufwand eines viel kleineren haben, braucht aber weiterhin den Speicher des großen.

### Quellen
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer.* ICLR 2017. [arXiv:1701.06538](https://arxiv.org/abs/1701.06538)
- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding.* [arXiv:2006.16668](https://arxiv.org/abs/2006.16668)
- Fedus, W., Zoph, B. & Shazeer, N. (2021). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity.* JMLR 23 (2022). [arXiv:2101.03961](https://arxiv.org/abs/2101.03961)
- Zoph, B. et al. (2022). *ST-MoE: Designing Stable and Transferable Sparse Expert Models.* [arXiv:2202.08906](https://arxiv.org/abs/2202.08906)
- Jiang, A. Q. et al. (2024). *Mixtral of Experts.* [arXiv:2401.04088](https://arxiv.org/abs/2401.04088)
- Dai, D. et al. (2024). *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.* [arXiv:2401.06066](https://arxiv.org/abs/2401.06066)
- Yang, A. et al. (2025). *Qwen3 Technical Report.* [arXiv:2505.09388](https://arxiv.org/abs/2505.09388)
