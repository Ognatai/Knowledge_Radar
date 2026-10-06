> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the documents published by the Basel Committee on Banking Supervision and the European Central Bank are authoritative.

### TL;DR

BCBS 239 is the Basel Committee's set of 14 principles for effective risk data aggregation and risk reporting (RDARR), published in January 2013 in response to the financial crisis, when many banks could not aggregate their risk exposures quickly and accurately. The principles cover governance and IT infrastructure, the accuracy, completeness, timeliness and adaptability of risk data, the quality of risk reports, and supervisory review. The ECB Guide on effective risk data aggregation and risk reporting of May 2024 sets out the ECB's minimum supervisory expectations for the banks it supervises directly, with a focus on management body responsibility, scope of application, data governance, an integrated data architecture, data quality management, timely reporting and implementation programmes.

### Key facts

| | |
| --- | --- |
| Official reference | Basel Committee on Banking Supervision, Principles for effective risk data aggregation and risk reporting (BCBS 239), January 2013; ECB Banking Supervision, Guide on effective risk data aggregation and risk reporting, May 2024 |
| Type and jurisdiction | international standard of the Basel Committee and supervisory guide of the ECB; neither is legally binding, but supervisors use them as a benchmark |
| Published | January 2013 (BCBS 239); May 2024 (ECB guide) |
| Competent authorities | national supervisors; for significant institutions in the euro area, the ECB in the Single Supervisory Mechanism |
| Version summarised | documents as published; both are available in English only |

### Scope

**Who**: BCBS 239 applies primarily to global systemically important banks (G-SIBs); the Basel Committee strongly suggests that national supervisors also apply the principles to domestic systemically important banks (D-SIBs) three years after their designation. The ECB guide addresses the significant institutions directly supervised by the ECB and uses the BCBS 239 principles as a benchmark of best practices.

**Proportionality**: the principles may be applied to a wider range of banks in a way that is proportionate to the size, nature and complexity of their operations.

**Legal anchor in the EU**: the expectations specify the governance and risk management requirements of the [[crr-and-crd|CRD]] (Articles 74, 76 and 88) as interpreted by the [[eba-governance-and-outsourcing-guidelines|EBA guidelines on internal governance]].

**Structure**: BCBS 239 groups its 14 principles into four parts: overarching governance and infrastructure (Principles 1–2), risk data aggregation capabilities (3–6), risk reporting practices (7–11) and supervisory review, tools and cooperation (12–14). The ECB guide sets out seven supervisory expectations (Section 3) and its supervisory approach (Section 4).

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| January 2013 | Publication of BCBS 239 |
| January 2016 | Deadline for G-SIBs designated in 2011 or 2012 to meet the principles; G-SIBs designated later have three years from designation |
| May 2024 | Publication of the ECB Guide on effective risk data aggregation and risk reporting |

### Enforcement and penalties

- **No penalties of their own**: BCBS 239 and the ECB guide are not legally binding; they describe supervisory expectations.
- **Supervisory measures** (Principle 13): supervisors should require effective and timely remedial action and can use a range of tools, including Pillar 2 measures under the [[crr-and-crd|CRD]].
- **ECB approach** (Section 4 of the guide): more targeted supervisory activities and a more intrusive use of supervisory powers to tackle severe, long-lasting deficiencies.

### Relationship to other acts

- **[[crr-and-crd|CRR and CRD]]**: the RDARR expectations build on the CRD requirements for robust governance arrangements and risk management.
- **[[eba-governance-and-outsourcing-guidelines|EBA guidelines on internal governance]]**: the ECB guide refers to Title II of the EBA guidelines for the responsibilities of the management body.
- **[[marisk|MaRisk]]**: for less significant institutions in Germany, the requirements on data quality (AT 7.2) and risk reporting (BT 2) of MaRisk reflect the same principles.
- **[[dora|DORA]]**: data architecture and IT infrastructure supporting risk data aggregation are also subject to DORA's ICT risk management requirements.

### Relevance for AI development

- **Data quality as a precondition**: accurate, complete and timely risk data (Principles 3–6) are also a precondition for reliable machine learning models in banking; the ECB guide explicitly includes models in the scope of the data architecture.
- **Automation** (Principle 3): risk data should be aggregated on a largely automated basis to minimise errors, which favours automated data pipelines with documented controls.
- **Data lineage and metadata** (ECB guide Sections 3.2 and 3.4): data taxonomies, a business glossary, a metadata repository and coverage of the whole data lifecycle support traceability, which is also needed for training and input data of AI systems.
- **Ad hoc analyses** (Principle 6): the ability to produce aggregated risk data on demand, including in a crisis, is a use case for AI-based analytics, but results must meet the same accuracy and validation standards.
- **Reporting** (Principles 7–11): AI-generated risk reports must be accurate, reconciled and validated, clear and tailored to their recipients.

### Official sources

- [BCBS 239 – Principles for effective risk data aggregation and risk reporting (bis.org)](https://www.bis.org/publ/bcbs239.htm)
- [ECB Guide on effective risk data aggregation and risk reporting (bankingsupervision.europa.eu)](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guides240503_riskreporting.en.pdf)
