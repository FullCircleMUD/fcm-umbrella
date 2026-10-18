---
name: feedback-few-events-distinguished-by-payload
description: "Keep PerceptionEventType small — one general event, told apart by its payload, over a new type per skill or command"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d7e19f82-9bda-42ff-9273-76269da062b4
  modified: 2026-10-18T18:08:02.176Z
---

Current practice: keep the number of event types down, and tell cases apart by what the payload carries. A skill tried is `ACTOR_USED_SKILL` / `ACTOR_FAILED_SKILL` with `{"skill": <key>, ...}`, never an event per skill. A general command is `ACTOR_USED_COMMAND` with `{"command": <key>, ...}` — through `tell_room` or `tell_actor` alike; the event type never decides who is told (Tim, 2026-10-18).

**Why:** Tim (2026-10-13) — no separate "actor failed X" for every skill; nothing gains from the extra types.

**How to apply:** before proposing a new event, check whether an existing one plus a payload field covers it. Tim still places event types ([[tim-places-new-event-types]]).
