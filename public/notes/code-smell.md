---
title_en: Code Smell
title_de: Code Smell
entity_type: Concept
aliases:
- Code smell
- Code smells
- Design smell
sources:
- https://martinfowler.com/bliki/CodeSmell.html
- https://martinfowler.com/books/refactoring.html
- https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A code smell is "a surface indication that usually corresponds to a deeper problem in the system"; [[kent-beck|Kent Beck]] coined the term while helping [[martin-fowler|Martin Fowler]] with the book *Refactoring* (Fowler, 2006). A smell is quick to spot, for example a method longer than a dozen lines or a class with data but no behaviour, but it is not always a problem: it tells you where to look more closely, and the fix is usually [[refactoring|refactoring]] (Fowler, 2006). Sculley et al. (2015) carried the idea over to machine learning systems with smells such as the plain-old-data type smell, the multiple-language smell and the prototype smell, as indicators of [[technical-debt|technical debt]].

### How it works

```text
read code → notice a smell (quick, "sniffable")
  ├─ look deeper: is there an underlying problem?
  │     no  → leave it (some long methods are fine)
  │     yes → refactor in small, behaviour-preserving steps
  └─ examples: long method · data class without behaviour
     ML systems: plain-old-data types · multiple languages · prototype used in production
```

#### 1. A surface indication

The definition has two parts: a smell is by definition something quick to spot, and it does not always indicate a problem (Fowler, 2006). Fowler's example is a long method: "my nose twitches if I see more than a dozen lines of java", yet "some long methods are just fine" (Fowler, 2006).

#### 2. Leading to deeper problems

The best smells are easy to spot and most of the time lead to interesting problems. Data classes, with all data and no behaviour, prompt the question which behaviour belongs in the class, and refactoring then moves that behaviour there (Fowler, 2006). The *Refactoring* book has introductory chapters on the code smells that suggest refactoring, followed by a catalogue of around seventy refactorings (Fowler, 2018).

#### 3. Smells in ML systems

Sculley et al. (2015) describe ML system smells as "not hard-and-fast rules, but as subjective indicators": the plain-old-data type smell, where model parameters and predictions are raw floats and integers that do not know what they mean or which model produced them; the multiple-language smell, which raises testing costs and makes handing over ownership harder; and the prototype smell, where relying on a prototyping environment signals a brittle full-scale system and risks a prototype being used in production. Common processes with many manual steps are another system-level smell (Sculley et al., 2015).

#### Origin and variants

Beck coined the term while working with Fowler on *Refactoring*, first published in 1999 (Fowler, 2006; Fowler, 2018). Sculley et al. (2015) speak of "design smells" and add ML-specific ones.

### When to use it

- In code reviews, to name a pattern that deserves a closer look without claiming it is a bug ([[clean-code|clean code]]).
- When deciding what to refactor, as a pointer to the underlying problem (Fowler, 2006).
- For reviewing ML systems at the system level, using the smells of Sculley et al. (2015).

### Strengths and limitations

**Strengths**
- Easy to learn: inexperienced developers can spot smells even before they can judge or fix the underlying problem (Fowler, 2006).
- Gives teams a shared vocabulary; Fowler mentions leads who pick a "smell of the week" to train their teams (Fowler, 2006).

**Limitations**
- Subjective: a smell is an indicator, not a rule, and must be checked (Fowler, 2006; Sculley et al., 2015).
- Pointing out smells does not by itself fix anything; it takes judgement and refactoring (Fowler, 2006).

### Comparison

| | Code smell | Bug | Technical debt |
|---|---|---|---|
| What it is | surface indication of a possible design problem | wrong behaviour | accumulated cost of poor internal quality |
| Visible to users? | no | yes | indirectly, through slower change |
| Typical response | look deeper, refactor | fix | pay down, e.g. by refactoring |

Sources: Fowler (2006); [[technical-debt|technical debt]].

### In practice

When AI coding assistants generate code, smells such as ever-growing functions are a quick check before accepting a change; Kent Beck notes that today's assistants "lack taste" and will add another 20 lines to a giant function ([[kent-beck|Kent Beck]]). In [[ml-pipelines|ML pipelines]], typed objects for model outputs and fewer languages address the plain-old-data and multiple-language smells (Sculley et al., 2015).

### Key takeaway

A code smell is a quick-to-spot hint that something deeper may be wrong; it calls for a closer look and often a refactoring, not an automatic verdict.

### Sources

- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. with Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2nd ed. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Code Smell ist „a surface indication that usually corresponds to a deeper problem in the system“; [[kent-beck|Kent Beck]] prägte den Begriff, als er [[martin-fowler|Martin Fowler]] beim Buch *Refactoring* half (Fowler, 2006). Ein Smell ist schnell zu erkennen, etwa eine Methode mit mehr als einem Dutzend Zeilen oder eine Klasse mit Daten, aber ohne Verhalten, ist aber nicht immer ein Problem: Er zeigt, wo genauer hinzusehen ist, und die Abhilfe ist meist [[refactoring|Refactoring]] (Fowler, 2006). Sculley et al. (2015) übertrugen die Idee auf Systeme des maschinellen Lernens, mit Smells wie dem Plain-Old-Data-Type-Smell, dem Multiple-Language-Smell und dem Prototype-Smell als Hinweisen auf [[technical-debt|technische Schulden]].

### Funktionsweise

```text
Code lesen → Smell bemerken (schnell, „riechbar“)
  ├─ genauer hinsehen: gibt es ein tieferes Problem?
  │     nein → so lassen (manche langen Methoden sind in Ordnung)
  │     ja   → in kleinen, verhaltenserhaltenden Schritten refaktorieren
  └─ Beispiele: lange Methode · Datenklasse ohne Verhalten
     ML-Systeme: einfache Datentypen · mehrere Sprachen · Prototyp im Produktivbetrieb
```

#### 1. Ein oberflächliches Anzeichen

Die Definition hat zwei Teile: Ein Smell ist per Definition schnell zu erkennen, und er weist nicht immer auf ein Problem hin (Fowler, 2006). Fowlers Beispiel ist eine lange Methode: „my nose twitches if I see more than a dozen lines of java“, und doch gilt: „some long methods are just fine“ (Fowler, 2006).

#### 2. Der Weg zu tieferen Problemen

Die besten Smells sind leicht zu erkennen und führen meist zu interessanten Problemen. Datenklassen, mit allen Daten und ohne Verhalten, werfen die Frage auf, welches Verhalten in die Klasse gehört, und Refactoring verschiebt es dann dorthin (Fowler, 2006). Das Buch *Refactoring* hat einführende Kapitel zu den Code Smells, die ein Refactoring nahelegen, gefolgt von einem Katalog mit rund siebzig Refactorings (Fowler, 2018).

#### 3. Smells in ML-Systemen

Sculley et al. (2015) beschreiben Smells von ML-Systemen als „not hard-and-fast rules, but as subjective indicators“: den Plain-Old-Data-Type-Smell, bei dem Modellparameter und Vorhersagen einfache Gleitkomma- und Ganzzahlen sind, die nicht wissen, was sie bedeuten oder welches Modell sie erzeugt hat; den Multiple-Language-Smell, der die Kosten für Tests erhöht und die Übergabe der Verantwortung erschwert; und den Prototype-Smell, bei dem die Abhängigkeit von einer Prototyp-Umgebung auf ein brüchiges Gesamtsystem hinweist und die Gefahr birgt, dass ein Prototyp produktiv genutzt wird. Gängige Abläufe mit vielen manuellen Schritten sind ein weiterer Smell auf Systemebene (Sculley et al., 2015).

#### Herkunft und Varianten

Beck prägte den Begriff bei der Arbeit mit Fowler an *Refactoring*, erstmals 1999 erschienen (Fowler, 2006; Fowler, 2018). Sculley et al. (2015) sprechen von „design smells“ und ergänzen ML-spezifische.

### Wann einsetzen

- In Code Reviews, um ein Muster zu benennen, das genauer betrachtet werden sollte, ohne es als Fehler zu bezeichnen ([[clean-code|Clean Code]]).
- Bei der Entscheidung, was refaktoriert werden soll, als Hinweis auf das zugrunde liegende Problem (Fowler, 2006).
- Zur Prüfung von ML-Systemen auf Systemebene mit den Smells von Sculley et al. (2015).

### Stärken und Grenzen

**Stärken**
- Leicht zu lernen: Auch Unerfahrene erkennen Smells, bevor sie das zugrunde liegende Problem beurteilen oder beheben können (Fowler, 2006).
- Gibt Teams ein gemeinsames Vokabular; Fowler erwähnt Leads, die einen „smell of the week“ wählen, um ihr Team zu schulen (Fowler, 2006).

**Grenzen**
- Subjektiv: Ein Smell ist ein Hinweis, keine Regel, und muss geprüft werden (Fowler, 2006; Sculley et al., 2015).
- Smells zu benennen behebt noch nichts; dafür braucht es Urteilsvermögen und Refactoring (Fowler, 2006).

### Vergleich

| | Code Smell | Fehler (Bug) | Technische Schulden |
|---|---|---|---|
| Was es ist | oberflächlicher Hinweis auf ein mögliches Designproblem | falsches Verhalten | angesammelte Kosten schlechter innerer Qualität |
| Für Nutzende sichtbar? | nein | ja | indirekt, durch langsamere Änderungen |
| Typische Reaktion | genauer hinsehen, refaktorieren | beheben | abbauen, etwa durch Refactoring |

Quellen: Fowler (2006); [[technical-debt|technische Schulden]].

### In der Praxis

Erzeugen KI-Programmierassistenten Code, sind Smells wie immer weiter wachsende Funktionen eine schnelle Prüfung, bevor eine Änderung übernommen wird; Kent Beck merkt an, dass heutige Assistenten „lack taste“ und einer riesigen Funktion weitere 20 Zeilen hinzufügen ([[kent-beck|Kent Beck]]). In [[ml-pipelines|ML-Pipelines]] helfen typisierte Objekte für Modellausgaben und weniger Sprachen gegen den Plain-Old-Data- und den Multiple-Language-Smell (Sculley et al., 2015).

### Merksatz

Ein Code Smell ist ein schnell erkennbarer Hinweis, dass tiefer etwas nicht stimmen könnte; er verlangt genaueres Hinsehen und oft ein Refactoring, kein automatisches Urteil.

### Quellen

- Fowler, M. (2006). *Code Smell*. [martinfowler.com](https://martinfowler.com/bliki/CodeSmell.html)
- Fowler, M. mit Beck, K. (2018). *Refactoring: Improving the Design of Existing Code*, 2. Aufl. [martinfowler.com](https://martinfowler.com/books/refactoring.html)
- Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F. & Dennison, D. (2015). *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. [NeurIPS proceedings](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)
