---
name: logging-migration-pass-pending
description: "Tim will migrate all libraries to evennia-logging-extension, newest first — not a session's job to start"
metadata: 
  node_type: memory
  type: project
  originSessionId: f7d8cab1-b454-46a6-b725-7b76d2d34e2c
  modified: 2026-09-11T13:14:41.345Z
---

The corpus-wide logging migration (every library's hand-rolled `log.py` → three-line bind through `evennia-logging-extension`) is Tim's own pass, run once he's satisfied the standards are settled: newest libraries first (least refactor), oldest last. Decided 2026-09-10.

**Why:** the linter now reports 16 `log_shim_mechanism` errors and 17 `log_dependency_undeclared` warns — that is the pass's work queue, not defects to fix opportunistically.

**How to apply:** don't migrate a library's logging unless asked. Known items for the pass: `evennia-ai-memory` has the module-scope `from .log import` cycle in `config.py`; `evennia-database-cascade`'s CLAUDE.md principle 8 ("cannot log") is disproven and needs rewriting; `evennia-yaml-reader` likely gets a documented exception. `evennia-targeting` migrated 2026-09-11 (binding only, no call sites — see [[library-no-logging-evennia-targeting]]). `evennia-archive` migrated 2026-09-11 (phase 1 + live-validated; phase 2 boot logging not discussed).

The logging extension's own `interoperability.md` is deliberately left stale during the pass — Tim updates it in one sweep after all libraries are converted (decided 2026-09-11). Don't fix its per-library entries piecemeal.
