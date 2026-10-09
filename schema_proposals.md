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

## Edges waiting for these proposals

Reviewed notes whose extraction will gain edges once the proposals are decided:

- bias-in-nlp: StereoSet, BBQ, taz2024full as datasets (1)
- classification-metrics: precision, recall, F1, MCC, ROC and PR curves `IS_EXAMPLE_OF` classification-metrics (2)
- contract-intelligence: `IS_EXAMPLE_OF legal-ai` (2); CUAD, ContractNLI as datasets (1)
- context-engineering: multi-agent systems as a system implementation (2)
- convolutional-neural-networks: ImageNet (1)
- gold notes: GLUE, MT-bench, Chatbot Arena, HumanEval, AgentBench, SWE-bench (1); prompt injection (2)
