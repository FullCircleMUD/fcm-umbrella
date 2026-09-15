---
name: scaling-shard-first-boot-in-isolation
description: "A shard on a fresh database must be started normally in isolation first to create Account #1 and Limbo, then stopped, before server_start will work."
metadata: 
  node_type: memory
  type: project
  originSessionId: ec8709eb-feba-4e03-9ef4-988743d934bf
  modified: 2026-09-14T20:10:02.197Z
---

Under `evennia-scaling`, each shard runs its own game database. On a fresh one, boot it in this
order:

1. `evennia start --settings settings_shard0` — normal start, in isolation. Creates Account #1 and
   Limbo.
2. Shut it down.
3. `evennia server_start --settings settings_shard0` — attaches to the router's Portal.

**Why:** `server_start` runs a Server and speaks to no Portal, so it never reaches the initial-setup
path that creates the superuser and Limbo. Skip step 1 and the shard attaches to a database with no
`#1` and nowhere to put anyone.

**How to apply:** once per shard, per fresh database. `installing.md` documents only `server_start`
for a shard — this is the missing first boot. Credentials for local instances:
[[feedback_test_instance_credentials]].
