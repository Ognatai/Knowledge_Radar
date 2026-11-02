---
title_en: MMLU
title_de: MMLU
entity_type: Dataset
aliases:
- MMLU
- Massive Multitask Language Understanding
- MMLU-Pro
- MMLU-Redux
sources:
- https://arxiv.org/abs/2009.03300
- https://arxiv.org/abs/2406.01574
- https://arxiv.org/abs/2406.04127
- https://web.stanford.edu/~jurafsky/slp3/11.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MMLU (Massive Multitask Language Understanding) is a benchmark of 15,908 four-option multiple-choice questions in 57 subjects, from elementary mathematics and US history to law, medicine and computer science, taken from exams and other materials written for people (Hendrycks et al., 2021). It tests the knowledge and problem solving a language model acquired in pretraining, in zero-shot and few-shot settings, and became one of the most widely reported scores for [[large-language-models|large language models]] (Hendrycks et al., 2021; Wang et al., 2024). As models approached its ceiling, its errors and prompt sensitivity led to successors such as MMLU-Pro and the re-annotated MMLU-Redux (Wang et al., 2024; Gema et al., 2024).

### How it works

```text
57 subjects (STEM, humanities, social sciences, other)
   ▼  questions from exams (e.g. GRE, USMLE, AP) and other human-oriented sources
split: 5 few-shot examples per subject (dev) · 1,540 validation · 14,079 test
   ▼
prompt: "The following are multiple choice questions (with answers) about [subject]."
        + k examples (few-shot) + question + options A–D
   ▼
score: accuracy (exact match on the chosen letter), averaged over subjects; chance = 25%
```

#### 1. Content and construction

The questions were collected manually from freely available sources such as practice questions for graduate admission and medical licensing exams, covering four broad areas: humanities, social sciences, STEM and other subjects such as professional medicine and accounting (Hendrycks et al., 2021). Each subject has at least 100 test questions (Hendrycks et al., 2021). Jurafsky and Martin (2026) classify MMLU as a probing data set: its questions are designed to test knowledge, not to reflect real information needs as in [[natural-questions|Natural Questions]].

#### 2. Evaluation protocol

MMLU is meant to measure knowledge from pretraining, so models are evaluated only zero-shot or few-shot, without fine-tuning on the task (Hendrycks et al., 2021). The prompt names the subject, optionally gives up to five solved examples from the development set, and the model chooses one of the letters A–D; accuracy is the score, with 25% as random chance (Hendrycks et al., 2021). Because answers are multiple choice, the metric is exact match ([[classification-metrics|classification metrics]]; Jurafsky & Martin, 2026; [[few-shot-prompting|few-shot prompting]]).

#### 3. Original results

Few-shot GPT-3 models up to 13 billion parameters scored at chance level, while the 175-billion-parameter model reached 43.9% (Hendrycks et al., 2021). Performance was lopsided, with almost 70% in the best subject and near-chance results in calculation-heavy subjects such as physics and mathematics and in subjects related to human values such as law and morality (Hendrycks et al., 2021). GPT-3's confidence was a poor estimate of its accuracy, off by up to 24% (Hendrycks et al., 2021). Amazon Mechanical Turk workers scored 34.5%; the authors estimated expert-level accuracy at about 89.8% (Hendrycks et al., 2021).

#### 4. Errors in the ground truth

Gema et al. (2024) re-annotated 5,700 questions across all 57 subjects (MMLU-Redux) and estimated that 6.49% of MMLU questions contain errors such as wrong answer keys, unclear questions or several correct options; in the virology subset, 57% of the analysed questions had errors. Re-evaluating models on the corrected questions changed reported performance considerably (Gema et al., 2024).

#### 5. MMLU-Pro

As scores plateaued, MMLU-Pro removed trivial and noisy questions, added more reasoning-focused ones and expanded the options from four to ten, which lowers the chance of a correct guess; it has 12,032 questions in 14 disciplines (Wang et al., 2024). Accuracy dropped by 16 to 33 percentage points compared with MMLU, sensitivity to 24 prompt styles fell from 4–5% to 2%, and chain-of-thought prompting helped on MMLU-Pro, unlike on the original MMLU (Wang et al., 2024; [[chain-of-thought-prompting|chain-of-thought prompting]]).

#### Origin and variants

Dan Hendrycks and colleagues published MMLU at ICLR 2021 (Hendrycks et al., 2021). MMLU-Pro appeared in the NeurIPS 2024 Datasets and Benchmarks track (Wang et al., 2024); MMLU-Redux is a corrected subset (Gema et al., 2024).

### When to use it

- Comparing the broad academic and professional knowledge of language models ([[llm-evaluation|LLM evaluation]]).
- Identifying weak subjects of a model, since results are reported per subject (Hendrycks et al., 2021).
- Checking calibration: whether a model's confidence matches its accuracy (Hendrycks et al., 2021; [[temperature-scaling|temperature scaling]]).

### Strengths and limitations

**Strengths**
- Broad: 57 subjects at several difficulty levels (Hendrycks et al., 2021).
- Simple, cheap evaluation with an unambiguous metric (Jurafsky & Martin, 2026).
- Discriminated well between models when it was introduced, unlike earlier benchmarks on which small models already scored well above chance (Hendrycks et al., 2021).

**Limitations**
- About 6.5% of questions are estimated to be wrong or ambiguous (Gema et al., 2024).
- Scores of strong models have plateaued and are sensitive to prompt wording by 4–5% (Wang et al., 2024).
- Multiple choice tests recognition of the right option, not open-ended explanation or real information needs (Jurafsky & Martin, 2026).
- English, US-centred exam material.

### Comparison

| Benchmark | Questions | Options | Focus |
|---|---|---|---|
| MMLU | 15,908 in 57 subjects | 4 | breadth of knowledge |
| MMLU-Pro | 12,032 in 14 disciplines | 10 | reasoning, robustness to prompts |
| MMLU-Redux | 5,700 re-annotated | 4 | corrected ground truth |
| [[natural-questions\|Natural Questions]] | real search queries | free text | open-domain QA |
| [[humaneval\|HumanEval]] | programming tasks | code | functional correctness |

Sources: Hendrycks et al. (2021), Wang et al. (2024), Gema et al. (2024).

### In practice

Reported MMLU scores depend on the number of shots, the prompt template and the answer extraction, so comparisons need the same setup (Wang et al., 2024). For strong current models, MMLU-Pro or a corrected subset such as MMLU-Redux separates models better than the original (Wang et al., 2024; Gema et al., 2024).

### Key takeaway

MMLU tests broad knowledge with 57 subjects of four-option exam questions; it shaped LLM evaluation, but errors in its answer key and saturation make corrected and harder successors preferable today.

### Sources

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding.* ICLR 2021. [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)
- Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* NeurIPS 2024 Datasets and Benchmarks. [arXiv:2406.01574](https://arxiv.org/abs/2406.01574)
- Gema, A. P. et al. (2024). *Are We Done with MMLU?* [arXiv:2406.04127](https://arxiv.org/abs/2406.04127)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MMLU (Massive Multitask Language Understanding) ist ein Benchmark aus 15.908 Multiple-Choice-Fragen mit vier Optionen in 57 Fächern, von Elementarmathematik und US-Geschichte bis zu Recht, Medizin und Informatik, entnommen aus Prüfungen und anderen für Menschen geschriebenen Materialien (Hendrycks et al., 2021). Er prüft das Wissen und die Problemlösefähigkeit, die ein Sprachmodell im Vortraining erworben hat, im Zero-Shot- und Few-Shot-Setting und wurde zu einem der am häufigsten berichteten Werte für [[large-language-models|große Sprachmodelle]] (Hendrycks et al., 2021; Wang et al., 2024). Als Modelle sich seiner Obergrenze näherten, führten seine Fehler und die Empfindlichkeit gegenüber Prompts zu Nachfolgern wie MMLU-Pro und dem neu annotierten MMLU-Redux (Wang et al., 2024; Gema et al., 2024).

### Funktionsweise

```text
57 Fächer (MINT, Geisteswissenschaften, Sozialwissenschaften, Sonstiges)
   ▼  Fragen aus Prüfungen (z. B. GRE, USMLE, AP) und anderen Quellen für Menschen
Aufteilung: 5 Few-Shot-Beispiele pro Fach (Dev) · 1.540 Validierung · 14.079 Test
   ▼
Prompt: „The following are multiple choice questions (with answers) about [subject].“
        + k Beispiele (Few-Shot) + Frage + Optionen A–D
   ▼
Score: Accuracy (Exact Match auf den gewählten Buchstaben), gemittelt über Fächer; Zufall = 25 %
```

#### 1. Inhalt und Aufbau

Die Fragen wurden von Hand aus frei verfügbaren Quellen gesammelt, etwa Übungsfragen für Zulassungs- und medizinische Approbationsprüfungen, und decken vier große Bereiche ab: Geisteswissenschaften, Sozialwissenschaften, MINT und Sonstiges wie Fachmedizin und Rechnungswesen (Hendrycks et al., 2021). Jedes Fach hat mindestens 100 Testfragen (Hendrycks et al., 2021). Jurafsky und Martin (2026) ordnen MMLU den Prüfdatensätzen zu: Seine Fragen sollen Wissen testen und spiegeln keine echten Informationsbedürfnisse wie [[natural-questions|Natural Questions]].

#### 2. Evaluationsprotokoll

MMLU soll Wissen aus dem Vortraining messen; Modelle werden daher nur zero-shot oder few-shot bewertet, ohne Fine-Tuning auf die Aufgabe (Hendrycks et al., 2021). Der Prompt nennt das Fach, gibt optional bis zu fünf gelöste Beispiele aus der Entwicklungsmenge, und das Modell wählt einen der Buchstaben A–D; der Score ist die Accuracy, mit 25 % als Zufallsniveau (Hendrycks et al., 2021). Weil die Antworten Multiple Choice sind, ist die Metrik Exact Match ([[classification-metrics|Klassifikationsmetriken]]; Jurafsky & Martin, 2026; [[few-shot-prompting|Few-Shot-Prompting]]).

#### 3. Ursprüngliche Ergebnisse

Few-Shot-Modelle von GPT-3 mit bis zu 13 Milliarden Parametern lagen auf Zufallsniveau, das Modell mit 175 Milliarden Parametern erreichte 43,9 % (Hendrycks et al., 2021). Die Leistung war ungleich verteilt, mit fast 70 % im besten Fach und Ergebnissen nahe dem Zufall in rechenlastigen Fächern wie Physik und Mathematik und in Fächern rund um menschliche Werte wie Recht und Moral (Hendrycks et al., 2021). Die Konfidenz von GPT-3 schätzte seine Accuracy schlecht, mit Abweichungen bis zu 24 % (Hendrycks et al., 2021). Crowdworker von Amazon Mechanical Turk erreichten 34,5 %; die Autoren schätzten das Expertenniveau auf etwa 89,8 % (Hendrycks et al., 2021).

#### 4. Fehler in der Referenz

Gema et al. (2024) annotierten 5.700 Fragen aus allen 57 Fächern neu (MMLU-Redux) und schätzten, dass 6,49 % der MMLU-Fragen Fehler enthalten, etwa falsche Lösungsschlüssel, unklare Fragen oder mehrere richtige Optionen; in der Teilmenge Virologie hatten 57 % der analysierten Fragen Fehler. Die Neubewertung von Modellen auf den korrigierten Fragen veränderte die berichtete Leistung erheblich (Gema et al., 2024).

#### 5. MMLU-Pro

Als die Werte stagnierten, entfernte MMLU-Pro triviale und verrauschte Fragen, ergänzte stärker auf Schlussfolgern ausgerichtete und erhöhte die Zahl der Optionen von vier auf zehn, was die Wahrscheinlichkeit eines richtigen Ratens senkt; es umfasst 12.032 Fragen in 14 Disziplinen (Wang et al., 2024). Die Accuracy sank gegenüber MMLU um 16 bis 33 Prozentpunkte, die Empfindlichkeit gegenüber 24 Prompt-Stilen fiel von 4–5 % auf 2 %, und Chain-of-Thought-Prompting half bei MMLU-Pro, anders als beim ursprünglichen MMLU (Wang et al., 2024; [[chain-of-thought-prompting|Chain-of-Thought-Prompting]]).

#### Ursprung und Varianten

Dan Hendrycks und Kollegen veröffentlichten MMLU auf der ICLR 2021 (Hendrycks et al., 2021). MMLU-Pro erschien im Datasets-and-Benchmarks-Track der NeurIPS 2024 (Wang et al., 2024); MMLU-Redux ist eine korrigierte Teilmenge (Gema et al., 2024).

### Wann einsetzen

- Das breite akademische und berufliche Wissen von Sprachmodellen vergleichen ([[llm-evaluation|LLM-Evaluation]]).
- Schwache Fächer eines Modells erkennen, da Ergebnisse pro Fach berichtet werden (Hendrycks et al., 2021).
- Kalibrierung prüfen: ob die Konfidenz eines Modells zu seiner Accuracy passt (Hendrycks et al., 2021; [[temperature-scaling|Temperature Scaling]]).

### Stärken und Grenzen

**Stärken**
- Breit: 57 Fächer auf mehreren Schwierigkeitsstufen (Hendrycks et al., 2021).
- Einfache, günstige Evaluation mit eindeutiger Metrik (Jurafsky & Martin, 2026).
- Trennte bei seiner Einführung gut zwischen Modellen, anders als frühere Benchmarks, auf denen schon kleine Modelle deutlich über Zufall lagen (Hendrycks et al., 2021).

**Grenzen**
- Etwa 6,5 % der Fragen sind schätzungsweise falsch oder mehrdeutig (Gema et al., 2024).
- Die Werte starker Modelle stagnieren und schwanken mit der Formulierung des Prompts um 4–5 % (Wang et al., 2024).
- Multiple Choice prüft das Erkennen der richtigen Option, nicht offene Erklärungen oder echte Informationsbedürfnisse (Jurafsky & Martin, 2026).
- Englisches, auf die USA ausgerichtetes Prüfungsmaterial.

### Vergleich

| Benchmark | Fragen | Optionen | Schwerpunkt |
|---|---|---|---|
| MMLU | 15.908 in 57 Fächern | 4 | Breite des Wissens |
| MMLU-Pro | 12.032 in 14 Disziplinen | 10 | Schlussfolgern, Robustheit gegenüber Prompts |
| MMLU-Redux | 5.700 neu annotiert | 4 | korrigierte Referenz |
| [[natural-questions\|Natural Questions]] | echte Suchanfragen | freier Text | Open-Domain-QA |
| [[humaneval\|HumanEval]] | Programmieraufgaben | Code | funktionale Korrektheit |

Quellen: Hendrycks et al. (2021), Wang et al. (2024), Gema et al. (2024).

### In der Praxis

Berichtete MMLU-Werte hängen von der Zahl der Beispiele im Prompt, dem Prompt-Template und der Extraktion der Antwort ab; Vergleiche brauchen daher dasselbe Setup (Wang et al., 2024). Für starke aktuelle Modelle trennen MMLU-Pro oder eine korrigierte Teilmenge wie MMLU-Redux Modelle besser als das Original (Wang et al., 2024; Gema et al., 2024).

### Merksatz

MMLU prüft breites Wissen mit Prüfungsfragen mit vier Optionen aus 57 Fächern; es prägte die Evaluation von LLMs, doch Fehler im Lösungsschlüssel und Sättigung machen korrigierte und schwierigere Nachfolger heute vorzuziehen.

### Quellen

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding.* ICLR 2021. [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)
- Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* NeurIPS 2024 Datasets and Benchmarks. [arXiv:2406.01574](https://arxiv.org/abs/2406.01574)
- Gema, A. P. et al. (2024). *Are We Done with MMLU?* [arXiv:2406.04127](https://arxiv.org/abs/2406.04127)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
