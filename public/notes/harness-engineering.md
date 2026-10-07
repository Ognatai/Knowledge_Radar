---
title_en: Harness Engineering
title_de: Harness Engineering
entity_type: Method
sources:
- https://addyosmani.com/blog/agent-harness-engineering/
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/building-effective-agents
- https://arxiv.org/abs/2302.12173
- https://modelcontextprotocol.io/specification/latest/server/tools
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Harness engineering is the design of everything around a language model that turns it into a working agent: prompts and instruction files, tools and their descriptions, context policies, hooks, sandboxes, subagents, feedback loops and recovery paths (Osmani, 2026a). The short form is Agent = Model + Harness: the same model can behave very differently in two harnesses, and a decent model with a great harness beats a great model with a bad harness (Osmani, 2026a). The prompt tells the model what to do; the harness determines what it can do at all and what happens when it is wrong.

### How it works

#### 1. Model, prompt and harness

| | Model | Prompt | Harness |
|---|---|---|---|
| Changes | Weights, capabilities | A single request | Environment, tools, rules |
| Time horizon | Training | Per call | The whole session or application |
| Typical question | What can the model do at all? | What do I tell the model now? | What may the model do, and how is that enforced? |

[[prompt-engineering|Prompt Engineering]] and [[loop-engineering|Loop Engineering]] both build on a working harness.

#### 2. Components

- **Instruction files and prompts:** system prompts, AGENTS.md or CLAUDE.md files, skill files and subagent prompts (Osmani, 2026a; [[agent-skills|Agent Skills]]).
- **Tool definitions:** which tools exist and how their interfaces look; an unclear or overly broad tool definition is a harness weakness, not a prompt weakness. Tool documentation and testing form the agent-computer interface (Anthropic, 2024a).
- **Permissions:** least privilege, so that an agent can only use the tools and data its task requires.
- **Sandboxing:** code execution and file access run in an isolated environment; extensive testing in sandboxed environments with guardrails is recommended for agents (Anthropic, 2024a).
- **Context assembly:** what enters the context in each iteration, such as earlier tool results, summaries and relevant files ([[context-engineering|Context Engineering]]).
- **Output validation:** model outputs are checked against a schema before they are executed as actions.
- **Hooks and middleware:** deterministic steps such as compaction, continuation or lint checks (Osmani, 2026a).
- **Durable state:** the file system and Git give the agent a workspace, versioning and the ability to roll back (Osmani, 2026a).
- **Observability:** logs, traces and cost metering for every tool call ([[llm-observability-and-tracing|LLM Observability and Tracing]]).

#### 3. The harness as line of defence

What can be checked deterministically is enforced in the harness, not left to the model: whether a file exists is checked by code, whether a change makes sense is a semantic question for the model ([[rag-generation-evaluation|RAG: Generation Evaluation]]). Agents that read web pages or documents are exposed to indirect prompt injection, in which instructions hidden in retrieved data manipulate the application and control which APIs are called (Greshake et al., 2023); the harness can treat external content as data and require human approval for critical actions independently of the model. For tools connected via MCP, the specification asks for a human in the loop who can deny tool invocations, for validated inputs and results, timeouts and audit logs (MCP tools specification).

#### 4. The ratchet: every mistake becomes a rule

Agent failures are treated as permanent signals: a missing convention goes into AGENTS.md, a destructive command gets a blocking hook, a lost agent in a long task gets a planner–executor split, and constraints are removed when a more capable model makes them redundant (Osmani, 2026a).

#### 5. Harnesses for long-running work

Long-running agents work in sessions without memory of earlier sessions. Without structure, a coding agent tried to do too much at once, declared the job done too early or marked features as complete without end-to-end tests (Anthropic, 2025b). The described harness uses an initializer agent that writes an init script, a progress file, a JSON feature list with all features marked as failing and an initial commit; each later session reads progress and git history, runs a basic test, works on one feature, tests it end to end and ends with a commit and a progress update (Anthropic, 2025b).

#### Origin and variants

The term harness engineering was coined by Viv Trivedy and was widely discussed in 2026; products such as Claude Code, Cursor or Codex are harnesses around models (Osmani, 2026a). Earlier advice on designing tools and the agent-computer interface (Anthropic, 2024a) and harnesses for long-running agents (Anthropic, 2025b) describe the same idea; [[loop-engineering|Loop Engineering]] is described as one level above the harness.

### When to use it

- Whenever an agent may act: execute code, change files, call APIs or spend money.
- When an agent repeatedly makes the same kind of mistake.
- When a model is moved into a new environment or codebase.

### Strengths and limitations

**Strengths**
- Enforces safety and correctness deterministically instead of relying on model behaviour.
- Improvements accumulate: each fixed failure stays fixed (Osmani, 2026a).
- Makes agent behaviour traceable through logs and version history.

**Limitations**
- A harness is shaped by the failure history of a specific codebase and cannot simply be downloaded (Osmani, 2026a).
- Effective defences against indirect prompt injection are still lacking (Greshake et al., 2023).
- More rules and tools also mean more context and maintenance; too many or overlapping tools confuse the agent ([[context-engineering|Context Engineering]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Prompt engineering | Changes what the model is told | Single requests |
| Context engineering | Curates what the model sees | Long tasks and large inputs |
| Harness engineering | Defines tools, permissions, checks and recovery (Osmani, 2026a) | Agents that act in real environments |
| Loop engineering | Designs the system that prompts the agent over time ([[loop-engineering|Loop Engineering]]) | Recurring, autonomous work |

### In practice

A coding agent's harness might look like this:

```text
tools:       read file, write file, run shell command
permission:  write access only inside the project directory
sandbox:     isolated working directory (e.g. a Git worktree or container)
validation:  diff shown and confirmed before it is applied
logging:     every tool call recorded
recovery:    commits after each step, so bad changes can be reverted
```

Containers isolate execution ([[docker|Docker]]), tools often come from MCP servers ([[mcp-and-related-protocols|MCP and Related Protocols]]), and the same harness principles apply to agents in general ([[agentic-ai|Agentic AI]]), to working styles such as [[vibe-coding|Vibe Coding]] and to multi-agent setups ([[graph-engineering|Graph Engineering]]). Robustness is tested with varied inputs ([[llm-evaluation|LLM Evaluation]]), costs are capped ([[llm-cost-optimization|LLM Cost Optimization]]), and the discipline sits among the others described in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]]; background on the models themselves is in [[large-language-models|Large Language Models]]. Tools usually wrap existing [[apis|APIs]], so their permissions and error handling become part of the harness.

### Key takeaway

The prompt tells the model what it should do; the harness determines what it can do, checks what it did and decides what happens when it is wrong.

### Sources

- Osmani, A. (2026). *Agent Harness Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/agent-harness-engineering/)
- Young, J. (2025). *Effective harnesses for long-running agents.* Anthropic Engineering, 26 November 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Model Context Protocol. *Specification: Tools.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/latest/server/tools)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Harness Engineering ist die Gestaltung von allem rund um ein Sprachmodell, das es zu einem funktionierenden Agenten macht: Prompts und Anweisungsdateien, Werkzeuge und ihre Beschreibungen, Kontextregeln, Hooks, Sandboxes, Sub-Agenten, Rückkopplungsschleifen und Wiederherstellungswege (Osmani, 2026a). Die Kurzform lautet Agent = Modell + Harness: Dasselbe Modell kann sich in zwei Harnessen sehr unterschiedlich verhalten, und ein ordentliches Modell mit einem sehr guten Harness schlägt ein sehr gutes Modell mit einem schlechten Harness (Osmani, 2026a). Der Prompt sagt dem Modell, was es tun soll; der Harness bestimmt, was es überhaupt tun kann und was passiert, wenn es sich irrt.

### Funktionsweise

#### 1. Modell, Prompt und Harness

| | Modell | Prompt | Harness |
|---|---|---|---|
| Verändert | Gewichte, Fähigkeiten | Eine einzelne Anfrage | Umgebung, Werkzeuge, Regeln |
| Zeithorizont | Training | Pro Aufruf | Gesamte Sitzung oder Anwendung |
| Typische Frage | Was kann das Modell grundsätzlich? | Was sage ich dem Modell jetzt? | Was darf das Modell, und wie wird das durchgesetzt? |

[[prompt-engineering|Prompt Engineering]] und [[loop-engineering|Loop Engineering]] setzen beide auf einem funktionierenden Harness auf.

#### 2. Bausteine

- **Anweisungsdateien und Prompts:** Systemprompts, AGENTS.md- oder CLAUDE.md-Dateien, Skill-Dateien und Prompts für Sub-Agenten (Osmani, 2026a; [[agent-skills|Agent Skills]]).
- **Werkzeugdefinitionen:** welche Werkzeuge es gibt und wie ihre Schnittstellen aussehen; eine unklare oder zu weit gefasste Werkzeugdefinition ist eine Schwäche des Harness, nicht des Prompts. Dokumentation und Tests der Werkzeuge bilden die Schnittstelle zwischen Agent und Computer (Anthropic, 2024a).
- **Berechtigungen:** Least Privilege, sodass ein Agent nur die Werkzeuge und Daten nutzen kann, die seine Aufgabe erfordert.
- **Sandboxing:** Codeausführung und Dateizugriffe laufen in einer isolierten Umgebung; für Agenten werden ausführliche Tests in Sandbox-Umgebungen mit Guardrails empfohlen (Anthropic, 2024a).
- **Kontextaufbau:** was in jeder Iteration in den Kontext gelangt, etwa frühere Werkzeugergebnisse, Zusammenfassungen und relevante Dateien ([[context-engineering|Context Engineering]]).
- **Ausgabevalidierung:** Modellausgaben werden gegen ein Schema geprüft, bevor sie als Aktion ausgeführt werden.
- **Hooks und Middleware:** deterministische Schritte wie Kompaktierung, Fortsetzung oder Lint-Prüfungen (Osmani, 2026a).
- **Dauerhafter Zustand:** Dateisystem und Git geben dem Agenten einen Arbeitsbereich, Versionierung und die Möglichkeit zurückzurollen (Osmani, 2026a).
- **Observability:** Logs, Traces und Kostenmessung für jeden Werkzeugaufruf ([[llm-observability-and-tracing|LLM-Observability und Tracing]]).

#### 3. Der Harness als Verteidigungslinie

Was sich deterministisch prüfen lässt, wird im Harness erzwungen und nicht dem Modell überlassen: Ob eine Datei existiert, prüft Code; ob eine Änderung sinnvoll ist, ist eine semantische Frage für das Modell ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]). Agenten, die Webseiten oder Dokumente lesen, sind indirekter Prompt Injection ausgesetzt, bei der in abgerufenen Daten versteckte Anweisungen die Anwendung manipulieren und steuern, welche APIs aufgerufen werden (Greshake et al., 2023); der Harness kann externe Inhalte als Daten behandeln und für kritische Aktionen unabhängig vom Modell eine menschliche Freigabe verlangen. Für über MCP angebundene Werkzeuge verlangt die Spezifikation einen Menschen im Prozess, der Werkzeugaufrufe ablehnen kann, sowie validierte Eingaben und Ergebnisse, Timeouts und Audit-Logs (MCP tools specification).

#### 4. Die Ratsche: Jeder Fehler wird zur Regel

Fehler des Agenten gelten als dauerhafte Signale: Eine fehlende Konvention kommt in die AGENTS.md, ein destruktiver Befehl erhält einen blockierenden Hook, ein Agent, der sich in einer langen Aufgabe verliert, eine Trennung von Planer und Ausführer, und Einschränkungen werden entfernt, sobald ein leistungsfähigeres Modell sie überflüssig macht (Osmani, 2026a).

#### 5. Harnesse für lang laufende Arbeit

Lang laufende Agenten arbeiten in Sitzungen ohne Erinnerung an frühere Sitzungen. Ohne Struktur versuchte ein Coding-Agent, zu viel auf einmal zu erledigen, erklärte die Arbeit zu früh für fertig oder markierte Features ohne End-to-End-Tests als erledigt (Anthropic, 2025b). Der beschriebene Harness nutzt einen Initialisierungs-Agenten, der ein Init-Skript, eine Fortschrittsdatei, eine JSON-Featureliste mit allen Features als „nicht bestanden“ und einen ersten Commit anlegt; jede spätere Sitzung liest Fortschritt und Git-Historie, führt einen Basistest aus, arbeitet an einem Feature, testet es End-to-End und endet mit einem Commit und einer Fortschrittsnotiz (Anthropic, 2025b).

#### Ursprung und Varianten

Der Begriff Harness Engineering wurde von Viv Trivedy geprägt und 2026 breit diskutiert; Produkte wie Claude Code, Cursor oder Codex sind Harnesse um Modelle (Osmani, 2026a). Frühere Empfehlungen zur Gestaltung von Werkzeugen und der Schnittstelle zwischen Agent und Computer (Anthropic, 2024a) und Harnesse für lang laufende Agenten (Anthropic, 2025b) beschreiben dieselbe Idee; [[loop-engineering|Loop Engineering]] wird als Ebene oberhalb des Harness beschrieben.

### Wann einsetzen

- Immer, wenn ein Agent handeln darf: Code ausführen, Dateien ändern, APIs aufrufen oder Geld ausgeben.
- Wenn ein Agent wiederholt dieselbe Art von Fehler macht.
- Wenn ein Modell in eine neue Umgebung oder Codebasis übertragen wird.

### Stärken und Grenzen

**Stärken**
- Erzwingt Sicherheit und Korrektheit deterministisch, statt sich auf das Modellverhalten zu verlassen.
- Verbesserungen summieren sich: Jeder behobene Fehler bleibt behoben (Osmani, 2026a).
- Macht das Verhalten des Agenten über Logs und Versionsgeschichte nachvollziehbar.

**Einschränkungen**
- Ein Harness wird von der Fehlergeschichte einer konkreten Codebasis geprägt und lässt sich nicht einfach herunterladen (Osmani, 2026a).
- Wirksame Abwehrmaßnahmen gegen indirekte Prompt Injection fehlen bislang (Greshake et al., 2023).
- Mehr Regeln und Werkzeuge bedeuten auch mehr Kontext und Pflegeaufwand; zu viele oder sich überschneidende Werkzeuge verwirren den Agenten ([[context-engineering|Context Engineering]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Prompt Engineering | Verändert, was dem Modell gesagt wird | Einzelne Anfragen |
| Context Engineering | Wählt aus, was das Modell sieht | Lange Aufgaben und große Eingaben |
| Harness Engineering | Legt Werkzeuge, Berechtigungen, Prüfungen und Wiederherstellung fest (Osmani, 2026a) | Agenten, die in realen Umgebungen handeln |
| Loop Engineering | Gestaltet das System, das den Agenten über die Zeit anstößt ([[loop-engineering|Loop Engineering]]) | Wiederkehrende, autonome Arbeit |

### In der Praxis

Der Harness eines Coding-Agenten kann so aussehen:

```text
Werkzeuge:      Datei lesen, Datei schreiben, Shell-Befehl ausführen
Berechtigung:   Schreibzugriff nur im Projektverzeichnis
Sandbox:        isoliertes Arbeitsverzeichnis (z. B. Git-Worktree oder Container)
Validierung:    Diff wird vor dem Anwenden angezeigt und bestätigt
Logging:        jeder Werkzeugaufruf wird protokolliert
Wiederherstellung: Commit nach jedem Schritt, sodass schlechte Änderungen rückgängig gemacht werden können
```

Container isolieren die Ausführung ([[docker|Docker]]), Werkzeuge stammen oft von MCP-Servern ([[mcp-and-related-protocols|MCP und ähnliche Protokolle]]), und dieselben Prinzipien gelten für Agenten allgemein ([[agentic-ai|Agentic AI]]), für Arbeitsweisen wie [[vibe-coding|Vibe Coding]] und für Multi-Agenten-Setups ([[graph-engineering|Graph Engineering]]). Die Robustheit wird mit variierten Eingaben getestet ([[llm-evaluation|LLM-Evaluation]]), Kosten werden begrenzt ([[llm-cost-optimization|LLM-Kostenoptimierung]]), und die Disziplin steht neben den anderen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]] beschriebenen; Hintergrund zu den Modellen selbst bietet [[large-language-models|Large Language Models]]. Werkzeuge kapseln meist bestehende [[apis|APIs (Programmierschnittstellen)]], sodass deren Berechtigungen und Fehlerbehandlung Teil des Harness werden.

### Merksatz

Der Prompt sagt dem Modell, was es tun soll; der Harness bestimmt, was es tun kann, prüft, was es getan hat, und legt fest, was passiert, wenn es sich irrt.

### Quellen

- Osmani, A. (2026). *Agent Harness Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/agent-harness-engineering/)
- Young, J. (2025). *Effective harnesses for long-running agents.* Anthropic Engineering, 26 November 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Model Context Protocol. *Specification: Tools.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/latest/server/tools)
