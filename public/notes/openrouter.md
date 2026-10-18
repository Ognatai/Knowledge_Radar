---
title_en: OpenRouter
title_de: OpenRouter
entity_type: Organisation
jurisdiction: International
aliases:
- OpenRouter
- Open Router
- openrouter.ai
sources:
- https://openrouter.ai/docs/quickstart
- https://openrouter.ai/docs/features/provider-routing
- https://openrouter.ai/docs/faq
- https://openrouter.ai/api/v1/models
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

OpenRouter is a platform that gives access to hundreds of AI models from many providers through a single API endpoint; it is compatible with the OpenAI SDK, routes each request to one of the providers serving the chosen model and falls back to others when a provider fails (OpenRouter Quickstart). Model ids carry the model's developer as a prefix, for example `openai/…` or `anthropic/…`, and on 18 October 2026 the public model list contained 471 models under 67 prefixes (OpenRouter models API). OpenRouter states that it adds no markup to inference prices and earns a fee on credit purchases, and that it does not log prompts and completions unless a customer opts in (OpenRouter FAQ). For AI development it is a gateway: one key and one API to compare, switch and combine models from different vendors.

### Key facts

| | |
|---|---|
| Type | commercial API platform (LLM gateway / router) |
| Access | one [[http\|HTTP]] endpoint, `https://openrouter.ai/api/v1/chat/completions`; OpenAI SDK as drop-in client |
| Models | "hundreds of AI models"; 471 models under 67 developer prefixes in the models API on 18 October 2026 |
| Pricing | no markup on inference prices; 5.5% fee (minimum 0.80 USD) on credit purchases, 5% for crypto payments |
| Data | no logging of prompts and completions unless opted in |
| Regional routing | EU in-region routing for Business and Enterprise customers |

Sources: OpenRouter Quickstart; OpenRouter FAQ; OpenRouter models API.

### Mandate and tasks

OpenRouter describes its purpose as providing "a unified API to access all the major LLM models on the market" (OpenRouter FAQ). It handles fallbacks automatically and picks the most cost-effective option for each request (OpenRouter Quickstart). Its tasks are therefore to aggregate model providers behind one interface, to route and fail over requests between providers, and to bill usage centrally.

### Structure and working methods

#### One API for many providers

Requests go to one endpoint and name a model by a slug prefixed with its developer; the full list of slugs is available through `GET /api/v1/models`, and the OpenAI SDK can be pointed at OpenRouter as a drop-in replacement (OpenRouter Quickstart). Applications written against the OpenAI chat completions format can thus switch to models of other vendors by changing the model id, which is how [[apis|APIs]] with a shared format reduce lock-in.

#### Provider routing

Many models are served by several providers. By default, OpenRouter load-balances requests across the top providers to maximise uptime: it prioritises providers without significant outages in the last 30 seconds and then selects one weighted by the inverse square of the price (OpenRouter provider routing). A `provider` object in the request overrides this: `order` lists providers to try in sequence, `only` and `ignore` allow or exclude providers, `sort` orders them by price, throughput or latency, `allow_fallbacks` controls whether backup providers may be used, `data_collection: deny` restricts routing to providers that do not store user data non-transiently or train on it, and `zdr` restricts it to zero-data-retention endpoints (OpenRouter provider routing). Setting `sort` or `order` disables load balancing, and restricting providers reduces fallback options (OpenRouter provider routing).

#### Billing and data handling

Customers buy credits; OpenRouter states that there is no markup on inference pricing and charges 5.5% (at least 0.80 USD) on credit purchases, or 5% for crypto payments (OpenRouter FAQ). With bring-your-own-key (BYOK), customers use their own provider keys; pay-as-you-go includes 25,000 USD per month of BYOK usage without fee, after which a fee of 5% of the normal OpenRouter price applies (OpenRouter FAQ). OpenRouter states that it does no logging of prompts and completions, even on errors, unless the customer opts in, which earns a 1% discount (OpenRouter FAQ); the providers it routes to have their own data policies, which the `data_collection` and `zdr` options take into account (OpenRouter provider routing).

### Key outputs

- The unified chat completions API with OpenAI SDK compatibility and streaming (OpenRouter Quickstart).
- The public models list with slugs prefixed by the developer (OpenRouter models API).
- Provider routing with load balancing, fallbacks and filters for price, latency, throughput and data policy (OpenRouter provider routing).

### Relationship to other bodies

OpenRouter routes to model developers and hosting providers such as [[openai|OpenAI]] and [[anthropic|Anthropic]], whose models appear under their own prefixes in the models list (OpenRouter models API). Hyperscaler platforms such as Azure, Vertex AI or Bedrock offer a similar choice of models within one cloud, see [[cloud-ai-platforms|cloud AI platforms]].

### In practice

A gateway like OpenRouter is useful for prototyping and evaluation, because many models can be tested with one key and one client ([[model-comparison|model comparison]], [[llm-evaluation|LLM evaluation]]), and for setups that combine models from different vendors, such as [[cross-model-review|cross-model review]], where a model from a different lineage checks another model's output. Routing by price and fallbacks between providers support [[llm-cost-optimisation|LLM cost optimisation]] and availability. Agent frameworks that accept an OpenAI-compatible endpoint can use it as a provider ([[agent-frameworks|agent frameworks]]).

### Relevance for AI development

An extra intermediary sits between the application and the model provider, so data protection reviews have to cover both OpenRouter's and the selected providers' data handling; the `data_collection: deny` and `zdr` options and EU in-region routing exist for this purpose (OpenRouter provider routing; OpenRouter Quickstart). Whether such routing is adequate for personal data under the [[gdpr|GDPR]] is a question for the deploying organisation, not something the documentation settles. Because the same model can be served by different providers, results can differ between providers; pinning providers with `order` or `only` keeps evaluations reproducible at the cost of fallback options (OpenRouter provider routing).

### Sources

- OpenRouter (2026). *Quickstart.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/quickstart)
- OpenRouter (2026). *Provider Routing.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/features/provider-routing)
- OpenRouter (2026). *FAQ.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/faq)
- OpenRouter (2026). *Models API* (`GET /api/v1/models`), retrieved 18 October 2026. [openrouter.ai](https://openrouter.ai/api/v1/models)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

OpenRouter ist eine Plattform, die über einen einzigen API-Endpunkt Zugang zu Hunderten von KI-Modellen vieler Anbieter bietet; sie ist mit dem OpenAI-SDK kompatibel, leitet jede Anfrage an einen der Anbieter weiter, die das gewählte Modell betreiben, und weicht auf andere aus, wenn ein Anbieter ausfällt (OpenRouter Quickstart). Modell-IDs tragen den Entwickler des Modells als Präfix, etwa `openai/…` oder `anthropic/…`, und am 18. Oktober 2026 enthielt die öffentliche Modellliste 471 Modelle unter 67 Präfixen (OpenRouter Models API). OpenRouter gibt an, auf Inferenzpreise keinen Aufschlag zu erheben und an einer Gebühr beim Kauf von Guthaben zu verdienen, und Prompts und Antworten nicht zu protokollieren, sofern Kundinnen und Kunden dem nicht zustimmen (OpenRouter FAQ). Für die KI-Entwicklung ist es ein Gateway: ein Schlüssel und eine API, um Modelle verschiedener Hersteller zu vergleichen, zu wechseln und zu kombinieren.

### Eckdaten

| | |
|---|---|
| Art | kommerzielle API-Plattform (LLM-Gateway / Router) |
| Zugang | ein HTTP-Endpunkt, `https://openrouter.ai/api/v1/chat/completions`; OpenAI-SDK als direkter Ersatz-Client |
| Modelle | „hundreds of AI models“; 471 Modelle unter 67 Entwickler-Präfixen in der Models API am 18. Oktober 2026 |
| Preise | kein Aufschlag auf Inferenzpreise; 5,5 % Gebühr (mindestens 0,80 USD) beim Kauf von Guthaben, 5 % bei Zahlung mit Kryptowährung |
| Daten | keine Protokollierung von Prompts und Antworten ohne Zustimmung |
| Regionales Routing | Routing innerhalb der EU für Business- und Enterprise-Kunden |

Quellen: OpenRouter Quickstart; OpenRouter FAQ; OpenRouter Models API.

### Auftrag und Aufgaben

OpenRouter beschreibt seinen Zweck als „a unified API to access all the major LLM models on the market“ (OpenRouter FAQ). Die Plattform übernimmt Fallbacks automatisch und wählt für jede Anfrage die kostengünstigste Option (OpenRouter Quickstart). Ihre Aufgaben sind damit, Modellanbieter hinter einer Schnittstelle zu bündeln, Anfragen zwischen Anbietern zu verteilen und bei Ausfällen umzuleiten sowie die Nutzung zentral abzurechnen.

### Aufbau und Arbeitsweise

#### Eine API für viele Anbieter

Anfragen gehen an einen Endpunkt und nennen ein Modell über einen Slug mit dem Entwickler als Präfix; die vollständige Liste der Slugs liefert `GET /api/v1/models`, und das OpenAI-SDK lässt sich als direkter Ersatz auf OpenRouter richten (OpenRouter Quickstart). Anwendungen, die für das Chat-Completions-Format von OpenAI geschrieben sind, können so durch Ändern der Modell-ID zu Modellen anderer Hersteller wechseln; so verringern [[apis|APIs]] mit gemeinsamem Format die Bindung an einen Anbieter.

#### Routing zwischen Anbietern

Viele Modelle werden von mehreren Anbietern betrieben. Standardmäßig verteilt OpenRouter Anfragen auf die besten Anbieter, um die Verfügbarkeit zu maximieren: Es bevorzugt Anbieter ohne nennenswerte Ausfälle in den letzten 30 Sekunden und wählt dann einen, gewichtet mit dem Kehrwert des Quadrats des Preises (OpenRouter Provider Routing). Ein `provider`-Objekt in der Anfrage überschreibt das: `order` nennt Anbieter, die der Reihe nach versucht werden, `only` und `ignore` lassen Anbieter zu oder schließen sie aus, `sort` ordnet sie nach Preis, Durchsatz oder Latenz, `allow_fallbacks` legt fest, ob Ersatzanbieter genutzt werden dürfen, `data_collection: deny` beschränkt das Routing auf Anbieter, die Nutzerdaten nicht dauerhaft speichern oder damit trainieren, und `zdr` auf Endpunkte ohne Datenspeicherung (Zero Data Retention) (OpenRouter Provider Routing). Mit `sort` oder `order` wird die Lastverteilung abgeschaltet, und wer Anbieter einschränkt, verringert die Ausweichmöglichkeiten (OpenRouter Provider Routing).

#### Abrechnung und Umgang mit Daten

Kundinnen und Kunden kaufen Guthaben; OpenRouter gibt an, auf Inferenzpreise keinen Aufschlag zu erheben, und berechnet beim Kauf von Guthaben 5,5 % (mindestens 0,80 USD), bei Kryptowährung 5 % (OpenRouter FAQ). Mit eigenen Schlüsseln der Anbieter (Bring Your Own Key, BYOK) sind im Pay-as-you-go-Tarif 25.000 USD BYOK-Nutzung pro Monat gebührenfrei, darüber fällt eine Gebühr von 5 % des normalen OpenRouter-Preises an (OpenRouter FAQ). OpenRouter gibt an, Prompts und Antworten nicht zu protokollieren, auch nicht bei Fehlern, sofern dem nicht zugestimmt wird; eine Zustimmung bringt 1 % Rabatt (OpenRouter FAQ). Die Anbieter, an die weitergeleitet wird, haben eigene Datenrichtlinien, die die Optionen `data_collection` und `zdr` berücksichtigen (OpenRouter Provider Routing).

### Wichtige Ergebnisse

- Die einheitliche Chat-Completions-API mit Kompatibilität zum OpenAI-SDK und Streaming (OpenRouter Quickstart).
- Die öffentliche Modellliste mit Slugs samt Entwickler-Präfix (OpenRouter Models API).
- Routing zwischen Anbietern mit Lastverteilung, Fallbacks und Filtern für Preis, Latenz, Durchsatz und Datenrichtlinie (OpenRouter Provider Routing).

### Verhältnis zu anderen Stellen

OpenRouter leitet an Modellentwickler und Hosting-Anbieter wie [[openai|OpenAI]] und [[anthropic|Anthropic]] weiter, deren Modelle unter eigenen Präfixen in der Modellliste stehen (OpenRouter Models API). Plattformen der großen Cloud-Anbieter wie Azure, Vertex AI oder Bedrock bieten eine ähnliche Modellauswahl innerhalb einer Cloud, siehe [[cloud-ai-platforms|Cloud-KI-Plattformen]].

### In der Praxis

Ein Gateway wie OpenRouter hilft bei Prototypen und Evaluationen, weil sich viele Modelle mit einem Schlüssel und einem Client testen lassen ([[model-comparison|Modellvergleich]], [[llm-evaluation|LLM-Evaluation]]), und bei Aufbauten, die Modelle verschiedener Hersteller kombinieren, etwa beim [[cross-model-review|Cross-Model Review]], in dem ein Modell einer anderen Modellfamilie die Ausgabe eines anderen prüft. Routing nach Preis und Fallbacks zwischen Anbietern unterstützen die [[llm-cost-optimisation|LLM-Kostenoptimierung]] und die Verfügbarkeit. Agent-Frameworks, die einen OpenAI-kompatiblen Endpunkt akzeptieren, können es als Anbieter nutzen ([[agent-frameworks|Agent-Frameworks]]).

### Bedeutung für die KI-Entwicklung

Zwischen Anwendung und Modellanbieter sitzt eine weitere Stelle, sodass Datenschutzprüfungen sowohl den Umgang von OpenRouter als auch den der gewählten Anbieter mit Daten abdecken müssen; dafür gibt es die Optionen `data_collection: deny` und `zdr` sowie das Routing innerhalb der EU (OpenRouter Provider Routing; OpenRouter Quickstart). Ob ein solches Routing für personenbezogene Daten nach der [[gdpr|DSGVO]] ausreicht, muss die einsetzende Organisation beurteilen; die Dokumentation klärt das nicht. Weil dasselbe Modell von verschiedenen Anbietern betrieben werden kann, können Ergebnisse zwischen Anbietern abweichen; Anbieter mit `order` oder `only` festzulegen hält Evaluationen reproduzierbar, kostet aber Ausweichmöglichkeiten (OpenRouter Provider Routing).

### Quellen

- OpenRouter (2026). *Quickstart.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/quickstart)
- OpenRouter (2026). *Provider Routing.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/features/provider-routing)
- OpenRouter (2026). *FAQ.* OpenRouter documentation. [openrouter.ai](https://openrouter.ai/docs/faq)
- OpenRouter (2026). *Models API* (`GET /api/v1/models`), retrieved 18 October 2026. [openrouter.ai](https://openrouter.ai/api/v1/models)
