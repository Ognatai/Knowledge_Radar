---
title_en: Agent Skills
title_de: Agent Skills
entity_type: Concept
sources:
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://agentskills.io/specification
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://addyosmani.com/blog/loop-engineering/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Agent Skills are organised folders of instructions, scripts and resources that an agent discovers and loads dynamically to perform better at specific tasks (Anthropic, 2025c). A skill is a directory with a SKILL.md file whose YAML frontmatter contains a name and a description (Agent Skills specification). Only names and descriptions are permanently in the context; the full instructions and bundled files are loaded when a task needs them. A tool tells the model what it can do; a skill tells it how a particular task is done, and it costs context only when it is used.

### How it works

#### 1. Progressive disclosure

```text
startup:   system prompt contains name + description of every installed skill   (level 1)
task:      agent recognises "this matches skill X" and reads SKILL.md           (level 2)
as needed: agent reads further files bundled with the skill, e.g. forms.md       (level 3+)
```

Because agents with a file system and code execution read further files only when needed, the amount of context that can be bundled into a skill is effectively unbounded (Anthropic, 2025c). This implements the principle of keeping the context small and loading information just in time ([[context-engineering|Context Engineering]]; Anthropic, 2025a).

#### 2. Structure of a skill

```text
pdf-processing/
├── SKILL.md        # required: YAML frontmatter + Markdown instructions
├── scripts/        # optional: executable code
├── references/     # optional: further documentation
└── assets/         # optional: templates, resources
```

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills PDF forms and merges PDFs. Use when working with PDF documents or forms.
---
# PDF processing
1. Run scripts/extract_fields.py to list form fields.
2. ...
```

The name has 1 to 64 lowercase letters, numbers and hyphens and matches the directory; the description, up to 1024 characters, says what the skill does and when to use it, with keywords that help the agent recognise relevant tasks. Optional fields are license, compatibility, metadata and an experimental list of pre-approved tools (Agent Skills specification).

#### 3. Code in skills

Skills can include scripts that the agent runs instead of generating the result token by token: sorting a list by generation is far more expensive than running a sorting algorithm, and code is deterministic and repeatable. A PDF skill can, for example, run a script that extracts all form fields without loading the script or the PDF into context (Anthropic, 2025c).

#### 4. Writing good skills

Start with evaluation: run the agent on representative tasks, observe where it struggles and build skills for these gaps; split large skills into separate files; pay special attention to name and description, because the agent decides on that basis whether to use a skill; and let the agent capture successful approaches and common mistakes into the skill (Anthropic, 2025c). A vague description makes the agent overlook a suitable skill; an overly broad one triggers it too often.

#### Origin and variants

Anthropic introduced Agent Skills in October 2025 and published them as an open standard in December 2025 (Anthropic, 2025c); the format is described in the specification (Agent Skills specification). By 2026, both Claude Code and Codex use the same SKILL.md format, and skills are one of the building blocks of agent loops, used to codify project knowledge that the agent would otherwise guess (Osmani, 2026b).

### When to use it

- For recurring procedures with project-specific conventions, such as release steps, document formats or review checklists.
- When a system prompt grows because it contains instructions for many different tasks.
- When deterministic steps can be delegated to scripts.

### Strengths and limitations

**Strengths**
- Saves context: only short descriptions are always loaded (Anthropic, 2025c).
- Skills can be maintained, versioned and reused independently instead of editing one monolithic system prompt.
- Bundled scripts make steps deterministic and cheap (Anthropic, 2025c).

**Limitations**
- The agent must recognise when a skill applies; this depends on the quality of the description (Agent Skills specification).
- Malicious skills can introduce vulnerabilities or direct the agent to exfiltrate data; skills should come from trusted sources and be audited otherwise (Anthropic, 2025c).
- Support for optional fields such as pre-approved tools varies between agent implementations (Agent Skills specification).

### Comparison

| Concept | Provides | Triggered by |
|----------|----------------|------------|
| Tool | A single callable function | The model's decision per call |
| Skill | Procedural knowledge for a whole workflow, possibly with scripts (Anthropic, 2025c) | Recognised relevance to the current task |
| MCP server | Transport of tools, resources and prompts ([[mcp-and-related-protocols|MCP and Related Protocols]]) | A connection to the server |
| Long system prompt | All instructions at once | Every request, whether relevant or not |

### In practice

Skills complement MCP servers: MCP connects capabilities, skills describe how to use them in a particular workflow (Anthropic, 2025c). A large system prompt with instructions for every case would occupy context on every request and pollute it with irrelevant material ([[rag-failure-modes|RAG: Failure Modes]]); skills replace it with short descriptions ([[prompt-engineering|Prompt Engineering]]). The harness decides which skills are available and with which rights their scripts run ([[harness-engineering|Harness Engineering]]), skills reduce token costs ([[llm-cost-optimization|LLM Cost Optimization]]), and their use is traced like any tool call ([[llm-observability-and-tracing|LLM Observability and Tracing]]). They are one of the layers in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]], used in agents ([[agentic-ai|Agentic AI]]), loops ([[loop-engineering|Loop Engineering]]), multi-agent systems ([[graph-engineering|Graph Engineering]]) and everyday AI-assisted coding ([[vibe-coding|Vibe Coding]]).

### Key takeaway

A skill is knowledge that waits until it is needed: a short description is always visible, the full instructions and scripts are loaded only when the task requires them.

### Sources

- Zhang, B., Lazuka, K. & Murag, M. (2025). *Equipping agents for the real world with Agent Skills.* Anthropic Engineering, 16 October 2025. [anthropic.com](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- Agent Skills. *Specification.* agentskills.io. [agentskills.io](https://agentskills.io/specification)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Agent Skills sind geordnete Ordner mit Anweisungen, Skripten und Ressourcen, die ein Agent selbstständig entdeckt und bei Bedarf lädt, um bestimmte Aufgaben besser zu erledigen (Anthropic, 2025c). Ein Skill ist ein Verzeichnis mit einer Datei SKILL.md, deren YAML-Frontmatter einen Namen und eine Beschreibung enthält (Agent Skills specification). Dauerhaft im Kontext stehen nur Namen und Beschreibungen; die vollständigen Anweisungen und beigelegten Dateien werden geladen, wenn eine Aufgabe sie braucht. Ein Werkzeug sagt dem Modell, was es tun kann; ein Skill sagt ihm, wie eine bestimmte Aufgabe erledigt wird, und kostet erst dann Kontext, wenn er genutzt wird.

### Funktionsweise

#### 1. Progressive Disclosure

```text
Start:        Systemprompt enthält Name + Beschreibung jedes installierten Skills   (Stufe 1)
Aufgabe:      Agent erkennt "das passt zu Skill X" und liest SKILL.md               (Stufe 2)
bei Bedarf:   Agent liest weitere Dateien des Skills, z. B. forms.md                (Stufe 3+)
```

Weil Agenten mit Dateisystem und Codeausführung weitere Dateien nur bei Bedarf lesen, ist die Menge an Kontext, die sich in einem Skill bündeln lässt, praktisch unbegrenzt (Anthropic, 2025c). Damit wird das Prinzip umgesetzt, den Kontext klein zu halten und Informationen erst zum benötigten Zeitpunkt zu laden ([[context-engineering|Context Engineering]]; Anthropic, 2025a).

#### 2. Aufbau eines Skills

```text
pdf-processing/
├── SKILL.md        # Pflicht: YAML-Frontmatter + Markdown-Anweisungen
├── scripts/        # optional: ausführbarer Code
├── references/     # optional: weitere Dokumentation
└── assets/         # optional: Vorlagen, Ressourcen
```

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills PDF forms and merges PDFs. Use when working with PDF documents or forms.
---
# PDF processing
1. Run scripts/extract_fields.py to list form fields.
2. ...
```

Der Name besteht aus 1 bis 64 Kleinbuchstaben, Ziffern und Bindestrichen und entspricht dem Verzeichnisnamen; die Beschreibung mit bis zu 1024 Zeichen sagt, was der Skill tut und wann er einzusetzen ist, mit Schlüsselwörtern, an denen der Agent passende Aufgaben erkennt. Optionale Felder sind license, compatibility, metadata und eine experimentelle Liste vorab freigegebener Werkzeuge (Agent Skills specification).

#### 3. Code in Skills

Skills können Skripte enthalten, die der Agent ausführt, statt das Ergebnis Token für Token zu erzeugen: Eine Liste per Generierung zu sortieren, ist weit teurer, als einen Sortieralgorithmus auszuführen, und Code ist deterministisch und wiederholbar. Ein PDF-Skill kann etwa ein Skript ausführen, das alle Formularfelder ausliest, ohne Skript oder PDF in den Kontext zu laden (Anthropic, 2025c).

#### 4. Gute Skills schreiben

Mit Evaluation beginnen: den Agenten an repräsentativen Aufgaben arbeiten lassen, beobachten, wo er scheitert, und für diese Lücken Skills bauen; große Skills auf mehrere Dateien aufteilen; besonders auf Name und Beschreibung achten, weil der Agent danach entscheidet, ob er einen Skill nutzt; und den Agenten erfolgreiche Vorgehensweisen und typische Fehler in den Skill übernehmen lassen (Anthropic, 2025c). Eine vage Beschreibung führt dazu, dass ein passender Skill übersehen wird, eine zu weit gefasste dazu, dass er zu oft anspringt.

#### Ursprung und Varianten

Anthropic führte Agent Skills im Oktober 2025 ein und veröffentlichte sie im Dezember 2025 als offenen Standard (Anthropic, 2025c); das Format ist in der Spezifikation beschrieben (Agent Skills specification). 2026 nutzen Claude Code und Codex dasselbe SKILL.md-Format, und Skills sind einer der Bausteine von Agentenschleifen, mit denen Projektwissen festgehalten wird, das der Agent sonst raten würde (Osmani, 2026b).

### Wann einsetzen

- Für wiederkehrende Abläufe mit projektspezifischen Konventionen, etwa Release-Schritte, Dokumentformate oder Review-Checklisten.
- Wenn ein Systemprompt wächst, weil er Anweisungen für viele verschiedene Aufgaben enthält.
- Wenn sich deterministische Schritte an Skripte delegieren lassen.

### Stärken und Grenzen

**Stärken**
- Spart Kontext: Dauerhaft geladen sind nur kurze Beschreibungen (Anthropic, 2025c).
- Skills lassen sich unabhängig pflegen, versionieren und wiederverwenden, statt einen monolithischen Systemprompt zu bearbeiten.
- Beigelegte Skripte machen Schritte deterministisch und günstig (Anthropic, 2025c).

**Einschränkungen**
- Der Agent muss erkennen, wann ein Skill passt; das hängt von der Qualität der Beschreibung ab (Agent Skills specification).
- Bösartige Skills können Schwachstellen einschleusen oder den Agenten zum Abfluss von Daten verleiten; Skills sollten aus vertrauenswürdigen Quellen stammen oder sonst geprüft werden (Anthropic, 2025c).
- Die Unterstützung optionaler Felder wie vorab freigegebener Werkzeuge unterscheidet sich zwischen Agenten-Implementierungen (Agent Skills specification).

### Vergleich

| Konzept | Liefert | Ausgelöst durch |
|----------|----------------|------------|
| Werkzeug | Eine einzelne aufrufbare Funktion | Entscheidung des Modells pro Aufruf |
| Skill | Verfahrenswissen für einen ganzen Ablauf, ggf. mit Skripten (Anthropic, 2025c) | Erkannte Relevanz für die aktuelle Aufgabe |
| MCP-Server | Transport von Werkzeugen, Ressourcen und Prompts ([[mcp-and-related-protocols|MCP und ähnliche Protokolle]]) | Verbindung zum Server |
| Langer Systemprompt | Alle Anweisungen auf einmal | Jede Anfrage, ob relevant oder nicht |

### In der Praxis

Skills ergänzen MCP-Server: MCP bindet Fähigkeiten an, Skills beschreiben, wie sie in einem bestimmten Ablauf genutzt werden (Anthropic, 2025c). Ein großer Systemprompt mit Anweisungen für jeden Fall würde bei jeder Anfrage Kontext belegen und ihn mit irrelevantem Material verunreinigen ([[rag-failure-modes|RAG: Typische Fehlerarten]]); Skills ersetzen ihn durch kurze Beschreibungen ([[prompt-engineering|Prompt Engineering]]). Der Harness entscheidet, welche Skills verfügbar sind und mit welchen Rechten ihre Skripte laufen ([[harness-engineering|Harness Engineering]]), Skills senken Token-Kosten ([[llm-cost-optimization|LLM-Kostenoptimierung]]), und ihre Nutzung wird wie jeder Werkzeugaufruf getraced ([[llm-observability-and-tracing|LLM-Observability und Tracing]]). Sie sind eine der Ebenen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]] und werden in Agenten ([[agentic-ai|Agentic AI]]), Schleifen ([[loop-engineering|Loop Engineering]]), Multi-Agenten-Systemen ([[graph-engineering|Graph Engineering]]) und beim alltäglichen KI-gestützten Programmieren ([[vibe-coding|Vibe Coding]]) eingesetzt.

### Merksatz

Ein Skill ist Wissen, das wartet, bis es gebraucht wird: Eine kurze Beschreibung ist immer sichtbar, die vollständigen Anweisungen und Skripte werden erst geladen, wenn die Aufgabe sie verlangt.

### Quellen

- Zhang, B., Lazuka, K. & Murag, M. (2025). *Equipping agents for the real world with Agent Skills.* Anthropic Engineering, 16 October 2025. [anthropic.com](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- Agent Skills. *Specification.* agentskills.io. [agentskills.io](https://agentskills.io/specification)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Osmani, A. (2026). *Loop Engineering.* AddyOsmani.com. [addyosmani.com](https://addyosmani.com/blog/loop-engineering/)
