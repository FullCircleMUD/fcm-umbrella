---
name: feedback-commit-includes-push
description: "Approval to commit includes approval to push — don't stop for a second confirmation between the two."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d071573e-c5fd-48e2-8692-c0d228c411dc
  modified: 2026-08-10T02:15:50.584Z
---

When the user approves a commit, push it in the same step. Don't commit, report, and then wait for a separate "push it" — treat the two as one approved action.

**Why:** stated directly after I committed the umbrella docs, pushed, and then offered to hold pushes in future — "commit and push is fine". The same round-trip had already happened on the `src/game` fix, where the user had to come back with "push it please".

**How to apply:** on approval, commit and push, then report both in one line (branch + short SHA + remote result). This does not loosen the two rules that still gate the commit itself: game-repo changes need explicit board approval per change (see [[CLAUDE.md]]), and destructive git operations always need their own in-conversation approval. It only removes the extra confirmation step between an approved commit and its push. Related: [[feedback-terse-confirmations]].
