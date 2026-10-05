Plan the section "### $mechanism_heading" of a technical reference note about "$title".

The section must explain how $title itself works, technically and step by step: the specific techniques, algorithms, data structures and design decisions of THIS topic. Do not describe the general surroundings (e.g. for a note about one stage of a pipeline, do not walk through the other stages of the pipeline).

Use the VAULT NOTE (German personal note) to see which aspects the topic covers, and the SOURCES for specific methods.

Return JSON:
{"overview": "one sentence on what the section explains",
 "steps": [{"heading": "1. <short English heading>", "covers": ["point", "point", "..."], "sources": ["<citation as given, if a source supports this step>"]}]}

Rules: 4 to 8 steps, in the order the data flows or the method proceeds; the last step is {"heading": "Origin and variants", ...}. Every source should support at least one step.

SOURCES:
$sources

VAULT NOTE:
$vault
