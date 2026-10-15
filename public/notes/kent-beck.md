---
title_en: Kent Beck
title_de: Kent Beck
entity_type: Person
aliases:
- Kent Beck
sources:
- https://www.kentbeck.com/
- https://tidyfirst.substack.com/about
- https://martinfowler.com/bliki/ExtremeProgramming.html
- https://martinfowler.com/bliki/TestDrivenDevelopment.html
- https://martinfowler.com/articles/continuousIntegration.html
- https://martinfowler.com/bliki/UserStory.html
- https://martinfowler.com/bliki/CodeSmell.html
- https://martinfowler.com/books/refactoring.html
- https://agilemanifesto.org/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong. It covers only Kent Beck's public, professional work.

### TL;DR

Kent Beck is a software design author and speaker who describes himself as the "creator of Extreme Programming and Test-Driven Development" and the author of *Tidy First?* (Beck, n.d.-a). Extreme Programming (XP), which he developed primarily, was one of the first agile methods and popularised [[ci-cd|continuous integration]], [[refactoring|refactoring]], test-driven development and agile planning (Fowler, 2013a); with Erich Gamma he originally wrote the JUnit testing framework (Fowler, 2024). He co-signed the Manifesto for Agile Software Development in 2001 (Beck et al., 2001), coined the term "[[code-smell|code smell]]" (Fowler, 2006) and co-wrote the second edition of *Refactoring* with [[martin-fowler|Martin Fowler]] (Fowler, 2018). He now writes about "augmented coding", software development with AI coding assistants (Beck, n.d.-a).

### Key facts

| | |
|---|---|
| Field | software design, agile methods, developer testing |
| Known for | Extreme Programming, test-driven development, JUnit (with Erich Gamma), continuous integration as a practice |
| Agile Manifesto | one of its 17 authors (2001) |
| Current work | newsletter *Software Design: Tidy First?*, book series on "Empirical Software Design", research on augmented coding |

Sources: Beck (n.d.-a); Fowler (2024); Beck et al. (2001).

### Career

Beck developed XP while consulting for Smalltalk projects in the late 1980s and early 1990s; its practices were first used together in the C3 project, where Martin Fowler worked with him (Fowler, 2013a). He describes the first two decades of his career as tied together by patterns, JUnit, TDD and Extreme Programming, all of which he sees as ways to help developers "feel safe" (Beck, n.d.-b). In 2005, twenty-five years into his career, a panel with the authors of *Structured Design* led him to study coupling and cohesion, which eventually resulted in his book *Tidy First?* (Beck, n.d.-a). He also works as a consultant and speaker (Beck, n.d.-a).

### Key contributions

#### Extreme Programming

XP is "a software development methodology developed primarily by Kent Beck" and was the dominant agile method in the late 1990s and early 2000s; Beck describes it as a progression from values through principles to concrete practices (Fowler, 2013a). Within XP he introduced the term user story, to encourage "a more informal and conversational style of requirements elicitation than long written specifications" ([[requirements-engineering|requirements engineering]]; Fowler, 2013b).

#### Test-driven development and JUnit

Test-driven development was "developed by Kent Beck in the late 1990's as part of Extreme Programming": write a test for the next bit of functionality, write code until it passes, then refactor, often summarised as red, green, refactor (Fowler, 2023; [[software-testing|software testing]]). JUnit, originally written by Beck and Erich Gamma, had a marked impact on the Java community in the late 1990s and inspired the xUnit family of testing frameworks in other languages (Fowler, 2024).

#### Continuous integration

Continuous integration "was developed as a practice by Kent Beck as part of Extreme Programming in the 1990s"; his guidelines include "no code sits unintegrated for more than a couple of hours" and "nobody has a higher priority task than fixing the build" (Fowler, 2024; [[ci-cd|CI/CD]]).

#### Code smells and refactoring

Beck coined the term "code smell" while helping Fowler with the *Refactoring* book and is co-author of its second edition (Fowler, 2006; Fowler, 2018; [[refactoring|refactoring]]).

### Key works

| Work | Notes |
|---|---|
| *Test-Driven Development* | book on TDD (Fowler, 2023) |
| *Planning Extreme Programming* (2000) | with Martin Fowler ([[martin-fowler|Martin Fowler]]) |
| *Refactoring* (2nd ed., 2018) | with Martin Fowler (Fowler, 2018) |
| *Tidy First? A Personal Exercise in Empirical Design* | first book in his "Empirical Software Design" series (Beck, n.d.-a) |
| *The Good News Factory* | executive briefing on software design (Beck, n.d.-a) |
| *Tidy Together* | third book of the series, in progress (Beck, n.d.-a) |

### Influence and reception

Fowler calls XP "the primary catalyst that got attention to agile methods" and notes that practices it popularised, such as continuous integration, refactoring and TDD, have since been widely used (Fowler, 2013a). The Manifesto for Agile Software Development, which Beck co-authored, values "individuals and interactions over processes and tools" and "working software over comprehensive documentation" (Beck et al., 2001).

### Relevance for AI development

Beck explores "augmented coding", collaborating with AI coding assistants; he observes that the assistants go beyond stated requirements but "lack taste", for example by adding 20 more lines to an already giant function (Beck, n.d.-a). His principles are to constrain the context given to the AI, preserve optionality through good design, balance feature expansion with refactoring and keep human judgement over architecture (Beck, n.d.-a; [[context-engineering|context engineering]]). The XP practices he shaped, small steps, fast tests and continuous integration, are the safety net for reviewing AI-generated changes ([[ci-cd|CI/CD]], [[software-testing|software testing]]).

### Sources

- Beck, K. (n.d.-a). *Kent Beck – Software Design Pioneer*. [kentbeck.com](https://www.kentbeck.com/)
- Beck, K. (n.d.-b). *About – Software Design: Tidy First?* [tidyfirst.substack.com](https://tidyfirst.substack.com/about)
- Beck, K., Fowler, M. et al. (2001). *Manifesto for Agile Software Development*. [agilemanifesto.org](https://agilemanifesto.org/)
- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. (2013a). *Extreme Programming*. [martinfowler.com](https://martinfowler.com/bliki/ExtremeProgramming.html)
- Fowler, M. (2013b). *User Story*. [martinfowler.com](https://martinfowler.com/bliki/UserStory.html)
- Fowler, M. with Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2nd ed. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Fowler, M. (2023). *Test Driven Development*. [martinfowler.com](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- Fowler, M. (2024). *Continuous Integration*. [martinfowler.com](https://martinfowler.com/articles/continuousIntegration.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein. Sie behandelt nur die öffentliche, berufliche Arbeit von Kent Beck.

### TL;DR

Kent Beck ist Autor und Redner zum Thema Softwaredesign und beschreibt sich als „Creator of Extreme Programming and Test-Driven Development“ und Autor von *Tidy First?* (Beck, n.d.-a). Extreme Programming (XP), das er maßgeblich entwickelte, war eine der ersten agilen Methoden und machte [[ci-cd|kontinuierliche Integration]], [[refactoring|Refactoring]], testgetriebene Entwicklung und agile Planung bekannt (Fowler, 2013a); gemeinsam mit Erich Gamma schrieb er ursprünglich das Testframework JUnit (Fowler, 2024). Er unterzeichnete 2001 das Manifest für agile Softwareentwicklung mit (Beck et al., 2001), prägte den Begriff „[[code-smell|Code Smell]]“ (Fowler, 2006) und schrieb die zweite Auflage von *Refactoring* gemeinsam mit [[martin-fowler|Martin Fowler]] (Fowler, 2018). Heute schreibt er über „Augmented Coding“, Softwareentwicklung mit KI-Programmierassistenten (Beck, n.d.-a).

### Eckdaten

| | |
|---|---|
| Fachgebiet | Softwaredesign, agile Methoden, Testen durch Entwickler |
| Bekannt für | Extreme Programming, testgetriebene Entwicklung, JUnit (mit Erich Gamma), kontinuierliche Integration als Praxis |
| Agiles Manifest | einer der 17 Autoren (2001) |
| Aktuelle Arbeit | Newsletter *Software Design: Tidy First?*, Buchreihe „Empirical Software Design“, Forschung zu Augmented Coding |

Quellen: Beck (n.d.-a); Fowler (2024); Beck et al. (2001).

### Werdegang

Beck entwickelte XP während seiner Beratung für Smalltalk-Projekte Ende der 1980er und Anfang der 1990er Jahre; die Praktiken wurden erstmals gemeinsam im Projekt C3 angewandt, in dem Martin Fowler mit ihm arbeitete (Fowler, 2013a). Die ersten zwei Jahrzehnte seiner Laufbahn verbindet er selbst über Patterns, JUnit, TDD und Extreme Programming, die er alle als Wege sieht, Entwicklern ein Gefühl von Sicherheit zu geben (Beck, n.d.-b). 2005, nach 25 Berufsjahren, brachte ihn ein Podium mit den Autoren von *Structured Design* dazu, sich mit Kopplung und Kohäsion zu befassen, woraus schließlich sein Buch *Tidy First?* entstand (Beck, n.d.-a). Er arbeitet außerdem als Berater und Redner (Beck, n.d.-a).

### Wichtige Beiträge

#### Extreme Programming

XP ist „a software development methodology developed primarily by Kent Beck“ und war Ende der 1990er und Anfang der 2000er Jahre die vorherrschende agile Methode; Beck beschreibt es als Abfolge von Werten über Prinzipien zu konkreten Praktiken (Fowler, 2013a). Im Rahmen von XP führte er den Begriff User Story ein, um „a more informal and conversational style of requirements elicitation than long written specifications“ zu fördern ([[requirements-engineering|Requirements Engineering]]; Fowler, 2013b).

#### Testgetriebene Entwicklung und JUnit

Testgetriebene Entwicklung wurde „developed by Kent Beck in the late 1990's as part of Extreme Programming“: einen Test für das nächste Stück Funktionalität schreiben, Code schreiben, bis er besteht, dann refaktorieren, oft als Red, Green, Refactor zusammengefasst (Fowler, 2023; [[software-testing|Softwaretests]]). JUnit, ursprünglich von Beck und Erich Gamma geschrieben, prägte Ende der 1990er Jahre die Java-Gemeinschaft deutlich und regte die xUnit-Familie von Testframeworks für andere Sprachen an (Fowler, 2024).

#### Kontinuierliche Integration

Kontinuierliche Integration „was developed as a practice by Kent Beck as part of Extreme Programming in the 1990s“; zu seinen Richtwerten gehören „no code sits unintegrated for more than a couple of hours“ und „nobody has a higher priority task than fixing the build“ (Fowler, 2024; [[ci-cd|CI/CD]]).

#### Code Smells und Refactoring

Beck prägte den Begriff „Code Smell“, als er Fowler beim Buch *Refactoring* half, und ist Mitautor der zweiten Auflage (Fowler, 2006; Fowler, 2018; [[refactoring|Refactoring]]).

### Wichtige Werke

| Werk | Anmerkungen |
|---|---|
| *Test-Driven Development* | Buch über TDD (Fowler, 2023) |
| *Planning Extreme Programming* (2000) | mit Martin Fowler ([[martin-fowler|Martin Fowler]]) |
| *Refactoring* (2. Aufl., 2018) | mit Martin Fowler (Fowler, 2018) |
| *Tidy First? A Personal Exercise in Empirical Design* | erstes Buch seiner Reihe „Empirical Software Design“ (Beck, n.d.-a) |
| *The Good News Factory* | Kurzbriefing für Führungskräfte zu Softwaredesign (Beck, n.d.-a) |
| *Tidy Together* | drittes Buch der Reihe, in Arbeit (Beck, n.d.-a) |

### Wirkung und Rezeption

Fowler nennt XP „the primary catalyst that got attention to agile methods“ und hält fest, dass die von XP bekannt gemachten Praktiken wie kontinuierliche Integration, Refactoring und TDD seither weit verbreitet sind (Fowler, 2013a). Das von Beck mitverfasste Manifest für agile Softwareentwicklung stellt „individuals and interactions over processes and tools“ und „working software over comprehensive documentation“ (Beck et al., 2001).

### Bedeutung für die KI-Entwicklung

Beck erforscht „Augmented Coding“, die Zusammenarbeit mit KI-Programmierassistenten; er beobachtet, dass die Assistenten über die genannten Anforderungen hinausgehen, aber „lack taste“, etwa indem sie einer ohnehin riesigen Funktion 20 weitere Zeilen hinzufügen (Beck, n.d.-a). Seine Prinzipien lauten, den Kontext für die KI zu begrenzen, durch gutes Design Optionen offenzuhalten, Feature-Ausbau und Refactoring auszubalancieren und das menschliche Urteil über die Architektur zu behalten (Beck, n.d.-a; [[context-engineering|Context Engineering]]). Die von ihm geprägten XP-Praktiken, kleine Schritte, schnelle Tests und kontinuierliche Integration, sind das Sicherheitsnetz, um KI-generierte Änderungen zu prüfen ([[ci-cd|CI/CD]], [[software-testing|Softwaretests]]).

### Quellen

- Beck, K. (n.d.-a). *Kent Beck – Software Design Pioneer*. [kentbeck.com](https://www.kentbeck.com/)
- Beck, K. (n.d.-b). *About – Software Design: Tidy First?* [tidyfirst.substack.com](https://tidyfirst.substack.com/about)
- Beck, K., Fowler, M. et al. (2001). *Manifesto for Agile Software Development*. [agilemanifesto.org](https://agilemanifesto.org/)
- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. (2013a). *Extreme Programming*. [martinfowler.com](https://martinfowler.com/bliki/ExtremeProgramming.html)
- Fowler, M. (2013b). *User Story*. [martinfowler.com](https://martinfowler.com/bliki/UserStory.html)
- Fowler, M. mit Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2. Aufl. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Fowler, M. (2023). *Test Driven Development*. [martinfowler.com](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- Fowler, M. (2024). *Continuous Integration*. [martinfowler.com](https://martinfowler.com/articles/continuousIntegration.html)
