---
title_en: APIs
title_de: APIs (Programmierschnittstellen)
entity_type: Concept
sources:
- https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- https://www.rfc-editor.org/rfc/rfc9110.html
- https://spec.openapis.org/oas/latest.html
- https://www.jsonrpc.org/specification
- https://spec.graphql.org/October2021/
- https://grpc.io/docs/what-is-grpc/introduction/
- https://cloud.google.com/apis/design
- https://www.rfc-editor.org/rfc/rfc9457.html
- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

An API (application programming interface) is a defined contract through which software components communicate: which operations exist, which inputs they take, what they return and how errors are reported. Web APIs mostly follow one of a few styles: REST over HTTP, which treats data as resources with a uniform interface (Fielding, 2000), remote procedure calls such as gRPC (gRPC docs) or JSON-RPC (JSON-RPC 2.0 specification), or query languages such as GraphQL (GraphQL specification). Good APIs are consistent, documented in a machine-readable form (OpenAPI Specification), secured per object and per user (OWASP API Top 10 (2023)) and evolve without breaking existing clients (Azure REST API guidelines).

### How it works

#### 1. API as a contract

An API separates what a component offers from how it is implemented. The client only needs to know the interface; the implementation behind it can change as long as the contract stays the same. Names of public API elements should reflect how they are used rather than how they are implemented ([[clean-code|Clean Code]]).

#### 2. REST

REST is an architectural style defined by constraints: client and server are separated; communication is stateless, so each request contains all information needed to understand it; responses are labelled as cacheable or not; components share a uniform interface, with resources identified by URIs, manipulated through representations and linked by hypermedia; the system can be layered; and code-on-demand is optional (Fielding, 2000). The uniform interface decouples implementations from services, at the cost of efficiency, because data is transferred in a standardised rather than application-specific form (Fielding, 2000).

```http
GET /contracts/42 HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "party": "Example GmbH", "notice_period_months": 3}
```

#### 3. HTTP semantics

- **Safe methods** are essentially read-only: GET, HEAD, OPTIONS and TRACE.
- **Idempotent methods** have the same intended effect whether sent once or several times: PUT, DELETE and the safe methods; such requests can be repeated automatically after a network failure (RFC 9110).
- **Status codes** are grouped by their first digit: 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error (RFC 9110).

POST is neither safe nor idempotent, so retrying it can create duplicates; APIs often add idempotency keys for that reason.

#### 4. Errors

Problem details carry machine-readable error information in the response body in a standard format, so that each API does not need its own error format; the status code tells generic software the general meaning, while the details explain the specific reason (RFC 9457).

```json
{"type": "https://example.org/problems/insufficient-credit",
 "title": "Insufficient credit", "status": 403,
 "detail": "The balance is 30, but the transfer costs 50."}
```

#### 5. Other API styles

- **RPC:** the client calls a remote method as if it were local. gRPC defines services with methods, parameters and return types, by default with Protocol Buffers as interface definition language and message format (gRPC docs); JSON-RPC is a light, stateless and transport-agnostic RPC protocol with JSON messages (JSON-RPC 2.0 specification), used for example by [[mcp-and-related-protocols|MCP and Related Protocols]].
- **GraphQL:** a strongly typed query language in which the client specifies at field level which data it needs, instead of the server fixing the shape of the response per endpoint; the type system can be queried itself (GraphQL specification).
- **Query endpoints for data:** knowledge graphs offer SPARQL endpoints, a query API over HTTP ([[sparql|SPARQL]]).

#### 6. Description and design guidelines

The OpenAPI Specification describes HTTP APIs in a language-agnostic, machine-readable way, so that humans and tools can understand a service without reading its code or traffic; documentation, server and client code and tests can be generated from it (OpenAPI Specification). Google's API design guide, used internally since 2014, recommends resource-oriented design with standard methods (Get, List, Create, Update, Delete) and custom methods (Google API design guide).

#### 7. Versioning and compatibility

When a service changes, running clients must not break, and clients must be able to adopt a new version without code changes. Breaking changes include adding required fields, removing required fields or changing whether a field is optional (Azure REST API guidelines).

#### Origin and variants

REST was described in 2000 as an architectural style for distributed hypermedia systems, optimised for the common case of the web (Fielding, 2000); HTTP semantics are defined in RFC 9110 (RFC 9110). JSON-RPC 2.0 dates from 2010 (JSON-RPC 2.0 specification), GraphQL is published in specification editions such as October 2021 (GraphQL specification), and gRPC builds on Protocol Buffers (gRPC docs). Large providers publish their own design guidelines (Google API design guide; Azure REST API guidelines).

### When to use it

- REST over HTTP for resource-oriented public web APIs that should work with generic tools, caches and proxies (Fielding, 2000).
- gRPC for communication between services with strictly defined interfaces (gRPC docs).
- GraphQL when clients need flexible, field-level selection of related data (GraphQL specification).
- JSON-RPC for simple method calls, also over non-HTTP transports (JSON-RPC 2.0 specification).

### Strengths and limitations

**Strengths**
- Decouples components so that implementations can change independently (Fielding, 2000).
- Machine-readable descriptions enable documentation, client generation and contract tests (OpenAPI Specification).
- Standard HTTP semantics let generic software such as caches handle requests correctly (RFC 9110).

**Limitations**
- A uniform interface is not optimal for every kind of interaction (Fielding, 2000).
- APIs are an attack surface: broken object-level authorisation, where users access objects of others through IDs, tops the list of API security risks, followed by broken authentication (OWASP API Top 10 (2023)).
- Once published, an API is hard to change without breaking clients (Azure REST API guidelines).

### Comparison

| Style | How it differs | Suited for |
|----------|----------------|------------|
| REST | Resources, uniform interface, stateless HTTP (Fielding, 2000) | Public web APIs |
| gRPC | Remote methods with Protocol Buffers (gRPC docs) | Internal, high-performance services |
| GraphQL | Client selects fields via a typed schema (GraphQL specification) | Flexible data needs of front ends |
| JSON-RPC | Lightweight method calls, transport-agnostic (JSON-RPC 2.0 specification) | Simple RPC, tool protocols |

### In practice

APIs are designed contract-first with an OpenAPI description, checked in reviews like code and tested against the contract ([[clean-code|Clean Code]]). Every endpoint that receives an object ID checks whether the caller may access that object, and tokens are validated (OWASP API Top 10 (2023)). API services are often deployed as containers and scaled on clusters ([[docker|Docker]]; [[kubernetes|Kubernetes]]); Python frameworks are a common way to build them ([[python|Python]]). LLM agents use APIs as tools, so tool descriptions, permissions and rate limits matter ([[agentic-ai|Agentic AI]]; [[harness-engineering|Harness Engineering]]), and the APIs of model providers are billed per token ([[llm-cost-optimization|LLM Cost Optimization]]).

### Key takeaway

An API is a contract: choose the style that fits, describe it machine-readably, use HTTP semantics correctly, check authorisation for every object and change it only in backwards-compatible ways.

### Sources

- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*, chapter 5: Representational State Transfer (REST). Dissertation, University of California, Irvine. [ics.uci.edu](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics.* RFC 9110, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)
- OpenAPI Initiative. *OpenAPI Specification.* spec.openapis.org. [spec.openapis.org](https://spec.openapis.org/oas/latest.html)
- JSON-RPC Working Group (2010). *JSON-RPC 2.0 Specification.* jsonrpc.org. [jsonrpc.org](https://www.jsonrpc.org/specification)
- GraphQL Foundation (2021). *GraphQL Specification, October 2021 Edition.* spec.graphql.org. [spec.graphql.org](https://spec.graphql.org/October2021/)
- gRPC Authors. *Introduction to gRPC.* grpc.io. [grpc.io](https://grpc.io/docs/what-is-grpc/introduction/)
- Google. *API design guide.* Google Cloud documentation. [cloud.google.com](https://cloud.google.com/apis/design)
- Nottingham, M., Wilde, E. & Dalal, S. (2023). *Problem Details for HTTP APIs.* RFC 9457, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9457.html)
- OWASP (2023). *OWASP Top 10 API Security Risks – 2023.* OWASP API Security Project. [owasp.org](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- Microsoft. *Microsoft Azure REST API Guidelines.* GitHub repository microsoft/api-guidelines. [github.com](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine API (Application Programming Interface, Programmierschnittstelle) ist ein festgelegter Vertrag, über den Softwarekomponenten miteinander kommunizieren: welche Operationen es gibt, welche Eingaben sie erwarten, was sie zurückgeben und wie Fehler gemeldet werden. Web-APIs folgen meist einem von wenigen Stilen: REST über HTTP, das Daten als Ressourcen mit einheitlicher Schnittstelle behandelt (Fielding, 2000), entfernte Prozeduraufrufe wie gRPC (gRPC docs) oder JSON-RPC (JSON-RPC 2.0 specification) oder Abfragesprachen wie GraphQL (GraphQL specification). Gute APIs sind einheitlich, maschinenlesbar beschrieben (OpenAPI Specification), pro Objekt und Nutzer abgesichert (OWASP API Top 10 (2023)) und entwickeln sich weiter, ohne bestehende Clients zu brechen (Azure REST API guidelines).

### Funktionsweise

#### 1. Die API als Vertrag

Eine API trennt, was eine Komponente anbietet, davon, wie sie umgesetzt ist. Der Client muss nur die Schnittstelle kennen; die Implementierung dahinter kann sich ändern, solange der Vertrag gleich bleibt. Namen öffentlicher API-Elemente sollten beschreiben, wie sie verwendet werden, nicht wie sie umgesetzt sind ([[clean-code|Clean Code]]).

#### 2. REST

REST ist ein Architekturstil, der durch Randbedingungen bestimmt ist: Client und Server sind getrennt; die Kommunikation ist zustandslos, sodass jede Anfrage alle Informationen enthält, die zu ihrem Verständnis nötig sind; Antworten sind als zwischenspeicherbar oder nicht gekennzeichnet; Komponenten teilen eine einheitliche Schnittstelle, bei der Ressourcen über URIs identifiziert, über Repräsentationen verändert und durch Hypermedia verknüpft werden; das System kann geschichtet sein; und Code-on-Demand ist optional (Fielding, 2000). Die einheitliche Schnittstelle entkoppelt Implementierungen von Diensten, kostet aber Effizienz, weil Daten in standardisierter statt anwendungsspezifischer Form übertragen werden (Fielding, 2000).

```http
GET /contracts/42 HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "party": "Example GmbH", "notice_period_months": 3}
```

#### 3. HTTP-Semantik

- **Sichere Methoden** sind im Wesentlichen nur lesend: GET, HEAD, OPTIONS und TRACE.
- **Idempotente Methoden** haben dieselbe beabsichtigte Wirkung, ob sie einmal oder mehrfach gesendet werden: PUT, DELETE und die sicheren Methoden; solche Anfragen lassen sich nach einem Netzwerkfehler automatisch wiederholen (RFC 9110).
- **Statuscodes** sind nach ihrer ersten Ziffer gruppiert: 1xx Information, 2xx Erfolg, 3xx Umleitung, 4xx Fehler des Clients, 5xx Fehler des Servers (RFC 9110).

POST ist weder sicher noch idempotent, sodass eine Wiederholung Duplikate erzeugen kann; APIs ergänzen deshalb oft Idempotenzschlüssel.

#### 4. Fehler

Problem Details transportieren maschinenlesbare Fehlerinformationen im Antwortkörper in einem Standardformat, sodass nicht jede API ein eigenes Fehlerformat braucht; der Statuscode teilt allgemeiner Software die grundsätzliche Bedeutung mit, die Details erklären den konkreten Grund (RFC 9457).

```json
{"type": "https://example.org/problems/insufficient-credit",
 "title": "Insufficient credit", "status": 403,
 "detail": "The balance is 30, but the transfer costs 50."}
```

#### 5. Weitere API-Stile

- **RPC:** Der Client ruft eine entfernte Methode auf, als wäre sie lokal. gRPC definiert Dienste mit Methoden, Parametern und Rückgabetypen, standardmäßig mit Protocol Buffers als Schnittstellenbeschreibungssprache und Nachrichtenformat (gRPC docs); JSON-RPC ist ein schlankes, zustandsloses und transportunabhängiges RPC-Protokoll mit JSON-Nachrichten (JSON-RPC 2.0 specification), das etwa [[mcp-and-related-protocols|MCP und ähnliche Protokolle]] nutzen.
- **GraphQL:** eine stark typisierte Abfragesprache, in der der Client auf Feldebene festlegt, welche Daten er braucht, statt dass der Server die Form der Antwort pro Endpunkt bestimmt; das Typsystem lässt sich selbst abfragen (GraphQL specification).
- **Abfrage-Endpunkte für Daten:** Wissensgraphen bieten SPARQL-Endpunkte, eine Abfrage-API über HTTP ([[sparql|SPARQL]]).

#### 6. Beschreibung und Designrichtlinien

Die OpenAPI Specification beschreibt HTTP-APIs sprachunabhängig und maschinenlesbar, sodass Menschen und Werkzeuge einen Dienst verstehen, ohne seinen Code oder Datenverkehr zu lesen; daraus lassen sich Dokumentation, Server- und Client-Code und Tests erzeugen (OpenAPI Specification). Googles API-Designleitfaden, intern seit 2014 im Einsatz, empfiehlt ressourcenorientiertes Design mit Standardmethoden (Get, List, Create, Update, Delete) und benutzerdefinierten Methoden (Google API design guide).

#### 7. Versionierung und Kompatibilität

Ändert sich ein Dienst, dürfen laufende Clients nicht brechen, und Clients müssen eine neue Version ohne Codeänderungen übernehmen können. Inkompatible Änderungen sind etwa neue Pflichtfelder, das Entfernen von Pflichtfeldern oder das Ändern, ob ein Feld optional ist (Azure REST API guidelines).

#### Ursprung und Varianten

REST wurde im Jahr 2000 als Architekturstil für verteilte Hypermedia-Systeme beschrieben, optimiert für den häufigsten Fall, das Web (Fielding, 2000); die HTTP-Semantik ist in RFC 9110 festgelegt (RFC 9110). JSON-RPC 2.0 stammt aus dem Jahr 2010 (JSON-RPC 2.0 specification), GraphQL erscheint in Spezifikationsausgaben wie der vom Oktober 2021 (GraphQL specification), und gRPC baut auf Protocol Buffers auf (gRPC docs). Große Anbieter veröffentlichen eigene Designrichtlinien (Google API design guide; Azure REST API guidelines).

### Wann einsetzen

- REST über HTTP für ressourcenorientierte öffentliche Web-APIs, die mit allgemeinen Werkzeugen, Caches und Proxys funktionieren sollen (Fielding, 2000).
- gRPC für die Kommunikation zwischen Diensten mit streng festgelegten Schnittstellen (gRPC docs).
- GraphQL, wenn Clients zusammenhängende Daten flexibel und feldgenau auswählen müssen (GraphQL specification).
- JSON-RPC für einfache Methodenaufrufe, auch über Transporte jenseits von HTTP (JSON-RPC 2.0 specification).

### Stärken und Grenzen

**Stärken**
- Entkoppelt Komponenten, sodass sich Implementierungen unabhängig ändern können (Fielding, 2000).
- Maschinenlesbare Beschreibungen ermöglichen Dokumentation, Erzeugung von Clients und Vertragstests (OpenAPI Specification).
- Standardisierte HTTP-Semantik lässt allgemeine Software wie Caches Anfragen richtig behandeln (RFC 9110).

**Einschränkungen**
- Eine einheitliche Schnittstelle ist nicht für jede Art von Interaktion optimal (Fielding, 2000).
- APIs sind eine Angriffsfläche: Fehlerhafte Autorisierung auf Objektebene, bei der Nutzende über IDs auf fremde Objekte zugreifen, führt die Liste der API-Sicherheitsrisiken an, gefolgt von fehlerhafter Authentifizierung (OWASP API Top 10 (2023)).
- Eine veröffentlichte API lässt sich nur schwer ändern, ohne Clients zu brechen (Azure REST API guidelines).

### Vergleich

| Stil | Unterschiede | Geeignet für |
|----------|----------------|------------|
| REST | Ressourcen, einheitliche Schnittstelle, zustandsloses HTTP (Fielding, 2000) | Öffentliche Web-APIs |
| gRPC | Entfernte Methoden mit Protocol Buffers (gRPC docs) | Interne, leistungsstarke Dienste |
| GraphQL | Client wählt Felder über ein typisiertes Schema (GraphQL specification) | Flexibler Datenbedarf von Frontends |
| JSON-RPC | Schlanke Methodenaufrufe, transportunabhängig (JSON-RPC 2.0 specification) | Einfaches RPC, Werkzeugprotokolle |

### In der Praxis

APIs werden vertragsorientiert mit einer OpenAPI-Beschreibung entworfen, in Reviews wie Code geprüft und gegen den Vertrag getestet ([[clean-code|Clean Code]]). Jeder Endpunkt, der eine Objekt-ID erhält, prüft, ob der Aufrufer auf dieses Objekt zugreifen darf, und Token werden validiert (OWASP API Top 10 (2023)). API-Dienste werden oft als Container ausgeliefert und auf Clustern skaliert ([[docker|Docker]]; [[kubernetes|Kubernetes]]); Python-Frameworks sind ein verbreiteter Weg, sie zu bauen ([[python|Python]]). LLM-Agenten nutzen APIs als Werkzeuge, daher zählen Werkzeugbeschreibungen, Berechtigungen und Ratenbegrenzungen ([[agentic-ai|Agentic AI]]; [[harness-engineering|Harness Engineering]]), und die APIs von Modellanbietern werden pro Token abgerechnet ([[llm-cost-optimization|LLM-Kostenoptimierung]]).

### Merksatz

Eine API ist ein Vertrag: den passenden Stil wählen, ihn maschinenlesbar beschreiben, HTTP-Semantik richtig nutzen, für jedes Objekt die Berechtigung prüfen und nur abwärtskompatibel ändern.

### Quellen

- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*, chapter 5: Representational State Transfer (REST). Dissertation, University of California, Irvine. [ics.uci.edu](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics.* RFC 9110, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)
- OpenAPI Initiative. *OpenAPI Specification.* spec.openapis.org. [spec.openapis.org](https://spec.openapis.org/oas/latest.html)
- JSON-RPC Working Group (2010). *JSON-RPC 2.0 Specification.* jsonrpc.org. [jsonrpc.org](https://www.jsonrpc.org/specification)
- GraphQL Foundation (2021). *GraphQL Specification, October 2021 Edition.* spec.graphql.org. [spec.graphql.org](https://spec.graphql.org/October2021/)
- gRPC Authors. *Introduction to gRPC.* grpc.io. [grpc.io](https://grpc.io/docs/what-is-grpc/introduction/)
- Google. *API design guide.* Google Cloud documentation. [cloud.google.com](https://cloud.google.com/apis/design)
- Nottingham, M., Wilde, E. & Dalal, S. (2023). *Problem Details for HTTP APIs.* RFC 9457, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9457.html)
- OWASP (2023). *OWASP Top 10 API Security Risks – 2023.* OWASP API Security Project. [owasp.org](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- Microsoft. *Microsoft Azure REST API Guidelines.* GitHub repository microsoft/api-guidelines. [github.com](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md)
