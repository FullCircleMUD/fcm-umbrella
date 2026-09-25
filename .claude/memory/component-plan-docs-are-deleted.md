---
name: component-plan-docs-are-deleted
description: "A working plan document is deleted before a component is called finished; only README, test-plan, tests and __init__ remain."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 20a5b4dc-8932-44b9-98c8-dce60087d6dd
  modified: 2026-09-24T15:26:08.775Z
---

A finished component carries four documents and no others: `README.md`, `test-plan.md`, `tests.py`
and `__init__.py` (plus its implementation modules). Any working plan, checklist or design note
written while building it gets deleted before the component is called finished.

**Why:** a plan is not a living document. Left behind it goes stale immediately and a later session
reads it as current intent, competing with the test plan — which is the one document that does
describe agreed behaviour and stays.

The same applies to a work list kept *inside* one of the four — most often as an "Open" section in
`test-plan.md` that has drifted from unresolved cases into general to-dos. That section is sanctioned
only for cases carrying a `[TBD]`; anything else in it is a plan in disguise.

**How to apply:** it is fine to keep a working plan while building, in a file or in a section. Clear
it as part of finalisation, before the README pass and the commit: every item becomes a case, moves
into the README, or is dropped. Stale entries for work already done are the signal it has drifted.
See [[feedback-code-before-docs]] and [[feedback_docs_short_and_plain]].
