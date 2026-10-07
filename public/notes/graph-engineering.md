---
title_en: Graph Engineering
title_de: Graph Engineering
entity_type: Method
sources:
- https://www.truefoundry.com/blog/graph-engineering-enterprise-guide
- https://theaioperator.io/p/what-is-graph-engineering-a-field
- https://docs.langchain.com/oss/python/langgraph/overview
- https://arxiv.org/abs/2308.08155
- https://arxiv.org/abs/2404.16130
- https://a2a-protocol.org/latest/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

"Graph engineering" is a term that spread rapidly in the AI engineering community in July 2026 as the supposed next step after [[loop-engineering|Loop Engineering]]. It has no single established definition: within 48 hours of its viral spread it had three competing meanings, orchestration graphs of multiple agents, graphs of feedback loops, and graph-structured knowledge and memory for agents (Ghelbur, 2026). The most discussed reading treats the topology of a multi-agent system, which nodes exist and which transitions are allowed, as an engineered artifact (Wang, 2026). Before using the term, it is worth asking which of the three meanings is meant.

### How it works

#### 1. Three competing meanings

```text
1. orchestration graphs       → multi-agent systems as an explicit topology
2. graphs of loops            → feedback loops that monitor and limit each other
3. graph-structured knowledge → agent memory as a typed graph instead of vector search
```

All three use "graph" as a metaphor for something beyond a single linear chain or loop, but they describe different systems (Ghelbur, 2026).

#### 2. Orchestration graphs

Graph engineering in this sense designs the topology of a multi-agent system: nodes can be agents, deterministic functions, routers, joins, tools or human checkpoints; edges are permitted transitions and communication paths; and runtime work graphs form, split and merge while tasks are processed. Loop engineering designs how each agentic node executes, graph engineering how the nodes are organised (Wang, 2026). An example assigns stable areas of ownership: a security agent owns authentication and audit logs, a data agent owns schema and migrations, an API agent owns endpoints (Wang, 2026). Patterns described earlier, such as orchestrator-workers, routers and supervisors, are building blocks of such graphs ([[agentic-ai|Agentic AI]]).

Production use requires explicit identities for every caller, graph, run and node identifiers propagated across systems, policy enforcement for which nodes may use which tools and MCP servers, budgets against cost explosions through fan-out and retries, and observability per node (Wang, 2026; [[mcp-and-related-protocols|MCP and Related Protocols]]; [[harness-engineering|Harness Engineering]]). Agent-to-agent communication across frameworks can use the A2A protocol, which lets agents delegate tasks and share results without exposing their internal memory or tools (A2A protocol docs).

#### 3. Graphs of loops

A second, more abstract reading wires many feedback loops, such as metrics, evaluations, audits and policies, into a network in which they monitor and correct each other; it is the least actionable meaning so far (Ghelbur, 2026). It overlaps with established quality control: deciding which check may override which other check, and keeping fixed reference points such as held-out test sets ([[quality-control|Quality Control]]; [[llm-evaluation|LLM Evaluation]]).

#### 4. Graph-structured knowledge

The third reading stores an agent's knowledge as typed nodes and edges, such as supersedes, depends_on, decided_by or caused, instead of a collection of documents searched by similarity; typed edges carry meaning that untyped links lack, and graph traversal can follow chains of reasoning across several notes (Ghelbur, 2026). Graphs help with multi-hop and corpus-wide questions, as GraphRAG shows for global questions (Edge et al., 2024), but they lose on simple lookups and cost more (Ghelbur, 2026). This reading is closest to [[knowledge-graph-engineering|Knowledge Graph Engineering]], [[graphrag|GraphRAG]] and [[knowledge-graphs|Knowledge Graphs]]; it should not be confused with the topology meaning, because knowledge graphs structure what a system knows, while orchestration graphs structure who the system is (Wang, 2026).

#### Origin and variants

The earliest documented use found was a blog post in early July 2026; the term spread after Peter Steinberger posted on 18 July 2026 "Are we still talking loops or did we shift to graphs yet?", and a viral claim about a large Stanford and Anthropic study turned out to be fabricated (Ghelbur, 2026). The underlying practice is older: dataflow and DAG orchestration, multi-agent systems research and agent frameworks that made graphs first-class objects (Wang, 2026), such as LangGraph, which mixes deterministic and LLM-driven steps in one graph (LangGraph docs), and AutoGen, in which multiple agents converse to solve tasks (Wu et al., 2023). What is new in 2026 is mainly the vocabulary and the framing as a step after loop engineering.

### When to use it

- When a system consists of several agents or loops whose responsibilities, transitions and permissions must be designed explicitly.
- When agent memory needs typed relations, for example decisions that supersede earlier decisions.
- In discussions, only after clarifying which of the three meanings is meant.

### Strengths and limitations

**Strengths**
- Makes the structure of multi-agent systems explicit, versionable and governable (Wang, 2026).
- Per-node identities, budgets and traces make complex runs traceable.
- Typed knowledge graphs answer multi-hop questions that vector search misses (Ghelbur, 2026).

**Limitations**
- The term is used inconsistently and is partly driven by hype, including fabricated claims (Ghelbur, 2026).
- Multi-agent graphs add failure modes: the failure of an intermediate agent cascades to downstream nodes, and missing edges keep information from where it is needed.
- Fan-out and retries can multiply costs ([[llm-cost-optimization|LLM Cost Optimization]]).
- Of the three readings, only graph-structured knowledge has a long research history and reproducible benchmarks; the other two rest mostly on practitioner reports (Ghelbur, 2026).

### Comparison

| Meaning | Closest established topic | Evidence |
|----------|----------------|------------|
| Orchestration graphs | Multi-agent systems, LangGraph, AutoGen (Wu et al., 2023) | Frameworks and practitioner reports |
| Graphs of loops | [[quality-control|Quality Control]], [[llm-evaluation|LLM Evaluation]] | Mostly conceptual (Ghelbur, 2026) |
| Graph-structured knowledge | GraphRAG, knowledge graphs (Edge et al., 2024) | Research and benchmarks |

### In practice

Orchestration graphs are built with frameworks such as [[langchain-and-langgraph|LangChain and LangGraph]], with each node traced and budgeted ([[llm-observability-and-tracing|LLM Observability and Tracing]]); recurring procedures for nodes can be packaged as [[agent-skills|Agent Skills]]. For knowledge, typed relations and validity dates are modelled in a knowledge graph. The term sits among the disciplines in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]], and its effect on daily work resembles that of [[vibe-coding|Vibe Coding]]: more automation needs more deliberate verification.

### Key takeaway

In 2026, "graph engineering" is not a settled technical term but a collective name for three different ideas; the solid core is graph-based orchestration of agents and graph-structured knowledge, both of which existed before the name.

### Sources

- Wang, B. (2026). *Graph Engineering for Multi-Agent Systems: Architecture, Governance, and Observability.* TrueFoundry Blog, 20 July 2026. [truefoundry.com](https://www.truefoundry.com/blog/graph-engineering-enterprise-guide)
- Ghelbur, E. (2026). *What Is Graph Engineering? A Field Guide for Builders.* The AI Operator, 21 July 2026. [theaioperator.io](https://theaioperator.io/p/what-is-graph-engineering-a-field)
- LangChain. *LangGraph overview.* LangChain documentation. [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview)
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* COLM 2024. [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- A2A Project. *Agent2Agent (A2A) Protocol.* a2a-protocol.org. [a2a-protocol.org](https://a2a-protocol.org/latest/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

„Graph Engineering“ ist ein Begriff, der sich im Juli 2026 schnell in der AI-Engineering-Community verbreitete, als angeblich nächste Stufe nach [[loop-engineering|Loop Engineering]]. Er hat keine einheitliche, etablierte Definition: Innerhalb von 48 Stunden nach seiner viralen Verbreitung hatte er drei konkurrierende Bedeutungen, Orchestrierungsgraphen mehrerer Agenten, Graphen aus Feedback-Schleifen und graphstrukturiertes Wissen und Gedächtnis für Agenten (Ghelbur, 2026). Die meistdiskutierte Lesart behandelt die Topologie eines Multi-Agenten-Systems, also welche Knoten es gibt und welche Übergänge erlaubt sind, als bewusst gestaltetes Artefakt (Wang, 2026). Bevor der Begriff verwendet wird, lohnt die Rückfrage, welche der drei Bedeutungen gemeint ist.

### Funktionsweise

#### 1. Drei konkurrierende Bedeutungen

```text
1. Orchestrierungsgraphen      → Multi-Agenten-Systeme als ausdrückliche Topologie
2. Graphen aus Loops           → Feedback-Schleifen, die sich gegenseitig überwachen und begrenzen
3. Graphstrukturiertes Wissen  → Agenten-Gedächtnis als typisierter Graph statt Vektorsuche
```

Alle drei nutzen „Graph“ als Metapher für etwas, das über eine einzelne lineare Kette oder Schleife hinausgeht, beschreiben aber unterschiedliche Systeme (Ghelbur, 2026).

#### 2. Orchestrierungsgraphen

Graph Engineering in diesem Sinn gestaltet die Topologie eines Multi-Agenten-Systems: Knoten können Agenten, deterministische Funktionen, Router, Zusammenführungen, Werkzeuge oder menschliche Freigabepunkte sein; Kanten sind erlaubte Übergänge und Kommunikationswege; und Arbeitsgraphen bilden sich zur Laufzeit, teilen sich und laufen wieder zusammen, während Aufgaben bearbeitet werden. Loop Engineering gestaltet, wie jeder agentische Knoten arbeitet, Graph Engineering, wie die Knoten organisiert sind (Wang, 2026). Ein Beispiel verteilt feste Zuständigkeiten: Ein Security-Agent verantwortet Authentifizierung und Audit-Logs, ein Daten-Agent Schema und Migrationen, ein API-Agent die Endpunkte (Wang, 2026). Früher beschriebene Muster wie Orchestrator-Worker, Router und Supervisor sind Bausteine solcher Graphen ([[agentic-ai|Agentic AI]]).

Im Produktivbetrieb braucht es eindeutige Identitäten für jeden Aufrufer, über Systemgrenzen weitergereichte Graph-, Lauf- und Knotenkennungen, durchgesetzte Regeln, welche Knoten welche Werkzeuge und MCP-Server nutzen dürfen, Budgets gegen Kostenexplosionen durch Fan-out und Wiederholungen sowie Observability pro Knoten (Wang, 2026; [[mcp-and-related-protocols|MCP und ähnliche Protokolle]]; [[harness-engineering|Harness Engineering]]). Für die Kommunikation zwischen Agenten verschiedener Frameworks steht das A2A-Protokoll bereit, mit dem Agenten Aufgaben delegieren und Ergebnisse teilen, ohne ihr internes Gedächtnis oder ihre Werkzeuge offenzulegen (A2A protocol docs).

#### 3. Graphen aus Loops

Eine zweite, abstraktere Lesart verbindet viele Feedback-Schleifen wie Metriken, Evaluationen, Audits und Richtlinien zu einem Netz, in dem sie sich gegenseitig überwachen und korrigieren; sie ist bislang die am wenigsten umsetzbare Bedeutung (Ghelbur, 2026). Sie überschneidet sich mit etablierter Qualitätskontrolle: festzulegen, welche Prüfung welche andere übersteuern darf, und feste Bezugspunkte wie zurückgehaltene Testsets beizubehalten ([[quality-control|Qualitätskontrolle]]; [[llm-evaluation|LLM-Evaluation]]).

#### 4. Graphstrukturiertes Wissen

Die dritte Lesart speichert das Wissen eines Agenten als typisierte Knoten und Kanten, etwa supersedes, depends_on, decided_by oder caused, statt als Sammlung von Dokumenten, die nach Ähnlichkeit durchsucht werden; typisierte Kanten tragen Bedeutung, die untypisierte Verweise nicht haben, und eine Traversierung kann Begründungsketten über mehrere Notizen verfolgen (Ghelbur, 2026). Graphen helfen bei Multi-Hop- und korpusweiten Fragen, wie GraphRAG für globale Fragen zeigt (Edge et al., 2024), unterliegen aber bei einfachen Nachschlagefragen und kosten mehr (Ghelbur, 2026). Diese Lesart steht [[knowledge-graph-engineering|Knowledge Graph Engineering]], [[graphrag|GraphRAG]] und [[knowledge-graphs|Wissensgraphen]] am nächsten; sie sollte nicht mit der Topologie-Bedeutung verwechselt werden, denn Wissensgraphen strukturieren, was ein System weiß, Orchestrierungsgraphen dagegen, wer das System ist (Wang, 2026).

#### Ursprung und Varianten

Die früheste gefundene Verwendung war ein Blogbeitrag Anfang Juli 2026; verbreitet hat sich der Begriff, nachdem Peter Steinberger am 18. Juli 2026 schrieb: „Are we still talking loops or did we shift to graphs yet?“, und eine viral geteilte Behauptung über eine große Studie von Stanford und Anthropic erwies sich als erfunden (Ghelbur, 2026). Die zugrunde liegende Praxis ist älter: Dataflow- und DAG-Orchestrierung, Forschung zu Multi-Agenten-Systemen und Agenten-Frameworks, die Graphen zu Objekten erster Klasse machten (Wang, 2026), etwa LangGraph, das deterministische und LLM-gesteuerte Schritte in einem Graphen verbindet (LangGraph docs), und AutoGen, in dem mehrere Agenten im Gespräch Aufgaben lösen (Wu et al., 2023). Neu ist 2026 vor allem das Vokabular und die Einordnung als Stufe nach Loop Engineering.

### Wann einsetzen

- Wenn ein System aus mehreren Agenten oder Loops besteht, deren Zuständigkeiten, Übergänge und Berechtigungen ausdrücklich gestaltet werden müssen.
- Wenn das Gedächtnis eines Agenten typisierte Beziehungen braucht, etwa Entscheidungen, die frühere Entscheidungen ablösen.
- In Diskussionen erst, nachdem geklärt ist, welche der drei Bedeutungen gemeint ist.

### Stärken und Grenzen

**Stärken**
- Macht die Struktur von Multi-Agenten-Systemen ausdrücklich, versionierbar und steuerbar (Wang, 2026).
- Identitäten, Budgets und Traces pro Knoten machen komplexe Läufe nachvollziehbar.
- Typisierte Wissensgraphen beantworten Multi-Hop-Fragen, die Vektorsuche verfehlt (Ghelbur, 2026).

**Einschränkungen**
- Der Begriff wird uneinheitlich verwendet und ist teils von Hype getrieben, einschließlich erfundener Behauptungen (Ghelbur, 2026).
- Multi-Agenten-Graphen bringen neue Fehlerbilder: Der Ausfall eines zwischengeschalteten Agenten wirkt sich kaskadierend auf nachgelagerte Knoten aus, und fehlende Kanten halten Informationen von dort fern, wo sie gebraucht werden.
- Fan-out und Wiederholungen können die Kosten vervielfachen ([[llm-cost-optimization|LLM-Kostenoptimierung]]).
- Von den drei Lesarten hat nur graphstrukturiertes Wissen eine lange Forschungsgeschichte und reproduzierbare Benchmarks; die beiden anderen stützen sich überwiegend auf Praxisberichte (Ghelbur, 2026).

### Vergleich

| Bedeutung | Nächstes etabliertes Thema | Belege |
|----------|----------------|------------|
| Orchestrierungsgraphen | Multi-Agenten-Systeme, LangGraph, AutoGen (Wu et al., 2023) | Frameworks und Praxisberichte |
| Graphen aus Loops | [[quality-control|Qualitätskontrolle]], [[llm-evaluation|LLM-Evaluation]] | Überwiegend konzeptionell (Ghelbur, 2026) |
| Graphstrukturiertes Wissen | GraphRAG, Wissensgraphen (Edge et al., 2024) | Forschung und Benchmarks |

### In der Praxis

Orchestrierungsgraphen werden mit Frameworks wie [[langchain-and-langgraph|LangChain und LangGraph]] gebaut, wobei jeder Knoten getraced und budgetiert wird ([[llm-observability-and-tracing|LLM-Observability und Tracing]]); wiederkehrende Abläufe für Knoten lassen sich als [[agent-skills|Agent Skills]] verpacken. Für Wissen werden typisierte Beziehungen und Gültigkeitsdaten in einem Wissensgraphen modelliert. Der Begriff steht neben den Disziplinen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]], und seine Wirkung auf die tägliche Arbeit ähnelt der von [[vibe-coding|Vibe Coding]]: Mehr Automatisierung verlangt mehr bewusste Prüfung.

### Merksatz

„Graph Engineering“ ist 2026 kein feststehender Fachbegriff, sondern ein Sammelname für drei verschiedene Ideen; der belastbare Kern sind graphbasierte Orchestrierung von Agenten und graphstrukturiertes Wissen, die beide schon vor dem Namen existierten.

### Quellen

- Wang, B. (2026). *Graph Engineering for Multi-Agent Systems: Architecture, Governance, and Observability.* TrueFoundry Blog, 20 July 2026. [truefoundry.com](https://www.truefoundry.com/blog/graph-engineering-enterprise-guide)
- Ghelbur, E. (2026). *What Is Graph Engineering? A Field Guide for Builders.* The AI Operator, 21 July 2026. [theaioperator.io](https://theaioperator.io/p/what-is-graph-engineering-a-field)
- LangChain. *LangGraph overview.* LangChain documentation. [docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/overview)
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* COLM 2024. [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- A2A Project. *Agent2Agent (A2A) Protocol.* a2a-protocol.org. [a2a-protocol.org](https://a2a-protocol.org/latest/)
