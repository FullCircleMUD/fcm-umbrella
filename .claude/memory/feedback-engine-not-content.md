---
name: feedback-engine-not-content
description: "Judge the machinery by what it can handle once declared, never by which content exists yet"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c8b68d75-546f-40ec-938a-71d67627c3a3
  modified: 2026-10-01T19:06:04.504Z
---

The rebuild is building the engine; specific potions, spells and items are configuration/content that comes after. Whether a piece of content exists is irrelevant to whether the engine is complete.

**Why:** 2026-09-30 — asked whether instant heals work, I answered "no healing potion is declared yet" as if that explained it. Tim: the engine has to handle potions not yet declared so the content can be built on it.

2026-10-01 — scoping the haste spell, I flagged that no world trainer teaches transmutation so nobody could cast it. Tim: not my problem. My job is to build something that *could* be cast; who can cast it, and the world content, are someone else's.

**How to apply:** when asked "does X work", answer whether the machinery supports X if someone declares it — trace the mechanism end to end. Never cite missing content as the reason, or as evidence something works. When scoping a build, raise only a prerequisite that directly stops the mechanic being built — never follow-on content, world entries, or "no one can use it yet". Related: [[feedback-build-for-the-intended-game]].
