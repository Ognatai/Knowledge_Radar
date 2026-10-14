---
title_en: REST
title_de: REST
entity_type: Concept
aliases:
- REST
- Representational State Transfer
- RESTful API
sources:
- https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- https://ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm
- https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven
- https://www.rfc-editor.org/rfc/rfc9110.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

REST (Representational State Transfer) is an architectural style for distributed hypermedia systems that Roy Fielding defined in his 2000 dissertation to describe the design rationale of the web (Fielding, 2000). It is a set of constraints: client-server separation, stateless communication, cacheable responses, a uniform interface, a layered system and optional code-on-demand. Its key abstraction is the resource, anything that can be named, which clients manipulate by transferring representations of its state (Fielding, 2000). In everyday use, "REST API" usually means a resource-oriented HTTP API with URLs for resources and HTTP methods for actions ([[apis|APIs]]); Fielding himself objected to calling any HTTP-based interface REST unless it is hypertext-driven (Fielding, 2008).

### How it works

```text
client                                   server (or cache / proxy in between: layered system)
  │ GET /orders/42      Accept: application/json
  │────────────────────────────────────────────►  resource "order 42" → representation
  │◄────────────────────────────────────────────  200 OK, Cache-Control: max-age=60
  │   {"id": 42, "status": "open",
  │    "links": {"cancel": "/orders/42/cancellation"}}   ← hypermedia: next possible actions
  │ every request self-contained (stateless) – session state stays on the client
```

#### 1. Deriving REST from constraints

Fielding (2000) derives REST by starting from a style with no constraints and adding them one by one, each chosen for the properties it induces. Client-server separates user interface from data storage, so components can evolve independently across organisations. Statelessness requires each request to contain all information needed to understand it, with session state kept on the client; this improves visibility, reliability and scalability, at the cost of repeating data in every request (Fielding, 2000).

#### 2. Cache, layers and code-on-demand

Responses must be labelled, implicitly or explicitly, as cacheable or not, so that caches can reuse them and eliminate some interactions, at the risk of stale data (Fielding, 2000). A layered system lets each component see only the next layer, which allows proxies, shared caches, load balancers and firewalls but adds latency. Code-on-demand, downloading scripts to extend clients, is the only optional constraint (Fielding, 2000).

#### 3. The uniform interface

The central feature that distinguishes REST from other network-based styles is the uniform interface between components (Fielding, 2000). It consists of four constraints: identification of resources; manipulation of resources through representations; self-descriptive messages; and hypermedia as the engine of application state (HATEOAS). The trade-off is efficiency: information is transferred in a standardised form rather than one tailored to an application, which suits large-grain hypermedia transfer but not every kind of interaction (Fielding, 2000).

#### 4. Resources and representations

Any information that can be named can be a resource, such as a document, a collection, a person or "today's weather in Los Angeles"; a resource is a mapping to a set of values over time, not one particular value (Fielding, 2000). Components act on resources by transferring representations, a sequence of bytes plus metadata describing them, which may capture the current or intended state of the resource. Because clients reference the concept rather than one representation, content negotiation and changes of format do not break links (Fielding, 2000).

#### Origin and variants

Fielding developed REST as an architectural model to guide the web's protocol standards, HTTP, URI and HTML, in IETF and [[w3c|W3C]] work, and described it in chapter 5 of his dissertation at UC Irvine in 2000 (Fielding, 2000). HTTP's standardised methods are not resource-specific because uniform interfaces provide better visibility and reuse, and RFC 9110 cites REST for this (Fielding et al., 2022). In 2008, Fielding stressed that a REST API must not define fixed resource names or hierarchies and should be entered with no prior knowledge beyond the initial URI and standardised media types (Fielding, 2008). Most practical "REST APIs" follow the resource-and-method part but not hypermedia; alternatives include RPC styles such as gRPC and query languages such as GraphQL ([[apis|APIs]]).

### When to use it

- Public and partner APIs that many independent clients use over the internet, where caching, intermediaries and independent evolution matter (Fielding, 2000).
- CRUD-like access to resources, mapped to HTTP methods with defined safe and idempotent semantics (Fielding et al., 2022).
- Less suited to chatty, fine-grained or streaming interactions, for which the uniform interface is not optimal (Fielding, 2000; [[asynchronous-apis|asynchronous APIs]]).

### Strengths and limitations

**Strengths**
- Statelessness and caching support scalability and reliability (Fielding, 2000).
- Uniform interface decouples implementations from services and supports independent evolution (Fielding, 2000).
- Works with existing web infrastructure: proxies, caches, firewalls.

**Limitations**
- Repeating context in every request adds overhead (Fielding, 2000).
- Standardised representations are less efficient than application-specific formats (Fielding, 2000).
- Layers add latency (Fielding, 2000).
- "REST" is used loosely; many APIs called REST ignore hypermedia and couple clients to fixed URL structures (Fielding, 2008).

### Comparison

| Constraint | Property gained | Cost |
|---|---|---|
| Client-server | independent evolution, portability | — |
| Stateless | visibility, reliability, scalability | repeated data per request |
| Cache | efficiency, lower latency | stale data |
| Uniform interface | simplicity, decoupling | less efficient than custom formats |
| Layered system | intermediaries, security boundaries | added latency |
| Code-on-demand (optional) | extensible clients | less visibility |

Source: Fielding (2000).

### In practice

Model nouns as resources and use HTTP methods for what they mean: GET for safe reads, PUT and DELETE as idempotent operations that clients may retry, POST for other processing (Fielding et al., 2022; [[http|HTTP]]). Keep requests stateless, so that any server instance can handle them, and set cache headers deliberately. Describe the API in a machine-readable format and handle errors and authentication consistently ([[apis|APIs]], [[api-authentication|API authentication]]). Use links in responses where clients should discover next steps instead of building URLs themselves (Fielding, 2008).

### Key takeaway

REST is a set of architectural constraints, stateless client-server interaction, caching, layers and above all a uniform interface over resources and their representations, that explains why the web scales; most "REST APIs" adopt its resource-and-method part on top of HTTP.

### Sources

- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*, chapters 5–6. Dissertation, University of California, Irvine. [ics.uci.edu](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm), [ch. 6](https://ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm)
- Fielding, R. T. (2008). *REST APIs must be hypertext-driven*. Blog post, 20 October 2008. [roy.gbiv.com](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)
- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics*. RFC 9110, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

REST (Representational State Transfer) ist ein Architekturstil für verteilte Hypermedia-Systeme, den Roy Fielding in seiner Dissertation von 2000 definierte, um die Entwurfsprinzipien des Webs zu beschreiben (Fielding, 2000). Er besteht aus einer Reihe von Einschränkungen: Trennung von Client und Server, zustandslose Kommunikation, cachebare Antworten, eine einheitliche Schnittstelle, ein geschichtetes System und optionaler Code-on-Demand. Seine zentrale Abstraktion ist die Ressource, alles, was sich benennen lässt, die Clients bearbeiten, indem sie Repräsentationen ihres Zustands übertragen (Fielding, 2000). Im Alltag meint „REST-API“ meist eine ressourcenorientierte HTTP-API mit URLs für Ressourcen und HTTP-Methoden für Aktionen ([[apis|APIs]]); Fielding selbst widersprach, jede HTTP-basierte Schnittstelle REST zu nennen, sofern sie nicht hypertextgesteuert ist (Fielding, 2008).

### Funktionsweise

```text
Client                                   Server (oder Cache / Proxy dazwischen: geschichtetes System)
  │ GET /orders/42      Accept: application/json
  │────────────────────────────────────────────►  Ressource "Bestellung 42" → Repräsentation
  │◄────────────────────────────────────────────  200 OK, Cache-Control: max-age=60
  │   {"id": 42, "status": "open",
  │    "links": {"cancel": "/orders/42/cancellation"}}   ← Hypermedia: nächste mögliche Aktionen
  │ jede Anfrage in sich vollständig (zustandslos) – Sitzungszustand bleibt beim Client
```

#### 1. REST aus Einschränkungen herleiten

Fielding (2000) leitet REST her, indem er von einem Stil ohne Einschränkungen ausgeht und diese nacheinander hinzufügt, jede gewählt wegen der Eigenschaften, die sie bewirkt. Client-Server trennt Benutzeroberfläche und Datenhaltung, sodass sich Komponenten über Organisationsgrenzen hinweg unabhängig entwickeln können. Zustandslosigkeit verlangt, dass jede Anfrage alle zu ihrem Verständnis nötigen Informationen enthält und der Sitzungszustand beim Client bleibt; das verbessert Sichtbarkeit, Zuverlässigkeit und Skalierbarkeit, kostet aber die Wiederholung von Daten in jeder Anfrage (Fielding, 2000).

#### 2. Cache, Schichten und Code-on-Demand

Antworten müssen implizit oder explizit als cachebar oder nicht cachebar gekennzeichnet sein, damit Caches sie wiederverwenden und manche Interaktionen ganz einsparen können, mit dem Risiko veralteter Daten (Fielding, 2000). Ein geschichtetes System lässt jede Komponente nur die nächste Schicht sehen, was Proxys, gemeinsame Caches, Load Balancer und Firewalls ermöglicht, aber Latenz hinzufügt. Code-on-Demand, das Herunterladen von Skripten zur Erweiterung von Clients, ist die einzige optionale Einschränkung (Fielding, 2000).

#### 3. Die einheitliche Schnittstelle

Das zentrale Merkmal, das REST von anderen netzwerkbasierten Stilen unterscheidet, ist die einheitliche Schnittstelle zwischen Komponenten (Fielding, 2000). Sie besteht aus vier Einschränkungen: Identifikation von Ressourcen; Bearbeitung von Ressourcen über Repräsentationen; selbstbeschreibende Nachrichten; und Hypermedia als Motor des Anwendungszustands (HATEOAS). Der Preis ist Effizienz: Informationen werden in standardisierter Form übertragen statt in einer auf die Anwendung zugeschnittenen, was zu grobkörnigem Hypermedia-Transfer passt, aber nicht zu jeder Art von Interaktion (Fielding, 2000).

#### 4. Ressourcen und Repräsentationen

Jede Information, die sich benennen lässt, kann eine Ressource sein, etwa ein Dokument, eine Sammlung, eine Person oder „das heutige Wetter in Los Angeles“; eine Ressource ist eine zeitlich veränderliche Zuordnung zu einer Menge von Werten, nicht ein bestimmter Wert (Fielding, 2000). Komponenten wirken auf Ressourcen ein, indem sie Repräsentationen übertragen, eine Bytefolge plus beschreibende Metadaten, die den aktuellen oder gewünschten Zustand der Ressource erfassen kann. Da Clients auf das Konzept statt auf eine bestimmte Repräsentation verweisen, brechen Content Negotiation und Formatwechsel keine Links (Fielding, 2000).

#### Herkunft und Varianten

Fielding entwickelte REST als Architekturmodell, das die Protokollstandards des Webs, HTTP, URI und HTML, in der Arbeit von IETF und [[w3c|W3C]] leiten sollte, und beschrieb es im fünften Kapitel seiner Dissertation an der UC Irvine im Jahr 2000 (Fielding, 2000). Die standardisierten HTTP-Methoden sind nicht ressourcenspezifisch, weil einheitliche Schnittstellen bessere Sichtbarkeit und Wiederverwendung bieten; RFC 9110 verweist dafür auf REST (Fielding et al., 2022). 2008 betonte Fielding, dass eine REST-API keine festen Ressourcennamen oder Hierarchien definieren darf und ohne Vorwissen außer der Einstiegs-URI und standardisierten Medientypen nutzbar sein sollte (Fielding, 2008). Die meisten praktischen „REST-APIs“ übernehmen den Teil mit Ressourcen und Methoden, nicht aber Hypermedia; Alternativen sind RPC-Stile wie gRPC und Abfragesprachen wie GraphQL ([[apis|APIs]]).

### Wann einsetzen

- Öffentliche und Partner-APIs, die viele unabhängige Clients über das Internet nutzen, wo Caching, Zwischenstationen und unabhängige Weiterentwicklung zählen (Fielding, 2000).
- CRUD-artiger Zugriff auf Ressourcen, abgebildet auf HTTP-Methoden mit definierter sicherer und idempotenter Semantik (Fielding et al., 2022).
- Weniger geeignet für gesprächige, feingranulare oder streamende Interaktionen, für die die einheitliche Schnittstelle nicht optimal ist (Fielding, 2000; [[asynchronous-apis|asynchrone APIs]]).

### Stärken und Grenzen

**Stärken**
- Zustandslosigkeit und Caching fördern Skalierbarkeit und Zuverlässigkeit (Fielding, 2000).
- Die einheitliche Schnittstelle entkoppelt Implementierungen von Diensten und unterstützt unabhängige Weiterentwicklung (Fielding, 2000).
- Funktioniert mit vorhandener Web-Infrastruktur: Proxys, Caches, Firewalls.

**Grenzen**
- Kontext in jeder Anfrage zu wiederholen, erzeugt Overhead (Fielding, 2000).
- Standardisierte Repräsentationen sind weniger effizient als anwendungsspezifische Formate (Fielding, 2000).
- Schichten erhöhen die Latenz (Fielding, 2000).
- „REST“ wird unscharf verwendet; viele APIs, die REST heißen, ignorieren Hypermedia und binden Clients an feste URL-Strukturen (Fielding, 2008).

### Vergleich

| Einschränkung | Gewonnene Eigenschaft | Kosten |
|---|---|---|
| Client-Server | unabhängige Weiterentwicklung, Portabilität | — |
| Zustandslos | Sichtbarkeit, Zuverlässigkeit, Skalierbarkeit | wiederholte Daten je Anfrage |
| Cache | Effizienz, geringere Latenz | veraltete Daten |
| Einheitliche Schnittstelle | Einfachheit, Entkopplung | weniger effizient als eigene Formate |
| Geschichtetes System | Zwischenstationen, Sicherheitsgrenzen | zusätzliche Latenz |
| Code-on-Demand (optional) | erweiterbare Clients | weniger Sichtbarkeit |

Quelle: Fielding (2000).

### In der Praxis

Substantive werden als Ressourcen modelliert und HTTP-Methoden in ihrer Bedeutung genutzt: GET für sichere Lesezugriffe, PUT und DELETE als idempotente Operationen, die Clients wiederholen dürfen, POST für sonstige Verarbeitung (Fielding et al., 2022; [[http|HTTP]]). Anfragen bleiben zustandslos, damit jede Serverinstanz sie bearbeiten kann, und Cache-Header werden bewusst gesetzt. Die API wird in einem maschinenlesbaren Format beschrieben, Fehler und Authentifizierung werden einheitlich behandelt ([[apis|APIs]], [[api-authentication|API-Authentifizierung]]). Wo Clients nächste Schritte entdecken sollen, statt URLs selbst zusammenzusetzen, gehören Links in die Antworten (Fielding, 2008).

### Merksatz

REST ist eine Reihe von Architektureinschränkungen, zustandslose Client-Server-Interaktion, Caching, Schichten und vor allem eine einheitliche Schnittstelle über Ressourcen und ihre Repräsentationen, die erklärt, warum das Web skaliert; die meisten „REST-APIs“ übernehmen davon den Teil mit Ressourcen und Methoden auf Basis von HTTP.

### Quellen

- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*, Kapitel 5–6. Dissertation, University of California, Irvine. [ics.uci.edu](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm), [ch. 6](https://ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm)
- Fielding, R. T. (2008). *REST APIs must be hypertext-driven*. Blogbeitrag, 20. Oktober 2008. [roy.gbiv.com](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)
- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics*. RFC 9110, IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)
