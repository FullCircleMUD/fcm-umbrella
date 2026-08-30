# Test plan — library-standards-linter

Every test case the linter commits to covering, and the test function that covers it. The linter is
built test-first: cases are agreed here, tests are written against them, then the implementation is
written to pass. The **Test function** column is the auditable trail — an empty cell means the case is
agreed but not yet covered.

Case IDs are stable and referenceable. Do not renumber; retire an ID rather than reuse it. Each test
function carries its case ID as its docstring, so the trail reads in both directions.

All test functions live in `tests.py`, beside this plan. Run them with
`python .claude/skills/library-standards-linter/tests.py`.

| Prefix | Covers |
|---|---|
| `RF` | `check_root_files` |
| `DC` | `check_docs` |
| `TP` | `check_test_plan` — the adapter onto the `test-plan-linter` skill |
| `SL` | `check_src_layout` |
| `NM` | `check_naming` |
| `SP` | `check_spdx` |
| `TD` | `check_tests_dir` |
| `MS` | `check_memory_surface` |
| `PP` | `check_pyproject` |
| `DS` | `discover` / `lint` |
| `CL` | CLI: `main`, `render_human`, exit codes, `--json` |
| `XC` | Cross-cutting |

## Fixtures

The suite needs no network and no real library — every case builds a synthetic library in a temp dir
and calls one validator in isolation.

| Fixture | Purpose |
|---|---|
| `compliant()` | Spec dict for a fully-compliant `libraries/my-lib`, with `tests/` and `docs/archive/` satisfied by placeholders |
| `build(spec)` | Writes a spec dict to a `TemporaryDirectory` and returns `(tmp, root)` |
| `ValidatorBase.ctx(drop=…, **add)` | Builds a mutated tree and returns the `LibContext` for `my-lib` |
| `kinds(findings, severity)` | The set of `check` names at a severity — assertions name the check, not the message |
| `PYPROJECT` | Compliant `pyproject.toml` text; cases mutate one field at a time |
| `TEST_PLAN` | Compliant `docs/test-plan.md` text — a prefix legend table plus one case table |
| `SPDX` | The header line prepended to compliant sources |

## RF — `check_root_files`

| ID | Case | Test function |
|---|---|---|
| RF-01 | A compliant library produces no findings | `CheckRootFiles.test_clean` |
| RF-02 | Missing `LICENSE` is an error | `CheckRootFiles.test_missing_license_is_error` |
| RF-03 | Missing `.gitignore` is a warn, not an error | `CheckRootFiles.test_missing_gitignore_is_warn` |
| RF-04 | Each required root file, dropped on its own, yields exactly one finding at its documented severity (`pyproject.toml`/`README.md`/`CLAUDE.md`/`LICENSE` error; `.gitignore`/`runtests.py` warn) | `CheckRootFiles.test_each_required_file_has_its_documented_severity` |

## DC — `check_docs`

| ID | Case | Test function |
|---|---|---|
| DC-01 | A compliant library produces no findings | `CheckDocs.test_clean` |
| DC-02 | A missing `docs/` directory yields one `missing_docs` error and no per-file findings | `CheckDocs.test_missing_docs_dir_is_single_error` |
| DC-03 | Missing `docs/INDEX.md` is an error | `CheckDocs.test_missing_index_is_error` |
| DC-04 | Missing `docs/progress.md` is a warn | `CheckDocs.test_missing_progress_is_warn` |
| DC-05 | Missing `docs/archive/` is a warn; a `.gitkeep` satisfies it | `CheckDocs.test_missing_archive_is_warn` |
| DC-06 | A `docs/documentation-structure.md` is a `forbidden_meta_doc` error | `CheckDocs.test_documentation_structure_md_forbidden` |

## TP — `check_test_plan`

The plan-vs-suite rules live in the sibling `test-plan-linter` skill, which owns their cases and their
tests. What this linter owns is the adapter: supplying the plan path and the library's test roots, and
reporting what comes back under the library.

TP-03 to TP-18 are retired — those cases moved to that skill when the checks did. Do not reuse the IDs.

| ID | Case | Test function |
|---|---|---|
| TP-01 | A compliant plan produces no findings | `CheckTestPlan.test_clean` |
| TP-02 | A missing `docs/test-plan.md` is a warn, renamed to the library standard's `missing_file` | `CheckTestPlan.test_missing_plan_is_warn` |
| TP-19 | Findings from the plan linter are reported under the library, with repo-relative paths | `CheckTestPlan.test_plan_findings_are_reported_under_the_library` |
| TP-20 | The library's own test modules are the reverse check's roots — a ghost test there is an error | `CheckTestPlan.test_ghost_test_surfaces_as_an_error` |

## SL — `check_src_layout`

| ID | Case | Test function |
|---|---|---|
| SL-01 | A compliant layout produces no findings | `CheckSrcLayout.test_clean` |
| SL-02 | A missing `src/` directory is an error | `CheckSrcLayout.test_missing_src_is_error` |
| SL-03 | A `src/` with no package (no dir carrying `__init__.py`) is an error | `CheckSrcLayout.test_no_package_under_src_is_error` |
| SL-04 | A package `__init__.py` without `__version__` is a warn | `CheckSrcLayout.test_missing_version_is_warn` |

## NM — `check_naming`

| ID | Case | Test function |
|---|---|---|
| NM-01 | A package matching the underscored repo name produces no findings | `CheckNaming.test_clean` |
| NM-02 | A package name that does not match is an error | `CheckNaming.test_mismatch_is_error` |

## SP — `check_spdx`

| ID | Case | Test function |
|---|---|---|
| SP-01 | Sources carrying the header produce no findings | `CheckSpdx.test_clean` |
| SP-02 | A source missing the header is a warn naming the file | `CheckSpdx.test_missing_is_warn` |
| SP-03 | `migrations/` and `__pycache__/` are excluded | `CheckSpdx.test_migrations_excluded` |
| SP-04 | A header below the first five lines counts as missing | `CheckSpdx.test_header_below_first_five_lines_is_missing` |

## TD — `check_tests_dir`

| ID | Case | Test function |
|---|---|---|
| TD-01 | A `tests/` holding only a placeholder passes | `CheckTestsDir.test_placeholder_passes` |
| TD-02 | A missing `tests/` is a warn, not an error | `CheckTestsDir.test_missing_is_warn_not_error` |

## MS — `check_memory_surface`

| ID | Case | Test function |
|---|---|---|
| MS-01 | No `.claude/memory/` produces no findings | `CheckMemorySurface.test_clean` |
| MS-02 | A per-library memory surface is a warn | `CheckMemorySurface.test_forbidden` |

## PP — `check_pyproject`

| ID | Case | Test function |
|---|---|---|
| PP-01 | A compliant `pyproject.toml` produces no findings | `CheckPyproject.test_clean` |
| PP-02 | A license other than BSD-3-Clause is an error | `CheckPyproject.test_wrong_license_is_error` |
| PP-03 | A `[project] name` not matching the repo dir is an error | `CheckPyproject.test_name_mismatch_is_error` |
| PP-04 | Unparseable TOML is a single error and no field findings | `CheckPyproject.test_unparseable_is_error` |
| PP-05 | An absent `pyproject.toml` produces no findings here — `check_root_files` owns that | `CheckPyproject.test_absent_pyproject_is_not_reported_here` |
| PP-06 | A bare-string `license = "BSD-3-Clause"` is accepted, as is the `{text = …}` table form | `CheckPyproject.test_bare_string_license_accepted` |
| PP-07 | A missing `requires-python`, or one below 3.10, is a warn | `CheckPyproject.test_requires_python_missing_or_too_old_is_warn` |
| PP-08 | A missing `[build-system]` table is a warn | `CheckPyproject.test_missing_build_system_is_warn` |
| PP-09 | `[tool.setuptools.packages.find] where` other than `["src"]` is a warn | `CheckPyproject.test_packages_where_must_be_src` |

## DS — `discover` / `lint`

| ID | Case | Test function |
|---|---|---|
| DS-01 | A compliant library lints clean end to end | `Integration.test_compliant_is_clean` |
| DS-02 | A directory under `libraries/` without a `pyproject.toml` is not a library | `Integration.test_discovery_skips_non_library_dirs` |
| DS-03 | A scope argument restricts the run to the named libraries | `Integration.test_scope_restricts_to_named_libraries` |
| DS-04 | A root with no `libraries/` directory returns no libraries and does not raise | `Integration.test_root_without_libraries_dir_is_empty` |

## CL — CLI and output

| ID | Case | Test function |
|---|---|---|
| CL-01 | A clean library exits 0 | `Cli.test_clean_library_exits_zero` |
| CL-02 | Any error exits 1 | `Cli.test_error_exits_one` |
| CL-03 | Warnings alone exit 0, and exit 1 under `--strict` | `Cli.test_warnings_exit_zero_unless_strict` |
| CL-04 | `--json` emits parseable JSON carrying every finding and the error/warning counts | `Cli.test_json_output_carries_findings_and_counts` |

## XC — Cross-cutting

| ID | Case | Test function |
|---|---|---|
| XC-01 | Every validator in `CHECKS` is named by at least one case in this plan | `CrossCutting.test_every_check_is_named_in_the_plan` |
| XC-02 | Every test function in `tests.py` is named by a case in this plan — the linter's own ghost-test check, applied to itself | `CrossCutting.test_every_test_is_named_in_the_plan` |
| XC-03 | Finding paths are repo-relative, never absolute | `CrossCutting.test_finding_paths_are_repo_relative` |
