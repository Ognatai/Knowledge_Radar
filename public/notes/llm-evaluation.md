---
title_en: LLM Evaluation
title_de: LLM-Evaluation
entity_type: Method
sources:
- https://arxiv.org/abs/2211.09110
- https://arxiv.org/abs/2009.03300
- https://arxiv.org/abs/2109.07958
- https://arxiv.org/abs/2306.05685
- https://arxiv.org/abs/2403.04132
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LLM evaluation measures what a language model or LLM application can do. It combines benchmarks with reference answers for knowledge and truthfulness, holistic frameworks that report several metrics across many scenarios, strong LLMs as judges for open-ended answers, and crowdsourced pairwise comparisons that rank models by human preference (Hendrycks et al., 2020; Lin et al., 2021; Liang et al., 2022; Zheng et al., 2023; Chiang et al., 2024).

### How it works

A capability is turned into a measurable task, the model's outputs are scored against reference answers, metrics, judges or human preferences, and the scores are aggregated. Different methods cover different aspects: fixed benchmarks are cheap and reproducible, holistic frameworks broaden what is measured, and judges or human comparisons are needed for open-ended outputs.

```text
1. Knowledge benchmarks with reference answers
▼
2. Truthfulness benchmarks
▼
3. Holistic multi-metric evaluation
▼
4. Strong LLMs as judges
▼
5. Crowdsourced pairwise comparison
```

#### 1. Knowledge benchmarks

MMLU (Hendrycks et al., 2020) is a multitask test of 57 tasks, including elementary mathematics, US history, computer science and law, that requires extensive world knowledge and problem-solving ability; models are scored by accuracy on multiple-choice questions. Most models were near random chance, while the largest GPT-3 model improved on random chance by almost 20 percentage points on average. Even the best models still had lopsided performance and near-random accuracy on some socially important subjects such as morality and law (Hendrycks et al., 2020).

#### 2. Truthfulness

TruthfulQA (Lin et al., 2021) contains 817 questions in 38 categories, including health, law, finance and politics, crafted so that some humans would answer falsely because of a misconception. The best model tested was truthful on 58% of the questions, compared with 94% for humans, and the largest models were generally the least truthful, in contrast to other NLP tasks where performance improves with size (Lin et al., 2021). The authors suggest that scaling alone is less promising for truthfulness than fine-tuning with objectives other than imitating web text.

#### 3. Holistic evaluation

HELM (Liang et al., 2022) first taxonomises the space of possible scenarios and metrics and then selects a broad subset. It measures seven metrics, namely accuracy, calibration, robustness, fairness, bias, toxicity and efficiency, for each of 16 core scenarios where possible (87.5% of the time), and adds targeted evaluations of aspects such as reasoning and disinformation. HELM evaluated 30 prominent models on all 42 scenarios, 21 of them not previously used in mainstream evaluation; before HELM, models had on average been evaluated on just 17.9% of the core scenarios, and HELM raised this to 96.0% (Liang et al., 2022).

#### 4. LLM as a judge

For open-ended answers without a single correct reference, strong LLMs can act as judges ([[llm-as-a-judge|LLM-as-a-Judge]]). Zheng et al. (2023) found that GPT-4 as judge agreed with both controlled and crowdsourced human preferences in over 80% of cases, the same level of agreement as between humans, using the multi-turn question set MT-bench and the Chatbot Arena platform. Judges have limitations: position bias, verbosity bias, self-enhancement bias (favouring answers produced by the judge's own model) and limited reasoning ability.

#### 5. Crowdsourced pairwise comparison

Chatbot Arena (Chiang et al., 2024) lets users ask a question, compare the answers of two anonymous models side by side and vote for the better one. The platform collected over 240,000 votes and uses statistical methods to rank models efficiently and accurately from these pairwise comparisons. The authors found the crowdsourced questions sufficiently diverse and discriminating and the crowdsourced votes in good agreement with those of expert raters (Chiang et al., 2024).

#### Origin and variants

Benchmarks with reference answers such as MMLU (Hendrycks et al., 2020) and TruthfulQA (Lin et al., 2021) were followed by holistic frameworks such as HELM (Liang et al., 2022), which broadened evaluation beyond accuracy. For chat assistants, LLM judges (Zheng et al., 2023) and crowdsourced human comparisons (Chiang et al., 2024) became common because open-ended answers are hard to score against references.

### When to use it

- When comparing the general knowledge of models on a standard set of questions (Hendrycks et al., 2020).
- When an application must avoid repeating common misconceptions, which requires testing truthfulness specifically (Lin et al., 2021).
- When accuracy alone is not enough and calibration, robustness, fairness, bias, toxicity or efficiency also matter (Liang et al., 2022).
- When answers are open-ended and must be scored at scale, using an LLM judge validated against human preferences (Zheng et al., 2023).

### Strengths and limitations

**Strengths**
- Fixed benchmarks with reference answers are cheap, reproducible and allow comparison across many models (Hendrycks et al., 2020).
- Holistic evaluation makes trade-offs visible between accuracy and other properties and evaluates all models on the same scenarios (Liang et al., 2022).
- LLM judges and crowdsourced comparisons capture human preferences for open-ended answers, with high agreement with human or expert raters (Zheng et al., 2023; Chiang et al., 2024).

**Limitations**
- High average scores can hide near-random performance on specific subjects (Hendrycks et al., 2020).
- Larger models are not automatically more truthful (Lin et al., 2021).
- LLM judges have position, verbosity and self-enhancement biases (Zheng et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Knowledge benchmark (MMLU) | Multiple-choice questions in 57 tasks, scored by accuracy (Hendrycks et al., 2020) | Comparing broad world knowledge |
| Truthfulness benchmark (TruthfulQA) | Questions designed to elicit common misconceptions (Lin et al., 2021) | Testing whether a model repeats falsehoods |
| Holistic framework (HELM) | Seven metrics across many scenarios for all models (Liang et al., 2022) | Broad, standardised model assessment |
| LLM judge (MT-bench) | A strong LLM scores or compares open-ended answers (Zheng et al., 2023) | Scalable evaluation of chat answers |
| Crowdsourced arena (Chatbot Arena) | Anonymous pairwise votes by users, aggregated into a ranking (Chiang et al., 2024) | Ranking models by real user preference |

### In practice

Applications are evaluated on data from their own use case in addition to public benchmarks, since benchmark scores say little about a specific task. Several metrics are reported rather than accuracy alone (Liang et al., 2022), and where an LLM judge is used, its agreement with human ratings is checked on a sample ([[llm-as-a-judge|LLM-as-a-Judge]], Zheng et al., 2023). Prompt variants are compared on fixed inputs ([[prompt-comparison|Prompt Comparison]]).

### Key takeaway

No single benchmark captures what an LLM can do; reliable evaluation combines reference-based benchmarks, several metrics and human or LLM judgements of open-ended answers.

### Sources

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models.* TMLR. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110)
- Hendrycks, D. et al. (2020). *Measuring Massive Multitask Language Understanding.* ICLR 2021. [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)
- Lin, S. et al. (2021). *TruthfulQA: Measuring How Models Mimic Human Falsehoods.* ACL 2022. [arXiv:2109.07958](https://arxiv.org/abs/2109.07958)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Chiang, W. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference.* ICML 2024. [arXiv:2403.04132](https://arxiv.org/abs/2403.04132)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LLM-Evaluation misst, was ein Sprachmodell oder eine LLM-Anwendung kann. Sie kombiniert Benchmarks mit Referenzantworten für Wissen und Wahrhaftigkeit, ganzheitliche Frameworks, die mehrere Metriken über viele Szenarien berichten, starke LLMs als Judges für offene Antworten sowie per Crowdsourcing erhobene paarweise Vergleiche, die Modelle anhand menschlicher Präferenzen bewerten (Hendrycks et al., 2020; Lin et al., 2021; Liang et al., 2022; Zheng et al., 2023; Chiang et al., 2024).

### Funktionsweise

Eine Fähigkeit wird in eine messbare Aufgabe umgewandelt, die Ausgaben des Modells werden anhand von Referenzantworten, Metriken, Judges oder menschlichen Präferenzen bewertet, und die Scores werden aggregiert. Verschiedene Methoden decken unterschiedliche Aspekte ab: feste Benchmarks sind günstig und reproduzierbar, ganzheitliche Frameworks erweitern, was gemessen wird, und Judges oder menschliche Vergleiche sind für offene Ausgaben erforderlich.

```text
1. Wissensbenchmarks mit Referenzantworten
▼
2. Benchmarks für Wahrhaftigkeit
▼
3. Ganzheitliche Evaluation mit mehreren Metriken
▼
4. Starke LLMs als Judges
▼
5. Paarweise Vergleiche per Crowdsourcing
```

#### 1. Wissensbenchmarks

MMLU (Hendrycks et al., 2020) ist ein Multitask-Test mit 57 Aufgaben, einschließlich elementarer Mathematik, US-Geschichte, Informatik und Recht, der umfangreiches Weltwissen und Problemlösefähigkeit erfordert; Modelle werden anhand der Genauigkeit bei Multiple-Choice-Fragen bewertet. Die meisten Modelle lagen nahe dem Zufall, während das größte GPT-3-Modell den Zufall im Durchschnitt um fast 20 Prozentpunkte übertraf. Selbst die besten Modelle zeigten noch immer ungleichmäßige Leistungen und nahezu zufällige Genauigkeit bei einigen sozial wichtigen Themen wie Moral und Recht (Hendrycks et al., 2020).

#### 2. Wahrhaftigkeit

TruthfulQA (Lin et al., 2021) enthält 817 Fragen in 38 Kategorien, einschließlich Gesundheit, Recht, Finanzen und Politik, die so formuliert wurden, dass einige Menschen aufgrund einer verbreiteten Fehlvorstellung falsch antworten würden. Das beste getestete Modell antwortete bei 58 % der Fragen wahrheitsgemäß, im Vergleich zu 94 % bei Menschen, und die größten Modelle waren im Allgemeinen am wenigsten wahrhaftig, im Gegensatz zu anderen NLP-Aufgaben, bei denen die Leistung mit der Größe zunimmt (Lin et al., 2021). Die Autoren schlagen vor, dass Skalieren allein für die Wahrhaftigkeit weniger vielversprechend ist als Fine-Tuning mit Trainingszielen, die nicht im Nachahmen von Webtext bestehen.

#### 3. Ganzheitliche Bewertung

HELM (Liang et al., 2022) ordnet zunächst den Raum möglicher Szenarien und Metriken in einer Taxonomie und wählt dann eine breite Teilmenge aus. Es misst sieben Metriken, nämlich Genauigkeit, Kalibrierung, Robustheit, Fairness, Bias, Toxizität und Effizienz, für jedes der 16 Kernszenarien, wo dies möglich ist (87,5 % der Zeit), und ergänzt gezielte Evaluationen von Aspekten wie Schlussfolgern und Desinformation. HELM bewertete 30 bekannte Modelle in allen 42 Szenarien, von denen 21 zuvor nicht in gängigen Evaluationen verwendet worden waren; vor HELM wurden Modelle im Durchschnitt nur auf 17,9 % der Kernszenarien bewertet, und HELM erhöhte dies auf 96,0 % (Liang et al., 2022).

#### 4. LLM als Judge

Für offene Antworten ohne eindeutig korrekte Referenz können starke LLMs als Judges dienen ([[llm-as-a-judge|LLM-as-a-Judge]]). Zheng et al. (2023) fanden, dass GPT-4 als Judge in über 80 % der Fälle mit kontrolliert erhobenen und per Crowdsourcing gesammelten menschlichen Präferenzen übereinstimmte, ein Grad der Übereinstimmung, der dem zwischen Menschen entspricht, auf Grundlage des Fragenkatalogs MT-bench mit mehreren Gesprächsrunden und der Plattform Chatbot Arena. Judges haben Grenzen: Position Bias, Verbosity Bias, Self-Enhancement Bias (Bevorzugung von Antworten des eigenen Modells) und begrenzte Fähigkeiten zum Schließen.

#### 5. Paarweise Vergleiche per Crowdsourcing

Chatbot Arena (Chiang et al., 2024) ermöglicht es Nutzern, eine Frage zu stellen, die Antworten zweier anonymer Modelle nebeneinander zu vergleichen und für die bessere zu stimmen. Die Plattform sammelte über 240.000 Stimmen und verwendet statistische Methoden, um Modelle anhand dieser paarweisen Vergleiche effizient und genau zu ranken. Die Autoren fanden die per Crowdsourcing gestellten Fragen ausreichend vielfältig und trennscharf, und die abgegebenen Stimmen stimmten gut mit denen von Fachleuten überein (Chiang et al., 2024).

#### Ursprung und Varianten

Auf Benchmarks mit Referenzantworten wie MMLU (Hendrycks et al., 2020) und TruthfulQA (Lin et al., 2021) folgten ganzheitliche Frameworks wie HELM (Liang et al., 2022), die die Bewertung über die Genauigkeit hinaus erweiterten. Bei Chat-Assistenten wurden aufgrund der Schwierigkeit, offene Antworten anhand von Referenzen zu bewerten, LLM-Judges (Zheng et al., 2023) und menschliche Vergleiche per Crowdsourcing (Chiang et al., 2024) üblich.

### Wann einsetzen

- Beim Vergleich des allgemeinen Wissens von Modellen anhand einer Standardmenge von Fragen (Hendrycks et al., 2020).
- Wenn eine Anwendung gezielt falsche Vorstellungen vermeiden muss, was eine gezielte Prüfung der Wahrhaftigkeit erfordert (Lin et al., 2021).
- Wenn die Genauigkeit allein nicht ausreicht und Kalibrierung, Robustheit, Fairness, Bias, Toxizität oder Effizienz ebenfalls eine Rolle spielen (Liang et al., 2022).
- Wenn die Antworten offen sind und auf einer großen Skala bewertet werden müssen, wobei ein LLM-Judge an menschlichen Präferenzen validiert wird (Zheng et al., 2023).

### Stärken und Grenzen

**Stärken**
- Festgelegte Benchmarks mit Referenzantworten sind günstig, reproduzierbar und ermöglichen den Vergleich zwischen vielen Modellen (Hendrycks et al., 2020).
- Eine ganzheitliche Evaluation macht Zielkonflikte zwischen Genauigkeit und anderen Eigenschaften sichtbar und bewertet alle Modelle in denselben Szenarien (Liang et al., 2022).
- LLM-Judges und Vergleiche per Crowdsourcing erfassen menschliche Präferenzen für offene Antworten, mit hoher Übereinstimmung mit menschlichen Bewertungen oder Fachleuten (Zheng et al., 2023; Chiang et al., 2024).

**Einschränkungen**
- Hohe Durchschnittswerte können eine nahezu zufällige Leistung bei bestimmten Themen verbergen (Hendrycks et al., 2020).
- Größere Modelle sind nicht automatisch wahrhaftiger (Lin et al., 2021).
- LLM-Judges haben Position, Verbosity und Self-Enhancement Bias (Zheng et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Wissensbenchmark (MMLU) | Multiple-Choice-Fragen in 57 Aufgaben, bewertet nach Genauigkeit (Hendrycks et al., 2020) | Vergleich von breitem Weltwissen |
| Wahrheitsbenchmark (TruthfulQA) | Fragen, die dazu dienen, verbreitete Fehlvorstellungen hervorzurufen (Lin et al., 2021) | Prüfen, ob ein Modell Unwahrheiten wiederholt |
| Holistisches Framework (HELM) | Sieben Metriken über viele Szenarien für alle Modelle (Liang et al., 2022) | Umfassende, standardisierte Modellbewertung |
| LLM-Judge (MT-bench) | Ein starkes LLM bewertet oder vergleicht offene Antworten (Zheng et al., 2023) | Skalierbare Bewertung von Chat-Antworten |
| Arena mit Crowdsourcing (Chatbot Arena) | Anonyme paarweise Stimmen von Nutzern, aggregiert zu einer Rangliste (Chiang et al., 2024) | Ranking von Modellen nach echten Nutzerpräferenzen |

### In der Praxis

Anwendungen werden anhand von Daten aus ihrem eigenen Anwendungsfall bewertet, zusätzlich zu öffentlichen Benchmarks, da Benchmark-Ergebnisse wenig über eine spezifische Aufgabe aussagen. Mehrere Metriken werden berichtet, nicht nur die Genauigkeit (Liang et al., 2022), und wo ein LLM-Judge verwendet wird, wird dessen Übereinstimmung mit menschlichen Bewertungen anhand einer Stichprobe überprüft ([[llm-as-a-judge|LLM-as-a-Judge]], Zheng et al., 2023). Prompt-Varianten werden anhand fester Eingaben verglichen ([[prompt-comparison|Prompt-Vergleich]]).

### Merksatz

Kein einzelner Benchmark erfasst, was ein LLM kann; eine zuverlässige Evaluation kombiniert referenzbasierte Benchmarks, mehrere Metriken und menschliche oder LLM-Bewertungen von offenen Antworten.

### Quellen

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models.* TMLR. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110)
- Hendrycks, D. et al. (2020). *Measuring Massive Multitask Language Understanding.* ICLR 2021. [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)
- Lin, S. et al. (2021). *TruthfulQA: Measuring How Models Mimic Human Falsehoods.* ACL 2022. [arXiv:2109.07958](https://arxiv.org/abs/2109.07958)
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Chiang, W. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference.* ICML 2024. [arXiv:2403.04132](https://arxiv.org/abs/2403.04132)
