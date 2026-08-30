---
name: library-standards-linter
description: |
  Deterministic linter that checks the reusable libraries under `libraries/` against
  the mechanically-decidable parts of `design/library-standards.md` — required files,
  src layout, naming consistency, pyproject fields (license, requires-python,
  packages-where), the package __version__, SPDX headers, the required docs/ files,
  the docs/test-plan.md coverage trail in both directions (uncovered cases, named
  test functions that do not exist, tests no case claims, duplicate case IDs and
  unresolved [TBD] cases), and absence of a per-repo documentation-structure.md or
  memory surface. Use to
  check a library meets the standard, before bootstrapping a new one, when auditing
  library structure, or as the first step of a library-standards-auditor (which
  applies judgment on top). Pure Python, no model in the loop: same input always
  gives the same findings.
allowed-tools:
  - Bash
---

# library-standards-linter

The **mechanical half** of the library-standards audit. It reports only what a
script can decide with certainty about a library's structure, leaving judgment —
chiefly *whether a deviation is a sanctioned divergence* — to a human or a future
`library-standards-auditor` agent that consumes its output.

## What it checks (against `design/library-standards.md`)

| Check | Severity |
|---|---|
| `missing_file` / `missing_docs` / `missing_src` / `missing_package` — required structure | error |
| `naming_mismatch` — src package name ≠ underscored repo name | error |
| `pyproject_name` / `license` — pyproject `name`≠dir, or license≠BSD-3-Clause | error |
| `forbidden_meta_doc` — a `docs/documentation-structure.md` exists (reduced-set rule) | error |
| `test_plan_dangling_ref` — a test function named in `docs/test-plan.md` doesn't exist | error |
| `test_plan_ghost_test` — a test function no case in the plan names | error |
| `test_plan_duplicate_id` — the same case ID used on two rows | error |
| `test_plan_tbd` — a case still carrying an unresolved `[TBD]` | error |
| `missing_dir` — no `tests/` or `docs/archive/` (a placeholder satisfies these) | warn |
| `test_plan_uncovered` — cases in `docs/test-plan.md` with an empty `Test function` cell | warn |
| `test_plan_no_column` — the test plan has no case table with a `Test function` column | warn |
| `missing_spdx` — source files lacking the SPDX header (migrations excluded) | warn |
| `missing_version` — no `__version__` in the package `__init__.py` | warn |
| `requires_python` / `build_system` / `packages_where` — pyproject field gaps | warn |
| `forbidden_memory` — library carries its own `.claude/memory/` | warn |

It deliberately does **not** judge: whether a missing `tests/` is a legitimate
pure-Python divergence, whether the CLAUDE.md sections are right, or whether the
architectural principles are sound. Those need a model.

## Calibration — placeholders are acceptable

Structural folders (`tests/`, `docs/archive/`) are checked at **folder-presence**
level. A library that doesn't need the contents can satisfy the standard with a
placeholder (a `.gitkeep`, or a short README explaining why) — that clears the
check. The linter surfaces a gap; the **accepted resolutions** are "add the
structure (placeholder OK)" or "document the divergence in the library's
`CLAUDE.md`". Adjudicating which applies is the judgment layer's job. `examples/`
is optional (only meaningful once there's code to exercise) — its absence is never
flagged.

## Calibration — the test plan

Libraries are built test-first (see the Testing section of `library-standards.md`),
so an uncovered case is the **normal in-progress state**, not a defect — a library
early in its life legitimately reports every case uncovered. `test_plan_uncovered`
is a warn precisely so it reads as a work queue.

A **dangling reference is an error**: the `Test function` column is the coverage
trail, and a name in it that doesn't exist anywhere in the library's sources is a
false claim of coverage. Names are matched loosely — backticks, markdown links and
`Class.test_method` qualification are all tolerated, and the last dotted segment is
matched against every `def` / `class` in `src/<package>/` and `tests/`.

Only tables carrying a `Test function` column are read, so the prefix legend and
the fixtures table are ignored.

## How to run

From the **umbrella root**:

```bash
# Human-readable report (per library), exit 1 if any error:
python .claude/skills/library-standards-linter/lint_library.py

# Structured findings for an agent to ingest:
python .claude/skills/library-standards-linter/lint_library.py --json

# Check one or more named libraries:
python .claude/skills/library-standards-linter/lint_library.py evennia-shards

# Also fail on warnings (stricter gate):
python .claude/skills/library-standards-linter/lint_library.py --strict
```

A library is any directory under `libraries/` carrying a `pyproject.toml`;
auxiliary repos (test-content / fixture repos) have none and are skipped — they are
not bound by the standards.

`--json` emits `{ "findings": [...], "summary": {...} }`; each finding carries
`check`, `severity`, `library`, `path`, `message`.

## Notes

- **Tests ship with the skill.** `python .claude/skills/library-standards-linter/tests.py`
  runs the stdlib unit tests (compliant library is clean; each check in isolation;
  the placeholder calibration). Run it after any change to `lint_library.py`.
- Each check is a single-purpose `LibContext -> list[Finding]` validator in the
  `CHECKS` list in `lint_library.py` (`check_root_files`, `check_docs`,
  `check_src_layout`, `check_naming`, `check_spdx`, `check_tests_dir`,
  `check_memory_surface`, `check_pyproject`). Add or remove a check by editing that
  list; each has its own unit test. `design/library-standards.md` is the
  human-readable spec; this linter encodes its mechanical subset.
