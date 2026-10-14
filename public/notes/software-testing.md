---
title_en: Software Testing
title_de: Softwaretests
entity_type: Method
aliases:
- Software testing
- Test pyramid
- Unit testing
- Integration testing
- End-to-end testing
- Unit-Tests
- Integrationstests
sources:
- https://martinfowler.com/articles/practical-test-pyramid.html
- https://martinfowler.com/bliki/TestDouble.html
- https://docs.pytest.org/en/stable/getting-started.html
- https://docs.pytest.org/en/stable/explanation/fixtures.html
- https://playwright.dev/docs/intro
- https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Automated software tests check that code behaves as intended and keep checking it with every change, which makes them the foundation of [[ci-cd|CI/CD]] and refactoring. The test pyramid organises them by granularity: many fast unit tests at the bottom, fewer integration and contract tests in the middle, and only a few slow end-to-end tests through the user interface at the top (Vocke, 2018). Test doubles such as stubs and mocks replace real collaborators to keep tests fast and isolated (Fowler, 2006). In Python, pytest is the common framework; Playwright drives real browsers for end-to-end tests of web applications (pytest docs; Playwright docs). ML systems need additional tests for data, models and [[monitoring-and-alerting|monitoring]], which Breck et al. (2017) collect in the [[ml-test-score|ML Test Score]].

### How it works

```text
            /\        end-to-end / UI tests      few, slow, broad, flaky
           /  \       contract tests             interfaces between services
          /    \      integration tests          one integration point each
         /______\     unit tests                 many, fast, isolated
 every test: arrange → act → assert (given → when → then)
 placed in the deployment pipeline by speed: fast tests first
```

#### 1. The test pyramid

The pyramid comes from Mike Cohn's *Succeeding with Agile* and originally had unit, service and UI tests (Vocke, 2018). Its names are simplistic, but two rules hold: write tests with different granularity, and "the more high-level you get the fewer tests you should have". The opposite shape, the "test ice-cream cone" with many high-level tests, is slow and hard to maintain. Two further rules avoid duplicated effort: if a higher-level test finds an error that no lower-level test catches, write a lower-level test, and push tests as far down the pyramid as possible (Vocke, 2018).

#### 2. Unit tests

What counts as a unit is flexible: a function, a method or a class. Solitary unit tests replace all collaborators with test doubles, sociable ones use the real collaborators; both have their place (Vocke, 2018). Unit tests avoid databases, the file system and network calls to stay fast. They test the public interface and observable behaviour rather than internal structure, so that refactoring does not break them; needing to test a private method is a sign that a class does too much. Each test follows arrange, act, assert, or given, when, then (Vocke, 2018).

#### 3. Test doubles

"Test Double is a generic term for any case where you replace a production object for testing purposes" (Fowler, 2006, after Gerard Meszaros). There are five kinds:
- **Dummy:** passed around but never used, typically to fill parameter lists.
- **Fake:** a working implementation with shortcuts that make it unsuitable for production.
- **Stub:** returns canned answers to the calls made during the test.
- **Spy:** a stub that also records how it was called.
- **Mock:** pre-programmed with expectations that specify the calls it should receive.

#### 4. Integration and contract tests

Integration tests check the code's integration with databases, file systems and other services. Narrow integration tests cover one integration point at a time, for example by starting a database, writing through the application and checking the stored data; they belong wherever data is serialised or deserialised, such as [[rest|REST]] calls, queues and file I/O (Vocke, 2018). A faked external service can drift away from the real one. Contract tests close this gap: in consumer-driven contract testing, consumers publish tests describing what they need from an interface, and the provider runs them in its own pipeline; Pact is a common tool (Vocke, 2018). Interface design itself is covered in [[apis|APIs]].

#### 5. UI, end-to-end and acceptance tests

UI tests check behaviour, layout and usability and need not be end-to-end; single-page applications can unit test their components (Vocke, 2018), see [[frontend-development|frontend development]]. End-to-end tests run against the deployed system, through the browser or the API. They give the most confidence but are slow, costly to maintain and "notoriously flaky", so they are limited to a few critical user journeys (Vocke, 2018). Playwright Test is an end-to-end framework that "bundles test runner, assertions, isolation, parallelization and rich tooling", runs Chromium, WebKit and Firefox headless by default and can emulate mobile browsers (Playwright docs). Acceptance tests describe features from the user's perspective and can be written at any level of the pyramid; exploratory testing by people finds design and usability problems that automated tests miss (Vocke, 2018).

#### 6. pytest

pytest collects files named `test_*.py` or `*_test.py`, functions prefixed with `test_` and classes prefixed with `Test`; tests use the plain `assert` statement, and pytest's introspection reports the intermediate values when an assertion fails (pytest docs). `pytest.raises` checks for expected exceptions and `pytest.approx()` compares floating-point values. Fixtures are functions marked with `@pytest.fixture` that provide "a defined, reliable and consistent context for the tests": a test requests one by naming it as a parameter, fixtures can depend on other fixtures, can be reused across function, class, module or session scope, and can be parametrised (pytest fixtures). The built-in `tmp_path` fixture, for example, gives each test its own temporary directory (pytest docs). Python itself is covered in [[python|Python]].

#### 7. Testing ML systems

Breck et al. (2017) present 28 tests and monitoring needs from Google's production ML systems in four sections of seven: features and data (for example, feature expectations are captured in a schema and all input feature code is tested), model development (for example, offline proxy metrics correlate with the actual impact and a simpler model is not better), ML infrastructure (for example, training is reproducible, model specification code is unit tested, the full pipeline is integration tested and models can be rolled back quickly) and monitoring (for example, training and serving are not skewed and prediction quality has not regressed). Each test earns half a point if run manually with documented results and a full point if automated; the ML Test Score is the minimum over the four sections, so no area can be neglected (Breck et al., 2017). Outputs of LLM applications are checked with evaluation sets rather than exact assertions, see [[regression-testing|regression testing]] and [[llm-evaluation|LLM evaluation]].

#### Origin and variants

The pyramid goes back to Mike Cohn; Vocke's 2018 article on martinfowler.com reworks it for microservices with contract tests (Vocke, 2018). The test-double vocabulary comes from Gerard Meszaros's *xUnit Test Patterns* (Fowler, 2006). Breck et al. (2017) developed the ML Test Score for an internal ML Test Certified programme at Google, inspired by its Test Certified programme for general software.

### When to use it

- Every codebase that is changed by more than one person or over a longer period, and every project that integrates continuously (Vocke, 2018).
- Before refactoring: tests of observable behaviour show that the change kept the behaviour (Vocke, 2018).
- ML systems before production: the ML Test Score shows which of data, model, infrastructure and monitoring are under-tested (Breck et al., 2017).

### Strengths and limitations

**Strengths**
- Fast unit tests give feedback within seconds and pinpoint the failing code (Vocke, 2018).
- Contract tests let independent teams change services without slow end-to-end suites (Vocke, 2018).
- A quantified rubric makes ML testing debt visible and improvable over time (Breck et al., 2017).

**Limitations**
- Tests tied to implementation details break on every refactoring (Vocke, 2018).
- Fakes and stubs can drift from the real component; integration and contract tests are needed to catch it (Vocke, 2018).
- End-to-end tests are flaky and slow, and their ownership is unclear in microservice landscapes (Vocke, 2018).
- Test code needs the same care as production code; Vocke (2018) writes that "test code is as important as production code".

### Comparison

| Test type | Scope | Speed | Typical tools |
|---|---|---|---|
| Unit test | one function, method or class | milliseconds | pytest, JUnit |
| Integration test | one integration point (database, file, HTTP) | seconds | pytest with a test database, WireMock |
| Contract test | interface between consumer and provider | seconds | Pact |
| End-to-end test | whole deployed system through UI or API | minutes | Playwright, Selenium, REST-assured |
| ML tests | data, model, pipeline, monitoring | varies | data validation, canary releases |
| LLM evaluation | quality of generated outputs | minutes | evaluation sets, [[llm-as-a-judge\|LLM as a judge]] |

Sources: Vocke (2018); Breck et al. (2017); Playwright docs.

### In practice

The deployment pipeline orders tests by speed, not by type, so that fast unit and narrow integration tests run first and give quick feedback (Vocke, 2018). Each test checks one condition, and readability counts for more than avoiding repetition in test code (Vocke, 2018). Production systems should not be used as test partners, since tests clutter their logs or can overload them (Vocke, 2018). Among the 36 ML systems of Google teams that Breck et al. (2017) examined, the test for training/serving skew was perhaps the most important and one of the least frequently implemented, although such skew caused production issues for many teams. For long-lived code, missing tests are a form of [[technical-debt|technical debt]].

### Key takeaway

Automated tests are layered from many fast unit tests to few slow end-to-end tests, with test doubles for isolation and contract tests between services; ML systems additionally test their data, models, pipelines and monitoring.

### Sources

- Vocke, H. (2018). *The Practical Test Pyramid.* martinfowler.com, 26 February 2018. [martinfowler.com](https://martinfowler.com/articles/practical-test-pyramid.html)
- Fowler, M. (2006). *TestDouble.* martinfowler.com, 17 January 2006. [martinfowler.com](https://martinfowler.com/bliki/TestDouble.html)
- pytest docs. *Get Started.* [docs.pytest.org](https://docs.pytest.org/en/stable/getting-started.html)
- pytest fixtures. *About fixtures.* [docs.pytest.org](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- Playwright docs. *Installation.* [playwright.dev](https://playwright.dev/docs/intro)
- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* Proceedings of IEEE Big Data 2017. [research.google](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Automatisierte Softwaretests prüfen, ob sich Code wie beabsichtigt verhält, und prüfen das bei jeder Änderung erneut; damit sind sie die Grundlage von [[ci-cd|CI/CD]] und Refactoring. Die Testpyramide ordnet sie nach Granularität: viele schnelle Unit-Tests unten, weniger Integrations- und Contract-Tests in der Mitte und nur wenige langsame End-to-End-Tests über die Benutzeroberfläche oben (Vocke, 2018). Test Doubles wie Stubs und Mocks ersetzen echte Kollaborateure, damit Tests schnell und isoliert bleiben (Fowler, 2006). In Python ist pytest das verbreitete Framework; Playwright steuert echte Browser für End-to-End-Tests von Webanwendungen (pytest docs; Playwright docs). ML-Systeme brauchen zusätzliche Tests für Daten, Modelle und [[monitoring-and-alerting|Monitoring]], die Breck et al. (2017) im [[ml-test-score|ML Test Score]] zusammenfassen.

### Funktionsweise

```text
            /\        End-to-End- / UI-Tests      wenige, langsam, breit, instabil
           /  \       Contract-Tests              Schnittstellen zwischen Diensten
          /    \      Integrationstests           je ein Integrationspunkt
         /______\     Unit-Tests                  viele, schnell, isoliert
 jeder Test: Arrange → Act → Assert (Given → When → Then)
 in der Deployment-Pipeline nach Geschwindigkeit angeordnet: schnelle Tests zuerst
```

#### 1. Die Testpyramide

Die Pyramide stammt aus Mike Cohns *Succeeding with Agile* und hatte ursprünglich Unit-, Service- und UI-Tests (Vocke, 2018). Ihre Bezeichnungen sind vereinfachend, aber zwei Regeln gelten: Tests mit unterschiedlicher Granularität schreiben, und „the more high-level you get the fewer tests you should have“. Die umgekehrte Form, die „Test-Eistüte“ mit vielen High-Level-Tests, ist langsam und schwer zu pflegen. Zwei weitere Regeln vermeiden doppelten Aufwand: Findet ein High-Level-Test einen Fehler, den kein Test darunter erkennt, wird ein Test auf niedrigerer Ebene ergänzt, und Tests werden so weit unten in der Pyramide angesiedelt wie möglich (Vocke, 2018).

#### 2. Unit-Tests

Was als Unit gilt, ist flexibel: eine Funktion, eine Methode oder eine Klasse. Solitäre Unit-Tests ersetzen alle Kollaborateure durch Test Doubles, soziale Unit-Tests nutzen die echten Kollaborateure; beide haben ihren Platz (Vocke, 2018). Unit-Tests meiden Datenbanken, Dateisystem und Netzwerkaufrufe, um schnell zu bleiben. Sie testen die öffentliche Schnittstelle und beobachtbares Verhalten statt der inneren Struktur, damit Refactoring sie nicht bricht; wer eine private Methode testen möchte, hat meist eine Klasse, die zu viel tut. Jeder Test folgt Arrange, Act, Assert bzw. Given, When, Then (Vocke, 2018).

#### 3. Test Doubles

„Test Double is a generic term for any case where you replace a production object for testing purposes“ (Fowler, 2006, nach Gerard Meszaros). Es gibt fünf Arten:
- **Dummy:** wird weitergereicht, aber nie benutzt, typischerweise zum Füllen von Parameterlisten.
- **Fake:** eine funktionierende Implementierung mit Abkürzungen, die sie für die Produktion ungeeignet machen.
- **Stub:** liefert vorgefertigte Antworten auf die Aufrufe im Test.
- **Spy:** ein Stub, der zusätzlich festhält, wie er aufgerufen wurde.
- **Mock:** ist mit Erwartungen vorprogrammiert, die festlegen, welche Aufrufe er erhalten soll.

#### 4. Integrations- und Contract-Tests

Integrationstests prüfen die Anbindung des Codes an Datenbanken, Dateisysteme und andere Dienste. Schmale Integrationstests decken jeweils einen Integrationspunkt ab, etwa indem sie eine Datenbank starten, über die Anwendung schreiben und die gespeicherten Daten prüfen; sie gehören überall dorthin, wo Daten serialisiert oder deserialisiert werden, etwa bei REST-Aufrufen, Queues und Datei-I/O (Vocke, 2018). Ein simulierter externer Dienst kann vom echten abweichen. Contract-Tests schließen diese Lücke: Beim Consumer-Driven Contract Testing veröffentlichen die Nutzer einer Schnittstelle Tests, die beschreiben, was sie brauchen, und der Anbieter führt sie in seiner eigenen Pipeline aus; ein verbreitetes Werkzeug ist Pact (Vocke, 2018). Den Entwurf von Schnittstellen behandelt [[apis|APIs]].

#### 5. UI-, End-to-End- und Akzeptanztests

UI-Tests prüfen Verhalten, Layout und Benutzbarkeit und müssen nicht End-to-End sein; Single-Page-Anwendungen können ihre Komponenten mit Unit-Tests prüfen (Vocke, 2018), siehe [[frontend-development|Frontend-Entwicklung]]. End-to-End-Tests laufen gegen das ausgelieferte System, über den Browser oder die API. Sie geben die meiste Sicherheit, sind aber langsam, teuer in der Pflege und „notoriously flaky“, daher beschränkt man sie auf wenige kritische Nutzerwege (Vocke, 2018). Playwright Test ist ein End-to-End-Framework, das „bundles test runner, assertions, isolation, parallelization and rich tooling“, standardmäßig Chromium, WebKit und Firefox ohne sichtbares Fenster ausführt und mobile Browser emulieren kann (Playwright docs). Akzeptanztests beschreiben Features aus Sicht der Nutzenden und können auf jeder Ebene der Pyramide geschrieben werden; exploratives Testen durch Menschen findet Design- und Bedienprobleme, die automatisierte Tests übersehen (Vocke, 2018).

#### 6. pytest

pytest sammelt Dateien namens `test_*.py` oder `*_test.py`, Funktionen mit dem Präfix `test_` und Klassen mit dem Präfix `Test`; Tests nutzen die einfache `assert`-Anweisung, und pytest zeigt bei einer fehlgeschlagenen Prüfung die Zwischenwerte an (pytest docs). `pytest.raises` prüft erwartete Exceptions, `pytest.approx()` vergleicht Gleitkommawerte. Fixtures sind mit `@pytest.fixture` markierte Funktionen, die „a defined, reliable and consistent context for the tests“ bereitstellen: Ein Test fordert eine Fixture an, indem er sie als Parameter nennt; Fixtures können von anderen Fixtures abhängen, über Funktion, Klasse, Modul oder Sitzung wiederverwendet und parametrisiert werden (pytest fixtures). Die eingebaute Fixture `tmp_path` gibt etwa jedem Test ein eigenes temporäres Verzeichnis (pytest docs). Python selbst behandelt [[python|Python]].

#### 7. ML-Systeme testen

Breck et al. (2017) stellen 28 Tests und Monitoring-Anforderungen aus den produktiven ML-Systemen von Google vor, in vier Abschnitten zu je sieben: Features und Daten (etwa: Erwartungen an Features sind in einem Schema festgehalten, und aller Code für Eingabefeatures ist getestet), Modellentwicklung (etwa: Offline-Ersatzmetriken korrelieren mit der tatsächlichen Wirkung, und ein einfacheres Modell ist nicht besser), ML-Infrastruktur (etwa: Training ist reproduzierbar, Code der Modellspezifikation hat Unit-Tests, die gesamte Pipeline hat Integrationstests, und Modelle lassen sich schnell zurückrollen) und Monitoring (etwa: Training und Serving weichen nicht voneinander ab, und die Vorhersagequalität hat sich nicht verschlechtert). Jeder Test bringt einen halben Punkt, wenn er manuell mit dokumentierten Ergebnissen ausgeführt wird, und einen ganzen Punkt, wenn er automatisiert ist; der ML Test Score ist das Minimum über die vier Abschnitte, sodass kein Bereich vernachlässigt werden kann (Breck et al., 2017). Ausgaben von LLM-Anwendungen werden mit Evaluationssets statt exakter Assertions geprüft, siehe [[regression-testing|Regressionstests]] und [[llm-evaluation|LLM-Evaluation]].

#### Herkunft und Varianten

Die Pyramide geht auf Mike Cohn zurück; Vockes Artikel von 2018 auf martinfowler.com überarbeitet sie für Microservices mit Contract-Tests (Vocke, 2018). Das Vokabular der Test Doubles stammt aus Gerard Meszaros' *xUnit Test Patterns* (Fowler, 2006). Breck et al. (2017) entwickelten den ML Test Score für ein internes ML-Test-Certified-Programm bei Google, angelehnt an dessen Test-Certified-Programm für allgemeine Software.

### Wann einsetzen

- In jeder Codebasis, die von mehr als einer Person oder über längere Zeit geändert wird, und in jedem Projekt mit Continuous Integration (Vocke, 2018).
- Vor einem Refactoring: Tests des beobachtbaren Verhaltens zeigen, dass die Änderung das Verhalten erhalten hat (Vocke, 2018).
- Bei ML-Systemen vor dem Produktivgang: Der ML Test Score zeigt, welcher Bereich aus Daten, Modell, Infrastruktur und Monitoring zu wenig getestet ist (Breck et al., 2017).

### Stärken und Grenzen

**Stärken**
- Schnelle Unit-Tests geben innerhalb von Sekunden Rückmeldung und zeigen genau auf den fehlerhaften Code (Vocke, 2018).
- Contract-Tests erlauben unabhängigen Teams, Dienste ohne langsame End-to-End-Suites zu ändern (Vocke, 2018).
- Ein quantifiziertes Bewertungsschema macht Testschulden bei ML sichtbar und über die Zeit verbesserbar (Breck et al., 2017).

**Grenzen**
- Tests, die an Implementierungsdetails hängen, brechen bei jedem Refactoring (Vocke, 2018).
- Fakes und Stubs können vom echten Bestandteil abweichen; Integrations- und Contract-Tests sind nötig, um das zu bemerken (Vocke, 2018).
- End-to-End-Tests sind instabil und langsam, und ihre Zuständigkeit ist in Microservice-Landschaften unklar (Vocke, 2018).
- Testcode braucht dieselbe Sorgfalt wie Produktionscode; Vocke (2018) schreibt, „test code is as important as production code“.

### Vergleich

| Testart | Umfang | Geschwindigkeit | Typische Werkzeuge |
|---|---|---|---|
| Unit-Test | eine Funktion, Methode oder Klasse | Millisekunden | pytest, JUnit |
| Integrationstest | ein Integrationspunkt (Datenbank, Datei, [[http\|HTTP]]) | Sekunden | pytest mit Testdatenbank, WireMock |
| Contract-Test | Schnittstelle zwischen Nutzer und Anbieter | Sekunden | Pact |
| End-to-End-Test | gesamtes ausgeliefertes System über UI oder API | Minuten | Playwright, Selenium, REST-assured |
| ML-Tests | Daten, Modell, Pipeline, Monitoring | unterschiedlich | Datenvalidierung, Canary Releases |
| LLM-Evaluation | Qualität generierter Ausgaben | Minuten | Evaluationssets, [[llm-as-a-judge\|LLM as a Judge]] |

Quellen: Vocke (2018); Breck et al. (2017); Playwright docs.

### In der Praxis

Die Deployment-Pipeline ordnet Tests nach Geschwindigkeit, nicht nach Art, sodass schnelle Unit-Tests und schmale Integrationstests zuerst laufen und schnell Rückmeldung geben (Vocke, 2018). Jeder Test prüft eine Bedingung, und Lesbarkeit zählt im Testcode mehr als das Vermeiden von Wiederholungen (Vocke, 2018). Produktivsysteme sollten nicht als Testpartner dienen, weil Tests ihre Logs füllen oder sie überlasten können (Vocke, 2018). Unter den 36 ML-Systemen von Google-Teams, die Breck et al. (2017) untersuchten, war der Test auf Abweichungen zwischen Training und Serving womöglich der wichtigste und zugleich einer der am seltensten umgesetzten, obwohl solche Abweichungen bei vielen Teams Produktionsprobleme verursachten. Bei langlebigem Code sind fehlende Tests eine Form von [[technical-debt|technischen Schulden]].

### Merksatz

Automatisierte Tests sind geschichtet, von vielen schnellen Unit-Tests bis zu wenigen langsamen End-to-End-Tests, mit Test Doubles zur Isolation und Contract-Tests zwischen Diensten; ML-Systeme testen zusätzlich ihre Daten, Modelle, Pipelines und ihr Monitoring.

### Quellen

- Vocke, H. (2018). *The Practical Test Pyramid.* martinfowler.com, 26. Februar 2018. [martinfowler.com](https://martinfowler.com/articles/practical-test-pyramid.html)
- Fowler, M. (2006). *TestDouble.* martinfowler.com, 17. Januar 2006. [martinfowler.com](https://martinfowler.com/bliki/TestDouble.html)
- pytest docs. *Get Started.* [docs.pytest.org](https://docs.pytest.org/en/stable/getting-started.html)
- pytest fixtures. *About fixtures.* [docs.pytest.org](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- Playwright docs. *Installation.* [playwright.dev](https://playwright.dev/docs/intro)
- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.* Proceedings of IEEE Big Data 2017. [research.google](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
