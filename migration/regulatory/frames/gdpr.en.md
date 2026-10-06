> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the texts published in the Official Journal of the European Union are authentic.

### TL;DR

The General Data Protection Regulation (GDPR) is the EU's central law on the processing of personal data. It sets out when processing is lawful, which principles every processing must follow, which rights data subjects have, and which obligations controllers and processors carry. It applies to organisations in the EU and to organisations outside the EU that offer goods or services to people in the EU or monitor their behaviour. Independent supervisory authorities enforce it, with fines of up to EUR 20 million or 4% of worldwide annual turnover.

### Key facts

| | |
| --- | --- |
| Official reference | Regulation (EU) 2016/679, OJ L 119, 4.5.2016 |
| Type and jurisdiction | EU regulation, directly applicable in all Member States |
| Adopted | 27 April 2016 |
| Entry into force | 24 May 2016 |
| Application | 25 May 2018 |
| Amendments | none; corrigenda only. Amendments were proposed by the Commission in 2025 (COM(2025) 501 and COM(2025) 837) |
| Competent authorities | national supervisory authorities; the European Data Protection Board for consistency |
| Version summarised | consolidated text of 4 May 2016 |

### Scope

**Material scope** (Art. 2): processing of personal data wholly or partly by automated means, and manual processing of personal data that form part of a filing system. Personal data is any information relating to an identified or identifiable natural person (Art. 4(1)).

**Territorial scope** (Art. 3): processing in the context of an establishment of a controller or processor in the EU, regardless of where the processing takes place; and processing of data of people in the EU by controllers or processors outside the EU, where it relates to offering goods or services to them or to monitoring their behaviour in the EU.

**Exclusions** (Art. 2(2)): activities outside the scope of Union law, the common foreign and security policy, purely personal or household activities, and processing by competent authorities for criminal law enforcement, which falls under Directive (EU) 2016/680.

**Key roles**: the *controller* decides on the purposes and means of processing; the *processor* processes data on the controller's behalf; the *data subject* is the person the data relates to.

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 4 May 2016 | Publication in the Official Journal |
| 24 May 2016 | Entry into force |
| 25 May 2018 | Application; repeal of Directive 95/46/EC (Art. 94) |
| 2025 | Commission proposals to amend the GDPR (COM(2025) 501 and COM(2025) 837); not adopted in the version summarised here |

### Enforcement and penalties

- **Supervision**: each Member State has at least one independent supervisory authority (Art. 51). For cross-border processing, the authority of the controller's main establishment acts as lead authority (one-stop shop, Art. 56); the European Data Protection Board ensures consistent application (Art. 63-76).
- **Fines** (Art. 83): up to **EUR 10 million or 2%** of worldwide annual turnover, whichever is higher, for infringements of, among others, the obligations of controllers and processors (Art. 8, 11, 25-39, 42, 43); up to **EUR 20 million or 4%** for infringements of the principles and legal bases (Art. 5, 6, 7, 9), data subjects' rights (Art. 12-22), international transfers (Art. 44-49) and orders of the supervisory authority.
- **Remedies**: complaint to a supervisory authority (Art. 77), judicial remedies against authorities, controllers and processors (Art. 78-79), and compensation for material and non-material damage (Art. 82).

### Relationship to other acts

- **[[eprivacy-directive|ePrivacy Directive]]**: for publicly available electronic communications services, the GDPR imposes no additional obligations where the ePrivacy Directive sets specific obligations with the same objective (Art. 95). In Germany, the Directive is implemented by the [[tdddg|TDDDG]].
- **[[bdsg|BDSG]]**: the German Federal Data Protection Act uses the GDPR's opening clauses, e.g. for employee data and for processing by public bodies, and implements Directive (EU) 2016/680.
- **Directive (EU) 2016/680**: governs processing by authorities for the prevention, investigation and prosecution of criminal offences instead of the GDPR.
- **[[eu-ai-act|EU AI Act]]**: does not affect the GDPR (Art. 2(7) AI Act); AI systems that process personal data need a legal basis under the GDPR. The AI Act adds its own rules for processing special categories of data for bias detection (Art. 4a AI Act).
- **[[data-act|Data Act]] and [[data-governance-act|Data Governance Act]]**: apply without prejudice to the GDPR; where they concern personal data, the GDPR prevails.

### Relevance for AI development

- **Legal basis for training data** (Art. 6): collecting or reusing personal data to train or fine-tune models needs a legal basis, typically consent or legitimate interests; the purpose limitation principle (Art. 5(1)(b)) restricts reusing data collected for other purposes.
- **Data minimisation** (Art. 5(1)(c)): only data necessary for the purpose may be processed, which favours anonymisation, pseudonymisation and privacy-preserving techniques such as [[differential-privacy-and-federated-learning|differential privacy and federated learning]].
- **Special categories** (Art. 9): health, biometric or ethnic-origin data may only be processed under the narrow conditions of Art. 9(2), which also limits collecting such data for [[bias-in-nlp|bias analysis]] and [[fairness-metrics|fairness testing]].
- **Transparency and access** (Art. 12-15): data subjects must be informed about processing and can request access to their data, including when it is used in AI systems.
- **Right to erasure** (Art. 17): personal data must be deletable; data held in a [[retrieval-augmented-generation|retrieval index]] can be deleted directly, whereas data absorbed into model weights cannot be removed selectively without retraining.
- **Automated decisions** (Art. 22): decisions based solely on automated processing that produce legal or similarly significant effects are only permitted under the exceptions of Art. 22(2), with safeguards including human intervention and the right to contest; this links to [[explainable-ai|explainable AI]].
- **Data protection by design** (Art. 25) and **impact assessments** (Art. 35): new technologies with likely high risk require a data protection impact assessment before processing starts.
- **International transfers** (Art. 44-49): using cloud-hosted models or APIs outside the EU is a transfer that needs an adequacy decision or appropriate safeguards such as standard contractual clauses.

### Official sources

- Regulation (EU) 2016/679, Official Journal: [English](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) and [German](https://eur-lex.europa.eu/eli/reg/2016/679/oj/deu)
- [Consolidated text of 4 May 2016 (English)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504)
