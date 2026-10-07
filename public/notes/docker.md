---
title_en: Docker
title_de: Docker
entity_type: Technology
sources:
- https://docs.docker.com/get-started/docker-overview/
- https://docs.docker.com/reference/dockerfile/
- https://docs.docker.com/engine/storage/volumes/
- https://docs.docker.com/compose/
- https://doi.org/10.1145/2890784
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Docker packages an application with everything it needs into a container, a lightweight, isolated runtime that behaves the same on every machine, which separates applications from infrastructure (Docker overview). Containers are started from images, which are built from a Dockerfile (Dockerfile reference); volumes keep data beyond the life of a container (Docker volumes), and Docker Compose runs multi-container applications from one YAML file (Docker Compose docs). Containers became the unit of deployment that orchestrators such as Kubernetes manage (Burns et al., 2016).

### Core concepts

- **Containers:** A container is a runnable instance of an image; it is lightweight and contains everything needed to run the application, so it does not depend on what is installed on the host (Docker overview).
- **Images:** An image is a read-only template with instructions for creating a container, often based on another image; images are stored and shared in registries such as Docker Hub (Docker overview).
- **Container versus virtual machine:** Containers isolate applications and package their dependencies while sharing the host's operating system kernel, which makes them lighter than virtual machines; the same image runs in development and production (Burns et al., 2016).
- **Dockerfile:** A text document with the instructions to assemble an image: FROM sets the base image, RUN executes commands, COPY adds files, WORKDIR, ENV and EXPOSE configure the environment, and CMD or ENTRYPOINT set the default command; each instruction creates a layer that can be reused from the build cache (Dockerfile reference).
- **Volumes:** Persistent data stores created and managed by Docker; they live on the host and are mounted into containers, so data survives when a container is removed (Docker volumes).
- **Docker Compose:** Defines services, networks and volumes of a multi-container application in a YAML file and starts them with one command (Docker Compose docs).

### Common usage

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t notes-api:1.0 .                     # build an image
docker run -d -p 8000:8000 --name api notes-api:1.0  # start a container
docker ps                                           # list running containers
docker logs api                                     # show container output
docker volume create notes-data                     # create a volume
docker compose up -d                                # start all services from compose.yaml
```

Copying the dependency file and installing it before copying the rest of the code lets Docker reuse the cached dependency layer when only the code changes (Dockerfile reference).

### When to use it

- When an application must run identically on developer machines, CI and servers (Docker overview).
- When several services, such as an API, a database and a vector store, should be started together locally (Docker Compose docs).
- When containers must be scheduled, scaled and healed across many machines, an orchestrator such as Kubernetes is added ([[kubernetes|Kubernetes]]).

### Strengths and limitations

**Strengths**
- Same environment everywhere, independent of the host's installed software (Docker overview).
- Layered images with build cache make rebuilds fast (Dockerfile reference).
- One command starts a complete multi-container stack (Docker Compose docs).

**Limitations**
- Container file systems are ephemeral; persistent data needs volumes (Docker volumes).
- Containers share the host kernel, so they isolate less strongly than virtual machines (Burns et al., 2016).
- Docker alone does not manage scheduling, scaling or self-healing across machines ([[kubernetes|Kubernetes]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Virtual machine | Full guest operating system per instance | Strong isolation, different OS kernels |
| Docker container | Isolated process with packaged dependencies, shared kernel (Burns et al., 2016) | Reproducible application packaging |
| Docker Compose | Several containers defined in one YAML file (Docker Compose docs) | Local multi-service development |
| Kubernetes | Orchestrates containers across a cluster ([[kubernetes|Kubernetes]]) | Production at scale |

### In practice

ML models are commonly served from container images that pin the model, code and dependencies, which makes deployments reproducible ([[mlops-and-deployment|MLOps and Deployment]]). Images are kept small with slim base images, secrets are passed at run time rather than baked into images, and agent sandboxes often run tool code inside containers to isolate it from the host.

### Key takeaway

Docker packages applications with their dependencies into images and runs them as isolated containers, giving the same behaviour on every machine.

### Sources

- Docker Inc. *What is Docker?* Docker documentation. [docs.docker.com](https://docs.docker.com/get-started/docker-overview/)
- Docker Inc. *Dockerfile reference.* Docker documentation. [docs.docker.com](https://docs.docker.com/reference/dockerfile/)
- Docker Inc. *Volumes.* Docker documentation. [docs.docker.com](https://docs.docker.com/engine/storage/volumes/)
- Docker Inc. *Docker Compose.* Docker documentation. [docs.docker.com](https://docs.docker.com/compose/)
- Burns, B., Grant, B., Oppenheimer, D., Brewer, E. & Wilkes, J. (2016). *Borg, Omega, and Kubernetes.* Communications of the ACM 59(5). [doi:10.1145/2890784](https://doi.org/10.1145/2890784)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Docker verpackt eine Anwendung mit allem, was sie braucht, in einen Container, eine leichtgewichtige, isolierte Laufzeitumgebung, die sich auf jedem Rechner gleich verhält; so werden Anwendungen von der Infrastruktur getrennt (Docker overview). Container werden aus Images gestartet, die aus einem Dockerfile gebaut werden (Dockerfile reference); Volumes bewahren Daten über die Lebensdauer eines Containers hinaus (Docker volumes), und Docker Compose startet Anwendungen aus mehreren Containern über eine YAML-Datei (Docker Compose docs). Container wurden zur Einheit des Deployments, die Orchestrierer wie Kubernetes verwalten (Burns et al., 2016).

### Kernkonzepte

- **Container:** Ein Container ist eine ausführbare Instanz eines Images; er ist leichtgewichtig und enthält alles, was die Anwendung braucht, sodass er nicht davon abhängt, was auf dem Host installiert ist (Docker overview).
- **Images:** Ein Image ist eine schreibgeschützte Vorlage mit Anweisungen zum Erzeugen eines Containers, oft auf Basis eines anderen Images; Images werden in Registries wie Docker Hub gespeichert und geteilt (Docker overview).
- **Container und virtuelle Maschine:** Container isolieren Anwendungen und verpacken ihre Abhängigkeiten, teilen sich aber den Betriebssystemkern des Hosts und sind dadurch leichter als virtuelle Maschinen; dasselbe Image läuft in Entwicklung und Produktivbetrieb (Burns et al., 2016).
- **Dockerfile:** Ein Textdokument mit den Anweisungen zum Zusammenbau eines Images: FROM legt das Basis-Image fest, RUN führt Befehle aus, COPY fügt Dateien hinzu, WORKDIR, ENV und EXPOSE konfigurieren die Umgebung, und CMD oder ENTRYPOINT legen den Standardbefehl fest; jede Anweisung erzeugt eine Schicht, die aus dem Build-Cache wiederverwendet werden kann (Dockerfile reference).
- **Volumes:** Persistente, von Docker erzeugte und verwaltete Datenspeicher; sie liegen auf dem Host und werden in Container eingebunden, sodass Daten das Entfernen eines Containers überstehen (Docker volumes).
- **Docker Compose:** Legt Dienste, Netzwerke und Volumes einer Mehr-Container-Anwendung in einer YAML-Datei fest und startet sie mit einem Befehl (Docker Compose docs).

### Typische Verwendung

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t notes-api:1.0 .                     # Image bauen
docker run -d -p 8000:8000 --name api notes-api:1.0  # Container starten
docker ps                                           # laufende Container anzeigen
docker logs api                                     # Ausgabe des Containers zeigen
docker volume create notes-data                     # Volume anlegen
docker compose up -d                                # alle Dienste aus compose.yaml starten
```

Wird die Abhängigkeitsdatei vor dem übrigen Code kopiert und installiert, kann Docker die zwischengespeicherte Abhängigkeitsschicht wiederverwenden, wenn sich nur der Code ändert (Dockerfile reference).

### Wann einsetzen

- Wenn eine Anwendung auf Entwicklungsrechnern, in der CI und auf Servern identisch laufen muss (Docker overview).
- Wenn mehrere Dienste wie eine API, eine Datenbank und ein Vektorspeicher lokal gemeinsam gestartet werden sollen (Docker Compose docs).
- Wenn Container über viele Rechner verteilt, skaliert und selbstheilend betrieben werden müssen, kommt ein Orchestrierer wie Kubernetes hinzu ([[kubernetes|Kubernetes]]).

### Stärken und Grenzen

**Stärken**
- Überall dieselbe Umgebung, unabhängig von der auf dem Host installierten Software (Docker overview).
- Geschichtete Images mit Build-Cache machen Neubauten schnell (Dockerfile reference).
- Ein Befehl startet einen kompletten Mehr-Container-Stack (Docker Compose docs).

**Einschränkungen**
- Dateisysteme von Containern sind flüchtig; persistente Daten brauchen Volumes (Docker volumes).
- Container teilen sich den Kern des Hosts und isolieren daher schwächer als virtuelle Maschinen (Burns et al., 2016).
- Docker allein übernimmt weder Planung noch Skalierung oder Selbstheilung über mehrere Rechner ([[kubernetes|Kubernetes]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Virtuelle Maschine | Vollständiges Gastbetriebssystem je Instanz | Starke Isolation, unterschiedliche Betriebssystemkerne |
| Docker-Container | Isolierter Prozess mit verpackten Abhängigkeiten, geteilter Kern (Burns et al., 2016) | Reproduzierbares Verpacken von Anwendungen |
| Docker Compose | Mehrere Container in einer YAML-Datei (Docker Compose docs) | Lokale Entwicklung mit mehreren Diensten |
| Kubernetes | Orchestriert Container über einen Cluster ([[kubernetes|Kubernetes]]) | Produktivbetrieb im großen Maßstab |

### In der Praxis

ML-Modelle werden häufig aus Container-Images bereitgestellt, die Modell, Code und Abhängigkeiten festschreiben, was Deployments reproduzierbar macht ([[mlops-and-deployment|MLOps und Deployment]]). Images werden mit schlanken Basis-Images klein gehalten, Geheimnisse werden zur Laufzeit übergeben statt ins Image eingebaut, und Sandboxes für Agenten führen Werkzeugcode oft in Containern aus, um ihn vom Host zu isolieren.

### Merksatz

Docker verpackt Anwendungen mit ihren Abhängigkeiten in Images und führt sie als isolierte Container aus, die sich auf jedem Rechner gleich verhalten.

### Quellen

- Docker Inc. *What is Docker?* Docker documentation. [docs.docker.com](https://docs.docker.com/get-started/docker-overview/)
- Docker Inc. *Dockerfile reference.* Docker documentation. [docs.docker.com](https://docs.docker.com/reference/dockerfile/)
- Docker Inc. *Volumes.* Docker documentation. [docs.docker.com](https://docs.docker.com/engine/storage/volumes/)
- Docker Inc. *Docker Compose.* Docker documentation. [docs.docker.com](https://docs.docker.com/compose/)
- Burns, B., Grant, B., Oppenheimer, D., Brewer, E. & Wilkes, J. (2016). *Borg, Omega, and Kubernetes.* Communications of the ACM 59(5). [doi:10.1145/2890784](https://doi.org/10.1145/2890784)
