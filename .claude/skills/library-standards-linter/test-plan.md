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
| `LG` | `check_logging` |
| `CN` | `check_constants` |
| `CM` | `check_claude_md` |
| `IO` | `check_interoperability` |
| `IN` | `check_installing` |
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
| DC-07 | Missing `docs/installing.md` is an error. It is the page a consumer arrives at, and the standard names one filename so a consumer running several libraries looks in the same place each time — so a differently-named install doc must not satisfy it | `CheckDocs.test_missing_installing_is_error` |
| DC-08 | Missing `docs/interoperability.md` is an error. The standard requires every library to carry it so a reader deciding whether two can be co-installed gets a definite statement from either side rather than inferring from silence | `CheckDocs.test_missing_interoperability_is_error` |

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

## LG — `check_logging`

The mechanically decidable parts of the logging standard: that `log.py` exists, uses Evennia's
`logger.log_file`, names a log file of its own, degrades outside an Evennia engine, carries the
prescribed function name and signature, stamps no timestamp of its own, and stays internal — and that
no other module has fallen back to stdlib `logging`, whose records reach nobody when the consumer has
configured no handler. Whether a missing shim is a documented divergence is the judgment layer's call,
so its absence is a warn.

Every check here tests for the *presence of the mechanism* rather than proving the behaviour — the
linter reads source, it does not execute it. `LG-03` asks whether `log_file` is called, not whether the
line it writes is correct, and `LG-14` asks whether the `NoneType: None` suppression is there, not
whether it fires. That is the ceiling of a mechanical linter, and the reason the judgment layer exists.

| ID | Case | Test function |
|---|---|---|
| LG-01 | A compliant shim produces no findings | `CheckLogging.test_clean` |
| LG-02 | A missing `log.py` is a warn, not an error | `CheckLogging.test_missing_shim_is_warn_not_error` |
| LG-03 | A shim that does not call `logger.log_file` is an error — it has one and it is the wrong mechanism | `CheckLogging.test_shim_not_using_log_file_is_error` |
| LG-04 | A shim naming no `.log` file is a warn | `CheckLogging.test_shim_naming_no_log_file_is_warn` |
| LG-05 | A shim that does not handle `ImportError` is a warn — it must no-op outside an Evennia engine | `CheckLogging.test_shim_without_importerror_handling_is_warn` |
| LG-06 | `logging.getLogger` outside the shim is a warn, and the finding names the file | `CheckLogging.test_stdlib_logging_outside_the_shim_is_warn` |
| LG-07 | The shim itself is exempt from the stdlib check | `CheckLogging.test_the_shim_itself_may_mention_logging` |
| LG-08 | A library with no package produces no findings | `CheckLogging.test_no_package_is_silent` |
| LG-09 | The shim's public function is named for the library — `bus_log`, `ai_memory_log`. A warn. A consumer reading a stack trace uses that name to tell whose log line it is | `CheckLogging.test_function_not_named_for_the_library_is_warn` |
| LG-10 | Its signature is `(message, level="INFO", trace=False)`. A warn. The shim is copied between libraries, so a changed signature means a copy was edited rather than adapted | `CheckLogging.test_wrong_signature_is_warn` |
| LG-11 | `_VALID_LEVELS` holds exactly `INFO`, `WARN`, `ERROR`. A warn. `CN-04` checks the constant's name; nothing checks its value, so a shim could carry a fourth level and pass | `CheckLogging.test_wrong_levels_is_warn` |
| LG-12 | `log.py` stamps no timestamp of its own — no `datetime`, `strftime` or `time.time()`. A warn. `log_file` already prefixes one in UTC, so a second stamps every line twice and the file stops reading against `server.log` | `CheckLogging.test_own_timestamp_is_warn` |
| LG-13 | The shim is not re-exported from `__init__.py`. A warn. It is internal; a consumer who imports it is depending on something the standard does not offer them | `CheckLogging.test_shim_reexported_from_init_is_warn` |
| LG-14 | The `trace` path is present — `format_exc` is called and the `NoneType: None` case is suppressed. A warn. Without the suppression every `trace=True` call outside an `except` block writes a line of noise | `CheckLogging.test_missing_trace_handling_is_warn` |

`LG-09` to `LG-14` are all warns. `LG-03` is the section's only error, and it is reserved for a shim
that logs through the wrong mechanism — the one failure where the lines go somewhere nobody reads.
Everything else here is a shim that works and diverges.

## CN — `check_constants`

Covers *Where constants are declared* in `library-standards.md`: every module-level constant lives in
`config.py`, with `log.py` exempt for exactly two names.

Severity is deliberately split. The main rule is a **warn**, because 224 constants across the fifteen
libraries currently sit outside `config.py` — it is a work queue a library drains at its own pace, not
a gate that fails every run. The bounded-exemption rule is an **error**, because no library violates it
today, so it costs nothing now and catches the first attempt to smuggle a constant into `log.py` to
escape the main rule.

| ID | Case | Test function |
|---|---|---|
| CN-01 | A compliant library produces no findings | `CheckConstants.test_clean` |
| CN-02 | A module-level constant in any module other than `config.py` is a warn, and the finding names the module and the constant | `test_constant_outside_config_is_warn` |
| CN-03 | Constants in `config.py` produce nothing — it is the declared home | `test_constants_in_config_are_clean` |
| CN-04 | `log.py` declaring exactly `_LOG_FILENAME` and `_VALID_LEVELS` produces nothing. The standard's one exemption | `test_log_shim_constants_are_exempt` |
| CN-05 | A third constant in `log.py` is an error. The exemption is bounded by name, so it cannot be widened into an escape hatch | `test_a_third_log_constant_is_an_error` |
| CN-06 | `tests.py` is excluded. It lives inside the package by Django convention, but its constants are test scaffolding rather than library surface | `test_constants_in_tests_are_ignored` |
| CN-07 | `migrations/` is excluded — Django generates those files and nobody hand-places their constants | `test_constants_in_migrations_are_ignored` |
| CN-08 | An import other than `traceback` above `log.py`'s constants is a warn. The standard puts the two names at the top with `import traceback` alone above them | `test_extra_import_above_log_constants_is_warn` |
| CN-09 | A lowercase or mixed-case module-level assignment is not a constant and is ignored — otherwise every module-level variable would be a finding | `test_lowercase_assignment_is_not_a_constant` |

`CN-08` is a warn rather than an error because one library already breaches it: `evennia-shards`'
`log.py` carries `from datetime import datetime, timezone` for its `security=True` dual-write. That is
either a sanctioned divergence or a finding, and it has not been adjudicated — a warn reports it
without pre-judging.

## CM — `check_claude_md`

Covers *CLAUDE.md structure* in `library-standards.md`: nine sections in a fixed order, and the
principles section 4 must carry.

Severity is split on what the corpus already satisfies. All fifteen libraries carry the nine sections,
with identical wording and in order, so **a missing or misordered section is an error** — it costs
nothing today and catches the first drift. Five of the fifteen have no test-first principle, so
**principles are a warn**: a queue, not a gate.

Extra sections are allowed and common — `The starting point`, `Sibling libraries to reference`,
`Scope, in two phases`. Only the nine required ones are checked, and only their order relative to each
other.

| ID | Case | Test function |
|---|---|---|
| CM-01 | A compliant `CLAUDE.md` produces no findings | `CheckClaudeMd.test_clean` |
| CM-02 | A missing required section is an error, and the finding names it | `CheckClaudeMd.test_missing_section_is_error` |
| CM-03 | The nine sections out of order is an error | `CheckClaudeMd.test_sections_out_of_order_is_error` |
| CM-04 | Extra sections interleaved between required ones are fine — the corpus has them and they are not drift | `CheckClaudeMd.test_extra_sections_are_fine` |
| CM-05 | An `evennia-*` library whose principles omit one of the three is a warn naming it | `CheckClaudeMd.test_missing_principle_is_warn` |
| CM-06 | An `fcm-*` library is not required to carry the two scope principles. The standard has it state that they deliberately do not apply, and a mention either way reads the same to a linter — so it does not check them | `CheckClaudeMd.test_fcm_library_needs_neither_scope_principle` |
| CM-07 | An `fcm-*` library still needs test-first, and its absence is a warn | `CheckClaudeMd.test_fcm_library_still_needs_test_first` |
| CM-08 | A library with no `CLAUDE.md` produces no findings here — `check_root_files` owns that, and two findings for one missing file is noise | `CheckClaudeMd.test_no_claude_md_is_silent` |

## IO — `check_interoperability`

Covers *Library interoperability* in `library-standards.md`: `docs/interoperability.md` carries a
section for **every** library under `libraries/` — including itself — in alphabetical order, and each
sibling section names a relationship.

This is the one check that reads the corpus rather than the library alone, and it has to: "every
sibling" is a fact about the directory, not about the file. The library list comes from the same
`discover` rule the CLI uses, so a new library appears in every sibling's queue the moment it has a
`pyproject.toml`.

All three findings are **warns**. Section counts across the corpus run from 6 to 15 against 15
libraries, so every library has a gap here; this is a queue, not a gate.

The library's own section is exempt from the relationship check — the standard has it say
*"This library."* and nothing else, so demanding a relationship there would flag every compliant file.

| ID | Case | Test function |
|---|---|---|
| IO-01 | A doc covering every library in alphabetical order produces no findings | `CheckInteroperability.test_clean` |
| IO-02 | A library under `libraries/` with no section is a warn naming it | `CheckInteroperability.test_missing_sibling_is_warn` |
| IO-03 | The library's own section is required too — a doc covering every sibling but itself is a warn | `CheckInteroperability.test_own_section_is_required` |
| IO-04 | Sections out of alphabetical order is a warn | `CheckInteroperability.test_out_of_order_is_warn` |
| IO-05 | A sibling section naming none of the three relationships is a warn. An empty section is the common form of this | `CheckInteroperability.test_section_without_a_relationship_is_warn` |
| IO-06 | The library's own section needs no relationship — `"This library."` is the whole entry | `CheckInteroperability.test_own_section_needs_no_relationship` |
| IO-07 | Headings that name no library are ignored, so a preamble or a trailing note is not a finding | `CheckInteroperability.test_non_library_headings_are_ignored` |
| IO-08 | No `docs/interoperability.md` produces no findings here — `DC-08` owns its absence | `CheckInteroperability.test_missing_doc_is_silent` |

## IN — `check_installing`

Covers *The installation document* in `library-standards.md`: `docs/installing.md` carries a numbered
step list and three named parts — the required settings, the optional settings with their defaults,
and what is not checked for you.

`DC-07` owns the file's absence; this checks what is in it. Without that split, a rename turns the
linter green while the document still fails the standard, which is exactly what happened when
`archive-settings.md` became `installing.md`.

All four findings are **warns**. Across the six libraries that have the document, three carry numbered
steps, two name required settings, one names optional settings and three have the not-checked section
— so this is a queue. `evennia-equipment` is the only one satisfying all four, and is the reference
shape.

A step list is three or more `## <n>.` headings. One or two numbered headings is a document that
happens to have a number in it, not a consumer walking down a list.

| ID | Case | Test function |
|---|---|---|
| IN-01 | A document with numbered steps and all three parts produces no findings | `CheckInstalling.test_clean` |
| IN-02 | Fewer than three numbered step headings is a warn | `CheckInstalling.test_too_few_numbered_steps_is_warn` |
| IN-03 | No required-settings section is a warn | `CheckInstalling.test_no_required_settings_is_warn` |
| IN-04 | No optional-settings section is a warn | `CheckInstalling.test_no_optional_settings_is_warn` |
| IN-05 | No "what is not checked for you" section is a warn | `CheckInstalling.test_no_unchecked_section_is_warn` |
| IN-06 | A library stating it reads no settings satisfies both settings parts. The standard has it say so in one line rather than drop the section, and an absent section reads as an oversight where a sentence is an answer | `CheckInstalling.test_stating_no_settings_satisfies_both` |
| IN-07 | No `docs/installing.md` produces no findings here — `DC-07` owns its absence | `CheckInstalling.test_missing_doc_is_silent` |

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
| XC-04 | Every finding name the code emits is documented in `SKILL.md`. `XC-01` guards the plan; nothing guarded the skill's own check table, which is how three findings shipped undocumented | `CrossCutting.test_every_finding_is_documented_in_the_skill` |
