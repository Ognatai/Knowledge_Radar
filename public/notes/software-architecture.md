---
title_en: Software Architecture
title_de: Softwarearchitektur
entity_type: Concept
aliases:
- Software architecture
- Application architecture
- Microservices
- Microservice architecture
- Monolith
- Monolithic architecture
- Monolith first
- Conway's law
- Softwarearchitektur
- Microservice-Architektur
sources:
- https://martinfowler.com/architecture/
- https://martinfowler.com/articles/microservices.html
- https://martinfowler.com/bliki/MonolithFirst.html
- https://www.melconway.com/Home/Committees_Paper.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Software architecture is, in Ralph Johnson's phrase quoted by [[martin-fowler|Martin Fowler]], "about the important stuff. Whatever that is": the parts of a system's design that expert developers share an understanding of and that cause serious problems if not kept in good condition (Fowler, 2019). Good architecture matters because poor architecture lets cruft grow, which slows down new features and adds defects (Fowler, 2019; [[technical-debt|technical debt]]). A central choice is between a monolith, an application built as a single unit, and microservices, a suite of small, independently deployable services organised around business capabilities (Lewis & Fowler, 2014). Conway's law adds that a system's structure tends to copy the communication structure of the organisation that designs it (Conway, 1968).

### How it works

```text
Monolith                                   Microservices
┌───────────────────────────┐              ┌────────┐  ┌────────┐  ┌────────┐
│ UI │ domain logic │ data   │              │ orders │  │ billing│  │ search │   one team per service,
│      one process,         │   split ──►  │ UI+DB  │  │ UI+DB  │  │ UI+DB  │   own database,
│      one database,        │   along      └───┬────┘  └───┬────┘  └───┬────┘   deployed independently
│      one deployment       │   business       └──── HTTP / messaging ──┘
└───────────────────────────┘   capabilities     (smart endpoints, dumb pipes)

Conway's law: team communication structure ──► system structure
```

#### 1. What counts as architecture

Definitions such as "the fundamental organization of a system" or "the decisions that need to be made early" were questioned by Ralph Johnson: there is no objective way to say what is fundamental, and early decisions are rather those one wishes to get right early (Fowler, 2019). Architecture is thus the shared understanding of the expert developers, and architectural thinking means deciding what is important and keeping those elements in good condition (Fowler, 2019). Unlike user experience, internal quality does not trade off against speed: high internal quality leads to faster delivery because less cruft gets in the way, and the pay-off comes in weeks, not months (Fowler, 2019; [[clean-code|clean code]], [[refactoring|refactoring]]).

#### 2. The monolith

A typical enterprise application has a browser client, a relational database and a server-side application that handles [[http|HTTP]] requests, runs domain logic and renders views; this server-side application is a monolith, a single logical executable (Lewis & Fowler, 2014). All logic runs in one process, can be tested on a laptop and scaled by running many instances behind a load balancer (Lewis & Fowler, 2014). The frustrations: change cycles are tied together, so a small change requires rebuilding and redeploying the whole monolith; a good modular structure is hard to keep over time; and the whole application must be scaled rather than the parts that need it (Lewis & Fowler, 2014).

#### 3. Microservices

Lewis and Fowler (2014) describe common characteristics rather than a formal definition:

- **Componentisation via services:** services are out-of-process components, independently replaceable, upgradeable and deployable, with an explicit interface.
- **Organised around business capabilities:** each service covers user interface, storage and external collaborations for one business area, built by a cross-functional team, the largest about a "two pizza team" of no more than a dozen people.
- **Products not projects:** a team owns its product over its lifetime ("you build it, you run it").
- **Smart endpoints and dumb pipes:** services own their logic and communicate via simple REST-style HTTP or lightweight messaging instead of an enterprise service bus ([[rest|REST]], [[asynchronous-apis|asynchronous APIs]]).
- **Decentralised governance and data:** teams choose languages and tools, and each service manages its own database (polyglot persistence); instead of distributed transactions, services accept eventual consistency and fix errors with compensating operations.
- **Infrastructure automation:** continuous delivery and automated deployment ([[ci-cd|CI/CD]]).
- **Design for failure:** any service call can fail, so services need circuit breakers, timeouts and real-time monitoring of technical and business metrics ([[monitoring-and-alerting|monitoring and alerting]]).
- **Evolutionary design:** components are cut where they can be rewritten without affecting collaborators; some services are expected to be scrapped rather than evolved.

#### 4. Monolith first

Almost all successful microservice stories started with a monolith that grew too big and was broken up, while systems built as microservices from scratch often ended up in serious trouble (Fowler, 2015). Microservices carry a premium, the cost of managing a suite of services, that slows a team down and pays off only for complex systems (Fowler, 2015). They also need good, stable service boundaries, which even experienced architects rarely get right at the start, and refactoring across services is much harder than within a monolith (Fowler, 2015). A monolith-first strategy therefore builds a carefully modular monolith, then peels off services at the edges or splits coarse-grained services later; the counter-argument is that a team used to separate services from the start scales more easily (Fowler, 2015).

#### 5. Conway's law

In 1968, Melvin Conway argued that "organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations" (Conway, 1968). Organising a design team already fixes some design decisions, since alternatives for which no communication paths exist cannot be pursued (Conway, 1968). Lewis and Fowler (2014) cite the law for teams split by technology layer, which push logic into whichever application they can change; microservices instead align service boundaries with cross-functional team boundaries.

#### Origin and variants

Lewis and Fowler (2014) trace the microservice style back to the design principles of Unix and relate it to service-oriented architecture (SOA), which they see as too vaguely defined and often reduced to integrating monoliths over an enterprise service bus. Variants covered in Fowler's (2019) guide include presentation-domain-data layering, micro frontends and serverless architectures.

### When to use it

- A monolith for new or simple applications, where speed of feedback matters more than independent scaling (Fowler, 2015).
- Microservices for complex systems with several teams, stable domain boundaries and mature deployment and monitoring (Lewis & Fowler, 2014; Fowler, 2015; [[docker|Docker]], [[kubernetes|Kubernetes]]).
- Conway's law when structuring teams: team boundaries shape service boundaries (Conway, 1968; Lewis & Fowler, 2014).

### Strengths and limitations

**Strengths**
- Microservices are independently deployable and scalable and give firm module boundaries (Lewis & Fowler, 2014).
- Explicit service boundaries are harder to patch around, which may slow architectural decay (Lewis & Fowler, 2014).

**Limitations**
- Remote calls are more expensive than in-process calls and need coarser interfaces (Lewis & Fowler, 2014).
- Moving code across service boundaries is hard: interface changes need coordination, backwards compatibility layers and more complex testing (Lewis & Fowler, 2014; [[software-testing|software testing]]).
- Distribution weakens consistency and demands operational maturity (Fowler, 2019).
- Microservice boundaries drawn too early are hard to correct (Fowler, 2015).

### Comparison

| Aspect | Monolith | Microservices |
|---|---|---|
| Deployment | whole application at once | per service |
| Scaling | whole application | per service |
| Module boundaries | language-level, need discipline | process-level, explicit |
| Data | one logical database, transactions | database per service, eventual consistency |
| Refactoring boundaries | comparatively easy | hard across services |
| Operational cost | low | high (microservice premium) |

Sources: Lewis & Fowler (2014); Fowler (2015).

### Key takeaway

Architecture is the important part of a design that must be kept in good condition; start with a modular monolith and split it into microservices along business capabilities once the boundaries are clear, remembering that team structure shapes system structure.

### Sources

- Fowler, M. (2019). *Software Architecture Guide.* martinfowler.com. [martinfowler.com](https://martinfowler.com/architecture/)
- Lewis, J. & Fowler, M. (2014). *Microservices: a definition of this new architectural term.* martinfowler.com. [martinfowler.com](https://martinfowler.com/articles/microservices.html)
- Fowler, M. (2015). *Monolith First.* martinfowler.com. [martinfowler.com](https://martinfowler.com/bliki/MonolithFirst.html)
- Conway, M. E. (1968). *How Do Committees Invent?* Datamation, April 1968. [melconway.com](https://www.melconway.com/Home/Committees_Paper.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Softwarearchitektur ist, mit den von [[martin-fowler|Martin Fowler]] zitierten Worten Ralph Johnsons, „about the important stuff. Whatever that is“: die Teile eines Systementwurfs, die erfahrene Entwicklerinnen und Entwickler gemeinsam verstehen und die ernste Probleme verursachen, wenn sie nicht in gutem Zustand gehalten werden (Fowler, 2019). Gute Architektur ist wichtig, weil schlechte Architektur Cruft wachsen lässt, was neue Funktionen verlangsamt und Fehler mit sich bringt (Fowler, 2019; [[technical-debt|technische Schulden]]). Eine zentrale Entscheidung fällt zwischen einem Monolithen, einer als eine Einheit gebauten Anwendung, und Microservices, einer Menge kleiner, unabhängig deploybarer Dienste, die nach Geschäftsfähigkeiten geschnitten sind (Lewis & Fowler, 2014). Conways Gesetz ergänzt, dass die Struktur eines Systems dazu neigt, die Kommunikationsstruktur der entwerfenden Organisation abzubilden (Conway, 1968).

### Funktionsweise

```text
Monolith                                   Microservices
┌───────────────────────────┐              ┌────────┐  ┌────────┐  ┌────────┐
│ UI │ Domänenlogik │ Daten  │              │Bestell.│  │Abrechn.│  │ Suche  │   ein Team pro Dienst,
│      ein Prozess,         │  Schnitt ──► │ UI+DB  │  │ UI+DB  │  │ UI+DB  │   eigene Datenbank,
│      eine Datenbank,      │  nach        └───┬────┘  └───┬────┘  └───┬────┘   unabhängig deployt
│      ein Deployment       │  Geschäfts-      └──── HTTP / Messaging ──┘
└───────────────────────────┘  fähigkeiten       (smart endpoints, dumb pipes)

Conways Gesetz: Kommunikationsstruktur der Teams ──► Systemstruktur
```

#### 1. Was als Architektur gilt

Definitionen wie „die grundlegende Organisation eines Systems“ oder „die Entscheidungen, die früh im Projekt getroffen werden müssen“ stellte Ralph Johnson infrage: Es gibt keinen objektiven Maßstab dafür, was grundlegend ist, und frühe Entscheidungen sind eher solche, die man gern früh richtig treffen würde (Fowler, 2019). Architektur ist daher das gemeinsame Verständnis der erfahrenen Entwicklerinnen und Entwickler, und architektonisches Denken heißt, zu entscheiden, was wichtig ist, und diese Elemente in gutem Zustand zu halten (Fowler, 2019). Anders als bei der User Experience steht interne Qualität nicht im Zielkonflikt mit Geschwindigkeit: Hohe interne Qualität führt zu schnellerer Auslieferung, weil weniger Cruft im Weg steht, und zahlt sich in Wochen statt Monaten aus (Fowler, 2019; [[clean-code|Clean Code]], [[refactoring|Refactoring]]).

#### 2. Der Monolith

Eine typische Unternehmensanwendung hat einen Browser-Client, eine relationale Datenbank und eine serverseitige Anwendung, die HTTP-Anfragen bearbeitet, Domänenlogik ausführt und Ansichten erzeugt; diese serverseitige Anwendung ist ein Monolith, ein einzelnes logisches Programm (Lewis & Fowler, 2014). Die gesamte Logik läuft in einem Prozess, lässt sich auf einem Laptop testen und skalieren, indem viele Instanzen hinter einem Load Balancer laufen (Lewis & Fowler, 2014). Die Probleme: Änderungszyklen sind gekoppelt, sodass eine kleine Änderung den Neubau und das erneute Deployment des ganzen Monolithen verlangt; eine gute modulare Struktur ist auf Dauer schwer zu halten; und die ganze Anwendung muss skaliert werden statt nur der Teile, die mehr Ressourcen brauchen (Lewis & Fowler, 2014).

#### 3. Microservices

Lewis und Fowler (2014) beschreiben gemeinsame Merkmale statt einer formalen Definition:

- **Komponenten als Dienste:** Dienste sind Komponenten außerhalb des Prozesses, unabhängig austauschbar, aktualisierbar und deploybar, mit expliziter Schnittstelle.
- **Nach Geschäftsfähigkeiten geschnitten:** Jeder Dienst umfasst Benutzeroberfläche, Speicherung und externe Anbindungen für einen Geschäftsbereich und wird von einem funktionsübergreifenden Team gebaut, die größten etwa ein „Two Pizza Team“ von höchstens einem Dutzend Personen.
- **Produkte statt Projekte:** Ein Team verantwortet sein Produkt über die gesamte Lebensdauer („you build it, you run it“).
- **Smart endpoints and dumb pipes:** Dienste besitzen ihre Logik und kommunizieren über einfaches REST-artiges [[http|HTTP]] oder leichtgewichtiges Messaging statt über einen Enterprise Service Bus ([[rest|REST]], [[asynchronous-apis|asynchrone APIs]]).
- **Dezentrale Steuerung und Daten:** Teams wählen Sprachen und Werkzeuge, und jeder Dienst verwaltet seine eigene Datenbank (Polyglot Persistence); statt verteilter Transaktionen nehmen Dienste letztendliche Konsistenz in Kauf und beheben Fehler mit kompensierenden Operationen.
- **Automatisierte Infrastruktur:** Continuous Delivery und automatisiertes Deployment ([[ci-cd|CI/CD]]).
- **Auf Ausfälle ausgelegt:** Jeder Dienstaufruf kann scheitern, daher brauchen Dienste Circuit Breaker, Timeouts und Echtzeit-Monitoring technischer und geschäftlicher Kennzahlen ([[monitoring-and-alerting|Monitoring und Alerting]]).
- **Evolutionäres Design:** Komponenten werden dort geschnitten, wo sie neu geschrieben werden können, ohne ihre Partner zu beeinträchtigen; manche Dienste werden eher ersetzt als weiterentwickelt.

#### 4. Monolith First

Fast alle erfolgreichen Microservice-Geschichten begannen mit einem Monolithen, der zu groß wurde und aufgeteilt wurde, während von Grund auf als Microservices gebaute Systeme oft in ernste Schwierigkeiten gerieten (Fowler, 2015). Microservices haben einen Aufschlag, die Kosten für die Verwaltung vieler Dienste, der ein Team bremst und sich nur bei komplexen Systemen lohnt (Fowler, 2015). Sie brauchen außerdem gute, stabile Dienstgrenzen, die selbst erfahrene Architektinnen und Architekten am Anfang selten richtig ziehen, und Refactoring über Dienste hinweg ist viel schwerer als innerhalb eines Monolithen (Fowler, 2015). Eine Monolith-first-Strategie baut daher einen sorgfältig modularen Monolithen und löst später Dienste an den Rändern heraus oder teilt grobe Dienste weiter auf; das Gegenargument lautet, dass ein von Anfang an an getrennte Dienste gewöhntes Team leichter wächst (Fowler, 2015).

#### 5. Conways Gesetz

1968 argumentierte Melvin Conway, dass „organizations which design systems … are constrained to produce designs which are copies of the communication structures of these organizations“ (Conway, 1968). Schon die Organisation eines Entwurfsteams legt Entwurfsentscheidungen fest, denn Alternativen, für die keine Kommunikationswege bestehen, lassen sich nicht verfolgen (Conway, 1968). Lewis und Fowler (2014) führen das Gesetz für Teams an, die nach technischen Schichten getrennt sind und Logik in die Anwendung drücken, die sie ändern können; Microservices richten Dienstgrenzen dagegen an funktionsübergreifenden Teamgrenzen aus.

#### Ursprung und Varianten

Lewis und Fowler (2014) führen den Microservice-Stil auf die Entwurfsprinzipien von Unix zurück und setzen ihn in Bezug zur serviceorientierten Architektur (SOA), die sie für zu unscharf definiert halten und die oft auf die Integration von Monolithen über einen Enterprise Service Bus hinauslief. Als Varianten nennt Fowlers (2019) Leitfaden etwa die Schichtung in Präsentation, Domäne und Daten, Micro Frontends und Serverless-Architekturen.

### Wann einsetzen

- Ein Monolith für neue oder einfache Anwendungen, bei denen schnelles Feedback wichtiger ist als unabhängige Skalierung (Fowler, 2015).
- Microservices für komplexe Systeme mit mehreren Teams, stabilen Domänengrenzen und ausgereiftem Deployment und Monitoring (Lewis & Fowler, 2014; Fowler, 2015; [[docker|Docker]], [[kubernetes|Kubernetes]]).
- Conways Gesetz bei der Teamstruktur: Teamgrenzen prägen Dienstgrenzen (Conway, 1968; Lewis & Fowler, 2014).

### Stärken und Grenzen

**Stärken**
- Microservices sind unabhängig deploybar und skalierbar und geben feste Modulgrenzen (Lewis & Fowler, 2014).
- Explizite Dienstgrenzen lassen sich schwerer umgehen, was den Verfall der Architektur bremsen kann (Lewis & Fowler, 2014).

**Grenzen**
- Entfernte Aufrufe sind teurer als Aufrufe im Prozess und verlangen gröbere Schnittstellen (Lewis & Fowler, 2014).
- Code über Dienstgrenzen zu verschieben ist schwer: Schnittstellenänderungen brauchen Abstimmung, Schichten für Rückwärtskompatibilität und aufwendigere Tests (Lewis & Fowler, 2014; [[software-testing|Softwaretests]]).
- Verteilung schwächt die Konsistenz und verlangt betriebliche Reife (Fowler, 2019).
- Zu früh gezogene Dienstgrenzen lassen sich schwer korrigieren (Fowler, 2015).

### Vergleich

| Aspekt | Monolith | Microservices |
|---|---|---|
| Deployment | ganze Anwendung auf einmal | pro Dienst |
| Skalierung | ganze Anwendung | pro Dienst |
| Modulgrenzen | auf Sprachebene, brauchen Disziplin | auf Prozessebene, explizit |
| Daten | eine logische Datenbank, Transaktionen | Datenbank pro Dienst, letztendliche Konsistenz |
| Grenzen umbauen | vergleichsweise einfach | schwer über Dienste hinweg |
| Betriebsaufwand | gering | hoch (Microservice-Aufschlag) |

Quellen: Lewis & Fowler (2014); Fowler (2015).

### Merksatz

Architektur ist der wichtige Teil eines Entwurfs, der in gutem Zustand gehalten werden muss; mit einem modularen Monolithen beginnen und ihn nach Geschäftsfähigkeiten in Microservices aufteilen, sobald die Grenzen klar sind, im Wissen, dass die Teamstruktur die Systemstruktur prägt.

### Quellen

- Fowler, M. (2019). *Software Architecture Guide.* martinfowler.com. [martinfowler.com](https://martinfowler.com/architecture/)
- Lewis, J. & Fowler, M. (2014). *Microservices: a definition of this new architectural term.* martinfowler.com. [martinfowler.com](https://martinfowler.com/articles/microservices.html)
- Fowler, M. (2015). *Monolith First.* martinfowler.com. [martinfowler.com](https://martinfowler.com/bliki/MonolithFirst.html)
- Conway, M. E. (1968). *How Do Committees Invent?* Datamation, April 1968. [melconway.com](https://www.melconway.com/Home/Committees_Paper.html)
