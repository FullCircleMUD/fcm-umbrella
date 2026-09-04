---
name: libraries_commit_straight_to_main
description: Libraries under libraries/ commit and push straight to main — no branches until they stabilise into production
metadata: 
  node_type: memory
  type: project
  originSessionId: 4afd8299-0aa5-4091-8c8e-e5fd1dee1126
  modified: 2026-09-01T19:36:39.732Z
---

Commit and push straight to `main` in the `libraries/` repos. No feature branches, no PRs.

**Why:** none of them is in production. They are early enough that a lot will change before anything
stabilises, and branch overhead buys nothing against a repo with one author and no deployed consumer.

**How to apply:** don't offer to branch, and don't treat committing to `main` as needing a caveat. This
supersedes the general "branch first on the default branch" default, for these repos only. Approval to
commit is still per-request — this covers *where* the commit goes, not *whether* to make one.

Changes once a library stabilises into production, at which point branches and proper change control
start. `src/game` is already there: see [[feedback_work_on_dev_branch]].
