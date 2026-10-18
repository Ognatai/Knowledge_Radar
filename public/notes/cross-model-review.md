---
title_en: Cross-Model Review
title_de: Cross-Model Review
entity_type: Method
aliases:
- Multi-brain
- Multibrain
- multi-brain debugging
- Multi-LLM review
- Cross-model code review
sources:
- https://skillsmp.com/creators/gerardordz96/aios-starter-kit/claude-skills-multi-brain
- https://arxiv.org/abs/2404.13076
- https://arxiv.org/abs/2305.14325
- https://arxiv.org/abs/2404.17153
- https://arxiv.org/abs/2410.01242
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Cross-model review is a pattern for debugging and reviewing AI-generated work in which a different model, ideally from a different model family, checks what one model produced, instead of letting the model review its own output. In the "multi-brain" skill for coding assistants this is the "NO-SELF-REVIEW LAW": "A model reviewing its own output has the same blind spots that produced the bug", so reviews are routed to a model of a different lineage if one is available (multi-brain skill). The research basis is that LLM evaluators recognise and favour their own generations (Panickssery et al., 2024), and that several model instances debating their answers improves reasoning and factuality (Du et al., 2023). Multi-agent debugging frameworks such as UniDebugger and RGD split debugging into roles handled by different agents (Lee et al., 2024; Jin et al., 2024). "Multi-brain" is a name used in the community, not an established technical term.

### How it works

```text
task (code, fix, analysis)
 ▼
author model A produces output
 ▼
review routed to model B  (different family / lineage if available)
   no second lineage? → say so, re-derive the check from scratch
 ▼
B returns findings → A (or a human) fixes → tests run
 ▼
optional: several reviewers or debate rounds until agreement
```

#### 1. Why self-review is weak

Panickssery et al. (2024) studied self-preference, the bias of an LLM evaluator to score its own outputs higher than others' while human annotators judge them equal. GPT-4 and [[llama|Llama 2]] could distinguish their own outputs from those of other LLMs and humans with non-trivial accuracy out of the box, and fine-tuning showed a linear correlation between self-recognition and the strength of self-preference; the authors argue that self-recognition can interfere with unbiased evaluation and AI safety (Panickssery et al., 2024). For code, the multi-brain skill states the practical consequence: a model checking its own work shares the blind spots that produced the error (multi-brain skill). The same bias affects [[llm-as-a-judge|LLM-as-a-judge]] setups.

#### 2. Routing to a different model

The multi-brain skill describes itself as a multi-LLM auto-router: the main assistant orchestrates and hands a sub-task to a different model only when that model fits the job better, and the user keeps working with one assistant (multi-brain skill). The roster of available models is configured by the user; the examples (Codex, Gemini and a local Ollama model) are placeholders (multi-brain skill). When the user asks for a check of work the assistant just produced, the review goes to a model from a different lineage; if no second lineage is installed, the assistant has to say so and re-derive the check from scratch instead of rubber-stamping (multi-brain skill). Gateways such as [[openrouter|OpenRouter]] make several model families available through one API.

#### 3. Debate between models

Du et al. (2023) let multiple language model instances propose answers and debate their responses and reasoning over several rounds until they reach a common answer. This improved mathematical and strategic reasoning and the factual validity of generated content, reducing fallacious answers and hallucinations, and works with black-box models using the same procedure and prompts for all tasks (Du et al., 2023). In their experiments the instances were copies of the same model; cross-model review adds diversity by using different models.

#### 4. Multi-agent debugging frameworks

UniDebugger (FixAgent) handles the debugging process end to end with several agents, each specialised for one step of a developer's cognitive debugging process, such as fault localisation and patch generation, coordinated in a three-level design; it fixed 1.25 to 2.56 times as many bugs as state-of-the-art repair methods on the repository-level benchmark Defects4J, without needing ground-truth root-cause statements (Lee et al., 2024). RGD splits code generation and debugging into a Guide Agent, a Debug Agent and a Feedback Agent that refine code iteratively based on self-reflection and feedback, and reported improvements of 9.8% on [[humaneval|HumanEval]] and 16.2% on MBPP over earlier approaches (Jin et al., 2024). These frameworks assign roles to agents; whether the agents run on the same or different models is a configuration choice ([[multi-agent-systems|multi-agent systems]]).

#### Origin and variants

The research ingredients are multi-agent debate (Du et al., 2023), the finding of self-preference bias (Panickssery et al., 2024) and multi-agent debugging frameworks (Lee et al., 2024; Jin et al., 2024). The name "multi-brain" comes from a community skill for coding assistants (multi-brain skill); similar practices are described as second-opinion or cross-vendor review. Coding with AI assistants in general is covered in [[vibe-coding|vibe coding]].

### When to use it

- When AI-generated code or fixes are about to be merged and a second, independent check is wanted before human review (multi-brain skill).
- When the same model already wrote and failed to fix a bug, since its blind spots are likely to repeat (multi-brain skill).
- When an LLM is used as an evaluator of outputs that it or a closely related model produced (Panickssery et al., 2024).

### Strengths and limitations

**Strengths**
- Avoids self-preference bias in evaluation (Panickssery et al., 2024).
- Several models debating improves reasoning and reduces hallucinated answers (Du et al., 2023).
- Role-based multi-agent debugging fixed more real bugs than state-of-the-art repair methods (Lee et al., 2024).

**Limitations**
- More model calls mean more cost and latency ([[llm-cost-optimisation|LLM cost optimisation]]).
- Models from different vendors may share training data and errors, so agreement is not proof of correctness.
- A reviewer model can be wrong or confidently mistaken; tests and human review remain necessary ([[software-testing|software testing]]).
- "Multi-brain" is not a standardised method; the skill's rules are a practice, not an evaluated technique (multi-brain skill).

### Comparison

| Approach | Who checks | Diversity | Example |
|---|---|---|---|
| Self-review / self-refinement | the same model | none | asking the model to check its answer |
| Cross-model review | a different model family | high | multi-brain skill |
| Multi-agent debate | several instances, often the same model | low to high | Du et al. (2023) |
| Role-based multi-agent debugging | specialised agents | depends on configuration | UniDebugger, RGD |
| Human code review | developers | different kind of judgement | pull request review |

Sources: Panickssery et al. (2024); Du et al. (2023); Lee et al. (2024); Jin et al. (2024); multi-brain skill.

### In practice

Cross-model review fits into [[agent-skills|agent skills]] and harnesses that can call several model providers ([[harness-engineering|harness engineering]]). Findings from the reviewing model should be verified by running tests rather than accepted on trust ([[regression-testing|regression testing]]), and the review prompt should ask for concrete failure scenarios. In [[llm-evaluation|LLM evaluation]], the same idea means using a judge model from a different family than the models being compared.

### Key takeaway

A model is a weak judge of its own work, so cross-model review lets a model from a different family check AI-generated code and answers, as a complement to tests and human review rather than a replacement.

### Sources

- GerardoRdz96 (n.d.). *multi-brain* skill, aios-starter-kit. SkillsMP. [skillsmp.com](https://skillsmp.com/creators/gerardordz96/aios-starter-kit/claude-skills-multi-brain)
- Panickssery, A., Bowman, S. R. & Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* arXiv:2404.13076. [arXiv](https://arxiv.org/abs/2404.13076)
- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B. & Mordatch, I. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.* arXiv:2305.14325. [arXiv](https://arxiv.org/abs/2305.14325)
- Lee, C., Xia, C. S., Yang, L., Huang, J., Zhu, Z., Zhang, L. & Lyu, M. R. (2024). *UniDebugger: Hierarchical Multi-Agent Framework for Unified Software Debugging.* arXiv:2404.17153. [arXiv](https://arxiv.org/abs/2404.17153)
- Jin, H., Sun, Z. & Chen, H. (2024). *RGD: Multi-LLM Based Agent Debugger via Refinement and Generation Guidance.* arXiv:2410.01242. [arXiv](https://arxiv.org/abs/2410.01242)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Cross-Model Review ist ein Muster zum Debuggen und Prüfen KI-erzeugter Arbeit, bei dem ein anderes Modell, möglichst aus einer anderen Modellfamilie, prüft, was ein Modell erzeugt hat, statt das Modell seine eigene Ausgabe prüfen zu lassen. Im „multi-brain“-Skill für Coding-Assistenten heißt das „NO-SELF-REVIEW LAW“: „A model reviewing its own output has the same blind spots that produced the bug“; Reviews gehen daher an ein Modell einer anderen Modellfamilie, sofern eines verfügbar ist (multi-brain-Skill). Die Forschungsgrundlage ist, dass LLM-Bewerter ihre eigenen Erzeugnisse erkennen und bevorzugen (Panickssery et al., 2024) und dass mehrere Modellinstanzen, die über ihre Antworten debattieren, Schlussfolgern und Faktentreue verbessern (Du et al., 2023). Multi-Agenten-Frameworks zum Debuggen wie UniDebugger und RGD teilen das Debugging in Rollen auf, die verschiedene Agenten übernehmen (Lee et al., 2024; Jin et al., 2024). „Multi-brain“ ist ein in der Community verwendeter Name, kein etablierter Fachbegriff.

### Funktionsweise

```text
Aufgabe (Code, Fix, Analyse)
 ▼
Autor-Modell A erzeugt Ausgabe
 ▼
Review geht an Modell B  (andere Familie / Herkunft, falls verfügbar)
   keine zweite Modellfamilie? → offen sagen, Prüfung von Grund auf neu herleiten
 ▼
B liefert Befunde → A (oder ein Mensch) korrigiert → Tests laufen
 ▼
optional: mehrere Prüfende oder Debattenrunden bis zur Einigung
```

#### 1. Warum Selbstprüfung schwach ist

Panickssery et al. (2024) untersuchten Self-Preference, die Neigung eines LLM-Bewerters, eigene Ausgaben höher zu bewerten als fremde, obwohl menschliche Annotierende sie gleich gut finden. GPT-4 und [[llama|Llama 2]] konnten ohne Anpassung mit nicht trivialer Genauigkeit eigene Ausgaben von denen anderer LLMs und von Menschen unterscheiden, und Fine-Tuning zeigte einen linearen Zusammenhang zwischen Selbsterkennung und der Stärke der Self-Preference; die Autorinnen und Autoren argumentieren, dass Selbsterkennung unvoreingenommene Evaluation und KI-Sicherheit beeinträchtigen kann (Panickssery et al., 2024). Für Code formuliert der multi-brain-Skill die praktische Folge: Ein Modell, das seine eigene Arbeit prüft, teilt die blinden Flecken, die den Fehler verursacht haben (multi-brain-Skill). Dieselbe Verzerrung betrifft [[llm-as-a-judge|LLM-as-a-Judge]]-Aufbauten.

#### 2. Weiterleitung an ein anderes Modell

Der multi-brain-Skill beschreibt sich als Multi-LLM-Auto-Router: Der Hauptassistent steuert und gibt eine Teilaufgabe nur dann an ein anderes Modell ab, wenn dieses besser dafür geeignet ist, und die Nutzenden arbeiten weiter mit einem Assistenten (multi-brain-Skill). Die verfügbaren Modelle legen die Nutzenden selbst fest; die Beispiele (Codex, Gemini und ein lokales Ollama-Modell) sind Platzhalter (multi-brain-Skill). Soll Arbeit geprüft werden, die der Assistent gerade erzeugt hat, geht das Review an ein Modell einer anderen Modellfamilie; ist keine zweite installiert, muss der Assistent das sagen und die Prüfung von Grund auf neu herleiten, statt sie einfach abzunicken (multi-brain-Skill). Gateways wie [[openrouter|OpenRouter]] machen mehrere Modellfamilien über eine API verfügbar.

#### 3. Debatte zwischen Modellen

Du et al. (2023) ließen mehrere Instanzen eines Sprachmodells Antworten vorschlagen und über mehrere Runden über ihre Antworten und Begründungen debattieren, bis sie zu einer gemeinsamen Antwort kamen. Das verbesserte mathematisches und strategisches Schlussfolgern sowie die Faktentreue der erzeugten Inhalte, verringerte Fehlschlüsse und Halluzinationen und funktioniert mit Black-Box-Modellen mit demselben Ablauf und denselben Prompts für alle Aufgaben (Du et al., 2023). In ihren Experimenten waren die Instanzen Kopien desselben Modells; Cross-Model Review erhöht die Vielfalt, indem es verschiedene Modelle nutzt.

#### 4. Multi-Agenten-Frameworks zum Debuggen

UniDebugger (FixAgent) deckt den Debugging-Prozess durchgängig mit mehreren Agenten ab, die jeweils auf einen Schritt des kognitiven Debugging-Prozesses von Entwicklerinnen und Entwicklern spezialisiert sind, etwa Fehlerlokalisierung und Patch-Erzeugung, koordiniert in einem dreistufigen Aufbau; es behob auf dem Repository-Benchmark Defects4J 1,25- bis 2,56-mal so viele Fehler wie führende Reparaturverfahren, ohne die tatsächlich fehlerverursachenden Codezeilen vorgegeben zu bekommen (Lee et al., 2024). RGD teilt Codeerzeugung und Debugging in einen Guide Agent, einen Debug Agent und einen Feedback Agent auf, die Code anhand von Selbstreflexion und Rückmeldungen schrittweise verbessern, und berichtete Verbesserungen um 9,8 % auf [[humaneval|HumanEval]] und 16,2 % auf MBPP gegenüber früheren Ansätzen (Jin et al., 2024). Diese Frameworks verteilen Rollen auf Agenten; ob die Agenten auf demselben oder verschiedenen Modellen laufen, ist eine Frage der Konfiguration ([[multi-agent-systems|Multi-Agenten-Systeme]]).

#### Herkunft und Varianten

Die Forschungsbausteine sind die Debatte mehrerer Agenten (Du et al., 2023), der Befund der Self-Preference (Panickssery et al., 2024) und Multi-Agenten-Frameworks zum Debuggen (Lee et al., 2024; Jin et al., 2024). Der Name „multi-brain“ stammt aus einem Community-Skill für Coding-Assistenten (multi-brain-Skill); ähnliche Praktiken heißen Zweitmeinung oder herstellerübergreifendes Review. Programmieren mit KI-Assistenten allgemein behandelt [[vibe-coding|Vibe Coding]].

### Wann einsetzen

- Wenn KI-erzeugter Code oder Fixes übernommen werden sollen und vor dem menschlichen Review eine zweite, unabhängige Prüfung gewünscht ist (multi-brain-Skill).
- Wenn dasselbe Modell einen Fehler bereits geschrieben und nicht beheben konnte, da sich seine blinden Flecken wahrscheinlich wiederholen (multi-brain-Skill).
- Wenn ein LLM Ausgaben bewertet, die es selbst oder ein eng verwandtes Modell erzeugt hat (Panickssery et al., 2024).

### Stärken und Grenzen

**Stärken**
- Vermeidet Self-Preference bei der Bewertung (Panickssery et al., 2024).
- Debattierende Modelle schlussfolgern besser und halluzinieren seltener (Du et al., 2023).
- Rollenbasiertes Debugging mit mehreren Agenten behob mehr echte Fehler als führende Reparaturverfahren (Lee et al., 2024).

**Grenzen**
- Mehr Modellaufrufe bedeuten mehr Kosten und Latenz ([[llm-cost-optimisation|LLM-Kostenoptimierung]]).
- Modelle verschiedener Hersteller können Trainingsdaten und Fehler teilen; Übereinstimmung beweist keine Korrektheit.
- Ein prüfendes Modell kann irren oder überzeugt falsch liegen; Tests und menschliches Review bleiben nötig ([[software-testing|Softwaretests]]).
- „Multi-brain“ ist kein standardisiertes Verfahren; die Regeln des Skills sind eine Praxis, keine evaluierte Technik (multi-brain-Skill).

### Vergleich

| Ansatz | Wer prüft | Vielfalt | Beispiel |
|---|---|---|---|
| Selbstprüfung / Self-Refinement | dasselbe Modell | keine | Modell bitten, seine Antwort zu prüfen |
| Cross-Model Review | eine andere Modellfamilie | hoch | multi-brain-Skill |
| Debatte mehrerer Agenten | mehrere Instanzen, oft desselben Modells | gering bis hoch | Du et al. (2023) |
| Rollenbasiertes Debugging mit Agenten | spezialisierte Agenten | je nach Konfiguration | UniDebugger, RGD |
| Menschliches Code Review | Entwicklerinnen und Entwickler | andere Art von Urteil | Review eines Pull Requests |

Quellen: Panickssery et al. (2024); Du et al. (2023); Lee et al. (2024); Jin et al. (2024); multi-brain-Skill.

### In der Praxis

Cross-Model Review passt in [[agent-skills|Agent Skills]] und Harnesses, die mehrere Modellanbieter aufrufen können ([[harness-engineering|Harness Engineering]]). Befunde des prüfenden Modells sollten durch Ausführen von Tests bestätigt statt im Vertrauen übernommen werden ([[regression-testing|Regressionstests]]), und der Review-Prompt sollte nach konkreten Fehlerszenarien fragen. In der [[llm-evaluation|LLM-Evaluation]] bedeutet dieselbe Idee, ein Judge-Modell aus einer anderen Familie zu nutzen als die verglichenen Modelle.

### Merksatz

Ein Modell ist ein schwacher Richter über die eigene Arbeit; Cross-Model Review lässt daher ein Modell einer anderen Familie KI-erzeugten Code und Antworten prüfen, als Ergänzung zu Tests und menschlichem Review, nicht als Ersatz.

### Quellen

- GerardoRdz96 (n.d.). *multi-brain* skill, aios-starter-kit. SkillsMP. [skillsmp.com](https://skillsmp.com/creators/gerardordz96/aios-starter-kit/claude-skills-multi-brain)
- Panickssery, A., Bowman, S. R. & Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* arXiv:2404.13076. [arXiv](https://arxiv.org/abs/2404.13076)
- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B. & Mordatch, I. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.* arXiv:2305.14325. [arXiv](https://arxiv.org/abs/2305.14325)
- Lee, C., Xia, C. S., Yang, L., Huang, J., Zhu, Z., Zhang, L. & Lyu, M. R. (2024). *UniDebugger: Hierarchical Multi-Agent Framework for Unified Software Debugging.* arXiv:2404.17153. [arXiv](https://arxiv.org/abs/2404.17153)
- Jin, H., Sun, Z. & Chen, H. (2024). *RGD: Multi-LLM Based Agent Debugger via Refinement and Generation Guidance.* arXiv:2410.01242. [arXiv](https://arxiv.org/abs/2410.01242)
