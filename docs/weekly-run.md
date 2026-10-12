# The weekly run as a graph

`app/agents/monitoring/weekly.py` runs the weekly monitoring as a
[LangGraph](https://github.com/langchain-ai/langgraph) state graph. Each step
is a node that starts the step's module as its own process. After a required
step, a conditional edge (dashed) goes on to the next step, or straight to the
summary when the step failed. The optional steps (drafts, inbox) always go on.
After the summary, the proposal branch is created only when there are drafts.

Regenerate this diagram after changing the steps:

```powershell
python -m app.agents.monitoring.weekly --diagram
```

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	validate_notes(validate notes)
	update_index(update index)
	fetch_sources(fetch sources)
	assess_relevance(assess relevance)
	write_drafts(write drafts)
	propose_inbox(propose inbox)
	summarise(summarise)
	propose_branch(propose branch)
	save_summary(save summary)
	__end__([<p>__end__</p>]):::last
	__start__ --> validate_notes;
	assess_relevance -.-> summarise;
	assess_relevance -.-> write_drafts;
	fetch_sources -.-> assess_relevance;
	fetch_sources -.-> summarise;
	propose_branch --> save_summary;
	propose_inbox --> summarise;
	summarise -.-> propose_branch;
	summarise -.-> save_summary;
	update_index -.-> fetch_sources;
	update_index -.-> summarise;
	validate_notes -.-> summarise;
	validate_notes -.-> update_index;
	write_drafts --> propose_inbox;
	save_summary --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```
