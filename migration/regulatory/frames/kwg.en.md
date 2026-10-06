> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial translation.

### TL;DR

The German Banking Act (Kreditwesengesetz, KWG) is the core of German banking supervision. Anyone who wants to conduct banking business or provide financial services in Germany needs an authorisation (section 32); acting without one is a criminal offence (section 54). The Act transposes the Capital Requirements Directive (CRD) and supplements the directly applicable [[crr-and-crd|CRR]]: it governs capital buffers, a proper business organisation with risk management (section 25a), outsourcing (section 25b), requirements for managers and supervisory bodies, notification and reporting obligations and supervisory powers up to the dismissal of managers, moratoria and the revocation of authorisation.

### Key facts

| | |
| --- | --- |
| Official reference | Gesetz über das Kreditwesen, BGBl. I 1961, 881; republished by notice of 9 September 1998, BGBl. I 1998, 2776 |
| Type and jurisdiction | German federal act |
| Signed | 10 July 1961 |
| Competent authorities | the supervisory authority is the European Central Bank where it performs tasks under the SSM Regulation (EU) No 1024/2013, otherwise the Federal Financial Supervisory Authority (BaFin) (section 1(5)); the Deutsche Bundesbank carries out ongoing monitoring (section 7) |
| Version summarised | consolidated version, last amended by Article 9 of the Act of 12 May 2026 (BGBl. 2026 I No. 139) |

### Scope

**Who**: credit institutions conducting banking business such as deposit, lending or custody business, and financial services institutions, for instance for investment broking, portfolio management, factoring, finance leasing or qualified crypto custody (section 1), as well as financial holding companies, branches of foreign undertakings and central counterparties. Certain bodies such as the Deutsche Bundesbank and the KfW are exempt (section 2).

**CRR as the benchmark** (section 1a): institutions that are not CRR credit institutions are subject to the CRR and CRD requirements as if they were CRR credit institutions; from 1 January 2027 the same applies to the requirements of [[dora|DORA]] (section 1a(2a), section 65a(3)).

**Structure**: eight divisions.

- Division 1 (sections 1–9): definitions, exemptions, qualifying holdings, prohibited business and the tasks and cooperation of the supervisors.
- Division 2 (sections 10–31): own funds, capital buffers and liquidity, lending, refinancing registers, customer rights, notifications, special organisational obligations, prevention of money laundering, accounting, ESG risks and audit.
- Division 3 (sections 32–51): authorisation, protection of designations, information and audits, and supervisory measures.
- Divisions 4 to 6 (sections 51a–53q): housing companies with savings facilities, branches and representative offices of foreign undertakings including CRD third-country branches, central counterparties and central securities depositories.
- Division 6a (sections 53r–53v): DLT pilot regime.
- Divisions 7 and 8 (sections 54–65a): criminal provisions, fines and transitional provisions.

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 10 July 1961 | Banking Act signed |
| 9 September 1998 | Republication of the Act |
| 1 January 2014 | Version under the CRD IV Implementation Act (section 64r) |
| 17 January 2025 | Reporting requirements under Chapter III of DORA apply (section 65a(3)) |
| 1 April 2026 | New notification deadlines for managers and board members apply for the first time (section 64c(2)) |
| 12 May 2026 | Latest amendment of the consolidated version |
| 1 January 2027 | DORA requirements also apply to institutions outside DORA's scope (section 1a(2a)) |

### Enforcement and penalties

- **Supervisory measures** (sections 44–48u): information and audit rights, measures in case of insufficient own funds or organisational deficiencies, special representatives, interim measures in case of danger, moratoria and the dismissal of managers and bans on their activity (sections 36, 36a); as a last resort, revocation of authorisation (section 35).
- **Criminal offences** (sections 54–55b): imprisonment of up to **five years** for banking business without authorisation and for managers who fail to ensure the required risk management and thereby endanger the institution's existence (section 54a).
- **Fines** (section 56): depending on the breach, up to **EUR 5 million**; for legal persons in certain cases up to **EUR 20 million or 10 %** of the previous year's total turnover and up to twice the economic benefit derived from the breach.
- **Periodic penalty payments and publication**: periodic penalty payments for continuing breaches (section 50); final measures and decisions on fines are published on BaFin's website (section 60b).

### Relationship to other acts

- **[[crr-and-crd|CRR and CRD]]**: the KWG transposes the CRD and contains the national supplements to the directly applicable CRR, such as capital buffers (sections 10c–10j) and powers to issue ordinances.
- **[[marisk|MaRisk]]**: BaFin's circular specifies the risk management requirements under section 25a and the outsourcing requirements under section 25b.
- **[[dora|DORA]]**: BaFin has special powers for breaches of DORA (section 47a); measures and sanctions are published under section 60c.
- **[[eba-governance-and-outsourcing-guidelines|EBA guidelines on internal governance and outsourcing]]**: they specify at EU level the governance and outsourcing requirements that the KWG lays down in sections 25a to 25d.
- **Money Laundering Act**: sections 25g to 25m supplement the due diligence obligations of the Money Laundering Act (Geldwäschegesetz) for institutions.
- **[[gdpr|GDPR]]**: section 10(2) allows institutions to process personal data for the purposes of the CRR, such as risk models, under certain conditions.

### Relevance for AI development

- **Risk models and data** (section 10(2)): institutions may process personal data of customers and guarantors for the purposes of the CRR; this is the legal basis for data-driven rating and risk models.
- **Creditworthiness assessment** (section 18a): creditworthiness must be assessed before a consumer credit agreement, and the agreement may only be concluded if the result is positive. AI-based credit scoring is also subject to the obligations of the [[eu-ai-act|AI Act]] for high-risk AI systems.
- **Business organisation** (section 25a): AI systems used in banking fall under risk management and internal control procedures; contingency management must cover IT systems in particular.
- **Outsourcing** (section 25b): where AI services are sourced from third parties, the institution must avoid excessive additional risks and ensure the proper conduct of business and risk management.
- **Transaction monitoring** (section 25h(2)): credit institutions must operate data processing systems that detect suspicious business relationships and transactions; machine learning is frequently used for this.

### Official sources

- [KWG on gesetze-im-internet.de (German)](https://www.gesetze-im-internet.de/kredwg/)
