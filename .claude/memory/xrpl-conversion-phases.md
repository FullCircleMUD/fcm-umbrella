---
name: xrpl-conversion-phases
description: fcm-xrpl library-standards conversion — agreed phase list and linter baseline (2026-09-12); blocked on cascade multi-label change
metadata: 
  node_type: memory
  type: project
  originSessionId: abdee214-f244-40df-90bc-44186d0e890c
  modified: 2026-09-13T02:07:41.786Z
---

Conversion of `libraries/fcm-xrpl` to current library standards. Cascade `app_labels` change landed 2026-09-12 — no longer blocked.

Linter baseline 2026-09-12: standards linter 6 errors / 13 warns; test-plan linter clean; doc linter clean bar 10 `was_phrasing` advisories. The licence errors (no LICENSE, `Proprietary`, missing SPDX) are the sanctioned fcm-* divergence — leave them.

Phases (2–4 test-plan-first):

1. ~~Design decisions~~ — done: seed-app steering via cascade `app_labels`; scaffolding helper `xrpl_library_must_run_before_installed_apps_declaration()` is DROPPED (one-time setup, consumer creates `xrpl_seed` by hand per installing.md; agreed 2026-09-12).
2. ~~Database cascade~~ — DONE, committed+pushed 2026-09-12 (fcm-xrpl 19f781a). `db_spec.py` app_labels=("xrpl", "xrpl_seed") — note label is `xrpl`, not `fcm_xrpl`. Docs cascade-pass done same commit; 822 tests green. Live smoke test in a new `examples/demo` gamedir (afc26a3) — separation, seed steering, runtime routing, real boot, and the seed-app refusal all confirmed; see `examples/README.md`.
   Demo gotcha: `pip install -r requirements.txt` can leave Twisted's `twistd` out of `venv/bin`, so `evennia start` fails — `pip install --force-reinstall --no-deps twisted` fixes it.
   Seed-app contract (agreed 2026-09-12): fixed label `xrpl_seed`, consumer creates the folder + `migrations/` + two `__init__.py` by hand, location free via dotted `INSTALLED_APPS` entry (label = last segment). Mandatory: `check_settings()` refuses boot when no `INSTALLED_APPS` entry ends in `xrpl_seed`; no separate path setting.
   `XRPL_CONN_MAX_AGE` setting + accessor go; spec pins `conn_max_age=0` so a cascade default change can't drift under us (agreed 2026-09-12).
3. Logging phase 1 (mechanical) — DONE, committed+pushed 2026-09-12 (ca32e91). `make_logger` binding, `xrpl_log`/`xrpl.log` unchanged, 24 call sites untouched; LG-01..05 retired → LG-06; 818 tests green; validated live in `examples/demo` incl. a real call site. Phase 2 (logging the pre-reactor window — `ready()`/`check_settings()` refusals) NOT started; own conversation.
   Demo boot gotcha (corrected): `twistd` failure is a PATH problem — run `export PATH="$PWD/../venv/bin:$PATH"; evennia start`, not `../venv/bin/evennia start`.
   Live `py` over telnet works: demo/demopass123 on localhost:4000 (helper script pattern in session scratchpad).
4. Settings refactor: `validate_settings` → `check_settings` (collect-all raise, called from ready()); required accessors become plain reads; fold the 2 stray settings reads into accessors.
5. Mechanical sweep — constants DONE (8b1d98a, 28d55a9): 39 of 44 moved to `config.py`; 5 stay by decision and are recorded in fcm-xrpl's CLAUDE.md — `DISTRIBUTED` (reads model attrs, config.py is on the settings path) plus `NOTHING`/`UNSIGNED`/`BROKEN`/`_NO_VARIANT` (player-facing text). The linter's remaining `constant_outside_config` warn is that decision, don't "fix" it. Still to do: 16 Evennia-import comments, 9 `.db` writes (mixins/fungible_inventory.py, nft_mirror.py).
6. Docs: write `docs/installing.md`; interoperability — 7 missing sibling sections, 3 sections lacking a relationship; CLAUDE.md layout/tooling; eyeball the 10 advisories.
7. Close out: full linter re-run, full test suite, progress.md entry.
