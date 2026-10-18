---
title_en: Tool Calling
title_de: Tool Calling
entity_type: Method
aliases:
- Tool calling
- Function calling
- Function Calling
- Tool use
- Tool Use
sources:
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- https://developers.openai.com/api/docs/guides/function-calling
- https://arxiv.org/abs/2302.04761
- https://arxiv.org/abs/2305.15334
- https://arxiv.org/abs/2307.16789
- https://arxiv.org/abs/2210.03629
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Tool calling, also called function calling or tool use, lets a language model call functions that a developer defines or that the provider offers: the application describes each tool with a name, a description and a JSON schema for its arguments, the model decides when a request needs a tool and returns a structured call instead of text, and the application executes it and sends the result back (Anthropic documentation; OpenAI documentation). It is the mechanism behind [[agentic-ai|agents]], which repeat this loop until the task is done (Yao et al., 2022). Research showed that models can learn when and how to call APIs (Schick et al., 2023), that fine-tuning plus retrieval of API documentation reduces hallucinated calls (Patil et al., 2023), and that training on thousands of real APIs generalises to unseen ones (Qin et al., 2023).

### How it works

```text
request: messages + tool definitions (name, description, JSON schema) + tool_choice
 ▼
model decides: answer directly  or  emit tool call(s) {name, arguments}
 ▼
application validates arguments → executes tool (client tool)
        or provider executes it (server tool)
 ▼
tool result sent back, linked to the call id
 ▼
model answers  or  calls further tools  (loop)
```

#### 1. Defining tools

Each tool is described by a name, a description of when and how to use it, and a JSON schema for its input parameters; OpenAI adds a `strict` flag that enforces the schema (OpenAI documentation), and Anthropic offers strict tool use so that calls always match the schema exactly (Anthropic documentation). The definitions are part of the input: they count against the context window and are billed as input tokens, and Anthropic adds a tool-use system prompt of a few hundred tokens per request (OpenAI documentation; Anthropic documentation). OpenAI recommends clear, detailed names and descriptions and keeping the number of initially available functions small, aiming for fewer than 20 at the start of a turn (OpenAI documentation). Writing tool descriptions is therefore a form of [[prompt-engineering|prompt engineering]] and [[context-engineering|context engineering]].

#### 2. Deciding whether to call

With the default `tool_choice` of `auto`, the model decides on each turn whether to call a tool or answer directly; Claude calls a tool when the request maps to a tool's described capability and the answer is not already in context (Anthropic documentation). Developers can force a call (`any` or `required`), force one specific tool, restrict calls to a subset of tools or disable them with `none` (Anthropic documentation; OpenAI documentation). If required parameters are missing from the request, a model may ask for them or infer a value, which Anthropic notes is not guaranteed for less capable models or ambiguous prompts (Anthropic documentation).

#### 3. The tool call

Instead of text, the model returns a structured call: in the Anthropic API a `tool_use` block with an id, the tool name and the arguments, with `stop_reason` set to `tool_use`; in the OpenAI API a tool call in the response (Anthropic documentation; OpenAI documentation). Models may call several tools in one turn (parallel tool calls), which can be switched off so that at most one tool is called (Anthropic documentation; OpenAI documentation).

#### 4. Executing the tool

Client tools run in the developer's application, which executes the operation and returns the output; server tools such as web search or code execution run on the provider's infrastructure, and their results come back without handling by the application (Anthropic documentation). Because the arguments come from a model, the application validates them and decides what the tool may do; limiting tools and requiring approval for side effects are [[llm-guardrails|guardrails]] in their own right, and tools are often thin wrappers around existing [[apis|APIs]].

#### 5. Returning the result and looping

The application sends the output back in a second request, in Anthropic's API as a `tool_result` block that refers to the call's id, and the model then answers or calls further tools (Anthropic documentation; OpenAI documentation). Repeating this loop, with the model reasoning between calls, is the ReAct pattern: interleaving reasoning traces with actions let a model on HotpotQA and FEVER query a Wikipedia API and reduce hallucination and error propagation compared with chain-of-thought alone (Yao et al., 2022). Agent frameworks and SDKs automate the loop ([[agent-frameworks|agent frameworks]]).

#### 6. Teaching models to use tools

Toolformer showed that a model can teach itself, in a self-supervised way and from only a handful of demonstrations per API, which APIs to call, when, with which arguments and how to use the results, with tools including a calculator, a question-answering system, two search engines, a translation system and a calendar (Schick et al., 2023). Gorilla, a fine-tuned LLaMA-based model, surpassed GPT-4 on writing API calls for the HuggingFace, TorchHub and TensorHub APIs of the APIBench dataset, and combined with a document retriever it adapted to changes in API documentation at test time and hallucinated fewer wrong API usages (Patil et al., 2023). ToolLLM built ToolBench from 16,464 real-world REST APIs in 49 categories, with instructions and solution paths generated by [[chatgpt|ChatGPT]], fine-tuned [[llama|LLaMA]] into ToolLLaMA with a neural API retriever, and reported performance comparable to ChatGPT and zero-shot generalisation to unseen APIs (Qin et al., 2023).

#### Origin and variants

Early research taught models to emit API calls inside generated text (Schick et al., 2023) or interleaved actions with reasoning in prompts (Yao et al., 2022); providers then added native tool definitions and structured tool calls to their APIs (OpenAI documentation; Anthropic documentation). Protocols such as MCP standardise how tools are offered to many clients ([[mcp-and-related-protocols|MCP and related protocols]]), and [[agent-skills|agent skills]] package instructions on how to use tools for a particular workflow.

### When to use it

- When answers need current or private data that is not in the model, such as databases, search or internal systems (Anthropic documentation).
- When the model has to act, for example create a ticket or run code, rather than only write text ([[agentic-ai|agentic AI]]).
- When structured output with a fixed schema is needed, since tool arguments follow a JSON schema (OpenAI documentation).
- For tasks such as arithmetic or factual lookup where small specialised tools beat the model (Schick et al., 2023).

### Strengths and limitations

**Strengths**
- Gives the model access to fresh data and actions while the application keeps control over execution (Anthropic documentation).
- Structured, schema-checked calls are easier to validate and log than free text (OpenAI documentation).
- Interleaving tool calls with reasoning reduces hallucination on knowledge-intensive tasks (Yao et al., 2022).

**Limitations**
- Models can choose the wrong tool, call a tool unnecessarily or fill in missing arguments with guesses (Anthropic documentation).
- Accuracy drops when many tools are offered at once, and every definition costs input tokens (OpenAI documentation).
- Models can hallucinate API usage without access to current documentation (Patil et al., 2023).
- Tool outputs are untrusted input: content returned by a tool can carry [[prompt-injection|prompt injection]].

### Comparison

| Approach | What the model does | Who executes | Example |
|---|---|---|---|
| Tool calling | returns a structured call | application or provider | `tool_use` / tool calls |
| [[retrieval-augmented-generation\|RAG]] | reads retrieved context | retrieval pipeline before the call | vector search |
| [[mcp-and-related-protocols\|MCP]] | calls tools offered by a server | MCP server | protocol for tool discovery |
| [[agent-skills\|Agent skills]] | loads instructions for using tools | harness | skill files |
| Self-taught tool use | emits API calls in text | wrapper around the model | Toolformer |

Sources: Anthropic documentation; OpenAI documentation; Schick et al. (2023).

### In practice

Every tool call and result is traced so that wrong tool choices and failed calls can be analysed ([[llm-observability-and-tracing|LLM observability and tracing]]); agents are evaluated on tool selection and task success, not only on the final answer ([[llm-evaluation|LLM evaluation]]). Tool definitions should be few and well described, with the most powerful tools behind approval steps ([[harness-engineering|harness engineering]]). The cost of definitions and repeated calls belongs in [[llm-cost-optimisation|LLM cost optimisation]].

### Key takeaway

Tool calling turns a model's decision to act into a structured, schema-bound call that the application executes, which makes agents possible and keeps execution under the application's control.

### Sources

- Anthropic (2026). *Tool use with Claude.* Claude Developer Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- OpenAI (2026). *Function calling.* OpenAI API documentation. [developers.openai.com](https://developers.openai.com/api/docs/guides/function-calling)
- Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N. & Scialom, T. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* arXiv:2302.04761. [arXiv](https://arxiv.org/abs/2302.04761)
- Patil, S. G., Zhang, T., Wang, X. & Gonzalez, J. E. (2023). *Gorilla: Large Language Model Connected with Massive APIs.* arXiv:2305.15334. [arXiv](https://arxiv.org/abs/2305.15334)
- Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y. et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.* arXiv:2307.16789. [arXiv](https://arxiv.org/abs/2307.16789)
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Tool Calling, auch Function Calling oder Tool Use genannt, erlaubt einem Sprachmodell, Funktionen aufzurufen, die Entwicklerinnen und Entwickler definieren oder der Anbieter bereitstellt: Die Anwendung beschreibt jedes Tool mit Namen, Beschreibung und einem JSON-Schema für die Argumente, das Modell entscheidet, wann eine Anfrage ein Tool braucht, und gibt statt Text einen strukturierten Aufruf zurück, den die Anwendung ausführt und dessen Ergebnis sie zurückschickt (Anthropic-Dokumentation; OpenAI-Dokumentation). Es ist der Mechanismus hinter [[agentic-ai|Agenten]], die diese Schleife wiederholen, bis die Aufgabe erledigt ist (Yao et al., 2022). Die Forschung zeigte, dass Modelle lernen können, wann und wie sie APIs aufrufen (Schick et al., 2023), dass Fine-Tuning zusammen mit Retrieval der API-Dokumentation erfundene Aufrufe verringert (Patil et al., 2023) und dass Training auf Tausenden realer APIs auf unbekannte APIs übertragbar ist (Qin et al., 2023).

### Funktionsweise

```text
Anfrage: Nachrichten + Tool-Definitionen (Name, Beschreibung, JSON-Schema) + tool_choice
 ▼
Modell entscheidet: direkt antworten  oder  Tool-Aufruf(e) ausgeben {Name, Argumente}
 ▼
Anwendung prüft Argumente → führt Tool aus (Client-Tool)
        oder Anbieter führt es aus (Server-Tool)
 ▼
Tool-Ergebnis zurück, verknüpft mit der Aufruf-ID
 ▼
Modell antwortet  oder  ruft weitere Tools auf  (Schleife)
```

#### 1. Tools definieren

Jedes Tool wird durch einen Namen, eine Beschreibung, wann und wie es zu nutzen ist, und ein JSON-Schema für seine Eingabeparameter beschrieben; [[openai|OpenAI]] ergänzt ein `strict`-Flag, das das Schema durchsetzt (OpenAI-Dokumentation), und [[anthropic|Anthropic]] bietet Strict Tool Use, damit Aufrufe immer genau dem Schema entsprechen (Anthropic-Dokumentation). Die Definitionen gehören zur Eingabe: Sie zählen gegen das Kontextfenster und werden als Input-Tokens berechnet, und Anthropic fügt je Anfrage einen Tool-Use-System-Prompt von einigen hundert Tokens hinzu (OpenAI-Dokumentation; Anthropic-Dokumentation). OpenAI empfiehlt klare, ausführliche Namen und Beschreibungen und wenige anfangs verfügbare Funktionen, möglichst weniger als 20 zu Beginn eines Turns (OpenAI-Dokumentation). Tool-Beschreibungen zu schreiben ist daher eine Form von [[prompt-engineering|Prompt Engineering]] und [[context-engineering|Context Engineering]].

#### 2. Entscheiden, ob ein Aufruf nötig ist

Mit der Voreinstellung `tool_choice` = `auto` entscheidet das Modell in jedem Turn, ob es ein Tool aufruft oder direkt antwortet; Claude ruft ein Tool auf, wenn die Anfrage zur beschriebenen Fähigkeit eines Tools passt und die Antwort noch nicht im Kontext steht (Anthropic-Dokumentation). Entwicklerinnen und Entwickler können einen Aufruf erzwingen (`any` bzw. `required`), ein bestimmtes Tool erzwingen, Aufrufe auf eine Teilmenge von Tools beschränken oder sie mit `none` abschalten (Anthropic-Dokumentation; OpenAI-Dokumentation). Fehlen in der Anfrage Pflichtparameter, kann ein Modell nachfragen oder einen Wert ableiten; laut Anthropic ist das bei weniger leistungsfähigen Modellen und mehrdeutigen Prompts nicht garantiert (Anthropic-Dokumentation).

#### 3. Der Tool-Aufruf

Statt Text gibt das Modell einen strukturierten Aufruf zurück: in der Anthropic-API einen `tool_use`-Block mit ID, Tool-Namen und Argumenten, wobei `stop_reason` auf `tool_use` steht, in der OpenAI-API einen Tool-Call in der Antwort (Anthropic-Dokumentation; OpenAI-Dokumentation). Modelle können in einem Turn mehrere Tools aufrufen (parallele Tool-Aufrufe); das lässt sich abschalten, sodass höchstens ein Tool aufgerufen wird (Anthropic-Dokumentation; OpenAI-Dokumentation).

#### 4. Das Tool ausführen

Client-Tools laufen in der Anwendung, die die Operation ausführt und die Ausgabe zurückgibt; Server-Tools wie Websuche oder Codeausführung laufen auf der Infrastruktur des Anbieters, und ihre Ergebnisse kommen zurück, ohne dass die Anwendung sie bearbeiten muss (Anthropic-Dokumentation). Weil die Argumente von einem Modell stammen, prüft die Anwendung sie und legt fest, was das Tool darf; Tools zu begrenzen und für Nebenwirkungen eine Freigabe zu verlangen sind eigene [[llm-guardrails|Guardrails]], und Tools sind oft dünne Hüllen um bestehende [[apis|APIs]].

#### 5. Ergebnis zurückgeben und Schleife

Die Anwendung schickt die Ausgabe in einer zweiten Anfrage zurück, in der Anthropic-API als `tool_result`-Block mit Bezug auf die ID des Aufrufs, und das Modell antwortet dann oder ruft weitere Tools auf (Anthropic-Dokumentation; OpenAI-Dokumentation). Wiederholt man diese Schleife und lässt das Modell zwischen den Aufrufen schlussfolgern, entsteht das ReAct-Muster: Mit abwechselnden Gedankengängen und Aktionen fragte ein Modell auf HotpotQA und FEVER eine Wikipedia-API ab und verringerte Halluzinationen und Fehlerfortpflanzung gegenüber reinem Chain-of-Thought (Yao et al., 2022). Agent-Frameworks und SDKs automatisieren die Schleife ([[agent-frameworks|Agent-Frameworks]]).

#### 6. Modellen die Tool-Nutzung beibringen

Toolformer zeigte, dass ein Modell sich selbstüberwacht und mit nur wenigen Beispielen je API beibringen kann, welche APIs es wann mit welchen Argumenten aufruft und wie es die Ergebnisse nutzt, mit Werkzeugen wie Taschenrechner, Frage-Antwort-System, zwei Suchmaschinen, Übersetzungssystem und Kalender (Schick et al., 2023). Gorilla, ein feinabgestimmtes Modell auf LLaMA-Basis, übertraf GPT-4 beim Schreiben von API-Aufrufen für die HuggingFace-, TorchHub- und TensorHub-APIs des Datensatzes APIBench, passte sich zusammen mit einem Dokument-Retriever zur Testzeit an geänderte API-Dokumentation an und erfand seltener falsche API-Nutzungen (Patil et al., 2023). ToolLLM baute ToolBench aus 16.464 realen REST-APIs in 49 Kategorien, mit von [[chatgpt|ChatGPT]] erzeugten Anweisungen und Lösungswegen, stimmte [[llama|LLaMA]] darauf zu ToolLLaMA mit einem neuronalen API-Retriever ab und berichtete eine mit ChatGPT vergleichbare Leistung sowie Zero-Shot-Übertragung auf unbekannte APIs (Qin et al., 2023).

#### Herkunft und Varianten

Frühe Forschung brachte Modellen bei, API-Aufrufe in den erzeugten Text einzubetten (Schick et al., 2023), oder verschränkte Aktionen und Schlussfolgern im Prompt (Yao et al., 2022); danach ergänzten Anbieter ihre APIs um native Tool-Definitionen und strukturierte Tool-Aufrufe (OpenAI-Dokumentation; Anthropic-Dokumentation). Protokolle wie MCP vereinheitlichen, wie Tools vielen Clients angeboten werden ([[mcp-and-related-protocols|MCP und verwandte Protokolle]]), und [[agent-skills|Agent Skills]] bündeln Anweisungen, wie Tools in einem bestimmten Ablauf genutzt werden.

### Wann einsetzen

- Wenn Antworten aktuelle oder private Daten brauchen, die nicht im Modell stecken, etwa Datenbanken, Suche oder interne Systeme (Anthropic-Dokumentation).
- Wenn das Modell handeln soll, etwa ein Ticket anlegen oder Code ausführen, statt nur Text zu schreiben ([[agentic-ai|Agentic AI]]).
- Wenn strukturierte Ausgaben mit festem Schema gebraucht werden, da Tool-Argumente einem JSON-Schema folgen (OpenAI-Dokumentation).
- Für Aufgaben wie Rechnen oder Faktennachschlagen, bei denen kleine spezialisierte Werkzeuge das Modell übertreffen (Schick et al., 2023).

### Stärken und Grenzen

**Stärken**
- Gibt dem Modell Zugang zu aktuellen Daten und Aktionen, während die Anwendung die Kontrolle über die Ausführung behält (Anthropic-Dokumentation).
- Strukturierte, gegen ein Schema geprüfte Aufrufe lassen sich leichter validieren und protokollieren als freier Text (OpenAI-Dokumentation).
- Tool-Aufrufe im Wechsel mit Schlussfolgern verringern Halluzinationen bei wissensintensiven Aufgaben (Yao et al., 2022).

**Grenzen**
- Modelle können das falsche Tool wählen, ein Tool unnötig aufrufen oder fehlende Argumente raten (Anthropic-Dokumentation).
- Die Genauigkeit sinkt, wenn viele Tools gleichzeitig angeboten werden, und jede Definition kostet Input-Tokens (OpenAI-Dokumentation).
- Ohne Zugang zur aktuellen Dokumentation können Modelle API-Nutzungen erfinden (Patil et al., 2023).
- Tool-Ausgaben sind nicht vertrauenswürdige Eingaben: Was ein Tool zurückgibt, kann [[prompt-injection|Prompt Injection]] enthalten.

### Vergleich

| Ansatz | Was das Modell tut | Wer ausführt | Beispiel |
|---|---|---|---|
| Tool Calling | gibt einen strukturierten Aufruf zurück | Anwendung oder Anbieter | `tool_use` / Tool Calls |
| [[retrieval-augmented-generation\|RAG]] | liest abgerufenen Kontext | Retrieval-Pipeline vor dem Aufruf | Vektorsuche |
| [[mcp-and-related-protocols\|MCP]] | ruft Tools auf, die ein Server anbietet | MCP-Server | Protokoll zum Auffinden von Tools |
| [[agent-skills\|Agent Skills]] | lädt Anweisungen zur Tool-Nutzung | Harness | Skill-Dateien |
| Selbst erlernte Tool-Nutzung | gibt API-Aufrufe im Text aus | Hülle um das Modell | Toolformer |

Quellen: Anthropic-Dokumentation; OpenAI-Dokumentation; Schick et al. (2023).

### In der Praxis

Jeder Tool-Aufruf und jedes Ergebnis wird nachverfolgt, damit falsche Tool-Wahl und fehlgeschlagene Aufrufe analysiert werden können ([[llm-observability-and-tracing|LLM-Observability und Tracing]]); Agenten werden an Tool-Auswahl und Aufgabenerfolg gemessen, nicht nur an der Endantwort ([[llm-evaluation|LLM-Evaluation]]). Tool-Definitionen sollten wenige und gut beschrieben sein, die mächtigsten Tools hinter Freigabeschritten liegen ([[harness-engineering|Harness Engineering]]). Die Kosten der Definitionen und wiederholten Aufrufe gehören in die [[llm-cost-optimisation|LLM-Kostenoptimierung]].

### Merksatz

Tool Calling macht aus der Entscheidung eines Modells zu handeln einen strukturierten, an ein Schema gebundenen Aufruf, den die Anwendung ausführt; das ermöglicht Agenten und lässt die Ausführung unter der Kontrolle der Anwendung.

### Quellen

- Anthropic (2026). *Tool use with Claude.* Claude Developer Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- OpenAI (2026). *Function calling.* OpenAI API documentation. [developers.openai.com](https://developers.openai.com/api/docs/guides/function-calling)
- Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N. & Scialom, T. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* arXiv:2302.04761. [arXiv](https://arxiv.org/abs/2302.04761)
- Patil, S. G., Zhang, T., Wang, X. & Gonzalez, J. E. (2023). *Gorilla: Large Language Model Connected with Massive APIs.* arXiv:2305.15334. [arXiv](https://arxiv.org/abs/2305.15334)
- Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y. et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.* arXiv:2307.16789. [arXiv](https://arxiv.org/abs/2307.16789)
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)
