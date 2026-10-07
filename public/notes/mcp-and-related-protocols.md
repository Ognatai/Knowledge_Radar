---
title_en: MCP and Related Protocols
title_de: MCP und ähnliche Protokolle
entity_type: Concept
sources:
- https://www.anthropic.com/news/model-context-protocol
- https://modelcontextprotocol.io/docs/learn/architecture
- https://modelcontextprotocol.io/specification/2025-06-18
- https://modelcontextprotocol.io/specification/latest/server/tools
- https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- https://a2a-protocol.org/latest/
- https://arxiv.org/abs/2302.12173
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The Model Context Protocol (MCP) is an open protocol that standardises how AI applications connect to external tools, data sources and prompt templates, instead of every application building its own integration for every tool (Anthropic, 2024b). It follows a client-server architecture with JSON-RPC 2.0 messages: a host application creates one client per server, and servers expose tools, resources and prompts (MCP architecture docs). MCP takes some inspiration from the Language Server Protocol (MCP specification). Related protocols cover other axes, most prominently A2A for communication between agents (A2A protocol docs). MCP standardises the connection, not the trust: a shared protocol does not make a foreign server safe.

### How it works

#### 1. The M×N problem

```text
without a shared protocol:   M applications × N tools = M×N integrations
with MCP:                    M clients + N servers    = M+N implementations
```

Every new data source used to require its own custom implementation; MCP replaces these fragmented integrations with a single protocol (Anthropic, 2024b). The Language Server Protocol solved the same problem for programming languages and editors, and MCP standardises the integration of context and tools into AI applications in a similar way (MCP specification).

#### 2. Architecture

```text
host (AI application, e.g. Claude Code or VS Code)
  ├── MCP client 1 ── stdio ──────────────► MCP server 1 (e.g. local file system)
  └── MCP client 2 ── Streamable HTTP ────► MCP server 2 (e.g. remote issue tracker)
```

- **Host:** the AI application that coordinates one or several clients.
- **Client:** maintains a dedicated connection to one server.
- **Server:** a program that provides context, locally via stdio (typically for one client) or remotely via Streamable HTTP (typically for many clients) (MCP architecture docs).

The data layer is based on JSON-RPC 2.0 and covers discovery, server and client features and notifications; the transport layer handles connections, message framing and authorisation, with OAuth recommended for tokens (MCP architecture docs). MCP only defines the protocol for exchanging context; how an application uses LLMs or manages the provided context is up to the application (MCP architecture docs).

#### 3. Primitives

- **Tools:** executable functions that the application can invoke, such as file operations, API calls or database queries; discovered with tools/list and executed with tools/call.
- **Resources:** data sources that provide context, such as file contents, database records or API responses.
- **Prompts:** reusable templates, such as system prompts or few-shot examples (MCP architecture docs).

Clients can offer elicitation, with which servers ask users for information or confirmation; sampling, with which servers requested completions from the client's model, is deprecated as of protocol version 2026-07-28 (MCP architecture docs).

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
 "params": {"name": "search_norms", "arguments": {"query": "data portability"}}}
```

#### 4. MCP vs. proprietary function calling

| | Proprietary function calling | MCP |
|---|---|---|
| Scope | Tools (function calls) | Tools, resources and prompts (MCP architecture docs) |
| Binding | Tied to one model API | Independent of model and vendor |
| Reuse | Integration rebuilt per application | One server, usable by every MCP host (Anthropic, 2024b) |
| Transport | Part of the API call | Separate protocol (stdio or HTTP, JSON-RPC) |

Function calling remains the basis; MCP standardises how tool definitions and results travel between application and tool provider.

#### 5. Security

MCP servers are third-party code inside the harness, and their tool descriptions reach the model as text:

- **Human in the loop:** there should always be a human who can deny tool invocations; clients should show tool inputs before calling a server, validate results before passing them to the model and log tool use; tool annotations from untrusted servers are themselves untrusted (MCP tools specification).
- **Prompt injection via tools and data:** retrieved content and tool descriptions blur the line between data and instructions (Greshake et al., 2023).
- **Local server compromise:** local servers run on the user's machine with direct system access; malicious startup commands can execute arbitrary code, exfiltrate data or destroy it, so clients must show the exact command and require explicit approval (MCP security best practices).
- **Authorisation:** token passthrough is forbidden, broad token scopes increase the impact of a compromise, and MCP proxy servers can create confused-deputy vulnerabilities (MCP security best practices).

#### 6. Related protocols

- **A2A (Agent2Agent):** communication between agents of different frameworks and vendors, who delegate tasks and share results without exposing internal memory or tools; MCP is agent-to-tool, A2A agent-to-agent, and both are complementary (A2A protocol docs).
- **OpenAPI:** a description format for HTTP APIs, sometimes used when only classic API access is needed.
- **LSP:** not an AI protocol, but the model for MCP's client-server idea (MCP specification).

#### Origin and variants

Anthropic open-sourced MCP on 25 November 2024 together with the specification, SDKs, local server support in Claude Desktop and reference servers for systems such as Google Drive, Slack, GitHub, Git and Postgres (Anthropic, 2024b). The protocol has been revised several times; the current version makes requests stateless, so that every request carries the protocol version and capabilities, and servers announce their capabilities through a discovery request (MCP architecture docs).

### When to use it

- When tools or data sources should be usable by several AI applications or agents.
- When an application should integrate a growing number of existing servers instead of custom connectors.
- Not when a single application calls one internal function; plain function calling or a direct API call is simpler.

### Strengths and limitations

**Strengths**
- One server per tool instead of one integration per application and tool (Anthropic, 2024b).
- Independent of model and vendor; tools, resources and prompts in one protocol (MCP architecture docs).
- Dynamic discovery: clients list the available primitives at run time (MCP architecture docs).

**Limitations**
- Third-party servers are an attack surface: local servers can execute arbitrary code, and tool descriptions can carry injected instructions (MCP security best practices; Greshake et al., 2023).
- Many connected servers add many tool descriptions to the context ([[context-engineering|Context Engineering]]).
- The protocol is still evolving, with deprecated features and new versions.

### Comparison

| Protocol | Axis | Suited for |
|----------|----------------|------------|
| MCP | Agent or application ↔ tools and data (MCP architecture docs) | Reusable tool and data integrations |
| A2A | Agent ↔ agent (A2A protocol docs) | Delegation between agents of different vendors |
| Function calling | Model ↔ functions of one application | Few, application-specific tools |
| OpenAPI | Client ↔ HTTP API | Describing classic web APIs |

### In practice

MCP touches two disciplines: resources are a structured source of what [[context-engineering|Context Engineering]] puts into the context, and tools and their safe integration belong to [[harness-engineering|Harness Engineering]]. Which servers are trusted, which permissions apply and what reaches the context remain decisions of the application. Frameworks such as [[langchain-and-langgraph|LangChain and LangGraph]] convert MCP tools into their own tools, skills describe how to use connected tools in workflows ([[agent-skills|Agent Skills]]), and MCP connectors are building blocks of agent loops ([[loop-engineering|Loop Engineering]]) and multi-agent graphs ([[graph-engineering|Graph Engineering]]). Tool calls are traced ([[llm-observability-and-tracing|LLM Observability and Tracing]]), and tool descriptions count towards token costs ([[llm-cost-optimization|LLM Cost Optimization]]). MCP is one of the layers in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]] and is used by agents ([[agentic-ai|Agentic AI]]) and coding tools ([[vibe-coding|Vibe Coding]]).

### Key takeaway

MCP standardises the connection between AI applications and tools, data and prompts; it does not standardise trust, so every server still needs least privilege, human approval for critical actions and a check of where it comes from.

### Sources

- Anthropic (2024). *Introducing the Model Context Protocol.* Anthropic News, 25 November 2024. [anthropic.com](https://www.anthropic.com/news/model-context-protocol)
- Model Context Protocol. *Architecture overview.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/learn/architecture)
- Model Context Protocol. *Specification, version 2025-06-18.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18)
- Model Context Protocol. *Specification: Tools.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/latest/server/tools)
- Model Context Protocol. *Security Best Practices.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- A2A Project. *Agent2Agent (A2A) Protocol.* a2a-protocol.org. [a2a-protocol.org](https://a2a-protocol.org/latest/)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Das Model Context Protocol (MCP) ist ein offenes Protokoll, das standardisiert, wie KI-Anwendungen externe Werkzeuge, Datenquellen und Prompt-Vorlagen anbinden, statt dass jede Anwendung für jedes Werkzeug eine eigene Integration baut (Anthropic, 2024b). Es folgt einer Client-Server-Architektur mit JSON-RPC-2.0-Nachrichten: Eine Host-Anwendung erzeugt je Server einen Client, und Server stellen Werkzeuge, Ressourcen und Prompts bereit (MCP architecture docs). MCP ist teilweise vom Language Server Protocol inspiriert (MCP specification). Verwandte Protokolle decken andere Achsen ab, am bekanntesten A2A für die Kommunikation zwischen Agenten (A2A protocol docs). MCP standardisiert die Verbindung, nicht das Vertrauen: Ein gemeinsames Protokoll macht einen fremden Server nicht sicher.

### Funktionsweise

#### 1. Das M×N-Problem

```text
ohne gemeinsames Protokoll:   M Anwendungen × N Werkzeuge = M×N Integrationen
mit MCP:                      M Clients + N Server        = M+N Implementierungen
```

Bisher brauchte jede neue Datenquelle eine eigene Implementierung; MCP ersetzt diese zersplitterten Integrationen durch ein einziges Protokoll (Anthropic, 2024b). Das Language Server Protocol löste dasselbe Problem für Programmiersprachen und Editoren, und MCP standardisiert auf ähnliche Weise die Einbindung von Kontext und Werkzeugen in KI-Anwendungen (MCP specification).

#### 2. Architektur

```text
Host (KI-Anwendung, z. B. Claude Code oder VS Code)
  ├── MCP-Client 1 ── stdio ──────────────► MCP-Server 1 (z. B. lokales Dateisystem)
  └── MCP-Client 2 ── Streamable HTTP ────► MCP-Server 2 (z. B. entfernter Issue-Tracker)
```

- **Host:** die KI-Anwendung, die einen oder mehrere Clients koordiniert.
- **Client:** hält eine eigene Verbindung zu genau einem Server.
- **Server:** ein Programm, das Kontext bereitstellt, lokal über stdio (meist für einen Client) oder entfernt über Streamable HTTP (meist für viele Clients) (MCP architecture docs).

Die Datenschicht beruht auf JSON-RPC 2.0 und umfasst Discovery, Server- und Client-Funktionen sowie Benachrichtigungen; die Transportschicht regelt Verbindungen, Nachrichtenrahmen und Autorisierung, wobei OAuth für Token empfohlen wird (MCP architecture docs). MCP legt nur das Protokoll für den Austausch von Kontext fest; wie eine Anwendung LLMs nutzt oder den bereitgestellten Kontext verwaltet, bleibt der Anwendung überlassen (MCP architecture docs).

#### 3. Primitive

- **Tools:** ausführbare Funktionen, die die Anwendung aufrufen kann, etwa Dateioperationen, API-Aufrufe oder Datenbankabfragen; ermittelt mit tools/list und ausgeführt mit tools/call.
- **Resources:** Datenquellen, die Kontext liefern, etwa Dateiinhalte, Datenbankeinträge oder API-Antworten.
- **Prompts:** wiederverwendbare Vorlagen, etwa Systemprompts oder Few-Shot-Beispiele (MCP architecture docs).

Clients können Elicitation anbieten, mit der Server Nutzende um Informationen oder Bestätigungen bitten; Sampling, mit dem Server Antworten vom Modell des Clients anforderten, ist seit Protokollversion 2026-07-28 veraltet (MCP architecture docs).

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
 "params": {"name": "search_norms", "arguments": {"query": "data portability"}}}
```

#### 4. MCP vs. proprietäres Function Calling

| | Proprietäres Function Calling | MCP |
|---|---|---|
| Umfang | Werkzeuge (Funktionsaufrufe) | Werkzeuge, Ressourcen und Prompts (MCP architecture docs) |
| Bindung | An eine Modell-API gebunden | Unabhängig von Modell und Anbieter |
| Wiederverwendung | Integration je Anwendung neu gebaut | Ein Server, nutzbar von jedem MCP-Host (Anthropic, 2024b) |
| Transport | Teil des API-Aufrufs | Eigenes Protokoll (stdio oder HTTP, JSON-RPC) |

Function Calling bleibt die Grundlage; MCP standardisiert, wie Werkzeugdefinitionen und Ergebnisse zwischen Anwendung und Werkzeuganbieter transportiert werden.

#### 5. Sicherheit

MCP-Server sind Fremdcode im Harness, und ihre Werkzeugbeschreibungen erreichen das Modell als Text:

- **Mensch im Prozess:** Es sollte immer einen Menschen geben, der Werkzeugaufrufe ablehnen kann; Clients sollten Werkzeugeingaben vor dem Aufruf eines Servers anzeigen, Ergebnisse vor der Weitergabe an das Modell prüfen und die Werkzeugnutzung protokollieren; Annotationen von nicht vertrauenswürdigen Servern gelten selbst als nicht vertrauenswürdig (MCP tools specification).
- **Prompt Injection über Werkzeuge und Daten:** Abgerufene Inhalte und Werkzeugbeschreibungen verwischen die Grenze zwischen Daten und Anweisungen (Greshake et al., 2023).
- **Kompromittierte lokale Server:** Lokale Server laufen auf dem Rechner der Nutzenden mit direktem Systemzugriff; bösartige Startbefehle können beliebigen Code ausführen, Daten abfließen lassen oder zerstören, daher müssen Clients den genauen Befehl anzeigen und eine ausdrückliche Zustimmung verlangen (MCP security best practices).
- **Autorisierung:** Token-Passthrough ist verboten, weit gefasste Token-Berechtigungen vergrößern den Schaden einer Kompromittierung, und MCP-Proxy-Server können Confused-Deputy-Schwachstellen erzeugen (MCP security best practices).

#### 6. Verwandte Protokolle

- **A2A (Agent2Agent):** Kommunikation zwischen Agenten verschiedener Frameworks und Anbieter, die Aufgaben delegieren und Ergebnisse teilen, ohne internes Gedächtnis oder Werkzeuge offenzulegen; MCP verbindet Agent und Werkzeug, A2A Agent und Agent, beide ergänzen sich (A2A protocol docs).
- **OpenAPI:** ein Beschreibungsformat für HTTP-APIs, teils genutzt, wenn nur klassischer API-Zugriff nötig ist.
- **LSP:** kein KI-Protokoll, aber das Vorbild für MCPs Client-Server-Idee (MCP specification).

#### Ursprung und Varianten

Anthropic veröffentlichte MCP am 25. November 2024 als Open Source, zusammen mit der Spezifikation, SDKs, Unterstützung lokaler Server in Claude Desktop und Referenzservern für Systeme wie Google Drive, Slack, GitHub, Git und Postgres (Anthropic, 2024b). Das Protokoll wurde mehrfach überarbeitet; die aktuelle Version macht Anfragen zustandslos, sodass jede Anfrage Protokollversion und Fähigkeiten mitführt, und Server geben ihre Fähigkeiten über eine Discovery-Anfrage bekannt (MCP architecture docs).

### Wann einsetzen

- Wenn Werkzeuge oder Datenquellen von mehreren KI-Anwendungen oder Agenten nutzbar sein sollen.
- Wenn eine Anwendung eine wachsende Zahl bestehender Server einbinden soll statt eigener Konnektoren.
- Nicht, wenn eine einzelne Anwendung eine interne Funktion aufruft; einfaches Function Calling oder ein direkter API-Aufruf ist dann einfacher.

### Stärken und Grenzen

**Stärken**
- Ein Server pro Werkzeug statt einer Integration pro Anwendung und Werkzeug (Anthropic, 2024b).
- Unabhängig von Modell und Anbieter; Werkzeuge, Ressourcen und Prompts in einem Protokoll (MCP architecture docs).
- Dynamische Discovery: Clients fragen die verfügbaren Primitive zur Laufzeit ab (MCP architecture docs).

**Einschränkungen**
- Server von Dritten sind eine Angriffsfläche: Lokale Server können beliebigen Code ausführen, und Werkzeugbeschreibungen können eingeschleuste Anweisungen enthalten (MCP security best practices; Greshake et al., 2023).
- Viele angebundene Server bringen viele Werkzeugbeschreibungen in den Kontext ([[context-engineering|Context Engineering]]).
- Das Protokoll entwickelt sich weiter, mit veralteten Funktionen und neuen Versionen.

### Vergleich

| Protokoll | Achse | Geeignet für |
|----------|----------------|------------|
| MCP | Agent oder Anwendung ↔ Werkzeuge und Daten (MCP architecture docs) | Wiederverwendbare Werkzeug- und Datenanbindungen |
| A2A | Agent ↔ Agent (A2A protocol docs) | Delegation zwischen Agenten verschiedener Anbieter |
| Function Calling | Modell ↔ Funktionen einer Anwendung | Wenige, anwendungsspezifische Werkzeuge |
| OpenAPI | Client ↔ HTTP-API | Beschreibung klassischer Web-APIs |

### In der Praxis

MCP berührt zwei Disziplinen: Resources sind eine strukturierte Quelle für das, was [[context-engineering|Context Engineering]] in den Kontext bringt, und Werkzeuge und ihre sichere Einbindung gehören zum [[harness-engineering|Harness Engineering]]. Welchen Servern vertraut wird, welche Berechtigungen gelten und was in den Kontext gelangt, bleiben Entscheidungen der Anwendung. Frameworks wie [[langchain-and-langgraph|LangChain und LangGraph]] wandeln MCP-Werkzeuge in eigene Werkzeuge um, Skills beschreiben, wie angebundene Werkzeuge in Abläufen genutzt werden ([[agent-skills|Agent Skills]]), und MCP-Konnektoren sind Bausteine von Agentenschleifen ([[loop-engineering|Loop Engineering]]) und Multi-Agenten-Graphen ([[graph-engineering|Graph Engineering]]). Werkzeugaufrufe werden getraced ([[llm-observability-and-tracing|LLM-Observability und Tracing]]), und Werkzeugbeschreibungen zählen zu den Token-Kosten ([[llm-cost-optimization|LLM-Kostenoptimierung]]). MCP ist eine der Ebenen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]] und wird von Agenten ([[agentic-ai|Agentic AI]]) und Coding-Werkzeugen ([[vibe-coding|Vibe Coding]]) genutzt.

### Merksatz

MCP standardisiert die Verbindung zwischen KI-Anwendungen und Werkzeugen, Daten und Prompts, nicht aber das Vertrauen; jeder Server braucht weiterhin Least Privilege, menschliche Freigabe für kritische Aktionen und eine Prüfung seiner Herkunft.

### Quellen

- Anthropic (2024). *Introducing the Model Context Protocol.* Anthropic News, 25 November 2024. [anthropic.com](https://www.anthropic.com/news/model-context-protocol)
- Model Context Protocol. *Architecture overview.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/learn/architecture)
- Model Context Protocol. *Specification, version 2025-06-18.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18)
- Model Context Protocol. *Specification: Tools.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/latest/server/tools)
- Model Context Protocol. *Security Best Practices.* modelcontextprotocol.io. [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- A2A Project. *Agent2Agent (A2A) Protocol.* a2a-protocol.org. [a2a-protocol.org](https://a2a-protocol.org/latest/)
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
