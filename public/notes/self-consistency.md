---
title_en: Self-Consistency
title_de: Self-Consistency
entity_type: Method
aliases:
- Self-consistency
- Self-consistency decoding
- CoT-SC
- Sample-and-marginalize
sources:
- https://arxiv.org/abs/2203.11171
- https://arxiv.org/abs/2201.11903
- https://arxiv.org/abs/2210.03629
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Self-consistency is a decoding strategy for [[chain-of-thought-prompting|chain-of-thought prompting]]: instead of taking the single greedy reasoning path, it samples many diverse reasoning paths and chooses the final answer that most of them reach, a majority vote over answers (Wang et al., 2022). It rests on the intuition that a complex reasoning problem admits several ways of thinking that lead to the same correct answer (Wang et al., 2022). With 40 sampled paths it improved chain-of-thought prompting by large margins, for example by 17.9 percentage points on GSM8K, 11.0 on SVAMP, 12.2 on AQuA, 6.4 on StrategyQA and 3.9 on ARC-challenge, across four language models from 20 to 540 billion parameters (Wang et al., 2022). The share of paths that agree also works as an uncertainty estimate; the price is many model calls per question (Wang et al., 2022).

### How it works

```text
few-shot chain-of-thought prompt + question
 ▼
sample m reasoning paths (r_i, a_i) from the decoder   (e.g. m = 40, temperature sampling)
 ▼
extract final answer a_i from each path
 ▼
majority vote: argmax_a Σ_i 1(a_i = a)
 ▼
answer  (+ agreement rate as confidence)
```

#### 1. Prompting

The model is prompted exactly as in chain-of-thought prompting, with a few worked examples that show intermediate reasoning steps before the answer (Wei et al., 2022; Wang et al., 2022). Self-consistency changes only how the output is decoded, so it needs no extra training, verifier or human annotation and can be applied to off-the-shelf models (Wang et al., 2022).

#### 2. Sampling diverse reasoning paths

Instead of greedy decoding, which follows the single most probable path, the decoder samples several outputs, each consisting of a reasoning path `r_i` and a final answer `a_i` (Wang et al., 2022). The authors describe this as a "sample-and-marginalize" procedure that avoids the repetitiveness and local optimality of greedy decoding while reducing the randomness of a single sampled generation (Wang et al., 2022). In the main experiments 40 outputs were sampled per question and results were averaged over 10 runs (Wang et al., 2022). The temperature controls how diverse the paths are ([[large-language-models|large language models]]).

#### 3. Aggregating answers

The answers are assumed to come from a fixed answer set, such as a number or a multiple-choice option; the reasoning path is treated as a latent variable and marginalised out by taking the most frequent answer, `argmax_a Σ_i 1(a_i = a)` (Wang et al., 2022). Weighting each path by its probability under the model gave very similar accuracy to the unweighted majority vote, because the model assigned the generations similar probabilities, which the authors take as a sign that the model is not well calibrated ([[temperature-scaling|calibration]]; Wang et al., 2022).

#### 4. Results

Self-consistency was evaluated on arithmetic and commonsense reasoning with UL2-20B, GPT-3-175B, LaMDA-137B and PaLM-540B and improved over chain-of-thought prompting on all four models and all tasks; with PaLM-540B or GPT-3 it set new state-of-the-art results on several benchmarks at the time (Wang et al., 2022). It also beat beam search with the same number of beams and paths, because beam search produces less diverse outputs (Wang et al., 2022).

#### 5. Consistency as confidence

The share of sampled paths that agree with the final answer was highly correlated with accuracy on GSM8K, so a low agreement rate signals low confidence; in this sense self-consistency gives the model some ability to "know when it doesn't know" (Wang et al., 2022). This is related to sampling-based checks in [[hallucination-detection|hallucination detection]], which compare several answers for consistency.

#### Origin and variants

Self-consistency was introduced by Wang et al. (2022) as an extension of chain-of-thought prompting (Wei et al., 2022). It is often combined with other methods: [[react|ReAct]] falls back to chain-of-thought with self-consistency when it cannot find an answer, and the reverse fallback is used when agreement is low ([[prompt-engineering|prompt engineering]]; Yao et al., 2022).

### When to use it

- For reasoning tasks with a short, comparable final answer, such as maths word problems or multiple choice (Wang et al., 2022).
- When accuracy matters more than cost and latency, since every question needs many samples (Wang et al., 2022).
- When a confidence signal is wanted to decide whether to trust an answer or escalate it (Wang et al., 2022).

### Strengths and limitations

**Strengths**
- Large accuracy gains without training, verifiers or annotations (Wang et al., 2022).
- Works across model families and sizes (Wang et al., 2022).
- Agreement rate provides an uncertainty estimate (Wang et al., 2022).

**Limitations**
- Higher computation cost; the authors suggest starting with 5 or 10 paths, since performance usually saturates quickly (Wang et al., 2022).
- Majority voting needs answers that can be compared, which open-ended text does not provide directly (Wang et al., 2022).
- Models can still produce incorrect or nonsensical reasoning paths even when the final answer is right (Wang et al., 2022).

### Comparison

| Decoding | Paths | How the answer is chosen | Source |
|---|---|---|---|
| Greedy chain-of-thought | 1 | most probable path | Wei et al. (2022) |
| Beam search | k beams | highest-scoring beam | Wang et al. (2022) |
| Self-consistency | m samples | majority vote over answers | Wang et al. (2022) |
| [[llm-as-a-judge\|LLM-as-a-judge]] selection | m samples | a model rates the candidates | – |
| [[react\|ReAct]] + self-consistency | samples plus [[tool-calling\|tool use]] | fallback between both | Yao et al. (2022) |

Sources: Wang et al. (2022); Wei et al. (2022).

### In practice

A handful of samples, typically 5 to 10, captures most of the gain (Wang et al., 2022). Each sample is a full generation, so the method multiplies token costs ([[llm-cost-optimisation|LLM cost optimisation]]); answers have to be normalised (numbers, option letters) before voting. Agreement rates can be logged as a quality signal in evaluation and [[monitoring-and-alerting|monitoring]] ([[llm-evaluation|LLM evaluation]]).

### Key takeaway

Self-consistency samples many chain-of-thought answers and takes the majority, which makes reasoning more accurate and gives a confidence signal at the price of many model calls.

### Sources

- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A. & Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv:2203.11171. [arXiv](https://arxiv.org/abs/2203.11171)
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* arXiv:2201.11903. [arXiv](https://arxiv.org/abs/2201.11903)
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Self-Consistency ist eine Dekodierstrategie für [[chain-of-thought-prompting|Chain-of-Thought-Prompting]]: Statt nur den einen wahrscheinlichsten Lösungsweg zu nehmen, zieht sie viele unterschiedliche Lösungswege und wählt die Endantwort, zu der die meisten gelangen, also eine Mehrheitsentscheidung über die Antworten (Wang et al., 2022). Sie beruht auf der Annahme, dass ein komplexes Problem mehrere Denkwege zulässt, die zur selben richtigen Antwort führen (Wang et al., 2022). Mit 40 gezogenen Lösungswegen verbesserte sie Chain-of-Thought-Prompting deutlich, etwa um 17,9 Prozentpunkte auf GSM8K, 11,0 auf SVAMP, 12,2 auf AQuA, 6,4 auf StrategyQA und 3,9 auf ARC-Challenge, über vier Sprachmodelle mit 20 bis 540 Milliarden Parametern hinweg (Wang et al., 2022). Der Anteil übereinstimmender Wege taugt zudem als Unsicherheitsmaß; der Preis sind viele Modellaufrufe je Frage (Wang et al., 2022).

### Funktionsweise

```text
Few-Shot-Chain-of-Thought-Prompt + Frage
 ▼
m Lösungswege (r_i, a_i) aus dem Decoder ziehen   (z. B. m = 40, Temperature Sampling)
 ▼
Endantwort a_i aus jedem Weg herauslösen
 ▼
Mehrheitsentscheidung: argmax_a Σ_i 1(a_i = a)
 ▼
Antwort  (+ Übereinstimmungsrate als Konfidenz)
```

#### 1. Prompting

Das Modell wird genau wie beim Chain-of-Thought-Prompting angesprochen, mit einigen durchgerechneten Beispielen, die Zwischenschritte vor der Antwort zeigen (Wei et al., 2022; Wang et al., 2022). Self-Consistency ändert nur, wie die Ausgabe dekodiert wird; sie braucht daher weder zusätzliches Training noch einen Verifier oder menschliche Annotation und lässt sich auf fertige Modelle anwenden (Wang et al., 2022).

#### 2. Vielfältige Lösungswege ziehen

Statt Greedy Decoding, das dem einen wahrscheinlichsten Weg folgt, zieht der Decoder mehrere Ausgaben, jede bestehend aus einem Lösungsweg `r_i` und einer Endantwort `a_i` (Wang et al., 2022). Die Autorinnen und Autoren beschreiben das als „Sample-and-Marginalize“-Verfahren, das die Wiederholungen und lokalen Optima des Greedy Decoding vermeidet und zugleich den Zufall einer einzelnen gezogenen Ausgabe verringert (Wang et al., 2022). In den Hauptexperimenten wurden je Frage 40 Ausgaben gezogen und die Ergebnisse über 10 Läufe gemittelt (Wang et al., 2022). Die Temperatur steuert, wie unterschiedlich die Wege ausfallen ([[large-language-models|große Sprachmodelle]]).

#### 3. Antworten zusammenführen

Die Antworten stammen annahmegemäß aus einer festen Antwortmenge, etwa einer Zahl oder einer Antwortoption; der Lösungsweg wird als latente Variable behandelt und herausmarginalisiert, indem die häufigste Antwort gewählt wird, `argmax_a Σ_i 1(a_i = a)` (Wang et al., 2022). Jeden Weg mit seiner Wahrscheinlichkeit unter dem Modell zu gewichten, ergab fast dieselbe Genauigkeit wie die ungewichtete Mehrheitsentscheidung, weil das Modell den Ausgaben ähnliche Wahrscheinlichkeiten gab; die Autorinnen und Autoren sehen darin ein Zeichen, dass das Modell nicht gut kalibriert ist ([[temperature-scaling|Kalibrierung]]; Wang et al., 2022).

#### 4. Ergebnisse

Self-Consistency wurde auf arithmetischem und Alltagsschlussfolgern mit UL2-20B, GPT-3-175B, LaMDA-137B und PaLM-540B evaluiert und verbesserte Chain-of-Thought-Prompting bei allen vier Modellen und allen Aufgaben; mit PaLM-540B oder GPT-3 erzielte es damals neue Bestwerte auf mehreren Benchmarks (Wang et al., 2022). Es übertraf auch Beam Search mit gleich vielen Beams und Wegen, weil Beam Search weniger vielfältige Ausgaben erzeugt (Wang et al., 2022).

#### 5. Übereinstimmung als Konfidenz

Der Anteil der gezogenen Wege, die mit der Endantwort übereinstimmen, korrelierte auf GSM8K stark mit der Genauigkeit; eine niedrige Übereinstimmung zeigt also geringe Zuversicht an, und in diesem Sinn verleiht Self-Consistency dem Modell eine gewisse Fähigkeit, zu „wissen, wann es etwas nicht weiß“ (Wang et al., 2022). Das ist verwandt mit stichprobenbasierten Prüfungen in der [[hallucination-detection|Halluzinationserkennung]], die mehrere Antworten auf Übereinstimmung vergleichen.

#### Herkunft und Varianten

Self-Consistency wurde von Wang et al. (2022) als Erweiterung des Chain-of-Thought-Prompting (Wei et al., 2022) eingeführt. Es wird oft mit anderen Verfahren kombiniert: [[react|ReAct]] fällt auf Chain-of-Thought mit Self-Consistency zurück, wenn es keine Antwort findet, und der umgekehrte Rückfall greift bei geringer Übereinstimmung ([[prompt-engineering|Prompt Engineering]]; Yao et al., 2022).

### Wann einsetzen

- Für Schlussfolgerungsaufgaben mit kurzer, vergleichbarer Endantwort, etwa mathematische Textaufgaben oder Multiple Choice (Wang et al., 2022).
- Wenn Genauigkeit wichtiger ist als Kosten und Latenz, da jede Frage viele Stichproben braucht (Wang et al., 2022).
- Wenn ein Konfidenzsignal gebraucht wird, um zu entscheiden, ob einer Antwort vertraut oder sie weitergereicht wird (Wang et al., 2022).

### Stärken und Grenzen

**Stärken**
- Große Genauigkeitsgewinne ohne Training, Verifier oder Annotationen (Wang et al., 2022).
- Funktioniert über Modellfamilien und -größen hinweg (Wang et al., 2022).
- Die Übereinstimmungsrate liefert eine Unsicherheitsschätzung (Wang et al., 2022).

**Grenzen**
- Höherer Rechenaufwand; die Autorinnen und Autoren empfehlen, mit 5 oder 10 Wegen zu beginnen, da die Leistung meist schnell gesättigt ist (Wang et al., 2022).
- Die Mehrheitsentscheidung braucht vergleichbare Antworten, die offener Text nicht direkt liefert (Wang et al., 2022).
- Modelle können weiterhin falsche oder unsinnige Lösungswege erzeugen, auch wenn die Endantwort stimmt (Wang et al., 2022).

### Vergleich

| Dekodierung | Wege | Wie die Antwort gewählt wird | Quelle |
|---|---|---|---|
| Greedy Chain-of-Thought | 1 | wahrscheinlichster Weg | Wei et al. (2022) |
| Beam Search | k Beams | Beam mit dem höchsten Wert | Wang et al. (2022) |
| Self-Consistency | m Stichproben | Mehrheitsentscheidung über Antworten | Wang et al. (2022) |
| Auswahl per [[llm-as-a-judge\|LLM-as-a-Judge]] | m Stichproben | ein Modell bewertet die Kandidaten | – |
| [[react\|ReAct]] + Self-Consistency | Stichproben plus Tool-Nutzung | Rückfall zwischen beiden | Yao et al. (2022), siehe ReAct |

Quellen: Wang et al. (2022); Wei et al. (2022).

### In der Praxis

Eine Handvoll Stichproben, meist 5 bis 10, erfasst den Großteil des Gewinns (Wang et al., 2022). Jede Stichprobe ist eine vollständige Generierung, das Verfahren vervielfacht also die Token-Kosten ([[llm-cost-optimisation|LLM-Kostenoptimierung]]); Antworten müssen vor der Abstimmung vereinheitlicht werden (Zahlen, Buchstaben von Antwortoptionen). Übereinstimmungsraten lassen sich als Qualitätssignal in Evaluation und [[monitoring-and-alerting|Monitoring]] protokollieren ([[llm-evaluation|LLM-Evaluation]]).

### Merksatz

Self-Consistency zieht viele Chain-of-Thought-Antworten und nimmt die Mehrheit; das macht Schlussfolgern genauer und liefert ein Konfidenzsignal, kostet aber viele Modellaufrufe.

### Quellen

- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A. & Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv:2203.11171. [arXiv](https://arxiv.org/abs/2203.11171)
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* arXiv:2201.11903. [arXiv](https://arxiv.org/abs/2201.11903)
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)
