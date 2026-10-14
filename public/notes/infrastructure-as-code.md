---
title_en: Infrastructure as Code
title_de: Infrastructure as Code
entity_type: Method
aliases:
- Infrastructure as Code
- IaC
sources:
- https://martinfowler.com/bliki/InfrastructureAsCode.html
- https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code
- https://developer.hashicorp.com/terraform/intro
- https://developer.hashicorp.com/terraform/language/state/purpose
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Infrastructure as code (IaC) is "the approach to defining computing and network infrastructure through source code", so that servers, networks and other resources can be versioned, reviewed, tested and delivered like any other software (Fowler, 2016). A versioned definition produces the same environment on every deployment, just as the same source code produces the same binary, which removes the drift that turns manually maintained environments into irreproducible "snowflakes" (Microsoft Learn). Declarative tools such as Terraform, Azure Resource Manager templates and Bicep describe the desired end state and work out the changes needed to reach it (HashiCorp; Microsoft Learn).

### How it works

```text
definition files in version control (desired state)
 ▼
review and automated checks in the pipeline
 ▼
plan: compare desired state with recorded state and the real resources
 ▼
apply: create / update / destroy resources via provider APIs, in dependency order
 ▼
state updated; the next change starts again from the definition, never from the live system
```

#### 1. Definition files instead of manual changes

All configuration lives in executable definition files; "at no time should anyone log into a server and make on-the-fly adjustments", because such changes produce servers that cannot be reproduced (Fowler, 2016). Teams change the source, not the target (Microsoft Learn). The code doubles as documentation that is more reliable than written instructions, and version control records every change for audit (Fowler, 2016).

#### 2. Declarative and imperative definitions

A declarative definition states which components and configuration an environment needs, not how to install them; this leaves the provider room for optimised techniques and avoids the [[technical-debt|technical debt]] of growing deployment scripts (Microsoft Learn). Terraform configuration is declarative in this sense: it describes the end state, and Terraform handles the steps (HashiCorp). Imperative scripts and configuration management tools such as Ansible playbooks, Chef recipes and Puppet manifests are older forms of the same idea (Fowler, 2016). There is no standard syntax; platforms use YAML, JSON, XML or their own languages (Microsoft Learn).

#### 3. Idempotence

An IaC deployment always sets the target into the same configuration, whatever its starting state. This is achieved either by reconfiguring the existing target or by discarding it and creating a fresh one (Microsoft Learn); the second route corresponds to immutable and phoenix servers, which Fowler (2016) names as a good fit for IaC.

#### 4. Plan, apply and state (Terraform)

Terraform talks to cloud platforms and other services through their [[apis|APIs]] via plugins called providers. Its workflow has three steps: write the configuration, plan by comparing the configuration with the existing infrastructure to produce an execution plan of creations, updates and deletions, and apply the approved plan in the right order (HashiCorp). A resource graph captures dependencies, so independent resources are changed in parallel; modules package reusable sets of resources (HashiCorp). Terraform keeps a state file that maps the configuration to real resources and stores the last known dependencies, which decide the order in which removed resources are destroyed. Teams share state through a remote backend, which can lock it so that two people do not run Terraform at the same time (HashiCorp State). By default, plan and apply refresh the state from the providers; large setups sometimes skip this, and then the cached state is treated as the record of truth (HashiCorp State).

#### 5. IaC in the delivery pipeline

IaC is a component of continuous delivery: infrastructure changes pass through the same pipeline as application code, and tests catch configuration errors early (Microsoft Learn; Fowler, 2016). Pipelines can create production-like test environments on demand and tear them down again (Microsoft Learn). Small changes are easier to debug and revert than batches, and blue-green deployment or parallel change keep services available during updates (Fowler, 2016). See [[ci-cd|CI/CD]].

#### Origin and variants

IaC became practical when cloud platforms made it possible to create a server in seconds instead of months, which Fowler (2016) contrasts as the cloud age and the "Iron Age". Fowler's article draws its list of practices from Kief Morris's book *Infrastructure as Code*. On Azure, native IaC uses Azure Resource Manager with ARM templates in JSON or the Bicep language; Terraform supports Azure and many other platforms through providers (Microsoft Learn; HashiCorp).

### When to use it

- Environments (development, test, production) must be identical and reproducible (Microsoft Learn).
- Infrastructure changes need an audit trail, for example in regulated settings (Fowler, 2016).
- Many servers or services are created and removed dynamically, as with microservices or on-demand test environments (Fowler, 2016; Microsoft Learn).

### Strengths and limitations

**Strengths**
- Consistency between servers and environments, and fewer hard-to-debug faults (Fowler, 2016).
- Changes can be reviewed, tested and reverted to the last working configuration (Fowler, 2016).
- Repeatable deployments prevent runtime problems from configuration drift or missing dependencies (Microsoft Learn).

**Limitations**
- Manual changes to live systems bypass the definition and make the recorded state wrong; the approach only works if everyone changes the source (Fowler, 2016; Microsoft Learn).
- Tools such as Terraform depend on a state file that must be shared, locked and kept in sync with reality (HashiCorp State).
- Without a standard syntax, definitions are tied to a tool or platform (Microsoft Learn).

### Comparison

| Approach | How the environment is described | Typical tools |
|---|---|---|
| Manual administration | not at all; knowledge in people and runbooks | consoles, ad-hoc logins |
| Imperative scripts / configuration management | steps to reach the configuration | shell scripts, Ansible, Chef, Puppet |
| Declarative IaC | desired end state; the tool computes the steps | Terraform, ARM templates, Bicep |

Sources: Fowler (2016); Microsoft Learn; HashiCorp. Container images ([[docker|Docker]]) and cluster manifests ([[kubernetes|Kubernetes]]) apply the same declarative idea to applications.

### In practice

Infrastructure definitions are stored next to the application code or in their own repository and changed only through pull requests and the pipeline (Fowler, 2016). A plan is reviewed before it is applied, since it shows which resources would be destroyed (HashiCorp). Microsoft points to scanning IaC definitions for misconfigurations (Microsoft Learn). For AI workloads, the same definitions can create model endpoints, vector stores and networking for a [[cloud-ai-platforms|cloud AI platform]] in each environment.

### Key takeaway

Infrastructure as code describes servers and networks in versioned, preferably declarative files that a pipeline applies idempotently, so environments are reproducible, reviewable and free of manual drift.

### Sources

- Fowler, M. (2016). *InfrastructureAsCode.* martinfowler.com, 1 March 2016. [martinfowler.com](https://martinfowler.com/bliki/InfrastructureAsCode.html)
- Microsoft Learn. *What is infrastructure as code (IaC)?* [learn.microsoft.com](https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code)
- HashiCorp. *What is Terraform?* Terraform documentation. [developer.hashicorp.com](https://developer.hashicorp.com/terraform/intro)
- HashiCorp State. *Purpose of Terraform State.* Terraform documentation. [developer.hashicorp.com](https://developer.hashicorp.com/terraform/language/state/purpose)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Infrastructure as Code (IaC) ist „the approach to defining computing and network infrastructure through source code“, sodass Server, Netzwerke und andere Ressourcen wie jede andere Software versioniert, geprüft, getestet und ausgeliefert werden können (Fowler, 2016). Eine versionierte Definition erzeugt bei jedem Deployment dieselbe Umgebung, so wie derselbe Quellcode dasselbe Binary erzeugt; das beseitigt die Abweichungen, durch die manuell gepflegte Umgebungen zu nicht reproduzierbaren „Snowflakes“ werden (Microsoft Learn). Deklarative Werkzeuge wie Terraform, Azure-Resource-Manager-Templates und Bicep beschreiben den gewünschten Endzustand und ermitteln die nötigen Änderungen selbst (HashiCorp; Microsoft Learn).

### Funktionsweise

```text
Definitionsdateien in der Versionsverwaltung (Sollzustand)
 ▼
Review und automatisierte Prüfungen in der Pipeline
 ▼
Plan: Sollzustand mit gespeichertem Zustand und realen Ressourcen vergleichen
 ▼
Apply: Ressourcen über Provider-APIs anlegen / ändern / löschen, in Abhängigkeitsreihenfolge
 ▼
Zustand aktualisiert; die nächste Änderung beginnt wieder bei der Definition, nie am laufenden System
```

#### 1. Definitionsdateien statt manueller Änderungen

Die gesamte Konfiguration liegt in ausführbaren Definitionsdateien; „at no time should anyone log into a server and make on-the-fly adjustments“, weil solche Änderungen Server erzeugen, die sich nicht reproduzieren lassen (Fowler, 2016). Teams ändern die Quelle, nicht das Ziel (Microsoft Learn). Der Code dient zugleich als Dokumentation, die verlässlicher ist als schriftliche Anleitungen, und die Versionsverwaltung hält jede Änderung für Prüfungen fest (Fowler, 2016).

#### 2. Deklarative und imperative Definitionen

Eine deklarative Definition legt fest, welche Komponenten und welche Konfiguration eine Umgebung braucht, nicht wie sie installiert werden; das lässt dem Anbieter Raum für optimierte Verfahren und vermeidet die technischen Schulden wachsender Deployment-Skripte (Microsoft Learn). Terraform-Konfiguration ist in diesem Sinne deklarativ: Sie beschreibt den Endzustand, und Terraform übernimmt die Schritte (HashiCorp). Imperative Skripte und Werkzeuge für Konfigurationsmanagement wie Ansible-Playbooks, Chef-Rezepte und Puppet-Manifeste sind ältere Formen derselben Idee (Fowler, 2016). Eine Standardsyntax gibt es nicht; Plattformen nutzen YAML, JSON, XML oder eigene Sprachen (Microsoft Learn).

#### 3. Idempotenz

Ein IaC-Deployment versetzt das Ziel immer in dieselbe Konfiguration, unabhängig vom Ausgangszustand. Erreicht wird das entweder, indem das bestehende Ziel umkonfiguriert wird, oder indem es verworfen und neu erstellt wird (Microsoft Learn); der zweite Weg entspricht Immutable und Phoenix Servers, die Fowler (2016) als gute Ergänzung zu IaC nennt.

#### 4. Plan, Apply und State (Terraform)

Terraform spricht Cloud-Plattformen und andere Dienste über deren [[apis|APIs]] mithilfe von Plugins an, den Providern. Der Ablauf hat drei Schritte: Konfiguration schreiben, planen, indem die Konfiguration mit der bestehenden Infrastruktur verglichen und ein Ausführungsplan aus Anlage, Änderung und Löschung erstellt wird, und den genehmigten Plan in der richtigen Reihenfolge anwenden (HashiCorp). Ein Ressourcengraph erfasst Abhängigkeiten, sodass unabhängige Ressourcen parallel geändert werden; Module bündeln wiederverwendbare Ressourcengruppen (HashiCorp). Terraform führt eine State-Datei, die die Konfiguration den realen Ressourcen zuordnet und die zuletzt bekannten Abhängigkeiten speichert; diese bestimmen die Reihenfolge, in der entfernte Ressourcen gelöscht werden. Teams teilen den State über ein Remote-Backend, das ihn sperren kann, damit nicht zwei Personen Terraform gleichzeitig ausführen (HashiCorp State). Standardmäßig aktualisieren Plan und Apply den State bei den Providern; große Installationen lassen das teils aus, dann gilt der zwischengespeicherte State als maßgeblich (HashiCorp State).

#### 5. IaC in der Auslieferungspipeline

IaC ist ein Bestandteil von Continuous Delivery: Infrastrukturänderungen durchlaufen dieselbe Pipeline wie Anwendungscode, und Tests finden Konfigurationsfehler früh (Microsoft Learn; Fowler, 2016). Pipelines können produktionsnahe Testumgebungen bei Bedarf erstellen und wieder abbauen (Microsoft Learn). Kleine Änderungen lassen sich leichter untersuchen und zurücknehmen als große Pakete, und Blue-Green-Deployment oder Parallel Change halten Dienste während Updates verfügbar (Fowler, 2016). Siehe [[ci-cd|CI/CD]].

#### Herkunft und Varianten

IaC wurde praktikabel, als Cloud-Plattformen es möglich machten, einen Server in Sekunden statt in Monaten bereitzustellen; Fowler (2016) stellt dem Cloud-Zeitalter die „Iron Age“ gegenüber. Fowlers Artikel übernimmt seine Liste von Praktiken aus Kief Morris' Buch *Infrastructure as Code*. Auf Azure nutzt natives IaC den Azure Resource Manager mit ARM-Templates in JSON oder der Sprache Bicep; Terraform unterstützt Azure und viele andere Plattformen über Provider (Microsoft Learn; HashiCorp).

### Wann einsetzen

- Umgebungen (Entwicklung, Test, Produktion) müssen identisch und reproduzierbar sein (Microsoft Learn).
- Infrastrukturänderungen brauchen einen Prüfpfad, etwa in regulierten Umfeldern (Fowler, 2016).
- Viele Server oder Dienste werden dynamisch erstellt und entfernt, etwa bei Microservices oder Testumgebungen auf Abruf (Fowler, 2016; Microsoft Learn).

### Stärken und Grenzen

**Stärken**
- Konsistenz zwischen Servern und Umgebungen und weniger schwer zu findende Fehler (Fowler, 2016).
- Änderungen lassen sich prüfen, testen und auf die letzte funktionierende Konfiguration zurücksetzen (Fowler, 2016).
- Wiederholbare Deployments verhindern Laufzeitprobleme durch Konfigurationsabweichungen oder fehlende Abhängigkeiten (Microsoft Learn).

**Grenzen**
- Manuelle Änderungen an laufenden Systemen umgehen die Definition und machen den gespeicherten Zustand falsch; der Ansatz funktioniert nur, wenn alle die Quelle ändern (Fowler, 2016; Microsoft Learn).
- Werkzeuge wie Terraform hängen von einer State-Datei ab, die geteilt, gesperrt und mit der Realität synchron gehalten werden muss (HashiCorp State).
- Ohne Standardsyntax sind Definitionen an ein Werkzeug oder eine Plattform gebunden (Microsoft Learn).

### Vergleich

| Ansatz | Wie die Umgebung beschrieben wird | Typische Werkzeuge |
|---|---|---|
| Manuelle Administration | gar nicht; Wissen steckt in Personen und Runbooks | Konsolen, Ad-hoc-Logins |
| Imperative Skripte / Konfigurationsmanagement | Schritte zur Konfiguration | Shell-Skripte, Ansible, Chef, Puppet |
| Deklaratives IaC | gewünschter Endzustand; das Werkzeug berechnet die Schritte | Terraform, ARM-Templates, Bicep |

Quellen: Fowler (2016); Microsoft Learn; HashiCorp. Container-Images ([[docker|Docker]]) und Cluster-Manifeste ([[kubernetes|Kubernetes]]) übertragen dieselbe deklarative Idee auf Anwendungen.

### In der Praxis

Infrastrukturdefinitionen liegen neben dem Anwendungscode oder in einem eigenen Repository und werden nur über Pull Requests und die Pipeline geändert (Fowler, 2016). Ein Plan wird vor dem Anwenden geprüft, weil er zeigt, welche Ressourcen gelöscht würden (HashiCorp). Microsoft verweist darauf, IaC-Definitionen auf Fehlkonfigurationen zu prüfen (Microsoft Learn). Für KI-Workloads können dieselben Definitionen Modell-Endpunkte, Vektorspeicher und Netzwerke einer [[cloud-ai-platforms|Cloud-KI-Plattform]] in jeder Umgebung anlegen.

### Merksatz

Infrastructure as Code beschreibt Server und Netzwerke in versionierten, möglichst deklarativen Dateien, die eine Pipeline idempotent anwendet, sodass Umgebungen reproduzierbar, prüfbar und frei von manuellen Abweichungen sind.

### Quellen

- Fowler, M. (2016). *InfrastructureAsCode.* martinfowler.com, 1. März 2016. [martinfowler.com](https://martinfowler.com/bliki/InfrastructureAsCode.html)
- Microsoft Learn. *What is infrastructure as code (IaC)?* [learn.microsoft.com](https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code)
- HashiCorp. *What is Terraform?* Terraform-Dokumentation. [developer.hashicorp.com](https://developer.hashicorp.com/terraform/intro)
- HashiCorp State. *Purpose of Terraform State.* Terraform-Dokumentation. [developer.hashicorp.com](https://developer.hashicorp.com/terraform/language/state/purpose)
