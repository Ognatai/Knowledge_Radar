> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial translation.

### TL;DR

The Federal Data Protection Act (Bundesdatenschutzgesetz, BDSG) is Germany's general data protection law alongside the [[gdpr|GDPR]]. It does not repeat the GDPR. Instead, it fills the GDPR's opening clauses with German rules, for example on employee data, video surveillance, scoring, research and data protection officers. It also implements the EU directive on data protection in criminal law enforcement (Directive (EU) 2016/680) and sets out the federal data protection authority and criminal penalties. Specific federal laws such as the [[tdddg|TDDDG]] take precedence over it.

### Key facts

| | |
| --- | --- |
| Official reference | Bundesdatenschutzgesetz, BGBl. I 2017, 2097 |
| Type and jurisdiction | German federal law |
| Enacted | 30 June 2017, as Article 1 of the Data Protection Adaptation and Implementation Act EU (DSAnpUG-EU) |
| Entry into force | 25 May 2018, together with the application of the GDPR; replaced the previous BDSG |
| Competent authorities | Federal Commissioner for Data Protection and Freedom of Information (BfDI) for federal public bodies; state data protection authorities for private bodies (§ 40) |
| Version summarised | consolidated text, last amended by Article 3 of the Act of 12 May 2026 |

### Scope

**Who** (§ 1(1)): federal public bodies; state public bodies where no state data protection law applies and they execute federal law or act as judicial bodies; and private bodies (nichtöffentliche Stellen) for automated processing and for manual processing in a filing system. Purely personal or household activities of natural persons are excluded.

**Subsidiarity** (§ 1(2)): other federal data protection rules take precedence; the BDSG applies where they do not regulate a matter or do not regulate it conclusively.

**Relation to EU law** (§ 1(5)): the BDSG does not apply where the GDPR applies directly.

**Structure**: the Act has four parts.

- Part 1 (§§ 1-21): common provisions for all processing, e.g. definitions, video surveillance, data protection officers of public bodies and the BfDI.
- Part 2 (§§ 22-44): implementing provisions for processing under the GDPR.
- Part 3 (§§ 45-84): implementation of Directive (EU) 2016/680 for criminal law enforcement.
- Part 4 (§§ 85-86): activities outside the scope of both EU acts.

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 30 June 2017 | Enactment of the DSAnpUG-EU; Article 1 contains the new BDSG |
| 5 July 2017 | Publication in the Federal Law Gazette (BGBl. I 2017, 2097) |
| 25 May 2018 | Entry into force, together with the application of the GDPR |
| 2019 | Second Data Protection Adaptation and Implementation Act EU; among other things, it raises the threshold for appointing a data protection officer in private bodies to 20 persons (§ 38) |
| 30 March 2023 | CJEU judgment C-34/21 on a Hessian provision worded like § 26(1) BDSG: such national rules on employee data must meet the requirements of Art. 88(2) GDPR |
| 7 December 2023 | CJEU judgment C-634/21 (SCHUFA): calculating a credit score can itself be an automated decision under Art. 22 GDPR, which raises questions about § 31 BDSG |

### Enforcement and penalties

- **Supervision**: the BfDI supervises federal public bodies and, for their telecommunications services, telecommunications companies (§ 9); the state authorities supervise private bodies (§ 40). The BfDI represents Germany in the European Data Protection Board and acts as the single point of contact (§ 17).
- **GDPR fines**: fines under Art. 83 GDPR are imposed under the German Act on Regulatory Offences (OWiG), with modifications (§ 41). No fines are imposed on federal public bodies (§ 43(3)).
- **Own fines** (§ 43): up to **EUR 50,000** for infringements of the consumer credit rules of § 30.
- **Criminal offences** (§ 42): up to **3 years** imprisonment for knowingly and commercially passing on or disclosing non-public personal data of a large number of persons without authorisation; up to **2 years** for unauthorised processing or obtaining data by deception for payment or with intent to enrich or harm. Prosecution only on application (§ 42(3)).
- **Court actions** (§ 44): data subjects can sue controllers and processors at the court of an establishment or at their own habitual residence.

### Relationship to other acts

- **[[gdpr|GDPR]]**: the GDPR applies directly; the BDSG only specifies and supplements it where the GDPR allows national rules (opening clauses, e.g. Art. 6(2), 9(2), 23, 37(4), 85, 88, 89).
- **Directive (EU) 2016/680**: transposed in Part 3 for police and criminal justice authorities.
- **[[tdddg|TDDDG]]**: special rules for telecommunications and digital services, including consent for access to terminal equipment; it takes precedence over the BDSG (§ 1(2)).
- **State data protection laws**: apply to the public bodies of the German states instead of the BDSG.
- **[[eu-ai-act|EU AI Act]]**: does not affect data protection law; AI systems processing personal data in Germany must comply with the GDPR and the BDSG.

### Relevance for AI development

- **Employee data** (§ 26): AI tools in recruiting, performance analysis or workforce monitoring process employee data; § 26 and works agreements govern this, but after C-34/21 the GDPR's general legal bases have to be checked as well.
- **Scoring** (§ 31): models predicting a person's future behaviour for contract decisions, e.g. credit scoring, must rely on a scientifically recognised mathematical-statistical method and may not use address data only.
- **Automated decisions** (§ 37): an additional exception to Art. 22 GDPR, limited to decisions under insurance contracts.
- **Special categories and research** (§§ 22, 27): health or biometric data may be processed for research and statistics without consent if the controller's interests significantly outweigh those of the data subject, with appropriate safeguards; this is relevant for training models on such data, also for [[bias-in-nlp|bias analysis]] and [[fairness-metrics|fairness testing]].
- **Video surveillance** (§ 4): computer vision on cameras in publicly accessible spaces is only permitted for the purposes listed and has to be made recognisable.
- **Data protection officer** (§ 38): required from **20** persons permanently engaged in automated processing, or regardless of size if the processing requires a data protection impact assessment, which is frequent for AI systems.

### Official sources

- [Bundesdatenschutzgesetz on gesetze-im-internet.de (German)](https://www.gesetze-im-internet.de/bdsg_2018/)
