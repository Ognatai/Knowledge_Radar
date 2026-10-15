---
title_en: Agent Frameworks
title_de: Agent-Frameworks
entity_type: Concept
aliases:
- Agent frameworks
- Agent framework
- Agentic frameworks
- Semantic Kernel
- Microsoft Agent Framework
- LlamaIndex
- CrewAI
sources:
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/semantic-kernel/overview/
- https://arxiv.org/abs/2308.08155
- https://developers.llamaindex.ai/python/framework/
- https://docs.crewai.com/en/introduction
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Agent frameworks are libraries that provide the recurring building blocks of LLM agents: clients for different model providers, tool and function calling, connections to data and MCP servers, memory and session state, multi-step workflows that coordinate several agents, and hooks for tracing and safety checks. Widely used examples are LangChain/LangGraph, [[microsoft|Microsoft]]'s Semantic Kernel and [[autogen|AutoGen]], now merged into Microsoft Agent Framework, LlamaIndex, which started from retrieval over private data, and CrewAI, which organises agents into crews (Microsoft Learn; Wu et al., 2023; LlamaIndex; CrewAI). They differ mainly in how much control flow they make explicit: free conversation between agents, event-driven workflows or graphs with defined execution paths. Microsoft's own guidance is that a plain function beats an agent whenever one can be written (Microsoft Learn).

### How it works

```text
model client (OpenAI, Anthropic, Azure, local models, …)
 ▼
agent = model + instructions + tools (functions, APIs, MCP servers, retrieval)
 ▼
session / memory: conversation state, context providers
 ▼
orchestration: single agent loop · multi-agent conversation · workflow / graph with explicit paths
 ▼
middleware / filters: approvals, content checks, telemetry and tracing
```

#### 1. Model clients and tools

All frameworks wrap model [[apis|APIs]] behind a common interface so that models can be swapped; Semantic Kernel describes this as connecting code to the latest models "without needing to rewrite your entire codebase" (Semantic Kernel). Tools are existing code exposed to the model: in Semantic Kernel, code is added as plugins, the model requests a function call, and the kernel "is the middleware translating the model's request to a function call and passes the results back to the model"; plugins can also be described with OpenAPI specifications (Semantic Kernel). Microsoft Agent Framework agents call tools and MCP servers and support Microsoft Foundry, [[anthropic|Anthropic]], Azure OpenAI, [[openai|OpenAI]], Ollama and other providers (Microsoft Learn). The protocol layer is covered in [[mcp-and-related-protocols|MCP and related protocols]], the agent loop itself in [[agentic-ai|agentic AI]].

#### 2. Data and retrieval

LlamaIndex describes itself as "a [[python|Python]] toolkit for building LLM-powered agents over your data". Its central idea is context augmentation, which "makes that data available to the model at the moment it answers", with [[retrieval-augmented-generation|RAG]] as the best-known form; data connectors, indexes, vector stores and query and chat engines are its building blocks, and a RAG pipeline can be one tool among others for an agent (LlamaIndex). Harder documents such as scanned PDFs, forms and slides are handled by its hosted parsing service LlamaParse (LlamaIndex), see [[document-processing|document processing]].

#### 3. Multi-agent conversation

AutoGen, introduced by Wu et al. (2023), builds applications from several customisable agents that converse with each other to solve a task; agents can combine LLMs, human input and tools, and developers program the interaction patterns in natural language and code (Wu et al., 2023). The authors report applications in mathematics, coding, question answering, operations research, online decision-making and entertainment (Wu et al., 2023). CrewAI groups agents with specific goals and tools into crews, "teams of autonomous agents that collaborate to solve specific tasks delegated to them by the Flow" (CrewAI). Patterns and risks of such systems are discussed in [[agentic-ai|agentic AI]].

#### 4. Workflows with explicit control flow

Open conversation between agents is hard to predict, so newer frameworks add explicit workflows. Microsoft Agent Framework offers functional and graph-based workflows "that connect agents and functions through explicit execution paths", with state management for long-running and human-in-the-loop scenarios (Microsoft Learn). LlamaIndex workflows are "event-driven, multi-step processes" with branching, retries and human review (LlamaIndex), and CrewAI flows manage state, events, conditions, loops and branching around crews (CrewAI). LangGraph models the same idea as a state graph, see [[langchain-and-langgraph|LangChain and LangGraph]]. Microsoft summarises the choice: use an agent for open-ended or conversational tasks that need autonomous tool use, and a workflow when steps are well defined, execution order must be controlled or several agents and functions have to coordinate (Microsoft Learn).

#### 5. State, middleware and observability

Production features distinguish frameworks more than the agent loop does. Semantic Kernel emphasises telemetry, hooks and filters and promises stable APIs from version 1.0 in C#, Python and Java (Semantic Kernel). Microsoft Agent Framework provides agent sessions for state, context providers for memory, middleware that intercepts agent actions, and a "harness agent" with planning, context compaction, file access, memory and tool approval for long tasks (Microsoft Learn). The surrounding engineering practices are covered in [[harness-engineering|harness engineering]], [[context-engineering|context engineering]] and [[llm-observability-and-tracing|LLM observability and tracing]].

#### Origin and variants

Semantic Kernel was built as an SDK for enterprise applications and AutoGen as a framework for multi-agent conversation (Semantic Kernel; Wu et al., 2023). Microsoft has since merged both into Microsoft Agent Framework, described as "the direct successor, created by the same teams" and "the next generation of both Semantic Kernel and AutoGen", available for .NET and Python, with Go in public preview (Microsoft Learn). Cloud platforms also host agents built with these frameworks, see [[cloud-ai-platforms|cloud AI platforms]].

### When to use it

- An application needs several of: multiple model providers, tool calling, retrieval, memory, multi-step orchestration and tracing, and these should not be built from scratch (Microsoft Learn).
- Retrieval over heterogeneous internal documents is central: LlamaIndex starts from data connectors and indexes (LlamaIndex).
- Several specialised agents should collaborate: AutoGen-style conversation or CrewAI crews (Wu et al., 2023; CrewAI).
- The organisation is on Microsoft's stack and needs .NET support: Semantic Kernel or its successor (Semantic Kernel; Microsoft Learn).

### Strengths and limitations

**Strengths**
- Provider abstraction makes models swappable (Semantic Kernel).
- Reusable components for tools, retrieval, memory and tracing shorten development (Microsoft Learn; LlamaIndex).
- Explicit workflows make multi-agent execution controllable and resumable (Microsoft Learn).

**Limitations**
- Frameworks change fast: Semantic Kernel and AutoGen have been superseded by Agent Framework, and users need migration guides (Microsoft Learn).
- An extra abstraction layer can hide prompts and control flow; Microsoft advises using a plain function where possible (Microsoft Learn).
- Responsibility for safety stays with the developer: Microsoft's documentation requires users to implement their own responsible AI mitigations such as content filters and to check data flows to third-party systems (Microsoft Learn).

### Comparison

| Framework | Origin | Focus | Orchestration |
|---|---|---|---|
| [[langchain-and-langgraph\|LangChain / LangGraph]] | open source | general LLM apps | chains, state graphs |
| Semantic Kernel | Microsoft | enterprise SDK with plugins (C#, Python, Java) | function calling via the kernel |
| AutoGen | Microsoft Research | multi-agent conversation | conversation patterns |
| Microsoft Agent Framework | successor of both | agents plus workflows (.NET, Python, Go preview) | graph-based and functional workflows |
| LlamaIndex | open source | agents over private data, RAG | event-driven workflows |
| CrewAI | open source | role-based agent teams | crews within flows |

Sources: Microsoft Learn; Semantic Kernel; Wu et al. (2023); LlamaIndex; CrewAI.

### In practice

Framework choice matters less than evaluation: agent runs should be traced and tested on representative tasks before release ([[llm-evaluation|LLM evaluation]], [[llm-observability-and-tracing|LLM observability and tracing]]). Tool access needs the same care as any API, including approval steps for actions with side effects and defences against [[prompt-injection|prompt injection]]; see also [[llm-guardrails-and-red-teaming|LLM guardrails and red teaming]].

### Key takeaway

Agent frameworks package model clients, tools, retrieval, memory, orchestration and tracing; they differ in how explicit the control flow is, from free multi-agent conversation to graph-based workflows, and change quickly, as Microsoft's merger of Semantic Kernel and AutoGen shows.

### Sources

- Microsoft Learn. *Microsoft Agent Framework Overview.* Updated August 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/overview/)
- Semantic Kernel. *Introduction to Semantic Kernel.* Microsoft Learn. [learn.microsoft.com](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D. & Wang, C. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* arXiv:2308.08155. [arXiv](https://arxiv.org/abs/2308.08155)
- LlamaIndex. *LlamaIndex framework documentation.* [developers.llamaindex.ai](https://developers.llamaindex.ai/python/framework/)
- CrewAI. *Introduction.* CrewAI documentation. [docs.crewai.com](https://docs.crewai.com/en/introduction)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Agent-Frameworks sind Bibliotheken, die die wiederkehrenden Bausteine von LLM-Agenten bereitstellen: Clients für verschiedene Modellanbieter, Tool- und Function Calling, Anbindungen an Daten und MCP-Server, Gedächtnis und Sitzungszustand, mehrstufige Workflows, die mehrere Agenten koordinieren, sowie Einstiegspunkte für Tracing und Sicherheitsprüfungen. Verbreitete Beispiele sind LangChain/LangGraph, Microsofts Semantic Kernel und [[autogen|AutoGen]], inzwischen zu Microsoft Agent Framework zusammengeführt, LlamaIndex, das von Retrieval über private Daten ausging, und CrewAI, das Agenten in Crews organisiert (Microsoft Learn; Wu et al., 2023; LlamaIndex; CrewAI). Sie unterscheiden sich vor allem darin, wie explizit sie den Kontrollfluss machen: freie Konversation zwischen Agenten, ereignisgesteuerte Workflows oder Graphen mit festgelegten Ausführungspfaden. Microsofts eigene Empfehlung lautet, dass eine einfache Funktion einem Agenten vorzuziehen ist, wann immer sie sich schreiben lässt (Microsoft Learn).

### Funktionsweise

```text
Modell-Client (OpenAI, Anthropic, Azure, lokale Modelle, …)
 ▼
Agent = Modell + Anweisungen + Tools (Funktionen, APIs, MCP-Server, Retrieval)
 ▼
Sitzung / Gedächtnis: Gesprächszustand, Context Provider
 ▼
Orchestrierung: Schleife eines Agenten · Multi-Agenten-Konversation · Workflow / Graph mit expliziten Pfaden
 ▼
Middleware / Filter: Freigaben, Inhaltsprüfungen, Telemetrie und Tracing
```

#### 1. Modell-Clients und Tools

Alle Frameworks kapseln Modell-APIs hinter einer gemeinsamen Schnittstelle, damit sich Modelle austauschen lassen; Semantic Kernel beschreibt das als Anbindung des Codes an neue Modelle „without needing to rewrite your entire codebase“ (Semantic Kernel). Tools sind bestehender Code, der dem Modell zur Verfügung gestellt wird: In Semantic Kernel wird Code als Plugin hinzugefügt, das Modell fordert einen Funktionsaufruf an, und der Kernel „is the middleware translating the model's request to a function call and passes the results back to the model“; Plugins lassen sich auch über OpenAPI-Spezifikationen beschreiben (Semantic Kernel). Agenten in Microsoft Agent Framework rufen Tools und MCP-Server auf und unterstützen Microsoft Foundry, [[anthropic|Anthropic]], Azure OpenAI, [[openai|OpenAI]], Ollama und weitere Anbieter (Microsoft Learn). Die Protokollebene behandelt [[mcp-and-related-protocols|MCP und verwandte Protokolle]], die Agentenschleife selbst [[agentic-ai|Agentic AI]].

#### 2. Daten und Retrieval

LlamaIndex beschreibt sich als „a [[python|Python]] toolkit for building LLM-powered agents over your data“. Sein zentraler Gedanke ist Context Augmentation, die „makes that data available to the model at the moment it answers“, mit [[retrieval-augmented-generation|RAG]] als bekanntester Form; Datenkonnektoren, Indizes, Vektorspeicher sowie Query und Chat Engines sind seine Bausteine, und eine RAG-Pipeline kann für einen Agenten ein Tool unter mehreren sein (LlamaIndex). Schwierigere Dokumente wie gescannte PDFs, Formulare und Folien verarbeitet der gehostete Parsing-Dienst LlamaParse (LlamaIndex), siehe [[document-processing|Dokumentenverarbeitung]].

#### 3. Multi-Agenten-Konversation

AutoGen, vorgestellt von Wu et al. (2023), baut Anwendungen aus mehreren anpassbaren Agenten auf, die miteinander sprechen, um eine Aufgabe zu lösen; Agenten können LLMs, menschliche Eingaben und Tools kombinieren, und Entwicklerinnen und Entwickler programmieren die Interaktionsmuster in natürlicher Sprache und Code (Wu et al., 2023). Die Autorinnen und Autoren berichten von Anwendungen in Mathematik, Programmierung, Fragebeantwortung, Operations Research, Online-Entscheidungen und Unterhaltung (Wu et al., 2023). CrewAI fasst Agenten mit bestimmten Zielen und Tools zu Crews zusammen, „teams of autonomous agents that collaborate to solve specific tasks delegated to them by the Flow“ (CrewAI). Muster und Risiken solcher Systeme behandelt [[agentic-ai|Agentic AI]].

#### 4. Workflows mit explizitem Kontrollfluss

Offene Konversation zwischen Agenten ist schwer vorherzusagen, deshalb ergänzen neuere Frameworks explizite Workflows. Microsoft Agent Framework bietet funktionale und graphbasierte Workflows, „that connect agents and functions through explicit execution paths“, mit Zustandsverwaltung für lang laufende Abläufe und Abläufe mit menschlicher Beteiligung (Microsoft Learn). Workflows in LlamaIndex sind „event-driven, multi-step processes“ mit Verzweigungen, Wiederholungen und menschlicher Prüfung (LlamaIndex), und Flows in CrewAI verwalten Zustand, Ereignisse, Bedingungen, Schleifen und Verzweigungen rund um Crews (CrewAI). LangGraph bildet dieselbe Idee als Zustandsgraph ab, siehe [[langchain-and-langgraph|LangChain und LangGraph]]. Microsoft fasst die Wahl so zusammen: ein Agent für offene oder dialogorientierte Aufgaben mit autonomer Tool-Nutzung, ein Workflow, wenn die Schritte klar sind, die Reihenfolge kontrolliert werden muss oder mehrere Agenten und Funktionen zusammenwirken (Microsoft Learn).

#### 5. Zustand, Middleware und Observability

Produktionsfunktionen unterscheiden Frameworks stärker als die Agentenschleife. Semantic Kernel betont Telemetrie, Hooks und Filter und verspricht ab Version 1.0 stabile [[apis|APIs]] in C#, Python und Java (Semantic Kernel). Microsoft Agent Framework bietet Agentensitzungen für den Zustand, Context Provider für das Gedächtnis, Middleware, die Aktionen von Agenten abfängt, und einen „Harness Agent“ mit Planung, Kontextverdichtung, Dateizugriff, Gedächtnis und Tool-Freigaben für lange Aufgaben (Microsoft Learn). Die umgebenden Engineering-Praktiken behandeln [[harness-engineering|Harness Engineering]], [[context-engineering|Context Engineering]] und [[llm-observability-and-tracing|LLM-Observability und Tracing]].

#### Herkunft und Varianten

Semantic Kernel entstand als SDK für Unternehmensanwendungen und AutoGen als Framework für Multi-Agenten-Konversation (Semantic Kernel; Wu et al., 2023). Inzwischen hat Microsoft beide zu Microsoft Agent Framework zusammengeführt, beschrieben als „the direct successor, created by the same teams“ und „the next generation of both Semantic Kernel and AutoGen“, verfügbar für .NET und Python, Go in einer öffentlichen Vorschau (Microsoft Learn). Auch Cloud-Plattformen betreiben Agenten, die mit diesen Frameworks gebaut sind, siehe [[cloud-ai-platforms|Cloud-KI-Plattformen]].

### Wann einsetzen

- Eine Anwendung braucht mehreres davon: mehrere Modellanbieter, Tool Calling, Retrieval, Gedächtnis, mehrstufige Orchestrierung und Tracing, und das soll nicht von Grund auf gebaut werden (Microsoft Learn).
- Retrieval über heterogene interne Dokumente steht im Mittelpunkt: LlamaIndex setzt bei Datenkonnektoren und Indizes an (LlamaIndex).
- Mehrere spezialisierte Agenten sollen zusammenarbeiten: Konversation nach Art von AutoGen oder Crews in CrewAI (Wu et al., 2023; CrewAI).
- Die Organisation arbeitet mit Microsoft-Technologie und braucht .NET-Unterstützung: Semantic Kernel oder sein Nachfolger (Semantic Kernel; Microsoft Learn).

### Stärken und Grenzen

**Stärken**
- Die Abstraktion über Anbieter macht Modelle austauschbar (Semantic Kernel).
- Wiederverwendbare Bausteine für Tools, Retrieval, Gedächtnis und Tracing verkürzen die Entwicklung (Microsoft Learn; LlamaIndex).
- Explizite Workflows machen die Ausführung mehrerer Agenten steuerbar und fortsetzbar (Microsoft Learn).

**Grenzen**
- Frameworks ändern sich schnell: Semantic Kernel und AutoGen wurden von Agent Framework abgelöst, und Nutzende brauchen Migrationsleitfäden (Microsoft Learn).
- Eine zusätzliche Abstraktionsschicht kann Prompts und Kontrollfluss verbergen; Microsoft rät, wo möglich eine einfache Funktion zu nutzen (Microsoft Learn).
- Die Verantwortung für Sicherheit bleibt bei den Entwickelnden: Microsofts Dokumentation verlangt, eigene Maßnahmen für verantwortungsvolle KI wie Inhaltsfilter umzusetzen und Datenflüsse zu Drittsystemen zu prüfen (Microsoft Learn).

### Vergleich

| Framework | Herkunft | Schwerpunkt | Orchestrierung |
|---|---|---|---|
| [[langchain-and-langgraph\|LangChain / LangGraph]] | Open Source | allgemeine LLM-Anwendungen | Chains, Zustandsgraphen |
| Semantic Kernel | Microsoft | Unternehmens-SDK mit Plugins (C#, Python, Java) | Function Calling über den Kernel |
| AutoGen | Microsoft Research | Multi-Agenten-Konversation | Konversationsmuster |
| Microsoft Agent Framework | Nachfolger beider | Agenten und Workflows (.NET, Python, Go-Vorschau) | graphbasierte und funktionale Workflows |
| LlamaIndex | Open Source | Agenten über private Daten, RAG | ereignisgesteuerte Workflows |
| CrewAI | Open Source | rollenbasierte Agententeams | Crews innerhalb von Flows |

Quellen: Microsoft Learn; Semantic Kernel; Wu et al. (2023); LlamaIndex; CrewAI.

### In der Praxis

Die Wahl des Frameworks zählt weniger als die Evaluation: Agentenläufe sollten vor dem Release auf repräsentativen Aufgaben nachverfolgt und getestet werden ([[llm-evaluation|LLM-Evaluation]], [[llm-observability-and-tracing|LLM-Observability und Tracing]]). Tool-Zugriff braucht dieselbe Sorgfalt wie jede API, einschließlich Freigabeschritten für Aktionen mit Nebenwirkungen und Schutz vor [[prompt-injection|Prompt Injection]]; siehe auch [[llm-guardrails-and-red-teaming|LLM-Guardrails und Red Teaming]].

### Merksatz

Agent-Frameworks bündeln Modell-Clients, Tools, Retrieval, Gedächtnis, Orchestrierung und Tracing; sie unterscheiden sich darin, wie explizit der Kontrollfluss ist, von freier Multi-Agenten-Konversation bis zu graphbasierten Workflows, und ändern sich schnell, wie Microsofts Zusammenführung von Semantic Kernel und AutoGen zeigt.

### Quellen

- Microsoft Learn. *Microsoft Agent Framework Overview.* Aktualisiert im August 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/overview/)
- Semantic Kernel. *Introduction to Semantic Kernel.* Microsoft Learn. [learn.microsoft.com](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D. & Wang, C. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* arXiv:2308.08155. [arXiv](https://arxiv.org/abs/2308.08155)
- LlamaIndex. *LlamaIndex framework documentation.* [developers.llamaindex.ai](https://developers.llamaindex.ai/python/framework/)
- CrewAI. *Introduction.* CrewAI-Dokumentation. [docs.crewai.com](https://docs.crewai.com/en/introduction)
