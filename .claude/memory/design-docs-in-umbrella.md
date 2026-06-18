---
name: Design docs live in the umbrella docs/ (design repo superseded)
description: FCM system-design documentation now lives in FCM-umbrella/docs/ (kebab-case). The standalone `design` repo is superseded/deprecated — read and edit design docs in the umbrella, not the design repo. Reusable libraries document themselves in their own docs/.
type: project
---
FCM system-design documentation was migrated from the standalone `design` repo into the **umbrella**
at `FCM-umbrella/docs/` (kebab-case filenames; the design README was folded into
`docs/design-overview.md`). The umbrella `docs/` is now the **source of truth** for system design.

**How to apply:**
- Read and edit design docs in `FCM-umbrella/docs/`, **not** the standalone `design` repo. That repo
  is **superseded/deprecated** — kept for now as an archive (not deleted), left untouched.
- All cross-repo references to `design/*.md` were repointed to the umbrella `docs/` (in `src/game`,
  `ops`, `lore`).
- **Reusable libraries self-document**: each `libraries/evennia-*` repo documents itself in its own
  `docs/` (an `INDEX.md` + kebab-case topic files; renamed from `DESIGN/`). This is a deliberate
  exception to the umbrella's one-docs-surface rule so a library can be understood in isolation. The
  umbrella `docs/INDEX.md` lists these under "Self-documenting sub-repos."
- Known stale ref deliberately left as-is: `src/game/server/conf/settings.py` references
  `design/DEPLOYMENT.md`; that doc actually lives at `ops/DEVELOPMENT/DEPLOYMENT.md`.
