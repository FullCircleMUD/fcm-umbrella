---
name: feedback-always-include-imports
description: Every in-game py snippet must be self-contained — include the imports every time
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5c171053-81dc-40eb-a35d-b8d83ca4cc34
  modified: 2026-08-18T23:24:19.035Z
---

When giving Evennia `py` console commands, **always include the imports**, every
time, even if the same imports were given minutes earlier.

**Why:** Tim runs these as superuser and has to leave and re-enter `py` constantly
to do things in game. Each re-entry is a fresh namespace, so a snippet that assumes
an earlier import just fails and costs a round trip.

**How to apply:**
- Treat every snippet as if it runs in a brand-new console.
- One statement per line — the game splits input on `;`.
- Common ones: `from evennia.objects.models import ObjectDB`,
  `from evennia import ScriptDB`, `import evennia, evennia_shards`,
  `from utils import mob_move_probe as p` (dev only — not deployed to staging).
