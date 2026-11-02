---
title_en: FlashAttention
title_de: FlashAttention
entity_type: Method
aliases:
- FlashAttention
- Flash Attention
- FlashAttention-2
- FlashAttention-3
- IO-aware attention
sources:
- https://arxiv.org/abs/2205.14135
- https://arxiv.org/abs/2307.08691
- https://arxiv.org/abs/2407.08608
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

FlashAttention computes exact Transformer attention faster and with memory linear instead of quadratic in sequence length, by never writing the full N × N attention matrix to the GPU's slow high-bandwidth memory (HBM) (Dao et al., 2022). It splits queries, keys and values into blocks that fit into fast on-chip SRAM, computes the [[softmax|softmax]] block by block with running normalisation statistics, and recomputes attention in the backward pass instead of storing it. It gave up to 7.6× faster attention on GPT-2 and made longer [[context-window|context windows]] practical; FlashAttention-2 roughly doubled the speed (Dao, 2024) and FlashAttention-3 uses the asynchrony and FP8 support of H100 GPUs (Shah et al., 2024).

### How it works

```text
standard attention:   S = QKᵀ  →  write S (N×N) to HBM  →  read S, P = softmax(S), write P to HBM  →  read P, O = PV
                       (O(N²) memory, many slow HBM reads and writes)

FlashAttention:
  for each block of K, V (outer loop):          load block into SRAM
      for each block of Q (inner loop):         load block into SRAM
          S_ij = Q_i K_jᵀ                        (on chip)
          update running max m and sum ℓ        (online softmax)
          O_i ← rescaled O_i + softmax-part · V_j
      write O_i, m_i, ℓ_i back to HBM            (no N×N matrix ever stored)
  backward pass: recompute S, P block-wise from Q, K, V and (m, ℓ)
```

#### 1. Why attention is memory-bound

For inputs Q, K, V of shape N × d, standard attention computes `S = QKᵀ`, `P = softmax(S)` row by row and `O = PV`, materialising S and P in HBM, which takes O(N²) memory; typically N ≫ d, for example N = 1,024 and d = 64 in GPT-2 (Dao et al., 2022). Many of these operations, such as softmax, masking and dropout, are memory-bound: runtime is dominated by moving data, not by arithmetic (Dao et al., 2022; [[attention-and-transformers|attention]]). On an A100 GPU, the 40–80 GB of HBM deliver 1.5–2.0 TB/s, while the 192 KB of on-chip SRAM in each of the 108 streaming multiprocessors reach about 19 TB/s, an order of magnitude faster but far smaller (Dao et al., 2022).

#### 2. Tiling with an online softmax

The softmax couples all keys of a row, so it cannot be split naively. FlashAttention keeps two statistics per row, the running maximum `m(x)` and the running sum of exponentials `ℓ(x)`; when a new block arrives, earlier partial results are rescaled with `e^(m_old − m_new)` and combined, which gives exactly the same result as a softmax over the whole row (Dao et al., 2022). Blocks of K and V are loaded into SRAM in the outer loop and blocks of Q in the inner loop, so the N × N matrix is never stored (Dao et al., 2022).

#### 3. Recomputation in the backward pass

Gradients normally need S and P. FlashAttention stores only the output O and the statistics (m, ℓ) and recomputes S and P block by block from Q, K and V during the backward pass; despite the extra FLOPs it runs faster, because it saves far more HBM traffic, and memory becomes linear in N (Dao et al., 2022; [[back-propagation|back-propagation]]).

#### 4. IO complexity

Standard attention needs Ω(Nd + N²) HBM accesses, FlashAttention O(N² d² / M) for SRAM size M, which for typical d and M is up to 9 times fewer; Dao et al. (2022) also prove a lower bound showing that no exact attention algorithm can asymptotically do better across all SRAM sizes. A block-sparse variant extends the same idea to approximate attention (Dao et al., 2022).

#### 5. FlashAttention-2 and -3

FlashAttention reached only 25–40% of the theoretical maximum FLOPs per second. FlashAttention-2 reduces non-matrix-multiply FLOPs, which run up to 16 times slower than matrix multiplies on GPUs, parallelises over the sequence length even for a single head, and distributes work between warps to reduce shared-memory communication; it is about twice as fast as FlashAttention, reaching 50–73% of peak on A100 and up to 225 TFLOP/s per GPU in end-to-end [[gpt|GPT]] training (Dao, 2024). FlashAttention-2 used only 35% of an H100; FlashAttention-3 overlaps computation and data movement through warp specialisation, interleaves block-wise matrix multiplies and softmax, and supports FP8 with block quantisation, reaching 740 TFLOP/s in FP16 (75% utilisation) and close to 1.2 PFLOP/s in FP8, with 2.6 times lower numerical error than a baseline FP8 attention (Shah et al., 2024; [[quantisation|quantisation]]).

#### Origin and variants

Tri Dao, Daniel Fu, Stefano Ermon, Atri Rudra and Christopher Ré presented FlashAttention at NeurIPS 2022 (Dao et al., 2022). It applies the established techniques of tiling and recomputation, and the softmax decomposition builds on earlier work on scaling softmax (Dao et al., 2022). FlashAttention-2 (Dao, 2024) and FlashAttention-3 (Shah et al., 2024) adapt it to newer GPUs.

### When to use it

- Training and serving Transformers on GPUs, especially with long sequences ([[large-language-models|large language models]], [[neural-network-training|neural network training]]).
- Extending context length without approximating attention: FlashAttention enabled the first Transformers to beat chance on Path-X (16K tokens) and Path-256 (64K tokens) (Dao et al., 2022).
- Reducing training cost: 15% faster BERT-large training than the MLPerf 1.1 record and 3× faster GPT-2 training (Dao et al., 2022; [[llm-cost-optimisation|LLM cost optimisation]]).

### Strengths and limitations

**Strengths**
- Exact: the result equals standard attention, unlike sparse or low-rank approximations (Dao et al., 2022).
- Memory linear in sequence length, which allows longer contexts and larger batches (Dao et al., 2022).
- Faster in wall-clock time despite extra FLOPs (Dao et al., 2022).

**Limitations**
- Still quadratic in compute: it reduces memory traffic, not the number of attention operations.
- Written as specialised GPU kernels that must be re-engineered for new hardware; FlashAttention-2 used only 35% of an H100 before FlashAttention-3 (Shah et al., 2024).
- Low-precision FP8 attention needs extra techniques to keep numerical error low (Shah et al., 2024).

### Comparison

| Method | Exact | Memory | Speed-up reported |
|---|---|---|---|
| Standard attention | yes | O(N²) | baseline |
| Approximate (sparse, low-rank) attention | no | sub-quadratic | often no wall-clock gain (Dao et al., 2022) |
| FlashAttention | yes | O(N) | up to 7.6× attention on GPT-2 (Dao et al., 2022) |
| FlashAttention-2 | yes | O(N) | about 2× over FlashAttention (Dao, 2024) |
| FlashAttention-3 | yes (FP16) | O(N) | 1.5–2× over FA-2 on H100 (Shah et al., 2024) |

Sources as given in the table.

### In practice

Because each generation of the kernels targets specific GPUs, the main decisions are hardware and precision: matching the kernel generation to the GPU and choosing between 16-bit formats and FP8 (Dao, 2024; Shah et al., 2024; [[mixed-precision-training|mixed-precision training]]). Because memory no longer grows quadratically, the [[context-window|context window]] is limited mainly by compute time and the KV cache at inference.

### Key takeaway

FlashAttention makes exact attention IO-aware: block-wise computation in fast SRAM with an online softmax and recomputation removes the N × N matrix from memory, cutting memory to linear and speeding up attention several-fold.

### Sources

- Dao, T., Fu, D. Y., Ermon, S., Rudra, A. & Ré, C. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- Dao, T. (2024). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning.* ICLR 2024. [arXiv:2307.08691](https://arxiv.org/abs/2307.08691)
- Shah, J., Bikshandi, G., Zhang, Y., Thakkar, V., Ramani, P. & Dao, T. (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision.* [arXiv:2407.08608](https://arxiv.org/abs/2407.08608)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

FlashAttention berechnet exakte Transformer-Attention schneller und mit Speicherbedarf linear statt quadratisch in der Sequenzlänge, indem es die vollständige N × N-Attention-Matrix nie in den langsamen High-Bandwidth-Speicher (HBM) der GPU schreibt (Dao et al., 2022). Es teilt Queries, Keys und Values in Blöcke auf, die in den schnellen SRAM auf dem Chip passen, berechnet die [[softmax|Softmax]] Block für Block mit laufenden Normierungsstatistiken und berechnet die Attention im Backward Pass neu, statt sie zu speichern. Das ergab bis zu 7,6-fach schnellere Attention bei GPT-2 und machte längere [[context-window|Kontextfenster]] praktikabel; FlashAttention-2 verdoppelte die Geschwindigkeit etwa (Dao, 2024), und FlashAttention-3 nutzt die Asynchronität und FP8-Unterstützung von H100-GPUs (Shah et al., 2024).

### Funktionsweise

```text
Standard-Attention:   S = QKᵀ  →  S (N×N) in HBM schreiben  →  S lesen, P = softmax(S), P in HBM schreiben  →  P lesen, O = PV
                      (O(N²) Speicher, viele langsame HBM-Zugriffe)

FlashAttention:
  für jeden Block von K, V (äußere Schleife):    Block in SRAM laden
      für jeden Block von Q (innere Schleife):    Block in SRAM laden
          S_ij = Q_i K_jᵀ                          (auf dem Chip)
          laufendes Maximum m und Summe ℓ aktualisieren   (Online-Softmax)
          O_i ← reskaliertes O_i + Softmax-Anteil · V_j
      O_i, m_i, ℓ_i zurück in HBM schreiben        (nie eine N×N-Matrix gespeichert)
  Backward Pass: S, P blockweise aus Q, K, V und (m, ℓ) neu berechnen
```

#### 1. Warum Attention speichergebunden ist

Für Eingaben Q, K, V der Form N × d berechnet Standard-Attention `S = QKᵀ`, zeilenweise `P = softmax(S)` und `O = PV` und legt S und P im HBM ab, was O(N²) Speicher braucht; typischerweise ist N ≫ d, etwa N = 1.024 und d = 64 bei GPT-2 (Dao et al., 2022). Viele dieser Operationen wie Softmax, Maskierung und Dropout sind speichergebunden: Die Laufzeit wird vom Datentransport bestimmt, nicht von der Rechnung (Dao et al., 2022; [[attention-and-transformers|Attention]]). Auf einer A100-GPU liefern die 40–80 GB HBM 1,5–2,0 TB/s, während die 192 KB SRAM auf dem Chip in jedem der 108 Streaming-Multiprozessoren etwa 19 TB/s erreichen, eine Größenordnung schneller, aber viel kleiner (Dao et al., 2022).

#### 2. Kachelung mit Online-Softmax

Die Softmax verknüpft alle Keys einer Zeile und lässt sich daher nicht einfach aufteilen. FlashAttention führt pro Zeile zwei Statistiken, das laufende Maximum `m(x)` und die laufende Summe der Exponentialwerte `ℓ(x)`; kommt ein neuer Block hinzu, werden frühere Teilergebnisse mit `e^(m_alt − m_neu)` umskaliert und kombiniert, was genau dasselbe Ergebnis wie eine Softmax über die ganze Zeile liefert (Dao et al., 2022). Blöcke von K und V werden in der äußeren Schleife in den SRAM geladen, Blöcke von Q in der inneren, sodass die N × N-Matrix nie gespeichert wird (Dao et al., 2022).

#### 3. Neuberechnung im Backward Pass

Gradienten brauchen normalerweise S und P. FlashAttention speichert nur die Ausgabe O und die Statistiken (m, ℓ) und berechnet S und P im Backward Pass blockweise aus Q, K und V neu; trotz der zusätzlichen FLOPs läuft es schneller, weil es viel mehr HBM-Verkehr spart, und der Speicher wird linear in N (Dao et al., 2022; [[back-propagation|Backpropagation]]).

#### 4. IO-Komplexität

Standard-Attention braucht Ω(Nd + N²) HBM-Zugriffe, FlashAttention O(N² d² / M) bei SRAM-Größe M, was für übliche d und M bis zu 9-mal weniger ist; Dao et al. (2022) beweisen außerdem eine untere Schranke, nach der kein exakter Attention-Algorithmus über alle SRAM-Größen asymptotisch besser sein kann. Eine blockdünn besetzte Variante überträgt dieselbe Idee auf approximative Attention (Dao et al., 2022).

#### 5. FlashAttention-2 und -3

FlashAttention erreichte nur 25–40 % der theoretisch möglichen FLOPs pro Sekunde. FlashAttention-2 verringert die FLOPs außerhalb von Matrixmultiplikationen, die auf GPUs bis zu 16-mal langsamer laufen, parallelisiert auch bei einem einzelnen Head über die Sequenzlänge und verteilt die Arbeit so auf Warps, dass weniger über den Shared Memory kommuniziert wird; es ist etwa doppelt so schnell wie FlashAttention, erreicht 50–73 % des Maximums auf der A100 und bis zu 225 TFLOP/s pro GPU beim Ende-zu-Ende-Training von GPT-Modellen (Dao, 2024). FlashAttention-2 nutzte eine H100 nur zu 35 %; FlashAttention-3 überlappt Rechnung und Datentransport durch Warp-Spezialisierung, verschränkt blockweise Matrixmultiplikationen und Softmax und unterstützt FP8 mit Blockquantisierung, womit es 740 TFLOP/s in FP16 (75 % Auslastung) und fast 1,2 PFLOP/s in FP8 erreicht, bei 2,6-mal geringerem numerischem Fehler als eine FP8-Baseline (Shah et al., 2024; [[quantisation|Quantisierung]]).

#### Ursprung und Varianten

Tri Dao, Daniel Fu, Stefano Ermon, Atri Rudra und Christopher Ré stellten FlashAttention auf der NeurIPS 2022 vor (Dao et al., 2022). Es wendet die etablierten Techniken Kachelung und Neuberechnung an, und die Zerlegung der Softmax baut auf früheren Arbeiten zur skalierten Softmax auf (Dao et al., 2022). FlashAttention-2 (Dao, 2024) und FlashAttention-3 (Shah et al., 2024) passen es an neuere GPUs an.

### Wann einsetzen

- Training und Betrieb von Transformern auf GPUs, besonders bei langen Sequenzen ([[large-language-models|große Sprachmodelle]], [[neural-network-training|Training neuronaler Netze]]).
- Kontextlänge erweitern, ohne die Attention zu approximieren: FlashAttention ermöglichte die ersten Transformer, die bei Path-X (16K Tokens) und Path-256 (64K Tokens) besser als Zufall abschnitten (Dao et al., 2022).
- Trainingskosten senken: 15 % schnelleres BERT-large-Training als der MLPerf-1.1-Rekord und dreifach schnelleres GPT-2-Training (Dao et al., 2022; [[llm-cost-optimisation|LLM-Kostenoptimierung]]).

### Stärken und Grenzen

**Stärken**
- Exakt: Das Ergebnis entspricht der Standard-Attention, anders als bei dünn besetzten oder niedrigrangigen Näherungen (Dao et al., 2022).
- Speicher linear in der Sequenzlänge, was längere Kontexte und größere Batches erlaubt (Dao et al., 2022).
- Trotz zusätzlicher FLOPs in Echtzeit schneller (Dao et al., 2022).

**Grenzen**
- Der Rechenaufwand bleibt quadratisch: Es verringert den Speicherverkehr, nicht die Zahl der Attention-Operationen.
- Als spezialisierte GPU-Kernel geschrieben, die für neue Hardware neu entwickelt werden müssen; FlashAttention-2 nutzte eine H100 nur zu 35 %, bevor FlashAttention-3 kam (Shah et al., 2024).
- Attention in FP8 braucht zusätzliche Techniken, um den numerischen Fehler gering zu halten (Shah et al., 2024).

### Vergleich

| Verfahren | Exakt | Speicher | Berichtete Beschleunigung |
|---|---|---|---|
| Standard-Attention | ja | O(N²) | Baseline |
| Approximative (dünn besetzte, niedrigrangige) Attention | nein | subquadratisch | oft kein Gewinn in Echtzeit (Dao et al., 2022) |
| FlashAttention | ja | O(N) | bis zu 7,6× bei der Attention von GPT-2 (Dao et al., 2022) |
| FlashAttention-2 | ja | O(N) | etwa 2× gegenüber FlashAttention (Dao, 2024) |
| FlashAttention-3 | ja (FP16) | O(N) | 1,5–2× gegenüber FA-2 auf H100 (Shah et al., 2024) |

Quellen wie in der Tabelle angegeben.

### In der Praxis

Weil jede Generation der Kernel auf bestimmte GPUs zielt, betreffen die wichtigsten Entscheidungen Hardware und Genauigkeit: die Kernel-Generation passend zur GPU wählen und zwischen 16-Bit-Formaten und FP8 entscheiden (Dao, 2024; Shah et al., 2024; [[mixed-precision-training|Mixed-Precision-Training]]). Weil der Speicher nicht mehr quadratisch wächst, wird das [[context-window|Kontextfenster]] vor allem durch Rechenzeit und bei der Inferenz durch den KV-Cache begrenzt.

### Merksatz

FlashAttention macht exakte Attention IO-bewusst: Blockweise Rechnung im schnellen SRAM mit Online-Softmax und Neuberechnung entfernt die N × N-Matrix aus dem Speicher, senkt den Speicherbedarf auf linear und beschleunigt die Attention um ein Mehrfaches.

### Quellen

- Dao, T., Fu, D. Y., Ermon, S., Rudra, A. & Ré, C. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- Dao, T. (2024). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning.* ICLR 2024. [arXiv:2307.08691](https://arxiv.org/abs/2307.08691)
- Shah, J., Bikshandi, G., Zhang, Y., Thakkar, V., Ramani, P. & Dao, T. (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision.* [arXiv:2407.08608](https://arxiv.org/abs/2407.08608)
