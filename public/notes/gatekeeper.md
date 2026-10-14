---
title_en: Gatekeeper (DMA)
title_de: Torwächter (DMA)
entity_type: Concept
aliases:
- Gatekeeper (DMA)
- gatekeeper
- Torwächter
- Gatekeeper platform
sources:
- https://eur-lex.europa.eu/eli/reg/2022/1925/oj/eng
- https://eur-lex.europa.eu/eli/reg/2022/1925/oj/deu
- https://digital-markets-act.ec.europa.eu/gatekeepers_en
---

## EN

> **Important notice:** LLM-generated summary; may be incomplete, outdated or wrong. Not legal advice; only the texts published in the Official Journal are authentic.

### TL;DR

Under the Digital Markets Act (DMA), a gatekeeper is an undertaking that provides core platform services and has been designated by the [[european-commission|European Commission]] (Art. 2(1) DMA). An undertaking is designated if it has a significant impact on the internal market, operates a core platform service that is an important gateway for business users to reach end users, and enjoys an entrenched and durable position; this is presumed above thresholds of €7.5 billion annual EU turnover or €75 billion market capitalisation, 45 million monthly active end users and 10,000 yearly active business users (Art. 3 DMA). Gatekeepers must comply with the obligations of Articles 5 to 7, such as bans on combining personal data across services without consent and on self-preferencing, within six months of designation. Seven companies are designated, with 23 core platform services: [[google|Alphabet]], Amazon, Apple, Booking, ByteDance, Meta and [[microsoft|Microsoft]] (European Commission, 2026). See [[digital-markets-act|Digital Markets Act]] for the full act.

### How it works

```text
undertaking with core platform services (search, social network, OS, browser, cloud, ads, ...)
  │ thresholds met (Art. 3(2))?  ── yes ─► notify Commission within 2 months (Art. 3(3))
  │                                         ► designation within 45 working days (Art. 3(4))
  │                                           (rebuttal possible with substantiated arguments, Art. 3(5))
  │ ── no, but qualitative criteria met ─► market investigation, designation (Art. 3(8), Art. 17)
  ▼
designation decision lists the core platform services (Art. 3(9))
  → obligations of Art. 5, 6, 7 within 6 months (Art. 3(10))
  → review at least every 3 years (Art. 4(2)); fines up to 10 % / 20 % of worldwide turnover (Art. 30)
```

#### 1. Core platform services

The DMA lists ten types of core platform services: online intermediation services, online search engines, online social networking services, video-sharing platform services, number-independent interpersonal communication services, operating systems, web browsers, virtual assistants, cloud computing services and online advertising services offered by a provider of one of the other services (Art. 2(2) DMA). Gatekeeper obligations apply per service listed in the designation decision, not to everything a company does (Art. 3(9), Art. 5(1) DMA).

#### 2. Qualitative criteria and quantitative presumptions

An undertaking is designated as a gatekeeper if it (a) has a significant impact on the internal market, (b) provides a core platform service that is an important gateway for business users to reach end users, and (c) enjoys an entrenched and durable position or will foreseeably do so (Art. 3(1) DMA). These criteria are presumed when the undertaking achieved an annual EU turnover of at least **€7.5 billion** in each of the last three financial years or had an average market capitalisation of at least **€75 billion** in the last financial year and provides the same core platform service in at least three Member States; when the service had at least **45 million** monthly active end users and **10,000** yearly active business users in the EU; and when these user thresholds were met in each of the last three years (Art. 3(2) DMA).

#### 3. Designation procedure

An undertaking that meets all thresholds must notify the Commission within two months; the Commission then designates it within 45 working days after receiving the complete information (Art. 3(3)–(4) DMA). The undertaking can present sufficiently substantiated arguments that it exceptionally does not meet the qualitative criteria despite meeting the thresholds. Conversely, the Commission can designate an undertaking that meets the qualitative criteria without reaching every threshold, after a market investigation, taking into account for example size, numbers of users, network effects and data advantages, lock-in and conglomerate structure (Art. 3(5), (8) DMA).

#### 4. Obligations

Article 5 contains directly applicable obligations: among others, a gatekeeper may not process personal data of end users using third-party services for online advertising, combine or cross-use personal data across its services, or sign users in to other services to combine data, unless the end user has been given a specific choice and has consented under the GDPR (Art. 5(2) DMA). It may not prevent business users from offering different prices via other channels (Art. 5(3)), must let them communicate offers to end users free of charge (Art. 5(4)), and may not require the use of its identification service, browser engine or payment service (Art. 5(7)). Article 6 contains obligations that the Commission may further specify, such as not using non-public data of business users to compete with them (Art. 6(2)), allowing apps to be uninstalled and defaults changed, including choice screens for search engines, virtual assistants and browsers (Art. 6(3)), allowing third-party apps and app stores (Art. 6(4)), not favouring its own products in ranking (Art. 6(5)), data portability for end users (Art. 6(9)), data access for business users (Art. 6(10)) and access to search ranking, query, click and view data for other search engines on fair, reasonable and non-discriminatory terms (Art. 6(11)). Article 7 requires interoperability of basic functions of messaging services (Art. 7 DMA).

#### 5. Ongoing duties and enforcement

Gatekeepers must inform the Commission of every intended concentration in the digital sector (Art. 14 DMA) and submit an independently audited description of their consumer profiling techniques within six months of designation, which the Commission passes on to the European Data Protection Board (Art. 15 DMA). The Commission reviews at least every three years whether gatekeepers still meet the criteria and publishes the list of gatekeepers and their core platform services (Art. 4 DMA). Fines reach up to **10%** of total worldwide turnover, and up to **20%** for repeated infringements (Art. 30 DMA); systematic non-compliance can lead to behavioural or structural remedies (Art. 18 DMA).

#### Origin and variants

The DMA, Regulation (EU) 2022/1925, applies from **2 May 2023** (Art. 54 DMA). On 6 September 2023, the Commission designated Alphabet, Amazon, Apple, ByteDance, Meta and Microsoft; it added Apple's iPadOS on 29 April 2024 and Booking on 13 May 2024, and undesignated Facebook Marketplace on 23 April 2025 (European Commission, 2026). The DMA term differs from the broader economic use of "gatekeeper" and from the "very large online platforms" of the [[digital-services-act|Digital Services Act]], which are defined by user numbers alone.

### When to use it

- Assessing whether a digital service falls under DMA obligations: check the designation decision and the list of core platform services (Art. 3(9), Art. 4(3) DMA).
- Building products on gatekeeper platforms, for example app distribution, data access requests or messaging interoperability (Art. 6–7 DMA).
- Understanding data-use limits of large platforms that train or deploy AI across their services (Art. 5(2) DMA).

### Strengths and limitations

**Strengths**
- Clear, quantitative presumptions make designation predictable (Art. 3(2) DMA).
- Ex-ante obligations apply without a lengthy competition case (Art. 5–7 DMA).
- Rights for business users and end users that can be used directly, such as data portability and data access (Art. 6(9)–(10) DMA).

**Limitations**
- Covers only the listed core platform services of designated undertakings (Art. 3(9) DMA).
- Many Article 6 obligations need further specification and dialogue with the Commission (Art. 6, Art. 8 DMA).
- Generative AI services are not a core platform service type of their own; they are caught only if they form part of or are offered as one of the listed services (Art. 2(2) DMA).

### Comparison

| | Gatekeeper (DMA) | Very large online platform (DSA) |
|---|---|---|
| Purpose | contestable and fair digital markets | safe online environment, systemic risks |
| Criteria | impact, gateway, entrenched position; turnover and user thresholds | at least 45 million monthly active recipients in the EU |
| Obligations | conduct rules on data, self-preferencing, interoperability | risk assessment, mitigation, audits |
| Maximum fine | 10 % (20 % repeat) of worldwide turnover | 6 % of worldwide turnover |

Sources: Art. 3 and 30 DMA; for the DSA see [[digital-services-act|Digital Services Act]].

### In practice

The Commission's register lists for each gatekeeper the exact services designated, for example Google Search, Chrome and Android for Alphabet, or WhatsApp and Messenger for Meta (European Commission, 2026). Developers building on these services can rely on DMA rights such as installing third-party apps and app stores on designated operating systems or requesting data access for business users. Gatekeepers that combine personal data across services, for instance to train or personalise AI features, need the end user's specific consent (Art. 5(2) DMA; [[gdpr|GDPR]]).

### Regulatory context

The DMA complements EU competition law and the GDPR; consent for combining personal data follows Article 4(11) and Article 7 GDPR (Art. 5(2) DMA). Data access rights of Art. 6 DMA sit alongside the sectoral data access rules of the [[data-act|Data Act]].

### Key takeaway

A gatekeeper is a large platform company that the Commission has designated under the DMA for specific core platform services; from then on it must follow conduct rules on data use, self-preferencing, defaults, app distribution and interoperability, under fines of up to 10% of worldwide turnover.

### Sources

- Regulation (EU) 2022/1925 (Digital Markets Act), Official Journal L 265, 12.10.2022. [EUR-Lex (EN)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj/eng), [EUR-Lex (DE)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj/deu)
- European Commission (2026). *Gatekeepers*. Digital Markets Act website. [digital-markets-act.ec.europa.eu](https://digital-markets-act.ec.europa.eu/gatekeepers_en)

## DE

> **Wichtiger Hinweis:** LLM-generierte Zusammenfassung; kann unvollständig, veraltet oder falsch sein. Keine Rechtsberatung; verbindlich sind nur die im Amtsblatt veröffentlichten Texte.

### TL;DR

Nach dem Gesetz über digitale Märkte (Digital Markets Act, DMA) ist ein Torwächter ein Unternehmen, das zentrale Plattformdienste bereitstellt und von der Europäischen Kommission benannt worden ist (Art. 2 Nr. 1 DMA). Ein Unternehmen wird benannt, wenn es erheblichen Einfluss auf den Binnenmarkt hat, einen zentralen Plattformdienst bereitstellt, der gewerblichen Nutzern als wichtiges Zugangstor zu Endnutzern dient, und eine gefestigte und dauerhafte Position innehat; vermutet wird dies oberhalb der Schwellenwerte von 7,5 Mrd. EUR Jahresumsatz in der Union oder 75 Mrd. EUR Marktkapitalisierung, 45 Millionen monatlich aktiven Endnutzern und 10 000 jährlich aktiven gewerblichen Nutzern (Art. 3 DMA). Torwächter müssen die Verpflichtungen der Artikel 5 bis 7, etwa das Verbot, personenbezogene Daten ohne Einwilligung dienstübergreifend zusammenzuführen, und das Verbot der Selbstbevorzugung, binnen sechs Monaten nach der Benennung erfüllen. Benannt sind sieben Unternehmen mit 23 zentralen Plattformdiensten: [[google|Alphabet]], Amazon, Apple, Booking, ByteDance, Meta und [[microsoft|Microsoft]] (European Commission, 2026). Den vollständigen Rechtsakt beschreibt [[digital-markets-act|Digital Markets Act]].

### Funktionsweise

```text
Unternehmen mit zentralen Plattformdiensten (Suche, soziales Netzwerk, Betriebssystem, Browser, Cloud, Werbung, ...)
  │ Schwellenwerte erreicht (Art. 3 Abs. 2)?  ── ja ─► Mitteilung an Kommission binnen 2 Monaten (Art. 3 Abs. 3)
  │                                                    ► Benennung binnen 45 Arbeitstagen (Art. 3 Abs. 4)
  │                                                      (Widerlegung mit substanziierten Argumenten möglich, Art. 3 Abs. 5)
  │ ── nein, aber qualitative Anforderungen erfüllt ─► Marktuntersuchung, Benennung (Art. 3 Abs. 8, Art. 17)
  ▼
Benennungsbeschluss führt die zentralen Plattformdienste auf (Art. 3 Abs. 9)
  → Verpflichtungen aus Art. 5, 6, 7 binnen 6 Monaten (Art. 3 Abs. 10)
  → Überprüfung mindestens alle 3 Jahre (Art. 4 Abs. 2); Geldbußen bis 10 % / 20 % des weltweiten Umsatzes (Art. 30)
```

#### 1. Zentrale Plattformdienste

Der DMA nennt zehn Arten zentraler Plattformdienste: Online-Vermittlungsdienste, Online-Suchmaschinen, Online-Dienste sozialer Netzwerke, Video-Sharing-Plattform-Dienste, nummernunabhängige interpersonelle Kommunikationsdienste, Betriebssysteme, Webbrowser, virtuelle Assistenten, Cloud-Computing-Dienste sowie Online-Werbedienste eines Unternehmens, das einen der übrigen Dienste bereitstellt (Art. 2 Nr. 2 DMA). Die Pflichten der Torwächter gelten je Dienst, der im Benennungsbeschluss aufgeführt ist, nicht für alles, was ein Unternehmen tut (Art. 3 Abs. 9, Art. 5 Abs. 1 DMA).

#### 2. Qualitative Anforderungen und quantitative Vermutungen

Ein Unternehmen wird als Torwächter benannt, wenn es a) erheblichen Einfluss auf den Binnenmarkt hat, b) einen zentralen Plattformdienst bereitstellt, der gewerblichen Nutzern als wichtiges Zugangstor zu Endnutzern dient, und c) eine gefestigte und dauerhafte Position innehat oder absehbar erlangen wird (Art. 3 Abs. 1 DMA). Vermutet werden diese Anforderungen, wenn das Unternehmen in jedem der vergangenen drei Geschäftsjahre in der Union einen Jahresumsatz von mindestens **7,5 Mrd. EUR** erzielt hat oder seine durchschnittliche Marktkapitalisierung im vergangenen Geschäftsjahr mindestens **75 Mrd. EUR** betrug und es in mindestens drei Mitgliedstaaten denselben zentralen Plattformdienst bereitstellt; wenn der Dienst mindestens **45 Millionen** monatlich aktive Endnutzer und **10 000** jährlich aktive gewerbliche Nutzer in der Union hatte; und wenn diese Nutzerschwellen in jedem der vergangenen drei Geschäftsjahre erreicht wurden (Art. 3 Abs. 2 DMA).

#### 3. Benennungsverfahren

Ein Unternehmen, das alle Schwellenwerte erreicht, teilt dies der Kommission binnen zwei Monaten mit; die Kommission benennt es dann spätestens 45 Arbeitstage nach Erhalt der vollständigen Angaben (Art. 3 Abs. 3–4 DMA). Das Unternehmen kann hinreichend substanziierte Argumente vorbringen, dass es trotz erreichter Schwellenwerte die qualitativen Anforderungen ausnahmsweise nicht erfüllt. Umgekehrt kann die Kommission ein Unternehmen, das die qualitativen Anforderungen erfüllt, aber nicht jeden Schwellenwert erreicht, nach einer Marktuntersuchung benennen und dabei etwa Größe, Nutzerzahlen, Netzwerkeffekte und Datenvorteile, Bindungseffekte und konglomeratsartige Strukturen berücksichtigen (Art. 3 Abs. 5, 8 DMA).

#### 4. Verpflichtungen

Artikel 5 enthält unmittelbar geltende Verpflichtungen: Unter anderem darf ein Torwächter personenbezogene Daten von Endnutzern, die Dienste Dritter nutzen, nicht für Online-Werbedienste verarbeiten, personenbezogene Daten nicht dienstübergreifend zusammenführen oder weiterverwenden und Endnutzer nicht in anderen Diensten anmelden, um Daten zusammenzuführen, außer der Endnutzer hatte die spezifische Wahl und hat nach der DSGVO eingewilligt (Art. 5 Abs. 2 DMA). Er darf gewerbliche Nutzer nicht hindern, über andere Kanäle andere Preise anzubieten (Art. 5 Abs. 3), muss ihnen ermöglichen, Endnutzern kostenlos Angebote zu kommunizieren (Art. 5 Abs. 4), und darf die Nutzung seines Identifizierungsdienstes, seiner Webbrowser-Engine oder seines Zahlungsdienstes nicht verlangen (Art. 5 Abs. 7). Artikel 6 enthält Verpflichtungen, die die Kommission näher ausführen kann, etwa keine nicht öffentlich zugänglichen Daten gewerblicher Nutzer im Wettbewerb mit ihnen zu verwenden (Art. 6 Abs. 2), Deinstallation von Software-Anwendungen und Änderung von Standardeinstellungen samt Auswahlbildschirmen für Suchmaschinen, virtuelle Assistenten und Webbrowser zu ermöglichen (Art. 6 Abs. 3), Software-Anwendungen und Geschäfte Dritter zuzulassen (Art. 6 Abs. 4), eigene Angebote beim Ranking nicht zu bevorzugen (Art. 6 Abs. 5), Endnutzern Datenübertragbarkeit (Art. 6 Abs. 9) und gewerblichen Nutzern Datenzugang zu gewähren (Art. 6 Abs. 10) sowie anderen Suchmaschinen zu fairen, zumutbaren und diskriminierungsfreien Bedingungen Zugang zu Ranking-, Anfrage-, Klick- und Ansichtsdaten zu geben (Art. 6 Abs. 11). Artikel 7 verlangt Interoperabilität grundlegender Funktionen von Nachrichtendiensten (Art. 7 DMA).

#### 5. Laufende Pflichten und Durchsetzung

Torwächter unterrichten die Kommission über jeden geplanten Zusammenschluss im digitalen Sektor (Art. 14 DMA) und legen binnen sechs Monaten nach der Benennung eine von unabhängiger Stelle geprüfte Beschreibung ihrer Techniken zum Verbraucher-Profiling vor, die die Kommission dem Europäischen Datenschutzausschuss übermittelt (Art. 15 DMA). Die Kommission überprüft mindestens alle drei Jahre, ob die Torwächter die Anforderungen noch erfüllen, und veröffentlicht die Liste der Torwächter und ihrer zentralen Plattformdienste (Art. 4 DMA). Geldbußen betragen bis zu **10 %** des weltweiten Gesamtumsatzes, bei wiederholten Zuwiderhandlungen bis zu **20 %** (Art. 30 DMA); systematische Nichteinhaltung kann zu verhaltensbezogenen oder strukturellen Abhilfemaßnahmen führen (Art. 18 DMA).

#### Herkunft und Varianten

Der DMA, Verordnung (EU) 2022/1925, gilt ab dem **2. Mai 2023** (Art. 54 DMA). Am 6. September 2023 benannte die Kommission Alphabet, Amazon, Apple, ByteDance, Meta und Microsoft; am 29. April 2024 kam Apples iPadOS hinzu, am 13. Mai 2024 Booking, und am 23. April 2025 wurde die Benennung für Facebook Marketplace aufgehoben (European Commission, 2026). Der Begriff des DMA unterscheidet sich vom weiteren ökonomischen Sprachgebrauch und von den „sehr großen Online-Plattformen“ des [[digital-services-act|Digital Services Act]], die allein über Nutzerzahlen bestimmt werden.

### Wann einsetzen

- Prüfung, ob ein digitaler Dienst unter die Pflichten des DMA fällt: Benennungsbeschluss und Liste der zentralen Plattformdienste prüfen (Art. 3 Abs. 9, Art. 4 Abs. 3 DMA).
- Entwicklung von Produkten auf Torwächter-Plattformen, etwa App-Vertrieb, Anträge auf Datenzugang oder Interoperabilität von Nachrichtendiensten (Art. 6–7 DMA).
- Verständnis der Grenzen der Datennutzung großer Plattformen, die KI dienstübergreifend trainieren oder einsetzen (Art. 5 Abs. 2 DMA).

### Stärken und Grenzen

**Stärken**
- Klare quantitative Vermutungen machen die Benennung vorhersehbar (Art. 3 Abs. 2 DMA).
- Vorab geltende Verpflichtungen greifen ohne langwieriges Wettbewerbsverfahren (Art. 5–7 DMA).
- Unmittelbar nutzbare Rechte für gewerbliche Nutzer und Endnutzer, etwa Datenübertragbarkeit und Datenzugang (Art. 6 Abs. 9–10 DMA).

**Grenzen**
- Erfasst nur die aufgeführten zentralen Plattformdienste benannter Unternehmen (Art. 3 Abs. 9 DMA).
- Viele Verpflichtungen aus Artikel 6 brauchen nähere Ausführung und den Dialog mit der Kommission (Art. 6, Art. 8 DMA).
- Generative KI-Dienste sind keine eigene Art zentraler Plattformdienste; sie werden nur erfasst, wenn sie Teil eines der aufgeführten Dienste sind oder als solcher angeboten werden (Art. 2 Nr. 2 DMA).

### Vergleich

| | Torwächter (DMA) | Sehr große Online-Plattform (DSA) |
|---|---|---|
| Zweck | bestreitbare und faire digitale Märkte | sicheres Online-Umfeld, systemische Risiken |
| Kriterien | Einfluss, Zugangstor, gefestigte Position; Umsatz- und Nutzerschwellen | mindestens 45 Millionen monatlich aktive Nutzer in der Union |
| Pflichten | Verhaltensregeln zu Daten, Selbstbevorzugung, Interoperabilität | Risikobewertung, Risikominderung, Prüfungen |
| Höchstbuße | 10 % (20 % bei Wiederholung) des weltweiten Umsatzes | 6 % des weltweiten Umsatzes |

Quellen: Art. 3 und 30 DMA; zum DSA siehe [[digital-services-act|Digital Services Act]].

### In der Praxis

Das Register der Kommission führt für jeden Torwächter die genau benannten Dienste auf, etwa Google Search, Chrome und Android für Alphabet oder WhatsApp und Messenger für Meta (European Commission, 2026). Wer auf diesen Diensten entwickelt, kann sich auf Rechte aus dem DMA stützen, etwa die Installation von Software-Anwendungen und Geschäften Dritter auf benannten Betriebssystemen oder Anträge auf Datenzugang als gewerblicher Nutzer. Torwächter, die personenbezogene Daten dienstübergreifend zusammenführen, etwa um KI-Funktionen zu trainieren oder zu personalisieren, brauchen die spezifische Einwilligung der Endnutzer (Art. 5 Abs. 2 DMA; [[gdpr|DSGVO]]).

### Regulatorischer Kontext

Der DMA ergänzt das EU-Wettbewerbsrecht und die DSGVO; die Einwilligung zur Zusammenführung personenbezogener Daten richtet sich nach Artikel 4 Nummer 11 und Artikel 7 DSGVO (Art. 5 Abs. 2 DMA). Die Datenzugangsrechte aus Art. 6 DMA stehen neben den Regeln des [[data-act|Data Act]].

### Merksatz

Ein Torwächter ist ein großes Plattformunternehmen, das die Kommission nach dem DMA für bestimmte zentrale Plattformdienste benannt hat; von da an gelten Verhaltensregeln zu Datennutzung, Selbstbevorzugung, Standardeinstellungen, App-Vertrieb und Interoperabilität, bei Geldbußen bis zu 10 % des weltweiten Umsatzes.

### Quellen

- Verordnung (EU) 2022/1925 (Gesetz über digitale Märkte), ABl. L 265 vom 12.10.2022. [EUR-Lex (EN)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj/eng), [EUR-Lex (DE)](https://eur-lex.europa.eu/eli/reg/2022/1925/oj/deu)
- European Commission (2026). *Gatekeepers*. Website zum Digital Markets Act. [digital-markets-act.ec.europa.eu](https://digital-markets-act.ec.europa.eu/gatekeepers_en)
