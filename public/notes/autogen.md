---
title_en: AutoGen
title_de: AutoGen
entity_type: Technology
aliases:
- AutoGen
- Microsoft AutoGen
- AutoGen AgentChat
sources:
- https://arxiv.org/abs/2308.08155
- https://github.com/microsoft/autogen
- https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

AutoGen is an open-source framework from [[microsoft|Microsoft]] Research for building LLM applications from several agents that converse with each other to solve a task; agents can be backed by LLMs, human input, tools or a combination, and developers program their interaction in natural language and code (Wu et al., 2023). Its two central ideas are "conversable agents" and "conversation programming", which turns a workflow into message passing between agents (Wu et al., 2023). Later versions split the framework into a low-level event-driven Core API, the higher-level AgentChat API and extensions (Microsoft, n.d.). AutoGen is now in maintenance mode: it receives no new features, and Microsoft points new users to its successor, Microsoft Agent Framework, built by the AutoGen and Semantic Kernel teams (Microsoft, n.d.; Microsoft Learn, 2026).

### Core concepts

```text
ConversableAgent  (send / receive / generate_reply; backed by LLM, human, tools)
  ├─ AssistantAgent   – LLM-backed, writes answers and code
  └─ UserProxyAgent   – asks the human or executes code / function calls
GroupChatManager      – coordinates several agents in a group chat
auto-reply: on every received message an agent generates a reply and sends it back,
            until a termination condition holds → control flow emerges from the conversation
```

#### Conversable agents

A conversable agent has a role, sends and receives messages, keeps its context from these messages and can be configured with capabilities from LLMs, humans and tools (Wu et al., 2023). The built-in AssistantAgent acts as an AI assistant backed by an LLM; the UserProxyAgent solicits human input or executes code and function calls suggested by the LLM; developers create specialised agents by reusing or extending these classes (Wu et al., 2023).

#### Conversation programming

Applications are built in two steps: defining conversable agents with roles and capabilities, then programming their interaction (Wu et al., 2023). By default each agent automatically generates a reply when it receives a message and sends it back unless a termination condition is met, so the flow of the conversation follows from registered reply functions without a separate control plane; control can be expressed both in code and in natural-language prompts (Wu et al., 2023).

#### Conversation patterns

The paper demonstrates two-agent chats, hierarchical and dynamic group chats in which a manager selects the next speaker, and human-in-the-loop modes, with applications from maths problem solving and retrieval-augmented question answering to multi-agent coding and conversational chess (Wu et al., 2023). In the OptiGuide coding application, a Commander, Writer and Safeguard agent check and execute code; AutoGen reduced its core workflow code from over 430 to 100 lines (Wu et al., 2023).

#### Origin and variants

Wu et al. (2023), from Microsoft Research and several universities, introduced AutoGen in 2023. The current code base uses a layered design: the Core API implements message passing and event-driven agents with local and distributed runtimes, AgentChat offers an opinionated API for patterns such as two-agent and group chats, and Extensions add model clients and code execution; AutoGen Studio is a no-code GUI and AutoGen Bench a benchmarking suite (Microsoft, n.d.). Microsoft Agent Framework replaces AutoGen's two programming models with a single data-flow workflow abstraction inspired by AutoGen's experimental GraphFlow (Microsoft Learn, 2026).

### Common usage

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Say 'Hello World!'"))
    await model_client.close()

asyncio.run(main())
# several agents: RoundRobinGroupChat(participants=[agent1, agent2],
#                 termination_condition=...) then await team.run(task=...)
```

Source: Microsoft (n.d.), README quickstart; group chat from Microsoft Learn (2026).

### When to use it

- Prototyping [[multi-agent-systems|multi-agent systems]] in which agents with different roles critique, check or extend each other's work (Wu et al., 2023).
- Maintaining existing AutoGen applications, or reading research that builds on its conversation patterns.
- Not for new production projects: Microsoft recommends starting with Microsoft Agent Framework and offers a migration guide ([[agent-frameworks|agent frameworks]]; Microsoft, n.d.).

### Strengths and limitations

**Strengths**
- A generic agent abstraction that mixes LLMs, humans and tools and supports many conversation patterns (Wu et al., 2023).
- Less development code: the OptiGuide workflow shrank from over 430 to 100 lines (Wu et al., 2023).
- Human-in-the-loop modes are a configuration option of the user proxy agent (Wu et al., 2023).

**Limitations**
- In maintenance mode with no new features, community managed (Microsoft, n.d.).
- Microsoft's migration guide describes its low-level model as too complex for most users and its high-level team model as limiting for complex behaviour (Microsoft Learn, 2026).
- Free conversation between agents makes control flow implicit; newer frameworks add explicit workflows ([[agent-frameworks|agent frameworks]]).

### Comparison

| | AutoGen | Microsoft Agent Framework |
|---|---|---|
| Status | maintenance mode | successor, production-ready release |
| Multi-agent model | event-driven Core API plus high-level teams (e.g. round-robin group chat) | one workflow abstraction with typed, data-flow edges |
| Extra features | AutoGen Studio, AutoGen Bench | middleware, hosted tools, checkpointing |

Sources: Microsoft (n.d.); Microsoft Learn (2026).

### In practice

Agent conversations can loop or execute generated code, so set termination conditions, sandbox code execution and connect only to trusted MCP servers; the README warns that MCP servers may execute local commands or expose sensitive information (Microsoft, n.d.; [[mcp-and-related-protocols|MCP and related protocols]]). Single-agent code migrates to Agent Framework with similar APIs, while multi-agent patterns need rethinking from event-driven to data-flow workflows (Microsoft Learn, 2026).

### Key takeaway

AutoGen made multi-agent conversation a programming model, with conversable agents backed by LLMs, humans and tools; it shaped later frameworks but is now in maintenance mode in favour of Microsoft Agent Framework.

### Sources

- Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D. & Wang, C. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- Microsoft (n.d.). *AutoGen* (README). GitHub. [github.com](https://github.com/microsoft/autogen)
- Microsoft Learn (2026). *AutoGen to Microsoft Agent Framework Migration Guide.* Last updated 25 August 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

AutoGen ist ein Open-Source-Framework von [[microsoft|Microsoft]] Research, um LLM-Anwendungen aus mehreren Agenten aufzubauen, die miteinander sprechen, um eine Aufgabe zu lösen; Agenten können auf LLMs, menschlichen Eingaben, Tools oder einer Kombination beruhen, und ihr Zusammenspiel wird in natürlicher Sprache und Code programmiert (Wu et al., 2023). Seine zwei zentralen Ideen sind „Conversable Agents“ und „Conversation Programming“, das einen Workflow in Nachrichtenaustausch zwischen Agenten übersetzt (Wu et al., 2023). Spätere Versionen teilen das Framework in eine ereignisgesteuerte Core API, die höhere AgentChat API und Erweiterungen (Microsoft, n.d.). AutoGen befindet sich inzwischen im Wartungsmodus: Es erhält keine neuen Funktionen, und Microsoft verweist neue Nutzende auf den Nachfolger Microsoft Agent Framework, entwickelt von den Teams von AutoGen und Semantic Kernel (Microsoft, n.d.; Microsoft Learn, 2026).

### Kernkonzepte

```text
ConversableAgent  (send / receive / generate_reply; gestützt auf LLM, Mensch, Tools)
  ├─ AssistantAgent   – LLM-gestützt, schreibt Antworten und Code
  └─ UserProxyAgent   – fragt den Menschen oder führt Code / Funktionsaufrufe aus
GroupChatManager      – koordiniert mehrere Agenten in einem Gruppenchat
Auto-Reply: auf jede empfangene Nachricht erzeugt ein Agent eine Antwort und sendet sie zurück,
            bis eine Abbruchbedingung gilt → Kontrollfluss ergibt sich aus der Konversation
```

#### Conversable Agents

Ein Conversable Agent hat eine Rolle, sendet und empfängt Nachrichten, führt seinen Kontext aus diesen Nachrichten und lässt sich mit Fähigkeiten aus LLMs, Menschen und Tools ausstatten (Wu et al., 2023). Der eingebaute AssistantAgent arbeitet als KI-Assistent auf Basis eines LLM; der UserProxyAgent holt menschliche Eingaben ein oder führt Code und vom LLM vorgeschlagene Funktionsaufrufe aus; spezialisierte Agenten entstehen durch Wiederverwenden oder Erweitern dieser Klassen (Wu et al., 2023).

#### Conversation Programming

Anwendungen entstehen in zwei Schritten: Conversable Agents mit Rollen und Fähigkeiten definieren und dann ihr Zusammenspiel programmieren (Wu et al., 2023). Standardmäßig erzeugt jeder Agent beim Empfang einer Nachricht automatisch eine Antwort und sendet sie zurück, sofern keine Abbruchbedingung erfüllt ist; der Gesprächsverlauf ergibt sich so aus registrierten Antwortfunktionen ohne eigene Steuerungsschicht, und die Steuerung lässt sich sowohl in Code als auch in Prompts in natürlicher Sprache ausdrücken (Wu et al., 2023).

#### Konversationsmuster

Das Paper zeigt Chats zweier Agenten, hierarchische und dynamische Gruppenchats, in denen ein Manager den nächsten Sprecher wählt, sowie Modi mit Menschen in der Schleife, mit Anwendungen vom Lösen mathematischer Aufgaben und Fragebeantwortung mit Retrieval bis zu Multi-Agenten-Programmierung und Schach im Dialog (Wu et al., 2023). In der Programmieranwendung OptiGuide prüfen und führen ein Commander-, ein Writer- und ein Safeguard-Agent Code aus; AutoGen verringerte den zentralen Workflow-Code von über 430 auf 100 Zeilen (Wu et al., 2023).

#### Herkunft und Varianten

Wu et al. (2023) von Microsoft Research und mehreren Universitäten stellten AutoGen 2023 vor. Die aktuelle Codebasis ist geschichtet: Die Core API setzt Nachrichtenaustausch und ereignisgesteuerte Agenten mit lokaler und verteilter Laufzeitumgebung um, AgentChat bietet eine festgelegte API für Muster wie Zwei-Agenten- und Gruppenchats, und Extensions ergänzen Modell-Clients und Codeausführung; AutoGen Studio ist eine Oberfläche ohne Programmierung und AutoGen Bench eine Benchmark-Sammlung (Microsoft, n.d.). Microsoft Agent Framework ersetzt die zwei Programmiermodelle von AutoGen durch eine einzige Workflow-Abstraktion mit Datenfluss, angelehnt an das experimentelle GraphFlow von AutoGen (Microsoft Learn, 2026).

### Typische Verwendung

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Say 'Hello World!'"))
    await model_client.close()

asyncio.run(main())
# mehrere Agenten: RoundRobinGroupChat(participants=[agent1, agent2],
#                  termination_condition=...) und dann await team.run(task=...)
```

Quelle: Microsoft (n.d.), Schnellstart im README; Gruppenchat aus Microsoft Learn (2026).

### Wann einsetzen

- Für Prototypen von [[multi-agent-systems|Multi-Agenten-Systemen]], in denen Agenten mit verschiedenen Rollen die Arbeit der anderen kritisieren, prüfen oder ergänzen (Wu et al., 2023).
- Zur Pflege bestehender AutoGen-Anwendungen oder beim Lesen von Forschung, die auf seinen Konversationsmustern aufbaut.
- Nicht für neue Produktivprojekte: Microsoft empfiehlt, mit Microsoft Agent Framework zu beginnen, und bietet einen Migrationsleitfaden ([[agent-frameworks|Agenten-Frameworks]]; Microsoft, n.d.).

### Stärken und Grenzen

**Stärken**
- Eine allgemeine Agenten-Abstraktion, die LLMs, Menschen und Tools verbindet und viele Konversationsmuster unterstützt (Wu et al., 2023).
- Weniger Entwicklungscode: Der Workflow von OptiGuide schrumpfte von über 430 auf 100 Zeilen (Wu et al., 2023).
- Modi mit Menschen in der Schleife sind eine Konfigurationsoption des User-Proxy-Agenten (Wu et al., 2023).

**Grenzen**
- Im Wartungsmodus ohne neue Funktionen, von der Community betreut (Microsoft, n.d.).
- Der Migrationsleitfaden von Microsoft beschreibt das Low-Level-Modell als zu komplex für die meisten Nutzenden und das High-Level-Team-Modell als einschränkend für komplexes Verhalten (Microsoft Learn, 2026).
- Freie Konversation zwischen Agenten macht den Kontrollfluss implizit; neuere Frameworks ergänzen explizite Workflows ([[agent-frameworks|Agenten-Frameworks]]).

### Vergleich

| | AutoGen | Microsoft Agent Framework |
|---|---|---|
| Status | Wartungsmodus | Nachfolger, produktionsreife Version |
| Multi-Agenten-Modell | ereignisgesteuerte Core API plus High-Level-Teams (z. B. Round-Robin-Gruppenchat) | eine Workflow-Abstraktion mit typisierten Datenfluss-Kanten |
| Weitere Funktionen | AutoGen Studio, AutoGen Bench | Middleware, gehostete Tools, Checkpointing |

Quellen: Microsoft (n.d.); Microsoft Learn (2026).

### In der Praxis

Agentengespräche können in Schleifen geraten oder erzeugten Code ausführen; deshalb gehören Abbruchbedingungen, eine abgeschottete Codeausführung und nur vertrauenswürdige MCP-Server dazu; das README warnt, dass MCP-Server lokale Befehle ausführen oder sensible Informationen preisgeben können (Microsoft, n.d.; [[mcp-and-related-protocols|MCP und verwandte Protokolle]]). Code mit einem einzelnen Agenten lässt sich mit ähnlichen [[apis|APIs]] zu Agent Framework migrieren, während Multi-Agenten-Muster ein Umdenken von ereignisgesteuerten zu Datenfluss-Workflows verlangen (Microsoft Learn, 2026).

### Merksatz

AutoGen machte die Konversation mehrerer Agenten zum Programmiermodell, mit Conversable Agents auf Basis von LLMs, Menschen und Tools; es prägte spätere Frameworks, ist aber zugunsten von Microsoft Agent Framework im Wartungsmodus.

### Quellen

- Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D. & Wang, C. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- Microsoft (n.d.). *AutoGen* (README). GitHub. [github.com](https://github.com/microsoft/autogen)
- Microsoft Learn (2026). *AutoGen to Microsoft Agent Framework Migration Guide.* Zuletzt aktualisiert am 25. August 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
