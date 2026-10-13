---
title_en: Model Compression
title_de: Model Compression
entity_type: Concept
aliases:
- Network compression
sources:
- https://doi.org/10.1145/1150402.1150464
- https://arxiv.org/abs/1710.09282
- https://doi.org/10.1109/jproc.2020.2976475
- https://arxiv.org/abs/2610.07032
- https://arxiv.org/abs/2610.11115
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
Model compression makes trained [[neural-networks|neural networks]] smaller and faster so that they can run on devices with little memory or under strict latency requirements, ideally without a significant loss of accuracy (Cheng et al., 2017). The main families are parameter pruning and quantisation, low-rank factorisation, compact convolutional filters and knowledge distillation (Cheng et al., 2017); the idea goes back to compressing large ensembles of classifiers into one small, fast model (Buciluǎ et al., 2006).

### How it works

Deep networks owe much of their accuracy to millions or billions of parameters, which makes them expensive in computation and memory (Cheng et al., 2017). Loading the weights of LLaMA-2 70B in 16-bit precision, for example, takes about 140 GB, nearly six times the memory of a consumer GPU (Gao et al., 2026). Compression methods exploit the fact that many of these parameters are redundant; they differ in what they remove or replace.

```text
trained model ─▶ prune redundant weights ─▶ quantize remaining weights ─▶ encode ─▶ compressed model
                 (or: factorise layers, or: train a small student on the large model's outputs)
```

#### 1. Pruning
Pruning removes weights, neurons or whole structures that contribute little. Early methods such as Optimal Brain Damage and Optimal Brain Surgeon chose connections to remove based on the Hessian of the loss function and achieved higher accuracy than pruning by weight magnitude. Later work prunes redundant weights in pre-trained networks, or adds sparsity constraints (l0 or l1 regularisers) during training; group sparsity removes entire filters, channels or layers, which yields structured instead of scattered sparsity (Cheng et al., 2017).

#### 2. Quantisation and binarisation
[[quantisation|Quantisation]] reduces the number of bits used to represent each weight; 8-bit quantisation of the parameters already brings a significant speed-up with minimal loss of accuracy (Cheng et al., 2017). The "deep compression" pipeline combines three stages: it prunes small-weight connections, quantises the remaining weights by weight sharing and then encodes them with Huffman coding. In the extreme case, binary networks use one bit per weight, but their accuracy drops considerably for large networks (Cheng et al., 2017).

#### 3. Low-rank factorisation and structured matrices
Weight matrices of fully connected layers and convolution kernels, viewed as tensors, can be approximated by products of smaller matrices or tensors. Reported results include a 2× speed-up of a single convolutional layer with a 1% drop in accuracy and a 4.5× speed-up with a 1% drop in text recognition. Structured matrices go further by restricting a layer's weight matrix to a form that needs fewer parameters: a circulant matrix stores a d × d layer in O(d) instead of O(d²) memory and, via the fast Fourier transform, computes it in O(d log d) time (Cheng et al., 2017).

#### 4. Knowledge distillation
Instead of shrinking the network itself, [[knowledge-distillation|knowledge distillation]] trains a separate small model to reproduce a large one. Buciluǎ et al. (2006) compressed ensembles of hundreds or thousands of classifiers this way: they labelled pseudo-data with the ensemble and trained a smaller, faster model on it, usually without significant loss in performance. Later work transfers the large model's softened output distribution to a small student network and extends this to thin but deep students that also learn from intermediate representations (Cheng et al., 2017).

#### Origin and variants
Buciluǎ et al. (2006) introduced the term for compressing large ensembles. Surveys by Cheng et al. (2017) and Deng et al. (2020) organise the methods for deep networks; Deng et al. (2020) also cover how compression shapes the design of hardware accelerators for neural networks. Methods are increasingly combined: Zafar et al. (2026) distil and quantise a translation model together. New paradigms continue to appear, such as dynamic-system-based compression, which stores high-dimensional weights as the index of a trajectory of a dynamic system and recovers them during decompression, a mechanism distinct from pruning, quantisation, distillation and low-rank decomposition (Gao et al., 2026).

### When to use it
- Deployment on devices with little memory, such as smartphones, wearables and embedded systems, or in applications with strict latency requirements (Cheng et al., 2017; Deng et al., 2020; Gao et al., 2026).
- Serving a model more cheaply and with lower energy use and emissions (Zafar et al., 2026); see also [[llm-cost-optimisation|LLM cost optimisation]].
- Replacing a large ensemble or teacher model with a single small model at inference time (Buciluǎ et al., 2006).

### Strengths and limitations
Strengths:
- Pruning and quantisation are robust across settings and work both when training from scratch and on pre-trained models (Cheng et al., 2017).
- Low-rank factorisation follows a standardised pipeline that is easy to implement (Cheng et al., 2017).
- Combined methods can shrink a model substantially with little or no loss in quality (Zafar et al., 2026).

Limitations:
- Pruning with l1 or l2 regularisation needs more iterations to converge, pruning criteria require manual per-layer settings, and pruning often reduces model size without speeding up training or inference (Cheng et al., 2017).
- Binary networks lose considerable accuracy on large models, and structural constraints on weight matrices can bias the model, with no theoretical way to choose the right structure (Cheng et al., 2017).
- Quantisation degrades performance as bit precision decreases, and distillation is limited when domain-specific training data is scarce (Zafar et al., 2026).

### Comparison
| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Pruning and [[quantisation\|quantisation]] | Remove redundant parameters or store them with fewer bits (Cheng et al., 2017) | Pre-trained models as well as training from scratch |
| Low-rank factorisation | Approximate weight matrices and kernels by smaller factors (Cheng et al., 2017) | Convolutional and fully connected layers |
| Compact convolutional filters | Use special filter structures with fewer parameters; depends on the application (Cheng et al., 2017) | New convolutional architectures trained from scratch |
| [[knowledge-distillation\|Knowledge distillation]] | Train a small model to reproduce a large one; results depend on the application and network structure (Cheng et al., 2017) | Replacing large models or ensembles by small ones |

### In practice
Compression methods are compared by compression rate and speed-up together with the change in accuracy (Cheng et al., 2017). Combining methods can pay off: for French-to-English biomedical translation, a student model that was distilled and quantised together was 69% smaller and ran 98.21% faster than its teacher, with 98.46% lower CO2 emissions and little or no loss of translation quality (Zafar et al., 2026).

### Key takeaway
Most trained networks contain many redundant parameters; pruning, quantisation, factorisation and distillation remove or replace them so that a model fits the memory, latency and cost budget of its deployment.

### Sources
- Buciluǎ, C., Caruana, R. & Niculescu-Mizil, A. (2006). *Model compression.* KDD 2006. [DOI](https://doi.org/10.1145/1150402.1150464)
- Cheng, Y. et al. (2017). *A Survey of Model Compression and Acceleration for Deep Neural Networks.* [arXiv:1710.09282](https://arxiv.org/abs/1710.09282)
- Deng, L. et al. (2020). *Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey.* Proceedings of the IEEE. [DOI](https://doi.org/10.1109/jproc.2020.2976475)
- Zafar, M. et al. (2026). *Investigating Model Compression for Neural Machine Translation in the Biomedical Domain.* [arXiv:2610.07032](https://arxiv.org/abs/2610.07032)
- Gao, F. et al. (2026). *Dynamics as Code: On Model Compression via Dynamic System.* [arXiv:2610.11115](https://arxiv.org/abs/2610.11115)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Model Compression macht trainierte [[neural-networks|neuronale Netze]] kleiner und schneller, damit sie auf Geräten mit wenig Speicher oder unter strengen Latenzanforderungen laufen können, idealerweise ohne nennenswerten Genauigkeitsverlust (Cheng et al., 2017). Die wichtigsten Verfahrensfamilien sind Pruning und Quantisierung, Low-Rank-Faktorisierung, kompakte Faltungsfilter und Knowledge Distillation (Cheng et al., 2017); die Idee geht darauf zurück, große Ensembles von Klassifikatoren zu einem kleinen, schnellen Modell zu verdichten (Buciluǎ et al., 2006).

### Funktionsweise

Tiefe Netze verdanken ihre Genauigkeit zu einem großen Teil Millionen oder Milliarden von Parametern, was sie rechen- und speicherintensiv macht (Cheng et al., 2017). Die Gewichte von LLaMA-2 70B in 16-Bit-Genauigkeit zu laden, braucht zum Beispiel etwa 140 GB, fast das Sechsfache des Speichers einer Consumer-GPU (Gao et al., 2026). Kompressionsverfahren nutzen aus, dass viele dieser Parameter redundant sind; sie unterscheiden sich darin, was sie entfernen oder ersetzen.

```text
trainiertes Modell ─▶ redundante Gewichte prunen ─▶ verbleibende Gewichte quantisieren ─▶ kodieren ─▶ komprimiertes Modell
                      (oder: Schichten faktorisieren, oder: kleines Student-Modell auf die Ausgaben des großen trainieren)
```

#### 1. Pruning
Pruning entfernt Gewichte, Neuronen oder ganze Strukturen, die wenig beitragen. Frühe Verfahren wie Optimal Brain Damage und Optimal Brain Surgeon wählten die zu entfernenden Verbindungen anhand der Hesse-Matrix der Verlustfunktion und erreichten damit eine höhere Genauigkeit als Pruning nach Gewichtsbetrag. Spätere Arbeiten prunen redundante Gewichte in vortrainierten Netzen oder fügen beim Training Sparsity-Nebenbedingungen hinzu (l0- oder l1-Regularisierer); Group Sparsity entfernt ganze Filter, Kanäle oder Schichten und erzeugt so strukturierte statt verstreuter Sparsity (Cheng et al., 2017).

#### 2. Quantisierung und Binarisierung
[[quantisation|Quantisierung]] verringert die Zahl der Bits, mit denen jedes Gewicht dargestellt wird; schon eine 8-Bit-Quantisierung der Parameter bringt eine deutliche Beschleunigung bei minimalem Genauigkeitsverlust (Cheng et al., 2017). Die Pipeline „Deep Compression“ kombiniert drei Stufen: Sie entfernt Verbindungen mit kleinen Gewichten, quantisiert die verbleibenden Gewichte durch Weight Sharing und kodiert sie anschließend mit Huffman-Kodierung. Im Extremfall verwenden binäre Netze ein Bit pro Gewicht, doch ihre Genauigkeit sinkt bei großen Netzen deutlich (Cheng et al., 2017).

#### 3. Low-Rank-Faktorisierung und strukturierte Matrizen
Gewichtsmatrizen vollständig verbundener Schichten und Faltungskerne, als Tensoren betrachtet, lassen sich durch Produkte kleinerer Matrizen oder Tensoren annähern. Berichtet wurden unter anderem eine 2-fache Beschleunigung einer einzelnen Faltungsschicht bei 1 % Genauigkeitsverlust und eine 4,5-fache Beschleunigung bei 1 % Verlust in der Texterkennung. Strukturierte Matrizen gehen weiter, indem sie die Gewichtsmatrix einer Schicht auf eine Form mit weniger Parametern beschränken: Eine zirkulante Matrix speichert eine d × d-Schicht mit O(d) statt O(d²) Speicher und berechnet sie über die schnelle Fourier-Transformation in O(d log d) Zeit (Cheng et al., 2017).

#### 4. Knowledge Distillation
Statt das Netz selbst zu verkleinern, trainiert [[knowledge-distillation|Knowledge Distillation]] ein separates kleines Modell, das ein großes nachbildet. Buciluǎ et al. (2006) verdichteten so Ensembles aus Hunderten oder Tausenden von Klassifikatoren: Sie ließen das Ensemble Pseudodaten labeln und trainierten darauf ein kleineres, schnelleres Modell, meist ohne nennenswerten Leistungsverlust. Spätere Arbeiten übertragen die geglättete Ausgabeverteilung des großen Modells auf ein kleines Student-Netz und erweitern dies auf schmale, aber tiefe Student-Netze, die auch aus Zwischenrepräsentationen lernen (Cheng et al., 2017).

#### Ursprung und Varianten
Buciluǎ et al. (2006) prägten den Begriff für das Verdichten großer Ensembles. Übersichtsarbeiten von Cheng et al. (2017) und Deng et al. (2020) ordnen die Verfahren für tiefe Netze; Deng et al. (2020) behandeln zudem, wie Kompression das Design von Hardware-Beschleunigern für neuronale Netze prägt. Verfahren werden zunehmend kombiniert: Zafar et al. (2026) destillieren und quantisieren ein Übersetzungsmodell gemeinsam. Es entstehen weiterhin neue Ansätze, etwa Kompression auf Basis dynamischer Systeme, die hochdimensionale Gewichte als Index einer Trajektorie eines dynamischen Systems speichert und bei der Dekompression zurückgewinnt, ein Mechanismus, der sich von Pruning, Quantisierung, Distillation und Low-Rank-Zerlegung unterscheidet (Gao et al., 2026).

### Wann einsetzen
- Einsatz auf Geräten mit wenig Speicher, etwa Smartphones, Wearables und eingebetteten Systemen, oder in Anwendungen mit strengen Latenzanforderungen (Cheng et al., 2017; Deng et al., 2020; Gao et al., 2026).
- Ein Modell günstiger und mit geringerem Energieverbrauch und geringeren Emissionen betreiben (Zafar et al., 2026); siehe auch [[llm-cost-optimisation|LLM-Kostenoptimierung]].
- Ein großes Ensemble oder Teacher-Modell zur Inferenzzeit durch ein einzelnes kleines Modell ersetzen (Buciluǎ et al., 2006).

### Stärken und Grenzen
Stärken:
- Pruning und Quantisierung sind in verschiedenen Situationen robust und funktionieren sowohl beim Training von Grund auf als auch mit vortrainierten Modellen (Cheng et al., 2017).
- Low-Rank-Faktorisierung folgt einer standardisierten, leicht umsetzbaren Pipeline (Cheng et al., 2017).
- Kombinierte Verfahren können ein Modell erheblich verkleinern, mit geringem oder keinem Qualitätsverlust (Zafar et al., 2026).

Grenzen:
- Pruning mit l1- oder l2-Regularisierung braucht mehr Iterationen bis zur Konvergenz, Pruning-Kriterien erfordern manuelle Einstellungen pro Schicht, und Pruning verkleinert oft das Modell, ohne Training oder Inferenz zu beschleunigen (Cheng et al., 2017).
- Binäre Netze verlieren bei großen Modellen deutlich an Genauigkeit, und strukturelle Vorgaben für Gewichtsmatrizen können das Modell verzerren, ohne dass es einen theoretischen Weg gibt, die richtige Struktur zu wählen (Cheng et al., 2017).
- Quantisierung verschlechtert die Leistung, je geringer die Bit-Genauigkeit wird, und Distillation stößt an Grenzen, wenn domänenspezifische Trainingsdaten knapp sind (Zafar et al., 2026).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Pruning und [[quantisation\|Quantisierung]] | Redundante Parameter entfernen oder mit weniger Bits speichern (Cheng et al., 2017) | Vortrainierte Modelle ebenso wie Training von Grund auf |
| Low-Rank-Faktorisierung | Gewichtsmatrizen und Kerne durch kleinere Faktoren annähern (Cheng et al., 2017) | Faltungsschichten und vollständig verbundene Schichten |
| Kompakte Faltungsfilter | Spezielle Filterstrukturen mit weniger Parametern; abhängig von der Anwendung (Cheng et al., 2017) | Neue Faltungsarchitekturen, die von Grund auf trainiert werden |
| [[knowledge-distillation\|Knowledge Distillation]] | Ein kleines Modell trainieren, das ein großes nachbildet; Ergebnisse hängen von Anwendung und Netzstruktur ab (Cheng et al., 2017) | Große Modelle oder Ensembles durch kleine ersetzen |

### In der Praxis
Kompressionsverfahren werden nach Kompressionsrate und Beschleunigung zusammen mit der Veränderung der Genauigkeit verglichen (Cheng et al., 2017). Die Kombination von Verfahren kann sich lohnen: Für biomedizinische Übersetzung von Französisch nach Englisch war ein gemeinsam destilliertes und quantisiertes Student-Modell 69 % kleiner und 98,21 % schneller als sein Teacher, mit 98,46 % weniger CO2-Emissionen und geringem oder keinem Verlust an Übersetzungsqualität (Zafar et al., 2026).

### Merksatz
Die meisten trainierten Netze enthalten viele redundante Parameter; Pruning, Quantisierung, Faktorisierung und Distillation entfernen oder ersetzen sie, damit ein Modell in das Speicher-, Latenz- und Kostenbudget seines Einsatzes passt.

### Quellen
- Buciluǎ, C., Caruana, R. & Niculescu-Mizil, A. (2006). *Model compression.* KDD 2006. [DOI](https://doi.org/10.1145/1150402.1150464)
- Cheng, Y. et al. (2017). *A Survey of Model Compression and Acceleration for Deep Neural Networks.* [arXiv:1710.09282](https://arxiv.org/abs/1710.09282)
- Deng, L. et al. (2020). *Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey.* Proceedings of the IEEE. [DOI](https://doi.org/10.1109/jproc.2020.2976475)
- Zafar, M. et al. (2026). *Investigating Model Compression for Neural Machine Translation in the Biomedical Domain.* [arXiv:2610.07032](https://arxiv.org/abs/2610.07032)
- Gao, F. et al. (2026). *Dynamics as Code: On Model Compression via Dynamic System.* [arXiv:2610.11115](https://arxiv.org/abs/2610.11115)
