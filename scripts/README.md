# Scripts

Helpers for setting up and running Knowledge Radar on Windows (PowerShell), plus
the private-data check. Run them from the repository root. Secrets (Neo4j
passwords, GitLab token) are read from the Windows Credential Manager and are
never written to a file.

| Script | Purpose |
| --- | --- |
| `setup-local-app.ps1` | Sets up a machine for the local app from a fresh clone: checks prerequisites, clones the private repository, creates `.venv`, writes `local-config.yaml`, pulls the models, asks for missing secrets, builds the indices and starts the app. Safe to run again |
| `start-app.ps1` | Starts the local app (API, chat UI and both indices in Docker) and opens `http://127.0.0.1:8080`. `-NoPrivate` starts without the private index |
| `start-neo4j.ps1` | Starts the public local index (Neo4j in Docker, localhost only); `-Private` starts the separate private index |
| `start-ollama.ps1` | Starts Ollama with the settings the agent pipeline expects (GPU backend, quantised KV cache); can serve as the autostart entry |
| `run-monitoring.ps1` | The weekly monitoring run: starts Docker, Neo4j and Ollama if needed, runs `app.agents.monitoring.weekly`, writes a log to `.knowledge-radar/logs/` and shows a notification |
| `register-scheduled-task.ps1` | Registers `run-monitoring.ps1` as a weekly Windows Task Scheduler task from `scheduled_task.xml`; `-DryRun` prints the XML only |
| `check_private_leaks.py` | Fails if added content contains absolute local paths, paths into the private repository, symlinks or private-data patterns. Used by the pre-commit hook and in CI |

```powershell
.\scripts\start-app.ps1
python scripts\check_private_leaks.py --staged      # staged changes
python scripts\check_private_leaks.py --all         # all tracked files
```

Private-data patterns are never stored in this repository: they come from the
environment variable `KNOWLEDGE_RADAR_PRIVATE_PATTERNS` or the untracked file
`.knowledge-radar/private-patterns.txt` (one regex per line).
