---
name: doc-conventions-home
description: Documentation conventions live in docs/doco-structure.md; the doc-convention-auditor enforces them
metadata: 
  node_type: memory
  type: project
  originSessionId: b3bba4c6-d5c8-403d-8943-4b214af2df80
---

Documentation conventions for FCM are captured in **`docs/doco-structure.md`** (the
"Conventions for `docs/` documents" section). When a new doc convention is agreed,
record it there — that file is the single source of truth for doc rules.

The **`doc-convention-auditor`** agent enforces what `doco-structure.md` specifies:
the doc is the *spec*, the auditor is the *enforcer*. Keep the auditor reading from
`doco-structure.md` rather than carrying its own private rule list, so the rules
have one home and can't drift between doc and agent. The deterministic, mechanical
subset is checked by the [[doc-convention-linter]] skill.

Example convention captured this way (2026-06-19): third-party/dependency code
(e.g. Evennia) is cited as an inline-code path relative to that package's own root
(`` `evennia/objects/objects.py` ``), never as a working link into `src/venv/`.

See also [[design-docs-in-umbrella]].
