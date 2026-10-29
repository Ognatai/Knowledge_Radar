---
title_en: Matei Zaharia
title_de: Matei Zaharia
entity_type: Person
aliases:
- Matei Zaharia
sources:
- https://people.eecs.berkeley.edu/~matei/
- https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia
- https://arxiv.org/abs/2004.12832
- https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong. It covers only Matei Zaharia's public, professional work.

### TL;DR

Matei Zaharia is an associate professor of electrical engineering and computer sciences at UC Berkeley, working on computer systems and AI in the Sky Lab, and co-founder and CTO of [[databricks|Databricks]] (Zaharia, n.d.). During his PhD he started [[apache-spark|Apache Spark]], whose resilient distributed datasets (RDDs) made in-memory cluster computing fault-tolerant (Zaharia, n.d.; Zaharia et al., 2012). At Databricks he helped develop [[mlflow|MLflow]] and Delta Lake, and he co-authored the [[data-lakehouse|lakehouse]] paper (Zaharia, n.d.; Armbrust et al., 2021). His group's work on AI includes the retrieval model [[colbert|ColBERT]], the DSPy framework for LLM programs and the prompt optimiser GEPA (Zaharia, n.d.; Khattab & Zaharia, 2020). He received the ACM Prize in Computing in 2025 (Zaharia, n.d.).

### Key facts

| | |
|---|---|
| Position | Associate Professor of EECS, UC Berkeley (Sky Lab) |
| Company | co-founder and CTO of Databricks |
| Research interests | computer systems for large-scale workloads such as AI, data analytics and cloud computing; security and privacy |
| Selected awards | ACM Prize in Computing (2025); SIGMOD Systems Award for Apache Spark (2022); PECASE (2019); ACM Doctoral Dissertation Award (2014) |
| Service | General Chair of MLSys 2025; General Co-Chair of ACM CAIS 2026 |

Source: Zaharia (n.d.).

### Career

Zaharia started Apache Spark during his PhD and co-started other datacenter software such as Apache Mesos and Spark Streaming; his dissertation received the ACM Doctoral Dissertation Award in 2014 (Zaharia, n.d.). On the 2021 lakehouse paper he was affiliated with Databricks and Stanford University (Armbrust et al., 2021). He is now an associate professor at UC Berkeley and co-founder and CTO of Databricks, where he helped develop MLflow and Delta Lake (Zaharia, n.d.).

### Key contributions

#### Apache Spark and RDDs

The RDD paper introduced resilient distributed datasets, read-only, partitioned collections created by deterministic operations, which recover lost partitions from their lineage instead of replicating data (Zaharia et al., 2012; [[apache-spark|Apache Spark]]). Spark received the SIGMOD Systems Award in 2022, and Zaharia lists best paper awards at NSDI 2012 and SIGCOMM 2012 (Zaharia, n.d.). Zaharia describes Spark as "now one of the most widely used frameworks for distributed data processing" (Zaharia, n.d.).

#### Lakehouse and Databricks platform

With colleagues at Databricks, Zaharia argued that the lakehouse, based on open direct-access data formats such as Apache Parquet, with first-class support for machine learning and data science and state-of-the-art performance, would replace the classic [[data-warehouse|data warehouse]] architecture (Armbrust et al., 2021; [[data-lakehouse|data lakehouse]]). He helped develop MLflow and Delta Lake (Zaharia, n.d.).

#### Retrieval and LLM programs

With Omar Khattab he introduced ColBERT, which encodes queries and documents separately with [[bert|BERT]] and scores them by "late interaction", the sum over query tokens of the maximum similarity to any document token (Khattab & Zaharia, 2020; [[colbert|ColBERT]]). His group's recent software includes DSPy for LLM programs, GEPA for optimising prompts, code and text parameters, and LOTUS for semantic queries (Zaharia, n.d.).

### Key works

| Year | Work | Co-authors |
|---|---|---|
| 2012 | *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing* (NSDI) | Chowdhury, Das, Dave, Ma, McCauley, Franklin, Shenker, Stoica |
| 2020 | *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT* (SIGIR) | Khattab |
| 2021 | *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics* (CIDR) | Armbrust, Ghodsi, Xin |

Sources: Zaharia et al. (2012); Khattab & Zaharia (2020); Armbrust et al. (2021).

### Relevance for AI development

Spark and the lakehouse are common foundations for preparing training data and features at scale ([[apache-spark|Apache Spark]], [[data-lakehouse|data lakehouse]]); MLflow and Delta Lake, which he helped develop, are parts of the Databricks platform for ML workflows (Zaharia, n.d.; [[databricks|Databricks]]). ColBERT can serve as the retriever in [[retrieval-augmented-generation|retrieval-augmented generation]], and DSPy and GEPA treat prompts as parameters to be optimised rather than written by hand (Zaharia, n.d.; [[colbert|ColBERT]]).

### Sources

- Zaharia, M. (n.d.). *Matei Zaharia's Homepage*. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~matei/)
- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Armbrust, M., Ghodsi, A., Xin, R. & Zaharia, M. (2021). *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics.* CIDR 2021. [cidrdb.org](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein. Sie behandelt nur die öffentliche, berufliche Arbeit von Matei Zaharia.

### TL;DR

Matei Zaharia ist Associate Professor für Elektrotechnik und Informatik an der UC Berkeley, wo er im Sky Lab zu Computersystemen und KI forscht, und Mitgründer und CTO von [[databricks|Databricks]] (Zaharia, n.d.). Während seiner Promotion startete er [[apache-spark|Apache Spark]], dessen Resilient Distributed Datasets (RDDs) In-Memory-Berechnungen auf Clustern fehlertolerant machten (Zaharia, n.d.; Zaharia et al., 2012). Bei Databricks wirkte er an der Entwicklung von [[mlflow|MLflow]] und Delta Lake mit und ist Mitautor des Papers zum [[data-lakehouse|Lakehouse]] (Zaharia, n.d.; Armbrust et al., 2021). Zu den KI-Arbeiten seiner Gruppe gehören das Retrieval-Modell [[colbert|ColBERT]], das Framework DSPy für LLM-Programme und der Prompt-Optimierer GEPA (Zaharia, n.d.; Khattab & Zaharia, 2020). 2025 erhielt er den ACM Prize in Computing (Zaharia, n.d.).

### Eckdaten

| | |
|---|---|
| Position | Associate Professor of EECS, UC Berkeley (Sky Lab) |
| Unternehmen | Mitgründer und CTO von Databricks |
| Forschungsinteressen | Computersysteme für große Arbeitslasten wie KI, Datenanalyse und Cloud Computing; Sicherheit und Privatsphäre |
| Ausgewählte Auszeichnungen | ACM Prize in Computing (2025); SIGMOD Systems Award für Apache Spark (2022); PECASE (2019); ACM Doctoral Dissertation Award (2014) |
| Ehrenämter | General Chair der MLSys 2025; General Co-Chair der ACM CAIS 2026 |

Quelle: Zaharia (n.d.).

### Werdegang

Zaharia startete Apache Spark während seiner Promotion und initiierte weitere Rechenzentrumssoftware wie Apache Mesos und Spark Streaming mit; seine Dissertation erhielt 2014 den ACM Doctoral Dissertation Award (Zaharia, n.d.). Im Lakehouse-Paper von 2021 war er Databricks und der Stanford University zugeordnet (Armbrust et al., 2021). Heute ist er Associate Professor an der UC Berkeley sowie Mitgründer und CTO von Databricks, wo er an der Entwicklung von MLflow und Delta Lake mitwirkte (Zaharia, n.d.).

### Wichtige Beiträge

#### Apache Spark und RDDs

Das RDD-Paper führte Resilient Distributed Datasets ein, schreibgeschützte, partitionierte Sammlungen, die durch deterministische Operationen entstehen und verlorene Partitionen aus ihrer Lineage wiederherstellen, statt Daten zu replizieren (Zaharia et al., 2012; [[apache-spark|Apache Spark]]). Spark erhielt 2022 den SIGMOD Systems Award, und Zaharia nennt Best Paper Awards auf der NSDI 2012 und der SIGCOMM 2012 (Zaharia, n.d.). Zaharia beschreibt Spark als „now one of the most widely used frameworks for distributed data processing“ (Zaharia, n.d.).

#### Lakehouse und Databricks-Plattform

Mit Kollegen bei Databricks vertrat Zaharia die These, dass das Lakehouse, gestützt auf offene, direkt zugängliche Datenformate wie Apache Parquet, mit vollwertiger Unterstützung für maschinelles Lernen und Data Science und mit hoher Leistung, die klassische Data-Warehouse-Architektur ablösen werde (Armbrust et al., 2021; [[data-lakehouse|Data Lakehouse]]). Er wirkte an der Entwicklung von MLflow und Delta Lake mit (Zaharia, n.d.).

#### Retrieval und LLM-Programme

Mit Omar Khattab stellte er ColBERT vor, das Anfragen und Dokumente getrennt mit [[bert|BERT]] kodiert und sie per „Late Interaction“ bewertet, der Summe über die Anfrage-Tokens der maximalen Ähnlichkeit zu einem Dokument-Token (Khattab & Zaharia, 2020; [[colbert|ColBERT]]). Zu den neueren Werkzeugen seiner Gruppe gehören DSPy für LLM-Programme, GEPA zur Optimierung von Prompts, Code und Textparametern sowie LOTUS für semantische Abfragen (Zaharia, n.d.).

### Wichtige Werke

| Jahr | Werk | Mitautoren |
|---|---|---|
| 2012 | *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing* (NSDI) | Chowdhury, Das, Dave, Ma, McCauley, Franklin, Shenker, Stoica |
| 2020 | *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT* (SIGIR) | Khattab |
| 2021 | *Lakehouse: A New Generation of Open Platforms that Unify [[data-warehouse\|Data Warehousing]] and Advanced Analytics* (CIDR) | Armbrust, Ghodsi, Xin |

Quellen: Zaharia et al. (2012); Khattab & Zaharia (2020); Armbrust et al. (2021).

### Bedeutung für die KI-Entwicklung

Spark und das Lakehouse sind verbreitete Grundlagen, um Trainingsdaten und Features in großem Maßstab aufzubereiten ([[apache-spark|Apache Spark]], [[data-lakehouse|Data Lakehouse]]); MLflow und Delta Lake, an denen er mitwirkte, sind Teile der Databricks-Plattform für ML-Workflows (Zaharia, n.d.; [[databricks|Databricks]]). ColBERT kann als Retriever für [[retrieval-augmented-generation|Retrieval-Augmented Generation]] dienen, und DSPy und GEPA behandeln Prompts als zu optimierende Parameter statt als handgeschriebene Texte (Zaharia, n.d.; [[colbert|ColBERT]]).

### Quellen

- Zaharia, M. (n.d.). *Matei Zaharia's Homepage*. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~matei/)
- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)
- Khattab, O. & Zaharia, M. (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR 2020. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)
- Armbrust, M., Ghodsi, A., Xin, R. & Zaharia, M. (2021). *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics.* CIDR 2021. [cidrdb.org](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf)
