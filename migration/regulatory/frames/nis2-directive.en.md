> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the texts published in the Official Journal of the European Union are authentic.

### TL;DR

The NIS2 Directive sets EU-wide cybersecurity rules for medium-sized and large organisations in 18 sectors, from energy, health and digital infrastructure to manufacturing, digital providers and research. Covered entities are classed as essential or important; they must take risk-management measures, report significant incidents in stages (24 hours, 72 hours, one month), and their management bodies must approve the measures and can be held liable. Member States must set up competent authorities and CSIRTs and provide for fines of up to at least 10 million euros or 2 % of worldwide turnover. NIS2 replaces the first NIS Directive of 2016; in Germany it is implemented by the [[bsig|BSI Act]].

### Key facts

| | |
| --- | --- |
| Official reference | Directive (EU) 2022/2555, OJ L 333, 27.12.2022 |
| Type and jurisdiction | EU directive, to be transposed into national law |
| Adopted | 14 December 2022 |
| Entry into force | 16 January 2023 |
| Transposition | by 17 October 2024; national measures apply from 18 October 2024 (Art. 41) |
| Amendments | none |
| Competent authorities | national competent authorities, single points of contact, cyber crisis management authorities and CSIRTs (Art. 8–10); at EU level the Cooperation Group, the CSIRTs network, EU-CyCLONe and ENISA; in Germany the Federal Office for Information Security (BSI) |
| Version summarised | text as published in the Official Journal |

### Scope

**Who** (Art. 2): public or private entities of a type listed in Annex I or II that are at least medium-sized enterprises and provide services or carry out activities in the Union. Regardless of size, the Directive also covers, among others, providers of public electronic communications networks and services, trust service providers, TLD name registries and DNS service providers, entities identified as critical entities under the [[cer-directive|CER Directive]], domain name registration services, and central government public administration entities.

**Sectors**: Annex I (sectors of high criticality) covers energy, transport, banking, financial market infrastructures, health, drinking water, waste water, digital infrastructure (including cloud computing services, data centre services and content delivery networks), ICT service management (business-to-business, managed service providers and managed security service providers), public administration and space. Annex II (other critical sectors) covers postal and courier services, waste management, chemicals, food, manufacturing (such as medical devices, electronics, machinery and vehicles), digital providers (online marketplaces, search engines and social networking services platforms) and research.

**Essential and important entities** (Art. 3): essential entities are mainly large entities in Annex I sectors, qualified trust service providers, TLD registries and DNS providers, medium-sized telecoms providers, central government entities and critical entities; all other covered entities are important entities. The difference matters for supervision (proactive or only ex post) and fines.

**Limits**: the Directive does not apply to public administration entities active in national security, public security, defence or law enforcement (Art. 2(7)). Sector-specific Union acts with at least equivalent requirements, such as [[dora|DORA]] for the financial sector, take precedence (Art. 4).

**Structure**: nine chapters: general provisions (Chapter I), coordinated cybersecurity frameworks (Chapter II), cooperation at Union and international level (Chapter III), risk-management measures and reporting obligations (Chapter IV), jurisdiction and registration (Chapter V), information sharing (Chapter VI), supervision and enforcement (Chapter VII), delegated and implementing acts (Chapter VIII) and final provisions (Chapter IX), plus three annexes.

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 14 December 2022 | Adoption |
| 27 December 2022 | Publication in the Official Journal |
| 16 January 2023 | Entry into force |
| 17 October 2024 | Transposition deadline; Commission implementing acts on risk-management measures and significant incidents for digital providers due (Art. 21(5), 23(11), 41) |
| 18 October 2024 | National measures apply; Directive (EU) 2016/1148 (NIS1) is repealed (Art. 41, 44) |
| 17 January 2025 | Deadline for national penalty rules and for registration of digital providers such as cloud and data centre service providers (Art. 27, 36) |
| 17 April 2025 | Member States establish lists of essential and important entities, reviewed at least every two years (Art. 3(3)) |
| 6 December 2025 | Germany's implementing act, the new [[bsig|BSI Act]], enters into force |
| 17 October 2027 | First Commission review, then every 36 months (Art. 40) |

### Enforcement and penalties

- **Essential entities** (Art. 32): proactive supervision, including on-site inspections, regular and targeted security audits, ad hoc audits and security scans. Enforcement includes binding instructions, a monitoring officer and, as a last resort, temporary suspension of authorisations and temporary bans on managers.
- **Important entities** (Art. 33): only ex post supervision when evidence indicates non-compliance, with similar but more limited powers.
- **Fines** (Art. 34): for breaches of Articles 21 and 23, maximum fines of at least **10 million euros or 2 %** of worldwide annual turnover for essential entities and at least **7 million euros or 1.4 %** for important entities, whichever is higher.
- **Management liability** (Art. 20, 32(6)): management bodies approve and oversee the measures, must follow training and can be held liable.
- **Data protection** (Art. 35): if an infringement may entail a personal data breach, the data protection authorities are informed; no double fines for the same conduct.

### Relationship to other acts

- **[[cer-directive|CER Directive]]**: adopted alongside NIS2 and covers the physical resilience of critical entities; entities identified as critical entities under CER are essential entities under NIS2 (Art. 3(1)(f)), and the authorities cooperate (Art. 13(5)).
- **[[dora|DORA]]**: as a sector-specific act with equivalent requirements, DORA takes precedence for financial entities (Art. 4); NIS2 authorities cooperate with DORA authorities (Art. 32(10)).
- **[[cybersecurity-act|Cybersecurity Act]]**: defines cybersecurity, cyber threats and ICT products (Art. 6); Member States can require certified products under its European certification schemes (Art. 24).
- **[[cyber-resilience-act|Cyber Resilience Act]]**: covers the security of products with digital elements, while NIS2 covers the security of the entities using them; CRA products help entities secure their supply chain.
- **[[eecc|EECC]]** and **[[eidas|eIDAS]]**: NIS2 replaces the security and incident rules for telecoms providers (Articles 40 and 41 EECC) and trust service providers (Article 19 eIDAS), deleted from 18 October 2024 (Art. 42, 43).
- **[[gdpr|GDPR]]**: applies alongside NIS2; processing of personal data under NIS2 relies on Article 6 GDPR (Art. 2(14)).
- **German implementation**: the [[bsig|BSI Act]] of 2 December 2025; the [[bsi-kritisv|BSI-KritisV]] determines critical facilities.

### Relevance for AI development

- **AI infrastructure providers**: cloud computing services, data centre services and content delivery networks (digital infrastructure) and managed service providers (ICT service management) are Annex I sectors; providers of training and inference platforms are covered from medium size and fall under the jurisdiction of the Member State of their main establishment in the Union (Art. 26).
- **Research organisations** (Annex II): organisations whose primary goal is applied research or experimental development for commercial exploitation are covered; educational institutions are not (Art. 6(41)), though Member States may include them (Art. 2(5)).
- **Supply chain security** (Art. 21(2)(d), (3)): entities must assess the security of their direct suppliers and their secure development procedures, which also applies to providers of AI models, AI services and machine learning libraries.
- **Secure development** (Art. 21(2)(e)): security in acquisition, development and maintenance, including vulnerability handling, applies to AI systems built or bought by covered entities.
- **Incident reporting** (Art. 23): attacks on AI systems such as data poisoning, model theft or prompt injection leading to data leaks can be significant incidents with a 24-hour early warning.
- **Information sharing** (Art. 29): voluntary exchange of indicators of compromise and attack techniques can cover AI-specific threats.

### Official sources

- Directive (EU) 2022/2555, Official Journal: [English](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng) and [German](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/deu)
