---
title_en: Loop Engineering
title_de: Loop Engineering
entity_type: Method
sources:
- https://addyosmani.com/blog/loop-engineering/
- https://thenewstack.io/loop-engineering/
- https://arxiv.org/abs/2210.03629
- https://arxiv.org/abs/2303.11366
- https://arxiv.org/abs/2303.17651
- https://arxiv.org/abs/2307.03172
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/building-effective-agents
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Loop engineering is the deliberate design of the iterative control loop around an agent: not only what a single prompt says, but how often, how long and under which conditions an agent runs, how it keeps state, handles errors and verifies results. In its 2026 sense, loop engineering means replacing yourself as the person who prompts the agent and designing a system that finds work, hands it out, checks it, records what is done and decides the next step (Osmani, 2026b). An agent loop that was not designed still runs, only unpredictably.

### How it works

#### 1. The agent loop

```text
while not goal_reached and within_limits:
    evaluate_state()
    choose_action()
    execute_action()
    observe_result()
```

Agents are LLMs using tools based on environmental feedback in a loop; they need ground truth from the environment at each step and often use stopping conditions such as a maximum number of iterations (Anthropic, 2024a). Interleaving reasoning with actions makes the loop explicit (Yao et al., 2022; [[agentic-ai|Agentic AI]]).

#### 2. Termination

A loop needs a clear end, otherwise it can run forever or waste budget:

```text
maximum number of iterations
time limit
cost limit
convergence criterion ("no new information")
verifiable goal condition ("all tests in test/auth pass")
explicit stop signal from a human
```

A good stopping rule usually combines several criteria; an iteration limit alone prevents endless loops but not long, inefficient runs within the limit. A goal command that keeps an agent working until a verifiable condition holds, checked after every turn by a separate model, is one implementation (Osmani, 2026b).

#### 3. State and context across iterations

With each iteration the history grows. The loop design decides what is carried forward in full, what is summarised and what is dropped. Relevant information in the middle of long contexts is used less reliably than at the beginning or end (Liu et al., 2023; [[rag-chunking|RAG: Chunking]]); countermeasures are compaction, structured notes outside the context window and sub-agents with clean contexts (Anthropic, 2025a; [[context-engineering|Context Engineering]]). Memory that survives between runs lives on disk, for example in a Markdown file or an issue board, because the model forgets between runs (Osmani, 2026b).

#### 4. Error handling

A single failed step should not break the whole loop: retry with an adjusted approach, escalate to a human, or stop with an error report. Without deliberate handling, an early error propagates through later iterations and becomes harder to detect.

#### 5. Verification: separate maker and checker

Reflection loops let a model review and improve its own output: Self-Refine uses the same LLM as generator, critic and refiner and improved task performance by about 20% on average (Madaan et al., 2023); Reflexion stores verbal reflections on feedback in an episodic memory for later attempts (Shinn et al., 2023). In practice, separating the agent that writes from the agent that checks is considered the most consequential design choice, because a model grading its own output is too generous (Janakiram MSV, 2026).

#### 6. Pacing and outer loops

Not every loop should iterate as fast as possible. Loops can run on a fixed schedule, adapt their interval to how much has changed, or checkpoint their state to resume later. An outer loop in the 2026 sense combines scheduled automations for discovery and triage, isolated worktrees for parallel agents, skills with project knowledge, connectors to existing tools, sub-agents that propose and verify, and persistent memory (Osmani, 2026b; [[agent-skills|Agent Skills]]; [[mcp-and-related-protocols|MCP and Related Protocols]]). Loops can also be nested, for example when an agent starts a sub-agent with its own loop; then limits, costs and errors must be passed between the loops.

#### Origin and variants

Iterating with feedback is an old idea in agents (Yao et al., 2022; Shinn et al., 2023; Madaan et al., 2023). As a named practice, loop engineering emerged in June 2026, when Boris Cherny, head of Claude Code, said "My job is to write loops" and Addy Osmani gave the pattern its name (Janakiram MSV, 2026). It is described as one level above [[harness-engineering|Harness Engineering]] (Osmani, 2026b); the organisation of several loops or agents is discussed as [[graph-engineering|Graph Engineering]].

### When to use it

- For long-running or recurring agent work, such as daily triage of CI failures or issue backlogs.
- When a task has a verifiable end condition, such as passing tests.
- When an agent tends to stop too early, loop endlessly or drift from its goal.

### Strengths and limitations

**Strengths**
- Makes termination, state and error handling explicit design decisions instead of leaving them to model behaviour.
- Verifier agents catch failures the writing agent reasoned itself into (Janakiram MSV, 2026).
- Persistent memory lets work continue across runs (Osmani, 2026b).

**Limitations**
- Token costs vary widely, and a loop running unattended also makes mistakes unattended (Janakiram MSV, 2026).
- Comprehension debt grows when a system ships code nobody has read (Janakiram MSV, 2026; [[vibe-coding|Vibe Coding]]).
- Typical failure patterns: thrashing between the same actions, slow drift from the original goal, context exhaustion and silent error propagation.
- The practice is new; Osmani calls it early and remains sceptical (Osmani, 2026b).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Prompt engineering | Designs a single request | One-off tasks |
| Reflection loop | Model critiques and refines its own output (Madaan et al., 2023) | Improving a single result |
| Agent loop | Model chooses actions until a stop condition (Anthropic, 2024a) | Open-ended tasks |
| Outer loop (loop engineering) | System schedules, distributes and verifies agent work (Osmani, 2026b) | Recurring, autonomous work |
| Cron job | Runs a fixed script on a schedule | Deterministic recurring tasks |

### In practice

A cron job runs a fixed script, while a loop runs a model that reads the current state and chooses its next action (Janakiram MSV, 2026). A practical start is a single scheduled triage task with a verifier sub-agent, cost limits and a progress file. Loop quality is measured by task success over the whole loop, by efficiency (steps, cost, time) and by robustness to slightly changed starting conditions ([[llm-evaluation|LLM Evaluation]]); every iteration is traced and costs are attributed per run ([[llm-observability-and-tracing|LLM Observability and Tracing]]; [[llm-cost-optimization|LLM Cost Optimization]]). The loop runs inside a harness that provides tools and permissions, and it is one of the layers in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]].

### Key takeaway

Loop engineering turns termination, state, error handling and verification into explicit design decisions; the most important rules are a verifiable stop condition, a separate checker and limits on iterations and costs.

### Sources

- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Madaan, A. et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback.* NeurIPS 2023. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Loop Engineering ist die bewusste Gestaltung der iterativen Steuerschleife um einen Agenten: nicht nur, was in einem einzelnen Prompt steht, sondern wie oft, wie lange und unter welchen Bedingungen ein Agent läuft, wie er Zustand hält, Fehler behandelt und Ergebnisse prüft. Im Sinn von 2026 bedeutet Loop Engineering, sich selbst als die Person zu ersetzen, die den Agenten anstößt, und ein System zu entwerfen, das Arbeit findet, verteilt, prüft, festhält, was erledigt ist, und über den nächsten Schritt entscheidet (Osmani, 2026b). Eine nicht gestaltete Agentenschleife läuft trotzdem, nur unvorhersehbar.

### Funktionsweise

#### 1. Die Agentenschleife

```text
while not goal_reached and within_limits:
    evaluate_state()
    choose_action()
    execute_action()
    observe_result()
```

Agenten sind LLMs, die Werkzeuge auf Grundlage von Rückmeldungen aus der Umgebung in einer Schleife nutzen; sie brauchen bei jedem Schritt verlässliche Rückmeldungen aus der Umgebung und nutzen oft Abbruchbedingungen wie eine maximale Zahl an Iterationen (Anthropic, 2024a). Das Verzahnen von Überlegen und Handeln macht die Schleife ausdrücklich (Yao et al., 2022; [[agentic-ai|Agentic AI]]).

#### 2. Abbruch

Eine Schleife braucht ein klares Ende, sonst kann sie endlos laufen oder Budget verschwenden:

```text
maximale Zahl an Iterationen
Zeitlimit
Kostenlimit
Konvergenzkriterium ("keine neuen Informationen")
überprüfbare Zielbedingung ("alle Tests in test/auth bestehen")
ausdrückliches Stoppsignal eines Menschen
```

Eine gute Abbruchregel kombiniert meist mehrere Kriterien; ein reines Iterationslimit verhindert Endlosschleifen, aber keine langen, ineffizienten Läufe innerhalb des Limits. Ein Goal-Befehl, der einen Agenten weiterarbeiten lässt, bis eine überprüfbare Bedingung erfüllt ist, und der nach jedem Durchgang von einem separaten Modell geprüft wird, ist eine Umsetzung (Osmani, 2026b).

#### 3. Zustand und Kontext über Iterationen

Mit jeder Iteration wächst der Verlauf. Das Schleifendesign entscheidet, was vollständig weitergetragen, was zusammengefasst und was verworfen wird. Relevante Informationen in der Mitte langer Kontexte werden weniger zuverlässig genutzt als am Anfang oder Ende (Liu et al., 2023; [[rag-chunking|RAG: Chunking]]); Gegenmittel sind Kompaktierung, strukturierte Notizen außerhalb des Kontextfensters und Sub-Agenten mit leerem Kontext (Anthropic, 2025a; [[context-engineering|Context Engineering]]). Gedächtnis, das zwischen Läufen erhalten bleibt, liegt auf der Festplatte, etwa in einer Markdown-Datei oder einem Issue-Board, weil das Modell zwischen Läufen vergisst (Osmani, 2026b).

#### 4. Fehlerbehandlung

Ein einzelner fehlgeschlagener Schritt sollte nicht die ganze Schleife scheitern lassen: neuer Versuch mit angepasstem Ansatz, Eskalation an einen Menschen oder Abbruch mit Fehlerbericht. Ohne bewusste Behandlung pflanzt sich ein früher Fehler durch spätere Iterationen fort und wird schwerer erkennbar.

#### 5. Verifikation: Erzeugen und Prüfen trennen

Reflexionsschleifen lassen ein Modell seine eigene Ausgabe prüfen und verbessern: Self-Refine nutzt dasselbe LLM als Erzeuger, Kritiker und Überarbeiter und verbesserte die Aufgabenleistung im Mittel um etwa 20 % (Madaan et al., 2023); Reflexion speichert sprachliche Reflexionen über Rückmeldungen in einem episodischen Gedächtnis für spätere Versuche (Shinn et al., 2023). In der Praxis gilt die Trennung zwischen dem Agenten, der schreibt, und dem Agenten, der prüft, als folgenreichste Designentscheidung, weil ein Modell seine eigene Ausgabe zu wohlwollend bewertet (Janakiram MSV, 2026).

#### 6. Taktung und äußere Schleifen

Nicht jede Schleife sollte so schnell wie möglich iterieren. Schleifen können in festem Takt laufen, ihr Intervall daran anpassen, wie viel sich verändert hat, oder ihren Zustand sichern, um später fortzusetzen. Eine äußere Schleife im Sinn von 2026 verbindet zeitgesteuerte Automatisierungen für Sichtung und Triage, isolierte Worktrees für parallele Agenten, Skills mit Projektwissen, Konnektoren zu bestehenden Werkzeugen, Sub-Agenten, die vorschlagen und prüfen, und dauerhaftes Gedächtnis (Osmani, 2026b; [[agent-skills|Agent Skills]]; [[mcp-and-related-protocols|MCP und ähnliche Protokolle]]). Schleifen können auch verschachtelt sein, etwa wenn ein Agent einen Sub-Agenten mit eigener Schleife startet; dann müssen Limits, Kosten und Fehler zwischen den Schleifen weitergereicht werden.

#### Ursprung und Varianten

Iteration mit Rückmeldung ist bei Agenten eine alte Idee (Yao et al., 2022; Shinn et al., 2023; Madaan et al., 2023). Als benannte Praxis entstand Loop Engineering im Juni 2026, als Boris Cherny, Leiter von Claude Code, sagte: „My job is to write loops“, und Addy Osmani dem Muster seinen Namen gab (Janakiram MSV, 2026). Es wird als Ebene oberhalb von [[harness-engineering|Harness Engineering]] beschrieben (Osmani, 2026b); die Organisation mehrerer Loops oder Agenten wird als [[graph-engineering|Graph Engineering]] diskutiert.

### Wann einsetzen

- Für lang laufende oder wiederkehrende Agentenarbeit, etwa die tägliche Sichtung von CI-Fehlern oder Issue-Backlogs.
- Wenn eine Aufgabe eine überprüfbare Endbedingung hat, etwa bestandene Tests.
- Wenn ein Agent dazu neigt, zu früh aufzuhören, endlos zu laufen oder vom Ziel abzudriften.

### Stärken und Grenzen

**Stärken**
- Macht Abbruch, Zustand und Fehlerbehandlung zu ausdrücklichen Designentscheidungen, statt sie dem Modellverhalten zu überlassen.
- Prüfende Agenten finden Fehler, in die sich der schreibende Agent hineinargumentiert hat (Janakiram MSV, 2026).
- Dauerhaftes Gedächtnis lässt die Arbeit über mehrere Läufe weitergehen (Osmani, 2026b).

**Einschränkungen**
- Token-Kosten schwanken stark, und eine unbeaufsichtigte Schleife macht auch unbeaufsichtigt Fehler (Janakiram MSV, 2026).
- „Comprehension Debt“ wächst, wenn ein System Code ausliefert, den niemand gelesen hat (Janakiram MSV, 2026; [[vibe-coding|Vibe Coding]]).
- Typische Fehlermuster: Hin- und Herspringen zwischen denselben Aktionen, schleichendes Abdriften vom ursprünglichen Ziel, erschöpfter Kontext und stille Fehlerfortpflanzung.
- Die Praxis ist neu; Osmani hält sie selbst für früh und bleibt skeptisch (Osmani, 2026b).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Prompt Engineering | Gestaltet eine einzelne Anfrage | Einmalige Aufgaben |
| Reflexionsschleife | Modell kritisiert und überarbeitet die eigene Ausgabe (Madaan et al., 2023) | Verbesserung eines einzelnen Ergebnisses |
| Agentenschleife | Modell wählt Aktionen bis zu einer Abbruchbedingung (Anthropic, 2024a) | Offene Aufgaben |
| Äußere Schleife (Loop Engineering) | System plant, verteilt und prüft Agentenarbeit (Osmani, 2026b) | Wiederkehrende, autonome Arbeit |
| Cronjob | Führt ein festes Skript nach Zeitplan aus | Deterministische, wiederkehrende Aufgaben |

### In der Praxis

Ein Cronjob führt ein festes Skript aus, eine Schleife dagegen ein Modell, das den aktuellen Zustand liest und seine nächste Aktion wählt (Janakiram MSV, 2026). Ein praktischer Einstieg ist eine einzelne zeitgesteuerte Triage-Aufgabe mit einem prüfenden Sub-Agenten, Kostenlimits und einer Fortschrittsdatei. Die Qualität einer Schleife wird am Aufgabenerfolg über die ganze Schleife, an der Effizienz (Schritte, Kosten, Zeit) und an der Robustheit gegenüber leicht veränderten Ausgangsbedingungen gemessen ([[llm-evaluation|LLM-Evaluation]]); jede Iteration wird getraced, und Kosten werden je Lauf zugeordnet ([[llm-observability-and-tracing|LLM-Observability und Tracing]]; [[llm-cost-optimization|LLM-Kostenoptimierung]]). Die Schleife läuft innerhalb eines Harness, der Werkzeuge und Berechtigungen bereitstellt, und ist eine der Ebenen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]].

### Merksatz

Loop Engineering macht Abbruch, Zustand, Fehlerbehandlung und Verifikation zu ausdrücklichen Designentscheidungen; die wichtigsten Regeln sind eine überprüfbare Abbruchbedingung, eine getrennte prüfende Instanz und Grenzen für Iterationen und Kosten.

### Quellen

- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Madaan, A. et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback.* NeurIPS 2023. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
