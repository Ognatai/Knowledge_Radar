---
title_en: OWASP
title_de: OWASP
entity_type: Organisation
jurisdiction: International
aliases:
- OWASP
- Open Worldwide Application Security Project
- OWASP Foundation
sources:
- https://owasp.org/about/
- https://owasp.org/www-project-top-ten/
- https://owasp.org/Top10/2025/
- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://genai.owasp.org/llm-top-10/
- https://owasp.org/www-project-application-security-verification-standard/
- https://cheatsheetseries.owasp.org/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The Open Worldwide Application Security Project (OWASP) is a 501(c)(3) nonprofit foundation that works to improve the security of software through community-led open-source projects, local chapters, conferences and training; all its projects, tools and documents are free and open to anyone (OWASP, About). It is best known for its Top 10 awareness documents: the OWASP Top 10 for web applications, whose current version is from 2025, the API Security Top 10 (2023) and the Top 10 for LLM applications (2025), which names prompt injection as the first risk (OWASP Top 10; OWASP API Security; OWASP GenAI). For verification and implementation it publishes the Application Security Verification Standard (ASVS) and the Cheat Sheet Series, which by now includes sheets on LLM prompt injection, RAG security and MCP security (OWASP ASVS; OWASP Cheat Sheet Series). For AI development, the LLM Top 10 is the common checklist for securing LLM applications ([[llm-guardrails|LLM guardrails]], [[red-teaming|red teaming]]).

### Key facts

| | |
|---|---|
| Legal form | 501(c)(3) nonprofit foundation, OWASP Foundation, Inc. (United States) |
| Founded | project launched 1 December 2001; incorporated 21 April 2004 |
| Community | 250+ local chapters, 275+ active projects, tens of thousands of members (own figures) |
| Governance | elected board since 2011 |
| Licence of outputs | free and open; e.g. ASVS under CC BY-SA 4.0 |
| Known for | OWASP Top 10, API Security Top 10, Top 10 for LLM applications, ASVS, Cheat Sheet Series |

Sources: OWASP, About; OWASP ASVS.

### Mandate and tasks

OWASP's mission is "to be the global open community that powers secure software through education, tools, and collaboration", with the vision of "No More Insecure Software" (OWASP, About). It describes itself as an open community dedicated to enabling organisations to conceive, develop, acquire, operate and maintain applications that can be trusted, and lists openness, innovation, global participation and integrity, including vendor neutrality, as core values (OWASP, About).

### Structure and working methods

OWASP's programme consists of community-led open-source projects (code, documentation and standards), more than 250 local chapters worldwide, members, and conferences and training (OWASP, About). Projects are run by volunteer project leaders and contributors; the OWASP Top 10 and the ASVS are classified as flagship projects (OWASP Top 10; OWASP ASVS). OWASP started as a passion project in 2001, was incorporated as a nonprofit in 2004, established chapters on every continent by 2010 and introduced an elected board in 2011 (OWASP, About). Generative AI security is organised in the separate OWASP Gen AI Security Project, which maintains the LLM Top 10 together with initiatives on agentic security, AI red teaming and AI security governance (OWASP GenAI).

### Key outputs

#### OWASP Top 10 (web applications)

The OWASP Top 10 is "a standard awareness document for developers and web application security" and represents a broad consensus about the most critical security risks to web applications; OWASP calls adopting it perhaps the most effective first step towards a development culture that produces secure code (OWASP Top 10). The 2025 edition lists A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures and A10 Mishandling of Exceptional Conditions; previous editions are from 2021 and 2017 (OWASP Top 10:2025).

#### API Security Top 10

The API Security Top 10 (2023) covers risks specific to [[apis|APIs]]: broken object level authorisation, broken authentication, broken object property level authorisation, unrestricted resource consumption, broken function level authorisation, unrestricted access to sensitive business flows, server-side request forgery, security misconfiguration, improper inventory management and unsafe consumption of APIs (OWASP API Security). Broken object level authorisation is first because APIs expose endpoints that handle object identifiers, so every function that accesses data by an ID from the user needs an authorisation check (OWASP API Security); authentication flaws are covered in detail in [[api-authentication|API authentication]].

#### Top 10 for LLM applications

The Top 10 for LLM and generative AI applications (2025) names LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation and LLM10 Unbounded Consumption (OWASP GenAI). It is available in many languages, including German, and an earlier 2023/24 version exists (OWASP GenAI). The individual risks are discussed in [[prompt-injection|prompt injection]], [[sleeper-agents|sleeper agents]] (poisoning), [[llm-guardrails|LLM guardrails]] and [[red-teaming|red teaming]].

#### ASVS and Cheat Sheet Series

The Application Security Verification Standard provides a basis for testing technical security controls of web applications and a list of requirements for secure development; it aims to normalise the coverage and rigour of security verification with a commercially workable open standard (OWASP ASVS). Requirements have identifiers such as `v5.0.0-1.2.5` (version, chapter, section, requirement), are available as CSV and JSON, and the current version is 5.0.0 under CC BY-SA 4.0 (OWASP ASVS). The Cheat Sheet Series is a concise collection of guidance on specific topics, from authentication, injection prevention and secrets management to LLM prompt injection prevention, RAG security, MCP security, AI agent security and secure coding with AI (OWASP Cheat Sheet Series).

### Relationship to other bodies

OWASP is independent and vendor neutral and is financed by members, corporate supporters and donations (OWASP, About). Its documents can be used alongside national guidance, such as that of the [[bsi|BSI]] on attacks on AI systems, and alongside EU requirements on cybersecurity, for example those of the [[cyber-resilience-act|Cyber Resilience Act]] for products with digital elements, without being part of them.

### In practice

The Top 10 lists are used to structure threat models, code reviews, penetration tests and training; ASVS requirements turn them into testable checks, for example as acceptance criteria or in [[ci-cd|CI/CD]] pipelines (OWASP ASVS). For LLM applications, the LLM Top 10 gives red-team plans and guardrail designs a shared vocabulary ([[red-teaming|red teaming]]), and agent tools are reviewed against excessive agency and improper output handling ([[agentic-ai|agentic AI]], [[tool-calling|tool calling]]).

### Relevance for AI development

AI applications are also web applications and APIs, so the classic Top 10 and the API Top 10 apply to them unchanged, for example broken access control on a retrieval endpoint or unrestricted resource consumption on a model API (OWASP Top 10:2025; OWASP API Security). The LLM Top 10 adds the risks that come from the model itself: prompt injection, poisoning, leakage of sensitive data or system prompts, weaknesses in vector stores and [[embeddings|embeddings]] ([[vector-databases|vector databases]]), misinformation and unbounded consumption (OWASP GenAI). OWASP's cheat sheets on RAG and MCP security translate these risks into implementation advice for [[retrieval-augmented-generation|RAG]] systems and [[mcp-and-related-protocols|MCP]] servers (OWASP Cheat Sheet Series).

### Sources

- OWASP Foundation (2026). *About OWASP.* [owasp.org](https://owasp.org/about/)
- OWASP Foundation (2026). *OWASP Top 10* (project page). [owasp.org](https://owasp.org/www-project-top-ten/)
- OWASP Top 10 Team (2025). *OWASP Top 10:2025.* [owasp.org](https://owasp.org/Top10/2025/)
- OWASP API Security Project (2023). *OWASP Top 10 API Security Risks – 2023.* [owasp.org](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- OWASP Gen AI Security Project (2025). *OWASP Top 10 for LLM Applications 2025.* [genai.owasp.org](https://genai.owasp.org/llm-top-10/)
- OWASP Foundation (2026). *OWASP Application Security Verification Standard (ASVS).* [owasp.org](https://owasp.org/www-project-application-security-verification-standard/)
- OWASP Foundation (2026). *OWASP Cheat Sheet Series.* [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Das Open Worldwide Application Security Project (OWASP) ist eine gemeinnützige Stiftung nach 501(c)(3) US-Recht, die die Sicherheit von Software durch gemeinschaftlich getragene Open-Source-Projekte, lokale Gruppen (Chapters), Konferenzen und Schulungen verbessern will; alle Projekte, Werkzeuge und Dokumente sind kostenlos und für alle offen (OWASP, About). Bekannt ist es vor allem für seine Top-10-Dokumente: die OWASP Top 10 für Webanwendungen, deren aktuelle Fassung von 2025 stammt, die API Security Top 10 (2023) und die Top 10 für LLM-Anwendungen (2025), die Prompt Injection als erstes Risiko nennen (OWASP Top 10; OWASP API Security; OWASP GenAI). Für Prüfung und Umsetzung veröffentlicht es den Application Security Verification Standard (ASVS) und die Cheat Sheet Series, die inzwischen auch Blätter zu LLM Prompt Injection, RAG-Sicherheit und MCP-Sicherheit enthält (OWASP ASVS; OWASP Cheat Sheet Series). Für die KI-Entwicklung sind die LLM Top 10 die gemeinsame Checkliste zur Absicherung von LLM-Anwendungen ([[llm-guardrails|LLM-Guardrails]], [[red-teaming|Red Teaming]]).

### Eckdaten

| | |
|---|---|
| Rechtsform | gemeinnützige Stiftung nach 501(c)(3), OWASP Foundation, Inc. (USA) |
| Gründung | Projektstart am 1. Dezember 2001; eingetragen am 21. April 2004 |
| Gemeinschaft | über 250 lokale Chapters, über 275 aktive Projekte, Zehntausende Mitglieder (eigene Angaben) |
| Leitung | gewählter Vorstand (Board) seit 2011 |
| Lizenz der Ergebnisse | kostenlos und offen; z. B. ASVS unter CC BY-SA 4.0 |
| Bekannt für | OWASP Top 10, API Security Top 10, Top 10 für LLM-Anwendungen, ASVS, Cheat Sheet Series |

Quellen: OWASP, About; OWASP ASVS.

### Auftrag und Aufgaben

Die Mission von OWASP lautet „to be the global open community that powers secure software through education, tools, and collaboration“, die Vision „No More Insecure Software“ (OWASP, About). OWASP beschreibt sich als offene Gemeinschaft, die Organisationen befähigen will, vertrauenswürdige Anwendungen zu konzipieren, zu entwickeln, zu beschaffen, zu betreiben und zu pflegen, und nennt Offenheit, Innovation, weltweite Beteiligung und Integrität, einschließlich Herstellerneutralität, als Grundwerte (OWASP, About).

### Aufbau und Arbeitsweise

Das Programm von OWASP besteht aus gemeinschaftlich getragenen Open-Source-Projekten (Code, Dokumentation und Standards), über 250 lokalen Chapters weltweit, Mitgliedern sowie Konferenzen und Schulungen (OWASP, About). Projekte werden von ehrenamtlichen Projektleitungen und Mitwirkenden betrieben; die OWASP Top 10 und der ASVS sind als Flagship-Projekte eingestuft (OWASP Top 10; OWASP ASVS). OWASP begann 2001 als Herzensprojekt, wurde 2004 als gemeinnützige Organisation eingetragen, hatte 2010 Chapters auf allen Kontinenten und führte 2011 einen gewählten Vorstand ein (OWASP, About). Die Sicherheit generativer KI ist im eigenen OWASP Gen AI Security Project organisiert, das die LLM Top 10 pflegt, zusammen mit Initiativen zu agentischer Sicherheit, AI Red Teaming und AI Security Governance (OWASP GenAI).

### Wichtige Ergebnisse

#### OWASP Top 10 (Webanwendungen)

Die OWASP Top 10 sind „a standard awareness document for developers and web application security“ und bilden einen breiten Konsens über die kritischsten Sicherheitsrisiken von Webanwendungen; OWASP nennt ihre Übernahme den vielleicht wirksamsten ersten Schritt zu einer Entwicklungskultur, die sicheren Code hervorbringt (OWASP Top 10). Die Ausgabe 2025 nennt A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures und A10 Mishandling of Exceptional Conditions; frühere Ausgaben stammen von 2021 und 2017 (OWASP Top 10:2025).

#### API Security Top 10

Die API Security Top 10 (2023) behandeln Risiken speziell für [[apis|APIs]]: fehlerhafte Autorisierung auf Objektebene (Broken Object Level Authorization), fehlerhafte Authentifizierung, fehlerhafte Autorisierung auf Ebene der Objekteigenschaften, unbegrenzter Ressourcenverbrauch, fehlerhafte Autorisierung auf Funktionsebene, uneingeschränkter Zugriff auf sensible Geschäftsabläufe, Server-Side Request Forgery, Fehlkonfiguration, mangelhafte Bestandsverwaltung und unsichere Nutzung fremder APIs (OWASP API Security). Fehlerhafte Autorisierung auf Objektebene steht an erster Stelle, weil APIs Endpunkte anbieten, die Objektkennungen verarbeiten; jede Funktion, die mit einer ID der Nutzenden auf Daten zugreift, braucht daher eine Autorisierungsprüfung (OWASP API Security). Authentifizierungsfehler behandelt [[api-authentication|API-Authentifizierung]] ausführlich.

#### Top 10 für LLM-Anwendungen

Die Top 10 für LLM- und GenAI-Anwendungen (2025) nennen LLM01 Prompt Injection, LLM02 Offenlegung sensibler Informationen, LLM03 Lieferkette, LLM04 Daten- und Modellvergiftung, LLM05 unsachgemäße Verarbeitung von Ausgaben, LLM06 übermäßige Handlungsbefugnis (Excessive Agency), LLM07 Offenlegung des System-Prompts, LLM08 Schwächen von Vektoren und [[embeddings|Embeddings]], LLM09 Fehlinformation und LLM10 unbegrenzter Ressourcenverbrauch (OWASP GenAI). Sie liegen in vielen Sprachen vor, auch auf Deutsch, und es gibt eine frühere Fassung 2023/24 (OWASP GenAI). Die einzelnen Risiken behandeln [[prompt-injection|Prompt Injection]], [[sleeper-agents|Sleeper Agents]] (Vergiftung), [[llm-guardrails|LLM-Guardrails]] und [[red-teaming|Red Teaming]].

#### ASVS und Cheat Sheet Series

Der Application Security Verification Standard bietet eine Grundlage, um technische Sicherheitsmaßnahmen von Webanwendungen zu prüfen, und eine Liste von Anforderungen für sichere Entwicklung; er soll Abdeckung und Gründlichkeit von Sicherheitsprüfungen mit einem kommerziell nutzbaren offenen Standard vereinheitlichen (OWASP ASVS). Die Anforderungen haben Kennungen wie `v5.0.0-1.2.5` (Version, Kapitel, Abschnitt, Anforderung), liegen als CSV und JSON vor, und die aktuelle Version 5.0.0 steht unter CC BY-SA 4.0 (OWASP ASVS). Die Cheat Sheet Series ist eine knappe Sammlung von Anleitungen zu einzelnen Themen, von Authentifizierung, Schutz vor Injection und Verwaltung von Secrets bis zu LLM Prompt Injection Prevention, RAG-Sicherheit, MCP-Sicherheit, Sicherheit von KI-Agenten und sicherem Programmieren mit KI (OWASP Cheat Sheet Series).

### Verhältnis zu anderen Stellen

OWASP ist unabhängig und herstellerneutral und finanziert sich über Mitglieder, Unternehmensunterstützer und Spenden (OWASP, About). Seine Dokumente lassen sich neben nationalen Hinweisen nutzen, etwa denen des [[bsi|BSI]] zu Angriffen auf KI-Systeme, und neben EU-Anforderungen an die Cybersicherheit, etwa denen des [[cyber-resilience-act|Cyber Resilience Act]] für Produkte mit digitalen Elementen, ohne Teil davon zu sein.

### In der Praxis

Die Top-10-Listen dienen dazu, Bedrohungsmodelle, Code Reviews, Penetrationstests und Schulungen zu gliedern; die ASVS-Anforderungen machen daraus prüfbare Kriterien, etwa als Abnahmekriterien oder in [[ci-cd|CI/CD]]-Pipelines (OWASP ASVS). Bei LLM-Anwendungen geben die LLM Top 10 Red-Team-Plänen und Guardrail-Entwürfen ein gemeinsames Vokabular ([[red-teaming|Red Teaming]]), und Agenten-Tools werden auf übermäßige Handlungsbefugnis und unsachgemäße Verarbeitung von Ausgaben geprüft ([[agentic-ai|Agentic AI]], [[tool-calling|Tool Calling]]).

### Bedeutung für die KI-Entwicklung

KI-Anwendungen sind auch Webanwendungen und APIs, daher gelten die klassischen Top 10 und die API Top 10 für sie unverändert, etwa fehlerhafte Zugriffskontrolle an einem Retrieval-Endpunkt oder unbegrenzter Ressourcenverbrauch an einer Modell-API (OWASP Top 10:2025; OWASP API Security). Die LLM Top 10 ergänzen die Risiken, die vom Modell selbst ausgehen: Prompt Injection, Vergiftung, Abfluss sensibler Daten oder des System-Prompts, Schwächen in Vektorspeichern und Embeddings ([[vector-databases|Vektordatenbanken]]), Fehlinformation und unbegrenzter Verbrauch (OWASP GenAI). Die Cheat Sheets von OWASP zu RAG- und MCP-Sicherheit übersetzen diese Risiken in Umsetzungshinweise für [[retrieval-augmented-generation|RAG]]-Systeme und [[mcp-and-related-protocols|MCP]]-Server (OWASP Cheat Sheet Series).

### Quellen

- OWASP Foundation (2026). *About OWASP.* [owasp.org](https://owasp.org/about/)
- OWASP Foundation (2026). *OWASP Top 10* (project page). [owasp.org](https://owasp.org/www-project-top-ten/)
- OWASP Top 10 Team (2025). *OWASP Top 10:2025.* [owasp.org](https://owasp.org/Top10/2025/)
- OWASP API Security Project (2023). *OWASP Top 10 API Security Risks – 2023.* [owasp.org](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- OWASP Gen AI Security Project (2025). *OWASP Top 10 for LLM Applications 2025.* [genai.owasp.org](https://genai.owasp.org/llm-top-10/)
- OWASP Foundation (2026). *OWASP Application Security Verification Standard (ASVS).* [owasp.org](https://owasp.org/www-project-application-security-verification-standard/)
- OWASP Foundation (2026). *OWASP Cheat Sheet Series.* [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/)
