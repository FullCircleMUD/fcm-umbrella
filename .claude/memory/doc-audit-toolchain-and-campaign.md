---
name: doc-audit-toolchain-and-campaign
description: The doc/library audit toolchain (linter+auditor pairs) and the in-flight code-vs-doc consistency audit campaign across the project
metadata: 
  node_type: memory
  type: project
  originSessionId: b3bba4c6-d5c8-403d-8943-4b214af2df80
---

A toolchain of **deterministic linter skills + read-only judgment auditor agents** was built for keeping
documentation honest. The pattern is **spec → linter → auditor**: a human-readable spec holds the rules,
a deterministic stdlib-Python linter skill checks the mechanical subset, and a read-only agent reads its
rules *from the spec* and applies the judgment the linter can't. **All auditors are read-only — they
surface findings; a human or orchestrator applies fixes.** All are written generic (no FCM/Evennia
specifics) so they port to other projects.

- **Docs conventions:** `doc-convention-linter` skill + `doc-convention-auditor` agent; spec =
  `docs/doco-structure.md`. (Full-repo run done; findings fixed.)
- **Library structure:** `library-standards-linter` skill + `library-standards-auditor` agent; spec =
  `docs/library-standards.md`. (5 libraries lint clean; auditor validated.)
- **Code-vs-doc drift:** `doc-consistency-auditor` agent (no linter yet — agent-first by design). Reads
  design docs + the code they cite, flags only **concrete, high-confidence contradictions**.

**Consistency-auditor calibration (load-bearing):** these are *design* docs, not API docs. Flag only a
cited path/symbol/command that is gone/renamed/no-longer-matches. **Design-ahead-of-code, `[TBD]`, and
built/not-built markers are NOT drift.** Report **code-docstring drift** (stale docstring vs its own
implementation) in a *separate* group from design-doc drift. **Scope: a system/subsystem cluster beats a
single doc** — validated: docs cross-reference each other, so cluster scope catches drift single-doc
scope structurally cannot.

**Campaign in progress — consistency sweep across the project, one target at a time (system scope):**
- ✅ `evennia-shards` (3 drifts) · ✅ `evennia-world-builder` (5 drifts) · ✅ `evennia-mob-spawner`
  (7 drifts) · ✅ `evennia-yaml-reader` (CLEAN, 0 drift)
- ⏳ in progress: **umbrella `docs/` ↔ `src/game`, audited by system** (too large for one pass).
  ✅ Combat cluster (`combat-system.md` + `weapon-damage-scaling.md`): 12 doc drifts fixed, pushed.
  Next game systems: effects, spells, npc/mob, items/rooms, economy/spawn, etc.
- ⏸ `evennia-targeting` deferred — it's a scaffold (no library code yet), so its docs are all
  design-ahead with nothing to drift against until code lands

**`src/game` is a game repo — board approval needed to change game code.** This phase fixes umbrella
`docs/` only; anything that would edit `src/game` (incl. stale code docstrings/comments) is surfaced
for the board, not committed. **Board-surface items from the combat-cluster audit (open):**
- `world/damage_tables.py` comment groups Sai/Nunchaku under "d6 Base" but both are `base_damage="d4"`.
- `combat/combat_utils.py` `force_drop_weapon` docstring claims mob floor-drop vs PC inventory; code
  always removes to inventory (no branching).
- `universal_parry` on `staff_nft_item.py` is documented as gating staff parry vs all attack types but
  is never read by `execute_attack()`/the handler — may be unimplemented (needs combat-code look).
- Quarterstaff: `weapon-damage-scaling.md` design (lines 21/28/30) says quarterstaff→bronze tier
  ("material is flavour, tier is mechanical"); prototype `quarterstaff.py` sets `material="wood"`.
  Left unresolved per owner — needs someone with the design history.

Fixes so far have been doc/docstring text only (no logic). See [[doc-conventions-home]],
[[design-docs-in-umbrella]]. Note: pushing `FullCircleMUD/*` repos needs the `FullCircleMUD` gh account.
