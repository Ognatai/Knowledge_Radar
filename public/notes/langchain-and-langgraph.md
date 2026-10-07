---
title_en: LangChain and LangGraph
title_de: LangChain und LangGraph
entity_type: Technology
sources:
- https://docs.langchain.com/oss/python/langchain/overview
- https://docs.langchain.com/oss/python/langgraph/overview
- https://github.com/langchain-ai/langchain-mcp-adapters
- https://arxiv.org/abs/2210.03629
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LangChain and LangGraph are open-source frameworks for building LLM applications and agents. LangChain provides create_agent, a minimal, configurable agent harness composed of a model, tools, a prompt and middleware (LangChain docs); LangGraph is the lower-level orchestration framework and runtime underneath, in which agents are graphs of steps over a shared state with durable execution, persistence and human-in-the-loop support (LangGraph docs). Adapters connect both to tools exposed through the Model Context Protocol (LangChain MCP adapters).

### Core concepts

- **Agent = model + harness:** In LangChain, the harness is everything around the model loop, the prompt, the tools and any middleware; create_agent composes them, and a standard interface supports many model providers (LangChain docs; [[harness-engineering|Harness Engineering]]).
- **Agent loop:** The agent alternates between reasoning and tool calls until it can answer, an approach introduced as ReAct, which interleaves reasoning traces with actions such as API calls (Yao et al., 2022; [[agentic-ai|Agentic AI]]).
- **LangGraph graphs:** Applications are graphs whose nodes are steps, either deterministic code or LLM-driven decisions, that read and update a shared state, and whose edges determine the next step; this allows deterministic and agentic steps in the same graph (LangGraph docs).
- **Durable execution and persistence:** LangGraph persists the state so that long-running agents can resume after failures, pause for human approval and keep memory across turns (LangGraph docs).
- **Relationship:** LangChain agents are built on top of LangGraph, using its durable execution, human-in-the-loop support and persistence (LangChain docs).
- **MCP adapters:** Convert Model Context Protocol tools into LangChain tools and connect to several MCP servers (LangChain MCP adapters; [[mcp-and-related-protocols|MCP and Related Protocols]]).

### Common usage

```python
from langchain.agents import create_agent

def search_norms(query: str) -> str:
    """Search the legal knowledge base for norms matching the query."""
    ...

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[search_norms],
    system_prompt="Answer with citations to the norms you used.",
)
result = agent.invoke({"messages": [{"role": "user", "content": "Which norms govern data portability?"}]})
```

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    context: list[str]
    answer: str

def retrieve(state: State) -> dict: ...
def generate(state: State) -> dict: ...

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
app = graph.compile()
```

The first example is a tool-calling agent with LangChain; the second a fixed RAG workflow in LangGraph, in which each step is a node and the edges fix the order (LangChain docs; LangGraph docs). The model identifier in the first example is illustrative.

### When to use it

- When a standard tool-calling agent should be built quickly with configurable model, tools and prompt (LangChain docs).
- When a workflow needs explicit control over steps, branching, loops, persistence or human approval, LangGraph fits (LangGraph docs).
- When tools are already exposed as MCP servers, the adapters reuse them directly (LangChain MCP adapters).

### Strengths and limitations

**Strengths**
- Composable agents from model, tools, prompt and middleware with a standard model interface (LangChain docs).
- Fine-grained control that mixes deterministic and LLM-driven steps in one graph (LangGraph docs).
- Durable execution, streaming and human-in-the-loop built into the runtime (LangGraph docs).

**Limitations**
- LangGraph is deliberately low-level, so more of the application logic must be written explicitly (LangGraph docs).
- Abstractions add a layer between the application and the model provider's API, which must be understood when debugging; tracing tools help (LangChain docs; [[llm-observability-and-tracing|LLM Observability and Tracing]]).
- Agent loops in the ReAct style still depend on the model's reasoning and can fail on tool use (Yao et al., 2022).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| LangChain create_agent | High-level agent harness from model, tools, prompt and middleware (LangChain docs) | Standard tool-calling agents |
| LangGraph | Low-level graph runtime with shared state and durable execution (LangGraph docs) | Custom workflows and long-running agents |
| Direct provider SDK | Calls the model API without a framework | Small applications with few steps |
| MCP | Protocol for exposing tools and context to any client (LangChain MCP adapters) | Tools shared across frameworks and clients |

### In practice

Applications start with the simplest structure that works: a fixed workflow where the steps are known, an agent only where the model must decide the next step ([[agentic-ai|Agentic AI]]; LangGraph docs). Traces of agent runs are inspected to debug tool calls and state transitions (LangChain docs), and agent behaviour is evaluated on task sets before deployment.

### Key takeaway

LangChain offers a high-level agent harness, and LangGraph the underlying graph runtime for controllable, stateful and long-running agent workflows.

### Sources

- LangChain. *LangChain overview.* LangChain documentation (Python). [docs.langchain.com](https://docs.langchain.com/oss/python/langchain/overview)
- LangChain. *LangGraph overview.* LangGraph documentation (Python). [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview)
- LangChain. *langchain-mcp-adapters.* GitHub repository. [github.com](https://github.com/langchain-ai/langchain-mcp-adapters)
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LangChain und LangGraph sind Open-Source-Frameworks zum Bau von LLM-Anwendungen und Agenten. LangChain stellt create_agent bereit, einen minimalen, konfigurierbaren Agent-Harness aus Modell, Tools, Prompt und Middleware (LangChain docs); LangGraph ist das darunterliegende Orchestrierungs-Framework und Laufzeitsystem auf niedrigerer Ebene, in dem Agenten Graphen aus Schritten über einen gemeinsamen Zustand sind, mit dauerhafter Ausführung, Persistenz und Unterstützung für Human-in-the-Loop (LangGraph docs). Adapter verbinden beide mit Tools, die über das Model Context Protocol bereitgestellt werden (LangChain MCP adapters).

### Kernkonzepte

- **Agent = Modell + Harness:** In LangChain ist der Harness alles rund um die Modellschleife: Prompt, Tools und Middleware; create_agent setzt sie zusammen, und eine einheitliche Schnittstelle unterstützt viele Modellanbieter (LangChain docs; [[harness-engineering|Harness Engineering]]).
- **Agent-Schleife:** Der Agent wechselt zwischen Überlegen und Tool-Aufrufen, bis er antworten kann; dieser Ansatz wurde als ReAct eingeführt, das Gedankengänge mit Aktionen wie API-Aufrufen verzahnt (Yao et al., 2022; [[agentic-ai|Agentic AI]]).
- **LangGraph-Graphen:** Anwendungen sind Graphen, deren Knoten Schritte sind, entweder deterministischer Code oder LLM-gesteuerte Entscheidungen, die einen gemeinsamen Zustand lesen und aktualisieren, und deren Kanten den nächsten Schritt bestimmen; so lassen sich deterministische und agentische Schritte im selben Graphen verbinden (LangGraph docs).
- **Dauerhafte Ausführung und Persistenz:** LangGraph speichert den Zustand, sodass lang laufende Agenten nach Fehlern weitermachen, für menschliche Freigaben pausieren und über mehrere Runden ein Gedächtnis behalten können (LangGraph docs).
- **Verhältnis:** LangChain-Agenten bauen auf LangGraph auf und nutzen dessen dauerhafte Ausführung, Human-in-the-Loop-Unterstützung und Persistenz (LangChain docs).
- **MCP-Adapter:** Wandeln Tools des Model Context Protocol in LangChain-Tools um und verbinden sich mit mehreren MCP-Servern (LangChain MCP adapters; [[mcp-and-related-protocols|MCP und ähnliche Protokolle]]).

### Typische Verwendung

```python
from langchain.agents import create_agent

def search_norms(query: str) -> str:
    """Search the legal knowledge base for norms matching the query."""
    ...

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[search_norms],
    system_prompt="Answer with citations to the norms you used.",
)
result = agent.invoke({"messages": [{"role": "user", "content": "Which norms govern data portability?"}]})
```

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    context: list[str]
    answer: str

def retrieve(state: State) -> dict: ...
def generate(state: State) -> dict: ...

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
app = graph.compile()
```

Das erste Beispiel ist ein Tool-aufrufender Agent mit LangChain, das zweite ein fester RAG-Ablauf in LangGraph, in dem jeder Schritt ein Knoten ist und die Kanten die Reihenfolge festlegen (LangChain docs; LangGraph docs). Die Modellbezeichnung im ersten Beispiel ist nur beispielhaft.

### Wann einsetzen

- Wenn ein Standard-Agent mit Tool-Aufrufen schnell und mit konfigurierbarem Modell, Tools und Prompt gebaut werden soll (LangChain docs).
- Wenn ein Ablauf ausdrückliche Kontrolle über Schritte, Verzweigungen, Schleifen, Persistenz oder menschliche Freigaben braucht, passt LangGraph (LangGraph docs).
- Wenn Tools bereits als MCP-Server vorliegen, verwenden die Adapter sie direkt wieder (LangChain MCP adapters).

### Stärken und Grenzen

**Stärken**
- Zusammensetzbare Agenten aus Modell, Tools, Prompt und Middleware mit einheitlicher Modellschnittstelle (LangChain docs).
- Feingranulare Kontrolle, die deterministische und LLM-gesteuerte Schritte in einem Graphen verbindet (LangGraph docs).
- Dauerhafte Ausführung, Streaming und Human-in-the-Loop sind im Laufzeitsystem eingebaut (LangGraph docs).

**Einschränkungen**
- LangGraph ist bewusst auf niedriger Ebene angesiedelt, sodass mehr Anwendungslogik ausdrücklich geschrieben werden muss (LangGraph docs).
- Abstraktionen schieben eine Schicht zwischen Anwendung und API des Modellanbieters, die beim Debugging verstanden werden muss; Tracing-Werkzeuge helfen (LangChain docs; [[llm-observability-and-tracing|LLM-Observability und Tracing]]).
- Agent-Schleifen im ReAct-Stil hängen weiterhin vom Schlussfolgern des Modells ab und können bei der Tool-Nutzung scheitern (Yao et al., 2022).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| LangChain create_agent | High-Level-Agent-Harness aus Modell, Tools, Prompt und Middleware (LangChain docs) | Standard-Agenten mit Tool-Aufrufen |
| LangGraph | Graph-Laufzeitsystem auf niedriger Ebene mit gemeinsamem Zustand und dauerhafter Ausführung (LangGraph docs) | Eigene Abläufe und lang laufende Agenten |
| Direktes SDK des Anbieters | Ruft die Modell-API ohne Framework auf | Kleine Anwendungen mit wenigen Schritten |
| MCP | Protokoll, um Tools und Kontext beliebigen Clients bereitzustellen (LangChain MCP adapters) | Tools, die über Frameworks und Clients hinweg geteilt werden |

### In der Praxis

Anwendungen beginnen mit der einfachsten funktionierenden Struktur: einem festen Ablauf, wo die Schritte bekannt sind, und einem Agenten nur dort, wo das Modell den nächsten Schritt entscheiden muss ([[agentic-ai|Agentic AI]]; LangGraph docs). Traces von Agentenläufen werden untersucht, um Tool-Aufrufe und Zustandsübergänge zu debuggen (LangChain docs), und das Verhalten von Agenten wird vor dem Einsatz an Aufgabensammlungen evaluiert.

### Merksatz

LangChain bietet einen High-Level-Agent-Harness, LangGraph das darunterliegende Graph-Laufzeitsystem für kontrollierbare, zustandsbehaftete und lang laufende Agentenabläufe.

### Quellen

- LangChain. *LangChain overview.* LangChain documentation (Python). [docs.langchain.com](https://docs.langchain.com/oss/python/langchain/overview)
- LangChain. *LangGraph overview.* LangGraph documentation (Python). [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview)
- LangChain. *langchain-mcp-adapters.* GitHub repository. [github.com](https://github.com/langchain-ai/langchain-mcp-adapters)
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
