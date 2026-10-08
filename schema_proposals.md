# Schema proposals

Proposed extensions to `schema.yaml`, reviewed together with the change that
needs them. On acceptance the type is added to `schema.yaml` and its entry is
removed from this file.

## 1. `BASED_ON`: allow Technology at both ends

**Change:** `BASED_ON.from` and `BASED_ON.to` add `Technology`.

**Justification:** technologies build on other technologies (protocols on
message formats, frameworks on libraries), and concepts such as protocols build
on technologies; today `BASED_ON` connects only methods and concepts. Found while
labelling the gold standard:

- mcp-and-related-protocols: "MCP builds on JSON-RPC, one of several API styles"
- mcp-and-related-protocols: LSP is "the model for MCP's client-server idea"
- sparql: "SPARQL is the W3C query language for RDF knowledge graphs"
- docker: "images, which are built from a Dockerfile"; "orchestrators such as
  Kubernetes" manage containers
- langchain-and-langgraph: the agent loop is "an approach introduced as ReAct"

## 2. `DEVELOPED_BY`: allow Regulation → Organization

**Change:** `DEVELOPED_BY.from` adds `Regulation`.

**Justification:** who issued a standard, guideline or ordinance is a central
fact about it, especially for soft law; today only methods, concepts and
technologies can have an author. Found while labelling the gold standard:

- bcbs-239-and-ecb-rdarr-guide: "BCBS 239 is the Basel Committee's set of 14
  principles"; "The ECB Guide (...) sets out the ECB's minimum supervisory
  expectations"
