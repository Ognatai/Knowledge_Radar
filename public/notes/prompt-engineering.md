---
title_en: Prompt Engineering
title_de: Prompt Engineering
entity_type: Method
sources:
- https://arxiv.org/abs/2005.14165
- https://arxiv.org/abs/2201.11903
- https://arxiv.org/abs/2205.11916
- https://arxiv.org/abs/2203.11171
- https://arxiv.org/abs/2406.06608
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Prompt engineering designs the input text so that a large language model performs a task without any change to its weights. Instructions alone (zero-shot), a few demonstrations (few-shot), demonstrations with intermediate reasoning steps (chain of thought) and voting over several sampled reasoning paths (self-consistency) can substantially improve results, especially on reasoning tasks (Brown et al., 2020; Wei et al., 2022; Wang et al., 2022).

### How it works

The model's behaviour is steered only through the prompt. A task description, optional demonstrations and optional reasoning cues are placed in the input, the model continues the text, and for self-consistency several continuations are sampled and their answers aggregated. Surveys collect these techniques into a common vocabulary ([[prompt-comparison|Prompt Comparison]] covers how to compare variants).

```text
1. Zero-shot: instruction only
▼
2. Few-shot: instruction plus demonstrations
▼
3. Chain of thought: demonstrations with reasoning steps
▼
4. Self-consistency: several reasoning paths, majority answer
▼
5. Taxonomy of prompting techniques
```

#### 1. Zero-shot prompting

A zero-shot prompt contains only the task instruction and the input. Kojima et al. (2022) showed that simply adding "Let's think step by step" before the answer makes large models produce reasoning steps without any demonstrations (zero-shot chain of thought). With text-davinci-002, this raised accuracy on MultiArith from 17.7% to 78.7% and on GSM8K from 10.4% to 40.7% (Kojima et al., 2022).

#### 2. Few-shot prompting

A few-shot prompt adds a small number of input-output demonstrations before the new input, and the model infers the task from them in context, without gradient updates or fine-tuning (Brown et al., 2020). GPT-3 with 175 billion parameters achieved strong performance this way on many NLP tasks, including translation and question answering, but still struggled on some data sets (Brown et al., 2020). Which and how many demonstrations are used is part of the prompt design.

#### 3. Chain-of-thought prompting

Chain-of-thought prompting uses demonstrations that contain a series of intermediate reasoning steps before the answer, so the model also generates such steps (Wei et al., 2022). This improved performance on arithmetic, commonsense and symbolic reasoning in sufficiently large models; with only eight chain-of-thought demonstrations, a 540B-parameter model reached state-of-the-art accuracy on the GSM8K math word problems, surpassing even fine-tuned GPT-3 with a verifier (Wei et al., 2022).

#### 4. Self-consistency

Self-consistency replaces greedy decoding in chain-of-thought prompting: it samples a diverse set of reasoning paths and selects the most consistent answer, that is, the answer most paths arrive at (Wang et al., 2022). The idea is that a complex problem usually allows several ways of reasoning that lead to the same correct answer. Self-consistency improved chain-of-thought results on GSM8K by 17.9%, on SVAMP by 11.0% and on AQuA by 12.2%, at the cost of generating several outputs per question (Wang et al., 2022).

#### 5. Taxonomy of prompting techniques

The Prompt Report (Schulhoff et al., 2024) assembles a vocabulary of 33 terms and a taxonomy of 58 text-based prompting techniques, together with best practices and guidelines for prompting state-of-the-art models. Such taxonomies make it easier to describe which technique a prompt uses and to compare prompts systematically.

#### Origin and variants

In-context learning from a few demonstrations was popularised by GPT-3 (Brown et al., 2020). Chain-of-thought prompting (Wei et al., 2022), its zero-shot variant (Kojima et al., 2022) and self-consistency (Wang et al., 2022) followed in 2022, and the Prompt Report (Schulhoff et al., 2024) systematised the field.

### When to use it

- When a task can be described in text and no labelled training data or fine-tuning budget is available (Brown et al., 2020).
- When a task requires multi-step reasoning, such as arithmetic word problems, where chain-of-thought or zero-shot chain-of-thought prompting helps (Wei et al., 2022; Kojima et al., 2022).
- When accuracy on reasoning tasks matters more than generation cost, so that several sampled reasoning paths can be combined with self-consistency (Wang et al., 2022).

### Strengths and limitations

**Strengths**
- Adapts a model to a new task without training or changing its weights (Brown et al., 2020).
- Simple prompt changes can bring large gains on reasoning tasks, such as GSM8K accuracy rising from 10.4% to 40.7% with zero-shot chain of thought (Kojima et al., 2022).
- Self-consistency improves accuracy further without additional training (Wang et al., 2022).

**Limitations**
- Few-shot learning still struggles on some data sets, and some evaluations face methodological issues from training on large web corpora (Brown et al., 2020).
- Chain-of-thought prompting brings its gains mainly in sufficiently large models (Wei et al., 2022).
- Self-consistency multiplies generation cost because several reasoning paths are sampled per input (Wang et al., 2022).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Zero-shot prompting | Instruction only; zero-shot chain of thought adds a reasoning cue (Kojima et al., 2022) | Quick use without demonstrations |
| Few-shot prompting | Adds demonstrations; the model learns the task in context (Brown et al., 2020) | Tasks whose format is easier to show than to describe |
| Chain of thought with self-consistency | Demonstrations with reasoning steps; several sampled paths and a majority answer (Wei et al., 2022; Wang et al., 2022) | Multi-step reasoning where accuracy justifies extra cost |
| Fine-tuning ([[llm-adaptation|LLM Adaptation]]) | Changes the model's weights with task-specific training data | Tasks with enough training data and stable requirements |

### In practice

Prompt variants are compared on a fixed evaluation set before one is chosen, since small wording and format changes can change results ([[prompt-comparison|Prompt Comparison]], [[llm-evaluation|LLM Evaluation]]). Reasoning cues and demonstrations with intermediate steps are added where tasks need several steps (Wei et al., 2022; Kojima et al., 2022), and self-consistency is used where the extra generation cost is acceptable (Wang et al., 2022).

### Key takeaway

Prompt engineering steers a model through its input alone, and instructions, demonstrations, reasoning steps and answer voting can substantially improve results without any training.

### Sources

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* NeurIPS 2022. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Kojima, T. et al. (2022). *Large Language Models are Zero-Shot Reasoners.* NeurIPS 2022. [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Schulhoff, S. et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* [arXiv:2406.06608](https://arxiv.org/abs/2406.06608)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Prompt-Engineering gestaltet den Eingabetext so, dass ein großes Sprachmodell eine Aufgabe ausführt, ohne dass sich seine Gewichte ändern. Reine Anweisungen (Zero-Shot), einige Demonstrationsbeispiele (Few-Shot), Demonstrationen mit Zwischenschritten des Schließens (Chain of Thought) und die Abstimmung über mehrere gesampelte Lösungswege (Self-Consistency) können die Ergebnisse erheblich verbessern, insbesondere bei Aufgaben, die logisches Denken erfordern (Brown et al., 2020; Wei et al., 2022; Wang et al., 2022).

### Funktionsweise

Das Verhalten des Modells wird ausschließlich durch den Prompt gesteuert. Eine Aufgabenbeschreibung, optionale Demonstrationsbeispiele und optionale Hinweise zum schrittweisen Schließen stehen in der Eingabe, das Modell setzt den Text fort, und für Self-Consistency werden mehrere Fortsetzungen gesampelt und ihre Antworten zusammengeführt. Überblicksarbeiten fassen diese Techniken in einem gemeinsamen Vokabular zusammen ([[prompt-comparison|Prompt Comparison]] behandelt, wie Varianten verglichen werden).

```text
1. Zero-shot: nur Anweisung
▼
2. Few-shot: Anweisung plus Demonstrationsbeispiele
▼
3. Chain of Thought: Demonstrationen mit Zwischenschritten
▼
4. Self-Consistency: mehrere Lösungswege, Mehrheitsantwort
▼
5. Taxonomie der Prompting-Techniken
```

#### 1. Zero-Shot-Prompting

Ein Zero-Shot-Prompt enthält nur die Aufgabenanweisung und die Eingabe. Kojima et al. (2022) zeigten, dass das Hinzufügen von „Let's think step by step“ vor der Antwort dazu führt, dass große Modelle Zwischenschritte erzeugen, ohne dass Beispiele gezeigt werden (Zero-Shot-Chain-of-Thought). Mit text-davinci-002 stieg die Genauigkeit bei MultiArith von 17,7 % auf 78,7 % und bei GSM8K von 10,4 % auf 40,7 % (Kojima et al., 2022).

#### 2. Few-Shot-Prompting

Ein Few-Shot-Prompt fügt vor der neuen Eingabe einige wenige Eingabe-Ausgabe-Beispiele hinzu, und das Modell schließt aus diesen Beispielen im Kontext die Aufgabe, ohne Gradienten-Updates oder Fine-Tuning (Brown et al., 2020). GPT-3 mit 175 Milliarden Parametern erzielte auf diese Weise starke Leistungen bei vielen NLP-Aufgaben, einschließlich Übersetzung und Fragebeantwortung, stieß jedoch immer noch auf Schwierigkeiten bei einigen Datensätzen (Brown et al., 2020). Welche und wie viele Beispiele verwendet werden, ist Teil des Prompt-Designs.

#### 3. Chain-of-Thought-Prompting

Chain-of-Thought-Prompting verwendet Demonstrationen, die vor der Antwort eine Reihe von Zwischenschritten enthalten, sodass das Modell ebenfalls solche Schritte generiert (Wei et al., 2022). Dies verbesserte die Leistung beim arithmetischen, alltagsweltlichen und symbolischen Schließen in hinreichend großen Modellen; mit nur acht Chain-of-Thought-Demonstrationen erreichte ein Modell mit 540 Milliarden Parametern den Stand der Technik bei den mathematischen Textaufgaben von GSM8K und übertraf sogar das mit einem Verifier feinabgestimmte GPT-3 (Wei et al., 2022).

#### 4. Self-Consistency

Self-Consistency ersetzt beim Chain-of-Thought-Prompting die Greedy-Decodierung: Es erzeugt eine vielfältige Menge an Lösungswegen und wählt die konsistenteste Antwort aus, also die Antwort, zu der die meisten Pfade führen (Wang et al., 2022). Die Idee ist, dass ein komplexes Problem in der Regel mehrere Lösungswege erlaubt, die zu derselben richtigen Antwort führen. Self-Consistency verbesserte die Chain-of-Thought-Ergebnisse auf GSM8K um 17,9 %, auf SVAMP um 11,0 % und auf AQuA um 12,2 %, allerdings zum Preis der Generierung mehrerer Ausgaben pro Frage (Wang et al., 2022).

#### 5. Taxonomie von Prompting-Techniken

Der Prompt Report (Schulhoff et al., 2024) stellt ein Vokabular von 33 Begriffen und eine Taxonomie von 58 textbasierten Prompting-Techniken zusammen, dazu Best Practices und Richtlinien für das Prompten modernster Modelle. Solche Taxonomien erleichtern es, zu beschreiben, welche Technik ein Prompt verwendet, und ermöglichen eine systematische Vergleichbarkeit von Prompts.

#### Ursprung und Varianten

In-Context Learning mit wenigen Demonstrationsbeispielen wurde durch GPT-3 (Brown et al., 2020) bekannt. Chain-of-Thought-Prompting (Wei et al., 2022), seine Zero-Shot-Variante (Kojima et al., 2022) und Self-Consistency (Wang et al., 2022) folgten 2022, und der Prompt Report (Schulhoff et al., 2024) systematisierte das Feld.

### Wann einsetzen

- Wenn eine Aufgabe in Text beschrieben werden kann und keine annotierten Trainingsdaten oder ein Budget für das Fine-Tuning vorliegen (Brown et al., 2020).
- Wenn eine Aufgabe mehrschrittiges Denken erfordert, wie z. B. arithmetische Wortprobleme, bei denen Chain-of-Thought- oder Zero-Shot-Chain-of-Thought-Prompting hilft (Wei et al., 2022; Kojima et al., 2022).
- Wenn die Genauigkeit bei Aufgaben mit mehrschrittigem Schließen wichtiger ist als der Generierungsaufwand, sodass mehrere gesampelte Lösungswege mit Self-Consistency kombiniert werden können (Wang et al., 2022).

### Stärken und Grenzen

**Stärken**
- Passt ein Modell an eine neue Aufgabe an, ohne Training oder Änderung seiner Gewichte (Brown et al., 2020).
- Einfache Änderungen des Prompts können große Verbesserungen bei Aufgaben mit mehrschrittigem Schließen bringen, z. B. steigt die Genauigkeit bei GSM8K von 10,4 % auf 40,7 % durch Zero-Shot-Chain-of-Thought (Kojima et al., 2022).
- Self-Consistency verbessert die Genauigkeit weiter, ohne zusätzliches Training (Wang et al., 2022).

**Einschränkungen**
- Few-Shot-Learning hat weiterhin Schwierigkeiten bei einigen Datensätzen, und einige Evaluierungen stoßen auf methodische Probleme durch das Training auf großen Web-Korpora (Brown et al., 2020).
- Chain-of-Thought-Prompting bringt seine Verbesserungen hauptsächlich bei ausreichend großen Modellen (Wei et al., 2022).
- Self-Consistency vervielfacht den Generierungsaufwand, da pro Eingabe mehrere Lösungswege erzeugt werden (Wang et al., 2022).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Zero-Shot-Prompting | Nur Anweisung; Zero-Shot-Chain-of-Thought fügt einen Hinweis zum schrittweisen Vorgehen hinzu (Kojima et al., 2022) | Schnelle Verwendung ohne Beispiele |
| Few-Shot-Prompting | Fügt Beispiele hinzu; das Modell lernt die Aufgabe im Kontext (Brown et al., 2020) | Aufgaben, deren Format leichter zu zeigen als zu beschreiben ist |
| Chain of Thought mit Self-Consistency | Beispiele mit Zwischenschritten; mehrere gesampelte Lösungswege und eine Mehrheitsantwort (Wei et al., 2022; Wang et al., 2022) | Mehrschrittiges Schließen, wenn die Genauigkeit den zusätzlichen Aufwand rechtfertigt |
| Fine-Tuning ([[llm-adaptation|LLM Adaptation]]) | Ändert die Modellgewichte mit aufgabenbezogenen Trainingsdaten | Aufgaben mit genügend Trainingsdaten und stabilen Anforderungen |

### In der Praxis

Promptvarianten werden auf einem festen Evaluierungssatz verglichen, bevor eine ausgewählt wird, da kleine Änderungen im Wortlaut und Format die Ergebnisse verändern können ([[prompt-comparison|Prompt Comparison]], [[llm-evaluation|LLM Evaluation]]). Bei Aufgaben, die mehrere Schritte erfordern, werden Hinweise zum schrittweisen Vorgehen und Demonstrationen mit Zwischenschritten hinzugefügt (Wei et al., 2022; Kojima et al., 2022), und Self-Consistency wird dort verwendet, wo der zusätzliche Generierungsaufwand akzeptabel ist (Wang et al., 2022).

### Merksatz

Prompt Engineering steuert ein Modell allein über die Eingabe, und Anweisungen, Demonstrationen, Zwischenschritte und die Abstimmung über Antworten können die Ergebnisse ohne jedes Training erheblich verbessern.

### Quellen

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* NeurIPS 2022. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Kojima, T. et al. (2022). *Large Language Models are Zero-Shot Reasoners.* NeurIPS 2022. [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Schulhoff, S. et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* [arXiv:2406.06608](https://arxiv.org/abs/2406.06608)
