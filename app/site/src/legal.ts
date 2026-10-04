/**
 * Legal pages of the public site (Markdown). The German text is authoritative.
 *
 * `TODO(...)` marks information only the operator can provide or must verify.
 * The site shows such pages as drafts, and the Pages workflow refuses to deploy
 * while any marker is left (see .github/workflows/pages.yml).
 */

export interface LegalPage {
  id: string;
  title_en: string;
  title_de: string;
  body_en: string;
  body_de: string;
}

export const TODO_MARKER = "TODO(";

export const isDraft = (page: LegalPage) =>
  page.body_de.includes(TODO_MARKER) || page.body_en.includes(TODO_MARKER);

const GERMAN_AUTHORITATIVE = "*This English version is a courtesy translation; the German version is authoritative.*";

export const legalPages: LegalPage[] = [
  {
    id: "imprint",
    title_en: "Imprint",
    title_de: "Impressum",
    body_de: `### Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)

TODO(Vor- und Nachname)  
TODO(Straße und Hausnummer)  
TODO(Postleitzahl und Ort)  
Deutschland

### Kontakt

E-Mail: TODO(E-Mail-Adresse)

### Verantwortlich für den Inhalt nach § 18 Abs. 2 Medienstaatsvertrag (MStV)

TODO(Vor- und Nachname, Anschrift wie oben; prüfen, ob diese Angabe für die Seite erforderlich ist)
`,
    body_en: `${GERMAN_AUTHORITATIVE}

### Information pursuant to Section 5 of the German Digital Services Act (DDG)

TODO(first and last name)  
TODO(street and house number)  
TODO(postcode and city)  
Germany

### Contact

Email: TODO(email address)

### Responsible for content pursuant to Section 18(2) of the German Interstate Media Treaty (MStV)

TODO(first and last name, address as above; verify whether this statement is required)
`,
  },
  {
    id: "contact",
    title_en: "Contact",
    title_de: "Kontakt",
    body_de: `Fragen, Hinweise auf Fehler in einer Notiz und Rückmeldungen zur Barrierefreiheit bitte per E-Mail an TODO(E-Mail-Adresse).

Die Seite hat kein Kontaktformular und keine Kommentarfunktion. Wie Nachrichten verarbeitet werden, steht in der [Datenschutzerklärung](?view=legal&id=privacy).
`,
    body_en: `Questions, reports of errors in a note and feedback on accessibility: please email TODO(email address).

The site has no contact form and no comment function. How messages are processed is described in the [privacy policy](?view=legal&id=privacy).
`,
  },
  {
    id: "privacy",
    title_en: "Privacy",
    title_de: "Datenschutz",
    body_de: `### 1. Verantwortliche Stelle

Verantwortlich für die Verarbeitung personenbezogener Daten auf dieser Website ist die im [Impressum](?view=legal&id=imprint) genannte Person.

### 2. Hosting über GitHub Pages

Die Website ist eine statische Seite und wird über GitHub Pages bereitgestellt. Für Nutzerinnen und Nutzer im Europäischen Wirtschaftsraum ist GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Niederlande, verantwortlich. Beim Aufruf einer GitHub-Pages-Seite wird laut GitHub die IP-Adresse der Besucherin oder des Besuchers zu Sicherheitszwecken protokolliert und gespeichert, unabhängig davon, ob sie oder er bei GitHub angemeldet ist.

Rechtsgrundlage ist Art. 6 Abs. 1 Buchst. f DSGVO; das berechtigte Interesse liegt in der sicheren und zuverlässigen Bereitstellung der Website. Dabei können Daten in die USA übermittelt werden. GitHub ist nach eigenen Angaben nach dem EU-U.S. Data Privacy Framework zertifiziert (Angemessenheitsbeschluss nach Art. 45 DSGVO) und stützt Übermittlungen zusätzlich auf Standardvertragsklauseln.

Weitere Informationen: [GitHub-Datenschutzerklärung](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) und [Hinweise zu GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

TODO(Hosting-Angaben vor Veröffentlichung mit den dann aktuellen GitHub-Bedingungen abgleichen)

### 3. Keine Cookies, keine Analyse, keine Inhalte Dritter

Diese Website setzt keine Cookies, speichert keine Daten in Ihrem Browser und verwendet keine Analyse- oder Tracking-Werkzeuge. Schriften, Skripte und Daten werden ausschließlich von dieser Website selbst geladen; es werden keine Inhalte von Drittanbietern eingebunden. Suche, Graph und Sprachwechsel laufen vollständig in Ihrem Browser.

### 4. Links zu anderen Websites

Die Notizen verlinken auf ihre Quellen und weitere Websites. Erst wenn Sie einen solchen Link anklicken, werden Daten an den jeweiligen Anbieter übertragen; für dessen Verarbeitung ist dieser Anbieter verantwortlich.

### 5. Kontakt per E-Mail

Wenn Sie eine E-Mail schreiben, werden Ihre Adresse und der Inhalt der Nachricht verarbeitet, um Ihr Anliegen zu beantworten (Art. 6 Abs. 1 Buchst. f DSGVO). Die Nachricht wird gelöscht, wenn sie erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.

### 6. Ihre Rechte

Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 Buchst. f (Art. 21). Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO), zum Beispiel bei TODO(zuständige Aufsichtsbehörde am Wohnsitz des Betreibers, etwa das Bayerische Landesamt für Datenschutzaufsicht).

Stand: TODO(Datum der Veröffentlichung)
`,
    body_en: `${GERMAN_AUTHORITATIVE}

### 1. Controller

The controller for the processing of personal data on this website is the person named in the [imprint](?view=legal&id=imprint).

### 2. Hosting on GitHub Pages

This website is a static site served by GitHub Pages. For users in the European Economic Area, the responsible entity is GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, the Netherlands. According to GitHub, when a GitHub Pages site is visited, the visitor's IP address is logged and stored for security purposes, regardless of whether the visitor is signed in to GitHub.

The legal basis is Art. 6(1)(f) GDPR; the legitimate interest is the secure and reliable provision of the website. Data may be transferred to the United States. GitHub states that it is certified under the EU-U.S. Data Privacy Framework (adequacy decision under Art. 45 GDPR) and additionally relies on standard contractual clauses.

More information: [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) and [about GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

TODO(check the hosting details against GitHub's terms current at publication)

### 3. No cookies, no analytics, no third-party content

This website sets no cookies, stores no data in your browser and uses no analytics or tracking tools. Fonts, scripts and data are loaded only from this website itself; no third-party content is embedded. Search, graph and language switching run entirely in your browser.

### 4. Links to other websites

The notes link to their sources and to other websites. Data is transferred to the respective provider only when you click such a link; that provider is responsible for its processing.

### 5. Contact by email

If you send an email, your address and the content of your message are processed to answer your request (Art. 6(1)(f) GDPR). The message is deleted once it has been dealt with, unless statutory retention obligations apply.

### 6. Your rights

You have the right of access (Art. 15 GDPR), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and to object to processing based on Art. 6(1)(f) (Art. 21). You may also lodge a complaint with a data protection supervisory authority (Art. 77 GDPR), for example TODO(competent supervisory authority).

Last updated: TODO(date of publication)
`,
  },
  {
    id: "accessibility",
    title_en: "Accessibility",
    title_de: "Barrierefreiheit",
    body_de: `TODO(prüfen, ob für diese Website eine gesetzliche Pflicht zur Barrierefreiheit oder zu einer Erklärung besteht; die folgende Erklärung ist als freiwillige Erklärung formuliert)

Diese Website soll für möglichst alle Menschen nutzbar sein. Ziel sind die Anforderungen der Web Content Accessibility Guidelines (WCAG) 2.2 auf Stufe AA.

### Umgesetzt

- Bedienung vollständig per Tastatur, mit sichtbarem Fokus und einem Link „Zum Inhalt springen“
- semantische Gliederung mit Überschriften, Landmarken und einem Inhaltsverzeichnis je Notiz
- Sprachauszeichnung der Seite (Deutsch/Englisch) und des deutschen Originaltexts von Rechtsquellen
- Berücksichtigung der Systemeinstellung für reduzierte Bewegung
- Inhalte und Suche ohne Anmeldung, ohne Cookies und ohne Zeitlimits

### Bekannte Einschränkungen

- Der interaktive Graph ist eine Grafik (Canvas) und mit Screenreadern nicht nutzbar. Alle Knoten des Graphen stehen deshalb zusätzlich als Liste unter dem Graphen zur Verfügung, und alle Notizen sind über die Notizliste und die Suche erreichbar.
- Die Notizen werden mit Sprachmodellen erstellt und behandeln Fachthemen; sie sind nicht in Leichter oder Einfacher Sprache verfasst.
- TODO(Ergebnis einer Prüfung der Barrierefreiheit eintragen, z. B. Selbstbewertung nach WCAG 2.2, mit Datum)

### Rückmeldung

Wenn Sie auf Barrieren stoßen, schreiben Sie bitte über die [Kontaktseite](?view=legal&id=contact).
`,
    body_en: `${GERMAN_AUTHORITATIVE}

TODO(verify whether a legal accessibility obligation or statement applies to this website; the statement below is written as a voluntary one)

This website aims to be usable by as many people as possible. The target is conformance with the Web Content Accessibility Guidelines (WCAG) 2.2, level AA.

### Implemented

- fully keyboard-operable, with a visible focus and a "skip to content" link
- semantic structure with headings, landmarks and a table of contents per note
- language markup of the page (English/German) and of the German original text of legal sources
- respect for the system setting for reduced motion
- content and search without sign-in, cookies or time limits

### Known limitations

- The interactive graph is a canvas graphic and cannot be used with screen readers. All nodes of the graph are therefore also available as a list below the graph, and all notes can be reached via the note list and the search.
- The notes are generated with language models and cover specialised topics; they are not written in plain language.
- TODO(add the result of an accessibility review, e.g. a WCAG 2.2 self-assessment, with date)

### Feedback

If you encounter barriers, please get in touch via the [contact page](?view=legal&id=contact).
`,
  },
  {
    id: "sources",
    title_en: "Sources and use",
    title_de: "Quellen und Nutzung",
    body_de: `### Wie die Notizen entstehen

Die Notizen werden mit Hilfe von Sprachmodellen auf Grundlage der jeweils angegebenen Quellen erstellt und vor der Veröffentlichung geprüft. Sie können dennoch unvollständig, veraltet oder falsch sein. Maßgeblich sind immer die verlinkten Quellen.

### Keine Rechtsberatung

Notizen zu Gesetzen und Regulierung sind Zusammenfassungen zu Informationszwecken. Sie sind keine Rechtsberatung und keine verbindliche Auslegung. Rechtlich maßgeblich sind allein die amtlich veröffentlichten Texte, für das Unionsrecht die im Amtsblatt der Europäischen Union veröffentlichten Fassungen.

### Lizenz

Code und Notizen dieser Website stehen unter der [MIT-Lizenz](https://github.com/Ognatai/Knowledge_Radar/blob/main/LICENSE). Für die verlinkten Quellen gelten deren eigene Bedingungen.

### Zitierte amtliche Texte

Zitate aus Rechtsakten der Europäischen Union stammen von EUR-Lex; die Weiterverwendung ist nach dem Beschluss 2011/833/EU der Kommission zulässig. Deutsche Gesetze sind als amtliche Werke nach § 5 Urheberrechtsgesetz nicht urheberrechtlich geschützt.

### Fehler melden

Hinweise auf Fehler bitte über die [Kontaktseite](?view=legal&id=contact).
`,
    body_en: `${GERMAN_AUTHORITATIVE}

### How the notes are made

The notes are generated with the help of language models based on the sources cited in each note and reviewed before publication. They may nevertheless be incomplete, outdated or wrong. The linked sources always take precedence.

### No legal advice

Notes on laws and regulation are summaries for information purposes. They are not legal advice and not a binding interpretation. Only the officially published texts are legally authoritative; for Union law, the versions published in the Official Journal of the European Union.

### Licence

The code and notes of this website are released under the [MIT licence](https://github.com/Ognatai/Knowledge_Radar/blob/main/LICENSE). The linked sources are subject to their own terms.

### Quoted official texts

Quotations from legal acts of the European Union are taken from EUR-Lex; their reuse is permitted under Commission Decision 2011/833/EU. German statutes are official works and, under Section 5 of the German Copyright Act, not protected by copyright.

### Reporting errors

Please report errors via the [contact page](?view=legal&id=contact).
`,
  },
];
