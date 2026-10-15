---
title_en: Requirements Engineering and Domain Modelling
title_de: Requirements Engineering und Domänenmodellierung
entity_type: Method
aliases:
- Requirements engineering
- Requirements management
- User story
- User stories
- BPMN
- UML
- Domain-driven design
- Domain model
- Anforderungsmanagement
sources:
- https://martinfowler.com/bliki/UserStory.html
- https://martinfowler.com/bliki/UseCasesAndStories.html
- https://xp123.com/invest-in-good-stories-and-smart-tasks/
- https://www.omg.org/spec/BPMN/2.0/About-BPMN
- https://www.omg.org/spec/UML/
- https://martinfowler.com/bliki/DomainDrivenDesign.html
- https://martinfowler.com/bliki/BoundedContext.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Requirements engineering turns what stakeholders need into descriptions that a team can build, test and change: use cases describe how users interact with a system as a narrative, user stories cut requirements into small, plannable chunks, process models in BPMN show how work flows through an organisation, UML diagrams describe software structure and behaviour, and domain models capture the concepts and language of the business (Fowler, 2003; Fowler, 2013; OMG BPMN; OMG UML; Fowler, 2020). Domain-driven design puts the domain model at the centre of development and splits large domains into bounded contexts, each with a consistent model and vocabulary (Fowler, 2020; Fowler, 2014). For AI projects, the same methods translate expert knowledge and business processes into concrete use cases, for example steps that an agent can take over ([[agentic-ai|agentic AI]]).

### How it works

```text
stakeholders, experts, existing processes and systems
 ▼
elicitation: interviews, workshops, observation, documents
 ▼
process view: BPMN models of the current and target process
 ▼
domain view: concepts, terms, relationships → domain model, bounded contexts
 ▼
behaviour view: use cases (narrative) → user stories (plannable chunks, INVEST)
 ▼
acceptance criteria and tests → backlog → iterative delivery and feedback
```

#### 1. Use cases and user stories

Use cases "organize requirements to form a narrative of how users relate to and use a system", whereas user stories "break requirements into chunks for planning purposes"; stories are usually finer-grained because each must be buildable within one iteration, and a story may correspond to one or more steps of a use case (Fowler, 2003). [[kent-beck|Kent Beck]] introduced the term user story in Extreme Programming to encourage "a more informal and conversational style of requirements elicitation"; the essence of a story fits on a single card, and a common form is "As a … I want … so that …" (Fowler, 2013). Detailed requirements are therefore negotiated in conversation rather than fixed up front.

#### 2. Good stories: INVEST

Bill Wake's INVEST mnemonic names six properties of good stories (Wake, 2003): **I**ndependent, so they can be scheduled in any order; **N**egotiable, since "a good story captures the essence, not the details"; **V**aluable to the customer; **E**stimable, so that it can be sized for planning; **S**mall; and **T**estable, clear enough to write a test for it. Testability links requirements to acceptance tests, see [[software-testing|software testing]].

#### 3. Process models: BPMN

Business Process Model and Notation (BPMN) 2.0, published by the Object Management Group in 2010 and since superseded by 2.0.1, offers "an easy-to-use flowchart-like notation that is independent of any particular implementation environment" (OMG BPMN). It is intended for the stakeholders who design, manage and implement business processes and is precise enough for diagrams to be turned into executable process components; OMG calls it the de-facto standard for business process diagrams (OMG BPMN). In automation projects, a BPMN model of the current process shows where steps could be handled by software or an agent and where people stay in the loop.

#### 4. Software models: UML

The Unified Modeling Language (UML), maintained by the Object Management Group with version 2.5.1 from December 2017 as the latest formal version, is "a graphical language for visualizing, specifying, constructing, and documenting the artifacts of distributed object systems" (OMG UML). Its diagram types include class, component, deployment and activity diagrams (OMG UML); class diagrams often serve to draw domain models, activity diagrams to describe workflows.

#### 5. Domain models and domain-driven design

Domain-driven design (DDD) is "an approach to software development that centers the development on programming a domain model", named after Eric Evans's book of 2003 (Fowler, 2020). Its central practices are a ubiquitous language, a shared vocabulary that "embeds domain terminology into the software systems that we build", and models that are built in software and evolve with the product (Fowler, 2020). Strategic design organises large domains into bounded contexts, each with a unified model, because the same word can mean different things in different parts of a business, such as "meter" in different departments of an electricity utility; a context map shows how the contexts relate (Fowler, 2014). Within a context, DDD classifies objects into entities, value objects and services and groups them into aggregates (Fowler, 2020). Structuring domain knowledge for machines rather than code is covered in [[ontology-design|ontology design]] and [[knowledge-graphs|knowledge graphs]]; database structures in [[data-modelling|data modelling]].

#### Origin and variants

User stories come from Extreme Programming (Fowler, 2013), INVEST from Wake (2003), UML from version 1.1 in 1997 (OMG UML), BPMN 2.0 from 2010 (OMG BPMN) and DDD from Evans's 2003 book (Fowler, 2020).

### When to use it

- Translating expert knowledge and historically grown processes into well-defined use cases for automation or AI (OMG BPMN; Fowler, 2020).
- Planning iterative development with a backlog of small, testable stories (Fowler, 2013; Wake, 2003).
- Large systems where different departments use the same terms differently, which bounded contexts make explicit (Fowler, 2014).

### Strengths and limitations

**Strengths**
- Stories keep requirements small and negotiable and link them to tests (Wake, 2003).
- Standard notations such as BPMN and UML give business and IT a shared, precise picture (OMG BPMN; OMG UML).
- A ubiquitous language reduces translation errors between experts and code (Fowler, 2020).

**Limitations**
- Stories alone lose the narrative of how users work with the whole system; use cases provide it (Fowler, 2003).
- Models drift from reality unless they are kept in the software and evolved with it, as DDD demands (Fowler, 2020).

### Comparison

| Artefact | Question it answers | Granularity | Source |
|---|---|---|---|
| Use case | How does a user achieve a goal with the system? | whole interaction | Fowler (2003) |
| User story | What small piece of value comes next? | one iteration | Fowler (2013); Wake (2003) |
| BPMN model | How does work flow through the organisation? | process | OMG BPMN |
| UML diagram | How is the software structured and how does it behave? | system or component | OMG UML |
| Domain model | Which concepts and terms does the business use? | bounded context | Fowler (2020); Fowler (2014) |

### In practice

Workshops with domain experts produce the process model and the glossary first; stories and acceptance criteria follow. For agentic AI projects, each process step is checked for whether a deterministic function, an agent or a person should handle it, in line with the advice to prefer plain functions where possible ([[agent-frameworks|agent frameworks]]). Neglected modelling shows up later as [[technical-debt|technical debt]].

### Key takeaway

Requirements engineering combines narratives (use cases), plannable chunks (INVEST user stories), process models (BPMN), software models (UML) and a shared domain model with a ubiquitous language and bounded contexts, so that expert knowledge becomes buildable and testable software.

### Sources

- Fowler, M. (2013). *UserStory.* martinfowler.com, 22 April 2013. [martinfowler.com](https://martinfowler.com/bliki/UserStory.html)
- Fowler, M. (2003). *UseCasesAndStories.* martinfowler.com, 18 August 2003. [martinfowler.com](https://martinfowler.com/bliki/UseCasesAndStories.html)
- Wake, B. (2003). *INVEST in Good Stories, and SMART Tasks.* xp123.com, 17 August 2003. [xp123.com](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- OMG BPMN. *Business Process Model and Notation, Version 2.0.* Object Management Group, 2010. [omg.org](https://www.omg.org/spec/BPMN/2.0/About-BPMN)
- OMG UML. *Unified Modeling Language, Version 2.5.1.* Object Management Group, 2017. [omg.org](https://www.omg.org/spec/UML/)
- Fowler, M. (2020). *DomainDrivenDesign.* martinfowler.com, 22 April 2020. [martinfowler.com](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- Fowler, M. (2014). *BoundedContext.* martinfowler.com, 15 January 2014. [martinfowler.com](https://martinfowler.com/bliki/BoundedContext.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Requirements Engineering macht aus dem, was Beteiligte brauchen, Beschreibungen, die ein Team bauen, testen und ändern kann: Use Cases beschreiben als Erzählung, wie Nutzende mit einem System umgehen, User Stories schneiden Anforderungen in kleine, planbare Stücke, Prozessmodelle in BPMN zeigen, wie Arbeit durch eine Organisation läuft, UML-Diagramme beschreiben Aufbau und Verhalten von Software, und Domänenmodelle halten die Begriffe und die Sprache des Fachbereichs fest (Fowler, 2003; Fowler, 2013; OMG BPMN; OMG UML; Fowler, 2020). Domain-Driven Design stellt das Domänenmodell in den Mittelpunkt der Entwicklung und teilt große Domänen in Bounded Contexts mit jeweils einheitlichem Modell und Vokabular (Fowler, 2020; Fowler, 2014). In KI-Projekten übersetzen dieselben Methoden Expertenwissen und Geschäftsprozesse in konkrete Use Cases, etwa Schritte, die ein Agent übernehmen kann ([[agentic-ai|Agentic AI]]).

### Funktionsweise

```text
Beteiligte, Fachleute, bestehende Prozesse und Systeme
 ▼
Erhebung: Interviews, Workshops, Beobachtung, Dokumente
 ▼
Prozesssicht: BPMN-Modelle des Ist- und Sollprozesses
 ▼
Domänensicht: Begriffe, Beziehungen → Domänenmodell, Bounded Contexts
 ▼
Verhaltenssicht: Use Cases (Erzählung) → User Stories (planbare Stücke, INVEST)
 ▼
Akzeptanzkriterien und Tests → Backlog → iterative Lieferung und Rückmeldung
```

#### 1. Use Cases und User Stories

Use Cases „organize requirements to form a narrative of how users relate to and use a system“, während User Stories „break requirements into chunks for planning purposes“; Stories sind meist feiner, weil jede innerhalb einer Iteration umsetzbar sein muss, und eine Story kann einem oder mehreren Schritten eines Use Case entsprechen (Fowler, 2003). [[kent-beck|Kent Beck]] führte den Begriff User Story im Extreme Programming ein, um „a more informal and conversational style of requirements elicitation“ zu fördern; der Kern einer Story passt auf eine Karteikarte, und eine verbreitete Form lautet „As a … I want … so that …“ (Fowler, 2013). Details werden daher im Gespräch ausgehandelt statt vorab festgeschrieben.

#### 2. Gute Stories: INVEST

Bill Wakes Merkwort INVEST nennt sechs Eigenschaften guter Stories (Wake, 2003): **I**ndependent, damit sie in beliebiger Reihenfolge eingeplant werden können; **N**egotiable, denn „a good story captures the essence, not the details“; **V**aluable für die Kundschaft; **E**stimable, damit sie für die Planung geschätzt werden kann; **S**mall; und **T**estable, klar genug, um einen Test dafür zu schreiben. Testbarkeit verbindet Anforderungen mit Akzeptanztests, siehe [[software-testing|Softwaretests]].

#### 3. Prozessmodelle: BPMN

Business Process Model and Notation (BPMN) 2.0, 2010 von der Object Management Group veröffentlicht und inzwischen durch 2.0.1 abgelöst, bietet „an easy-to-use flowchart-like notation that is independent of any particular implementation environment“ (OMG BPMN). Sie richtet sich an die Beteiligten, die Geschäftsprozesse entwerfen, steuern und umsetzen, und ist präzise genug, um Diagramme in ausführbare Prozesskomponenten zu überführen; die OMG nennt sie den De-facto-Standard für Geschäftsprozessdiagramme (OMG BPMN). In Automatisierungsprojekten zeigt ein BPMN-Modell des Istprozesses, wo Schritte von Software oder einem Agenten übernommen werden könnten und wo Menschen beteiligt bleiben.

#### 4. Softwaremodelle: UML

Die Unified Modeling Language (UML), gepflegt von der Object Management Group mit Version 2.5.1 vom Dezember 2017 als neuester formaler Fassung, ist „a graphical language for visualizing, specifying, constructing, and documenting the artifacts of distributed object systems“ (OMG UML). Zu ihren Diagrammarten gehören Klassen-, Komponenten-, Verteilungs- und Aktivitätsdiagramme (OMG UML); Klassendiagramme dienen oft zum Zeichnen von Domänenmodellen, Aktivitätsdiagramme zum Beschreiben von Abläufen.

#### 5. Domänenmodelle und Domain-Driven Design

Domain-Driven Design (DDD) ist „an approach to software development that centers the development on programming a domain model“, benannt nach Eric Evans' Buch von 2003 (Fowler, 2020). Seine zentralen Praktiken sind eine Ubiquitous Language, ein gemeinsames Vokabular, das „embeds domain terminology into the software systems that we build“, und Modelle, die in Software gebaut und mit dem Produkt weiterentwickelt werden (Fowler, 2020). Strategisches Design ordnet große Domänen in Bounded Contexts mit jeweils einheitlichem Modell, weil dasselbe Wort in verschiedenen Teilen eines Unternehmens Verschiedenes bedeuten kann, etwa „Zähler“ in verschiedenen Abteilungen eines Energieversorgers; eine Context Map zeigt, wie die Kontexte zusammenhängen (Fowler, 2014). Innerhalb eines Kontexts ordnet DDD Objekte in Entities, Value Objects und Services und fasst sie zu Aggregates zusammen (Fowler, 2020). Domänenwissen für Maschinen statt für Code zu strukturieren, behandeln [[ontology-design|Ontologie-Design]] und [[knowledge-graphs|Knowledge Graphs]]; Datenbankstrukturen [[data-modelling|Datenmodellierung]].

#### Herkunft und Varianten

User Stories stammen aus dem Extreme Programming (Fowler, 2013), INVEST von Wake (2003), UML ab Version 1.1 von 1997 (OMG UML), BPMN 2.0 von 2010 (OMG BPMN) und DDD aus Evans' Buch von 2003 (Fowler, 2020).

### Wann einsetzen

- Expertenwissen und historisch gewachsene Prozesse in klar umrissene Use Cases für Automatisierung oder KI übersetzen (OMG BPMN; Fowler, 2020).
- Iterative Entwicklung mit einem Backlog aus kleinen, testbaren Stories planen (Fowler, 2013; Wake, 2003).
- Große Systeme, in denen Abteilungen dieselben Begriffe unterschiedlich verwenden, was Bounded Contexts sichtbar machen (Fowler, 2014).

### Stärken und Grenzen

**Stärken**
- Stories halten Anforderungen klein und verhandelbar und verbinden sie mit Tests (Wake, 2003).
- Standardnotationen wie BPMN und UML geben Fachbereich und IT ein gemeinsames, präzises Bild (OMG BPMN; OMG UML).
- Eine Ubiquitous Language verringert Übersetzungsfehler zwischen Fachleuten und Code (Fowler, 2020).

**Grenzen**
- Stories allein verlieren die Erzählung, wie Nutzende mit dem ganzen System arbeiten; Use Cases liefern sie (Fowler, 2003).
- Modelle entfernen sich von der Wirklichkeit, wenn sie nicht in der Software gehalten und mit ihr weiterentwickelt werden, wie DDD es verlangt (Fowler, 2020).

### Vergleich

| Artefakt | Beantwortete Frage | Granularität | Quelle |
|---|---|---|---|
| Use Case | Wie erreicht eine Person mit dem System ein Ziel? | ganze Interaktion | Fowler (2003) |
| User Story | Welches kleine Stück Nutzen kommt als Nächstes? | eine Iteration | Fowler (2013); Wake (2003) |
| BPMN-Modell | Wie läuft Arbeit durch die Organisation? | Prozess | OMG BPMN |
| UML-Diagramm | Wie ist die Software aufgebaut und wie verhält sie sich? | System oder Komponente | OMG UML |
| Domänenmodell | Welche Begriffe und Konzepte nutzt der Fachbereich? | Bounded Context | Fowler (2020); Fowler (2014) |

### In der Praxis

Workshops mit Fachleuten erzeugen zuerst das Prozessmodell und das Glossar; Stories und Akzeptanzkriterien folgen. In Projekten mit Agentic AI wird für jeden Prozessschritt geprüft, ob eine deterministische Funktion, ein Agent oder ein Mensch ihn übernehmen soll, im Einklang mit der Empfehlung, wo möglich einfache Funktionen vorzuziehen ([[agent-frameworks|Agent-Frameworks]]). Vernachlässigte Modellierung zeigt sich später als [[technical-debt|technische Schulden]].

### Merksatz

Requirements Engineering verbindet Erzählungen (Use Cases), planbare Stücke (User Stories nach INVEST), Prozessmodelle (BPMN), Softwaremodelle (UML) und ein gemeinsames Domänenmodell mit Ubiquitous Language und Bounded Contexts, damit aus Expertenwissen baubare und testbare Software wird.

### Quellen

- Fowler, M. (2013). *UserStory.* martinfowler.com, 22. April 2013. [martinfowler.com](https://martinfowler.com/bliki/UserStory.html)
- Fowler, M. (2003). *UseCasesAndStories.* martinfowler.com, 18. August 2003. [martinfowler.com](https://martinfowler.com/bliki/UseCasesAndStories.html)
- Wake, B. (2003). *INVEST in Good Stories, and SMART Tasks.* xp123.com, 17. August 2003. [xp123.com](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- OMG BPMN. *Business Process Model and Notation, Version 2.0.* Object Management Group, 2010. [omg.org](https://www.omg.org/spec/BPMN/2.0/About-BPMN)
- OMG UML. *Unified Modeling Language, Version 2.5.1.* Object Management Group, 2017. [omg.org](https://www.omg.org/spec/UML/)
- Fowler, M. (2020). *DomainDrivenDesign.* martinfowler.com, 22. April 2020. [martinfowler.com](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- Fowler, M. (2014). *BoundedContext.* martinfowler.com, 15. Januar 2014. [martinfowler.com](https://martinfowler.com/bliki/BoundedContext.html)
