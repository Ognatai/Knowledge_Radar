> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the texts published in the Official Journal of the European Union are authentic.

### TL;DR

The ePrivacy Directive protects privacy and the confidentiality of communications in the electronic communications sector. It requires consent before information is stored on or read from a user's device (the basis of cookie banners), restricts the use of traffic and location data, protects the confidentiality of communications and regulates unsolicited marketing messages. As a directive, it applies through national law; in Germany mainly through the [[tdddg|TDDDG]]. It particularises and complements the general data protection rules now set out in the [[gdpr|GDPR]].

### Key facts

| | |
| --- | --- |
| Official reference | Directive 2002/58/EC, OJ L 201, 31.7.2002 |
| Type and jurisdiction | EU directive; applies through national transposition |
| Adopted | 12 July 2002 |
| Entry into force | 31 July 2002 (day of publication, Art. 20) |
| Transposition deadline | 31 October 2003 (Art. 17) |
| Main amendment | Directive 2009/136/EC (consent for storage on terminal equipment, breach notification, penalties) |
| Version summarised | consolidated text of 19 December 2009 |

### Scope

The Directive applies to the processing of personal data in connection with the provision of **publicly available electronic communications services in public communications networks** in the EU (Art. 3). Most of its obligations address the providers of these services and networks.

Some provisions apply more broadly:

- **Art. 5(3)** applies to anyone who stores information on, or reads information from, the terminal equipment of a subscriber or user, e.g. websites and apps using cookies or similar technologies.
- **Art. 13** applies to anyone who sends unsolicited communications for direct marketing.

It particularises and complements the general data protection law (Art. 1(2)); references to Directive 95/46/EC are read as references to the GDPR (Art. 94(2) GDPR).

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 12 July 2002 | Adoption |
| 31 July 2002 | Publication and entry into force |
| 31 October 2003 | Transposition deadline |
| 2006 | Directive 2006/24/EC on data retention amends the Directive; it was later declared invalid by the Court of Justice (2014) |
| 2009 | Directive 2009/136/EC amends the Directive (consent rule for terminal equipment, personal data breach notification, penalties); national penalty rules to be notified by 25 May 2011 |
| 2017 | Commission proposal for an ePrivacy Regulation to replace the Directive (COM(2017) 10) |
| 2025 | The Commission announced the withdrawal of the ePrivacy Regulation proposal; the Directive remains in force |

### Enforcement and penalties

- **Through national law**: the Directive has to be transposed; supervision and sanctions follow the national implementing acts. In Germany, the [[tdddg|TDDDG]] implements the provisions on terminal equipment and telemedia, telecommunications-specific rules are contained in the TDDDG and the Telecommunications Act (TKG).
- **Penalties** (Art. 15a): Member States lay down effective, proportionate and dissuasive penalties, including criminal sanctions where appropriate, and give competent national authorities powers to order the cessation of infringements.
- **Breach notification** (Art. 4(3)): providers of publicly available electronic communications services must notify personal data breaches to the competent national authority and, where the breach is likely to adversely affect them, to the subscribers or individuals concerned.

### Relationship to other acts

- **[[gdpr|GDPR]]**: the Directive is the more specific law for electronic communications; the GDPR imposes no additional obligations where the Directive sets specific obligations with the same objective (Art. 95 GDPR). Consent under Art. 5(3) follows the GDPR's definition of consent. Storing or reading information on a device (Art. 5(3)) and the subsequent processing of personal data are two separate questions: the latter still needs a legal basis under the GDPR.
- **[[tdddg|TDDDG]]**: the German implementation; § 25 TDDDG transposes Art. 5(3).
- **[[eecc|European Electronic Communications Code]]**: defines electronic communications services; since its definition also covers number-independent interpersonal communications services (e.g. messaging apps), these are subject to the confidentiality rules as well.
- **ePrivacy Regulation (proposal)**: was intended to replace the Directive; the proposal was withdrawn.

### Relevance for AI development

- **Device storage and tracking** (Art. 5(3)): collecting usage data from websites or apps through cookies, SDKs or device fingerprinting, e.g. to train recommendation or personalisation models, requires the user's consent unless strictly necessary for the requested service.
- **Confidentiality of communications** (Art. 5(1)): analysing the content of communications with AI, e.g. assistants or classifiers operating on messages or calls, is only permitted with the consent of the users concerned or under a legal exception; this covers interpersonal communications services that fall under the Directive.
- **Traffic and location data** (Art. 6 and 9): telecommunications metadata may only be used for value-added services or analysis with consent or after anonymisation, which affects machine learning on such data.
- **Automated marketing** (Art. 13): AI-generated or personalised marketing e-mails and messages need prior consent, apart from the narrow exception for existing customers.
- **Security** (Art. 4): providers must protect their services according to the state of the art, which includes AI components processing communications data.

### Official sources

- Directive 2002/58/EC, Official Journal: [English](https://eur-lex.europa.eu/eli/dir/2002/58/oj/eng) and [German](https://eur-lex.europa.eu/eli/dir/2002/58/oj/deu)
- [Consolidated text of 19 December 2009 (English)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02002L0058-20091219)
