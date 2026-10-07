---
title_en: LoRA (Low-Rank Adaptation)
title_de: LoRA (Low-Rank Adaptation)
entity_type: Method
sources:
- https://arxiv.org/abs/2106.09685
- https://arxiv.org/abs/2012.13255
- https://arxiv.org/abs/2305.14314
- https://arxiv.org/abs/2402.09353
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning method ([[llm-adaptation|LLM Adaptation]]) that freezes the pretrained weights and learns a low-rank update for selected weight matrices of a Transformer. For GPT-3 175B it reduced the number of trainable parameters by 10,000 times and the GPU memory requirement by three times compared with full fine-tuning, while performing on par or better and adding no inference latency (Hu et al., 2021).

### How it works

Fine-tuning a pretrained model changes its weights only within a low-dimensional subspace, so the change can be represented by the product of two small matrices. LoRA trains only these matrices, keeps the original weights frozen and merges the product into the weights for inference.

```text
1. Why low rank works
▼
2. Low-rank decomposition of the weight update
▼
3. Training with frozen weights
▼
4. Merging for inference and task switching
▼
5. QLoRA: 4-bit quantized base model
▼
6. DoRA: magnitude and direction
```

#### 1. Why low rank works

Aghajanyan et al. (2020) showed that fine-tuning has a low intrinsic dimension: optimising only 200 trainable parameters, randomly projected back into the full parameter space, reached 90% of full fine-tuning performance on the MRPC task with RoBERTa. They also found that pretraining implicitly lowers the intrinsic dimension and that larger models tend to have a lower intrinsic dimension after a fixed number of pretraining updates. This motivates representing the weight change during fine-tuning by a low-rank matrix.

#### 2. Low-rank decomposition of the weight update

For a pretrained weight matrix W of size d×k, LoRA represents the update as ΔW = BA, where B has size d×r, A has size r×k and the rank r is much smaller than d and k (Hu et al., 2021). The number of trainable parameters per matrix falls from d·k to r·(d+k); for d = k = 4096 and r = 8, for example, from about 16.8 million to about 65,500. The rank r is a hyperparameter ([[regularization-and-hyperparameters|Regularization and Hyperparameters]]).

#### 3. Training with frozen weights

During training, W stays frozen and only A and B receive gradients; the forward pass computes h = Wx + BAx (Hu et al., 2021). The matrices are typically added to the attention projections of each Transformer layer. Because the optimiser state is needed only for the small matrices, training uses less GPU memory and achieves higher training throughput than full fine-tuning (Hu et al., 2021).

#### 4. Merging for inference and task switching

After training, BA can be added to W, so the adapted model computes exactly as many operations as the base model and, unlike adapter layers, adds no inference latency (Hu et al., 2021). Different tasks can share one frozen base model and only swap their small A and B matrices, which saves storage compared with keeping a full fine-tuned copy per task.

#### 5. QLoRA

QLoRA backpropagates gradients through a frozen, 4-bit quantized pretrained model into LoRA adapters (Dettmers et al., 2023). It uses 4-bit NormalFloat (NF4), a data type that is information-theoretically optimal for normally distributed weights, double quantization, which also quantizes the quantization constants, and paged optimizers to manage memory spikes. This made it possible to fine-tune a 65B-parameter model on a single 48 GB GPU while preserving full 16-bit fine-tuning performance; the resulting Guanaco models reached 99.3% of ChatGPT's performance on the Vicuna benchmark (Dettmers et al., 2023).

#### 6. DoRA

DoRA (Weight-Decomposed Low-Rank Adaptation) decomposes each pretrained weight matrix into a magnitude and a direction component and fine-tunes both, using LoRA for the direction to keep the number of trainable parameters small (Liu et al., 2024). The aim is to come closer to the learning behaviour of full fine-tuning and to close the accuracy gap that remains between LoRA and full fine-tuning, without additional inference cost. DoRA consistently outperformed LoRA when fine-tuning LLaMA, LLaVA and VL-BART on tasks such as commonsense reasoning, visual instruction tuning and image or video-text understanding (Liu et al., 2024).

#### Origin and variants

LoRA was proposed by Hu et al. (2021), who evaluated it on RoBERTa, DeBERTa, GPT-2 and GPT-3 175B. The motivation from intrinsic dimensionality comes from Aghajanyan et al. (2020). QLoRA (Dettmers et al., 2023) applies LoRA to a 4-bit quantized base model, and DoRA (Liu et al., 2024) separates magnitude and direction of the weights.

### When to use it

- When full fine-tuning of a large model is too expensive in GPU memory or storage (Hu et al., 2021).
- When one base model serves many tasks, since each task only needs its own small pair of matrices (Hu et al., 2021).
- When a very large model has to be fine-tuned on a single GPU, in which case QLoRA combines LoRA with a 4-bit base model (Dettmers et al., 2023).
- When the adapted model must run as fast as the base model, since the update can be merged into the weights (Hu et al., 2021).

### Strengths and limitations

**Strengths**
- No additional inference latency, unlike adapter layers (Hu et al., 2021).
- Far fewer trainable parameters, lower GPU memory use and higher training throughput than full fine-tuning (Hu et al., 2021).
- Performance on par with or better than full fine-tuning on RoBERTa, DeBERTa, GPT-2 and GPT-3 (Hu et al., 2021).

**Limitations**
- An accuracy gap to full fine-tuning can remain, which DoRA aims to close (Liu et al., 2024).
- The rank r has to be chosen as a hyperparameter (Hu et al., 2021).
- The approach relies on the weight update being low-dimensional, as observed for fine-tuning pretrained language models (Aghajanyan et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Full fine-tuning | Updates all weights; one full model copy per task (Hu et al., 2021) | Settings with ample compute and storage |
| Adapter layers | Add extra layers to the network, which increases inference latency (Hu et al., 2021) | Modular adaptation when latency matters less |
| QLoRA | LoRA on a frozen 4-bit quantized base model (Dettmers et al., 2023) | Fine-tuning very large models on limited GPU memory |
| DoRA | Fine-tunes magnitude and direction separately, with LoRA for the direction (Liu et al., 2024) | Closing the accuracy gap to full fine-tuning without inference overhead |

### In practice

LoRA matrices are commonly added to the attention projections, and the rank r is chosen per task (Hu et al., 2021). Because adapters are small, many task-specific adapters can be stored and loaded on top of a single base model. Where GPU memory is the limiting factor, QLoRA is used, and adapted models are evaluated on the target task ([[llm-evaluation|LLM Evaluation]]).

### Key takeaway

LoRA fine-tunes a frozen model by learning a small low-rank update per weight matrix, which matches full fine-tuning on many tasks at a fraction of the trainable parameters and with no extra inference cost.

### Sources

- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models.* ICLR 2022. [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- Aghajanyan, A. et al. (2020). *Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning.* ACL 2021. [arXiv:2012.13255](https://arxiv.org/abs/2012.13255)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- Liu, S. et al. (2024). *DoRA: Weight-Decomposed Low-Rank Adaptation.* ICML 2024. [arXiv:2402.09353](https://arxiv.org/abs/2402.09353)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LoRA (Low-Rank Adaptation) ist eine parametereffiziente Fine-Tuning-Methode ([[llm-adaptation|LLM Adaptation]]), die die vortrainierten Gewichte einfriert und für ausgewählte Gewichtsmatrizen eines Transformers eine niedrigrangige Aktualisierung lernt. Bei GPT-3 175B verringerte sie die Anzahl der trainierbaren Parameter auf ein Zehntausendstel und den GPU-Speicherbedarf auf ein Drittel im Vergleich zum vollständigen Fine-Tuning, schnitt gleich gut oder besser ab und fügte keine Inferenzlatenz hinzu (Hu et al., 2021).

### Funktionsweise

Das Fine-Tuning eines vortrainierten Modells verändert seine Gewichte nur innerhalb eines niedrigdimensionalen Unterraums, sodass die Veränderung durch das Produkt von zwei kleinen Matrizen dargestellt werden kann. LoRA trainiert nur diese Matrizen, lässt die ursprünglichen Gewichte eingefroren und rechnet das Produkt für die Inferenz in die Gewichte ein.

```text
1. Warum ein niedriger Rang genügt
▼
2. Zerlegung der Gewichtsaktualisierung mit niedrigem Rang
▼
3. Training mit eingefrorenen Gewichten
▼
4. Zusammenführen für die Inferenz und Aufgabenwechsel
▼
5. QLoRA: 4-Bit quantisiertes Basismodell
▼
6. DoRA: Betrag und Richtung
```

#### 1. Warum ein niedriger Rang genügt

Aghajanyan et al. (2020) zeigten, dass das Fine-Tuning eine niedrige intrinsische Dimension hat: durch Optimierung von nur 200 trainierbaren Parametern, die zufällig in den vollständigen Parameterraum zurückprojiziert wurden, wurde auf der MRPC-Aufgabe mit RoBERTa 90 % der Leistung des vollständigen Fine-Tuning erreicht. Sie fanden auch heraus, dass das Vortraining die intrinsische Dimension implizit senkt und größere Modelle nach einer festen Anzahl von Vortrainingsschritten tendenziell eine niedrigere intrinsische Dimension haben. Dies motiviert, die Gewichtsänderung während des Fine-Tuning durch eine Matrix mit niedrigem Rang darzustellen.

#### 2. Zerlegung der Gewichtsaktualisierung mit niedrigem Rang

Für eine vortrainierte Gewichtsmatrix W der Größe d×k stellt LoRA die Aktualisierung als ΔW = BA dar, wobei B die Größe d×r hat, A die Größe r×k hat und der Rang r viel kleiner als d und k ist (Hu et al., 2021). Die Anzahl der trainierbaren Parameter pro Matrix sinkt von d·k auf r·(d+k); beispielsweise von etwa 16,8 Millionen auf etwa 65.500 bei d = k = 4096 und r = 8. Der Rang r ist ein Hyperparameter ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]).

#### 3. Training mit eingefrorenen Gewichten

Während des Trainings bleibt W eingefroren und nur A und B erhalten Gradienten; der Vorwärtsdurchlauf berechnet h = Wx + BAx (Hu et al., 2021). Die Matrizen werden typischerweise den Aufmerksamkeitsprojektionen jeder Transformer-Schicht hinzugefügt. Da der Optimiererzustand nur für die kleinen Matrizen benötigt wird, braucht das Training weniger GPU-Speicher und erreicht einen höheren Trainingsdurchsatz als das vollständige Fine-Tuning (Hu et al., 2021).

#### 4. Zusammenführung für die Inferenz und Aufgabenwechsel

Nach dem Training kann BA zu W addiert werden, sodass das angepasste Modell genauso viele Operationen berechnet wie das Basismodell und, im Gegensatz zu Adapter-Schichten, keine Inferenz-Latenz hinzufügt (Hu et al., 2021). Verschiedene Aufgaben können ein eingefrorenes Basismodell teilen und nur ihre kleinen A- und B-Matrizen austauschen, was im Vergleich dazu, eine vollständige feinabgestimmte Kopie pro Aufgabe zu speichern, Speicherplatz spart.

#### 5. QLoRA

QLoRA propagiert Gradienten durch ein eingefrorenes, auf 4 Bit quantisiertes vortrainiertes Modell in LoRA-Adapter (Dettmers et al., 2023). Es verwendet 4-Bit NormalFloat (NF4), einen Datentyp, der informationstheoretisch optimal für normalverteilte Gewichte ist, eine Doppelquantisierung, die auch die Quantisierungs-Konstanten quantisiert, und Paged Optimizers, um Speicherspitzen abzufangen. Damit ließ sich ein Modell mit 65 Milliarden Parametern auf einer einzelnen 48-GB-GPU feinabstimmen, während die volle 16-Bit-Feinabstimmungsleistung bewahrt blieb; die entstandenen Guanaco-Modelle erreichten auf dem Vicuna-Benchmark 99,3 % der Leistung von ChatGPT (Dettmers et al., 2023).

#### 6. DoRA

DoRA (Weight-Decomposed Low-Rank Adaptation) zerlegt jede vortrainierte Gewichtsmatrix in eine Betrags- und eine Richtungskomponente und stimmt beide fein ab, wobei LoRA für die Richtung verwendet wird, um die Anzahl der trainierbaren Parameter klein zu halten (Liu et al., 2024). Das Ziel besteht darin, dem Lernverhalten einer vollständigen Feinabstimmung näher zu kommen und den Genauigkeitsabstand zwischen LoRA und vollständigem Fine-Tuning zu verringern, ohne zusätzliche Inferenzkosten. DoRA übertraf LoRA konsistent bei der Feinabstimmung von LLaMA, LLaVA und VL-BART bei Aufgaben wie Commonsense Reasoning, Visual Instruction Tuning und Bild- oder Video-Text-Verstehen (Liu et al., 2024).

#### Ursprung und Varianten

LoRA wurde von Hu et al. (2021) vorgeschlagen, die es an RoBERTa, DeBERTa, GPT-2 und GPT-3 175B bewerteten. Die Motivation über die intrinsische Dimension stammt von Aghajanyan et al. (2020). QLoRA (Dettmers et al., 2023) wendet LoRA auf ein auf 4 Bit quantisiertes Basismodell an, und DoRA (Liu et al., 2024) trennt Betrag und Richtung der Gewichte.

### Wann einsetzen

- Wenn vollständiges Fine-Tuning eines großen Modells wegen GPU-Speicher oder Speicherplatz zu teuer ist (Hu et al., 2021).
- Wenn ein Basismodell viele Aufgaben bedienen soll, da jede Aufgabe nur ihre eigenen kleinen Matrizen benötigt (Hu et al., 2021).
- Wenn ein sehr großes Modell auf einer einzelnen GPU feinabgestimmt werden muss, wofür QLoRA LoRA mit einem 4-Bit-Basismodell kombiniert (Dettmers et al., 2023).
- Wenn das angepasste Modell so schnell laufen muss wie das Basismodell, da die Aktualisierung in die Gewichte eingerechnet werden kann (Hu et al., 2021).

### Stärken und Grenzen

**Stärken**
- Keine zusätzliche Inferenzverzögerung, im Gegensatz zu Adapter-Schichten (Hu et al., 2021).
- Viel weniger trainierbare Parameter, geringerer GPU-Speicherbedarf und höherer Trainingsdurchsatz als beim vollständigen Fine-Tuning (Hu et al., 2021).
- Gleiche oder bessere Leistung als vollständiges Fine-Tuning bei RoBERTa, DeBERTa, GPT-2 und GPT-3 (Hu et al., 2021).

**Einschränkungen**
- Ein Genauigkeitsabstand zum vollständigen Fine-Tuning kann bestehen bleiben, den DoRA schließen soll (Liu et al., 2024).
- Der Rang r muss als Hyperparameter gewählt werden (Hu et al., 2021).
- Der Ansatz basiert darauf, dass die Gewichtsaktualisierung niedrigdimensional ist, wie es beim Fine-Tuning vortrainierter Sprachmodelle beobachtet wurde (Aghajanyan et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Vollständiges Fine-Tuning | Aktualisiert alle Gewichte; eine vollständige Modellkopie pro Aufgabe (Hu et al., 2021) | Umgebungen mit ausreichender Rechenleistung und Speicher |
| Adapter-Schichten | Zusätzliche Schichten werden zur Netzwerkarchitektur hinzugefügt, was die Inferenzlatenz erhöht (Hu et al., 2021) | Modulare Anpassung, wenn Latenz weniger wichtig ist |
| QLoRA | LoRA auf einem eingefrorenen, auf 4 Bit quantisierten Basismodell (Dettmers et al., 2023) | Fine-Tuning sehr großer Modelle mit begrenztem GPU-Speicher |
| DoRA | Betrag und Richtung werden getrennt feinabgestimmt, wobei LoRA für die Richtung verwendet wird (Liu et al., 2024) | Schließung der Genauigkeitslücke zum vollständigen Fine-Tuning ohne Inferenz-Overhead |

### In der Praxis

LoRA-Matrizen werden häufig den Aufmerksamkeitsprojektionen hinzugefügt, und der Rang r wird pro Aufgabe gewählt (Hu et al., 2021). Da Adapter klein sind, können viele aufgabenspezifische Adapter für ein einzelnes Basismodell gespeichert und geladen werden. Wo der GPU-Speicher der limitierende Faktor ist, wird QLoRA verwendet, und angepasste Modelle werden auf der Zielaufgabe bewertet ([[llm-evaluation|LLM Evaluation]]).

### Merksatz

LoRA stimmt ein eingefrorenes Modell fein, indem es pro Gewichtsmatrix eine kleine Aktualisierung mit niedrigem Rang lernt, und erreicht bei vielen Aufgaben die Qualität vollständigen Fine-Tunings mit einem Bruchteil der trainierbaren Parameter und ohne zusätzliche Inferenzkosten.

### Quellen

- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models.* ICLR 2022. [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- Aghajanyan, A. et al. (2020). *Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning.* ACL 2021. [arXiv:2012.13255](https://arxiv.org/abs/2012.13255)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- Liu, S. et al. (2024). *DoRA: Weight-Decomposed Low-Rank Adaptation.* ICML 2024. [arXiv:2402.09353](https://arxiv.org/abs/2402.09353)
