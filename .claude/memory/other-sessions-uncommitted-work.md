---
name: other-sessions-uncommitted-work
description: "Uncommitted changes in a repo may belong to another session in flight — never commit them, and don't offer to"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25438ffb-5927-4494-bbfa-cce458e38867
  modified: 2026-10-02T22:45:11.585Z
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

**The index is shared too.** Anything left staged — including what `git mv` stages on its own — goes
into whichever session commits next (2026-10-02: a staged rename landed in another session's survival
commit). Stage only at the moment of committing. Where a file also holds another session's hunks,
build the commit from a temporary index (`GIT_INDEX_FILE`, `read-tree HEAD`, `update-index
--cacheinfo` with your content), then `git reset -q -- <your paths>` to sync the shared index.

Commit the component you are working in, not the whole repo. A change you make in another component
along the way is committed as you go, once Tim approves it, so the working tree stays clear for other
sessions rather than accumulating your edits across the repo.

Scope is what the task named, and it is not a claim on the area — the next session may be asked to
work in the same component, or in a different one, and neither is an intrusion. Related:
[[confirm-before-crossing-repos]], [[feedback-never-refactor-dependencies-unasked]],
[[feedback_no_troubleshooting_relics]].
