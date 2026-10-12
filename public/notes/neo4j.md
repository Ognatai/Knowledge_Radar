---
title_en: Neo4j
title_de: Neo4j
entity_type: Technology
sources:
- https://neo4j.com/docs/getting-started/whats-neo4j/
- https://neo4j.com/docs/operations-manual/current/introduction/
- https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/
- https://neo4j.com/docs/cypher-manual/current/clauses/merge/
- https://neo4j.com/docs/graph-data-science/current/introduction/
- https://doi.org/10.1145/3183713.3190657
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Neo4j is a native property graph database: nodes carry labels, relationships have a type and a direction, and both store properties as key-value pairs; the graph model is implemented down to the storage level, with ACID transactions and optional clustering (Neo4j docs: What is Neo4j). It is queried with [[cypher|Cypher]], comes as a self-managed Community or Enterprise Edition and as the managed cloud service Aura (Neo4j Operations Manual), and adds vector indexes for similarity search and a Graph Data Science library with graph algorithms (Neo4j Cypher Manual: Vector indexes; Neo4j GDS Manual).

### Core concepts

- **Property graph model:** Nodes are entities classified by labels; a node can have zero or more labels, and a label "marks a node as a member of a named and indexed subset". Relationships link a source node to a target node and are classified by a type; properties are key-value pairs on nodes and relationships (Neo4j docs: What is Neo4j). The model is the property graph described in [[graph-databases|Graph Databases]].
- **Native graph storage:** Neo4j describes itself as a native graph database that "implements a true graph model all the way down to the storage level" (Neo4j docs: What is Neo4j).
- **Transactions and clusters:** Neo4j provides ACID transactions; a cluster spans several servers to increase fault tolerance and read scalability, with failover at runtime (Neo4j docs: What is Neo4j).
- **Query language:** Cypher is a declarative language "similar to SQL, but optimized for graphs"; it was designed for Neo4j and is governed by the openCypher project, which other systems such as SAP HANA Graph also use (Neo4j docs: What is Neo4j; Francis et al., 2018).
- **Indexes and constraints:** Key and uniqueness constraints are index-backed and protect against duplicate nodes when data is loaded concurrently with MERGE (Neo4j Cypher Manual: MERGE; [[cypher|Cypher]]).
- **Vector indexes:** A vector index stores [[embeddings|embeddings]] of nodes or relationships for approximate nearest neighbour search with HNSW graphs (implemented by Lucene); it supports cosine and Euclidean similarity and up to 4,096 dimensions, and has been generally available since Neo4j 5.13 (Neo4j Cypher Manual: Vector indexes).
- **Graph Data Science (GDS):** A library of parallel graph algorithms exposed as Cypher procedures, for example centralities, community detection and machine learning pipelines that predict missing relationships; it loads the graph from the database into an in-memory graph catalog first (Neo4j GDS Manual).
- **Editions and deployment:** The Community Edition is suited to single-instance deployments; the Enterprise Edition adds clustering, online backup, role-based access control and LDAP. Neo4j runs locally, in Docker, on [[kubernetes|Kubernetes]] via Helm charts, or as the fully managed Aura cloud service (Neo4j Operations Manual; Neo4j docs: What is Neo4j).
- **Drivers:** Neo4j supports Java, JavaScript, .NET, Python and Go, among others; the Query API serves languages without a driver (Neo4j docs: What is Neo4j).

### Common usage

```cypher
// uniqueness first, then idempotent loading
CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;
MERGE (a:Person {name: 'Ada'})
MERGE (c:Company {name: 'ACME'})
MERGE (a)-[:WORKS_AT {since: 2024}]->(c);

// vector index on text embeddings (1536 dimensions, cosine)
CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS
FOR (c:Chunk) ON c.embedding
OPTIONS { indexConfig: { `vector.dimensions`: 1536, `vector.similarity_function`: 'cosine' } };
```

Since release 2026.01, vector indexes are queried with the SEARCH clause; the older procedure db.index.vector.queryNodes(indexName, k, query) still works but is deprecated (Neo4j Cypher Manual: Vector indexes).

### When to use it

- When questions follow relationships over several steps, such as who is connected to whom through which projects, and the data model changes over time ([[graph-databases|Graph Databases]]; Neo4j docs: What is Neo4j).
- For [[knowledge-graphs|knowledge graphs]] in the property graph model, and for [[graphrag|GraphRAG]], where graph structure and vector search are combined in one database (Neo4j Cypher Manual: Vector indexes).
- For graph analytics such as finding central entities or communities with GDS (Neo4j GDS Manual).
- When data must be exchanged as linked data with global identifiers, an [[rdf|RDF]] store with [[sparql|SPARQL]] fits better.

### Strengths and limitations

**Strengths**
- Graph model down to the storage level, ACID transactions and a declarative query language (Neo4j docs: What is Neo4j).
- Graph traversal, vector search and graph algorithms in one system (Neo4j Cypher Manual: Vector indexes; Neo4j GDS Manual).
- Many deployment options, from a local Docker container to a managed cloud service (Neo4j docs: What is Neo4j).

**Limitations**
- Clustering, online backup and role-based access control need the Enterprise Edition (Neo4j Operations Manual).
- The Community edition of GDS limits concurrency to four CPU cores and the model catalog to three models (Neo4j GDS Manual).
- Vector search is approximate: results are not guaranteed to be the exact nearest neighbours (Neo4j Cypher Manual: Vector indexes).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Neo4j | Property graph, Cypher, vector index and GDS in one database (Neo4j docs: What is Neo4j) | Connected application data, GraphRAG |
| RDF triple store | Triples with global IRIs, queried with [[sparql\|SPARQL]] | Linked data, data integration |
| [[vector-databases\|Vector databases]] | Similarity search only, no graph traversal | Pure semantic search |
| Relational database | Tables and joins with [[sql\|SQL]] | Fixed schemas, transactional records |

### In practice

Constraints are created before data is loaded, so that MERGE finds existing nodes instead of creating duplicates (Neo4j Cypher Manual: MERGE). Because vector indexes can be created on nodes and on relationships, embeddings of text chunks for [[retrieval-augmented-generation|RAG]] can be stored in the same database as the entities and relationships of a [[graphrag|GraphRAG]] graph (Neo4j Cypher Manual: Vector indexes). Graph algorithms in GDS run on a projected in-memory copy, so the projection should include only the labels and relationship types an analysis needs (Neo4j GDS Manual). Neo4j images for Docker cover both editions, which keeps a local development setup close to production (Neo4j docs: What is Neo4j; [[docker|Docker]]).

### Key takeaway

Neo4j is a native property graph database with ACID transactions, queried with Cypher, that combines graph traversal, vector search and graph algorithms in one system.

### Sources

- Neo4j. *What is Neo4j?* Getting Started Guide. [neo4j.com](https://neo4j.com/docs/getting-started/whats-neo4j/)
- Neo4j. *Introduction.* Operations Manual. [neo4j.com](https://neo4j.com/docs/operations-manual/current/introduction/)
- Neo4j. *Vector indexes.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- Neo4j. *Introduction.* Graph Data Science Manual. [neo4j.com](https://neo4j.com/docs/graph-data-science/current/introduction/)
- Neo4j. *MERGE.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Neo4j ist eine native Property-Graph-Datenbank: Knoten tragen Labels, Beziehungen haben einen Typ und eine Richtung, und beide speichern Eigenschaften als Schlüssel-Wert-Paare; das Graphmodell ist bis auf die Speicherebene umgesetzt, mit ACID-Transaktionen und optionalem Clustering (Neo4j docs: What is Neo4j). Abgefragt wird mit [[cypher|Cypher]]; es gibt die selbst betriebene Community- und Enterprise Edition sowie den verwalteten Cloud-Dienst Aura (Neo4j Operations Manual), dazu Vektorindizes für Ähnlichkeitssuche und eine Graph-Data-Science-Bibliothek mit Graphalgorithmen (Neo4j Cypher Manual: Vector indexes; Neo4j GDS Manual).

### Kernkonzepte

- **Property-Graph-Modell:** Knoten sind Entitäten, die über Labels klassifiziert werden; ein Knoten kann null oder mehr Labels haben, und ein Label kennzeichnet einen Knoten als Mitglied einer benannten und indizierten Teilmenge. Beziehungen verbinden einen Start- mit einem Zielknoten und werden über einen Typ klassifiziert; Eigenschaften sind Schlüssel-Wert-Paare an Knoten und Beziehungen (Neo4j docs: What is Neo4j). Das Modell ist der in [[graph-databases|Graphdatenbanken]] beschriebene Property Graph.
- **Native Graphspeicherung:** Neo4j beschreibt sich als native Graphdatenbank, die ein echtes Graphmodell bis hinunter auf die Speicherebene umsetzt (Neo4j docs: What is Neo4j).
- **Transaktionen und Cluster:** Neo4j bietet ACID-Transaktionen; ein Cluster erstreckt sich über mehrere Server, um Ausfallsicherheit und Leseskalierung zu erhöhen, mit Failover zur Laufzeit (Neo4j docs: What is Neo4j).
- **Abfragesprache:** Cypher ist eine deklarative Sprache, ähnlich wie SQL, aber für Graphen optimiert; sie wurde für Neo4j entworfen und wird vom openCypher-Projekt gepflegt, das auch andere Systeme wie SAP HANA Graph nutzen (Neo4j docs: What is Neo4j; Francis et al., 2018).
- **Indizes und Constraints:** Key- und Uniqueness-Constraints sind indexgestützt und verhindern doppelte Knoten, wenn Daten parallel mit MERGE geladen werden (Neo4j Cypher Manual: MERGE; [[cypher|Cypher]]).
- **Vektorindizes:** Ein Vektorindex speichert [[embeddings|Embeddings]] von Knoten oder Beziehungen für Approximate Nearest Neighbor Search mit HNSW-Graphen (umgesetzt von Lucene); er unterstützt Cosine- und euklidische Ähnlichkeit sowie bis zu 4.096 Dimensionen und ist seit Neo4j 5.13 allgemein verfügbar (Neo4j Cypher Manual: Vector indexes).
- **Graph Data Science (GDS):** Eine Bibliothek paralleler Graphalgorithmen, die als Cypher-Prozeduren bereitstehen, etwa Zentralitäten, Community Detection und Machine-Learning-Pipelines, die fehlende Beziehungen vorhersagen; dazu wird der Graph zuerst aus der Datenbank in einen In-Memory-Graphkatalog geladen (Neo4j GDS Manual).
- **Editionen und Betrieb:** Die Community Edition eignet sich für Einzelinstanzen; die Enterprise Edition ergänzt Clustering, Online-Backup, rollenbasierte Zugriffskontrolle und LDAP. Neo4j läuft lokal, in Docker, auf [[kubernetes|Kubernetes]] über Helm-Charts oder als vollständig verwalteter Cloud-Dienst Aura (Neo4j Operations Manual; Neo4j docs: What is Neo4j).
- **Treiber:** Neo4j unterstützt unter anderem Java, JavaScript, .NET, Python und Go; die Query API bedient Sprachen ohne eigenen Treiber (Neo4j docs: What is Neo4j).

### Typische Verwendung

```cypher
// erst Eindeutigkeit, dann idempotent laden
CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;
MERGE (a:Person {name: 'Ada'})
MERGE (c:Company {name: 'ACME'})
MERGE (a)-[:WORKS_AT {since: 2024}]->(c);

// Vektorindex für Text-Embeddings (1536 Dimensionen, Cosine)
CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS
FOR (c:Chunk) ON c.embedding
OPTIONS { indexConfig: { `vector.dimensions`: 1536, `vector.similarity_function`: 'cosine' } };
```

Seit Release 2026.01 werden Vektorindizes mit der SEARCH-Klausel abgefragt; die ältere Prozedur db.index.vector.queryNodes(indexName, k, query) funktioniert weiter, ist aber veraltet (Neo4j Cypher Manual: Vector indexes).

### Wann einsetzen

- Wenn Fragen Beziehungen über mehrere Schritte folgen, etwa wer über welche Projekte mit wem verbunden ist, und sich das Datenmodell mit der Zeit ändert ([[graph-databases|Graphdatenbanken]]; Neo4j docs: What is Neo4j).
- Für [[knowledge-graphs|Wissensgraphen]] im Property-Graph-Modell und für [[graphrag|GraphRAG]], wo Graphstruktur und Vektorsuche in einer Datenbank zusammenkommen (Neo4j Cypher Manual: Vector indexes).
- Für Graphanalysen wie das Finden zentraler Entitäten oder Communities mit GDS (Neo4j GDS Manual).
- Wenn Daten als Linked Data mit globalen Bezeichnern ausgetauscht werden sollen, passt ein [[rdf|RDF]]-Store mit [[sparql|SPARQL]] besser.

### Stärken und Grenzen

**Stärken**
- Graphmodell bis auf die Speicherebene, ACID-Transaktionen und eine deklarative Abfragesprache (Neo4j docs: What is Neo4j).
- Graphtraversierung, Vektorsuche und Graphalgorithmen in einem System (Neo4j Cypher Manual: Vector indexes; Neo4j GDS Manual).
- Viele Betriebsformen, vom lokalen Docker-Container bis zum verwalteten Cloud-Dienst (Neo4j docs: What is Neo4j).

**Grenzen**
- Clustering, Online-Backup und rollenbasierte Zugriffskontrolle erfordern die Enterprise Edition (Neo4j Operations Manual).
- Die Community-Variante von GDS begrenzt die Parallelität auf vier CPU-Kerne und den Modellkatalog auf drei Modelle (Neo4j GDS Manual).
- Die Vektorsuche ist approximativ: Die Ergebnisse sind nicht garantiert die exakt nächsten Nachbarn (Neo4j Cypher Manual: Vector indexes).

### Vergleich

| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Neo4j | Property Graph, Cypher, Vektorindex und GDS in einer Datenbank (Neo4j docs: What is Neo4j) | Vernetzte Anwendungsdaten, GraphRAG |
| RDF-Triple-Store | Tripel mit globalen IRIs, abgefragt mit [[sparql\|SPARQL]] | Linked Data, Datenintegration |
| [[vector-databases\|Vektordatenbanken]] | Nur Ähnlichkeitssuche, keine Graphtraversierung | Reine semantische Suche |
| Relationale Datenbank | Tabellen und Joins mit [[sql\|SQL]] | Festes Schema, transaktionale Datensätze |

### In der Praxis

Constraints werden vor dem Laden der Daten angelegt, damit MERGE vorhandene Knoten findet, statt Duplikate zu erzeugen (Neo4j Cypher Manual: MERGE). Weil sich Vektorindizes auf Knoten und auf Beziehungen anlegen lassen, können Embeddings von Textabschnitten für [[retrieval-augmented-generation|RAG]] in derselben Datenbank liegen wie die Entitäten und Beziehungen eines [[graphrag|GraphRAG]]-Graphen (Neo4j Cypher Manual: Vector indexes). Graphalgorithmen in GDS laufen auf einer projizierten In-Memory-Kopie, daher sollte die Projektion nur die Labels und Beziehungstypen enthalten, die eine Analyse braucht (Neo4j GDS Manual). Die Docker-Images decken beide Editionen ab, sodass eine lokale Entwicklungsumgebung nah an der Produktion bleibt (Neo4j docs: What is Neo4j; [[docker|Docker]]).

### Merksatz

Neo4j ist eine native Property-Graph-Datenbank mit ACID-Transaktionen, abgefragt mit Cypher, die Graphtraversierung, Vektorsuche und Graphalgorithmen in einem System verbindet.

### Quellen

- Neo4j. *What is Neo4j?* Getting Started Guide. [neo4j.com](https://neo4j.com/docs/getting-started/whats-neo4j/)
- Neo4j. *Introduction.* Operations Manual. [neo4j.com](https://neo4j.com/docs/operations-manual/current/introduction/)
- Neo4j. *Vector indexes.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- Neo4j. *Introduction.* Graph Data Science Manual. [neo4j.com](https://neo4j.com/docs/graph-data-science/current/introduction/)
- Neo4j. *MERGE.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
