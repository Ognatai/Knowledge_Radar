---
title_en: QLoRA (Quantised Low-Rank Adaptation)
title_de: QLoRA (Quantised Low-Rank Adaptation)
entity_type: Method
aliases:
- QLoRA
- 4-bit NormalFloat
- NF4
sources:
- https://arxiv.org/abs/2305.14314
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

QLoRA fine-tunes [[large-language-models|large language models]] on a single GPU by keeping the pre-trained weights frozen in 4-bit precision and training only small [[lora|LoRA]] adapters on top: gradients flow through the quantised model into the adapters (Dettmers et al., 2023). Three techniques make this work without losing quality: the 4-bit NormalFloat (NF4) data type, which is information-theoretically optimal for normally distributed weights, double quantisation of the quantisation constants, and paged optimisers that move optimiser states to CPU memory when the GPU runs out (Dettmers et al., 2023). With QLoRA, a 65-billion-parameter model can be fine-tuned on one 48 GB GPU instead of more than 780 GB of GPU memory, while matching 16-bit fine-tuning performance in the authors' experiments.

### How it works

```text
pre-trained model weights W (16-bit)
 ▼ quantise in blocks of 64 to 4-bit NormalFloat (NF4); store one quantisation constant per block
 ▼ double quantisation: quantise those constants to 8-bit in blocks of 256
frozen 4-bit model + LoRA adapters L₁, L₂ (BFloat16) on all linear Transformer layers
forward:  Y = X · dequant(W_NF4) + X · L₁ · L₂       (computation in BFloat16)
backward: gradients only for L₁, L₂ (through the dequantised weights)
 ▼ paged optimiser states: evicted to CPU RAM on memory spikes, paged back for the update
```

#### 1. The memory problem

Regular 16-bit fine-tuning of a 65-billion-parameter LLaMA model requires more than 780 GB of GPU memory (Dettmers et al., 2023). Quantisation could reduce the footprint, but earlier methods only worked for inference and broke down during training. LoRA reduces the number of trainable parameters, yet the frozen base model still has to fit in memory in 16 bit ([[lora|LoRA]], [[quantisation|quantisation]]). QLoRA combines both: a 4-bit base model plus 16-bit adapters (Dettmers et al., 2023).

#### 2. 4-bit NormalFloat (NF4)

Quantile quantisation assigns each quantisation bin an equal share of the values, which is optimal but expensive and error-prone when quantiles must be estimated (Dettmers et al., 2023). Pre-trained weights, however, are approximately zero-centred and normally distributed, so their quantiles are known up to a scale factor. NF4 takes the quantiles of a standard normal distribution, normalises them to the range [−1, 1] and quantises each weight block after rescaling it by its absolute maximum; an asymmetric construction ensures an exact zero. Empirically, NF4 gave better results than 4-bit integers and 4-bit floats (Dettmers et al., 2023).

#### 3. Double quantisation

Precise 4-bit quantisation needs small blocks, and each block needs a quantisation constant: with 32-bit constants and blocks of 64 weights, the constants add 0.5 bits per parameter (Dettmers et al., 2023). Double quantisation quantises these constants again, to 8-bit floats in blocks of 256, which reduces the overhead to about 0.127 bits per parameter, a saving of about 0.37 bits per parameter or roughly 3 GB for a 65B model (Dettmers et al., 2023).

#### 4. Paged optimisers and the forward pass

Long sequences can cause memory spikes during gradient checkpointing. Paged optimisers use NVIDIA unified memory to evict optimiser states to CPU RAM when the GPU runs out and page them back for the update step (Dettmers et al., 2023). In the forward pass, each 4-bit weight tensor is dequantised to BFloat16 for the matrix multiplication, so QLoRA has one storage data type (NF4) and one computation data type (BFloat16). Only the adapter weights receive gradients. Applying LoRA adapters to all linear Transformer layers, not just the attention projections, was critical to match 16-bit performance (Dettmers et al., 2023).

#### 5. Results and findings

With QLoRA, the authors fine-tuned more than 1,000 models from 80 million to 65 billion parameters (Dettmers et al., 2023). Their Guanaco models, LLaMA fine-tuned on the 9,000-example OASST1 dataset, reached 99.3% of [[chatgpt|ChatGPT]]'s performance on the Vicuna benchmark after 24 hours on a single GPU; the 7B Guanaco needed 5 GB of memory. [[data-governance|Data quality]] mattered more than size: the 9,000-example OASST1 dataset outperformed a 450,000-example subsample of FLAN v2 for chatbot performance. Strong MMLU scores did not imply strong chatbot performance, and GPT-4 judgements were a cheap, reasonable alternative to human evaluation, although chatbot benchmarks proved unreliable (Dettmers et al., 2023); see [[llm-as-a-judge|LLM as a judge]].

#### Origin and variants

Tim Dettmers, Artidoro Pagnoni, Ari Holtzman and Luke Zettlemoyer at the University of Washington published QLoRA in 2023 and released code including CUDA kernels for 4-bit training (Dettmers et al., 2023). It builds on [[lora|LoRA]] and on earlier 8-bit and 4-bit inference quantisation. Fine-tuning methods are compared in [[llm-adaptation|LLM adaptation]].

### When to use it

- Fine-tuning large open models such as [[llama|LLaMA]] on limited GPU memory, for example one consumer or workstation GPU (Dettmers et al., 2023).
- [[llm-alignment|Instruction tuning]] or domain adaptation with a small, high-quality dataset (Dettmers et al., 2023).
- Many experiments over models and datasets, where cheap fine-tuning runs matter (Dettmers et al., 2023).

### Strengths and limitations

**Strengths**
- Fine-tuning of 33B and 65B models on a single 24 or 48 GB GPU (Dettmers et al., 2023).
- Matched 16-bit fine-tuning performance in the experiments where both could be compared (Dettmers et al., 2023).
- Small adapters are cheap to store and swap ([[lora|LoRA]]).

**Limitations**
- The authors did not establish that QLoRA matches full 16-bit fine-tuning at 33B and 65B scale, because the comparison was too expensive (Dettmers et al., 2023).
- Benchmarks for chatbot quality are unreliable, so gains must be checked on the target task (Dettmers et al., 2023).

### Comparison

| Method | Base weights | Trainable | GPU memory (65B) |
|---|---|---|---|
| Full fine-tuning | 16-bit, trained | all | > 780 GB |
| [[lora\|LoRA]] | 16-bit, frozen | low-rank adapters | base model in 16-bit |
| QLoRA | 4-bit NF4, frozen | low-rank adapters on all linear layers | < 48 GB |

Source: Dettmers et al. (2023).

### In practice

QLoRA makes adapting large open models feasible on a single GPU; the adapters can be merged into the base model or kept separate for serving ([[lora|LoRA]]). Because data quality outweighs quantity, a few thousand well-chosen examples are often a better starting point than a large, noisy dataset (Dettmers et al., 2023). Whether fine-tuning is the right tool at all is discussed in [[rag-vs-fine-tuning|RAG vs fine-tuning]].

### Key takeaway

QLoRA freezes an LLM in 4-bit NormalFloat, adds LoRA adapters to every linear layer and trains only those, with double quantisation and paged optimisers saving further memory, which brings fine-tuning of 65-billion-parameter models down to a single GPU without measurable quality loss in the reported experiments.

### Sources

- Dettmers, T., Pagnoni, A., Holtzman, A. & Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

QLoRA feinjustiert große Sprachmodelle auf einer einzigen GPU, indem es die vortrainierten Gewichte eingefroren in 4-Bit-Präzision hält und nur kleine [[lora|LoRA]]-Adapter darauf trainiert: Gradienten fließen durch das quantisierte Modell in die Adapter (Dettmers et al., 2023). Drei Techniken machen das ohne Qualitätsverlust möglich: der Datentyp 4-bit NormalFloat (NF4), der informationstheoretisch optimal für normalverteilte Gewichte ist, die doppelte Quantisierung der Quantisierungskonstanten und Paged Optimizer, die Optimierungszustände in den CPU-Speicher verschieben, wenn der GPU-Speicher knapp wird (Dettmers et al., 2023). Mit QLoRA lässt sich ein Modell mit 65 Milliarden Parametern auf einer GPU mit 48 GB statt mit mehr als 780 GB GPU-Speicher feinjustieren und erreicht in den Experimenten der Autoren die Leistung von Fine-Tuning in 16 Bit.

### Funktionsweise

```text
vortrainierte Modellgewichte W (16 Bit)
 ▼ in Blöcken von 64 zu 4-bit NormalFloat (NF4) quantisieren; eine Quantisierungskonstante je Block speichern
 ▼ doppelte Quantisierung: diese Konstanten in Blöcken von 256 auf 8 Bit quantisieren
eingefrorenes 4-Bit-Modell + LoRA-Adapter L₁, L₂ (BFloat16) auf allen linearen Transformer-Schichten
vorwärts:  Y = X · dequant(W_NF4) + X · L₁ · L₂       (Berechnung in BFloat16)
rückwärts: Gradienten nur für L₁, L₂ (über die dequantisierten Gewichte)
 ▼ Paged Optimizer: Zustände bei Speicherspitzen in den CPU-RAM ausgelagert, für das Update zurückgeholt
```

#### 1. Das Speicherproblem

Gewöhnliches Fine-Tuning eines LLaMA-Modells mit 65 Milliarden Parametern in 16 Bit braucht mehr als 780 GB GPU-Speicher (Dettmers et al., 2023). Quantisierung könnte den Bedarf senken, frühere Verfahren funktionierten aber nur für die Inferenz und versagten im Training. LoRA verringert die Zahl der trainierbaren Parameter, doch das eingefrorene Basismodell muss weiterhin in 16 Bit in den Speicher passen ([[lora|LoRA]], [[quantisation|Quantisierung]]). QLoRA verbindet beides: ein Basismodell in 4 Bit plus Adapter in 16 Bit (Dettmers et al., 2023).

#### 2. 4-bit NormalFloat (NF4)

Quantil-Quantisierung weist jedem Quantisierungsintervall gleich viele Werte zu, was optimal, aber teuer und fehleranfällig ist, wenn Quantile geschätzt werden müssen (Dettmers et al., 2023). Vortrainierte Gewichte sind jedoch annähernd um null zentriert und normalverteilt, sodass ihre Quantile bis auf einen Skalierungsfaktor bekannt sind. NF4 nimmt die Quantile einer Standardnormalverteilung, normalisiert sie auf den Bereich [−1, 1] und quantisiert jeden Gewichtsblock nach Skalierung mit seinem Betragsmaximum; eine asymmetrische Konstruktion sorgt für eine exakte Null. Empirisch lieferte NF4 bessere Ergebnisse als 4-Bit-Ganzzahlen und 4-Bit-Gleitkommazahlen (Dettmers et al., 2023).

#### 3. Doppelte Quantisierung

Genaue 4-Bit-Quantisierung braucht kleine Blöcke, und jeder Block braucht eine Quantisierungskonstante: Mit 32-Bit-Konstanten und Blöcken zu 64 Gewichten kommen 0,5 Bit je Parameter hinzu (Dettmers et al., 2023). Die doppelte Quantisierung quantisiert diese Konstanten erneut, auf 8-Bit-Gleitkommazahlen in Blöcken zu 256, was den Zusatzaufwand auf etwa 0,127 Bit je Parameter senkt, eine Ersparnis von etwa 0,37 Bit je Parameter oder rund 3 GB für ein 65B-Modell (Dettmers et al., 2023).

#### 4. Paged Optimizer und Vorwärtsdurchlauf

Lange Sequenzen können beim Gradient Checkpointing Speicherspitzen verursachen. Paged Optimizer nutzen den Unified Memory von NVIDIA, um Optimierungszustände in den CPU-RAM auszulagern, wenn der GPU-Speicher ausgeht, und sie für den Update-Schritt zurückzuholen (Dettmers et al., 2023). Im Vorwärtsdurchlauf wird jeder 4-Bit-Gewichtstensor für die Matrixmultiplikation zu BFloat16 dequantisiert, sodass QLoRA einen Speicherdatentyp (NF4) und einen Rechendatentyp (BFloat16) hat. Nur die Adaptergewichte erhalten Gradienten. LoRA-Adapter auf allen linearen Transformer-Schichten statt nur auf den Attention-Projektionen waren entscheidend, um die Leistung in 16 Bit zu erreichen (Dettmers et al., 2023).

#### 5. Ergebnisse und Befunde

Mit QLoRA feinjustierten die Autoren mehr als 1.000 Modelle mit 80 Millionen bis 65 Milliarden Parametern (Dettmers et al., 2023). Ihre Guanaco-Modelle, LLaMA feinjustiert auf dem Datensatz OASST1 mit 9.000 Beispielen, erreichten nach 24 Stunden auf einer GPU 99,3 % der Leistung von [[chatgpt|ChatGPT]] auf dem Vicuna-Benchmark; das 7B-Guanaco brauchte 5 GB Speicher. [[data-governance|Datenqualität]] zählte mehr als Menge: Der Datensatz OASST1 mit 9.000 Beispielen übertraf eine Stichprobe von 450.000 Beispielen aus FLAN v2 bei der Chatbot-Leistung. Hohe MMLU-Werte bedeuteten keine starke Chatbot-Leistung, und Urteile von GPT-4 waren eine günstige, vernünftige Alternative zur menschlichen Bewertung, wobei sich Chatbot-Benchmarks als unzuverlässig erwiesen (Dettmers et al., 2023); siehe [[llm-as-a-judge|LLM as a Judge]].

#### Herkunft und Varianten

Tim Dettmers, Artidoro Pagnoni, Ari Holtzman und Luke Zettlemoyer von der University of Washington veröffentlichten QLoRA 2023 samt Code einschließlich CUDA-Kerneln für 4-Bit-Training (Dettmers et al., 2023). Es baut auf [[lora|LoRA]] auf und auf früheren Verfahren zur 8- und 4-Bit-Quantisierung für die Inferenz. Fine-Tuning-Verfahren vergleicht [[llm-adaptation|LLM-Anpassung]].

### Wann einsetzen

- Fine-Tuning großer offener Modelle wie [[llama|LLaMA]] mit begrenztem GPU-Speicher, etwa auf einer einzelnen Consumer- oder Workstation-GPU (Dettmers et al., 2023).
- [[llm-alignment|Instruction Tuning]] oder Domänenanpassung mit einem kleinen, hochwertigen Datensatz (Dettmers et al., 2023).
- Viele Experimente über Modelle und Datensätze hinweg, bei denen günstige Fine-Tuning-Läufe zählen (Dettmers et al., 2023).

### Stärken und Grenzen

**Stärken**
- Fine-Tuning von Modellen mit 33 und 65 Milliarden Parametern auf einer GPU mit 24 oder 48 GB (Dettmers et al., 2023).
- Erreichte in den Experimenten, in denen beides verglichen werden konnte, die Leistung von Fine-Tuning in 16 Bit (Dettmers et al., 2023).
- Kleine Adapter sind günstig zu speichern und auszutauschen ([[lora|LoRA]]).

**Grenzen**
- Die Autoren konnten nicht belegen, dass QLoRA bei 33B und 65B vollständiges Fine-Tuning in 16 Bit erreicht, weil der Vergleich zu teuer war (Dettmers et al., 2023).
- Benchmarks für Chatbot-Qualität sind unzuverlässig, daher müssen Verbesserungen auf der Zielaufgabe geprüft werden (Dettmers et al., 2023).

### Vergleich

| Verfahren | Basisgewichte | Trainierbar | GPU-Speicher (65B) |
|---|---|---|---|
| Vollständiges Fine-Tuning | 16 Bit, trainiert | alle | > 780 GB |
| [[lora\|LoRA]] | 16 Bit, eingefroren | Low-Rank-Adapter | Basismodell in 16 Bit |
| QLoRA | 4 Bit NF4, eingefroren | Low-Rank-Adapter auf allen linearen Schichten | < 48 GB |

Quelle: Dettmers et al. (2023).

### In der Praxis

QLoRA macht es möglich, große offene Modelle auf einer einzelnen GPU anzupassen; die Adapter können in das Basismodell eingerechnet oder für den Betrieb getrennt gehalten werden ([[lora|LoRA]]). Weil Datenqualität mehr zählt als Menge, sind einige Tausend gut gewählte Beispiele oft ein besserer Ausgangspunkt als ein großer, verrauschter Datensatz (Dettmers et al., 2023). Ob Fine-Tuning überhaupt das richtige Werkzeug ist, behandelt [[rag-vs-fine-tuning|RAG vs. Fine-Tuning]].

### Merksatz

QLoRA friert ein LLM in 4-bit NormalFloat ein, ergänzt LoRA-Adapter auf jeder linearen Schicht und trainiert nur diese, wobei doppelte Quantisierung und Paged Optimizer weiteren Speicher sparen; so wird Fine-Tuning von Modellen mit 65 Milliarden Parametern auf einer einzelnen GPU möglich, ohne messbaren Qualitätsverlust in den berichteten Experimenten.

### Quellen

- Dettmers, T., Pagnoni, A., Holtzman, A. & Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
