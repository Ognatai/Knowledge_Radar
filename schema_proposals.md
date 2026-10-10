# Schema proposals

Proposed extensions to `schema.yaml`, reviewed together with the change that
needs them. On acceptance the type is added to `schema.yaml` and its entry is
removed from this file.

## 1. New entity type `Dataset` and relation `EVALUATES`

**Change:** node type `Dataset` (public; properties name_en, name_de,
description, aliases) for benchmarks and corpora; relation `EVALUATES` from
`Dataset` and `Method` to `Method`, `Concept` and `Technology` ("StereoSet
measures stereotypical bias in language models").

**Justification:** benchmarks and corpora are central facts in many notes, but
no type fits them: they are neither methods nor technologies, and `Source` is
for the documents a note cites. Found while reviewing:

- bias-in-nlp: "StereoSet (...) is a large-scale natural dataset in English for
  measuring stereotypical bias"; "The Bias Benchmark for QA (BBQ ...) consists of
  hand-built question sets on social biases"; the corpus taz2024full.
- also in gold notes: GLUE (attention-and-transformers), MT-bench and Chatbot
  Arena (llm-as-a-judge), HumanEval, AgentBench and SWE-bench (agentic-ai).

Until decided, such datasets are left out of the reviewed extractions.

## 2. `IS_EXAMPLE_OF`: allow Concept as subject

**Change:** `IS_EXAMPLE_OF.from` adds `Concept`.

**Justification:** concepts are often instances of broader concepts, and today
only methods, regulations and technologies can be an example of something.
Found while reviewing:

- classification-metrics: precision, recall, F1, MCC and ROC AUC are classification
  metrics ("Classification metrics measure how well a classifier's predictions
  match the true labels. Most are computed from the confusion matrix (...)").
- agentic-ai and mcp-and-related-protocols (gold): prompt injection as a
  security risk of agents.

On acceptance, the reviewed notes gain these links (e.g. `precision
IS_EXAMPLE_OF classification-metrics`).

## 3. `BASED_ON`: allow Regulation → Regulation

**Change:** `BASED_ON.from` and `BASED_ON.to` add `Regulation`.

**Justification:** acts build on frameworks of other acts without transposing
them (`IMPLEMENTS`) or changing them (`AMENDS`). Found while reviewing:

- cybersecurity-act: "Other acts such as the NIS2 Directive and the Cyber
  Resilience Act build on these schemes."
- cyber-resilience-act: "the CRA uses NIS2's definitions of incident and near
  miss and its CSIRTs designated as coordinators".

## Edges waiting for these proposals

Reviewed notes whose extraction will gain edges once the proposals are decided:

- bias-in-nlp: StereoSet, BBQ, taz2024full as datasets (1)
- classification-metrics: precision, recall, F1, MCC, ROC and PR curves `IS_EXAMPLE_OF` classification-metrics (2)
- contract-intelligence: `IS_EXAMPLE_OF legal-ai` (2); CUAD, ContractNLI as datasets (1)
- context-engineering: multi-agent systems as a system implementation (2)
- convolutional-neural-networks: ImageNet (1)
- cybersecurity-act: NIS2 and CRA `BASED_ON` cybersecurity-act (3)
- cyber-resilience-act: `BASED_ON nis2-directive` (3)
- eecc: eprivacy-directive `BASED_ON` eecc (3)
- embeddings: MTEB (1)
- engineering-methods-for-ai-systems: agent-skills, mcp-and-related-protocols, vibe-coding `IS_EXAMPLE_OF` it (2)
- entity-extraction: CoNLL-2003 (1)
- fairness-metrics: individual, group and subgroup fairness `IS_EXAMPLE_OF` fairness-metrics; fairness through (un)awareness and counterfactual fairness `IS_EXAMPLE_OF` individual-fairness; demographic parity, equalised odds, equal opportunity, predictive parity `IS_EXAMPLE_OF` group-fairness (2)
- information-retrieval: bias-preserving-gender-fairness `IS_EXAMPLE_OF` fairness-metrics (2)
- knowledge-graph-engineering: DBpedia, YAGO, Freebase (1)
- legal-ai: LexGLUE, LegalBench (1)
- llm-evaluation: MMLU, TruthfulQA, MT-bench, Chatbot Arena (1)
- natural-language-processing: GLUE, SQuAD, WMT 2014 (1)
- nis2-directive: repeal of NIS1 (Directive (EU) 2016/1148); no relation type for repeal yet
- rag-failure-modes: context-pollution, citation-hallucination, grounding-hallucination `IS_EXAMPLE_OF` rag-failure-modes (2); ALCE, ELI5 (1)
- rag-evaluation: KILT, SuperGLUE, AIS (1)
- gold notes: GLUE, MT-bench, Chatbot Arena, HumanEval, AgentBench, SWE-bench (1); prompt injection (2)
