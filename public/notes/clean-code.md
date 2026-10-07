---
title_en: Clean Code
title_de: Clean Code
entity_type: Concept
sources:
- https://peps.python.org/pep-0008/
- https://martinfowler.com/bliki/CodeSmell.html
- https://martinfowler.com/bliki/TechnicalDebt.html
- https://refactoring.com/
- https://google.github.io/eng-practices/review/reviewer/looking-for.html
- https://qntm.org/clean
- https://doi.org/10.1145/361598.361623
- https://doi.org/10.1109/TSE.2009.70
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Clean code is code that other people can read, understand and change safely: clear names, small units with one responsibility, a consistent style, tests and comments that explain why rather than what. The underlying insight is that code is read much more often than it is written (PEP 8). The term goes back to Robert C. Martin's 2008 book Clean Code, whose basic advice is widely accepted but whose stricter rules, such as functions of two to four lines, are criticised as dogmatic (qntm, 2020). Measured readability correlates with software quality, such as fewer changes and defect reports (Buse & Weimer, 2010).

### How it works

#### 1. Readability first

Code is read far more often than it is written, so guidelines aim at readability and consistency: consistency within a project matters more than with a general style guide, and consistency within a module or function matters most (PEP 8). Readability can be measured: a model trained on judgements of 120 annotators was 80 percent effective at predicting readability judgements, and its scores correlated with code changes and defect reports in over 2.2 million lines of code (Buse & Weimer, 2010).

#### 2. Names

A good name is long enough to communicate what an item is or does, without becoming hard to read (Google code review guide). Names of public API elements reflect their usage, not their implementation (PEP 8).

```python
# unclear
def calc(d, f):
    return [x for x in d if x[2] > f]

# clear
def contracts_above_value(contracts, minimum_value):
    return [contract for contract in contracts if contract.value > minimum_value]
```

#### 3. Functions and modules

Widely accepted advice on functions: do not mix levels of abstraction, do one thing, choose descriptive and consistent names, avoid hidden side effects and output arguments, and separate commands that change state from queries that answer questions (qntm, 2020). At module level, the criteria used to divide a system into modules determine how flexible and understandable it is (Parnas, 1972).

#### 4. Comments

Comments should usually explain why code exists, not what it does; if the code cannot explain itself, it should be made simpler. Exceptions are regular expressions or complex algorithms (Google code review guide).

```python
# bad: repeats the code
i += 1  # increment i

# good: explains the decision
# Contract clause 7: the notice period starts on the day after delivery.
deadline = delivery_date + timedelta(days=1) + notice_period
```

#### 5. Simplicity instead of speculation

Code that cannot be understood quickly or invites bugs is too complex; reviewers watch especially for over-engineering, code made more generic than needed or functionality not needed yet: solve the problem that exists now (Google code review guide). A little duplication can be clearer and cheaper than the wrong abstraction (qntm, 2020).

#### 6. Code smells, refactoring and technical debt

A code smell, such as a long method or a class with only data and no behaviour, is a surface indication that usually points to a deeper problem, but not always (Fowler, CodeSmell). Refactoring removes such problems in small, behaviour-preserving steps, keeping the system working after each step (Fowler, Refactoring). Unclean code accumulates technical debt: the extra effort for every new feature is the interest; paying it off gradually concentrates clean-up where code changes most often (Fowler, TechnicalDebt).

#### 7. Tests

Tests belong in the same change as the code, must fail when the code is broken and are themselves code that has to be maintained (Google code review guide); they make refactoring safe ([[regression-testing|Regression Testing]]).

#### Origin and variants

Modular design as a means to flexibility and comprehensibility goes back to the early 1970s (Parnas, 1972). The term clean code became popular through Robert C. Martin's 2008 book; its strict rules on function length, nesting and number of arguments are disputed, and A Philosophy of Software Design by John Ousterhout (2018) is recommended as a more current alternative focused on design (qntm, 2020). Language style guides such as PEP 8 (PEP 8) and review guidelines such as Google's (Google code review guide) turn the principles into concrete rules.

### When to use it

- Always for code that others will read, change or review, including one's future self.
- Especially for long-lived code, shared libraries and APIs ([[apis|APIs]]).
- With less rigour for throwaway prototypes, as long as they stay throwaway.

### Strengths and limitations

**Strengths**
- Readable code is easier to review, change and debug, and readability correlates with fewer changes and defects (Buse & Weimer, 2010).
- Small, behaviour-preserving refactorings keep code changeable over time (Fowler, Refactoring).
- A shared style reduces friction in teams (PEP 8).

**Limitations**
- There is no empirical definition of clean code; many rules are opinions (qntm, 2020).
- Rules applied dogmatically, such as very short functions or zero duplication, can make code harder to follow (qntm, 2020).
- Clean-up costs time, and its benefit can only be estimated, not measured exactly (Fowler, TechnicalDebt).
- A style guide must yield to backwards compatibility and local consistency (PEP 8).

### Comparison

| Practice | How it differs | Suited for |
|----------|----------------|------------|
| Style guide | Fixes formatting and naming conventions (PEP 8) | Consistency, automatic checks with linters |
| Code review | People check design, complexity, tests and names (Google code review guide) | Every change |
| Refactoring | Improves structure without changing behaviour (Fowler, Refactoring) | Code that is changed frequently |
| Clean Code rules | Principles for names, functions and comments (qntm, 2020) | Orientation, not as fixed laws |

### In practice

Formatters and linters enforce the style automatically, so that reviews can focus on design and naming ([[python|Python]]); small, well-described commits make changes reviewable and reversible ([[git|Git]]). Code with technical debt is cleaned up where it is touched anyway. With AI-generated code, the ability to judge code becomes more important: instruction files can tell coding agents the project's conventions, and generated code is checked like any other ([[vibe-coding|Vibe Coding]]; [[harness-engineering|Harness Engineering]]; [[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]]). The same principles apply to ML code and pipelines, where readable, tested code supports reproducibility ([[quality-control|Quality Control]]; [[mlops-and-deployment|MLOps and Deployment]]).

### Key takeaway

Clean code optimises for the reader: clear names, focused units, comments that explain why and tests that make change safe; the principles are useful, but they are judgement calls, not laws.

### Sources

- van Rossum, G., Warsaw, B. & Coghlan, A. (2001). *PEP 8 – Style Guide for Python Code.* Python Enhancement Proposals. [peps.python.org](https://peps.python.org/pep-0008/)
- Fowler, M. *CodeSmell.* martinfowler.com (bliki). [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. *TechnicalDebt.* martinfowler.com (bliki). [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebt.html)
- Fowler, M. *Refactoring.* refactoring.com. [refactoring.com](https://refactoring.com/)
- Google. *What to look for in a code review.* Google Engineering Practices Documentation. [google.github.io](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- qntm (2020). *It's probably time to stop recommending Clean Code.* Things Of Interest, 28 June 2020. [qntm.org](https://qntm.org/clean)
- Parnas, D. L. (1972). *On the criteria to be used in decomposing systems into modules.* Communications of the ACM 15(12). [doi:10.1145/361598.361623](https://doi.org/10.1145/361598.361623)
- Buse, R. P. L. & Weimer, W. R. (2010). *Learning a Metric for Code Readability.* IEEE Transactions on Software Engineering 36(4). [doi:10.1109/TSE.2009.70](https://doi.org/10.1109/TSE.2009.70)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Clean Code ist Code, den andere lesen, verstehen und sicher ändern können: klare Namen, kleine Einheiten mit einer Verantwortung, ein einheitlicher Stil, Tests und Kommentare, die erklären, warum etwas so ist, statt was passiert. Dahinter steht die Einsicht, dass Code viel öfter gelesen als geschrieben wird (PEP 8). Der Begriff geht auf Robert C. Martins Buch Clean Code von 2008 zurück, dessen Grundratschläge breit akzeptiert sind, dessen strengere Regeln, etwa Funktionen von zwei bis vier Zeilen, aber als dogmatisch kritisiert werden (qntm, 2020). Gemessene Lesbarkeit hängt mit Softwarequalität zusammen, etwa mit weniger Änderungen und Fehlerberichten (Buse & Weimer, 2010).

### Funktionsweise

#### 1. Lesbarkeit zuerst

Code wird weit öfter gelesen als geschrieben, deshalb zielen Richtlinien auf Lesbarkeit und Einheitlichkeit: Einheitlichkeit innerhalb eines Projekts zählt mehr als die mit einem allgemeinen Styleguide, und Einheitlichkeit innerhalb eines Moduls oder einer Funktion zählt am meisten (PEP 8). Lesbarkeit lässt sich messen: Ein Modell, trainiert auf den Urteilen von 120 Annotierenden, war zu 80 Prozent wirksam darin, Lesbarkeitsurteile vorherzusagen, und seine Werte korrelierten mit Codeänderungen und Fehlerberichten in über 2,2 Millionen Codezeilen (Buse & Weimer, 2010).

#### 2. Namen

Ein guter Name ist lang genug, um zu sagen, was ein Element ist oder tut, ohne schwer lesbar zu werden (Google code review guide). Namen öffentlicher API-Elemente spiegeln ihre Verwendung wider, nicht ihre Implementierung (PEP 8).

```python
# unklar
def calc(d, f):
    return [x for x in d if x[2] > f]

# klar
def contracts_above_value(contracts, minimum_value):
    return [contract for contract in contracts if contract.value > minimum_value]
```

#### 3. Funktionen und Module

Breit akzeptierte Ratschläge zu Funktionen: keine Abstraktionsebenen vermischen, eine Sache tun, beschreibende und einheitliche Namen wählen, versteckte Nebenwirkungen und Ausgabeparameter vermeiden und Befehle, die Zustand ändern, von Abfragen trennen, die Fragen beantworten (qntm, 2020). Auf Modulebene bestimmen die Kriterien, nach denen ein System in Module zerlegt wird, wie flexibel und verständlich es ist (Parnas, 1972).

#### 4. Kommentare

Kommentare sollten meist erklären, warum Code existiert, nicht was er tut; kann sich der Code nicht selbst erklären, sollte er einfacher werden. Ausnahmen sind reguläre Ausdrücke oder komplexe Algorithmen (Google code review guide).

```python
# schlecht: wiederholt den Code
i += 1  # i erhöhen

# gut: erklärt die Entscheidung
# Vertragsklausel 7: Die Kündigungsfrist beginnt am Tag nach der Lieferung.
deadline = delivery_date + timedelta(days=1) + notice_period
```

#### 5. Einfachheit statt Spekulation

Code, der sich nicht schnell verstehen lässt oder zu Fehlern einlädt, ist zu komplex; Reviewende achten besonders auf Over-Engineering, also Code, der allgemeiner ist als nötig, oder Funktionen, die noch nicht gebraucht werden: das Problem lösen, das jetzt besteht (Google code review guide). Ein wenig Duplikation kann klarer und günstiger sein als die falsche Abstraktion (qntm, 2020).

#### 6. Code Smells, Refactoring und technische Schulden

Ein Code Smell, etwa eine lange Methode oder eine Klasse mit nur Daten und ohne Verhalten, ist ein oberflächliches Anzeichen, das meist, aber nicht immer auf ein tieferes Problem hinweist (Fowler, CodeSmell). Refactoring beseitigt solche Probleme in kleinen, verhaltenserhaltenden Schritten, wobei das System nach jedem Schritt funktionsfähig bleibt (Fowler, Refactoring). Unsauberer Code häuft technische Schulden an: Der Mehraufwand für jedes neue Feature sind die Zinsen; schrittweises Tilgen konzentriert das Aufräumen dort, wo Code am häufigsten geändert wird (Fowler, TechnicalDebt).

#### 7. Tests

Tests gehören in dieselbe Änderung wie der Code, müssen fehlschlagen, wenn der Code kaputt ist, und sind selbst Code, der gepflegt werden muss (Google code review guide); sie machen Refactoring sicher ([[regression-testing|Regressionstests]]).

#### Ursprung und Varianten

Modularer Entwurf als Mittel für Flexibilität und Verständlichkeit geht auf die frühen 1970er-Jahre zurück (Parnas, 1972). Der Begriff Clean Code wurde durch Robert C. Martins Buch von 2008 bekannt; seine strengen Regeln zu Funktionslänge, Verschachtelung und Zahl der Argumente sind umstritten, und A Philosophy of Software Design von John Ousterhout (2018) wird als aktuellere, stärker auf Entwurf ausgerichtete Alternative empfohlen (qntm, 2020). Sprach-Styleguides wie PEP 8 (PEP 8) und Review-Richtlinien wie die von Google (Google code review guide) übersetzen die Prinzipien in konkrete Regeln.

### Wann einsetzen

- Immer für Code, den andere lesen, ändern oder prüfen, einschließlich des eigenen zukünftigen Ichs.
- Besonders für langlebigen Code, gemeinsam genutzte Bibliotheken und APIs ([[apis|APIs (Programmierschnittstellen)]]).
- Mit weniger Strenge für Wegwerf-Prototypen, solange sie Wegwerf-Prototypen bleiben.

### Stärken und Grenzen

**Stärken**
- Lesbarer Code lässt sich leichter prüfen, ändern und debuggen, und Lesbarkeit hängt mit weniger Änderungen und Fehlern zusammen (Buse & Weimer, 2010).
- Kleine, verhaltenserhaltende Refactorings halten Code dauerhaft änderbar (Fowler, Refactoring).
- Ein gemeinsamer Stil verringert Reibung im Team (PEP 8).

**Einschränkungen**
- Es gibt keine empirische Definition von Clean Code; viele Regeln sind Meinungen (qntm, 2020).
- Dogmatisch angewandte Regeln, etwa sehr kurze Funktionen oder null Duplikation, können Code schwerer nachvollziehbar machen (qntm, 2020).
- Aufräumen kostet Zeit, und sein Nutzen lässt sich nur schätzen, nicht genau messen (Fowler, TechnicalDebt).
- Ein Styleguide muss hinter Abwärtskompatibilität und lokaler Einheitlichkeit zurückstehen (PEP 8).

### Vergleich

| Praxis | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Styleguide | Legt Formatierung und Namenskonventionen fest (PEP 8) | Einheitlichkeit, automatische Prüfung mit Lintern |
| Code-Review | Menschen prüfen Entwurf, Komplexität, Tests und Namen (Google code review guide) | Jede Änderung |
| Refactoring | Verbessert die Struktur, ohne das Verhalten zu ändern (Fowler, Refactoring) | Häufig geänderten Code |
| Clean-Code-Regeln | Prinzipien für Namen, Funktionen und Kommentare (qntm, 2020) | Orientierung, nicht als feste Gesetze |

### In der Praxis

Formatter und Linter setzen den Stil automatisch durch, sodass sich Reviews auf Entwurf und Benennung konzentrieren können ([[python|Python]]); kleine, gut beschriebene Commits machen Änderungen prüfbar und umkehrbar ([[git|Git]]). Code mit technischen Schulden wird dort aufgeräumt, wo er ohnehin angefasst wird. Bei KI-generiertem Code wird die Fähigkeit, Code zu beurteilen, wichtiger: Anweisungsdateien können Coding-Agenten die Projektkonventionen mitteilen, und erzeugter Code wird wie jeder andere geprüft ([[vibe-coding|Vibe Coding]]; [[harness-engineering|Harness Engineering]]; [[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]]). Dieselben Prinzipien gelten für ML-Code und Pipelines, wo lesbarer, getesteter Code die Reproduzierbarkeit unterstützt ([[quality-control|Qualitätskontrolle]]; [[mlops-and-deployment|MLOps und Deployment]]).

### Merksatz

Clean Code optimiert für die Lesenden: klare Namen, fokussierte Einheiten, Kommentare, die das Warum erklären, und Tests, die Änderungen sicher machen; die Prinzipien sind nützlich, aber Abwägungssache, keine Gesetze.

### Quellen

- van Rossum, G., Warsaw, B. & Coghlan, A. (2001). *PEP 8 – Style Guide for Python Code.* Python Enhancement Proposals. [peps.python.org](https://peps.python.org/pep-0008/)
- Fowler, M. *CodeSmell.* martinfowler.com (bliki). [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. *TechnicalDebt.* martinfowler.com (bliki). [martinfowler.com](https://martinfowler.com/bliki/TechnicalDebt.html)
- Fowler, M. *Refactoring.* refactoring.com. [refactoring.com](https://refactoring.com/)
- Google. *What to look for in a code review.* Google Engineering Practices Documentation. [google.github.io](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- qntm (2020). *It's probably time to stop recommending Clean Code.* Things Of Interest, 28 June 2020. [qntm.org](https://qntm.org/clean)
- Parnas, D. L. (1972). *On the criteria to be used in decomposing systems into modules.* Communications of the ACM 15(12). [doi:10.1145/361598.361623](https://doi.org/10.1145/361598.361623)
- Buse, R. P. L. & Weimer, W. R. (2010). *Learning a Metric for Code Readability.* IEEE Transactions on Software Engineering 36(4). [doi:10.1109/TSE.2009.70](https://doi.org/10.1109/TSE.2009.70)
