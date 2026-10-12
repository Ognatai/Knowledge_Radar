---
title_en: Cypher
title_de: Cypher
entity_type: Technology
aliases:
- openCypher
sources:
- https://doi.org/10.1145/3183713.3190657
- https://neo4j.com/docs/cypher-manual/current/clauses/
- https://neo4j.com/docs/cypher-manual/current/queries/basic/
- https://neo4j.com/docs/cypher-manual/current/clauses/merge/
- https://neo4j.com/docs/cypher-manual/current/introduction/
- https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Cypher is a declarative query language for property graphs: a query describes the subgraph it is looking for as an ASCII-art pattern such as (a:Person)-[:KNOWS]->(b:Person), and clauses such as MATCH, WHERE, RETURN, CREATE and MERGE read and change the graph (Francis et al., 2018; Neo4j Cypher Manual: Clauses). It was designed for [[neo4j|Neo4j]], is governed by the openCypher project, and the ISO standard [[gql|GQL]] adopted much of its query construction (Francis et al., 2018; Neo4j Cypher Manual: GQL conformance).

### Core concepts

- **Patterns:** Nodes are written in round brackets with an optional variable, labels and properties, (p:Person {name: 'Tom Hanks'}); relationships in square brackets with a type and direction, -[:ACTED_IN]->. A pattern describes a subgraph, and MATCH finds all its occurrences (Francis et al., 2018; Neo4j Cypher Manual: Basic queries).
- **Reading clauses:** MATCH specifies the patterns to search for; OPTIONAL MATCH does the same but uses null for missing parts of the pattern (Neo4j Cypher Manual: Clauses).
- **Filtering and projection:** WHERE adds constraints to a MATCH or filters the results of a WITH; RETURN defines the result; WITH chains query parts and pipes results from one part to the next; UNWIND expands a list into rows (Neo4j Cypher Manual: Clauses).
- **Sorting and paging:** ORDER BY sorts ascending by default or DESC, SKIP sets where output starts, LIMIT caps the number of rows; DISTINCT removes duplicate rows (Neo4j Cypher Manual: Clauses; Neo4j Cypher Manual: Basic queries).
- **Aggregation:** Functions such as count() aggregate rows, for example to count how often a person appears in the matched patterns (Neo4j Cypher Manual: Basic queries).
- **Paths:** Quantifiers match paths of fixed or variable length, for example --{2} for exactly two hops or --{1,4} for one to four; ALL SHORTEST returns all shortest paths between two nodes (Neo4j Cypher Manual: Basic queries).
- **Writing clauses:** CREATE creates nodes and relationships; SET updates labels and properties; REMOVE removes them; DELETE deletes nodes, relationships or paths, where nodes must first lose their relationships, and DETACH DELETE removes a node together with its relationships (Neo4j Cypher Manual: Clauses).
- **MERGE:** MERGE ensures that a pattern exists: if the exact pattern is found, it acts like MATCH, otherwise it creates the pattern; ON CREATE and ON MATCH run different updates for the two cases (Neo4j Cypher Manual: MERGE).
- **Procedures and subqueries:** CALL … YIELD invokes a procedure deployed in the database; CALL { … } evaluates a subquery, and CALL { … } IN TRANSACTIONS splits large imports, such as with LOAD CSV, into separate transactions (Neo4j Cypher Manual: Clauses).
- **Versions:** The Neo4j manual covers Cypher 25; since Neo4j 2025.06, new features are added only to Cypher 25, while Cypher 5 is frozen (Neo4j Cypher Manual: Introduction).

### Common usage

```cypher
// who directed The Matrix (incoming relationship)
MATCH (m:Movie {title: 'The Matrix'})<-[:DIRECTED]-(p:Person)
RETURN p.name AS director

// filter, sort, page
MATCH (p:Person)
WHERE p.born >= 1980 AND p.born < 1990
RETURN p.name AS name, p.born AS born
ORDER BY born DESC
LIMIT 5

// recommendation: co-co-actors Keanu Reeves has not worked with
MATCH (keanu:Person {name:'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActors:Person),
      (coActors)-[:ACTED_IN]->(m2:Movie)<-[:ACTED_IN]-(cocoActors:Person)
WHERE NOT (keanu)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND keanu <> cocoActors
RETURN cocoActors.name AS recommended, count(cocoActors) AS strength
ORDER BY strength DESC
LIMIT 7

// create or update
MERGE (keanu:Person {name: 'Keanu Reeves'})
ON CREATE SET keanu.created = timestamp()
ON MATCH SET keanu.lastSeen = timestamp()
```

The examples come from the Neo4j movie dataset (Neo4j Cypher Manual: Basic queries; Neo4j Cypher Manual: MERGE).

### When to use it

- For queries over property [[graph-databases|graph databases]] such as [[neo4j|Neo4j]], especially when a question follows relationships over several steps (Francis et al., 2018).
- For loading and updating graphs idempotently with MERGE and constraints (Neo4j Cypher Manual: MERGE).
- For [[rdf|RDF]] data, [[sparql|SPARQL]] is the standard language; for tables, [[sql|SQL]].

### Strengths and limitations

**Strengths**
- Patterns read like a drawing of the subgraph, which makes multi-step queries short (Francis et al., 2018).
- Declarative: the query states what to find, the database plans how (Neo4j Cypher Manual: Introduction).
- Close to the ISO standard GQL, so queries carry over with minimal differences (Neo4j Cypher Manual: GQL conformance).

**Limitations**
- MERGE checks the whole pattern including relationships; if one part is missing, it creates the complete pattern, so merging a full pattern can create duplicate nodes (Neo4j Cypher Manual: MERGE).
- MERGE cannot use properties whose value is null (Neo4j Cypher Manual: MERGE).
- DETACH DELETE is not suited to deleting large amounts of data and leaves indexes and the schema in place (Neo4j Cypher Manual: Basic queries).

### Comparison

| Language | Data model | Notes |
|----------|------------|-------|
| Cypher | Property graph, ASCII-art patterns (Francis et al., 2018) | Neo4j and openCypher implementations |
| [[gql\|GQL]] | Property graph, ISO standard (Neo4j Cypher Manual: GQL conformance) | Adopted much of Cypher's query construction |
| [[sparql\|SPARQL]] | RDF triples | W3C standard for linked data |
| [[sql\|SQL]] | Tables | Joins instead of patterns |

### In practice

To avoid duplicates, constraints are created first and MERGE is applied to single nodes, then to the relationship between them, instead of merging a long pattern at once (Neo4j Cypher Manual: MERGE). Constraints also add index-backed performance and protect against duplicate creation under concurrent loads (Neo4j Cypher Manual: MERGE). Longer queries are built from parts chained with WITH, which pipes the results of one part into the next (Neo4j Cypher Manual: Clauses).

### Key takeaway

Cypher describes the subgraph it looks for as an ASCII-art pattern and reads and writes property graphs with clauses such as MATCH, MERGE and RETURN; GQL standardises much of it.

### Sources

- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
- Neo4j. *Clauses.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/)
- Neo4j. *Basic queries.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/queries/basic/)
- Neo4j. *MERGE.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- Neo4j. *Introduction.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Neo4j. *GQL conformance.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Cypher ist eine deklarative Abfragesprache für Property Graphs: Eine Abfrage beschreibt den gesuchten Teilgraphen als ASCII-Art-Muster wie (a:Person)-[:KNOWS]->(b:Person), und Klauseln wie MATCH, WHERE, RETURN, CREATE und MERGE lesen und ändern den Graphen (Francis et al., 2018; Neo4j Cypher Manual: Clauses). Sie wurde für [[neo4j|Neo4j]] entworfen, wird vom openCypher-Projekt gepflegt, und der ISO-Standard [[gql|GQL]] hat viel von ihrem Abfrageaufbau übernommen (Francis et al., 2018; Neo4j Cypher Manual: GQL conformance).

### Kernkonzepte

- **Muster:** Knoten stehen in runden Klammern mit optionaler Variable, Labels und Eigenschaften, (p:Person {name: 'Tom Hanks'}); Beziehungen in eckigen Klammern mit Typ und Richtung, -[:ACTED_IN]->. Ein Muster beschreibt einen Teilgraphen, und MATCH findet alle seine Vorkommen (Francis et al., 2018; Neo4j Cypher Manual: Basic queries).
- **Leseklauseln:** MATCH gibt die gesuchten Muster an; OPTIONAL MATCH tut dasselbe, setzt für fehlende Teile des Musters aber null ein (Neo4j Cypher Manual: Clauses).
- **Filtern und Projizieren:** WHERE schränkt ein MATCH ein oder filtert die Ergebnisse eines WITH; RETURN legt das Ergebnis fest; WITH verkettet Abfrageteile und reicht Ergebnisse von einem Teil an den nächsten weiter; UNWIND macht aus einer Liste Zeilen (Neo4j Cypher Manual: Clauses).
- **Sortieren und Blättern:** ORDER BY sortiert standardmäßig aufsteigend oder mit DESC absteigend, SKIP legt fest, ab welcher Zeile ausgegeben wird, LIMIT begrenzt die Zahl der Zeilen; DISTINCT entfernt doppelte Zeilen (Neo4j Cypher Manual: Clauses; Neo4j Cypher Manual: Basic queries).
- **Aggregation:** Funktionen wie count() fassen Zeilen zusammen, etwa um zu zählen, wie oft eine Person in den gefundenen Mustern vorkommt (Neo4j Cypher Manual: Basic queries).
- **Pfade:** Quantoren finden Pfade fester oder variabler Länge, etwa --{2} für genau zwei Schritte oder --{1,4} für einen bis vier; ALL SHORTEST liefert alle kürzesten Pfade zwischen zwei Knoten (Neo4j Cypher Manual: Basic queries).
- **Schreibklauseln:** CREATE legt Knoten und Beziehungen an; SET ändert Labels und Eigenschaften; REMOVE entfernt sie; DELETE löscht Knoten, Beziehungen oder Pfade, wobei Knoten zuerst ihre Beziehungen verlieren müssen, und DETACH DELETE entfernt einen Knoten samt seinen Beziehungen (Neo4j Cypher Manual: Clauses).
- **MERGE:** MERGE stellt sicher, dass ein Muster existiert: Wird das exakte Muster gefunden, wirkt es wie MATCH, sonst legt es das Muster an; ON CREATE und ON MATCH führen für beide Fälle unterschiedliche Änderungen aus (Neo4j Cypher Manual: MERGE).
- **Prozeduren und Subqueries:** CALL … YIELD ruft eine in der Datenbank installierte Prozedur auf; CALL { … } wertet eine Subquery aus, und CALL { … } IN TRANSACTIONS teilt große Importe, etwa mit LOAD CSV, in einzelne Transaktionen auf (Neo4j Cypher Manual: Clauses).
- **Versionen:** Das Neo4j-Handbuch beschreibt Cypher 25; seit Neo4j 2025.06 kommen neue Funktionen nur noch in Cypher 25 hinzu, Cypher 5 ist eingefroren (Neo4j Cypher Manual: Introduction).

### Typische Verwendung

```cypher
// wer hat The Matrix inszeniert (eingehende Beziehung)
MATCH (m:Movie {title: 'The Matrix'})<-[:DIRECTED]-(p:Person)
RETURN p.name AS director

// filtern, sortieren, blättern
MATCH (p:Person)
WHERE p.born >= 1980 AND p.born < 1990
RETURN p.name AS name, p.born AS born
ORDER BY born DESC
LIMIT 5

// Empfehlung: Co-Co-Schauspieler, mit denen Keanu Reeves noch nicht gespielt hat
MATCH (keanu:Person {name:'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActors:Person),
      (coActors)-[:ACTED_IN]->(m2:Movie)<-[:ACTED_IN]-(cocoActors:Person)
WHERE NOT (keanu)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND keanu <> cocoActors
RETURN cocoActors.name AS recommended, count(cocoActors) AS strength
ORDER BY strength DESC
LIMIT 7

// anlegen oder aktualisieren
MERGE (keanu:Person {name: 'Keanu Reeves'})
ON CREATE SET keanu.created = timestamp()
ON MATCH SET keanu.lastSeen = timestamp()
```

Die Beispiele stammen aus dem Film-Datensatz von Neo4j (Neo4j Cypher Manual: Basic queries; Neo4j Cypher Manual: MERGE).

### Wann einsetzen

- Für Abfragen auf Property-[[graph-databases|Graphdatenbanken]] wie [[neo4j|Neo4j]], besonders wenn eine Frage Beziehungen über mehrere Schritte folgt (Francis et al., 2018).
- Zum idempotenten Laden und Aktualisieren von Graphen mit MERGE und Constraints (Neo4j Cypher Manual: MERGE).
- Für RDF-Daten ist [[sparql|SPARQL]] die Standardsprache, für Tabellen [[sql|SQL]].

### Stärken und Grenzen

**Stärken**
- Muster lesen sich wie eine Zeichnung des Teilgraphen, was Abfragen über mehrere Schritte kurz macht (Francis et al., 2018).
- Deklarativ: Die Abfrage sagt, was gesucht wird, die Datenbank plant, wie (Neo4j Cypher Manual: Introduction).
- Nah am ISO-Standard GQL, sodass sich Abfragen mit minimalen Unterschieden übertragen lassen (Neo4j Cypher Manual: GQL conformance).

**Grenzen**
- MERGE prüft das ganze Muster einschließlich der Beziehungen; fehlt ein Teil, legt es das komplette Muster an, sodass das Mergen eines vollen Musters doppelte Knoten erzeugen kann (Neo4j Cypher Manual: MERGE).
- MERGE kann keine Eigenschaften mit dem Wert null verwenden (Neo4j Cypher Manual: MERGE).
- DETACH DELETE eignet sich nicht zum Löschen großer Datenmengen und lässt Indizes und Schema bestehen (Neo4j Cypher Manual: Basic queries).

### Vergleich

| Sprache | Datenmodell | Anmerkung |
|---------|-------------|-----------|
| Cypher | Property Graph, ASCII-Art-Muster (Francis et al., 2018) | Neo4j und openCypher-Implementierungen |
| [[gql\|GQL]] | Property Graph, ISO-Standard (Neo4j Cypher Manual: GQL conformance) | Hat viel vom Abfrageaufbau von Cypher übernommen |
| [[sparql\|SPARQL]] | RDF-Tripel | W3C-Standard für Linked Data |
| [[sql\|SQL]] | Tabellen | Joins statt Muster |

### In der Praxis

Um Duplikate zu vermeiden, werden zuerst Constraints angelegt und MERGE auf einzelne Knoten und danach auf die Beziehung zwischen ihnen angewendet, statt ein langes Muster auf einmal zu mergen (Neo4j Cypher Manual: MERGE). Constraints bringen außerdem indexgestützte Performance und schützen vor doppeltem Anlegen bei parallelen Ladevorgängen (Neo4j Cypher Manual: MERGE). Längere Abfragen entstehen aus Teilen, die mit WITH verkettet werden; WITH reicht die Ergebnisse eines Teils an den nächsten weiter (Neo4j Cypher Manual: Clauses).

### Merksatz

Cypher beschreibt den gesuchten Teilgraphen als ASCII-Art-Muster und liest und schreibt Property Graphs mit Klauseln wie MATCH, MERGE und RETURN; GQL standardisiert vieles davon.

### Quellen

- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
- Neo4j. *Clauses.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/)
- Neo4j. *Basic queries.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/queries/basic/)
- Neo4j. *MERGE.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- Neo4j. *Introduction.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Neo4j. *GQL conformance.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/)
