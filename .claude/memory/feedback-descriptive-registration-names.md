---
name: feedback-descriptive-registration-names
description: Functions called from at_server_start say what they register — register_hourly_telemetry, register_xrpl_sink_drain — never a bare register_schedule
metadata:
  type: feedback
---

Every function `at_server_start()` calls names the thing it registers and whose it is:
`register_hourly_telemetry()`, `register_xrpl_sink_drain()`, `register_tick_5s()`. Never a generic
`register_schedule()`, and never two registrations folded into one function.

**Why:** `at_server_start()` collects many registrations; generic names force Tim to trace each one back
to learn what it starts (2026-10-03, renaming `register_schedule`).

**How to apply:** one clearly named registration function per signal, called by name from
`at_server_start()`. Related: [[feedback-follow-evennia-conventions]].
