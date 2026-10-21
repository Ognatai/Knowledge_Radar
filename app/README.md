# Application

The code of Knowledge Radar, in five parts:

| Folder | Contents |
| --- | --- |
| `backend/` | Python package `knowledge_radar`: loading and validating notes and the graph, the static-site export, the local indices (Neo4j), and the FastAPI backend of the local app |
| `site/` | The public static site (React), deployed to GitHub Pages |
| `frontend/` | The local app UI (React): chat, interview commands, Review Dashboard |
| `agents/` | The agent pipeline: note validation, extraction, entity resolution, linking, and the weekly monitoring run |
| `mcp/` | MCP servers |

Python modules are run from the repository root as modules, e.g.
`python -m app.agents.validate_notes`. See [SETUP.md](../SETUP.md) for how to
install and run everything.
