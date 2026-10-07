---
title_en: SQL
title_de: SQL
entity_type: Technology
sources:
- https://doi.org/10.1145/362384.362685
- https://www.postgresql.org/docs/current/tutorial-sql-intro.html
- https://www.postgresql.org/docs/current/tutorial-window.html
- https://www.postgresql.org/docs/current/queries-with.html
- https://www.postgresql.org/docs/current/indexes-intro.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

SQL is the language of relational databases, which store data in tables of rows and columns based on the relational model (Codd, 1970). It reads data with SELECT, combines tables with joins, summarises with aggregates and GROUP BY, and modifies data with INSERT, UPDATE and DELETE (PostgreSQL SQL tutorial). Window functions compute values across related rows without collapsing them (PostgreSQL window functions), common table expressions structure complex queries (PostgreSQL CTEs), and indexes speed up lookups at the cost of write overhead (PostgreSQL indexes).

### Core concepts

- **Relational model:** Data is organised as relations (tables), and applications are independent of how data is stored internally (Codd, 1970).
- **Querying:** SELECT ... FROM ... WHERE ... ORDER BY reads rows; WHERE filters rows before aggregation, and HAVING filters groups after aggregation (PostgreSQL SQL tutorial).
- **Joins:** Inner joins return matching rows; left, right and full outer joins also keep unmatched rows, filling missing columns with NULL (PostgreSQL SQL tutorial).
- **Aggregates:** count, sum, avg, max and min compute one result from many rows, grouped with GROUP BY (PostgreSQL SQL tutorial).
- **Window functions:** OVER (PARTITION BY ... ORDER BY ...) computes rankings, running totals or averages across related rows while each row keeps its identity (PostgreSQL window functions).
- **CTEs:** WITH defines named auxiliary queries that act like temporary tables for one query; WITH RECURSIVE traverses hierarchies (PostgreSQL CTEs).
- **Indexes:** CREATE INDEX avoids full table scans for selective queries but must be maintained on every write (PostgreSQL indexes).

### Common usage

```sql
-- decisions per court with their share of all decisions
WITH counts AS (
    SELECT court, COUNT(*) AS n
    FROM decisions
    WHERE year >= 2020
    GROUP BY court
    HAVING COUNT(*) > 10
)
SELECT court, n,
       ROUND(100.0 * n / SUM(n) OVER (), 1) AS share_pct,
       RANK() OVER (ORDER BY n DESC)         AS rank
FROM counts
ORDER BY rank;

-- keep decisions without a cited norm (LEFT JOIN)
SELECT d.id, c.norm_id
FROM decisions d
LEFT JOIN citations c ON c.decision_id = d.id;

CREATE INDEX idx_citations_decision ON citations (decision_id);
```

NULL represents missing values and is tested with IS NULL rather than with an equals sign; COALESCE replaces NULL with a default. CASE WHEN expresses conditional logic inside queries.

### When to use it

- For structured, tabular data with a stable schema and transactional updates (Codd, 1970).
- For reporting and analytics with grouping, ranking and running totals (PostgreSQL window functions).
- When data is highly connected and queries follow many relationships, graph databases may be simpler ([[graph-databases|Graph Databases]]).

### Strengths and limitations

**Strengths**
- Declarative queries independent of the physical storage (Codd, 1970).
- Powerful analytics with aggregates, window functions and CTEs (PostgreSQL window functions; PostgreSQL CTEs).
- Indexes make selective queries fast (PostgreSQL indexes).

**Limitations**
- Indexes add overhead to every insert, update and delete (PostgreSQL indexes).
- Database products extend the SQL standard differently, so queries are not always portable (PostgreSQL SQL tutorial).
- Multi-step relationship queries need many joins or recursive CTEs (PostgreSQL CTEs).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| GROUP BY aggregate | Collapses rows into one row per group (PostgreSQL SQL tutorial) | Summaries per group |
| Window function | Computes across related rows, keeps each row (PostgreSQL window functions) | Rankings, running totals, shares |
| CTE | Named intermediate result for one query (PostgreSQL CTEs) | Readable multi-step queries, recursion |
| SPARQL / Cypher | Graph pattern matching ([[sparql|SPARQL]]) | Highly connected data |

### In practice

Queries are written step by step with CTEs and checked on small samples; frequently filtered or joined columns get indexes (PostgreSQL indexes), and query plans are inspected with EXPLAIN. Coding interviews often test joins, GROUP BY with HAVING, window functions such as ROW_NUMBER for "top n per group", and correct NULL handling (PostgreSQL SQL tutorial; PostgreSQL window functions).

### Key takeaway

SQL queries relational tables declaratively; joins, aggregates, window functions and CTEs cover most analytical needs, and indexes make them fast.

### Sources

- Codd, E. F. (1970). *A relational model of data for large shared data banks.* Communications of the ACM 13(6). [doi:10.1145/362384.362685](https://doi.org/10.1145/362384.362685)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, Chapter 2: The SQL Language.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-sql-intro.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 3.5: Window Functions.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-window.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 7.8: WITH Queries (Common Table Expressions).* [postgresql.org](https://www.postgresql.org/docs/current/queries-with.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 11.1: Indexes, Introduction.* [postgresql.org](https://www.postgresql.org/docs/current/indexes-intro.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

SQL ist die Sprache relationaler Datenbanken, die Daten auf Basis des relationalen Modells in Tabellen aus Zeilen und Spalten speichern (Codd, 1970). Es liest Daten mit SELECT, verbindet Tabellen mit Joins, fasst mit Aggregaten und GROUP BY zusammen und ändert Daten mit INSERT, UPDATE und DELETE (PostgreSQL SQL tutorial). Fensterfunktionen berechnen Werte über zusammengehörige Zeilen, ohne sie zusammenzufassen (PostgreSQL window functions), Common Table Expressions strukturieren komplexe Abfragen (PostgreSQL CTEs), und Indizes beschleunigen Abfragen auf Kosten zusätzlichen Schreibaufwands (PostgreSQL indexes).

### Kernkonzepte

- **Relationales Modell:** Daten sind als Relationen (Tabellen) organisiert, und Anwendungen sind unabhängig davon, wie die Daten intern gespeichert werden (Codd, 1970).
- **Abfragen:** SELECT ... FROM ... WHERE ... ORDER BY liest Zeilen; WHERE filtert Zeilen vor der Aggregation, HAVING filtert Gruppen danach (PostgreSQL SQL tutorial).
- **Joins:** Inner Joins liefern zusammenpassende Zeilen; Left, Right und Full Outer Joins behalten auch Zeilen ohne Partner und füllen fehlende Spalten mit NULL (PostgreSQL SQL tutorial).
- **Aggregate:** count, sum, avg, max und min berechnen ein Ergebnis aus vielen Zeilen, gruppiert mit GROUP BY (PostgreSQL SQL tutorial).
- **Fensterfunktionen:** OVER (PARTITION BY ... ORDER BY ...) berechnet Ränge, laufende Summen oder Mittelwerte über zusammengehörige Zeilen, wobei jede Zeile erhalten bleibt (PostgreSQL window functions).
- **CTEs:** WITH definiert benannte Hilfsabfragen, die für eine Abfrage wie temporäre Tabellen wirken; WITH RECURSIVE durchläuft Hierarchien (PostgreSQL CTEs).
- **Indizes:** CREATE INDEX vermeidet vollständige Tabellenscans bei selektiven Abfragen, muss aber bei jedem Schreibvorgang mitgepflegt werden (PostgreSQL indexes).

### Typische Verwendung

```sql
-- Entscheidungen je Gericht mit ihrem Anteil an allen Entscheidungen
WITH counts AS (
    SELECT court, COUNT(*) AS n
    FROM decisions
    WHERE year >= 2020
    GROUP BY court
    HAVING COUNT(*) > 10
)
SELECT court, n,
       ROUND(100.0 * n / SUM(n) OVER (), 1) AS share_pct,
       RANK() OVER (ORDER BY n DESC)         AS rank
FROM counts
ORDER BY rank;

-- auch Entscheidungen ohne zitierte Norm behalten (LEFT JOIN)
SELECT d.id, c.norm_id
FROM decisions d
LEFT JOIN citations c ON c.decision_id = d.id;

CREATE INDEX idx_citations_decision ON citations (decision_id);
```

NULL steht für fehlende Werte und wird mit IS NULL statt mit einem Gleichheitszeichen geprüft; COALESCE ersetzt NULL durch einen Standardwert. CASE WHEN drückt bedingte Logik innerhalb von Abfragen aus.

### Wann einsetzen

- Für strukturierte, tabellarische Daten mit stabilem Schema und transaktionalen Aktualisierungen (Codd, 1970).
- Für Berichte und Analysen mit Gruppierung, Rangfolgen und laufenden Summen (PostgreSQL window functions).
- Wenn Daten stark vernetzt sind und Abfragen vielen Beziehungen folgen, können Graphdatenbanken einfacher sein ([[graph-databases|Graphdatenbanken]]).

### Stärken und Grenzen

**Stärken**
- Deklarative Abfragen unabhängig von der physischen Speicherung (Codd, 1970).
- Leistungsfähige Analysen mit Aggregaten, Fensterfunktionen und CTEs (PostgreSQL window functions; PostgreSQL CTEs).
- Indizes machen selektive Abfragen schnell (PostgreSQL indexes).

**Einschränkungen**
- Indizes verursachen zusätzlichen Aufwand bei jedem Einfügen, Ändern und Löschen (PostgreSQL indexes).
- Datenbankprodukte erweitern den SQL-Standard unterschiedlich, sodass Abfragen nicht immer übertragbar sind (PostgreSQL SQL tutorial).
- Abfragen über mehrere Beziehungen hinweg brauchen viele Joins oder rekursive CTEs (PostgreSQL CTEs).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Aggregat mit GROUP BY | Fasst Zeilen zu einer Zeile je Gruppe zusammen (PostgreSQL SQL tutorial) | Zusammenfassungen je Gruppe |
| Fensterfunktion | Rechnet über zusammengehörige Zeilen, behält jede Zeile (PostgreSQL window functions) | Rangfolgen, laufende Summen, Anteile |
| CTE | Benanntes Zwischenergebnis für eine Abfrage (PostgreSQL CTEs) | Lesbare mehrstufige Abfragen, Rekursion |
| SPARQL / Cypher | Abgleich von Graphmustern ([[sparql|SPARQL]]) | Stark vernetzte Daten |

### In der Praxis

Abfragen werden Schritt für Schritt mit CTEs aufgebaut und an kleinen Stichproben geprüft; häufig gefilterte oder verknüpfte Spalten erhalten Indizes (PostgreSQL indexes), und Ausführungspläne werden mit EXPLAIN untersucht. In Coding-Interviews werden oft Joins, GROUP BY mit HAVING, Fensterfunktionen wie ROW_NUMBER für „Top n je Gruppe“ und der korrekte Umgang mit NULL geprüft (PostgreSQL SQL tutorial; PostgreSQL window functions).

### Merksatz

SQL fragt relationale Tabellen deklarativ ab; Joins, Aggregate, Fensterfunktionen und CTEs decken die meisten Analyseaufgaben ab, und Indizes machen sie schnell.

### Quellen

- Codd, E. F. (1970). *A relational model of data for large shared data banks.* Communications of the ACM 13(6). [doi:10.1145/362384.362685](https://doi.org/10.1145/362384.362685)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, Chapter 2: The SQL Language.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-sql-intro.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 3.5: Window Functions.* [postgresql.org](https://www.postgresql.org/docs/current/tutorial-window.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 7.8: WITH Queries (Common Table Expressions).* [postgresql.org](https://www.postgresql.org/docs/current/queries-with.html)
- PostgreSQL Global Development Group. *PostgreSQL Documentation, 11.1: Indexes, Introduction.* [postgresql.org](https://www.postgresql.org/docs/current/indexes-intro.html)
