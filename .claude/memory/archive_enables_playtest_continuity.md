---
name: archive-enables-playtest-continuity
description: "Why the archive exists: rebuild the world freely without playtesters losing their investment. From alpha, archive.db3 / xrpl.db3 / subscriptions.db3 are never deleted."
metadata: 
  node_type: memory
  type: project
  originSessionId: 54aaf291-e083-4c0c-88f7-bccc200ec8d0
  modified: 2026-08-25T20:32:52.369Z
---

The recovery system exists so Tim can **reload the whole world at will** — to ship new
content, clear stale data, or chase a leak — without playtesters starting from zero.
Stated 2026-08-25, on the day the account and character recovery path was proven live.

**Why it matters:** invited playtesters are the audience from alpha onward. If a world
rebuild costs them their account, characters and progression, they feel the loss of
investment and stop testing. The archive makes a rebuild invisible to them.

**How to apply — two tiers of database:**

- **Disposable:** `evennia.db3`. Rebuilt from YAML whenever needed. Holds nothing that
  cannot be regenerated.
- **Permanent:** `archive.db3` (who players are, what they built), `xrpl.db3` (what they
  own), `subscriptions.db3` (payments and spent trials). Not derivable from anything
  else. From alpha these are never deleted, and in production they get backups and
  restore procedures. `ai_memory.db3` sits between — regenerable in principle, but losing
  it is a visible quality regression.

**The one combination that corrupts data:** deleting `evennia.db3` *and* `archive.db3`
while keeping `xrpl.db3`. A new character then takes a reused name and inherits the
previous holder's `character_key` rows. Wipe all three or none. Wallet-keyed data
(`location=ACCOUNT`) is immune; only `character_key` can be adopted by a stranger.

Related: [[feedback_no_legacy_data_concerns]].
