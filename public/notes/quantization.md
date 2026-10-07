---
title_en: Quantization
title_de: Quantisierung
entity_type: Method
sources:
- https://arxiv.org/abs/2106.08295
- https://arxiv.org/abs/1712.05877
- https://arxiv.org/abs/2208.07339
- https://arxiv.org/abs/2210.17323
- https://arxiv.org/abs/2306.00978
- https://arxiv.org/abs/2305.14314
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Quantization stores a network's weights, and often its activations, with fewer bits, for example 8-bit integers instead of 32-bit floats, which reduces memory, power and latency at the cost of some added noise (Nagel et al., 2021). Post-training quantization works without retraining and usually suffices for 8 bits; quantization-aware training enables lower bit widths (Nagel et al., 2021; Jacob et al., 2017). For large language models, methods such as LLM.int8() (Dettmers et al., 2022), GPTQ (Frantar et al., 2022) and AWQ (Lin et al., 2023) quantize weights to 8, 4 or 3 bits with little loss, and QLoRA fine-tunes on a 4-bit base model (Dettmers et al., 2023).

### How it works

Floating-point values are mapped to a small set of integer levels using a scale and, optionally, an offset; computations then run on the integers, or the weights are converted back to higher precision just before use. The methods differ in how they choose the mapping and how they protect values that are sensitive to rounding.

```text
1. Why quantize
▼
2. Post-training quantization
▼
3. Quantization-aware training
▼
4. Outliers in large language models
▼
5. Low-bit weight quantization for LLMs
▼
6. Fine-tuning quantized models
```

#### 1. Why quantize

Reducing the power and latency of neural network inference is key for edge devices with strict power and compute limits, and quantization is one of the most effective ways to achieve it, although the noise it introduces can reduce accuracy (Nagel et al., 2021). Jacob et al. (2017) proposed a scheme in which inference uses integer-only arithmetic, which runs more efficiently than floating point on common integer hardware and improved the trade-off between accuracy and on-device latency even for efficient MobileNets.

#### 2. Post-training quantization

Post-training quantization (PTQ) converts a trained model without retraining or labelled data, a lightweight push-button approach; in most cases it suffices for 8-bit quantization with close to floating-point accuracy (Nagel et al., 2021).

#### 3. Quantization-aware training

Quantization-aware training (QAT) simulates quantization during training or fine-tuning so that the model adapts to it; it needs labelled training data but enables lower bit widths with competitive results (Nagel et al., 2021). Jacob et al. (2017) co-designed such a training procedure with their integer-only inference scheme to preserve end-to-end accuracy.

#### 4. Outliers in large language models

Large language models contain highly systematic emergent outlier features that dominate attention and predictive performance and break simple 8-bit schemes (Dettmers et al., 2022). LLM.int8() quantizes most features with vector-wise scaling and isolates the outlier dimensions in a 16-bit matrix multiplication, while more than 99.9% of values are still multiplied in 8 bits. This halves the memory for inference and allowed models with up to 175 billion parameters to be used without performance degradation.

#### 5. Low-bit weight quantization for LLMs

GPTQ is a one-shot weight quantization method based on approximate second-order information; it quantized GPT models with 175 billion parameters in about four GPU hours to 3 or 4 bits per weight with negligible accuracy loss, allowing such a model to run on a single GPU, with inference speedups over FP16 of around 3.25× on A100 GPUs (Frantar et al., 2022). AWQ observes that not all weights are equally important: protecting only 1% of salient weight channels, identified from activation statistics, greatly reduces quantization error, and scaling these channels avoids hardware-unfriendly mixed precision (Lin et al., 2023).

#### 6. Fine-tuning quantized models

QLoRA back-propagates gradients through a frozen, 4-bit quantized pretrained language model into low-rank adapters, which reduced memory enough to fine-tune a 65-billion-parameter model on a single 48 GB GPU while preserving full 16-bit fine-tuning performance (Dettmers et al., 2023; [[lora|LoRA]]).

#### Origin and variants

Integer-only inference with quantization-aware training (Jacob et al., 2017) and the systematic treatment of PTQ and QAT (Nagel et al., 2021) established quantization for efficient inference. LLM.int8() (Dettmers et al., 2022), GPTQ (Frantar et al., 2022) and AWQ (Lin et al., 2023) adapted it to large language models, and QLoRA (Dettmers et al., 2023) combined it with parameter-efficient fine-tuning.

### When to use it

- When a model must run on edge devices or with limited memory and latency budgets (Nagel et al., 2021; Jacob et al., 2017).
- When a large language model should run on fewer or smaller GPUs, low-bit weight quantization fits (Frantar et al., 2022; Lin et al., 2023).
- When a large model must be fine-tuned on limited hardware, QLoRA fits (Dettmers et al., 2023).

### Strengths and limitations

**Strengths**
- 8-bit post-training quantization is usually close to floating-point accuracy without retraining (Nagel et al., 2021).
- LLM.int8() halves inference memory without performance degradation up to 175 billion parameters (Dettmers et al., 2022).
- 3- to 4-bit weight quantization lets very large models run on a single GPU (Frantar et al., 2022).

**Limitations**
- Quantization noise can reduce accuracy, especially at low bit widths (Nagel et al., 2021).
- Lower bit widths often require quantization-aware training with labelled data (Nagel et al., 2021).
- Outlier features in LLMs break naive quantization schemes (Dettmers et al., 2022).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Post-training quantization | No retraining, no labels (Nagel et al., 2021) | 8-bit deployment |
| Quantization-aware training | Simulates quantization during training (Nagel et al., 2021; Jacob et al., 2017) | Lower bit widths |
| LLM.int8() | 8-bit with 16-bit handling of outlier features (Dettmers et al., 2022) | Large LLM inference without accuracy loss |
| GPTQ / AWQ | 3- to 4-bit weight-only quantization using second-order or activation information (Frantar et al., 2022; Lin et al., 2023) | Running large LLMs on few GPUs |
| QLoRA | Fine-tuning adapters on a frozen 4-bit model (Dettmers et al., 2023) | Fine-tuning on limited hardware |

### In practice

Quantized models are evaluated on the target task against the full-precision model, since average benchmarks can hide degradations ([[llm-evaluation|LLM Evaluation]]). Calibration data for PTQ should resemble the deployment data, and the bit width is chosen as a trade-off between memory, speed and accuracy (Nagel et al., 2021). Quantization complements distillation and parameter-efficient fine-tuning in the toolbox for adapting LLMs ([[llm-adaptation|LLM Adaptation]]).

### Key takeaway

Quantization stores models with fewer bits to save memory and time; post-training methods suffice for 8 bits, while LLM-specific methods reach 3 to 4 bits by protecting sensitive values.

### Sources

- Nagel, M. et al. (2021). *A White Paper on Neural Network Quantization.* [arXiv:2106.08295](https://arxiv.org/abs/2106.08295)
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference.* CVPR 2018. [arXiv:1712.05877](https://arxiv.org/abs/1712.05877)
- Dettmers, T. et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale.* NeurIPS 2022. [arXiv:2208.07339](https://arxiv.org/abs/2208.07339)
- Frantar, E. et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers.* ICLR 2023. [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)
- Lin, J. et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration.* MLSys 2024. [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Quantisierung speichert die Gewichte eines Netzes und oft auch seine Aktivierungen mit weniger Bits, etwa als 8-Bit-Ganzzahlen statt 32-Bit-Gleitkommazahlen; das senkt Speicherbedarf, Energieverbrauch und Latenz, fügt aber etwas Rauschen hinzu (Nagel et al., 2021). Post-Training Quantization kommt ohne Neutraining aus und genügt meist für 8 Bit; Quantization-Aware Training ermöglicht geringere Bitbreiten (Nagel et al., 2021; Jacob et al., 2017). Für große Sprachmodelle quantisieren Verfahren wie LLM.int8() (Dettmers et al., 2022), GPTQ (Frantar et al., 2022) und AWQ (Lin et al., 2023) die Gewichte mit geringem Verlust auf 8, 4 oder 3 Bit, und QLoRA stimmt auf einem 4-Bit-Basismodell fein ab (Dettmers et al., 2023).

### Funktionsweise

Gleitkommawerte werden mit einem Skalierungsfaktor und optional einem Versatz auf eine kleine Menge ganzzahliger Stufen abgebildet; die Berechnungen laufen dann auf den Ganzzahlen, oder die Gewichte werden erst unmittelbar vor der Verwendung in höhere Genauigkeit zurückgewandelt. Die Verfahren unterscheiden sich darin, wie sie die Abbildung wählen und wie sie rundungsempfindliche Werte schützen.

```text
1. Warum quantisieren
▼
2. Post-Training Quantization
▼
3. Quantization-Aware Training
▼
4. Ausreißer in großen Sprachmodellen
▼
5. Gewichtsquantisierung mit wenigen Bits für LLMs
▼
6. Fine-Tuning quantisierter Modelle
```

#### 1. Warum quantisieren

Energieverbrauch und Latenz der Inferenz zu senken ist für Edge-Geräte mit strengen Energie- und Rechengrenzen entscheidend, und Quantisierung ist einer der wirksamsten Wege dorthin, auch wenn das eingeführte Rauschen die Genauigkeit mindern kann (Nagel et al., 2021). Jacob et al. (2017) schlugen ein Verfahren vor, bei dem die Inferenz nur Ganzzahlarithmetik nutzt, die auf üblicher Ganzzahlhardware effizienter läuft als Gleitkommarechnung, und verbesserten damit selbst bei effizienten MobileNets die Abwägung zwischen Genauigkeit und Latenz auf dem Gerät.

#### 2. Post-Training Quantization

Post-Training Quantization (PTQ) wandelt ein trainiertes Modell ohne Neutraining und ohne gelabelte Daten um, ein leichtgewichtiger Ansatz auf Knopfdruck; in den meisten Fällen genügt sie für 8-Bit-Quantisierung mit nahezu Gleitkomma-Genauigkeit (Nagel et al., 2021).

#### 3. Quantization-Aware Training

Quantization-Aware Training (QAT) simuliert die Quantisierung während Training oder Fine-Tuning, damit sich das Modell daran anpasst; es braucht gelabelte Trainingsdaten, ermöglicht aber geringere Bitbreiten mit konkurrenzfähigen Ergebnissen (Nagel et al., 2021). Jacob et al. (2017) entwickelten ein solches Trainingsverfahren zusammen mit ihrer reinen Ganzzahl-Inferenz, um die Genauigkeit durchgängig zu erhalten.

#### 4. Ausreißer in großen Sprachmodellen

Große Sprachmodelle enthalten sehr systematische emergente Ausreißermerkmale, die Attention und Vorhersageleistung dominieren und einfache 8-Bit-Verfahren scheitern lassen (Dettmers et al., 2022). LLM.int8() quantisiert die meisten Merkmale mit vektorweiser Skalierung und lagert die Ausreißerdimensionen in eine 16-Bit-Matrixmultiplikation aus, während mehr als 99,9 % der Werte weiterhin in 8 Bit multipliziert werden. Das halbiert den Speicher für die Inferenz und erlaubte, Modelle mit bis zu 175 Milliarden Parametern ohne Leistungsverlust zu nutzen.

#### 5. Gewichtsquantisierung mit wenigen Bits für LLMs

GPTQ ist ein einstufiges Verfahren zur Gewichtsquantisierung auf Basis näherungsweiser Information zweiter Ordnung; es quantisierte GPT-Modelle mit 175 Milliarden Parametern in etwa vier GPU-Stunden auf 3 oder 4 Bit je Gewicht bei vernachlässigbarem Genauigkeitsverlust, sodass ein solches Modell auf einer einzigen GPU läuft, mit einer Inferenzbeschleunigung gegenüber FP16 von etwa 3,25-fach auf A100-GPUs (Frantar et al., 2022). AWQ geht davon aus, dass nicht alle Gewichte gleich wichtig sind: Werden nur 1 % der hervorstechenden Gewichtskanäle geschützt, die anhand von Aktivierungsstatistiken bestimmt werden, sinkt der Quantisierungsfehler stark, und das Skalieren dieser Kanäle vermeidet hardwareunfreundliche gemischte Genauigkeit (Lin et al., 2023).

#### 6. Fine-Tuning quantisierter Modelle

QLoRA propagiert Gradienten durch ein eingefrorenes, auf 4 Bit quantisiertes vortrainiertes Sprachmodell in Low-Rank-Adapter und verringerte den Speicherbedarf so weit, dass sich ein Modell mit 65 Milliarden Parametern auf einer einzigen 48-GB-GPU feinabstimmen ließ, bei voller 16-Bit-Fine-Tuning-Leistung (Dettmers et al., 2023; [[lora|LoRA]]).

#### Ursprung und Varianten

Reine Ganzzahl-Inferenz mit Quantization-Aware Training (Jacob et al., 2017) und die systematische Darstellung von PTQ und QAT (Nagel et al., 2021) etablierten Quantisierung für effiziente Inferenz. LLM.int8() (Dettmers et al., 2022), GPTQ (Frantar et al., 2022) und AWQ (Lin et al., 2023) übertrugen sie auf große Sprachmodelle, und QLoRA (Dettmers et al., 2023) verband sie mit parametereffizientem Fine-Tuning.

### Wann einsetzen

- Wenn ein Modell auf Edge-Geräten oder mit knappem Speicher- und Latenzbudget laufen muss (Nagel et al., 2021; Jacob et al., 2017).
- Wenn ein großes Sprachmodell auf weniger oder kleineren GPUs laufen soll, passt Gewichtsquantisierung mit wenigen Bits (Frantar et al., 2022; Lin et al., 2023).
- Wenn ein großes Modell auf begrenzter Hardware feinabgestimmt werden muss, passt QLoRA (Dettmers et al., 2023).

### Stärken und Grenzen

**Stärken**
- 8-Bit-Post-Training-Quantization erreicht meist nahezu Gleitkomma-Genauigkeit ohne Neutraining (Nagel et al., 2021).
- LLM.int8() halbiert den Inferenzspeicher ohne Leistungsverlust bis 175 Milliarden Parameter (Dettmers et al., 2022).
- Gewichtsquantisierung auf 3 bis 4 Bit lässt sehr große Modelle auf einer einzigen GPU laufen (Frantar et al., 2022).

**Einschränkungen**
- Quantisierungsrauschen kann die Genauigkeit mindern, besonders bei geringen Bitbreiten (Nagel et al., 2021).
- Geringere Bitbreiten erfordern oft Quantization-Aware Training mit gelabelten Daten (Nagel et al., 2021).
- Ausreißermerkmale in LLMs lassen naive Quantisierungsverfahren scheitern (Dettmers et al., 2022).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Post-Training Quantization | Kein Neutraining, keine Labels (Nagel et al., 2021) | 8-Bit-Bereitstellung |
| Quantization-Aware Training | Simuliert die Quantisierung im Training (Nagel et al., 2021; Jacob et al., 2017) | Geringere Bitbreiten |
| LLM.int8() | 8 Bit mit 16-Bit-Behandlung von Ausreißermerkmalen (Dettmers et al., 2022) | Inferenz großer LLMs ohne Genauigkeitsverlust |
| GPTQ / AWQ | Reine Gewichtsquantisierung auf 3 bis 4 Bit mit Information zweiter Ordnung oder aus Aktivierungen (Frantar et al., 2022; Lin et al., 2023) | Große LLMs auf wenigen GPUs |
| QLoRA | Fine-Tuning von Adaptern auf einem eingefrorenen 4-Bit-Modell (Dettmers et al., 2023) | Fine-Tuning auf begrenzter Hardware |

### In der Praxis

Quantisierte Modelle werden auf der Zielaufgabe gegen das Modell in voller Genauigkeit evaluiert, da durchschnittliche Benchmarks Verschlechterungen verbergen können ([[llm-evaluation|LLM-Evaluation]]). Kalibrierungsdaten für PTQ sollten den Einsatzdaten ähneln, und die Bitbreite wird als Abwägung zwischen Speicher, Geschwindigkeit und Genauigkeit gewählt (Nagel et al., 2021). Quantisierung ergänzt Distillation und parametereffizientes Fine-Tuning im Werkzeugkasten zur Anpassung von LLMs ([[llm-adaptation|LLM-Anpassung]]).

### Merksatz

Quantisierung speichert Modelle mit weniger Bits, um Speicher und Zeit zu sparen; Post-Training-Verfahren genügen für 8 Bit, während LLM-spezifische Verfahren durch den Schutz empfindlicher Werte 3 bis 4 Bit erreichen.

### Quellen

- Nagel, M. et al. (2021). *A White Paper on Neural Network Quantization.* [arXiv:2106.08295](https://arxiv.org/abs/2106.08295)
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference.* CVPR 2018. [arXiv:1712.05877](https://arxiv.org/abs/1712.05877)
- Dettmers, T. et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale.* NeurIPS 2022. [arXiv:2208.07339](https://arxiv.org/abs/2208.07339)
- Frantar, E. et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers.* ICLR 2023. [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)
- Lin, J. et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration.* MLSys 2024. [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
