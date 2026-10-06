> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial translation.

### TL;DR

The BSI Critical Infrastructure Ordinance (BSI-Kritisverordnung, BSI-KritisV) determines which facilities in Germany count as critical facilities. For nine sectors, from energy and water to health, finance and municipal waste disposal, it defines the critical services and refers to annexes with facility categories and thresholds. Anyone operating a facility that reaches a threshold is an operator of a critical facility and therefore a particularly important entity under the [[bsig|BSI Act]], with the strictest obligations. The Ordinance is a transitional solution: it ceases to have effect once the ordinance under the KRITIS Umbrella Act enters into force.

### Key facts

| | |
| --- | --- |
| Official reference | Verordnung zur Bestimmung kritischer Anlagen nach dem BSI-Gesetz (BSI-Kritisverordnung), BGBl. I 2016, 958 |
| Type and jurisdiction | German federal ordinance |
| Enacted | 22 April 2016, then as the Ordinance on the Determination of Critical Infrastructures under the BSI Act |
| Entry into force | 3 May 2016 |
| Current title | since 6 December 2025 (Act implementing the NIS2 Directive) |
| Competent authorities | Federal Office for Information Security (BSI) for operators' obligations under the BSIG; Federal Ministry of the Interior as issuer of the Ordinance |
| Version summarised | consolidated text, last amended by Article 3(1) of the Act of 15 May 2026 |

### Scope

**Subject matter**: the Ordinance specifies which facilities are critical facilities within the meaning of the BSI Act. For each sector, it defines the critical services, the areas in which they are provided, and the critical facilities: facilities of a category listed in the relevant annex (column B) that reach or exceed the threshold given there (column D).

**Definitions** (§ 1): facilities are premises, mobile equipment, and software and IT services necessary to provide a critical service. The level of supply measures a facility's contribution to supplying the general public; the threshold marks the point from which this contribution is significant. Several facilities of the same category that are operationally connected count as one joint facility.

**Sectors** (§§ 2–10): energy; water; food; information technology and telecommunications; health; finance; social insurance benefits and basic income support for jobseekers; transport and traffic; municipal waste disposal.

**Who**: operators of facilities in these sectors that reach a threshold. Where several persons operate a facility jointly, each is responsible for the obligations (§ 1(2)).

**Structure**: twelve sections (definitions, nine sectors, evaluation, expiry) and annexes with facility categories and thresholds for each sector; the annexes are not summarised here.

### Sections

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 22 April 2016 | Ordinance on the Determination of Critical Infrastructures enacted |
| 3 May 2016 | Entry into force |
| 6 December 2025 | Renamed Ordinance on the Determination of Critical Facilities; references updated to the new BSI Act |
| 15 May 2026 | Latest amendment of the version summarised here |
| open | Ceases to have effect when the ordinance under § 4(3) and § 5(1) of the KRITIS Umbrella Act enters into force; the Federal Ministry of the Interior announces the date in the Federal Law Gazette (§ 12) |

### Enforcement and penalties

- The Ordinance itself contains no obligations and no penalties. It determines who operates a critical facility; obligations and fines follow from the [[bsig|BSI Act]].
- **Consequences of classification**: operators of critical facilities are particularly important entities (§ 28(1) BSIG). Among other things, they must take enhanced risk management measures and use attack detection systems (§ 31 BSIG), report incidents (§ 32 BSIG) and demonstrate implementation every three years through audits, inspections or certifications (§ 39 BSIG).
- **Evaluation** (§ 11): critical services, facility categories and thresholds are reviewed every two years.

### Relationship to other acts

- **[[bsig|BSI Act]]**: the Ordinance is based on the BSIG and determines which facilities fall under its rules for critical facilities. Under § 66 BSIG, the KRITIS Umbrella Act's definitions of critical facility and critical service apply only once its ordinance has entered into force; until then, the previous rules remain.
- **KRITIS Umbrella Act** (KRITIS-Dachgesetz): implements the [[cer-directive|CER Directive]] and governs the physical resilience of critical facilities. The ordinance under § 4(3) and § 5(1) of the KRITIS Umbrella Act is to lay down critical services, facility categories and thresholds uniformly in future; its standard threshold is 500,000 inhabitants supplied. When it enters into force, the BSI-KritisV ceases to have effect.
- **[[nis2-directive|NIS2 Directive]]**: classification as operator of a critical facility makes an entity a particularly important entity under the German implementation of NIS2 in the BSIG.

### Relevance for AI development

- **Data centres and hosting** (§ 5): housing and IT hosting are part of the critical service of data storage and processing. Operators of large data centres, including those used for training and running AI models, can be operators of critical facilities once they reach the threshold.
- **Software and IT services as facilities** (§ 1(1)): software and IT services necessary to provide a critical service are part of the facility. AI components in control rooms, grid control or laboratory diagnostics can therefore be part of a critical facility.
- **Consequences for AI projects**: anyone using AI in a critical facility must include it in risk management, attack detection and the evidence required under the BSIG; providers of AI solutions should expect corresponding requirements from their customers.

### Official sources

- [BSI-KritisV on gesetze-im-internet.de (German)](https://www.gesetze-im-internet.de/bsi-kritisv/)
