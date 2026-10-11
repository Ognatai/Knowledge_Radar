export type Scope = "all" | "public" | "private";
export type Language = "de" | "en";

export interface Turn {
  role: "user" | "assistant";
  content: string;
}

export interface ChatSource {
  number: number;
  note: string;
  title: string;
  heading: string;
  visibility: "public" | "private";
  text: string;
  score: number;
}

export interface ChatAnswer {
  answer: string;
  sources: ChatSource[];
  facts: string[];
  unavailable: string[];
}

// Public notes open on the published site; private documents have no public address.
export const PUBLIC_SITE = "https://ognatai.github.io/Knowledge_Radar/";

export function publicNoteUrl(slug: string): string {
  return `${PUBLIC_SITE}?view=note&slug=${encodeURIComponent(slug)}`;
}

export interface Interviewer {
  name: string;
  role: string;
  focus: string;
}

export interface RoundInfo {
  number: number;
  date: string | null;
  has_retro: boolean;
  has_prep: boolean;
}

export interface Application {
  company: string;
  company_name: string;
  role: string;
  role_title: string;
  rounds: RoundInfo[];
}

export interface RefreshStatus {
  state: "idle" | "running" | "done" | "failed";
  message: string;
  log: string[];
}

export interface Written {
  files: string[];
  refresh: RefreshStatus | null;
}

async function call<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(path, body === undefined ? undefined : {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const data = await response.json();
      detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail ?? data);
    } catch {
      // not JSON; keep the status line
    }
    throw new Error(detail);
  }
  return response.json();
}

export const privateApi = {
  applications: () => call<{ configured: boolean; applications: Application[] }>("/api/private/applications"),
  newApplication: (body: unknown) => call<Written>("/api/private/applications", body),
  newRound: (body: unknown) => call<Written>("/api/private/rounds", body),
  draftRetro: (body: unknown) => call<{ text: string }>("/api/private/retro/draft", body),
  saveRetro: (body: unknown) => call<Written>("/api/private/retro", body),
  draftPrep: (body: unknown) => call<{ text: string; exists: boolean }>("/api/private/prep/draft", body),
  savePrep: (body: unknown) => call<Written>("/api/private/prep", body),
  refresh: () => call<RefreshStatus | null>("/api/private/refresh"),
};

export function ask(question: string, history: Turn[], scope: Scope, language: Language): Promise<ChatAnswer> {
  return call<ChatAnswer>("/api/chat", { question, history, scope, language });
}

export type DraftStatus = "open" | "wanted" | "discarded";

export interface DraftSummary {
  slug: string;
  kind: string;
  new_note: boolean;
  verdicts: string;
  status: DraftStatus;
}

export interface ProposalRun {
  run: string;
  branch: string;
  created: string;
  drafts: DraftSummary[];
}

export interface InboxBranch {
  branch: string;
  files: { path: string; title: string; text: string }[];
}

export interface ReviewOverview {
  public: { available: boolean; runs: ProposalRun[] };
  private: { configured: boolean; branches: InboxBranch[]; error: string | null };
}

export const reviewApi = {
  overview: () => call<ReviewOverview>("/api/review"),
  draft: (run: string, slug: string) => call<{ review: string; diff: string; draft: string }>(`/api/review/public/${run}/${slug}`),
  decide: (run: string, slug: string, status: DraftStatus) => call<{ status: string }>(`/api/review/public/${run}/${slug}`, { status }),
  removeRun: (run: string) => call<{ removed: string }>(`/api/review/public/${run}`, {}),
  accept: (branch: string) => call<Written>("/api/review/private/accept", { branch }),
  discard: (branch: string) => call<{ discarded: string }>("/api/review/private/discard", { branch }),
};
