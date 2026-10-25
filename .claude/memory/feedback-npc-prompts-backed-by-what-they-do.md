---
name: feedback-npc-prompts-backed-by-what-they-do
description: "An NPC's persona and goals may only suggest trades, teaching or services the NPC can actually perform — its shop stock, its trainable skills and masteries, its room's recipes"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3490b4dc-5abb-479a-b0a7-1fa9de845af4
  modified: 2026-10-25T00:30:41.090Z
---

Anything in a conversational NPC's `llm_persona` or `llm_goals` that the LLM could be tempted to offer a player has to be backed by what that NPC can actually do or sell (Tim, 2026-10-24).

**Why:** the LLM acts on the prompt. A jeweller whose persona says she "buys gems" or "takes any commission" will offer both, and nothing in the game can honour it.

**How to apply:** before proposing a persona, check the NPC's `inventory` (and what each id or item type is), its `trainable_skills` and `trainer_masteries`, and the recipes its room's `crafting_type` and `mastery_level` allow. Name only those as things it trades, makes or teaches. Rumours, opinions, homely flavour (a kettle on the hob) and goals that name no particular item or service ("make anyone presentable") are fine; the line is a concrete offer the game cannot honour, such as a named item to hand over or a test brew to drink. Frame its standing to match too: a trainer who teaches only to BASIC is a village craftsperson, never a master of the craft. Related: [[player-led-economy-everything-crafted]].
