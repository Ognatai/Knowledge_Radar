# Git hooks

Hooks that guard the boundary between this public repository and private data.
Enable them once per clone:

```powershell
git config core.hooksPath .githooks
```

- `pre-commit`: runs `scripts/check_private_leaks.py --staged` and blocks commits
  that contain absolute local paths, paths into the private repository, symlinks
  or private-data patterns.
- `pre-push`: refuses to push branches `proposals/*`. They hold unreviewed drafts
  of the weekly run, and every branch of a public repository is public.
