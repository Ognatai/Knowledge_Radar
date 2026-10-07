---
title_en: LLM Cost Optimization
title_de: LLM-Kostenoptimierung
entity_type: Method
sources:
- https://arxiv.org/abs/2305.05176
- https://arxiv.org/abs/2406.18665
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://arxiv.org/abs/2310.05736
- https://www.anthropic.com/engineering/building-effective-agents
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LLM cost optimisation reduces the cost and latency of running LLM-based systems without unnecessarily lowering answer quality. Prices of LLM APIs differ by up to two orders of magnitude (Chen et al., 2023), and at high request volumes the choice of model per request quickly becomes the largest variable cost. The main levers are caching, routing requests to smaller models, batching, shorter contexts and outputs, and smaller or compressed models; FrugalGPT, for example, matched the best single model with up to 98% lower cost (Chen et al., 2023). The cheapest request is the one that never needed to be made.

### How it works

#### 1. Where costs arise

```text
cost per request ≈ input tokens × input price + output tokens × output price
```

Output tokens usually cost several times as much as input tokens, for example 2 versus 10 US dollars per million tokens (Prompt caching docs), so long answers, long contexts and the number of calls are separate levers.

```text
request: 2,000 input tokens + 300 output tokens
large model:  input 3 / output 15  (USD per 1M tokens) → (2,000 × 3 + 300 × 15) / 1,000,000 = 0.0105 USD
small model:  input 0.25 / output 1.25                 → (2,000 × 0.25 + 300 × 1.25) / 1,000,000 ≈ 0.0009 USD
```

The prices in this example are illustrative; at 100,000 requests per day the difference adds up to about 1,050 versus 88 US dollars daily.

#### 2. Caching

- **Exact-match caching:** identical requests are answered from a cache without a model call.
- **Prompt caching:** the provider caches a prompt prefix up to a breakpoint and reuses it in later requests with the same prefix, which reduces processing time and cost; it suits long system prompts, many examples, large background context and multi-turn conversations. Cache writes cost more than normal input tokens, cache hits only a fraction of the input price, and the cache lives for a few minutes by default (Prompt caching docs).
- **Semantic caching:** similar, not only identical, requests are answered from the cache using embeddings ([[embeddings|Embeddings]]); this saves more calls but risks missing nuances between similar requests.

The cache hit rate is the key metric: with a 40% hit rate and 0.01 US dollars per uncached request, average costs fall to about 0.006 US dollars.

#### 3. Model routing and cascades

Not every request needs the most capable model. A router, often a small model or a classifier ([[classification|Classification]]), estimates the difficulty and selects the target model; easy and common questions can go to smaller, cheaper models and hard ones to more capable models (Anthropic, 2024a). RouteLLM trains routers on human preference data that choose between a strong and a weak model and reduced costs by more than half in some cases without lowering response quality (Ong et al., 2024). FrugalGPT combines prompt adaptation, LLM approximation and LLM cascades, which learn which combination of models to use for which queries (Chen et al., 2023). The same advisor–worker idea appears in multi-agent systems ([[graph-engineering|Graph Engineering]]).

#### 4. Batching

Requests that do not need an immediate answer can be submitted together for asynchronous processing; batch APIs reduce costs by 50%, with most batches finishing within an hour and a maximum of 24 hours (Batch processing docs). This suits bulk processing and large evaluations, for example with [[llm-as-a-judge|LLM-as-a-Judge]].

#### 5. Limiting context and output

- **Reranking** before passing context, instead of sending as much as possible ([[rag-retrieval|RAG: Retrieval]]; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).
- **Skills** instead of a long, permanently loaded system prompt ([[agent-skills|Agent Skills]]).
- **Prompt compression:** LLMLingua compresses prompts by up to 20 times with little loss in performance (Jiang et al., 2023).
- **Shorter outputs** where possible, because output tokens are more expensive.

The same prioritisation is described from a quality perspective in [[context-engineering|Context Engineering]].

#### 6. Smaller and compressed models

For self-hosted models, [[quantization|Quantization]] reduces memory and compute, and [[knowledge-distillation|Knowledge Distillation]] transfers capabilities of a large model to a smaller one; both lower the cost per request structurally.

#### Origin and variants

With the spread of paid LLM APIs, systematic cost strategies emerged: prompt adaptation, model approximation and cascades (Chen et al., 2023), learned routers (Ong et al., 2024) and prompt compression (Jiang et al., 2023), complemented by provider features such as prompt caching (Prompt caching docs) and batch APIs (Batch processing docs). Streaming does not reduce costs but lowers perceived latency, because users see the first tokens while the rest is generated.

### When to use it

- When request volumes are high or costs grow faster than usage.
- When requests vary in difficulty, so that not all need the largest model.
- When large, stable prompt prefixes or many non-urgent tasks exist.

### Strengths and limitations

**Strengths**
- Large savings are possible: up to 98% at equal performance with cascades (Chen et al., 2023), more than half with routers (Ong et al., 2024), 50% with batching (Batch processing docs).
- Caching also reduces latency (Prompt caching docs).
- Many measures need little implementation effort.

**Limitations**
- Routers and cascades must be trained, tested and monitored; a wrong routing decision lowers quality.
- Semantic caching can return answers to similar but different questions.
- Compression and smaller models can lose information or quality (Jiang et al., 2023).
- Agentic systems trade latency and cost for better task performance (Anthropic, 2024a), so savings in single calls can be eaten up by many calls.

### Comparison

| Measure | Effect | Effort |
|----------|----------------|------------|
| Prompt caching | High for stable prefixes (Prompt caching docs) | Low |
| Model routing | High for requests of mixed difficulty (Ong et al., 2024) | Medium: build and test a router |
| Limiting context | Medium to high (Jiang et al., 2023) | Low to medium |
| Batching | High, only for non-urgent tasks (Batch processing docs) | Low |
| Quantization or distillation | Structurally high | High: own model infrastructure |

### In practice

Budget control comes first: fan-out patterns, in which an agent triggers many sub-calls, and retries can multiply the cost of a single user request unnoticed, so budgets per run and alerts on cost thresholds are necessary ([[agentic-ai|Agentic AI]]; [[loop-engineering|Loop Engineering]]; [[harness-engineering|Harness Engineering]]). Cost attribution per trace shows which step causes the costs ([[llm-observability-and-tracing|LLM Observability and Tracing]]). Every optimisation is checked against an evaluation set, because cheaper must not mean worse unnoticed. Tool descriptions from connected servers also count as input tokens ([[mcp-and-related-protocols|MCP and Related Protocols]]), and spending limits matter in AI-assisted coding ([[vibe-coding|Vibe Coding]]). Cost is one of the cross-cutting topics in [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]]. Model providers offer their models through [[apis|APIs]] that are billed per token.

### Key takeaway

LLM costs depend on tokens, model choice and the number of calls; caching, routing, batching and shorter contexts save the most, but only budgets and tracing show whether savings in single calls survive in the whole system.

### Sources

- Chen, L. et al. (2023). *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance.* TMLR 2024. [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)
- Ong, I. et al. (2024). *RouteLLM: Learning to Route LLMs with Preference Data.* ICLR 2025. [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)
- Anthropic. *Prompt caching.* Claude Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- Anthropic. *Batch processing.* Claude Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- Jiang, H. et al. (2023). *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models.* EMNLP 2023. [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LLM-Kostenoptimierung senkt Kosten und Latenz beim Betrieb LLM-gestützter Systeme, ohne die Antwortqualität unnötig zu verschlechtern. Die Preise von LLM-APIs unterscheiden sich um bis zu zwei Größenordnungen (Chen et al., 2023), und bei hohem Anfragevolumen wird die Modellwahl pro Anfrage schnell zur größten variablen Kostenposition. Die wichtigsten Hebel sind Caching, das Weiterleiten von Anfragen an kleinere Modelle, Batching, kürzere Kontexte und Ausgaben sowie kleinere oder komprimierte Modelle; FrugalGPT erreichte etwa die Leistung des besten Einzelmodells bei bis zu 98 % geringeren Kosten (Chen et al., 2023). Die günstigste Anfrage ist die, die gar nicht nötig war.

### Funktionsweise

#### 1. Wo Kosten entstehen

```text
Kosten pro Anfrage ≈ Input-Token × Input-Preis + Output-Token × Output-Preis
```

Output-Token kosten meist ein Mehrfaches der Input-Token, etwa 2 gegenüber 10 US-Dollar pro Million Token (Prompt caching docs); lange Antworten, lange Kontexte und die Zahl der Aufrufe sind daher getrennte Hebel.

```text
Anfrage: 2.000 Input-Token + 300 Output-Token
großes Modell:  Input 3 / Output 15  (USD pro 1 Mio. Token) → (2.000 × 3 + 300 × 15) / 1.000.000 = 0,0105 USD
kleines Modell: Input 0,25 / Output 1,25                   → (2.000 × 0,25 + 300 × 1,25) / 1.000.000 ≈ 0,0009 USD
```

Die Preise im Beispiel sind beispielhaft; bei 100.000 Anfragen pro Tag summiert sich der Unterschied auf etwa 1.050 gegenüber 88 US-Dollar täglich.

#### 2. Caching

- **Exact-Match-Caching:** Identische Anfragen werden ohne Modellaufruf aus einem Cache beantwortet.
- **Prompt Caching:** Der Anbieter speichert einen Prompt-Präfix bis zu einem Haltepunkt und nutzt ihn bei späteren Anfragen mit demselben Präfix wieder, was Verarbeitungszeit und Kosten senkt; das eignet sich für lange Systemprompts, viele Beispiele, umfangreichen Hintergrundkontext und Unterhaltungen über viele Runden. Cache-Schreibvorgänge kosten mehr als normale Input-Token, Cache-Treffer nur einen Bruchteil des Input-Preises, und der Cache lebt standardmäßig wenige Minuten (Prompt caching docs).
- **Semantisches Caching:** Ähnliche, nicht nur identische Anfragen werden mithilfe von Embeddings aus dem Cache beantwortet ([[embeddings|Embeddings]]); das spart mehr Aufrufe, riskiert aber, Unterschiede zwischen ähnlichen Anfragen zu übersehen.

Die Cache-Trefferquote ist die zentrale Kennzahl: Bei 40 % Trefferquote und 0,01 US-Dollar pro nicht gecachter Anfrage sinken die Durchschnittskosten auf etwa 0,006 US-Dollar.

#### 3. Model Routing und Kaskaden

Nicht jede Anfrage braucht das leistungsfähigste Modell. Ein Router, oft ein kleines Modell oder ein Klassifikator ([[classification|Klassifikation]]), schätzt die Schwierigkeit ein und wählt das Zielmodell; einfache und häufige Fragen können an kleinere, günstigere Modelle gehen und schwierige an leistungsfähigere (Anthropic, 2024a). RouteLLM trainiert Router auf menschlichen Präferenzdaten, die zwischen einem starken und einem schwachen Modell wählen, und senkte die Kosten in manchen Fällen um mehr als die Hälfte, ohne die Antwortqualität zu verringern (Ong et al., 2024). FrugalGPT verbindet Prompt-Anpassung, Approximation von LLMs und LLM-Kaskaden, die lernen, welche Modellkombination für welche Anfragen genutzt wird (Chen et al., 2023). Dieselbe Idee aus beratendem und ausführendem Modell taucht in Multi-Agenten-Systemen auf ([[graph-engineering|Graph Engineering]]).

#### 4. Batching

Anfragen, die keine sofortige Antwort brauchen, lassen sich gemeinsam zur asynchronen Verarbeitung einreichen; Batch-APIs senken die Kosten um 50 %, die meisten Batches sind innerhalb einer Stunde fertig, spätestens nach 24 Stunden (Batch processing docs). Das eignet sich für Massenverarbeitung und große Evaluationen, etwa mit [[llm-as-a-judge|LLM-as-a-Judge]].

#### 5. Kontext und Ausgabe begrenzen

- **Reranking** vor der Kontextübergabe, statt möglichst viel mitzuschicken ([[rag-retrieval|RAG: Retrieval]]; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).
- **Skills** statt eines langen, dauerhaft geladenen Systemprompts ([[agent-skills|Agent Skills]]).
- **Prompt-Kompression:** LLMLingua komprimiert Prompts bis auf ein Zwanzigstel bei geringem Leistungsverlust (Jiang et al., 2023).
- **Kürzere Ausgaben**, wo möglich, weil Output-Token teurer sind.

Dieselbe Priorisierung beschreibt [[context-engineering|Context Engineering]] aus Sicht der Qualität.

#### 6. Kleinere und komprimierte Modelle

Für selbst betriebene Modelle senkt [[quantization|Quantisierung]] Speicher- und Rechenbedarf, und [[knowledge-distillation|Knowledge Distillation]] überträgt Fähigkeiten eines großen Modells auf ein kleineres; beide senken die Kosten pro Anfrage strukturell.

#### Ursprung und Varianten

Mit der Verbreitung kostenpflichtiger LLM-APIs entstanden systematische Kostenstrategien: Prompt-Anpassung, Modellapproximation und Kaskaden (Chen et al., 2023), gelernte Router (Ong et al., 2024) und Prompt-Kompression (Jiang et al., 2023), ergänzt durch Anbieterfunktionen wie Prompt Caching (Prompt caching docs) und Batch-APIs (Batch processing docs). Streaming senkt die Kosten nicht, verringert aber die gefühlte Latenz, weil Nutzende die ersten Token sehen, während der Rest noch erzeugt wird.

### Wann einsetzen

- Wenn das Anfragevolumen hoch ist oder die Kosten schneller wachsen als die Nutzung.
- Wenn Anfragen unterschiedlich schwierig sind und nicht alle das größte Modell brauchen.
- Wenn große, stabile Prompt-Präfixe oder viele nicht dringende Aufgaben vorliegen.

### Stärken und Grenzen

**Stärken**
- Große Einsparungen sind möglich: bis zu 98 % bei gleicher Leistung mit Kaskaden (Chen et al., 2023), mehr als die Hälfte mit Routern (Ong et al., 2024), 50 % mit Batching (Batch processing docs).
- Caching senkt zusätzlich die Latenz (Prompt caching docs).
- Viele Maßnahmen erfordern wenig Umsetzungsaufwand.

**Einschränkungen**
- Router und Kaskaden müssen trainiert, getestet und überwacht werden; eine falsche Weiterleitung senkt die Qualität.
- Semantisches Caching kann Antworten auf ähnliche, aber andere Fragen liefern.
- Kompression und kleinere Modelle können Informationen oder Qualität verlieren (Jiang et al., 2023).
- Agentische Systeme tauschen Latenz und Kosten gegen bessere Aufgabenleistung (Anthropic, 2024a); Einsparungen bei einzelnen Aufrufen können durch viele Aufrufe aufgezehrt werden.

### Vergleich

| Maßnahme | Wirkung | Aufwand |
|----------|----------------|------------|
| Prompt Caching | Hoch bei stabilen Präfixen (Prompt caching docs) | Gering |
| Model Routing | Hoch bei unterschiedlich schwierigen Anfragen (Ong et al., 2024) | Mittel: Router bauen und testen |
| Kontext begrenzen | Mittel bis hoch (Jiang et al., 2023) | Gering bis mittel |
| Batching | Hoch, nur für nicht dringende Aufgaben (Batch processing docs) | Gering |
| Quantisierung oder Distillation | Strukturell hoch | Hoch: eigene Modellinfrastruktur |

### In der Praxis

Budgetkontrolle steht an erster Stelle: Fan-out-Muster, bei denen ein Agent viele Unteraufrufe auslöst, und Wiederholungen können die Kosten einer einzelnen Nutzeranfrage unbemerkt vervielfachen; Budgets pro Lauf und Alarme bei Kostenschwellen sind daher nötig ([[agentic-ai|Agentic AI]]; [[loop-engineering|Loop Engineering]]; [[harness-engineering|Harness Engineering]]). Die Kostenzuordnung pro Trace zeigt, welcher Schritt die Kosten verursacht ([[llm-observability-and-tracing|LLM-Observability und Tracing]]). Jede Optimierung wird gegen ein Evaluationsset geprüft, denn günstiger darf nicht unbemerkt schlechter bedeuten. Werkzeugbeschreibungen angebundener Server zählen ebenfalls als Input-Token ([[mcp-and-related-protocols|MCP und ähnliche Protokolle]]), und beim KI-gestützten Programmieren sind Ausgabelimits wichtig ([[vibe-coding|Vibe Coding]]). Kosten sind eines der Querschnittsthemen in [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]]. Modellanbieter stellen ihre Modelle über [[apis|APIs (Programmierschnittstellen)]] bereit, die pro Token abgerechnet werden.

### Merksatz

LLM-Kosten hängen von Token, Modellwahl und Zahl der Aufrufe ab; Caching, Routing, Batching und kürzere Kontexte sparen am meisten, doch erst Budgets und Tracing zeigen, ob Einsparungen bei einzelnen Aufrufen im Gesamtsystem bestehen bleiben.

### Quellen

- Chen, L. et al. (2023). *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance.* TMLR 2024. [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)
- Ong, I. et al. (2024). *RouteLLM: Learning to Route LLMs with Preference Data.* ICLR 2025. [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)
- Anthropic. *Prompt caching.* Claude Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- Anthropic. *Batch processing.* Claude Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- Jiang, H. et al. (2023). *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models.* EMNLP 2023. [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
