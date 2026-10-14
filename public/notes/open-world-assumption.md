---
title_en: Open-World Assumption
title_de: Open-World-Annahme
entity_type: Concept
aliases:
- Open-world assumption
- Open world assumption
- OWA
- Closed-world assumption
sources:
- https://www.w3.org/TR/owl2-primer/
- https://www.w3.org/TR/shacl/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Under the open-world assumption, a fact that is not stated is unknown, not false: it may simply be missing but still be true. Under the closed-world assumption, which databases usually follow, a fact that is not present is considered false (W3C OWL Working Group, 2012). OWL ontologies and the semantic web stack work under the open-world assumption, which suits data published by many independent parties, but it surprises people with a database background: OWL does not flag missing information, infers new facts from domain and range declarations instead of rejecting data, and does not assume that different names denote different individuals ([[ontology-design|ontology design]]). Validation of what must be present is therefore done with a separate closed-world tool such as SHACL (W3C, 2017).

### How it works

```text
data:  :John :hasChild :Mary .        question: does John have a child named Bill?
                                       closed world (SQL):  no row → false
                                       open world (OWL):    not stated → unknown

schema: :hasWife rdfs:domain :Man .   data: :Sasha :hasWife :Hillary .
                                       closed world: Sasha is not typed Man → constraint violation
                                       open world:   reasoner infers  :Sasha a :Man
```

#### 1. Missing is not false

The OWL 2 Primer contrasts OWL with databases: if a fact is not present in a database, it is usually considered false, the closed-world assumption, whereas in an OWL document it may simply be missing but possibly true, following the open-world assumption (W3C OWL Working Group, 2012). The default stance in OWL is that anything is possible until stated otherwise; to say that something is not true, it has to be asserted explicitly, for example with a negative property assertion such as "Mary is not Bill's wife" (W3C OWL Working Group, 2012).

#### 2. Axioms infer instead of constrain

OWL is not a schema language for syntax conformance: there is no way to enforce that a piece of information, such as a social security number, is present (W3C OWL Working Group, 2012). Declaring that the property hasWife has domain Man and range Woman does not reject data that lacks these types; given that Sasha hasWife Hillary, a reasoner infers that Sasha is a man and Hillary a woman. Similarly, stating that John has at most four children who are parents still allows arbitrarily many further children who are not parents (W3C OWL Working Group, 2012).

#### 3. No unique name assumption

OWL does not assume that different names refer to different individuals: unless stated otherwise, John and Bill might be the same person, and distinctness has to be declared explicitly, for example with owl:differentFrom (W3C OWL Working Group, 2012). The primer explains that this suits the semantic web, where names are coined by different organisations at different times that may unknowingly refer to the same individual ([[rdf|RDF]], [[knowledge-graphs|knowledge graphs]]).

#### 4. Closed-world validation with SHACL

SHACL, the Shapes Constraint Language, validates RDF data graphs against conditions expressed as shapes in a shapes graph (W3C, 2017). Its definitions are complete within the specification: if no rule makes a situation true, it is false, which gives the closed-world behaviour that validation needs, such as reporting a node that lacks a required property. Shapes can also serve as a description of valid data for user interfaces, code generation and data integration (W3C, 2017).

#### Origin and variants

The assumption matters wherever logic-based knowledge representation meets data management. OWL 2 is a computational logic-based language whose ontologies can be published on the web and refer to each other, so no single source can claim to know everything (W3C OWL Working Group, 2012). Databases and many application data models work under the closed-world assumption, and the primer notes that databases are still a viable backbone in many ontology-based systems. In practice, systems combine both: OWL reasoning for inference, SHACL or queries for completeness checks ([[sparql|SPARQL]], [[ontology-design|ontology design]]).

### When to use it

- Integrating data from many independent sources, where any single source is incomplete (W3C OWL Working Group, 2012; [[knowledge-graph-engineering|knowledge graph engineering]]).
- Reasoning that should derive implicit facts rather than reject incomplete data (W3C OWL Working Group, 2012).
- Use a closed-world approach instead, such as SHACL or database constraints, when data must be complete and valid for an application (W3C, 2017).

### Strengths and limitations

**Strengths**
- Matches a web of partial, independently published knowledge (W3C OWL Working Group, 2012).
- Lets reasoners derive new facts from domain, range and class axioms (W3C OWL Working Group, 2012).
- Avoids false conclusions from the mere absence of data.

**Limitations**
- Counter-intuitive for database users: axioms that look like constraints act as inference rules (W3C OWL Working Group, 2012).
- Negative knowledge and distinct individuals must be stated explicitly (W3C OWL Working Group, 2012).
- Cannot check completeness; a separate closed-world validation layer is needed (W3C, 2017).

### Comparison

| | Open-world assumption | Closed-world assumption |
|---|---|---|
| Fact not stated | unknown | false |
| Typical systems | OWL ontologies, semantic web | relational databases, SHACL validation |
| Domain/range or cardinality | used to infer facts | used to reject invalid data |
| Different names | may be the same individual | usually distinct records |

Sources: W3C OWL Working Group (2012); W3C (2017).

### In practice

Decide per use case which assumption a query or check needs: "no result" from an open-world knowledge graph means "not known", not "does not exist". Model negative facts and distinct individuals explicitly where they matter. Keep OWL axioms for inference and put required fields, cardinalities and value checks into SHACL shapes run in the data pipeline ([[ontology-design|ontology design]]). Link prediction starts from the same observation that knowledge graphs are incomplete and predicts missing edges, although training usually treats corrupted edges that are not in the graph as negative examples ([[knowledge-graph-embeddings|knowledge graph embeddings]]).

### Key takeaway

Under the open-world assumption, what is not stated is unknown rather than false; OWL reasons this way, which suits the open web but makes its axioms infer rather than validate, so closed-world checks belong in a separate layer such as SHACL.

### Sources

- W3C OWL Working Group (2012). *OWL 2 Web Ontology Language Primer (Second Edition)*. W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- W3C (2017). *Shapes Constraint Language (SHACL)*. W3C Recommendation. [w3.org](https://www.w3.org/TR/shacl/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Unter der Open-World-Annahme ist eine nicht genannte Tatsache unbekannt, nicht falsch: Sie kann einfach fehlen und dennoch wahr sein. Unter der Closed-World-Annahme, der Datenbanken meist folgen, gilt eine nicht vorhandene Tatsache als falsch (W3C OWL Working Group, 2012). OWL-Ontologien und der Semantic-Web-Stack arbeiten unter der Open-World-Annahme, was zu Daten passt, die von vielen unabhängigen Stellen veröffentlicht werden, aber Menschen mit Datenbankhintergrund überrascht: OWL meldet fehlende Information nicht, leitet aus Domain- und Range-Angaben neue Fakten ab, statt Daten abzulehnen, und nimmt nicht an, dass verschiedene Namen verschiedene Individuen bezeichnen ([[ontology-design|Ontologie-Design]]). Was vorhanden sein muss, wird daher mit einem eigenen Closed-World-Werkzeug wie SHACL geprüft (W3C, 2017).

### Funktionsweise

```text
Daten:  :John :hasChild :Mary .       Frage: Hat John ein Kind namens Bill?
                                       Closed World (SQL): keine Zeile → falsch
                                       Open World (OWL):   nicht genannt → unbekannt

Schema: :hasWife rdfs:domain :Man .   Daten: :Sasha :hasWife :Hillary .
                                       Closed World: Sasha ist nicht als Man typisiert → Regelverstoß
                                       Open World:   Reasoner folgert  :Sasha a :Man
```

#### 1. Fehlend heißt nicht falsch

Das OWL 2 Primer stellt OWL Datenbanken gegenüber: Fehlt eine Tatsache in einer Datenbank, gilt sie meist als falsch, die Closed-World-Annahme, während sie in einem OWL-Dokument einfach fehlen kann, aber möglicherweise wahr ist, gemäß der Open-World-Annahme (W3C OWL Working Group, 2012). Die Grundhaltung in OWL ist, dass alles möglich ist, bis etwas anderes gesagt wird; um auszudrücken, dass etwas nicht zutrifft, muss es ausdrücklich behauptet werden, etwa mit einer negativen Eigenschaftsaussage wie „Mary ist nicht Bills Ehefrau“ (W3C OWL Working Group, 2012).

#### 2. Axiome folgern statt einzuschränken

OWL ist keine Schemasprache für syntaktische Konformität: Es gibt keine Möglichkeit zu erzwingen, dass eine Information, etwa eine Sozialversicherungsnummer, vorhanden ist (W3C OWL Working Group, 2012). Die Angabe, dass die Eigenschaft hasWife die Domain Man und die Range Woman hat, weist Daten ohne diese Typen nicht zurück; aus „Sasha hasWife Hillary“ folgert ein Reasoner, dass Sasha ein Mann und Hillary eine Frau ist. Ebenso erlaubt die Aussage, dass John höchstens vier Kinder hat, die selbst Eltern sind, beliebig viele weitere Kinder, die keine Eltern sind (W3C OWL Working Group, 2012).

#### 3. Keine Unique Name Assumption

OWL nimmt nicht an, dass verschiedene Namen verschiedene Individuen bezeichnen: Sofern nichts anderes gesagt ist, könnten John und Bill dieselbe Person sein, und Verschiedenheit muss ausdrücklich erklärt werden, etwa mit owl:differentFrom (W3C OWL Working Group, 2012). Das Primer erklärt, dass dies zum Semantic Web passt, wo Namen von verschiedenen Organisationen zu verschiedenen Zeiten vergeben werden und unwissentlich dasselbe Individuum bezeichnen können ([[rdf|RDF]], [[knowledge-graphs|Knowledge Graphs]]).

#### 4. Closed-World-Validierung mit SHACL

SHACL, die Shapes Constraint Language, validiert RDF-Datengraphen gegen Bedingungen, die als Shapes in einem Shapes-Graphen formuliert sind (W3C, 2017). Ihre Definitionen sind innerhalb der Spezifikation vollständig: Macht keine Regel eine Situation wahr, ist sie falsch, was das Closed-World-Verhalten liefert, das Validierung braucht, etwa die Meldung eines Knotens ohne erforderliche Eigenschaft. Shapes können zudem als Beschreibung gültiger Daten für Benutzeroberflächen, Codegenerierung und Datenintegration dienen (W3C, 2017).

#### Herkunft und Varianten

Die Annahme ist überall wichtig, wo logikbasierte Wissensrepräsentation auf Datenverwaltung trifft. OWL 2 ist eine auf rechnergestützter Logik beruhende Sprache, deren Ontologien im Web veröffentlicht werden und aufeinander verweisen können, sodass keine einzelne Quelle beanspruchen kann, alles zu wissen (W3C OWL Working Group, 2012). Datenbanken und viele Anwendungsdatenmodelle arbeiten unter der Closed-World-Annahme, und das Primer merkt an, dass Datenbanken dennoch in vielen ontologiebasierten Systemen ein tragfähiges Rückgrat sind. In der Praxis kombinieren Systeme beides: OWL-Reasoning für Schlussfolgerungen, SHACL oder Abfragen für Vollständigkeitsprüfungen ([[sparql|SPARQL]], [[ontology-design|Ontologie-Design]]).

### Wann einsetzen

- Integration von Daten aus vielen unabhängigen Quellen, von denen jede unvollständig ist (W3C OWL Working Group, 2012; [[knowledge-graph-engineering|Knowledge Graph Engineering]]).
- Schlussfolgern, das implizite Fakten ableiten statt unvollständige Daten abweisen soll (W3C OWL Working Group, 2012).
- Stattdessen ein Closed-World-Ansatz wie SHACL oder Datenbank-Constraints, wenn Daten für eine Anwendung vollständig und gültig sein müssen (W3C, 2017).

### Stärken und Grenzen

**Stärken**
- Passt zu einem Web aus unvollständigem, unabhängig veröffentlichtem Wissen (W3C OWL Working Group, 2012).
- Lässt Reasoner aus Domain-, Range- und Klassenaxiomen neue Fakten ableiten (W3C OWL Working Group, 2012).
- Vermeidet falsche Schlüsse aus dem bloßen Fehlen von Daten.

**Grenzen**
- Für Datenbanknutzende kontraintuitiv: Axiome, die wie Einschränkungen aussehen, wirken als Schlussregeln (W3C OWL Working Group, 2012).
- Negatives Wissen und verschiedene Individuen müssen ausdrücklich angegeben werden (W3C OWL Working Group, 2012).
- Kann Vollständigkeit nicht prüfen; dafür ist eine eigene Closed-World-Validierungsschicht nötig (W3C, 2017).

### Vergleich

| | Open-World-Annahme | Closed-World-Annahme |
|---|---|---|
| Nicht genannte Tatsache | unbekannt | falsch |
| Typische Systeme | OWL-Ontologien, Semantic Web | relationale Datenbanken, SHACL-Validierung |
| Domain/Range oder Kardinalität | dienen der Ableitung von Fakten | dienen dem Abweisen ungültiger Daten |
| Verschiedene Namen | können dasselbe Individuum sein | meist verschiedene Datensätze |

Quellen: W3C OWL Working Group (2012); W3C (2017).

### In der Praxis

Je Anwendungsfall ist zu entscheiden, welche Annahme eine Abfrage oder Prüfung braucht: „Kein Ergebnis“ aus einem Open-World-Knowledge-Graph bedeutet „nicht bekannt“, nicht „existiert nicht“. Negative Fakten und verschiedene Individuen werden ausdrücklich modelliert, wo es darauf ankommt. OWL-Axiome bleiben dem Schlussfolgern vorbehalten, Pflichtfelder, Kardinalitäten und Wertprüfungen gehören in SHACL-Shapes, die in der Datenpipeline laufen ([[ontology-design|Ontologie-Design]]). Link Prediction geht von derselben Beobachtung aus, dass Knowledge Graphs unvollständig sind, und sagt fehlende Kanten vorher, auch wenn das Training veränderte Kanten, die nicht im Graphen stehen, meist als Negativbeispiele behandelt ([[knowledge-graph-embeddings|Knowledge Graph Embeddings]]).

### Merksatz

Unter der Open-World-Annahme ist, was nicht gesagt wird, unbekannt statt falsch; OWL schließt auf diese Weise, was zum offenen Web passt, aber seine Axiome folgern lässt statt zu validieren, daher gehören Closed-World-Prüfungen in eine eigene Schicht wie SHACL.

### Quellen

- W3C OWL Working Group (2012). *OWL 2 Web Ontology Language Primer (Second Edition)*. W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- W3C (2017). *Shapes Constraint Language (SHACL)*. W3C Recommendation. [w3.org](https://www.w3.org/TR/shacl/)
