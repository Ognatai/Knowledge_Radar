> **Important notice:** This page is an LLM-generated summary. It may be incomplete, outdated or wrong. It is not legal advice and has no legal effect; only the German text published in the Federal Law Gazette (Bundesgesetzblatt) is authentic. The English text is an unofficial translation.

### TL;DR

The German Trade Secrets Act (Gesetz zum Schutz von Geschäftsgeheimnissen, GeschGehG) transposes Directive (EU) 2016/943 on the protection of undisclosed know-how. Information is protected only if it is not generally known and therefore of economic value, there is a legitimate interest in keeping it confidential and the holder has taken reasonable confidentiality measures (section 2). The Act sets out which acts are permitted (such as independent development and reverse engineering, section 3) and which are prohibited (section 4), exempts whistleblowing and journalism (section 5) and gives the holder claims for injunctions, destruction, recall, information and damages. Special confidentiality rules apply in court proceedings, and intentional infringements are criminal offences.

### Key facts

| | |
| --- | --- |
| Official reference | Gesetz zum Schutz von Geschäftsgeheimnissen, BGBl. I 2019, 466 |
| Type and jurisdiction | German federal act; transposes Directive (EU) 2016/943 |
| Signed | 18 April 2019 |
| Entry into force | 26 April 2019; replaces the criminal provisions of sections 17 to 19 of the Act against Unfair Competition (UWG) |
| Competent authorities | no supervisory authority; enforcement through the civil courts (exclusively the regional courts, section 15) and criminal prosecution (section 23) |
| Version summarised | version of 18 April 2019; the Act has not been amended since |

### Scope

**What** (section 2 no. 1): trade secrets of all kinds, such as technical know-how, formulas, source code, customer lists, business strategies or data, provided the three conditions are met. Without reasonable confidentiality measures (technical, organisational, contractual) there is no protection.

**Who**: the holder is whoever has lawful control over the trade secret (section 2 no. 2); claims are directed against the infringer (section 2 no. 3) and in some cases against the owner of the business for which the infringer works (section 12).

**Precedence and boundaries** (section 1): public-law confidentiality rules take precedence; freedom of expression and of the media, collective bargaining autonomy, employee rights and professional secrecy under section 203 of the Criminal Code remain unaffected.

**Structure**: four divisions: general provisions (sections 1–5), claims in case of infringement (sections 6–14), procedure in trade secret litigation (sections 15–22) and criminal provisions (section 23).

<!-- PROVISIONS -->

### Timeline

| Date | Event |
| --- | --- |
| 8 June 2016 | Adoption of Directive (EU) 2016/943; transposition deadline 9 June 2018 |
| 18 April 2019 | GeschGehG signed |
| 26 April 2019 | Entry into force |

### Enforcement and penalties

- **Civil claims** (sections 6–13): removal and injunction, destruction, surrender, recall and withdrawal of infringing products from the market, information and damages, calculated on the basis of actual loss, the infringer's profit or a reasonable licence fee; claims are excluded where disproportionate (section 9), and abusive claims are inadmissible (section 14).
- **Confidentiality in court** (sections 16–20): the court can classify information as confidential and restrict access; breaches can lead to a coercive fine of up to **EUR 100,000** or coercive detention of up to six months (section 17).
- **Criminal offence** (section 23): imprisonment of up to **three years** or a fine, up to **five years** for commercial-scale acts or use abroad; attempts are punishable, and as a rule the offence is prosecuted only on request.

### Relationship to other acts

- **[[data-act|Data Act]]**: where data must be shared, trade secrets are to be preserved through confidentiality measures; data holders may refuse sharing in exceptional cases.
- **[[eu-ai-act|EU AI Act]]**: authorities must keep trade secrets confidential; the summary of training data of general-purpose AI models takes into account the interest in protecting trade secrets.
- **[[gdpr|GDPR]]**: data subjects' rights of access must not adversely affect the rights of others, including trade secrets; conversely, a trade secret does not justify refusing all information.
- **[[copyright-and-ai-training-data|Copyright and AI training data]]**: copyright protects works regardless of secrecy; the GeschGehG also protects information that is not protected by copyright, but only as long as it is kept secret.

### Relevance for AI development

- **Models, weights and training data as trade secrets** (section 2 no. 1): model weights, training datasets, architecture details or system prompts can be protected if they are not generally known and are reasonably secured, for instance through access restrictions and confidentiality agreements. Publishing them as open source ends the protection.
- **Reverse engineering** (section 3(1) no. 2): studying and testing publicly available products is permitted; for lawfully possessed products only if there is no duty to restrict acquisition. Terms of use that prohibit, for example, extracting models through an API can therefore be decisive.
- **Infringing products** (section 2 no. 4, section 7): an AI model or product whose design or functioning is based to a significant extent on an unlawfully acquired trade secret may be subject to claims for recall, destruction and withdrawal from the market.
- **Inputs into external AI services**: if staff enter confidential information into external AI tools, this may breach confidentiality obligations and call the reasonable confidentiality measures into question; businesses therefore regulate this in policies and contracts.
- **Whistleblowing** (section 5 no. 2): disclosing trade secrets to reveal unlawful practices, including in the training or use of AI systems, can be justified.

### Official sources

- [GeschGehG on gesetze-im-internet.de (German)](https://www.gesetze-im-internet.de/geschgehg/)
