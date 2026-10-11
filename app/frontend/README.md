# Local app frontend

React UI of the local app, served by nginx in Docker together with the FastAPI
backend (`docker-compose.yml`, started by `scripts/start-app.ps1`) on
`http://127.0.0.1:8080`, bound to `localhost` only. The public note browser lives
in `app/site/`.

- **Chat** over the public and the private index (`POST /api/chat`), with the
  sources of every answer. The conversation lives in the browser tab only.
- **Review Dashboard** for the weekly proposal branches: planned.

Development: `npm install`, then `npm run dev` (port 5173; `/api` is proxied to
the API on port 8000).
