---
title_en: Technical Debt
title_de: Technische Schulden
entity_type: Concept
aliases:
- Technical debt
- Tech debt
- Technische Schulden
- Hidden technical debt
- Cruft
sources:
- http://c2.com/doc/oopsla92.html
- https://martinfowler.com/bliki/TechnicalDebt.html
- https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Technical debt is a metaphor, coined by Ward Cunningham, for deficiencies in the internal quality of software that make it harder to change and extend; the extra effort they cause for each new feature is the interest paid on the debt (Fowler, 2019). Cunningham compared shipping first-time code to going into debt: a little debt speeds development as long as it is paid back promptly with a rewrite, but every minute spent on not-quite-right code counts as interest (Cunningham, 1992). Debt can be deliberate or inadvertent and prudent or reckless (Fowler, 2009). Machine learning systems have all the maintenance problems of traditional code plus ML-specific debt at the system level, which ordinary [[refactoring|refactoring]] does not remove (Sculley et al., 2015).

### How it works

```text
quick or not-quite-right solution (deliberate or inadvertent)
 ▼
principal: the deficiency in internal quality ("cruft")
 ▼
interest: extra effort each time that part of the system is changed
 ▼
decision per area: keep paying interest  or  pay down the principal
  (refactoring, tests, deleting dead code, fewer dependencies, documentation)
```

#### 1. Principal and interest

Fowler illustrates the metaphor with a confusing module structure: a feature that would take four days with a clear structure takes six, and the two-day difference is the interest. Cleaning up the structure for five days pays off the principal; for one feature that is no gain, nine days instead of six, but with two more similar features coming up it is faster to remove the cruft first. Because productivity cannot be measured objectively and such estimates are inaccurate, the usual route is to pay the principal off gradually, removing some cruft with each feature. Interest is only paid when a part of the code is changed, so crufty but stable areas can be left alone, while areas of high activity need a zero-tolerance attitude, because cruft accumulates where developers make changes without attention to internal quality (Fowler, 2019).

#### 2. The debt quadrant

Whether a design flaw counts as debt is the wrong question; the useful distinctions are between prudent and reckless and between deliberate and inadvertent debt. A team that knowingly takes a shortcut to reach a release and weighs the payoff against the cost takes on prudent, deliberate debt. A team ignorant of design practices takes on reckless debt without realising it, and a team that goes "quick and dirty" because it thinks it cannot afford clean code usually takes on reckless, deliberate debt. Prudent, inadvertent debt is inevitable even for excellent designers: it can take a year of programming before a team understands what the best design should have been (Fowler, 2009).

#### 3. Hidden technical debt in ML systems

ML debt is hard to detect because it exists at the system level rather than the code level (Sculley et al., 2015). Sculley et al. (2015) describe several risk factors:
- **Entanglement:** changing one input feature can change the weights and use of all others, which they call CACE, "Changing Anything Changes Everything".
- **Undeclared consumers:** other systems silently use a model's output as input, creating a hidden tight coupling and possibly hidden feedback loops.
- **Unstable and underutilised data dependencies:** input signals change behaviour over time, for example when they come from another model; unnecessary features can be found with regular leave-one-feature-out evaluations.
- **Feedback loops:** live systems influence their own future training data, directly or indirectly through the world.
- **System anti-patterns:** a mature system may be at most 5% ML code and at least 95% glue code; data preparation turns into pipeline jungles; experimental code paths left in production code raise complexity.
- **Configuration debt:** in a mature system, lines of configuration can far exceed lines of code, and each can contain a mistake.
- **Changes in the external world:** manually set decision thresholds become invalid when the model is updated, and tests alone do not show that a system still works in a changing world.

#### Origin and variants

Cunningham introduced the metaphor in an OOPSLA 1992 experience report on the WyCASH+ portfolio management system, built in Smalltalk by incremental growth from a working prototype; he argued that the modularity of objects and the practice of consolidation make incremental growth feasible, whereas the waterfall approach amounts to paying up front and in full (Cunningham, 1992). Fowler's quadrant answered the debate over which flaws count as debt (Fowler, 2009), and Sculley et al. (2015) applied the framework to machine learning systems.

### When to use it

- Deciding whether to clean up a part of the code before adding features to it, by comparing the interest on upcoming changes with the cost of paying down the principal (Fowler, 2019).
- Explaining design problems to non-technical people, for whom the debt metaphor is particularly handy (Fowler, 2009).
- Reviewing the design of ML systems for system-level risks such as entanglement, glue code and undeclared consumers (Sculley et al., 2015).

### Strengths and limitations

**Strengths**
- Frames quality work as an economic choice between paying interest and paying down principal (Fowler, 2019).
- Covers both deliberate shortcuts and the debt that only becomes visible as a team learns (Fowler, 2009).

**Limitations**
- The metaphor gives no strict metric that can be tracked over time; a team that still moves quickly is not evidence of low debt (Sculley et al., 2015).
- It is sometimes used to justify neglecting internal quality, although cruft slows down the very features that are needed quickly and teams reach the point where the shortcut stops paying off within weeks rather than months (Fowler, 2019).
- Unlike financial interest, technical interest is triggered by changes rather than by the passage of time, and prudent, inadvertent debt has no financial parallel (Fowler, 2019; Fowler, 2009).

### Comparison

| | Reckless | Prudent |
|---|----------|---------|
| **Deliberate** | Skipping design because there seems to be no time for clean code | Knowingly taking a shortcut to reach a release and planning to pay it back |
| **Inadvertent** | Messy code from a team that does not know good design practices | Realising after delivery what the design should have been |

Source: Fowler (2009).

### In practice

Debt is paid down by refactoring code, improving unit tests, deleting dead code, reducing dependencies, tightening APIs and improving documentation; the goal is not new functionality but future improvements, fewer errors and better maintainability (Sculley et al., 2015). Code with debt is best cleaned up where it is touched anyway, as described in [[clean-code|clean code]]. For ML systems, useful questions are how easily an entirely new approach can be tested at full scale, what the transitive closure of all data dependencies is, how precisely the impact of a change can be measured, whether improving one model degrades others and how quickly new team members get up to speed; paying down ML debt often requires a shift in team culture (Sculley et al., 2015). Practices against ML debt are covered in [[mlops-and-deployment|MLOps and deployment]], [[data-pipelines|data pipelines]] and [[monitoring-and-alerting|monitoring and alerting]]; the risk of code that nobody understands any more is discussed in [[vibe-coding|vibe coding]].

### Key takeaway

Technical debt is the extra effort that deficient internal quality adds to every change; it can be a sensible deliberate choice, but it has to be paid down where code changes often, and ML systems accumulate additional hidden debt at the system level.

### Sources

- Cunningham, W. (1992). *The WyCash Portfolio Management System.* OOPSLA '92 Experience Report. [c2.com](http://c2.com/doc/oopsla92.html)
- Fowler, M. (2019). *Technical Debt.* martinfowler.com, 21 May 2019. [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebt.html)
- Fowler, M. (2009). *Technical Debt Quadrant.* martinfowler.com, 14 October 2009. [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Technische Schulden sind eine von Ward Cunningham geprägte Metapher für Mängel in der inneren Qualität von Software, die Änderungen und Erweiterungen erschweren; der Mehraufwand, den sie bei jedem neuen Feature verursachen, sind die Zinsen auf die Schulden (Fowler, 2019). Cunningham verglich das Ausliefern von Code in erster Fassung mit dem Aufnehmen von Schulden: Ein wenig Schulden beschleunigt die Entwicklung, solange sie zügig durch eine Überarbeitung zurückgezahlt werden, aber jede Minute, die für nicht ganz richtigen Code aufgewendet wird, zählt als Zins (Cunningham, 1992). Schulden können bewusst oder unbewusst und umsichtig oder leichtsinnig entstehen (Fowler, 2009). Machine-Learning-Systeme haben alle Wartungsprobleme herkömmlichen Codes und zusätzlich ML-spezifische Schulden auf Systemebene, die gewöhnliches [[refactoring|Refactoring]] nicht beseitigt (Sculley et al., 2015).

### Funktionsweise

```text
schnelle oder nicht ganz richtige Lösung (bewusst oder unbewusst)
 ▼
Tilgungsbetrag: der Mangel in der inneren Qualität („Cruft“)
 ▼
Zinsen: Mehraufwand bei jeder Änderung an diesem Teil des Systems
 ▼
Entscheidung je Bereich: weiter Zinsen zahlen  oder  Schulden tilgen
  (Refactoring, Tests, toten Code löschen, weniger Abhängigkeiten, Dokumentation)
```

#### 1. Tilgung und Zinsen

Fowler veranschaulicht die Metapher mit einer unübersichtlichen Modulstruktur: Ein Feature, das bei klarer Struktur vier Tage dauern würde, dauert sechs, und die zwei Tage Unterschied sind die Zinsen. Fünf Tage in das Aufräumen der Struktur zu stecken, tilgt die Schulden; für ein einzelnes Feature lohnt sich das nicht, neun statt sechs Tage, aber wenn zwei weitere ähnliche Features anstehen, ist es schneller, den Cruft zuerst zu entfernen. Da sich Produktivität nicht objektiv messen lässt und solche Schätzungen ungenau sind, ist der übliche Weg, die Schulden schrittweise zu tilgen und mit jedem Feature etwas Cruft zu entfernen. Zinsen fallen nur an, wenn ein Teil des Codes geändert wird; unaufgeräumte, aber stabile Bereiche können daher bleiben, wie sie sind, während Bereiche mit hoher Aktivität null Toleranz für Cruft brauchen, weil er sich dort ansammelt, wo Änderungen ohne Blick auf die innere Qualität erfolgen (Fowler, 2019).

#### 2. Der Schuldenquadrant

Ob ein Designfehler als Schuld zählt, ist die falsche Frage; hilfreich ist die Unterscheidung zwischen umsichtigen und leichtsinnigen sowie zwischen bewussten und unbewussten Schulden. Ein Team, das wissentlich eine Abkürzung nimmt, um ein Release zu erreichen, und den Nutzen gegen die Kosten abwägt, nimmt umsichtige, bewusste Schulden auf. Ein Team, das gute Designpraktiken nicht kennt, nimmt leichtsinnige Schulden auf, ohne es zu merken, und ein Team, das „quick and dirty“ arbeitet, weil es glaubt, sich sauberen Code nicht leisten zu können, nimmt meist leichtsinnige, bewusste Schulden auf. Umsichtige, unbewusste Schulden sind selbst für hervorragende Designer unvermeidlich: Oft dauert es ein Jahr Programmierarbeit, bis ein Team versteht, wie das beste Design hätte aussehen sollen (Fowler, 2009).

#### 3. Versteckte technische Schulden in ML-Systemen

ML-Schulden sind schwer zu erkennen, weil sie auf Systemebene statt auf Codeebene bestehen (Sculley et al., 2015). Sculley et al. (2015) beschreiben mehrere Risikofaktoren:
- **Verflechtung:** Die Änderung eines Eingabemerkmals kann die Gewichte und die Nutzung aller anderen verändern, was sie CACE nennen, „Changing Anything Changes Everything“.
- **Nicht deklarierte Nutzer:** Andere Systeme nutzen die Ausgabe eines Modells unbemerkt als Eingabe, was eine versteckte enge Kopplung und möglicherweise versteckte Rückkopplungsschleifen erzeugt.
- **Instabile und kaum genutzte Datenabhängigkeiten:** Eingangssignale ändern ihr Verhalten mit der Zeit, etwa wenn sie von einem anderen Modell stammen; unnötige Merkmale lassen sich mit regelmäßigen Leave-one-feature-out-Evaluationen finden.
- **Rückkopplungsschleifen:** Live-Systeme beeinflussen ihre eigenen künftigen Trainingsdaten, direkt oder indirekt über die Welt.
- **Anti-Patterns auf Systemebene:** Ein ausgereiftes System kann zu höchstens 5 % aus ML-Code und zu mindestens 95 % aus Glue Code bestehen; die Datenaufbereitung wird zum Pipeline-Dschungel; im Produktionscode verbliebene experimentelle Codepfade erhöhen die Komplexität.
- **Konfigurationsschulden:** In einem ausgereiften System kann die Zahl der Konfigurationszeilen die der Codezeilen weit übersteigen, und jede kann einen Fehler enthalten.
- **Veränderungen in der Außenwelt:** Manuell gesetzte Entscheidungsschwellen werden ungültig, wenn das Modell aktualisiert wird, und Tests allein zeigen nicht, dass ein System in einer sich ändernden Welt noch funktioniert.

#### Herkunft und Varianten

Cunningham führte die Metapher 1992 in einem Erfahrungsbericht auf der OOPSLA über das Portfolio-Management-System WyCASH+ ein, das in Smalltalk schrittweise aus einem funktionierenden Prototyp entwickelt wurde; er argumentierte, dass die Modularität von Objekten und die Praxis der Konsolidierung schrittweises Wachstum möglich machen, während das Wasserfallmodell darauf hinausläuft, im Voraus und vollständig zu bezahlen (Cunningham, 1992). Fowlers Quadrant beantwortete die Debatte, welche Mängel als Schulden zählen (Fowler, 2009), und Sculley et al. (2015) übertrugen das Konzept auf Machine-Learning-Systeme.

### Wann einsetzen

- Entscheiden, ob ein Teil des Codes vor neuen Features aufgeräumt wird, indem die Zinsen anstehender Änderungen mit den Kosten der Tilgung verglichen werden (Fowler, 2019).
- Designprobleme Menschen ohne technischen Hintergrund erklären, wofür die Schuldenmetapher besonders gut geeignet ist (Fowler, 2009).
- Das Design von ML-Systemen auf Risiken auf Systemebene prüfen, etwa Verflechtung, Glue Code und nicht deklarierte Nutzer (Sculley et al., 2015).

### Stärken und Grenzen

**Stärken**
- Stellt Qualitätsarbeit als wirtschaftliche Wahl zwischen Zinszahlung und Tilgung dar (Fowler, 2019).
- Erfasst sowohl bewusste Abkürzungen als auch Schulden, die erst sichtbar werden, während ein Team dazulernt (Fowler, 2009).

**Grenzen**
- Die Metapher liefert keine feste Kennzahl, die sich über die Zeit verfolgen lässt; dass ein Team noch schnell vorankommt, belegt keine geringen Schulden (Sculley et al., 2015).
- Sie wird manchmal genutzt, um vernachlässigte innere Qualität zu rechtfertigen, obwohl Cruft gerade die dringend benötigten Features verlangsamt und Teams den Punkt, ab dem sich die Abkürzung nicht mehr lohnt, eher nach Wochen als nach Monaten erreichen (Fowler, 2019).
- Anders als finanzielle Zinsen fallen technische Zinsen bei Änderungen an und nicht mit der Zeit, und umsichtige, unbewusste Schulden haben keine finanzielle Entsprechung (Fowler, 2019; Fowler, 2009).

### Vergleich

| | Leichtsinnig | Umsichtig |
|---|--------------|-----------|
| **Bewusst** | Design auslassen, weil scheinbar keine Zeit für sauberen Code bleibt | Wissentlich eine Abkürzung für ein Release nehmen und die Rückzahlung einplanen |
| **Unbewusst** | Unordentlicher Code eines Teams, das gute Designpraktiken nicht kennt | Nach der Auslieferung erkennen, wie das Design hätte aussehen sollen |

Quelle: Fowler (2009).

### In der Praxis

Schulden werden getilgt, indem Code refaktoriert, [[software-testing|Unit-Tests]] verbessert, toter Code gelöscht, Abhängigkeiten reduziert, APIs geschärft und die Dokumentation verbessert wird; Ziel ist keine neue Funktionalität, sondern künftige Verbesserungen, weniger Fehler und bessere Wartbarkeit (Sculley et al., 2015). Code mit Schulden wird am besten dort aufgeräumt, wo er ohnehin angefasst wird, wie bei [[clean-code|Clean Code]] beschrieben. Für ML-Systeme helfen die Fragen, wie leicht sich ein völlig neuer Ansatz im vollen Maßstab testen lässt, wie die transitive Hülle aller Datenabhängigkeiten aussieht, wie genau sich die Wirkung einer Änderung messen lässt, ob die Verbesserung eines Modells andere verschlechtert und wie schnell neue Teammitglieder einsteigen können; die Tilgung von ML-Schulden erfordert oft einen Wandel der Teamkultur (Sculley et al., 2015). Praktiken gegen ML-Schulden behandeln [[mlops-and-deployment|MLOps und Deployment]], [[data-pipelines|Datenpipelines]] und [[monitoring-and-alerting|Monitoring und Alerting]]; das Risiko von Code, den niemand mehr versteht, behandelt [[vibe-coding|Vibe Coding]].

### Merksatz

Technische Schulden sind der Mehraufwand, den mangelhafte innere Qualität jeder Änderung hinzufügt; sie können eine sinnvolle bewusste Entscheidung sein, müssen aber dort getilgt werden, wo sich Code oft ändert, und ML-Systeme häufen zusätzlich versteckte Schulden auf Systemebene an.

### Quellen

- Cunningham, W. (1992). *The WyCash Portfolio Management System.* OOPSLA '92 Experience Report. [c2.com](http://c2.com/doc/oopsla92.html)
- Fowler, M. (2019). *Technical Debt.* martinfowler.com, 21. Mai 2019. [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebt.html)
- Fowler, M. (2009). *Technical Debt Quadrant.* martinfowler.com, 14. Oktober 2009. [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
