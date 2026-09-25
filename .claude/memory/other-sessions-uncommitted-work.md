---
name: other-sessions-uncommitted-work
description: "Uncommitted changes in a repo may belong to another session in flight — never commit them, and don't offer to"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25438ffb-5927-4494-bbfa-cce458e38867
  modified: 2026-09-23T20:34:51.687Z
---

Sessions run in parallel in the same repo. A dirty working tree is normal and most of it is not yours.
Commit only the files your own task touched; leave every other modified or untracked path alone, and
do not offer to include them.

**Why:** in-flight work is often half-built — one half of a pair present, a README still `[TBD]`,
tests not run. Committing it ships something broken under someone else's name, and a push cannot be
taken back without a force push.

**How to apply:** before committing, list the paths your task actually touched and stage those
explicitly (`git add <path>`), never `git add -A` or `git add .`. Say plainly in the report which
paths you left and that they are another session's. Do not ask whether to include them — if Tim wants
them in, he will say so. "Sweep it all up" means your work, not everyone's.

Scope is what the task named, and it is not a claim on the area — the next session may be asked to
work in the same component, or in a different one, and neither is an intrusion. Related:
[[confirm-before-crossing-repos]], [[feedback-never-refactor-dependencies-unasked]],
[[feedback_no_troubleshooting_relics]].
