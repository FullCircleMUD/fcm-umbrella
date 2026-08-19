---
name: feedback-commit-includes-push
description: "In src/game, pushing is deploying — commit when approved, but never push until Tim says so."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5c171053-81dc-40eb-a35d-b8d83ca4cc34
  modified: 2026-08-18T15:34:41.533Z
---

**In the `src/game` repo, a push to `main` redeploys the live instance.** Pushes
to other branches do not deploy. Regardless of branch: commit when a commit is
approved, then stop and report. Never push until Tim explicitly says to push.

**Why:** stated 2026-08-18 after I committed the delayed-attack guard and pushed
it in the same step — "it is the push that deploys... so commit, do not push
until I say so". Tim also wants fixes proven on the dev instance before they
reach the staging instance he is playtesting on, and an unrequested push can put
them there ahead of that.

**How to apply:** on approval, commit and report branch + short SHA + "not
pushed". Wait for an explicit push instruction. This sits on top of the rules
that gate the commit itself: game-repo changes need explicit board approval per
change (see [[CLAUDE.md]]), and destructive git operations always need their own
in-conversation approval. Related: [[feedback_terse_confirmations]].
