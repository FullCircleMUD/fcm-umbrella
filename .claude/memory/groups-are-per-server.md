---
name: groups-are-per-server
description: Group members are always on the same server; cross-shard travel (not built) is planned so a group never spans servers
metadata:
  node_type: memory
  type: project
  originSessionId: 14abcdd1-3175-40c5-bd72-a38e6fda5af3
  modified: 2026-09-28T22:45:31.097Z
---

A group never spans servers. Cross-shard travel is not built yet, and the current plan (2026-09-28) builds it so group members are always on one server.

**Why:** Tim stated it while designing experience shares — `member_instances` maps an off-server member to `None`, and he said not to filter for that.

**How to apply:** don't guard group code against off-server members (`None` in `member_instances`). If cross-shard travel lands differently, revisit. Related: [[shards-superseded-by-scaling]].
