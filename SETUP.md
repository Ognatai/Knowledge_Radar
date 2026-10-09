# Setup

This is the reproducible setup for anyone cloning this repository. It runs on a
single machine, is free, and uses local models only (Ollama); no Claude/API key
is needed. Without a private repository configured, everything operates on the
public notes only.

Requirements: Python 3.11+, Node.js 20.19+ (or 22.12+), Git. Optional: Ollama,
Docker Desktop.

## 1. Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## 2. Enable the pre-commit hook

The hook blocks commits that contain absolute local paths, paths into the
private repository, symlinks, or private-data patterns:

```powershell
git config core.hooksPath .githooks
```

Optional: put additional private-data regexes (one per line, e.g. company
names) into `.knowledge-radar/private-patterns.txt`. That directory is
untracked, so the patterns never enter this public repository.

## 3. Validate notes and run the tests

```powershell
python -m app.agents.validate_notes
python -m pytest
```

## 4. Public static site

The site is built from a JSON export of `public/notes/` and needs no backend:

```powershell
python -m app.backend.knowledge_radar.site_export   # writes app/site/public/data/site-data.json
Set-Location app\site
npm install
npm run dev        # development server on http://127.0.0.1:5173
npm run build      # static build in app/site/dist
```

In VS Code: **Terminal: Run Task → Knowledge Radar: Public site (dev)** exports
the data and starts the development server.

To test exactly what would be published, run **Knowledge Radar: Public site
(production preview)**: it exports the data, builds the site and serves
`app/site/dist` on `http://127.0.0.1:4173`.

Publishing is manual: the workflow `.github/workflows/pages.yml` runs the same
export and build and deploys `app/site/dist` to GitHub Pages only when started
via **Actions → Deploy public site → Run workflow** (repository settings:
**Pages → Source** set to **GitHub Actions**). It is deliberately not triggered
by merges until the site, including its legal pages, is cleared for
publication.

## 5. Local app API

```powershell
uvicorn app.backend.knowledge_radar.api:app --reload
```

The API listens on `http://127.0.0.1:8000` (documentation at `/docs`). With
Docker Desktop running, `docker compose up --build` starts the same API, bound
to `localhost` only. The chat and Review Dashboard UI are not implemented yet.

## 6. Ollama

Install Ollama on the host (it is not containerized). Models:

| Use | Model | Machine in this project's deployment |
| --- | --- | --- |
| Chat (local app) | `ollama pull qwen3.5:4b` | ThinkPad (CUDA) |
| Agent pipeline (extraction) | `ollama pull qwen3:30b-a3b` | Desktop (AMD, Vulkan) |

On a single machine, pull whichever fits your GPU. In VS Code, **Knowledge
Radar: Ollama chat** opens an interactive session with a model of your choice.

### AMD GPUs on Windows

On the Desktop (Radeon RX 7900 XT, 20 GB), `scripts\start-ollama.ps1` starts
Ollama with the Vulkan backend and a q8_0 KV cache, for the Ollama processes
only. Under ROCm, decode speed fell from about 110 to 18 tokens/s as the context
grew to 14k tokens; Vulkan keeps about 30 tokens/s, and the smaller cache lets
`qwen3:30b-a3b` with a 24k context fit completely into VRAM. To use it at logon,
replace Ollama's own autostart shortcut:

```powershell
$startup = [Environment]::GetFolderPath('Startup')
Move-Item "$startup\Ollama.lnk" "$env:LOCALAPPDATA\Ollama\Ollama.lnk.bak"
$shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut("$startup\Ollama (Vulkan).lnk")
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PWD\scripts\start-ollama.ps1`" -Delay 20"
$shortcut.Save()
```

Ollama updates may restore `Ollama.lnk`; the script then replaces that instance
20 seconds after logon. Running the script by hand restarts Ollama the same way.

## 7. Optional: private repository

Copy `local-config.example.yaml` to `local-config.yaml` and set
`private_repo_path` to the absolute path of the private checkout. It must be a
sibling directory, never nested inside this repository; the app refuses a
nested path.

## 8. Optional: weekly monitoring job (Windows)

```powershell
.\scripts\register-scheduled-task.ps1 -DryRun   # show the task definition
.\scripts\register-scheduled-task.ps1           # register it for the current user
```

The task runs Sundays at 02:00 (or at the next opportunity if the machine was
off) as the logged-on user, which is required for toast notifications and for
reading secrets from the Windows Credential Manager. Every run writes a log to
`.knowledge-radar/logs/` and shows a toast on success and on failure.

## 9. GitHub repository settings

- **Secrets → Actions:** `KNOWLEDGE_RADAR_PRIVATE_PATTERNS`, newline-separated
  regexes for the CI private-data check (company names, interview markers, …).
- **Branch protection on `main`:** require pull requests and the CI checks.
- **Dependabot** is configured in `.github/dependabot.yml`.
