---
name: feedback-commit-side-work-hold-main-body
description: Current practice — commit each side change to another component as it finishes; the main body of work rides uncommitted until it is stable
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6eb3c265-c48c-4bae-ac31-82de2775d8ce
  modified: 2026-10-04T15:15:20.706Z
---

While building one main body of work (e.g. the chargen component), a change it needs in another component — a signal, a receiver, a helper — is committed and pushed as soon as it is green and its README is updated. The main body stays uncommitted until it reaches a stable, finished, working state, then goes in as one body of work.

**Why:** other sessions work in those other components; small side changes left uncommitted cause them conflicts. The main body is this session's own area. (Tim, 2026-10-04.)

**How to apply:** finish a side unit (tests green, plan lints, README) → ask to commit and push it, then return to the main body. Don't ask to commit the main body piecemeal. Anything committed must not import uncommitted code, or `main` breaks for everyone else. Related: [[feedback-one-commit-per-component]], [[other-sessions-uncommitted-work]].
