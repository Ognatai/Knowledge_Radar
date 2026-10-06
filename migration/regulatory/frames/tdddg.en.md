> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial translation.

### TL;DR

The Telecommunications Digital Services Data Protection Act (Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz, TDDDG) contains Germany's special privacy rules for telecommunications and digital services. It protects the secrecy of telecommunications, regulates traffic and location data, and in § 25 requires consent before information is stored on or read from a user's device, unless strictly necessary. This is the German basis for cookie banners. The Act implements the [[eprivacy-directive|ePrivacy Directive]] and was called TTDSG until 2024.

### Key facts

| | |
| --- | --- |
| Official reference | Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz, BGBl. I 2021, 1982 |
| Type and jurisdiction | German federal law |
| Enacted | 23 June 2021, as Telekommunikation-Telemedien-Datenschutz-Gesetz (TTDSG) |
| Entry into force | 1 December 2021 |
| Renamed | 14 May 2024 by the Digital Services Act implementation law (Digitale-Dienste-Gesetz); "telemedia" became "digital services" |
| Competent authorities | Federal Commissioner for Data Protection and Freedom of Information (BfDI) for telecommunications (§ 29); Federal Network Agency for Part 2 where the BfDI is not responsible (§ 30); state data protection authorities for digital services (§ 1(1) no. 8) |
| Version summarised | consolidated text, last amended by Article 3 of the Act of 10 March 2026 |

### Scope

**Subject matter** (§ 1(1)): the secrecy of telecommunications; special rules on personal data in telecommunications and digital services; caller identification and call forwarding; directories; technical and organisational measures of digital service providers; disclosure of subscriber and usage data; protection of terminal equipment; and supervision.

**Who** (§ 1(3)): all companies and persons that have an establishment in Germany, provide services there, participate in providing them or place goods on the German market.

**Structure**:

- Part 1 (§§ 1-2): scope and definitions.
- Part 2 (§§ 3-18): telecommunications, i.e. secrecy of telecommunications, traffic and location data, caller identification, directories.
- Part 3 (§§ 19-26): digital services and terminal equipment, including information requests by authorities and the consent rule of § 25.
- Part 4 (§§ 27-30): criminal and fine provisions, supervision.

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 23 June 2021 | Enactment as TTDSG; it merges the data protection rules from the Telecommunications Act (TKG) and the Telemedia Act (TMG) |
| 1 December 2021 | Entry into force |
| 14 May 2024 | Renamed TDDDG by the Digitale-Dienste-Gesetz, which implements the EU Digital Services Act |
| 2025 | Ordinance on recognised consent management services (Einwilligungsverwaltungsverordnung) under § 26 enters into force |

### Enforcement and penalties

- **Supervision**: the BfDI supervises the processing of data for commercially provided telecommunications services and compliance with § 25 by telecommunications providers and federal public bodies (§ 29); the GDPR's investigative and corrective powers (Art. 58 GDPR) apply accordingly. The Federal Network Agency enforces the rest of Part 2 and can impose penalty payments of up to **EUR 1 million** (§ 30). For other digital services, the state data protection authorities are responsible.
- **Fines** (§ 28): up to **EUR 300,000**, among others for storing or accessing information on terminal equipment without consent contrary to § 25(1) and for unlawful processing of traffic data. Lower ceilings of **EUR 100,000**, **EUR 50,000** and **EUR 10,000** apply to other infringements. No fines are imposed on public bodies (§ 28(4)).
- **Criminal offences** (§ 27): up to **2 years** imprisonment, for example for intercepting messages with a radio installation or for producing or selling telecommunications equipment disguised for covert eavesdropping (§ 8).

### Relationship to other acts

- **[[eprivacy-directive|ePrivacy Directive]]**: the TDDDG implements it in German law; § 25 transposes Art. 5(3).
- **[[gdpr|GDPR]]**: information and consent under § 25 follow the GDPR (§ 25(1)). The TDDDG only covers access to the device; any subsequent processing of personal data needs a legal basis under the GDPR.
- **[[bdsg|BDSG]]**: the TDDDG is a specific federal data protection law and takes precedence over the BDSG (§ 1(2) BDSG).
- **Telecommunications Act (TKG)** and **Digitale-Dienste-Gesetz**: contain the general rules for telecommunications and digital services; the country-of-origin principle of § 3 DDG remains unaffected (§ 1(3)).

### Relevance for AI development

- **Collecting usage data** (§ 25): cookies, SDKs, local storage, device fingerprinting or reading device identifiers to collect data, for example to train recommendation or personalisation models, require consent unless strictly necessary for the service the user explicitly requested.
- **On-device AI**: storing models, embeddings or user profiles on a user's device, or reading them from it, also falls under § 25; the exception for strictly necessary storage covers only what the requested service needs.
- **Secrecy of telecommunications** (§ 3): analysing the content of messages or calls with AI, for example spam or fraud detection, is restricted for providers of telecommunications services, including messaging services.
- **Traffic and location data** (§§ 9, 13): traffic data may only be processed for the purposes listed in § 9, such as establishing connections and billing; location data may only be used for value-added services after anonymisation or with consent. This limits analytics and model training on telecommunications metadata.
- **Consent management** (§ 26): recognised consent management services are intended to reduce consent banners; they matter for data collection pipelines that depend on user consent.

### Official sources

- [TDDDG on gesetze-im-internet.de (German)](https://www.gesetze-im-internet.de/ttdsg/)
