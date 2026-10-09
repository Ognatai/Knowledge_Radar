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
