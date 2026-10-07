---
title_en: Agentic AI
title_de: Agentic AI
entity_type: Concept
sources:
- https://arxiv.org/abs/2210.03629
- https://arxiv.org/abs/2302.04761
- https://arxiv.org/abs/2303.11366
- https://arxiv.org/abs/2308.11432
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://arxiv.org/abs/2302.12173
- https://arxiv.org/abs/2308.03688
- https://arxiv.org/abs/2310.06770
- https://arxiv.org/abs/2310.08560
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Agentic AI describes systems in which a language model does not only answer a single input but pursues a goal over several steps: it plans, calls tools, observes the results and decides what to do next. A useful distinction separates workflows, in which LLMs and tools follow predefined code paths, from agents, in which the LLM dynamically directs its own process and tool use (Anthropic, 2024a); in the simplest definition, agents are LLMs autonomously using tools in a loop (Anthropic, 2025a). Agents can solve open-ended tasks, but they cost more, compound errors and open new attack surfaces such as indirect prompt injection (Greshake et al., 2023).

### How it works

#### 1. Workflow vs. agent

```text
workflow:  input → step A → step B → step C → output        (path fixed in code)
agent:     goal → LLM decides → tool A | tool B | ask | stop  (path chosen at run time)
```

The building block of both is an LLM augmented with retrieval, tools and memory. Common workflow patterns are prompt chaining, routing, parallelisation, orchestrator-workers and evaluator-optimizer (Anthropic, 2024a); an agent repeats a cycle of reasoning, action and observation until the goal is reached, no useful action remains or a stopping condition applies.

#### 2. Tools and tool calling

Tools let the model act outside the text: search, databases, APIs, code execution or file systems. Toolformer showed that a model can learn which APIs to call, when, with which arguments and how to use the results (Schick et al., 2023); today, models usually call tools through function calling or protocols such as MCP ([[mcp-and-related-protocols|MCP and Related Protocols]]). How tools, permissions and execution environment are designed is the subject of [[harness-engineering|Harness Engineering]].

#### 3. Reasoning and acting: ReAct

ReAct interleaves reasoning traces with actions: reasoning helps to create and update plans and handle exceptions, actions gather information from external sources (Yao et al., 2022). With a simple Wikipedia API, ReAct reduced hallucination and error propagation compared with pure chain-of-thought reasoning (Yao et al., 2022).

```text
while not done:
    thought = llm.reason(state)        # what is missing?
    action  = llm.choose_tool(thought)  # e.g. search
    observation = run(action)           # ground truth from the environment
    state.update(thought, action, observation)
```

The design of this loop, with termination, state and error handling, is described in [[loop-engineering|Loop Engineering]].

#### 4. State and memory

Agents keep state: completed steps, tool results, open tasks and errors. Short-term memory covers the current task; long-term memory covers preferences, earlier projects and facts across sessions, often stored in [[vector-databases|Vector Databases]] or [[knowledge-graphs|Knowledge Graphs]]. Because context windows are limited, MemGPT manages several memory tiers and moves information in and out of the context, similar to an operating system (Packer et al., 2023); compaction and structured note-taking keep long tasks coherent ([[context-engineering|Context Engineering]]; Anthropic, 2025a).

#### 5. Reflection and self-correction

Reflexion agents reflect verbally on feedback and keep these reflections in an episodic memory for later attempts, reaching 91% pass@1 on the HumanEval coding benchmark (Shinn et al., 2023). An evaluator, possibly another LLM, can check intermediate results and trigger a retry ([[llm-as-a-judge|LLM-as-a-Judge]]).

#### 6. Single-agent and multi-agent systems

A single agent handles all subtasks, which is simple but leads to large prompts. In multi-agent systems, specialised agents take roles such as researcher, analyst or reviewer, coordinated by a supervisor, a router or a planner–executor split. Sub-agents with clean context windows that return condensed summaries help with long tasks (Anthropic, 2025a). The organisation of many agents is discussed as [[graph-engineering|Graph Engineering]].

#### Origin and variants

LLM-based autonomous agents grew quickly after models acquired broad knowledge from the web; a survey proposes a unified framework for their construction and reviews applications and evaluation (Wang et al., 2023). Key building blocks were tool use (Schick et al., 2023), interleaved reasoning and acting (Yao et al., 2022) and verbal self-reflection (Shinn et al., 2023); frameworks such as [[langchain-and-langgraph|LangChain and LangGraph]] made them easier to build.

### When to use it

- For open-ended problems where the number of steps cannot be predicted and a fixed path cannot be hard-coded (Anthropic, 2024a).
- When results can be verified, for example by automated tests in coding or by clear success criteria in customer support (Anthropic, 2024a).
- Not when a fixed workflow or a single well-prompted LLM call with retrieval is enough: start with the simplest solution and add complexity only when it demonstrably improves outcomes (Anthropic, 2024a; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).

### Strengths and limitations

**Strengths**
- Solves multi-step tasks that need external information or actions.
- Grounding in tool results reduces hallucinations compared with reasoning alone (Yao et al., 2022).
- Self-reflection and evaluator loops improve results over several attempts (Shinn et al., 2023).

**Limitations**
- Poor long-term reasoning, decision-making and instruction following are the main obstacles; open models trailed commercial models considerably on AgentBench (Liu et al., 2023).
- Realistic tasks remain hard: on SWE-bench, the best model at the time resolved 1.96% of real GitHub issues (Jimenez et al., 2023).
- Higher costs and compounding errors (Anthropic, 2024a); agents can get stuck in loops ([[llm-cost-optimization|LLM Cost Optimization]]).
- Retrieved content blurs data and instructions: indirect prompt injection lets attackers control an agent through web pages or documents it reads (Greshake et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Single LLM call | One prompt, one answer | Classification, extraction, simple Q&A |
| Workflow | LLM calls in predefined code paths (Anthropic, 2024a) | Well-defined, repeatable tasks |
| RAG | Retrieve, then generate ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]) | Questions over a document collection |
| Agent | LLM chooses tools and steps in a loop (Anthropic, 2025a) | Open-ended tasks with verifiable results |
| Multi-agent system | Several specialised agents coordinated by a supervisor or router | Complex tasks with separable subtasks |

### In practice

Critical actions, such as payments, sending contracts, deleting data or changing production systems, require human approval before execution; agents get only the tools they need (least privilege) and stop after defined limits ([[harness-engineering|Harness Engineering]]), and extensive testing in sandboxed environments with guardrails is recommended (Anthropic, 2024a). Every tool call and intermediate step is traced ([[llm-observability-and-tracing|LLM Observability and Tracing]]), and agents are evaluated on task success, tool selection and efficiency rather than on the final answer alone ([[llm-evaluation|LLM Evaluation]]). Recurring procedures are packaged as [[agent-skills|Agent Skills]], and the engineering disciplines around agents are collected in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]]; agents also change how software is written ([[vibe-coding|Vibe Coding]]).

### Key takeaway

An agent is an LLM that uses tools in a loop and decides its own next step; it pays off for open-ended tasks with verifiable results, while simpler workflows are more predictable, cheaper and safer wherever the path is known.

### Sources

- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* NeurIPS 2023. [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents.* Frontiers of Computer Science 2024. [arXiv:2308.11432](https://arxiv.org/abs/2308.11432)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Liu, X. et al. (2023). *AgentBench: Evaluating LLMs as Agents.* ICLR 2024. [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)
- Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Agentic AI bezeichnet Systeme, in denen ein Sprachmodell nicht nur auf eine einzelne Eingabe antwortet, sondern ein Ziel über mehrere Schritte verfolgt: Es plant, ruft Werkzeuge auf, beobachtet die Ergebnisse und entscheidet über den nächsten Schritt. Eine hilfreiche Unterscheidung trennt Workflows, in denen LLMs und Werkzeuge vorgegebenen Codepfaden folgen, von Agenten, in denen das LLM seinen Ablauf und die Werkzeugnutzung selbst steuert (Anthropic, 2024a); in der einfachsten Definition sind Agenten LLMs, die Werkzeuge selbstständig in einer Schleife nutzen (Anthropic, 2025a). Agenten können offene Aufgaben lösen, kosten aber mehr, häufen Fehler an und öffnen neue Angriffsflächen wie indirekte Prompt Injection (Greshake et al., 2023).

### Funktionsweise

#### 1. Workflow vs. Agent

```text
Workflow:  Eingabe → Schritt A → Schritt B → Schritt C → Ausgabe        (Pfad im Code festgelegt)
Agent:     Ziel → LLM entscheidet → Tool A | Tool B | nachfragen | stopp  (Pfad zur Laufzeit gewählt)
```

Baustein beider ist ein LLM, das um Retrieval, Werkzeuge und Gedächtnis erweitert ist. Verbreitete Workflow-Muster sind Prompt Chaining, Routing, Parallelisierung, Orchestrator-Worker und Evaluator-Optimizer (Anthropic, 2024a); ein Agent wiederholt einen Zyklus aus Überlegen, Handeln und Beobachten, bis das Ziel erreicht ist, keine sinnvolle Aktion mehr bleibt oder eine Abbruchbedingung greift.

#### 2. Werkzeuge und Tool Calling

Werkzeuge erlauben dem Modell, außerhalb des Textes zu handeln: Suche, Datenbanken, APIs, Codeausführung oder Dateisysteme. Toolformer zeigte, dass ein Modell lernen kann, welche APIs es wann mit welchen Argumenten aufruft und wie es die Ergebnisse nutzt (Schick et al., 2023); heute rufen Modelle Werkzeuge meist über Function Calling oder Protokolle wie MCP auf ([[mcp-and-related-protocols|MCP und ähnliche Protokolle]]). Wie Werkzeuge, Berechtigungen und Ausführungsumgebung gestaltet werden, behandelt [[harness-engineering|Harness Engineering]].

#### 3. Überlegen und Handeln: ReAct

ReAct verzahnt Gedankengänge mit Aktionen: Das Überlegen hilft, Pläne aufzustellen und anzupassen und Ausnahmen zu behandeln, die Aktionen holen Informationen aus externen Quellen (Yao et al., 2022). Mit einer einfachen Wikipedia-API verringerte ReAct Halluzinationen und Fehlerfortpflanzung gegenüber reinem Chain-of-Thought-Schlussfolgern (Yao et al., 2022).

```text
while not done:
    thought = llm.reason(state)        # was fehlt noch?
    action  = llm.choose_tool(thought)  # z. B. Suche
    observation = run(action)           # Rückmeldung aus der Umgebung
    state.update(thought, action, observation)
```

Wie diese Schleife mit Abbruch, Zustand und Fehlerbehandlung gestaltet wird, beschreibt [[loop-engineering|Loop Engineering]].

#### 4. Zustand und Gedächtnis

Agenten führen einen Zustand: erledigte Schritte, Werkzeugergebnisse, offene Aufgaben und Fehler. Das Kurzzeitgedächtnis umfasst die aktuelle Aufgabe, das Langzeitgedächtnis Vorlieben, frühere Projekte und Fakten über Sitzungen hinweg, oft gespeichert in [[vector-databases|Vektordatenbanken]] oder [[knowledge-graphs|Wissensgraphen]]. Weil Kontextfenster begrenzt sind, verwaltet MemGPT mehrere Speicherebenen und verschiebt Informationen in den Kontext hinein und heraus, ähnlich einem Betriebssystem (Packer et al., 2023); Kompaktierung und strukturierte Notizen halten lange Aufgaben zusammen ([[context-engineering|Context Engineering]]; Anthropic, 2025a).

#### 5. Reflexion und Selbstkorrektur

Reflexion-Agenten reflektieren Rückmeldungen in Worten und halten diese Reflexionen in einem episodischen Gedächtnis für spätere Versuche fest; sie erreichten 91 % pass@1 im Coding-Benchmark HumanEval (Shinn et al., 2023). Eine bewertende Instanz, etwa ein weiteres LLM, kann Zwischenergebnisse prüfen und einen neuen Versuch auslösen ([[llm-as-a-judge|LLM-as-a-Judge]]).

#### 6. Einzel- und Multi-Agenten-Systeme

Ein einzelner Agent übernimmt alle Teilaufgaben, was einfach ist, aber zu großen Prompts führt. In Multi-Agenten-Systemen übernehmen spezialisierte Agenten Rollen wie Recherche, Analyse oder Review, koordiniert durch einen Supervisor, einen Router oder eine Trennung von Planer und Ausführer. Sub-Agenten mit eigenem, leerem Kontextfenster, die verdichtete Zusammenfassungen zurückgeben, helfen bei langen Aufgaben (Anthropic, 2025a). Die Organisation vieler Agenten wird als [[graph-engineering|Graph Engineering]] diskutiert.

#### Ursprung und Varianten

LLM-basierte autonome Agenten verbreiteten sich schnell, nachdem Modelle breites Wissen aus dem Web erworben hatten; ein Überblicksartikel schlägt einen einheitlichen Rahmen für ihren Aufbau vor und behandelt Anwendungen und Evaluation (Wang et al., 2023). Zentrale Bausteine waren Werkzeugnutzung (Schick et al., 2023), verzahntes Überlegen und Handeln (Yao et al., 2022) und sprachliche Selbstreflexion (Shinn et al., 2023); Frameworks wie [[langchain-and-langgraph|LangChain und LangGraph]] erleichterten den Bau.

### Wann einsetzen

- Für offene Probleme, bei denen sich die Zahl der Schritte nicht vorhersagen und kein fester Pfad im Code festlegen lässt (Anthropic, 2024a).
- Wenn sich Ergebnisse überprüfen lassen, etwa durch automatisierte Tests beim Programmieren oder durch klare Erfolgskriterien im Kundenservice (Anthropic, 2024a).
- Nicht, wenn ein fester Workflow oder ein einzelner gut gestalteter LLM-Aufruf mit Retrieval genügt: mit der einfachsten Lösung beginnen und Komplexität nur ergänzen, wenn sie die Ergebnisse nachweislich verbessert (Anthropic, 2024a; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).

### Stärken und Grenzen

**Stärken**
- Löst mehrstufige Aufgaben, die externe Informationen oder Aktionen brauchen.
- Die Rückbindung an Werkzeugergebnisse verringert Halluzinationen gegenüber reinem Schlussfolgern (Yao et al., 2022).
- Selbstreflexion und bewertende Schleifen verbessern Ergebnisse über mehrere Versuche (Shinn et al., 2023).

**Einschränkungen**
- Schwaches langfristiges Schlussfolgern, Entscheiden und Befolgen von Anweisungen sind die Haupthindernisse; offene Modelle lagen in AgentBench deutlich hinter kommerziellen Modellen (Liu et al., 2023).
- Realistische Aufgaben bleiben schwer: In SWE-bench löste das damals beste Modell 1,96 % echter GitHub-Issues (Jimenez et al., 2023).
- Höhere Kosten und sich aufschaukelnde Fehler (Anthropic, 2024a); Agenten können in Schleifen festhängen ([[llm-cost-optimization|LLM-Kostenoptimierung]]).
- Abgerufene Inhalte verwischen die Grenze zwischen Daten und Anweisungen: Über indirekte Prompt Injection können Angreifende einen Agenten über Webseiten oder Dokumente steuern, die er liest (Greshake et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Einzelner LLM-Aufruf | Ein Prompt, eine Antwort | Klassifikation, Extraktion, einfache Fragen |
| Workflow | LLM-Aufrufe in vorgegebenen Codepfaden (Anthropic, 2024a) | Klar umrissene, wiederkehrende Aufgaben |
| RAG | Erst abrufen, dann generieren ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]) | Fragen über eine Dokumentsammlung |
| Agent | LLM wählt Werkzeuge und Schritte in einer Schleife (Anthropic, 2025a) | Offene Aufgaben mit überprüfbaren Ergebnissen |
| Multi-Agenten-System | Mehrere spezialisierte Agenten, koordiniert durch Supervisor oder Router | Komplexe Aufgaben mit trennbaren Teilaufgaben |

### In der Praxis

Kritische Aktionen wie Zahlungen, der Versand von Verträgen, das Löschen von Daten oder Änderungen an Produktivsystemen brauchen vor der Ausführung eine menschliche Freigabe; Agenten erhalten nur die Werkzeuge, die sie benötigen (Least Privilege), und stoppen nach festgelegten Grenzen ([[harness-engineering|Harness Engineering]]); empfohlen werden ausführliche Tests in Sandbox-Umgebungen mit Guardrails (Anthropic, 2024a). Jeder Werkzeugaufruf und Zwischenschritt wird getraced ([[llm-observability-and-tracing|LLM-Observability und Tracing]]), und Agenten werden nach Aufgabenerfolg, Werkzeugwahl und Effizienz bewertet, nicht nur nach der Endantwort ([[llm-evaluation|LLM-Evaluation]]). Wiederkehrende Abläufe werden als [[agent-skills|Agent Skills]] verpackt, und die Engineering-Disziplinen rund um Agenten bündelt [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]]; Agenten verändern auch, wie Software geschrieben wird ([[vibe-coding|Vibe Coding]]).

### Merksatz

Ein Agent ist ein LLM, das Werkzeuge in einer Schleife nutzt und seinen nächsten Schritt selbst wählt; das lohnt sich bei offenen Aufgaben mit überprüfbaren Ergebnissen, während einfachere Workflows überall dort vorhersehbarer, günstiger und sicherer sind, wo der Weg bekannt ist.

### Quellen

- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* NeurIPS 2023. [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents.* Frontiers of Computer Science 2024. [arXiv:2308.11432](https://arxiv.org/abs/2308.11432)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
- Rajasekaran, P., Dixon, E., Ryan, C. & Hadfield, J. (2025). *Effective context engineering for AI agents.* Anthropic Engineering, 29 September 2025. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Liu, X. et al. (2023). *AgentBench: Evaluating LLMs as Agents.* ICLR 2024. [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)
- Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
