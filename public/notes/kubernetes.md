---
title_en: Kubernetes
title_de: Kubernetes
entity_type: Technology
sources:
- https://kubernetes.io/docs/concepts/overview/
- https://kubernetes.io/docs/concepts/workloads/pods/
- https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
- https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
- https://helm.sh/docs/intro/using_helm/
- https://doi.org/10.1145/2890784
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Kubernetes is an open-source platform for managing containerized workloads and services through declarative configuration and automation (Kubernetes overview). Users describe the desired state, for example three replicas of an API, and controllers continuously move the actual state towards it, restarting failed containers, rolling out new versions and rolling them back (Kubernetes Deployments docs). Its design grew out of a decade of container management at Google (Burns et al., 2016), and Helm packages Kubernetes applications as charts (Helm docs).

### Core concepts

- **Pods:** The smallest deployable unit: one or more containers with shared storage and network resources that are always co-located and co-scheduled (Kubernetes Pods docs).
- **Deployments:** Provide declarative updates for Pods and ReplicaSets; the Deployment controller changes the actual state to the desired state at a controlled rate, supports rolling updates, rollbacks and scaling (Kubernetes Deployments docs).
- **Declarative configuration:** Resources are described in manifests (usually YAML) and applied to the cluster; Kubernetes reconciles the actual state with the described state (Kubernetes overview; Burns et al., 2016).
- **Self-healing:** Kubernetes restarts failed containers, replaces them, kills containers that do not respond to health checks and does not advertise them to clients until they are ready (Kubernetes overview).
- **Probes:** Liveness probes decide when to restart a container, for example after a deadlock; readiness probes decide when a container may receive traffic, for example after warming caches; startup probes protect slow-starting containers (Kubernetes probes docs).
- **Namespaces:** Isolate groups of resources within one cluster; names must be unique within a namespace but not across namespaces (Kubernetes namespaces docs).
- **Helm:** A package manager in which a chart bundles the resource definitions of an application, a repository shares charts, and a release is an installed instance of a chart (Helm docs).

### Common usage

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notes-api
  namespace: knowledge
spec:
  replicas: 3
  selector:
    matchLabels: {app: notes-api}
  template:
    metadata:
      labels: {app: notes-api}
    spec:
      containers:
        - name: api
          image: registry.example.org/notes-api:1.1
          ports: [{containerPort: 8000}]
          readinessProbe:
            httpGet: {path: /health/ready, port: 8000}
          livenessProbe:
            httpGet: {path: /health/live, port: 8000}
```

```bash
kubectl apply -f deployment.yaml              # create or update resources
kubectl get pods -n knowledge                 # list pods in a namespace
kubectl rollout status deployment/notes-api   # follow a rolling update
kubectl rollout undo deployment/notes-api     # roll back
helm install notes ./chart                    # install a chart as a release
helm upgrade notes ./chart                    # change the release
helm rollback notes 1                         # return to revision 1
```

### When to use it

- When containerised services must run reliably across many machines with automatic restarts, scaling and rollouts (Kubernetes overview).
- When many teams share one cluster, separated by namespaces (Kubernetes namespaces docs).
- For a single small service, a simpler platform or plain Docker Compose may be sufficient ([[docker|Docker]]).

### Strengths and limitations

**Strengths**
- Declarative desired state with controllers that reconcile continuously (Burns et al., 2016).
- Self-healing, rolling updates and rollbacks are built in (Kubernetes overview; Kubernetes Deployments docs).
- Health probes keep unready or stuck containers away from traffic (Kubernetes probes docs).

**Limitations**
- Many concepts and manifests make it complex to learn and operate compared with running containers on a single host ([[docker|Docker]]).
- Misconfigured probes can restart healthy containers or route traffic to unready ones (Kubernetes probes docs).
- Namespaces do not isolate cluster-wide objects such as nodes or persistent volumes (Kubernetes namespaces docs).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Docker Compose | Runs containers on one host from a YAML file ([[docker|Docker]]) | Local development, small setups |
| Kubernetes | Orchestrates containers across a cluster with desired-state controllers (Kubernetes overview) | Production services at scale |
| Helm on Kubernetes | Packages and versions Kubernetes manifests as charts (Helm docs) | Reusable, configurable deployments |

### In practice

ML models and LLM services are deployed as container images in Deployments, with readiness probes that wait until the model is loaded and rolling updates for new model versions ([[mlops-and-deployment|MLOps and Deployment]]; Kubernetes probes docs). Configuration and secrets are kept separate from images, and Helm values files hold environment-specific settings (Kubernetes overview; Helm docs). Services on the cluster offer their functionality through [[apis|APIs]].

### Key takeaway

Kubernetes runs containers on a cluster by continuously reconciling the actual state with a declared desired state, which provides self-healing, scaling and safe rollouts.

### Sources

- The Kubernetes Authors. *Overview.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/overview/)
- The Kubernetes Authors. *Pods.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/workloads/pods/)
- The Kubernetes Authors. *Deployments.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- The Kubernetes Authors. *Liveness, Readiness, and Startup Probes.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- The Kubernetes Authors. *Namespaces.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- The Helm Authors. *Using Helm.* Helm documentation. [helm.sh](https://helm.sh/docs/intro/using_helm/)
- Burns, B., Grant, B., Oppenheimer, D., Brewer, E. & Wilkes, J. (2016). *Borg, Omega, and Kubernetes.* Communications of the ACM 59(5). [doi:10.1145/2890784](https://doi.org/10.1145/2890784)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Kubernetes ist eine Open-Source-Plattform zur Verwaltung containerisierter Workloads und Dienste über deklarative Konfiguration und Automatisierung (Kubernetes overview). Nutzende beschreiben den gewünschten Zustand, etwa drei Replikate einer API, und Controller führen den tatsächlichen Zustand laufend dorthin: Sie starten ausgefallene Container neu, rollen neue Versionen aus und nehmen sie bei Bedarf zurück (Kubernetes Deployments docs). Der Entwurf entstand aus einem Jahrzehnt Containerverwaltung bei Google (Burns et al., 2016), und Helm verpackt Kubernetes-Anwendungen als Charts (Helm docs).

### Kernkonzepte

- **Pods:** Die kleinste bereitstellbare Einheit: ein oder mehrere Container mit gemeinsamen Speicher- und Netzwerkressourcen, die immer gemeinsam platziert und eingeplant werden (Kubernetes Pods docs).
- **Deployments:** Liefern deklarative Aktualisierungen für Pods und ReplicaSets; der Deployment-Controller führt den tatsächlichen Zustand kontrolliert in den gewünschten über und unterstützt Rolling Updates, Rollbacks und Skalierung (Kubernetes Deployments docs).
- **Deklarative Konfiguration:** Ressourcen werden in Manifesten (meist YAML) beschrieben und auf den Cluster angewendet; Kubernetes gleicht den tatsächlichen mit dem beschriebenen Zustand ab (Kubernetes overview; Burns et al., 2016).
- **Selbstheilung:** Kubernetes startet ausgefallene Container neu, ersetzt sie, beendet Container, die auf Health Checks nicht antworten, und bietet sie Clients erst an, wenn sie bereit sind (Kubernetes overview).
- **Probes:** Liveness-Probes entscheiden, wann ein Container neu gestartet wird, etwa nach einem Deadlock; Readiness-Probes entscheiden, wann ein Container Datenverkehr erhalten darf, etwa nach dem Aufwärmen von Caches; Startup-Probes schützen langsam startende Container (Kubernetes probes docs).
- **Namespaces:** Isolieren Gruppen von Ressourcen innerhalb eines Clusters; Namen müssen innerhalb eines Namespace eindeutig sein, nicht aber über Namespaces hinweg (Kubernetes namespaces docs).
- **Helm:** Ein Paketmanager, in dem ein Chart die Ressourcendefinitionen einer Anwendung bündelt, ein Repository Charts teilt und ein Release eine installierte Instanz eines Charts ist (Helm docs).

### Typische Verwendung

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notes-api
  namespace: knowledge
spec:
  replicas: 3
  selector:
    matchLabels: {app: notes-api}
  template:
    metadata:
      labels: {app: notes-api}
    spec:
      containers:
        - name: api
          image: registry.example.org/notes-api:1.1
          ports: [{containerPort: 8000}]
          readinessProbe:
            httpGet: {path: /health/ready, port: 8000}
          livenessProbe:
            httpGet: {path: /health/live, port: 8000}
```

```bash
kubectl apply -f deployment.yaml              # Ressourcen anlegen oder aktualisieren
kubectl get pods -n knowledge                 # Pods in einem Namespace anzeigen
kubectl rollout status deployment/notes-api   # Rolling Update verfolgen
kubectl rollout undo deployment/notes-api     # zurückrollen
helm install notes ./chart                    # Chart als Release installieren
helm upgrade notes ./chart                    # Release ändern
helm rollback notes 1                         # zu Revision 1 zurückkehren
```

### Wann einsetzen

- Wenn containerisierte Dienste zuverlässig auf vielen Rechnern laufen müssen, mit automatischen Neustarts, Skalierung und Rollouts (Kubernetes overview).
- Wenn viele Teams einen Cluster teilen, getrennt durch Namespaces (Kubernetes namespaces docs).
- Für einen einzelnen kleinen Dienst kann eine einfachere Plattform oder Docker Compose genügen ([[docker|Docker]]).

### Stärken und Grenzen

**Stärken**
- Deklarativer Sollzustand mit Controllern, die laufend abgleichen (Burns et al., 2016).
- Selbstheilung, Rolling Updates und Rollbacks sind eingebaut (Kubernetes overview; Kubernetes Deployments docs).
- Health-Probes halten nicht bereite oder festhängende Container vom Datenverkehr fern (Kubernetes probes docs).

**Einschränkungen**
- Viele Konzepte und Manifeste machen Einstieg und Betrieb komplexer als das Ausführen von Containern auf einem einzelnen Host ([[docker|Docker]]).
- Falsch konfigurierte Probes können gesunde Container neu starten oder Verkehr an nicht bereite leiten (Kubernetes probes docs).
- Namespaces isolieren keine clusterweiten Objekte wie Nodes oder Persistent Volumes (Kubernetes namespaces docs).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Docker Compose | Startet Container auf einem Host aus einer YAML-Datei ([[docker|Docker]]) | Lokale Entwicklung, kleine Setups |
| Kubernetes | Orchestriert Container über einen Cluster mit Sollzustands-Controllern (Kubernetes overview) | Produktive Dienste im großen Maßstab |
| Helm auf Kubernetes | Verpackt und versioniert Kubernetes-Manifeste als Charts (Helm docs) | Wiederverwendbare, konfigurierbare Deployments |

### In der Praxis

ML-Modelle und LLM-Dienste werden als Container-Images in Deployments bereitgestellt, mit Readiness-Probes, die warten, bis das Modell geladen ist, und Rolling Updates für neue Modellversionen ([[mlops-and-deployment|MLOps und Deployment]]; Kubernetes probes docs). Konfiguration und Geheimnisse werden von den Images getrennt gehalten, und Helm-Values-Dateien enthalten umgebungsspezifische Einstellungen (Kubernetes overview; Helm docs). Dienste im Cluster stellen ihre Funktionen über [[apis|APIs (Programmierschnittstellen)]] bereit.

### Merksatz

Kubernetes betreibt Container auf einem Cluster, indem es den tatsächlichen Zustand laufend mit einem deklarierten Sollzustand abgleicht; das bringt Selbstheilung, Skalierung und sichere Rollouts.

### Quellen

- The Kubernetes Authors. *Overview.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/overview/)
- The Kubernetes Authors. *Pods.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/workloads/pods/)
- The Kubernetes Authors. *Deployments.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- The Kubernetes Authors. *Liveness, Readiness, and Startup Probes.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- The Kubernetes Authors. *Namespaces.* Kubernetes documentation. [kubernetes.io](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- The Helm Authors. *Using Helm.* Helm documentation. [helm.sh](https://helm.sh/docs/intro/using_helm/)
- Burns, B., Grant, B., Oppenheimer, D., Brewer, E. & Wilkes, J. (2016). *Borg, Omega, and Kubernetes.* Communications of the ACM 59(5). [doi:10.1145/2890784](https://doi.org/10.1145/2890784)
