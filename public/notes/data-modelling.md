---
title_en: Data Modelling
title_de: Datenmodellierung
entity_type: Method
aliases:
- Data modelling
- Data modeling
- Dimensional modelling
- Dimensional modeling
- Star schema
- Slowly changing dimension
- Datenmodellierung
sources:
- https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Data modelling decides how the information of a domain is structured into tables, keys and relationships so that it can be stored consistently and queried efficiently. Two styles dominate. For operational systems, the relational model with normalisation stores each fact once and avoids redundancy and inconsistency, as proposed by Codd (1970). For analytics, dimensional modelling, introduced to data warehousing by Ralph Kimball in 1996, organises data into fact tables of numeric measurements surrounded by descriptive dimension tables, usually as a star schema, and tracks history with slowly changing dimensions (Kimball Group). In a lakehouse, the gold layer is typically modelled dimensionally ([[data-lakehouse|data lakehouse]]).

### How it works

```text
business questions and source data
 ▼
operational model (normalised): entities → relations with keys → normal form
 ▼
analytical model (dimensional):
  1. select the business process
  2. declare the grain (what one fact row means)
  3. identify the dimensions (who, what, where, when, how)
  4. identify the facts (numeric measurements)
 ▼
star schema: fact table + dimension tables, joined by surrogate keys
 ▼
history: slowly changing dimensions (type 1 overwrite, type 2 new row, …)
```

#### 1. The relational model and normalisation

Codd (1970) proposed representing data as n-ary relations so that users and programs are protected from the internal representation of the data: applications should remain unaffected when storage changes, which he called data independence. The relational view also provides "a sound basis for treating derivability, redundancy, and consistency of relations" (Codd, 1970). Normalisation removes non-simple domains, that is, attributes that themselves contain relations: in Codd's example, an employee relation with nested job history and children is split into separate relations for employees, job history, salary history and children, each carrying the employee number as part of its key (Codd, 1970). Querying normalised data is covered in [[sql|SQL]].

#### 2. The four-step dimensional design process

Dimensional models answer analytical questions. Kimball's design process makes four decisions: "Select the business process", "Declare the grain", which fixes what a single fact row represents, "Identify the dimensions", the descriptive context around the measurements, and "Identify the facts", the numeric measurements (Kimball Group four-step). The answers come from business needs and the realities of the source data, worked out in collaborative modelling sessions with business data governance representatives (Kimball Group four-step); see [[data-governance|data governance]].

#### 3. Facts, dimensions and the star schema

Fact tables hold measurements at the declared grain. Kimball distinguishes additive, semi-additive and non-additive facts and three basic fact table types: transaction, periodic snapshot and accumulating snapshot, plus factless and aggregated fact tables (Kimball Group). Dimension tables carry descriptive attributes and are joined through surrogate keys. In a relational database the result is a star schema: "fact tables linked to associated dimension tables via primary/foreign key relationships"; the same model can be stored as an OLAP cube, usually derived from the star schema and queried with analytic languages such as XMLA (Kimball Group star schema). Normalising dimensions further gives snowflaked dimensions (Kimball Group). Conformed dimensions shared across business processes, documented in an enterprise bus matrix, allow results from different fact tables to be combined (Kimball Group).

#### 4. Slowly changing dimensions

Dimension attributes change, for example a customer's address. Kimball names types 0 to 7 (Kimball Group): type 0 retains the original value, type 1 overwrites it, type 2 adds a new row and type 3 adds a new attribute; types 4 to 7 combine mini-dimensions, outriggers and hybrids. Type 2 "add[s] a new row in the dimension with the updated attribute values": the new row gets a new surrogate key that fact tables use from then on, and at least three columns are added, a row effective date, a row expiration date and a current row indicator (Kimball Group type 2). Type 2 keeps history so that past facts stay linked to the attribute values valid at that time.

#### Origin and variants

Codd published the relational model in 1970 (Codd, 1970); Kimball introduced dimensional modelling to data warehousing in 1996 (Kimball Group). Other styles exist for other needs: graph models for densely connected data ([[graph-databases|graph databases]]), ontologies and knowledge graphs for shared meaning across systems ([[ontology-design|ontology design]], [[knowledge-graphs|knowledge graphs]]), and domain models in requirements work ([[requirements-engineering|requirements engineering]]).

### When to use it

- Normalised models for operational systems with many concurrent updates, where redundancy would cause inconsistency (Codd, 1970).
- Dimensional models for reporting, [[data-visualisation|dashboards]] and BI, where business users slice measurements by descriptive attributes (Kimball Group).
- Type 2 slowly changing dimensions where reports must reflect attribute values as they were at the time of each fact (Kimball Group type 2).

### Strengths and limitations

**Strengths**
- Normalisation keeps each fact in one place, so updates cannot create contradictions (Codd, 1970).
- Star schemas are easy to understand and query: one join from the fact to each dimension (Kimball Group star schema).
- Conformed dimensions make figures from different processes comparable (Kimball Group).

**Limitations**
- Normalised models split data into many relations that analytical queries have to join again (Codd, 1970).
- Dimensional models duplicate descriptive attributes and need ETL logic to load and historise them (Kimball Group type 2).
- The grain has to be declared before dimensions and facts are chosen, which requires agreement on business needs and knowledge of the source data (Kimball Group four-step).

### Comparison

| | Normalised (relational) model | Dimensional model |
|---|---|---|
| Purpose | consistent operational data | analytical queries |
| Structure | many relations, keys, normal forms | fact tables + dimension tables (star schema) |
| Redundancy | avoided | accepted in dimensions |
| History | usually current state | slowly changing dimensions |
| Origin | Codd (1970) | Kimball (1996) |

Sources: Codd (1970); Kimball Group.

### In practice

In a medallion architecture, silver tables are usually close to the source model, while gold tables are dimensional models built for reports and ML features ([[data-lakehouse|data lakehouse]]). The transformation logic lives in [[data-pipelines|data pipelines]]. For web and marketing analytics, events are typically modelled as fact tables at the grain of one event or session ([[web-analytics|web analytics]]).

### Key takeaway

Data modelling structures data for its use: normalised relations keep operational data consistent, and dimensional star schemas with declared grain, conformed dimensions and slowly changing dimensions make analytical data easy to query and historically correct.

### Sources

- Codd, E. F. (1970). *A Relational Model of Data for Large Shared Data Banks.* Communications of the ACM 13(6), 377–387. [seas.upenn.edu](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)
- Kimball Group. *Dimensional Modeling Techniques.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- Kimball Group four-step. *Four-Step Dimensional Design Process.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/)
- Kimball Group star schema. *Star Schemas and OLAP Cubes.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/)
- Kimball Group type 2. *Type 2: Add New Row.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Datenmodellierung legt fest, wie die Informationen einer Domäne in Tabellen, Schlüssel und Beziehungen gegliedert werden, damit sie konsistent gespeichert und effizient abgefragt werden können. Zwei Stile herrschen vor. Für operative Systeme speichert das relationale Modell mit Normalisierung jede Tatsache nur einmal und vermeidet Redundanz und Inkonsistenz, wie von Codd (1970) vorgeschlagen. Für Analysen ordnet die dimensionale Modellierung, 1996 von Ralph Kimball in das Data Warehousing eingeführt, Daten in Faktentabellen mit numerischen Messgrößen und umgebende beschreibende Dimensionstabellen, meist als Sternschema, und bildet Historie mit Slowly Changing Dimensions ab (Kimball Group). In einem Lakehouse wird die Gold-Schicht typischerweise dimensional modelliert ([[data-lakehouse|Data Lakehouse]]).

### Funktionsweise

```text
fachliche Fragen und Quelldaten
 ▼
operatives Modell (normalisiert): Entitäten → Relationen mit Schlüsseln → Normalform
 ▼
analytisches Modell (dimensional):
  1. Geschäftsprozess auswählen
  2. Granularität festlegen (was eine Faktenzeile bedeutet)
  3. Dimensionen bestimmen (wer, was, wo, wann, wie)
  4. Fakten bestimmen (numerische Messgrößen)
 ▼
Sternschema: Faktentabelle + Dimensionstabellen, verbunden über Surrogatschlüssel
 ▼
Historie: Slowly Changing Dimensions (Typ 1 überschreiben, Typ 2 neue Zeile, …)
```

#### 1. Das relationale Modell und Normalisierung

Codd (1970) schlug vor, Daten als n-stellige Relationen darzustellen, damit Nutzende und Programme von der internen Darstellung der Daten abgeschirmt sind: Anwendungen sollen unberührt bleiben, wenn sich die Speicherung ändert, was er Datenunabhängigkeit nannte. Die relationale Sicht bietet außerdem „a sound basis for treating derivability, redundancy, and consistency of relations“ (Codd, 1970). Normalisierung entfernt nicht einfache Domänen, also Attribute, die selbst Relationen enthalten: In Codds Beispiel wird eine Mitarbeiterrelation mit verschachtelter Stellenhistorie und Kindern in getrennte Relationen für Mitarbeitende, Stellenhistorie, Gehaltshistorie und Kinder aufgeteilt, die jeweils die Personalnummer als Teil ihres Schlüssels tragen (Codd, 1970). Das Abfragen normalisierter Daten behandelt [[sql|SQL]].

#### 2. Der vierstufige dimensionale Entwurfsprozess

Dimensionale Modelle beantworten analytische Fragen. Kimballs Entwurfsprozess trifft vier Entscheidungen: „Select the business process“, „Declare the grain“, was festlegt, wofür eine einzelne Faktenzeile steht, „Identify the dimensions“, den beschreibenden Kontext der Messgrößen, und „Identify the facts“, die numerischen Messgrößen (Kimball Group four-step). Die Antworten ergeben sich aus fachlichem Bedarf und der Lage der Quelldaten und werden in gemeinsamen Modellierungssitzungen mit Vertreterinnen und Vertretern der fachlichen Data Governance erarbeitet (Kimball Group four-step); siehe [[data-governance|Data Governance]].

#### 3. Fakten, Dimensionen und das Sternschema

Faktentabellen halten Messgrößen in der festgelegten Granularität. Kimball unterscheidet additive, semiadditive und nicht additive Fakten sowie drei grundlegende Arten von Faktentabellen: Transaktion, periodischer Snapshot und kumulierender Snapshot, dazu faktlose und aggregierte Faktentabellen (Kimball Group). Dimensionstabellen enthalten beschreibende Attribute und werden über Surrogatschlüssel verknüpft. In einer relationalen Datenbank entsteht so ein Sternschema: „fact tables linked to associated dimension tables via primary/foreign key relationships“; dasselbe Modell lässt sich als OLAP-Würfel speichern, meist aus dem Sternschema abgeleitet und mit analytischen Sprachen wie XMLA abgefragt (Kimball Group star schema). Werden Dimensionen weiter normalisiert, entstehen Snowflake-Dimensionen (Kimball Group). Konforme Dimensionen, die mehrere Geschäftsprozesse teilen und in einer Enterprise-Bus-Matrix dokumentiert sind, erlauben es, Ergebnisse verschiedener Faktentabellen zu verbinden (Kimball Group).

#### 4. Slowly Changing Dimensions

Dimensionsattribute ändern sich, etwa die Adresse einer Kundin oder eines Kunden. Kimball nennt die Typen 0 bis 7 (Kimball Group): Typ 0 behält den ursprünglichen Wert, Typ 1 überschreibt ihn, Typ 2 fügt eine neue Zeile hinzu und Typ 3 ein neues Attribut; die Typen 4 bis 7 kombinieren Mini-Dimensionen, Outrigger und Mischformen. Typ 2 fügt „a new row in the dimension with the updated attribute values“ hinzu: Die neue Zeile erhält einen neuen Surrogatschlüssel, den Faktentabellen ab dann verwenden, und es kommen mindestens drei Spalten hinzu, ein Gültigkeitsbeginn, ein Gültigkeitsende und ein Kennzeichen für die aktuelle Zeile (Kimball Group type 2). Typ 2 bewahrt die Historie, sodass vergangene Fakten mit den damals gültigen Attributwerten verknüpft bleiben.

#### Herkunft und Varianten

Codd veröffentlichte das relationale Modell 1970 (Codd, 1970); Kimball führte die dimensionale Modellierung 1996 in das Data Warehousing ein (Kimball Group). Für andere Zwecke gibt es andere Stile: Graphmodelle für dicht vernetzte Daten ([[graph-databases|Graphdatenbanken]]), Ontologien und Knowledge Graphs für gemeinsame Bedeutung über Systeme hinweg ([[ontology-design|Ontologie-Design]], [[knowledge-graphs|Knowledge Graphs]]) und Domänenmodelle in der Anforderungsarbeit ([[requirements-engineering|Requirements Engineering]]).

### Wann einsetzen

- Normalisierte Modelle für operative Systeme mit vielen gleichzeitigen Änderungen, in denen Redundanz zu Inkonsistenz führen würde (Codd, 1970).
- Dimensionale Modelle für Berichte, [[data-visualisation|Dashboards]] und BI, in denen Fachanwenderinnen und -anwender Messgrößen nach beschreibenden Attributen aufschlüsseln (Kimball Group).
- Slowly Changing Dimensions vom Typ 2, wenn Berichte die Attributwerte zum Zeitpunkt jedes Fakts zeigen müssen (Kimball Group type 2).

### Stärken und Grenzen

**Stärken**
- Normalisierung hält jede Tatsache an einer Stelle, sodass Änderungen keine Widersprüche erzeugen (Codd, 1970).
- Sternschemata sind leicht zu verstehen und abzufragen: ein Join vom Fakt zu jeder Dimension (Kimball Group star schema).
- Konforme Dimensionen machen Zahlen aus verschiedenen Prozessen vergleichbar (Kimball Group).

**Grenzen**
- Normalisierte Modelle verteilen Daten auf viele Relationen, die analytische Abfragen wieder verknüpfen müssen (Codd, 1970).
- Dimensionale Modelle duplizieren beschreibende Attribute und brauchen ETL-Logik zum Laden und Historisieren (Kimball Group type 2).
- Die Granularität muss festgelegt werden, bevor Dimensionen und Fakten gewählt werden, was Einigkeit über den fachlichen Bedarf und Kenntnis der Quelldaten erfordert (Kimball Group four-step).

### Vergleich

| | Normalisiertes (relationales) Modell | Dimensionales Modell |
|---|---|---|
| Zweck | konsistente operative Daten | analytische Abfragen |
| Struktur | viele Relationen, Schlüssel, Normalformen | Faktentabellen + Dimensionstabellen (Sternschema) |
| Redundanz | vermieden | in Dimensionen in Kauf genommen |
| Historie | meist aktueller Stand | Slowly Changing Dimensions |
| Herkunft | Codd (1970) | Kimball (1996) |

Quellen: Codd (1970); Kimball Group.

### In der Praxis

In einer Medallion-Architektur liegen Silber-Tabellen meist nah am Quellmodell, während Gold-Tabellen dimensionale Modelle für Berichte und ML-Features sind ([[data-lakehouse|Data Lakehouse]]). Die Transformationslogik liegt in [[data-pipelines|Datenpipelines]]. In Web- und Marketing-Analytics werden Events typischerweise als Faktentabellen mit der Granularität eines Events oder einer Sitzung modelliert ([[web-analytics|Web-Analytics]]).

### Merksatz

Datenmodellierung gliedert Daten nach ihrem Zweck: Normalisierte Relationen halten operative Daten konsistent, und dimensionale Sternschemata mit festgelegter Granularität, konformen Dimensionen und Slowly Changing Dimensions machen analytische Daten leicht abfragbar und historisch korrekt.

### Quellen

- Codd, E. F. (1970). *A Relational Model of Data for Large Shared Data Banks.* Communications of the ACM 13(6), 377–387. [seas.upenn.edu](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)
- Kimball Group. *Dimensional Modeling Techniques.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- Kimball Group four-step. *Four-Step Dimensional Design Process.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/)
- Kimball Group star schema. *Star Schemas and OLAP Cubes.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/)
- Kimball Group type 2. *Type 2: Add New Row.* [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/)
