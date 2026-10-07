---
title_en: Engineering Methods for AI Systems
title_de: Engineering-Methoden für KI-Systeme
entity_type: Concept
sources:
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://addyosmani.com/blog/agent-harness-engineering/
- https://addyosmani.com/blog/loop-engineering/
- https://thenewstack.io/loop-engineering/
- https://simonwillison.net/2025/Mar/19/vibe-coding/
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2211.03622
- https://arxiv.org/abs/2507.09089
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Around LLMs and agents, several "engineering" disciplines have emerged, each addressing a different layer of the same system: the prompt, the context, skills, protocols, the agent loop, the organisation of several agents, the harness and the day-to-day way of working. Practitioners describe a sequence from prompt engineering to context engineering, harness engineering and loop engineering within fewer than 18 months (Janakiram MSV, 2026). The practical value of the layers is diagnostic: when an AI-supported process fails, the first question is on which layer the problem lies, because solving it on the wrong layer, for example a harness problem with a prompt, works unreliably at best.

### How it works

#### 1. The layers

```text
model     → what capabilities exist at all?                     (training)
prompt    → what is the model told in this moment?              Prompt Engineering
context   → what is in the context window, in which form?       Context Engineering
skills    → which procedural knowledge is loaded on demand?     Agent Skills
protocol  → how are tools and data connected?                   MCP
loop      → how often, how long, under which conditions?        Loop Engineering
graph     → how are several agents or loops organised?          Graph Engineering
harness   → what may the model do, how is it limited and checked? Harness Engineering
practice  → what does daily work with it look like?             Vibe Coding
```

The order is not a ranking; depending on the problem, the most effective lever is on a different layer.

#### 2. The disciplines

- **[[prompt-engineering|Prompt Engineering]]:** wording a single instruction, with zero- or few-shot examples, chain of thought and structured output formats.
- **[[context-engineering|Context Engineering]]:** curating everything that enters the limited context window, including system prompt, tools, retrieved data and message history; as the context grows, recall decreases, so the goal is the smallest set of high-signal tokens (Anthropic, 2025a).
- **[[agent-skills|Agent Skills]]:** packaged procedural knowledge that is fully loaded only when needed.
- **[[mcp-and-related-protocols|MCP and Related Protocols]]:** standardised connection of tools, data and prompt templates.
- **[[loop-engineering|Loop Engineering]]:** designing the system that prompts the agent, with schedules, verifiers and memory (Osmani, 2026b).
- **[[graph-engineering|Graph Engineering]]:** an emerging and inconsistently used term for organising several agents or loops.
- **[[harness-engineering|Harness Engineering]]:** everything around the model, such as tools, permissions, sandboxes, hooks and observability; Agent = Model + Harness (Osmani, 2026a).
- **[[vibe-coding|Vibe Coding]]:** building software with an LLM without reviewing the code it writes (Willison, 2025).

Two topics cut across all layers: [[llm-cost-optimization|LLM Cost Optimization]] and [[llm-observability-and-tracing|LLM Observability and Tracing]].

#### 3. Example: a coding agent

```text
task: "Fix the bug in the checkout flow"

prompt    → is the task clear, with a success criterion?
context   → which files, error messages and tests are loaded?
skills    → does a debugging or testing skill apply?
protocol  → how does the agent reach repository, ticket system and CI (MCP)?
loop      → how often does it test hypotheses before stopping or escalating?
harness   → which files may it change, is the diff shown before it is applied?
practice  → is the result verified by tests rather than by reading every line?
```

#### Origin and variants

The labels follow each other quickly: prompt engineering, then context engineering as its progression (Anthropic, 2025a), then harness engineering (Osmani, 2026a) and loop engineering, named in June 2026 (Janakiram MSV, 2026). The underlying advice is older and stable: start with the simplest solution and add complexity only when it demonstrably improves outcomes (Anthropic, 2024a).

### When to use it

- When an AI-supported process does not work as expected and the cause must be located.
- When designing a new agent system, to decide deliberately on each layer.
- When teams discuss AI tooling and need a shared vocabulary.

### Strengths and limitations

**Strengths**
- Separates concerns, so that fixes target the right component.
- Connects new terms to established software practices such as testing, version control and least privilege.

**Limitations**
- The terms are young and change quickly; several, especially graph engineering, are used inconsistently.
- Layers overlap: skills are a context technique, MCP servers are part of the harness.
- The evidence base is mostly practitioner reports rather than systematic studies.

### Comparison

| Layer | Changes | Typical question |
|----------|----------------|------------|
| Model | Weights, capabilities | What can the model do at all? |
| Prompt | A single request | What do I tell the model now? |
| Context | The whole context window (Anthropic, 2025a) | What does the model see, and in which order? |
| Loop | The process over many requests (Osmani, 2026b) | When does it continue, stop or escalate? |
| Harness | Environment, tools, rules (Osmani, 2026a) | What may the model do, and how is that enforced? |

### In practice

Best practices for AI-assisted programming follow from the layers:

- **Formulate tasks clearly and verifiably:** goal, success criterion and constraints before implementation.
- **Verification before trust:** automated tests and actual execution, in small, checkable steps; for coding agents, tests verify functionality, but human review remains crucial (Anthropic, 2024a).
- **Curate context instead of maximising it:** relevant information in the middle of long contexts is used less reliably than at the beginning or end (Liu et al., 2023), and recurring procedures belong in a skill ([[rag-failure-modes|RAG: Failure Modes]]).
- **Set permissions deliberately:** least privilege, and human approval for critical or hard-to-reverse actions ([[agentic-ai|Agentic AI]]).
- **Limit iteration:** iteration, time or cost limits and convergence criteria.
- **Software fundamentals remain mandatory:** in a user study, participants with an AI code assistant wrote significantly less secure code but were more likely to believe it was secure (Perry et al., 2022), and in a randomised trial, experienced open-source developers took 19% longer with early-2025 AI tools although they believed they had been faster (Becker et al., 2025). Judging architecture, test coverage and security becomes more important, not less.
- **Maintain documentation and memory:** project conventions and known pitfalls belong in maintained files, not in every single request.

Further background: [[large-language-models|Large Language Models]].

### Key takeaway

When an AI-supported process does not work, first ask on which layer the problem lies, whether prompt, context, skills, protocol, loop, harness or practice; the answer determines which lever actually works.

### Sources

- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Osmani, A. (2026). *Agent Harness Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/agent-harness-engineering/)
- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Willison, S. (2025). *Not all AI-assisted programming is vibe coding (but vibe coding rocks).* Simon Willison's Weblog, 19 March 2025. [simonwillison.net](https://simonwillison.net/2025/Mar/19/vibe-coding/)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Perry, N. et al. (2022). *Do Users Write More Insecure Code with AI Assistants?* ACM CCS 2023. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622)
- Becker, J. et al. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Rund um LLMs und Agenten sind mehrere „Engineering“-Disziplinen entstanden, die jeweils eine andere Ebene desselben Systems behandeln: den Prompt, den Kontext, Skills, Protokolle, die Agentenschleife, die Organisation mehrerer Agenten, den Harness und die tägliche Arbeitsweise. In der Praxis wird eine Abfolge von Prompt Engineering über Context Engineering und Harness Engineering bis Loop Engineering in weniger als 18 Monaten beschrieben (Janakiram MSV, 2026). Der praktische Wert der Ebenen liegt in der Diagnose: Scheitert ein KI-gestützter Prozess, lautet die erste Frage, auf welcher Ebene das Problem liegt, denn ein Problem auf der falschen Ebene zu lösen, etwa ein Harness-Problem per Prompt, funktioniert bestenfalls unzuverlässig.

### Funktionsweise

#### 1. Die Ebenen

```text
Modell     → welche Fähigkeiten sind grundsätzlich vorhanden?           (Training)
Prompt     → was wird dem Modell in diesem Moment gesagt?               Prompt Engineering
Kontext    → was steht im Kontextfenster, in welcher Form?              Context Engineering
Skills     → welches Verfahrenswissen wird bei Bedarf geladen?          Agent Skills
Protokoll  → wie werden Werkzeuge und Daten angebunden?                 MCP
Loop       → wie oft, wie lange, unter welchen Bedingungen?             Loop Engineering
Graph      → wie sind mehrere Agenten oder Loops organisiert?           Graph Engineering
Harness    → was darf das Modell, wie wird es begrenzt und geprüft?     Harness Engineering
Praxis     → wie sieht die tägliche Arbeit damit aus?                   Vibe Coding
```

Die Reihenfolge ist keine Rangfolge; je nach Problem liegt der wirksamste Hebel auf einer anderen Ebene.

#### 2. Die Disziplinen

- **[[prompt-engineering|Prompt Engineering]]:** Formulierung einer einzelnen Anweisung, mit Zero- oder Few-Shot-Beispielen, Chain of Thought und strukturierten Ausgabeformaten.
- **[[context-engineering|Context Engineering]]:** Auswahl von allem, was in das begrenzte Kontextfenster gelangt, einschließlich Systemprompt, Werkzeugen, abgerufenen Daten und Verlauf; mit wachsendem Kontext sinkt die Erinnerungsleistung, Ziel ist daher die kleinste Menge aussagekräftiger Token (Anthropic, 2025a).
- **[[agent-skills|Agent Skills]]:** verpacktes Verfahrenswissen, das erst bei Bedarf vollständig geladen wird.
- **[[mcp-and-related-protocols|MCP und ähnliche Protokolle]]:** standardisierte Anbindung von Werkzeugen, Daten und Prompt-Vorlagen.
- **[[loop-engineering|Loop Engineering]]:** Gestaltung des Systems, das den Agenten anstößt, mit Zeitplänen, prüfenden Agenten und Gedächtnis (Osmani, 2026b).
- **[[graph-engineering|Graph Engineering]]:** ein aufkommender, uneinheitlich verwendeter Begriff für die Organisation mehrerer Agenten oder Loops.
- **[[harness-engineering|Harness Engineering]]:** alles rund um das Modell, etwa Werkzeuge, Berechtigungen, Sandboxes, Hooks und Observability; Agent = Modell + Harness (Osmani, 2026a).
- **[[vibe-coding|Vibe Coding]]:** Software mit einem LLM bauen, ohne den erzeugten Code zu prüfen (Willison, 2025).

Zwei Themen liegen quer zu allen Ebenen: [[llm-cost-optimization|LLM-Kostenoptimierung]] und [[llm-observability-and-tracing|LLM-Observability und Tracing]].

#### 3. Beispiel: ein Coding-Agent

```text
Aufgabe: "Behebe den Bug im Checkout-Flow"

Prompt     → ist die Aufgabe klar, mit Erfolgskriterium?
Kontext    → welche Dateien, Fehlermeldungen und Tests werden geladen?
Skills     → greift ein Debugging- oder Testing-Skill?
Protokoll  → wie erreicht der Agent Repository, Ticketsystem und CI (MCP)?
Loop       → wie oft testet er Hypothesen, bevor er abbricht oder eskaliert?
Harness    → welche Dateien darf er ändern, wird der Diff vor dem Anwenden gezeigt?
Praxis     → wird das Ergebnis über Tests geprüft statt jede Zeile zu lesen?
```

#### Ursprung und Varianten

Die Begriffe folgen schnell aufeinander: Prompt Engineering, dann Context Engineering als dessen Weiterentwicklung (Anthropic, 2025a), dann Harness Engineering (Osmani, 2026a) und Loop Engineering, benannt im Juni 2026 (Janakiram MSV, 2026). Der zugrunde liegende Rat ist älter und stabil: mit der einfachsten Lösung beginnen und Komplexität nur ergänzen, wenn sie die Ergebnisse nachweislich verbessert (Anthropic, 2024a).

### Wann einsetzen

- Wenn ein KI-gestützter Prozess nicht wie erwartet funktioniert und die Ursache gefunden werden muss.
- Beim Entwurf eines neuen Agentensystems, um auf jeder Ebene bewusst zu entscheiden.
- Wenn Teams über KI-Werkzeuge sprechen und ein gemeinsames Vokabular brauchen.

### Stärken und Grenzen

**Stärken**
- Trennt Zuständigkeiten, sodass Korrekturen die richtige Komponente treffen.
- Verbindet neue Begriffe mit etablierten Softwarepraktiken wie Tests, Versionskontrolle und Least Privilege.

**Einschränkungen**
- Die Begriffe sind jung und ändern sich schnell; mehrere, besonders Graph Engineering, werden uneinheitlich verwendet.
- Die Ebenen überschneiden sich: Skills sind eine Kontexttechnik, MCP-Server Teil des Harness.
- Die Belege stammen überwiegend aus Praxisberichten, nicht aus systematischen Studien.

### Vergleich

| Ebene | Verändert | Typische Frage |
|----------|----------------|------------|
| Modell | Gewichte, Fähigkeiten | Was kann das Modell grundsätzlich? |
| Prompt | Eine einzelne Anfrage | Was sage ich dem Modell jetzt? |
| Kontext | Das gesamte Kontextfenster (Anthropic, 2025a) | Was sieht das Modell, in welcher Reihenfolge? |
| Loop | Den Prozess über viele Anfragen (Osmani, 2026b) | Wann geht es weiter, wann wird abgebrochen oder eskaliert? |
| Harness | Umgebung, Werkzeuge, Regeln (Osmani, 2026a) | Was darf das Modell, und wie wird das durchgesetzt? |

### In der Praxis

Aus den Ebenen folgen Best Practices für KI-gestütztes Programmieren:

- **Aufgaben klar und überprüfbar formulieren:** Ziel, Erfolgskriterium und Randbedingungen vor der Umsetzung.
- **Verifikation vor Vertrauen:** automatisierte Tests und tatsächliches Ausführen, in kleinen, prüfbaren Schritten; bei Coding-Agenten prüfen Tests die Funktion, die menschliche Prüfung bleibt aber entscheidend (Anthropic, 2024a).
- **Kontext kuratieren statt maximieren:** Relevante Informationen in der Mitte langer Kontexte werden weniger zuverlässig genutzt als am Anfang oder Ende (Liu et al., 2023), und wiederkehrende Abläufe gehören in einen Skill ([[rag-failure-modes|RAG: Typische Fehlerarten]]).
- **Berechtigungen bewusst setzen:** Least Privilege und menschliche Freigabe für kritische oder schwer umkehrbare Aktionen ([[agentic-ai|Agentic AI]]).
- **Iteration begrenzen:** Iterations-, Zeit- oder Kostenlimits und Konvergenzkriterien.
- **Software-Grundlagen bleiben Pflicht:** In einer Nutzerstudie schrieben Teilnehmende mit KI-Code-Assistent deutlich unsichereren Code, hielten ihn aber eher für sicher (Perry et al., 2022), und in einer randomisierten Studie brauchten erfahrene Open-Source-Entwickler:innen mit KI-Werkzeugen von Anfang 2025 19 % länger, obwohl sie glaubten, schneller gewesen zu sein (Becker et al., 2025). Architektur, Testabdeckung und Sicherheit beurteilen zu können, wird wichtiger, nicht unwichtiger.
- **Dokumentation und Gedächtnis pflegen:** Projektkonventionen und bekannte Stolperfallen gehören in gepflegte Dateien, nicht in jede einzelne Anfrage.

Weiterer Hintergrund: [[large-language-models|Large Language Models]].

### Merksatz

Funktioniert ein KI-gestützter Prozess nicht, zuerst fragen, auf welcher Ebene das Problem liegt, ob Prompt, Kontext, Skills, Protokoll, Loop, Harness oder Praxis; die Antwort bestimmt, welcher Hebel tatsächlich wirkt.

### Quellen

- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Osmani, A. (2026). *Agent Harness Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/agent-harness-engineering/)
- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Willison, S. (2025). *Not all AI-assisted programming is vibe coding (but vibe coding rocks).* Simon Willison's Weblog, 19 March 2025. [simonwillison.net](https://simonwillison.net/2025/Mar/19/vibe-coding/)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Perry, N. et al. (2022). *Do Users Write More Insecure Code with AI Assistants?* ACM CCS 2023. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622)
- Becker, J. et al. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)
