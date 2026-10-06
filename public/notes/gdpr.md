---
title_en: General Data Protection Regulation (GDPR)
title_de: Datenschutz-Grundverordnung (DSGVO)
entity_type: Regulation
jurisdiction: EU
instrument: regulation
status: in-force
official_reference: Regulation (EU) 2016/679
consolidated_version: 2016-05-04
aliases:
- GDPR
- DSGVO
- DS-GVO
sources:
- https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
- https://eur-lex.europa.eu/eli/reg/2016/679/oj/deu
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504
---

## EN

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

### Chapter I — General provisions

#### Article 1 — Subject-matter and objectives

Lays down rules relating to the protection of natural persons with regard to the processing of personal data and the free movement of personal data.

#### Article 2 — Material scope

Applies to processing of personal data by automated means or forming part of a filing system, and does not apply to certain specified exceptions.

#### Article 3 — Territorial scope

Applies the Regulation to processing in the context of an EU establishment of a controller or processor, and to non-EU controllers or processors that offer goods or services to, or monitor the behaviour of, people in the Union.

#### Article 4 — Definitions

Defines the key terms of the Regulation, including personal data, processing, profiling, pseudonymisation, controller, processor, consent, personal data breach, and genetic, biometric and health data.

### Chapter II — Principles

#### Article 5 — Principles relating to processing of personal data

##### What is it about?

Article 5 sets out the principles that personal data must be processed in accordance with, including lawfulness, fairness, transparency, purpose limitation, data minimisation, accuracy, storage limitation, and integrity and confidentiality. It also establishes the accountability principle for controllers.

##### What does the article require?

- **Paragraph 1** – Personal data shall be:
  - (a) processed lawfully, fairly and in a transparent manner (*lawfulness, fairness and transparency*);
  - (b) collected for specified, explicit and legitimate purposes and not further processed in a manner incompatible with those purposes; further processing for archiving in the public interest, scientific or historical research or statistical purposes under Article 89(1) is not considered incompatible (*purpose limitation*);
  - (c) adequate, relevant and limited to what is necessary for the purposes (*data minimisation*);
  - (d) accurate and, where necessary, kept up to date; inaccurate data must be erased or rectified without delay (*accuracy*);
  - (e) kept in a form which permits identification no longer than necessary; longer storage is possible for the purposes under Article 89(1) with appropriate safeguards (*storage limitation*);
  - (f) processed with appropriate security, including protection against unauthorised or unlawful processing and accidental loss, destruction or damage (*integrity and confidentiality*).
- **Paragraph 2** – The controller is responsible for, and must be able to demonstrate, compliance with paragraph 1 (*accountability*).

##### Who is affected?

Every controller, for every processing of personal data. Processors are bound indirectly through their contracts and their own obligations under the Regulation.

##### What is not specified?

The article does not specify the exact methods for demonstrating compliance with paragraph 1. It does not define "fairness" in specific contexts; the legal bases for lawfulness are set out in Article 6. It does not detail the "appropriate technical or organisational measures" required for security under point (f) of paragraph 1. It does not specify the scope or nature of the "demonstration" required under paragraph 2.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Define and document the purpose of each training or fine-tuning dataset before collecting data; check compatibility before reusing data collected for other purposes (purpose limitation).
- Remove fields that the model does not need, and prefer anonymised or pseudonymised data (data minimisation).
- Set retention periods for training data, logs and prompts and delete data when they expire (storage limitation).
- Keep records that show how each principle is met, since the controller must be able to demonstrate compliance (accountability).

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 6 — Lawfulness of processing

##### What is it about?

Article 6 establishes the conditions under which the processing of personal data is lawful. It defines the lawful bases for processing, including consent, contract, legal obligation, vital interests, public interest, and legitimate interests. It also specifies requirements for legal bases related to points (c) and (e) of paragraph 1, and sets out criteria for determining compatibility of further processing.

##### What does the article require?

- **Paragraph 1** – Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent; (b) processing is necessary for a contract; (c) processing is necessary for compliance with a legal obligation; (d) processing is necessary to protect vital interests; (e) processing is necessary for a task in the public interest or exercise of official authority; (f) processing is necessary for legitimate interests, except where overridden by the data subject’s rights (including children’s rights). Point (f) does not apply to public authorities performing their tasks.
- **Paragraph 2** – Member States may maintain or introduce more specific provisions to adapt the application of rules regarding processing for compliance with points (c) and (e) of paragraph 1, including determining specific requirements for processing and ensuring lawful and fair processing.
- **Paragraph 3** – The basis for processing referred to in points (c) and (e) of paragraph 1 shall be laid down by Union law or Member State law. The legal basis must meet an objective of public interest and be proportionate. It may contain specific provisions on general conditions, types of data, data subjects, disclosure entities, purpose limitation, storage periods, processing operations, and safeguards.
- **Paragraph 4** – Where further processing is not based on consent or Union/Member State law under Article 23(1), the controller must assess compatibility by considering: (a) link between initial and further purposes; (b) context of collection; (c) nature of data (including special categories under Article 9 or criminal data under Article 10); (d) consequences for data subjects; (e) existence of appropriate safeguards (e.g., encryption).

##### Who is affected?

Controllers are directly affected by the requirements in paragraphs 1, 3, and 4. Member States are affected by the obligation in paragraph 2. Public authorities are affected by the exclusion in paragraph 1, point (f).

##### What is not specified?

The article does not specify what constitutes "necessary" for contract performance or legal obligation. It does not define "vital interests" or "public interest" in detail. It does not prescribe specific safeguards beyond mentioning encryption or pseudonymisation in paragraph 4. It does not detail how to determine proportionality under paragraph 3.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Choose and document a legal basis for each processing purpose before it starts, e.g. separately for operating a service and for training models on its data.
- Where legitimate interests (point (f)) are relied on for training, document the balancing test, including the reasonable expectations of the data subjects.
- Before reusing data for a new purpose such as model training, carry out the compatibility test of paragraph 4 and consider safeguards such as pseudonymisation.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 7 — Conditions for consent

Requires the controller to be able to demonstrate that the data subject has consented to processing of his or her personal data.

#### Article 8 — Conditions applicable to child's consent in relation to information society services

Sets the conditions for a child's consent to information society services offered directly to a child; below the age of 16, which Member States may lower to 13, consent must be given or authorised by the holder of parental responsibility.

#### Article 9 — Processing of special categories of personal data

##### What is it about?

Article 9 prohibits the processing of special categories of personal data, including racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, genetic data, biometric data for identification, health data, and data concerning sex life or sexual orientation. It sets out specific exceptions to this prohibition.

##### What does the article require?

- **Paragraph 1** – Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation is prohibited.
- **Paragraph 2** – Paragraph 1 shall not apply if one of the following applies:
  - (a) the data subject has given explicit consent;
  - (b) processing is necessary for obligations or rights in employment and social security law;
  - (c) processing is necessary to protect vital interests where the data subject cannot consent;
  - (d) processing is carried out by a foundation, association, or non-profit body with a political, philosophical, religious, or trade union aim, with appropriate safeguards and solely for members or persons with regular contact;
  - (e) processing relates to data manifestly made public by the data subject;
  - (f) processing is necessary for legal claims or judicial proceedings;
  - (g) processing is necessary for substantial public interest under proportionate law providing safeguards;
  - (h) processing is necessary for preventive or occupational medicine, medical diagnosis, or health care under specific law and safeguards;
  - (i) processing is necessary for public health under specific law providing safeguards;
  - (j) processing is necessary for archiving, research, or statistical purposes under specific law providing safeguards.
- **Paragraph 3** – Personal data referred to in paragraph 1 may be processed for the purposes referred to in point (h) of paragraph 2 when processed by or under the responsibility of a professional subject to professional secrecy, or by another person subject to an obligation of secrecy.
- **Paragraph 4** – Member States may maintain or introduce further conditions, including limitations, regarding the processing of genetic data, biometric data, or data concerning health.

##### Who is affected?

Controllers processing special categories of personal data are directly affected. The data subject is affected regarding consent requirements. Member States are affected regarding the ability to maintain or introduce further conditions. Entities processing data for purposes listed in paragraph 2(b), (d), (h), (i), or (j) are affected by the specific conditions stated.

##### What is not specified?

The article does not specify what constitutes "explicit consent" under paragraph 2(a), nor the precise content of "appropriate safeguards" under paragraphs 2(b), (d), (h), and (j). It does not define "substantial public interest" under paragraph 2(g) or "proportionate" measures under paragraphs 2(g) and (j). It does not specify the nature of "further conditions" Member States may introduce under paragraph 4.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Check training and evaluation datasets for special categories of data, including data from which such characteristics can be inferred, e.g. health or ethnic origin.
- Process biometric data for uniquely identifying persons, e.g. face recognition, only under one of the exceptions of paragraph 2.
- Where special categories are needed for bias detection, identify the exception relied on; for high-risk AI systems, Art. 4a of the AI Act adds a specific basis.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 10 — Processing of personal data relating to criminal convictions and offences

Requires processing of personal data relating to criminal convictions and offences to be carried out only under the control of official authority or when authorised by Union or Member State law with appropriate safeguards.

#### Article 11 — Processing which does not require identification

Exempts the controller from maintaining, acquiring, or processing additional information to identify the data subject when such identification is not required for the processing purposes.

### Chapter III — Rights of the data subject

**Section 1 — Transparency and modalities**

#### Article 12 — Transparent information, communication and modalities for the exercise of the rights of the data subject

Requires the controller to provide information and communications to the data subject in a concise, transparent, intelligible and easily accessible form using clear and plain language.

**Section 2 — Information and access to personal data**

#### Article 13 — Information to be provided where personal data are collected from the data subject

Requires the controller to give the data subject specified information when collecting personal data from them, including the controller's identity, the purposes and legal basis of the processing and the data subject's rights.

#### Article 14 — Information to be provided where personal data have not been obtained from the data subject

Requires the controller to give the data subject specified information when personal data have not been obtained from them, including the controller's identity, the purposes, the categories of data and their source.

#### Article 15 — Right of access by the data subject

Gives the data subject the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed and, where that is the case, access to the personal data and specific information.

**Section 3 — Rectification and erasure**

#### Article 16 — Right to rectification

Gives the data subject the right to obtain from the controller without undue delay the rectification of inaccurate personal data concerning him or her.

#### Article 17 — Right to erasure (‘right to be forgotten’)

##### What is it about?

Article 17 establishes the right of a data subject to obtain the erasure of personal data concerning them from a controller without undue delay, and the controller's obligation to erase such data where specific grounds apply. It also addresses the controller's duty when personal data has been made public and outlines exceptions to this right.

##### What does the article require?

- **Paragraph 1** – The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay, and the controller shall have the obligation to erase personal data without undue delay where one of the following grounds applies: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing; (c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding legitimate grounds for the processing, or the data subject objects to the processing pursuant to Article 21(2); (d) the personal data have been unlawfully processed; (e) the personal data have to be erased for compliance with a legal obligation in Union or Member State law to which the controller is subject; (f) the personal data have been collected in relation to the offer of information society services referred to in Article 8(1).
- **Paragraph 2** – Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller, taking account of available technology and the cost of implementation, shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.
- **Paragraph 3** – Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (a) for exercising the right of freedom of expression and information; (b) for compliance with a legal obligation which requires processing by Union or Member State law to which the controller is subject or for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller; (c) for reasons of public interest in the area of public health in accordance with points (h) and (i) of Article 9(2) as well as Article 9(3); (d) for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) in so far as the right referred to in paragraph 1 is likely to render impossible or seriously impair the achievement of the objectives of that processing; or (e) for the establishment, exercise or defence of legal claims.

##### Who is affected?

The data subject is affected by the right to erasure. The controller is affected by the obligation to erase personal data under the specified grounds and by the duty to inform other controllers under paragraph 2. Other controllers processing data made public by the controller are to be informed under paragraph 2; the article does not itself oblige them to erase.

##### What is not specified?

The article does not specify what constitutes "undue delay" for the erasure obligation. It does not define the scope or limits of "reasonable steps" or "technical measures" under paragraph 2. It does not elaborate on the meaning of "overriding legitimate grounds" under paragraph 1(c). It does not specify the criteria for determining when processing is "necessary" under paragraph 3 for the listed exceptions.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Set up a process to receive, verify and answer erasure requests without undue delay, and check the exceptions of paragraph 3 before refusing.
- Design systems so that personal data can be found and deleted, e.g. documents in a retrieval index of a RAG system.
- Note that data absorbed into model weights cannot be removed selectively without retraining; decide in advance how erasure requests affecting training data will be handled.
- Where data were made public, inform other controllers processing them, e.g. by technical means, as far as reasonable.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 18 — Right to restriction of processing

Gives the data subject the right to obtain restriction of processing where certain conditions apply, including contested accuracy, unlawful processing, no longer needed data, or objection pending verification.

#### Article 19 — Notification obligation regarding rectification or erasure of personal data or restriction of processing

Requires the controller to communicate rectification, erasure or restriction of personal data to each recipient unless impossible or involving disproportionate effort and to inform the data subject about those recipients upon request.

#### Article 20 — Right to data portability

Gives the data subject the right to receive personal data concerning him or her in a structured, commonly used and machine-readable format and to transmit those data to another controller without hindrance.

**Section 4 — Right to object and automated individual decision-making**

#### Article 21 — Right to object

Gives the data subject the right to object to processing based on public interest or legitimate interests, including profiling, and an unconditional right to object to processing for direct marketing.

#### Article 22 — Automated individual decision-making, including profiling

##### What is it about?

Article 22 concerns the right of a data subject not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning the data subject or similarly significantly affects them.

##### What does the article require?

- **Paragraph 1** – The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her.
- **Paragraph 2** – Paragraph 1 shall not apply if the decision: (a) is necessary for entering into, or performance of, a contract between the data subject and a data controller; (b) is authorised by Union or Member State law to which the controller is subject and which also lays down suitable measures to safeguard the data subject's rights and freedoms and legitimate interests; or (c) is based on the data subject's explicit consent.
- **Paragraph 3** – In the cases referred to in points (a) and (c) of paragraph 2, the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.
- **Paragraph 4** – Decisions referred to in paragraph 2 shall not be based on special categories of personal data referred to in Article 9(1), unless point (a) or (g) of Article 9(2) applies and suitable measures to safeguard the data subject's rights and freedoms and legitimate interests are in place.

##### Who is affected?

The data subject is affected by the right under Paragraph 1. The data controller is affected by the requirements in Paragraphs 2, 3, and 4, particularly regarding the implementation of suitable measures and restrictions on processing special categories of personal data. In Germany, § 37 BDSG adds a further exception for insurance contracts.

##### What is not specified?

The article does not specify what constitutes "suitable measures" to safeguard rights and freedoms. It does not define "legal effects" or "similarly significantly affects" in detail. It does not specify how "human intervention" must be implemented. It does not detail the requirements for "suitable measures" under Paragraph 4 when applying Article 9(2)(a) or (g).

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Identify decisions taken solely by an AI system that have legal or similarly significant effects, e.g. credit, recruiting or insurance decisions.
- Use such decisions only under one of the exceptions of paragraph 2 and provide human intervention, a way to express one's point of view and a way to contest the decision.
- Make sure that human review is meaningful and not a formality; otherwise the decision may still be solely automated.
- Avoid special categories of data in such decisions unless point (a) or (g) of Art. 9(2) applies.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

**Section 5 — Restrictions**

#### Article 23 — Restrictions

Allows Union or Member State law to restrict certain obligations and rights under Articles 12 to 22, Article 34, and part of Article 5 when necessary and proportionate for safeguarding national security, public security, and other important objectives.

### Chapter IV — Controller and processor

**Section 1 — General obligations**

#### Article 24 — Responsibility of the controller

Requires the controller to implement and review appropriate technical and organisational measures to ensure and demonstrate compliance with the Regulation.

#### Article 25 — Data protection by design and by default

##### What is it about?

Article 25 sets out requirements for controllers to implement data protection by design and by default, including technical and organisational measures to ensure compliance with the Regulation.

##### What does the article require?

- **Paragraph 1** – The controller shall implement appropriate technical and organisational measures, such as pseudonymisation, taking into account the state of the art, the cost of implementation, and the nature, scope, context and purposes of processing as well as the risks of varying likelihood and severity for rights and freedoms of natural persons. These measures must be designed to implement data-protection principles, such as data minimisation, in an effective manner and integrate necessary safeguards into processing to meet the requirements of this Regulation and protect the rights of data subjects. This applies both at the time of determining the means for processing and at the time of processing itself.
- **Paragraph 2** – The controller shall implement appropriate technical and organisational measures to ensure that, by default, only personal data necessary for each specific purpose of the processing are processed. This obligation applies to the amount of personal data collected, the extent of their processing, the period of their storage, and their accessibility. In particular, such measures shall ensure that by default personal data are not made accessible without the individual's intervention to an indefinite number of natural persons.
- **Paragraph 3** – An approved certification mechanism pursuant to **Article 42** may be used as an element to demonstrate compliance with the requirements set out in paragraphs 1 and 2 of this Article.

##### Who is affected?

The controller. Recital 78 encourages producers of products, services and applications to take the right to data protection into account during development; the article itself does not oblige them.

##### What is not specified?

The article does not specify what constitutes the "state of the art" or the "cost of implementation" for the purposes of paragraph 1. It does not specify the exact technical or organisational measures required beyond examples given. It does not define "by default" beyond the context of paragraph 2. It does not specify the criteria for an "approved certification mechanism" under Article 42.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Consider data protection when designing an AI system, e.g. pseudonymise training data, limit features to what the purpose needs and restrict access to models and logs.
- Choose privacy-friendly defaults, e.g. no use of user inputs for training unless the user decides otherwise, and short retention of prompts and outputs.
- Consider privacy-preserving techniques such as differential privacy or federated learning where they fit the purpose.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 26 — Joint controllers

Requires joint controllers to determine their respective responsibilities for compliance with the Regulation through an arrangement, ensuring transparency and the data subject's rights.

#### Article 27 — Representatives of controllers or processors not established in the Union

Requires the controller or processor not established in the Union to designate in writing a representative in the Union where Article 3(2) applies.

#### Article 28 — Processor

Requires the controller to use only processors providing sufficient guarantees to implement appropriate technical and organisational measures to ensure compliance with the Regulation and protection of data subjects' rights.

#### Article 29 — Processing under the authority of the controller or processor

Requires the processor and any person acting under the authority of the controller or processor who has access to personal data to process those data only on instructions from the controller, unless required by Union or Member State law.

#### Article 30 — Records of processing activities

Requires controllers and processors, and where applicable their representatives, to maintain records of processing activities with specified content.

#### Article 31 — Cooperation with the supervisory authority

Requires the controller and the processor, and where applicable their representatives, to cooperate with the supervisory authority on request in the performance of its tasks.

**Section 2 — Security of personal data**

#### Article 32 — Security of processing

Requires the controller and the processor to implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk.

#### Article 33 — Notification of a personal data breach to the supervisory authority

Requires the controller to notify the supervisory authority of a personal data breach without undue delay and within 72 hours after becoming aware of it, unless the breach is unlikely to risk the rights and freedoms of natural persons.

#### Article 34 — Communication of a personal data breach to the data subject

Requires the controller to communicate a personal data breach to the data subject without undue delay if it is likely to result in a high risk to the rights and freedoms of natural persons.

**Section 3 — Data protection impact assessment and prior consultation**

#### Article 35 — Data protection impact assessment

##### What is it about?

Article 35 establishes the requirement for a data protection impact assessment in specific circumstances involving processing operations likely to result in high risk to the rights and freedoms of natural persons. It defines the scope, content, and procedural steps for such assessments.

##### What does the article require?

- **Paragraph 1** – Where a type of processing, particularly using new technologies and considering nature, scope, context, and purposes, is likely to result in high risk to rights and freedoms of natural persons, the controller shall carry out a data protection impact assessment prior to processing. A single assessment may cover similar processing operations presenting similar high risks.
- **Paragraph 2** – The controller shall seek the advice of the data protection officer, where designated, when carrying out a data protection impact assessment.
- **Paragraph 3** – A data protection impact assessment is required in the case of: (a) systematic and extensive evaluation of personal aspects based on automated processing including profiling, leading to decisions with legal effects or significant impacts; (b) large-scale processing of special categories of data under Article 9(1), or personal data relating to criminal convictions under Article 10; or (c) systematic monitoring of a publicly accessible area on a large scale.
- **Paragraph 4** – The supervisory authority shall establish and make public a list of processing operations subject to the impact assessment requirement. This list shall be communicated to the Board referred to in Article 68.
- **Paragraph 5** – The supervisory authority may establish and make public a list of processing operations for which no impact assessment is required. This list shall be communicated to the Board.
- **Paragraph 6** – Prior to adopting lists under paragraphs 4 and 5, the competent supervisory authority shall apply the consistency mechanism under Article 63 for processing activities related to offering goods/services or monitoring behaviour across several Member States, or affecting the free movement of personal data within the Union.
- **Paragraph 7** – The assessment shall contain at least: (a) systematic description of processing operations and purposes, including legitimate interest; (b) assessment of necessity and proportionality; (c) assessment of risks to rights and freedoms; and (d) measures to address risks, including safeguards and security measures.
- **Paragraph 8** – Compliance with approved codes of conduct under Article 40 shall be taken into account when assessing the impact of processing operations for the purpose of a data protection impact assessment.
- **Paragraph 9** – Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to protection of commercial or public interests or security.
- **Paragraph 10** – Where processing under Article 6(1) points (c) or (e) has a legal basis in Union or Member State law that regulates the specific processing, and a data protection impact assessment has already been carried out as part of a general impact assessment for that legal basis, paragraphs 1 to 7 do not apply unless Member States deem it necessary to carry out such an assessment prior to processing.
- **Paragraph 11** – The controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change in the risk represented by processing operations.

##### Who is affected?

The controller is directly affected by the requirement to carry out a data protection impact assessment. The data protection officer, where designated, is affected by the requirement to be consulted under paragraph 2. The supervisory authority is affected by the requirements to establish and communicate lists under paragraphs 4, 5, and 6. The Board referred to in Article 68 is affected by the requirement to receive lists under paragraphs 4 and 5.

##### What is not specified?

The article does not specify the exact format or duration of the data protection impact assessment. It does not define the threshold for "high risk" beyond the circumstances listed in paragraph 3. It does not specify how to determine "necessity and proportionality" in paragraph 7(b). It does not detail the content of "approved codes of conduct" under Article 40 that would be taken into account under paragraph 8. It does not specify the criteria for when Member States deem it necessary to carry out an assessment under paragraph 10.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Check new AI systems against paragraph 3 and the national lists under paragraph 4; profiling with significant effects and large-scale processing of special categories regularly require an assessment.
- Carry out the assessment before processing starts, involve the data protection officer, and document the content required by paragraph 7.
- Review the assessment when the risk changes, e.g. after retraining a model on new data or extending it to new purposes.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 36 — Prior consultation

Requires the controller to consult the supervisory authority prior to processing when a data protection impact assessment indicates a high risk that remains after risk mitigation measures are taken.

**Section 4 — Data protection officer**

#### Article 37 — Designation of the data protection officer

Requires the controller and the processor to designate a data protection officer in cases where processing is carried out by a public authority or body, or involves large-scale monitoring or processing of special categories of data.

#### Article 38 — Position of the data protection officer

Requires the controller and the processor to ensure the data protection officer is involved in all issues relating to the protection of personal data and is supported with necessary resources and access.

#### Article 39 — Tasks of the data protection officer

Requires the data protection officer to inform, advise, monitor compliance, provide advice on data protection impact assessments, cooperate with the supervisory authority, and act as a contact point for the supervisory authority.

**Section 5 — Codes of conduct and certification**

#### Article 40 — Codes of conduct

Encourages the drawing up of codes of conduct to contribute to the proper application of this Regulation, taking account of the specific features of the various processing sectors and the specific needs of micro, small and medium-sized enterprises.

#### Article 41 — Monitoring of approved codes of conduct

Allows compliance with approved codes of conduct to be monitored by bodies accredited for this purpose by the competent supervisory authority.

#### Article 42 — Certification

Encourages the establishment of data protection certification mechanisms, seals, and marks to demonstrate compliance with this Regulation by controllers and processors.

#### Article 43 — Certification bodies

Requires certification bodies with data protection expertise to issue and renew certification after informing the supervisory authority and being accredited by the competent authority or national accreditation body.

### Chapter V — Transfers of personal data to third countries or international organisations

#### Article 44 — General principle for transfers

Requires transfers of personal data to third countries or international organisations to comply with the conditions laid down in this Chapter to ensure the level of protection of natural persons is not undermined.

#### Article 45 — Transfers on the basis of an adequacy decision

Allows transfers of personal data to third countries or international organisations where the Commission has decided that an adequate level of protection is ensured.

#### Article 46 — Transfers subject to appropriate safeguards

##### What is it about?

Article 46 establishes the conditions under which a controller or processor may transfer personal data to a third country or an international organisation. It requires appropriate safeguards to ensure enforceable data subject rights and effective legal remedies are available for such transfers, without relying on a decision under Article 45(3).

##### What does the article require?

- **Paragraph 1** – In the absence of an adequacy decision under Article 45(3), a controller or processor may transfer personal data to a third country or international organisation only if appropriate safeguards are provided, and enforceable data subject rights and effective legal remedies are available.
- **Paragraph 2** – The appropriate safeguards may be provided without requiring specific authorisation from a supervisory authority by: (a) a legally binding and enforceable instrument between public authorities or bodies; (b) binding corporate rules under Article 47; (c) standard data protection clauses adopted by the Commission under Article 93(2); (d) standard data protection clauses adopted by a supervisory authority and approved by the Commission under Article 93(2); (e) an approved code of conduct under Article 40 with binding commitments from the controller or processor in the third country; or (f) an approved certification mechanism under Article 42 with binding commitments from the controller or processor in the third country.
- **Paragraph 3** – Subject to authorisation from the competent supervisory authority, appropriate safeguards may also be provided by: (a) contractual clauses between the controller or processor and the recipient in the third country or international organisation; or (b) provisions in administrative arrangements between public authorities or bodies that include enforceable and effective data subject rights.
- **Paragraph 4** – The supervisory authority shall apply the consistency mechanism under Article 63 for cases referred to in paragraph 3.
- **Paragraph 5** – Authorisations under Article 26(2) of Directive 95/46/EC remain valid until amended, replaced, or repealed by the supervisory authority. Decisions under Article 26(4) of Directive 95/46/EC remain in force until amended, replaced, or repealed by a Commission Decision under paragraph 2 of this Article.

##### Who is affected?

Controllers and processors are affected by the requirements in paragraphs 1, 2, and 3. Supervisory authorities are affected by the requirements in paragraphs 3 and 4 regarding authorisation and the consistency mechanism. Under paragraph 5, earlier authorisations and Commission decisions under Directive 95/46/EC remain valid until amended, replaced or repealed.

##### What is not specified?

The article does not specify the exact nature or form of "appropriate safeguards" beyond the listed mechanisms. It does not define "enforceable data subject rights" or "effective legal remedies." It does not specify the criteria for supervisory authority authorisation under paragraph 3. It does not detail how supervisory authorities must apply the consistency mechanism under Article 63 for paragraph 3 cases.

##### What could this mean in practice?

**Possible implementation – not a legally prescribed checklist:**

- Before using AI services or APIs hosted outside the EU, check whether personal data are transferred and whether an adequacy decision exists.
- Without an adequacy decision, use one of the safeguards of paragraph 2, typically the Commission's standard data protection clauses, and keep them up to date.
- Check whether the recipient's commitments make data subject rights enforceable in practice.

##### When does it apply?

Applies from **25 May 2018** (Art. 99(2)).

#### Article 47 — Binding corporate rules

Requires the competent supervisory authority to approve binding corporate rules that meet the specified requirements and sets out their minimum content.

#### Article 48 — Transfers or disclosures not authorised by Union law

Provides that a third-country court judgment or administrative decision requiring the transfer or disclosure of personal data is only recognised or enforceable if based on an international agreement such as a mutual legal assistance treaty.

#### Article 49 — Derogations for specific situations

Allows transfers without an adequacy decision or appropriate safeguards only in specific situations, such as explicit consent of the data subject or necessity for the performance of a contract.

#### Article 50 — International cooperation for the protection of personal data

Promotes international cooperation mechanisms and mutual assistance in enforcing personal data protection legislation, involving relevant stakeholders and ensuring safeguards for fundamental rights.

### Chapter VI — Independent supervisory authorities

**Section 1 — Independent status**

#### Article 51 — Supervisory authority

Requires each Member State to provide for one or more independent public authorities responsible for monitoring the application of the Regulation.

#### Article 52 — Independence

Ensures that each supervisory authority acts with complete independence in performing its tasks and exercising its powers in accordance with this Regulation.

#### Article 53 — General conditions for the members of the supervisory authority

Requires Member States to appoint the members of their supervisory authorities by a transparent procedure, through their parliament, government, head of state or an independent body.

#### Article 54 — Rules on the establishment of the supervisory authority

Establishes rules on the establishment of each supervisory authority, including its composition, term of office, reappointment, and obligations of its members and staff.

**Section 2 — Competence, tasks and powers**

#### Article 55 — Competence

Determines the competence of supervisory authorities to perform tasks and exercise powers within their Member State's territory.

#### Article 56 — Competence of the lead supervisory authority

Designates the supervisory authority of the main or single establishment as competent to act as lead supervisory authority for cross-border processing.

#### Article 57 — Tasks

Requires supervisory authorities to monitor and enforce the application of this Regulation and promote public awareness of data protection rules and rights.

#### Article 58 — Powers

Sets out the investigative, corrective, authorisation and advisory powers of each supervisory authority, including the information it may require, the access it may obtain, and the actions it may take against controllers and processors.

#### Article 59 — Activity reports

Requires supervisory authorities to draw up annual reports on their activities, which may include lists of infringements and measures taken, and to transmit them to designated authorities and make them publicly available.

### Chapter VII — Cooperation and consistency

**Section 1 — Cooperation**

#### Article 60 — Cooperation between the lead supervisory authority and the other supervisory authorities concerned

Requires the lead supervisory authority to cooperate with the other supervisory authorities concerned, to exchange all relevant information with them and to endeavour to reach consensus.

#### Article 61 — Mutual assistance

Requires supervisory authorities to provide each other with relevant information and mutual assistance to implement and apply the Regulation consistently.

#### Article 62 — Joint operations of supervisory authorities

Provides for joint operations of supervisory authorities, including joint investigations and joint enforcement measures with members or staff of the authorities of other Member States.

**Section 2 — Consistency**

#### Article 63 — Consistency mechanism

Requires supervisory authorities to cooperate with each other and, where relevant, with the Commission through the consistency mechanism in order to ensure consistent application of this Regulation throughout the Union.

#### Article 64 — Opinion of the Board

Requires the competent supervisory authority to communicate a draft decision to the Board when aiming to adopt specific measures related to data protection impact assessments, codes of conduct, accreditation requirements, standard data protection clauses, contractual clauses, or binding corporate rules.

#### Article 65 — Dispute resolution by the Board

Requires the Board to adopt a binding decision in cases of objections to draft decisions, disputes over competence, or non-compliance with its opinions, and sets the procedure for adopting and communicating such decisions.

#### Article 66 — Urgency procedure

Allows a supervisory authority to adopt provisional measures immediately in exceptional circumstances to protect data subjects' rights and freedoms, specifying a validity period not exceeding three months.

#### Article 67 — Exchange of information

Allows the Commission to adopt implementing acts specifying the arrangements for the electronic exchange of information between supervisory authorities and with the Board.

**Section 3 — European data protection board**

#### Article 68 — European Data Protection Board

Establishes the European Data Protection Board as a Union body with legal personality, composed of the heads of each Member State's supervisory authority and the European Data Protection Supervisor.

#### Article 69 — Independence

Requires the Board to act independently when performing its tasks or exercising its powers and not to seek or take instructions from anybody.

#### Article 70 — Tasks of the Board

Sets out the tasks of the Board for ensuring the consistent application of the Regulation, including monitoring, advising the Commission and issuing guidelines, recommendations and best practices.

#### Article 71 — Reports

Requires the Board to draw up and make public an annual report on the protection of natural persons regarding processing in the Union and, where relevant, in third countries and international organisations.

#### Article 72 — Procedure

Provides that the Board takes decisions by a simple majority of its members unless otherwise provided and adopts its rules of procedure by a two-thirds majority.

#### Article 73 — Chair

Requires the Board to elect a chair and two deputy chairs from among its members by simple majority, for a term of five years renewable once.

#### Article 74 — Tasks of the Chair

Sets out the tasks of the Chair, including convening meetings of the Board, notifying decisions to supervisory authorities, and ensuring timely performance of the Board's tasks.

#### Article 75 — Secretariat

Provides the Board with a secretariat managed by the European Data Protection Supervisor, responsible for administrative, logistical, and analytical support to the Board.

#### Article 76 — Confidentiality

Provides that the discussions of the Board are confidential where the Board deems it necessary, as provided for in its rules of procedure.

### Chapter VIII — Remedies, liability and penalties

#### Article 77 — Right to lodge a complaint with a supervisory authority

Gives the data subject the right to lodge a complaint with a supervisory authority if the data subject considers that the processing of personal data relating to him or her infringes this Regulation.

#### Article 78 — Right to an effective judicial remedy against a supervisory authority

Gives every natural or legal person the right to an effective judicial remedy against a legally binding decision of a supervisory authority, and data subjects a remedy where the authority does not handle their complaint or inform them within three months.

#### Article 79 — Right to an effective judicial remedy against a controller or processor

Gives the data subject the right to an effective judicial remedy against a controller or processor when their rights under this Regulation have been infringed due to non-compliant processing of personal data.

#### Article 80 — Representation of data subjects

Gives the data subject the right to mandate a not-for-profit body to lodge a complaint and exercise certain rights on his or her behalf.

#### Article 81 — Suspension of proceedings

Allows a court to suspend its proceedings where proceedings concerning the same subject matter and the same controller or processor are pending in a court of another Member State.

#### Article 82 — Right to compensation and liability

Gives any person who has suffered material or non-material damage as a result of an infringement of the Regulation the right to compensation from the controller or processor.

#### Article 83 — General conditions for imposing administrative fines

Sets out the conditions for imposing administrative fines, including the factors to be taken into account and maximum amounts of up to EUR 20 million or 4 % of total worldwide annual turnover.

#### Article 84 — Penalties

Requires Member States to establish effective, proportionate and dissuasive penalties for infringements not subject to administrative fines and to notify such provisions to the Commission by 25 May 2018 and any subsequent amendments.

### Chapter IX — Provisions relating to specific processing situations

#### Article 85 — Processing and freedom of expression and information

Requires Member States to reconcile data protection with freedom of expression and information through legal provisions allowing exemptions for journalistic, academic, artistic, or literary processing.

#### Article 86 — Processing and public access to official documents

Allows personal data in official documents held by public authorities or bodies, or by private bodies performing public interest tasks, to be disclosed under Union or Member State law to reconcile public access with data protection.

#### Article 87 — Processing of the national identification number

Permits Member States to establish specific conditions for processing a national identification number, which may only be used under appropriate safeguards for the data subject's rights and freedoms.

#### Article 88 — Processing in the context of employment

Permits Member States to establish more specific rules for processing employees' personal data in employment contexts, including recruitment, contract performance, and workplace management, while ensuring safeguards for data subjects' rights and dignity.

#### Article 89 — Safeguards and derogations relating to processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes

Requires appropriate safeguards for processing for archiving, scientific or historical research or statistical purposes and allows Union or Member State law to provide for derogations from certain data subject rights.

#### Article 90 — Obligations of secrecy

Allows Member States to adopt specific rules on the powers of supervisory authorities in relation to controllers or processors subject to professional secrecy, where necessary to reconcile data protection with that obligation.

#### Article 91 — Existing data protection rules of churches and religious associations

Allows churches and religious associations to continue to apply comprehensive data protection rules applied when the Regulation entered into force if they are brought into line with the Regulation and subject to an independent supervisory authority.

### Chapter X — Delegated acts and implementing acts

#### Article 92 — Exercise of the delegation

Sets out the conditions under which the Commission exercises the power to adopt delegated acts, including revocation by the European Parliament or the Council and the objection procedure.

#### Article 93 — Committee procedure

Provides that the Commission is assisted by a committee within the meaning of Regulation (EU) No 182/2011.

### Chapter XI — Final provisions

#### Article 94 — Repeal of Directive 95/46/EC

Repeals Directive 95/46/EC with effect from 25 May 2018 and replaces references to it with references to this Regulation.

#### Article 95 — Relationship with Directive 2002/58/EC

Provides that the Regulation imposes no additional obligations on providers of publicly available electronic communications services where Directive 2002/58/EC sets specific obligations with the same objective.

#### Article 96 — Relationship with previously concluded Agreements

Permits international agreements involving personal data transfers to third countries or international organisations, concluded by Member States before 24 May 2016 and compliant with Union law as applicable then, to remain in force until amended, replaced or revoked.

#### Article 97 — Commission reports

Requires the Commission to submit reports on the evaluation and review of this Regulation to the European Parliament and the Council by 25 May 2020 and every four years thereafter.

#### Article 98 — Review of other Union legal acts on data protection

Requires the Commission to submit legislative proposals to amend other Union legal acts on data protection to ensure uniform and consistent protection of natural persons regarding processing.

#### Article 99 — Entry into force and application

Provides that the Regulation enters into force on the twentieth day following its publication and applies from 25 May 2018.

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

## DE

> **Wichtiger Hinweis:** Diese Seite ist eine LLM-generierte Zusammenfassung. Sie kann unvollständig, veraltet oder falsch sein. Sie ist keine Rechtsberatung und entfaltet keine rechtliche Wirkung; verbindlich sind allein die im Amtsblatt der Europäischen Union veröffentlichten Texte.

### TL;DR

Die Datenschutz-Grundverordnung (DSGVO) ist das zentrale Gesetz der EU für die Verarbeitung personenbezogener Daten. Sie legt fest, wann eine Verarbeitung rechtmäßig ist, welche Grundsätze jede Verarbeitung einhalten muss, welche Rechte betroffene Personen haben und welche Pflichten Verantwortliche und Auftragsverarbeiter tragen. Sie gilt für Organisationen in der EU und für Organisationen außerhalb der EU, die Personen in der EU Waren oder Dienstleistungen anbieten oder ihr Verhalten beobachten. Unabhängige Aufsichtsbehörden setzen sie durch, mit Geldbußen von bis zu 20 Millionen Euro oder 4 % des weltweiten Jahresumsatzes.

### Eckdaten

| | |
| --- | --- |
| Fundstelle | Verordnung (EU) 2016/679, ABl. L 119 vom 4.5.2016 |
| Art und Geltung | EU-Verordnung, unmittelbar in allen Mitgliedstaaten anwendbar |
| Erlassen | 27. April 2016 |
| Inkrafttreten | 24. Mai 2016 |
| Geltungsbeginn | 25. Mai 2018 |
| Änderungen | keine, nur Berichtigungen. Die Kommission hat 2025 Änderungen vorgeschlagen (COM(2025) 501 und COM(2025) 837) |
| Zuständige Behörden | nationale Aufsichtsbehörden; der Europäische Datenschutzausschuss für die einheitliche Anwendung |
| Zusammengefasste Fassung | konsolidierte Fassung vom 4. Mai 2016 |

### Anwendungsbereich

**Sachlicher Anwendungsbereich** (Art. 2): ganz oder teilweise automatisierte Verarbeitung personenbezogener Daten sowie nichtautomatisierte Verarbeitung personenbezogener Daten, die in einem Dateisystem gespeichert sind oder gespeichert werden sollen. Personenbezogene Daten sind alle Informationen, die sich auf eine identifizierte oder identifizierbare natürliche Person beziehen (Art. 4 Nr. 1).

**Räumlicher Anwendungsbereich** (Art. 3): Verarbeitung im Rahmen der Tätigkeiten einer Niederlassung eines Verantwortlichen oder Auftragsverarbeiters in der EU, unabhängig davon, wo die Verarbeitung stattfindet; außerdem Verarbeitung von Daten von Personen in der EU durch Verantwortliche oder Auftragsverarbeiter außerhalb der EU, wenn sie diesen Personen Waren oder Dienstleistungen anbieten oder ihr Verhalten in der EU beobachten.

**Ausnahmen** (Art. 2 Abs. 2): Tätigkeiten außerhalb des Unionsrechts, die Gemeinsame Außen- und Sicherheitspolitik, ausschließlich persönliche oder familiäre Tätigkeiten sowie die Verarbeitung durch zuständige Behörden zur Strafverfolgung, für die die Richtlinie (EU) 2016/680 gilt.

**Zentrale Rollen**: Der *Verantwortliche* entscheidet über Zwecke und Mittel der Verarbeitung; der *Auftragsverarbeiter* verarbeitet Daten im Auftrag des Verantwortlichen; die *betroffene Person* ist die Person, auf die sich die Daten beziehen.

### Kapitel I – Allgemeine Bestimmungen

#### Artikel 1 – Gegenstand und Ziele

Legt Vorschriften zum Schutz natürlicher Personen bei der Verarbeitung personenbezogener Daten und zum freien Verkehr solcher Daten fest.

#### Artikel 2 – Sachlicher Anwendungsbereich

Erfasst die ganz oder teilweise automatisierte Verarbeitung personenbezogener Daten und die Verarbeitung in Dateisystemen und nimmt bestimmte Verarbeitungen aus.

#### Artikel 3 – Räumlicher Anwendungsbereich

Erstreckt die Verordnung auf Verarbeitungen im Rahmen einer Niederlassung in der Union sowie auf Verantwortliche und Auftragsverarbeiter außerhalb der Union, die Personen in der Union Waren oder Dienstleistungen anbieten oder ihr Verhalten beobachten.

#### Artikel 4 – Begriffsbestimmungen

Bestimmt die zentralen Begriffe der Verordnung, darunter personenbezogene Daten, Verarbeitung, Profiling, Pseudonymisierung, Verantwortlicher, Auftragsverarbeiter, Einwilligung, Verletzung des Schutzes personenbezogener Daten sowie genetische, biometrische und Gesundheitsdaten.

### Kapitel II – Grundsätze

#### Artikel 5 – Grundsätze für die Verarbeitung personenbezogener Daten

##### Worum geht es?

Artikel 5 legt die Grundsätze fest, die jede Verarbeitung personenbezogener Daten einhalten muss: Rechtmäßigkeit, Verarbeitung nach Treu und Glauben, Transparenz, Zweckbindung, Datenminimierung, Richtigkeit, Speicherbegrenzung sowie Integrität und Vertraulichkeit. Außerdem begründet er die Rechenschaftspflicht des Verantwortlichen.

##### Was verlangt der Artikel?

- **Absatz 1** – Personenbezogene Daten müssen
  - a) auf rechtmäßige Weise, nach Treu und Glauben und in einer für die betroffene Person nachvollziehbaren Weise verarbeitet werden (*Rechtmäßigkeit, Verarbeitung nach Treu und Glauben, Transparenz*);
  - b) für festgelegte, eindeutige und legitime Zwecke erhoben und nicht in einer damit unvereinbaren Weise weiterverarbeitet werden; eine Weiterverarbeitung für im öffentlichen Interesse liegende Archivzwecke, wissenschaftliche oder historische Forschungszwecke oder statistische Zwecke gilt nach Artikel 89 Absatz 1 nicht als unvereinbar (*Zweckbindung*);
  - c) dem Zweck angemessen und erheblich sowie auf das notwendige Maß beschränkt sein (*Datenminimierung*);
  - d) sachlich richtig und erforderlichenfalls auf dem neuesten Stand sein; unrichtige Daten sind unverzüglich zu löschen oder zu berichtigen (*Richtigkeit*);
  - e) nur so lange in identifizierbarer Form gespeichert werden, wie es für die Zwecke erforderlich ist; für die Zwecke nach Artikel 89 Absatz 1 ist mit geeigneten Garantien eine längere Speicherung möglich (*Speicherbegrenzung*);
  - f) mit angemessener Sicherheit verarbeitet werden, einschließlich Schutz vor unbefugter oder unrechtmäßiger Verarbeitung und vor unbeabsichtigtem Verlust, unbeabsichtigter Zerstörung oder Schädigung (*Integrität und Vertraulichkeit*).
- **Absatz 2** – Der Verantwortliche ist für die Einhaltung des Absatzes 1 verantwortlich und muss sie nachweisen können (*Rechenschaftspflicht*).

##### Wer ist betroffen?

Jeder Verantwortliche, bei jeder Verarbeitung personenbezogener Daten. Auftragsverarbeiter sind mittelbar über ihre Verträge und ihre eigenen Pflichten aus der Verordnung gebunden.

##### Was ist nicht ausdrücklich geregelt?

- Wie die Einhaltung nach Absatz 2 im Einzelnen nachzuweisen ist.
- Was „nach Treu und Glauben“ im konkreten Fall bedeutet; die Rechtsgrundlagen für die Rechtmäßigkeit stehen in Artikel 6.
- Welche technischen und organisatorischen Maßnahmen für die Sicherheit nach Buchstabe f geeignet sind.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Den Zweck jedes Trainings- oder Fine-Tuning-Datensatzes vor der Erhebung festlegen und dokumentieren; vor der Weiterverwendung von Daten, die zu anderen Zwecken erhoben wurden, die Vereinbarkeit prüfen (Zweckbindung).
- Felder entfernen, die das Modell nicht braucht, und anonymisierte oder pseudonymisierte Daten bevorzugen (Datenminimierung).
- Speicherfristen für Trainingsdaten, Logs und Prompts festlegen und Daten nach Ablauf löschen (Speicherbegrenzung).
- Nachweise darüber führen, wie jeder Grundsatz eingehalten wird, da der Verantwortliche die Einhaltung belegen können muss (Rechenschaftspflicht).

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 6 – Rechtmäßigkeit der Verarbeitung

##### Worum geht es?

Artikel 6 bestimmt, wann eine Verarbeitung personenbezogener Daten rechtmäßig ist. Er nennt die Rechtsgrundlagen (Einwilligung, Vertrag, rechtliche Verpflichtung, lebenswichtige Interessen, öffentliches Interesse, berechtigte Interessen), regelt die Anforderungen an Rechtsgrundlagen im Unionsrecht und im Recht der Mitgliedstaaten und legt fest, wie die Vereinbarkeit einer Weiterverarbeitung zu prüfen ist.

##### Was verlangt der Artikel?

- **Absatz 1** – Die Verarbeitung ist nur rechtmäßig, wenn mindestens eine der folgenden Bedingungen erfüllt ist:
  - a) die betroffene Person hat eingewilligt;
  - b) die Verarbeitung ist für die Erfüllung eines Vertrags oder vorvertragliche Maßnahmen erforderlich;
  - c) sie ist zur Erfüllung einer rechtlichen Verpflichtung des Verantwortlichen erforderlich;
  - d) sie ist erforderlich, um lebenswichtige Interessen zu schützen;
  - e) sie ist für eine Aufgabe im öffentlichen Interesse oder in Ausübung öffentlicher Gewalt erforderlich;
  - f) sie ist zur Wahrung der berechtigten Interessen des Verantwortlichen oder eines Dritten erforderlich, sofern nicht die Interessen oder Grundrechte der betroffenen Person überwiegen, insbesondere wenn es sich um ein Kind handelt.

  Buchstabe f gilt nicht für die von Behörden in Erfüllung ihrer Aufgaben vorgenommene Verarbeitung.
- **Absatz 2** – Die Mitgliedstaaten können spezifischere Bestimmungen für Verarbeitungen nach Absatz 1 Buchstaben c und e beibehalten oder einführen.
- **Absatz 3** – Die Rechtsgrundlage für Verarbeitungen nach Absatz 1 Buchstaben c und e wird durch Unionsrecht oder das Recht der Mitgliedstaaten festgelegt. Sie muss ein im öffentlichen Interesse liegendes Ziel verfolgen und verhältnismäßig sein; sie kann spezifische Bestimmungen etwa zu Datenarten, betroffenen Personen, Empfängern, Zweckbindung und Speicherfristen enthalten.
- **Absatz 4** – Beruht eine Weiterverarbeitung zu einem anderen Zweck weder auf einer Einwilligung noch auf einer Rechtsvorschrift im Sinne des Artikels 23 Absatz 1, prüft der Verantwortliche die Vereinbarkeit der Zwecke, unter anderem anhand
  - a) der Verbindung zwischen den Zwecken,
  - b) des Zusammenhangs, in dem die Daten erhoben wurden,
  - c) der Art der Daten, insbesondere besonderer Kategorien nach Artikel 9 oder Daten über Straftaten nach Artikel 10,
  - d) der möglichen Folgen für die betroffenen Personen und
  - e) des Vorhandenseins geeigneter Garantien wie Verschlüsselung oder Pseudonymisierung.

##### Wer ist betroffen?

Jeder Verantwortliche, der personenbezogene Daten verarbeitet. Die Mitgliedstaaten können nach den Absätzen 2 und 3 Rechtsgrundlagen schaffen. Behörden können sich bei der Erfüllung ihrer Aufgaben nicht auf Absatz 1 Buchstabe f stützen.

##### Was ist nicht ausdrücklich geregelt?

- Wann eine Verarbeitung im Einzelfall „erforderlich“ ist.
- Wie die Interessenabwägung nach Absatz 1 Buchstabe f vorzunehmen ist.
- Wie die Verhältnismäßigkeit einer Rechtsgrundlage nach Absatz 3 zu beurteilen ist.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Für jeden Verarbeitungszweck vor Beginn eine Rechtsgrundlage wählen und dokumentieren, etwa getrennt für den Betrieb eines Dienstes und für das Training von Modellen mit dessen Daten.
- Wenn das Training auf berechtigte Interessen (Buchstabe f) gestützt wird, die Interessenabwägung dokumentieren, einschließlich der vernünftigen Erwartungen der betroffenen Personen.
- Vor der Weiterverwendung von Daten für einen neuen Zweck wie Modelltraining die Vereinbarkeitsprüfung nach Absatz 4 durchführen und Garantien wie Pseudonymisierung vorsehen.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 7 – Bedingungen für die Einwilligung

Verpflichtet den Verantwortlichen nachzuweisen, dass die betroffene Person in die Verarbeitung ihrer personenbezogenen Daten eingewilligt hat.

#### Artikel 8 – Bedingungen für die Einwilligung eines Kindes in Bezug auf Dienste der Informationsgesellschaft

Regelt die Einwilligung eines Kindes bei Diensten der Informationsgesellschaft; unter 16 Jahren, von den Mitgliedstaaten absenkbar bis auf 13 Jahre, muss der Träger der elterlichen Verantwortung einwilligen oder zustimmen.

#### Artikel 9 – Verarbeitung besonderer Kategorien personenbezogener Daten

##### Worum geht es?

Artikel 9 verbietet grundsätzlich die Verarbeitung besonderer Kategorien personenbezogener Daten, etwa zur ethnischen Herkunft, zu Gesundheit oder Sexualleben, und nennt die Ausnahmen von diesem Verbot.

##### Was verlangt der Artikel?

- **Absatz 1** – Untersagt ist die Verarbeitung personenbezogener Daten, aus denen die rassische und ethnische Herkunft, politische Meinungen, religiöse oder weltanschauliche Überzeugungen oder die Gewerkschaftszugehörigkeit hervorgehen, sowie die Verarbeitung von genetischen Daten, biometrischen Daten zur eindeutigen Identifizierung einer natürlichen Person, Gesundheitsdaten oder Daten zum Sexualleben oder der sexuellen Orientierung.
- **Absatz 2** – Das Verbot gilt nicht, wenn unter anderem
  - a) die betroffene Person ausdrücklich eingewilligt hat;
  - b) die Verarbeitung für Rechte und Pflichten aus dem Arbeitsrecht und dem Recht der sozialen Sicherheit und des Sozialschutzes erforderlich ist;
  - c) sie zum Schutz lebenswichtiger Interessen erforderlich ist und die betroffene Person nicht einwilligen kann;
  - d) eine politisch, weltanschaulich, religiös oder gewerkschaftlich ausgerichtete Organisation ohne Gewinnerzielungsabsicht mit geeigneten Garantien Daten ihrer Mitglieder oder regelmäßiger Kontaktpersonen verarbeitet;
  - e) die betroffene Person die Daten offensichtlich öffentlich gemacht hat;
  - f) die Verarbeitung zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen oder bei justizieller Tätigkeit der Gerichte erforderlich ist;
  - g) sie aus Gründen eines erheblichen öffentlichen Interesses auf Grundlage einer verhältnismäßigen Rechtsvorschrift mit Schutzmaßnahmen erforderlich ist;
  - h) sie für Gesundheitsvorsorge, Arbeitsmedizin, medizinische Diagnostik oder Versorgung auf gesetzlicher oder vertraglicher Grundlage erforderlich ist;
  - i) sie aus Gründen des öffentlichen Interesses im Bereich der öffentlichen Gesundheit auf gesetzlicher Grundlage erforderlich ist;
  - j) sie für Archiv-, Forschungs- oder Statistikzwecke nach Artikel 89 Absatz 1 auf gesetzlicher Grundlage erforderlich ist.
- **Absatz 3** – Für Zwecke nach Absatz 2 Buchstabe h dürfen die Daten von Fachpersonal oder unter dessen Verantwortung verarbeitet werden, das einem Berufsgeheimnis oder einer Geheimhaltungspflicht unterliegt.
- **Absatz 4** – Die Mitgliedstaaten können für genetische, biometrische und Gesundheitsdaten zusätzliche Bedingungen einschließlich Beschränkungen einführen oder aufrechterhalten.

##### Wer ist betroffen?

Alle Verantwortlichen, die besondere Kategorien personenbezogener Daten verarbeiten. Die Mitgliedstaaten können nach Absatz 2 Buchstaben b, g, h, i und j sowie Absatz 4 Rechtsgrundlagen und weitere Bedingungen schaffen; in Deutschland etwa in §§ 22, 26 und 27 BDSG.

##### Was ist nicht ausdrücklich geregelt?

- Was eine „ausdrückliche“ Einwilligung von einer einfachen Einwilligung unterscheidet.
- Welche „geeigneten Garantien“ im Einzelnen erforderlich sind.
- Wann ein „erhebliches öffentliches Interesse“ nach Buchstabe g vorliegt.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Trainings- und Evaluationsdatensätze auf besondere Kategorien prüfen, auch auf Daten, aus denen sich solche Merkmale ableiten lassen, etwa Gesundheit oder ethnische Herkunft.
- Biometrische Daten zur eindeutigen Identifizierung, etwa für Gesichtserkennung, nur unter einer der Ausnahmen des Absatzes 2 verarbeiten.
- Wenn besondere Kategorien für die Erkennung von Bias benötigt werden, die genutzte Ausnahme festhalten; für Hochrisiko-KI-Systeme sieht Art. 4a AI Act eine eigene Grundlage vor.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 10 – Verarbeitung von personenbezogenen Daten über strafrechtliche Verurteilungen und Straftaten

Erlaubt die Verarbeitung von Daten über strafrechtliche Verurteilungen und Straftaten nur unter behördlicher Aufsicht oder wenn das Unionsrecht oder mitgliedstaatliche Recht sie mit geeigneten Garantien zulässt.

#### Artikel 11 – Verarbeitung, für die eine Identifizierung der betroffenen Person nicht erforderlich ist

Befreit den Verantwortlichen von der Pflicht, zusätzliche Informationen zur Identifizierung der betroffenen Person aufzubewahren, einzuholen oder zu verarbeiten, wenn der Zweck keine Identifizierung erfordert.

### Kapitel III – Rechte der betroffenen Person

**Abschnitt 1 – Transparenz und Modalitäten**

#### Artikel 12 – Transparente Information, Kommunikation und Modalitäten für die Ausübung der Rechte der betroffenen Person

Verpflichtet den Verantwortlichen, Informationen und Mitteilungen in präziser, transparenter, verständlicher und leicht zugänglicher Form in einer klaren und einfachen Sprache zu übermitteln.

**Abschnitt 2 – Informationspflicht und Recht auf Auskunft zu personenbezogenen Daten**

#### Artikel 13 – Informationspflicht bei Erhebung von personenbezogenen Daten bei der betroffenen Person

Verpflichtet den Verantwortlichen, der betroffenen Person bei der Erhebung ihrer Daten bestimmte Informationen zu geben, darunter seine Identität, Zwecke und Rechtsgrundlage der Verarbeitung und ihre Rechte.

#### Artikel 14 – Informationspflicht, wenn die personenbezogenen Daten nicht bei der betroffenen Person erhoben wurden

Verpflichtet den Verantwortlichen, der betroffenen Person bestimmte Informationen zu geben, wenn die Daten nicht bei ihr erhoben wurden, darunter seine Identität, die Zwecke, die Datenkategorien und die Quelle.

#### Artikel 15 – Auskunftsrecht der betroffenen Person

Gibt der betroffenen Person das Recht auf Bestätigung, ob sie betreffende personenbezogene Daten verarbeitet werden, und auf Auskunft über diese Daten und weitere Informationen.

**Abschnitt 3 – Berichtigung und Löschung**

#### Artikel 16 – Recht auf Berichtigung

Gibt der betroffenen Person das Recht, vom Verantwortlichen unverzüglich die Berichtigung sie betreffender unrichtiger personenbezogener Daten zu verlangen.

#### Artikel 17 – Recht auf Löschung („Recht auf Vergessenwerden“)

##### Worum geht es?

Artikel 17 gibt der betroffenen Person das Recht, die unverzügliche Löschung ihrer personenbezogenen Daten zu verlangen, und verpflichtet den Verantwortlichen zur Löschung, wenn einer der genannten Gründe vorliegt („Recht auf Vergessenwerden“). Er regelt außerdem Pflichten bei veröffentlichten Daten und die Ausnahmen vom Löschungsrecht.

##### Was verlangt der Artikel?

- **Absatz 1** – Die betroffene Person kann die unverzügliche Löschung verlangen, und der Verantwortliche muss unverzüglich löschen, wenn
  - a) die Daten für die Zwecke nicht mehr notwendig sind;
  - b) die betroffene Person ihre Einwilligung nach Artikel 6 Absatz 1 Buchstabe a oder Artikel 9 Absatz 2 Buchstabe a widerruft und keine andere Rechtsgrundlage besteht;
  - c) sie nach Artikel 21 Absatz 1 widerspricht und keine vorrangigen berechtigten Gründe vorliegen, oder nach Artikel 21 Absatz 2 gegen Direktwerbung widerspricht;
  - d) die Daten unrechtmäßig verarbeitet wurden;
  - e) die Löschung zur Erfüllung einer rechtlichen Verpflichtung erforderlich ist;
  - f) die Daten in Bezug auf angebotene Dienste der Informationsgesellschaft nach Artikel 8 Absatz 1 erhoben wurden.
- **Absatz 2** – Hat der Verantwortliche die Daten öffentlich gemacht und ist er zur Löschung verpflichtet, trifft er unter Berücksichtigung der verfügbaren Technologie und der Implementierungskosten angemessene Maßnahmen, auch technischer Art, um andere Verantwortliche, die die Daten verarbeiten, darüber zu informieren, dass die betroffene Person die Löschung aller Links, Kopien oder Replikationen verlangt hat.
- **Absatz 3** – Die Absätze 1 und 2 gelten nicht, soweit die Verarbeitung erforderlich ist
  - a) zur Ausübung des Rechts auf freie Meinungsäußerung und Information;
  - b) zur Erfüllung einer rechtlichen Verpflichtung oder einer Aufgabe im öffentlichen Interesse oder in Ausübung öffentlicher Gewalt;
  - c) aus Gründen des öffentlichen Interesses im Bereich der öffentlichen Gesundheit;
  - d) für Archiv-, Forschungs- oder Statistikzwecke nach Artikel 89 Absatz 1, soweit die Löschung diese Zwecke unmöglich machen oder ernsthaft beeinträchtigen würde;
  - e) zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen.

##### Wer ist betroffen?

Die betroffene Person als Inhaberin des Rechts und der Verantwortliche als Verpflichteter. Andere Verantwortliche, die vom Verantwortlichen veröffentlichte Daten verarbeiten, sind nach Absatz 2 zu informieren; der Artikel verpflichtet sie nicht selbst zur Löschung.

##### Was ist nicht ausdrücklich geregelt?

- Was „unverzüglich“ im Einzelfall bedeutet.
- Welche Maßnahmen nach Absatz 2 „angemessen“ sind.
- Wann „vorrangige berechtigte Gründe“ nach Absatz 1 Buchstabe c vorliegen.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Einen Prozess einrichten, um Löschanträge entgegenzunehmen, zu prüfen und unverzüglich zu beantworten; vor einer Ablehnung die Ausnahmen des Absatzes 3 prüfen.
- Systeme so gestalten, dass personenbezogene Daten auffindbar und löschbar sind, etwa Dokumente im Retrieval-Index eines RAG-Systems.
- Beachten, dass in Modellgewichte eingeflossene Daten ohne erneutes Training nicht gezielt entfernt werden können, und vorab festlegen, wie mit Löschanträgen zu Trainingsdaten umgegangen wird.
- Bei veröffentlichten Daten andere Verantwortliche, soweit angemessen, auch mit technischen Mitteln informieren.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 18 – Recht auf Einschränkung der Verarbeitung

Gibt der betroffenen Person das Recht auf Einschränkung der Verarbeitung, etwa wenn die Richtigkeit bestritten wird, die Verarbeitung unrechtmäßig ist oder über einen Widerspruch noch nicht entschieden ist.

#### Artikel 19 – Mitteilungspflicht im Zusammenhang mit der Berichtigung oder Löschung personenbezogener Daten oder der Einschränkung der Verarbeitung

Verpflichtet den Verantwortlichen, allen Empfängern jede Berichtigung, Löschung oder Einschränkung mitzuteilen, sofern das nicht unmöglich oder unverhältnismäßig ist, und die betroffene Person auf Verlangen über diese Empfänger zu unterrichten.

#### Artikel 20 – Recht auf Datenübertragbarkeit

Gibt der betroffenen Person das Recht, ihre Daten in einem strukturierten, gängigen und maschinenlesbaren Format zu erhalten und einem anderen Verantwortlichen ohne Behinderung zu übermitteln.

**Abschnitt 4 – Widerspruchsrecht und automatisierte Entscheidungsfindung im Einzelfall**

#### Artikel 21 – Widerspruchsrecht

Gibt der betroffenen Person das Recht, Verarbeitungen aufgrund öffentlichen Interesses oder berechtigter Interessen einschließlich Profiling zu widersprechen, und ein uneingeschränktes Widerspruchsrecht gegen Direktwerbung.

#### Artikel 22 – Automatisierte Entscheidungen im Einzelfall einschließlich Profiling

##### Worum geht es?

Artikel 22 gibt der betroffenen Person das Recht, nicht einer ausschließlich auf einer automatisierten Verarbeitung, einschließlich Profiling, beruhenden Entscheidung unterworfen zu werden, die ihr gegenüber rechtliche Wirkung entfaltet oder sie in ähnlicher Weise erheblich beeinträchtigt. Für KI-Systeme, die über Menschen entscheiden, ist er eine der wichtigsten Vorschriften der DSGVO.

##### Was verlangt der Artikel?

- **Absatz 1** – Die betroffene Person hat das Recht, nicht einer ausschließlich automatisierten Entscheidung einschließlich Profiling unterworfen zu werden, die ihr gegenüber rechtliche Wirkung entfaltet oder sie in ähnlicher Weise erheblich beeinträchtigt.
- **Absatz 2** – Absatz 1 gilt nicht, wenn die Entscheidung
  - a) für den Abschluss oder die Erfüllung eines Vertrags zwischen der betroffenen Person und dem Verantwortlichen erforderlich ist,
  - b) aufgrund von Unionsrecht oder dem Recht der Mitgliedstaaten zulässig ist, das angemessene Schutzmaßnahmen enthält, oder
  - c) mit ausdrücklicher Einwilligung der betroffenen Person erfolgt.
- **Absatz 3** – In den Fällen von Absatz 2 Buchstaben a und c trifft der Verantwortliche angemessene Maßnahmen zum Schutz der betroffenen Person, wozu mindestens das Recht auf Erwirkung des Eingreifens einer Person seitens des Verantwortlichen, auf Darlegung des eigenen Standpunkts und auf Anfechtung der Entscheidung gehört.
- **Absatz 4** – Entscheidungen nach Absatz 2 dürfen nicht auf besonderen Kategorien personenbezogener Daten nach Artikel 9 Absatz 1 beruhen, es sei denn, Artikel 9 Absatz 2 Buchstabe a oder g gilt und angemessene Schutzmaßnahmen sind getroffen.

##### Wer ist betroffen?

Verantwortliche, die Entscheidungen ausschließlich automatisiert treffen, und die betroffenen Personen, über die entschieden wird. In Deutschland ergänzt § 37 BDSG eine weitere Ausnahme für Versicherungsverträge.

##### Was ist nicht ausdrücklich geregelt?

- Wann eine Entscheidung „ausschließlich“ automatisiert ist, insbesondere wie weit eine menschliche Beteiligung gehen muss.
- Was eine „in ähnlicher Weise erhebliche“ Beeinträchtigung ist.
- Wie das Eingreifen einer Person nach Absatz 3 auszugestalten ist.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Entscheidungen identifizieren, die ein KI-System allein trifft und die rechtliche oder ähnlich erhebliche Wirkung haben, etwa bei Kredit-, Bewerbungs- oder Versicherungsentscheidungen.
- Solche Entscheidungen nur unter einer Ausnahme des Absatzes 2 treffen und das Eingreifen einer Person, die Darlegung des eigenen Standpunkts und eine Anfechtungsmöglichkeit vorsehen.
- Sicherstellen, dass die menschliche Prüfung tatsächlich inhaltlich erfolgt und keine bloße Formalität ist; sonst kann die Entscheidung weiterhin ausschließlich automatisiert sein.
- Besondere Kategorien personenbezogener Daten in solchen Entscheidungen vermeiden, sofern nicht Artikel 9 Absatz 2 Buchstabe a oder g greift.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

**Abschnitt 5 – Beschränkungen**

#### Artikel 23 – Beschränkungen

Erlaubt dem Unionsrecht und dem Recht der Mitgliedstaaten, Pflichten und Rechte nach den Artikeln 12 bis 22 und 34 sowie Teile des Artikels 5 zu beschränken, wenn dies zum Schutz wichtiger Ziele wie der nationalen oder öffentlichen Sicherheit notwendig und verhältnismäßig ist.

### Kapitel IV – Verantwortlicher und Auftragsverarbeiter

**Abschnitt 1 – Allgemeine Pflichten**

#### Artikel 24 – Verantwortung des für die Verarbeitung Verantwortlichen

Verpflichtet den Verantwortlichen, geeignete technische und organisatorische Maßnahmen umzusetzen und zu überprüfen, um die Einhaltung der Verordnung sicherzustellen und nachweisen zu können.

#### Artikel 25 – Datenschutz durch Technikgestaltung und durch datenschutzfreundliche Voreinstellungen

##### Worum geht es?

Artikel 25 verpflichtet den Verantwortlichen zu Datenschutz durch Technikgestaltung („Privacy by Design“) und durch datenschutzfreundliche Voreinstellungen („Privacy by Default“).

##### Was verlangt der Artikel?

- **Absatz 1** – Der Verantwortliche trifft sowohl bei der Festlegung der Mittel für die Verarbeitung als auch bei der Verarbeitung selbst geeignete technische und organisatorische Maßnahmen, etwa Pseudonymisierung, um die Datenschutzgrundsätze wie Datenminimierung wirksam umzusetzen und die nötigen Garantien in die Verarbeitung aufzunehmen. Dabei berücksichtigt er den Stand der Technik, die Implementierungskosten, Art, Umfang, Umstände und Zwecke der Verarbeitung sowie die Risiken für die Rechte und Freiheiten natürlicher Personen.
- **Absatz 2** – Der Verantwortliche stellt durch Voreinstellungen sicher, dass nur die für den jeweiligen Zweck erforderlichen Daten verarbeitet werden. Das gilt für die Menge der erhobenen Daten, den Umfang der Verarbeitung, die Speicherfrist und die Zugänglichkeit. Insbesondere dürfen Daten durch Voreinstellungen nicht ohne Eingreifen der Person einer unbestimmten Zahl von Personen zugänglich gemacht werden.
- **Absatz 3** – Ein genehmigtes Zertifizierungsverfahren nach Artikel 42 kann als Faktor herangezogen werden, um die Erfüllung der Absätze 1 und 2 nachzuweisen.

##### Wer ist betroffen?

Der Verantwortliche. Hersteller von Produkten, Diensten und Anwendungen werden in Erwägungsgrund 78 ermutigt, das Recht auf Datenschutz bei der Entwicklung zu berücksichtigen; der Artikel selbst verpflichtet sie nicht.

##### Was ist nicht ausdrücklich geregelt?

- Was der „Stand der Technik“ im Einzelfall ist.
- Welche Maßnahmen über die genannten Beispiele hinaus erforderlich sind.
- Nach welchen Kriterien Zertifizierungsverfahren nach Artikel 42 genehmigt werden.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Datenschutz schon beim Entwurf eines KI-Systems berücksichtigen, etwa Trainingsdaten pseudonymisieren, Merkmale auf das für den Zweck Nötige beschränken und den Zugriff auf Modelle und Logs begrenzen.
- Datenschutzfreundliche Voreinstellungen wählen, etwa keine Nutzung von Nutzereingaben für das Training ohne Entscheidung der Nutzer und kurze Speicherfristen für Prompts und Ausgaben.
- Datenschutzfreundliche Verfahren wie Differential Privacy oder Federated Learning prüfen, wo sie zum Zweck passen.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 26 – Gemeinsam Verantwortliche

Verpflichtet gemeinsam Verantwortliche, in einer Vereinbarung in transparenter Form festzulegen, wer welche Pflichten aus der Verordnung erfüllt.

#### Artikel 27 – Vertreter von nicht in der Union niedergelassenen Verantwortlichen oder Auftragsverarbeitern

Verpflichtet nicht in der Union niedergelassene Verantwortliche oder Auftragsverarbeiter, in den Fällen des Artikels 3 Absatz 2 schriftlich einen Vertreter in der Union zu benennen.

#### Artikel 28 – Auftragsverarbeiter

Verpflichtet den Verantwortlichen, nur mit Auftragsverarbeitern zu arbeiten, die hinreichende Garantien für geeignete technische und organisatorische Maßnahmen bieten.

#### Artikel 29 – Verarbeitung unter der Aufsicht des Verantwortlichen oder des Auftragsverarbeiters

Verpflichtet den Auftragsverarbeiter und alle ihm oder dem Verantwortlichen unterstellten Personen, personenbezogene Daten nur auf Weisung des Verantwortlichen zu verarbeiten, sofern nicht gesetzlich anders vorgeschrieben.

#### Artikel 30 – Verzeichnis von Verarbeitungstätigkeiten

Verpflichtet Verantwortliche und Auftragsverarbeiter sowie gegebenenfalls ihre Vertreter, ein Verzeichnis von Verarbeitungstätigkeiten mit festgelegtem Inhalt zu führen.

#### Artikel 31 – Zusammenarbeit mit der Aufsichtsbehörde

Verpflichtet Verantwortliche, Auftragsverarbeiter und gegebenenfalls ihre Vertreter, auf Anfrage mit der Aufsichtsbehörde zusammenzuarbeiten.

**Abschnitt 2 – Sicherheit personenbezogener Daten**

#### Artikel 32 – Sicherheit der Verarbeitung

Verpflichtet Verantwortliche und Auftragsverarbeiter zu geeigneten technischen und organisatorischen Maßnahmen, die ein dem Risiko angemessenes Schutzniveau gewährleisten.

#### Artikel 33 – Meldung von Verletzungen des Schutzes personenbezogener Daten an die Aufsichtsbehörde

Verpflichtet den Verantwortlichen, eine Verletzung des Schutzes personenbezogener Daten unverzüglich und möglichst binnen 72 Stunden der Aufsichtsbehörde zu melden, es sei denn, sie führt voraussichtlich nicht zu einem Risiko für natürliche Personen.

#### Artikel 34 – Benachrichtigung der von einer Verletzung des Schutzes personenbezogener Daten betroffenen Person

Verpflichtet den Verantwortlichen, die betroffene Person unverzüglich zu benachrichtigen, wenn eine Verletzung des Schutzes personenbezogener Daten voraussichtlich ein hohes Risiko für ihre Rechte und Freiheiten zur Folge hat.

**Abschnitt 3 – Datenschutz-Folgenabschätzung und vorherige Konsultation**

#### Artikel 35 – Datenschutz-Folgenabschätzung

##### Worum geht es?

Artikel 35 verpflichtet den Verantwortlichen, vor Verarbeitungen mit voraussichtlich hohem Risiko für die Rechte und Freiheiten natürlicher Personen eine Datenschutz-Folgenabschätzung durchzuführen. Er legt fest, wann sie erforderlich ist, was sie enthalten muss und welche Rolle Aufsichtsbehörden, Datenschutzbeauftragte und betroffene Personen dabei haben.

##### Was verlangt der Artikel?

- **Absatz 1** – Hat eine Form der Verarbeitung, insbesondere bei Verwendung neuer Technologien, aufgrund ihrer Art, ihres Umfangs, ihrer Umstände und ihrer Zwecke voraussichtlich ein hohes Risiko zur Folge, führt der Verantwortliche vorab eine Datenschutz-Folgenabschätzung durch. Für ähnliche Verarbeitungsvorgänge mit ähnlich hohen Risiken genügt eine einzige Abschätzung.
- **Absatz 2** – Der Verantwortliche holt dabei den Rat der oder des Datenschutzbeauftragten ein, sofern benannt.
- **Absatz 3** – Erforderlich ist sie insbesondere bei
  - a) systematischer und umfassender Bewertung persönlicher Aspekte auf Grundlage automatisierter Verarbeitung einschließlich Profiling, die als Grundlage für Entscheidungen mit rechtlicher oder ähnlich erheblicher Wirkung dient,
  - b) umfangreicher Verarbeitung besonderer Kategorien nach Artikel 9 Absatz 1 oder von Daten über Straftaten nach Artikel 10,
  - c) systematischer umfangreicher Überwachung öffentlich zugänglicher Bereiche.
- **Absatz 4** – Die Aufsichtsbehörde erstellt und veröffentlicht eine Liste der Verarbeitungsvorgänge, für die eine Abschätzung durchzuführen ist, und übermittelt sie dem Europäischen Datenschutzausschuss.
- **Absatz 5** – Die Aufsichtsbehörde kann außerdem eine Liste der Vorgänge veröffentlichen, für die keine Abschätzung erforderlich ist.
- **Absatz 6** – Betreffen die Listen grenzüberschreitende Tätigkeiten, wendet die Aufsichtsbehörde vor ihrer Festlegung das Kohärenzverfahren nach Artikel 63 an.
- **Absatz 7** – Die Abschätzung enthält mindestens
  - a) eine systematische Beschreibung der Verarbeitungsvorgänge und Zwecke,
  - b) eine Bewertung der Notwendigkeit und Verhältnismäßigkeit,
  - c) eine Bewertung der Risiken für die Rechte und Freiheiten der betroffenen Personen und
  - d) die geplanten Abhilfemaßnahmen, Garantien und Sicherheitsvorkehrungen.
- **Absatz 8** – Die Einhaltung genehmigter Verhaltensregeln nach Artikel 40 ist bei der Beurteilung gebührend zu berücksichtigen.
- **Absatz 9** – Gegebenenfalls holt der Verantwortliche den Standpunkt der betroffenen Personen oder ihrer Vertreter ein, unbeschadet geschäftlicher oder öffentlicher Interessen und der Sicherheit der Verarbeitung.
- **Absatz 10** – Beruht eine Verarbeitung nach Artikel 6 Absatz 1 Buchstabe c oder e auf einer Rechtsvorschrift, bei deren Erlass bereits eine allgemeine Folgenabschätzung durchgeführt wurde, gelten die Absätze 1 bis 7 nicht, sofern die Mitgliedstaaten eine vorherige Abschätzung nicht für erforderlich halten.
- **Absatz 11** – Der Verantwortliche überprüft erforderlichenfalls, ob die Verarbeitung gemäß der Abschätzung erfolgt, zumindest wenn sich das Risiko ändert.

##### Wer ist betroffen?

Verantwortliche, die Verarbeitungen mit voraussichtlich hohem Risiko planen; die oder der Datenschutzbeauftragte, die oder der beratend mitwirkt; die Aufsichtsbehörden, die die Listen nach den Absätzen 4 bis 6 erstellen.

##### Was ist nicht ausdrücklich geregelt?

- Ab wann ein Risiko „hoch“ ist, über die Fälle des Absatzes 3 und die Listen der Aufsichtsbehörden hinaus.
- Welche Form und Methodik die Abschätzung haben muss.
- Wie Notwendigkeit und Verhältnismäßigkeit nach Absatz 7 Buchstabe b zu bewerten sind.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Neue KI-Systeme anhand des Absatzes 3 und der nationalen Listen nach Absatz 4 prüfen; Profiling mit erheblicher Wirkung und umfangreiche Verarbeitung besonderer Kategorien erfordern regelmäßig eine Abschätzung.
- Die Abschätzung vor Beginn der Verarbeitung durchführen, die oder den Datenschutzbeauftragten einbinden und die Inhalte nach Absatz 7 dokumentieren.
- Die Abschätzung überprüfen, wenn sich das Risiko ändert, etwa nach erneutem Training eines Modells mit neuen Daten oder bei Erweiterung auf neue Zwecke.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 36 – Vorherige Konsultation

Verpflichtet den Verantwortlichen, vor der Verarbeitung die Aufsichtsbehörde zu konsultieren, wenn die Datenschutz-Folgenabschätzung trotz Abhilfemaßnahmen ein hohes Risiko ergibt.

**Abschnitt 4 – Datenschutzbeauftragter**

#### Artikel 37 – Benennung eines Datenschutzbeauftragten

Verpflichtet Verantwortliche und Auftragsverarbeiter, einen Datenschutzbeauftragten zu benennen, etwa bei Behörden, umfangreicher Überwachung von Personen oder umfangreicher Verarbeitung besonderer Datenkategorien.

#### Artikel 38 – Stellung des Datenschutzbeauftragten

Verpflichtet Verantwortliche und Auftragsverarbeiter, den Datenschutzbeauftragten frühzeitig in alle Datenschutzfragen einzubinden und ihn mit den nötigen Ressourcen zu unterstützen.

#### Artikel 39 – Aufgaben des Datenschutzbeauftragten

Legt die Aufgaben des Datenschutzbeauftragten fest, darunter Unterrichtung, Beratung, Überwachung der Einhaltung, Beratung zur Datenschutz-Folgenabschätzung und Zusammenarbeit mit der Aufsichtsbehörde.

**Abschnitt 5 – Verhaltensregeln und Zertifizierung**

#### Artikel 40 – Verhaltensregeln

Fördert die Ausarbeitung von Verhaltensregeln, die zur ordnungsgemäßen Anwendung der Verordnung beitragen und die Besonderheiten einzelner Branchen sowie kleiner und mittlerer Unternehmen berücksichtigen.

#### Artikel 41 – Überwachung der genehmigten Verhaltensregeln

Erlaubt die Überwachung genehmigter Verhaltensregeln durch Stellen, die von der zuständigen Aufsichtsbehörde dafür akkreditiert wurden.

#### Artikel 42 – Zertifizierung

Fördert datenschutzspezifische Zertifizierungsverfahren sowie Datenschutzsiegel und -prüfzeichen, mit denen Verantwortliche und Auftragsverarbeiter die Einhaltung der Verordnung nachweisen können.

#### Artikel 43 – Zertifizierungsstellen

Regelt die Zertifizierungsstellen, die über Fachwissen im Datenschutz verfügen und von der Aufsichtsbehörde oder der nationalen Akkreditierungsstelle akkreditiert sein müssen.

### Kapitel V – Übermittlungen personenbezogener Daten an Drittländer oder an internationale Organisationen

#### Artikel 44 – Allgemeine Grundsätze der Datenübermittlung

Verlangt, dass jede Übermittlung personenbezogener Daten an Drittländer oder internationale Organisationen die Bedingungen dieses Kapitels einhält, damit das Schutzniveau nicht untergraben wird.

#### Artikel 45 – Datenübermittlung auf der Grundlage eines Angemessenheitsbeschlusses

Erlaubt Übermittlungen an Drittländer oder internationale Organisationen, für die die Kommission ein angemessenes Schutzniveau beschlossen hat.

#### Artikel 46 – Datenübermittlung vorbehaltlich geeigneter Garantien

##### Worum geht es?

Artikel 46 regelt Übermittlungen personenbezogener Daten an Drittländer oder internationale Organisationen, für die kein Angemessenheitsbeschluss der Kommission vorliegt. Sie sind nur mit geeigneten Garantien zulässig, etwa Standarddatenschutzklauseln oder verbindlichen internen Datenschutzvorschriften.

##### Was verlangt der Artikel?

- **Absatz 1** – Liegt kein Beschluss nach Artikel 45 Absatz 3 vor, darf ein Verantwortlicher oder Auftragsverarbeiter Daten nur übermitteln, wenn er geeignete Garantien vorsieht und den betroffenen Personen durchsetzbare Rechte und wirksame Rechtsbehelfe zur Verfügung stehen.
- **Absatz 2** – Ohne besondere Genehmigung einer Aufsichtsbehörde können geeignete Garantien bestehen in
  - a) einem rechtlich bindenden und durchsetzbaren Dokument zwischen Behörden oder öffentlichen Stellen,
  - b) verbindlichen internen Datenschutzvorschriften nach Artikel 47,
  - c) von der Kommission erlassenen Standarddatenschutzklauseln,
  - d) von einer Aufsichtsbehörde angenommenen und von der Kommission genehmigten Standarddatenschutzklauseln,
  - e) genehmigten Verhaltensregeln nach Artikel 40 mit verbindlichen Verpflichtungen des Empfängers im Drittland oder
  - f) einem genehmigten Zertifizierungsmechanismus nach Artikel 42 mit verbindlichen Verpflichtungen des Empfängers im Drittland.
- **Absatz 3** – Mit Genehmigung der zuständigen Aufsichtsbehörde können geeignete Garantien auch bestehen in
  - a) individuell ausgehandelten Vertragsklauseln mit dem Empfänger oder
  - b) Bestimmungen in Verwaltungsvereinbarungen zwischen Behörden mit durchsetzbaren Rechten der betroffenen Personen.
- **Absatz 4** – In den Fällen des Absatzes 3 wendet die Aufsichtsbehörde das Kohärenzverfahren nach Artikel 63 an.
- **Absatz 5** – Genehmigungen und Beschlüsse der Kommission nach Artikel 26 der Richtlinie 95/46/EG bleiben gültig, bis sie geändert, ersetzt oder aufgehoben werden.

##### Wer ist betroffen?

Verantwortliche und Auftragsverarbeiter, die Daten in Drittländer oder an internationale Organisationen übermitteln, und die Aufsichtsbehörden, die nach Absatz 3 genehmigen.

##### Was ist nicht ausdrücklich geregelt?

- Was „durchsetzbare Rechte“ und „wirksame Rechtsbehelfe“ im Einzelnen erfordern.
- Nach welchen Kriterien Aufsichtsbehörden Vertragsklauseln nach Absatz 3 genehmigen.

##### Was könnte das in der Praxis bedeuten?

**Mögliche Umsetzung – keine gesetzlich vorgeschriebene Checkliste:**

- Vor der Nutzung von KI-Diensten oder APIs, die außerhalb der EU betrieben werden, prüfen, ob personenbezogene Daten übermittelt werden und ob ein Angemessenheitsbeschluss besteht.
- Ohne Angemessenheitsbeschluss eine Garantie nach Absatz 2 nutzen, typischerweise die Standarddatenschutzklauseln der Kommission, und sie aktuell halten.
- Prüfen, ob die Zusagen des Empfängers die Rechte der betroffenen Personen tatsächlich durchsetzbar machen.

##### Ab wann gilt der Artikel?

Gilt ab dem **25. Mai 2018** (Art. 99 Abs. 2).

#### Artikel 47 – Verbindliche interne Datenschutzvorschriften

Verpflichtet die zuständige Aufsichtsbehörde, verbindliche interne Datenschutzvorschriften zu genehmigen, die die festgelegten Anforderungen erfüllen, und legt ihren Mindestinhalt fest.

#### Artikel 48 – Nach dem Unionsrecht nicht zulässige Übermittlung oder Offenlegung

Bestimmt, dass Urteile und Entscheidungen von Drittlandsgerichten oder -behörden, die eine Übermittlung oder Offenlegung verlangen, nur auf Grundlage einer internationalen Übereinkunft wie eines Rechtshilfeabkommens anerkannt oder vollstreckt werden.

#### Artikel 49 – Ausnahmen für bestimmte Fälle

Erlaubt Übermittlungen ohne Angemessenheitsbeschluss oder geeignete Garantien nur in bestimmten Fällen, etwa mit ausdrücklicher Einwilligung der betroffenen Person oder zur Erfüllung eines Vertrags.

#### Artikel 50 – Internationale Zusammenarbeit zum Schutz personenbezogener Daten

Verpflichtet die Kommission und die Aufsichtsbehörden, die internationale Zusammenarbeit beim Schutz personenbezogener Daten zu fördern.

### Kapitel VI – Unabhängige Aufsichtsbehörden

**Abschnitt 1 – Unabhängigkeit**

#### Artikel 51 – Aufsichtsbehörde

Verpflichtet jeden Mitgliedstaat, eine oder mehrere unabhängige Behörden mit der Überwachung der Anwendung der Verordnung zu betrauen.

#### Artikel 52 – Unabhängigkeit

Garantiert, dass jede Aufsichtsbehörde bei der Erfüllung ihrer Aufgaben und der Ausübung ihrer Befugnisse völlig unabhängig handelt.

#### Artikel 53 – Allgemeine Bedingungen für die Mitglieder der Aufsichtsbehörde

Verpflichtet die Mitgliedstaaten, die Mitglieder ihrer Aufsichtsbehörden in einem transparenten Verfahren durch Parlament, Regierung, Staatsoberhaupt oder eine unabhängige Stelle ernennen zu lassen.

#### Artikel 54 – Errichtung der Aufsichtsbehörde

Verpflichtet die Mitgliedstaaten, die Errichtung jeder Aufsichtsbehörde gesetzlich zu regeln, darunter Qualifikation, Amtszeit, Wiederernennung und Pflichten der Mitglieder und Bediensteten.

**Abschnitt 2 – Zuständigkeit, Aufgaben und Befugnisse**

#### Artikel 55 – Zuständigkeit

Bestimmt, dass jede Aufsichtsbehörde im Hoheitsgebiet ihres eigenen Mitgliedstaats zuständig ist.

#### Artikel 56 – Zuständigkeit der federführenden Aufsichtsbehörde

Bestimmt die Aufsichtsbehörde der Haupt- oder einzigen Niederlassung als federführende Aufsichtsbehörde für grenzüberschreitende Verarbeitungen.

#### Artikel 57 – Aufgaben

Legt die Aufgaben der Aufsichtsbehörden fest, darunter die Überwachung und Durchsetzung der Verordnung und die Sensibilisierung der Öffentlichkeit.

#### Artikel 58 – Befugnisse

Legt die Untersuchungs-, Abhilfe-, Genehmigungs- und beratenden Befugnisse jeder Aufsichtsbehörde fest.

#### Artikel 59 – Tätigkeitsbericht

Verpflichtet die Aufsichtsbehörden, einen Jahresbericht über ihre Tätigkeit zu erstellen, ihn den zuständigen Stellen zu übermitteln und zu veröffentlichen.

### Kapitel VII – Zusammenarbeit und Kohärenz

**Abschnitt 1 – Zusammenarbeit**

#### Artikel 60 – Zusammenarbeit zwischen der federführenden Aufsichtsbehörde und den anderen betroffenen Aufsichtsbehörden

Verpflichtet die federführende Aufsichtsbehörde, mit den anderen betroffenen Aufsichtsbehörden zusammenzuarbeiten, alle zweckdienlichen Informationen auszutauschen und einen Konsens anzustreben.

#### Artikel 61 – Gegenseitige Amtshilfe

Verpflichtet die Aufsichtsbehörden, einander zweckdienliche Informationen zu übermitteln und Amtshilfe zu leisten, damit die Verordnung einheitlich angewendet wird.

#### Artikel 62 – Gemeinsame Maßnahmen der Aufsichtsbehörden

Sieht gemeinsame Maßnahmen der Aufsichtsbehörden vor, darunter gemeinsame Untersuchungen und Durchsetzungsmaßnahmen mit Mitgliedern oder Bediensteten anderer Mitgliedstaaten.

**Abschnitt 2 – Kohärenz**

#### Artikel 63 – Kohärenzverfahren

Verpflichtet die Aufsichtsbehörden, im Kohärenzverfahren untereinander und gegebenenfalls mit der Kommission zusammenzuarbeiten, damit die Verordnung einheitlich angewendet wird.

#### Artikel 64 – Stellungnahme des Ausschusses

Verpflichtet die zuständige Aufsichtsbehörde, dem Ausschuss Beschlussentwürfe zu bestimmten Maßnahmen vorzulegen, etwa zu Listen für Datenschutz-Folgenabschätzungen, Standarddatenschutzklauseln oder verbindlichen internen Datenschutzvorschriften, und regelt die Stellungnahme des Ausschusses.

#### Artikel 65 – Streitbeilegung durch den Ausschuss

Verpflichtet den Ausschuss, bei Einsprüchen gegen Beschlussentwürfe, Zuständigkeitsstreitigkeiten oder Nichtbeachtung seiner Stellungnahmen einen verbindlichen Beschluss zu erlassen.

#### Artikel 66 – Dringlichkeitsverfahren

Erlaubt einer Aufsichtsbehörde, unter außergewöhnlichen Umständen sofort einstweilige Maßnahmen mit einer Geltungsdauer von höchstens drei Monaten zu erlassen.

#### Artikel 67 – Informationsaustausch

Erlaubt der Kommission, Durchführungsrechtsakte über den elektronischen Informationsaustausch zwischen den Aufsichtsbehörden und mit dem Ausschuss zu erlassen.

**Abschnitt 3 – Europäischer Datenschutzausschuss**

#### Artikel 68 – Europäischer Datenschutzausschuss

Errichtet den Europäischen Datenschutzausschuss als Einrichtung der Union mit eigener Rechtspersönlichkeit, bestehend aus den Leitern der Aufsichtsbehörden und dem Europäischen Datenschutzbeauftragten.

#### Artikel 69 – Unabhängigkeit

Verpflichtet den Ausschuss, seine Aufgaben unabhängig zu erfüllen und weder Weisungen einzuholen noch entgegenzunehmen.

#### Artikel 70 – Aufgaben des Ausschusses

Legt die Aufgaben des Ausschusses für die einheitliche Anwendung der Verordnung fest, darunter Überwachung, Beratung der Kommission sowie Leitlinien, Empfehlungen und bewährte Verfahren.

#### Artikel 71 – Berichterstattung

Verpflichtet den Ausschuss, einen öffentlichen Jahresbericht über den Schutz natürlicher Personen bei der Verarbeitung in der Union und gegebenenfalls in Drittländern zu erstellen.

#### Artikel 72 – Verfahrensweise

Bestimmt, dass der Ausschuss in der Regel mit einfacher Mehrheit beschließt und sich mit Zweidrittelmehrheit eine Geschäftsordnung gibt.

#### Artikel 73 – Vorsitz

Verpflichtet den Ausschuss, mit einfacher Mehrheit einen Vorsitz und zwei stellvertretende Vorsitzende für fünf Jahre zu wählen, einmal wiederwählbar.

#### Artikel 74 – Aufgaben des Vorsitzes

Legt die Aufgaben des Vorsitzes fest, darunter die Einberufung der Sitzungen, die Mitteilung der Beschlüsse und die fristgerechte Erfüllung der Aufgaben des Ausschusses.

#### Artikel 75 – Sekretariat

Stellt dem Ausschuss ein Sekretariat beim Europäischen Datenschutzbeauftragten zur Seite, das ihn analytisch, administrativ und logistisch unterstützt.

#### Artikel 76 – Vertraulichkeit

Bestimmt, dass die Beratungen des Ausschusses vertraulich sind, wenn er dies für erforderlich hält.

### Kapitel VIII – Rechtsbehelfe, Haftung und Sanktionen

#### Artikel 77 – Recht auf Beschwerde bei einer Aufsichtsbehörde

Gibt jeder betroffenen Person das Recht auf Beschwerde bei einer Aufsichtsbehörde, wenn sie meint, dass die Verarbeitung ihrer Daten gegen die Verordnung verstößt.

#### Artikel 78 – Recht auf wirksamen gerichtlichen Rechtsbehelf gegen eine Aufsichtsbehörde

Gibt jeder Person das Recht auf einen wirksamen gerichtlichen Rechtsbehelf gegen rechtsverbindliche Beschlüsse einer Aufsichtsbehörde und betroffenen Personen einen Rechtsbehelf, wenn die Behörde eine Beschwerde nicht binnen drei Monaten bearbeitet oder sie unterrichtet.

#### Artikel 79 – Recht auf wirksamen gerichtlichen Rechtsbehelf gegen Verantwortliche oder Auftragsverarbeiter

Gibt der betroffenen Person das Recht auf einen wirksamen gerichtlichen Rechtsbehelf gegen Verantwortliche oder Auftragsverarbeiter, wenn ihre Rechte durch eine verordnungswidrige Verarbeitung verletzt wurden.

#### Artikel 80 – Vertretung von betroffenen Personen

Gibt der betroffenen Person das Recht, eine Organisation ohne Gewinnerzielungsabsicht zu beauftragen, in ihrem Namen Beschwerde einzulegen und bestimmte Rechte wahrzunehmen.

#### Artikel 81 – Aussetzung des Verfahrens

Erlaubt einem Gericht, sein Verfahren auszusetzen, wenn in einem anderen Mitgliedstaat ein Verfahren zum selben Gegenstand und gegen denselben Verantwortlichen oder Auftragsverarbeiter anhängig ist.

#### Artikel 82 – Haftung und Recht auf Schadenersatz

Gibt jeder Person, der wegen eines Verstoßes gegen die Verordnung ein materieller oder immaterieller Schaden entstanden ist, einen Anspruch auf Schadenersatz gegen den Verantwortlichen oder Auftragsverarbeiter.

#### Artikel 83 – Allgemeine Bedingungen für die Verhängung von Geldbußen

Regelt die Verhängung von Geldbußen, die dabei zu berücksichtigenden Kriterien und Höchstbeträge von bis zu 20 Millionen Euro oder 4 % des weltweiten Jahresumsatzes.

#### Artikel 84 – Sanktionen

Verpflichtet die Mitgliedstaaten, wirksame, verhältnismäßige und abschreckende Sanktionen für Verstöße ohne Geldbuße festzulegen und der Kommission bis zum 25. Mai 2018 mitzuteilen.

### Kapitel IX – Vorschriften für besondere Verarbeitungssituationen

#### Artikel 85 – Verarbeitung und Freiheit der Meinungsäußerung und Informationsfreiheit

Verpflichtet die Mitgliedstaaten, den Datenschutz mit der Meinungs- und Informationsfreiheit in Einklang zu bringen, und erlaubt Ausnahmen für journalistische, wissenschaftliche, künstlerische und literarische Zwecke.

#### Artikel 86 – Verarbeitung und Zugang der Öffentlichkeit zu amtlichen Dokumenten

Erlaubt die Offenlegung personenbezogener Daten in amtlichen Dokumenten von Behörden oder öffentlich beauftragten privaten Einrichtungen nach Unionsrecht oder mitgliedstaatlichem Recht, um den Zugang der Öffentlichkeit mit dem Datenschutz in Einklang zu bringen.

#### Artikel 87 – Verarbeitung der nationalen Kennziffer

Erlaubt den Mitgliedstaaten, die Verarbeitung einer nationalen Kennziffer oder anderer Kennzeichen von allgemeiner Bedeutung näher zu regeln, nur mit geeigneten Garantien.

#### Artikel 88 – Datenverarbeitung im Beschäftigungskontext

Erlaubt den Mitgliedstaaten spezifischere Vorschriften für die Verarbeitung von Beschäftigtendaten im Beschäftigungskontext, etwa bei Einstellung und Vertragserfüllung, mit Schutzmaßnahmen für die Rechte und die Würde der Beschäftigten.

#### Artikel 89 – Garantien und Ausnahmen in Bezug auf die Verarbeitung zu im öffentlichen Interesse liegenden Archivzwecken, zu wissenschaftlichen oder historischen Forschungszwecken und zu statistischen Zwecken

Verlangt geeignete Garantien für Verarbeitungen zu Archiv-, Forschungs- und Statistikzwecken und erlaubt dem Unionsrecht und dem Recht der Mitgliedstaaten Ausnahmen von bestimmten Betroffenenrechten.

#### Artikel 90 – Geheimhaltungspflichten

Erlaubt den Mitgliedstaaten besondere Vorschriften zu den Befugnissen der Aufsichtsbehörden gegenüber Verantwortlichen oder Auftragsverarbeitern, die einem Berufsgeheimnis unterliegen.

#### Artikel 91 – Bestehende Datenschutzvorschriften von Kirchen und religiösen Vereinigungen oder Gemeinschaften

Erlaubt Kirchen und religiösen Vereinigungen, bei Inkrafttreten der Verordnung bestehende umfassende Datenschutzregeln weiter anzuwenden, wenn sie mit der Verordnung in Einklang gebracht werden und einer unabhängigen Aufsicht unterliegen.

### Kapitel X – Delegierte Rechtsakte und Durchführungsrechtsakte

#### Artikel 92 – Ausübung der Befugnisübertragung

Regelt die Ausübung der Befugnis der Kommission zum Erlass delegierter Rechtsakte, einschließlich Widerruf durch Europäisches Parlament oder Rat und Einwandverfahren.

#### Artikel 93 – Ausschussverfahren

Bestimmt, dass die Kommission von einem Ausschuss im Sinne der Verordnung (EU) Nr. 182/2011 unterstützt wird.

### Kapitel XI – Schlussbestimmungen

#### Artikel 94 – Aufhebung der Richtlinie 95/46/EG

Hebt die Richtlinie 95/46/EG mit Wirkung vom 25. Mai 2018 auf; Verweise auf sie gelten als Verweise auf diese Verordnung.

#### Artikel 95 – Verhältnis zur Richtlinie 2002/58/EG

Bestimmt, dass die Verordnung Anbietern öffentlich zugänglicher elektronischer Kommunikationsdienste keine zusätzlichen Pflichten auferlegt, soweit die Richtlinie 2002/58/EG besondere Pflichten mit derselben Zielsetzung enthält.

#### Artikel 96 – Verhältnis zu bereits geschlossenen Übereinkünften

Lässt vor dem 24. Mai 2016 von Mitgliedstaaten geschlossene und mit dem damaligen Unionsrecht vereinbare internationale Übereinkünfte über Datenübermittlungen in Kraft, bis sie geändert, ersetzt oder aufgehoben werden.

#### Artikel 97 – Berichte der Kommission

Verpflichtet die Kommission, dem Europäischen Parlament und dem Rat bis zum 25. Mai 2020 und danach alle vier Jahre Berichte über die Bewertung und Überprüfung der Verordnung vorzulegen.

#### Artikel 98 – Überprüfung anderer Rechtsakte der Union zum Datenschutz

Verpflichtet die Kommission, gegebenenfalls Gesetzgebungsvorschläge zur Änderung anderer Datenschutzrechtsakte der Union vorzulegen, um einen einheitlichen Schutz sicherzustellen.

#### Artikel 99 – Inkrafttreten und Anwendung

Bestimmt, dass die Verordnung am zwanzigsten Tag nach ihrer Veröffentlichung in Kraft tritt und ab dem 25. Mai 2018 gilt.

### Zeitplan

| Datum | Ereignis |
| --- | --- |
| 4. Mai 2016 | Veröffentlichung im Amtsblatt |
| 24. Mai 2016 | Inkrafttreten |
| 25. Mai 2018 | Geltungsbeginn; Aufhebung der Richtlinie 95/46/EG (Art. 94) |
| 2025 | Vorschläge der Kommission zur Änderung der DSGVO (COM(2025) 501 und COM(2025) 837); in der hier zusammengefassten Fassung nicht enthalten |

### Durchsetzung und Sanktionen

- **Aufsicht**: Jeder Mitgliedstaat hat mindestens eine unabhängige Aufsichtsbehörde (Art. 51). Bei grenzüberschreitender Verarbeitung ist die Aufsichtsbehörde der Hauptniederlassung federführend (One-Stop-Shop, Art. 56); der Europäische Datenschutzausschuss sorgt für die einheitliche Anwendung (Art. 63–76).
- **Geldbußen** (Art. 83): bis zu **10 Millionen Euro oder 2 %** des weltweiten Jahresumsatzes, je nachdem, welcher Betrag höher ist, unter anderem für Verstöße gegen die Pflichten von Verantwortlichen und Auftragsverarbeitern (Art. 8, 11, 25–39, 42, 43); bis zu **20 Millionen Euro oder 4 %** für Verstöße gegen die Grundsätze und Rechtsgrundlagen (Art. 5, 6, 7, 9), die Rechte betroffener Personen (Art. 12–22), die Vorschriften über Drittlandübermittlungen (Art. 44–49) und Anordnungen der Aufsichtsbehörde.
- **Rechtsbehelfe**: Beschwerde bei einer Aufsichtsbehörde (Art. 77), gerichtliche Rechtsbehelfe gegen Aufsichtsbehörden, Verantwortliche und Auftragsverarbeiter (Art. 78–79) und Schadenersatz für materielle und immaterielle Schäden (Art. 82).

### Verhältnis zu anderen Rechtsakten

- **[[eprivacy-directive|ePrivacy-Richtlinie]]**: Für öffentlich zugängliche elektronische Kommunikationsdienste erlegt die DSGVO keine zusätzlichen Pflichten auf, soweit die ePrivacy-Richtlinie besondere Pflichten mit derselben Zielsetzung enthält (Art. 95). In Deutschland wird die Richtlinie durch das [[tdddg|TDDDG]] umgesetzt.
- **[[bdsg|BDSG]]**: Das Bundesdatenschutzgesetz nutzt die Öffnungsklauseln der DSGVO, etwa für Beschäftigtendaten und die Verarbeitung durch öffentliche Stellen, und setzt die Richtlinie (EU) 2016/680 um.
- **Richtlinie (EU) 2016/680**: gilt anstelle der DSGVO für Behörden, die Straftaten verhüten, ermitteln, aufdecken oder verfolgen.
- **[[eu-ai-act|EU AI Act]]**: lässt die DSGVO unberührt (Art. 2 Abs. 7 AI Act); KI-Systeme, die personenbezogene Daten verarbeiten, brauchen eine Rechtsgrundlage nach der DSGVO. Der AI Act ergänzt eigene Regeln für die Verarbeitung besonderer Kategorien personenbezogener Daten zur Erkennung von Bias (Art. 4a AI Act).
- **[[data-act|Data Act]] und [[data-governance-act|Data Governance Act]]**: gelten unbeschadet der DSGVO; soweit sie personenbezogene Daten betreffen, hat die DSGVO Vorrang.

### Bedeutung für die KI-Entwicklung

- **Rechtsgrundlage für Trainingsdaten** (Art. 6): Wer personenbezogene Daten für Training oder Fine-Tuning von Modellen erhebt oder weiterverwendet, braucht eine Rechtsgrundlage, meist Einwilligung oder berechtigte Interessen; der Grundsatz der Zweckbindung (Art. 5 Abs. 1 Buchst. b) begrenzt die Weiterverwendung von Daten, die zu anderen Zwecken erhoben wurden.
- **Datenminimierung** (Art. 5 Abs. 1 Buchst. c): Nur die für den Zweck notwendigen Daten dürfen verarbeitet werden; das spricht für Anonymisierung, Pseudonymisierung und datenschutzfreundliche Verfahren wie [[differential-privacy-and-federated-learning|Differential Privacy und Federated Learning]].
- **Besondere Kategorien** (Art. 9): Gesundheitsdaten, biometrische Daten oder Daten zur ethnischen Herkunft dürfen nur unter den engen Voraussetzungen des Art. 9 Abs. 2 verarbeitet werden; das begrenzt auch die Erhebung solcher Daten für [[bias-in-nlp|Bias-Analysen]] und [[fairness-metrics|Fairness-Tests]].
- **Transparenz und Auskunft** (Art. 12–15): Betroffene Personen müssen über die Verarbeitung informiert werden und können Auskunft über ihre Daten verlangen, auch wenn diese in KI-Systemen verwendet werden.
- **Recht auf Löschung** (Art. 17): Personenbezogene Daten müssen gelöscht werden können; Daten in einem [[retrieval-augmented-generation|Retrieval-Index]] lassen sich direkt löschen, während in Modellgewichten aufgenommene Daten ohne erneutes Training nicht gezielt entfernt werden können.
- **Automatisierte Entscheidungen** (Art. 22): Ausschließlich automatisierte Entscheidungen mit rechtlicher oder ähnlich erheblicher Wirkung sind nur unter den Ausnahmen des Art. 22 Abs. 2 zulässig, mit Schutzmaßnahmen wie dem Eingreifen einer Person und dem Recht auf Anfechtung; hier besteht ein Bezug zu [[explainable-ai|Explainable AI]].
- **Datenschutz durch Technikgestaltung** (Art. 25) und **Datenschutz-Folgenabschätzung** (Art. 35): Neue Technologien mit voraussichtlich hohem Risiko erfordern vor Beginn der Verarbeitung eine Datenschutz-Folgenabschätzung.
- **Drittlandübermittlungen** (Art. 44–49): Die Nutzung von Modellen oder APIs, die außerhalb der EU gehostet werden, ist eine Übermittlung und braucht einen Angemessenheitsbeschluss oder geeignete Garantien wie Standardvertragsklauseln.

### Amtliche Quellen

- Verordnung (EU) 2016/679, Amtsblatt: [Englisch](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) und [Deutsch](https://eur-lex.europa.eu/eli/reg/2016/679/oj/deu)
- [Konsolidierte Fassung vom 4. Mai 2016 (Englisch)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504)
