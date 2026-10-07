---
title_en: Prompt Comparison
title_de: Prompt-Vergleiche
entity_type: Method
sources:
- https://arxiv.org/abs/2310.11324
- https://arxiv.org/abs/2401.00595
- https://arxiv.org/abs/2406.06608
- https://arxiv.org/abs/2306.05685
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Prompt comparison evaluates several prompt variants on the same fixed set of inputs to find out whether a change really improves results. This matters because language models are highly sensitive to meaning-preserving changes in format and wording: formatting alone changed accuracy by up to 76 points in one study, and model rankings shift depending on which instruction paraphrase is used (Sclar et al., 2023; Mizrahi et al., 2023).

### How it works

Variants of a prompt are defined, each is run on the same evaluation inputs, and the outputs are scored, by reference answers, human raters or a strong LLM as judge. Because single prompts give brittle results, the comparison reports the spread of performance across variants rather than a single number.

```text
1. Define what is varied
▼
2. Account for formatting sensitivity
▼
3. Evaluate several instruction paraphrases
▼
4. Score the outputs, for instance with an LLM judge
```

#### 1. What can be varied

A prompt combines several components, such as instructions, demonstrations, output format and reasoning cues, and each can be varied. The Prompt Report provides a vocabulary of 33 terms and a taxonomy of 58 text-based prompting techniques that helps name what exactly differs between two variants (Schulhoff et al., 2024). A clean comparison changes one component at a time so that a difference in results can be attributed to it.

#### 2. Sensitivity to formatting

Sclar et al. (2023) found that several widely used open models are extremely sensitive to subtle, meaning-preserving changes in prompt formatting in few-shot settings, with performance differences of up to 76 accuracy points for LLaMA-2-13B. Sensitivity remained when model size, the number of few-shot examples or instruction tuning changed. Their method FormatSpread quickly evaluates a sampled set of plausible prompt formats for a task and reports the interval of expected performance, without access to model weights (Sclar et al., 2023).

#### 3. Several instruction paraphrases

Mizrahi et al. (2023) analysed the brittleness of single-prompt evaluations across 6.5 million instances, 20 different LLMs and 39 tasks and found that results and model rankings depend strongly on the chosen instruction. They propose evaluating with a diverse set of instruction paraphrases and choosing metrics that suit the use case, for instance different metrics for LLM developers comparing models and for developers choosing a prompt for a downstream task.

#### 4. Scoring the variants

For open-ended outputs, strong LLMs can serve as judges ([[llm-as-a-judge|LLM-as-a-Judge]]): GPT-4 as judge agreed with both controlled and crowdsourced human preferences in over 80% of cases, the same level of agreement as between humans (Zheng et al., 2023). Judges show known biases, namely position bias, verbosity bias and self-enhancement bias, the tendency to favour answers from the judge's own model, and limited reasoning ability; Zheng et al. (2023) propose solutions to mitigate some of them. When prompt variants lead to answers of different length or style, these biases can affect the comparison.

#### Origin and variants

Systematic prompt comparison builds on findings that LLM evaluation is sensitive to prompt formatting (Sclar et al., 2023) and to instruction wording (Mizrahi et al., 2023), on LLM judges for open-ended answers (Zheng et al., 2023) and on taxonomies of prompting techniques (Schulhoff et al., 2024).

### When to use it

- When deciding whether a new prompt version should replace the current one in an application.
- When comparing models, since a single prompt format can produce misleading differences between models (Sclar et al., 2023; Mizrahi et al., 2023).
- When reporting evaluation results, which are more reliable as a range over plausible formats or paraphrases than as a single score (Sclar et al., 2023).

### Strengths and limitations

**Strengths**
- Reveals how much results depend on formatting and wording instead of hiding it behind a single score (Sclar et al., 2023).
- Multi-prompt evaluation gives more robust model rankings than single-prompt evaluation (Mizrahi et al., 2023).
- LLM judges make it affordable to score many variants on open-ended tasks (Zheng et al., 2023).

**Limitations**
- Evaluating many variants multiplies the cost of evaluation (Mizrahi et al., 2023).
- LLM judges have position, verbosity and self-enhancement biases that can distort comparisons (Zheng et al., 2023).
- The space of possible variants is large, so only a sample of formats or paraphrases can be tested (Sclar et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Single-prompt evaluation | One fixed prompt per task; results can change with meaning-preserving variations (Mizrahi et al., 2023) | Quick checks where the prompt is fixed |
| Format sampling (FormatSpread) | Samples plausible formats and reports a performance interval (Sclar et al., 2023) | Measuring sensitivity to formatting and comparing models fairly |
| Multi-prompt evaluation | Evaluates several instruction paraphrases with use-case-specific metrics (Mizrahi et al., 2023) | Robust model comparisons and prompt selection |

### In practice

Prompt variants are compared on a fixed evaluation set with the same inputs for every variant, ideally changing one component at a time ([[llm-evaluation|LLM Evaluation]], [[model-comparison|Model Comparison]]). Results are reported as ranges across formats or paraphrases rather than single values (Sclar et al., 2023; Mizrahi et al., 2023). Where an LLM judge scores the outputs, answer order is randomised or both orders are evaluated to limit position bias (Zheng et al., 2023).

### Key takeaway

Because small, meaning-preserving prompt changes can shift results substantially, prompts are compared on fixed inputs across several variants and reported as ranges.

### Sources

- Sclar, M. et al. (2023). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting.* ICLR 2024. [arXiv:2310.11324](https://arxiv.org/abs/2310.11324)
- Mizrahi, M. et al. (2023). *State of What Art? A Call for Multi-Prompt LLM Evaluation.* TACL. [arXiv:2401.00595](https://arxiv.org/abs/2401.00595)
- Schulhoff, S. et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* [arXiv:2406.06608](https://arxiv.org/abs/2406.06608)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Prompt-Vergleich bewertet mehrere Prompt-Varianten auf demselben festen Satz von Eingaben, um festzustellen, ob eine Änderung tatsächlich die Ergebnisse verbessert. Dies ist wichtig, da Sprachmodelle sehr empfindlich auf bedeutungserhaltende Änderungen im Format und in der Formulierung reagieren: allein das Format änderte die Genauigkeit in einer Studie um bis zu 76 Punkte, und Modellranglisten verschieben sich je nach verwendeter Anweisungsparaphrase (Sclar et al., 2023; Mizrahi et al., 2023).

### Funktionsweise

Varianten eines Prompts werden definiert, jede wird auf denselben Evaluierungseingaben ausgeführt, und die Ausgaben werden bewertet, anhand von Referenzantworten, durch menschliche Bewertende oder durch ein starkes LLM als Judge. Da einzelne Prompts fragile Ergebnisse liefern, berichtet der Vergleich die Streuung der Leistung über die Varianten statt einer einzelnen Zahl.

```text
1. Festlegen, was variiert wird
▼
2. Empfindlichkeit gegenüber Formatierung berücksichtigen
▼
3. Mehrere Paraphrasen der Anweisung evaluieren
▼
4. Ausgaben bewerten, etwa mit einem LLM als Judge
```

#### 1. Was kann variiert werden

Ein Prompt kombiniert mehrere Komponenten, wie Anweisungen, Demonstrationsbeispiele, Ausgabeformat und Hinweise zum schrittweisen Vorgehen, und jede davon kann variiert werden. Der Prompt Report bietet ein Vokabular von 33 Begriffen und eine Taxonomie von 58 textbasierten Prompting-Techniken, die helfen, zu benennen, was sich genau zwischen zwei Varianten unterscheidet (Schulhoff et al., 2024). Ein sauberer Vergleich ändert jeweils nur eine Komponente, damit sich ein Unterschied in den Ergebnissen darauf zurückführen lässt.

#### 2. Empfindlichkeit gegenüber Formatierung

Sclar et al. (2023) fanden heraus, dass mehrere weit verbreitete offene Modelle extrem empfindlich auf subtile, bedeutungserhaltende Änderungen der Prompt-Formatierung in Few-Shot-Szenarien reagieren, wobei Leistungsunterschiede von bis zu 76 Genauigkeitspunkten für LLaMA-2-13B auftreten. Die Empfindlichkeit blieb bestehen, wenn die Modellgröße, die Anzahl der Few-Shot-Beispiele oder das Instruction Tuning verändert wurden. Ihr Verfahren FormatSpread bewertet schnell eine Stichprobe plausibler Prompt-Formate für eine Aufgabe und berichtet das Intervall der erwarteten Leistung, ohne Zugriff auf die Modellgewichte (Sclar et al., 2023).

#### 3. Mehrere Anweisungsparaphrasen

Mizrahi et al. (2023) analysierten die Fragilität von Evaluierungen mit einzelnen Prompts über 6,5 Millionen Instanzen, 20 verschiedene LLMs und 39 Aufgaben und fanden heraus, dass Ergebnisse und Modellranglisten stark von der gewählten Anweisung abhängen. Sie schlagen vor, mit einer Vielzahl von Anweisungsparaphrasen zu bewerten und Metriken zu wählen, die dem Anwendungsfall entsprechen, beispielsweise unterschiedliche Metriken für LLM-Entwickler, die Modelle vergleichen, und für Entwickler, die einen Prompt für eine nachgelagerte Aufgabe wählen.

#### 4. Bewertung der Varianten

Für offene Ausgaben können starke LLMs als Judge dienen ([[llm-as-a-judge|LLM-as-a-Judge]]): GPT-4 als Judge stimmte in über 80 % der Fälle sowohl mit kontrolliert erhobenen als auch mit per Crowdsourcing gesammelten menschlichen Präferenzen überein, ein Grad der Übereinstimmung, der dem zwischen Menschen entspricht (Zheng et al., 2023). Judges zeigen bekannte Verzerrungen, nämlich Position Bias, Verbosity Bias (Bevorzugung längerer Antworten) und Self-Enhancement Bias, also die Tendenz, Antworten des eigenen Modells zu bevorzugen, sowie begrenzte Fähigkeiten zum Schließen; Zheng et al. (2023) schlagen Lösungen vor, um einige dieser Verzerrungen zu verringern. Wenn Prompt-Varianten zu Antworten unterschiedlicher Länge oder unterschiedlichen Stils führen, können diese Verzerrungen den Vergleich beeinflussen.

#### Ursprung und Varianten

Systematische Prompt-Vergleiche bauen auf Erkenntnissen auf, dass die Evaluierung von LLMs empfindlich auf die Formatierung von Prompts (Sclar et al., 2023) und auf die Formulierung von Anweisungen (Mizrahi et al., 2023) reagiert, auf LLM-Judges für offene Antworten (Zheng et al., 2023) und auf Taxonomien von Prompt-Techniken (Schulhoff et al., 2024).

### Wann einsetzen

- Wenn entschieden werden soll, ob eine neue Promptversion die aktuelle in einer Anwendung ersetzen sollte.
- Beim Vergleich von Modellen, da ein einzelnes Prompt-Format irreführende Unterschiede zwischen Modellen erzeugen kann (Sclar et al., 2023; Mizrahi et al., 2023).
- Beim Berichten von Evaluationsergebnissen, die als Bereich über plausible Formate oder Paraphrasen zuverlässiger sind als ein einzelner Wert (Sclar et al., 2023).

### Stärken und Grenzen

**Stärken**
- Zeigt, wie stark die Ergebnisse von der Formatierung und der Formulierung abhängen, anstatt dies hinter einem einzigen Score zu verbergen (Sclar et al., 2023).
- Die Bewertung mit mehreren Prompts führt zu robusteren Modellranglisten als die Bewertung mit einem einzigen Prompt (Mizrahi et al., 2023).
- LLM-Judges machen es kostengünstig, viele Varianten bei offenen Aufgaben zu bewerten (Zheng et al., 2023).

**Einschränkungen**
- Die Bewertung vieler Varianten vervielfacht die Kosten der Bewertung (Mizrahi et al., 2023).
- LLM-Judges haben Position, Verbosity und Self-Enhancement Bias, die Vergleiche verzerren können (Zheng et al., 2023).
- Der Raum der möglichen Varianten ist groß, sodass nur eine Stichprobe von Formaten oder Paraphrasen getestet werden kann (Sclar et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Evaluierung mit einem Prompt | Ein fester Prompt pro Aufgabe; Ergebnisse können sich bei bedeutungserhaltenden Variationen ändern (Mizrahi et al., 2023) | Schnelle Überprüfung, bei der der Prompt fest ist |
| Format-Sampling (FormatSpread) | Zieht eine Stichprobe plausibler Formate und berichtet ein Leistungsintervall (Sclar et al., 2023) | Sensitivität gegenüber Formatierung messen und Modelle fair vergleichen |
| Multi-Prompt-Evaluierung | Bewertet mehrere Paraphrasen der Anweisung mit anwendungsspezifischen Metriken (Mizrahi et al., 2023) | Robuste Modellvergleiche und Promptauswahl |

### In der Praxis

Promptvarianten werden anhand eines festen Evaluierungssatzes verglichen, bei dem für jede Variante die gleichen Eingaben verwendet werden, idealerweise mit nur einer geänderten Komponente pro Variante ([[llm-evaluation|LLM Evaluation]], [[model-comparison|Model Comparison]]). Die Ergebnisse werden als Bereiche über Formate oder Paraphrasen berichtet, nicht als einzelne Werte (Sclar et al., 2023; Mizrahi et al., 2023). Wo ein LLM-Judge die Ausgaben bewertet, wird die Reihenfolge der Antworten zufällig gewählt oder es werden beide Reihenfolgen bewertet, um den Position Bias zu begrenzen (Zheng et al., 2023).

### Merksatz

Da kleine, bedeutungserhaltende Änderungen an Prompts die Ergebnisse erheblich beeinflussen können, werden Prompts anhand fester Eingaben über mehrere Varianten hinweg verglichen und als Bereiche berichtet.

### Quellen

- Sclar, M. et al. (2023). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting.* ICLR 2024. [arXiv:2310.11324](https://arxiv.org/abs/2310.11324)
- Mizrahi, M. et al. (2023). *State of What Art? A Call for Multi-Prompt LLM Evaluation.* TACL. [arXiv:2401.00595](https://arxiv.org/abs/2401.00595)
- Schulhoff, S. et al. (2024). *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques.* [arXiv:2406.06608](https://arxiv.org/abs/2406.06608)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
