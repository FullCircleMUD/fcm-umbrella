---
name: library-standards-linter
description: |
  Deterministic linter that checks the reusable libraries under `libraries/` against
  the mechanically-decidable parts of `design/library-standards.md` — required files,
  src layout, naming consistency, pyproject fields (license, requires-python,
  packages-where), the package __version__, SPDX headers, the required docs/ files,
  the docs/test-plan.md coverage trail in both directions (uncovered cases, named
  test functions that do not exist, tests no case claims, duplicate case IDs and
  unresolved [TBD] cases), the logging wiring (the
  evennia-logging-extension dependency, the three-line log.py binding through
  make_logger, the bound name, the filename, no module-scope log import in
  config.py, and that the shim stays internal), where module-level constants are declared, CLAUDE.md's nine
  standard sections and its section-4 principles, interoperability.md against the
  live contents of libraries/, installing.md's step list and its settings and
  not-checked-for-you parts, that settings are read through an accessor in
  config.py rather than directly, that a shim is actually used, and absence of a
  per-repo documentation-structure.md or memory surface. Use to
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
| `family_prefix` — library name carries neither `evennia-` nor `fcm-` | error |
| `library_name_form` — library name is not hyphenated lowercase | error |
| `pyproject_name` / `license` — pyproject `name`≠dir, or license≠BSD-3-Clause | error |
| `legacy_build_file` — a `setup.py`, `setup.cfg` or `requirements.txt` at the repo root | error |
| `pyproject_unparseable` — `pyproject.toml` is not valid TOML | error |
| `forbidden_meta_doc` — a `docs/documentation-structure.md` exists (reduced-set rule) | error |
| `test_plan_dangling_ref` — a test function named in `docs/test-plan.md` doesn't exist | error |
| `test_plan_ghost_test` — a test function no case in the plan names | error |
| `test_plan_duplicate_id` — the same case ID used on two rows | error |
| `test_plan_tbd` — a case still carrying an unresolved `[TBD]` | error |
| `claude_md_section` / `claude_md_order` — a missing or misordered `CLAUDE.md` standard section | error |
| `claude_md_principle` — section 4 omits one of the principles its family carries | warn |
| `interop_missing_sibling` / `interop_order` — `interoperability.md` omits a library under `libraries/`, or its sections are not alphabetical | warn |
| `interop_no_relationship` — a sibling section naming none of hard dependency / optional integration / no coupling | warn |
| `installing_no_steps` — `installing.md` has fewer than three `## <n>.` step headings | warn |
| `installing_no_required_settings` / `installing_no_optional_settings` — neither settings part named, and the document does not state that the library reads none | warn |
| `installing_no_unchecked_section` — no "what is not checked for you" section | warn |
| `missing_dir` — no `tests/` or `docs/archive/` (a placeholder satisfies these) | warn |
| `tests_dir_incomplete` — a `tests/` with Python files but no `test_settings.py` / `urls.py` | warn |
| `pytest_in_use` — a conftest.py, a pytest import, or a pytest dependency | warn |
| `venv_not_ignored` — `.gitignore` does not ignore `venv/` | warn |
| `log_shim_mechanism` — a `log.py` that doesn't bind through `make_logger`, including the old hand-rolled shim | error |
| `missing_log_shim` / `log_shim_filename` — no `log.py`, or a literal filename that is not a plain `<name>.log` | warn |
| `log_dependency_undeclared` — `evennia-logging-extension` missing from `pyproject.toml` dependencies | warn |
| `log_shim_function_name` — the bound name is not the library's name plus `_log` | warn |
| `log_shim_unreadable` — a `log.py` the checks cannot read: unparseable, or more than one public binding. Cannot-tell is reported, never skipped | warn |
| `log_import_in_config_scope` — `config.py` imports the log function at module scope, completing an order-dependent cycle with a settable filename | warn |
| `log_shim_exported` — `__init__.py` re-exports the shim, which is internal | warn |
| `log_shim_unused` — a `log.py` no module calls, so the library emits nothing | warn |
| `claude_md_reading_order` — `Where to read first` does not name `docs/test-plan.md` | warn |
| `stdlib_logging` — `logging.getLogger` outside the shim; those records reach nobody | warn |
| `evennia_import_unexplained` — an Evennia import outside `log.py` with no comment saying why | warn |
| `db_attribute_write` — a write through `.db`, which never reaches the descriptor's `at_set()` | warn |
| `creates_directories` — library code calling `makedirs`/`mkdir` in the consumer's gamedir | warn |
| `core_imports_contrib` — a core module importing from `contrib/` | error |
| `models_without_spec` — `models.py` with no `db_spec.py` declaring the alias to `evennia-database-cascade` | warn |
| `hand_rolled_router` / `hand_rolled_resolution` — a `db_router.py` or router-method class, or `dj_database_url` / a `DATABASE_URL*` environ read; routing and resolution belong to `evennia-database-cascade` | error |
| `cascade_dependency_undeclared` — a `db_spec.py` with no `evennia-database-cascade` in `pyproject.toml` dependencies | warn |
| `db_spec_imports_django` — `db_spec.py` imports Django at module scope, on the consumer's settings path | error |
| `installing_documents_databases` — `installing.md` documents `DATABASE_ROUTERS` or hand-written `DATABASES[…]` entries instead of pointing at the cascade's docs | warn |
| `targeting_module_missing` / `targeting_callable_outside_module` — depends on targeting with no `targeting.py`, or a `p_`/`f_`/`op_` declared elsewhere | warn |
| `contrib_empty` — a `contrib/` scaffolded with no modules in it | warn |
| `constant_outside_config` — a module-level constant declared outside `config.py` | warn |
| `settings_read_outside_config` — a `settings.X` or `getattr(settings, …)` read bypassing its accessor | warn |
| `settings_validator_uncalled` / `settings_validator_outside_config` — `check_settings()` defined but never called from `ready()`, or defined outside `config.py` | error |
| `settings_validator_name` — the boot validator is not named `check_settings` | warn |
| `settings_read_at_module_scope` / `settings_import_at_module_scope` — a read or the `django.conf` import evaluated at import time rather than inside the accessor | warn |
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

## Calibration — constants

`constant_outside_config` is a **warn** because the corpus predates the rule: over
two hundred constants across the libraries sit outside `config.py` today. It reads
as a queue each library drains at its own pace, not a gate that fails every run.

`tests.py` and `migrations/` are out of scope: the first is scaffolding that lives
in the package by Django convention, the second is generated.

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
  `check_test_plan`, `check_src_layout`, `check_naming`, `check_spdx`,
  `check_tests_dir`, `check_logging`, `check_constants`, `check_memory_surface`,
  `check_pyproject`). Add or remove a check by editing that list; each has its own
  unit test. `design/library-standards.md` is the human-readable spec; this linter
  encodes its mechanical subset.
