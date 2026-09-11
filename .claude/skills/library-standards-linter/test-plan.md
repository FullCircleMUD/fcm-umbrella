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
| `SA` | `check_settings_access` |
| `BV` | `check_boot_validation` |
| `EI` | `check_evennia_imports` |
| `OS` | `check_object_state` |
| `BS` | `check_boot_side_effects` |
| `DB` | `check_database` |
| `TG` | `check_targeting` |
| `CT` | `check_contrib` |
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
| `compliant()` | Spec dict for a fully-compliant `libraries/evennia-lib`, with `tests/` and `docs/archive/` satisfied by placeholders |
| `build(spec)` | Writes a spec dict to a `TemporaryDirectory` and returns `(tmp, root)` |
| `ValidatorBase.ctx(drop=…, **add)` | Builds a mutated tree and returns the `LibContext` for `evennia-lib` |
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
| RF-05 | A `setup.py`, `setup.cfg` or `requirements.txt` at the repo root is an error. `pyproject.toml` is the only build and dependency declaration, and a second one is a second source of truth | `CheckRootFiles.test_legacy_build_file_is_error` |
| RF-06 | A `.gitignore` not ignoring `venv/` is a warn. Each library is developed against a dedicated venv at its root, and an unignored one is committed sooner or later | `CheckRootFiles.test_venv_not_ignored_is_warn` |

`RF-05` is an error: no library carries a legacy build file today, so enforcing costs nothing.

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
| NM-03 | A library name carrying neither family prefix is an error. The prefix states what the code is allowed to know, so a library without one has not answered the question | `CheckNaming.test_no_family_prefix_is_error` |
| NM-04 | `fcm-` is a valid prefix as well as `evennia-` | `CheckNaming.test_fcm_prefix_is_accepted` |
| NM-05 | A name that is not hyphenated lowercase — an underscore or a capital — is an error. The repo name and the PyPI distribution name are the same string | `CheckNaming.test_name_must_be_hyphenated_lowercase` |

`NM-03` to `NM-05` are errors: all fifteen libraries already satisfy them, so enforcing costs nothing
now and catches the first library bootstrapped without a family decision.

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
| TD-03 | A `tests/` carrying Python files but missing `test_settings.py` or `urls.py` is a warn naming them. The standard's layout puts the standalone runner's settings and an empty URL conf there | `CheckTestsDir.test_incomplete_tests_dir_is_warn` |
| TD-04 | A placeholder-only `tests/` stays clean, per `TD-01`. Empty is the documented not-yet state; half-built is the one worth reporting | `CheckTestsDir.test_placeholder_only_stays_clean` |
| TD-05 | pytest in use — a `conftest.py`, an `import pytest`, or a pytest dependency — is a warn. The standard is Django's test runner via `runtests.py` | `CheckTestsDir.test_pytest_in_use_is_warn` |

## LG — `check_logging`

The mechanically decidable parts of the logging standard: that the library declares
`evennia-logging-extension`, that `log.py` exists and binds its log function through `make_logger`,
that the name it binds is named for the library, that the file it names ends in `.log`, that the shim
stays internal, and that no module has fallen back to stdlib `logging`, whose records reach nobody
when the consumer has configured no handler. Whether a missing shim is a documented divergence is the
judgment layer's call, so its absence is a warn.

Every check here tests for the *presence of the mechanism* rather than proving the behaviour — the
linter reads source, it does not execute it. That is the ceiling of a mechanical linter, and the
reason the judgment layer exists.

**`log.py` is three lines now**, so most of what this section used to check has nowhere left to go
wrong. The levels, the signature, the `ImportError` fallback, the traceback suppression and the
timestamp all live in `evennia-logging-extension` and are covered by its own suite. What is left is
whether a library is wired to it.

**The public name is an assignment, not a `def`.** That is the trap in this section: the old checks
were gated on finding a single public `FunctionDef` in `log.py`, and against the new shape that gate
does not match — producing no finding and no error. A check that stops checking reads as a clean
corpus.

Two things make that failure loud rather than silent:

- **`LG-09` and `LG-15` are tested against the three-line shim.** If the name extraction ever regresses
  to `FunctionDef`-only, those cases fail rather than going quiet.
- **`LG-20` reports a `log.py` the linter cannot read.** The old gate skipped when it could not
  identify the public name; the replacement treats that as a finding. **An unknown answer is not a
  clean one**, and a linter that silently narrows its own coverage is worse than one that complains
  about a file it does not understand.

`LG-20` walks a list of unreadable shapes rather than one, so it cannot be satisfied by special-casing
whichever shape is in front of whoever implements it — an implementation that skips on an unfamiliar
`log.py` fails the case rather than reporting a clean library. The list is the point, and it grows
whenever a shape turns up that slipped through.

| ID | Case | Test function |
|---|---|---|
| LG-01 | A compliant three-line shim produces no findings | `CheckLogging.test_clean` |
| LG-02 | A missing `log.py` is a warn, not an error | `CheckLogging.test_missing_shim_is_warn_not_error` |
| LG-04 | A shim naming no `.log` file is a warn | `CheckLogging.test_shim_naming_no_log_file_is_warn` |
| LG-06 | `logging.getLogger` outside the shim is a warn, and the finding names the file | `CheckLogging.test_stdlib_logging_outside_the_shim_is_warn` |
| LG-08 | A library with no package produces no findings | `CheckLogging.test_no_package_is_silent` |
| LG-09 | The name bound in `log.py` is named for the library — `bus_log`, `ai_memory_log`. A warn. A consumer reading a stack trace uses that name to tell whose log line it is | `CheckLogging.test_function_not_named_for_the_library_is_warn` |
| LG-13 | The shim is not re-exported from `__init__.py`. A warn. It is internal; a consumer who imports it is depending on something the standard does not offer them | `CheckLogging.test_shim_reexported_from_init_is_warn` |
| LG-15 | A shim no module calls is a warn. The library emits nothing, so the log file the standard asks for never exists — which is worth a look rather than a defect, since what to log is a decision | `CheckLogging.test_unused_shim_is_warn` |
| LG-16 | A `log.py` that does not call `make_logger` is an **error** — it has a shim and it is the wrong mechanism. This is what an un-migrated library reports | `CheckLogging.test_shim_not_calling_make_logger_is_error` |
| LG-17 | A library that does not declare `evennia-logging-extension` in `dependencies` is a warn. The shim imports it, so without the declaration the library works only where something else happened to install it | `CheckLogging.test_undeclared_dependency_is_warn` |
| LG-18 | A filename that is not a literal — `make_logger(get_log_filename())` — produces no findings. Whether the name is hardcoded or read from a setting is the library's decision, and the extension has no opinion | `CheckLogging.test_a_filename_from_an_accessor_is_clean` |
| LG-19 | `evennia-logging-extension` itself produces no findings in this section. It has no `log.py` because it *is* the mechanism, and a logger that logs its own failures through itself is a cycle | `CheckLogging.test_the_extension_itself_is_exempt` |
| LG-20 | A `log.py` the linter cannot read produces **at least one finding, for every unreadable shape** — a `def` where a binding belongs, two public bindings, none at all, an empty file. "Cannot tell" is reported, never treated as clean | `CheckLogging.test_an_unreadable_shim_is_reported_not_skipped` |
| LG-21 | A module-scope import of `.log` in `config.py` is a warn. `log.py` may import `config.py` for a settable filename, so the reverse import at module scope completes a cycle that resolves or crashes on declaration order. Imports inside function bodies are fine and are not inspected; no import at all is fine — logging from `config.py` is optional | `CheckLogging.test_module_scope_log_import_in_config_is_warn` |

`LG-16` is the section's only error, and it is reserved for a shim that logs through the wrong
mechanism — the one failure where the lines go somewhere nobody reads. Everything else here is a
library that works and diverges.

**Retired**, with the shape they checked. IDs are not reused.

| ID | Why |
|---|---|
| LG-03 | Nothing in a library calls `logger.log_file` any more. `LG-16` is its replacement |
| LG-05 | The `ImportError` no-op lives in the extension |
| LG-07 | The shim's exemption from the stdlib check. A three-line `log.py` has no way to trip a `logging.getLogger` grep |
| LG-10 | The signature comes from the extension; `log.py` declares none |
| LG-11 | `_VALID_LEVELS` no longer exists in a library |
| LG-12 | The duplicate-timestamp drift came from copied shims, and there is nothing left to copy |
| LG-14 | The `trace` path lives in the extension |

## CN — `check_constants`

Covers *Where constants are declared* in `library-standards.md`: every module-level constant lives in
`config.py`. There are no exemptions — `log.py` declares nothing, since a hardcoded log filename is a
literal in the one call that uses it and a settable one lives in `config.py` like any other setting.

A **warn**, because 224 constants across the fifteen libraries currently sit outside `config.py` — it
is a work queue a library drains at its own pace, not a gate that fails every run.

| ID | Case | Test function |
|---|---|---|
| CN-01 | A compliant library produces no findings | `CheckConstants.test_clean` |
| CN-02 | A module-level constant in any module other than `config.py` is a warn, and the finding names the module and the constant | `test_constant_outside_config_is_warn` |
| CN-03 | Constants in `config.py` produce nothing — it is the declared home | `test_constants_in_config_are_clean` |
| CN-06 | `tests.py` is excluded. It lives inside the package by Django convention, but its constants are test scaffolding rather than library surface | `test_constants_in_tests_are_ignored` |
| CN-07 | `migrations/` is excluded — Django generates those files and nobody hand-places their constants | `test_constants_in_migrations_are_ignored` |
| CN-09 | A lowercase or mixed-case module-level assignment is not a constant and is ignored — otherwise every module-level variable would be a finding | `test_lowercase_assignment_is_not_a_constant` |
| CN-10 | A constant in `log.py` is a warn like any other module. The exemption is gone, and this is what fails if anyone re-adds it | `test_a_constant_in_the_shim_is_a_warn` |

**Retired.** `CN-04`, `CN-05` and `CN-08` covered the `log.py` constants exemption, which no longer
exists — a hardcoded log filename is a literal in the one call that uses it, and a settable one lives
in `config.py` like any other setting. IDs are not reused.

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
| CM-09 | A `Where to read first` section not naming `docs/test-plan.md` is a warn. The standard puts it in that list, high, marked as where a behavioural change starts — it is the first thing a session changing behaviour has to open | `CheckClaudeMd.test_reading_order_without_test_plan_is_warn` |

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

## SA — `check_settings_access`

Covers *Reading settings* in `library-standards.md`: every setting is read through a named accessor in
`config.py`, and both the read and the `from django.conf import settings` sit inside the function
rather than at module scope.

Three findings, all **warns**. Seven of the fifteen libraries read settings outside `config.py`, four
import `settings` at module scope, and one reads one there — so this is a queue.

The module-scope *read* check applies to `config.py` only. Everywhere else the read is already
reported as outside its accessor, and two findings for one line is noise.

What this cannot see is an accessor that is *missing* — the linter only knows about the reads that
exist, not the ones a library ought to have. That is the judgment layer's.

| ID | Case | Test function |
|---|---|---|
| SA-01 | A library reading no settings produces no findings | `CheckSettingsAccess.test_clean` |
| SA-02 | A `settings.X` read outside `config.py` is a warn naming the module | `CheckSettingsAccess.test_direct_read_outside_config_is_warn` |
| SA-03 | A `getattr(settings, …)` read outside `config.py` is a warn — the defaulted form bypasses the accessor just as the direct one does | `CheckSettingsAccess.test_getattr_read_outside_config_is_warn` |
| SA-04 | Reads inside a function in `config.py` produce no findings. That is the accessor the rule asks for | `CheckSettingsAccess.test_reads_inside_config_are_clean` |
| SA-05 | A settings read at module scope in `config.py` is a warn. It is in the right file and still evaluates at import time, which is the failure the rule exists to prevent | `CheckSettingsAccess.test_module_scope_read_in_config_is_warn` |
| SA-06 | `from django.conf import settings` at module scope is a warn, wherever it appears | `CheckSettingsAccess.test_module_scope_import_is_warn` |
| SA-07 | The same import inside a function produces no findings | `CheckSettingsAccess.test_import_inside_a_function_is_clean` |
| SA-08 | `tests.py` is exempt — a test legitimately reaches for settings directly | `CheckSettingsAccess.test_tests_module_is_exempt` |
| SA-09 | A library with no package produces no findings | `CheckSettingsAccess.test_no_package_is_silent` |

## BV — `check_boot_validation`

Covers the boot half of *Reading settings*: required settings are validated once in `check_settings()`,
which lives in `config.py` and is called from `AppConfig.ready()`.

Five libraries define a validator and all five call it, so **an uncalled or misplaced validator is an
error** — free today, and it catches the one failure that is otherwise silent: a validator nothing
calls, which looks like validation and performs none. Two of the five name it `validate_settings`,
so **the name is a warn**.

The inverse is not decidable. A library with required settings and no validator at all is invisible
here, because the linter cannot know which of a library's settings are required. That is the judgment
layer's.

| ID | Case | Test function |
|---|---|---|
| BV-01 | A `check_settings` in `config.py` called from `ready()` produces no findings | `CheckBootValidation.test_clean` |
| BV-02 | A validator defined but not called from `ready()` is an error. It looks like validation and performs none | `CheckBootValidation.test_uncalled_validator_is_error` |
| BV-03 | A library defining no validator produces no findings — the linter cannot know which settings are required | `CheckBootValidation.test_no_validator_is_silent` |
| BV-04 | A validator defined outside `config.py` is an error. One function, one place, in every library | `CheckBootValidation.test_validator_outside_config_is_error` |
| BV-05 | A validator named `validate_settings` rather than `check_settings` is a warn | `CheckBootValidation.test_nonstandard_validator_name_is_warn` |
| BV-06 | A call somewhere in `apps.py` but outside `ready()` does not satisfy it — boot is the point | `CheckBootValidation.test_call_outside_ready_does_not_count` |
| BV-07 | A library with no package produces no findings | `CheckBootValidation.test_no_package_is_silent` |

## EI — `check_evennia_imports`

Covers *Importing Evennia*: every import site carries a comment saying why that module needs the
engine. There is no default home — `log.py` imports `evennia-logging-extension`, which holds the
Evennia coupling, so a library with no other need for the engine imports it nowhere.

A **warn**, and a large one — 95 of the 102 Evennia imports outside `log.py` have no comment today,
and every `log.py` import joins them once the libraries migrate. The corpus predates the rule, so this
is a queue.

`tests.py` and `tests/` are exempt: they exist to emulate a running game, so the import is the job.

The comment is looked for on the line above the import, which is where the standard's example puts it.
A comment elsewhere in the module does not count — the rule is that a reader landing on the import can
see the reason without hunting.

| ID | Case | Test function |
|---|---|---|
| EI-01 | A library that imports Evennia nowhere produces no findings | `CheckEvenniaImports.test_clean` |
| EI-02 | An import elsewhere with a comment on the line above produces no findings | `CheckEvenniaImports.test_commented_import_is_clean` |
| EI-03 | An import elsewhere with no comment is a warn naming the module | `CheckEvenniaImports.test_uncommented_import_is_warn` |
| EI-04 | `import evennia` counts as well as `from evennia… import …` | `CheckEvenniaImports.test_plain_import_counts` |
| EI-05 | `tests.py` is exempt | `CheckEvenniaImports.test_tests_module_is_exempt` |
| EI-06 | A library with no package produces no findings | `CheckEvenniaImports.test_no_package_is_silent` |
| EI-07 | An uncommented Evennia import in `log.py` is a warn like any other. `log.py` is no longer exempt, and the skip that made it so has to go | `CheckEvenniaImports.test_an_import_in_the_shim_is_not_exempt` |

## OS — `check_object_state`

Covers *Reading and writing object state*: a library sets its own attributes by assignment, never
through `.db`, because `.db` goes through the `AttributeHandler` and never reaches the descriptor's
`at_set()`.

A **warn**: four libraries write through `.db`, 64 sites between them.

| ID | Case | Test function |
|---|---|---|
| OS-01 | A library making no `.db` writes produces no findings | `CheckObjectState.test_clean` |
| OS-02 | A `.db` write is a warn naming the module. An unvalidated property is one commit away from a validated one, and every `.db` write that was harmless before is then silently wrong | `CheckObjectState.test_db_write_is_warn` |
| OS-03 | A `.db` *read* is not a finding — the bypass the standard names is the write | `CheckObjectState.test_db_read_is_not_a_finding` |
| OS-04 | `tests.py` is exempt | `CheckObjectState.test_tests_module_is_exempt` |

## BS — `check_boot_side_effects`

Covers the prohibition in *Consumer-authored config*: a library does not create directories in the
consumer's gamedir. Where those modules sit is the consumer's business, and a library that creates one
takes the decision away and leaves something behind in a repo it does not own.

A **warn**; two libraries call `mkdir`/`makedirs` today.

| ID | Case | Test function |
|---|---|---|
| BS-01 | A library creating no directories produces no findings | `CheckBootSideEffects.test_clean` |
| BS-02 | An `os.makedirs` call is a warn naming the module | `CheckBootSideEffects.test_makedirs_is_warn` |
| BS-03 | A `Path.mkdir` call is a warn — the same act through a different API | `CheckBootSideEffects.test_path_mkdir_is_warn` |
| BS-04 | `tests.py` is exempt; a test builds its own scratch directories | `CheckBootSideEffects.test_tests_module_is_exempt` |

## DB — `check_database`

Covers *Database aliases and routers*: a library owning tables on an alias depends on
`evennia-database-cascade` and declares a `db_spec` — no router, no `DATABASES` entry, no resolution
code of its own. The cascade derives routing and migration from one answer; hand-rolled they can
disagree, and the failure is silent.

Severities follow the logging precedent: a hand-rolled router or resolution is the wrong mechanism,
so `DB-09`/`DB-10` are **errors** — the migration queue, exactly as `log_shim_mechanism` is for
logging. Four libraries report them today. A `models.py` with no spec is a **warn**: it is either
un-migrated or legitimately game-database-scoped, and the `CLAUDE.md` pin that distinguishes those is
the judgment layer's to read.

`tests.py` is exempt from `DB-09` and `DB-10`, as it is everywhere in this linter — a test
legitimately builds router doubles and environment fixtures.

| ID | Case | Test function |
|---|---|---|
| DB-01 | A library with no `models.py` produces no findings | `CheckDatabase.test_no_models_is_silent` |
| DB-08 | A `models.py` with no `db_spec.py` is a warn — either un-migrated or legitimately game-database-scoped; the `CLAUDE.md` pin is the judgment layer's to read. A spec beside the models clears it | `CheckDatabase.test_models_without_spec_is_warn` |
| DB-09 | A `db_router.py`, or a class defining `db_for_read`/`db_for_write`/`allow_migrate` in any module but `tests.py`, is an error — it steers databases and it is the wrong mechanism. This is what an un-migrated library reports | `CheckDatabase.test_hand_rolled_router_is_error` |
| DB-10 | Hand-rolled resolution — `dj_database_url` imported, or an environ read of a `DATABASE_URL*` literal, outside `tests.py` — is an error naming the module | `CheckDatabase.test_hand_rolled_resolution_is_error` |
| DB-11 | A `db_spec.py` with no `evennia-database-cascade` in `pyproject.toml` dependencies is a warn. The spec imports it, so without the declaration the library works only where something else happened to install it | `CheckDatabase.test_spec_without_dependency_is_warn` |
| DB-12 | A `db_spec.py` importing Django at module scope is an error — the spec sits on the consumer's settings path, before `django.setup()` | `CheckDatabase.test_spec_importing_django_is_error` |
| DB-13 | An `installing.md` documenting `DATABASE_ROUTERS` or hand-written `DATABASES[…]` entries is a warn — it names the cascade dependency and points at the cascade's own docs. The `DATABASES, DATABASE_ROUTERS = configure(…)` call is the cascade's shape and is not a finding | `CheckDatabase.test_installing_documenting_databases_is_warn` |
| DB-14 | `evennia-database-cascade` itself produces no findings here — its `router.py` and environ reads *are* the mechanism | `CheckDatabase.test_the_cascade_itself_is_exempt` |
| DB-15 | A `models.py` with a `db_spec.py`, the declared dependency and an `installing.md` showing the `configure()` call produces no findings | `CheckDatabase.test_spec_with_dependency_is_clean` |

**Retired.** `DB-02` to `DB-07` enforced the hand-rolled pattern — the library's own router, the
`describe_*_database()` helper pair, and the `DATABASE_ROUTERS` append snippet — which the cascade
replaces. IDs are not reused.

## TG — `check_targeting`

Covers *Targeting callables live in `targeting.py`*: a library depending on `evennia-targeting`
declares its `p_`, `f_` and `op_` callables there and nowhere else.

Both **warns**. Nothing depends on `evennia-targeting` today, so both are no-ops on the corpus — but
`evennia-equipment` already carries a `targeting.py`, which is what the second rule binds to.

The dependency is read from an unconditional import or a `pyproject.toml` dependency. `evennia-targeting`
itself is excluded by construction: it does not depend on itself, and its own callables are its
implementation rather than a consumer's.

| ID | Case | Test function |
|---|---|---|
| TG-01 | A library not depending on targeting and carrying no `targeting.py` produces no findings | `CheckTargeting.test_no_dependency_is_silent` |
| TG-02 | A library importing `evennia_targeting` with no `targeting.py` is a warn | `CheckTargeting.test_dependency_without_module_is_warn` |
| TG-03 | A `p_`, `f_` or `op_` declared outside `targeting.py` is a warn naming it. One filename makes the corpus findable, so a session about to write `p_is_wielded` can discover somebody already did | `CheckTargeting.test_callable_outside_module_is_warn` |
| TG-04 | The same callables inside `targeting.py` produce no findings | `CheckTargeting.test_callables_inside_module_are_clean` |
| TG-05 | A library carrying a `targeting.py` is held to the rule even without an import — the file is the declaration of intent | `CheckTargeting.test_module_alone_binds_the_rule` |
| TG-06 | `tests.py` is exempt | `CheckTargeting.test_tests_module_is_exempt` |
| TG-07 | `evennia-targeting` itself is excluded. It re-exports its own callables from `__init__.py` by absolute import, which reads as depending on itself — and its callables are the implementation rather than a consumer's declaration | `CheckTargeting.test_targeting_library_itself_is_excluded` |

## CT — `check_contrib`

Covers *contrib/ — conditional*: the folder exists only when there are contrib modules in it, and
nothing in it may be imported by core.

**A warn for an empty scaffold, an error for a core import.** No library has a `contrib/` today, so
both are free — and the second is the load-bearing one: if core needs it, it isn't contrib, and the
separation exists only on paper the moment core reaches in.

| ID | Case | Test function |
|---|---|---|
| CT-01 | A library with no `contrib/` produces no findings | `CheckContrib.test_no_contrib_is_silent` |
| CT-02 | A `contrib/` holding only `__init__.py` is a warn — its presence is the signal that opt-in modules are available, so an empty one is a false signal | `CheckContrib.test_empty_contrib_is_warn` |
| CT-03 | A `contrib/` holding a module produces no findings | `CheckContrib.test_populated_contrib_is_clean` |
| CT-04 | A core module importing from `contrib` is an error. Core must remain fully functional with the directory absent | `CheckContrib.test_core_importing_contrib_is_error` |
| CT-05 | A contrib module importing another contrib module is fine — the rule is about the direction, not the folder | `CheckContrib.test_contrib_importing_contrib_is_clean` |

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
