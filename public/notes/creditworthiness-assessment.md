---
title_en: Creditworthiness Assessment
title_de: Kreditwürdigkeitsprüfung
entity_type: Concept
aliases:
- Creditworthiness assessment
- Kreditwürdigkeitsprüfung
- Credit scoring of consumers
- Bonitätsprüfung
sources:
- https://www.gesetze-im-internet.de/bgb/__505a.html
- https://www.gesetze-im-internet.de/kredwg/__18a.html
- https://eur-lex.europa.eu/eli/dir/2023/2225/oj/deu
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj/deu
- https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62021CJ0634
---

## EN

> **Important notice:** LLM-generated summary; may be incomplete, outdated or wrong. Not legal advice; only the official texts are authentic. The English version summarises the German and EU texts.

### TL;DR

Before concluding a consumer credit agreement, a lender in Germany must assess the borrower's creditworthiness and may only conclude the contract if, for general consumer loans, there are no significant doubts, and for residential property loans, it is likely that the borrower will meet their obligations (§ 505a BGB; for credit institutions also § 18a KWG). The assessment rests on information from the borrower and, where necessary, from credit agencies; for property loans it must be thorough and based on income, expenses and other financial circumstances, not mainly on the value of the property (§ 505b BGB). If the lender breaches the duty, the agreed interest rate is reduced to a market reference rate and the borrower can terminate without compensation (§ 505d BGB). The revised Consumer Credit Directive adds a right to human intervention and explanation for automated assessments (Art. 18 Directive (EU) 2023/2225), the [[eu-ai-act|AI Act]] classifies AI systems for creditworthiness assessment of natural persons as high-risk (Annex III point 5(b)), and the CJEU held that an automatically generated credit score can itself be an automated decision under Article 22 GDPR (CJEU, C-634/21).

### How it works

```text
credit application (consumer)
  │ information: borrower's own data + credit agency data (e.g. score)       § 505b(1) BGB, § 18a(3) KWG
  │ property loans: income, expenses, other circumstances; verify documents   § 505b(2)–(3) BGB
  ▼
assessment (manual, scorecard or ML model)  → documented procedures           § 505b(4) BGB, § 18a(5) KWG
  │ general loan: no significant doubts?   property loan: repayment likely?   § 505a(1) BGB
  ├─ yes → contract may be concluded
  └─ no  → must not be concluded; breach → interest cut, free termination   § 505d BGB
AI-based scoring of natural persons → high-risk AI system (AI Act Annex III 5(b))
automated assessment → human intervention, explanation, review (CCD2 Art. 18(8), from 20 Nov 2026)
```

#### 1. Duty to assess and to refuse

The lender must assess the borrower's creditworthiness before concluding a consumer credit agreement (§ 505a Abs. 1 BGB). For a general consumer credit agreement, it may conclude the contract only if there are no significant doubts; for a residential property credit agreement, only if it is likely that the borrower will meet the obligations under the contract (§ 505a Abs. 1 BGB). If the net loan amount is increased significantly after conclusion, creditworthiness must be reassessed on an updated basis (§ 505a Abs. 2 BGB). Credit institutions are bound by the same duties under banking supervisory law (§ 18a Abs. 1–2 KWG; [[kwg|KWG]]).

#### 2. Basis of the assessment

For general consumer loans, the assessment can rest on information from the borrower and, where necessary, from agencies that commercially collect personal data that may be used to assess consumers' creditworthiness (§ 505b Abs. 1 BGB). For property loans, the lender must assess thoroughly on the basis of necessary, sufficient and proportionate information on income, expenses and other financial and economic circumstances; the assessment may not rely mainly on the property value exceeding the loan amount or on expected increases in value, unless the loan finances construction or renovation (§ 505b Abs. 2 BGB). The information must be verified appropriately, if necessary with independently verifiable documents, and the procedures and data must be defined, documented and retained (§ 505b Abs. 3–4 BGB; § 18a Abs. 3, 5 KWG).

#### 3. Consequences of a breach

If the lender breaches the duty, an agreed fixed borrowing rate is reduced to the market rate for mortgage and public Pfandbriefe of matching maturity, and a variable rate to the three-month interbank rate in euro; the borrower can terminate at any time without early repayment compensation (§ 505d Abs. 1 BGB). The lender cannot claim damages for breaches by the borrower that a proper assessment would have revealed (§ 505d Abs. 2 BGB). These consequences do not apply if a proper assessment would have allowed the contract, or if the borrower intentionally or grossly negligently gave false information or withheld it (§ 505d Abs. 1, 3 BGB).

#### 4. Automated and AI-based assessment

The revised Consumer Credit Directive, to be applied from **20 November 2026**, requires a thorough assessment in the consumer's interest to prevent irresponsible lending and over-indebtedness, excludes special categories of personal data under Article 9 GDPR and states that social networks are not external sources (Art. 18 Abs. 1, 3, Art. 48 Directive (EU) 2023/2225). Where the assessment involves automated processing, consumers have the right to request human intervention, including a clear and comprehensible explanation of the assessment and of the logic and risks of the automated processing, to express their point of view and to request a review of the decision (Art. 18 Abs. 8 Directive (EU) 2023/2225). The AI Act lists AI systems intended to evaluate the creditworthiness of natural persons or establish their credit score, except fraud detection, as high-risk (Annex III point 5(b) Regulation (EU) 2024/1689). The CJEU ruled that the automated establishment of a probability value about a person's ability to meet future payment obligations by a credit agency is an "automated individual decision" under Article 22(1) GDPR if a third party to whom it is transmitted draws strongly on it to establish, implement or terminate a contract (CJEU, C-634/21).

#### Origin and variants

The German duties in §§ 505a–505d BGB and § 18a KWG distinguish general consumer credit from residential property credit, reflecting separate EU rules for the two. Directive (EU) 2023/2225 repeals Directive 2008/48/EC with effect from 20 November 2026 and had to be transposed by 20 November 2025 (Art. 47, 48 Directive (EU) 2023/2225). Supervisory expectations for credit processes in banks are set out by the [[eba|EBA]] and by [[bafin|BaFin]] in [[marisk|MaRisk]].

### When to use it

- Designing credit decision processes and scorecards for consumer loans (§§ 505a–505b BGB; [[classification|classification]]).
- Building or buying ML models for credit scoring of natural persons, which are high-risk AI systems (AI Act Annex III point 5(b); [[eu-ai-act|AI Act]]).
- Handling automated decisions and explanation requests from applicants (Art. 18 Abs. 8 Directive (EU) 2023/2225; Art. 22 GDPR; [[explainable-ai|explainable AI]]).

### Strengths and limitations

**Strengths**
- Protects consumers from over-indebtedness and lenders from bad loans by requiring a documented, verifiable assessment (§ 505b BGB).
- Clear civil-law sanctions give the duty practical force (§ 505d BGB).
- New rights to human review and explanation counter opaque automated scoring (Art. 18 Abs. 8 Directive (EU) 2023/2225).

**Limitations**
- "No significant doubts" for general loans leaves room for interpretation (§ 505a Abs. 1 BGB).
- Credit agency scores can be decisive without the lender knowing their logic, which the SCHUFA ruling addresses through Art. 22 GDPR (CJEU, C-634/21).
- Several regimes overlap: civil law, banking supervision, data protection and AI regulation each add requirements.

### Comparison

| Source | Requirement | Applies to |
|---|---|---|
| § 505a–505d BGB | assess before contract; refuse if negative; sanctions | all lenders of consumer credit |
| § 18a KWG | same duties plus documentation under banking supervision | credit institutions |
| Art. 18 Directive (EU) 2023/2225 | thorough assessment, no Art. 9 GDPR data, human intervention for automated assessment | lenders, from 20 Nov 2026 via national law |
| AI Act Annex III 5(b) | high-risk requirements for AI scoring | providers and deployers of such AI systems |
| Art. 22 GDPR (C-634/21) | limits on automated decisions, including scores | credit agencies and lenders |

Sources: as listed in the table.

### In practice

Document which data feed the decision, verify income and expenses for property loans, and keep the procedure reproducible for supervisors (§ 505b BGB; § 18a KWG). Models for scoring natural persons need the risk management, [[data-governance|data governance]], documentation, human oversight and accuracy requirements of high-risk AI systems, which the AI Act applies to Annex III systems from 2 December 2027 after the Digital Omnibus postponement ([[eu-ai-act|AI Act]]). Avoid special categories of data and social network data as inputs, offer a human review path with an understandable explanation, and test models for unfair differences between groups ([[fairness-metrics|fairness metrics]]).

### Regulatory context

Creditworthiness assessment links consumer credit law ([[kwg|KWG]], BGB), banking supervision ([[bafin|BaFin]], [[eba|EBA]]), data protection ([[gdpr|GDPR]], [[bdsg|BDSG]] on scoring) and AI regulation ([[eu-ai-act|AI Act]]).

### Key takeaway

Lenders must check, document and justify a consumer's ability to repay before granting credit, and may not lend if the check is negative; when the check is automated or AI-based, high-risk AI rules, GDPR limits on automated decisions and, from November 2026, rights to human review and explanation apply.

### Sources

- Bürgerliches Gesetzbuch (BGB), §§ 505a–505d. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bgb/__505a.html)
- Gesetz über das Kreditwesen (Kreditwesengesetz – KWG), § 18a. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kredwg/__18a.html)
- Directive (EU) 2023/2225 on credit agreements for consumers, Art. 18, 47, 48. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2023/2225/oj/deu)
- Regulation (EU) 2024/1689 (AI Act), Annex III point 5(b). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/deu)
- CJEU, judgment of 7 December 2023, C-634/21 (SCHUFA Holding, Scoring). [EUR-Lex](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62021CJ0634)

## DE

> **Wichtiger Hinweis:** LLM-generierte Zusammenfassung; kann unvollständig, veraltet oder falsch sein. Keine Rechtsberatung; verbindlich sind nur die amtlichen Texte.

### TL;DR

Vor dem Abschluss eines Verbraucherdarlehensvertrags muss der Darlehensgeber in Deutschland die Kreditwürdigkeit des Darlehensnehmers prüfen und darf den Vertrag nur abschließen, wenn bei einem Allgemein-Verbraucherdarlehensvertrag keine erheblichen Zweifel bestehen und es bei einem Immobiliar-Verbraucherdarlehensvertrag wahrscheinlich ist, dass der Darlehensnehmer seinen Verpflichtungen vertragsgemäß nachkommen wird (§ 505a BGB; für Kreditinstitute zudem § 18a KWG). Grundlage sind Auskünfte des Darlehensnehmers und erforderlichenfalls von Auskunfteien; bei Immobiliardarlehen ist eingehend auf Basis von Einkommen, Ausgaben und weiteren finanziellen Umständen zu prüfen, nicht hauptsächlich anhand des Immobilienwerts (§ 505b BGB). Verstößt der Darlehensgeber gegen die Pflicht, ermäßigt sich der vereinbarte Sollzins auf einen marktüblichen Referenzzins, und der Darlehensnehmer kann ohne Vorfälligkeitsentschädigung kündigen (§ 505d BGB). Die neue Verbraucherkreditrichtlinie ergänzt für automatisierte Prüfungen ein Recht auf menschliches Eingreifen und Erläuterung (Art. 18 Richtlinie (EU) 2023/2225), die [[eu-ai-act|KI-Verordnung]] stuft KI-Systeme zur Kreditwürdigkeitsprüfung natürlicher Personen als hochriskant ein (Anhang III Nummer 5 Buchstabe b), und der EuGH entschied, dass ein automatisiert erstellter Score selbst eine automatisierte Entscheidung nach Artikel 22 DSGVO sein kann (EuGH, C-634/21).

### Funktionsweise

```text
Kreditantrag (Verbraucher)
  │ Informationen: Angaben des Darlehensnehmers + Auskunfteidaten (z. B. Score)      § 505b Abs. 1 BGB, § 18a Abs. 3 KWG
  │ Immobiliardarlehen: Einkommen, Ausgaben, weitere Umstände; Unterlagen prüfen       § 505b Abs. 2–3 BGB
  ▼
Prüfung (manuell, Scorekarte oder ML-Modell) → dokumentierte Verfahren              § 505b Abs. 4 BGB, § 18a Abs. 5 KWG
  │ Allgemein-Darlehen: keine erheblichen Zweifel?  Immobiliardarlehen: Rückzahlung wahrscheinlich?   § 505a Abs. 1 BGB
  ├─ ja   → Vertrag darf geschlossen werden
  └─ nein → darf nicht geschlossen werden; Verstoß → Zinsminderung, fristlose Kündigung   § 505d BGB
KI-gestützte Bonitätsbewertung natürlicher Personen → Hochrisiko-KI-System (KI-VO Anhang III Nr. 5 b)
automatisierte Prüfung → menschliches Eingreifen, Erläuterung, Überprüfung (VKR Art. 18 Abs. 8, ab 20.11.2026)
```

#### 1. Prüfpflicht und Abschlussverbot

Der Darlehensgeber hat vor dem Abschluss eines Verbraucherdarlehensvertrags die Kreditwürdigkeit des Darlehensnehmers zu prüfen (§ 505a Abs. 1 BGB). Bei einem Allgemein-Verbraucherdarlehensvertrag darf er den Vertrag nur abschließen, wenn keine erheblichen Zweifel bestehen; bei einem Immobiliar-Verbraucherdarlehensvertrag nur, wenn es wahrscheinlich ist, dass der Darlehensnehmer seinen Verpflichtungen aus dem Vertrag vertragsgemäß nachkommen wird (§ 505a Abs. 1 BGB). Wird der Nettodarlehensbetrag nach Vertragsschluss deutlich erhöht, ist die Kreditwürdigkeit auf aktualisierter Grundlage neu zu prüfen (§ 505a Abs. 2 BGB). Kreditinstitute treffen dieselben Pflichten zudem aufsichtsrechtlich (§ 18a Abs. 1–2 KWG; [[kwg|KWG]]).

#### 2. Grundlage der Prüfung

Bei Allgemein-Verbraucherdarlehensverträgen können Grundlage der Prüfung Auskünfte des Darlehensnehmers und erforderlichenfalls Auskünfte von Stellen sein, die geschäftsmäßig personenbezogene Daten, die zur Bewertung der Kreditwürdigkeit von Verbrauchern genutzt werden dürfen, zum Zweck der Übermittlung erheben, speichern, verändern oder nutzen (§ 505b Abs. 1 BGB). Bei Immobiliar-Verbraucherdarlehensverträgen hat der Darlehensgeber auf der Grundlage notwendiger, ausreichender und angemessener Informationen zu Einkommen, Ausgaben sowie anderen finanziellen und wirtschaftlichen Umständen eingehend zu prüfen; die Prüfung darf sich nicht hauptsächlich darauf stützen, dass der Wert der Wohnimmobilie den Darlehensbetrag übersteigt, oder auf eine erwartete Wertsteigerung, es sei denn, das Darlehen dient dem Bau oder der Renovierung (§ 505b Abs. 2 BGB). Die Informationen sind in angemessener Weise zu überprüfen, erforderlichenfalls durch Einsichtnahme in unabhängig nachprüfbare Unterlagen, und Verfahren und Angaben sind festzulegen, zu dokumentieren und aufzubewahren (§ 505b Abs. 3–4 BGB; § 18a Abs. 3, 5 KWG).

#### 3. Folgen eines Verstoßes

Verstößt der Darlehensgeber gegen die Prüfpflicht, ermäßigt sich ein vereinbarter gebundener Sollzins auf den marktüblichen Zinssatz für Hypothekenpfandbriefe und öffentliche Pfandbriefe entsprechender Laufzeit und ein veränderlicher Sollzins auf den marktüblichen Zinssatz, zu dem europäische Banken einander Anleihen in Euro mit drei Monaten Laufzeit gewähren; der Darlehensnehmer kann jederzeit fristlos kündigen, ohne Vorfälligkeitsentschädigung (§ 505d Abs. 1 BGB). Der Darlehensgeber kann keine Ansprüche wegen Pflichtverletzungen des Darlehensnehmers geltend machen, die eine ordnungsgemäße Prüfung aufgedeckt hätte (§ 505d Abs. 2 BGB). Diese Folgen entfallen, wenn der Vertrag auch bei ordnungsgemäßer Prüfung hätte geschlossen werden dürfen oder wenn der Darlehensnehmer vorsätzlich oder grob fahrlässig unrichtige Informationen erteilt oder Informationen vorenthalten hat (§ 505d Abs. 1, 3 BGB).

#### 4. Automatisierte und KI-gestützte Prüfung

Die neue Verbraucherkreditrichtlinie, deren Umsetzungsvorschriften ab dem **20. November 2026** anzuwenden sind, verlangt eine eingehende Prüfung im Interesse des Verbrauchers, um unverantwortliche Kreditvergabe und Überschuldung zu verhindern, schließt besondere Kategorien personenbezogener Daten nach Artikel 9 DSGVO aus und bestimmt, dass soziale Netzwerke nicht als externe Quellen gelten (Art. 18 Abs. 1, 3, Art. 48 Richtlinie (EU) 2023/2225). Beinhaltet die Prüfung eine automatisierte Verarbeitung, hat der Verbraucher das Recht, das Eingreifen einer Person aufseiten des Kreditgebers zu verlangen, einschließlich klarer und verständlicher Erläuterungen zur Prüfung sowie zur Logik und zu den Risiken der automatisierten Verarbeitung, den eigenen Standpunkt darzulegen und eine Überprüfung der Entscheidung zu verlangen (Art. 18 Abs. 8 Richtlinie (EU) 2023/2225). Die KI-Verordnung führt KI-Systeme, die bestimmungsgemäß für die Kreditwürdigkeitsprüfung und Bonitätsbewertung natürlicher Personen verwendet werden sollen, mit Ausnahme der Aufdeckung von Finanzbetrug, als hochriskant auf (Anhang III Nummer 5 Buchstabe b Verordnung (EU) 2024/1689). Der EuGH entschied, dass eine „automatisierte Entscheidung im Einzelfall“ im Sinne von Artikel 22 Absatz 1 DSGVO vorliegt, wenn ein auf personenbezogene Daten gestützter Wahrscheinlichkeitswert zur Fähigkeit einer Person, künftige Zahlungsverpflichtungen zu erfüllen, durch eine Wirtschaftsauskunftei automatisiert erstellt wird und ein Dritter, dem dieser Wert übermittelt wird, maßgeblich davon abhängig macht, ob er ein Vertragsverhältnis begründet, durchführt oder beendet (EuGH, C-634/21).

#### Herkunft und Varianten

Die deutschen Pflichten in §§ 505a–505d BGB und § 18a KWG unterscheiden Allgemein- und Immobiliar-Verbraucherdarlehen, entsprechend getrennten EU-Vorgaben für beide. Die Richtlinie (EU) 2023/2225 hebt die Richtlinie 2008/48/EG mit Wirkung vom 20. November 2026 auf und war bis zum 20. November 2025 umzusetzen (Art. 47, 48 Richtlinie (EU) 2023/2225). Aufsichtliche Erwartungen an Kreditprozesse in Banken formulieren die [[eba|EBA]] und die [[bafin|BaFin]] in den [[marisk|MaRisk]].

### Wann einsetzen

- Gestaltung von Kreditentscheidungsprozessen und Scorekarten für Verbraucherdarlehen (§§ 505a–505b BGB; [[classification|Klassifikation]]).
- Entwicklung oder Einkauf von ML-Modellen für die Bonitätsbewertung natürlicher Personen, die Hochrisiko-KI-Systeme sind (KI-VO Anhang III Nr. 5 Buchstabe b; [[eu-ai-act|KI-Verordnung]]).
- Umgang mit automatisierten Entscheidungen und Erläuterungswünschen von Antragstellenden (Art. 18 Abs. 8 Richtlinie (EU) 2023/2225; Art. 22 DSGVO; [[explainable-ai|Explainable AI]]).

### Stärken und Grenzen

**Stärken**
- Schützt Verbraucher vor Überschuldung und Darlehensgeber vor Ausfällen, indem eine dokumentierte, überprüfbare Prüfung verlangt wird (§ 505b BGB).
- Klare zivilrechtliche Sanktionen verschaffen der Pflicht praktische Wirkung (§ 505d BGB).
- Neue Rechte auf menschliche Überprüfung und Erläuterung wirken undurchsichtigem automatisiertem Scoring entgegen (Art. 18 Abs. 8 Richtlinie (EU) 2023/2225).

**Grenzen**
- „Keine erheblichen Zweifel“ bei Allgemein-Darlehen lässt Auslegungsspielraum (§ 505a Abs. 1 BGB).
- Auskunfteiscores können entscheidend sein, ohne dass der Darlehensgeber ihre Logik kennt; das SCHUFA-Urteil greift dies über Art. 22 DSGVO auf (EuGH, C-634/21).
- Mehrere Regelwerke überlagern sich: Zivilrecht, Bankenaufsicht, Datenschutz und KI-Regulierung stellen jeweils eigene Anforderungen.

### Vergleich

| Quelle | Anforderung | Gilt für |
|---|---|---|
| §§ 505a–505d BGB | Prüfung vor Vertragsschluss; Abschlussverbot bei negativem Ergebnis; Sanktionen | alle Darlehensgeber bei Verbraucherdarlehen |
| § 18a KWG | dieselben Pflichten plus Dokumentation im Aufsichtsrecht | Kreditinstitute |
| Art. 18 Richtlinie (EU) 2023/2225 | eingehende Prüfung, keine Daten nach Art. 9 DSGVO, menschliches Eingreifen bei automatisierter Prüfung | Kreditgeber, ab 20.11.2026 über nationales Recht |
| KI-VO Anhang III Nr. 5 b | Hochrisiko-Anforderungen an KI-Scoring | Anbieter und Betreiber solcher KI-Systeme |
| Art. 22 DSGVO (C-634/21) | Grenzen automatisierter Entscheidungen, auch für Scores | Auskunfteien und Darlehensgeber |

Quellen: wie in der Tabelle angegeben.

### In der Praxis

Zu dokumentieren ist, welche Daten in die Entscheidung einfließen; bei Immobiliardarlehen sind Einkommen und Ausgaben zu prüfen, und das Verfahren muss für die Aufsicht nachvollziehbar bleiben (§ 505b BGB; § 18a KWG). Modelle zur Bonitätsbewertung natürlicher Personen brauchen die Anforderungen an Hochrisiko-KI-Systeme zu Risikomanagement, [[data-governance|Data Governance]], Dokumentation, menschlicher Aufsicht und Genauigkeit, die die KI-Verordnung nach der Verschiebung durch den Digital-Omnibus ab dem 2. Dezember 2027 auf Systeme nach Anhang III anwendet ([[eu-ai-act|KI-Verordnung]]). Besondere Kategorien personenbezogener Daten und Daten aus sozialen Netzwerken sollten nicht als Eingaben dienen; ein Weg zur menschlichen Überprüfung mit verständlicher Erläuterung gehört dazu, ebenso Tests auf unfaire Unterschiede zwischen Gruppen ([[fairness-metrics|Fairness-Metriken]]).

### Regulatorischer Kontext

Die Kreditwürdigkeitsprüfung verbindet Verbraucherkreditrecht ([[kwg|KWG]], BGB), Bankenaufsicht ([[bafin|BaFin]], [[eba|EBA]]), Datenschutz ([[gdpr|DSGVO]], [[bdsg|BDSG]] zum Scoring) und KI-Regulierung ([[eu-ai-act|KI-Verordnung]]).

### Merksatz

Darlehensgeber müssen vor der Kreditvergabe die Rückzahlungsfähigkeit eines Verbrauchers prüfen, dokumentieren und begründen und dürfen bei negativem Ergebnis keinen Kredit gewähren; erfolgt die Prüfung automatisiert oder KI-gestützt, greifen Hochrisiko-Regeln der KI-Verordnung, die Grenzen der DSGVO für automatisierte Entscheidungen und ab November 2026 Rechte auf menschliche Überprüfung und Erläuterung.

### Quellen

- Bürgerliches Gesetzbuch (BGB), §§ 505a–505d. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bgb/__505a.html)
- Gesetz über das Kreditwesen (Kreditwesengesetz – KWG), § 18a. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kredwg/__18a.html)
- Richtlinie (EU) 2023/2225 über Verbraucherkreditverträge, Art. 18, 47, 48. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2023/2225/oj/deu)
- Verordnung (EU) 2024/1689 (KI-Verordnung), Anhang III Nummer 5 Buchstabe b. [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/deu)
- EuGH, Urteil vom 7. Dezember 2023, C-634/21 (SCHUFA Holding, Scoring). [EUR-Lex](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62021CJ0634)
