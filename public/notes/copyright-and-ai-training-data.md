---
title_en: Copyright and AI Training Data
title_de: Urheberrecht und KI-Trainingsdaten
entity_type: Concept
sources:
- https://eur-lex.europa.eu/eli/dir/2019/790/oj
- https://www.gesetze-im-internet.de/urhg/__44b.html
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- https://medien-internet-und-recht.de/volltext.php?mir_dok_id=3526
- https://www.lto.de/recht/nachrichten/n/42o1413924-lg-muenchen-i-gema-openai-chatgpt-songtexte-ki
- https://www.law.cornell.edu/uscode/text/17/107
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Copying copyright-protected works to train an AI model is a reproduction that needs a legal exception or a licence. In the EU, the DSM Directive (2019) provides two text and data mining (TDM) exceptions: one for any purpose, which rightholders can exclude through a machine-readable reservation, and one for scientific research without an opt-out. The [[eu-ai-act|EU AI Act]] requires providers of general-purpose AI models to respect such reservations and to publish a summary of their training content. German courts have so far upheld dataset creation under the TDM exceptions but treated works memorised in a model as reproductions that the exceptions do not cover; neither ruling is final.

### How it works

The legal assessment follows the life cycle of training data: copies are made to collect and analyse works, an exception must cover them, providers of general-purpose models have additional AI Act obligations, and what the trained model stores and outputs is assessed separately.

```text
1. Training copies are reproductions; TDM is automated analysis
▼
2. Commercial TDM: allowed unless a machine-readable reservation exists
▼
3. Research TDM: research organisations, no opt-out
▼
4. AI Act: copyright policy and public training-content summary
▼
5. Memorisation and outputs: separate infringement question
```

#### 1. Training copies as reproductions and the definition of TDM

Collecting and processing works for training involves reproductions, which are permitted only with the rightholder's consent or under an exception. The DSM Directive (2019) defines text and data mining as any automated analytical technique aimed at analysing text and data in digital form to generate information such as patterns, trends and correlations (Art. 2(2)); § 44b(1) UrhG uses an equivalent definition (§§ 44b, 60d UrhG). Training an AI model on a large corpus falls under this definition, which is why the TDM exceptions are the central legal basis for training data in the EU.

#### 2. Commercial TDM exception and the opt-out

§ 44b UrhG, which transposes Art. 4 DSM Directive (2019), permits reproductions of lawfully accessible works for TDM for any purpose, including commercial ones; the copies must be deleted once they are no longer needed for TDM. The use is not permitted if the rightholder has reserved it, and for works available online a reservation is effective only if it is made in machine-readable form (§ 44b(3) UrhG). In the case of a photographer against the non-profit LAION, the Higher Regional Court of Hamburg held that a reservation formulated in natural language in a stock photo agency's terms was not machine-readable at the time of download, so § 44b applied (OLG Hamburg (2025)). The court allowed an appeal to the Federal Court of Justice; the judgment is not final.

#### 3. Research TDM exception

§ 60d UrhG, which transposes Art. 3 DSM Directive (2019), permits reproductions for TDM for scientific research by research organisations that pursue non-commercial purposes, reinvest all profits in research or act under a state-recognised public-interest mission, and by publicly accessible libraries, museums and archives (§§ 44b, 60d UrhG). Research organisations under the decisive influence of a private company that has preferential access to the results cannot rely on it. Rightholders cannot opt out of this exception, contractual provisions to the contrary are unenforceable, and copies may be retained for research purposes, including to verify results (Art. 3(2), 7(1) DSM Directive (2019)). The Higher Regional Court of Hamburg also applied § 60d to LAION's creation of an image-text dataset, which it regarded as a methodical, verifiable activity of applied research (OLG Hamburg (2025)).

#### 4. AI Act obligations for general-purpose AI model providers

Providers of general-purpose AI models must put in place a policy to comply with Union copyright law, in particular to identify and comply with reservations of rights under Art. 4(3) DSM Directive, including through state-of-the-art technologies (Art. 53(1)(c), AI Act (2024)). They must also publish a sufficiently detailed summary of the content used for training, according to a template provided by the AI Office (Art. 53(1)(d)). These obligations have applied since 2 August 2025 (Art. 113) and also bind providers of open-source models, who are exempt only from certain other documentation duties (Art. 53(2)). The summary helps rightholders find out whether their works were used.

#### 5. Memorisation and output as a separate risk

The Regional Court of Munich I ruled in a case brought by the collecting society GEMA against two OpenAI companies over nine German song lyrics that ChatGPT could reproduce exactly or almost exactly (LG München I (2025)). It found that the lyrics were memorised in the model parameters, which it treated as a reproduction (§ 16 UrhG), and that outputting them was a making available to the public (§ 19a UrhG). The TDM exception of § 44b UrhG did not cover the memorisation, and the court granted an injunction, information and damages. The judgment is not final. It illustrates that lawful training copies do not make everything a model stores or outputs lawful; output risk has to be assessed separately.

#### Origin and variants

The TDM exceptions were introduced by the DSM Directive (2019) and transposed into German law in §§ 44b and 60d UrhG. The exception of Art. 4 also covers computer programs (Art. 4(1)), so source code can be used for TDM under the same conditions. US law has no specific TDM exception: unlicensed uses are assessed under the fair use doctrine, which weighs the purpose and character of the use, the nature of the work, the amount used and the effect on the market for the work, and depends on the individual case (17 U.S.C. § 107). A separate rule applies to platforms that host user uploads: under Art. 17 DSM Directive (2019), online content-sharing service providers must seek authorisation from rightholders, for instance through licences, which can matter where users share AI-generated outputs.

### When to use it

- When a company collects lawfully accessible works from the internet to train or fine-tune a model and must check whether rightholders have made a machine-readable reservation (§ 44b UrhG).
- When a university or other non-commercial research organisation builds a training dataset for scientific research (§ 60d UrhG).
- When a provider places a general-purpose AI model on the EU market and needs a copyright policy and a public training-content summary (Art. 53(1)(c), (d), AI Act (2024)).
- When a model reproduces protected texts almost verbatim, which raises an infringement question independent of the training (LG München I (2025)).

### Strengths and limitations

**Strengths**
- The EU exceptions define in advance when TDM is permitted, which is more predictable than a case-by-case fair use assessment (DSM Directive (2019), 17 U.S.C. § 107).
- The research exception cannot be excluded by rightholders or by contract (Art. 3, 7(1) DSM Directive (2019)).
- The AI Act's training-content summary gives rightholders a way to find out whether their works were used (Art. 53(1)(d), AI Act (2024)).

**Limitations**
- Whether a reservation is machine-readable is disputed in practice; the first appellate ruling on this question is not final (OLG Hamburg (2025)).
- The exceptions cover training copies but, according to the Munich ruling, not works memorised in the model (LG München I (2025)).
- Commercial providers depend on rightholders not having opted out; where they have, a licence is needed.

### Comparison

| Approach | How it differs | Suited for |
|----------|-----------------|------------|
| Commercial TDM exception (Art. 4 DSM, § 44b UrhG) | Any purpose; excluded by a machine-readable reservation for online works; copies deleted when no longer needed | Commercial training on lawfully accessible content without reservations |
| Research TDM exception (Art. 3 DSM, § 60d UrhG) | Only research organisations and cultural heritage institutions; no opt-out; copies may be retained for research | Non-commercial scientific research, including dataset creation |
| US fair use (17 U.S.C. § 107) | No TDM exception; four-factor assessment case by case | Training subject to US law, with less predictable outcomes |

### In practice

Providers document where their training data comes from, whether a machine-readable reservation was checked for each source and which exception or licence covers it, because this information is needed both for the AI Act copyright policy and for the public training-content summary (Art. 53(1)(c), (d), AI Act (2024)). Separately from training, they test models for verbatim reproduction of protected content, since memorised works can infringe copyright regardless of how lawful the training copies were (LG München I (2025)). Where a company integrates a third-party general-purpose model, it checks what copyright assurances the model provider gives.

### Key takeaway

Training copies are lawful in the EU if a text and data mining exception covers them, which for commercial use depends on the absence of a machine-readable opt-out, but what a model memorises and outputs is a separate copyright question.

### Sources

- Directive (EU) 2019/790 of the European Parliament and of the Council of 17 April 2019 on copyright and related rights in the Digital Single Market (DSM Directive). [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2019/790/oj)
- Urheberrechtsgesetz (UrhG), § 44b Text und Data Mining and § 60d Text und Data Mining für Zwecke der wissenschaftlichen Forschung. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/urhg/__44b.html)
- Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Hanseatisches Oberlandesgericht Hamburg, judgment of 10 December 2025, 5 U 104/24 (Kneschke v. LAION), upholding Landgericht Hamburg, judgment of 27 September 2024, 310 O 227/23. [MIR full text](https://medien-internet-und-recht.de/volltext.php?mir_dok_id=3526)
- Landgericht München I, judgment of 11 November 2025, 42 O 14139/24 (GEMA v. OpenAI). [LTO report](https://www.lto.de/recht/nachrichten/n/42o1413924-lg-muenchen-i-gema-openai-chatgpt-songtexte-ki)
- 17 U.S.C. § 107, Limitations on exclusive rights: Fair use. [Cornell LII](https://www.law.cornell.edu/uscode/text/17/107)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Werden urheberrechtlich geschützte Werke kopiert, um ein KI-Modell zu trainieren, ist das eine Vervielfältigung, die eine gesetzliche Schranke oder eine Lizenz braucht. In der EU sieht die DSM-Richtlinie (2019) zwei Schranken für Text und Data Mining (TDM) vor: eine für jeden Zweck, die Rechteinhaber durch einen maschinenlesbaren Vorbehalt ausschließen können, und eine für die wissenschaftliche Forschung ohne Widerspruchsmöglichkeit. Der [[eu-ai-act|EU AI Act]] verpflichtet Anbieter von KI-Modellen mit allgemeinem Verwendungszweck, solche Vorbehalte zu beachten und eine Zusammenfassung ihrer Trainingsinhalte zu veröffentlichen. Deutsche Gerichte haben die Erstellung von Datensätzen bisher von den TDM-Schranken gedeckt gesehen, im Modell memorisierte Werke aber als Vervielfältigungen behandelt, die die Schranken nicht abdecken; beide Urteile sind nicht rechtskräftig.

### Funktionsweise

Die rechtliche Prüfung folgt dem Lebenszyklus der Trainingsdaten: Zum Sammeln und Analysieren werden Kopien angefertigt, eine Schranke muss sie decken, Anbieter von Modellen mit allgemeinem Verwendungszweck haben zusätzliche Pflichten aus dem AI Act, und was das trainierte Modell speichert und ausgibt, wird gesondert beurteilt.

```text
1. Trainingskopien sind Vervielfältigungen; TDM ist automatisierte Analyse
▼
2. Kommerzielles TDM: zulässig, wenn kein maschinenlesbarer Vorbehalt besteht
▼
3. TDM für die Forschung: Forschungsorganisationen, kein Widerspruch möglich
▼
4. AI Act: Urheberrechtsstrategie und öffentliche Zusammenfassung der Trainingsinhalte
▼
5. Memorisierung und Ausgaben: eigene Frage der Rechtsverletzung
```

#### 1. Trainingskopien als Vervielfältigungen und der Begriff des TDM

Das Sammeln und Verarbeiten von Werken für das Training erfordert Vervielfältigungen, die nur mit Zustimmung des Rechteinhabers oder aufgrund einer Schranke zulässig sind. Die DSM-Richtlinie (2019) definiert Text und Data Mining als jede automatisierte Analysetechnik, die Texte und Daten in digitaler Form analysiert, um Informationen wie Muster, Trends und Korrelationen zu gewinnen (Art. 2 Nr. 2); § 44b Abs. 1 UrhG verwendet eine entsprechende Definition (§§ 44b, 60d UrhG). Das Training eines KI-Modells auf einem großen Korpus fällt unter diese Definition, weshalb die TDM-Schranken in der EU die zentrale Rechtsgrundlage für Trainingsdaten sind.

#### 2. Kommerzielle TDM-Schranke und der Nutzungsvorbehalt

§ 44b UrhG, der Art. 4 der DSM-Richtlinie (2019) umsetzt, erlaubt Vervielfältigungen rechtmäßig zugänglicher Werke für TDM zu jedem Zweck, auch zu kommerziellen; die Kopien sind zu löschen, sobald sie für das TDM nicht mehr erforderlich sind. Die Nutzung ist unzulässig, wenn sich der Rechteinhaber sie vorbehalten hat, und bei online zugänglichen Werken ist ein Vorbehalt nur wirksam, wenn er in maschinenlesbarer Form erfolgt (§ 44b Abs. 3 UrhG). Im Verfahren eines Fotografen gegen den gemeinnützigen Verein LAION entschied das Hanseatische Oberlandesgericht Hamburg, dass ein in natürlicher Sprache formulierter Vorbehalt in den Nutzungsbedingungen einer Bildagentur zum Zeitpunkt des Downloads nicht maschinenlesbar war, sodass § 44b griff (OLG Hamburg (2025)). Das Gericht hat die Revision zum Bundesgerichtshof zugelassen; das Urteil ist nicht rechtskräftig.

#### 3. TDM-Schranke für die wissenschaftliche Forschung

§ 60d UrhG, der Art. 3 der DSM-Richtlinie (2019) umsetzt, erlaubt Vervielfältigungen für TDM zu Zwecken der wissenschaftlichen Forschung durch Forschungsorganisationen, die nicht kommerzielle Zwecke verfolgen, sämtliche Gewinne in die Forschung reinvestieren oder im Rahmen eines staatlich anerkannten Auftrags im öffentlichen Interesse tätig sind, sowie durch öffentlich zugängliche Bibliotheken, Museen und Archive (§§ 44b, 60d UrhG). Forschungsorganisationen unter dem bestimmenden Einfluss eines privaten Unternehmens mit bevorzugtem Zugang zu den Ergebnissen können sich nicht darauf berufen. Rechteinhaber können dieser Schranke nicht widersprechen, abweichende Vertragsklauseln sind nicht durchsetzbar, und Kopien dürfen für Forschungszwecke einschließlich der Überprüfung von Ergebnissen aufbewahrt werden (Art. 3 Abs. 2, Art. 7 Abs. 1 DSM-Richtlinie (2019)). Das OLG Hamburg wandte § 60d auch auf die Erstellung eines Bild-Text-Datensatzes durch LAION an, die es als methodisches, nachprüfbares Vorgehen angewandter Forschung ansah (OLG Hamburg (2025)).

#### 4. Pflichten aus dem AI Act für Anbieter von KI-Modellen mit allgemeinem Verwendungszweck

Anbieter von KI-Modellen mit allgemeinem Verwendungszweck müssen eine Strategie zur Einhaltung des Urheberrechts der Union einführen, insbesondere um Rechtsvorbehalte nach Art. 4 Abs. 3 der DSM-Richtlinie zu ermitteln und einzuhalten, auch mit modernsten Technologien (Art. 53 Abs. 1 Buchst. c, AI Act (2024)). Außerdem müssen sie eine hinreichend detaillierte Zusammenfassung der für das Training verwendeten Inhalte nach einer Vorlage des Büros für Künstliche Intelligenz veröffentlichen (Art. 53 Abs. 1 Buchst. d). Diese Pflichten gelten seit dem 2. August 2025 (Art. 113) und binden auch Anbieter quelloffener Modelle, die nur von bestimmten anderen Dokumentationspflichten befreit sind (Art. 53 Abs. 2). Die Zusammenfassung hilft Rechteinhabern zu erkennen, ob ihre Werke verwendet wurden.

#### 5. Memorisierung und Ausgaben als eigenes Risiko

Das Landgericht München I entschied in einem Verfahren der Verwertungsgesellschaft GEMA gegen zwei OpenAI-Gesellschaften über neun deutsche Liedtexte, die ChatGPT wörtlich oder nahezu wörtlich wiedergeben konnte (LG München I (2025)). Es sah die Liedtexte als in den Modellparametern memorisiert an, wertete dies als Vervielfältigung (§ 16 UrhG) und ihre Ausgabe als öffentliche Zugänglichmachung (§ 19a UrhG). Die TDM-Schranke des § 44b UrhG deckte die Memorisierung nicht; das Gericht sprach Unterlassung, Auskunft und Schadensersatz zu. Das Urteil ist nicht rechtskräftig. Es zeigt, dass rechtmäßige Trainingskopien nicht alles rechtmäßig machen, was ein Modell speichert oder ausgibt; das Ausgaberisiko ist gesondert zu bewerten.

#### Ursprung und Varianten

Die TDM-Schranken wurden mit der DSM-Richtlinie (2019) eingeführt und in den §§ 44b und 60d UrhG in deutsches Recht umgesetzt. Die Schranke des Art. 4 erfasst auch Computerprogramme (Art. 4 Abs. 1), sodass Quellcode unter denselben Bedingungen für TDM genutzt werden kann. Das US-Recht kennt keine besondere TDM-Schranke: Unlizenzierte Nutzungen werden nach der Fair-Use-Doktrin beurteilt, die Zweck und Art der Nutzung, die Art des Werks, den Umfang der Nutzung und die Auswirkungen auf den Markt für das Werk abwägt und vom Einzelfall abhängt (17 U.S.C. § 107). Eine eigene Regel gilt für Plattformen mit nutzergenerierten Inhalten: Nach Art. 17 der DSM-Richtlinie (2019) müssen Diensteanbieter für das Teilen von Online-Inhalten die Erlaubnis der Rechteinhaber einholen, etwa durch Lizenzen, was relevant werden kann, wenn Nutzer KI-generierte Ausgaben teilen.

### Wann einsetzen

- Wenn ein Unternehmen rechtmäßig zugängliche Werke aus dem Internet sammelt, um ein Modell zu trainieren oder feinabzustimmen, und prüfen muss, ob Rechteinhaber einen maschinenlesbaren Vorbehalt erklärt haben (§ 44b UrhG).
- Wenn eine Hochschule oder eine andere nicht kommerzielle Forschungsorganisation einen Trainingsdatensatz für die wissenschaftliche Forschung aufbaut (§ 60d UrhG).
- Wenn ein Anbieter ein KI-Modell mit allgemeinem Verwendungszweck in der EU in Verkehr bringt und eine Urheberrechtsstrategie sowie eine öffentliche Zusammenfassung der Trainingsinhalte braucht (Art. 53 Abs. 1 Buchst. c und d, AI Act (2024)).
- Wenn ein Modell geschützte Texte nahezu wörtlich wiedergibt, was eine vom Training unabhängige Frage der Rechtsverletzung aufwirft (LG München I (2025)).

### Stärken und Grenzen

**Stärken**
- Die EU-Schranken legen im Voraus fest, wann TDM zulässig ist; das ist vorhersehbarer als eine Fair-Use-Prüfung im Einzelfall (DSM-Richtlinie (2019), 17 U.S.C. § 107).
- Die Forschungsschranke kann weder durch Rechteinhaber noch durch Vertrag ausgeschlossen werden (Art. 3, Art. 7 Abs. 1 DSM-Richtlinie (2019)).
- Die Zusammenfassung der Trainingsinhalte nach dem AI Act gibt Rechteinhabern eine Möglichkeit festzustellen, ob ihre Werke verwendet wurden (Art. 53 Abs. 1 Buchst. d, AI Act (2024)).

**Einschränkungen**
- Ob ein Vorbehalt maschinenlesbar ist, ist in der Praxis umstritten; die erste Berufungsentscheidung dazu ist nicht rechtskräftig (OLG Hamburg (2025)).
- Die Schranken decken Trainingskopien, nach dem Münchner Urteil aber nicht im Modell memorisierte Werke (LG München I (2025)).
- Kommerzielle Anbieter sind darauf angewiesen, dass Rechteinhaber keinen Vorbehalt erklärt haben; andernfalls brauchen sie eine Lizenz.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|-----------------|------------|
| Kommerzielle TDM-Schranke (Art. 4 DSM-RL, § 44b UrhG) | Jeder Zweck; ausgeschlossen durch einen maschinenlesbaren Vorbehalt bei Online-Werken; Kopien werden gelöscht, wenn nicht mehr erforderlich | Kommerzielles Training mit rechtmäßig zugänglichen Inhalten ohne Vorbehalt |
| TDM-Schranke für die Forschung (Art. 3 DSM-RL, § 60d UrhG) | Nur Forschungsorganisationen und Kulturerbe-Einrichtungen; kein Widerspruch möglich; Kopien dürfen für die Forschung aufbewahrt werden | Nicht kommerzielle wissenschaftliche Forschung einschließlich der Erstellung von Datensätzen |
| US Fair Use (17 U.S.C. § 107) | Keine TDM-Schranke; Prüfung anhand von vier Faktoren im Einzelfall | Training unter US-Recht, mit weniger vorhersehbarem Ergebnis |

### In der Praxis

Anbieter dokumentieren, woher ihre Trainingsdaten stammen, ob für jede Quelle ein maschinenlesbarer Vorbehalt geprüft wurde und welche Schranke oder Lizenz sie deckt, weil diese Angaben sowohl für die Urheberrechtsstrategie als auch für die öffentliche Zusammenfassung der Trainingsinhalte nach dem AI Act gebraucht werden (Art. 53 Abs. 1 Buchst. c und d, AI Act (2024)). Unabhängig vom Training prüfen sie Modelle auf wörtliche Wiedergabe geschützter Inhalte, weil memorisierte Werke das Urheberrecht verletzen können, gleich wie rechtmäßig die Trainingskopien waren (LG München I (2025)). Wer ein Modell mit allgemeinem Verwendungszweck eines Dritten einbindet, prüft, welche urheberrechtlichen Zusicherungen der Modellanbieter gibt.

### Merksatz

Trainingskopien sind in der EU zulässig, wenn eine Schranke für Text und Data Mining sie deckt, was bei kommerzieller Nutzung vom Fehlen eines maschinenlesbaren Vorbehalts abhängt, doch was ein Modell memorisiert und ausgibt, ist eine eigene urheberrechtliche Frage.

### Quellen

- Directive (EU) 2019/790 of the European Parliament and of the Council of 17 April 2019 on copyright and related rights in the Digital Single Market (DSM Directive). [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2019/790/oj)
- Urheberrechtsgesetz (UrhG), § 44b Text und Data Mining and § 60d Text und Data Mining für Zwecke der wissenschaftlichen Forschung. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/urhg/__44b.html)
- Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Hanseatisches Oberlandesgericht Hamburg, judgment of 10 December 2025, 5 U 104/24 (Kneschke v. LAION), upholding Landgericht Hamburg, judgment of 27 September 2024, 310 O 227/23. [MIR full text](https://medien-internet-und-recht.de/volltext.php?mir_dok_id=3526)
- Landgericht München I, judgment of 11 November 2025, 42 O 14139/24 (GEMA v. OpenAI). [LTO report](https://www.lto.de/recht/nachrichten/n/42o1413924-lg-muenchen-i-gema-openai-chatgpt-songtexte-ki)
- 17 U.S.C. § 107, Limitations on exclusive rights: Fair use. [Cornell LII](https://www.law.cornell.edu/uscode/text/17/107)
