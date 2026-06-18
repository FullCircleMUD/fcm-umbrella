---
name: Design docs live in the umbrella docs/
description: FCM system-design documentation lives in FCM-umbrella/docs/ (kebab-case) — edit design docs there. Reusable libraries document themselves in their own docs/. The standalone design repo is a deprecated archive; do not edit it.
type: project
---
FCM system-design documentation lives in **`FCM-umbrella/docs/`** (kebab-case filenames) — the source
of truth for FCM system design. The overview is `docs/design-overview.md`; the catalogue is
`docs/INDEX.md`.

**How to apply:**
- Read and edit design docs in `FCM-umbrella/docs/`. The standalone `design` repo is a **deprecated
  archive** — do not edit design docs there.
- **Reusable libraries self-document**: each `libraries/evennia-*` repo holds its own `docs/` (an
  `INDEX.md` + kebab-case topic files) so the library reads in isolation — a deliberate exception to the
  umbrella's one-docs-surface rule. The umbrella `docs/INDEX.md` lists them under "Self-documenting
  sub-repos."
- Known wrong reference to fix if touched: `src/game/server/conf/settings.py` points at
  `design/DEPLOYMENT.md`; that doc is at `ops/DEVELOPMENT/DEPLOYMENT.md`.
