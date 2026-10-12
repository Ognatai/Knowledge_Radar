---
title_en: GQL (Graph Query Language)
title_de: GQL (Graph Query Language)
entity_type: Technology
aliases:
- GQL
- ISO/IEC 39075
sources:
- https://www.gqlstandards.org/
- https://arxiv.org/abs/2112.06217
- https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/
- https://doi.org/10.1145/3183713.3190657
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

GQL is the ISO standard database language for property graphs, published on 17 April 2024 as ISO/IEC 39075:2024 (GQL Standards). It covers querying, data manipulation and schema definition, integrates ideas from openCypher, PGQL, GSQL and G-CORE, and shares its graph pattern matching core with [[sql|SQL]]/PGQ, the property graph part of the SQL standard (GQL Standards; Deutsch et al., 2021). [[cypher|Cypher]] already supports most of its mandatory features (Neo4j Cypher Manual: GQL conformance).

### Core concepts

- **Standard and committee:** GQL is developed by ISO/IEC JTC1 SC32 WG3, the working group that also maintains SQL; it was published as ISO/IEC 39075:2024 on 17 April 2024 (GQL Standards; Deutsch et al., 2021).
- **A full database language:** GQL includes data manipulation (DML) and data definition (DDL) and supports both schema-fixed and schema-flexible graphs (GQL Standards).
- **Graph pattern matching (GPM):** The core of GQL is a sublanguage for matching patterns of nodes and edges, which Deutsch et al. call GPML; GQL and SQL/PGQ are required to share this core identically (Deutsch et al., 2021; GQL Standards).
- **SQL/PGQ:** A part of the SQL standard (ISO/IEC 9075-16) that defines graph views over existing relational tables and allows read-only graph queries on them; with GQL, the same pattern language works on native graph databases and on SQL databases (Deutsch et al., 2021; GQL Standards).
- **Origins:** GQL integrates proven ideas from openCypher, PGQL, GSQL and G-CORE (GQL Standards). openCypher governs [[cypher|Cypher]], which was designed for [[neo4j|Neo4j]] and writes patterns in an ASCII-art syntax (Francis et al., 2018).
- **Formal semantics:** Alongside the standard, an academic group of the Linked Data Benchmark Council (LDBC) works on a formal semantics of the pattern language (Deutsch et al., 2021).
- **Mandatory and optional features:** The standard defines mandatory features, such as a graph with an open graph type and the property types BOOLEAN, FLOAT, INTEGER and STRING, and optional features such as DATE, DURATION and POINT (Neo4j Cypher Manual: GQL conformance).

### Common usage

```cypher
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
WHERE a.name = 'Tom Hanks'
RETURN m.title
```

This query is valid both in GQL and in Cypher: GQL adopted much of Cypher's query construction semantics, so users should expect only minimal differences between the two languages (Neo4j Cypher Manual: GQL conformance).

### When to use it

- When graph queries should follow a vendor-neutral ISO standard rather than a product-specific dialect (GQL Standards).
- When graph patterns should run on graph views over relational data with SQL/PGQ and on native graph databases alike (Deutsch et al., 2021).
- In practice, through a database that implements it: Cypher in [[neo4j|Neo4j]] accommodates most mandatory GQL features and a substantial part of the optional ones (Neo4j Cypher Manual: GQL conformance).

### Strengths and limitations

**Strengths**
- An ISO standard query language for property [[graph-databases|graph databases]], developed by the same working group as SQL (GQL Standards; Deutsch et al., 2021).
- One pattern matching language for graph databases and SQL/PGQ (GQL Standards).
- Builds on languages already in use, so existing Cypher knowledge carries over (GQL Standards; Neo4j Cypher Manual: GQL conformance).

**Limitations**
- Implementations are still catching up: Neo4j, for example, does not yet support all mandatory features and is working on more optional ones (Neo4j Cypher Manual: GQL conformance).
- Products keep their own extensions; Cypher has features that are not part of GQL (Neo4j Cypher Manual: GQL conformance).
- The standard text itself is sold through the ISO web store, not freely available (GQL Standards).

### Comparison

| Language | Status | Data model |
|----------|--------|------------|
| GQL | ISO/IEC 39075:2024 (GQL Standards) | Property graphs |
| SQL/PGQ | Part of the SQL standard (Deutsch et al., 2021) | Graph views over relational tables |
| [[cypher\|Cypher]] | openCypher, Neo4j (Francis et al., 2018) | Property graphs |
| [[sparql\|SPARQL]] | W3C Recommendation | [[rdf\|RDF]] triples |

### In practice

For [[knowledge-graphs|knowledge graphs]] in the property graph model, writing queries in the part of Cypher that GQL shares keeps them portable; the conformance appendix of the Cypher manual lists which GQL features are supported and which Cypher equivalents exist for the others (Neo4j Cypher Manual: GQL conformance).

### Key takeaway

GQL is the ISO standard language for property graphs since 2024; it shares its pattern matching with SQL/PGQ and adopted much of Cypher, which already supports most of its mandatory features.

### Sources

- GQL Standards Committee. *GQL Standards.* [gqlstandards.org](https://www.gqlstandards.org/)
- Deutsch, A. et al. (2021). *Graph Pattern Matching in GQL and SQL/PGQ.* arXiv:2112.06217. [arxiv.org](https://arxiv.org/abs/2112.06217)
- Neo4j. *GQL conformance.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/)
- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

GQL ist die nach ISO standardisierte Datenbanksprache für Property Graphs, veröffentlicht am 17. April 2024 als ISO/IEC 39075:2024 (GQL Standards). Sie umfasst Abfragen, Datenänderung und Schemadefinition, übernimmt Ideen aus openCypher, PGQL, GSQL und G-CORE und teilt ihren Kern für Graph Pattern Matching mit [[sql|SQL]]/PGQ, dem Property-Graph-Teil des SQL-Standards (GQL Standards; Deutsch et al., 2021). [[cypher|Cypher]] unterstützt bereits die meisten ihrer verpflichtenden Funktionen (Neo4j Cypher Manual: GQL conformance).

### Kernkonzepte

- **Standard und Gremium:** GQL wird von ISO/IEC JTC1 SC32 WG3 entwickelt, der Arbeitsgruppe, die auch SQL pflegt; veröffentlicht wurde es am 17. April 2024 als ISO/IEC 39075:2024 (GQL Standards; Deutsch et al., 2021).
- **Vollständige Datenbanksprache:** GQL umfasst Datenänderung (DML) und Datendefinition (DDL) und unterstützt Graphen mit festem wie mit flexiblem Schema (GQL Standards).
- **Graph Pattern Matching (GPM):** Kern von GQL ist eine Teilsprache, die Muster aus Knoten und Kanten findet und die Deutsch et al. GPML nennen; GQL und SQL/PGQ müssen diesen Kern identisch teilen (Deutsch et al., 2021; GQL Standards).
- **SQL/PGQ:** Ein Teil des SQL-Standards (ISO/IEC 9075-16), der Graph-Views über bestehende relationale Tabellen definiert und darauf lesende Graphabfragen erlaubt; zusammen mit GQL funktioniert dieselbe Mustersprache auf nativen Graphdatenbanken und auf SQL-Datenbanken (Deutsch et al., 2021; GQL Standards).
- **Herkunft:** GQL übernimmt bewährte Ideen aus openCypher, PGQL, GSQL und G-CORE (GQL Standards). openCypher pflegt [[cypher|Cypher]], das für [[neo4j|Neo4j]] entworfen wurde und Muster in einer ASCII-Art-Syntax schreibt (Francis et al., 2018).
- **Formale Semantik:** Neben dem Standard arbeitet eine akademische Gruppe des Linked Data Benchmark Council (LDBC) an einer formalen Semantik der Mustersprache (Deutsch et al., 2021).
- **Verpflichtende und optionale Funktionen:** Der Standard legt verpflichtende Funktionen fest, etwa einen Graphen mit offenem Graphtyp und die Eigenschaftstypen BOOLEAN, FLOAT, INTEGER und STRING, sowie optionale wie DATE, DURATION und POINT (Neo4j Cypher Manual: GQL conformance).

### Typische Verwendung

```cypher
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
WHERE a.name = 'Tom Hanks'
RETURN m.title
```

Diese Abfrage ist in GQL und in Cypher gültig: GQL hat viel von der Abfragesemantik von Cypher übernommen, sodass zwischen beiden Sprachen nur minimale Unterschiede zu erwarten sind (Neo4j Cypher Manual: GQL conformance).

### Wann einsetzen

- Wenn Graphabfragen einem herstellerunabhängigen ISO-Standard folgen sollen statt einem produktspezifischen Dialekt (GQL Standards).
- Wenn Graphmuster gleichermaßen auf Graph-Views über relationalen Daten mit SQL/PGQ und auf nativen Graphdatenbanken laufen sollen (Deutsch et al., 2021).
- In der Praxis über eine Datenbank, die es umsetzt: Cypher in [[neo4j|Neo4j]] deckt die meisten verpflichtenden GQL-Funktionen und einen erheblichen Teil der optionalen ab (Neo4j Cypher Manual: GQL conformance).

### Stärken und Grenzen

**Stärken**
- Eine ISO-standardisierte Abfragesprache für Property-[[graph-databases|Graphdatenbanken]], entwickelt von derselben Arbeitsgruppe wie SQL (GQL Standards; Deutsch et al., 2021).
- Eine Mustersprache für Graphdatenbanken und SQL/PGQ (GQL Standards).
- Baut auf bereits genutzten Sprachen auf, sodass Wissen über Cypher übertragbar bleibt (GQL Standards; Neo4j Cypher Manual: GQL conformance).

**Grenzen**
- Die Umsetzungen holen noch auf: Neo4j etwa unterstützt noch nicht alle verpflichtenden Funktionen und arbeitet an weiteren optionalen (Neo4j Cypher Manual: GQL conformance).
- Produkte behalten eigene Erweiterungen; Cypher hat Funktionen, die nicht Teil von GQL sind (Neo4j Cypher Manual: GQL conformance).
- Der Standardtext selbst wird über den ISO-Webshop verkauft und ist nicht frei verfügbar (GQL Standards).

### Vergleich

| Sprache | Status | Datenmodell |
|---------|--------|-------------|
| GQL | ISO/IEC 39075:2024 (GQL Standards) | Property Graphs |
| SQL/PGQ | Teil des SQL-Standards (Deutsch et al., 2021) | Graph-Views über relationalen Tabellen |
| [[cypher\|Cypher]] | openCypher, Neo4j (Francis et al., 2018) | Property Graphs |
| [[sparql\|SPARQL]] | W3C-Empfehlung | RDF-Tripel |

### In der Praxis

Für [[knowledge-graphs|Wissensgraphen]] im Property-Graph-Modell bleiben Abfragen portabel, wenn sie den Teil von Cypher nutzen, den GQL teilt; der Konformitätsanhang des Cypher-Handbuchs listet, welche GQL-Funktionen unterstützt werden und welche Cypher-Entsprechungen es für die übrigen gibt (Neo4j Cypher Manual: GQL conformance).

### Merksatz

GQL ist seit 2024 die ISO-Standardsprache für Property Graphs; sie teilt ihr Pattern Matching mit SQL/PGQ und hat viel von Cypher übernommen, das bereits die meisten ihrer verpflichtenden Funktionen unterstützt.

### Quellen

- GQL Standards Committee. *GQL Standards.* [gqlstandards.org](https://www.gqlstandards.org/)
- Deutsch, A. et al. (2021). *Graph Pattern Matching in GQL and SQL/PGQ.* arXiv:2112.06217. [arxiv.org](https://arxiv.org/abs/2112.06217)
- Neo4j. *GQL conformance.* Cypher Manual. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/)
- Francis, N. et al. (2018). *Cypher: An Evolving Query Language for Property Graphs.* SIGMOD 2018. [doi:10.1145/3183713.3190657](https://doi.org/10.1145/3183713.3190657)
