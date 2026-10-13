---
title_en: Chain-of-thought prompting
title_de: Chain-of-Thought-Prompting
entity_type: Method
aliases:
- Chain of thought
- CoT prompting
sources:
- https://arxiv.org/abs/2201.11903
- https://arxiv.org/abs/2205.11916
- https://arxiv.org/abs/2203.11171
- https://arxiv.org/abs/2305.04388
- https://arxiv.org/abs/2303.16634
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
Chain-of-thought prompting makes a language model write out a series of intermediate reasoning steps before its answer, either by showing worked examples in the prompt or by an instruction such as "Let's think step by step" (Wei et al., 2022; Kojima et al., 2022). It substantially improves large models on arithmetic, commonsense and symbolic reasoning, but the written reasoning is not guaranteed to be correct, nor to be the actual reason for the answer (Wei et al., 2022; Turpin et al., 2023).

### How it works

```text
Standard prompt:   Q → A
Chain of thought:  Q → step 1 → step 2 → … → A

Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls.
   How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11.
   The answer is 11.            (example from Wei et al., 2022)
```

#### 1. Few-shot chain of thought
The prompt contains a few exemplars, each consisting of a question, a chain of thought and the answer; the model then produces a chain of thought for the new question as well. Wei et al. (2022) used one set of eight such exemplars for all math word problem benchmarks. The method needs no fine-tuning, lets the model spend more computation on problems that need more steps, and is in principle applicable to any task that humans can solve via language (Wei et al., 2022).

#### 2. Zero-shot chain of thought
Kojima et al. (2022) showed that no exemplars are needed: adding "Let's think step by step" before the answer makes large models reason step by step. Their method uses two prompts, a first one that extracts the reasoning and a second one that extracts the final answer from it. With the same prompt for all tasks, accuracy of [[llm-alignment|InstructGPT]] (text-davinci-002) rose from 17.7% to 78.7% on MultiArith and from 10.4% to 40.7% on GSM8K.

#### 3. Self-consistency
Instead of taking the single most likely chain of thought, self-consistency samples several diverse reasoning paths and returns the answer most of them reach, marginalising out the paths. This improved chain-of-thought results on GSM8K by 17.9 percentage points, on SVAMP by 11.0 and on AQuA by 12.2 (Wang et al., 2022).

#### 4. Chain of thought as part of other methods
Evaluation and debiasing use it as a building block: the judge G-Eval first generates evaluation steps with chain-of-thought prompting and then fills in an evaluation form (Liu et al., 2023; [[llm-as-a-judge|LLM-as-a-Judge]]). Urchs (2025) describes causal front-door adjustment, which routes an intervention through intermediate variables such as chain-of-thought prompts, as one strategy for mitigating bias in language models ([[causal-inference|Causal Inference]]).

#### Origin and variants
Wei et al. (2022) introduced chain-of-thought prompting with worked exemplars; Kojima et al. (2022) showed the zero-shot variant, and Wang et al. (2022) added self-consistency. Chain-of-thought prompting is one of the techniques of [[prompt-engineering|prompt engineering]].

### When to use it
- Multi-step problems: arithmetic word problems, commonsense and symbolic reasoning (Wei et al., 2022).
- With large models: the benefit appeared only at around 100B parameters in the original experiments (Wei et al., 2022).
- When a single answer is unreliable and sampling several times is affordable: self-consistency (Wang et al., 2022).
- When a model has to judge or grade outputs step by step (Liu et al., 2023).

### Strengths and limitations

**Strengths**
- No training: a few exemplars or a single instruction suffice (Wei et al., 2022; Kojima et al., 2022).
- With eight exemplars, PaLM 540B reached state-of-the-art accuracy on GSM8K, surpassing a fine-tuned GPT-3 with a verifier (Wei et al., 2022).
- The written steps offer an interpretable window into how the model may have reached an answer and where it went wrong (Wei et al., 2022).
- Results did not depend on the linguistic style of the exemplars: chains written by different annotators all outperformed standard prompting (Wei et al., 2022).

**Limitations**
- Whether the model is actually "reasoning" is an open question; chains of thought only emulate human reasoning (Wei et al., 2022).
- There is no guarantee that the reasoning path is correct, and generated chains of thought are not always factual (Wei et al., 2022).
- Small models do not benefit: the gains appeared only with models of around 100B parameters, which makes the method costly to serve (Wei et al., 2022).
- Explanations can be unfaithful: when models were biased towards an answer, for instance by reordering answer options, their chains of thought rationalised it without mentioning the bias, and accuracy dropped by up to 36% on 13 BIG-Bench Hard tasks (Turpin et al., 2023; [[explainable-ai|Explainable AI]]).
- Longer outputs and, with self-consistency, several samples per question increase cost and latency ([[llm-cost-optimization|LLM Cost Optimization]]).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| Standard few-shot prompting | Exemplars show only question and answer (Wei et al., 2022) | Tasks without multi-step reasoning |
| Few-shot chain of thought | Exemplars include the reasoning steps (Wei et al., 2022) | Multi-step reasoning with a few hand-written exemplars |
| Zero-shot chain of thought | One instruction, "Let's think step by step", no exemplars (Kojima et al., 2022) | Quick use across many tasks |
| Self-consistency | Samples several chains of thought and takes the majority answer (Wang et al., 2022) | Accuracy-critical reasoning when extra calls are affordable |

### In practice
Chain-of-thought prompting is usually combined with the other techniques of [[prompt-engineering|Prompt Engineering]] and compared on a test set before it is adopted ([[prompt-comparison|Prompt Comparison]]). The reasoning should not be read as an explanation of the model's decision: it can be fluent and plausible while leaving out what actually drove the answer (Turpin et al., 2023). Answers derived from a chain of thought still need checking against sources or a reference ([[hallucination-detection|Hallucination Detection]]).

### Key takeaway
Asking a large model to write out its intermediate steps makes it better at multi-step problems, but the steps are a generated text, not a reliable record of how the answer came about.

### Sources
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* NeurIPS 2022. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Kojima, T. et al. (2022). *Large Language Models are Zero-Shot Reasoners.* NeurIPS 2022. [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Turpin, M. et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* NeurIPS 2023. [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment.* EMNLP 2023. [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Chain-of-Thought-Prompting bringt ein Sprachmodell dazu, vor seiner Antwort eine Folge von Zwischenschritten auszuschreiben, entweder durch durchgerechnete Beispiele im Prompt oder durch eine Anweisung wie „Let's think step by step“ (Wei et al., 2022; Kojima et al., 2022). Große Modelle werden dadurch deutlich besser bei arithmetischem, alltagslogischem und symbolischem Schließen; die ausgeschriebene Begründung ist aber weder sicher richtig noch sicher der tatsächliche Grund für die Antwort (Wei et al., 2022; Turpin et al., 2023).

### Funktionsweise

```text
Standard-Prompt:   F → A
Chain of Thought:  F → Schritt 1 → Schritt 2 → … → A

F: Roger hat 5 Tennisbälle. Er kauft 2 weitere Dosen Tennisbälle mit je 3 Bällen.
   Wie viele Tennisbälle hat er jetzt?
A: Roger hatte 5 Bälle. 2 Dosen mit je 3 Tennisbällen sind 6 Tennisbälle. 5 + 6 = 11.
   Die Antwort ist 11.          (Beispiel aus Wei et al., 2022)
```

#### 1. Few-Shot-Chain-of-Thought
Der Prompt enthält einige Beispiele, jeweils aus Frage, Gedankenkette und Antwort; das Modell erzeugt dann auch für die neue Frage eine Gedankenkette. Wei et al. (2022) verwendeten einen Satz aus acht solchen Beispielen für alle Benchmarks mit Textaufgaben. Die Methode braucht kein Fine-Tuning, lässt das Modell mehr Rechenaufwand auf Aufgaben mit mehr Schritten verwenden und ist im Prinzip auf jede Aufgabe anwendbar, die Menschen sprachlich lösen können (Wei et al., 2022).

#### 2. Zero-Shot-Chain-of-Thought
Kojima et al. (2022) zeigten, dass es keine Beispiele braucht: Der Zusatz „Let's think step by step“ vor der Antwort bringt große Modelle dazu, schrittweise zu schließen. Ihre Methode nutzt zwei Prompts, einen ersten, der die Begründung erzeugt, und einen zweiten, der daraus die endgültige Antwort entnimmt. Mit demselben Prompt für alle Aufgaben stieg die Genauigkeit von [[llm-alignment|InstructGPT]] (text-davinci-002) auf MultiArith von 17,7 % auf 78,7 % und auf GSM8K von 10,4 % auf 40,7 %.

#### 3. Self-Consistency
Statt der einzelnen wahrscheinlichsten Gedankenkette zieht Self-Consistency mehrere unterschiedliche Lösungswege und gibt die Antwort zurück, zu der die meisten gelangen; die Lösungswege werden dabei herausgemittelt. Das verbesserte die Chain-of-Thought-Ergebnisse auf GSM8K um 17,9 Prozentpunkte, auf SVAMP um 11,0 und auf AQuA um 12,2 (Wang et al., 2022).

#### 4. Chain of Thought als Baustein anderer Methoden
Evaluation und Bias-Minderung nutzen sie als Baustein: Der Bewerter G-Eval erzeugt zunächst Bewertungsschritte per Chain-of-Thought-Prompting und füllt dann ein Bewertungsformular aus (Liu et al., 2023; [[llm-as-a-judge|LLM-as-a-Judge]]). Urchs (2025) beschreibt die kausale Front-Door-Adjustierung, die eine Intervention über Zwischenvariablen wie Chain-of-Thought-Prompts leitet, als eine Strategie zur Minderung von Bias in Sprachmodellen ([[causal-inference|Kausale Inferenz]]).

#### Ursprung und Varianten
Wei et al. (2022) führten Chain-of-Thought-Prompting mit durchgerechneten Beispielen ein; Kojima et al. (2022) zeigten die Zero-Shot-Variante, und Wang et al. (2022) ergänzten Self-Consistency. Chain-of-Thought-Prompting ist eine der Techniken des [[prompt-engineering|Prompt Engineering]].

### Wann einsetzen
- Mehrschrittige Aufgaben: Textaufgaben mit Rechnungen, alltagslogisches und symbolisches Schließen (Wei et al., 2022).
- Mit großen Modellen: In den ursprünglichen Experimenten zeigte sich der Nutzen erst ab etwa 100 Mrd. Parametern (Wei et al., 2022).
- Wenn eine einzelne Antwort unzuverlässig ist und mehrfaches Sampeln bezahlbar ist: Self-Consistency (Wang et al., 2022).
- Wenn ein Modell Ausgaben schrittweise bewerten oder benoten soll (Liu et al., 2023).

### Stärken und Grenzen

**Stärken**
- Kein Training: Einige Beispiele oder eine einzige Anweisung genügen (Wei et al., 2022; Kojima et al., 2022).
- Mit acht Beispielen erreichte PaLM 540B auf GSM8K den Stand der Technik und übertraf ein feinjustiertes GPT-3 mit Verifier (Wei et al., 2022).
- Die ausgeschriebenen Schritte geben einen interpretierbaren Einblick, wie das Modell zu einer Antwort gekommen sein könnte und wo es falsch abgebogen ist (Wei et al., 2022).
- Die Ergebnisse hingen nicht vom sprachlichen Stil der Beispiele ab: Von verschiedenen Annotierenden geschriebene Ketten übertrafen alle das Standard-Prompting (Wei et al., 2022).

**Grenzen**
- Ob das Modell tatsächlich „schließt“, ist eine offene Frage; Gedankenketten ahmen menschliches Schließen nur nach (Wei et al., 2022).
- Es gibt keine Garantie, dass der Lösungsweg richtig ist, und erzeugte Gedankenketten sind nicht immer faktisch korrekt (Wei et al., 2022).
- Kleine Modelle profitieren nicht: Die Gewinne zeigten sich erst bei Modellen mit etwa 100 Mrd. Parametern, was den Betrieb teuer macht (Wei et al., 2022).
- Begründungen können unzutreffend sein: Waren Modelle auf eine Antwort hin verzerrt, etwa durch umsortierte Antwortoptionen, rationalisierten ihre Gedankenketten diese, ohne die Verzerrung zu erwähnen, und die Genauigkeit sank auf 13 BIG-Bench-Hard-Aufgaben um bis zu 36 % (Turpin et al., 2023; [[explainable-ai|Erklärbare KI]]).
- Längere Ausgaben und bei Self-Consistency mehrere Samples pro Frage erhöhen Kosten und Latenz ([[llm-cost-optimization|LLM-Kostenoptimierung]]).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Standard-Few-Shot-Prompting | Beispiele zeigen nur Frage und Antwort (Wei et al., 2022) | Aufgaben ohne mehrschrittiges Schließen |
| Few-Shot-Chain-of-Thought | Beispiele enthalten die Lösungsschritte (Wei et al., 2022) | Mehrschrittiges Schließen mit einigen handgeschriebenen Beispielen |
| Zero-Shot-Chain-of-Thought | Eine Anweisung, „Let's think step by step“, keine Beispiele (Kojima et al., 2022) | Schneller Einsatz über viele Aufgaben |
| Self-Consistency | Zieht mehrere Gedankenketten und nimmt die Mehrheitsantwort (Wang et al., 2022) | Genauigkeitskritisches Schließen, wenn zusätzliche Aufrufe bezahlbar sind |

### In der Praxis
Chain-of-Thought-Prompting wird meist mit den anderen Techniken des [[prompt-engineering|Prompt Engineering]] kombiniert und vor dem Einsatz auf einer Testmenge verglichen ([[prompt-comparison|Prompt-Vergleich]]). Die Begründung sollte nicht als Erklärung der Modellentscheidung gelesen werden: Sie kann flüssig und plausibel sein und dennoch auslassen, was die Antwort tatsächlich bestimmt hat (Turpin et al., 2023). Aus einer Gedankenkette abgeleitete Antworten müssen weiterhin gegen Quellen oder eine Referenz geprüft werden ([[hallucination-detection|Halluzinationserkennung]]).

### Merksatz
Wer ein großes Modell seine Zwischenschritte ausschreiben lässt, macht es besser bei mehrschrittigen Aufgaben; die Schritte sind aber erzeugter Text, kein verlässliches Protokoll, wie die Antwort zustande kam.

### Quellen
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* NeurIPS 2022. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Kojima, T. et al. (2022). *Large Language Models are Zero-Shot Reasoners.* NeurIPS 2022. [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Turpin, M. et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* NeurIPS 2023. [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment.* EMNLP 2023. [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
