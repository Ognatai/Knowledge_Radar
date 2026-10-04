# Public static site

Static React site for GitHub Pages with no backend, cookies, or analytics. It loads
`public/data/site-data.json`, which is generated (not committed) by
`python -m app.backend.knowledge_radar.site_export` from `public/notes/` only.

- Graph view (`react-force-graph-2d`): entities by default, toggle to show notes;
  filter by entity type; click a node to open its note or the auto-generated
  stub view.
- Text view: rendered notes with sources, `[[wikilinks]]`, and backlinks. The original
  source text of regulatory notes is shown in both languages, never translated.
- DE/EN toggle (`react-i18next`); client-side full-text search (MiniSearch),
  limited to the active language.

```powershell
npm install
npm run dev     # after running the export once
npm run build   # output: dist/
```
