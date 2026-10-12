---
title_en: Asynchronous APIs
title_de: Asynchrone APIs
entity_type: Concept
aliases:
- Asynchronous request-reply
- Asynchronous response handling
- Webhooks
- Long-running operations
sources:
- https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply
- https://www.standardwebhooks.com/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Most API calls answer within about 100 ms over the same connection, but some back-end work takes seconds, minutes or longer, and the caller cannot wait for it (Azure: Asynchronous Request-Reply). Asynchronous APIs therefore acknowledge the request at once, typically with HTTP 202 Accepted and a status URL, and deliver the result later, either through polling of that URL or through a callback such as a webhook, a WebSocket or server-sent events (Azure: Asynchronous Request-Reply). Webhooks need protection against spoofing, replay and server-side request forgery (Standard Webhooks).

### How it works

```text
client ──POST /orders──────────────────► API ──► queue ──► worker ──► result store
       ◄─202 Accepted, Location: /status/42, Retry-After: 5
client ──GET /status/42──► 200 {status: "Running"}
client ──GET /status/42──► 303 See Other, Location: /orders/42
client ──GET /orders/42──► 200 {…result…}
```

#### 1. Accept quickly

The client calls the API synchronously to start the long-running operation. The API validates the request first and answers immediately with an error such as 400 if it is invalid; otherwise it hands the work to another component, for example a message queue, and returns HTTP 202 (Accepted) (Azure: Asynchronous Request-Reply).

#### 2. Tell the client where and how often to ask

The 202 response carries a Location header with the URL of a status endpoint and a Retry-After header with an estimated completion time, so that polling clients do not send too many requests (Azure: Asynchronous Request-Reply).

#### 3. Status endpoint

While work is in progress, the status endpoint answers 200 with a body describing the state: a documented status such as Pending, Running, Succeeded, Failed or Canceled, the time the operation was accepted and last updated, optionally a percentage, and a structured error in RFC 9457 format when it failed. A dedicated status endpoint avoids the ambiguity of polling the target resource and receiving 404 both for "not ready" and for invalid IDs (Azure: Asynchronous Request-Reply).

#### 4. Completion

When the work is done, the status endpoint redirects with 303 (See Other), which tells the client to fetch the result with GET regardless of the original method; 302 does not guarantee the method change, and some clients would replay the original POST. Errors are stored at the status location and returned with a matching 4xx code (Azure: Asynchronous Request-Reply).

#### 5. Retries, cancellation and clean-up

Clients can send an Idempotency-Key header with the initial request; if the back end sees a key again, it returns the existing status resource instead of queuing the work twice. This matters because a client cannot tell a lost response from a request that never arrived. A DELETE on the status resource can cancel the operation, and a retention policy, announced with an Expires header, removes old status resources and results (Azure: Asynchronous Request-Reply).

#### 6. Push instead of poll

Polling suits browser clients and environments where callback endpoints are hard to provide or firewalls block them. Where possible, the server can instead push the result: via webhooks to an open callback endpoint, via persistent connections such as WebSockets, via server-sent events when results stream in real time, or via a message broker when many results must be collected with low latency (Azure: Asynchronous Request-Reply). Webhook senders must protect themselves and their users against SSRF, spoofing and replay attacks; Standard Webhooks provides open-source guidelines and libraries for doing so (Standard Webhooks).

#### 7. Origin and variants

Long polling, where the server holds the request open until data is available or a timeout occurs, reduces latency compared with periodic polling but complicates connection management. Some services use their own variants of the pattern, for example Azure Resource Manager (Azure: Asynchronous Request-Reply).

### When to use it

- When back-end work runs for seconds, minutes or longer, so that the client cannot wait for it before getting a response (Azure: Asynchronous Request-Reply).
- For server-to-server calls in distributed systems such as microservices, where the same considerations apply (Azure: Asynchronous Request-Reply).
- When decoupling client and back end through a queue, so both can scale independently (Azure: Asynchronous Request-Reply); see also [[data-pipelines|Data Pipelines]].

### Strengths and limitations

**Strengths**
- The client gets a clear answer at once, while the back end schedules the work as capacity becomes available (Azure: Asynchronous Request-Reply).
- Polling over plain HTTP works through firewalls and with clients that cannot receive callbacks (Azure: Asynchronous Request-Reply).
- Idempotency keys make retries of the initial request safe (Azure: Asynchronous Request-Reply).

**Limitations**
- More moving parts: status endpoint, queue, result storage and retention (Azure: Asynchronous Request-Reply).
- Polling clients must be kept from sending too many requests, for example with Retry-After (Azure: Asynchronous Request-Reply).
- Implementations differ in their semantics, and legacy clients may need a facade that hides the asynchrony (Azure: Asynchronous Request-Reply).
- Webhooks open an endpoint that must be secured against spoofing and replay (Standard Webhooks).

### Comparison

| Approach | How the result arrives | Suited for |
|----------|------------------------|------------|
| Synchronous call | In the same response (Azure: Asynchronous Request-Reply) | Fast operations |
| 202 + status polling | Client polls the Location URL (Azure: Asynchronous Request-Reply) | Browsers, firewalled clients |
| Webhook | Server calls the client's endpoint (Azure: Asynchronous Request-Reply; Standard Webhooks) | Server-to-server integration |
| WebSocket / server-sent events | Pushed over a persistent connection (Azure: Asynchronous Request-Reply) | Real-time updates, streaming |
| Message broker | Results on a queue or topic (Azure: Asynchronous Request-Reply) | Many results, low latency |

### In practice

Every 202 response sets Location and Retry-After, the status body uses a fixed set of states, completion redirects with 303 and errors use the RFC 9457 problem format (Azure: Asynchronous Request-Reply). Requests that create something accept an Idempotency-Key, so that network retries do not create duplicates (Azure: Asynchronous Request-Reply). The general design rules for API contracts, versioning and errors are in [[apis|APIs]], and authentication of callers in [[api-authentication|API Authentication]].

### Key takeaway

An asynchronous API answers 202 with a status URL at once and delivers the result later by polling or push; idempotency keys, clear status states and a 303 on completion make it robust.

### Sources

- Microsoft. *Asynchronous Request-Reply pattern.* Azure Architecture Center. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply)
- Standard Webhooks. *Standard Webhooks.* [standardwebhooks.com](https://www.standardwebhooks.com/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die meisten API-Aufrufe antworten innerhalb von etwa 100 ms über dieselbe Verbindung, manche Arbeit im Backend dauert aber Sekunden, Minuten oder länger, und der Aufrufer kann nicht darauf warten (Azure: Asynchronous Request-Reply). Asynchrone APIs bestätigen die Anfrage deshalb sofort, typischerweise mit HTTP 202 Accepted und einer Status-URL, und liefern das Ergebnis später, entweder per Polling dieser URL oder über einen Rückkanal wie einen Webhook, eine WebSocket-Verbindung oder Server-Sent Events (Azure: Asynchronous Request-Reply). Webhooks brauchen Schutz vor Spoofing, Replay und Server-Side Request Forgery (Standard Webhooks).

### Funktionsweise

```text
Client ──POST /orders──────────────────► API ──► Queue ──► Worker ──► Ergebnisspeicher
       ◄─202 Accepted, Location: /status/42, Retry-After: 5
Client ──GET /status/42──► 200 {status: "Running"}
Client ──GET /status/42──► 303 See Other, Location: /orders/42
Client ──GET /orders/42──► 200 {…Ergebnis…}
```

#### 1. Schnell annehmen

Der Client ruft die API synchron auf, um die lange Operation zu starten. Die API prüft die Anfrage zuerst und antwortet bei Ungültigkeit sofort mit einem Fehler wie 400; andernfalls gibt sie die Arbeit an eine andere Komponente weiter, etwa eine Message Queue, und antwortet mit HTTP 202 (Accepted) (Azure: Asynchronous Request-Reply).

#### 2. Dem Client sagen, wo und wie oft er fragen soll

Die 202-Antwort enthält einen Location-Header mit der URL eines Status-Endpunkts und einen Retry-After-Header mit einer geschätzten Fertigstellungszeit, damit pollende Clients nicht zu viele Anfragen schicken (Azure: Asynchronous Request-Reply).

#### 3. Status-Endpunkt

Solange die Arbeit läuft, antwortet der Status-Endpunkt mit 200 und einem Body, der den Zustand beschreibt: einem dokumentierten Status wie Pending, Running, Succeeded, Failed oder Canceled, dem Zeitpunkt der Annahme und der letzten Aktualisierung, optional einem Prozentwert und bei einem Fehler einem strukturierten Fehlerobjekt im Format von RFC 9457. Ein eigener Status-Endpunkt vermeidet die Mehrdeutigkeit, die entsteht, wenn der Client die Zielressource abfragt und 404 sowohl für „noch nicht fertig“ als auch für ungültige IDs erhält (Azure: Asynchronous Request-Reply).

#### 4. Abschluss

Ist die Arbeit erledigt, leitet der Status-Endpunkt mit 303 (See Other) weiter, was den Client anweist, das Ergebnis unabhängig von der ursprünglichen Methode per GET zu holen; 302 garantiert diesen Methodenwechsel nicht, und manche Clients würden den ursprünglichen POST wiederholen. Fehler werden an der Status-Adresse gespeichert und mit einem passenden 4xx-Code zurückgegeben (Azure: Asynchronous Request-Reply).

#### 5. Wiederholungen, Abbruch und Aufräumen

Clients können mit der ersten Anfrage einen Idempotency-Key-Header schicken; sieht das Backend einen Schlüssel erneut, gibt es die vorhandene Statusressource zurück, statt die Arbeit doppelt einzureihen. Das ist wichtig, weil ein Client eine verlorene Antwort nicht von einer nie angekommenen Anfrage unterscheiden kann. Ein DELETE auf die Statusressource kann die Operation abbrechen, und eine Aufbewahrungsrichtlinie, angekündigt über einen Expires-Header, entfernt alte Statusressourcen und Ergebnisse (Azure: Asynchronous Request-Reply).

#### 6. Pushen statt pollen

Polling passt für Browser-Clients und Umgebungen, in denen Rückruf-Endpunkte schwer bereitzustellen sind oder Firewalls sie blockieren. Wo möglich, kann der Server das Ergebnis stattdessen pushen: per Webhook an einen offenen Rückruf-Endpunkt, über dauerhafte Verbindungen wie WebSockets, über Server-Sent Events, wenn Ergebnisse in Echtzeit gestreamt werden, oder über einen Message Broker, wenn viele Ergebnisse mit geringer Latenz eingesammelt werden müssen (Azure: Asynchronous Request-Reply). Webhook-Sender müssen sich und ihre Nutzer vor SSRF, Spoofing und Replay-Angriffen schützen; Standard Webhooks bietet dafür offene Richtlinien und Bibliotheken (Standard Webhooks).

#### 7. Herkunft und Varianten

Long Polling, bei dem der Server die Anfrage offen hält, bis Daten vorliegen oder ein Timeout eintritt, senkt die Latenz gegenüber periodischem Polling, verkompliziert aber die Verbindungsverwaltung. Manche Dienste nutzen eigene Varianten des Musters, etwa Azure Resource Manager (Azure: Asynchronous Request-Reply).

### Wann einsetzen

- Wenn Arbeit im Backend Sekunden, Minuten oder länger läuft, sodass der Client vor einer Antwort nicht darauf warten kann (Azure: Asynchronous Request-Reply).
- Für Aufrufe zwischen Servern in verteilten Systemen wie Microservices, für die dieselben Überlegungen gelten (Azure: Asynchronous Request-Reply).
- Wenn Client und Backend über eine Queue entkoppelt werden, sodass beide unabhängig skalieren (Azure: Asynchronous Request-Reply); siehe auch [[data-pipelines|Datenpipelines]].

### Stärken und Grenzen

**Stärken**
- Der Client bekommt sofort eine klare Antwort, während das Backend die Arbeit einplant, sobald Kapazität frei ist (Azure: Asynchronous Request-Reply).
- Polling über einfaches HTTP funktioniert durch Firewalls und mit Clients, die keine Rückrufe empfangen können (Azure: Asynchronous Request-Reply).
- Idempotency Keys machen Wiederholungen der ersten Anfrage sicher (Azure: Asynchronous Request-Reply).

**Grenzen**
- Mehr bewegliche Teile: Status-Endpunkt, Queue, Ergebnisspeicher und Aufbewahrung (Azure: Asynchronous Request-Reply).
- Pollende Clients müssen davon abgehalten werden, zu viele Anfragen zu schicken, etwa mit Retry-After (Azure: Asynchronous Request-Reply).
- Implementierungen unterscheiden sich in ihrer Semantik, und ältere Clients brauchen eventuell eine Fassade, die die Asynchronität verbirgt (Azure: Asynchronous Request-Reply).
- Webhooks öffnen einen Endpunkt, der gegen Spoofing und Replay gesichert werden muss (Standard Webhooks).

### Vergleich

| Ansatz | Wie das Ergebnis ankommt | Geeignet für |
|--------|--------------------------|--------------|
| Synchroner Aufruf | In derselben Antwort (Azure: Asynchronous Request-Reply) | Schnelle Operationen |
| 202 + Status-Polling | Client fragt die Location-URL ab (Azure: Asynchronous Request-Reply) | Browser, Clients hinter Firewalls |
| Webhook | Server ruft den Endpunkt des Clients auf (Azure: Asynchronous Request-Reply; Standard Webhooks) | Integration zwischen Servern |
| WebSocket / Server-Sent Events | Gepusht über eine dauerhafte Verbindung (Azure: Asynchronous Request-Reply) | Echtzeit-Updates, Streaming |
| Message Broker | Ergebnisse in einer Queue oder einem Topic (Azure: Asynchronous Request-Reply) | Viele Ergebnisse, geringe Latenz |

### In der Praxis

Jede 202-Antwort setzt Location und Retry-After, der Status-Body nutzt eine feste Menge von Zuständen, der Abschluss leitet mit 303 weiter, und Fehler nutzen das Problem-Format aus RFC 9457 (Azure: Asynchronous Request-Reply). Anfragen, die etwas anlegen, akzeptieren einen Idempotency Key, damit Wiederholungen nach Netzwerkfehlern keine Duplikate erzeugen (Azure: Asynchronous Request-Reply). Die allgemeinen Gestaltungsregeln für API-Verträge, Versionierung und Fehler stehen in [[apis|APIs]], die Authentifizierung der Aufrufer in [[api-authentication|API-Authentifizierung]].

### Merksatz

Eine asynchrone API antwortet sofort mit 202 und einer Status-URL und liefert das Ergebnis später per Polling oder Push; Idempotency Keys, klare Statuszustände und ein 303 beim Abschluss machen sie robust.

### Quellen

- Microsoft. *Asynchronous Request-Reply pattern.* Azure Architecture Center. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply)
- Standard Webhooks. *Standard Webhooks.* [standardwebhooks.com](https://www.standardwebhooks.com/)
