# MCP

MCP servers and protocol integrations live here.

## RSS server

`rss_server.py` serves the curated RSS/Atom feeds of `sources.yaml` (lab blogs,
YouTube channels, conferences, newsletters, regulatory feeds) to any MCP client.
It is built on the official MCP Python SDK (`mcp`), reuses the monitoring
agents' feed parser and keyword filters, and only reads.

| Tool | What it returns |
|---|---|
| `list_feeds(category?)` | The curated feeds with category, source kind and tier |
| `get_feed_items(feed, days=7, limit=20)` | Recent items of one feed, newest first |
| `search_feed_items(query, days=14, category?, limit=20)` | Recent items of all feeds containing every word of the query; unreachable feeds are listed under `errors` |

Feeds are cached for ten minutes per server process.

Run it over stdio:

```powershell
python -m app.mcp.rss_server
```

To use it in Claude Code, from the repository root:

```powershell
claude mcp add knowledge-radar-rss -- .venv\Scripts\python.exe -m app.mcp.rss_server
```
