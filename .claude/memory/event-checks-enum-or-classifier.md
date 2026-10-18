---
name: event-checks-enum-or-classifier
description: General best practice for checking a PerceptionEvent — compare the enum when the type is the whole question; a classifier only when the check goes beyond the type.
metadata:
  node_type: memory
  type: project
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T13:58:30.939Z
---

General best practice, not a rule: when the event type is the whole question, compare `PerceptionEventType` directly (`event.type is ...`, or `in` a tuple). When the check needs more than the type — who the subject is, what the payload says — use a shared event classifier. A good reason otherwise is a conversation, not a breach.

**Why:** a direct enum comparison reads better than a helper wrapping it; a classifier earns its place by standardising the parts that are easy to get wrong by hand (subject typeclass, payload keys). Tim, 2026-10-17, while splitting mob_ai into AI engines.

**How to apply:** in any AI engine or strategy criterion. Frame conventions like this as best practice with room to argue, never as rules. Related: [[feedback-few-events-distinguished-by-payload]], [[feedback_no_hardening_language]].
