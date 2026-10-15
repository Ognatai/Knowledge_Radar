---
title_en: Critical Facility (KRITIS)
title_de: Kritische Anlage (KRITIS)
entity_type: Concept
aliases:
- Critical facility
- Kritische Anlage
- Kritische Anlagen
- Operator of critical facilities
- Betreiber kritischer Anlagen
sources:
- https://www.gesetze-im-internet.de/kritisdachg/
- https://www.gesetze-im-internet.de/bsig_2025/
- https://www.gesetze-im-internet.de/bsi-kritisv/
- https://eur-lex.europa.eu/eli/dir/2022/2557/oj/deu
---

## EN

> **Important notice:** LLM-generated summary; may be incomplete, outdated or wrong. Not legal advice; only the official German texts are authentic. The English version is a summary of the German text.

### TL;DR

In German law, a critical facility (*kritische Anlage*) is a facility that is significant for providing a critical service (*kritische Dienstleistung*), that is, a service supplying the general public in sectors such as energy, transport, finance, health, water, food, IT and telecommunications, space or municipal waste disposal, whose failure would lead to significant supply shortages or threats to public safety (§ 2 Nr. 3–4 KRITISDachG). A "facility" covers sites, fixed and mobile installations, machines, devices, and also software and IT services (§ 2 Nr. 2 KRITISDachG). Whether a facility is critical is determined by thresholds of supply coverage set by ordinance, with a standard value of **500,000 inhabitants** supplied (§ 5 Abs. 2 KRITISDachG). Operators of critical facilities must register, carry out risk analyses and resilience measures under the [[kritis-dachgesetz|KRITIS-Dachgesetz]], and are automatically "particularly important entities" with stricter IT security duties under the [[bsig|BSI Act]], such as attack detection systems and audits every three years (§ 28, § 31, § 39 BSIG).

### How it works

```text
critical service (sector, e.g. electricity supply)          § 2 Nr. 4, § 4 KRITISDachG
   └─ facility category + threshold of supply coverage       ordinance under § 4(3), § 5(1) KRITISDachG
        (standard: 500,000 inhabitants supplied)              (until then: BSI-KritisV annexes)
   └─ facility reaches threshold → critical facility          § 2 Nr. 3 KRITISDachG
        or case-by-case decision by the Federal Interior Ministry  § 5(3)
operator → register with BBK within 3 months                 § 8 KRITISDachG
         → physical resilience: risk analysis, resilience plan, incident reporting   §§ 12, 13, 18
         → IT security as "particularly important entity": risk management, attack detection,
           proof every 3 years, possible ban of critical components                  §§ 28, 31, 39, 41 BSIG
```

#### 1. Critical service and critical facility

The KRITIS-Dachgesetz defines a critical service as a service supplying the general public in the sectors energy, transport, finance, social insurance and basic income support for job seekers, health, water, food, information technology and telecommunications, space, and municipal waste disposal, whose failure or impairment would lead to significant supply shortages or threats to public safety (§ 2 Nr. 4, § 4 Abs. 1 KRITISDachG). A critical facility is a facility that is significant for providing such a service (§ 2 Nr. 3 KRITISDachG). The operator is whoever exercises decisive influence over the facility, taking legal, economic and actual circumstances into account; in the finance sector, whoever has actual physical control (§ 2 Nr. 1 KRITISDachG).

#### 2. Software and IT services count as facilities

"Facility" is defined broadly: a site, other fixed installation, machine, device, other mobile technical installation, or software and IT services (§ 2 Nr. 2 KRITISDachG). For software and IT services that do not directly control, monitor or support physical processes of the critical service, only the requirements of the BSI Act apply (§ 2 Nr. 2 KRITISDachG). The earlier BSI-KritisV similarly counted software and IT services needed to provide a critical service as facilities (§ 1 Abs. 1 Nr. 1 BSI-KritisV).

#### 3. Thresholds of supply coverage

The [[federal-ministry-of-the-interior|Federal Ministry of the Interior]] determines by ordinance the critical services per sector, categories of facilities and threshold values of supply coverage above which a facility counts as significant (§ 4 Abs. 3, § 5 Abs. 1 KRITISDachG). The thresholds take into account national risk analyses and criteria such as the number of inhabitants supplied, dependencies of other sectors, the impact of failures, market share, the affected geographic area and the availability of alternatives; the standard threshold is **500,000** inhabitants supplied by one facility (§ 5 Abs. 2 KRITISDachG). The ministry can also declare a facility critical, or not critical, in an individual case (§ 5 Abs. 3 KRITISDachG). Until the new ordinance applies, the facility categories and thresholds of the BSI-KritisV continue to determine which facilities are critical (§ 66 BSIG; § 2 Abs. 6 BSI-KritisV for the energy sector).

#### 4. Duties of operators

Operators must register their critical facilities with the [[bbk|Federal Office of Civil Protection and Disaster Assistance (BBK)]], via a registration channel set up jointly with the [[bsi|BSI]], no later than three months after a facility counts as critical; the data include the sector, the critical service, values of supply coverage, location, public IP address ranges and the types of critical components used (§ 8 Abs. 1 KRITISDachG). Risk analysis and assessment apply nine months after registration, and the resilience duties, incident reporting and management responsibilities ten months after registration (§ 8 Abs. 7 KRITISDachG). Under the BSI Act, operators of critical facilities are particularly important entities (§ 28 Abs. 1 Nr. 1 BSIG); for the IT systems that are decisive for their critical facilities, measures beyond the usual level are proportionate, attack detection systems are mandatory, and implementation must be proven to the BSI through audits, tests or certifications every three years (§§ 31, 39 BSIG). The Federal Ministry of the Interior can prohibit the use of critical components of a manufacturer if their use is likely to impair public order or security (§ 41 BSIG).

#### Origin and variants

The concept replaces the earlier notion of "critical infrastructures" (*Kritische Infrastrukturen*) in the BSI Act of 2009; § 39 Abs. 3 BSIG refers to operators who were operators of critical infrastructures under the old BSI Act. The KRITIS-Dachgesetz transposes the EU [[cer-directive|CER Directive]] on the resilience of critical entities for physical protection, while the BSI Act in its 2025 version implements the [[nis2-directive|NIS2 Directive]] for cyber security; the registration data refer to essential services under Article 2 of Directive (EU) 2022/2557 (§ 8 Abs. 1 Nr. 6 KRITISDachG). The finance sector is largely governed by [[dora|DORA]]: many duties of the KRITIS-Dachgesetz do not apply to financial entities under Regulation (EU) 2022/2554 (§ 4 Abs. 2 KRITISDachG).

### When to use it

- Checking whether an organisation or one of its systems falls under KRITIS duties: identify the critical service, the facility category and its supply coverage (§§ 4, 5 KRITISDachG; [[bsi-kritisv|BSI-KritisV]]).
- Planning AI or software systems that control, monitor or support physical processes of critical services, since such software can itself be part of a critical facility (§ 2 Nr. 2 KRITISDachG).
- Preparing audits, attack detection and incident reporting for IT systems of critical facilities (§§ 31, 39 BSIG).

### Strengths and limitations

**Strengths**
- Threshold-based criteria make the classification largely objective and checkable (§ 5 KRITISDachG).
- One concept links physical resilience (KRITISDachG) and IT security (BSIG).
- Case-by-case decisions can capture facilities that thresholds miss (§ 5 Abs. 3 KRITISDachG).

**Limitations**
- The decisive ordinance with the new thresholds is required before the new definitions apply; until then the BSI-KritisV continues (§ 66 BSIG).
- Several duties do not apply to the finance, IT and telecommunications, waste and social insurance sectors, which are governed by other rules (§ 4 Abs. 2 KRITISDachG).
- The split between software that supports physical processes (KRITISDachG) and other software (BSIG only) needs careful assessment (§ 2 Nr. 2 KRITISDachG).

### Comparison

| | Critical facility (KRITISDachG / BSIG) | Particularly important entity (BSIG) | Critical entity (CER Directive) |
|---|---|---|---|
| Basis | significance for a critical service, thresholds | size and sector, or operator of a critical facility | identified by Member States by 17 July 2026 (Art. 6) |
| Unit | facility (site, device, software, IT service) | organisation | organisation |
| Main duties | registration, resilience, attack detection, audits | risk management, reporting, registration | resilience measures |

Sources: § 2, § 5, § 8 KRITISDachG; § 28, § 31, § 39 BSIG; Art. 6 Directive (EU) 2022/2557.

### In practice

Operators first map their critical services and facilities against the ordinance's categories and thresholds and register within three months (§ 8 KRITISDachG). For AI components in operational technology, for example forecasting or control software for grids or water supply, the question is whether they directly control, monitor or support the physical process; then both resilience and BSI duties can apply (§ 2 Nr. 2 KRITISDachG; [[it-governance-frameworks|IT governance frameworks]]). Attack detection must continuously and automatically record and evaluate operational parameters and follow the state of the art (§ 31 Abs. 2 BSIG).

### Regulatory context

The concept connects the [[kritis-dachgesetz|KRITIS-Dachgesetz]] (physical resilience, transposing the [[cer-directive|CER Directive]]), the [[bsig|BSI Act]] (cyber security, implementing [[nis2-directive|NIS2]]) and, during the transition, the [[bsi-kritisv|BSI-KritisV]]. Financial entities follow [[dora|DORA]] for digital operational resilience.

### Key takeaway

A critical facility is any site, device, software or IT service that is significant for a critical service to the public, usually because it supplies around 500,000 people or more; its operator must register, build resilience and meet heightened IT security duties.

### Sources

- Dachgesetz zur Stärkung der physischen Resilienz kritischer Anlagen (KRITIS-Dachgesetz – KRITISDachG), §§ 2, 4, 5, 8. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kritisdachg/)
- Gesetz über das Bundesamt für Sicherheit in der Informationstechnik und über die Sicherheit in der Informationstechnik von Einrichtungen (BSI-Gesetz – BSIG), §§ 28, 31, 39, 41, 66. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bsig_2025/)
- Verordnung zur Bestimmung kritischer Anlagen nach dem BSI-Gesetz (BSI-Kritisverordnung – BSI-KritisV), §§ 1–2. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bsi-kritisv/)
- Directive (EU) 2022/2557 on the resilience of critical entities (CER Directive), Art. 6. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2557/oj/deu)

## DE

> **Wichtiger Hinweis:** LLM-generierte Zusammenfassung; kann unvollständig, veraltet oder falsch sein. Keine Rechtsberatung; verbindlich sind nur die amtlichen Texte.

### TL;DR

Im deutschen Recht ist eine kritische Anlage eine Anlage, die für die Erbringung einer kritischen Dienstleistung erheblich ist, also einer Dienstleistung zur Versorgung der Allgemeinheit in Sektoren wie Energie, Transport und Verkehr, Finanzwesen, Gesundheitswesen, Wasser, Ernährung, Informationstechnik und Telekommunikation, Weltraum oder Siedlungsabfallentsorgung, deren Ausfall zu erheblichen Versorgungsengpässen oder zu Gefährdungen der öffentlichen Sicherheit führen würde (§ 2 Nr. 3–4 KRITISDachG). Als „Anlage“ gelten Betriebsstätten, ortsfeste und ortsveränderliche Installationen, Maschinen, Geräte sowie auch Software und IT-Dienste (§ 2 Nr. 2 KRITISDachG). Ob eine Anlage kritisch ist, bestimmen per Rechtsverordnung festgelegte Schwellenwerte zum Versorgungsgrad mit einem Regelwert von **500 000 versorgten Einwohnern** (§ 5 Abs. 2 KRITISDachG). Betreiber kritischer Anlagen müssen sich registrieren, Risikoanalysen und Resilienzmaßnahmen nach dem [[kritis-dachgesetz|KRITIS-Dachgesetz]] umsetzen und gelten nach dem [[bsig|BSI-Gesetz]] automatisch als besonders wichtige Einrichtungen mit strengeren Pflichten zur IT-Sicherheit, etwa Systemen zur Angriffserkennung und Nachweisen alle drei Jahre (§ 28, § 31, § 39 BSIG).

### Funktionsweise

```text
kritische Dienstleistung (Sektor, z. B. Stromversorgung)          § 2 Nr. 4, § 4 KRITISDachG
   └─ Anlagenkategorie + Schwellenwert zum Versorgungsgrad          Rechtsverordnung nach § 4 Abs. 3, § 5 Abs. 1 KRITISDachG
        (Regelwert: 500 000 versorgte Einwohner)                     (bis dahin: Anhänge der BSI-KritisV)
   └─ Anlage erreicht Schwellenwert → kritische Anlage              § 2 Nr. 3 KRITISDachG
        oder Feststellung im Einzelfall durch das Bundesinnenministerium   § 5 Abs. 3
Betreiber → Registrierung beim BBK binnen 3 Monaten                 § 8 KRITISDachG
          → physische Resilienz: Risikoanalyse, Resilienzplan, Meldewesen   §§ 12, 13, 18
          → IT-Sicherheit als „besonders wichtige Einrichtung“: Risikomanagement, Angriffserkennung,
            Nachweis alle 3 Jahre, mögliche Untersagung kritischer Komponenten   §§ 28, 31, 39, 41 BSIG
```

#### 1. Kritische Dienstleistung und kritische Anlage

Das KRITIS-Dachgesetz definiert eine kritische Dienstleistung als Dienstleistung zur Versorgung der Allgemeinheit in den Sektoren Energie, Transport und Verkehr, Finanzwesen, Leistungen der Sozialversicherung sowie Grundsicherung für Arbeitsuchende, Gesundheitswesen, Wasser, Ernährung, Informationstechnik und Telekommunikation, Weltraum oder Siedlungsabfallentsorgung, deren Ausfall oder Beeinträchtigung zu erheblichen Versorgungsengpässen oder zu Gefährdungen der öffentlichen Sicherheit führen würde (§ 2 Nr. 4, § 4 Abs. 1 KRITISDachG). Eine kritische Anlage ist eine Anlage, die für die Erbringung einer kritischen Dienstleistung erheblich ist (§ 2 Nr. 3 KRITISDachG). Betreiber ist, wer unter Berücksichtigung der rechtlichen, wirtschaftlichen und tatsächlichen Umstände bestimmenden Einfluss auf die Anlage ausübt; im Sektor Finanzwesen, wer die tatsächliche Sachherrschaft ausübt (§ 2 Nr. 1 KRITISDachG).

#### 2. Software und IT-Dienste als Anlagen

Der Begriff „Anlage“ ist weit gefasst: eine Betriebsstätte, sonstige ortsfeste Installation, Maschine, ein Gerät, eine sonstige ortsveränderliche technische Installation oder Software und IT-Dienste (§ 2 Nr. 2 KRITISDachG). Für Software und IT-Dienste, die nicht unmittelbar der Steuerung, Überwachung oder Unterstützung physischer Prozesse der Erbringung kritischer Dienstleistungen dienen, gelten ausschließlich die Vorgaben des BSI-Gesetzes (§ 2 Nr. 2 KRITISDachG). Auch die bisherige BSI-KritisV zählte Software und IT-Dienste, die für die Erbringung einer kritischen Dienstleistung notwendig sind, zu den Anlagen (§ 1 Abs. 1 Nr. 1 BSI-KritisV).

#### 3. Schwellenwerte zum Versorgungsgrad

Das [[federal-ministry-of-the-interior|Bundesministerium des Innern]] bestimmt durch Rechtsverordnung die kritischen Dienstleistungen je Sektor, Kategorien von Anlagen und Schwellenwerte zum Versorgungsgrad, ab denen eine Anlage als erheblich gilt (§ 4 Abs. 3, § 5 Abs. 1 KRITISDachG). Bei den Schwellenwerten werden die nationalen Risikoanalysen und Kriterien wie die Zahl der versorgten Einwohner, die Abhängigkeit anderer Sektoren, die Auswirkungen von Ausfällen, der Marktanteil, das betroffene geografische Gebiet und die Verfügbarkeit von Alternativen berücksichtigt; der Regelwert beträgt grundsätzlich **500 000** von einer Anlage zu versorgende Einwohner (§ 5 Abs. 2 KRITISDachG). Das Ministerium kann eine Anlage im Einzelfall auch als kritisch oder als nicht kritisch feststellen (§ 5 Abs. 3 KRITISDachG). Bis die neue Rechtsverordnung gilt, bestimmen weiter die Anlagenkategorien und Schwellenwerte der BSI-KritisV, welche Anlagen kritisch sind (§ 66 BSIG; § 2 Abs. 6 BSI-KritisV für den Sektor Energie).

#### 4. Pflichten der Betreiber

Betreiber müssen ihre kritischen Anlagen spätestens drei Monate, nachdem eine Anlage als kritische Anlage gilt, beim [[bbk|Bundesamt für Bevölkerungsschutz und Katastrophenhilfe (BBK)]] über eine gemeinsam mit dem [[bsi|BSI]] eingerichtete Registrierungsmöglichkeit registrieren; anzugeben sind unter anderem Sektor, kritische Dienstleistung, Werte zum Versorgungsgrad, Standort, öffentliche IP-Adressbereiche und die Typen eingesetzter kritischer Komponenten (§ 8 Abs. 1 KRITISDachG). Risikoanalyse und Risikobewertung gelten neun Monate, Resilienzpflichten, Meldewesen und Pflichten der Geschäftsleitung zehn Monate nach der Registrierung (§ 8 Abs. 7 KRITISDachG). Nach dem BSI-Gesetz gelten Betreiber kritischer Anlagen als besonders wichtige Einrichtungen (§ 28 Abs. 1 Nr. 1 BSIG); für die informationstechnischen Systeme, die für die Funktionsfähigkeit ihrer kritischen Anlagen maßgeblich sind, sind auch über das übliche Schutzniveau hinausgehende Maßnahmen verhältnismäßig, Systeme zur Angriffserkennung sind Pflicht, und die Umsetzung ist dem BSI alle drei Jahre durch Sicherheitsaudits, Prüfungen oder Zertifizierungen nachzuweisen (§§ 31, 39 BSIG). Das Bundesministerium des Innern kann den Einsatz kritischer Komponenten eines Herstellers untersagen, wenn er die öffentliche Ordnung oder Sicherheit voraussichtlich beeinträchtigt (§ 41 BSIG).

#### Herkunft und Varianten

Der Begriff löst die frühere Bezeichnung „Kritische Infrastrukturen“ des BSI-Gesetzes von 2009 ab; § 39 Abs. 3 BSIG verweist auf Betreiber, die nach dem alten BSI-Gesetz Betreiber Kritischer Infrastrukturen waren. Das KRITIS-Dachgesetz setzt die EU-[[cer-directive|CER-Richtlinie]] zur Resilienz kritischer Einrichtungen für den physischen Schutz um, während das BSI-Gesetz in der Fassung von 2025 die [[nis2-directive|NIS-2-Richtlinie]] für die Cybersicherheit umsetzt; die Registrierungsangaben verweisen auf wesentliche Dienste im Sinne des Artikels 2 der Richtlinie (EU) 2022/2557 (§ 8 Abs. 1 Nr. 6 KRITISDachG). Das Finanzwesen ist weitgehend durch [[dora|DORA]] geregelt: Viele Pflichten des KRITIS-Dachgesetzes gelten nicht für Finanzunternehmen nach der Verordnung (EU) 2022/2554 (§ 4 Abs. 2 KRITISDachG).

### Wann einsetzen

- Prüfung, ob eine Organisation oder eines ihrer Systeme unter KRITIS-Pflichten fällt: kritische Dienstleistung, Anlagenkategorie und Versorgungsgrad bestimmen (§§ 4, 5 KRITISDachG; [[bsi-kritisv|BSI-KritisV]]).
- Planung von KI- oder Softwaresystemen, die physische Prozesse kritischer Dienstleistungen steuern, überwachen oder unterstützen, da solche Software selbst Teil einer kritischen Anlage sein kann (§ 2 Nr. 2 KRITISDachG).
- Vorbereitung von Audits, Angriffserkennung und Meldewesen für IT-Systeme kritischer Anlagen (§§ 31, 39 BSIG).

### Stärken und Grenzen

**Stärken**
- Schwellenwertbasierte Kriterien machen die Einstufung weitgehend objektiv und überprüfbar (§ 5 KRITISDachG).
- Ein Begriff verbindet physische Resilienz (KRITISDachG) und IT-Sicherheit (BSIG).
- Einzelfallfeststellungen erfassen Anlagen, die Schwellenwerte verfehlen (§ 5 Abs. 3 KRITISDachG).

**Grenzen**
- Die maßgebliche Rechtsverordnung mit den neuen Schwellenwerten muss erst in Kraft treten, bevor die neuen Begriffe gelten; bis dahin gilt die BSI-KritisV weiter (§ 66 BSIG).
- Mehrere Pflichten gelten nicht für die Sektoren Finanzwesen, Informationstechnik und Telekommunikation, Siedlungsabfallentsorgung sowie Sozialversicherung, die anderen Regeln folgen (§ 4 Abs. 2 KRITISDachG).
- Die Abgrenzung zwischen Software, die physische Prozesse unterstützt (KRITISDachG), und sonstiger Software (nur BSIG) erfordert sorgfältige Prüfung (§ 2 Nr. 2 KRITISDachG).

### Vergleich

| | Kritische Anlage (KRITISDachG / BSIG) | Besonders wichtige Einrichtung (BSIG) | Kritische Einrichtung (CER-Richtlinie) |
|---|---|---|---|
| Grundlage | Erheblichkeit für eine kritische Dienstleistung, Schwellenwerte | Größe und Sektor oder Betreiber einer kritischen Anlage | Ermittlung durch die Mitgliedstaaten bis 17. Juli 2026 (Art. 6) |
| Einheit | Anlage (Betriebsstätte, Gerät, Software, IT-Dienst) | Organisation | Organisation |
| Hauptpflichten | Registrierung, Resilienz, Angriffserkennung, Audits | Risikomanagement, Meldungen, Registrierung | Resilienzmaßnahmen |

Quellen: § 2, § 5, § 8 KRITISDachG; § 28, § 31, § 39 BSIG; Art. 6 Richtlinie (EU) 2022/2557.

### In der Praxis

Betreiber ordnen zunächst ihre kritischen Dienstleistungen und Anlagen den Kategorien und Schwellenwerten der Rechtsverordnung zu und registrieren sich binnen drei Monaten (§ 8 KRITISDachG). Bei KI-Komponenten in der Betriebstechnik, etwa Prognose- oder Steuerungssoftware für Netze oder die Wasserversorgung, ist zu klären, ob sie den physischen Prozess unmittelbar steuern, überwachen oder unterstützen; dann können sowohl Resilienz- als auch BSI-Pflichten greifen (§ 2 Nr. 2 KRITISDachG; [[it-governance-frameworks|IT-Governance-Frameworks]]). Systeme zur Angriffserkennung müssen Parameter aus dem laufenden Betrieb kontinuierlich und automatisch erfassen und auswerten und den Stand der Technik einhalten (§ 31 Abs. 2 BSIG).

### Regulatorischer Kontext

Der Begriff verbindet das [[kritis-dachgesetz|KRITIS-Dachgesetz]] (physische Resilienz, Umsetzung der [[cer-directive|CER-Richtlinie]]), das [[bsig|BSI-Gesetz]] (Cybersicherheit, Umsetzung von [[nis2-directive|NIS 2]]) und im Übergang die [[bsi-kritisv|BSI-KritisV]]. Finanzunternehmen folgen für die digitale operationale Resilienz [[dora|DORA]].

### Merksatz

Eine kritische Anlage ist jede Betriebsstätte, jedes Gerät, jede Software oder jeder IT-Dienst, die für eine kritische Dienstleistung an die Allgemeinheit erheblich ist, in der Regel weil sie etwa 500 000 Menschen oder mehr versorgt; ihr Betreiber muss sich registrieren, Resilienz aufbauen und erhöhte Pflichten zur IT-Sicherheit erfüllen.

### Quellen

- Dachgesetz zur Stärkung der physischen Resilienz kritischer Anlagen (KRITIS-Dachgesetz – KRITISDachG), §§ 2, 4, 5, 8. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kritisdachg/)
- Gesetz über das Bundesamt für Sicherheit in der Informationstechnik und über die Sicherheit in der Informationstechnik von Einrichtungen (BSI-Gesetz – BSIG), §§ 28, 31, 39, 41, 66. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bsig_2025/)
- Verordnung zur Bestimmung kritischer Anlagen nach dem BSI-Gesetz (BSI-Kritisverordnung – BSI-KritisV), §§ 1–2. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bsi-kritisv/)
- Richtlinie (EU) 2022/2557 über die Resilienz kritischer Einrichtungen (CER-Richtlinie), Art. 6. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2557/oj/deu)
