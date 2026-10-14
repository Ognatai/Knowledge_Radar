---
title_en: IT Governance Frameworks (COBIT, ISO/IEC 27001, IT-Grundschutz)
title_de: IT-Governance-Rahmenwerke (COBIT, ISO/IEC 27001, IT-Grundschutz)
entity_type: Concept
aliases:
- IT governance
- IT governance frameworks
- COBIT
- ISO/IEC 27001
- ISO 27001
- IT-Grundschutz
- Information security management system
- ISMS
- IT-Governance
sources:
- https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html
- https://www.isaca.org/resources/cobit
- https://evs.ee/en/iso-iec-27001-2022
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

IT governance frameworks give organisations a structure for directing and controlling their IT and information security, so that IT serves the business, risks are managed and supervisors and auditors can check the result. Three are widely used in Germany. COBIT 2019 from ISACA is a framework for the governance and management of enterprise information and technology with 40 governance and management objectives (ISACA). ISO/IEC 27001 specifies the requirements for an information security management system (ISMS) and can be certified (EVS, 2022). The [[bsi|BSI]]'s IT-Grundschutz is a German method for identifying and implementing security measures systematically, on whose basis an ISO 27001 certificate can be obtained (BSI). In banks and insurers, these frameworks are used to meet supervisory requirements such as [[marisk|MaRisk]] and [[dora|DORA]].

### How it works

```text
business goals, risk appetite, regulation (MaRisk, DORA, NIS2)
 ▼
governance framework: objectives, roles, committees (COBIT)
 ▼
management system for information security: policy, risk assessment, controls, audits (ISO/IEC 27001)
 ▼
concrete requirements and measures per system type (IT-Grundschutz modules)
 ▼
internal control system, audits, management review → continual improvement
```

#### 1. COBIT: governance and management of enterprise IT

COBIT helps enterprises "optimize enterprise governance of information and technology (EGIT)" and implement it for maximum enterprise value (ISACA). The current version, COBIT 2019, is an evolution of COBIT 5 built around "an expanded definition of governance"; its core model contains 40 governance and management objectives, design factors tailor a governance system to an enterprise, and focus-area guides cover DevOps, information and technology risk, information security and the implementation of the NIST Cybersecurity Framework (ISACA). COBIT thus describes what the governance and management of IT should achieve, which organisations then tailor to their own structure (ISACA).

#### 2. ISO/IEC 27001: the information security management system

"ISO/IEC 27001 specifies the requirements for establishing, implementing, maintaining and continually improving an information security management system", covering the planning, support and evaluation of that system; the current edition has been valid since 25 October 2022 and was amended in 2024 (EVS, 2022). As a management system standard, it is about the organisational system around security measures, not a list of products, and it can be used for certification, including on the basis of IT-Grundschutz (BSI). The structure is shared with other ISO management system standards such as ISO/IEC 42001 for AI ([[responsible-ai|responsible AI]]).

#### 3. IT-Grundschutz (BSI)

IT-Grundschutz is the method of the German Federal Office for Information Security (BSI) for information security; it treats technical, infrastructural, organisational and personnel aspects equally and helps identify and implement the necessary security measures systematically (BSI). It consists of the BSI standards, the IT-Grundschutz Compendium with requirements as text, which is being replaced by a digital rule set in JSON format, IT-Grundschutz profiles and tools; checklists for a basic level of protection ("Weg in die Basis-Absicherung") are to become part of it (BSI). Small institutions can implement basic requirements with checklists without building a full ISMS, while larger ones build a complete ISMS step by step, and an ISO 27001 certificate can be obtained on the basis of IT-Grundschutz (BSI). The BSI's legal role is described in [[bsig|BSIG]].

#### 4. Use in regulated financial institutions

German banks and insurers translate supervisory requirements into these frameworks. [[marisk|MaRisk]] requires proper business organisation with an internal control system; [[dora|DORA]] requires an ICT risk management framework, incident reporting, resilience testing and management of ICT third-party risk; the details are summarised in [[information-security-in-banking|information security in banking]]. Critical infrastructure operators additionally fall under [[nis2-directive|NIS2]] and the German [[kritis-dachgesetz|KRITIS Umbrella Act]].

#### Origin and variants

COBIT was developed by ISACA, with COBIT 2019 succeeding COBIT 5 (ISACA). ISO/IEC 27001 is published jointly by ISO and IEC, in its current edition from 2022 (EVS, 2022). IT-Grundschutz is developed by the BSI, which has also used it as a basis for ISO 27001 certification (BSI).

### When to use it

- Building or reviewing IT governance in an organisation that must show supervisors or auditors how IT risks are controlled (ISACA).
- Establishing a certifiable information security management system (EVS, 2022).
- German public bodies and companies that want concrete, catalogued security requirements, including small institutions starting with a basic level of protection (BSI).

### Strengths and limitations

**Strengths**
- Common, recognised structures make IT governance comparable and auditable (ISACA; EVS, 2022).
- IT-Grundschutz provides concrete requirements and a route to ISO 27001 certification (BSI).
- Management system standards build in continual improvement (EVS, 2022).

**Limitations**
- COBIT needs tailoring to each enterprise, for which it provides design factors and a separate design guide (ISACA).
- The IT-Grundschutz Compendium is being replaced by a digital rule set, so references and tooling change (BSI).
- The standards themselves (COBIT publications, ISO/IEC 27001) are not freely available.

### Comparison

| | COBIT 2019 | ISO/IEC 27001:2022 | IT-Grundschutz |
|---|---|---|---|
| Publisher | ISACA | ISO/IEC | BSI (Germany) |
| Scope | governance and management of enterprise IT | information security management system | information security method with concrete requirements |
| Core | 40 governance and management objectives | requirements for establishing and improving an ISMS | standards, compendium, profiles, checklists |
| Certifiable | no (framework) | yes | ISO 27001 certificate on the basis of IT-Grundschutz |

Sources: ISACA; EVS (2022); BSI.

### In practice

AI systems are brought into existing IT governance rather than governed separately: their models, data and cloud services appear in the IT asset inventory, risk assessment and outsourcing register ([[cloud-ai-platforms|cloud AI platforms]], [[eba-governance-and-outsourcing-guidelines|EBA outsourcing guidelines]]), and an AI management system can be aligned with an existing ISMS ([[responsible-ai|responsible AI]]).

### Regulatory context

[[dora|DORA]], [[marisk|MaRisk]], [[nis2-directive|NIS2]] and the [[bsig|BSIG]] set the legal requirements; COBIT, ISO/IEC 27001 and IT-Grundschutz are common ways to implement and demonstrate them.

### Key takeaway

COBIT structures the governance and management of enterprise IT, ISO/IEC 27001 defines a certifiable information security management system and IT-Grundschutz supplies concrete German security requirements with a route to ISO 27001 certification; regulated institutions use them to meet MaRisk and DORA.

### Sources

- BSI. *IT-Grundschutz.* Bundesamt für Sicherheit in der Informationstechnik. [bsi.bund.de](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html)
- ISACA. *COBIT.* ISACA resources. [isaca.org](https://www.isaca.org/resources/cobit)
- EVS (2022). *ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection — Information security management systems — Requirements.* Estonian Centre for Standardisation and Accreditation, catalogue entry. [evs.ee](https://evs.ee/en/iso-iec-27001-2022)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

IT-Governance-Rahmenwerke geben Organisationen eine Struktur, um ihre IT und Informationssicherheit zu steuern und zu überwachen, damit die IT dem Geschäft dient, Risiken gesteuert werden und Aufsicht und Prüfende das Ergebnis kontrollieren können. Drei sind in Deutschland verbreitet. COBIT 2019 von ISACA ist ein Rahmenwerk für Governance und Management von Unternehmensinformation und -technologie mit 40 Governance- und Managementzielen (ISACA). ISO/IEC 27001 legt die Anforderungen an ein Informationssicherheits-Managementsystem (ISMS) fest und ist zertifizierbar (EVS, 2022). Der IT-Grundschutz des [[bsi|BSI]] ist eine Methode, um Sicherheitsmaßnahmen systematisch zu ermitteln und umzusetzen, auf deren Grundlage ein ISO-27001-Zertifikat erlangt werden kann (BSI). In Banken und Versicherungen dienen diese Rahmenwerke dazu, aufsichtliche Anforderungen wie die [[marisk|MaRisk]] und [[dora|DORA]] zu erfüllen.

### Funktionsweise

```text
Geschäftsziele, Risikoappetit, Regulierung (MaRisk, DORA, NIS2)
 ▼
Governance-Rahmenwerk: Ziele, Rollen, Gremien (COBIT)
 ▼
Managementsystem für Informationssicherheit: Leitlinie, Risikobewertung, Maßnahmen, Audits (ISO/IEC 27001)
 ▼
konkrete Anforderungen und Maßnahmen je Systemart (Bausteine des IT-Grundschutzes)
 ▼
internes Kontrollsystem, Prüfungen, Managementbewertung → kontinuierliche Verbesserung
```

#### 1. COBIT: Governance und Management der Unternehmens-IT

COBIT hilft Unternehmen, „optimize enterprise governance of information and technology (EGIT)“ und sie für den größtmöglichen Unternehmenswert umzusetzen (ISACA). Die aktuelle Fassung, COBIT 2019, ist eine Weiterentwicklung von COBIT 5 und baut auf „an expanded definition of governance“ auf; ihr Kernmodell enthält 40 Governance- und Managementziele, Designfaktoren passen ein Governance-System an ein Unternehmen an, und Leitfäden zu Schwerpunkten behandeln DevOps, Informations- und Technologierisiken, Informationssicherheit und die Umsetzung des NIST Cybersecurity Framework (ISACA). COBIT beschreibt damit, was Governance und Management der IT erreichen sollen, was Organisationen dann an ihre eigene Struktur anpassen (ISACA).

#### 2. ISO/IEC 27001: das Informationssicherheits-Managementsystem

„ISO/IEC 27001 specifies the requirements for establishing, implementing, maintaining and continually improving an information security management system“ und umfasst Planung, Unterstützung und Bewertung dieses Systems; die aktuelle Ausgabe gilt seit dem 25. Oktober 2022 und wurde 2024 ergänzt (EVS, 2022). Als Norm für Managementsysteme geht es um das organisatorische System rund um Sicherheitsmaßnahmen, nicht um eine Liste von Produkten, und sie kann zur Zertifizierung genutzt werden, auch auf Basis des IT-Grundschutzes (BSI). Den Aufbau teilt die Norm mit anderen ISO-Normen für Managementsysteme wie ISO/IEC 42001 für KI ([[responsible-ai|Responsible AI]]).

#### 3. IT-Grundschutz (BSI)

Der IT-Grundschutz ist die Methode des Bundesamts für Sicherheit in der Informationstechnik (BSI) für Informationssicherheit; er betrachtet technische, infrastrukturelle, organisatorische und personelle Aspekte gleichermaßen und hilft, notwendige Sicherheitsmaßnahmen systematisch zu ermitteln und umzusetzen (BSI). Er besteht aus den BSI-Standards, dem IT-Grundschutz-Kompendium mit Anforderungen als Text, das durch ein digitales Regelwerk im JSON-Format abgelöst wird, IT-Grundschutz-Profilen und Hilfsmitteln; Checklisten für die Basis-Absicherung („Weg in die Basis-Absicherung“) sollen fester Bestandteil werden (BSI). Kleine Institutionen können grundlegende Anforderungen mit Checklisten umsetzen, ohne ein vollständiges ISMS aufzubauen, größere bauen schrittweise ein vollständiges ISMS auf, und auf Basis des IT-Grundschutzes kann ein ISO-27001-Zertifikat erlangt werden (BSI). Die gesetzliche Rolle des BSI beschreibt [[bsig|BSIG]].

#### 4. Einsatz in regulierten Finanzinstituten

Deutsche Banken und Versicherungen übersetzen aufsichtliche Anforderungen in diese Rahmenwerke. Die [[marisk|MaRisk]] verlangen eine ordnungsgemäße Geschäftsorganisation mit internem Kontrollsystem; [[dora|DORA]] verlangt einen Rahmen für das IKT-Risikomanagement, Meldungen von Vorfällen, Tests der Widerstandsfähigkeit und die Steuerung von IKT-Drittparteirisiken; die Einzelheiten fasst [[information-security-in-banking|Informationssicherheit in Banken]] zusammen. Betreiber kritischer Infrastrukturen fallen zusätzlich unter [[nis2-directive|NIS2]] und das [[kritis-dachgesetz|KRITIS-Dachgesetz]].

#### Herkunft und Varianten

COBIT wurde von ISACA entwickelt, COBIT 2019 folgte auf COBIT 5 (ISACA). ISO/IEC 27001 wird gemeinsam von ISO und IEC herausgegeben, in der aktuellen Ausgabe von 2022 (EVS, 2022). Der IT-Grundschutz wird vom BSI entwickelt, das ihn auch als Grundlage für ISO-27001-Zertifizierungen nutzt (BSI).

### Wann einsetzen

- Beim Aufbau oder der Überprüfung der IT-Governance in einer Organisation, die Aufsicht oder Prüfenden zeigen muss, wie IT-Risiken gesteuert werden (ISACA).
- Beim Aufbau eines zertifizierbaren Informationssicherheits-Managementsystems (EVS, 2022).
- In deutschen Behörden und Unternehmen, die konkrete, katalogisierte Sicherheitsanforderungen wollen, auch kleine Institutionen, die mit einer Basis-Absicherung beginnen (BSI).

### Stärken und Grenzen

**Stärken**
- Gemeinsame, anerkannte Strukturen machen IT-Governance vergleichbar und prüfbar (ISACA; EVS, 2022).
- Der IT-Grundschutz liefert konkrete Anforderungen und einen Weg zur ISO-27001-Zertifizierung (BSI).
- Normen für Managementsysteme sehen kontinuierliche Verbesserung vor (EVS, 2022).

**Grenzen**
- COBIT muss an jedes Unternehmen angepasst werden, wofür es Designfaktoren und einen eigenen Designleitfaden bietet (ISACA).
- Das IT-Grundschutz-Kompendium wird durch ein digitales Regelwerk abgelöst, sodass sich Verweise und Werkzeuge ändern (BSI).
- Die Normen selbst (COBIT-Veröffentlichungen, ISO/IEC 27001) sind nicht frei verfügbar.

### Vergleich

| | COBIT 2019 | ISO/IEC 27001:2022 | IT-Grundschutz |
|---|---|---|---|
| Herausgeber | ISACA | ISO/IEC | BSI (Deutschland) |
| Gegenstand | Governance und Management der Unternehmens-IT | Informationssicherheits-Managementsystem | Methode der Informationssicherheit mit konkreten Anforderungen |
| Kern | 40 Governance- und Managementziele | Anforderungen an Aufbau und Verbesserung eines ISMS | Standards, Kompendium, Profile, Checklisten |
| Zertifizierbar | nein (Rahmenwerk) | ja | ISO-27001-Zertifikat auf Basis von IT-Grundschutz |

Quellen: ISACA; EVS (2022); BSI.

### In der Praxis

KI-Systeme werden in die bestehende IT-Governance eingebunden statt getrennt gesteuert: Ihre Modelle, Daten und Cloud-Dienste erscheinen im IT-Bestandsverzeichnis, in der Risikobewertung und im Auslagerungsregister ([[cloud-ai-platforms|Cloud-KI-Plattformen]], [[eba-governance-and-outsourcing-guidelines|EBA-Leitlinien zu Auslagerungen]]), und ein KI-Managementsystem lässt sich an einem bestehenden ISMS ausrichten ([[responsible-ai|Responsible AI]]).

### Regulatorischer Kontext

[[dora|DORA]], [[marisk|MaRisk]], [[nis2-directive|NIS2]] und das [[bsig|BSIG]] setzen die rechtlichen Anforderungen; COBIT, ISO/IEC 27001 und IT-Grundschutz sind verbreitete Wege, sie umzusetzen und nachzuweisen.

### Merksatz

COBIT strukturiert Governance und Management der Unternehmens-IT, ISO/IEC 27001 legt ein zertifizierbares Informationssicherheits-Managementsystem fest und der IT-Grundschutz liefert konkrete deutsche Sicherheitsanforderungen mit einem Weg zur ISO-27001-Zertifizierung; regulierte Institute nutzen sie, um MaRisk und DORA zu erfüllen.

### Quellen

- BSI. *IT-Grundschutz.* Bundesamt für Sicherheit in der Informationstechnik. [bsi.bund.de](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html)
- ISACA. *COBIT.* ISACA resources. [isaca.org](https://www.isaca.org/resources/cobit)
- EVS (2022). *ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection — Information security management systems — Requirements.* Estonian Centre for Standardisation and Accreditation, catalogue entry. [evs.ee](https://evs.ee/en/iso-iec-27001-2022)
