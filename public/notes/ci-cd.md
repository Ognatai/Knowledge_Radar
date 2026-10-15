---
title_en: CI/CD (Continuous Integration and Continuous Delivery)
title_de: CI/CD (Continuous Integration und Continuous Delivery)
entity_type: Method
aliases:
- CI/CD
- Continuous Integration
- Continuous Delivery
- Continuous Deployment
- Deployment pipeline
- CI pipeline
sources:
- https://martinfowler.com/articles/continuousIntegration.html
- https://continuousdelivery.com/
- https://docs.github.com/en/actions/get-started/understand-github-actions
- https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/key-pipelines-concepts
- https://dora.dev/guides/dora-metrics/
- https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Continuous integration (CI) is the practice of every team member merging their changes into a shared mainline at least daily, with each merge checked by an automated build that includes tests, so that integration errors surface within minutes instead of in a late integration phase (Fowler, 2024). Continuous delivery (CD) extends this so that the product is always in a releasable state and changes of all types reach production "safely and quickly in a sustainable way" (Humble, n.d.); continuous deployment goes one step further and releases every change that passes all automated checks (Fowler, 2024). Platforms such as GitHub Actions and Azure Pipelines run these steps as YAML-defined pipelines (GitHub Docs; Microsoft Learn). For ML systems, CI also tests data and models, and CD deploys a training pipeline rather than a single package (Google Cloud).

### How it works

```text
developer commits to mainline (several times a day)
 ▼
trigger: push, pull request, schedule or manual start
 ▼
commit build: compile, unit tests, static checks   (≈ 10 minutes)
 ▼
artefact: package or container image, stored once
 ▼
later stages: integration / end-to-end / performance tests in a production-like environment
 ▼
release gate: approval or automated checks
 ▼
deployment: staging → production (blue-green, canary, rolling) → monitoring
```

#### 1. Mainline integration

CI rests on a single version-controlled mainline that holds everything needed to build and run the product: code, scripts, database schemas, configuration and references to tools, but not build outputs (Fowler, 2024). Everyone pushes to the mainline at least once a day; [[kent-beck|Kent Beck]]'s guideline is that no code sits unintegrated for more than a couple of hours. Small, frequent integrations keep conflicts small; Fowler (2024) calls long-lived feature branches "semi-integration" and treats CI and feature branching as mutually exclusive, except for features finished within a day. Unfinished work is integrated but hidden, for example behind feature flags, keystone interfaces or branch by abstraction (Fowler, 2024). Pull-request reviews that take hours or days break this rhythm; pair programming, the Ship/Show/Ask approach or review after integration are alternatives (Fowler, 2024). Branching itself is covered in [[git|Git]].

#### 2. The self-testing build

The build runs from a single command and includes an automated test suite strong enough that a deliberately introduced bug makes it fail; Fowler (2024) names test skill as the biggest barrier to adopting CI. Every push to the mainline triggers a build in a reference environment, and a broken mainline is the team's top priority, usually fixed fastest by reverting the commit. The commit build should take about ten minutes, so it uses test doubles and skips slow checks; slower tests, for instance end-to-end tests against real databases, run in later stages (Fowler, 2024). Test types are described in [[software-testing|software testing]].

#### 3. The deployment pipeline

A deployment pipeline is a sequence of builds in which each stage gains confidence that a change is releasable (Fowler, 2024). Later stages run in a clone of the production environment; containers ([[docker|Docker]]) make this practical. When a later stage finds a bug, a test for it is added to the commit build. The build artefact is produced once and promoted through the stages: Azure Pipelines describes artefacts as files or packages published by a run and consumed by later deployment tasks (Microsoft Learn). Approvals and checks pause a run before a protected environment such as production until they pass (Microsoft Learn).

#### 4. Pipeline platforms

Both major hosted platforms share the same structure:

| Concept | GitHub Actions | Azure Pipelines |
|---|---|---|
| Definition | YAML workflow in `.github/workflows` | YAML pipeline (or the Classic editor) |
| Start | event (push, pull request, issue), schedule, [[rest\|REST]] call, manual | trigger: push, schedule, completion of another build, manual |
| Grouping | jobs (parallel unless they declare dependencies) | stages (sequential by default) containing jobs |
| Smallest unit | step: shell script or reusable action | step: script or prepackaged task |
| Executor | runner: GitHub-hosted VM or self-hosted | agent: Microsoft-hosted or self-hosted |

A GitHub Actions workflow is "a configurable automated process that will run one or more jobs"; a job is a set of steps executed on the same runner, and a matrix runs the same job across operating systems or language versions (GitHub Docs). In Azure Pipelines a stage marks a boundary such as build, test or production, and deployment jobs can use `runOnce`, `rolling` or `canary` strategies (Microsoft Learn).

#### 5. Delivery and deployment

Continuous delivery means "the product should always be in a state where we can release the latest build", which turns releasing into a business decision; continuous deployment releases every change that passes the pipeline and requires continuous delivery as a prerequisite (Fowler, 2024). Deployment is scripted for every environment, and blue-green deployment or automated rollback make frequent releases safe (Fowler, 2024; Humble, n.d.). Humble's heuristic for the whole approach is "if it hurts, do it more often, and bring the pain forward" (Humble, n.d.). The cloud resources a pipeline deploys to are themselves best defined in code, see [[infrastructure-as-code|infrastructure as code]].

#### 6. CI/CD for machine learning

ML changes three things (Google Cloud): CI tests and validates data, schemas and models as well as code; CD deploys a training pipeline that produces models instead of a single service; and continuous training (CT) retrains and serves models automatically. CI for ML adds unit tests for [[feature-engineering|feature engineering]] and model methods, convergence tests (the loss decreases and the model can overfit a few records), checks against NaN values and integration tests between pipeline components. CD adds checks that the serving infrastructure has the required packages, memory and accelerators, tests of the prediction service API, load tests for queries per second and latency, and performance gates before a model is promoted (Google Cloud). The pipelines themselves are covered in [[ml-pipelines|ML pipelines]], versioning and serving in [[mlops-and-deployment|MLOps and deployment]].

#### Origin and variants

Kent Beck developed CI in the 1990s as part of Extreme Programming; Grady Booch used the term only as an offhand description, and Microsoft's daily builds lacked the testing and immediate fixing that define CI (Fowler, 2024). Fowler's article first appeared in 2000 and was rewritten in 2006 and 2024. Humble and Farley's book *Continuous Delivery* (2010) generalised the approach, and the DORA research programme measures its effect (Humble, n.d.; DORA).

### When to use it

- A team of committed, full-time developers works on a shared codebase and wants integration to be routine rather than a project phase (Fowler, 2024).
- Releases should become predictable, frequent events that can happen on demand (Humble, n.d.).
- ML models need regular retraining or many pipeline changes, which calls for automated pipeline delivery (Google Cloud).

### Strengths and limitations

**Strengths**
- Removes delivery risk because each integration is small; Fowler (2024) writes that CI "effectively eliminates delivery risk".
- Bugs are found close to the change that caused them, and frequent integration makes [[refactoring|refactoring]] practical (Fowler, 2024).
- Speed and stability are not trade-offs: DORA reports that top performers do well on all its delivery metrics (DORA).

**Limitations**
- Depends on a strong automated test suite and discipline; without them, CI does not work (Fowler, 2024).
- Fits open-source projects with occasional, part-time contributors poorly (Fowler, 2024).
- Slow builds, often caused by tests against external services, discourage frequent commits (Fowler, 2024).

### Comparison

| Approach | Integration | Release |
|---|---|---|
| Pre-release integration | once, late in the project | after a long integration phase |
| Feature branches | when a feature is complete | variable |
| Continuous integration | daily or more often, on the mainline | not prescribed |
| Continuous delivery | as CI | any build can be released on decision |
| Continuous deployment | as CI | every passing build goes live automatically |

Sources: Fowler (2024). Related operational practices: [[mlops-and-deployment|MLOps and deployment]], [[regression-testing|regression testing]] for model outputs, [[monitoring-and-alerting|monitoring and alerting]] after deployment.

### In practice

DORA measures delivery performance with five metrics at the level of an application or service: change lead time, deployment frequency and failed deployment recovery time for throughput, and change fail rate and deployment rework rate for instability; DORA advises against comparing these numbers across teams with different contexts (DORA). Build status should be visible to everyone, for example on a dashboard or in chat (Fowler, 2024). Azure Pipelines keeps values and secrets in variable groups and secure files that pipelines reference, instead of in the pipeline definition (Microsoft Learn). For LLM applications, a pipeline stage that runs an evaluation set before release catches quality regressions that unit tests miss ([[regression-testing|regression testing]], [[llm-evaluation|LLM evaluation]]).

### Key takeaway

CI/CD keeps the mainline integrated and tested within minutes of every change and moves each build through an automated pipeline, so that releasing becomes a routine business decision; for ML, the pipeline also validates data and models and delivers training pipelines.

### Sources

- Fowler, M. (2024). *Continuous Integration.* martinfowler.com, revised 18 January 2024 (first published 2000). [martinfowler.com](https://martinfowler.com/articles/continuousIntegration.html)
- Humble, J. (n.d.). *Continuous Delivery.* continuousdelivery.com. [continuousdelivery.com](https://continuousdelivery.com/)
- GitHub Docs. *Understanding GitHub Actions.* [docs.github.com](https://docs.github.com/en/actions/get-started/understand-github-actions)
- Microsoft Learn. *Key Azure Pipelines concepts.* Updated March 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/key-pipelines-concepts)
- DORA. *DORA's software delivery performance metrics.* [dora.dev](https://dora.dev/guides/dora-metrics/)
- Google Cloud. *MLOps: Continuous delivery and automation pipelines in machine learning.* Cloud Architecture Center. [docs.cloud.google.com](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Continuous Integration (CI) ist die Praxis, dass alle Teammitglieder ihre Änderungen mindestens täglich in eine gemeinsame Mainline zusammenführen und jede Zusammenführung von einem automatisierten Build mit Tests geprüft wird, sodass Integrationsfehler innerhalb von Minuten statt in einer späten Integrationsphase auffallen (Fowler, 2024). Continuous Delivery (CD) erweitert das so, dass sich das Produkt jederzeit in einem auslieferbaren Zustand befindet und Änderungen aller Art „safely and quickly in a sustainable way“ in Produktion gelangen (Humble, o. J.); Continuous Deployment geht einen Schritt weiter und liefert jede Änderung aus, die alle automatisierten Prüfungen besteht (Fowler, 2024). Plattformen wie GitHub Actions und Azure Pipelines führen diese Schritte als in YAML definierte Pipelines aus (GitHub Docs; Microsoft Learn). Bei ML-Systemen testet CI zusätzlich Daten und Modelle, und CD liefert eine Trainingspipeline statt eines einzelnen Pakets aus (Google Cloud).

### Funktionsweise

```text
Entwicklerin oder Entwickler committet in die Mainline (mehrmals täglich)
 ▼
Trigger: Push, Pull Request, Zeitplan oder manueller Start
 ▼
Commit-Build: Kompilieren, Unit-Tests, statische Prüfungen   (≈ 10 Minuten)
 ▼
Artefakt: Paket oder Container-Image, einmal erzeugt und abgelegt
 ▼
spätere Stufen: Integrations-, End-to-End- und Performancetests in produktionsnaher Umgebung
 ▼
Freigabe: Genehmigung oder automatisierte Prüfungen
 ▼
Deployment: Staging → Produktion (Blue-Green, Canary, Rolling) → Monitoring
```

#### 1. Integration in die Mainline

CI beruht auf einer einzigen versionierten Mainline, die alles enthält, was zum Bauen und Ausführen des Produkts nötig ist: Code, Skripte, Datenbankschemata, Konfiguration und Verweise auf Werkzeuge, aber keine Build-Ergebnisse (Fowler, 2024). Alle pushen mindestens einmal täglich in die Mainline; Kent Becks Richtwert ist, dass kein Code länger als ein paar Stunden unintegriert bleibt. Kleine, häufige Integrationen halten Konflikte klein; Fowler (2024) nennt langlebige Feature-Branches „Semi-Integration“ und betrachtet CI und Feature-Branching als einander ausschließend, außer bei Features, die innerhalb eines Tages fertig werden. Unfertige Arbeit wird integriert, aber verborgen, etwa hinter Feature Flags, Keystone Interfaces oder per Branch by Abstraction (Fowler, 2024). Pull-Request-Reviews, die Stunden oder Tage dauern, unterbrechen diesen Rhythmus; Pair Programming, der Ship/Show/Ask-Ansatz oder Reviews nach der Integration sind Alternativen (Fowler, 2024). Branching selbst behandelt [[git|Git]].

#### 2. Der selbsttestende Build

Der Build läuft mit einem einzigen Befehl und enthält eine automatisierte Testsuite, die stark genug ist, dass ein absichtlich eingebauter Fehler sie fehlschlagen lässt; Fowler (2024) nennt fehlende Testkompetenz als größtes Hindernis für die Einführung von CI. Jeder Push in die Mainline löst einen Build in einer Referenzumgebung aus, und eine kaputte Mainline hat für das Team höchste Priorität; meist ist das Zurücknehmen des Commits der schnellste Weg. Der Commit-Build sollte etwa zehn Minuten dauern und nutzt daher Test Doubles und lässt langsame Prüfungen aus; langsamere Tests, etwa End-to-End-Tests gegen echte Datenbanken, laufen in späteren Stufen (Fowler, 2024). Die Testarten beschreibt [[software-testing|Softwaretests]].

#### 3. Die Deployment-Pipeline

Eine Deployment-Pipeline ist eine Folge von Builds, in der jede Stufe mehr Sicherheit schafft, dass eine Änderung auslieferbar ist (Fowler, 2024). Spätere Stufen laufen in einer Kopie der Produktionsumgebung; Container ([[docker|Docker]]) machen das praktikabel. Findet eine spätere Stufe einen Fehler, wird ein Test dafür in den Commit-Build aufgenommen. Das Build-Artefakt wird einmal erzeugt und durch die Stufen weitergereicht: Azure Pipelines beschreibt Artefakte als Dateien oder Pakete, die ein Lauf veröffentlicht und spätere Deployment-Tasks verwenden (Microsoft Learn). Genehmigungen und Prüfungen halten einen Lauf vor einer geschützten Umgebung wie der Produktion an, bis sie bestanden sind (Microsoft Learn).

#### 4. Pipeline-Plattformen

Beide großen gehosteten Plattformen haben denselben Aufbau:

| Konzept | GitHub Actions | Azure Pipelines |
|---|---|---|
| Definition | YAML-Workflow in `.github/workflows` | YAML-Pipeline (oder der Classic-Editor) |
| Start | Event (Push, Pull Request, Issue), Zeitplan, REST-Aufruf, manuell | Trigger: Push, Zeitplan, Abschluss eines anderen Builds, manuell |
| Gruppierung | Jobs (parallel, sofern sie keine Abhängigkeiten angeben) | Stages (standardmäßig nacheinander) mit Jobs |
| Kleinste Einheit | Step: Shell-Skript oder wiederverwendbare Action | Step: Skript oder vorgefertigter Task |
| Ausführung | Runner: von GitHub gehostete VM oder selbst gehostet | Agent: von Microsoft gehostet oder selbst gehostet |

Ein GitHub-Actions-Workflow ist „a configurable automated process that will run one or more jobs“; ein Job ist eine Folge von Steps auf demselben Runner, und eine Matrix führt denselben Job über mehrere Betriebssysteme oder Sprachversionen aus (GitHub Docs). In Azure Pipelines markiert eine Stage eine Grenze wie Build, Test oder Produktion, und Deployment-Jobs können die Strategien `runOnce`, `rolling` oder `canary` nutzen (Microsoft Learn).

#### 5. Delivery und Deployment

Continuous Delivery bedeutet, dass „the product should always be in a state where we can release the latest build“, wodurch die Auslieferung zu einer geschäftlichen Entscheidung wird; Continuous Deployment liefert jede Änderung aus, die die Pipeline besteht, und setzt Continuous Delivery voraus (Fowler, 2024). Das Deployment ist für jede Umgebung skriptgesteuert, und Blue-Green-Deployments oder automatisches Rollback machen häufige Auslieferungen sicher (Fowler, 2024; Humble, o. J.). Humbles Faustregel für den ganzen Ansatz lautet „if it hurts, do it more often, and bring the pain forward“ (Humble, o. J.). Die Cloud-Ressourcen, in die eine Pipeline ausliefert, werden am besten selbst als Code definiert, siehe [[infrastructure-as-code|Infrastructure as Code]].

#### 6. CI/CD für Machine Learning

ML verändert drei Dinge (Google Cloud): CI testet und validiert neben Code auch Daten, Schemata und Modelle; CD liefert eine Trainingspipeline aus, die Modelle erzeugt, statt eines einzelnen Dienstes; und Continuous Training (CT) trainiert Modelle automatisch neu und stellt sie bereit. CI für ML ergänzt Unit-Tests für [[feature-engineering|Feature Engineering]] und Modellmethoden, Konvergenztests (der Loss sinkt, und das Modell kann wenige Datensätze überanpassen), Prüfungen auf NaN-Werte und Integrationstests zwischen Pipeline-Komponenten. CD ergänzt Prüfungen, ob die Serving-Infrastruktur die nötigen Pakete, Speicher und Beschleuniger hat, Tests der API des Vorhersagedienstes, Lasttests für Anfragen pro Sekunde und Latenz sowie Performance-Schwellen, bevor ein Modell weitergegeben wird (Google Cloud). Die Pipelines selbst behandelt [[ml-pipelines|ML-Pipelines]], Versionierung und Serving [[mlops-and-deployment|MLOps und Deployment]].

#### Herkunft und Varianten

[[kent-beck|Kent Beck]] entwickelte CI in den 1990er-Jahren als Teil von Extreme Programming; Grady Booch verwendete den Begriff nur beiläufig, und den täglichen Builds bei Microsoft fehlten die Tests und die sofortige Fehlerbehebung, die CI ausmachen (Fowler, 2024). Fowlers Artikel erschien erstmals 2000 und wurde 2006 und 2024 neu geschrieben. Das Buch *Continuous Delivery* von Humble und Farley (2010) verallgemeinerte den Ansatz, und das Forschungsprogramm DORA misst seine Wirkung (Humble, o. J.; DORA).

### Wann einsetzen

- Ein Team engagierter Vollzeitentwicklerinnen und -entwickler arbeitet an einer gemeinsamen Codebasis und will die Integration zur Routine statt zu einer Projektphase machen (Fowler, 2024).
- Releases sollen zu planbaren, häufigen Ereignissen werden, die bei Bedarf stattfinden können (Humble, o. J.).
- ML-Modelle müssen regelmäßig neu trainiert werden oder Pipelines ändern sich oft, was eine automatisierte Auslieferung der Pipelines erfordert (Google Cloud).

### Stärken und Grenzen

**Stärken**
- Beseitigt Auslieferungsrisiken, weil jede Integration klein ist; Fowler (2024) schreibt, CI „effectively eliminates delivery risk“.
- Fehler werden nahe an der verursachenden Änderung gefunden, und häufige Integration macht [[refactoring|Refactoring]] praktikabel (Fowler, 2024).
- Geschwindigkeit und Stabilität sind kein Zielkonflikt: Laut DORA schneiden die besten Teams bei allen Auslieferungsmetriken gut ab (DORA).

**Grenzen**
- Setzt eine starke automatisierte Testsuite und Disziplin voraus; ohne sie funktioniert CI nicht (Fowler, 2024).
- Passt schlecht zu Open-Source-Projekten mit gelegentlichen Beiträgen in Teilzeit (Fowler, 2024).
- Langsame Builds, oft verursacht durch Tests gegen externe Dienste, halten von häufigen Commits ab (Fowler, 2024).

### Vergleich

| Ansatz | Integration | Auslieferung |
|---|---|---|
| Integration vor dem Release | einmal, spät im Projekt | nach einer langen Integrationsphase |
| Feature-Branches | wenn ein Feature fertig ist | unterschiedlich |
| Continuous Integration | täglich oder öfter, in die Mainline | nicht festgelegt |
| Continuous Delivery | wie CI | jeder Build kann auf Entscheidung ausgeliefert werden |
| Continuous Deployment | wie CI | jeder bestandene Build geht automatisch live |

Quelle: Fowler (2024). Verwandte Betriebspraktiken: [[mlops-and-deployment|MLOps und Deployment]], [[regression-testing|Regressionstests]] für Modellausgaben, [[monitoring-and-alerting|Monitoring und Alerting]] nach dem Deployment.

### In der Praxis

DORA misst die Auslieferungsleistung mit fünf Metriken auf Ebene einer Anwendung oder eines Dienstes: Change Lead Time, Deployment-Häufigkeit und Wiederherstellungszeit nach fehlgeschlagenen Deployments für den Durchsatz sowie Change Fail Rate und Deployment Rework Rate für die Instabilität; DORA rät davon ab, diese Werte zwischen Teams mit unterschiedlichem Kontext zu vergleichen (DORA). Der Build-Status sollte für alle sichtbar sein, etwa auf einem Dashboard oder im Chat (Fowler, 2024). Azure Pipelines hält Werte und Secrets in Variablengruppen und Secure Files, auf die Pipelines verweisen, statt in der Pipeline-Definition (Microsoft Learn). Bei LLM-Anwendungen fängt eine Pipeline-Stufe, die vor dem Release ein Evaluationsset ausführt, Qualitätsrückschritte ab, die Unit-Tests übersehen ([[regression-testing|Regressionstests]], [[llm-evaluation|LLM-Evaluation]]).

### Merksatz

CI/CD hält die Mainline innerhalb von Minuten nach jeder Änderung integriert und getestet und führt jeden Build durch eine automatisierte Pipeline, sodass die Auslieferung zu einer routinemäßigen geschäftlichen Entscheidung wird; bei ML validiert die Pipeline zusätzlich Daten und Modelle und liefert Trainingspipelines aus.

### Quellen

- Fowler, M. (2024). *Continuous Integration.* martinfowler.com, überarbeitet am 18. Januar 2024 (erstmals 2000). [martinfowler.com](https://martinfowler.com/articles/continuousIntegration.html)
- Humble, J. (o. J.). *Continuous Delivery.* continuousdelivery.com. [continuousdelivery.com](https://continuousdelivery.com/)
- GitHub Docs. *Understanding GitHub Actions.* [docs.github.com](https://docs.github.com/en/actions/get-started/understand-github-actions)
- Microsoft Learn. *Key Azure Pipelines concepts.* Aktualisiert im März 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/key-pipelines-concepts)
- DORA. *DORA's software delivery performance metrics.* [dora.dev](https://dora.dev/guides/dora-metrics/)
- Google Cloud. *MLOps: Continuous delivery and automation pipelines in machine learning.* Cloud Architecture Center. [docs.cloud.google.com](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
