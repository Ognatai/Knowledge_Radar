---
title_en: HTTP
title_de: HTTP
entity_type: Technology
aliases:
- HTTP
- Hypertext Transfer Protocol
- HTTPS
sources:
- https://www.rfc-editor.org/rfc/rfc9110.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The Hypertext Transfer Protocol (HTTP) is a family of stateless, application-level request/response protocols with a generic interface, extensible semantics and self-descriptive messages; it has been the web's primary information transfer protocol since 1990 (Fielding et al., 2022). A client sends a request with a method such as GET or POST to a resource identified by a URI, and the server answers with a three-digit status code, header fields and usually a representation of the resource. Since 2022, the shared semantics are defined in RFC 9110, separately from the wire formats of HTTP/1.1, HTTP/2 and HTTP/3, which coexist because each has its own benefits (Fielding et al., 2022). HTTP is the basis of web pages and of most web [[apis|APIs]], including [[rest|REST]] APIs.

### Core concepts

```text
request                                         response
GET /orders/42 HTTP/1.1                         HTTP/1.1 200 OK
Host: api.example.com                           Content-Type: application/json
Accept: application/json        ─────────►      ETag: "v7"
If-None-Match: "v6"                             Cache-Control: max-age=60
                                ◄─────────
                                                {"id": 42, "status": "open"}
method + target URI + header fields (+ content)  status code + header fields (+ content)
```

#### 1. Resources, representations and messages

The target of a request is a resource, usually identified by a URI; HTTP does not limit what a resource is, it only defines an interface to interact with it (Fielding et al., 2022). What travels is a representation, information that reflects a past, current or desired state of the resource, consisting of representation metadata and data. Each message is a request or a response: the client states its intention, the server interprets it for the target resource and replies; the client decides what to do next from the status code and content (Fielding et al., 2022).

#### 2. Methods and their properties

The method is the primary source of request semantics (Fielding et al., 2022). GET transfers a current representation, HEAD does the same without content, POST performs resource-specific processing on the request content, PUT replaces all current representations, DELETE removes them, and CONNECT, OPTIONS and TRACE serve tunnelling, discovery and loop-back tests. GET, HEAD, OPTIONS and TRACE are safe, essentially read-only; PUT, DELETE and the safe methods are idempotent, so a client may repeat them after a connection failure, while non-idempotent requests such as POST should not be retried automatically (Fielding et al., 2022). All general-purpose servers must support GET and HEAD.

#### 3. Status codes

Status codes are three-digit numbers from 100 to 599 whose first digit gives the class: 1xx informational, 2xx successful, 3xx redirection, 4xx client error, 5xx server error (Fielding et al., 2022). Clients must understand the class even of unknown codes and treat them like x00 of that class. For example, 405 means the method is not allowed for the resource, and 501 that it is not implemented at all.

#### 4. Content negotiation and conditional requests

Content negotiation selects among representations in different formats, languages or encodings, for example proactively by the server from the client's stated preferences (Fielding et al., 2022). Conditional requests carry preconditions that compare validators of a previous representation with the current one: a conditional GET is the most efficient way to update caches, and conditional PUT or DELETE prevent the "lost update" problem when clients work in parallel (Fielding et al., 2022).

#### Origin and variants

HTTP began in 1990 as a simple mechanism with a single method, GET, and grew to carry arbitrary media types and pass through intermediaries (HTTP/0.9 and 1.0) (Fielding et al., 2022). HTTP/1.1 (1997, revised 1999 and 2014) added chunked transfer, content negotiation, conditional requests, cache controls and persistent connections; HTTP/2 introduced multiplexing of concurrent messages and header compression over TLS and TCP; HTTP/3 uses QUIC over UDP for greater independence of concurrent messages (Fielding et al., 2022). The https URI scheme requires a TLS-secured connection in which the server is authenticated and communication is protected for confidentiality and integrity, on port 443 by default (Fielding et al., 2022).

### Common usage

| Task | Method / field | Typical status |
|---|---|---|
| Read a resource | `GET` | 200 OK, 304 Not Modified |
| Create via processing | `POST` | 201 Created |
| Replace a resource | `PUT` (idempotent) | 200 OK / 204 No Content |
| Delete a resource | `DELETE` (idempotent) | 204 No Content |
| Avoid lost updates | `If-Match: "<etag>"` | 412 Precondition Failed on conflict |
| Choose a format | `Accept`, `Content-Type` | 406 Not Acceptable if none fits |

Source: Fielding et al. (2022).

### When to use it

- Communication between browsers and web servers and between services across networks, where a uniform interface, intermediaries and caching help (Fielding et al., 2022).
- Public APIs that many clients use independently ([[rest|REST]], [[apis|APIs]]).
- For streaming or event-driven communication, patterns on top of HTTP or other protocols may fit better ([[asynchronous-apis|asynchronous APIs]]).

### Strengths and limitations

**Strengths**
- A uniform interface independent of resource types lets general-purpose clients, servers and intermediaries work together (Fielding et al., 2022).
- Each request can be considered in isolation, which reduces interaction complexity and allows independent evolution (Fielding et al., 2022).
- Clear semantics for safe and idempotent methods enable caching, prefetching and safe retries (Fielding et al., 2022).

**Limitations**
- Stateless by design: sessions and authentication must be layered on top ([[api-authentication|API authentication]]).
- Servers must ensure that actions triggered through URI parameters respect method semantics, otherwise automated GETs by crawlers or prefetchers cause side effects (Fielding et al., 2022).
- Plain http offers no confidentiality or integrity; https with TLS is required for that (Fielding et al., 2022).

### Comparison

| Version | Transport | Key feature |
|---|---|---|
| HTTP/1.1 | TCP (with TLS for https) | text-based messages, persistent connections |
| HTTP/2 | TCP + TLS | multiplexed concurrent messages, field compression |
| HTTP/3 | QUIC over UDP | independent concurrent streams |

Source: Fielding et al. (2022).

### In practice

Use methods for what they mean and make retries safe: design PUT and DELETE idempotent, and never trigger unsafe actions through GET (Fielding et al., 2022). Return precise status codes and machine-readable error bodies, and use ETags with conditional requests for caching and concurrency control ([[apis|APIs]]). Serve everything over https. HTTP-level request logs and status codes are also a basic data source for [[monitoring-and-alerting|monitoring]] and [[web-analytics|web analytics]].

### Key takeaway

HTTP is the web's stateless request/response protocol: methods with defined safe and idempotent semantics act on resources through representations, status codes report the result, and the same semantics run over HTTP/1.1, HTTP/2 and HTTP/3.

### Sources

- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics*. RFC 9110 (STD 97), IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Das Hypertext Transfer Protocol (HTTP) ist eine Familie zustandsloser Anfrage-Antwort-Protokolle auf Anwendungsebene mit generischer Schnittstelle, erweiterbarer Semantik und selbstbeschreibenden Nachrichten; seit 1990 ist es das wichtigste Übertragungsprotokoll des Webs (Fielding et al., 2022). Ein Client sendet eine Anfrage mit einer Methode wie GET oder POST an eine durch eine URI bezeichnete Ressource, und der Server antwortet mit einem dreistelligen Statuscode, Header-Feldern und meist einer Repräsentation der Ressource. Seit 2022 ist die gemeinsame Semantik in RFC 9110 festgelegt, getrennt von den Übertragungsformaten von HTTP/1.1, HTTP/2 und HTTP/3, die nebeneinander bestehen, weil jedes eigene Vorteile hat (Fielding et al., 2022). HTTP ist die Grundlage von Webseiten und der meisten Web-[[apis|APIs]], einschließlich [[rest|REST]]-APIs.

### Kernkonzepte

```text
Anfrage                                         Antwort
GET /orders/42 HTTP/1.1                         HTTP/1.1 200 OK
Host: api.example.com                           Content-Type: application/json
Accept: application/json        ─────────►      ETag: "v7"
If-None-Match: "v6"                             Cache-Control: max-age=60
                                ◄─────────
                                                {"id": 42, "status": "open"}
Methode + Ziel-URI + Header-Felder (+ Inhalt)    Statuscode + Header-Felder (+ Inhalt)
```

#### 1. Ressourcen, Repräsentationen und Nachrichten

Ziel einer Anfrage ist eine Ressource, meist durch eine URI bezeichnet; HTTP begrenzt nicht, was eine Ressource ist, sondern definiert nur eine Schnittstelle, um mit ihr zu interagieren (Fielding et al., 2022). Übertragen wird eine Repräsentation, also Information, die einen vergangenen, aktuellen oder gewünschten Zustand der Ressource wiedergibt, bestehend aus Repräsentations-Metadaten und Daten. Jede Nachricht ist eine Anfrage oder eine Antwort: Der Client äußert seine Absicht, der Server deutet sie für die Zielressource und antwortet; der Client entscheidet anhand von Statuscode und Inhalt, was als Nächstes geschieht (Fielding et al., 2022).

#### 2. Methoden und ihre Eigenschaften

Die Methode ist die wichtigste Quelle der Anfragesemantik (Fielding et al., 2022). GET überträgt eine aktuelle Repräsentation, HEAD dasselbe ohne Inhalt, POST führt ressourcenspezifische Verarbeitung des Anfrageinhalts aus, PUT ersetzt alle aktuellen Repräsentationen, DELETE entfernt sie, und CONNECT, OPTIONS und TRACE dienen Tunneln, Erkundung und Schleifentests. GET, HEAD, OPTIONS und TRACE sind sicher, also im Wesentlichen nur lesend; PUT, DELETE und die sicheren Methoden sind idempotent, sodass ein Client sie nach einem Verbindungsabbruch wiederholen darf, während nicht idempotente Anfragen wie POST nicht automatisch wiederholt werden sollten (Fielding et al., 2022). Alle Allzweck-Server müssen GET und HEAD unterstützen.

#### 3. Statuscodes

Statuscodes sind dreistellige Zahlen von 100 bis 599, deren erste Ziffer die Klasse angibt: 1xx Information, 2xx Erfolg, 3xx Umleitung, 4xx Client-Fehler, 5xx Server-Fehler (Fielding et al., 2022). Clients müssen die Klasse auch unbekannter Codes verstehen und sie wie x00 dieser Klasse behandeln. So bedeutet 405, dass die Methode für die Ressource nicht erlaubt ist, und 501, dass sie gar nicht implementiert ist.

#### 4. Content Negotiation und bedingte Anfragen

Content Negotiation wählt zwischen Repräsentationen in verschiedenen Formaten, Sprachen oder Kodierungen aus, etwa proaktiv durch den Server anhand der vom Client angegebenen Präferenzen (Fielding et al., 2022). Bedingte Anfragen tragen Vorbedingungen, die Validatoren einer früheren Repräsentation mit der aktuellen vergleichen: Ein bedingtes GET ist der effizienteste Weg, Caches zu aktualisieren, und bedingtes PUT oder DELETE verhindert das Problem verlorener Änderungen, wenn Clients parallel arbeiten (Fielding et al., 2022).

#### Herkunft und Varianten

HTTP begann 1990 als einfacher Mechanismus mit einer einzigen Methode, GET, und wuchs dazu, beliebige Medientypen zu übertragen und Zwischenstationen zu durchlaufen (HTTP/0.9 und 1.0) (Fielding et al., 2022). HTTP/1.1 (1997, überarbeitet 1999 und 2014) brachte Chunked Transfer, Content Negotiation, bedingte Anfragen, Cache-Steuerung und persistente Verbindungen; HTTP/2 führte das Multiplexing gleichzeitiger Nachrichten und Header-Kompression über TLS und TCP ein; HTTP/3 nutzt QUIC über UDP für größere Unabhängigkeit gleichzeitiger Nachrichten (Fielding et al., 2022). Das URI-Schema https verlangt eine mit TLS gesicherte Verbindung, bei der der Server authentifiziert ist und die Kommunikation vertraulich und integritätsgeschützt erfolgt, standardmäßig über Port 443 (Fielding et al., 2022).

### Typische Verwendung

| Aufgabe | Methode / Feld | Typischer Status |
|---|---|---|
| Ressource lesen | `GET` | 200 OK, 304 Not Modified |
| Durch Verarbeitung anlegen | `POST` | 201 Created |
| Ressource ersetzen | `PUT` (idempotent) | 200 OK / 204 No Content |
| Ressource löschen | `DELETE` (idempotent) | 204 No Content |
| Verlorene Änderungen vermeiden | `If-Match: "<etag>"` | 412 Precondition Failed bei Konflikt |
| Format wählen | `Accept`, `Content-Type` | 406 Not Acceptable, wenn keines passt |

Quelle: Fielding et al. (2022).

### Wann einsetzen

- Kommunikation zwischen Browsern und Webservern sowie zwischen Diensten über Netzwerke, wo eine einheitliche Schnittstelle, Zwischenstationen und Caching helfen (Fielding et al., 2022).
- Öffentliche APIs, die viele Clients unabhängig voneinander nutzen ([[rest|REST]], [[apis|APIs]]).
- Für Streaming oder ereignisgesteuerte Kommunikation passen Muster auf Basis von HTTP oder andere Protokolle oft besser ([[asynchronous-apis|asynchrone APIs]]).

### Stärken und Grenzen

**Stärken**
- Eine von Ressourcentypen unabhängige, einheitliche Schnittstelle lässt allgemeine Clients, Server und Zwischenstationen zusammenarbeiten (Fielding et al., 2022).
- Jede Anfrage lässt sich für sich betrachten, was die Komplexität der Interaktion senkt und unabhängige Weiterentwicklung erlaubt (Fielding et al., 2022).
- Klare Semantik sicherer und idempotenter Methoden ermöglicht Caching, Prefetching und sichere Wiederholungen (Fielding et al., 2022).

**Grenzen**
- Absichtlich zustandslos: Sitzungen und Authentifizierung müssen darüber aufgesetzt werden ([[api-authentication|API-Authentifizierung]]).
- Server müssen sicherstellen, dass über URI-Parameter ausgelöste Aktionen die Methodensemantik einhalten, sonst verursachen automatische GETs von Crawlern oder Prefetchern Nebenwirkungen (Fielding et al., 2022).
- Einfaches http bietet weder Vertraulichkeit noch Integrität; dafür ist https mit TLS nötig (Fielding et al., 2022).

### Vergleich

| Version | Transport | Kernmerkmal |
|---|---|---|
| HTTP/1.1 | TCP (mit TLS für https) | textbasierte Nachrichten, persistente Verbindungen |
| HTTP/2 | TCP + TLS | gemultiplexte gleichzeitige Nachrichten, Feldkompression |
| HTTP/3 | QUIC über UDP | unabhängige gleichzeitige Streams |

Quelle: Fielding et al. (2022).

### In der Praxis

Methoden werden in ihrer Bedeutung verwendet und Wiederholungen sicher gemacht: PUT und DELETE idempotent gestalten und nie unsichere Aktionen über GET auslösen (Fielding et al., 2022). Präzise Statuscodes und maschinenlesbare Fehlermeldungen zurückgeben und ETags mit bedingten Anfragen für Caching und Nebenläufigkeitskontrolle nutzen ([[apis|APIs]]). Alles über https ausliefern. HTTP-Anfrageprotokolle und Statuscodes sind zudem eine grundlegende Datenquelle für [[monitoring-and-alerting|Monitoring]] und [[web-analytics|Web Analytics]].

### Merksatz

HTTP ist das zustandslose Anfrage-Antwort-Protokoll des Webs: Methoden mit festgelegter sicherer und idempotenter Semantik wirken über Repräsentationen auf Ressourcen, Statuscodes melden das Ergebnis, und dieselbe Semantik läuft über HTTP/1.1, HTTP/2 und HTTP/3.

### Quellen

- Fielding, R., Nottingham, M. & Reschke, J. (2022). *HTTP Semantics*. RFC 9110 (STD 97), IETF. [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html)
