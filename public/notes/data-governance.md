---
title_en: Data Governance
title_de: Data Governance
entity_type: Concept
aliases:
- Data governance
- Data catalogue
- Data catalog
- Data lineage
- Data quality
- Data product
- Data products
- Data mesh
- Datenqualität
- Datenprodukt
sources:
- https://martinfowler.com/articles/data-mesh-principles.html
- https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework
- https://openlineage.io/docs/
- https://docs.databricks.com/aws/en/data-governance/unity-catalog/
- https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Data governance is the set of roles, rules and tools that decide who owns which data, who may use it, how good it has to be and how its origin can be traced. In practice it rests on a data catalogue that makes data findable and holds its metadata, access control and auditing, measurable data quality, for example along the six dimensions accuracy, completeness, uniqueness, consistency, timeliness and validity (Government Data Quality Hub, 2020), and lineage that records which job turned which input into which output (OpenLineage; Databricks Lineage). Data mesh shifts governance from a central team to the business domains, which publish their analytical data as products, while a federation sets global rules that the platform enforces automatically (Dehghani, 2020).

### How it works

```text
domains own and publish data products (data + metadata + code)
 ▼
catalogue: names, schemas, owners, descriptions, tags, classifications
 ▼
access control and auditing: privileges, row/column filters, audit log
 ▼
quality: rules per dimension, measured along the data lifecycle
 ▼
lineage: run → job → input and output datasets, down to columns
 ▼
consumers discover, understand and use trustworthy data; changes are checked for downstream impact
```

#### 1. Ownership and data products

Dehghani (2020) proposes four principles for analytical data at scale: domain-oriented ownership, data as a product, a self-serve data platform and federated computational governance. "Analytical data provided by the domains must be treated as a product": consumers are customers, and data product owners are accountable for quality and user satisfaction. A data product bundles code (pipelines that transform upstream data, [[apis|APIs]] that serve data, schemas, metrics and metadata, and code that enforces access control and provenance), the data and its metadata (semantics, syntax, quality metrics, policies) and the infrastructure that runs it (Dehghani, 2020). Data users should be able to "easily discover, understand and securely use high quality data" (Dehghani, 2020).

#### 2. Federated computational governance

In a central model, one team owns quality and custodianship, enforcement is manual, and success is measured by the volume of governed tables. In data mesh, a federation of domain and platform representatives defines global interoperability rules, for example how a customer is identified across domains, while domains keep autonomy over their own models; the platform enforces the rules automatically, and success is measured by the connections through which data products are consumed (Dehghani, 2020). Errors are detected and recovered through the platform's automated processing rather than prevented by a central gatekeeper (Dehghani, 2020).

#### 3. Catalogue and access control

A catalogue is the inventory that makes data discoverable. Databricks' Unity Catalog, as an example of a governance layer, organises tables, views, volumes, functions and models in a three-level namespace `catalog.schema.object`; permissions are granted on these securable objects through privileges, attribute-based policies and row and column filters, an audit log records data access, and data classification can tag sensitive data automatically (Databricks). Unity Catalog extends the same governance to AI assets such as models and model services and is also available as open source (Databricks). Platforms of this kind are described in [[data-lakehouse|data lakehouse]].

#### 4. Data quality

The UK Government Data Quality Framework adopts six dimensions defined by DAMA UK (Government Data Quality Hub, 2020):
- **Accuracy:** "the degree to which data matches reality".
- **Completeness:** "the degree to which records are present".
- **Uniqueness:** "the degree to which there is no duplication in records".
- **Consistency:** "the degree to which values in a data set do not contradict other values representing the same entity".
- **Timeliness:** "the degree to which the data is an accurate reflection of the period that they represent", including whether values are current.
- **Validity:** "the degree to which the data is in the range and format expected".

Its five principles are to commit to data quality, know the users and their needs, assess quality throughout the data lifecycle (plan; collect or acquire and ingest; prepare, store and maintain; use and process; share and publish; archive or destroy), communicate quality clearly and anticipate changes that affect it (Government Data Quality Hub, 2020). In pipelines, such rules become automated checks, see [[data-pipelines|data pipelines]] and the data validation step in [[ml-pipelines|ML pipelines]].

#### 5. Lineage

Lineage records where data comes from and what was done to it. OpenLineage is "an open framework for data lineage collection and analysis" whose specification defines a generic model of datasets, jobs and runs, extensible through facets, with integrations for Airflow, [[apache-spark|Spark]], dbt, Flink and others (OpenLineage). Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level where possible, and shows it as a graph that also includes jobs, [[data-visualisation|dashboards]] and model versions; lineage is lost when objects are renamed or when data is referenced by file path instead of table name (Databricks Lineage). Lineage is used for impact analysis before changing or deleting a table or column, for compliance audits that show where regulated data originates, and for debugging by tracing upstream sources (Databricks Lineage).

#### Origin and variants

Zhamak Dehghani first described data mesh in an earlier article on moving beyond a monolithic data lake and set out its principles in 2020 as an alternative to a central data lake or warehouse (Dehghani, 2020). The six DAMA UK dimensions are one widely used set; the framework uses them as a common basis for assessing quality (Government Data Quality Hub, 2020). Lineage standards such as OpenLineage make metadata portable across tools (OpenLineage).

### When to use it

- Many teams produce and consume data, and nobody can say who owns a table or whether it can be trusted (Dehghani, 2020).
- Regulated data must be traceable from source to report, as in risk data aggregation for banks ([[bcbs-239-and-ecb-rdarr-guide|BCBS 239]]) or personal data under the [[gdpr|GDPR]].
- ML and LLM applications are built on internal data, where the quality and permissions of the training or retrieval data determine the result (Databricks).

### Strengths and limitations

**Strengths**
- Findable, documented data reduces duplicated work and makes data products reusable (Dehghani, 2020).
- Quality dimensions turn vague complaints into measurable rules (Government Data Quality Hub, 2020).
- Lineage makes the downstream impact of a change visible before it is made (Databricks Lineage).

**Limitations**
- Data mesh requires domain teams with data skills and a mature self-serve platform; Dehghani (2020) describes principles, not a technology.
- Automated lineage has gaps, for example for renamed objects or access by file path (Databricks Lineage).
- Quality dimensions must be weighted per use; a valid value can still be inaccurate (Government Data Quality Hub, 2020).

### Comparison

| | Central data governance | Data mesh |
|---|---|---|
| Ownership | central data team | business domains |
| Quality | defined and owned centrally | modelled by federated teams |
| Enforcement | manual, by people | automated by the platform |
| Error handling | prevent errors | detect and recover automatically |
| Success measure | volume of governed tables | consumption connections across the mesh |

Source: Dehghani (2020). The legal framework for sharing data is covered in the [[data-governance-act|Data Governance Act]] and the [[data-act|Data Act]], which, despite the name, regulate data intermediaries and data access rather than an organisation's internal governance.

### In practice

Metadata, ownership and quality rules are maintained in the catalogue next to the data, not in separate documents, so that consumers find them where they search (Databricks). For RAG systems, document-level permissions and freshness decide whether an answer may use a source; see [[retrieval-augmented-generation|retrieval-augmented generation]]. For training data, documentation practices such as datasheets and the data requirements of the [[eu-ai-act|EU AI Act]] build on the same metadata.

### Regulatory context

The [[eu-ai-act|EU AI Act]] requires data governance for training, validation and test data of high-risk AI systems. [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] sets principles for the accuracy, completeness and timeliness of risk data in banks. The [[gdpr|GDPR]] requires knowing where personal data is processed, which lineage and classification support.

### Key takeaway

Data governance makes data owned, findable, permissioned, measurably good and traceable; data mesh distributes this work to domains that publish data products under global rules enforced by the platform.

### Sources

- Dehghani, Z. (2020). *Data Mesh Principles and Logical Architecture.* martinfowler.com, 3 December 2020. [martinfowler.com](https://martinfowler.com/articles/data-mesh-principles.html)
- Government Data Quality Hub (2020). *The Government Data Quality Framework.* GOV.UK, 3 December 2020. [gov.uk](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework)
- OpenLineage. *About OpenLineage.* [openlineage.io](https://openlineage.io/docs/)
- Databricks. *What is Unity Catalog?* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- Databricks Lineage. *View data lineage using Unity Catalog.* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Data Governance ist die Gesamtheit aus Rollen, Regeln und Werkzeugen, die festlegt, wem welche Daten gehören, wer sie nutzen darf, wie gut sie sein müssen und wie sich ihre Herkunft nachvollziehen lässt. In der Praxis stützt sie sich auf einen Datenkatalog, der Daten auffindbar macht und ihre Metadaten hält, auf Zugriffskontrolle und Protokollierung, auf messbare Datenqualität, etwa entlang der sechs Dimensionen Genauigkeit, Vollständigkeit, Eindeutigkeit, Konsistenz, Aktualität und Gültigkeit (Government Data Quality Hub, 2020), und auf Lineage, die festhält, welcher Job welche Eingabe in welche Ausgabe verwandelt hat (OpenLineage; Databricks Lineage). Data Mesh verlagert Governance von einem zentralen Team in die Fachdomänen, die ihre analytischen Daten als Produkte veröffentlichen, während ein Verbund globale Regeln festlegt, die die Plattform automatisch durchsetzt (Dehghani, 2020).

### Funktionsweise

```text
Domänen besitzen und veröffentlichen Datenprodukte (Daten + Metadaten + Code)
 ▼
Katalog: Namen, Schemata, Verantwortliche, Beschreibungen, Tags, Klassifikationen
 ▼
Zugriffskontrolle und Protokollierung: Rechte, Zeilen-/Spaltenfilter, Audit-Log
 ▼
Qualität: Regeln je Dimension, gemessen über den Datenlebenszyklus
 ▼
Lineage: Lauf → Job → Eingabe- und Ausgabedatensätze, bis auf Spaltenebene
 ▼
Nutzende finden, verstehen und nutzen vertrauenswürdige Daten; Änderungen werden auf ihre Folgen geprüft
```

#### 1. Verantwortung und Datenprodukte

Dehghani (2020) schlägt vier Prinzipien für analytische Daten im großen Maßstab vor: domänenorientierte Verantwortung, Daten als Produkt, eine Self-Service-Datenplattform und föderierte, automatisierte Governance. „Analytical data provided by the domains must be treated as a product“: Nutzende sind Kundschaft, und Verantwortliche für Datenprodukte stehen für Qualität und Zufriedenheit ein. Ein Datenprodukt bündelt Code (Pipelines, die vorgelagerte Daten umwandeln, [[apis|APIs]], die Daten, Schemata, Metriken und Metadaten bereitstellen, und Code, der Zugriffskontrolle und Herkunftsnachweis durchsetzt), die Daten samt Metadaten (Semantik, Syntax, Qualitätsmetriken, Richtlinien) und die Infrastruktur, die es betreibt (Dehghani, 2020). Datennutzende sollen „easily discover, understand and securely use high quality data“ können (Dehghani, 2020).

#### 2. Föderierte, automatisierte Governance

Im zentralen Modell verantwortet ein Team Qualität und Verwahrung, die Durchsetzung erfolgt manuell, und Erfolg wird an der Menge verwalteter Tabellen gemessen. Im Data Mesh legt ein Verbund aus Vertreterinnen und Vertretern der Domänen und der Plattform globale Regeln für die Interoperabilität fest, etwa wie eine Kundin oder ein Kunde domänenübergreifend identifiziert wird, während die Domänen über ihre eigenen Modelle selbst entscheiden; die Plattform setzt die Regeln automatisch durch, und Erfolg wird an den Verbindungen gemessen, über die Datenprodukte genutzt werden (Dehghani, 2020). Fehler werden durch die automatisierte Verarbeitung der Plattform erkannt und behoben, statt von einer zentralen Kontrollinstanz verhindert zu werden (Dehghani, 2020).

#### 3. Katalog und Zugriffskontrolle

Ein Katalog ist das Verzeichnis, das Daten auffindbar macht. Unity Catalog von Databricks, als Beispiel für eine Governance-Schicht, ordnet Tabellen, Views, Volumes, Funktionen und Modelle in einem dreistufigen Namensraum `catalog.schema.object`; Rechte auf diese Objekte werden über Privilegien, attributbasierte Richtlinien sowie Zeilen- und Spaltenfilter vergeben, ein Audit-Log hält Datenzugriffe fest, und eine Datenklassifikation kann sensible Daten automatisch markieren (Databricks). Unity Catalog überträgt dieselbe Governance auf KI-Bestandteile wie Modelle und Modelldienste und ist auch als Open Source verfügbar (Databricks). Plattformen dieser Art beschreibt [[data-lakehouse|Data Lakehouse]].

#### 4. Datenqualität

Das Data Quality Framework der britischen Regierung übernimmt sechs von DAMA UK definierte Dimensionen (Government Data Quality Hub, 2020):
- **Genauigkeit (Accuracy):** „the degree to which data matches reality“.
- **Vollständigkeit (Completeness):** „the degree to which records are present“.
- **Eindeutigkeit (Uniqueness):** „the degree to which there is no duplication in records“.
- **Konsistenz (Consistency):** „the degree to which values in a data set do not contradict other values representing the same entity“.
- **Aktualität (Timeliness):** „the degree to which the data is an accurate reflection of the period that they represent“, einschließlich der Frage, ob Werte aktuell sind.
- **Gültigkeit (Validity):** „the degree to which the data is in the range and format expected“.

Seine fünf Prinzipien lauten: sich zur Datenqualität verpflichten, die Nutzenden und ihre Bedürfnisse kennen, die Qualität über den gesamten Datenlebenszyklus prüfen (planen; erheben oder beschaffen und aufnehmen; aufbereiten, speichern und pflegen; nutzen und verarbeiten; teilen und veröffentlichen; archivieren oder vernichten), Qualität klar kommunizieren und Veränderungen vorhersehen, die sie beeinflussen (Government Data Quality Hub, 2020). In Pipelines werden solche Regeln zu automatisierten Prüfungen, siehe [[data-pipelines|Datenpipelines]] und den Schritt der Datenvalidierung in [[ml-pipelines|ML-Pipelines]].

#### 5. Lineage

Lineage hält fest, woher Daten stammen und was mit ihnen geschehen ist. OpenLineage ist „an open framework for data lineage collection and analysis“, dessen Spezifikation ein allgemeines Modell aus Datensätzen, Jobs und Läufen definiert, erweiterbar über Facets, mit Integrationen für Airflow, [[apache-spark|Spark]], dbt, Flink und andere (OpenLineage). Unity Catalog erfasst Lineage automatisch für Abfragen auf Databricks, wo möglich bis auf Spaltenebene, und zeigt sie als Graph, der auch Jobs, [[data-visualisation|Dashboards]] und Modellversionen enthält; Lineage geht verloren, wenn Objekte umbenannt werden oder Daten über einen Dateipfad statt über einen Tabellennamen angesprochen werden (Databricks Lineage). Lineage dient der Folgenabschätzung, bevor eine Tabelle oder Spalte geändert oder gelöscht wird, Compliance-Prüfungen, die zeigen, woher regulierte Daten stammen, und der Fehlersuche durch Rückverfolgung vorgelagerter Quellen (Databricks Lineage).

#### Herkunft und Varianten

Zhamak Dehghani beschrieb Data Mesh zuerst in einem früheren Artikel über die Abkehr vom monolithischen Data Lake und legte die Prinzipien 2020 als Alternative zu einem zentralen Data Lake oder [[data-warehouse|Data Warehouse]] dar (Dehghani, 2020). Die sechs Dimensionen von DAMA UK sind eine verbreitete Auswahl; das Rahmenwerk nutzt sie als gemeinsame Grundlage zur Bewertung der Qualität (Government Data Quality Hub, 2020). Lineage-Standards wie OpenLineage machen Metadaten zwischen Werkzeugen übertragbar (OpenLineage).

### Wann einsetzen

- Viele Teams erzeugen und nutzen Daten, und niemand kann sagen, wem eine Tabelle gehört oder ob man ihr trauen kann (Dehghani, 2020).
- Regulierte Daten müssen von der Quelle bis zum Bericht nachvollziehbar sein, etwa bei der Aggregation von Risikodaten in Banken ([[bcbs-239-and-ecb-rdarr-guide|BCBS 239]]) oder bei personenbezogenen Daten nach der [[gdpr|DSGVO]].
- ML- und LLM-Anwendungen bauen auf internen Daten auf, deren Qualität und Berechtigungen für Training oder Retrieval das Ergebnis bestimmen (Databricks).

### Stärken und Grenzen

**Stärken**
- Auffindbare, dokumentierte Daten vermeiden doppelte Arbeit und machen Datenprodukte wiederverwendbar (Dehghani, 2020).
- Qualitätsdimensionen machen aus vagen Beschwerden messbare Regeln (Government Data Quality Hub, 2020).
- Lineage zeigt die Folgen einer Änderung, bevor sie vorgenommen wird (Databricks Lineage).

**Grenzen**
- Data Mesh setzt Domänenteams mit Datenkompetenz und eine ausgereifte Self-Service-Plattform voraus; Dehghani (2020) beschreibt Prinzipien, keine Technologie.
- Automatisierte Lineage hat Lücken, etwa bei umbenannten Objekten oder Zugriff über Dateipfade (Databricks Lineage).
- Qualitätsdimensionen müssen je Verwendung gewichtet werden; ein gültiger Wert kann trotzdem ungenau sein (Government Data Quality Hub, 2020).

### Vergleich

| | Zentrale Data Governance | Data Mesh |
|---|---|---|
| Verantwortung | zentrales Datenteam | Fachdomänen |
| Qualität | zentral festgelegt und verantwortet | von föderierten Teams modelliert |
| Durchsetzung | manuell, durch Menschen | automatisiert durch die Plattform |
| Umgang mit Fehlern | Fehler verhindern | automatisch erkennen und beheben |
| Erfolgsmaß | Menge verwalteter Tabellen | Nutzungsverbindungen im Mesh |

Quelle: Dehghani (2020). Den rechtlichen Rahmen für das Teilen von Daten behandeln der [[data-governance-act|Data Governance Act]] und der [[data-act|Data Act]], die trotz des Namens Datenvermittler und Datenzugang regeln, nicht die interne Governance einer Organisation.

### In der Praxis

Metadaten, Verantwortlichkeiten und Qualitätsregeln werden im Katalog neben den Daten gepflegt, nicht in separaten Dokumenten, damit Nutzende sie dort finden, wo sie suchen (Databricks). Bei RAG-Systemen entscheiden Berechtigungen auf Dokumentebene und Aktualität, ob eine Antwort eine Quelle verwenden darf; siehe [[retrieval-augmented-generation|Retrieval-Augmented Generation]]. Für Trainingsdaten bauen Dokumentationspraktiken wie Datasheets und die Datenanforderungen des [[eu-ai-act|EU AI Act]] auf denselben Metadaten auf.

### Regulatorischer Kontext

Der [[eu-ai-act|EU AI Act]] verlangt Data Governance für Trainings-, Validierungs- und Testdaten von Hochrisiko-KI-Systemen. [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] legt Grundsätze für Genauigkeit, Vollständigkeit und Aktualität von Risikodaten in Banken fest. Die [[gdpr|DSGVO]] verlangt zu wissen, wo personenbezogene Daten verarbeitet werden, wobei Lineage und Klassifikation helfen.

### Merksatz

Data Governance macht Daten verantwortet, auffindbar, berechtigt, messbar gut und nachvollziehbar; Data Mesh verteilt diese Arbeit auf Domänen, die Datenprodukte unter globalen, von der Plattform durchgesetzten Regeln veröffentlichen.

### Quellen

- Dehghani, Z. (2020). *Data Mesh Principles and Logical Architecture.* martinfowler.com, 3. Dezember 2020. [martinfowler.com](https://martinfowler.com/articles/data-mesh-principles.html)
- Government Data Quality Hub (2020). *The Government Data Quality Framework.* GOV.UK, 3. Dezember 2020. [gov.uk](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework)
- OpenLineage. *About OpenLineage.* [openlineage.io](https://openlineage.io/docs/)
- Databricks. *What is Unity Catalog?* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- Databricks Lineage. *View data lineage using Unity Catalog.* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage)
