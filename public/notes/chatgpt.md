---
title_en: ChatGPT
title_de: ChatGPT
entity_type: Technology
aliases:
- Chat GPT
sources:
- https://openai.com/index/chatgpt/
- https://arxiv.org/abs/2203.02155
- https://doi.org/10.1007/978-3-031-74630-7_20
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

ChatGPT is a conversational system that OpenAI introduced on 30 November 2022 as a research preview; the dialogue format lets it answer follow-up questions, admit its mistakes, challenge incorrect premises and reject inappropriate requests (OpenAI, 2022). It was fine-tuned from a model in the [[gpt|GPT]]-3.5 series with reinforcement learning from human feedback (RLHF), using the same methods as InstructGPT with a different data collection setup (OpenAI, 2022). Combining a GPT model with RLHF and a dialogue interface made [[large-language-models|large language models]] accessible to the public, drove adoption in writing, education and programming and raised new concerns about ethics, misinformation and AI governance (Urchs, 2025). A study of English and German responses found ChatGPT useful for drafting texts, but its output has to be checked thoroughly for biases and grammatical mistakes (Urchs et al., 2023).

### Core concepts

```text
GPT-3.5 series model (finished training in early 2022)
 ▼
supervised fine-tuning: AI trainers write dialogues, playing both user and assistant
  + InstructGPT data transformed into dialogue format
 ▼
reward model: trainers rank several sampled alternative responses
 ▼
Proximal Policy Optimization against the reward model (several iterations)
 ▼
chat interface + Moderation API filter → research preview with user feedback
```

#### 1. Training with human feedback

OpenAI trained an initial model with supervised fine-tuning on conversations in which human AI trainers played both the user and the AI assistant, with access to model-written suggestions; this dialogue data set was mixed with the InstructGPT data set, transformed into dialogue format. For the reward model, trainers ranked several alternative completions sampled for model-written messages from their conversations with the chatbot, and the model was then fine-tuned against the reward models with Proximal Policy Optimization over several iterations (OpenAI, 2022). The underlying method comes from InstructGPT, which combined supervised fine-tuning, a reward model and reinforcement learning; there, outputs of a 1.3B-parameter aligned model were preferred to those of the 175B-parameter GPT-3 (Ouyang et al., 2022). How this post-training works in general is covered in [[llm-alignment|LLM alignment]] and [[reinforcement-learning|reinforcement learning]].

#### 2. Limitations named at launch

ChatGPT sometimes writes plausible-sounding but incorrect or nonsensical answers. This is hard to fix because RL training has no source of truth, training the model to be more cautious makes it decline questions it could answer, and supervised training misleads the model when the ideal answer depends on what the model knows rather than what the human demonstrator knows. The model is sensitive to small changes in phrasing and to repeating the same prompt; it is often excessively verbose, because trainers preferred longer answers and because of over-optimisation; it usually guesses what an ambiguous query means instead of asking a clarifying question; and it sometimes responds to harmful instructions or shows biased behaviour. The Moderation API warns about or blocks some unsafe content, with false negatives and positives expected (OpenAI, 2022). Detecting incorrect answers is covered in [[hallucination-detection|hallucination detection]].

#### Origin and variants

ChatGPT is a sibling model to InstructGPT, which is trained to follow an instruction in a prompt and give a detailed response; it was released as a step in OpenAI's iterative deployment, building on lessons from GPT-3 and Codex (OpenAI, 2022). The announcement notes that ChatGPT has evolved substantially since 2022 (OpenAI, 2022); the study by Urchs et al. (2023) covers GPT-3.5 and recommends exploring newer models, since other problems will arise with them. During its data collection, an unannounced update changed the responses to one prompt fundamentally, and OpenAI added a "continue response" button, before which responses could end mid-sentence or even mid-word (Urchs et al., 2023).

### Common usage

#### A dialogue interface for everyone

GPT-3 was a scaled-up GPT-2 that outperformed task-specific models on many benchmarks; adapted via RLHF to dialogue-style conversations and combined with a simple user interface, GPT-3.5 became the system known as ChatGPT. Users no longer need to program or have a computer science background: they have a natural language conversation and use the system to write texts, check grammar and spelling and even fact-check their work (Urchs et al., 2023). Users without IT expertise tend to see it as a "magical box" that knows all the answers, and a system that is this easy to use and sounds this natural is perceived as highly credible, so users trust it without questioning how the responses are generated (Urchs et al., 2023).

#### Gender bias in English and German responses

Urchs et al. (2023) prompted ChatGPT, based on GPT-3.5, in English and German to answer from a female, male or neutral perspective in the context of university communications, first with exploratory prompts and then by repeating two prompts ten times. German responses contained grammatical errors that are easy to miss in a mostly correct text; ChatGPT used German gender-neutral language only when the prompt did, sometimes broke its rules, for example with the non-existent form "Experte:r", and translated the gender-neutral English *they* into German as third person plural, giving an incorrect sentence with a possibly different meaning. Adding a gender to a prompt triggered a "gender template" that focused the response on fairness and equality, which can lead to embarrassing texts such as one advocating more men in academia; neutral prompts produced exclusively female professors and a bias towards STEM fields, while overall the responses used few gender-coded words (Urchs et al., 2023). Overt discrimination was rare, but post-hoc fairness interventions could inadvertently reinforce gender stereotypes, which shows the limits of downstream debiasing (Urchs, 2025); the wider field is covered in [[bias-in-nlp|bias in NLP]].

### When to use it

- Drafting texts for daily work, as long as the result is checked thoroughly for mistakes and biases (Urchs et al., 2023).
- Augmenting human work rather than replacing it: users should not let the system work autonomously for them (Urchs et al., 2023).
- Bilingual texts need extra care, because responses in German were grammatically weaker than in English (Urchs et al., 2023).

### Strengths and limitations

**Strengths**
- The dialogue format supports follow-up questions, admitting mistakes, challenging incorrect premises and rejecting inappropriate requests (OpenAI, 2022).
- No programming knowledge is needed; ChatGPT helps users without IT expertise to draft texts (Urchs et al., 2023).
- In English it uses the gender-neutral *they*, and in German the gender-neutral word for students, which helps in writing inclusive text (Urchs et al., 2023).

**Limitations**
- Plausible-sounding but incorrect answers, sensitivity to phrasing, verbosity and guessing instead of asking (OpenAI, 2022).
- Gendered prompts trigger template-like responses, and German gender-neutral language is often used incorrectly (Urchs et al., 2023).
- Responses vary between identical prompts, and unannounced system updates can make proven prompts stop working (Urchs et al., 2023).

### Comparison

| System | What it is built for | Interaction |
|--------|----------------------|-------------|
| GPT-3 | Scaled-up GPT-2 for zero- and few-shot use (Urchs et al., 2023) | Prompting a model |
| InstructGPT | Following an instruction in a prompt with a detailed response (OpenAI, 2022) | Single instruction and response |
| ChatGPT | Conversation, fine-tuned from GPT-3.5 with RLHF (OpenAI, 2022) | Multi-turn dialogue in a chat interface |

### In practice

Responses should be used only as a rough draft and proofread in depth, because errors are hard to find in a mostly correct text (Urchs et al., 2023). For German gender-neutral output, the prompt itself has to use gender-neutral language (Urchs et al., 2023). Because identical prompts give different answers and system updates change behaviour, prompts that worked before need to be re-tested for biased output after an update (Urchs et al., 2023). Systematic approaches to writing prompts are covered in [[prompt-engineering|prompt engineering]], and the copyright questions raised by models like ChatGPT in [[copyright-and-ai-training-data|copyright and AI training data]].

### Key takeaway

ChatGPT is a GPT-3.5 model fine-tuned with RLHF for dialogue and offered through a simple chat interface; that interface brought large language models to the general public, whose trust in natural-sounding answers makes careful checking for errors and biases essential.

### Sources

- OpenAI (2022). *Introducing ChatGPT.* 30 November 2022. [openai.com](https://openai.com/index/chatgpt/)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* NeurIPS 2022. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

ChatGPT ist ein Dialogsystem, das OpenAI am 30. November 2022 als Research Preview vorstellte; das Dialogformat ermöglicht es, Folgefragen zu beantworten, eigene Fehler einzugestehen, falsche Prämissen zurückzuweisen und unangemessene Anfragen abzulehnen (OpenAI, 2022). Es wurde aus einem Modell der [[gpt|GPT]]-3.5-Reihe mit Reinforcement Learning from Human Feedback (RLHF) feinabgestimmt, mit denselben Methoden wie InstructGPT, aber einer anderen Datenerhebung (OpenAI, 2022). Die Verbindung eines GPT-Modells mit RLHF und einer Dialogoberfläche machte große Sprachmodelle der Öffentlichkeit zugänglich, förderte ihre Nutzung beim Schreiben, in der Bildung und beim Programmieren und warf neue Fragen zu Ethik, Desinformation und KI-Governance auf (Urchs, 2025). Eine Studie zu englischen und deutschen Antworten zeigte, dass ChatGPT beim Entwerfen von Texten hilft, seine Ausgaben aber gründlich auf Verzerrungen und Grammatikfehler geprüft werden müssen (Urchs et al., 2023).

### Kernkonzepte

```text
Modell der GPT-3.5-Reihe (Training Anfang 2022 abgeschlossen)
 ▼
Supervised Fine-Tuning: AI-Trainer schreiben Dialoge und spielen Nutzer und Assistent
  + InstructGPT-Daten, ins Dialogformat überführt
 ▼
Reward-Modell: Trainer ordnen mehrere gesampelte alternative Antworten
 ▼
Proximal Policy Optimization gegen das Reward-Modell (mehrere Iterationen)
 ▼
Chat-Oberfläche + Filter über die Moderation API → Research Preview mit Nutzerfeedback
```

#### 1. Training mit menschlichem Feedback

OpenAI trainierte ein erstes Modell mit Supervised Fine-Tuning auf Gesprächen, in denen menschliche AI-Trainer sowohl die Nutzerseite als auch den KI-Assistenten spielten, unterstützt durch vom Modell geschriebene Vorschläge; dieser Dialogdatensatz wurde mit dem ins Dialogformat überführten InstructGPT-Datensatz gemischt. Für das Reward-Modell ordneten die Trainer mehrere alternative Fortsetzungen, die zu vom Modell geschriebenen Nachrichten aus ihren Gesprächen mit dem Chatbot gesampelt wurden, und das Modell wurde anschließend in mehreren Iterationen mit Proximal Policy Optimization gegen die Reward-Modelle feinabgestimmt (OpenAI, 2022). Das zugrunde liegende Verfahren stammt von InstructGPT, das Supervised Fine-Tuning, ein Reward-Modell und Reinforcement Learning kombinierte; dort wurden Ausgaben eines angepassten Modells mit 1,3 Milliarden Parametern denen des 175-Milliarden-Parameter-Modells GPT-3 vorgezogen (Ouyang et al., 2022). Wie dieses Post-Training allgemein funktioniert, behandeln [[llm-alignment|LLM-Alignment]] und [[reinforcement-learning|Reinforcement Learning]].

#### 2. Grenzen, benannt bei der Einführung

ChatGPT schreibt manchmal plausibel klingende, aber falsche oder unsinnige Antworten. Das ist schwer zu beheben, weil es beim RL-Training keine Quelle der Wahrheit gibt, ein vorsichtigeres Modell auch Fragen ablehnt, die es beantworten könnte, und Supervised Training das Modell in die Irre führt, wenn die ideale Antwort davon abhängt, was das Modell weiß, und nicht davon, was der menschliche Demonstrator weiß. Das Modell reagiert empfindlich auf kleine Änderungen der Formulierung und auf das Wiederholen desselben Prompts; es ist oft übermäßig ausführlich, weil die Trainer längere Antworten bevorzugten und wegen Überoptimierung; es rät meist, was eine mehrdeutige Anfrage meint, statt nachzufragen; und es reagiert manchmal auf schädliche Anweisungen oder zeigt verzerrtes Verhalten. Die Moderation API warnt vor bestimmten unsicheren Inhalten oder blockiert sie, wobei falsch Negative und falsch Positive erwartet werden (OpenAI, 2022). Das Erkennen falscher Antworten behandelt [[hallucination-detection|Halluzinationserkennung]].

#### Herkunft und Varianten

ChatGPT ist ein Schwestermodell von InstructGPT, das darauf trainiert ist, einer Anweisung in einem Prompt zu folgen und ausführlich zu antworten; es erschien als Schritt in OpenAIs schrittweiser Bereitstellung, aufbauend auf Erfahrungen mit GPT-3 und Codex (OpenAI, 2022). Die Ankündigung vermerkt, dass sich ChatGPT seit 2022 stark weiterentwickelt hat (OpenAI, 2022); die Studie von Urchs et al. (2023) behandelt GPT-3.5 und empfiehlt, neuere Modelle zu untersuchen, da bei ihnen andere Probleme auftreten werden. Während ihrer Datenerhebung änderte ein unangekündigtes Update die Antworten auf einen Prompt grundlegend, und OpenAI führte eine Schaltfläche „continue response“ ein, vor der Antworten mitten im Satz oder sogar mitten im Wort enden konnten (Urchs et al., 2023).

### Typische Verwendung

#### Eine Dialogoberfläche für alle

GPT-3 war ein hochskaliertes GPT-2, das auf vielen Benchmarks aufgabenspezifische Modelle übertraf; per RLHF an Gespräche im Dialogstil angepasst und mit einer einfachen Benutzeroberfläche kombiniert, wurde GPT-3.5 zum System namens ChatGPT. Wer es nutzt, muss weder programmieren können noch Informatik studiert haben: Ein Gespräch in natürlicher Sprache genügt, und das System wird genutzt, um Texte zu schreiben, Grammatik und Rechtschreibung zu prüfen und sogar Fakten zu überprüfen (Urchs et al., 2023). Menschen ohne IT-Hintergrund sehen es oft als „magische Box“, die alle Antworten kennt, und ein System, das so einfach zu bedienen ist und so natürlich klingt, wirkt sehr glaubwürdig, sodass ihm vertraut wird, ohne zu hinterfragen, wie die Antworten entstehen (Urchs et al., 2023).

#### Gender Bias in englischen und deutschen Antworten

Urchs et al. (2023) forderten ChatGPT auf Basis von GPT-3.5 auf Englisch und Deutsch auf, aus weiblicher, männlicher oder neutraler Perspektive zu antworten, im Kontext der Hochschulkommunikation, zunächst mit explorativen Prompts und dann durch zehnfache Wiederholung zweier Prompts. Deutsche Antworten enthielten Grammatikfehler, die in einem überwiegend korrekten Text leicht zu übersehen sind; ChatGPT nutzte gendergerechte Sprache im Deutschen nur, wenn der Prompt es tat, verletzte manchmal ihre Regeln, etwa mit der nicht existierenden Form „Experte:r“, und übersetzte das geschlechtsneutrale englische *they* als dritte Person Plural, was einen falschen Satz mit möglicherweise anderer Bedeutung ergab. Eine Geschlechtsangabe im Prompt löste ein „Gender-Template“ aus, das die Antwort auf Fairness und Gleichstellung lenkte, was zu peinlichen Texten führen kann, etwa einem Plädoyer für mehr Männer in der Wissenschaft; neutrale Prompts erzeugten ausschließlich Professorinnen und eine Tendenz zu MINT-Fächern, während die Antworten insgesamt wenige geschlechtlich konnotierte Wörter verwendeten (Urchs et al., 2023). Offene Diskriminierung war selten, aber nachträgliche Fairness-Eingriffe konnten Geschlechterstereotype unbeabsichtigt verstärken, was die Grenzen des Debiasing am Ende der Kette zeigt (Urchs, 2025); das Feld insgesamt behandelt [[bias-in-nlp|Bias in NLP]].

### Wann einsetzen

- Texte für die tägliche Arbeit entwerfen, sofern das Ergebnis gründlich auf Fehler und Verzerrungen geprüft wird (Urchs et al., 2023).
- Menschliche Arbeit ergänzen statt ersetzen: Das System sollte nicht eigenständig an Stelle der Nutzenden arbeiten (Urchs et al., 2023).
- Zweisprachige Texte brauchen besondere Sorgfalt, weil deutsche Antworten grammatisch schwächer waren als englische (Urchs et al., 2023).

### Stärken und Grenzen

**Stärken**
- Das Dialogformat erlaubt Folgefragen, das Eingestehen von Fehlern, das Zurückweisen falscher Prämissen und das Ablehnen unangemessener Anfragen (OpenAI, 2022).
- Programmierkenntnisse sind nicht nötig; ChatGPT hilft Menschen ohne IT-Hintergrund beim Entwerfen von Texten (Urchs et al., 2023).
- Im Englischen nutzt es das geschlechtsneutrale *they* und im Deutschen das geschlechtsneutrale Wort „Studierende“, was beim Schreiben inklusiver Texte hilft (Urchs et al., 2023).

**Grenzen**
- Plausibel klingende, aber falsche Antworten, Empfindlichkeit gegenüber Formulierungen, Weitschweifigkeit und Raten statt Nachfragen (OpenAI, 2022).
- Prompts mit Geschlechtsangabe lösen schablonenhafte Antworten aus, und gendergerechte Sprache im Deutschen wird oft falsch verwendet (Urchs et al., 2023).
- Antworten unterscheiden sich bei identischen Prompts, und unangekündigte Systemupdates können bewährte Prompts unbrauchbar machen (Urchs et al., 2023).

### Vergleich

| System | Wofür gebaut | Interaktion |
|--------|--------------|-------------|
| GPT-3 | Hochskaliertes GPT-2 für Zero- und Few-Shot-Nutzung (Urchs et al., 2023) | Prompting eines Modells |
| InstructGPT | Einer Anweisung im Prompt folgen und ausführlich antworten (OpenAI, 2022) | Einzelne Anweisung und Antwort |
| ChatGPT | Gespräch, aus GPT-3.5 mit RLHF feinabgestimmt (OpenAI, 2022) | Dialog über mehrere Runden in einer Chat-Oberfläche |

### In der Praxis

Antworten taugen nur als grober Entwurf und müssen gründlich korrekturgelesen werden, weil Fehler in einem überwiegend korrekten Text schwer zu finden sind (Urchs et al., 2023). Für gendergerechte deutsche Ausgaben muss der Prompt selbst gendergerechte Sprache verwenden (Urchs et al., 2023). Da identische Prompts unterschiedliche Antworten liefern und Systemupdates das Verhalten ändern, müssen bewährte Prompts nach einem Update erneut auf verzerrte Ausgaben geprüft werden (Urchs et al., 2023). Systematische Ansätze für Prompts behandelt [[prompt-engineering|Prompt Engineering]], die Urheberrechtsfragen, die Modelle wie ChatGPT aufwerfen, [[copyright-and-ai-training-data|Urheberrecht und KI-Trainingsdaten]].

### Merksatz

ChatGPT ist ein GPT-3.5-Modell, das mit RLHF für Dialoge feinabgestimmt und über eine einfache Chat-Oberfläche angeboten wurde; diese Oberfläche brachte große Sprachmodelle in die breite Öffentlichkeit, deren Vertrauen in natürlich klingende Antworten eine sorgfältige Prüfung auf Fehler und Verzerrungen unerlässlich macht.

### Quellen

- OpenAI (2022). *Introducing ChatGPT.* 30. November 2022. [openai.com](https://openai.com/index/chatgpt/)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* NeurIPS 2022. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
