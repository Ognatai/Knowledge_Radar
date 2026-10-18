---
title_en: Dialogflow CX
title_de: Dialogflow CX
entity_type: Technology
aliases:
- Dialogflow CX
- Conversational Agents (Dialogflow CX)
sources:
- https://docs.cloud.google.com/dialogflow/cx/docs/basics
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook
- https://docs.cloud.google.com/dialogflow/docs/editions
- https://docs.cloud.google.com/dialogflow/cx/docs/quick/api
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Dialogflow CX is Google Cloud's platform for building chat and voice agents that turn user text or audio into structured data and handle many conversations at once (Google Cloud, 2026a). Conversations are modelled deterministically as flows made of pages, the states of a session, with intents, parameters, forms and routes that decide the next page; generative playbooks let an LLM pursue a goal by following instructions and calling tools, and both approaches can be combined in one agent (Google Cloud, 2026a; Google Cloud, 2026b). Google positions CX for large or complex agents and the older Dialogflow ES, built on intents and contexts, for small to medium ones (Google Cloud, 2026c). The console is being renamed to Conversational Agents. It is one of the main platforms for enterprise [[conversational-ai|conversational AI]] and [[voice-agents|voice agents]].

### Core concepts

```text
agent ── Default Start Flow ── page A ──(intent route: "book_table")──► page B (form: date, party_size)
          │                      │                                          │ condition route: $page.params.status = "FINAL"
          │                      └─ event handlers: no-match, no-input      ▼
          ├── flow "Payments" ...                                         page C ── fulfillment: message / webhook
          └── playbook "Answer FAQ" (goal, instructions, examples, tools) ⇄ flows
```

#### 1. Agents, flows and pages

An agent is a virtual agent that handles concurrent conversations; flows model conversation topics, and every agent starts with a Default Start Flow (Google Cloud, 2026a). Pages represent the states of a session: at any time exactly one page is current, and each turn either keeps it or moves to another page. When creating an agent, a region is chosen in which data at rest stays; it cannot be changed later without exporting and restoring to a new agent (Google Cloud, 2026a).

#### 2. Intents, entity types and parameters

An intent classifies what the user means in a turn, based on training phrases, parameters and optional DTMF patterns for telephone keypads (Google Cloud, 2026a). Entity types control how values are extracted from input, either predefined system entities or custom ones, and parameters store the extracted values for later logic and responses. A page can define a form of parameters that the agent collects one by one with prompts until all required values are known (Google Cloud, 2026a; [[natural-language-understanding|natural language understanding]]).

#### 3. Routes, event handlers and fulfillment

Intent routes fire when an intent matches, and condition routes when a session condition is true; event handlers react to built-in events such as unexpected input or webhook errors and to custom events (Google Cloud, 2026a). Routes and handlers are processed by scope, evaluated in order, and then called, which runs their fulfillment and any transition. Fulfillment can contain static messages, webhook calls to the developer's own service and parameter presets; responses are queued and sent at the end of the turn (Google Cloud, 2026a).

#### 4. Generative playbooks

A playbook is the basic building block of generative agents: it has a name, a goal, step-by-step instructions, example conversations that act as few-shot prompts, parameters and tools that query external services, and its data is passed to the LLM ([[few-shot-prompting|few-shot prompting]]) (Google Cloud, 2026b). A playbook can hand a sub-task to a flow or another playbook. Task playbooks exchange input and output parameters and are reusable but add an LLM call each time; routine playbooks run sequential stages and can chain several transitions in one turn, which saves LLM calls and latency (Google Cloud, 2026b).

#### Origin and variants

Dialogflow comes in two editions: ES, where intents are the building blocks and contexts control conversation paths, suited to small to medium, moderately complex agents; and CX, for large or complex applications, with a deterministic design based on flows and a generative design with playbooks (Google Cloud, 2026c). CX is billed pay-as-you-go, for example $0.007 per text request, against $0.002 for ES Essentials (Google Cloud, 2026c). Built-in integrations cover telephony providers and text channels; when using the API directly, developers host their own interface and webhook service (Google Cloud, 2026a).

### Common usage

```python
import uuid
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session

agent = "projects/PROJECT/locations/LOCATION/agents/AGENT_ID"
session_path = f"{agent}/sessions/{uuid.uuid4()}"          # one session per conversation
client = SessionsClient(client_options={"api_endpoint": "LOCATION-dialogflow.googleapis.com"})

query_input = session.QueryInput(text=session.TextInput(text="Book a table for two"),
                                 language_code="en")
response = client.detect_intent(request=session.DetectIntentRequest(
    session=session_path, query_input=query_input))
print(" ".join(" ".join(m.text.text) for m in response.query_result.response_messages))
```

Adapted from the detect-intent sample in Google Cloud (2026d).

### When to use it

- Customer service bots and phone agents with many explicit paths, forms and handovers (Google Cloud, 2026a; [[conversation-design|conversation design]]).
- Large or complex agents that outgrow intent-and-context designs (Google Cloud, 2026c).
- Hybrid agents in which regulated or transactional steps stay deterministic while open questions go to generative playbooks (Google Cloud, 2026b).

### Strengths and limitations

**Strengths**
- Explicit state machine of flows and pages makes conversation paths visible and testable (Google Cloud, 2026a).
- Built-in handling of no-match and no-input events and of telephony integrations (Google Cloud, 2026a).
- Deterministic flows and generative playbooks in one agent (Google Cloud, 2026b).

**Limitations**
- Playbooks are excluded from the Dialogflow CX SLA and do not support DTMF input (Google Cloud, 2026b).
- Playbook instructions work best in English; for other languages, language support should be declared in the instructions and examples written in the target language (Google Cloud, 2026b).
- The agent's region cannot be changed after creation (Google Cloud, 2026a).
- Vendor lock-in: agents are built for Google Cloud's runtime and pricing.

### Comparison

| | Dialogflow ES | Dialogflow CX |
|---|---|---|
| Building blocks | intents and contexts | flows, pages, routes; generative playbooks |
| Recommended size | up to medium | up to very large |
| Recommended complexity | up to moderately complex | up to highly complex |
| Text request price (example) | $0.002 (Essentials) | $0.007 |

Source: Google Cloud (2026c).

### In practice

Model each topic as its own flow and keep pages small; define handlers for repeated no-match and no-input events that end in a handover to a human ([[conversational-ai|conversational AI]]). Use [[asynchronous-apis|webhooks]] for anything that touches back-end systems, and keep generative playbooks to tasks where free conversation helps, guarded like other LLM applications ([[llm-guardrails|LLM guardrails]] and [[red-teaming|red teaming]]). Conversation logs and analytics show where users drop out or are misunderstood ([[conversation-analytics|conversation analytics]]).

### Key takeaway

Dialogflow CX models conversations as flows of pages with intents, forms and routes, and adds generative playbooks for LLM-driven tasks; it is aimed at large, complex chat and voice agents on Google Cloud.

### Sources

- Google Cloud (2026a). *Dialogflow CX basics*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/basics)
- Google Cloud (2026b). *Playbooks*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook)
- Google Cloud (2026c). *Dialogflow editions*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/docs/editions)
- Google Cloud (2026d). *Interact with the API*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/quick/api)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Dialogflow CX ist die Plattform von Google Cloud zum Bau von Chat- und Sprachagenten, die Text- oder Audioeingaben in strukturierte Daten umwandeln und viele Gespräche gleichzeitig bearbeiten (Google Cloud, 2026a). Gespräche werden deterministisch als Flows aus Pages modelliert, den Zuständen einer Sitzung, mit Intents, Parametern, Formularen und Routen, die über die nächste Page entscheiden; generative Playbooks lassen ein LLM ein Ziel verfolgen, indem es Anweisungen befolgt und Werkzeuge aufruft, und beide Ansätze lassen sich in einem Agenten kombinieren (Google Cloud, 2026a; Google Cloud, 2026b). Google sieht CX für große oder komplexe Agenten vor und das ältere Dialogflow ES, das auf Intents und Kontexten beruht, für kleine bis mittlere (Google Cloud, 2026c). Die Konsole wird in Conversational Agents umbenannt. Sie ist eine der wichtigsten Plattformen für [[conversational-ai|Conversational AI]] und [[voice-agents|Voice Agents]] in Unternehmen.

### Kernkonzepte

```text
Agent ── Default Start Flow ── Page A ──(Intent-Route: "book_table")──► Page B (Formular: Datum, Personenzahl)
          │                      │                                          │ Bedingungsroute: $page.params.status = "FINAL"
          │                      └─ Event-Handler: no-match, no-input       ▼
          ├── Flow "Payments" ...                                         Page C ── Fulfillment: Nachricht / Webhook
          └── Playbook "Answer FAQ" (Ziel, Anweisungen, Beispiele, Werkzeuge) ⇄ Flows
```

#### 1. Agenten, Flows und Pages

Ein Agent ist ein virtueller Agent, der gleichzeitige Gespräche bearbeitet; Flows modellieren Gesprächsthemen, und jeder Agent beginnt mit einem Default Start Flow (Google Cloud, 2026a). Pages stellen die Zustände einer Sitzung dar: Zu jedem Zeitpunkt ist genau eine Page aktiv, und jeder Gesprächszug behält sie bei oder wechselt zu einer anderen. Beim Anlegen eines Agenten wird eine Region gewählt, in der ruhende Daten bleiben; sie lässt sich später nur durch Export und Wiederherstellung in einen neuen Agenten ändern (Google Cloud, 2026a).

#### 2. Intents, Entitätstypen und Parameter

Ein Intent klassifiziert, was Nutzende in einem Gesprächszug meinen, auf Basis von Trainingsphrasen, Parametern und optionalen DTMF-Mustern für Telefontastaturen (Google Cloud, 2026a). Entitätstypen steuern, wie Werte aus der Eingabe extrahiert werden, entweder vordefinierte Systementitäten oder eigene, und Parameter speichern die extrahierten Werte für spätere Logik und Antworten. Eine Page kann ein Formular aus Parametern definieren, die der Agent nacheinander mit Rückfragen erfasst, bis alle erforderlichen Werte bekannt sind (Google Cloud, 2026a; [[natural-language-understanding|Natural Language Understanding]]).

#### 3. Routen, Event-Handler und Fulfillment

Intent-Routen greifen, wenn ein Intent erkannt wird, Bedingungsrouten, wenn eine Sitzungsbedingung erfüllt ist; Event-Handler reagieren auf eingebaute Ereignisse wie unerwartete Eingaben oder Webhook-Fehler sowie auf eigene Ereignisse (Google Cloud, 2026a). Routen und Handler werden nach Geltungsbereich ausgewählt, der Reihe nach ausgewertet und dann aufgerufen, wobei ihr Fulfillment und ein etwaiger Übergang ausgeführt werden. Fulfillment kann statische Nachrichten, Webhook-Aufrufe an den eigenen Dienst und Parametervorgaben enthalten; Antworten werden gesammelt und am Ende des Gesprächszugs gesendet (Google Cloud, 2026a).

#### 4. Generative Playbooks

Ein Playbook ist der Grundbaustein generativer Agenten: Es hat einen Namen, ein Ziel, schrittweise Anweisungen, Beispielgespräche, die als Few-Shot-Prompts dienen, Parameter und Werkzeuge, die externe Dienste abfragen, und seine Daten werden an das LLM übergeben ([[few-shot-prompting|Few-Shot-Prompting]]) (Google Cloud, 2026b). Ein Playbook kann eine Teilaufgabe an einen Flow oder ein anderes Playbook übergeben. Task-Playbooks tauschen Ein- und Ausgabeparameter aus und sind wiederverwendbar, kosten aber jedes Mal einen LLM-Aufruf; Routine-Playbooks führen aufeinanderfolgende Phasen aus und können mehrere Übergänge in einem Gesprächszug verketten, was LLM-Aufrufe und Latenz spart (Google Cloud, 2026b).

#### Herkunft und Varianten

Dialogflow gibt es in zwei Editionen: ES, bei der Intents die Bausteine sind und Kontexte die Gesprächspfade steuern, geeignet für kleine bis mittlere, mäßig komplexe Agenten; und CX für große oder komplexe Anwendungen, mit einem deterministischen Entwurf auf Basis von Flows und einem generativen Entwurf mit Playbooks (Google Cloud, 2026c). CX wird nutzungsbasiert abgerechnet, etwa 0,007 US-Dollar je Textanfrage gegenüber 0,002 US-Dollar bei ES Essentials (Google Cloud, 2026c). Eingebaute Integrationen decken Telefonieanbieter und Textkanäle ab; bei direkter Nutzung der API betreiben Entwicklerinnen und Entwickler ihre eigene Oberfläche und ihren eigenen Webhook-Dienst (Google Cloud, 2026a).

### Typische Verwendung

```python
import uuid
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session

agent = "projects/PROJECT/locations/LOCATION/agents/AGENT_ID"
session_path = f"{agent}/sessions/{uuid.uuid4()}"          # eine Sitzung je Gespräch
client = SessionsClient(client_options={"api_endpoint": "LOCATION-dialogflow.googleapis.com"})

query_input = session.QueryInput(text=session.TextInput(text="Book a table for two"),
                                 language_code="en")
response = client.detect_intent(request=session.DetectIntentRequest(
    session=session_path, query_input=query_input))
print(" ".join(" ".join(m.text.text) for m in response.query_result.response_messages))
```

Angepasst nach dem Detect-Intent-Beispiel in Google Cloud (2026d).

### Wann einsetzen

- Kundenservice-Bots und Telefonagenten mit vielen expliziten Pfaden, Formularen und Übergaben (Google Cloud, 2026a; [[conversation-design|Conversation Design]]).
- Große oder komplexe Agenten, die über Entwürfe aus Intents und Kontexten hinauswachsen (Google Cloud, 2026c).
- Hybride Agenten, in denen regulierte oder transaktionale Schritte deterministisch bleiben, während offene Fragen an generative Playbooks gehen (Google Cloud, 2026b).

### Stärken und Grenzen

**Stärken**
- Die explizite Zustandsmaschine aus Flows und Pages macht Gesprächspfade sichtbar und testbar (Google Cloud, 2026a).
- Eingebaute Behandlung von no-match- und no-input-Ereignissen sowie Telefonieintegrationen (Google Cloud, 2026a).
- Deterministische Flows und generative Playbooks in einem Agenten (Google Cloud, 2026b).

**Grenzen**
- Playbooks sind vom SLA für Dialogflow CX ausgenommen und unterstützen keine DTMF-Eingaben (Google Cloud, 2026b).
- Playbook-Anweisungen funktionieren am besten auf Englisch; für andere Sprachen sollte die Sprachunterstützung in den Anweisungen erklärt und Beispiele in der Zielsprache geschrieben werden (Google Cloud, 2026b).
- Die Region eines Agenten lässt sich nach dem Anlegen nicht ändern (Google Cloud, 2026a).
- Anbieterbindung: Agenten sind für Laufzeit und Preismodell von Google Cloud gebaut.

### Vergleich

| | Dialogflow ES | Dialogflow CX |
|---|---|---|
| Bausteine | Intents und Kontexte | Flows, Pages, Routen; generative Playbooks |
| Empfohlene Größe | bis mittel | bis sehr groß |
| Empfohlene Komplexität | bis mäßig komplex | bis hoch komplex |
| Preis je Textanfrage (Beispiel) | 0,002 US-Dollar (Essentials) | 0,007 US-Dollar |

Quelle: Google Cloud (2026c).

### In der Praxis

Jedes Thema wird als eigener Flow modelliert, Pages bleiben klein; für wiederholte no-match- und no-input-Ereignisse werden Handler definiert, die mit einer Übergabe an einen Menschen enden ([[conversational-ai|Conversational AI]]). [[asynchronous-apis|Webhooks]] dienen allem, was Backend-Systeme berührt, und generative Playbooks bleiben Aufgaben vorbehalten, bei denen freie Konversation hilft, abgesichert wie andere LLM-Anwendungen ([[llm-guardrails|LLM-Guardrails]] und [[red-teaming|Red Teaming]]). Gesprächsprotokolle und Analysen zeigen, wo Nutzende abbrechen oder missverstanden werden ([[conversation-analytics|Conversation Analytics]]).

### Merksatz

Dialogflow CX modelliert Gespräche als Flows aus Pages mit Intents, Formularen und Routen und ergänzt generative Playbooks für LLM-gesteuerte Aufgaben; es zielt auf große, komplexe Chat- und Sprachagenten in Google Cloud.

### Quellen

- Google Cloud (2026a). *Dialogflow CX basics*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/basics)
- Google Cloud (2026b). *Playbooks*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook)
- Google Cloud (2026c). *Dialogflow editions*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/docs/editions)
- Google Cloud (2026d). *Interact with the API*. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/quick/api)
