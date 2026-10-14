---
title_en: Frontend Development
title_de: Frontend-Entwicklung
entity_type: Concept
aliases:
- Frontend development
- Front-end development
- Frontend
- Web frontend
- React.js
- TypeScript
- Node.js
- State management
- Frontend-Entwicklung
sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction
- https://react.dev/learn/thinking-in-react
- https://react.dev/learn/managing-state
- https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html
- https://nodejs.org/en/about
- https://www.w3.org/WAI/standards-guidelines/wcag/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Frontend development builds the part of an application that runs in the browser: HTML for structure, CSS for presentation and JavaScript for behaviour, all operating on the Document Object Model (DOM), the in-memory tree of the page that scripts can change (MDN). Modern frontends are built from components with a framework such as React, where the user interface is described declaratively as a function of state and data flows one way from parent to child components (React, Thinking in React; React, Managing state). TypeScript adds static type checking to JavaScript without changing its runtime behaviour, and Node.js runs JavaScript outside the browser for build tools and servers (TypeScript; Node.js). Accessible interfaces follow the Web Content Accessibility Guidelines (WCAG) ([[w3c|W3C]] WAI). For AI applications, the frontend is where users chat with assistants, inspect sources and approve agent actions.

### How it works

```text
backend APIs (REST, streaming) ←→ frontend app (TypeScript, React components)
 ▼
state: component state → lifted to common parent → reducer + context for complex screens
 ▼
render: UI = f(state) → framework updates the DOM
 ▼
browser: DOM tree → layout and paint → user events → event handlers → new state
 (tooling: Node.js-based build, type checking, tests, bundling)
```

#### 1. The DOM

"The Document Object Model (DOM) connects web pages to scripts or programming languages by representing the structure of a document—such as the HTML representing a web page—in memory" (MDN). The browser parses HTML into a tree of nodes, and DOM methods let scripts change the document's structure, style or content and attach event handlers that run when events fire. The DOM is a Web API, not part of JavaScript, but JavaScript is the usual way to use it (MDN).

#### 2. Components and one-way data flow

React's recommended process for building a user interface has five steps: break the UI into a component hierarchy, build a static version, find the minimal complete representation of the UI state, decide which component owns each piece of state, and add inverse data flow (React, Thinking in React). Props are "like arguments you pass to a function", state is "like a component's memory". Data flows down from the top-level component to the leaves, and changes flow back up only through callback functions passed down by the state owner. Each component should ideally be concerned with one thing and be split when it grows (React, Thinking in React).

#### 3. State management

With React, "you won't modify the UI from code directly": developers describe the UI for each visual state, such as typing, submitting or success, and change state in response to input (React, Managing state). State should not contain redundant or duplicated information, since values that can be computed from other state are easy to forget to update. To keep two components in sync, their state is lifted to the closest common parent and passed down as props. Components with many updates move the update logic into a reducer, a function that maps the current state and an action to the next state, and context makes values available to deeply nested components without passing props through every layer; reducers and context together manage complex screens (React, Managing state).

#### 4. TypeScript

TypeScript is a typed superset of JavaScript and a static type checker that finds errors "before execution", for example misspelled properties or invalid operations on values (TypeScript). It "never changes the runtime behavior of JavaScript code": the compiler erases types and emits plain JavaScript, and existing JavaScript can be moved into TypeScript files and typed step by step (TypeScript). Shared types between frontend and backend API definitions reduce integration errors ([[apis|APIs]]).

#### 5. Runtime and tooling: Node.js

Node.js is "an asynchronous event-driven JavaScript runtime" designed for scalable network applications: almost no function performs blocking I/O, and the process runs an event loop that sleeps when there is no work (Node.js). Frontend teams use it to run build tools, development servers and tests, and full-stack applications use it as a backend for the same language on both sides. Asynchronous patterns are discussed in [[asynchronous-apis|asynchronous APIs]].

#### 6. Accessibility

"The WCAG documents explain how to make web content more accessible to people with disabilities"; WCAG 2.2, first published in October 2023, organises its guidelines under four principles, perceivable, operable, understandable and robust, with testable success criteria at levels A, AA and AAA (W3C WAI). Charts and dashboards add specific requirements, for example not using colour alone, see [[data-visualisation|data visualisation]].

#### Origin and variants

The DOM is a Web API maintained as a web standard (MDN); React describes user interfaces declaratively as components (React, Thinking in React), and frameworks such as Angular take other approaches to the same task; TypeScript adds types on top of JavaScript (TypeScript); Node.js brought JavaScript to the server (Node.js). This site's own frontend is a React and TypeScript single-page application.

### When to use it

- Any application whose users interact through a browser: chat interfaces for LLM assistants, review dashboards, internal tools.
- Interfaces for agentic applications that need to show sources, intermediate steps and approval dialogs for tool calls ([[agentic-ai|agentic AI]]).
- Prototypes that make an AI use case tangible for business stakeholders ([[requirements-engineering|requirements engineering]]).

### Strengths and limitations

**Strengths**
- Declarative components make the UI predictable: the same state always renders the same output (React, Managing state).
- One-way data flow makes it clear which component changes which data (React, Thinking in React).
- Static types catch common errors before code runs, without changing runtime behaviour (TypeScript).

**Limitations**
- Redundant or badly placed state causes bugs that are hard to trace (React, Managing state).
- Type checking can be overly conservative and report errors for working code (TypeScript).
- Accessibility has to be checked against many testable success criteria at three conformance levels (W3C WAI).

### Comparison

| Layer | Responsibility | Example technologies |
|---|---|---|
| Structure | content and semantics | HTML, the DOM (MDN) |
| Presentation | layout, colours, typography | CSS |
| Behaviour and state | interactivity, data flow | JavaScript / TypeScript, React |
| Tooling and server | builds, dev server, backend | Node.js |
| Backend for AI | models, retrieval, agents | [[python\|Python]] services, [[apis\|APIs]] |

Sources: MDN; React; TypeScript; Node.js.

### In practice

Frontends are tested at several levels: unit tests for components and end-to-end tests in real browsers, for example with Playwright ([[software-testing|software testing]]), and deployed through [[ci-cd|CI/CD]]. For LLM chat interfaces, responses are streamed from the backend so that text appears as it is generated, and the frontend renders citations so users can check sources ([[retrieval-augmented-generation|RAG]]).

### Key takeaway

Frontend development builds browser interfaces as trees of components that render the DOM declaratively from state, with one-way data flow, TypeScript for type safety, Node.js-based tooling and WCAG for accessibility.

### Sources

- MDN. *Introduction to the DOM.* MDN Web Docs. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
- React, Thinking in React. *Thinking in React.* react.dev. [react.dev](https://react.dev/learn/thinking-in-react)
- React, Managing state. *Managing State.* react.dev. [react.dev](https://react.dev/learn/managing-state)
- TypeScript. *TypeScript for the New Programmer.* TypeScript Handbook. [typescriptlang.org](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- Node.js. *About Node.js.* [nodejs.org](https://nodejs.org/en/about)
- W3C WAI. *WCAG 2 Overview.* W3C Web Accessibility Initiative. [w3.org](https://www.w3.org/WAI/standards-guidelines/wcag/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Frontend-Entwicklung baut den Teil einer Anwendung, der im Browser läuft: HTML für die Struktur, CSS für die Darstellung und JavaScript für das Verhalten, alles auf Grundlage des Document Object Model (DOM), des Baums der Seite im Speicher, den Skripte verändern können (MDN). Moderne Frontends werden aus Komponenten mit einem Framework wie React gebaut, in dem die Benutzeroberfläche deklarativ als Funktion des Zustands beschrieben wird und Daten in eine Richtung von Eltern- zu Kindkomponenten fließen (React, Thinking in React; React, Managing state). TypeScript ergänzt JavaScript um statische Typprüfung, ohne sein Laufzeitverhalten zu ändern, und Node.js führt JavaScript außerhalb des Browsers aus, für Build-Werkzeuge und Server (TypeScript; Node.js). Barrierefreie Oberflächen folgen den Web Content Accessibility Guidelines (WCAG) ([[w3c|W3C]] WAI). Bei KI-Anwendungen ist das Frontend der Ort, an dem Nutzende mit Assistenten chatten, Quellen prüfen und Aktionen von Agenten freigeben.

### Funktionsweise

```text
Backend-APIs (REST, Streaming) ←→ Frontend-App (TypeScript, React-Komponenten)
 ▼
Zustand: Komponentenzustand → zum gemeinsamen Elternteil angehoben → Reducer + Context für komplexe Ansichten
 ▼
Rendern: UI = f(Zustand) → Framework aktualisiert das DOM
 ▼
Browser: DOM-Baum → Layout und Darstellung → Nutzerereignisse → Event Handler → neuer Zustand
 (Werkzeuge: Build auf Basis von Node.js, Typprüfung, Tests, Bündelung)
```

#### 1. Das DOM

„The Document Object Model (DOM) connects web pages to scripts or programming languages by representing the structure of a document—such as the HTML representing a web page—in memory“ (MDN). Der Browser zerlegt HTML in einen Baum aus Knoten, und DOM-Methoden erlauben Skripten, Struktur, Stil oder Inhalt des Dokuments zu ändern und Event Handler anzuhängen, die bei Ereignissen ausgeführt werden. Das DOM ist eine Web-API und nicht Teil von JavaScript, doch JavaScript ist der übliche Weg, es zu nutzen (MDN).

#### 2. Komponenten und Datenfluss in eine Richtung

Der von React empfohlene Weg zu einer Benutzeroberfläche hat fünf Schritte: die Oberfläche in eine Komponentenhierarchie zerlegen, eine statische Fassung bauen, die minimale vollständige Darstellung des UI-Zustands finden, festlegen, welche Komponente welchen Zustand besitzt, und den umgekehrten Datenfluss ergänzen (React, Thinking in React). Props sind „like arguments you pass to a function“, State ist „like a component's memory“. Daten fließen von der obersten Komponente zu den Blättern, und Änderungen fließen nur über Callback-Funktionen zurück nach oben, die der Besitzer des Zustands weitergibt. Jede Komponente sollte sich möglichst nur um eine Sache kümmern und aufgeteilt werden, wenn sie wächst (React, Thinking in React).

#### 3. Zustandsverwaltung

Mit React gilt: „you won't modify the UI from code directly“; Entwickelnde beschreiben die Oberfläche für jeden sichtbaren Zustand, etwa Tippen, Absenden oder Erfolg, und ändern den Zustand als Reaktion auf Eingaben (React, Managing state). Der Zustand sollte keine redundanten oder doppelten Informationen enthalten, denn Werte, die sich aus anderem Zustand berechnen lassen, werden leicht nicht mit aktualisiert. Um zwei Komponenten synchron zu halten, wird ihr Zustand zum nächsten gemeinsamen Elternteil angehoben und als Props weitergegeben. Komponenten mit vielen Aktualisierungen verlagern die Aktualisierungslogik in einen Reducer, eine Funktion, die den aktuellen Zustand und eine Aktion auf den nächsten Zustand abbildet, und Context stellt Werte tief verschachtelten Komponenten bereit, ohne Props durch jede Ebene zu reichen; Reducer und Context zusammen verwalten komplexe Ansichten (React, Managing state).

#### 4. TypeScript

TypeScript ist eine typisierte Obermenge von JavaScript und ein statischer Typprüfer, der Fehler „before execution“ findet, etwa falsch geschriebene Eigenschaften oder ungültige Operationen auf Werten (TypeScript). Es „never changes the runtime behavior of JavaScript code“: Der Compiler entfernt die Typen und erzeugt reines JavaScript, und bestehendes JavaScript lässt sich in TypeScript-Dateien übernehmen und Schritt für Schritt typisieren (TypeScript). Gemeinsame Typen für Frontend und API-Definitionen des Backends verringern Integrationsfehler ([[apis|APIs]]).

#### 5. Laufzeit und Werkzeuge: Node.js

Node.js ist „an asynchronous event-driven JavaScript runtime“ für skalierbare Netzwerkanwendungen: Fast keine Funktion führt blockierende Ein- und Ausgaben aus, und der Prozess betreibt eine Event Loop, die ruht, wenn keine Arbeit anfällt (Node.js). Frontend-Teams nutzen es für Build-Werkzeuge, Entwicklungsserver und Tests, und Full-Stack-Anwendungen nutzen es als Backend, sodass auf beiden Seiten dieselbe Sprache läuft. Asynchrone Muster behandelt [[asynchronous-apis|Asynchrone APIs]].

#### 6. Barrierefreiheit

„The WCAG documents explain how to make web content more accessible to people with disabilities“; WCAG 2.2, erstmals im Oktober 2023 veröffentlicht, ordnet seine Richtlinien vier Prinzipien zu, wahrnehmbar, bedienbar, verständlich und robust, mit prüfbaren Erfolgskriterien auf den Stufen A, AA und AAA (W3C WAI). Diagramme und Dashboards bringen eigene Anforderungen mit, etwa Farbe nicht als einziges Mittel einzusetzen, siehe [[data-visualisation|Datenvisualisierung]].

#### Herkunft und Varianten

Das DOM ist eine als Webstandard gepflegte Web-API (MDN); React beschreibt Benutzeroberflächen deklarativ als Komponenten (React, Thinking in React), und Frameworks wie Angular gehen dieselbe Aufgabe auf andere Weise an; TypeScript setzt Typen auf JavaScript (TypeScript); Node.js brachte JavaScript auf den Server (Node.js). Das Frontend dieser Seite ist selbst eine Single-Page-Anwendung mit React und TypeScript.

### Wann einsetzen

- Jede Anwendung, mit der Nutzende über einen Browser arbeiten: Chat-Oberflächen für LLM-Assistenten, Review-Dashboards, interne Werkzeuge.
- Oberflächen für agentische Anwendungen, die Quellen, Zwischenschritte und Freigabedialoge für Tool-Aufrufe zeigen müssen ([[agentic-ai|Agentic AI]]).
- Prototypen, die einen KI-Anwendungsfall für Fachbereiche greifbar machen ([[requirements-engineering|Requirements Engineering]]).

### Stärken und Grenzen

**Stärken**
- Deklarative Komponenten machen die Oberfläche vorhersagbar: Derselbe Zustand ergibt immer dieselbe Ausgabe (React, Managing state).
- Der Datenfluss in eine Richtung macht klar, welche Komponente welche Daten ändert (React, Thinking in React).
- Statische Typen finden häufige Fehler, bevor Code läuft, ohne das Laufzeitverhalten zu ändern (TypeScript).

**Grenzen**
- Redundanter oder falsch platzierter Zustand verursacht schwer nachvollziehbare Fehler (React, Managing state).
- Die Typprüfung kann übervorsichtig sein und bei funktionierendem Code Fehler melden (TypeScript).
- Barrierefreiheit muss anhand vieler prüfbarer Erfolgskriterien auf drei Konformitätsstufen geprüft werden (W3C WAI).

### Vergleich

| Schicht | Aufgabe | Beispieltechnologien |
|---|---|---|
| Struktur | Inhalt und Semantik | HTML, das DOM (MDN) |
| Darstellung | Layout, Farben, Typografie | CSS |
| Verhalten und Zustand | Interaktivität, Datenfluss | JavaScript / TypeScript, React |
| Werkzeuge und Server | Builds, Entwicklungsserver, Backend | Node.js |
| Backend für KI | Modelle, Retrieval, Agenten | Python-Dienste, [[apis\|APIs]] |

Quellen: MDN; React; TypeScript; Node.js.

### In der Praxis

Frontends werden auf mehreren Ebenen getestet: Unit-Tests für Komponenten und End-to-End-Tests in echten Browsern, etwa mit Playwright ([[software-testing|Softwaretests]]), und über [[ci-cd|CI/CD]] ausgeliefert. Bei LLM-Chatoberflächen werden Antworten vom Backend gestreamt, damit Text erscheint, während er erzeugt wird, und das Frontend zeigt Quellenangaben an, damit Nutzende sie prüfen können ([[retrieval-augmented-generation|RAG]]).

### Merksatz

Frontend-Entwicklung baut Browseroberflächen als Bäume aus Komponenten, die das DOM deklarativ aus dem Zustand erzeugen, mit Datenfluss in eine Richtung, TypeScript für Typsicherheit, Werkzeugen auf Basis von Node.js und WCAG für Barrierefreiheit.

### Quellen

- MDN. *Introduction to the DOM.* MDN Web Docs. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
- React, Thinking in React. *Thinking in React.* react.dev. [react.dev](https://react.dev/learn/thinking-in-react)
- React, Managing state. *Managing State.* react.dev. [react.dev](https://react.dev/learn/managing-state)
- TypeScript. *TypeScript for the New Programmer.* TypeScript Handbook. [typescriptlang.org](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- Node.js. *About Node.js.* [nodejs.org](https://nodejs.org/en/about)
- W3C WAI. *WCAG 2 Overview.* W3C Web Accessibility Initiative. [w3.org](https://www.w3.org/WAI/standards-guidelines/wcag/)
