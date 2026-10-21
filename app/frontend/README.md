# Local app frontend

React UI of the local app. It is served by nginx in Docker together with the
FastAPI backend (`docker-compose.yml`, started by `scripts/start-app.ps1`) on
`http://127.0.0.1:8080` and is bound to `localhost` only. The public note browser
lives in `app/site/`.

- **Chat** over the public and the private index (`POST /api/chat`), with the
  sources of every answer. The conversation lives in the browser tab only.
- **Interview commands** `/new-application`, `/new-round`, `/retro`: guided
  dialogues that write the private repository and refresh the private index
  afterwards.
- **`/prep`**: a briefing for one interview round, saved as `prep.md` after
  editing.
- **Review Dashboard** (`src/Review.tsx`): the weekly run's drafts (keep or
  discard) and the private inbox branches (accept or discard).

Development:

```powershell
npm install
npm run dev     # port 5173; /api is proxied to the API on port 8000
```
