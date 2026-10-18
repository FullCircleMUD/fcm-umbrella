---
name: feedback-no-legacy-data-concerns
description: "Never raise legacy/existing-data concerns for FCM — pre-alpha, fresh DB every deploy; no backfills, no pre-existing-row caveats, until a live production deployment exists"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c41cb4a-335c-4edf-8beb-92321dc36d13
  modified: 2026-10-18T17:45:11.988Z
---

**Do not raise existing-database or legacy-data impact** as a consideration for any FCM
change — stale rows, orphaned records, "objects created before this attribute existed",
backfilling an attribute onto existing rows, "is there a live DB still carrying X", data
a removed cleanup mechanism might strand. Confirmed 2026-08-03, re-confirmed emphatically
2026-08-25.

This is **not scoped to one workstream**. It was first stated during shards work and
re-stated during the archive work; it applies to all FCM development.

**Why:** FCM is pre-alpha. Every local test begins by redeploying a fresh database, and
each deployment replaces the previous one wholesale. There is no legacy data and there
never has been, so raising it adds friction to every decision without informing it.

**How to apply:** weigh only current and future correctness. Never propose a backfill for
a newly added attribute, and never caveat a change with "objects created before this
won't have it" — every object will be created after it. **Before any database or schema
work, ask Tim explicitly: "Greenfield, or does this stack on a previous deployment?"** — every time,
because at some point it stops being greenfield. Greenfield means regenerate the migrations as a fresh
`0001_initial`, never stack one that builds a table then rebuilds it (Tim, 2026-10-07). **Every schema
change while greenfield folds into the one `0001_initial`** — never `makemigrations` a `0002`. Restore any
hand edit the old `0001` carried (evennia-ai-memory reads its vector width at apply time). Tim drops and
redeploys the databases in this phase; extra migration files wait for real data to carry. Broken
2026-10-17/18 with evennia-ai-memory's 0003 and 0004, squashed back the same day. Playtest and
staging are both dropped and re-migrated, so the xrpl seed is greenfield too (Tim, 2026-10-07). Holds **until there is a live
production deployment carrying real player data**, after which existing-data impact
becomes real again. Distinct from [[feedback_stop_on_each_problem]] (surface findings one
at a time) — this is about which findings are worth surfacing at all.
