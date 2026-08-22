---
name: feedback-commit-includes-push
description: "Pushing no longer deploys — EC2 deploys are manual. Pushing to main is fine again; still commit only what's approved."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5c171053-81dc-40eb-a35d-b8d83ca4cc34
  modified: 2026-08-21T20:57:45.582Z
---

**Pushing does not deploy.** The game runs on an EC2 staging instance with no CD
set up. Tim deploys by hand: SSH in, shut everything down, `git pull`, start back
up. So pushing to `main` is safe and can be done freely when a commit is approved.

**Why:** stated 2026-08-21, replacing the Railway-era rule where a push to `main`
redeployed the live instance. The commit that moved the target is `88e4d12`
"Railway is no longer the deployment target".

**How to apply:** still commit only what has been approved, and stage only the
files belonging to that change — Tim usually has unrelated work in progress in the
same tree. Report branch + short SHA. Ask before pushing only when the change is
one he may want to sit on, not as a standing rule. Game-repo changes still need
explicit board approval per change (see [[CLAUDE.md]]), and destructive git
operations still need their own in-conversation approval.
Related: [[feedback_terse_confirmations]].
