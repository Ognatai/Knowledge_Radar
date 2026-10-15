---
title_en: GLUE
title_de: GLUE
entity_type: Dataset
aliases:
- GLUE
- General Language Understanding Evaluation
- GLUE benchmark
- SuperGLUE
sources:
- https://arxiv.org/abs/1804.07461
- https://arxiv.org/abs/1905.00537
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The General Language Understanding Evaluation (GLUE) benchmark, introduced in 2018 and published at ICLR 2019, collects nine existing English sentence and sentence-pair tasks, among them acceptability, sentiment, paraphrase, similarity and [[natural-language-inference|natural language inference]], with an online leaderboard based mostly on privately held test labels and a hand-crafted diagnostic set (Wang et al., 2019a). A model's GLUE score is the macro-average of its task scores (Wang et al., 2019a). GLUE became the showcase for pre-trained models such as [[gpt|GPT]] and [[bert|BERT]], which scored 72.8 and 80.2 against 66.5 for an ELMo-based baseline; by July 2019 the best system (88.4) exceeded the non-expert human estimate (87.1), and the authors released the harder SuperGLUE benchmark (Wang et al., 2019b).

### How it works

```text
9 tasks, all (sentence | sentence pair) → label, except STS-B (regression)
  single sentence:  CoLA (acceptability, Matthews corr.), SST-2 (sentiment, acc.)
  similarity/para.: MRPC, QQP (acc./F1), STS-B (Pearson/Spearman)
  inference:        MNLI (3-way, matched/mismatched), QNLI, RTE, WNLI (acc.)
model predicts on test inputs → upload to server (labels hidden) → per-task score → macro-average = GLUE score
+ diagnostic NLI set tagged with linguistic phenomena (analysis only)
```

#### 1. Nine tasks from existing datasets

None of the datasets was created for GLUE; the authors chose established datasets that the NLP community regarded as challenging (Wang et al., 2019a). The single-sentence tasks are CoLA, English acceptability judgements from linguistics literature, and SST-2, two-way sentiment of movie review sentences. The similarity and paraphrase tasks are MRPC (news sentence pairs), QQP (Quora question pairs) and STS-B (similarity scores from 1 to 5). The inference tasks are MNLI (entailment, contradiction or neutral across ten genres), QNLI (whether a Wikipedia sentence answers a question, recast from SQuAD), RTE (combined textual entailment challenges) and WNLI (Winograd schemas recast as sentence pairs) (Wang et al., 2019a). Training sets range from 634 examples (WNLI) to 393,000 (MNLI), so that good results should require sharing knowledge across tasks (Wang et al., 2019a).

#### 2. Metrics and the leaderboard

Tasks are scored on accuracy unless the data calls for something else: CoLA uses the Matthews correlation coefficient, MRPC and QQP report accuracy and F1 because their classes are imbalanced, and STS-B uses Pearson and Spearman correlation ([[classification-metrics|classification metrics]]; Wang et al., 2019a). For tasks with two metrics, their unweighted average is the task score, and the macro-average across tasks determines a system's position on the leaderboard (Wang et al., 2019a). GLUE places no constraint on the model architecture beyond processing single sentences and sentence pairs (Wang et al., 2019a).

#### 3. Diagnostic dataset

A small, expert-built set of NLI sentence pairs is tagged with linguistic phenomena in four coarse categories: lexical semantics, predicate-argument structure, logic and knowledge, for example negation, quantifiers, coreference and world knowledge (Wang et al., 2019a). It is meant for analysis, not for the main score; the baselines handled strong lexical signals well but often failed on deeper logical structure (Wang et al., 2019a).

#### 4. Baselines and the move to SuperGLUE

In the original paper, multi-task training on all tasks beat training one model per task, and the best baseline used ELMo; on WNLI no model beat majority-class guessing (65.1%) (Wang et al., 2019a). Within about a year, pre-trained Transformers had raised the state of the art beyond the human estimate, leaving little headroom (Wang et al., 2019b). SuperGLUE keeps the two hardest GLUE tasks, adds tasks chosen from an open call for difficulty (BoolQ, CB, COPA, MultiRC, ReCoRD, RTE, WiC, WSC), widens the formats to question answering and coreference, and reports human baselines for every task; its BERT-based baseline was nearly 20 points below human performance (Wang et al., 2019b).

#### Origin and variants

GLUE was built by researchers from New York University, the University of Washington and DeepMind (Wang et al., 2019a); SuperGLUE followed in 2019 at NeurIPS (Wang et al., 2019b). Domain benchmarks reuse the idea of a task suite with one aggregate score, for example LexGLUE for legal language ([[legal-ai|legal AI]]).

### When to use it

- Comparing encoder models for English sentence [[classification|classification]] and sentence-pair tasks, for example after pre-training, fine-tuning or [[knowledge-distillation|knowledge distillation]] ([[distilbert|DistilBERT]]).
- Reading older NLP papers, where GLUE scores were the standard summary of language understanding ([[natural-language-understanding|natural language understanding]]).
- Not for current [[large-language-models|large language models]]: GLUE is saturated, and generative or task-specific evaluation fits better ([[llm-evaluation|LLM evaluation]]).

### Strengths and limitations

**Strengths**
- One number summarises performance across tasks, data sizes and genres, while per-task scores stay visible (Wang et al., 2019a).
- Hidden test labels and a server reduce tuning on the test set (Wang et al., 2019a).
- The diagnostic set shows which linguistic phenomena a model misses (Wang et al., 2019a).

**Limitations**
- English only, and limited to sentence and sentence-pair classification or regression (Wang et al., 2019b).
- Saturated: top systems passed the non-expert human estimate in 2019 (Wang et al., 2019b).
- A macro-average hides large differences between tasks; small tasks such as WNLI and RTE weigh as much as MNLI (Wang et al., 2019a).

### Comparison

| | GLUE | SuperGLUE |
|---|---|---|
| Tasks | 9 | 8 |
| Formats | sentence and sentence-pair classification, one regression task | adds question answering and coreference |
| Human baseline | estimate added later (87.1) | for every task |
| Best model at release vs humans | 2019: 88.4 vs 87.1 | BERT baseline nearly 20 points below humans |

Sources: Wang et al. (2019a); Wang et al. (2019b).

### In practice

For small encoder models in production, GLUE tasks remain a quick sanity check that a compressed or distilled model has kept its language understanding; DistilBERT, for example, reported its quality as a share of BERT's GLUE score ([[distilbert|DistilBERT]]). For the actual application, a task-specific test set from the target domain says more than a public leaderboard number ([[llm-evaluation|LLM evaluation]]).

### Key takeaway

GLUE bundled nine English understanding tasks into one leaderboard score and became the yardstick of the pre-training era, until models surpassed its human estimate and SuperGLUE took over.

### Sources

- Wang, A., Singh, A., Michael, J., Hill, F., Levy, O. & Bowman, S. R. (2019a). GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding. *ICLR 2019*. [arXiv:1804.07461](https://arxiv.org/abs/1804.07461)
- Wang, A., Pruksachatkun, Y., Nangia, N., Singh, A., Michael, J., Hill, F., Levy, O. & Bowman, S. R. (2019b). SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems. *NeurIPS 2019*. [arXiv:1905.00537](https://arxiv.org/abs/1905.00537)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der Benchmark General Language Understanding Evaluation (GLUE), 2018 vorgestellt und auf der ICLR 2019 veröffentlicht, bündelt neun bestehende englische Aufgaben für Sätze und Satzpaare, darunter grammatische Akzeptabilität, Sentiment, Paraphrasen, Ähnlichkeit und [[natural-language-inference|Natural Language Inference]], mit einer Online-Rangliste, die überwiegend auf nicht veröffentlichten Test-Labels beruht, und einem von Hand erstellten Diagnose-Set (Wang et al., 2019a). Der GLUE-Score eines Modells ist der Makro-Durchschnitt seiner Aufgabenwerte (Wang et al., 2019a). GLUE wurde zum Schaufenster für vortrainierte Modelle wie [[gpt|GPT]] und [[bert|BERT]], die 72,8 und 80,2 Punkte gegenüber 66,5 für eine ELMo-basierte Baseline erreichten; im Juli 2019 übertraf das beste System (88,4) die Schätzung für menschliche Laien (87,1), und die Autoren veröffentlichten den schwierigeren Benchmark SuperGLUE (Wang et al., 2019b).

### Funktionsweise

```text
9 Aufgaben, alle (Satz | Satzpaar) → Label, außer STS-B (Regression)
  Einzelsatz:        CoLA (Akzeptabilität, Matthews-Korr.), SST-2 (Sentiment, Acc.)
  Ähnlichkeit/Para.: MRPC, QQP (Acc./F1), STS-B (Pearson/Spearman)
  Inferenz:          MNLI (3 Klassen, matched/mismatched), QNLI, RTE, WNLI (Acc.)
Modell sagt Test-Eingaben vorher → Upload an Server (Labels verborgen) → Wert je Aufgabe → Makro-Durchschnitt = GLUE-Score
+ Diagnose-Set für NLI mit markierten sprachlichen Phänomenen (nur zur Analyse)
```

#### 1. Neun Aufgaben aus bestehenden Datensätzen

Keiner der Datensätze wurde für GLUE erstellt; die Autoren wählten etablierte Datensätze, die in der NLP-Gemeinschaft als anspruchsvoll galten (Wang et al., 2019a). Die Einzelsatz-Aufgaben sind CoLA, Urteile zur Akzeptabilität englischer Sätze aus linguistischer Fachliteratur, und SST-2, zweiwertiges Sentiment von Sätzen aus Filmkritiken. Die Ähnlichkeits- und Paraphrasen-Aufgaben sind MRPC (Satzpaare aus Nachrichten), QQP (Fragenpaare von Quora) und STS-B (Ähnlichkeitswerte von 1 bis 5). Die Inferenz-Aufgaben sind MNLI (Folgerung, Widerspruch oder neutral über zehn Textsorten), QNLI (ob ein Wikipedia-Satz eine Frage beantwortet, umgewandelt aus SQuAD), RTE (zusammengeführte Textual-Entailment-Wettbewerbe) und WNLI (Winograd-Schemata, umgewandelt in Satzpaare) (Wang et al., 2019a). Die Trainingsmengen reichen von 634 Beispielen (WNLI) bis 393 000 (MNLI), sodass gute Ergebnisse geteiltes Wissen über Aufgaben hinweg erfordern sollen (Wang et al., 2019a).

#### 2. Metriken und Rangliste

Aufgaben werden nach Accuracy bewertet, sofern die Daten nichts anderes verlangen: CoLA nutzt den Matthews-Korrelationskoeffizienten, MRPC und QQP berichten Accuracy und F1, weil ihre Klassen unausgewogen sind, und STS-B nutzt Pearson- und Spearman-Korrelation ([[classification-metrics|Klassifikationsmetriken]]; Wang et al., 2019a). Bei Aufgaben mit zwei Metriken ist deren ungewichteter Mittelwert der Aufgabenwert, und der Makro-Durchschnitt über die Aufgaben bestimmt den Platz in der Rangliste (Wang et al., 2019a). GLUE schreibt keine Modellarchitektur vor, außer dass Einzelsätze und Satzpaare verarbeitet werden können (Wang et al., 2019a).

#### 3. Diagnose-Datensatz

Ein kleines, von Fachleuten erstelltes Set von NLI-Satzpaaren ist mit sprachlichen Phänomenen in vier Grobkategorien markiert: lexikalische Semantik, Prädikat-Argument-Struktur, Logik und Wissen, etwa Negation, Quantoren, Koreferenz und Weltwissen (Wang et al., 2019a). Es dient der Analyse, nicht dem Hauptwert; die Baselines kamen mit starken lexikalischen Signalen gut zurecht, scheiterten aber oft an tieferer logischer Struktur (Wang et al., 2019a).

#### 4. Baselines und der Wechsel zu SuperGLUE

Im ursprünglichen Paper schlug Multi-Task-Training auf allen Aufgaben das Training eines Modells je Aufgabe, und die beste Baseline nutzte ELMo; bei WNLI übertraf kein Modell das Raten der häufigsten Klasse (65,1 %) (Wang et al., 2019a). Innerhalb von etwa einem Jahr hoben vortrainierte Transformer den Stand der Technik über die menschliche Schätzung, sodass kaum Spielraum blieb (Wang et al., 2019b). SuperGLUE behält die zwei schwierigsten GLUE-Aufgaben, ergänzt Aufgaben, die aus einem offenen Aufruf nach ihrer Schwierigkeit ausgewählt wurden (BoolQ, CB, COPA, MultiRC, ReCoRD, RTE, WiC, WSC), erweitert die Formate um Fragebeantwortung und Koreferenz und gibt für jede Aufgabe eine menschliche Baseline an; seine BERT-basierte Baseline lag fast 20 Punkte unter der menschlichen Leistung (Wang et al., 2019b).

#### Herkunft und Varianten

GLUE wurde von Forschenden der New York University, der University of Washington und von DeepMind entwickelt (Wang et al., 2019a); SuperGLUE folgte 2019 auf der NeurIPS (Wang et al., 2019b). Fachspezifische Benchmarks übernehmen die Idee einer Aufgabensammlung mit einem Gesamtwert, etwa LexGLUE für Rechtssprache ([[legal-ai|Legal AI]]).

### Wann einsetzen

- Zum Vergleich von Encoder-Modellen für die [[classification|Klassifikation]] englischer Sätze und Satzpaare, etwa nach Vortraining, Fine-Tuning oder [[knowledge-distillation|Knowledge Distillation]] ([[distilbert|DistilBERT]]).
- Beim Lesen älterer NLP-Arbeiten, in denen GLUE-Werte die übliche Zusammenfassung des Sprachverstehens waren ([[natural-language-understanding|Natural Language Understanding]]).
- Nicht für aktuelle große Sprachmodelle: GLUE ist gesättigt, generative oder aufgabenspezifische Evaluation passt besser ([[llm-evaluation|LLM-Evaluation]]).

### Stärken und Grenzen

**Stärken**
- Eine Zahl fasst die Leistung über Aufgaben, Datenmengen und Textsorten zusammen, während die Werte je Aufgabe sichtbar bleiben (Wang et al., 2019a).
- Verborgene Test-Labels und ein Bewertungsserver erschweren das Abstimmen auf die Testmenge (Wang et al., 2019a).
- Das Diagnose-Set zeigt, welche sprachlichen Phänomene ein Modell verfehlt (Wang et al., 2019a).

**Grenzen**
- Nur Englisch und beschränkt auf Klassifikation oder Regression von Sätzen und Satzpaaren (Wang et al., 2019b).
- Gesättigt: Spitzensysteme übertrafen 2019 die Schätzung für menschliche Laien (Wang et al., 2019b).
- Ein Makro-Durchschnitt verdeckt große Unterschiede zwischen Aufgaben; kleine Aufgaben wie WNLI und RTE zählen so viel wie MNLI (Wang et al., 2019a).

### Vergleich

| | GLUE | SuperGLUE |
|---|---|---|
| Aufgaben | 9 | 8 |
| Formate | Klassifikation von Sätzen und Satzpaaren, eine Regressionsaufgabe | zusätzlich Fragebeantwortung und Koreferenz |
| Menschliche Baseline | Schätzung später ergänzt (87,1) | für jede Aufgabe |
| Bestes Modell bei Erscheinen vs. Menschen | 2019: 88,4 vs. 87,1 | BERT-Baseline fast 20 Punkte unter Menschen |

Quellen: Wang et al. (2019a); Wang et al. (2019b).

### In der Praxis

Für kleine Encoder-Modelle im Produktivbetrieb bleiben GLUE-Aufgaben eine schnelle Plausibilitätsprüfung, ob ein komprimiertes oder destilliertes Modell sein Sprachverstehen behalten hat; DistilBERT etwa gab seine Qualität als Anteil am GLUE-Wert von BERT an ([[distilbert|DistilBERT]]). Für die eigentliche Anwendung sagt eine aufgabenspezifische Testmenge aus der Zieldomäne mehr als ein öffentlicher Ranglistenwert ([[llm-evaluation|LLM-Evaluation]]).

### Merksatz

GLUE bündelte neun englische Verstehensaufgaben zu einem Ranglistenwert und wurde zum Maßstab der Vortrainings-Ära, bis Modelle die menschliche Schätzung übertrafen und SuperGLUE übernahm.

### Quellen

- Wang, A., Singh, A., Michael, J., Hill, F., Levy, O. & Bowman, S. R. (2019a). GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding. *ICLR 2019*. [arXiv:1804.07461](https://arxiv.org/abs/1804.07461)
- Wang, A., Pruksachatkun, Y., Nangia, N., Singh, A., Michael, J., Hill, F., Levy, O. & Bowman, S. R. (2019b). SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems. *NeurIPS 2019*. [arXiv:1905.00537](https://arxiv.org/abs/1905.00537)
