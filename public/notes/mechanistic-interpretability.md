---
title_en: Mechanistic Interpretability
title_de: Mechanistic Interpretability
entity_type: Method
aliases:
- Mechanistic interpretability
- LLM interpretability
- Probing classifiers
- Probing
- Logit lens
- Sparse autoencoders
- Superposition
- Induction heads
- Causal tracing
- Activation patching
sources:
- https://web.stanford.edu/~jurafsky/slp3/10.pdf
- https://arxiv.org/abs/1909.03368
- https://arxiv.org/abs/2102.12452
- https://arxiv.org/abs/2209.10652
- https://arxiv.org/abs/2309.08600
- https://arxiv.org/abs/2209.11895
- https://arxiv.org/abs/2202.05262
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Mechanistic interpretability tries to explain how a neural network, usually a Transformer language model, computes its outputs: which internal representations encode which information and which components ("circuits") carry out which steps (Jurafsky & Martin, 2026). Its main tools are probing classifiers that test what representations encode (Belinkov, 2022), lenses that read intermediate layers as token distributions, sparse autoencoders that split neurons into interpretable features (Cunningham et al., 2024), causal interventions that locate where a behaviour happens (Meng et al., 2022) and circuit analyses such as induction heads for in-context learning (Olsson et al., 2022). Unlike post-hoc [[explainable-ai|explainable AI]] methods that attribute a prediction to input features, it looks at the model's internals.

### How it works

```text
model + inputs ──► record activations (residual stream, attention heads, MLP outputs) at every layer
   │
   ├─ probing:        train a small classifier on frozen activations → is property X encoded? (with control tasks)
   ├─ logit lens:     project an intermediate vector through the unembedding → which tokens does it "mean"?
   ├─ sparse autoencoder: decompose activations into many sparse features → name features
   ├─ causal tracing / patching: corrupt the input, restore one activation → where is the behaviour computed?
   └─ circuits:       trace how specific heads and neurons combine (e.g. induction heads)
   ▼
hypothesis about the mechanism ──► test by ablation or editing
```

#### 1. Probing classifiers

A probe is a simple classifier, such as [[logistic-regression|logistic regression]] or a small MLP, trained on frozen activations from a chosen layer to predict a property such as part of speech, tense or coreference (Jurafsky & Martin, 2026). Probing has suggested that grammatical information is encoded in lower layers of a Transformer, semantic information in middle layers and discourse information such as coreference higher up (Jurafsky & Martin, 2026). Probes need controls: Hewitt and Liang (2019) introduced control tasks that assign random outputs to word types, which only the probe itself can learn; a good probe is selective, accurate on the linguistic task but not on the control task, and popular probes on ELMo were not. Even a successful probe shows only that information is present, not that the model uses it (Belinkov, 2022; Jurafsky & Martin, 2026).

#### 2. Logit lens

The logit lens multiplies a vector from any intermediate layer by the unembedding matrix and applies a [[softmax|softmax]], treating it as if it were the final layer, to see which tokens it represents (Jurafsky & Martin, 2026). Because intermediate layers were not trained to be read this way, it does not always work; a Jacobian-based variant, the J-lens, maps earlier layers through an approximation of the rest of the network and revealed layer-by-layer multi-step reasoning in a large model, for example resolving "the fourth planet" to Mars before producing "red" (Jurafsky & Martin, 2026).

#### 3. Superposition and sparse autoencoders

Neurons are often polysemantic: they respond to several unrelated concepts. Toy models show that this can arise when a network stores more sparse features than it has dimensions, in superposition, with a phase change between storing features in superposition or not (Elhage et al., 2022). Sparse autoencoders try to undo this: trained to reconstruct a layer's activations through a wider hidden layer with a ReLU and an L1 sparsity penalty, `L = ‖x − x̂‖² + α‖c‖₁`, they learn a dictionary of sparsely active features that are more interpretable and monosemantic than neurons or other directions, and some features could be shown to be causally responsible for model behaviour on an indirect-object task (Cunningham et al., 2024; [[autoencoders-and-gans|autoencoders]]).

#### 4. Causal interventions

Causal tracing runs a model three times: on the clean input, on an input whose subject tokens are corrupted with noise, and on the corrupted input with one internal state restored to its clean value; the states whose restoration recovers the correct answer mediate the behaviour (Meng et al., 2022). For factual recall in [[gpt|GPT]] this located decisive computations in middle-layer feed-forward modules processing the subject; editing these weights with rank-one model editing (ROME) changed specific facts while keeping specificity and generalisation (Meng et al., 2022).

#### 5. Circuits: induction heads

Induction heads are attention heads that complete patterns of the form [A][B] … [A] → [B] by looking back for an earlier occurrence of the current token and copying what followed (Olsson et al., 2022; Jurafsky & Martin, 2026). Olsson et al. (2022) found that they form at exactly the point in training where in-context learning ability rises sharply, visible as a bump in the loss, and argued from six lines of evidence that they may be the main mechanism of in-context learning; the evidence is causal for small attention-only models and correlational for larger models ([[few-shot-prompting|few-shot prompting]]).

#### Origin and variants

Probing grew out of analyses of NLP representations and has been critically reviewed by Belinkov (2022). The logit lens was proposed by nostalgebraist in 2020 (Jurafsky & Martin, 2026). Superposition (Elhage et al., 2022) and induction heads (Olsson et al., 2022) come from the Transformer Circuits research programme; sparse autoencoders for language models from Cunningham et al. (2024); causal tracing and ROME from Meng et al. (2022).

### When to use it

- Checking whether a model encodes or relies on a sensitive attribute, for example gender, in its representations ([[bias-in-nlp|bias in NLP]], [[fairness-metrics|fairness metrics]]).
- Locating and editing specific stored facts (Meng et al., 2022).
- Understanding failure modes such as hidden behaviours, as a complement to testing ([[sleeper-agents|sleeper agents]], [[red-teaming|red teaming]]).
- Studying how capabilities such as in-context learning emerge during training (Olsson et al., 2022).

### Strengths and limitations

**Strengths**
- Looks at the computation itself rather than only at input–output behaviour (Jurafsky & Martin, 2026).
- Causal methods test whether a component matters, not just whether information is present (Meng et al., 2022).
- Sparse features give more human-understandable units than neurons (Cunningham et al., 2024).

**Limitations**
- Probing results depend on probe capacity and controls and do not show use by the model (Hewitt & Liang, 2019; Belinkov, 2022).
- The logit lens assumes intermediate layers share the output space, which is not always true (Jurafsky & Martin, 2026).
- Evidence for larger models is often correlational rather than causal (Olsson et al., 2022).
- Feature interpretations in sparse autoencoders were rated with automated methods, and labelling them remains subjective (Cunningham et al., 2024).

### Comparison

| Method | Question answered | Causal? |
|---|---|---|
| Probing | Is property X decodable from layer L? | no |
| Logit lens / J-lens | Which tokens does an intermediate vector point to? | no |
| Sparse autoencoder | Which interpretable features make up an activation? | partly (with interventions) |
| Causal tracing / patching | Which states mediate a behaviour? | yes |
| Circuit analysis | Which components implement an algorithm? | yes in small models |
| [[explainable-ai\|Post-hoc attribution]] | Which input features drove this prediction? | no |

Sources: Jurafsky & Martin (2026), Belinkov (2022), Meng et al. (2022), Olsson et al. (2022), Cunningham et al. (2024).

### In practice

Interpretability claims are strongest when an observational finding (a probe, a lens, a feature) is confirmed by an intervention such as ablation or patching (Belinkov, 2022; Meng et al., 2022). Probes should be compared with control tasks or random-label baselines and kept simple (Hewitt & Liang, 2019; Jurafsky & Martin, 2026).

### Key takeaway

Mechanistic interpretability opens the model: probes and lenses show what representations encode, sparse autoencoders turn polysemantic neurons into features, and causal interventions and circuit analyses show which components actually produce a behaviour.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 10: Interpretability. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/10.pdf)
- Hewitt, J. & Liang, P. (2019). *Designing and Interpreting Probes with Control Tasks.* EMNLP 2019. [arXiv:1909.03368](https://arxiv.org/abs/1909.03368)
- Belinkov, Y. (2022). *Probing Classifiers: Promises, Shortcomings, and Advances.* Computational Linguistics. [arXiv:2102.12452](https://arxiv.org/abs/2102.12452)
- Elhage, N. et al. (2022). *Toy Models of Superposition.* Transformer Circuits Thread. [arXiv:2209.10652](https://arxiv.org/abs/2209.10652)
- Cunningham, H., Ewart, A., Riggs, L., Huben, R. & Sharkey, L. (2024). *Sparse Autoencoders Find Highly Interpretable Features in Language Models.* ICLR 2024. [arXiv:2309.08600](https://arxiv.org/abs/2309.08600)
- Olsson, C. et al. (2022). *In-context Learning and Induction Heads.* Transformer Circuits Thread. [arXiv:2209.11895](https://arxiv.org/abs/2209.11895)
- Meng, K., Bau, D., Andonian, A. & Belinkov, Y. (2022). *Locating and Editing Factual Associations in GPT.* NeurIPS 2022. [arXiv:2202.05262](https://arxiv.org/abs/2202.05262)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Mechanistic Interpretability versucht zu erklären, wie ein neuronales Netz, meist ein Transformer-Sprachmodell, seine Ausgaben berechnet: welche internen Repräsentationen welche Information kodieren und welche Komponenten („Circuits“) welche Schritte ausführen (Jurafsky & Martin, 2026). Ihre wichtigsten Werkzeuge sind Probing-Klassifikatoren, die prüfen, was Repräsentationen kodieren (Belinkov, 2022), Lenses, die Zwischenschichten als Token-Verteilungen lesen, Sparse Autoencoder, die Neuronen in interpretierbare Merkmale zerlegen (Cunningham et al., 2024), kausale Eingriffe, die verorten, wo ein Verhalten entsteht (Meng et al., 2022), und Circuit-Analysen wie die Induction Heads für In-Context Learning (Olsson et al., 2022). Anders als nachträgliche Verfahren der [[explainable-ai|Explainable AI]], die eine Vorhersage Eingabemerkmalen zuschreiben, betrachtet sie das Innere des Modells.

### Funktionsweise

```text
Modell + Eingaben ──► Aktivierungen aufzeichnen (Residual Stream, Attention-Heads, MLP-Ausgaben) in jeder Schicht
   │
   ├─ Probing:        kleinen Klassifikator auf eingefrorenen Aktivierungen trainieren → ist Eigenschaft X kodiert? (mit Kontrollaufgaben)
   ├─ Logit Lens:     Zwischenvektor durch das Unembedding projizieren → welche Tokens „meint“ er?
   ├─ Sparse Autoencoder: Aktivierungen in viele dünn besetzte Merkmale zerlegen → Merkmale benennen
   ├─ Causal Tracing / Patching: Eingabe stören, eine Aktivierung wiederherstellen → wo wird das Verhalten berechnet?
   └─ Circuits:       verfolgen, wie bestimmte Heads und Neuronen zusammenwirken (z. B. Induction Heads)
   ▼
Hypothese über den Mechanismus ──► per Ablation oder Editierung testen
```

#### 1. Probing-Klassifikatoren

Ein Probe ist ein einfacher Klassifikator, etwa eine [[logistic-regression|logistische Regression]] oder ein kleines MLP, der auf eingefrorenen Aktivierungen einer gewählten Schicht trainiert wird, um eine Eigenschaft wie Wortart, Tempus oder Koreferenz vorherzusagen (Jurafsky & Martin, 2026). Probing legt nahe, dass grammatische Information in unteren Schichten eines Transformers kodiert ist, semantische in mittleren und Diskursinformation wie Koreferenz weiter oben (Jurafsky & Martin, 2026). Probes brauchen Kontrollen: Hewitt und Liang (2019) führten Kontrollaufgaben ein, die Worttypen zufällige Ausgaben zuordnen und nur vom Probe selbst gelernt werden können; ein guter Probe ist selektiv, also genau bei der linguistischen Aufgabe, aber nicht bei der Kontrollaufgabe, und verbreitete Probes auf ELMo waren es nicht. Selbst ein erfolgreicher Probe zeigt nur, dass Information vorhanden ist, nicht, dass das Modell sie nutzt (Belinkov, 2022; Jurafsky & Martin, 2026).

#### 2. Logit Lens

Die Logit Lens multipliziert einen Vektor aus einer beliebigen Zwischenschicht mit der Unembedding-Matrix und wendet eine [[softmax|Softmax]] an, als wäre er die letzte Schicht, um zu sehen, welche Tokens er darstellt (Jurafsky & Martin, 2026). Weil Zwischenschichten nicht darauf trainiert wurden, so gelesen zu werden, funktioniert das nicht immer; eine Variante auf Basis der Jacobi-Matrix, die J-Lens, bildet frühere Schichten über eine Näherung des restlichen Netzes ab und zeigte in einem großen Modell schichtweises mehrstufiges Schlussfolgern, etwa die Auflösung von „dem vierten Planeten“ zu Mars, bevor „rot“ entsteht (Jurafsky & Martin, 2026).

#### 3. Superposition und Sparse Autoencoder

Neuronen sind oft polysemantisch: Sie reagieren auf mehrere unzusammenhängende Konzepte. Toy-Modelle zeigen, dass dies entstehen kann, wenn ein Netz mehr dünn besetzte Merkmale speichert, als es Dimensionen hat, in Superposition, mit einem Phasenübergang zwischen Speicherung in Superposition und ohne (Elhage et al., 2022). Sparse Autoencoder versuchen das rückgängig zu machen: Trainiert, die Aktivierungen einer Schicht über eine breitere verborgene Schicht mit ReLU und L1-Sparsity-Strafterm zu rekonstruieren, `L = ‖x − x̂‖² + α‖c‖₁`, lernen sie ein Wörterbuch dünn aktiver Merkmale, die interpretierbarer und monosemantischer sind als Neuronen oder andere Richtungen; für einige Merkmale ließ sich zeigen, dass sie das Verhalten des Modells bei einer Aufgabe zu indirekten Objekten kausal bestimmen (Cunningham et al., 2024; [[autoencoders-and-gans|Autoencoder]]).

#### 4. Kausale Eingriffe

Causal Tracing lässt ein Modell dreimal laufen: auf der sauberen Eingabe, auf einer Eingabe, deren Subjekt-Tokens mit Rauschen gestört sind, und auf der gestörten Eingabe mit einem auf seinen sauberen Wert zurückgesetzten internen Zustand; die Zustände, deren Wiederherstellung die richtige Antwort zurückbringt, vermitteln das Verhalten (Meng et al., 2022). Für das Abrufen von Fakten in [[gpt|GPT]] verortete das entscheidende Berechnungen in Feedforward-Modulen mittlerer Schichten, die das Subjekt verarbeiten; das Editieren dieser Gewichte mit Rank-One Model Editing (ROME) änderte bestimmte Fakten und erhielt dabei Spezifität und Generalisierung (Meng et al., 2022).

#### 5. Circuits: Induction Heads

Induction Heads sind Attention-Heads, die Muster der Form [A][B] … [A] → [B] vervollständigen, indem sie nach einem früheren Vorkommen des aktuellen Tokens suchen und kopieren, was darauf folgte (Olsson et al., 2022; Jurafsky & Martin, 2026). Olsson et al. (2022) fanden, dass sie genau an dem Punkt des Trainings entstehen, an dem die Fähigkeit zum In-Context Learning sprunghaft steigt, sichtbar als Delle im Verlust, und argumentierten mit sechs Belegsträngen, dass sie der Hauptmechanismus des In-Context Learning sein könnten; die Belege sind für kleine reine Attention-Modelle kausal und für größere Modelle korrelativ ([[few-shot-prompting|Few-Shot-Prompting]]).

#### Ursprung und Varianten

Probing entstand aus Analysen von NLP-Repräsentationen und wurde von Belinkov (2022) kritisch zusammengefasst. Die Logit Lens schlug nostalgebraist 2020 vor (Jurafsky & Martin, 2026). Superposition (Elhage et al., 2022) und Induction Heads (Olsson et al., 2022) stammen aus dem Forschungsprogramm Transformer Circuits, Sparse Autoencoder für Sprachmodelle von Cunningham et al. (2024), Causal Tracing und ROME von Meng et al. (2022).

### Wann einsetzen

- Prüfen, ob ein Modell ein sensibles Merkmal, etwa Geschlecht, in seinen Repräsentationen kodiert oder sich darauf stützt ([[bias-in-nlp|Bias in NLP]], [[fairness-metrics|Fairness-Metriken]]).
- Bestimmte gespeicherte Fakten verorten und editieren (Meng et al., 2022).
- Fehlermuster wie verborgene Verhaltensweisen verstehen, als Ergänzung zum Testen ([[sleeper-agents|Sleeper Agents]], [[red-teaming|Red Teaming]]).
- Untersuchen, wie Fähigkeiten wie In-Context Learning im Training entstehen (Olsson et al., 2022).

### Stärken und Grenzen

**Stärken**
- Betrachtet die Berechnung selbst statt nur das Ein-Ausgabe-Verhalten (Jurafsky & Martin, 2026).
- Kausale Verfahren prüfen, ob eine Komponente eine Rolle spielt, nicht nur, ob Information vorhanden ist (Meng et al., 2022).
- Dünn besetzte Merkmale liefern verständlichere Einheiten als Neuronen (Cunningham et al., 2024).

**Grenzen**
- Probing-Ergebnisse hängen von der Kapazität des Probes und den Kontrollen ab und zeigen keine Nutzung durch das Modell (Hewitt & Liang, 2019; Belinkov, 2022).
- Die Logit Lens setzt voraus, dass Zwischenschichten den Ausgaberaum teilen, was nicht immer zutrifft (Jurafsky & Martin, 2026).
- Belege für größere Modelle sind oft korrelativ statt kausal (Olsson et al., 2022).
- Die Interpretierbarkeit der Merkmale von Sparse Autoencodern wurde mit automatisierten Verfahren bewertet, und ihre Benennung bleibt subjektiv (Cunningham et al., 2024).

### Vergleich

| Verfahren | Beantwortete Frage | Kausal? |
|---|---|---|
| Probing | Lässt sich Eigenschaft X aus Schicht L dekodieren? | nein |
| Logit Lens / J-Lens | Auf welche Tokens zeigt ein Zwischenvektor? | nein |
| Sparse Autoencoder | Aus welchen interpretierbaren Merkmalen besteht eine Aktivierung? | teilweise (mit Eingriffen) |
| Causal Tracing / Patching | Welche Zustände vermitteln ein Verhalten? | ja |
| Circuit-Analyse | Welche Komponenten setzen einen Algorithmus um? | ja bei kleinen Modellen |
| [[explainable-ai\|Nachträgliche Attribution]] | Welche Eingabemerkmale trieben diese Vorhersage? | nein |

Quellen: Jurafsky & Martin (2026), Belinkov (2022), Meng et al. (2022), Olsson et al. (2022), Cunningham et al. (2024).

### In der Praxis

Aussagen zur Interpretierbarkeit sind am stärksten, wenn ein beobachtender Befund (ein Probe, eine Lens, ein Merkmal) durch einen Eingriff wie Ablation oder Patching bestätigt wird (Belinkov, 2022; Meng et al., 2022). Probes sollten mit Kontrollaufgaben oder Baselines mit Zufallslabels verglichen und einfach gehalten werden (Hewitt & Liang, 2019; Jurafsky & Martin, 2026).

### Merksatz

Mechanistic Interpretability öffnet das Modell: Probes und Lenses zeigen, was Repräsentationen kodieren, Sparse Autoencoder machen aus polysemantischen Neuronen Merkmale, und kausale Eingriffe und Circuit-Analysen zeigen, welche Komponenten ein Verhalten tatsächlich erzeugen.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 10: Interpretability. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/10.pdf)
- Hewitt, J. & Liang, P. (2019). *Designing and Interpreting Probes with Control Tasks.* EMNLP 2019. [arXiv:1909.03368](https://arxiv.org/abs/1909.03368)
- Belinkov, Y. (2022). *Probing Classifiers: Promises, Shortcomings, and Advances.* Computational Linguistics. [arXiv:2102.12452](https://arxiv.org/abs/2102.12452)
- Elhage, N. et al. (2022). *Toy Models of Superposition.* Transformer Circuits Thread. [arXiv:2209.10652](https://arxiv.org/abs/2209.10652)
- Cunningham, H., Ewart, A., Riggs, L., Huben, R. & Sharkey, L. (2024). *Sparse Autoencoders Find Highly Interpretable Features in Language Models.* ICLR 2024. [arXiv:2309.08600](https://arxiv.org/abs/2309.08600)
- Olsson, C. et al. (2022). *In-context Learning and Induction Heads.* Transformer Circuits Thread. [arXiv:2209.11895](https://arxiv.org/abs/2209.11895)
- Meng, K., Bau, D., Andonian, A. & Belinkov, Y. (2022). *Locating and Editing Factual Associations in GPT.* NeurIPS 2022. [arXiv:2202.05262](https://arxiv.org/abs/2202.05262)
