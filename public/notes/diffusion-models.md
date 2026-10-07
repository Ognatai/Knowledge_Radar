---
title_en: Diffusion Models
title_de: Diffusionsmodelle
entity_type: Method
sources:
- https://arxiv.org/abs/1503.03585
- https://arxiv.org/abs/2006.11239
- https://arxiv.org/abs/2011.13456
- https://arxiv.org/abs/2112.10752
- https://arxiv.org/abs/2207.12598
- https://arxiv.org/abs/1406.2661
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Diffusion models generate data by learning to reverse a gradual noising process: a fixed forward process slowly destroys the structure of the data by adding noise, and a neural network learns the reverse process that restores it step by step (Sohl-Dickstein et al., 2015; Ho et al., 2020). They reached state-of-the-art image quality (Ho et al., 2020; Song et al., 2020), run efficiently in the latent space of an autoencoder (Rombach et al., 2021) and are steered by text or other conditions with guidance (Ho & Salimans, 2022).

### How it works

During training, noise of a random strength is added to a training example and the network learns to predict and remove it. To generate, the model starts from pure noise and denoises it over many steps, optionally guided by a condition such as a text prompt.

```text
1. Forward and reverse process
▼
2. Training as denoising
▼
3. Continuous-time view
▼
4. Latent diffusion
▼
5. Conditioning and guidance
```

#### 1. Forward and reverse process

Sohl-Dickstein et al. (2015), inspired by non-equilibrium statistical physics, systematically and slowly destroy structure in a data distribution through an iterative forward diffusion process, and then learn a reverse diffusion process that restores structure in the data. This yields a generative model that is both highly flexible and tractable.

#### 2. Training as denoising

Ho et al. (2020) obtained high-quality image synthesis by training on a weighted variational bound derived from a connection between diffusion models and denoising score matching with Langevin dynamics; in practice the network learns to predict the noise added to an image. On unconditional CIFAR-10 they reached an Inception score of 9.46 and a state-of-the-art FID of 3.17, and on 256×256 LSUN sample quality similar to ProgressiveGAN.

#### 3. Continuous-time view

Song et al. (2020) describe the noising as a stochastic differential equation that slowly turns data into a known prior distribution, and generation as the corresponding reverse-time equation, which depends only on the score, the gradient of the log density of the perturbed data. Neural networks estimate this score, and numerical solvers generate samples. The framework unifies earlier score-based and diffusion models, adds an equivalent ODE that allows exact likelihood computation, and reached an Inception score of 9.89 and FID of 2.20 on CIFAR-10.

#### 4. Latent diffusion

Diffusion models operating directly on pixels are expensive: training can consume hundreds of GPU days, and sampling requires many sequential evaluations (Rombach et al., 2021). Latent diffusion models apply diffusion in the latent space of a powerful pretrained autoencoder, which greatly reduces computation while preserving detail ([[autoencoders-and-gans|Autoencoders and GANs]]). Cross-attention layers make them flexible generators for conditions such as text or bounding boxes and enable high-resolution synthesis.

#### 5. Conditioning and guidance

Classifier guidance trades off diversity and sample fidelity in conditional diffusion models by combining the model's score with the gradient of a separately trained classifier (Ho & Salimans, 2022). Classifier-free guidance avoids the extra classifier: a conditional and an unconditional diffusion model are trained jointly, and their score estimates are combined to reach a similar trade-off between sample quality and diversity.

#### Origin and variants

Diffusion probabilistic models were introduced by Sohl-Dickstein et al. (2015), made competitive for images by Ho et al. (2020), unified with score-based models through stochastic differential equations by Song et al. (2020), made efficient by latent diffusion (Rombach et al., 2021) and made controllable by classifier-free guidance (Ho & Salimans, 2022). They compete with GANs (Goodfellow et al., 2014) for image generation.

### When to use it

- When high-quality, diverse samples are needed, for example images (Ho et al., 2020; Song et al., 2020).
- When generation should follow a text prompt or another condition (Rombach et al., 2021; Ho & Salimans, 2022).
- When fast single-step generation matters more than sample quality, GANs may be preferable (Goodfellow et al., 2014).

### Strengths and limitations

**Strengths**
- State-of-the-art sample quality on image benchmarks (Ho et al., 2020; Song et al., 2020).
- Flexible and tractable generative models (Sohl-Dickstein et al., 2015).
- Conditioning via cross-attention and guidance without retraining for each condition (Rombach et al., 2021; Ho & Salimans, 2022).

**Limitations**
- Sampling requires many sequential network evaluations (Rombach et al., 2021).
- Training pixel-space models can take hundreds of GPU days (Rombach et al., 2021).
- Guidance trades diversity for fidelity (Ho & Salimans, 2022).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| GAN | One-step generator trained against a discriminator (Goodfellow et al., 2014) | Fast sampling |
| Pixel-space diffusion | Iterative denoising of images (Ho et al., 2020) | Highest sample quality, small images |
| Latent diffusion | Diffusion in an autoencoder's latent space (Rombach et al., 2021) | High-resolution, text-conditioned images |
| Score-based SDE models | Continuous-time noising and reverse SDE (Song et al., 2020) | Unified framework, exact likelihoods via ODE |

### In practice

Text-to-image systems typically use latent diffusion with cross-attention to a text encoder (Rombach et al., 2021) and classifier-free guidance to control how closely images follow the prompt (Ho & Salimans, 2022). Sample quality is measured with metrics such as FID and Inception score (Ho et al., 2020), and multimodal systems combine such generators with vision-language models ([[multimodal-models|Multimodal Models]]).

### Key takeaway

Diffusion models generate data by learning to remove noise step by step; latent diffusion and guidance make them efficient and controllable.

### Sources

- Sohl-Dickstein, J. et al. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics.* ICML 2015. [arXiv:1503.03585](https://arxiv.org/abs/1503.03585)
- Ho, J. et al. (2020). *Denoising Diffusion Probabilistic Models.* NeurIPS 2020. [arXiv:2006.11239](https://arxiv.org/abs/2006.11239)
- Song, Y. et al. (2020). *Score-Based Generative Modeling through Stochastic Differential Equations.* ICLR 2021. [arXiv:2011.13456](https://arxiv.org/abs/2011.13456)
- Rombach, R. et al. (2021). *High-Resolution Image Synthesis with Latent Diffusion Models.* CVPR 2022. [arXiv:2112.10752](https://arxiv.org/abs/2112.10752)
- Ho, J. & Salimans, T. (2022). *Classifier-Free Diffusion Guidance.* [arXiv:2207.12598](https://arxiv.org/abs/2207.12598)
- Goodfellow, I. J. et al. (2014). *Generative Adversarial Networks.* NeurIPS 2014. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Diffusionsmodelle erzeugen Daten, indem sie lernen, einen schrittweisen Verrauschungsprozess umzukehren: Ein fester Vorwärtsprozess zerstört die Struktur der Daten langsam durch hinzugefügtes Rauschen, und ein neuronales Netz lernt den Rückwärtsprozess, der sie Schritt für Schritt wiederherstellt (Sohl-Dickstein et al., 2015; Ho et al., 2020). Sie erreichten Spitzenqualität bei Bildern (Ho et al., 2020; Song et al., 2020), laufen effizient im latenten Raum eines Autoencoders (Rombach et al., 2021) und lassen sich mit Guidance durch Text oder andere Bedingungen steuern (Ho & Salimans, 2022).

### Funktionsweise

Beim Training wird einem Trainingsbeispiel Rauschen zufälliger Stärke hinzugefügt, und das Netz lernt, es vorherzusagen und zu entfernen. Zum Erzeugen beginnt das Modell mit reinem Rauschen und entrauscht es über viele Schritte, optional gesteuert durch eine Bedingung wie einen Text-Prompt.

```text
1. Vorwärts- und Rückwärtsprozess
▼
2. Training als Entrauschen
▼
3. Zeitkontinuierliche Sicht
▼
4. Latent Diffusion
▼
5. Conditioning und Guidance
```

#### 1. Vorwärts- und Rückwärtsprozess

Sohl-Dickstein et al. (2015), angeregt von der statistischen Physik des Nichtgleichgewichts, zerstören die Struktur einer Datenverteilung systematisch und langsam durch einen iterativen Vorwärts-Diffusionsprozess und lernen dann einen Rückwärts-Diffusionsprozess, der die Struktur wiederherstellt. So entsteht ein generatives Modell, das zugleich sehr flexibel und handhabbar ist.

#### 2. Training als Entrauschen

Ho et al. (2020) erzielten hochwertige Bildsynthese, indem sie auf einer gewichteten variationellen Schranke trainierten, die aus einer Verbindung zwischen Diffusionsmodellen und Denoising Score Matching mit Langevin-Dynamik folgt; praktisch lernt das Netz, das einem Bild hinzugefügte Rauschen vorherzusagen. Auf unbedingtem CIFAR-10 erreichten sie einen Inception Score von 9,46 und einen damals besten FID von 3,17, auf LSUN mit 256×256 Pixeln eine Qualität ähnlich ProgressiveGAN.

#### 3. Zeitkontinuierliche Sicht

Song et al. (2020) beschreiben das Verrauschen als stochastische Differentialgleichung, die Daten langsam in eine bekannte Prior-Verteilung überführt, und das Erzeugen als die zugehörige zeitlich rückwärts laufende Gleichung, die nur vom Score abhängt, dem Gradienten der logarithmierten Dichte der verrauschten Daten. Neuronale Netze schätzen diesen Score, und numerische Löser erzeugen die Beispiele. Der Ansatz vereint frühere score-basierte und Diffusionsmodelle, ergänzt eine gleichwertige gewöhnliche Differentialgleichung, die eine exakte Likelihood-Berechnung erlaubt, und erreichte auf CIFAR-10 einen Inception Score von 9,89 und einen FID von 2,20.

#### 4. Latent Diffusion

Diffusionsmodelle, die direkt auf Pixeln arbeiten, sind teuer: Das Training kann Hunderte GPU-Tage beanspruchen, und das Erzeugen erfordert viele aufeinanderfolgende Auswertungen (Rombach et al., 2021). Latent-Diffusion-Modelle wenden die Diffusion im latenten Raum eines leistungsfähigen vortrainierten Autoencoders an, was den Rechenaufwand stark verringert und Details erhält ([[autoencoders-and-gans|Autoencoder und GANs]]). Cross-Attention-Schichten machen sie zu flexiblen Generatoren für Bedingungen wie Text oder Begrenzungsrahmen und ermöglichen hochaufgelöste Synthese.

#### 5. Conditioning und Guidance

Classifier Guidance wägt bei bedingten Diffusionsmodellen Vielfalt gegen Wiedergabetreue ab, indem der Score des Modells mit dem Gradienten eines separat trainierten Klassifikators kombiniert wird (Ho & Salimans, 2022). Classifier-free Guidance kommt ohne zusätzlichen Klassifikator aus: Ein bedingtes und ein unbedingtes Diffusionsmodell werden gemeinsam trainiert, und ihre Score-Schätzungen werden kombiniert, um eine ähnliche Abwägung zwischen Qualität und Vielfalt zu erreichen.

#### Ursprung und Varianten

Diffusionsmodelle wurden von Sohl-Dickstein et al. (2015) eingeführt, von Ho et al. (2020) für Bilder konkurrenzfähig gemacht, von Song et al. (2020) über stochastische Differentialgleichungen mit score-basierten Modellen vereint, durch Latent Diffusion effizient (Rombach et al., 2021) und durch Classifier-free Guidance steuerbar (Ho & Salimans, 2022). Bei der Bilderzeugung konkurrieren sie mit GANs (Goodfellow et al., 2014).

### Wann einsetzen

- Wenn hochwertige, vielfältige Beispiele gebraucht werden, etwa Bilder (Ho et al., 2020; Song et al., 2020).
- Wenn die Erzeugung einem Text-Prompt oder einer anderen Bedingung folgen soll (Rombach et al., 2021; Ho & Salimans, 2022).
- Wenn schnelle Erzeugung in einem Schritt wichtiger ist als die Qualität, können GANs vorzuziehen sein (Goodfellow et al., 2014).

### Stärken und Grenzen

**Stärken**
- Spitzenqualität der Beispiele auf Bild-Benchmarks (Ho et al., 2020; Song et al., 2020).
- Flexible und zugleich handhabbare generative Modelle (Sohl-Dickstein et al., 2015).
- Steuerung über Cross-Attention und Guidance ohne Neutraining für jede Bedingung (Rombach et al., 2021; Ho & Salimans, 2022).

**Einschränkungen**
- Das Erzeugen erfordert viele aufeinanderfolgende Netzauswertungen (Rombach et al., 2021).
- Das Training von Modellen im Pixelraum kann Hunderte GPU-Tage dauern (Rombach et al., 2021).
- Guidance tauscht Vielfalt gegen Wiedergabetreue (Ho & Salimans, 2022).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| GAN | Generator in einem Schritt, trainiert gegen einen Diskriminator (Goodfellow et al., 2014) | Schnelles Erzeugen |
| Diffusion im Pixelraum | Iteratives Entrauschen von Bildern (Ho et al., 2020) | Höchste Qualität, kleine Bilder |
| Latent Diffusion | Diffusion im latenten Raum eines Autoencoders (Rombach et al., 2021) | Hochaufgelöste, textgesteuerte Bilder |
| Score-basierte SDE-Modelle | Zeitkontinuierliches Verrauschen und Rückwärts-SDE (Song et al., 2020) | Einheitlicher Rahmen, exakte Likelihood über ODE |

### In der Praxis

Text-zu-Bild-Systeme nutzen meist Latent Diffusion mit Cross-Attention zu einem Text-Encoder (Rombach et al., 2021) und Classifier-free Guidance, um zu steuern, wie eng die Bilder dem Prompt folgen (Ho & Salimans, 2022). Die Qualität der Beispiele wird mit Metriken wie FID und Inception Score gemessen (Ho et al., 2020), und multimodale Systeme verbinden solche Generatoren mit Vision-Language-Modellen ([[multimodal-models|Multimodale Modelle]]).

### Merksatz

Diffusionsmodelle erzeugen Daten, indem sie lernen, Rauschen Schritt für Schritt zu entfernen; Latent Diffusion und Guidance machen sie effizient und steuerbar.

### Quellen

- Sohl-Dickstein, J. et al. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics.* ICML 2015. [arXiv:1503.03585](https://arxiv.org/abs/1503.03585)
- Ho, J. et al. (2020). *Denoising Diffusion Probabilistic Models.* NeurIPS 2020. [arXiv:2006.11239](https://arxiv.org/abs/2006.11239)
- Song, Y. et al. (2020). *Score-Based Generative Modeling through Stochastic Differential Equations.* ICLR 2021. [arXiv:2011.13456](https://arxiv.org/abs/2011.13456)
- Rombach, R. et al. (2021). *High-Resolution Image Synthesis with Latent Diffusion Models.* CVPR 2022. [arXiv:2112.10752](https://arxiv.org/abs/2112.10752)
- Ho, J. & Salimans, T. (2022). *Classifier-Free Diffusion Guidance.* [arXiv:2207.12598](https://arxiv.org/abs/2207.12598)
- Goodfellow, I. J. et al. (2014). *Generative Adversarial Networks.* NeurIPS 2014. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661)
