---
title_en: Reinforcement Learning Fundamentals
title_de: Grundlagen des Reinforcement Learning
entity_type: Method
sources:
- http://incompleteideas.net/book/the-book-2nd.html
- https://doi.org/10.1007/BF00992698
- https://arxiv.org/abs/1312.5602
- https://arxiv.org/abs/1706.03741
- https://arxiv.org/abs/2203.02155
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Reinforcement learning (RL) trains an agent to act in an environment by trial and error: the agent observes states, takes actions and receives rewards, and learns a policy that maximises the expected cumulative reward (Sutton & Barto, 2018). Methods range from tabular Q-learning (Watkins & Dayan, 1992) to deep RL from raw pixels (Mnih et al., 2013) and learning from human preferences (Christiano et al., 2017), which is used to fine-tune language models to follow instructions (Ouyang et al., 2022).

### How it works

The agent repeatedly observes the current state, chooses an action, and receives a reward and the next state from the environment. From these experiences it estimates how good actions are and improves its policy, balancing trying new actions against using what it already knows.

```text
1. Agent, environment and reward
▼
2. Exploration and exploitation
▼
3. Q-learning
▼
4. Deep reinforcement learning
▼
5. Learning from human preferences
```

#### 1. Agent, environment and reward

In reinforcement learning an agent interacts with an environment: it observes states, takes actions and receives rewards, and its goal is a policy that maximises the expected cumulative, usually discounted, reward (Sutton & Barto, 2018). The problem is formalised as a Markov decision process, and value functions estimate how much future reward can be expected from a state or from an action in a state.

#### 2. Exploration and exploitation

An agent that always picks the action that currently looks best may never discover better ones; one that always experiments never uses what it has learned. This exploration-exploitation trade-off is handled, for example, with epsilon-greedy action selection, which mostly picks the best-known action and occasionally a random one (Sutton & Barto, 2018).

#### 3. Q-learning

Q-learning (Watkins & Dayan, 1992) is a model-free method: it needs no model of the environment and learns the values of actions in states, the Q-values, directly from experienced transitions and rewards. Watkins & Dayan proved that Q-learning converges to the optimal action-values with probability 1, provided that all actions are repeatedly sampled in all states and the values are represented discretely.

#### 4. Deep reinforcement learning

Mnih et al. (2013) presented the first deep learning model that learned control policies directly from high-dimensional sensory input with reinforcement learning. A convolutional neural network, trained with a variant of Q-learning, took raw pixels as input and estimated future rewards. On seven Atari 2600 games, with no adjustment of architecture or learning algorithm, it outperformed all previous approaches on six games and surpassed a human expert on three.

#### 5. Learning from human preferences

For complex tasks, a reward function is hard to specify. Christiano et al. (2017) defined goals through non-expert human preferences between pairs of trajectory segments and solved complex RL tasks without access to the reward function, with feedback on less than one percent of the agent's interactions. The same idea, reinforcement learning from human feedback, was used to fine-tune GPT-3 into InstructGPT, which human evaluators preferred to the much larger original model (Ouyang et al., 2022; [[llm-adaptation|LLM Adaptation]]).

#### Origin and variants

Sutton & Barto (2018) present the field, including temporal-difference learning, function approximation and policy-gradient methods. Q-learning (Watkins & Dayan, 1992), deep RL (Mnih et al., 2013) and RL from human preferences (Christiano et al., 2017; Ouyang et al., 2022) mark important steps.

### When to use it

- When an agent must learn a sequence of decisions from interaction and delayed rewards rather than from labelled examples (Sutton & Barto, 2018).
- When states are high-dimensional, such as images, deep RL can learn from raw input (Mnih et al., 2013).
- When the desired behaviour is easier to judge than to specify as a reward, learning from human preferences applies (Christiano et al., 2017).

### Strengths and limitations

**Strengths**
- Learns from interaction without labelled examples (Sutton & Barto, 2018).
- Q-learning has a convergence guarantee under the stated conditions (Watkins & Dayan, 1992).
- Human preferences can replace a hand-written reward with little feedback (Christiano et al., 2017).

**Limitations**
- The convergence guarantee of Q-learning requires all actions to be sampled repeatedly in all states (Watkins & Dayan, 1992).
- Complex goals are hard to express as a reward function (Christiano et al., 2017).
- The agent must explore, which can be costly or risky in real environments (Sutton & Barto, 2018).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Tabular Q-learning | Learns action values per state, model-free (Watkins & Dayan, 1992) | Small, discrete state spaces |
| Deep Q-learning | Neural network estimates action values from raw input (Mnih et al., 2013) | High-dimensional states such as images |
| RL from human preferences | Reward learned from human comparisons (Christiano et al., 2017; Ouyang et al., 2022) | Goals that are hard to specify |

### In practice

The reward must express what is actually wanted; poorly designed rewards lead agents to optimise the wrong behaviour, which is one motivation for learning rewards from human preferences (Christiano et al., 2017). In language models, RL from human feedback is one stage of a fine-tuning process after supervised training on demonstrations (Ouyang et al., 2022).

### Key takeaway

Reinforcement learning learns a policy from rewards obtained through interaction; with deep networks it scales to raw sensory input, and with human preferences it can learn goals that are hard to write down.

### Sources

- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. [book website](http://incompleteideas.net/book/the-book-2nd.html)
- Watkins, C. J. C. H. & Dayan, P. (1992). *Q-learning.* Machine Learning 8(3-4). [doi:10.1007/BF00992698](https://doi.org/10.1007/BF00992698)
- Mnih, V. et al. (2013). *Playing Atari with Deep Reinforcement Learning.* [arXiv:1312.5602](https://arxiv.org/abs/1312.5602)
- Christiano, P. et al. (2017). *Deep reinforcement learning from human preferences.* NeurIPS 2017. [arXiv:1706.03741](https://arxiv.org/abs/1706.03741)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* NeurIPS 2022. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Reinforcement Learning (RL) trainiert einen Agenten, durch Versuch und Irrtum in einer Umgebung zu handeln: Der Agent beobachtet Zustände, führt Aktionen aus, erhält Belohnungen und lernt eine Strategie (Policy), die die erwartete kumulierte Belohnung maximiert (Sutton & Barto, 2018). Die Verfahren reichen von tabellarischem Q-Learning (Watkins & Dayan, 1992) über Deep RL auf Rohpixeln (Mnih et al., 2013) bis zum Lernen aus menschlichen Präferenzen (Christiano et al., 2017), mit dem Sprachmodelle darauf feinabgestimmt werden, Anweisungen zu befolgen (Ouyang et al., 2022).

### Funktionsweise

Der Agent beobachtet wiederholt den aktuellen Zustand, wählt eine Aktion und erhält von der Umgebung eine Belohnung und den nächsten Zustand. Aus diesen Erfahrungen schätzt er, wie gut Aktionen sind, und verbessert seine Strategie; dabei wägt er ab, ob er Neues ausprobiert oder Bekanntes nutzt.

```text
1. Agent, Umgebung und Belohnung
▼
2. Exploration und Exploitation
▼
3. Q-Learning
▼
4. Deep Reinforcement Learning
▼
5. Lernen aus menschlichen Präferenzen
```

#### 1. Agent, Umgebung und Belohnung

Beim Reinforcement Learning interagiert ein Agent mit einer Umgebung: Er beobachtet Zustände, führt Aktionen aus und erhält Belohnungen, und sein Ziel ist eine Strategie, die die erwartete kumulierte, meist diskontierte Belohnung maximiert (Sutton & Barto, 2018). Das Problem wird als Markov-Entscheidungsprozess formalisiert, und Wertfunktionen schätzen, wie viel künftige Belohnung von einem Zustand oder einer Aktion in einem Zustand zu erwarten ist.

#### 2. Exploration und Exploitation

Ein Agent, der immer die aktuell beste Aktion wählt, entdeckt bessere womöglich nie; einer, der nur experimentiert, nutzt nie, was er gelernt hat. Diese Abwägung zwischen Exploration und Exploitation wird etwa mit Epsilon-Greedy gelöst: Meist wird die beste bekannte Aktion gewählt, gelegentlich eine zufällige (Sutton & Barto, 2018).

#### 3. Q-Learning

Q-Learning (Watkins & Dayan, 1992) ist ein modellfreies Verfahren: Es braucht kein Modell der Umgebung und lernt die Werte von Aktionen in Zuständen, die Q-Werte, direkt aus erlebten Übergängen und Belohnungen. Watkins & Dayan bewiesen, dass Q-Learning mit Wahrscheinlichkeit 1 gegen die optimalen Aktionswerte konvergiert, sofern alle Aktionen in allen Zuständen wiederholt ausprobiert und die Werte diskret dargestellt werden.

#### 4. Deep Reinforcement Learning

Mnih et al. (2013) stellten das erste Deep-Learning-Modell vor, das mit Reinforcement Learning Steuerungsstrategien direkt aus hochdimensionalen Sinnesdaten lernte. Ein konvolutionales neuronales Netz, trainiert mit einer Variante des Q-Learnings, erhielt Rohpixel als Eingabe und schätzte künftige Belohnungen. In sieben Atari-2600-Spielen übertraf es ohne Anpassung von Architektur oder Lernalgorithmus in sechs Spielen alle bisherigen Ansätze und in drei Spielen einen menschlichen Experten.

#### 5. Lernen aus menschlichen Präferenzen

Für komplexe Aufgaben ist eine Belohnungsfunktion schwer anzugeben. Christiano et al. (2017) definierten Ziele über Präferenzen von Laien zwischen Paaren von Trajektorienabschnitten und lösten komplexe RL-Aufgaben ohne Zugang zur Belohnungsfunktion, mit Feedback zu weniger als einem Prozent der Interaktionen des Agenten. Dieselbe Idee, Reinforcement Learning from Human Feedback, wurde genutzt, um GPT-3 zu InstructGPT feinabzustimmen, das menschliche Bewertende dem viel größeren Ausgangsmodell vorzogen (Ouyang et al., 2022; [[llm-adaptation|LLM-Anpassung]]).

#### Ursprung und Varianten

Sutton & Barto (2018) stellen das Gebiet dar, einschließlich Temporal-Difference-Lernen, Funktionsapproximation und Policy-Gradient-Verfahren. Q-Learning (Watkins & Dayan, 1992), Deep RL (Mnih et al., 2013) und RL aus menschlichen Präferenzen (Christiano et al., 2017; Ouyang et al., 2022) markieren wichtige Schritte.

### Wann einsetzen

- Wenn ein Agent eine Folge von Entscheidungen aus Interaktion und verzögerten Belohnungen lernen muss statt aus gelabelten Beispielen (Sutton & Barto, 2018).
- Wenn Zustände hochdimensional sind, etwa Bilder, kann Deep RL aus Rohdaten lernen (Mnih et al., 2013).
- Wenn sich das gewünschte Verhalten leichter beurteilen als als Belohnung formulieren lässt, eignet sich das Lernen aus menschlichen Präferenzen (Christiano et al., 2017).

### Stärken und Grenzen

**Stärken**
- Lernt aus Interaktion ohne gelabelte Beispiele (Sutton & Barto, 2018).
- Q-Learning hat unter den genannten Bedingungen eine Konvergenzgarantie (Watkins & Dayan, 1992).
- Menschliche Präferenzen können eine handgeschriebene Belohnung mit wenig Feedback ersetzen (Christiano et al., 2017).

**Einschränkungen**
- Die Konvergenzgarantie von Q-Learning setzt voraus, dass alle Aktionen in allen Zuständen wiederholt ausprobiert werden (Watkins & Dayan, 1992).
- Komplexe Ziele lassen sich schwer als Belohnungsfunktion ausdrücken (Christiano et al., 2017).
- Der Agent muss explorieren, was in realen Umgebungen teuer oder riskant sein kann (Sutton & Barto, 2018).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Tabellarisches Q-Learning | Lernt Aktionswerte je Zustand, modellfrei (Watkins & Dayan, 1992) | Kleine, diskrete Zustandsräume |
| Deep Q-Learning | Neuronales Netz schätzt Aktionswerte aus Rohdaten (Mnih et al., 2013) | Hochdimensionale Zustände wie Bilder |
| RL aus menschlichen Präferenzen | Belohnung aus menschlichen Vergleichen gelernt (Christiano et al., 2017; Ouyang et al., 2022) | Schwer formulierbare Ziele |

### In der Praxis

Die Belohnung muss ausdrücken, was tatsächlich gewollt ist; schlecht gestaltete Belohnungen führen dazu, dass Agenten das falsche Verhalten optimieren, was ein Grund ist, Belohnungen aus menschlichen Präferenzen zu lernen (Christiano et al., 2017). Bei Sprachmodellen ist RL aus menschlichem Feedback eine Stufe des Fine-Tunings nach überwachtem Training auf Demonstrationen (Ouyang et al., 2022).

### Merksatz

Reinforcement Learning lernt eine Strategie aus Belohnungen, die durch Interaktion entstehen; mit tiefen Netzen skaliert es auf Sinnesrohdaten, und mit menschlichen Präferenzen lernt es Ziele, die sich schwer aufschreiben lassen.

### Quellen

- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. [book website](http://incompleteideas.net/book/the-book-2nd.html)
- Watkins, C. J. C. H. & Dayan, P. (1992). *Q-learning.* Machine Learning 8(3-4). [doi:10.1007/BF00992698](https://doi.org/10.1007/BF00992698)
- Mnih, V. et al. (2013). *Playing Atari with Deep Reinforcement Learning.* [arXiv:1312.5602](https://arxiv.org/abs/1312.5602)
- Christiano, P. et al. (2017). *Deep reinforcement learning from human preferences.* NeurIPS 2017. [arXiv:1706.03741](https://arxiv.org/abs/1706.03741)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* NeurIPS 2022. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
