---
name: design-docs-live-in-the-design-repo
description: "Where FCM system-design documentation lives: the design repo, cloned into the umbrella root as design/ (kebab-case). Reusable libraries document themselves in their own docs/."
metadata: 
  node_type: memory
  type: project
  originSessionId: 16e9c7ed-12cb-4a3e-9ec8-f18634b22440
  modified: 2026-09-23T17:37:27.356Z
---

FCM system-design documentation lives in the **`design` repo**, cloned into the umbrella root as
`design/` (kebab-case filenames). The overview is `design/design-overview.md`; the catalogue is
`design/INDEX.md`.

This is where the docs live, not what they are current for — the corpus documents the legacy game and
is frozen: [[design-repo-not-maintained-for-rebuild]].

**How to apply:**
- Read and edit design docs in `design/`. It is its own git repo — commit and push it there, not
  through the umbrella (the umbrella gitignores it).
- **Reusable libraries self-document**: each `libraries/evennia-*` repo holds its own `docs/` (an
  `INDEX.md` + kebab-case topic files) so the library reads in isolation — a deliberate exception to the
  one-wiki-surface rule. `design/INDEX.md` lists them under "Self-documenting sub-repos."
- Known wrong reference to fix if touched: `src/game/server/conf/settings.py` points at
  `design/DEPLOYMENT.md`; that doc is at `ops/DEVELOPMENT/DEPLOYMENT.md`.
