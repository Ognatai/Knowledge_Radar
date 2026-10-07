---
title_en: Mixed Precision Training
title_de: Mixed Precision Training
entity_type: Method
sources:
- https://arxiv.org/abs/1710.03740
- https://arxiv.org/abs/1905.12322
- https://arxiv.org/abs/2110.02861
- https://arxiv.org/abs/2205.14135
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Mixed precision training stores and computes most tensors in 16-bit floating point instead of 32-bit, which nearly halves memory use and speeds up training on hardware with half-precision units (Micikevicius et al., 2017). Two measures preserve accuracy: a 32-bit master copy of the weights and loss scaling to keep small gradients representable. The bfloat16 format keeps the range of 32-bit floats and trains without hyperparameter changes (Kalamkar et al., 2019); 8-bit optimizer states reduce memory further (Dettmers et al., 2021).

### How it works

Weights, activations and gradients are held in half precision during the forward and backward pass, while a single-precision copy of the weights accumulates the updates. The loss is multiplied by a scaling factor before back-propagation so that small gradient values do not underflow, and the gradients are unscaled before the update.

```text
1. FP32, FP16 and BF16
▼
2. Master weights in single precision
▼
3. Loss scaling
▼
4. BF16 without loss scaling
▼
5. Reducing optimizer memory
```

#### 1. FP32, FP16 and BF16

Single precision (FP32) is the default number format for training. IEEE half precision (FP16) needs half the memory but has a limited numerical range compared with FP32 (Micikevicius et al., 2017). BFLOAT16 (BF16) also uses 16 bits but represents the same range of values as FP32, and conversion to and from FP32 is simple (Kalamkar et al., 2019).

#### 2. Master weights in single precision

Micikevicius et al. (2017) store weights, activations and gradients in FP16, but keep a single-precision copy of the weights that accumulates the gradients after each optimizer step and is rounded to half precision for the next forward and backward pass. This prevents small updates from being lost when they are added to much larger weights.

#### 3. Loss scaling

Because FP16 has a limited range, small gradient values can underflow to zero. Scaling the loss before back-propagation shifts the gradients into the representable range; they are unscaled before the weight update (Micikevicius et al., 2017). With both measures, the technique worked for convolutional, recurrent and generative adversarial networks with more than 100 million parameters and reduced memory consumption by nearly 2× ([[neural-network-training|Training Neural Networks]]).

#### 4. BF16 without loss scaling

Kalamkar et al. (2019) studied BF16 for training across image classification, speech recognition, language modelling, generative networks and recommendation systems. Because BF16 keeps the FP32 range, no hyperparameter tuning was needed for convergence, unlike FP16; training with BF16 tensors achieved the same state-of-the-art results as FP32 in the same number of iterations and with no changes to hyperparameters.

#### 5. Reducing optimizer memory

Stateful optimizers such as Adam keep statistics of past gradients, which use memory that could otherwise hold model parameters (Dettmers et al., 2021). Block-wise dynamic quantization stores these statistics in 8 bits while maintaining the performance of 32-bit optimizer states, without changing optimizer hyperparameters, on tasks from language modelling to ImageNet classification ([[quantization|Quantization]]).

#### Origin and variants

Mixed precision with master weights and loss scaling was introduced by Micikevicius et al. (2017), BF16 training was validated by Kalamkar et al. (2019), and 8-bit optimizers (Dettmers et al., 2021) extended low precision to optimizer states. IO-aware kernels such as FlashAttention further reduce memory traffic during training (Dao et al., 2022).

### When to use it

- When model size or batch size is limited by GPU memory (Micikevicius et al., 2017).
- When the hardware has fast half-precision units, to speed up training (Micikevicius et al., 2017).
- When BF16 is supported, as the simpler option because it needs no loss scaling or hyperparameter changes (Kalamkar et al., 2019).

### Strengths and limitations

**Strengths**
- Nearly halves memory consumption (Micikevicius et al., 2017).
- BF16 matches FP32 results without hyperparameter changes (Kalamkar et al., 2019).
- 8-bit optimizer states keep 32-bit performance with a fraction of the memory (Dettmers et al., 2021).

**Limitations**
- FP16 has a limited range and needs loss scaling to avoid underflow (Micikevicius et al., 2017).
- A 32-bit master copy of the weights is still needed (Micikevicius et al., 2017).
- Speedups depend on hardware support for half precision (Micikevicius et al., 2017).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| FP32 training | Full single precision everywhere | Baseline, numerically sensitive cases |
| FP16 mixed precision | Half precision with FP32 master weights and loss scaling (Micikevicius et al., 2017) | GPUs with FP16 units |
| BF16 mixed precision | FP32 range in 16 bits, no loss scaling needed (Kalamkar et al., 2019) | Hardware with BF16 support |
| 8-bit optimizers | Optimizer states quantized block-wise to 8 bits (Dettmers et al., 2021) | Very large models with memory-heavy optimizers |

### In practice

Frameworks provide automatic mixed precision, which handles casting and loss scaling, so it can be enabled with little code; training curves are compared with an FP32 run to check that accuracy is preserved (Micikevicius et al., 2017; [[keras-and-tensorflow|Keras and TensorFlow]]). For fine-tuning large language models, mixed precision is combined with quantization and parameter-efficient methods ([[lora|LoRA]]).

### Key takeaway

Mixed precision trains in 16-bit numbers while protecting accuracy with FP32 master weights and loss scaling, nearly halving memory use.

### Sources

- Micikevicius, P. et al. (2017). *Mixed Precision Training.* ICLR 2018. [arXiv:1710.03740](https://arxiv.org/abs/1710.03740)
- Kalamkar, D. et al. (2019). *A Study of BFLOAT16 for Deep Learning Training.* [arXiv:1905.12322](https://arxiv.org/abs/1905.12322)
- Dettmers, T. et al. (2021). *8-bit Optimizers via Block-wise Quantization.* ICLR 2022. [arXiv:2110.02861](https://arxiv.org/abs/2110.02861)
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Mixed Precision Training speichert und berechnet die meisten Tensoren in 16-Bit- statt 32-Bit-Gleitkommazahlen; das halbiert den Speicherbedarf nahezu und beschleunigt das Training auf Hardware mit Einheiten für halbe Genauigkeit (Micikevicius et al., 2017). Zwei Maßnahmen erhalten die Genauigkeit: eine 32-Bit-Hauptkopie der Gewichte und Loss Scaling, damit kleine Gradienten darstellbar bleiben. Das Format bfloat16 behält den Wertebereich von 32-Bit-Zahlen und trainiert ohne geänderte Hyperparameter (Kalamkar et al., 2019); 8-Bit-Optimiererzustände verringern den Speicherbedarf weiter (Dettmers et al., 2021).

### Funktionsweise

Gewichte, Aktivierungen und Gradienten werden im Vorwärts- und Rückwärtsdurchlauf in halber Genauigkeit gehalten, während eine Kopie der Gewichte in einfacher Genauigkeit die Aktualisierungen aufnimmt. Der Verlust wird vor der Backpropagation mit einem Skalierungsfaktor multipliziert, damit kleine Gradientenwerte nicht unterlaufen, und die Gradienten werden vor der Aktualisierung zurückskaliert.

```text
1. FP32, FP16 und BF16
▼
2. Hauptgewichte in einfacher Genauigkeit
▼
3. Loss Scaling
▼
4. BF16 ohne Loss Scaling
▼
5. Speicher des Optimierers verringern
```

#### 1. FP32, FP16 und BF16

Einfache Genauigkeit (FP32) ist das übliche Zahlenformat für das Training. Die IEEE-Halbgenauigkeit (FP16) braucht halb so viel Speicher, hat aber gegenüber FP32 einen begrenzten Wertebereich (Micikevicius et al., 2017). BFLOAT16 (BF16) nutzt ebenfalls 16 Bit, stellt aber denselben Wertebereich wie FP32 dar, und die Umwandlung von und nach FP32 ist einfach (Kalamkar et al., 2019).

#### 2. Hauptgewichte in einfacher Genauigkeit

Micikevicius et al. (2017) speichern Gewichte, Aktivierungen und Gradienten in FP16, halten aber eine Kopie der Gewichte in einfacher Genauigkeit, die nach jedem Optimiererschritt die Gradienten aufnimmt und für den nächsten Vorwärts- und Rückwärtsdurchlauf auf halbe Genauigkeit gerundet wird. So gehen kleine Aktualisierungen nicht verloren, wenn sie zu viel größeren Gewichten addiert werden.

#### 3. Loss Scaling

Da FP16 einen begrenzten Wertebereich hat, können kleine Gradientenwerte auf null unterlaufen. Wird der Verlust vor der Backpropagation skaliert, verschieben sich die Gradienten in den darstellbaren Bereich; vor der Gewichtsaktualisierung werden sie zurückskaliert (Micikevicius et al., 2017). Mit beiden Maßnahmen funktionierte das Verfahren für konvolutionale, rekurrente und Generative Adversarial Networks mit mehr als 100 Millionen Parametern und verringerte den Speicherbedarf nahezu um die Hälfte ([[neural-network-training|Training neuronaler Netze]]).

#### 4. BF16 ohne Loss Scaling

Kalamkar et al. (2019) untersuchten BF16 für das Training in Bildklassifikation, Spracherkennung, Sprachmodellierung, generativen Netzen und Empfehlungssystemen. Da BF16 den FP32-Wertebereich behält, war anders als bei FP16 kein Hyperparameter-Tuning für die Konvergenz nötig; das Training mit BF16-Tensoren erreichte dieselben Spitzenergebnisse wie FP32 in derselben Zahl von Iterationen und ohne geänderte Hyperparameter.

#### 5. Speicher des Optimierers verringern

Zustandsbehaftete Optimierer wie Adam führen Statistiken früherer Gradienten mit, die Speicher belegen, der sonst Modellparameter aufnehmen könnte (Dettmers et al., 2021). Blockweise dynamische Quantisierung speichert diese Statistiken in 8 Bit und hält dabei die Leistung von 32-Bit-Optimiererzuständen, ohne die Hyperparameter des Optimierers zu ändern, bei Aufgaben von Sprachmodellierung bis ImageNet-Klassifikation ([[quantization|Quantisierung]]).

#### Ursprung und Varianten

Mixed Precision mit Hauptgewichten und Loss Scaling führten Micikevicius et al. (2017) ein, Kalamkar et al. (2019) bestätigten das Training mit BF16, und 8-Bit-Optimierer (Dettmers et al., 2021) übertrugen geringe Genauigkeit auf Optimiererzustände. Speicherzugriffsbewusste Kernel wie FlashAttention verringern den Datenverkehr im Speicher während des Trainings weiter (Dao et al., 2022).

### Wann einsetzen

- Wenn Modell- oder Batchgröße durch den GPU-Speicher begrenzt sind (Micikevicius et al., 2017).
- Wenn die Hardware schnelle Einheiten für halbe Genauigkeit hat, um das Training zu beschleunigen (Micikevicius et al., 2017).
- Wenn BF16 unterstützt wird, als einfachere Option, weil weder Loss Scaling noch geänderte Hyperparameter nötig sind (Kalamkar et al., 2019).

### Stärken und Grenzen

**Stärken**
- Halbiert den Speicherbedarf nahezu (Micikevicius et al., 2017).
- BF16 erreicht FP32-Ergebnisse ohne geänderte Hyperparameter (Kalamkar et al., 2019).
- 8-Bit-Optimiererzustände halten die 32-Bit-Leistung mit einem Bruchteil des Speichers (Dettmers et al., 2021).

**Einschränkungen**
- FP16 hat einen begrenzten Wertebereich und braucht Loss Scaling gegen Unterlauf (Micikevicius et al., 2017).
- Eine 32-Bit-Hauptkopie der Gewichte bleibt nötig (Micikevicius et al., 2017).
- Die Beschleunigung hängt von Hardwareunterstützung für halbe Genauigkeit ab (Micikevicius et al., 2017).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| FP32-Training | Durchgängig einfache Genauigkeit | Baseline, numerisch empfindliche Fälle |
| FP16-Mixed-Precision | Halbe Genauigkeit mit FP32-Hauptgewichten und Loss Scaling (Micikevicius et al., 2017) | GPUs mit FP16-Einheiten |
| BF16-Mixed-Precision | FP32-Wertebereich in 16 Bit, kein Loss Scaling nötig (Kalamkar et al., 2019) | Hardware mit BF16-Unterstützung |
| 8-Bit-Optimierer | Optimiererzustände blockweise auf 8 Bit quantisiert (Dettmers et al., 2021) | Sehr große Modelle mit speicherintensiven Optimierern |

### In der Praxis

Frameworks bieten automatische Mixed Precision, die Typumwandlung und Loss Scaling übernimmt, sodass sie sich mit wenig Code aktivieren lässt; Trainingskurven werden mit einem FP32-Lauf verglichen, um zu prüfen, ob die Genauigkeit erhalten bleibt (Micikevicius et al., 2017; [[keras-and-tensorflow|Keras und TensorFlow]]). Beim Fine-Tuning großer Sprachmodelle wird Mixed Precision mit Quantisierung und parametereffizienten Verfahren kombiniert ([[lora|LoRA]]).

### Merksatz

Mixed Precision trainiert mit 16-Bit-Zahlen und schützt die Genauigkeit durch FP32-Hauptgewichte und Loss Scaling, wodurch sich der Speicherbedarf nahezu halbiert.

### Quellen

- Micikevicius, P. et al. (2017). *Mixed Precision Training.* ICLR 2018. [arXiv:1710.03740](https://arxiv.org/abs/1710.03740)
- Kalamkar, D. et al. (2019). *A Study of BFLOAT16 for Deep Learning Training.* [arXiv:1905.12322](https://arxiv.org/abs/1905.12322)
- Dettmers, T. et al. (2021). *8-bit Optimizers via Block-wise Quantization.* ICLR 2022. [arXiv:2110.02861](https://arxiv.org/abs/2110.02861)
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
