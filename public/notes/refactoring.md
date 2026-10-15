---
title_en: Refactoring
title_de: Refactoring
entity_type: Method
aliases:
- Refactoring
- Code refactoring
- Refaktorisierung
sources:
- https://refactoring.com/
- https://refactoring.com/catalog/
- https://martinfowler.com/books/refactoring.html
- https://martinfowler.com/bliki/DefinitionOfRefactoring.html
- https://martinfowler.com/bliki/RefactoringMalapropism.html
- https://martinfowler.com/bliki/OpportunisticRefactoring.html
- https://martinfowler.com/bliki/CodeSmell.html
- https://martinfowler.com/bliki/TestDrivenDevelopment.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Refactoring is "a disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior"; its heart is a series of small behaviour-preserving transformations, each called a refactoring, so the system keeps working after every step (Fowler, n.d.-a). As a noun, a refactoring is "a change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior" (Fowler, 2004a). [[martin-fowler|Martin Fowler]]'s book *Refactoring*, first published in 1999 and in a second edition with [[kent-beck|Kent Beck]] in 2018, catalogues around seventy such transformations (Fowler, 2018). Refactoring is a regular part of programming rather than a project phase, and it is the third step of test-driven development: red, green, refactor (Fowler, n.d.-a; Fowler, 2023).

### How it works

```text
tests green
  └─ spot a code smell (long function, duplication, data class, …)
       └─ apply one small refactoring (e.g. Extract Function, Rename Variable, Move Function)
            └─ run tests → still green? → commit / next step
                 └─ many small steps add up to a significant restructuring
never: system broken for days → that is restructuring, not refactoring
```

#### 1. Small, behaviour-preserving steps

Each refactoring does little and is "too small to be worth doing", but a sequence of them can produce a significant restructuring; because each step is small it is less likely to go wrong, and the system can be refactored gradually over a long period without being broken (Fowler, 2018). The second-edition catalogue lists refactorings such as Change Function Declaration, Extract Function, Extract Variable, Encapsulate Collection and Decompose Conditional, each with a motivation, mechanics and an example (Fowler, n.d.-b; Fowler, 2018).

#### 2. Code smells as triggers

A code smell is "a surface indication that usually corresponds to a deeper problem in the system", a term coined by Kent Beck while helping with the *Refactoring* book (Fowler, 2006). Smells are quick to spot, for example a long method or a class with data but no behaviour, but do not always indicate a problem; they point to where refactoring may help (Fowler, 2006).

#### 3. Tests as a safety net

Refactoring should only be done when the tests are green (Fowler, 2011). Automated refactorings in IDEs make many common transformations faster, but they are not essential: without tool support, small steps and frequent testing catch mistakes (Fowler, n.d.-a). In test-driven development, the cycle is to write a failing test, write code until it passes and then refactor new and old code; neglecting this third step is the most common way to get TDD wrong (Fowler, 2023).

#### 4. When to refactor

Fowler prefers opportunistic refactoring: whenever someone sees unclear code, they fix it then or within minutes, following the camp site rule of leaving code better than they found it (Fowler, 2011). Preparatory refactoring restructures existing code before adding a feature so that the change becomes easy; after adding it, a further refactoring makes the working code clearer (Fowler, n.d.-a; Fowler, 2011).

#### Origin and variants

Fowler wrote the first edition of *Refactoring* in 1997–1999, with examples in Java; the second edition uses JavaScript and is mirrored by an online web edition and catalogue (Fowler, n.d.-a). He calls himself "not the father or the inventor of refactoring - just a documenter" and distinguishes refactoring from the general term restructuring: if a system is broken for days, or the object has no well-defined behaviour, such as a document, it is not refactoring (Fowler, 2004b).

### When to use it

- Before adding a feature, when the existing structure makes the change hard (preparatory refactoring) (Fowler, n.d.-a).
- After getting code to work, to make it clear for the next reader, and as the third step of every TDD cycle (Fowler, n.d.-a; Fowler, 2023).
- To pay down [[technical-debt|technical debt]], including in [[ml-pipelines|ML pipelines]] where glue code and dead experimental paths accumulate.
- Not as a label for large rewrites that break the system for days; that is restructuring (Fowler, 2004b).

### Strengths and limitations

**Strengths**
- Lowers the cost of future enhancements, because changes are no longer stacked on increasingly tangled code (Fowler, n.d.-a).
- Low risk per step, and the system stays working throughout (Fowler, 2018).
- Easy to fit into everyday work: no separate project phase is needed (Fowler, 2011).

**Limitations**
- Depends on good tests; without them, behaviour preservation cannot be checked (Fowler, 2011).
- Opportunistic refactoring can turn into a rabbit hole; it takes judgement to stop (Fowler, 2011).
- The term is often misused for any restructuring, which blurs what is actually being done (Fowler, 2004b).

### Comparison

| | Refactoring | Restructuring (general) |
|---|---|---|
| Definition | specific technique of small behaviour-preserving transformations | any rearrangement of parts of a whole |
| Object | code with well-defined behaviour | also documents or other artefacts |
| System state | broken for at most a few minutes | may be broken for days |

Sources: Fowler (2004b); Fowler (n.d.-a).

### In practice

Teams can learn to spot smells one at a time, for example with a "smell of the week" that everyone looks for and raises with senior team members (Fowler, 2006; [[clean-code|clean code]]). Small refactorings fit continuous integration, where small, frequent integrations keep conflicts small ([[ci-cd|CI/CD]]). Refactoring with AI coding assistants is one of the topics on Fowler's site ([[martin-fowler|Martin Fowler]]); the rule still holds that refactoring starts only from green tests (Fowler, 2011).

### Key takeaway

Refactoring improves the internal structure of code through many tiny, test-protected transformations that never change what the code does; it is part of everyday programming, not a separate project.

### Sources

- Fowler, M. (n.d.-a). *Refactoring* (refactoring.com). [refactoring.com](https://refactoring.com/)
- Fowler, M. (n.d.-b). *Catalog of Refactorings*. [refactoring.com](https://refactoring.com/catalog/)
- Fowler, M. with Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2nd ed. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Fowler, M. (2004a). *Definition Of Refactoring*. [martinfowler.com](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)
- Fowler, M. (2004b). *Refactoring Malapropism*. [martinfowler.com](https://martinfowler.com/bliki/RefactoringMalapropism.html)
- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. (2011). *Opportunistic Refactoring*. [martinfowler.com](https://martinfowler.com/bliki/OpportunisticRefactoring.html)
- Fowler, M. (2023). *Test Driven Development*. [martinfowler.com](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Refactoring ist „a disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior“; sein Kern ist eine Folge kleiner, verhaltenserhaltender Transformationen, die jeweils selbst „Refactoring“ heißen, sodass das System nach jedem Schritt funktioniert (Fowler, n.d.-a). Als Substantiv ist ein Refactoring „a change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior“ (Fowler, 2004a). Das Buch *Refactoring* von [[martin-fowler|Martin Fowler]], 1999 erschienen und 2018 in zweiter Auflage mit [[kent-beck|Kent Beck]], beschreibt rund siebzig solcher Transformationen (Fowler, 2018). Refactoring ist ein regulärer Teil des Programmierens statt einer Projektphase und der dritte Schritt der testgetriebenen Entwicklung: Red, Green, Refactor (Fowler, n.d.-a; Fowler, 2023).

### Funktionsweise

```text
Tests grün
  └─ Code Smell erkennen (lange Funktion, Duplikat, Datenklasse, …)
       └─ ein kleines Refactoring anwenden (z. B. Extract Function, Rename Variable, Move Function)
            └─ Tests ausführen → weiter grün? → Commit / nächster Schritt
                 └─ viele kleine Schritte ergeben eine erhebliche Umstrukturierung
nie: System tagelang kaputt → das ist Restrukturierung, kein Refactoring
```

#### 1. Kleine, verhaltenserhaltende Schritte

Jedes Refactoring bewirkt wenig und ist für sich „too small to be worth doing“, doch eine Folge davon kann eine erhebliche Umstrukturierung ergeben; weil jeder Schritt klein ist, geht er seltener schief, und das System lässt sich über lange Zeit schrittweise umbauen, ohne kaputt zu sein (Fowler, 2018). Der Katalog der zweiten Auflage umfasst Refactorings wie Change Function Declaration, Extract Function, Extract Variable, Encapsulate Collection und Decompose Conditional, jeweils mit Motivation, Vorgehen und Beispiel (Fowler, n.d.-b; Fowler, 2018).

#### 2. Code Smells als Auslöser

Ein Code Smell ist „a surface indication that usually corresponds to a deeper problem in the system“, ein Begriff, den Kent Beck bei der Mitarbeit am Buch *Refactoring* prägte (Fowler, 2006). Smells sind schnell zu erkennen, etwa eine lange Methode oder eine Klasse mit Daten, aber ohne Verhalten, weisen aber nicht immer auf ein Problem hin; sie zeigen, wo Refactoring helfen kann (Fowler, 2006).

#### 3. Tests als Sicherheitsnetz

Refactoring sollte nur bei grünen Tests stattfinden (Fowler, 2011). Automatisierte Refactorings in Entwicklungsumgebungen machen viele übliche Transformationen schneller, sind aber nicht unverzichtbar: Ohne Werkzeugunterstützung fangen kleine Schritte und häufiges Testen Fehler ab (Fowler, n.d.-a). In der testgetriebenen Entwicklung wird ein fehlschlagender Test geschrieben, dann Code, bis er besteht, und dann neuer und alter Code refaktoriert; diesen dritten Schritt zu vernachlässigen ist der häufigste Fehler bei TDD (Fowler, 2023).

#### 4. Wann refaktorieren

Fowler bevorzugt opportunistisches Refactoring: Wer unklaren Code sieht, verbessert ihn sofort oder innerhalb weniger Minuten, nach der Pfadfinderregel, Code besser zu hinterlassen als vorgefunden (Fowler, 2011). Vorbereitendes Refactoring baut bestehenden Code vor einem neuen Feature so um, dass die Änderung leicht wird; nach dem Hinzufügen macht ein weiteres Refactoring den funktionierenden Code klarer (Fowler, n.d.-a; Fowler, 2011).

#### Herkunft und Varianten

Fowler schrieb die erste Auflage von *Refactoring* 1997–1999 mit Beispielen in Java; die zweite Auflage nutzt JavaScript und wird durch eine Web-Ausgabe und einen Online-Katalog ergänzt (Fowler, n.d.-a). Er sieht sich als „not the father or the inventor of refactoring - just a documenter“ und grenzt Refactoring vom allgemeinen Begriff der Restrukturierung ab: Ist ein System tagelang kaputt oder hat der Gegenstand kein klar definiertes Verhalten, etwa ein Dokument, handelt es sich nicht um Refactoring (Fowler, 2004b).

### Wann einsetzen

- Vor einem neuen Feature, wenn die bestehende Struktur die Änderung erschwert (vorbereitendes Refactoring) (Fowler, n.d.-a).
- Nachdem Code funktioniert, um ihn für die nächste lesende Person klar zu machen, und als dritter Schritt jedes TDD-Zyklus (Fowler, n.d.-a; Fowler, 2023).
- Zum Abbau [[technical-debt|technischer Schulden]], auch in [[ml-pipelines|ML-Pipelines]], in denen sich Glue Code und tote Experimentierpfade ansammeln.
- Nicht als Bezeichnung für große Umbauten, die das System tagelang lahmlegen; das ist Restrukturierung (Fowler, 2004b).

### Stärken und Grenzen

**Stärken**
- Senkt die Kosten künftiger Erweiterungen, weil Änderungen nicht mehr auf zunehmend verworrenen Code gestapelt werden (Fowler, n.d.-a).
- Geringes Risiko je Schritt, und das System bleibt durchgehend funktionsfähig (Fowler, 2018).
- Leicht in die tägliche Arbeit einzubauen: Eine eigene Projektphase ist nicht nötig (Fowler, 2011).

**Grenzen**
- Hängt von guten Tests ab; ohne sie lässt sich der Erhalt des Verhaltens nicht prüfen (Fowler, 2011).
- Opportunistisches Refactoring kann sich verzetteln; es braucht Urteilsvermögen, wann Schluss ist (Fowler, 2011).
- Der Begriff wird oft für jede Restrukturierung missbraucht, was verwischt, was tatsächlich geschieht (Fowler, 2004b).

### Vergleich

| | Refactoring | Restrukturierung (allgemein) |
|---|---|---|
| Definition | spezifische Technik kleiner, verhaltenserhaltender Transformationen | jede Neuanordnung von Teilen eines Ganzen |
| Gegenstand | Code mit klar definiertem Verhalten | auch Dokumente oder andere Artefakte |
| Zustand des Systems | höchstens wenige Minuten kaputt | kann tagelang kaputt sein |

Quellen: Fowler (2004b); Fowler (n.d.-a).

### In der Praxis

Teams können lernen, Smells einzeln zu erkennen, etwa mit einem „smell of the week“, nach dem alle suchen und den sie mit erfahrenen Teammitgliedern besprechen (Fowler, 2006; [[clean-code|Clean Code]]). Kleine Refactorings passen zur kontinuierlichen Integration, in der kleine, häufige Integrationen Konflikte klein halten ([[ci-cd|CI/CD]]). Refactoring mit KI-Programmierassistenten ist eines der Themen auf Fowlers Website ([[martin-fowler|Martin Fowler]]); die Regel, nur bei grünen Tests zu refaktorieren, gilt weiter (Fowler, 2011).

### Merksatz

Refactoring verbessert die innere Struktur von Code durch viele winzige, durch Tests abgesicherte Transformationen, die nie ändern, was der Code tut; es gehört zum täglichen Programmieren und ist kein eigenes Projekt.

### Quellen

- Fowler, M. (n.d.-a). *Refactoring* (refactoring.com). [refactoring.com](https://refactoring.com/)
- Fowler, M. (n.d.-b). *Catalog of Refactorings*. [refactoring.com](https://refactoring.com/catalog/)
- Fowler, M. mit Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2. Aufl. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Fowler, M. (2004a). *Definition Of Refactoring*. [martinfowler.com](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)
- Fowler, M. (2004b). *Refactoring Malapropism*. [martinfowler.com](https://martinfowler.com/bliki/RefactoringMalapropism.html)
- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. (2011). *Opportunistic Refactoring*. [martinfowler.com](https://martinfowler.com/bliki/OpportunisticRefactoring.html)
- Fowler, M. (2023). *Test Driven Development*. [martinfowler.com](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
