# Test plan — doc-convention-linter

Every test case the linter commits to covering, and the test function that covers it. The **Test
function** column is the auditable trail — an empty cell means the case is agreed but not yet covered.

Case IDs are stable and referenceable. Do not renumber; retire an ID rather than reuse it. Each test
function carries its case ID as its docstring, so the trail reads in both directions.

All test functions live in `tests.py`, beside this plan. Run them with
`python .claude/skills/doc-convention-linter/tests.py`.

| Prefix | Covers |
|---|---|
| `HP` | Pure helpers — `KEBAB_RE`, `find_h1`, `body_after_frontmatter`, `fenced_line_indices`, `resolve_link`, `links_in`, `path_in_scope`, `rel` |
| `DS` | `discover` / `Context` — corpus discovery and the structured/loose split — with `check_docs_present` and `check_index_present`, the structure a corpus must have before its contents are checked |
| `KB` | `check_filename_kebab` |
| `HD` | `check_h1` |
| `SM` | `check_summary` |
| `BL` | `check_broken_links` |
| `NI` | `check_not_indexed` |
| `OR` | `check_orphaned` |
| `WP` | `check_was_phrasing` |
| `SC` | `lint` — scope narrowing and the file/root counts |
| `CL` | CLI: `main`, `render_human`, exit codes, `--json`, `--root` |
| `XC` | Cross-cutting |

## Fixtures

The suite needs no network and no real corpus — every case builds a synthetic doc tree in a temp dir
and calls one check in isolation.

| Fixture | Purpose |
|---|---|
| `CLEAN` | A minimal fully-correct corpus: one `design/` root, an `INDEX.md` linking one good doc |
| `LOOSE` | `CLEAN` plus the loose surfaces (`README.md`, `CLAUDE.md`, `.claude/memory/some_file.md`) — for the structured-vs-loose exemption cases |
| `TWO_ROOTS` | `CLEAN` plus a `libraries/my-lib/docs/` root — for the per-root cases |
| `SCOPED` | Two docs with a broken link each, one linking the other — for the scope cases |
| `MIXED` | One finding at each severity: a broken link, an unindexed orphan, a `was_phrasing` line |
| `build_tree(spec)` | Writes a spec dict to a `TemporaryDirectory` and returns `(tmp, root)` |
| `TreeBase.tree(drop=…, base=…, **changes)` | Builds a mutated corpus and returns its root |
| `TreeBase.ctx(…)` | The same, returning the built `Context`, so a single check can be called on its own |
| `CheckBase.assert_clean()` | Runs one check over a clean corpus, asserting the file list is non-empty first |
| `kinds(findings, severity, path)` | The set of `check` names, optionally filtered — assertions name the check and its severity, not the message |
| `paths(findings, check)` | The set of paths reported, for asserting exactly which files a check named |
| `Cli.run_cli(spec, *argv)` | Runs `main()` against a temp tree with stdout captured; returns `(exit_code, output)` |

## HP — pure helpers

| ID | Case | Test function |
|---|---|---|
| HP-01 | `KEBAB_RE` accepts kebab `.md` names and rejects caps, underscores, spaces and non-`.md` | `HelperTests.test_kebab_regex` |
| HP-02 | `find_h1` returns `(index, title)` when the first content line is an H1 | `HelperTests.test_find_h1_returns_index_and_title` |
| HP-03 | `find_h1` returns `None` when the first content line is not an H1, and for an `##` heading | `HelperTests.test_find_h1_returns_none_when_first_content_line_is_not_h1` |
| HP-04 | `body_after_frontmatter` skips a leading `---` YAML block, and returns 0 when there is none | `HelperTests.test_body_after_frontmatter` |
| HP-05 | `fenced_line_indices` marks both fence lines and everything between them | `HelperTests.test_fenced_line_indices` |
| HP-06 | `resolve_link` returns `None` for `http://`, `https://` and bare `#anchor` targets | `HelperTests.test_resolve_link_ignores_external_and_anchor_targets` |
| HP-07 | `resolve_link` returns `None` for `mailto:` and `tel:` targets | `HelperTests.test_resolve_link_ignores_mailto_and_tel` |
| HP-08 | `resolve_link` strips a `#anchor` and a trailing `("title")` from the target | `HelperTests.test_resolve_link_strips_anchor_and_title` |
| HP-09 | `resolve_link` resolves relative to the source file's directory, including `../` | `HelperTests.test_resolve_link_resolves_relative_to_source_dir` |
| HP-10 | `resolve_link` resolves a root-absolute `/a/b.md` against the repo root, not the filesystem root | `HelperTests.test_resolve_link_resolves_root_absolute_against_repo_root` |
| HP-11 | `links_in` ignores links inside `` `inline code` `` | `HelperTests.test_links_in_skips_inline_code` |
| HP-12 | `links_in` skips lines inside a fenced block | `HelperTests.test_links_in_skips_fenced_lines` |
| HP-13 | `links_in` captures image links `![alt](x.png)` | `HelperTests.test_links_in_captures_image_links` |
| HP-14 | `path_in_scope` matches an exact file and a directory prefix, and rejects an unrelated path | `HelperTests.test_path_in_scope_matches_file_and_directory` |
| HP-15 | `path_in_scope` matches only at a path boundary — scope `design/a` does not match `design/ab.md` | `HelperTests.test_path_in_scope_matches_only_at_path_boundary` |
| HP-16 | `rel` falls back to the absolute string for a path outside the root | `HelperTests.test_rel_falls_back_to_absolute_outside_root` |

## DS — `discover` / `Context`

| ID | Case | Test function |
|---|---|---|
| DS-01 | A directory matching a doc-root glob is a docs root; its `*.md` are structured | `DiscoveryTests.test_doc_root_files_are_structured` |
| DS-02 | A docs root with no `INDEX.md` is a `missing_index` error naming the directory | `DiscoveryTests.test_docs_root_without_index_is_error` |
| DS-03 | `libraries/*/docs` roots are discovered alongside `design` | `DiscoveryTests.test_library_docs_roots_are_discovered` |
| DS-04 | `README.md`, `CLAUDE.md` and `.claude/memory/*.md` are discovered as loose, never structured | `DiscoveryTests.test_loose_surfaces_are_loose_not_structured` |
| DS-05 | A file matching two loose globs appears in the corpus once | `DiscoveryTests.test_duplicate_loose_glob_yields_one_entry` |
| DS-06 | Non-`.md` files in a docs root are not part of the corpus | `DiscoveryTests.test_non_markdown_files_are_not_in_the_corpus` |
| DS-07 | A root with neither `design/` nor `libraries/` yields an empty corpus and does not raise | `DiscoveryTests.test_root_without_docs_or_libraries_is_empty` |
| DS-08 | `Context.inbound` counts links from loose surfaces as well as from structured docs | `DiscoveryTests.test_inbound_counts_links_from_loose_surfaces` |
| DS-09 | A library under `libraries/` with no `docs/` directory at all is a `missing_docs` error naming the library | `DiscoveryTests.test_library_without_docs_dir_is_error` |
| DS-10 | The remaining checks still run over a root whose `INDEX.md` is missing — one absent file does not suppress the rest | `DiscoveryTests.test_other_checks_still_run_without_an_index` |
| DS-11 | `not_indexed` emits nothing for a root with no `INDEX.md` — the missing index is the finding | `DiscoveryTests.test_not_indexed_is_silent_without_an_index` |

## KB — `check_filename_kebab`

| ID | Case | Test function |
|---|---|---|
| KB-01 | A non-kebab filename in a docs root is a `filename_not_kebab` error | `CheckFilenameKebab.test_non_kebab_filename_is_error` |
| KB-02 | `INDEX.md`, `README.md`, `CLAUDE.md` and `MEMORY.md` are exempt inside a docs root | `CheckFilenameKebab.test_exempt_names_are_not_reported` |
| KB-03 | A snake_case loose file (`.claude/memory/some_file.md`) is not reported — loose surfaces are exempt | `CheckFilenameKebab.test_loose_snake_case_file_is_exempt` |
| KB-04 | Called in isolation over a clean corpus, returns `[]` — with the file list asserted non-empty, so a check that saw nothing cannot read as clean | `CheckFilenameKebab.test_clean` |

## HD — `check_h1`

| ID | Case | Test function |
|---|---|---|
| HD-01 | A doc whose first content line is not an H1 is an `h1_missing` error | `CheckH1.test_missing_h1_is_error` |
| HD-02 | `INDEX.md` is skipped — it has its own shape | `CheckH1.test_index_is_skipped` |
| HD-03 | A loose file with no H1 is not reported | `CheckH1.test_loose_file_without_h1_is_not_reported` |
| HD-04 | An H1 following a YAML frontmatter block counts as present | `CheckH1.test_h1_after_frontmatter_counts` |
| HD-05 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckH1.test_clean` |

## SM — `check_summary`

| ID | Case | Test function |
|---|---|---|
| SM-01 | An H1 followed straight by another heading is a `summary_missing` warn | `CheckSummary.test_heading_straight_after_h1_is_warn` |
| SM-02 | A doc with no H1 produces no summary finding — `check_h1` owns that absence | `CheckSummary.test_no_h1_produces_no_summary_finding` |
| SM-03 | `INDEX.md` is skipped | `CheckSummary.test_index_is_skipped` |
| SM-04 | An H1 with nothing after it is a `summary_missing` warn | `CheckSummary.test_h1_with_nothing_after_it_is_warn` |
| SM-05 | The finding's line number is the 1-based H1 line | `CheckSummary.test_line_number_is_the_h1_line` |
| SM-06 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckSummary.test_clean` |

## BL — `check_broken_links`

| ID | Case | Test function |
|---|---|---|
| BL-01 | A relative link to a missing file is a `broken_link` error naming the target | `CheckBrokenLinks.test_missing_target_is_error` |
| BL-02 | External (`http`, `https`, `mailto`, `tel`) and bare `#anchor` targets are never reported | `CheckBrokenLinks.test_external_and_anchor_targets_are_ignored` |
| BL-03 | A link inside a fenced block is not reported | `CheckBrokenLinks.test_link_inside_a_fence_is_ignored` |
| BL-04 | A broken link in a loose surface is reported — the check is corpus-wide | `CheckBrokenLinks.test_broken_link_in_a_loose_surface_is_reported` |
| BL-05 | A link that resolves, including one `../` out of the docs root, is silent | `CheckBrokenLinks.test_resolving_link_out_of_the_docs_root_is_silent` |
| BL-06 | The finding carries the 1-based line number of the link | `CheckBrokenLinks.test_line_number_is_the_link_line` |
| BL-07 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckBrokenLinks.test_clean` |

## NI — `check_not_indexed`

| ID | Case | Test function |
|---|---|---|
| NI-01 | A docs file not linked from its `INDEX.md` is a `not_indexed` warn | `CheckNotIndexed.test_unindexed_doc_is_warn` |
| NI-02 | A file linked from its `INDEX.md` is not reported | `CheckNotIndexed.test_indexed_doc_is_not_reported` |
| NI-03 | `INDEX.md` itself is never reported | `CheckNotIndexed.test_index_itself_is_never_reported` |
| NI-04 | Indexing is per-root — a link from another root's `INDEX.md` does not satisfy it | `CheckNotIndexed.test_indexing_is_per_root` |
| NI-05 | An `INDEX.md` link written inside a fence does not count as indexing | `CheckNotIndexed.test_index_link_inside_a_fence_does_not_count` |
| NI-06 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckNotIndexed.test_clean` |

## OR — `check_orphaned`

| ID | Case | Test function |
|---|---|---|
| OR-01 | A docs file with no inbound link anywhere is an `orphaned` warn | `CheckOrphaned.test_doc_with_no_inbound_link_is_warn` |
| OR-02 | An inbound link from its `INDEX.md` prevents the finding | `CheckOrphaned.test_inbound_link_from_index_prevents_it` |
| OR-03 | An inbound link from another docs file prevents the finding | `CheckOrphaned.test_inbound_link_from_another_doc_prevents_it` |
| OR-04 | An inbound link from a loose surface (`CLAUDE.md`, a memory file) prevents the finding | `CheckOrphaned.test_inbound_link_from_a_loose_surface_prevents_it` |
| OR-05 | `INDEX.md` is never orphaned, and loose files are never reported at all | `CheckOrphaned.test_index_and_loose_files_are_never_orphaned` |
| OR-06 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckOrphaned.test_clean` |

## WP — `check_was_phrasing`

| ID | Case | Test function |
|---|---|---|
| WP-01 | A trigger phrase is a `was_phrasing` advisory naming the phrase, at its 1-based line | `CheckWasPhrasing.test_trigger_phrase_is_advisory_with_line_number` |
| WP-02 | Matching is case-insensitive | `CheckWasPhrasing.test_matching_is_case_insensitive` |
| WP-03 | A phrase inside a fenced block is not reported | `CheckWasPhrasing.test_phrase_inside_a_fence_is_ignored` |
| WP-04 | Matching is word-bounded — `formerly` matches, `reformerly` does not | `CheckWasPhrasing.test_matching_is_word_bounded` |
| WP-05 | Every phrase in `WAS_PATTERNS` is matched by `WAS_RE` — the list and the regex cannot drift | `CheckWasPhrasing.test_every_pattern_is_matched_by_the_regex` |
| WP-06 | A phrase in a loose surface is reported — the check is corpus-wide | `CheckWasPhrasing.test_phrase_in_a_loose_surface_is_reported` |
| WP-07 | Called in isolation over a clean corpus, returns `[]`, with the file list asserted non-empty | `CheckWasPhrasing.test_clean` |

## SC — `lint` scope and counts

| ID | Case | Test function |
|---|---|---|
| SC-01 | Unscoped, findings from every file in the corpus are reported | `ScopeTests.test_unscoped_reports_every_file` |
| SC-02 | A single-file scope reports only that file's findings, and counts one file in one root | `ScopeTests.test_file_scope_reports_only_that_file` |
| SC-03 | Analysis stays global — a doc kept off the orphan list by a link from outside the scope is still not orphaned | `ScopeTests.test_scope_keeps_global_context` |
| SC-04 | A directory scope reports findings from every file under it | `ScopeTests.test_directory_scope_reports_every_file_under_it` |
| SC-05 | A scope with a trailing slash behaves identically to one without | `ScopeTests.test_trailing_slash_scope_behaves_the_same` |
| SC-06 | `n_roots` counts only the docs roots holding an in-scope file | `ScopeTests.test_n_roots_counts_only_roots_with_in_scope_files` |
| SC-07 | A scope matching nothing returns no findings and zero files, and does not raise | `ScopeTests.test_scope_matching_nothing_is_empty` |
| SC-08 | Unscoped, `n_files` and `n_roots` count the whole corpus, loose surfaces included | `ScopeTests.test_unscoped_counts_the_whole_corpus` |

## CL — CLI and output

| ID | Case | Test function |
|---|---|---|
| CL-01 | A clean corpus exits 0 | `Cli.test_clean_corpus_exits_zero` |
| CL-02 | Any error exits 1 | `Cli.test_error_exits_one` |
| CL-03 | Warnings alone exit 0 — only an `error` fails the run | `Cli.test_warnings_alone_exit_zero` |
| CL-04 | Advisories alone exit 0 | `Cli.test_advisories_alone_exit_zero` |
| CL-05 | `--json` emits parseable JSON carrying every finding and the error/warn/advisory counts | `Cli.test_json_carries_findings_and_counts` |
| CL-06 | `--json` orders findings error → warn → advisory, then by path and line | `Cli.test_json_orders_by_severity_then_path_and_line` |
| CL-07 | `render_human` groups by severity and ends with the `Scanned N files across M docs/ root(s)` line | `Cli.test_render_human_groups_by_severity_and_summarises` |
| CL-08 | `--root` points the scan at another directory, and scope arguments stay relative to it | `Cli.test_root_argument_scans_another_directory` |
| CL-09 | There is no `--strict` option — passing it is an argument error, not a stricter run | `Cli.test_strict_is_not_an_option` |

## XC — cross-cutting

| ID | Case | Test function |
|---|---|---|
| XC-01 | A clean corpus produces no findings from any check | `CrossCutting.test_clean_corpus_has_no_findings` |
| XC-02 | Inject then restore — clean, then a broken link, then clean again | `CrossCutting.test_inject_then_restore` |
| XC-03 | Every check in `CHECKS` is named by at least one case in this plan | `CrossCutting.test_every_check_is_named_in_the_plan` |
| XC-04 | This plan and this suite agree in both directions — delegated to the `test-plan-linter` skill, asserting it reports no errors | `CrossCutting.test_every_test_is_named_in_the_plan` |
| XC-05 | Finding paths are repo-relative, never absolute | `CrossCutting.test_finding_paths_are_repo_relative` |
| XC-06 | Every finding's severity is one of `error` / `warn` / `advisory` | `CrossCutting.test_every_severity_is_known` |
| XC-07 | `missing_docs` agrees with the `library-standards-linter` — both recognise the same directory as a library, both report the absent `docs/`, at the same severity. Skipped where that skill is not deployed alongside | `CrossCutting.test_missing_docs_agrees_with_the_library_linter` |

## Open decisions

None outstanding.

## Settled

- **`--strict` does not exist.** Only an `error` fails the run (CL-02, CL-03, CL-04). An advisory is a
  "go and check this" signal a human or agent adjudicates; a legitimate one — "use X, not Y" — can
  never be cleared, so gating a commit on it would only teach people to suppress the check (CL-09).
- **Structure is validated before its contents.** A library with no `docs/` (DS-09) and a docs root
  with no `INDEX.md` (DS-02) are both errors. The remaining checks still run over that root's files
  (DS-10); one missing file does not silence the rest.
- **Every check is exercised in isolation over a clean corpus** (KB-04, HD-05, SM-06, BL-07, NI-06,
  OR-06, WP-07), each asserting a non-empty file list. A check that silently receives no files
  otherwise reads as clean, and XC-01 alone cannot tell the two apart.
- **`missing_docs` is deliberately checked twice.** The `library-standards-linter` reports the same
  absence. Duplication between two read-only reporters costs a line of output; the risk is the two
  drifting on what counts as a library or how bad the absence is, so XC-07 pins them together and goes
  red on a divergence. Extraction into a shared helper is the answer once the overlap grows past a
  line or two — not for a single `is_dir()`.
- **XC-04 is delegated, not reimplemented.** The `test-plan-linter` skill owns plan-vs-suite checking;
  this suite imports it for the self-check only. The linter itself reads docs, not test plans, so
  `lint.py` carries no dependency on it.
