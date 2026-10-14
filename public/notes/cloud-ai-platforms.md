---
title_en: Cloud AI Platforms
title_de: Cloud-KI-Plattformen
entity_type: Concept
aliases:
- Cloud AI platforms
- Cloud AI platform
- Microsoft Foundry
- Azure AI Foundry
- Azure OpenAI
- Vertex AI
- Gemini Enterprise Agent Platform
- Amazon Bedrock
- Cloud-KI-Plattform
sources:
- https://csrc.nist.gov/pubs/sp/800/145/final
- https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry
- https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
- https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search
- https://docs.cloud.google.com/vertex-ai/docs/start/introduction-unified-platform
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes
- https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Cloud AI platforms are managed services from the large cloud providers that bundle access to foundation models with the tooling to build, ground, evaluate, deploy and govern AI applications: Microsoft Foundry (formerly Azure AI Studio and Azure AI Foundry, including Azure OpenAI), [[google|Google]]'s Gemini Enterprise Agent Platform (Vertex AI until April 2026) and Amazon Bedrock (Microsoft Learn; Google Cloud Release Notes; AWS). In NIST's terms they are mostly platform-as-a-service offerings: the customer deploys applications and models but does not manage the underlying servers, networks or storage (Mell & Grance, 2011). Choosing one is largely a question of which models, data integrations, security controls and data-processing commitments fit an organisation's existing cloud.

### How it works

```text
enterprise data (storage, databases, SharePoint, …)
 ▼
retrieval service: indexing, chunking, embeddings, hybrid search (e.g. Azure AI Search)
 ▼
model catalogue: proprietary and open models, deployed as managed endpoints
 ▼
agents and tools: hosted agent runtime, tool calling, memory
 ▼
evaluation, tracing, content filters / guardrails, monitoring
 ▼
identity, network isolation, policies, region of processing
```

#### 1. Cloud service models

NIST defines cloud computing as "a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources … that can be rapidly provisioned and released with minimal management effort or service provider interaction", with five essential characteristics (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service), three service models and four deployment models (private, community, public, hybrid) (Mell & Grance, 2011). In infrastructure as a service (IaaS), the customer controls operating systems, storage and deployed applications; in platform as a service (PaaS), only the deployed applications and possibly settings of the hosting environment; in software as a service (SaaS), at most limited user-specific settings (Mell & Grance, 2011). Model endpoints, managed agent runtimes and search services are PaaS in this sense; a chat assistant used as is would be SaaS.

#### 2. Model catalogue and endpoints

All three platforms offer many models behind one API. Microsoft Foundry gives access to more than 10,000 models from Microsoft, [[openai|OpenAI]], [[anthropic|Anthropic]], Meta and others (Microsoft Learn). Amazon Bedrock is "a fully managed service that provides secure, enterprise-grade access to high-performing foundation models from leading AI companies" and lists more than 100 models from providers including Amazon, Anthropic, DeepSeek, OpenAI and xAI; it also supports fine-tuning, continued pre-training and distillation (AWS). Google's platform provides managed training for PyTorch, TensorFlow, [[scikit-learn|scikit-learn]] and XGBoost, AutoML and a Model Registry as "a central repository where you can manage the lifecycle of your ML models" (Google Cloud). Models are deployed in a chosen region or with global or data-zone deployment types that spread processing across regions for capacity (Microsoft Learn Privacy).

#### 3. Retrieval and grounding

The platforms include managed retrieval for [[retrieval-augmented-generation|RAG]]. Azure AI Search, for example, is "a fully managed, cloud-hosted service that connects your data to AI": it indexes JSON documents into inverted indexes and vector indexes, can chunk and vectorise content during indexing, and supports full-text, vector, hybrid and multimodal queries (Microsoft Learn Search). In addition to classic single-request search it offers agentic retrieval, in which a knowledge base plans a query, splits it into sub-queries, retrieves from several sources in parallel, reranks semantically and merges the results (Microsoft Learn Search). Concepts behind this are covered in [[vector-databases|vector databases]], [[rag-retrieval|RAG retrieval]] and [[information-retrieval|information retrieval]].

#### 4. Agents and orchestration

Agent services host the loop of model, instructions and tools described in [[agentic-ai|agentic AI]]. In Microsoft Foundry, a prompt agent is declared with instructions, a model and tools and run by the platform, while a hosted agent packages the team's own code or framework, for example LangGraph or Semantic Kernel, as a container that Foundry runs with a managed endpoint, scaling, identity and observability (Microsoft Learn). Google renamed Vertex AI to Gemini Enterprise Agent Platform on 22 April 2026, with Agent Engine becoming Agent Runtime, Vertex AI Studio becoming Agent Studio and Vertex AI Pipelines becoming Agent Platform Pipelines (Google Cloud Release Notes). Framework choices are compared in [[agent-frameworks|agent frameworks]]; pipelines in [[ml-pipelines|ML pipelines]].

#### 5. Governance, safety and data protection

The platforms add evaluation, tracing and monitoring dashboards, identity and role-based access control, content filters, network isolation and policies (Microsoft Learn). Data-processing commitments matter for regulated users. Microsoft states that prompts, completions, [[embeddings|embeddings]] and training data are not available to OpenAI or other model providers and are not used to train generative AI foundation models without the customer's permission; the models are stateless, prompts are processed in the customer-specified geography unless a global or data-zone deployment is chosen, and a sample of prompts may be stored for abuse monitoring and reviewed by authorised employees, who for deployments in the European Economic Area are located there (Microsoft Learn Privacy). AWS states that model providers have no access to the accounts in which Bedrock runs their models and therefore none to customer prompts and completions (AWS Data Protection). Filters and guardrails are covered in [[llm-guardrails-and-red-teaming|LLM guardrails and red teaming]].

#### Origin and variants

The NIST definition dates from 2011 (Mell & Grance, 2011). The AI platforms have been renamed repeatedly: Microsoft's sequence runs from Azure AI Studio via Azure AI Foundry to Microsoft Foundry, with Azure AI Services becoming Foundry Tools and the Assistants API being replaced by the Responses API (Microsoft Learn), and Google consolidated Vertex AI into the Gemini Enterprise Agent Platform in 2026 (Google Cloud Release Notes). Data platforms such as [[databricks|Databricks]] offer similar model serving next to the data, see [[data-lakehouse|data lakehouse]].

### When to use it

- An organisation already runs its data and identity management in one cloud and wants models, retrieval and agents inside the same security perimeter (Microsoft Learn; AWS).
- Several models from different providers need to be compared or swapped behind one API (Microsoft Learn; AWS).
- Data residency and contractual data-processing commitments are required, for example for personal or confidential data (Microsoft Learn Privacy).

### Strengths and limitations

**Strengths**
- No infrastructure to run for models, search and agents; provisioning is on demand and billed by use (Mell & Grance, 2011).
- Built-in enterprise features: identity, network isolation, policies, evaluation and tracing (Microsoft Learn).
- Documented commitments that model providers do not see or train on customer data (Microsoft Learn Privacy; AWS Data Protection).

**Limitations**
- Products, names and [[apis|APIs]] change quickly, as the renamings of 2024–2026 show (Microsoft Learn; Google Cloud Release Notes).
- Global deployment types and abuse monitoring mean that data can be processed outside the chosen region or reviewed by people unless configured otherwise (Microsoft Learn Privacy).
- Platform-specific services bind applications to one provider; switching rules are covered in the [[data-act|Data Act]].

### Comparison

| | Microsoft Foundry | Gemini Enterprise Agent Platform | Amazon Bedrock |
|---|---|---|---|
| Former name | Azure AI Studio / Azure AI Foundry | Vertex AI (until April 2026) | — |
| Models | > 10,000 (Microsoft, OpenAI, Anthropic, Meta, …) | Model Garden; own training incl. AutoML | > 100 (Amazon, Anthropic, DeepSeek, OpenAI, xAI, …) |
| Retrieval | Azure AI Search, Foundry IQ knowledge bases | not covered by the cited sources | not covered by the cited sources |
| Agents | prompt agents, hosted agents | Agent Runtime, Agent Studio | not covered by the cited sources |
| ML lifecycle | not covered by the cited sources | training, Model Registry, Pipelines, Feature Store | fine-tuning, continued pre-training, distillation |

Sources: Microsoft Learn; Microsoft Learn Search; Google Cloud; Google Cloud Release Notes; AWS. Self-hosting open models instead is described in [[mlops-and-deployment|MLOps and deployment]] and [[llm-cost-optimisation|LLM cost optimisation]].

### In practice

Platform resources are best created with [[infrastructure-as-code|infrastructure as code]] and deployed through [[ci-cd|CI/CD]], so development, test and production stay identical. For EU personal data, the region and deployment type determine where prompts are processed (Microsoft Learn Privacy), which matters under the [[gdpr|GDPR]]. Banks and insurers treat such services as ICT outsourcing to third-party providers, with requirements from [[dora|DORA]] and the [[eba-governance-and-outsourcing-guidelines|EBA outsourcing guidelines]].

### Regulatory context

Using a cloud AI platform for personal data makes the provider a processor under the [[gdpr|GDPR]]; Microsoft's processing is governed by its Data Protection Addendum (Microsoft Learn Privacy). For financial entities, the cloud provider is an ICT third-party service provider under [[dora|DORA]]. The [[data-act|Data Act]] contains rules on switching between data processing services.

### Key takeaway

Cloud AI platforms bundle models, retrieval, agents, evaluation and governance as managed PaaS services; the choice between Microsoft Foundry, Google's Gemini Enterprise Agent Platform and Amazon Bedrock depends on the existing cloud, the models needed and the data-processing commitments required.

### Sources

- Mell, P. & Grance, T. (2011). *The NIST Definition of Cloud Computing.* NIST Special Publication 800-145. [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/145/final)
- Microsoft Learn. *What is Microsoft Foundry?* Updated September 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
- Microsoft Learn Privacy. *Data, privacy, and security for Foundry Models sold by Azure in Microsoft Foundry.* [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy)
- Microsoft Learn Search. *Introduction to Azure AI Search.* Updated September 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- Google Cloud. *Introduction to machine learning on Gemini Enterprise Agent Platform.* [docs.cloud.google.com](https://docs.cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
- Google Cloud Release Notes. *Gemini Enterprise Agent Platform release notes*, entry of 22 April 2026. [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)
- AWS. *What is Amazon Bedrock?* Amazon Bedrock User Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- AWS Data Protection. *Data protection.* Amazon Bedrock User Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Cloud-KI-Plattformen sind verwaltete Dienste der großen Cloud-Anbieter, die den Zugang zu Foundation Models mit den Werkzeugen bündeln, um KI-Anwendungen zu bauen, mit Daten zu verankern, zu evaluieren, auszuliefern und zu steuern: Microsoft Foundry (früher Azure AI Studio und Azure AI Foundry, einschließlich Azure OpenAI), Googles Gemini Enterprise Agent Platform (bis April 2026 Vertex AI) und Amazon Bedrock (Microsoft Learn; [[google|Google]] Cloud Release Notes; AWS). In der Terminologie von NIST sind sie überwiegend Platform-as-a-Service-Angebote: Die Kundschaft stellt Anwendungen und Modelle bereit, verwaltet aber nicht die zugrunde liegenden Server, Netzwerke oder Speicher (Mell & Grance, 2011). Die Wahl ist vor allem eine Frage, welche Modelle, Datenanbindungen, Sicherheitsfunktionen und Zusagen zur Datenverarbeitung zur bestehenden Cloud einer Organisation passen.

### Funktionsweise

```text
Unternehmensdaten (Speicher, Datenbanken, SharePoint, …)
 ▼
Retrieval-Dienst: Indexierung, Chunking, Embeddings, hybride Suche (z. B. Azure AI Search)
 ▼
Modellkatalog: proprietäre und offene Modelle, als verwaltete Endpunkte bereitgestellt
 ▼
Agenten und Tools: gehostete Agentenlaufzeit, Tool Calling, Gedächtnis
 ▼
Evaluation, Tracing, Inhaltsfilter / Guardrails, Monitoring
 ▼
Identität, Netzwerkisolation, Richtlinien, Region der Verarbeitung
```

#### 1. Cloud-Servicemodelle

NIST definiert Cloud Computing als „a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources … that can be rapidly provisioned and released with minimal management effort or service provider interaction“, mit fünf wesentlichen Merkmalen (On-Demand-Selbstbedienung, breiter Netzwerkzugang, Ressourcenbündelung, schnelle Elastizität, gemessener Dienst), drei Servicemodellen und vier Bereitstellungsmodellen (privat, Community, öffentlich, hybrid) (Mell & Grance, 2011). Bei Infrastructure as a Service (IaaS) kontrolliert die Kundschaft Betriebssysteme, Speicher und bereitgestellte Anwendungen; bei Platform as a Service (PaaS) nur die bereitgestellten Anwendungen und gegebenenfalls Einstellungen der Hosting-Umgebung; bei Software as a Service (SaaS) höchstens begrenzte nutzerspezifische Einstellungen (Mell & Grance, 2011). Modell-Endpunkte, verwaltete Agentenlaufzeiten und Suchdienste sind in diesem Sinne PaaS; ein unverändert genutzter Chat-Assistent wäre SaaS.

#### 2. Modellkatalog und Endpunkte

Alle drei Plattformen bieten viele Modelle hinter einer API. Microsoft Foundry gibt Zugang zu mehr als 10.000 Modellen von Microsoft, [[openai|OpenAI]], [[anthropic|Anthropic]], Meta und anderen (Microsoft Learn). Amazon Bedrock ist „a fully managed service that provides secure, enterprise-grade access to high-performing foundation models from leading AI companies“ und führt mehr als 100 Modelle von Anbietern wie Amazon, Anthropic, DeepSeek, OpenAI und xAI; es unterstützt außerdem Fine-Tuning, fortgesetztes Pre-Training und Distillation (AWS). Googles Plattform bietet verwaltetes Training für PyTorch, TensorFlow, [[scikit-learn|scikit-learn]] und XGBoost, AutoML und eine Model Registry als „a central repository where you can manage the lifecycle of your ML models“ (Google Cloud). Modelle werden in einer gewählten Region bereitgestellt oder mit globalen bzw. Data-Zone-Bereitstellungsarten, die die Verarbeitung aus Kapazitätsgründen über Regionen verteilen (Microsoft Learn Privacy).

#### 3. Retrieval und Verankerung in Daten

Die Plattformen enthalten verwaltetes Retrieval für [[retrieval-augmented-generation|RAG]]. Azure AI Search etwa ist „a fully managed, cloud-hosted service that connects your data to AI“: Der Dienst indexiert JSON-Dokumente in Inverted Indexes und Vektorindizes, kann Inhalte beim Indexieren in Chunks zerlegen und vektorisieren und unterstützt Volltext-, Vektor-, hybride und multimodale Abfragen (Microsoft Learn Search). Neben der klassischen Suche mit einer einzelnen Anfrage bietet er Agentic Retrieval, bei dem eine Wissensbasis eine Abfrage plant, in Teilabfragen zerlegt, parallel aus mehreren Quellen abruft, semantisch neu rankt und die Ergebnisse zusammenführt (Microsoft Learn Search). Die Konzepte dahinter behandeln [[vector-databases|Vektordatenbanken]], [[rag-retrieval|RAG: Retrieval]] und [[information-retrieval|Information Retrieval]].

#### 4. Agenten und Orchestrierung

Agentendienste betreiben die Schleife aus Modell, Anweisungen und Tools, die [[agentic-ai|Agentic AI]] beschreibt. In Microsoft Foundry wird ein Prompt Agent mit Anweisungen, Modell und Tools deklariert und von der Plattform ausgeführt, während ein Hosted Agent eigenen Code oder ein eigenes Framework, etwa LangGraph oder Semantic Kernel, als Container verpackt, den Foundry mit verwaltetem Endpunkt, Skalierung, Identität und [[monitoring-and-alerting|Observability]] betreibt (Microsoft Learn). Google benannte Vertex AI am 22. April 2026 in Gemini Enterprise Agent Platform um; dabei wurde Agent Engine zu Agent Runtime, Vertex AI Studio zu Agent Studio und Vertex AI Pipelines zu Agent Platform Pipelines (Google Cloud Release Notes). Frameworks vergleicht [[agent-frameworks|Agent-Frameworks]]; Pipelines behandelt [[ml-pipelines|ML-Pipelines]].

#### 5. Steuerung, Sicherheit und Datenschutz

Die Plattformen ergänzen Evaluation, Tracing und Monitoring-Dashboards, Identitäts- und rollenbasierte Zugriffskontrolle, Inhaltsfilter, Netzwerkisolation und Richtlinien (Microsoft Learn). Für regulierte Nutzerinnen und Nutzer zählen die Zusagen zur Datenverarbeitung. Microsoft erklärt, dass Prompts, Completions, [[embeddings|Embeddings]] und Trainingsdaten weder OpenAI noch anderen Modellanbietern zugänglich sind und ohne Erlaubnis der Kundschaft nicht zum Training generativer Foundation Models genutzt werden; die Modelle sind zustandslos, Prompts werden in der von der Kundschaft festgelegten Geografie verarbeitet, sofern keine globale oder Data-Zone-Bereitstellung gewählt ist, und eine Stichprobe von Prompts kann zur Missbrauchserkennung gespeichert und von autorisierten Beschäftigten geprüft werden, die sich bei Bereitstellungen im Europäischen Wirtschaftsraum dort befinden (Microsoft Learn Privacy). AWS erklärt, dass Modellanbieter keinen Zugriff auf die Konten haben, in denen Bedrock ihre Modelle betreibt, und damit auch nicht auf Prompts und Completions der Kundschaft (AWS Data Protection). Filter und Guardrails behandelt [[llm-guardrails-and-red-teaming|LLM-Guardrails und Red Teaming]].

#### Herkunft und Varianten

Die NIST-Definition stammt von 2011 (Mell & Grance, 2011). Die KI-Plattformen wurden mehrfach umbenannt: Bei Microsoft führt die Reihe von Azure AI Studio über Azure AI Foundry zu Microsoft Foundry, wobei Azure AI Services zu Foundry Tools wurden und die Assistants API durch die Responses API ersetzt wurde (Microsoft Learn), und Google fasste Vertex AI 2026 in der Gemini Enterprise Agent Platform zusammen (Google Cloud Release Notes). Datenplattformen wie [[databricks|Databricks]] bieten ähnliches Model Serving direkt neben den Daten an, siehe [[data-lakehouse|Data Lakehouse]].

### Wann einsetzen

- Eine Organisation betreibt ihre Daten und ihr Identitätsmanagement bereits in einer Cloud und will Modelle, Retrieval und Agenten innerhalb desselben Sicherheitsrahmens (Microsoft Learn; AWS).
- Mehrere Modelle verschiedener Anbieter sollen hinter einer API verglichen oder ausgetauscht werden (Microsoft Learn; AWS).
- Datenresidenz und vertragliche Zusagen zur Datenverarbeitung sind erforderlich, etwa bei personenbezogenen oder vertraulichen Daten (Microsoft Learn Privacy).

### Stärken und Grenzen

**Stärken**
- Keine eigene Infrastruktur für Modelle, Suche und Agenten; Bereitstellung bei Bedarf und Abrechnung nach Nutzung (Mell & Grance, 2011).
- Eingebaute Unternehmensfunktionen: Identität, Netzwerkisolation, Richtlinien, Evaluation und Tracing (Microsoft Learn).
- Dokumentierte Zusagen, dass Modellanbieter Kundendaten weder sehen noch damit trainieren (Microsoft Learn Privacy; AWS Data Protection).

**Grenzen**
- Produkte, Namen und [[apis|APIs]] ändern sich schnell, wie die Umbenennungen von 2024 bis 2026 zeigen (Microsoft Learn; Google Cloud Release Notes).
- Globale Bereitstellungsarten und Missbrauchserkennung bedeuten, dass Daten außerhalb der gewählten Region verarbeitet oder von Menschen geprüft werden können, sofern nichts anderes konfiguriert ist (Microsoft Learn Privacy).
- Plattformspezifische Dienste binden Anwendungen an einen Anbieter; Regeln zum Anbieterwechsel behandelt der [[data-act|Data Act]].

### Vergleich

| | Microsoft Foundry | Gemini Enterprise Agent Platform | Amazon Bedrock |
|---|---|---|---|
| Früherer Name | Azure AI Studio / Azure AI Foundry | Vertex AI (bis April 2026) | — |
| Modelle | > 10.000 (Microsoft, OpenAI, Anthropic, Meta, …) | Model Garden; eigenes Training inkl. AutoML | > 100 (Amazon, Anthropic, DeepSeek, OpenAI, xAI, …) |
| Retrieval | Azure AI Search, Wissensbasen in Foundry IQ | in den zitierten Quellen nicht behandelt | in den zitierten Quellen nicht behandelt |
| Agenten | Prompt Agents, Hosted Agents | Agent Runtime, Agent Studio | in den zitierten Quellen nicht behandelt |
| ML-Lebenszyklus | in den zitierten Quellen nicht behandelt | Training, Model Registry, Pipelines, Feature Store | Fine-Tuning, fortgesetztes Pre-Training, Distillation |

Quellen: Microsoft Learn; Microsoft Learn Search; Google Cloud; Google Cloud Release Notes; AWS. Den Selbstbetrieb offener Modelle beschreiben [[mlops-and-deployment|MLOps und Deployment]] und [[llm-cost-optimisation|LLM-Kostenoptimierung]].

### In der Praxis

Plattformressourcen werden am besten mit [[infrastructure-as-code|Infrastructure as Code]] angelegt und über [[ci-cd|CI/CD]] ausgeliefert, damit Entwicklung, Test und Produktion identisch bleiben. Bei personenbezogenen Daten aus der EU bestimmen Region und Bereitstellungsart, wo Prompts verarbeitet werden (Microsoft Learn Privacy), was für die [[gdpr|DSGVO]] relevant ist. Banken und Versicherungen behandeln solche Dienste als IKT-Auslagerung an Drittanbieter, mit Anforderungen aus [[dora|DORA]] und den [[eba-governance-and-outsourcing-guidelines|EBA-Leitlinien zu Auslagerungen]].

### Regulatorischer Kontext

Wer eine Cloud-KI-Plattform für personenbezogene Daten nutzt, macht den Anbieter zum Auftragsverarbeiter nach der [[gdpr|DSGVO]]; Microsofts Verarbeitung regelt dessen Data Protection Addendum (Microsoft Learn Privacy). Für Finanzunternehmen ist der Cloud-Anbieter ein IKT-Drittdienstleister nach [[dora|DORA]]. Der [[data-act|Data Act]] enthält Regeln zum Wechsel zwischen Datenverarbeitungsdiensten.

### Merksatz

Cloud-KI-Plattformen bündeln Modelle, Retrieval, Agenten, Evaluation und Steuerung als verwaltete PaaS-Dienste; die Wahl zwischen Microsoft Foundry, Googles Gemini Enterprise Agent Platform und Amazon Bedrock hängt von der bestehenden Cloud, den benötigten Modellen und den erforderlichen Zusagen zur Datenverarbeitung ab.

### Quellen

- Mell, P. & Grance, T. (2011). *The NIST Definition of Cloud Computing.* NIST Special Publication 800-145. [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/145/final)
- Microsoft Learn. *What is Microsoft Foundry?* Aktualisiert im September 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
- Microsoft Learn Privacy. *Data, privacy, and security for Foundry Models sold by Azure in Microsoft Foundry.* [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy)
- Microsoft Learn Search. *Introduction to Azure AI Search.* Aktualisiert im September 2026. [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- Google Cloud. *Introduction to machine learning on Gemini Enterprise Agent Platform.* [docs.cloud.google.com](https://docs.cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
- Google Cloud Release Notes. *Gemini Enterprise Agent Platform release notes*, Eintrag vom 22. April 2026. [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)
- AWS. *What is Amazon Bedrock?* Amazon Bedrock User Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- AWS Data Protection. *Data protection.* Amazon Bedrock User Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html)
