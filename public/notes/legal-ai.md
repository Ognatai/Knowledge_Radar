---
title_en: Legal AI
title_de: Legal AI
entity_type: Concept
sources:
- https://arxiv.org/abs/2401.01301
- https://arxiv.org/abs/2405.20362
- https://arxiv.org/abs/2308.11462
- https://arxiv.org/abs/2110.00976
- https://doi.org/10.1098/rsta.2023.0254
- https://arxiv.org/abs/2404.16130
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Legal AI is the use of AI systems in law: legal research, document and contract analysis, summarisation, compliance checks and question answering over legal sources. Large language models make these tasks far more accessible, but errors in law have direct legal or financial consequences, and studies find that general LLMs hallucinate on 58 to 88% of verifiable questions about US federal court cases (Dahl et al., 2024), while even commercial RAG-based legal research tools hallucinate on 17 to 33% of queries (Magesh et al., 2024). Grounding, verifiable citations and human review are therefore central.

### How it works

#### 1. Typical tasks

- **Legal research:** finding relevant norms, judgments and commentary for a legal question, usually through [[retrieval-augmented-generation|Retrieval-Augmented Generation]] over a curated corpus of statutes and case law.
- **Contract analysis and due diligence:** extracting parties, deadlines, termination and liability clauses and deviations from standard clauses ([[information-extraction|Information Extraction]]; [[contract-intelligence|Contract Intelligence]]).
- **Summarisation:** condensing judgments, opinions and contracts to their key statements, ideally with a reference to the passage each statement comes from.
- **Compliance monitoring:** checking internal processes or systems against regulatory requirements such as the [[eu-ai-act|EU AI Act]], the [[gdpr|General Data Protection Regulation (GDPR)]] or [[dora|Digital Operational Resilience Act (DORA)]].
- **Question answering:** answering concrete legal questions with references to the underlying norms.

#### 2. Why the domain is demanding

- **Accuracy and citation:** a fluent but wrong answer can have legal consequences, and a legal statement must be traceable to a specific norm or passage; citation correctness means that the cited source actually supports the statement ([[rag-generation-evaluation|RAG: Generation Evaluation]]; [[llm-evaluation|LLM Evaluation]]).
- **Versioned law:** statutes change, several versions can be in force for different periods, and transitional provisions are common, so a system must know which version applies at which point in time ([[vector-databases|Vector Databases]]).
- **Interlinked norms:** legal questions often combine several norms, exceptions and counter-exceptions, a multi-hop retrieval problem ([[graphrag|GraphRAG]]; [[knowledge-graphs|Knowledge Graphs]]).
- **Jurisdiction:** law is bound to a legal system, and performance varies across jurisdictions, courts, time periods and cases (Dahl et al., 2024).

#### 3. Measuring legal reasoning

Benchmarks make legal capabilities measurable. LexGLUE collects legal language understanding tasks in English and shows that legal-oriented models consistently outperform generic ones (Chalkidis et al., 2021). LegalBench consists of 162 tasks covering six types of legal reasoning, designed by legal professionals and used to evaluate 20 open-source and commercial LLMs (Guha et al., 2023). GPT-4 reached about 297 points on the US Uniform Bar Examination, above the passing threshold in all jurisdictions (Katz et al., 2024). Passing an exam shows broad legal knowledge, not reliability on concrete cases.

#### 4. RAG and GraphRAG for law

Keeping the legal knowledge outside the model weights makes it updatable and citable ([[rag-vs-fine-tuning|RAG vs. Fine-Tuning]]). Graph-based approaches build an entity knowledge graph from the documents and summaries for groups of related entities, which helps with global questions over an entire corpus (Edge et al., 2024); explicit relations between norms, such as references, exceptions and higher-ranking provisions, can be modelled in [[knowledge-graphs|Knowledge Graphs]].

#### Origin and variants

Legal NLP long relied on task-specific models and datasets such as those collected in LexGLUE (Chalkidis et al., 2021). With LLMs, the focus moved to broad legal reasoning benchmarks (Guha et al., 2023), bar exam performance (Katz et al., 2024) and the systematic measurement of hallucinations in general models (Dahl et al., 2024) and in commercial legal research tools (Magesh et al., 2024).

### When to use it

- For research, triage and first drafts where a qualified person checks every result before it is used.
- For extraction and comparison tasks with clear, checkable outputs, such as clause identification in contracts ([[contract-intelligence|Contract Intelligence]]).
- Not as the sole basis for binding legal assessments, especially for people without access to legal advice, who benefit most and are also most at risk from hallucinations (Dahl et al., 2024).

### Strengths and limitations

**Strengths**
- Speeds up research and review across large document collections.
- Answers grounded in retrieved sources can carry citations that are checked against the source text ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]).
- Legal-domain models outperform generic models on legal language understanding tasks (Chalkidis et al., 2021).

**Limitations**
- Legal hallucinations are frequent in general LLMs, models often fail to correct a user's wrong legal assumptions, and they do not reliably know when they hallucinate (Dahl et al., 2024).
- RAG reduces but does not eliminate hallucinations: commercial legal research tools hallucinated on 17 to 33% of queries despite claims of being hallucination-free (Magesh et al., 2024; [[rag-failure-modes|RAG: Failure Modes]]).
- Interpretation errors, where the right norms are retrieved but combined incorrectly, are hard to detect automatically because all cited sources are formally correct.
- Training corpora encode historical and structural inequalities, so models can reproduce discriminatory patterns, which is a quality problem and, in law, also a discrimination problem (Urchs, 2025; [[bias-in-nlp|Bias in NLP]]).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| General LLM chatbot | Answers from model knowledge without retrieval; high hallucination rates on legal questions (Dahl et al., 2024) | Brainstorming, not legal research |
| RAG-based legal research tool | Retrieves legal sources and cites them; fewer, but still frequent hallucinations (Magesh et al., 2024) | Research with verification of every citation |
| GraphRAG | Adds a knowledge graph and community summaries for corpus-wide questions (Edge et al., 2024) | Questions across many interlinked norms |
| Specialised extraction models | Trained for fixed tasks such as clause or entity extraction ([[contract-intelligence|Contract Intelligence]]) | High-volume document review |

### In practice

Systems provide research, suggestions and evidence, while a person makes the final legal assessment, approves contracts and briefs and takes risky compliance decisions ([[agentic-ai|Agentic AI]]). Citations are checked automatically for existence and manually for support, and evaluation uses domain-specific test sets with expert review rather than general benchmarks alone ([[llm-as-a-judge|LLM-as-a-Judge]]; [[quality-control|Quality Control]]; [[regression-testing|Regression Testing]]). Corpora are versioned with validity dates, and changes to models, prompts and indexes are tracked and tested before deployment ([[mlops-and-deployment|MLOps and Deployment]]; [[experiment-tracking|Experiment Tracking]]). Training data and outputs also raise questions of [[copyright-and-ai-training-data|Copyright and AI Training Data]], liability ([[ai-liability-law|AI Liability Law]]) and, for platforms, the [[digital-services-act|Digital Services Act]].

### Regulatory context

Under the [[eu-ai-act|EU AI Act]], high-risk AI systems include "AI systems intended to be used by a judicial authority or on their behalf to assist a judicial authority in researching and interpreting facts and the law and in applying the law to a concrete set of facts, or to be used in a similar way in alternative dispute resolution" (Art. 6(2) in conjunction with Annex III point 8(a)). An Annex III system "shall not be considered to be high-risk where it does not pose a significant risk of harm to the health, safety or fundamental rights of natural persons", for example because it only performs a narrow procedural task or a preparatory task (Art. 6(3)). Legal AI used in law firms or companies is therefore not automatically high-risk, but its intended purpose must be assessed. As soon as personal data from mandates, contracts or cases are processed, the [[gdpr|General Data Protection Regulation (GDPR)]] applies; in the financial sector, the [[dora|Digital Operational Resilience Act (DORA)]] can add requirements.

### Key takeaway

Legal AI can speed up research and document review, but hallucinated or unsupported citations remain frequent even with RAG, so every output needs verifiable sources and a qualified person who makes the final legal assessment.

### Sources

- Dahl, M. et al. (2024). *Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models.* Journal of Legal Analysis 2024. [arXiv:2401.01301](https://arxiv.org/abs/2401.01301)
- Magesh, V. et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.* Journal of Empirical Legal Studies 2025. [arXiv:2405.20362](https://arxiv.org/abs/2405.20362)
- Guha, N. et al. (2023). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models.* NeurIPS 2023 Datasets and Benchmarks. [arXiv:2308.11462](https://arxiv.org/abs/2308.11462)
- Chalkidis, I. et al. (2021). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.* ACL 2022. [arXiv:2110.00976](https://arxiv.org/abs/2110.00976)
- Katz, D. M., Bommarito, M. J., Gao, S. & Arredondo, P. (2024). *GPT-4 passes the bar exam.* Philosophical Transactions of the Royal Society A 382(2270). [doi:10.1098/rsta.2023.0254](https://doi.org/10.1098/rsta.2023.0254)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Legal AI bezeichnet den Einsatz von KI-Systemen im Recht: juristische Recherche, Dokumenten- und Vertragsanalyse, Zusammenfassung, Compliance-Prüfung und Frage-Antwort über Rechtsquellen. Große Sprachmodelle machen diese Aufgaben deutlich zugänglicher, doch Fehler haben im Recht unmittelbare rechtliche oder finanzielle Folgen. Studien zeigen, dass allgemeine LLMs bei 58 bis 88 % überprüfbarer Fragen zu US-Bundesgerichtsfällen halluzinieren (Dahl et al., 2024) und selbst kommerzielle, RAG-basierte juristische Recherchewerkzeuge bei 17 bis 33 % der Anfragen (Magesh et al., 2024). Grounding, überprüfbare Zitate und menschliche Prüfung stehen deshalb im Mittelpunkt.

### Funktionsweise

#### 1. Typische Aufgaben

- **Juristische Recherche:** relevante Normen, Urteile und Kommentierungen zu einer Rechtsfrage finden, meist über [[retrieval-augmented-generation|Retrieval-Augmented Generation]] auf einem kuratierten Korpus aus Gesetzen und Rechtsprechung.
- **Vertragsanalyse und Due Diligence:** Parteien, Fristen, Kündigungs- und Haftungsklauseln sowie Abweichungen von Standardklauseln extrahieren ([[information-extraction|Informationsextraktion]]; [[contract-intelligence|Contract Intelligence]]).
- **Zusammenfassung:** Urteile, Gutachten und Verträge auf ihre Kernaussagen verdichten, idealerweise mit Verweis auf die Fundstelle jeder Aussage.
- **Compliance-Monitoring:** interne Prozesse oder Systeme mit regulatorischen Anforderungen abgleichen, etwa mit der [[eu-ai-act|KI-Verordnung]], der [[gdpr|Datenschutz-Grundverordnung (DSGVO)]] oder dem [[dora|Digital Operational Resilience Act (DORA)]].
- **Frage-Antwort:** konkrete Rechtsfragen mit Verweis auf die zugrunde liegenden Normen beantworten.

#### 2. Warum die Domäne anspruchsvoll ist

- **Genauigkeit und Zitation:** Eine flüssige, aber falsche Antwort kann rechtliche Folgen haben, und eine juristische Aussage muss auf eine konkrete Norm oder Fundstelle zurückführbar sein; Zitationskorrektheit bedeutet, dass die zitierte Quelle die Aussage tatsächlich stützt ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]; [[llm-evaluation|LLM-Evaluation]]).
- **Versioniertes Recht:** Gesetze ändern sich, mehrere Fassungen können für unterschiedliche Zeiträume gelten, und Übergangsregelungen sind üblich; ein System muss daher wissen, welche Fassung zu welchem Zeitpunkt gilt ([[vector-databases|Vektordatenbanken]]).
- **Verknüpfte Normen:** Rechtsfragen verbinden oft mehrere Normen, Ausnahmen und Rückausnahmen, ein Multi-Hop-Retrieval-Problem ([[graphrag|GraphRAG]]; [[knowledge-graphs|Wissensgraphen]]).
- **Rechtsordnung:** Recht ist an ein Rechtssystem gebunden, und die Leistung schwankt zwischen Rechtsordnungen, Gerichten, Zeiträumen und Fällen (Dahl et al., 2024).

#### 3. Juristisches Schlussfolgern messen

Benchmarks machen juristische Fähigkeiten messbar. LexGLUE bündelt Aufgaben zum Verständnis englischer Rechtssprache und zeigt, dass auf Recht ausgerichtete Modelle generische Modelle durchgängig übertreffen (Chalkidis et al., 2021). LegalBench umfasst 162 Aufgaben zu sechs Arten juristischen Schlussfolgerns, die von Fachleuten aus dem Recht entworfen wurden, und evaluiert damit 20 offene und kommerzielle LLMs (Guha et al., 2023). GPT-4 erreichte im US Uniform Bar Examination rund 297 Punkte und lag damit in allen Rechtsordnungen über der Bestehensgrenze (Katz et al., 2024). Eine bestandene Prüfung zeigt breites juristisches Wissen, aber keine Verlässlichkeit bei konkreten Fällen.

#### 4. RAG und GraphRAG im Recht

Liegt das juristische Wissen außerhalb der Modellgewichte, bleibt es aktualisierbar und zitierbar ([[rag-vs-fine-tuning|RAG vs. Fine-Tuning]]). Graphbasierte Ansätze bauen aus den Dokumenten einen Wissensgraphen aus Entitäten und Zusammenfassungen für Gruppen verwandter Entitäten auf, was bei globalen Fragen über einen ganzen Korpus hilft (Edge et al., 2024); ausdrückliche Beziehungen zwischen Normen wie Verweise, Ausnahmen und übergeordnete Regelungen lassen sich in [[knowledge-graphs|Wissensgraphen]] abbilden.

#### Ursprung und Varianten

Juristische Sprachverarbeitung stützte sich lange auf aufgabenspezifische Modelle und Datensätze, wie sie LexGLUE bündelt (Chalkidis et al., 2021). Mit LLMs verlagerte sich der Fokus auf breite Benchmarks für juristisches Schlussfolgern (Guha et al., 2023), Ergebnisse in der Anwaltsprüfung (Katz et al., 2024) und die systematische Messung von Halluzinationen in allgemeinen Modellen (Dahl et al., 2024) und in kommerziellen juristischen Recherchewerkzeugen (Magesh et al., 2024).

### Wann einsetzen

- Für Recherche, Vorsortierung und erste Entwürfe, bei denen eine qualifizierte Person jedes Ergebnis vor der Verwendung prüft.
- Für Extraktions- und Vergleichsaufgaben mit klaren, überprüfbaren Ausgaben, etwa die Erkennung von Klauseln in Verträgen ([[contract-intelligence|Contract Intelligence]]).
- Nicht als alleinige Grundlage verbindlicher rechtlicher Einschätzungen, besonders für Menschen ohne Zugang zu Rechtsberatung, die am meisten profitieren und zugleich am stärksten durch Halluzinationen gefährdet sind (Dahl et al., 2024).

### Stärken und Grenzen

**Stärken**
- Beschleunigt Recherche und Prüfung über große Dokumentbestände.
- Antworten, die auf abgerufenen Quellen beruhen, können Zitate tragen, die am Quelltext überprüft werden ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]).
- Auf Recht spezialisierte Modelle übertreffen generische Modelle bei Aufgaben zum Verständnis von Rechtssprache (Chalkidis et al., 2021).

**Einschränkungen**
- Juristische Halluzinationen sind bei allgemeinen LLMs häufig; die Modelle korrigieren falsche rechtliche Annahmen der Nutzenden oft nicht und erkennen nicht zuverlässig, wann sie halluzinieren (Dahl et al., 2024).
- RAG verringert Halluzinationen, beseitigt sie aber nicht: Kommerzielle juristische Recherchewerkzeuge halluzinierten trotz gegenteiliger Werbeaussagen bei 17 bis 33 % der Anfragen (Magesh et al., 2024; [[rag-failure-modes|RAG: Typische Fehlerarten]]).
- Interpretationsfehler, bei denen die richtigen Normen gefunden, aber falsch kombiniert werden, sind automatisch schwer zu erkennen, weil alle zitierten Quellen formal korrekt sind.
- Trainingskorpora enthalten historische und strukturelle Ungleichheiten, sodass Modelle diskriminierende Muster reproduzieren können; das ist ein Qualitätsproblem und im Recht zugleich ein Diskriminierungsproblem (Urchs, 2025; [[bias-in-nlp|Bias in NLP]]).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Allgemeiner LLM-Chatbot | Antwortet aus dem Modellwissen ohne Retrieval; hohe Halluzinationsraten bei Rechtsfragen (Dahl et al., 2024) | Ideensammlung, nicht juristische Recherche |
| RAG-basiertes juristisches Recherchewerkzeug | Ruft Rechtsquellen ab und zitiert sie; weniger, aber weiterhin häufige Halluzinationen (Magesh et al., 2024) | Recherche mit Prüfung jedes Zitats |
| GraphRAG | Ergänzt einen Wissensgraphen und Zusammenfassungen von Entitätsgruppen für korpusweite Fragen (Edge et al., 2024) | Fragen über viele verknüpfte Normen |
| Spezialisierte Extraktionsmodelle | Für feste Aufgaben wie Klausel- oder Entitätsextraktion trainiert ([[contract-intelligence|Contract Intelligence]]) | Prüfung großer Dokumentmengen |

### In der Praxis

Systeme liefern Recherche, Vorschläge und Belege, während ein Mensch die finale rechtliche Bewertung trifft, Verträge und Schriftsätze freigibt und risikobehaftete Compliance-Entscheidungen verantwortet ([[agentic-ai|Agentic AI]]). Zitate werden automatisch auf Existenz und manuell darauf geprüft, ob sie die Aussage stützen; evaluiert wird mit domänenspezifischen Testsets und fachlicher Prüfung statt nur mit allgemeinen Benchmarks ([[llm-as-a-judge|LLM-as-a-Judge]]; [[quality-control|Qualitätskontrolle]]; [[regression-testing|Regressionstests]]). Korpora werden mit Gültigkeitsdaten versioniert, und Änderungen an Modellen, Prompts und Indizes werden vor dem Einsatz protokolliert und getestet ([[mlops-and-deployment|MLOps und Deployment]]; [[experiment-tracking|Experiment Tracking]]). Trainingsdaten und Ausgaben werfen außerdem Fragen des [[copyright-and-ai-training-data|Urheberrechts an KI-Trainingsdaten]], der Haftung ([[ai-liability-law|KI-Haftungsrecht]]) und bei Plattformen des [[digital-services-act|Gesetzes über digitale Dienste (DSA)]] auf.

### Regulatorischer Kontext

Nach der [[eu-ai-act|KI-Verordnung]] gelten als hochriskant „KI-Systeme, die bestimmungsgemäß von einer oder im Namen einer Justizbehörde verwendet werden sollen, um eine Justizbehörde bei der Ermittlung und Auslegung von Sachverhalten und Rechtsvorschriften und bei der Anwendung des Rechts auf konkrete Sachverhalte zu unterstützen, oder die auf ähnliche Weise für die alternative Streitbeilegung genutzt werden sollen" (Art. 6 Abs. 2 in Verbindung mit Anhang III Nr. 8 Buchst. a). Ein in Anhang III genanntes KI-System gilt nicht als hochriskant, „wenn es kein erhebliches Risiko der Beeinträchtigung in Bezug auf die Gesundheit, Sicherheit oder Grundrechte natürlicher Personen birgt", etwa weil es nur eine eng gefasste Verfahrensaufgabe oder eine vorbereitende Aufgabe durchführt (Art. 6 Abs. 3). Legal AI in Kanzleien oder Unternehmen ist daher nicht automatisch hochriskant, ihr bestimmungsgemäßer Zweck muss aber geprüft werden. Sobald personenbezogene Daten aus Mandaten, Verträgen oder Fällen verarbeitet werden, gilt die [[gdpr|Datenschutz-Grundverordnung (DSGVO)]]; im Finanzsektor kann der [[dora|Digital Operational Resilience Act (DORA)]] Anforderungen hinzufügen.

### Merksatz

Legal AI kann Recherche und Dokumentenprüfung beschleunigen, doch halluzinierte oder nicht tragende Zitate bleiben selbst mit RAG häufig; jede Ausgabe braucht deshalb überprüfbare Quellen und eine qualifizierte Person, die die finale rechtliche Bewertung trifft.

### Quellen

- Dahl, M. et al. (2024). *Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models.* Journal of Legal Analysis 2024. [arXiv:2401.01301](https://arxiv.org/abs/2401.01301)
- Magesh, V. et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.* Journal of Empirical Legal Studies 2025. [arXiv:2405.20362](https://arxiv.org/abs/2405.20362)
- Guha, N. et al. (2023). *LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models.* NeurIPS 2023 Datasets and Benchmarks. [arXiv:2308.11462](https://arxiv.org/abs/2308.11462)
- Chalkidis, I. et al. (2021). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.* ACL 2022. [arXiv:2110.00976](https://arxiv.org/abs/2110.00976)
- Katz, D. M., Bommarito, M. J., Gao, S. & Arredondo, P. (2024). *GPT-4 passes the bar exam.* Philosophical Transactions of the Royal Society A 382(2270). [doi:10.1098/rsta.2023.0254](https://doi.org/10.1098/rsta.2023.0254)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
