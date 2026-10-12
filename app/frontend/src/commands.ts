// The chat commands /new-application, /new-round and /retro: invoked without arguments,
// the app asks step by step for what it needs (architecture-private-repo.md).
import { Application, Interviewer, Language } from "./api";

export type CommandName = "/new-application" | "/new-round" | "/retro" | "/prep";

export const COMMANDS: Record<CommandName, Record<Language, string>> = {
  "/new-application": { de: "neue Bewerbung: Firma, Stelle, erste Runde", en: "new application: company, role, first round" },
  "/new-round": { de: "weitere Runde einer bestehenden Bewerbung", en: "further round of an existing application" },
  "/retro": { de: "Nachbereitung eines Gesprächs", en: "debrief after an interview" },
  "/prep": { de: "Vorbereitung auf eine Runde (prep.md)", en: "preparation for a round (prep.md)" },
};

export interface Choice {
  label: string;
  value: string;
}

type Answers = Record<string, string>;
type Text = Record<Language, string> | ((answers: Answers, language: Language) => string);

export interface Step {
  key: string;
  prompt: Text;
  optional?: boolean;
  choices?: Choice[];
  validate?: (answer: string) => Record<Language, string> | null;
  // Asked only when this returns true for the answers so far.
  when?: (answers: Answers) => boolean;
}

const YES_NO: Choice[] = [
  { label: "Ja / Yes", value: "yes" },
  { label: "Nein / No", value: "no" },
];

/** The index of the next step to ask at or after `index`, skipping steps whose condition fails. */
export function nextStep(wizard: Wizard, index: number): number {
  let next = index;
  while (next < wizard.steps.length && wizard.steps[next].when && !wizard.steps[next].when!(wizard.answers)) next += 1;
  return next;
}

export interface Wizard {
  command: CommandName;
  steps: Step[];
  index: number;
  answers: Answers;
}

export const SKIP = "-";
const YES = "yes";

const DATE = /^(\d{4}-\d{2}-\d{2}|\d{1,2}\.\d{1,2}\.\d{2,4})$/;
function validDate(answer: string) {
  return answer === SKIP || DATE.test(answer.trim())
    ? null
    : { de: "Bitte als 20.10.2026 oder 2026-10-20 angeben, oder - für unbekannt.", en: "Please give it as 2026-10-20 or 20.10.2026, or - for unknown." };
}

export function text(value: Text, answers: Answers, language: Language): string {
  return typeof value === "function" ? value(answers, language) : value[language];
}

export function value(answers: Answers, key: string): string {
  const answer = (answers[key] ?? "").trim();
  return answer === SKIP ? "" : answer;
}

/** "Jane Doe – Head of Data Science – NLP", one person per line. */
export function parseInterviewers(answer: string): Interviewer[] {
  if (answer.trim() === SKIP) return [];
  return answer
    .split("\n")
    .map((line) => line.split(/\s+[–—-]\s+|\s*;\s*/).map((part) => part.trim()))
    .filter((parts) => parts[0])
    .map(([name, role = "", focus = ""]) => ({ name, role, focus }));
}

// Company and interviewer research runs in the refresh after saving (research.py).
const RESEARCH = {
  de: "Danach recherchiert Claude öffentliche, berufliche Informationen zu Firma und Personen, die noch nicht recherchiert sind. Dafür verlassen nur die Namen den Rechner (ohne API-Schlüssel entfällt der Schritt; Budget 3 €/Monat).",
  en: "Claude then looks up public, professional information on the company and on people not researched yet. Only the names leave this machine (skipped without an API key; budget 3 € a month).",
};

const confirm = (summary: (answers: Answers, language: Language) => string): Step => ({
  key: "confirm",
  prompt: (answers, language) =>
    `${summary(answers, language)}\n\n${language === "de" ? "Speichern?" : "Save?"}`,
  choices: [
    { label: "Ja / Yes", value: YES },
    { label: "Abbrechen / Cancel", value: "no" },
  ],
});

const roundSteps = (): Step[] => [
  {
    key: "round_date",
    prompt: { de: "Wann ist die Runde? (z. B. 20.10.2026; - wenn noch unbekannt)", en: "When is the round? (e.g. 2026-10-20; - if not known yet)" },
    optional: true,
    validate: validDate,
  },
  {
    key: "round_known",
    prompt: {
      de: "Weißt du schon etwas über die Runde, etwa wer das Gespräch führt oder wie es abläuft?",
      en: "Do you know anything about the round yet, such as who interviews or the format?",
    },
    choices: YES_NO,
  },
  {
    key: "interviewers",
    prompt: {
      de: "Wer führt das Gespräch? Eine Person pro Zeile: „Name – Rolle – Schwerpunkt“ (Rolle und Schwerpunkt optional). Nur, was du schon weißt; - wenn niemand bekannt ist.",
      en: "Who interviews? One person per line: “Name – role – focus” (role and focus optional). Only what you know now; - if nobody is known.",
    },
    optional: true,
    when: (answers) => answers.round_known === "yes",
  },
  {
    key: "round_notes",
    prompt: { de: "Was ist zur Runde schon bekannt (Format, Ort, Dauer …)? - zum Überspringen.", en: "Anything known about the round (format, place, length …)? - to skip." },
    optional: true,
    when: (answers) => answers.round_known === "yes",
  },
];

function interviewerSummary(answers: Answers, language: Language): string {
  const people = parseInterviewers(answers.interviewers ?? SKIP);
  if (!people.length) return language === "de" ? "keine bekannt" : "none known";
  return people.map((p) => [p.name, p.role, p.focus].filter(Boolean).join(", ")).join("; ");
}

function applicationChoices(applications: Application[]): Choice[] {
  return applications.map((a) => ({ label: `${a.company_name} – ${a.role_title}`, value: `${a.company}/${a.role}` }));
}

function roundChoices(applications: Application[], language: Language): Choice[] {
  return applications.flatMap((a) =>
    a.rounds
      .filter((r) => !r.has_retro)
      .map((r) => ({
        label: `${a.company_name} – ${a.role_title} – ${language === "de" ? "Runde" : "round"} ${r.number}${r.date ? ` (${r.date})` : ""}`,
        value: `${a.company}/${a.role}/${r.number}`,
      })),
  );
}

function prepChoices(applications: Application[], language: Language): Choice[] {
  return applications.flatMap((a) =>
    a.rounds.map((r) => ({
      label: `${a.company_name} – ${a.role_title} – ${language === "de" ? "Runde" : "round"} ${r.number}${r.date ? ` (${r.date})` : ""}${
        r.has_prep ? (language === "de" ? " · Vorbereitung vorhanden" : " · prep exists") : ""
      }`,
      value: `${a.company}/${a.role}/${r.number}`,
    })),
  );
}

/** The wizard for a command, or the reason it cannot start. */
export function startWizard(command: CommandName, applications: Application[], language: Language): Wizard | string {
  if (command === "/prep") {
    const rounds = prepChoices(applications, language);
    if (!rounds.length) {
      return language === "de" ? "Es gibt noch keine Runde. Lege eine Bewerbung mit /new-application an." : "There is no round yet. Start an application with /new-application.";
    }
    return {
      command,
      index: 0,
      answers: {},
      steps: [
        {
          key: "round",
          prompt: {
            de: "Für welche Runde? Das lokale Modell braucht etwa eine Minute.",
            en: "For which round? The local model needs about a minute.",
          },
          choices: rounds,
        },
        {
          key: "practice",
          prompt: {
            de: "Sollen zusätzlich Übungsfragen erstellt werden, die dir im Gespräch gestellt werden könnten? (dauert etwas länger)",
            en: "Also write practice questions you might be asked in the interview? (takes a little longer)",
          },
          choices: YES_NO,
        },
      ],
    };
  }
  if (command === "/new-application") {
    return {
      command,
      index: 0,
      answers: {},
      steps: [
        { key: "company_name", prompt: { de: "Bei welcher Firma?", en: "Which company?" } },
        { key: "industry", prompt: { de: "Branche? (- zum Überspringen)", en: "Industry? (- to skip)" }, optional: true },
        { key: "role_title", prompt: { de: "Welche Stelle (Titel der Anzeige)?", en: "Which role (title of the posting)?" } },
        {
          key: "posting_text",
          prompt: { de: "Füge bitte den Text der Stellenanzeige ein.", en: "Please paste the text of the job posting." },
        },
        { key: "posting_url", prompt: { de: "Link zur Anzeige? (- zum Überspringen)", en: "Link to the posting? (- to skip)" }, optional: true },
        {
          key: "cv_text",
          prompt: {
            de: "Füge den Lebenslauf ein, mit dem du dich beworben hast (als Text). /prep stützt die Kurzvorstellung darauf. - zum Überspringen.",
            en: "Paste the CV you applied with (as text). /prep backs the self-introduction with it. - to skip.",
          },
          optional: true,
        },
        ...roundSteps(),
        confirm((answers, language) =>
          language === "de"
            ? `**${answers.company_name}** – ${answers.role_title}\nErste Runde: ${value(answers, "round_date") || "Datum offen"}; Gesprächspartner: ${interviewerSummary(answers, language)}.\nDie Anforderungen der Anzeige liest danach das lokale Modell aus. ${RESEARCH.de}`
            : `**${answers.company_name}** – ${answers.role_title}\nFirst round: ${value(answers, "round_date") || "date open"}; interviewers: ${interviewerSummary(answers, language)}.\nThe local model then extracts the posting's requirements. ${RESEARCH.en}`,
        ),
      ],
    };
  }
  if (command === "/new-round") {
    if (!applications.length) {
      return language === "de" ? "Es gibt noch keine Bewerbung. Lege zuerst eine mit /new-application an." : "There is no application yet. Start one with /new-application.";
    }
    return {
      command,
      index: 0,
      answers: {},
      steps: [
        { key: "application", prompt: { de: "Für welche Bewerbung?", en: "For which application?" }, choices: applicationChoices(applications) },
        ...roundSteps(),
        confirm((answers, language) => {
          const chosen = applications.find((a) => `${a.company}/${a.role}` === answers.application);
          const next = (chosen?.rounds.length ?? 0) + 1;
          return language === "de"
            ? `**${chosen?.company_name} – ${chosen?.role_title}**, Runde ${next}: ${value(answers, "round_date") || "Datum offen"}; Gesprächspartner: ${interviewerSummary(answers, language)}.\n${RESEARCH.de}`
            : `**${chosen?.company_name} – ${chosen?.role_title}**, round ${next}: ${value(answers, "round_date") || "date open"}; interviewers: ${interviewerSummary(answers, language)}.\n${RESEARCH.en}`;
        }),
      ],
    };
  }
  const rounds = roundChoices(applications, language);
  const scheduled: Record<string, boolean> = Object.fromEntries(
    applications.flatMap((a) => a.rounds.map((r) => [`${a.company}/${a.role}/${r.number}`, !!r.date])),
  );
  if (!rounds.length) {
    return language === "de" ? "Es gibt keine Runde ohne Retro. Neue Runden legst du mit /new-round an." : "There is no round without a retro. Add rounds with /new-round.";
  }
  return {
    command,
    index: 0,
    answers: {},
    steps: [
      { key: "round", prompt: { de: "Zu welchem Gespräch?", en: "Which interview?" }, choices: rounds },
      {
        key: "date",
        prompt: { de: "Wann war es? (- für heute)", en: "When was it? (- for today)" },
        optional: true,
        validate: validDate,
        // A round with a scheduled date keeps it; the draft can still be edited.
        when: (answers) => !scheduled[answers.round],
      },
      {
        key: "questions_asked",
        prompt: {
          de: "Welche Fragen wurden dir gestellt, fachlich wie persönlich? Schreib einfach drauflos; - wenn es keine gab.",
          en: "Which questions were you asked, technical or personal? Just write freely; - if there were none.",
        },
        optional: true,
      },
      {
        key: "company_told",
        prompt: {
          de: "Was hat die Firma über sich, das Team und die Stelle erzählt? Wird wörtlich übernommen und in der Firmennotiz ergänzt. - zum Überspringen.",
          en: "What did the company tell about itself, the team and the role? Kept verbatim and added to the company note. - to skip.",
        },
        optional: true,
      },
      { key: "struggled_with", prompt: { de: "Wobei bist du ins Schwimmen gekommen?", en: "What did you struggle with?" }, optional: true },
      { key: "personal_improvement", prompt: { de: "Was willst du beim nächsten Mal besser machen?", en: "What do you want to do better next time?" }, optional: true },
      {
        key: "kb_gaps_identified",
        prompt: {
          de: "Welche Themen sollte die Wissensbasis besser abdecken? Sie gehen als Suchbegriffe an das wöchentliche Monitoring (nur die Themennamen).",
          en: "Which topics should the knowledge base cover better? They go to the weekly monitoring as search phrases (topic names only).",
        },
        optional: true,
      },
      { key: "reflection", prompt: { de: "Sonst noch Gedanken zum Gespräch? (- zum Überspringen)", en: "Any other thoughts on the interview? (- to skip)" }, optional: true },
    ],
  };
}

export function retroDate(wizard: Wizard, applications: Application[]): string | null {
  const own = value(wizard.answers, "date");
  if (own) return own;
  const [company, role, number] = (wizard.answers.round ?? "").split("/");
  const application = applications.find((a) => a.company === company && a.role === role);
  return application?.rounds.find((r) => String(r.number) === number)?.date ?? null;
}

export function confirmed(wizard: Wizard): boolean {
  return wizard.answers.confirm === YES;
}
