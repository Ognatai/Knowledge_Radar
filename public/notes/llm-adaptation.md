---
title_en: LLM Adaptation
title_de: LLM-Anpassung
entity_type: Concept
sources:
- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2109.01652
- https://arxiv.org/abs/2106.09685
- https://arxiv.org/abs/2305.14314
- https://arxiv.org/abs/1503.02531
- https://arxiv.org/abs/1710.03740
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LLM adaptation covers the ways a pretrained language model is made to perform a specific task or use specific knowledge. The options range from leaving the weights unchanged (prompting, [[retrieval-augmented-generation|Retrieval-Augmented Generation]]) through updating all weights (fine-tuning, instruction tuning) or only a few (LoRA, QLoRA), to transferring knowledge into a smaller model (distillation). Mixed precision and quantization reduce the memory and compute these methods need.

### How it works

The methods differ in what they change: the input, all parameters, a small number of added parameters, or the model itself. The less a method changes, the cheaper and more flexible it is; the more it changes, the more the model's behaviour can be specialised.

```text
1. No weight changes: prompting, retrieval augmentation
▼
2. All weights: full fine-tuning, instruction tuning
▼
3. Few added weights: LoRA
▼
4. LoRA on a quantized base model: QLoRA
▼
5. Smaller model: knowledge distillation
▼
6. Lower precision: mixed precision training, quantization
```

#### 1. Adaptation without changing weights

Prompting steers a model through instructions or examples in the input and relies on what the model already knows ([[prompt-engineering|Prompt Engineering]]). Retrieval-augmented generation combines the parametric memory of a pretrained sequence-to-sequence model with a non-parametric memory, a dense vector index of Wikipedia accessed by a neural retriever; the model conditions either on the same retrieved passages for the whole output or on different passages per token (Lewis et al., 2020). Because knowledge sits in the index, it can be updated without retraining, and RAG models set the state of the art on three open-domain question answering tasks (Lewis et al., 2020).

#### 2. Full fine-tuning and instruction tuning

Full fine-tuning updates all parameters on task-specific data, so every task needs its own copy of the full model. Instruction tuning fine-tunes a model on a collection of tasks phrased as natural-language instructions so that it generalises to unseen tasks (Wei et al., 2021). Instruction tuning a 137B-parameter model on more than 60 NLP tasks (FLAN) substantially improved its zero-shot performance over the unmodified model, surpassed zero-shot 175B GPT-3 on 20 of 25 evaluated data sets and outperformed few-shot GPT-3 by a large margin on data sets such as ANLI, RTE, BoolQ and OpenbookQA (Wei et al., 2021).

#### 3. Parameter-efficient fine-tuning with LoRA

LoRA freezes the pretrained weights and injects trainable rank-decomposition matrices into each layer of the Transformer ([[lora|LoRA]]). For a frozen weight matrix W of size d×k, the update is the product BA of a d×r matrix B and an r×k matrix A, with a rank r much smaller than d and k (Hu et al., 2021). Compared with fine-tuning GPT-3 175B with Adam, LoRA reduced the number of trainable parameters by 10,000 times and the GPU memory requirement by three times, performed on par with or better than fine-tuning on RoBERTa, DeBERTa, GPT-2 and GPT-3, and adds no inference latency because the update can be merged into the weights (Hu et al., 2021).

#### 4. QLoRA

QLoRA backpropagates gradients through a frozen, 4-bit quantized pretrained model into LoRA adapters (Dettmers et al., 2023). It introduces 4-bit NormalFloat (NF4), a data type that is information-theoretically optimal for normally distributed weights, double quantization, which also quantizes the quantization constants, and paged optimizers to handle memory spikes. This reduces memory enough to fine-tune a 65B-parameter model on a single 48 GB GPU while preserving full 16-bit fine-tuning performance; the resulting Guanaco models reached 99.3% of ChatGPT's performance on the Vicuna benchmark after 24 hours of fine-tuning on one GPU (Dettmers et al., 2023).

#### 5. Knowledge distillation

Knowledge distillation compresses the knowledge of a large model or an ensemble of models into a single smaller model by training it on the soft output probabilities of the large one ([[knowledge-distillation|Knowledge Distillation]]). Hinton et al. (2015) reported surprising results on MNIST and showed that distilling an ensemble into a single model significantly improved the acoustic model of a heavily used commercial speech recognition system, making deployment cheaper than running the full ensemble.

#### 6. Mixed precision and quantization

Mixed precision training stores weights, activations and gradients in half-precision floating point, keeps a single-precision master copy of the weights that accumulates the updates, and scales the loss so that small gradient values do not underflow; this nearly halves the memory requirements without losing model accuracy (Micikevicius et al., 2017). Quantization stores weights in even fewer bits ([[quantization|Quantization]]), as in QLoRA's 4-bit base model, which is what makes fine-tuning very large models on a single GPU possible (Dettmers et al., 2023).

#### Origin and variants

Knowledge distillation (Hinton et al., 2015) and mixed precision training (Micikevicius et al., 2017) predate large language models. Retrieval augmentation (Lewis et al., 2020), instruction tuning (Wei et al., 2021) and LoRA (Hu et al., 2021) were proposed for pretrained Transformers; QLoRA (Dettmers et al., 2023) combined LoRA with 4-bit quantization of the base model.

### When to use it

- When a model needs knowledge that changes or is not in its training data, retrieval augmentation lets the knowledge be updated in the index instead of the weights (Lewis et al., 2020).
- When a model should follow instructions for tasks it was not trained on, instruction tuning improves zero-shot performance (Wei et al., 2021).
- When full fine-tuning is too expensive in memory or storage, LoRA or, on limited hardware, QLoRA adapt the model with few trainable parameters (Hu et al., 2021; Dettmers et al., 2023).
- When a model has to be cheaper to run, distillation transfers its knowledge into a smaller model (Hinton et al., 2015).

### Strengths and limitations

**Strengths**
- Retrieval augmentation set the state of the art on three open-domain question answering tasks and allows knowledge updates without retraining (Lewis et al., 2020).
- LoRA reduces trainable parameters by 10,000 times and GPU memory by three times compared with full fine-tuning of GPT-3 175B, without additional inference latency (Hu et al., 2021).
- QLoRA makes it possible to fine-tune a 65B-parameter model on a single 48 GB GPU while preserving 16-bit fine-tuning performance (Dettmers et al., 2023).

**Limitations**
- Full fine-tuning requires a complete copy of the model for every task (Hu et al., 2021).
- Distillation first needs a large trained teacher model or ensemble (Hinton et al., 2015).
- Dettmers et al. (2023) found current chatbot benchmarks not trustworthy for evaluating chatbot performance and showed failure cases of their models compared with ChatGPT, so adapted models need careful evaluation ([[llm-evaluation|LLM Evaluation]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Retrieval augmentation | No weight changes; retrieved passages are added to the input (Lewis et al., 2020) | Knowledge-intensive tasks and knowledge that changes |
| Instruction tuning | All weights updated on many tasks phrased as instructions (Wei et al., 2021) | Better zero-shot behaviour on unseen tasks |
| LoRA / QLoRA | Frozen base model plus small trainable low-rank matrices; QLoRA with a 4-bit base model (Hu et al., 2021; Dettmers et al., 2023) | Task adaptation with limited memory and many tasks per base model |
| Knowledge distillation | A smaller student model learns from a larger teacher's outputs (Hinton et al., 2015) | Cheaper deployment of a model's capabilities |

### In practice

Adaptation methods are usually combined: a LoRA or QLoRA adapter can be trained on top of a base model, and the adapted model can still be used with retrieval augmentation. For LoRA, the rank r of the update matrices is the central hyperparameter, since it determines the number of trainable parameters (Hu et al., 2021). Because benchmark results for adapted chat models can be misleading, they are evaluated on the target task as well (Dettmers et al., 2023).

### Key takeaway

Adapting an LLM means choosing how much of it to change: the input, a few added parameters, all weights or the model size, trading cost against how strongly the behaviour can be specialised.

### Sources

- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Wei, J. et al. (2021). *Finetuned Language Models Are Zero-Shot Learners.* ICLR 2022. [arXiv:2109.01652](https://arxiv.org/abs/2109.01652)
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models.* ICLR 2022. [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- Hinton, G. et al. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Micikevicius, P. et al. (2017). *Mixed Precision Training.* ICLR 2018. [arXiv:1710.03740](https://arxiv.org/abs/1710.03740)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LLM-Anpassung umfasst die Verfahren, mit denen ein vortrainiertes Sprachmodell so angepasst wird, dass es eine bestimmte Aufgabe ausführt oder spezifisches Wissen nutzt. Die Optionen reichen von unveränderten Gewichten (Prompting, [[retrieval-augmented-generation|Retrieval-Augmented Generation]]) über das Aktualisieren aller Gewichte (Fine-Tuning, Instruction Tuning) oder nur einiger weniger (LoRA, QLoRA) bis hin zum Übertragen von Wissen in ein kleineres Modell (Distillation). Mixed Precision und Quantisierung verringern den Speicher- und Rechenbedarf dieser Methoden.

### Funktionsweise

Die Methoden unterscheiden sich darin, was sie verändern: die Eingabe, alle Parameter, eine kleine Anzahl an hinzugefügten Parametern oder das Modell selbst. Je weniger eine Methode verändert, desto günstiger und flexibler ist sie; je mehr sie verändert, desto spezialisierter kann das Verhalten des Modells werden.

```text
1. Keine Gewichtsänderungen: Prompting, Retrieval-Augmentation
▼
2. Alle Gewichte: vollständiges Fine-Tuning, Instruction Tuning
▼
3. Wenige hinzugefügte Gewichte: LoRA
▼
4. LoRA auf einem quantisierten Basismodell: QLoRA
▼
5. Kleineres Modell: Knowledge Distillation
▼
6. Geringere Präzision: Mixed-Precision-Training, Quantisierung
```

#### 1. Anpassung ohne Gewichtsänderung

Prompting leitet ein Modell durch Anweisungen oder Beispiele in der Eingabe und nutzt, was das Modell bereits weiß ([[prompt-engineering|Prompt Engineering]]). Retrieval-augmented generation kombiniert den parametrischen Speicher eines vortrainierten Sequence-to-Sequence-Modells mit einem nicht-parametrischen Speicher, einem dichten Vektorindex von Wikipedia, der durch einen neuronalen Retriever abgerufen wird; das Modell konditioniert entweder auf dieselben abgerufenen Passagen für die gesamte Ausgabe oder auf unterschiedliche Passagen pro Token (Lewis et al., 2020). Da das Wissen im Index liegt, kann es ohne Neutraining aktualisiert werden, und RAG-Modelle erreichten den Stand der Technik bei drei Aufgaben des Open-Domain-Question-Answering (Lewis et al., 2020).

#### 2. Vollständiges Fine-Tuning und Instruction Tuning

Vollständiges Fine-Tuning aktualisiert alle Parameter anhand aufgabenspezifischer Daten, sodass jede Aufgabe ihre eigene Kopie des vollständigen Modells benötigt. Instruction Tuning stimmt ein Modell anhand einer Sammlung von Aufgaben fein, die als natürlichsprachliche Anweisungen formuliert sind, sodass es sich auf unbekannte Aufgaben verallgemeinern kann (Wei et al., 2021). Instruction Tuning eines Modells mit 137 Milliarden Parametern auf mehr als 60 NLP-Aufgaben (FLAN) verbesserte seine Zero-Shot-Leistung erheblich im Vergleich zum unveränderten Modell, übertraf die Zero-Shot-Leistung von GPT-3 mit 175 Milliarden Parametern bei 20 von 25 bewerteten Datensätzen und erzielte bei Datensätzen wie ANLI, RTE, BoolQ und OpenbookQA deutlich bessere Ergebnisse als das Few-Shot-GPT-3 (Wei et al., 2021).

#### 3. Parameter-effizientes Fine-Tuning mit LoRA

LoRA friert die vortrainierten Gewichte ein und injiziert in jede Schicht des Transformers trainierbare Rang-Zerlegungsmatrizen ([[lora|LoRA]]). Für eine gefrorene Gewichtsmatrix W der Größe d×k ist die Aktualisierung das Produkt BA einer d×r-Matrix B und einer r×k-Matrix A, wobei der Rang r deutlich kleiner als d und k ist (Hu et al., 2021). Im Vergleich zum Fine-Tuning von GPT-3 175B mit Adam verringerte LoRA die Anzahl der trainierbaren Parameter auf ein Zehntausendstel und den GPU-Speicherbedarf auf ein Drittel, erzielte gleich gute oder bessere Ergebnisse als das Fine-Tuning bei RoBERTa, DeBERTa, GPT-2 und GPT-3 waren, und fügt keine Inferenzverzögerung hinzu, da die Aktualisierung in die Gewichte eingerechnet werden kann (Hu et al., 2021).

#### 4. QLoRA

QLoRA propagiert Gradienten durch ein gefrorenes, 4-Bit-quantisiertes vortrainiertes Modell in LoRA-Adapter (Dettmers et al., 2023). Es führt 4-Bit NormalFloat (NF4) ein, einen Datentyp, der informationstheoretisch optimal für normalverteilte Gewichte ist, eine Doppelquantisierung, die auch die Quantisierungs-Konstanten quantisiert, und Paged Optimizers, um Speicherspitzen abzufangen. Dies reduziert den Speicherbedarf genug, um ein Modell mit 65 B Parametern auf einer einzigen 48-GB-GPU feinabzustimmen, während die volle 16-Bit-Feinabstimmungsleistung erhalten bleibt; die entstandenen Guanaco-Modelle erreichten nach 24 Stunden Feinabstimmung auf einer GPU 99,3 % der Leistung von ChatGPT auf dem Vicuna-Benchmark (Dettmers et al., 2023).

#### 5. Knowledge Distillation

Knowledge Distillation komprimiert das Wissen eines großen Modells oder einer Gruppe von Modellen in ein einzelnes kleineres Modell, indem es auf den weichen Ausgabewahrscheinlichkeiten des großen Modells trainiert wird ([[knowledge-distillation|Knowledge Distillation]]). Hinton et al. (2015) berichteten über überraschende Ergebnisse auf MNIST und zeigten, dass die Destillation eines Ensembles in ein einzelnes Modell das akustische Modell eines stark genutzten kommerziellen Spracherkennungssystems deutlich verbesserte und die Bereitstellung billiger als das Ausführen des vollständigen Ensembles war.

#### 6. Mixed Precision und Quantisierung

Mixed-Precision-Training speichert Gewichte, Aktivierungen und Gradienten als Gleitkommazahlen in halber Genauigkeit, behält eine Masterkopie der Gewichte in einfacher Genauigkeit, die die Updates sammelt, und skaliert den Verlust, damit kleine Gradientenwerte nicht unterlaufen; dies reduziert die Speicheranforderungen fast um die Hälfte, ohne die Modellgenauigkeit zu verlieren (Micikevicius et al., 2017). Quantisierung speichert Gewichte in noch weniger Bits ([[quantization|Quantisierung]]), wie beim 4-Bit-Basismodell von QLoRA, was das Fine-Tuning sehr großer Modelle auf einer einzigen GPU ermöglicht (Dettmers et al., 2023).

#### Ursprung und Varianten

Knowledge distillation (Hinton et al., 2015) und mixed precision training (Micikevicius et al., 2017) sind älter als große Sprachmodelle. Retrieval augmentation (Lewis et al., 2020), instruction tuning (Wei et al., 2021) und LoRA (Hu et al., 2021) wurden für vortrainierte Transformers vorgeschlagen; QLoRA (Dettmers et al., 2023) kombinierte LoRA mit 4-Bit-Quantisierung des Basismodells.

### Wann einsetzen

- Wenn ein Modell Wissen benötigt, das sich ändert oder nicht in seinen Trainingsdaten enthalten ist, ermöglicht Retrieval-Augmentation, dass das Wissen im Index anstelle der Gewichte aktualisiert wird (Lewis et al., 2020).
- Wenn ein Modell Anweisungen für Aufgaben folgen soll, für die es nicht trainiert wurde, verbessert Instruction Tuning die Leistung bei Zero-Shot-Aufgaben (Wei et al., 2021).
- Wenn vollständiges Fine-Tuning zu viel Arbeits- oder Datenspeicher erfordert, adaptieren LoRA oder, bei begrenzter Hardware, QLoRA das Modell mit nur wenigen trainierbaren Parametern (Hu et al., 2021; Dettmers et al., 2023).
- Wenn ein Modell günstiger laufen soll, überträgt Distillation sein Wissen in ein kleineres Modell (Hinton et al., 2015).

### Stärken und Grenzen

**Stärken**
- Retrieval-Augmentation erreichte den Stand der Technik bei drei Aufgaben des Open-Domain-Question-Answering und ermöglicht Wissensupdates ohne Neutraining (Lewis et al., 2020).
- LoRA verringert die trainierbaren Parameter auf ein Zehntausendstel und den GPU-Speicherbedarf auf ein Drittel im Vergleich zur vollständigen Feinabstimmung von GPT-3 175B, ohne zusätzliche Inferenzlatenz (Hu et al., 2021).
- QLoRA ermöglicht die Feinabstimmung eines 65B-Parameter-Modells auf einer einzelnen 48-GB-GPU, während die 16-Bit-Feinabstimmungsleistung beibehalten wird (Dettmers et al., 2023).

**Einschränkungen**
- Die vollständige Feinabstimmung erfordert eine vollständige Kopie des Modells für jede Aufgabe (Hu et al., 2021).
- Distillation benötigt zunächst ein großes, bereits trainiertes Lehrermodell oder ein Ensemble (Hinton et al., 2015).
- Dettmers et al. (2023) fanden die aktuellen Chatbot-Benchmarks nicht vertrauenswürdig, um die Leistung von Chatbots zu bewerten und zeigten Fehlerfälle ihrer Modelle im Vergleich zu ChatGPT, daher benötigen angepasste Modelle eine sorgfältige Bewertung ([[llm-evaluation|LLM Evaluation]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Retrieval-Augmentation | Keine Gewichtsänderungen; abgerufene Passagen werden der Eingabe hinzugefügt (Lewis et al., 2020) | Wissensintensive Aufgaben und Wissen, das sich verändert |
| Instruction Tuning | Alle Gewichte werden auf vielen Aufgaben aktualisiert, die als Anweisungen formuliert sind (Wei et al., 2021) | Besseres Zero-Shot-Verhalten bei unbekannten Aufgaben |
| LoRA / QLoRA | Eingefrorenes Basismodell plus kleine trainierbare Matrizen niedrigen Rangs; QLoRA mit einem 4-Bit Basismodell (Hu et al., 2021; Dettmers et al., 2023) | Anpassung an Aufgaben mit begrenztem Speicher und vielen Aufgaben pro Basismodell |
| Knowledge Distillation | Ein kleineres Schülermodell lernt aus den Ausgaben eines größeren Lehrermodells (Hinton et al., 2015) | Günstigere Bereitstellung der Fähigkeiten eines Modells |

### In der Praxis

Anpassungsmethoden werden in der Regel kombiniert: ein LoRA- oder QLoRA-Adapter kann auf einem Basismodell trainiert werden, und das angepasste Modell lässt sich weiterhin mit Retrieval-Augmentation nutzen. Bei LoRA ist der Rang r der Update-Matrizen der zentrale Hyperparameter, da er die Anzahl der trainierbaren Parameter bestimmt (Hu et al., 2021). Da Benchmark-Ergebnisse für angepasste Chat-Modelle irreführend sein können, werden sie zusätzlich auf der Zielaufgabe bewertet (Dettmers et al., 2023).

### Merksatz

Das Anpassen eines LLM bedeutet, zu entscheiden, wie viel davon geändert werden soll: die Eingabe, einige hinzugefügte Parameter, alle Gewichte oder die Modellgröße, wobei Kosten gegen die Stärke der Spezialisierung des Verhaltens abgewogen werden.

### Quellen

- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Wei, J. et al. (2021). *Finetuned Language Models Are Zero-Shot Learners.* ICLR 2022. [arXiv:2109.01652](https://arxiv.org/abs/2109.01652)
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models.* ICLR 2022. [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- Dettmers, T. et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs.* NeurIPS 2023. [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- Hinton, G. et al. (2015). *Distilling the Knowledge in a Neural Network.* [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Micikevicius, P. et al. (2017). *Mixed Precision Training.* ICLR 2018. [arXiv:1710.03740](https://arxiv.org/abs/1710.03740)
