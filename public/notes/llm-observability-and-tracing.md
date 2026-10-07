---
title_en: LLM Observability and Tracing
title_de: LLM-Observability und Tracing
entity_type: Method
sources:
- https://opentelemetry.io/docs/concepts/signals/traces/
- https://opentelemetry.io/docs/concepts/sampling/
- https://langfuse.com/docs/observability/overview
- https://www.anthropic.com/engineering/building-effective-agents
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LLM observability extends classical application monitoring to the particularities of LLM and agent systems: non-deterministic behaviour, multi-step call chains and costs that depend on tokens. Its core is application tracing, structured logs of every request with the exact prompt, the model's response, token usage, latency and all tool or retrieval steps in between (Langfuse docs). A classical log entry shows that an error occurred; an LLM trace also shows which prompt, which context and which intermediate steps led to the result. Without that, non-deterministic behaviour can hardly be debugged, and production traces also feed evaluations (Langfuse docs).

### How it works

#### 1. Traces and spans

```text
trace (one complete user request)
  ├── span: retrieval          (120 ms, 340 tokens)
  ├── span: LLM call 1         (800 ms, 1,200 tokens, large model)
  ├── span: tool call          (450 ms)
  └── span: LLM call 2         (600 ms, 900 tokens, small model)
```

A trace shows the full path a request takes through an application; a span is a unit of work and the building block of traces, with a name, a parent span ID, start and end times, a context with trace and span IDs, attributes, events, links and a status (OpenTelemetry traces docs). Nested spans reconstruct the call hierarchy of an agent run, even when steps run in parallel.

```json
{"trace_id": "a1b2c3", "span_id": "s2", "parent_span_id": "s1",
 "name": "llm_call", "model": "large-model-v2",
 "input_tokens": 1842, "output_tokens": 267, "latency_ms": 812,
 "cost_usd": 0.0091, "prompt": "...", "response": "..."}
```

#### 2. What is recorded beyond classical monitoring

```text
prompt (complete, including system prompt and context)
model response (complete)
token usage (input and output separately)
cost per call and per trace
model used (relevant with model routing)
tool calls with parameters and results
intermediate steps of multi-step agents
```

#### 3. Tools and standards

- **Specialised LLM tracing tools** such as Langfuse or LangSmith are tailored to prompts, tokens and costs; Langfuse is open source, can be self-hosted, sends tracing data asynchronously so that response times are not affected, and adds evaluation, prompt management and datasets (Langfuse docs).
- **Generic tracing with OpenTelemetry**, an open standard for distributed tracing, integrates LLM traces into the observability infrastructure that already exists for the rest of a system (OpenTelemetry traces docs).

#### 4. Sampling at high volume

```text
head sampling → decided at the start, e.g. a fixed percentage of traces based on the trace ID
tail sampling → decided after the trace, e.g. always keep traces with errors or high latency
```

Head sampling is easy but cannot ensure that all traces with errors are kept; tail sampling can, but it is difficult to implement and operate, needs stateful components that store large amounts of data and is often vendor-specific; both can be combined (OpenTelemetry sampling docs).

#### 5. Cost attribution

```text
trace total:              0.047 EUR
  ├── retrieval embedding: 0.0003 EUR  (0.6%)
  ├── LLM call 1 (plan):   0.0091 EUR  (19%)
  ├── tool calls:          0.0000 EUR  (0%)
  └── LLM call 2 (answer): 0.0376 EUR  (80%)   ← main cost driver
```

Breaking costs down per span shows which part of a request causes the costs and makes targeted [[llm-cost-optimization|LLM Cost Optimization]] possible.

#### Origin and variants

Distributed tracing makes the full path of a request visible, whether the application is a monolith with one database or a mesh of many services (OpenTelemetry traces docs). LLM applications added prompts, tokens, costs and tool calls as data to record, and agentic systems made traces of multi-step runs necessary; frameworks that hide prompts and responses behind abstraction layers make debugging harder, which tracing counteracts (Anthropic, 2024a).

### When to use it

- From the first production use of an LLM application onwards.
- Whenever agents, tool calls or several model calls are chained.
- When costs, latency or quality must be monitored and explained.

### Strengths and limitations

**Strengths**
- Makes non-deterministic, multi-step behaviour traceable (Langfuse docs).
- Supplies real production data for evaluation and new test cases (Langfuse docs).
- Cost attribution per trace finds the actual cost drivers.

**Limitations**
- Non-determinism: a single trace does not prove that a behaviour is reproducible.
- Data protection: prompts and responses can contain personal or confidential data, so logging needs the same care as any other processing, including masking of sensitive fields ([[gdpr|General Data Protection Regulation (GDPR)]]).
- Data volume: complete prompts and responses are much larger than classical log lines, which makes retention periods and sampling relevant (OpenTelemetry sampling docs).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Classical logging | Records events, not prompts, contexts or tokens | Infrastructure errors |
| Classical monitoring | Aggregated metrics such as latency and error rates ([[mlops-and-deployment|MLOps and Deployment]]) | Service health |
| Specialised LLM tracing | Prompts, responses, tokens, costs and tool calls per span (Langfuse docs) | Debugging and evaluating LLM applications |
| OpenTelemetry | Open standard, integrates with existing infrastructure (OpenTelemetry traces docs) | Systems with existing observability stack |

### In practice

Traces are used for continuous evaluation: samples of real requests are rated afterwards with [[llm-as-a-judge|LLM-as-a-Judge]], recurring error patterns across many traces reveal systematic problems ([[rag-failure-modes|RAG: Failure Modes]]), and each observed failure becomes a new [[regression-testing|Regression Testing]] case. A misconfigured agent caught in a retry loop can cause considerable costs in a short time; without cost attribution per trace, this often shows only in the monthly bill, so alerts on cost thresholds per trace or time window close this gap ([[agentic-ai|Agentic AI]]). In multi-agent systems, traces are kept per node with propagated identifiers ([[graph-engineering|Graph Engineering]]), and traces of tool calls, skills and MCP servers are part of the harness ([[harness-engineering|Harness Engineering]]; [[agent-skills|Agent Skills]]; [[mcp-and-related-protocols|MCP and Related Protocols]]), of agent loops ([[loop-engineering|Loop Engineering]]) and of AI-assisted coding ([[vibe-coding|Vibe Coding]]). Observability is one of the cross-cutting topics in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]].

### Key takeaway

A trace records which prompt, context and intermediate steps produced a result and what they cost; it is the basis for debugging, evaluation and cost control of LLM systems, and it must be handled like any other personal data.

### Sources

- OpenTelemetry. *Traces.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/signals/traces/)
- OpenTelemetry. *Sampling.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/sampling/)
- Langfuse. *Observability & Application Tracing.* Langfuse documentation. [langfuse.com](https://langfuse.com/docs/observability/overview)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LLM-Observability erweitert klassisches Anwendungsmonitoring um die Besonderheiten von LLM- und Agentensystemen: nicht deterministisches Verhalten, mehrstufige Aufrufketten und Kosten, die von Token abhängen. Ihr Kern ist Application Tracing, strukturierte Logs jeder Anfrage mit dem genauen Prompt, der Modellantwort, dem Token-Verbrauch, der Latenz und allen Werkzeug- oder Retrieval-Schritten dazwischen (Langfuse docs). Ein klassischer Logeintrag zeigt, dass ein Fehler aufgetreten ist; ein LLM-Trace zeigt zusätzlich, welcher Prompt, welcher Kontext und welche Zwischenschritte zum Ergebnis geführt haben. Ohne das lässt sich nicht deterministisches Verhalten kaum debuggen, und Traces aus dem Betrieb dienen zugleich als Grundlage für Evaluationen (Langfuse docs).

### Funktionsweise

#### 1. Traces und Spans

```text
Trace (eine vollständige Nutzeranfrage)
  ├── Span: Retrieval          (120 ms, 340 Token)
  ├── Span: LLM-Aufruf 1       (800 ms, 1.200 Token, großes Modell)
  ├── Span: Werkzeugaufruf     (450 ms)
  └── Span: LLM-Aufruf 2       (600 ms, 900 Token, kleines Modell)
```

Ein Trace zeigt den gesamten Weg einer Anfrage durch eine Anwendung; ein Span ist eine Arbeitseinheit und der Baustein von Traces, mit Name, Kennung des übergeordneten Spans, Start- und Endzeit, einem Kontext mit Trace- und Span-Kennung, Attributen, Ereignissen, Verknüpfungen und einem Status (OpenTelemetry traces docs). Verschachtelte Spans rekonstruieren die Aufrufhierarchie eines Agentenlaufs, auch wenn Schritte parallel laufen.

```json
{"trace_id": "a1b2c3", "span_id": "s2", "parent_span_id": "s1",
 "name": "llm_call", "model": "large-model-v2",
 "input_tokens": 1842, "output_tokens": 267, "latency_ms": 812,
 "cost_usd": 0.0091, "prompt": "...", "response": "..."}
```

#### 2. Was über klassisches Monitoring hinaus erfasst wird

```text
Prompt (vollständig, einschließlich Systemprompt und Kontext)
Modellantwort (vollständig)
Token-Verbrauch (Input und Output getrennt)
Kosten pro Aufruf und pro Trace
verwendetes Modell (wichtig bei Model Routing)
Werkzeugaufrufe mit Parametern und Ergebnissen
Zwischenschritte mehrstufiger Agenten
```

#### 3. Werkzeuge und Standards

- **Spezialisierte LLM-Tracing-Werkzeuge** wie Langfuse oder LangSmith sind auf Prompts, Token und Kosten zugeschnitten; Langfuse ist Open Source, lässt sich selbst betreiben, sendet Tracing-Daten asynchron, sodass Antwortzeiten nicht leiden, und ergänzt Evaluation, Prompt-Verwaltung und Datensätze (Langfuse docs).
- **Generisches Tracing mit OpenTelemetry**, einem offenen Standard für verteiltes Tracing, bindet LLM-Traces in die Observability-Infrastruktur ein, die für den Rest eines Systems ohnehin besteht (OpenTelemetry traces docs).

#### 4. Sampling bei hohem Volumen

```text
Head Sampling → Entscheidung zu Beginn, z. B. fester Prozentsatz der Traces anhand der Trace-Kennung
Tail Sampling → Entscheidung nach dem Trace, z. B. Traces mit Fehlern oder hoher Latenz immer behalten
```

Head Sampling ist einfach, kann aber nicht sicherstellen, dass alle Traces mit Fehlern erhalten bleiben; Tail Sampling kann das, ist aber schwierig umzusetzen und zu betreiben, braucht zustandsbehaftete Komponenten, die große Datenmengen speichern, und ist oft anbieterspezifisch; beide lassen sich kombinieren (OpenTelemetry sampling docs).

#### 5. Kostenzuordnung

```text
Trace gesamt:             0,047 EUR
  ├── Retrieval-Embedding: 0,0003 EUR  (0,6 %)
  ├── LLM-Aufruf 1 (Plan): 0,0091 EUR  (19 %)
  ├── Werkzeugaufrufe:     0,0000 EUR  (0 %)
  └── LLM-Aufruf 2 (Antwort): 0,0376 EUR  (80 %)   ← größter Kostentreiber
```

Die Aufschlüsselung der Kosten pro Span zeigt, welcher Teil einer Anfrage die Kosten verursacht, und macht gezielte [[llm-cost-optimization|LLM-Kostenoptimierung]] möglich.

#### Ursprung und Varianten

Verteiltes Tracing macht den gesamten Weg einer Anfrage sichtbar, ob die Anwendung ein Monolith mit einer Datenbank oder ein Geflecht vieler Dienste ist (OpenTelemetry traces docs). LLM-Anwendungen fügten Prompts, Token, Kosten und Werkzeugaufrufe als zu erfassende Daten hinzu, und agentische Systeme machten Traces mehrstufiger Läufe nötig; Frameworks, die Prompts und Antworten hinter Abstraktionsschichten verbergen, erschweren das Debugging, was Tracing ausgleicht (Anthropic, 2024a).

### Wann einsetzen

- Ab dem ersten produktiven Einsatz einer LLM-Anwendung.
- Immer, wenn Agenten, Werkzeugaufrufe oder mehrere Modellaufrufe verkettet sind.
- Wenn Kosten, Latenz oder Qualität überwacht und erklärt werden müssen.

### Stärken und Grenzen

**Stärken**
- Macht nicht deterministisches, mehrstufiges Verhalten nachvollziehbar (Langfuse docs).
- Liefert reale Betriebsdaten für Evaluation und neue Testfälle (Langfuse docs).
- Die Kostenzuordnung pro Trace findet die tatsächlichen Kostentreiber.

**Einschränkungen**
- Nicht-Determinismus: Ein einzelner Trace beweist nicht, dass ein Verhalten reproduzierbar ist.
- Datenschutz: Prompts und Antworten können personenbezogene oder vertrauliche Daten enthalten; Logging braucht daher dieselbe Sorgfalt wie jede andere Verarbeitung, einschließlich der Maskierung sensibler Felder ([[gdpr|Datenschutz-Grundverordnung (DSGVO)]]).
- Datenvolumen: Vollständige Prompts und Antworten sind deutlich größer als klassische Logzeilen, sodass Aufbewahrungsfristen und Sampling wichtig werden (OpenTelemetry sampling docs).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Klassisches Logging | Erfasst Ereignisse, keine Prompts, Kontexte oder Token | Infrastrukturfehler |
| Klassisches Monitoring | Aggregierte Metriken wie Latenz und Fehlerraten ([[mlops-and-deployment|MLOps und Deployment]]) | Zustand von Diensten |
| Spezialisiertes LLM-Tracing | Prompts, Antworten, Token, Kosten und Werkzeugaufrufe pro Span (Langfuse docs) | Debugging und Evaluation von LLM-Anwendungen |
| OpenTelemetry | Offener Standard, fügt sich in bestehende Infrastruktur ein (OpenTelemetry traces docs) | Systeme mit bestehendem Observability-Stack |

### In der Praxis

Traces dienen der laufenden Evaluation: Stichproben realer Anfragen werden nachträglich mit [[llm-as-a-judge|LLM-as-a-Judge]] bewertet, wiederkehrende Fehlermuster über viele Traces zeigen systematische Probleme ([[rag-failure-modes|RAG: Typische Fehlerarten]]), und jeder beobachtete Fehler wird ein neuer Fall für [[regression-testing|Regressionstests]]. Ein falsch konfigurierter Agent, der in einer Wiederholungsschleife festhängt, kann in kurzer Zeit erhebliche Kosten verursachen; ohne Kostenzuordnung pro Trace fällt das oft erst mit der Monatsrechnung auf, weshalb Alarme bei Kostenschwellen pro Trace oder Zeitfenster diese Lücke schließen ([[agentic-ai|Agentic AI]]). In Multi-Agenten-Systemen werden Traces pro Knoten mit weitergereichten Kennungen geführt ([[graph-engineering|Graph Engineering]]), und Traces von Werkzeugaufrufen, Skills und MCP-Servern gehören zum Harness ([[harness-engineering|Harness Engineering]]; [[agent-skills|Agent Skills]]; [[mcp-and-related-protocols|MCP und ähnliche Protokolle]]), zu Agentenschleifen ([[loop-engineering|Loop Engineering]]) und zum KI-gestützten Programmieren ([[vibe-coding|Vibe Coding]]). Observability ist eines der Querschnittsthemen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]].

### Merksatz

Ein Trace hält fest, welcher Prompt, welcher Kontext und welche Zwischenschritte ein Ergebnis erzeugt haben und was sie gekostet haben; er ist die Grundlage für Debugging, Evaluation und Kostenkontrolle von LLM-Systemen und muss wie andere personenbezogene Daten behandelt werden.

### Quellen

- OpenTelemetry. *Traces.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/signals/traces/)
- OpenTelemetry. *Sampling.* OpenTelemetry documentation. [opentelemetry.io](https://opentelemetry.io/docs/concepts/sampling/)
- Langfuse. *Observability & Application Tracing.* Langfuse documentation. [langfuse.com](https://langfuse.com/docs/observability/overview)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
