---
title_en: Graph Databases
title_de: Graphdatenbanken
entity_type: Concept
sources:
- https://doi.org/10.1145/1322432.1322433
- https://doi.org/10.1145/3183713.3190657
- https://www.w3.org/TR/sparql11-query/
- https://neo4j.com/docs/cypher-manual/current/introduction/
- https://arxiv.org/abs/2003.02320
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Graph databases store data as nodes and edges and express queries as graph patterns and traversals, which suits data whose value lies in its connections (Angles & Gutierrez, 2008). The two main models are property graphs, queried with languages such as Cypher (Francis et al., 2018), and RDF triple stores, queried with SPARQL (W3C SPARQL 1.1). They complement relational databases, which favour fixed schemas, and vector databases, which favour similarity search.

### How it works

Data is stored as nodes, edges and their properties, and queries describe the pattern of nodes and edges to find. The database matches the pattern by following edges from node to node, so multi-step relationships do not require many joins.

```text
1. Graph database models
▼
2. Property graphs and Cypher
▼
3. RDF triple stores and SPARQL
▼
4. Traversal-heavy queries
▼
5. Choosing a database model
```

#### 1. Graph database models

In graph database models, the data structures for schema and instances are modelled as graphs, and data manipulation is expressed by graph-oriented operations (Angles & Gutierrez, 2008). Such models emerged in the 1980s and early 1990s, faded, and regained relevance with the need to manage information whose structure is inherently a graph; the survey covers their data structures, query languages and integrity constraints.

#### 2. Property graphs and Cypher

A property graph consists of nodes with labels and relationships with exactly one type and a direction; both can carry properties as key-value pairs (Neo4j Cypher Manual). Cypher, originally designed for the Neo4j graph database and now governed by the openCypher project, expresses subgraphs of interest with an ASCII-art pattern syntax, for example MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN b (Francis et al., 2018; Neo4j Cypher Manual).

#### 3. RDF triple stores and SPARQL

RDF stores hold triples of subject, predicate and object. SPARQL matches triple patterns containing variables against the graph, combines them with FILTER, OPTIONAL and UNION, aggregates and orders results, and uses property paths to follow paths of arbitrary length (W3C SPARQL 1.1; [[sparql|SPARQL]]). The RDF model is suited to integrating and publishing data with global identifiers ([[rdf|RDF (Resource Description Framework)]]).

#### 4. Traversal-heavy queries

Questions such as "which documents cite a norm that amends this regulation" follow several relationships in sequence. Graph query languages express such paths directly as patterns (Francis et al., 2018), and SPARQL property paths match paths of arbitrary length (W3C SPARQL 1.1). Hogan et al. (2020) compare the graph data models and query languages used for knowledge graphs ([[knowledge-graphs|Knowledge Graphs]]).

#### 5. Choosing a database model

Relational databases suit stable schemas and tabular, transactional data ([[sql|SQL]]); graph databases suit connected data with traversal-heavy queries and evolving relationships (Angles & Gutierrez, 2008); vector databases suit similarity search over embeddings ([[vector-databases|Vector Databases]]). Applications such as GraphRAG combine graph and vector stores ([[graphrag|GraphRAG]]).

#### Origin and variants

Graph database models date back to the 1980s (Angles & Gutierrez, 2008). Property graph databases such as Neo4j with Cypher (Francis et al., 2018) and RDF triple stores with SPARQL (W3C SPARQL 1.1) are the two main families today, both used for knowledge graphs (Hogan et al., 2020).

### When to use it

- When the important questions are about relationships and paths, not single records (Angles & Gutierrez, 2008).
- When an application needs flexible, evolving connections between entities, a property graph fits (Francis et al., 2018).
- When data must be integrated and exchanged using web standards, an RDF store fits (W3C SPARQL 1.1).

### Strengths and limitations

**Strengths**
- Multi-step relationships are expressed directly as patterns (Francis et al., 2018).
- SPARQL property paths match paths of arbitrary length (W3C SPARQL 1.1).
- The graph structure accommodates new kinds of relationships easily (Hogan et al., 2020).

**Limitations**
- Several query languages coexist, such as Cypher and SPARQL, with different data models (Francis et al., 2018; W3C SPARQL 1.1).
- For tabular, transactional data with stable schemas, relational databases are often simpler ([[sql|SQL]]).
- Graph databases do not provide semantic similarity search by themselves ([[vector-databases|Vector Databases]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Property graph database | Labelled nodes, typed relationships with properties, Cypher (Neo4j Cypher Manual; Francis et al., 2018) | Application data with many traversals |
| RDF triple store | Triples with global IRIs, SPARQL (W3C SPARQL 1.1) | Linked data, standards-based integration |
| Relational database | Tables, joins, fixed schema ([[sql|SQL]]) | Transactional, tabular data |
| Vector database | Nearest-neighbour search over embeddings ([[vector-databases|Vector Databases]]) | Semantic search |

### In practice

A simple legal knowledge graph in Cypher might create nodes for norms and decisions and connect them: CREATE (d:Decision {id: "X"})-[:CITES]->(n:Norm {id: "Art. 6 GDPR"}), and later query MATCH (d:Decision)-[:CITES]->(n:Norm {id: "Art. 6 GDPR"}) RETURN d (Neo4j Cypher Manual). Data modelling starts from the queries the graph must answer ([[ontology-design|Ontology Design]]).

### Key takeaway

Graph databases store data as nodes and edges and query it as patterns, which makes connected, multi-step questions simple to express.

### Sources

- Angles, R. & Gutierrez, C. (2008). *Survey of graph database models.* ACM Computing Surveys 40(1). [doi:10.1145/1322432.1322433](https://doi.org/10.1145/1322432.1322433)
- Francis, N., Green, A., Guagliardo, P., Libkin, L., Lindaaker, T., Marsault, V., Plantikow, S., Rydberg, M., Selmer, P. & Taylor, A. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
- W3C (2013). *SPARQL 1.1 Query Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/sparql11-query/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Graphdatenbanken speichern Daten als Knoten und Kanten und formulieren Abfragen als Graphmuster und Traversierungen; das passt zu Daten, deren Wert in ihren Verbindungen liegt (Angles & Gutierrez, 2008). Die beiden Hauptmodelle sind Property Graphs, die mit Sprachen wie Cypher abgefragt werden (Francis et al., 2018), und RDF-Triplestores, die mit SPARQL abgefragt werden (W3C SPARQL 1.1). Sie ergänzen relationale Datenbanken, die feste Schemata bevorzugen, und Vektordatenbanken, die auf Ähnlichkeitssuche ausgelegt sind.

### Funktionsweise

Daten werden als Knoten, Kanten und deren Eigenschaften gespeichert, und Abfragen beschreiben das gesuchte Muster aus Knoten und Kanten. Die Datenbank findet das Muster, indem sie Kanten von Knoten zu Knoten folgt; Beziehungen über mehrere Schritte erfordern so keine vielen Joins.

```text
1. Graphdatenbankmodelle
▼
2. Property Graphs und Cypher
▼
3. RDF-Triplestores und SPARQL
▼
4. Abfragen mit vielen Traversierungen
▼
5. Wahl des Datenbankmodells
```

#### 1. Graphdatenbankmodelle

In Graphdatenbankmodellen werden die Datenstrukturen für Schema und Instanzen als Graphen modelliert, und die Datenmanipulation wird durch graphorientierte Operationen ausgedrückt (Angles & Gutierrez, 2008). Solche Modelle entstanden in den 1980er- und frühen 1990er-Jahren, traten dann in den Hintergrund und gewannen mit dem Bedarf, Information mit von Natur aus graphartiger Struktur zu verwalten, wieder an Bedeutung; die Übersicht behandelt ihre Datenstrukturen, Abfragesprachen und Integritätsbedingungen.

#### 2. Property Graphs und Cypher

Ein Property Graph besteht aus Knoten mit Labels und Beziehungen mit genau einem Typ und einer Richtung; beide können Eigenschaften als Schlüssel-Wert-Paare tragen (Neo4j Cypher Manual). Cypher, ursprünglich für die Graphdatenbank Neo4j entworfen und heute vom openCypher-Projekt betreut, beschreibt gesuchte Teilgraphen mit einer ASCII-Art-Mustersyntax, etwa MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN b (Francis et al., 2018; Neo4j Cypher Manual).

#### 3. RDF-Triplestores und SPARQL

RDF-Stores enthalten Tripel aus Subjekt, Prädikat und Objekt. SPARQL gleicht Tripelmuster mit Variablen gegen den Graphen ab, verbindet sie mit FILTER, OPTIONAL und UNION, aggregiert und sortiert Ergebnisse und folgt mit Property Paths Pfaden beliebiger Länge (W3C SPARQL 1.1; [[sparql|SPARQL]]). Das RDF-Modell eignet sich, um Daten mit globalen Bezeichnern zusammenzuführen und zu veröffentlichen ([[rdf|RDF (Resource Description Framework)]]).

#### 4. Abfragen mit vielen Traversierungen

Fragen wie „Welche Dokumente zitieren eine Norm, die diese Verordnung ändert?“ folgen mehreren Beziehungen nacheinander. Graph-Abfragesprachen drücken solche Pfade direkt als Muster aus (Francis et al., 2018), und SPARQL-Property-Paths finden Pfade beliebiger Länge (W3C SPARQL 1.1). Hogan et al. (2020) vergleichen die für Wissensgraphen genutzten Graph-Datenmodelle und Abfragesprachen ([[knowledge-graphs|Wissensgraphen]]).

#### 5. Wahl des Datenbankmodells

Relationale Datenbanken passen zu stabilen Schemata und tabellarischen Transaktionsdaten ([[sql|SQL]]); Graphdatenbanken passen zu vernetzten Daten mit vielen Traversierungen und sich entwickelnden Beziehungen (Angles & Gutierrez, 2008); Vektordatenbanken passen zur Ähnlichkeitssuche über Embeddings ([[vector-databases|Vektordatenbanken]]). Anwendungen wie GraphRAG kombinieren Graph- und Vektorspeicher ([[graphrag|GraphRAG]]).

#### Ursprung und Varianten

Graphdatenbankmodelle reichen bis in die 1980er-Jahre zurück (Angles & Gutierrez, 2008). Property-Graph-Datenbanken wie Neo4j mit Cypher (Francis et al., 2018) und RDF-Triplestores mit SPARQL (W3C SPARQL 1.1) sind heute die beiden Hauptfamilien, beide werden für Wissensgraphen genutzt (Hogan et al., 2020).

### Wann einsetzen

- Wenn die wichtigen Fragen Beziehungen und Pfade betreffen, nicht einzelne Datensätze (Angles & Gutierrez, 2008).
- Wenn eine Anwendung flexible, sich entwickelnde Verbindungen zwischen Entitäten braucht, passt ein Property Graph (Francis et al., 2018).
- Wenn Daten mit Webstandards zusammengeführt und ausgetauscht werden müssen, passt ein RDF-Store (W3C SPARQL 1.1).

### Stärken und Grenzen

**Stärken**
- Beziehungen über mehrere Schritte lassen sich direkt als Muster ausdrücken (Francis et al., 2018).
- SPARQL-Property-Paths finden Pfade beliebiger Länge (W3C SPARQL 1.1).
- Die Graphstruktur nimmt neue Arten von Beziehungen leicht auf (Hogan et al., 2020).

**Einschränkungen**
- Mehrere Abfragesprachen wie Cypher und SPARQL bestehen nebeneinander, mit unterschiedlichen Datenmodellen (Francis et al., 2018; W3C SPARQL 1.1).
- Für tabellarische Transaktionsdaten mit stabilen Schemata sind relationale Datenbanken oft einfacher ([[sql|SQL]]).
- Graphdatenbanken bieten von sich aus keine semantische Ähnlichkeitssuche ([[vector-databases|Vektordatenbanken]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Property-Graph-Datenbank | Knoten mit Labels, typisierte Beziehungen mit Eigenschaften, Cypher (Neo4j Cypher Manual; Francis et al., 2018) | Anwendungsdaten mit vielen Traversierungen |
| RDF-Triplestore | Tripel mit globalen IRIs, SPARQL (W3C SPARQL 1.1) | Linked Data, standardbasierte Integration |
| Relationale Datenbank | Tabellen, Joins, festes Schema ([[sql|SQL]]) | Transaktionale, tabellarische Daten |
| Vektordatenbank | Nächste-Nachbarn-Suche über Embeddings ([[vector-databases|Vektordatenbanken]]) | Semantische Suche |

### In der Praxis

Ein einfacher juristischer Wissensgraph in Cypher könnte Knoten für Normen und Entscheidungen anlegen und verbinden: CREATE (d:Decision {id: "X"})-[:CITES]->(n:Norm {id: "Art. 6 DSGVO"}), und später abfragen: MATCH (d:Decision)-[:CITES]->(n:Norm {id: "Art. 6 DSGVO"}) RETURN d (Neo4j Cypher Manual). Die Datenmodellierung beginnt mit den Abfragen, die der Graph beantworten soll ([[ontology-design|Ontologie-Design]]).

### Merksatz

Graphdatenbanken speichern Daten als Knoten und Kanten und fragen sie als Muster ab, wodurch sich vernetzte Fragen über mehrere Schritte einfach ausdrücken lassen.

### Quellen

- Angles, R. & Gutierrez, C. (2008). *Survey of graph database models.* ACM Computing Surveys 40(1). [doi:10.1145/1322432.1322433](https://doi.org/10.1145/1322432.1322433)
- Francis, N., Green, A., Guagliardo, P., Libkin, L., Lindaaker, T., Marsault, V., Plantikow, S., Rydberg, M., Selmer, P. & Taylor, A. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
- W3C (2013). *SPARQL 1.1 Query Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/sparql11-query/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
