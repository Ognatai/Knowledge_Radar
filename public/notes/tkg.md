---
title_en: Telecommunications Act (TKG)
title_de: Telekommunikationsgesetz (TKG)
entity_type: Regulation
jurisdiction: DE
instrument: national-law
status: in-force
official_reference: BGBl. I 2021, 1858
consolidated_version: 2026-10-06
aliases:
- TKG
- Telekommunikationsgesetz
- Telecommunications Act
sources:
- https://www.gesetze-im-internet.de/tkg_2021/
- https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62019CJ0793
---

## EN

> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial summary of the German text.

### TL;DR

The Telekommunikationsgesetz (TKG) regulates telecommunications in Germany: it aims to promote competition and high-performance infrastructure through technology-neutral regulation and to guarantee adequate services nationwide, and it applies to everyone who operates telecommunications networks or systems or provides telecommunications services in Germany (§ 1 TKG). Its about 230 sections cover market and access regulation, customer protection, frequencies, numbering, rights of way, universal service, public security and the [[federal-network-agency|Bundesnetzagentur]]. This note covers only the parts most relevant to data, security and AI: the purpose and definitions (Part 1), public security (Part 10, Section 1) with security measures, incident reporting, lawful interception, information requests and traffic data retention, and the agency's enforcement powers and fines. Confidentiality of communications and telecommunications data protection are no longer in the TKG but in the [[tdddg|TDDDG]].

### Key facts

| | |
|---|---|
| Official reference | Telekommunikationsgesetz of 23 June 2021, BGBl. I 2021, 1858 (Article 1 of the Telecommunications Modernisation Act) |
| Type / jurisdiction | federal law, Germany |
| In force | 1 December 2021 |
| Competent authority | Bundesnetzagentur (§ 191 TKG), with the [[bsi\|BSI]] and the Federal Commissioner for Data Protection for security and data matters (§§ 167, 168, 169 TKG) |
| Version summarised | consolidated text, last amended on 6 October 2026 |
| Coverage of this note | Part 1 (§§ 1–3), Part 10 Section 1 (§§ 164–183), §§ 191, 202, 203, 228 |

### Scope

The TKG applies to all undertakings and persons that operate telecommunications networks or systems or provide telecommunications services in Germany, and to others entitled or obliged under the Act (§ 1 Abs. 2 TKG). Telecommunications services are services normally provided for remuneration over telecommunications networks, namely internet access services, interpersonal telecommunications services and services consisting wholly or mainly in the conveyance of signals, excluding services that provide or exercise editorial control over content (§ 3 Nr. 61 TKG).

**Covered here:** general provisions (§§ 1–3), public security (§§ 164–183), the agency's general task, enforcement and information powers (§§ 191, 202, 203) and fines (§ 228). **Left out:** market and access regulation (Part 2), customer protection (Part 3), terminal equipment (Part 4), infrastructure information (Part 5), frequencies (Part 6), numbering (Part 7), rights of way (Part 8), universal service (Part 9), emergency preparedness (Part 10 Section 2), the remaining organisation and procedure rules of Part 11, levies (Part 12) and transitional provisions (Part 14).

### Part 1 — General Provisions

#### § 1 — Purpose of the Act, Scope

Aims to promote competition in telecommunications and high-performance infrastructure through **technology-neutral regulation** and to guarantee adequate and sufficient services nationwide; laying telecommunications lines for public networks is in the **overriding public interest until 31 December 2030**. Applies to everyone who operates networks or systems or provides telecommunications services in Germany.

#### § 2 — Objectives and Principles of Regulation

Makes telecommunications regulation a sovereign task of the Federation and lists its objectives: connectivity and access to very high capacity networks, fair competition, user and consumer interests including **public security and the security of networks and services**, the EU internal market and efficient, interference-free use of frequencies.

#### § 3 — Definitions

Defines over 70 terms. Relevant for data and security: **subscriber data** (*Bestandsdaten*), data needed to establish, shape, change or end a contract (Nr. 6); **end user** (Nr. 13); **interpersonal telecommunications service** (Nr. 24); **security of networks and services**, the ability to resist attacks on availability, authenticity, integrity or confidentiality (Nr. 52); **security incident** (Nr. 53); **telecommunications services** (Nr. 61); **traffic data** (*Verkehrsdaten*), data whose collection, processing or use is required to provide a telecommunications service (Nr. 70); and **personal data breach** (Nr. 71).

### Part 10 — Public Security and Emergency Preparedness (Section 1: Public Security)

#### § 164 — Emergency Calls

Requires providers of number-based interpersonal services to enable **free emergency calls to 112 and 110**, routed without delay to the competent emergency call centre with the caller's number and the data needed to determine the location; emergency calls take priority.

#### § 164a — Public Warnings

Requires mobile network operators to keep equipment ready to send warnings of major emergencies and disasters, triggered via the federal warning system, to all mobile devices in the area defined by the authority.

#### § 165 — Technical and Organisational Safeguards

##### What is it about?

The core security obligation of telecommunications providers.

##### What does the section require?

Everyone who provides or participates in telecommunications services must take appropriate technical precautions to protect the **secrecy of telecommunications** and against **personal data breaches**, taking the state of the art into account (Abs. 1). Operators of public networks and providers of publicly available services must protect their telecommunications and data processing systems against disruptions, including external attacks and disasters, and manage the risks to the security of networks and services, in particular with measures such as **encryption** against unauthorised access; the security level must be appropriate to the risk, considering state of the art, standards, costs, risk exposure, size, likelihood and severity of incidents (Abs. 2). Providers that are particularly important or important entities under the BSI Act must follow an all-hazards approach covering at least risk analysis, incident handling, business continuity, supply-chain security, secure acquisition and development including vulnerability management, effectiveness assessment, training, cryptography, personnel security and access control, and **multi-factor authentication** (Abs. 2a).

##### Who is affected?

All providers of telecommunications services, with stricter duties for operators of public networks and providers of publicly available services.

##### What could this mean in practice?

Possible implementation, not a legal requirement: AI components used in network operation, such as anomaly detection or automated network management, become part of the systems whose security, supply chain and access control must meet these requirements.

#### § 166 — Security Officer and Security Concept

Requires operators of public networks and providers of publicly available services to appoint a **security officer**, name a contact person in the EU and draw up a **security concept** describing threats and measures; network operators must submit it to the Bundesnetzagentur, which reviews implementation **at least every two years**.

#### § 167 — Catalogue of Security Requirements

Has the Bundesnetzagentur, in agreement with the **BSI** and the Federal Commissioner for Data Protection, set out the details of the § 165 measures in a catalogue, including which functions are **critical functions** realised by critical components and which providers have an increased risk potential; obligations apply at the latest one year after the catalogue takes effect.

#### § 168 — Reporting of Security Incidents

Requires operators and providers to report significant security incidents to the Bundesnetzagentur and the BSI: an **early warning within 24 hours**, an incident notification within **72 hours** with an initial assessment, interim reports on request and a **final report within one month**.

#### § 169 — Data and Information Security

Requires providers of publicly available services to notify the Bundesnetzagentur and the Federal Commissioner for Data Protection of a **personal data breach** without delay, and the persons concerned if they are likely to be seriously affected, unless the data were securely encrypted; providers must keep a register of breaches.

#### § 170 — Implementation of Surveillance Measures, Provision of Information

Requires operators of systems used for publicly available services to keep, at their own cost from the start of operation, **technical facilities for legally ordered telecommunications surveillance**, to notify the Bundesnetzagentur and to prove conformity with the surveillance ordinance and technical guideline.

#### § 171 — Cooperation in Technical Investigative Measures for Mobile Devices

Requires mobile network operators to allow authorised authorities to use technical means to determine a device's **location, device number and identifiers** without the end user noticing, and to provide automated information on identifiers.

#### § 172 — Data for Information Requests of Security Authorities

Requires providers that assign phone numbers or other connection identifiers to **collect and store** numbers, name, address, date of birth and other listed data **before activation**, even if not needed for business purposes, and to verify identity data for prepaid mobile services.

#### § 173 — Automated Information Procedure

Requires providers that assign numbers to keep customer files that the Bundesnetzagentur can query **automatically** on behalf of authorised authorities.

#### § 174 — Manual Information Procedure

Allows and governs the disclosure of subscriber data to authorised authorities on a written or electronic request citing a legal basis, including identification of the user behind an **IP address** at a given time, for which traffic data may be evaluated automatically.

#### § 175 — Obliged Parties; Compensation

Defines who must retain traffic data under §§ 176–181: providers of publicly available telecommunications services for end users, except **number-independent interpersonal services**; provides compensation for unreasonable hardship.

#### § 176 — Obligations to Retain Traffic Data

Obliges these providers to store traffic data in Germany for **ten weeks** and location data for **four weeks**, for example numbers, times and, for mobile and internet telephony, identifiers and IP addresses. The CJEU held that EU law precludes national rules providing for the general and indiscriminate preventive retention of traffic and location data, while allowing targeted retention, general retention of IP addresses for a period limited to what is strictly necessary and retention of identity data (CJEU, C-793/19 and C-794/19, which concerned the identical rules of the previous TKG).

#### § 177 — Use of the Data

Restricts the use of retained data to transfers to law enforcement for **particularly serious crimes**, to Länder police authorities to avert concrete dangers to life, limb or freedom or to the state, and to IP address information under § 174.

#### § 178 — Ensuring Data Security

Requires state-of-the-art protection of retained data, including **particularly secure encryption**, separate storage systems decoupled from the internet, restricted access and a **four-eyes principle**.

#### § 179 — Logging

Requires every access to retained data to be logged for data protection control, with logs deleted after one year.

#### § 180 — Catalogue of Requirements

Presumes a particularly high standard of data security and quality if the catalogue drawn up by the Bundesnetzagentur with the BSI and the Federal Commissioner for Data Protection is met.

#### § 181 — Security Concept

Requires the systems used for retention, their threats and measures to be included in the security concept under § 166.

#### § 182 — Information Requests of the Federal Intelligence Service

Requires network operators to inform the Federal Ministry for Digital Affairs on request about the **structure of their networks**, if requested by the Federal Intelligence Service for specified tasks; individual communications and subscriber data are excluded.

#### § 183 — Control and Enforcement of Obligations

Empowers the Bundesnetzagentur to issue orders, request information and inspect business premises to enforce Part 10 Section 1.

### Part 11 — Bundesnetzagentur (selected sections)

#### § 191 — Tasks and Powers

Assigns the Bundesnetzagentur the tasks and powers under the TKG and under Article 5 of the Open Internet Regulation (EU) 2015/2120.

#### § 202 — Enforcement of Obligations

Requires the agency to ask an undertaking that breaches its obligations to comment and remedy within a deadline, and allows it to order the necessary measures if the undertaking does not comply.

#### § 203 — Requests for Information and Further Investigative Rights

Obliges network operators and service providers to provide the agency with the information it needs to enforce the Act, for example for systematic or case-by-case checks of obligations.

### Part 13 — Fines

#### § 228 — Administrative Fines

Lists administrative offences and sets fines up to **€1 million**, €500,000, €300,000, €100,000 or less depending on the offence; for companies with total turnover above €50 million or €100 million, certain offences can be fined up to **2%** or **1%** of worldwide turnover. The Bundesnetzagentur is the administrative authority.

### Timeline

| Date | Event |
| --- | --- |
| 23 June 2021 | Enactment as Article 1 of the Telecommunications Modernisation Act |
| 1 December 2021 | Entry into force, replacing the TKG of 2004 |
| 20 September 2022 | CJEU judgment on the German traffic data retention rules (C-793/19, C-794/19) |
| 6 October 2026 | Most recent amendment in the consolidated text |

### Enforcement and penalties

The Bundesnetzagentur enforces the Act, can demand information, issue orders and inspect premises (§§ 183, 202, 203 TKG). Security incidents go to the Bundesnetzagentur and the BSI, personal data breaches to the Bundesnetzagentur and the Federal Commissioner for Data Protection (§§ 168, 169 TKG). Fines reach €1 million, or 1–2% of worldwide turnover for large companies in specified cases (§ 228 TKG).

### Relationship to other acts

- **[[eecc|European Electronic Communications Code]]:** the TKG transposes most of it in Germany ([[eecc|EECC]]).
- **[[tdddg|TDDDG]]:** contains the secrecy of telecommunications and data protection in telecommunications and digital services, previously part of the TKG.
- **[[bsig|BSI Act]]:** telecommunications providers can be particularly important or important entities; § 165 Abs. 2a TKG applies the [[nis2-directive|NIS2]] all-hazards measures to them.
- **[[kritis-dachgesetz|KRITIS-Dachgesetz]]:** the Bundesnetzagentur is the competent authority for public telecommunications as a critical service, and incidents that are solely security incidents under the TKG are excluded from KRITIS reporting.
- **[[eprivacy-directive|ePrivacy Directive]]:** Article 15(1) governs national retention of traffic data, as interpreted by the CJEU (CJEU, C-793/19).

### Relevance for AI development

- **Security of AI in network operations:** AI used to operate public networks and services falls under the security, supply-chain and access-control duties of § 165 and the security concept of § 166 TKG ([[mlops-and-deployment|MLOps and deployment]]).
- **Incident reporting:** failures or compromises of AI-based network components can be significant security incidents with 24-hour and 72-hour reporting deadlines (§ 168 TKG; [[monitoring-and-alerting|monitoring and alerting]]).
- **Traffic and subscriber data:** the strict purpose limitation of retained data (§ 177 TKG) and the rules on subscriber data mean that such data cannot simply be reused, for example to train models; telecommunications data protection is governed by the [[tdddg|TDDDG]] and the [[gdpr|GDPR]].
- **Voice and chat services:** providers of interpersonal telecommunications services, including some voice agents, must consider emergency call obligations if their service is number-based (§ 164 TKG; [[voice-agents|voice agents]]).

### Official sources

- Telekommunikationsgesetz (TKG) vom 23. Juni 2021, BGBl. I 2021, 1858, consolidated version. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/tkg_2021/)
- CJEU, judgment of 20 September 2022, joined cases C-793/19 and C-794/19 (SpaceNet and Telekom Deutschland). [EUR-Lex](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62019CJ0793)

## DE

> **Wichtiger Hinweis:** Diese Seite ist eine LLM-generierte Zusammenfassung. Sie kann unvollständig, veraltet oder falsch sein. Sie ist keine Rechtsberatung und hat keine Rechtswirkung; verbindlich ist nur der im Bundesgesetzblatt veröffentlichte Text.

### TL;DR

Das Telekommunikationsgesetz (TKG) regelt die Telekommunikation in Deutschland: Es soll durch technologieneutrale Regulierung den Wettbewerb und leistungsfähige Infrastrukturen fördern und flächendeckend angemessene Dienstleistungen gewährleisten, und es gilt für alle, die in Deutschland Telekommunikationsnetze oder -anlagen betreiben oder Telekommunikationsdienste erbringen (§ 1 TKG). Seine rund 230 Paragrafen behandeln Markt- und Zugangsregulierung, Kundenschutz, Frequenzen, Nummerierung, Wegerechte, das Recht auf Versorgung, öffentliche Sicherheit und die [[federal-network-agency|Bundesnetzagentur]]. Diese Notiz behandelt nur die für Daten, Sicherheit und KI wichtigsten Teile: Zweck und Begriffsbestimmungen (Teil 1), öffentliche Sicherheit (Teil 10 Abschnitt 1) mit Schutzmaßnahmen, Meldung von Sicherheitsvorfällen, Telekommunikationsüberwachung, Auskunftsverfahren und Speicherung von Verkehrsdaten sowie die Durchsetzungsbefugnisse und Bußgelder. Fernmeldegeheimnis und Datenschutz in der Telekommunikation stehen nicht mehr im TKG, sondern im [[tdddg|TDDDG]].

### Eckdaten

| | |
|---|---|
| Fundstelle | Telekommunikationsgesetz vom 23. Juni 2021, BGBl. I 2021, 1858 (Artikel 1 des Telekommunikationsmodernisierungsgesetzes) |
| Art / Geltungsbereich | Bundesgesetz, Deutschland |
| In Kraft | 1. Dezember 2021 |
| Zuständige Behörde | Bundesnetzagentur (§ 191 TKG), bei Sicherheits- und Datenfragen mit dem [[bsi\|BSI]] und der oder dem Bundesbeauftragten für den Datenschutz (§§ 167, 168, 169 TKG) |
| Zusammengefasste Fassung | konsolidierter Text, zuletzt geändert am 6. Oktober 2026 |
| Umfang dieser Notiz | Teil 1 (§§ 1–3), Teil 10 Abschnitt 1 (§§ 164–183), §§ 191, 202, 203, 228 |

### Anwendungsbereich

Das TKG gilt für alle Unternehmen und Personen, die im Geltungsbereich des Gesetzes Telekommunikationsnetze oder -anlagen betreiben oder Telekommunikationsdienste erbringen, sowie für weitere nach dem Gesetz Berechtigte und Verpflichtete (§ 1 Abs. 2 TKG). Telekommunikationsdienste sind in der Regel gegen Entgelt über Telekommunikationsnetze erbrachte Dienste, nämlich Internetzugangsdienste, interpersonelle Telekommunikationsdienste und Dienste, die ganz oder überwiegend in der Übertragung von Signalen bestehen, mit Ausnahme von Diensten, die Inhalte anbieten oder eine redaktionelle Kontrolle über sie ausüben (§ 3 Nr. 61 TKG).

**Hier behandelt:** allgemeine Vorschriften (§§ 1–3), öffentliche Sicherheit (§§ 164–183), allgemeine Aufgabe, Durchsetzungs- und Auskunftsbefugnisse der Bundesnetzagentur (§§ 191, 202, 203) und Bußgelder (§ 228). **Nicht behandelt:** Marktregulierung (Teil 2), Kundenschutz (Teil 3), Telekommunikationsendeinrichtungen (Teil 4), Informationen über Infrastruktur (Teil 5), Frequenzordnung (Teil 6), Nummerierung (Teil 7), Wegerechte (Teil 8), Recht auf Versorgung (Teil 9), Notfallvorsorge (Teil 10 Abschnitt 2), übrige Organisations- und Verfahrensvorschriften von Teil 11, Abgaben (Teil 12) sowie Übergangsvorschriften (Teil 14).

### Teil 1 — Allgemeine Vorschriften

#### § 1 — Zweck des Gesetzes, Anwendungsbereich

Soll durch **technologieneutrale Regulierung** den Wettbewerb in der Telekommunikation und leistungsfähige Infrastrukturen fördern und flächendeckend angemessene und ausreichende Dienstleistungen gewährleisten; die Verlegung von Telekommunikationslinien für öffentliche Netze liegt **bis zum 31. Dezember 2030 im überragenden öffentlichen Interesse**. Gilt für alle, die in Deutschland Netze oder Anlagen betreiben oder Telekommunikationsdienste erbringen.

#### § 2 — Ziele und Grundsätze der Regulierung

Macht die Regulierung der Telekommunikation zur hoheitlichen Aufgabe des Bundes und nennt ihre Ziele: Konnektivität und Zugang zu Netzen mit sehr hoher Kapazität, chancengleichen Wettbewerb, Nutzer- und Verbraucherinteressen einschließlich der **öffentlichen Sicherheit und der Sicherheit der Netze und Dienste**, den Binnenmarkt der Union sowie die effiziente und störungsfreie Nutzung von Frequenzen.

#### § 3 — Begriffsbestimmungen

Bestimmt über 70 Begriffe. Für Daten und Sicherheit wichtig: **Bestandsdaten**, also Daten, die für Begründung, Ausgestaltung, Änderung oder Beendigung eines Vertrags erforderlich sind (Nr. 6); **Endnutzer** (Nr. 13); **interpersoneller Telekommunikationsdienst** (Nr. 24); **Sicherheit von Netzen und Diensten**, die Fähigkeit, Angriffe auf Verfügbarkeit, Authentizität, Integrität oder Vertraulichkeit abzuwehren (Nr. 52); **Sicherheitsvorfall** (Nr. 53); **Telekommunikationsdienste** (Nr. 61); **Verkehrsdaten**, also Daten, deren Erhebung, Verarbeitung oder Nutzung bei der Erbringung eines Telekommunikationsdienstes erforderlich sind (Nr. 70); und **Verletzung des Schutzes personenbezogener Daten** (Nr. 71).

### Teil 10 — Öffentliche Sicherheit und Notfallvorsorge (Abschnitt 1: Öffentliche Sicherheit)

#### § 164 — Notruf

Verpflichtet Anbieter nummerngebundener interpersoneller Dienste, **unentgeltliche Notrufverbindungen zu 112 und 110** zu ermöglichen, die unverzüglich zur zuständigen Notrufabfragestelle hergestellt werden, mit Rufnummer und den Daten zur Standortermittlung; Notrufverbindungen haben Vorrang.

#### § 164a — Öffentliche Warnungen

Verpflichtet Betreiber öffentlicher Mobilfunknetze, technische Einrichtungen für Warnungen vor größeren Notfällen und Katastrophen vorzuhalten, die über das zentrale Warnsystem des Bundes ausgelöst und an alle Mobilfunkendgeräte im von der Behörde bestimmten Gebiet gesendet werden.

#### § 165 — Technische und organisatorische Schutzmaßnahmen

##### Worum geht es?

Die zentrale Sicherheitspflicht der Telekommunikationsanbieter.

##### Was verlangt die Vorschrift?

Wer Telekommunikationsdienste erbringt oder daran mitwirkt, hat angemessene technische Vorkehrungen zum Schutz des **Fernmeldegeheimnisses** und gegen die **Verletzung des Schutzes personenbezogener Daten** zu treffen, unter Berücksichtigung des Stands der Technik (Abs. 1). Betreiber öffentlicher Netze und Anbieter öffentlich zugänglicher Dienste müssen ihre Telekommunikations- und Datenverarbeitungssysteme gegen Störungen schützen, auch durch äußere Angriffe und Katastrophen, und die Risiken für die Sicherheit der Netze und Dienste beherrschen, insbesondere mit Maßnahmen wie **Verschlüsselung** gegen unerlaubte Zugriffe; das Sicherheitsniveau muss dem Risiko angemessen sein, unter Berücksichtigung von Stand der Technik, Normen, Kosten, Risikoexposition, Größe, Eintrittswahrscheinlichkeit und Schwere von Sicherheitsvorfällen (Abs. 2). Anbieter, die besonders wichtige oder wichtige Einrichtungen nach dem BSI-Gesetz sind, müssen einem gefahrenübergreifenden Ansatz folgen, der mindestens Risikoanalyse, Bewältigung von Sicherheitsvorfällen, Aufrechterhaltung des Betriebs, Sicherheit der Lieferkette, sichere Beschaffung und Entwicklung einschließlich Schwachstellenmanagement, Wirksamkeitsbewertung, Schulungen, Kryptografie, Personalsicherheit und Zugriffskontrolle sowie **Multi-Faktor-Authentifizierung** umfasst (Abs. 2a).

##### Wer ist betroffen?

Alle Anbieter von Telekommunikationsdiensten, mit strengeren Pflichten für Betreiber öffentlicher Netze und Anbieter öffentlich zugänglicher Dienste.

##### Was könnte das in der Praxis bedeuten?

Mögliche Umsetzung, keine gesetzliche Vorgabe: KI-Komponenten im Netzbetrieb, etwa Anomalieerkennung oder automatisiertes Netzmanagement, werden Teil der Systeme, deren Sicherheit, Lieferkette und Zugriffskontrolle diese Anforderungen erfüllen müssen.

#### § 166 — Sicherheitsbeauftragter und Sicherheitskonzept

Verpflichtet Betreiber öffentlicher Netze und Anbieter öffentlich zugänglicher Dienste, einen **Sicherheitsbeauftragten** zu bestimmen, einen in der EU ansässigen Ansprechpartner zu benennen und ein **Sicherheitskonzept** mit Gefährdungen und Maßnahmen zu erstellen; Netzbetreiber legen es der Bundesnetzagentur vor, die die Umsetzung **mindestens alle zwei Jahre** überprüfen soll.

#### § 167 — Katalog von Sicherheitsanforderungen

Lässt die Bundesnetzagentur im Einvernehmen mit dem **BSI** und der oder dem Bundesbeauftragten für den Datenschutz die Einzelheiten der Maßnahmen nach § 165 in einem Katalog festlegen, einschließlich der **kritischen Funktionen**, die von kritischen Komponenten realisiert werden, und der Anbieter mit erhöhtem Gefährdungspotenzial; die Vorgaben sind spätestens ein Jahr nach Inkrafttreten des Katalogs zu erfüllen.

#### § 168 — Meldung eines Sicherheitsvorfalls

Verpflichtet Betreiber und Anbieter, erhebliche Sicherheitsvorfälle an die Bundesnetzagentur und das BSI zu melden: eine **frühe Erstmeldung binnen 24 Stunden**, eine Meldung **binnen 72 Stunden** mit erster Bewertung, Zwischenmeldungen auf Ersuchen und eine **Abschlussmeldung binnen eines Monats**.

#### § 169 — Daten- und Informationssicherheit

Verpflichtet Anbieter öffentlich zugänglicher Dienste, eine **Verletzung des Schutzes personenbezogener Daten** unverzüglich der Bundesnetzagentur und der oder dem Bundesbeauftragten für den Datenschutz zu melden und die Betroffenen zu benachrichtigen, wenn sie voraussichtlich schwerwiegend beeinträchtigt werden, außer die Daten waren sicher verschlüsselt; zudem ist ein Verzeichnis der Verletzungen zu führen.

#### § 170 — Umsetzung von Überwachungsmaßnahmen, Erteilung von Auskünften

Verpflichtet Betreiber von Anlagen für öffentlich zugängliche Dienste, ab Betriebsaufnahme auf eigene Kosten **technische Einrichtungen zur Umsetzung gesetzlich vorgesehener Telekommunikationsüberwachung** vorzuhalten, dies der Bundesnetzagentur mitzuteilen und die Übereinstimmung mit Rechtsverordnung und Technischer Richtlinie nachzuweisen.

#### § 171 — Mitwirkung bei technischen Ermittlungsmaßnahmen bei Mobilfunkendgeräten

Verpflichtet Mobilfunknetzbetreiber, berechtigten Stellen den Einsatz technischer Mittel zur Ermittlung von **Standort, Gerätenummer und Kennungen** von Mobilfunkendgeräten zu ermöglichen, ohne dass dies dem Endnutzer bekannt wird, und automatisierte Auskunft über Kennungen zu erteilen.

#### § 172 — Daten für Auskunftsersuchen der Sicherheitsbehörden

Verpflichtet Anbieter, die Rufnummern oder andere Anschlusskennungen vergeben, Rufnummern, Name, Anschrift, Geburtsdatum und weitere genannte Daten **vor der Freischaltung zu erheben und zu speichern**, auch wenn sie betrieblich nicht erforderlich sind, und bei vorausbezahlten Mobilfunkdiensten die Identitätsdaten zu überprüfen.

#### § 173 — Automatisiertes Auskunftsverfahren

Verpflichtet Anbieter, die Rufnummern vergeben, Kundendateien zu führen, die die Bundesnetzagentur für berechtigte Stellen **automatisiert** abrufen kann.

#### § 174 — Manuelles Auskunftsverfahren

Erlaubt und regelt die Auskunft über Bestandsdaten an berechtigte Stellen auf schriftliches oder elektronisches Verlangen unter Angabe einer gesetzlichen Grundlage, einschließlich der Zuordnung einer zu einem Zeitpunkt zugewiesenen **IP-Adresse**, wofür Verkehrsdaten automatisiert ausgewertet werden dürfen.

#### § 175 — Verpflichtete; Entschädigung

Bestimmt, wer Verkehrsdaten nach §§ 176–181 speichern muss: Anbieter öffentlich zugänglicher Telekommunikationsdienste für Endnutzer, ausgenommen **nummernunabhängige interpersonelle Dienste**; sieht eine Entschädigung bei unbilligen Härten vor.

#### § 176 — Pflichten zur Speicherung von Verkehrsdaten

Verpflichtet diese Anbieter, Verkehrsdaten im Inland **zehn Wochen** und Standortdaten **vier Wochen** zu speichern, etwa Rufnummern, Zeitpunkte und bei Mobil- und Internettelefonie Kennungen und IP-Adressen. Der EuGH entschied, dass das Unionsrecht nationalen Vorschriften entgegensteht, die präventiv eine allgemeine und unterschiedslose Vorratsspeicherung von Verkehrs- und Standortdaten vorsehen, während eine gezielte Speicherung, eine auf das absolut Notwendige befristete allgemeine Speicherung der IP-Adressen und die Speicherung von Identitätsdaten zulässig sein können (EuGH, C-793/19 und C-794/19, zu den inhaltsgleichen Regeln des früheren TKG).

#### § 177 — Verwendung der Daten

Beschränkt die Verwendung gespeicherter Daten auf die Übermittlung an Strafverfolgungsbehörden zur Verfolgung **besonders schwerer Straftaten**, an Gefahrenabwehrbehörden der Länder zur Abwehr konkreter Gefahren für Leib, Leben oder Freiheit oder für den Bestand des Staates sowie auf Auskünfte zu IP-Adressen nach § 174.

#### § 178 — Gewährleistung der Sicherheit der Daten

Verlangt Schutz gespeicherter Daten nach dem Stand der Technik, unter anderem durch **besonders sichere Verschlüsselung**, getrennte, vom Internet entkoppelte Speichersysteme, beschränkten Zutritt und das **Vier-Augen-Prinzip**.

#### § 179 — Protokollierung

Verlangt, jeden Zugriff auf gespeicherte Daten zur Datenschutzkontrolle zu protokollieren und die Protokolle nach einem Jahr zu löschen.

#### § 180 — Anforderungskatalog

Vermutet einen besonders hohen Standard der Datensicherheit und -qualität, wenn der Katalog der Bundesnetzagentur, erstellt mit BSI und der oder dem Bundesbeauftragten für den Datenschutz, eingehalten wird.

#### § 181 — Sicherheitskonzept

Verlangt, Systeme, Gefährdungen und Maßnahmen der Speicherung in das Sicherheitskonzept nach § 166 aufzunehmen.

#### § 182 — Auskunftsersuchen des Bundesnachrichtendienstes

Verpflichtet Netzbetreiber, dem Bundesministerium für Digitales und Staatsmodernisierung auf Anfrage über die **Strukturen ihrer Netze** Auskunft zu geben, wenn ein Ersuchen des Bundesnachrichtendienstes für bestimmte Aufgaben vorliegt; einzelne Telekommunikationsvorgänge und Bestandsdaten sind ausgeschlossen.

#### § 183 — Kontrolle und Durchsetzung von Verpflichtungen

Ermächtigt die Bundesnetzagentur, Anordnungen zu treffen, Auskünfte zu verlangen und Geschäftsräume zu besichtigen, um Teil 10 Abschnitt 1 durchzusetzen.

### Teil 11 — Bundesnetzagentur (ausgewählte Vorschriften)

#### § 191 — Aufgaben und Befugnisse

Weist der Bundesnetzagentur die Aufgaben und Befugnisse nach dem TKG und nach Artikel 5 der Verordnung (EU) 2015/2120 über den Zugang zum offenen Internet zu.

#### § 202 — Durchsetzung von Verpflichtungen

Verlangt, dass die Behörde ein Unternehmen, das seine Pflichten nicht erfüllt, zur Stellungnahme und Abhilfe binnen einer Frist auffordert, und erlaubt ihr, die erforderlichen Maßnahmen anzuordnen, wenn das Unternehmen nicht abhilft.

#### § 203 — Auskunftsverlangen und weitere Untersuchungsrechte; Übermittlungspflichten

Verpflichtet Netzbetreiber und Diensteanbieter, der Behörde die für den Vollzug des Gesetzes erforderlichen Informationen bereitzustellen, etwa für systematische oder einzelfallbezogene Überprüfungen von Pflichten.

### Teil 13 — Bußgeldvorschriften

#### § 228 — Bußgeldvorschriften

Nennt Ordnungswidrigkeiten und Geldbußen bis zu **einer Million Euro**, 500 000 Euro, 300 000 Euro, 100 000 Euro oder weniger je nach Verstoß; gegenüber Unternehmen mit einem Gesamtumsatz von mehr als 50 Mio. Euro oder 100 Mio. Euro können bestimmte Verstöße mit bis zu **2 %** bzw. **1 %** des weltweiten Gesamtumsatzes geahndet werden. Verwaltungsbehörde ist die Bundesnetzagentur.

### Zeitplan

| Datum | Ereignis |
| --- | --- |
| 23. Juni 2021 | Ausfertigung als Artikel 1 des Telekommunikationsmodernisierungsgesetzes |
| 1. Dezember 2021 | Inkrafttreten, Ablösung des TKG von 2004 |
| 20. September 2022 | EuGH-Urteil zu den deutschen Regeln zur Speicherung von Verkehrsdaten (C-793/19, C-794/19) |
| 6. Oktober 2026 | Letzte Änderung im konsolidierten Text |

### Durchsetzung und Sanktionen

Die Bundesnetzagentur setzt das Gesetz durch, kann Auskünfte verlangen, Anordnungen treffen und Geschäftsräume besichtigen (§§ 183, 202, 203 TKG). Sicherheitsvorfälle gehen an Bundesnetzagentur und BSI, Verletzungen des Schutzes personenbezogener Daten an Bundesnetzagentur und die oder den Bundesbeauftragten für den Datenschutz (§§ 168, 169 TKG). Geldbußen reichen bis zu einer Million Euro, bei großen Unternehmen in bestimmten Fällen bis zu 1–2 % des weltweiten Umsatzes (§ 228 TKG).

### Verhältnis zu anderen Rechtsakten

- **[[eecc|Europäischer Kodex für die elektronische Kommunikation]]:** Das TKG setzt den größten Teil davon in Deutschland um ([[eecc|EECC]]).
- **[[tdddg|TDDDG]]:** enthält das Fernmeldegeheimnis und den Datenschutz bei Telekommunikation und digitalen Diensten, die früher Teil des TKG waren.
- **[[bsig|BSI-Gesetz]]:** Telekommunikationsanbieter können besonders wichtige oder wichtige Einrichtungen sein; § 165 Abs. 2a TKG überträgt die gefahrenübergreifenden Maßnahmen nach [[nis2-directive|NIS 2]] auf sie.
- **[[kritis-dachgesetz|KRITIS-Dachgesetz]]:** Die Bundesnetzagentur ist zuständige Behörde für öffentliche Telekommunikation als kritische Dienstleistung, und Ereignisse, die ausschließlich Sicherheitsvorfälle nach dem TKG sind, sind vom KRITIS-Meldewesen ausgenommen.
- **[[eprivacy-directive|ePrivacy-Richtlinie]]:** Artikel 15 Absatz 1 bestimmt den Rahmen für nationale Speicherung von Verkehrsdaten, wie ihn der EuGH auslegt (EuGH, C-793/19).

### Bedeutung für die KI-Entwicklung

- **Sicherheit von KI im Netzbetrieb:** KI, die beim Betrieb öffentlicher Netze und Dienste eingesetzt wird, fällt unter die Pflichten zu Sicherheit, Lieferkette und Zugriffskontrolle nach § 165 und das Sicherheitskonzept nach § 166 TKG ([[mlops-and-deployment|MLOps und Deployment]]).
- **Meldepflichten:** Ausfälle oder Kompromittierungen KI-gestützter Netzkomponenten können erhebliche Sicherheitsvorfälle mit Meldefristen von 24 und 72 Stunden sein (§ 168 TKG; [[monitoring-and-alerting|Monitoring und Alerting]]).
- **Verkehrs- und Bestandsdaten:** Die strenge Zweckbindung gespeicherter Daten (§ 177 TKG) und die Regeln zu Bestandsdaten bedeuten, dass solche Daten nicht ohne Weiteres weiterverwendet werden dürfen, etwa zum Training von Modellen; der Datenschutz in der Telekommunikation richtet sich nach dem [[tdddg|TDDDG]] und der [[gdpr|DSGVO]].
- **Sprach- und Chatdienste:** Anbieter interpersoneller Telekommunikationsdienste, darunter manche Voice Agents, müssen Notrufpflichten beachten, wenn ihr Dienst nummerngebunden ist (§ 164 TKG; [[voice-agents|Voice Agents]]).

### Amtliche Quellen

- Telekommunikationsgesetz (TKG) vom 23. Juni 2021, BGBl. I 2021, 1858, konsolidierte Fassung. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/tkg_2021/)
- EuGH, Urteil vom 20. September 2022, verbundene Rechtssachen C-793/19 und C-794/19 (SpaceNet und Telekom Deutschland). [EUR-Lex](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62019CJ0793)
