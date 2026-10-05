Plan the section "### $mechanism_heading" of a technical reference note about "$title".

The section must explain how $title itself works, technically and step by step: the specific techniques, algorithms, data structures and design decisions of THIS topic. Do not describe the general surroundings (e.g. for a note about one stage of a pipeline, do not walk through the other stages of the pipeline).

Use the VAULT NOTE (German personal note) to see which aspects the topic covers, and the SOURCES for specific methods.

Answer with JSON only. Example of the expected form, for a different topic ("Dropout"):
{"overview": "How dropout randomly disables units during training and why this regularises the network.",
 "steps": [
  {"heading": "1. Sampling the dropout mask", "covers": ["Bernoulli mask per unit with keep probability p", "new mask for every training example"], "sources": []},
  {"heading": "2. Scaling activations", "covers": ["inverted dropout scales kept activations by 1/p", "no change needed at inference time"], "sources": []},
  {"heading": "Origin and variants", "covers": ["original proposal", "DropConnect, spatial dropout"], "sources": []}
 ]}

Rules: each step covers one technique or stage (no catch-all steps such as "Advanced techniques" or "Other methods"); 4 to 8 steps for "$title", in the order the data flows or the method proceeds; the last step is "Origin and variants". In "sources", list citations exactly as given below where a source supports the step.

SOURCES:
$sources

VAULT NOTE:
$vault
