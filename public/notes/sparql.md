---
title_en: SPARQL
title_de: SPARQL
entity_type: Technology
sources:
- https://www.w3.org/TR/sparql11-query/
- https://doi.org/10.1145/1567274.1567278
- https://www.w3.org/TR/rdf11-concepts/
- https://neo4j.com/docs/cypher-manual/current/introduction/
- https://www.postgresql.org/docs/current/tutorial-sql-intro.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

SPARQL is the W3C query language for RDF knowledge graphs: a query describes triple patterns with variables, and the engine returns all ways in which they match the graph (W3C SPARQL 1.1). Patterns are combined with FILTER, OPTIONAL and UNION, results are grouped, aggregated and sorted, property paths follow chains of relations, and besides SELECT there are CONSTRUCT, ASK and DESCRIBE. Its semantics and complexity are formally well studied (Pérez et al., 2009).

### Core concepts

- **Triple patterns:** RDF data consists of subject-predicate-object triples (W3C RDF 1.1 Concepts); a triple pattern may contain variables such as ?decision, and a group of patterns forms a basic graph pattern that must match together (W3C SPARQL 1.1).
- **Prefixes:** PREFIX declares abbreviations for namespaces, so that IRIs are written as ex:cites (W3C SPARQL 1.1).
- **FILTER, OPTIONAL, UNION:** FILTER restricts solutions by conditions, OPTIONAL adds data if present without discarding solutions, and UNION combines alternative patterns (W3C SPARQL 1.1).
- **Solution modifiers and aggregation:** DISTINCT, ORDER BY, LIMIT and OFFSET shape results; GROUP BY with COUNT, SUM or AVG and HAVING aggregate them (W3C SPARQL 1.1).
- **BIND and VALUES:** BIND assigns computed values to variables, VALUES supplies inline data (W3C SPARQL 1.1).
- **Property paths:** ex:amends+ or ex:partOf* match paths of one or more or zero or more steps (W3C SPARQL 1.1).
- **Negation:** MINUS removes solutions compatible with another pattern; FILTER NOT EXISTS tests that a pattern does not match (W3C SPARQL 1.1).
- **Query forms:** SELECT returns variable bindings, CONSTRUCT a new RDF graph, ASK true or false, DESCRIBE an RDF description of resources (W3C SPARQL 1.1).

### Common usage

```sparql
PREFIX ex: <http://example.org/legal#>

# decisions citing a norm, with optional date, newest first
SELECT ?decision ?date
WHERE {
  ?decision a ex:Decision ;
            ex:cites ex:GDPR_Art6 .
  OPTIONAL { ?decision ex:date ?date }
}
ORDER BY DESC(?date)
LIMIT 10

# number of citations per norm
SELECT ?norm (COUNT(?decision) AS ?n)
WHERE { ?decision ex:cites ?norm }
GROUP BY ?norm
HAVING (COUNT(?decision) > 5)

# all norms reachable through one or more amendments
SELECT ?older WHERE { ex:NormA ex:amends+ ?older }
```

The examples follow the legal knowledge graph modelled in [[knowledge-graphs|Knowledge Graphs]], with decisions, norms and citation relations.

### When to use it

- When data is stored as RDF, for example in linked open data or enterprise knowledge graphs (W3C SPARQL 1.1).
- When queries follow chains of relations of unknown length (W3C SPARQL 1.1).
- When data lives in tables with a fixed schema, SQL is the natural choice ([[sql|SQL]]).

### Strengths and limitations

**Strengths**
- Standardised by the W3C and supported by many triple stores (W3C SPARQL 1.1).
- Property paths express multi-step relations compactly (W3C SPARQL 1.1).
- Formal semantics allow systematic analysis and optimisation (Pérez et al., 2009).

**Limitations**
- Evaluating general SPARQL patterns is PSPACE-complete; patterns that are not well designed, particularly with nested OPTIONAL, can be expensive (Pérez et al., 2009).
- OPTIONAL and negation are easy to misuse, giving unexpected results (W3C SPARQL 1.1).
- Only applicable to RDF data; property graph databases use other languages such as Cypher (Neo4j Cypher Manual).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| SPARQL | Triple patterns over RDF graphs (W3C SPARQL 1.1) | Linked data, RDF knowledge graphs |
| SQL | Tables, joins, aggregates (PostgreSQL SQL tutorial) | Relational data with fixed schema |
| Cypher | ASCII-art patterns over property graphs (Neo4j Cypher Manual) | Property graph databases |

### In practice

Queries are developed incrementally, starting with a basic graph pattern and adding OPTIONAL, FILTER and aggregation step by step; well-designed patterns, in which OPTIONAL is used in a disciplined way, evaluate more efficiently (Pérez et al., 2009). Named graphs can record where data comes from, and queries can restrict themselves to particular graphs (W3C RDF 1.1 Concepts; [[rdf|RDF (Resource Description Framework)]]).

### Key takeaway

SPARQL queries RDF graphs by matching triple patterns with variables; FILTER, OPTIONAL, aggregates and property paths make it expressive, but complex patterns must be designed carefully.

### Sources

- W3C (2013). *SPARQL 1.1 Query Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/sparql11-query/)
- Pérez, J., Arenas, M. & Gutierrez, C. (2009). *Semantics and complexity of SPARQL.* ACM Transactions on Database Systems 34(3). [doi:10.1145/1567274.1567278](https://doi.org/10.1145/1567274.1567278)
- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, Chapter 2: The SQL Language.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-sql-intro.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

SPARQL ist die W3C-Abfragesprache für RDF-Wissensgraphen: Eine Abfrage beschreibt Tripelmuster mit Variablen, und die Engine liefert alle Möglichkeiten, wie diese auf den Graphen passen (W3C SPARQL 1.1). Muster werden mit FILTER, OPTIONAL und UNION verbunden, Ergebnisse gruppiert, aggregiert und sortiert, Property Paths folgen Ketten von Beziehungen, und neben SELECT gibt es CONSTRUCT, ASK und DESCRIBE. Semantik und Komplexität sind formal gut untersucht (Pérez et al., 2009).

### Kernkonzepte

- **Tripelmuster:** RDF-Daten bestehen aus Tripeln aus Subjekt, Prädikat und Objekt (W3C RDF 1.1 Concepts); ein Tripelmuster kann Variablen wie ?decision enthalten, und eine Gruppe von Mustern bildet ein Basic Graph Pattern, das gemeinsam passen muss (W3C SPARQL 1.1).
- **Präfixe:** PREFIX legt Abkürzungen für Namensräume fest, sodass IRIs als ex:cites geschrieben werden (W3C SPARQL 1.1).
- **FILTER, OPTIONAL, UNION:** FILTER schränkt Lösungen über Bedingungen ein, OPTIONAL ergänzt vorhandene Daten, ohne Lösungen zu verwerfen, und UNION verbindet alternative Muster (W3C SPARQL 1.1).
- **Lösungsmodifikatoren und Aggregation:** DISTINCT, ORDER BY, LIMIT und OFFSET formen das Ergebnis; GROUP BY mit COUNT, SUM oder AVG und HAVING aggregieren es (W3C SPARQL 1.1).
- **BIND und VALUES:** BIND weist Variablen berechnete Werte zu, VALUES liefert eingebettete Daten (W3C SPARQL 1.1).
- **Property Paths:** ex:amends+ oder ex:partOf* finden Pfade aus einem oder mehr beziehungsweise null oder mehr Schritten (W3C SPARQL 1.1).
- **Negation:** MINUS entfernt Lösungen, die zu einem anderen Muster passen; FILTER NOT EXISTS prüft, dass ein Muster nicht passt (W3C SPARQL 1.1).
- **Abfrageformen:** SELECT liefert Variablenbelegungen, CONSTRUCT einen neuen RDF-Graphen, ASK wahr oder falsch, DESCRIBE eine RDF-Beschreibung von Ressourcen (W3C SPARQL 1.1).

### Typische Verwendung

```sparql
PREFIX ex: <http://example.org/legal#>

# Entscheidungen, die eine Norm zitieren, mit optionalem Datum, neueste zuerst
SELECT ?decision ?date
WHERE {
  ?decision a ex:Decision ;
            ex:cites ex:GDPR_Art6 .
  OPTIONAL { ?decision ex:date ?date }
}
ORDER BY DESC(?date)
LIMIT 10

# Zahl der Zitierungen je Norm
SELECT ?norm (COUNT(?decision) AS ?n)
WHERE { ?decision ex:cites ?norm }
GROUP BY ?norm
HAVING (COUNT(?decision) > 5)

# alle Normen, die über eine oder mehrere Änderungen erreichbar sind
SELECT ?older WHERE { ex:NormA ex:amends+ ?older }
```

Die Beispiele folgen dem juristischen Wissensgraphen aus [[knowledge-graphs|Wissensgraphen]] mit Entscheidungen, Normen und Zitierbeziehungen.

### Wann einsetzen

- Wenn Daten als RDF vorliegen, etwa in Linked Open Data oder Unternehmenswissensgraphen (W3C SPARQL 1.1).
- Wenn Abfragen Ketten von Beziehungen unbekannter Länge folgen (W3C SPARQL 1.1).
- Wenn Daten in Tabellen mit festem Schema liegen, ist SQL die naheliegende Wahl ([[sql|SQL]]).

### Stärken und Grenzen

**Stärken**
- Vom W3C standardisiert und von vielen Triplestores unterstützt (W3C SPARQL 1.1).
- Property Paths drücken Beziehungen über mehrere Schritte kompakt aus (W3C SPARQL 1.1).
- Die formale Semantik erlaubt systematische Analyse und Optimierung (Pérez et al., 2009).

**Einschränkungen**
- Die Auswertung allgemeiner SPARQL-Muster ist PSPACE-vollständig; nicht wohlgeformte Muster, besonders mit verschachteltem OPTIONAL, können teuer sein (Pérez et al., 2009).
- OPTIONAL und Negation werden leicht falsch eingesetzt und liefern dann unerwartete Ergebnisse (W3C SPARQL 1.1).
- Nur auf RDF-Daten anwendbar; Property-Graph-Datenbanken nutzen andere Sprachen wie Cypher (Neo4j Cypher Manual).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| SPARQL | Tripelmuster über RDF-Graphen (W3C SPARQL 1.1) | Linked Data, RDF-Wissensgraphen |
| SQL | Tabellen, Joins, Aggregate (PostgreSQL SQL tutorial) | Relationale Daten mit festem Schema |
| Cypher | ASCII-Art-Muster über Property Graphs (Neo4j Cypher Manual) | Property-Graph-Datenbanken |

### In der Praxis

Abfragen werden schrittweise entwickelt: zuerst ein Basic Graph Pattern, dann nach und nach OPTIONAL, FILTER und Aggregation; wohlgeformte Muster, in denen OPTIONAL diszipliniert eingesetzt wird, lassen sich effizienter auswerten (Pérez et al., 2009). Named Graphs können festhalten, woher Daten stammen, und Abfragen können sich auf bestimmte Graphen beschränken (W3C RDF 1.1 Concepts; [[rdf|RDF (Resource Description Framework)]]).

### Merksatz

SPARQL fragt RDF-Graphen ab, indem es Tripelmuster mit Variablen abgleicht; FILTER, OPTIONAL, Aggregate und Property Paths machen es ausdrucksstark, komplexe Muster müssen aber sorgfältig entworfen werden.

### Quellen

- W3C (2013). *SPARQL 1.1 Query Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/sparql11-query/)
- Pérez, J., Arenas, M. & Gutierrez, C. (2009). *Semantics and complexity of SPARQL.* ACM Transactions on Database Systems 34(3). [doi:10.1145/1567274.1567278](https://doi.org/10.1145/1567274.1567278)
- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, Chapter 2: The SQL Language.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-sql-intro.html)
