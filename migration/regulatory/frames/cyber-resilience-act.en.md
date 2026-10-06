> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the texts published in the Official Journal of the European Union are authentic.

### TL;DR

The Cyber Resilience Act (CRA) sets EU-wide cybersecurity requirements for hardware and software products with digital elements, from smart home devices and routers to operating systems and apps. Manufacturers must design products securely, assess cybersecurity risks, handle vulnerabilities and provide security updates for a support period of generally at least five years, and mark compliant products with the CE marking. Since 11 September 2026, they must report actively exploited vulnerabilities and severe incidents within 24 hours; most other obligations apply from 11 December 2027. Important and critical products, such as firewalls or smartcards, need stricter conformity assessment.

### Key facts

| | |
| --- | --- |
| Official reference | Regulation (EU) 2024/2847, OJ L, 2024/2847, 20.11.2024 |
| Type and jurisdiction | EU regulation, directly applicable in all Member States |
| Adopted | 23 October 2024 |
| Entry into force | 10 December 2024 |
| Application | 11 December 2027; reporting obligations (Art. 14) from 11 September 2026; notification of conformity assessment bodies (Chapter IV) from 11 June 2026 (Art. 71) |
| Amendments | Article 104 of Regulation (EU) 2025/327 (European Health Data Space), applicable from 26 March 2027: EHR systems demonstrate conformity through the EHDS procedure (new Art. 32(5a)); Art. 13(4) adjusted accordingly |
| Competent authorities | national market surveillance authorities (Art. 52); CSIRTs designated as coordinators and ENISA for reports (Art. 14, 16); notifying authorities and notified bodies (Chapter IV) |
| Version summarised | text as published in the Official Journal; the 2025 amendment is described here but not consolidated |

### Scope

**What** (Art. 2(1)): products with digital elements made available on the EU market whose intended purpose or reasonably foreseeable use includes a direct or indirect data connection to a device or network. Products with digital elements are software or hardware products, including their remote data processing solutions and components placed on the market separately (Art. 3(1)).

**Who**: manufacturers, authorised representatives, importers and distributors (Chapter II); anyone who substantially modifies a product and makes it available is treated as a manufacturer (Art. 21, 22). Open-source software stewards have lighter obligations (Art. 24); free and open-source software not made available in the course of a commercial activity is not covered.

**Exclusions** (Art. 2(2)–(7)): medical devices and in vitro diagnostics, motor vehicles, certified aviation products, marine equipment, identical spare parts, and products developed exclusively for national security or defence.

**Product classes**: important products in Annex III, class I (for example identity management systems, browsers, password managers, VPNs, operating systems, routers, smart home assistants and connected toys) and class II (hypervisors and container runtimes, firewalls, intrusion detection and prevention systems, tamper-resistant microprocessors); critical products in Annex IV (hardware devices with security boxes, smart meter gateways, smartcards and secure elements).

**Structure**: eight chapters: general provisions (Chapter I), obligations of economic operators and free and open-source software (Chapter II), conformity of products (Chapter III), notification of conformity assessment bodies (Chapter IV), market surveillance and enforcement (Chapter V), delegated powers and committee procedure (Chapter VI), confidentiality and penalties (Chapter VII), and transitional and final provisions (Chapter VIII), plus eight annexes, including the essential cybersecurity requirements (Annex I).

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 23 October 2024 | Adoption |
| 20 November 2024 | Publication in the Official Journal |
| 10 December 2024 | Entry into force |
| 11 December 2025 | Commission implementing act on technical descriptions of important and critical product categories due (Art. 7(4)) |
| 11 June 2026 | Chapter IV (notification of conformity assessment bodies) applies |
| 11 September 2026 | Reporting obligations for actively exploited vulnerabilities and severe incidents apply (Art. 14), also for products already on the market (Art. 69(3)) |
| 26 March 2027 | EHDS amendment of Art. 13(4) and new Art. 32(5a) apply |
| 11 December 2027 | General application; products placed on the market earlier are covered only if substantially modified afterwards (Art. 69(2)) |
| 11 June 2028 | Existing EU type-examination certificates under other legislation expire at the latest (Art. 69(1)) |
| 11 December 2030 | First Commission evaluation report, then every four years (Art. 70) |

### Enforcement and penalties

- **Market surveillance** (Art. 52–60): national authorities apply the Market Surveillance Regulation (EU) 2019/1020, evaluate products presenting a significant cybersecurity risk, order corrective action, withdrawal or recall, and carry out coordinated sweeps. The Commission can adopt Union-level measures in exceptional situations (Art. 56, 57).
- **Fines** (Art. 64): up to **15 million euros or 2.5 %** of worldwide annual turnover for breaches of the essential cybersecurity requirements and of Articles 13 and 14; up to **10 million euros or 2 %** for other obligations; up to **5 million euros or 1 %** for incorrect or misleading information. Micro and small enterprises are not fined for missing the 24-hour early warning deadline, and open-source software stewards are not fined at all.
- **Representative actions** (Art. 65): consumer organisations can bring collective actions under Directive (EU) 2020/1828.

### Relationship to other acts

- **[[eu-ai-act|EU AI Act]]**: high-risk AI systems that are products with digital elements are deemed to meet the AI Act's cybersecurity requirements (Article 15 AI Act) if they fulfil the CRA's essential requirements (Art. 12); the AI Act's market surveillance authorities are also responsible under the CRA for such systems (Art. 52(14)).
- **[[nis2-directive|NIS2 Directive]]**: the CRA uses NIS2's definitions of incident and near miss and its CSIRTs designated as coordinators; NIS2 entities benefit from secure products in their supply chains.
- **[[cybersecurity-act|Cybersecurity Act]]**: European cybersecurity certificates can give a presumption of conformity (Art. 27(8)–(9)) and may become mandatory for critical products (Art. 8).
- **[[gdpr|GDPR]]**: market surveillance authorities cooperate with data protection authorities (Art. 52(7)); the essential requirements include data minimisation and protection of confidentiality.
- **General Product Safety Regulation** (EU) 2023/988: applies for risks not covered by the CRA (Art. 11).
- **European Health Data Space** (Regulation (EU) 2025/327): EHR systems that are products with digital elements demonstrate CRA conformity through the EHDS procedure from 26 March 2027.

### Relevance for AI development

- **AI products are covered**: software and hardware with AI components, such as smart assistants, AI-enabled cameras or apps with machine learning features, are products with digital elements if they connect to a device or network; smart home general purpose virtual assistants are important products of class I.
- **High-risk AI** (Art. 12): CRA compliance, documented in the EU declaration of conformity, counts as compliance with the AI Act's cybersecurity requirement; manufacturers may also use AI regulatory sandboxes.
- **Remote processing**: cloud backends without which a product cannot perform a function count as remote data processing and are part of the product (Art. 3(2)); pure software as a service is not covered as such.
- **Secure by design**: the essential requirements of Annex I, such as protection against unauthorised access, data minimisation, resilience and logging, apply to AI features as to any other function; the risk assessment must cover them (Art. 13(2)–(3)).
- **Components and open source** (Art. 13(5)–(6)): manufacturers must exercise due diligence when integrating third-party components, including open-source models and libraries, and report vulnerabilities found in them to their maintainers.
- **Vulnerability reporting** (Art. 14): actively exploited vulnerabilities in AI features, for example prompt injection leading to code execution, must be reported within 24 hours.

### Official sources

- Regulation (EU) 2024/2847, Official Journal: [English](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng) and [German](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/deu)
- Regulation (EU) 2025/327 (European Health Data Space), Article 104: [English](https://eur-lex.europa.eu/eli/reg/2025/327/oj/eng)
