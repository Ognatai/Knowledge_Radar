---
title_en: AI Liability Law
title_de: KI-Haftungsrecht
entity_type: Concept
sources:
- https://eur-lex.europa.eu/eli/dir/2024/2853/oj
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022PC0496
- https://www.gesetze-im-internet.de/bgb/__823.html
- https://dserver.bundestag.de/btd/21/042/2104297.pdf
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

AI liability law answers who pays when an AI system causes damage. In the EU, the new Product Liability Directive (2024) makes manufacturers liable without fault for defective products, explicitly including software and therefore AI systems, and eases the claimant's burden of proof through disclosure orders and rebuttable presumptions. Fault-based liability, for instance for careless use of an AI system, remains a matter of national tort law, because the proposed AI Liability Directive was withdrawn in 2025. The obligations of the [[eu-ai-act|EU AI Act]] are not liability rules, but they matter as evidence in liability disputes.

### How it works

Two strands of liability apply side by side: no-fault product liability under the Product Liability Directive (2024), which looks only at whether a product was defective, and fault-based liability under national tort law, which asks whether someone acted culpably. The Directive addresses the main obstacle in AI cases, namely that injured persons can rarely prove a defect or causation in an opaque system, through disclosure of evidence and presumptions.

```text
1. Software and AI systems are products
▼
2. Liable: manufacturer, component manufacturer, importer, modifier
▼
3. Defective: lacks expected safety, incl. effect of continued learning
▼
4. Court orders disclosure once the claim is plausible
▼
5. Rebuttable presumptions of defectiveness and causation
▼
6. Outside product liability: fault-based national tort law
```

#### 1. Software and AI systems as products

The Product Liability Directive (2024) defines 'product' to include software (Art. 4(1)), so AI systems are covered whether they are integrated into a device or supplied on their own. The Directive applies to products placed on the market or put into service after 9 December 2026 (Art. 2(1)); free and open-source software developed or supplied outside a commercial activity is excluded (Art. 2(2)). Compensable damage comprises death or personal injury, including medically recognised harm to psychological health, damage to property not used exclusively for professional purposes, and the destruction or corruption of data not used for professional purposes (Art. 6).

#### 2. Who is liable

Liability falls on the manufacturer of the defective product, the manufacturer of a defective component integrated into it and, where the manufacturer is established outside the Union, the importer, the authorised representative or the fulfilment service provider (Art. 8(1), Product Liability Directive (2024)). Whoever substantially modifies a product outside the manufacturer's control and then makes it available or puts it into service is treated as its manufacturer (Art. 8(2)), which can apply to a company that substantially changes an AI system it has bought. Liability does not depend on fault: what counts is that the product was defective, that damage occurred and that the defect caused the damage.

#### 3. When an AI product is defective

A product is defective if it does not provide the safety that a person is entitled to expect or that Union or national law requires (Art. 7(1), Product Liability Directive (2024)). All circumstances are taken into account, explicitly including the effect of any ability to continue to learn or acquire new features after the product has been placed on the market (Art. 7(2)(c)). As a rule, a manufacturer can escape liability by proving that the defect probably did not exist when the product was placed on the market; this defence does not apply where the defect is due to software, including updates or upgrades, to a lack of updates necessary to maintain safety, to a related service or to a substantial modification, provided these are within the manufacturer's control (Art. 11(2)). For AI systems that keep learning or receive model updates, the manufacturer therefore remains responsible for their safety after sale.

#### 4. Disclosure of evidence

If a claimant presents facts and evidence sufficient to make the claim for compensation plausible, the court can require the defendant to disclose relevant evidence at its disposal (Art. 9, Product Liability Directive (2024)). The rule applies to all products, not only to high-risk AI systems. Conversely, a defendant that shows a need for evidence can obtain disclosure from the claimant (Art. 9(2)). For AI cases this gives injured persons access to documentation that only the manufacturer holds.

#### 5. Presumptions that ease the burden of proof

In principle, the claimant must prove that the product was defective, the damage and the causal link (Art. 10(1), Product Liability Directive (2024)). Defectiveness is presumed if the defendant fails to disclose relevant evidence, if the product does not comply with mandatory product safety requirements intended to protect against the damage suffered, or if the damage was caused by an obvious malfunction during reasonably foreseeable use (Art. 10(2)). Causation is presumed if the product is defective and the damage is of a kind typically consistent with that defect (Art. 10(3)). Where, despite disclosure, the claimant faces excessive difficulties, in particular due to technical or scientific complexity, and shows that defectiveness or causation is likely, the court presumes them (Art. 10(4)); this is the provision most relevant to opaque AI systems. The defendant can rebut all presumptions (Art. 10(5)).

#### 6. Fault-based liability and the role of the AI Act

Outside product liability, damage caused by using an AI system is governed by national tort law. In Germany, § 823 BGB makes liable whoever intentionally or negligently and unlawfully injures life, body, health, property or another right of another person, or culpably breaches a statute intended to protect others; the injured party generally has to prove fault, damage and causation. The AI Act (2024) sets obligations rather than liability rules: high-risk AI systems must allow automatic logging of events (Art. 12) and effective human oversight (Art. 14), and deployers must use them as instructed and assign human oversight to competent persons (Art. 26). In a dispute, compliance with or breaches of these obligations can serve as evidence, for instance as non-compliance with mandatory safety requirements under Art. 10(2) of the Product Liability Directive (2024).

#### Origin and variants

Directive 85/374/EEC of 1985, transposed in Germany by the Product Liability Act (Produkthaftungsgesetz) of 1989, did not clearly cover software. The new Directive replaces it; Member States must transpose it by 9 December 2026 (Art. 22). In Germany, the federal government introduced a bill in February 2026 that replaces the 1989 Act, brings software including AI systems within product liability and is to apply to products placed on the market from 9 December 2026 (German government bill on product liability (2026)). In 2022 the Commission had also proposed an AI Liability Directive to harmonise fault-based liability, with disclosure orders for high-risk AI systems and a rebuttable presumption of causation (AI Liability Directive proposal (2022)). The Commission withdrew the proposal for lack of foreseeable agreement; the withdrawal notice was published in the Official Journal on 6 October 2025.

### When to use it

- When an AI system or an AI-based product causes personal injury, property damage or the loss of private data, and the question is whether the manufacturer is liable without fault.
- When the damage stems from a model update, a missing safety update or the system's continued learning after sale (Art. 7(2)(c), 11(2), Product Liability Directive (2024)).
- When a company substantially modifies a purchased AI system and puts it into service, and may itself become liable as manufacturer (Art. 8(2)).
- When damage results from careless use of a functioning AI system, which is assessed under fault-based national tort law such as § 823 BGB.

### Strengths and limitations

**Strengths**
- Software and AI systems are explicitly products, closing the gap of the 1985 Directive (Art. 4(1), Product Liability Directive (2024)).
- Disclosure orders and presumptions, including for technically complex products, address the information asymmetry between injured persons and manufacturers (Art. 9, 10).
- Manufacturers remain liable for defects caused by updates or missing safety updates within their control (Art. 11(2)).

**Limitations**
- Only products placed on the market or put into service after 9 December 2026 are covered (Art. 2(1)).
- Free and open-source software supplied outside a commercial activity is excluded (Art. 2(2)), and property used exclusively for professional purposes and professional data are not compensated (Art. 6).
- Fault-based liability for AI is not harmonised in the EU after the withdrawal of the AI Liability Directive proposal; claimants depend on national law and its burden of proof.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Product Liability Directive (2024) | No-fault liability of manufacturers and other economic operators for defective products, including software; disclosure orders and rebuttable presumptions | Damage caused by a defective AI system or AI-based product |
| § 823 BGB (German tort law) | Fault-based liability; the injured party generally proves fault, damage and causation | Damage caused by careless development, deployment or use of an AI system |
| AI Liability Directive proposal (2022) | Would have harmonised fault-based liability with disclosure for high-risk AI and a presumption of causation; withdrawn in 2025 | No longer applicable; shows the gap in EU-level fault-based rules |

### In practice

Manufacturers and deployers of AI systems keep documentation, logs and update histories, because these become evidence once a court orders disclosure and can be used to rebut presumptions. Where a deployer substantially modifies an AI system, for instance by retraining it for a new purpose, it should check whether it becomes a manufacturer within the meaning of Art. 8(2) of the Product Liability Directive (2024). [[explainable-ai|Explainable AI]] can make it easier to show how a system reached a harmful output and thus to establish or rebut a defect.

### Key takeaway

From 9 December 2026, defective AI systems trigger no-fault product liability with disclosure orders and presumptions that ease proof, while fault-based liability for AI remains a matter of national law.

### Sources

- Directive (EU) 2024/2853 of the European Parliament and of the Council of 23 October 2024 on liability for defective products and repealing Council Directive 85/374/EEC. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2024/2853/oj)
- European Commission (2022). *Proposal for a Directive on adapting non-contractual civil liability rules to artificial intelligence (AI Liability Directive)*, COM(2022) 496 final. [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022PC0496)
- Bürgerliches Gesetzbuch (BGB), § 823 Schadensersatzpflicht. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bgb/__823.html)
- Deutscher Bundestag (2026). *Gesetzentwurf der Bundesregierung zur Modernisierung des Produkthaftungsrechts*, Drucksache 21/4297. [Bundestag PDF](https://dserver.bundestag.de/btd/21/042/2104297.pdf)
- Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Das KI-Haftungsrecht beantwortet, wer zahlt, wenn ein KI-System einen Schaden verursacht. In der EU macht die neue Produkthaftungsrichtlinie (2024) Hersteller verschuldensunabhängig für fehlerhafte Produkte haftbar, ausdrücklich auch für Software und damit für KI-Systeme, und erleichtert Geschädigten den Beweis durch Offenlegungsanordnungen und widerlegbare Vermutungen. Die verschuldensabhängige Haftung, etwa für einen sorglosen Einsatz eines KI-Systems, bleibt Sache des nationalen Deliktsrechts, weil die vorgeschlagene KI-Haftungsrichtlinie 2025 zurückgezogen wurde. Die Pflichten des [[eu-ai-act|EU AI Act]] sind keine Haftungsregeln, spielen in Haftungsstreitigkeiten aber als Beweismittel eine Rolle.

### Funktionsweise

Zwei Haftungsstränge stehen nebeneinander: die verschuldensunabhängige Produkthaftung nach der Produkthaftungsrichtlinie (2024), die nur fragt, ob ein Produkt fehlerhaft war, und die verschuldensabhängige Haftung nach nationalem Deliktsrecht, die fragt, ob jemand schuldhaft gehandelt hat. Die Richtlinie geht das Hauptproblem in KI-Fällen an, dass Geschädigte einen Fehler oder die Ursächlichkeit in einem undurchsichtigen System kaum beweisen können, und zwar mit Offenlegung von Beweismitteln und Vermutungen.

```text
1. Software und KI-Systeme sind Produkte
▼
2. Haftend: Hersteller, Komponentenhersteller, Einführer, wer wesentlich verändert
▼
3. Fehlerhaft: fehlende berechtigte Sicherheit, inkl. Folgen des Weiterlernens
▼
4. Gericht ordnet Offenlegung an, sobald der Anspruch plausibel ist
▼
5. Widerlegbare Vermutungen für Fehler und Ursächlichkeit
▼
6. Außerhalb der Produkthaftung: verschuldensabhängiges nationales Deliktsrecht
```

#### 1. Software und KI-Systeme als Produkte

Die Produkthaftungsrichtlinie (2024) zählt Software zu den Produkten (Art. 4 Nr. 1), sodass KI-Systeme erfasst sind, gleich ob sie in ein Gerät eingebaut oder eigenständig bereitgestellt werden. Die Richtlinie gilt für Produkte, die nach dem 9. Dezember 2026 in Verkehr gebracht oder in Betrieb genommen werden (Art. 2 Abs. 1); freie und quelloffene Software, die außerhalb einer Geschäftstätigkeit entwickelt oder bereitgestellt wird, ist ausgenommen (Art. 2 Abs. 2). Ersatzfähig sind Tod und Körperverletzung einschließlich medizinisch anerkannter Beeinträchtigungen der psychischen Gesundheit, Schäden an Sachen, die nicht ausschließlich beruflich genutzt werden, sowie die Vernichtung oder Beschädigung von Daten, die nicht beruflich genutzt werden (Art. 6).

#### 2. Wer haftet

Es haften der Hersteller des fehlerhaften Produkts, der Hersteller einer fehlerhaften eingebauten Komponente und, wenn der Hersteller außerhalb der Union niedergelassen ist, der Einführer, der Bevollmächtigte oder der Fulfilment-Dienstleister (Art. 8 Abs. 1, Produkthaftungsrichtlinie (2024)). Wer ein Produkt außerhalb der Kontrolle des Herstellers wesentlich verändert und es danach bereitstellt oder in Betrieb nimmt, gilt als dessen Hersteller (Art. 8 Abs. 2); das kann ein Unternehmen treffen, das ein gekauftes KI-System wesentlich verändert. Auf Verschulden kommt es nicht an: Entscheidend ist, dass das Produkt fehlerhaft war, ein Schaden eingetreten ist und der Fehler den Schaden verursacht hat.

#### 3. Wann ein KI-Produkt fehlerhaft ist

Ein Produkt ist fehlerhaft, wenn es nicht die Sicherheit bietet, die eine Person erwarten darf oder die das Unionsrecht oder das nationale Recht vorschreibt (Art. 7 Abs. 1, Produkthaftungsrichtlinie (2024)). Zu berücksichtigen sind alle Umstände, ausdrücklich auch die Auswirkungen einer etwaigen Fähigkeit, nach dem Inverkehrbringen weiterzulernen oder neue Funktionen zu erwerben (Art. 7 Abs. 2 Buchst. c). Grundsätzlich kann sich ein Hersteller entlasten, indem er nachweist, dass der Fehler beim Inverkehrbringen wahrscheinlich noch nicht bestand; das gilt nicht, wenn der Fehler auf Software einschließlich Aktualisierungen, auf fehlende sicherheitsnotwendige Aktualisierungen, auf einen verbundenen Dienst oder auf eine wesentliche Veränderung zurückgeht, soweit diese in der Kontrolle des Herstellers liegen (Art. 11 Abs. 2). Bei KI-Systemen, die weiterlernen oder Modellaktualisierungen erhalten, bleibt der Hersteller deshalb auch nach dem Verkauf für ihre Sicherheit verantwortlich.

#### 4. Offenlegung von Beweismitteln

Legt ein Kläger Tatsachen und Beweise vor, die seinen Schadensersatzanspruch plausibel machen, kann das Gericht den Beklagten verpflichten, relevante Beweismittel in seiner Verfügungsgewalt offenzulegen (Art. 9, Produkthaftungsrichtlinie (2024)). Die Regel gilt für alle Produkte, nicht nur für Hochrisiko-KI-Systeme. Umgekehrt kann ein Beklagter, der einen Bedarf an Beweismitteln darlegt, die Offenlegung durch den Kläger erreichen (Art. 9 Abs. 2). In KI-Fällen erhalten Geschädigte so Zugang zu Unterlagen, die nur der Hersteller besitzt.

#### 5. Vermutungen, die den Beweis erleichtern

Grundsätzlich muss der Kläger die Fehlerhaftigkeit, den Schaden und den Kausalzusammenhang beweisen (Art. 10 Abs. 1, Produkthaftungsrichtlinie (2024)). Die Fehlerhaftigkeit wird vermutet, wenn der Beklagte relevante Beweismittel nicht offenlegt, wenn das Produkt verbindliche Produktsicherheitsanforderungen zum Schutz vor dem eingetretenen Schaden nicht erfüllt oder wenn der Schaden durch eine offensichtliche Funktionsstörung bei vernünftigerweise vorhersehbarer Verwendung verursacht wurde (Art. 10 Abs. 2). Die Ursächlichkeit wird vermutet, wenn das Produkt fehlerhaft ist und der Schaden typischerweise mit diesem Fehler vereinbar ist (Art. 10 Abs. 3). Hat der Kläger trotz Offenlegung übermäßige Schwierigkeiten, insbesondere wegen technischer oder wissenschaftlicher Komplexität, und zeigt er, dass Fehlerhaftigkeit oder Ursächlichkeit wahrscheinlich sind, vermutet das Gericht sie (Art. 10 Abs. 4); das ist die für undurchsichtige KI-Systeme wichtigste Vorschrift. Der Beklagte kann alle Vermutungen widerlegen (Art. 10 Abs. 5).

#### 6. Verschuldensabhängige Haftung und die Rolle des AI Act

Außerhalb der Produkthaftung richten sich Schäden durch den Einsatz eines KI-Systems nach nationalem Deliktsrecht. In Deutschland haftet nach § 823 BGB, wer vorsätzlich oder fahrlässig und widerrechtlich Leben, Körper, Gesundheit, Eigentum oder ein sonstiges Recht eines anderen verletzt oder schuldhaft gegen ein Schutzgesetz verstößt; der Geschädigte muss Verschulden, Schaden und Ursächlichkeit grundsätzlich selbst beweisen. Der AI Act (2024) enthält Pflichten, keine Haftungsregeln: Hochrisiko-KI-Systeme müssen eine automatische Protokollierung von Ereignissen (Art. 12) und eine wirksame menschliche Aufsicht (Art. 14) ermöglichen, und Betreiber müssen sie gemäß der Betriebsanleitung verwenden und die menschliche Aufsicht kompetenten Personen übertragen (Art. 26). Im Streitfall können Einhaltung oder Verletzung dieser Pflichten als Beweismittel dienen, etwa als Nichterfüllung verbindlicher Sicherheitsanforderungen nach Art. 10 Abs. 2 der Produkthaftungsrichtlinie (2024).

#### Ursprung und Varianten

Die Richtlinie 85/374/EWG von 1985, in Deutschland umgesetzt durch das Produkthaftungsgesetz von 1989, erfasste Software nicht eindeutig. Die neue Richtlinie ersetzt sie; die Mitgliedstaaten müssen sie bis zum 9. Dezember 2026 umsetzen (Art. 22). In Deutschland hat die Bundesregierung im Februar 2026 einen Gesetzentwurf eingebracht, der das Gesetz von 1989 ersetzt, Software einschließlich KI-Systemen in die Produkthaftung einbezieht und für Produkte gelten soll, die ab dem 9. Dezember 2026 in Verkehr gebracht werden (Gesetzentwurf der Bundesregierung zur Produkthaftung (2026)). 2022 hatte die Kommission zudem eine KI-Haftungsrichtlinie vorgeschlagen, um die verschuldensabhängige Haftung zu harmonisieren, mit Offenlegungsanordnungen für Hochrisiko-KI-Systeme und einer widerlegbaren Kausalitätsvermutung (Vorschlag einer KI-Haftungsrichtlinie (2022)). Die Kommission hat den Vorschlag mangels absehbarer Einigung zurückgezogen; die Mitteilung darüber wurde am 6. Oktober 2025 im Amtsblatt veröffentlicht.

### Wann einsetzen

- Wenn ein KI-System oder ein KI-gestütztes Produkt Körperverletzungen, Sachschäden oder den Verlust privater Daten verursacht und zu klären ist, ob der Hersteller verschuldensunabhängig haftet.
- Wenn der Schaden auf eine Modellaktualisierung, eine fehlende Sicherheitsaktualisierung oder das Weiterlernen des Systems nach dem Verkauf zurückgeht (Art. 7 Abs. 2 Buchst. c, Art. 11 Abs. 2, Produkthaftungsrichtlinie (2024)).
- Wenn ein Unternehmen ein gekauftes KI-System wesentlich verändert und in Betrieb nimmt und dadurch selbst als Hersteller haften kann (Art. 8 Abs. 2).
- Wenn ein Schaden auf den sorglosen Einsatz eines funktionierenden KI-Systems zurückgeht; das richtet sich nach verschuldensabhängigem nationalem Deliktsrecht wie § 823 BGB.

### Stärken und Grenzen

**Stärken**
- Software und KI-Systeme sind ausdrücklich Produkte; die Lücke der Richtlinie von 1985 ist geschlossen (Art. 4 Nr. 1, Produkthaftungsrichtlinie (2024)).
- Offenlegungsanordnungen und Vermutungen, auch für technisch komplexe Produkte, gleichen das Informationsgefälle zwischen Geschädigten und Herstellern aus (Art. 9, 10).
- Hersteller haften weiter für Fehler durch Aktualisierungen oder fehlende Sicherheitsaktualisierungen in ihrer Kontrolle (Art. 11 Abs. 2).

**Einschränkungen**
- Erfasst sind nur Produkte, die nach dem 9. Dezember 2026 in Verkehr gebracht oder in Betrieb genommen werden (Art. 2 Abs. 1).
- Freie und quelloffene Software außerhalb einer Geschäftstätigkeit ist ausgenommen (Art. 2 Abs. 2), und Schäden an ausschließlich beruflich genutzten Sachen und an beruflichen Daten werden nicht ersetzt (Art. 6).
- Die verschuldensabhängige Haftung für KI ist nach dem Rückzug der vorgeschlagenen KI-Haftungsrichtlinie in der EU nicht harmonisiert; Geschädigte sind auf nationales Recht und dessen Beweislastregeln angewiesen.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Produkthaftungsrichtlinie (2024) | Verschuldensunabhängige Haftung von Herstellern und anderen Wirtschaftsakteuren für fehlerhafte Produkte einschließlich Software; Offenlegungsanordnungen und widerlegbare Vermutungen | Schäden durch ein fehlerhaftes KI-System oder KI-gestütztes Produkt |
| § 823 BGB (deutsches Deliktsrecht) | Verschuldensabhängige Haftung; der Geschädigte beweist grundsätzlich Verschulden, Schaden und Ursächlichkeit | Schäden durch sorglose Entwicklung, Bereitstellung oder Nutzung eines KI-Systems |
| Vorschlag einer KI-Haftungsrichtlinie (2022) | Hätte die verschuldensabhängige Haftung mit Offenlegung für Hochrisiko-KI und einer Kausalitätsvermutung harmonisiert; 2025 zurückgezogen | Nicht mehr anwendbar; zeigt die Lücke bei verschuldensabhängigen EU-Regeln |

### In der Praxis

Hersteller und Betreiber von KI-Systemen bewahren Dokumentation, Protokolle und Aktualisierungsverläufe auf, weil diese bei einer Offenlegungsanordnung zu Beweismitteln werden und zur Widerlegung von Vermutungen dienen können. Verändert ein Betreiber ein KI-System wesentlich, etwa durch Nachtraining für einen neuen Zweck, sollte er prüfen, ob er dadurch Hersteller im Sinne von Art. 8 Abs. 2 der Produkthaftungsrichtlinie (2024) wird. [[explainable-ai|Explainable AI]] kann erleichtern zu zeigen, wie ein System zu einer schädlichen Ausgabe kam, und damit einen Fehler zu belegen oder zu widerlegen.

### Merksatz

Ab dem 9. Dezember 2026 lösen fehlerhafte KI-Systeme eine verschuldensunabhängige Produkthaftung mit Offenlegungsanordnungen und beweiserleichternden Vermutungen aus, während die verschuldensabhängige Haftung für KI Sache des nationalen Rechts bleibt.

### Quellen

- Directive (EU) 2024/2853 of the European Parliament and of the Council of 23 October 2024 on liability for defective products and repealing Council Directive 85/374/EEC. [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2024/2853/oj)
- European Commission (2022). *Proposal for a Directive on adapting non-contractual civil liability rules to artificial intelligence (AI Liability Directive)*, COM(2022) 496 final. [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022PC0496)
- Bürgerliches Gesetzbuch (BGB), § 823 Schadensersatzpflicht. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bgb/__823.html)
- Deutscher Bundestag (2026). *Gesetzentwurf der Bundesregierung zur Modernisierung des Produkthaftungsrechts*, Drucksache 21/4297. [Bundestag PDF](https://dserver.bundestag.de/btd/21/042/2104297.pdf)
- Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
