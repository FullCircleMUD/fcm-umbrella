#!/usr/bin/env python3
"""Unit tests for the doc-convention-linter. Stdlib only (no pytest) so they ship
and run with the skill anywhere:
    python .claude/skills/doc-convention-linter/tests.py

Every case is agreed in test-plan.md first; each test names its case ID in its
docstring, so the coverage trail reads in both directions. Each check is exercised
in isolation against a synthetic corpus, plus integration tests over lint(), the
scope filter, the CLI, and an inject/restore round trip.

The plan-vs-suite self-check (XC-04) is delegated to the test-plan-linter skill,
imported here only for that purpose — this linter reads docs, not test plans."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "test-plan-linter"))
import lint  # noqa: E402
import lint_test_plan as plan_linter  # noqa: E402

PLAN_PATH = HERE / "test-plan.md"
LIB_LINTER = HERE.parent / "library-standards-linter"   # XC-07 only, and optional


# --- fixtures ----------------------------------------------------------------
# A minimal, fully-correct corpus: one docs/ root, an INDEX linking one good doc.
CLEAN = {
    "design/INDEX.md": "# Index\n\nThe docs catalogue.\n\n- [good](good.md)\n",
    "design/good.md": "# Good Doc\n\nA one-paragraph summary.\n\nBody text.\n",
}

# CLEAN plus the loose surfaces — link and was_phrasing checks only, never held to
# the kebab / H1 / summary rules.
LOOSE = {
    **CLEAN,
    "README.md": "# FCM\n\nThe workspace.\n",
    "CLAUDE.md": "Free-form operating context. No H1, by design.\n",
    ".claude/memory/some_file.md": "---\nname: some-file\n---\n\nA remembered fact.\n",
}

# Two docs/ roots, for the per-root cases.
TWO_ROOTS = {
    **CLEAN,
    "libraries/my-lib/docs/INDEX.md": "# Index\n\nLibrary docs.\n\n- [other](other.md)\n",
    "libraries/my-lib/docs/other.md": "# Other\n\nA summary.\n",
}

# Two docs with a broken link each, one linking the other — for the scope cases.
SCOPED = {
    "design/INDEX.md": "# Index\n\nCatalogue.\n\n- [a](a.md)\n- [b](b.md)\n",
    "design/a.md": "# A\n\nSummary.\n\n[bad](nope-a.md)\n",
    "design/b.md": "# B\n\nSummary.\n\n[to a](a.md) and [bad](nope-b.md)\n",
}

# One finding at each severity: broken_link (error), not_indexed + orphaned (warn),
# was_phrasing (advisory).
MIXED = {
    "design/INDEX.md": "# Index\n\nCatalogue.\n\n- [good](good.md)\n",
    "design/good.md": "# Good Doc\n\nSummary.\n\nSee [x](missing.md). It was formerly here.\n",
    "design/lonely.md": "# Lonely\n\nSummary.\n",
}


def build_tree(spec):
    """Write {relpath: content} into a temp dir; return (TemporaryDirectory, root)."""
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for relpath, content in spec.items():
        f = root / relpath
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    return tmp, root


def kinds(findings, severity=None, path=None):
    """The set of check names, optionally at one severity or for one path."""
    return {f.check for f in findings
            if (severity is None or f.severity == severity)
            and (path is None or f.path == path)}


def paths(findings, check=None):
    return {f.path for f in findings if check is None or f.check == check}


class TreeBase(unittest.TestCase):
    """Builds a corpus (CLEAN by default, mutated by drop= and **changes) and
    returns either the root or the built Context."""

    BASE = CLEAN

    def tree(self, drop=(), base=None, **changes):
        spec = dict(self.BASE if base is None else base)
        for k in drop:
            spec.pop(k, None)
        spec.update(changes)
        tmp, root = build_tree(spec)
        self.addCleanup(tmp.cleanup)
        return root

    def ctx(self, drop=(), base=None, **changes):
        return lint.build_context(self.tree(drop, base, **changes))


class CheckBase(TreeBase):
    """One check, called on its own against a Context."""

    CHECK = None

    def assert_clean(self, base=None):
        """A clean corpus produces nothing — with the file list asserted non-empty,
        so a check that silently received no files cannot read as clean."""
        ctx = self.ctx(base=base)
        self.assertTrue(ctx.structured, "no structured docs: the check saw nothing")
        self.assertTrue(ctx.corpus, "empty corpus: the check saw nothing")
        self.assertEqual(self.CHECK(ctx), [])


# --- HP: pure helpers --------------------------------------------------------
class HelperTests(unittest.TestCase):
    def test_kebab_regex(self):
        """HP-01"""
        for n in ["good.md", "good-name.md", "a1-b2-c3.md"]:
            self.assertRegex(n, lint.KEBAB_RE)
        for n in ["Bad.md", "bad_name.md", "Bad-Name.md", "spaces here.md", "x.txt"]:
            self.assertNotRegex(n, lint.KEBAB_RE)

    def test_find_h1_returns_index_and_title(self):
        """HP-02"""
        self.assertEqual(lint.find_h1(["# Title", "x"], 0), (0, "Title"))
        self.assertEqual(lint.find_h1(["", "", "# Late Title"], 0), (2, "Late Title"))

    def test_find_h1_returns_none_when_first_content_line_is_not_h1(self):
        """HP-03"""
        self.assertIsNone(lint.find_h1(["text first", "# Late"], 0))
        self.assertIsNone(lint.find_h1(["## Sub"], 0))
        self.assertIsNone(lint.find_h1([], 0))

    def test_body_after_frontmatter(self):
        """HP-04"""
        self.assertEqual(lint.body_after_frontmatter(["---", "name: x", "---", "# T"]), 3)
        self.assertEqual(lint.body_after_frontmatter(["# Title"]), 0)

    def test_fenced_line_indices(self):
        """HP-05"""
        lines = ["before", "```", "in fence", "```", "after"]
        self.assertEqual(lint.fenced_line_indices(lines), {1, 2, 3})

    def test_resolve_link_ignores_external_and_anchor_targets(self):
        """HP-06"""
        src, root = Path("/repo/docs/a.md"), Path("/repo")
        for t in ["https://x.com", "http://x.com", "#anchor", ""]:
            self.assertIsNone(lint.resolve_link(src, t, root))

    def test_resolve_link_ignores_mailto_and_tel(self):
        """HP-07"""
        src, root = Path("/repo/docs/a.md"), Path("/repo")
        self.assertIsNone(lint.resolve_link(src, "mailto:x@y.com", root))
        self.assertIsNone(lint.resolve_link(src, "tel:+61000", root))

    def test_resolve_link_strips_anchor_and_title(self):
        """HP-08"""
        src, root = Path("/repo/docs/a.md"), Path("/repo")
        self.assertEqual(lint.resolve_link(src, "b.md#sec", root), Path("/repo/docs/b.md"))
        self.assertEqual(lint.resolve_link(src, 'b.md "Title"', root), Path("/repo/docs/b.md"))

    def test_resolve_link_resolves_relative_to_source_dir(self):
        """HP-09"""
        src, root = Path("/repo/docs/a.md"), Path("/repo")
        self.assertEqual(lint.resolve_link(src, "b.md", root), Path("/repo/docs/b.md"))
        self.assertEqual(lint.resolve_link(src, "../CLAUDE.md", root), Path("/repo/CLAUDE.md"))

    def test_resolve_link_resolves_root_absolute_against_repo_root(self):
        """HP-10"""
        src, root = Path("/repo/docs/a.md"), Path("/repo")
        self.assertEqual(lint.resolve_link(src, "/design/x.md", root),
                         Path("/repo/design/x.md"))

    def test_links_in_skips_inline_code(self):
        """HP-11"""
        lines = ["a real [x](real.md) and an example `[y](ex.md)`"]
        self.assertEqual([t for _, t in lint.links_in(lines, set())], ["real.md"])

    def test_links_in_skips_fenced_lines(self):
        """HP-12"""
        lines = ["[real](real.md)", "```", "[fenced](fenced.md)", "```"]
        found = lint.links_in(lines, lint.fenced_line_indices(lines))
        self.assertEqual([t for _, t in found], ["real.md"])

    def test_links_in_captures_image_links(self):
        """HP-13"""
        self.assertEqual([t for _, t in lint.links_in(["![alt](diagram.png)"], set())],
                         ["diagram.png"])

    def test_path_in_scope_matches_file_and_directory(self):
        """HP-14"""
        self.assertTrue(lint.path_in_scope("design/a.md", ["design/a.md"]))
        self.assertTrue(lint.path_in_scope("design/a.md", ["design"]))
        self.assertFalse(lint.path_in_scope("design/b.md", ["design/a.md"]))
        self.assertFalse(lint.path_in_scope("README.md", ["design"]))

    def test_path_in_scope_matches_only_at_path_boundary(self):
        """HP-15"""
        self.assertFalse(lint.path_in_scope("design/ab.md", ["design/a"]))
        self.assertTrue(lint.path_in_scope("design/a/b.md", ["design/a"]))

    def test_rel_falls_back_to_absolute_outside_root(self):
        """HP-16"""
        self.assertEqual(lint.rel(Path("/elsewhere/x.md"), Path("/repo")), "/elsewhere/x.md")


# --- DS: discovery and the Context -------------------------------------------
class DiscoveryTests(TreeBase):
    def test_doc_root_files_are_structured(self):
        """DS-01"""
        ctx = self.ctx()
        self.assertEqual({ctx.rel(d) for d in ctx.doc_roots}, {"design"})
        self.assertEqual({ctx.rel(p) for p in ctx.structured},
                         {"design/INDEX.md", "design/good.md"})

    def test_docs_root_without_index_is_error(self):
        """DS-02"""
        findings, _, _ = lint.lint(self.tree(drop=["design/INDEX.md"]))
        self.assertIn("missing_index", kinds(findings, "error"))

    def test_library_docs_roots_are_discovered(self):
        """DS-03"""
        ctx = self.ctx(base=TWO_ROOTS)
        self.assertEqual({ctx.rel(d) for d in ctx.doc_roots},
                         {"design", "libraries/my-lib/docs"})

    def test_loose_surfaces_are_loose_not_structured(self):
        """DS-04"""
        ctx = self.ctx(base=LOOSE)
        self.assertEqual({ctx.rel(p) for p in ctx.loose},
                         {"README.md", "CLAUDE.md", ".claude/memory/some_file.md"})
        self.assertEqual({ctx.rel(p) for p in ctx.structured},
                         {"design/INDEX.md", "design/good.md"})

    def test_duplicate_loose_glob_yields_one_entry(self):
        """DS-05"""
        original = lint.LOOSE_GLOBS
        lint.LOOSE_GLOBS = ["README.md", "README.md"]
        self.addCleanup(setattr, lint, "LOOSE_GLOBS", original)
        ctx = self.ctx(base=LOOSE)
        self.assertEqual([ctx.rel(p) for p in ctx.loose], ["README.md"])

    def test_non_markdown_files_are_not_in_the_corpus(self):
        """DS-06"""
        ctx = self.ctx(**{"design/notes.txt": "not markdown\n"})
        self.assertNotIn("design/notes.txt", {ctx.rel(p) for p in ctx.corpus})

    def test_root_without_docs_or_libraries_is_empty(self):
        """DS-07"""
        root = self.tree(base={"notes.txt": "nothing here\n"})
        ctx = lint.build_context(root)
        self.assertEqual(ctx.doc_roots, {})
        self.assertEqual(ctx.corpus, [])
        self.assertEqual(lint.lint(root), ([], 0, 0))

    def test_inbound_counts_links_from_loose_surfaces(self):
        """DS-08"""
        ctx = self.ctx(base=LOOSE, **{
            "design/other.md": "# Other\n\nSummary.\n",
            "CLAUDE.md": "See [other](design/other.md).\n"})
        self.assertEqual(ctx.inbound[(ctx.root / "design/other.md").resolve()], 1)

    def test_library_without_docs_dir_is_error(self):
        """DS-09"""
        findings, _, _ = lint.lint(self.tree(**{
            "libraries/my-lib/pyproject.toml": '[project]\nname = "my-lib"\n',
            "libraries/my-lib/README.md": "# my-lib\n\nA summary.\n"}))
        self.assertIn("missing_docs", kinds(findings, "error"))

    def test_other_checks_still_run_without_an_index(self):
        """DS-10"""
        findings, _, _ = lint.lint(self.tree(drop=["design/INDEX.md"],
                                             **{"design/Bad_Name.md": "no h1 here\n"}))
        self.assertIn("filename_not_kebab", kinds(findings))
        self.assertIn("h1_missing", kinds(findings))

    def test_not_indexed_is_silent_without_an_index(self):
        """DS-11"""
        findings, _, _ = lint.lint(self.tree(drop=["design/INDEX.md"]))
        self.assertNotIn("not_indexed", kinds(findings))


# --- KB: check_filename_kebab ------------------------------------------------
class CheckFilenameKebab(CheckBase):
    CHECK = staticmethod(lint.check_filename_kebab)

    def test_non_kebab_filename_is_error(self):
        """KB-01"""
        f = lint.check_filename_kebab(self.ctx(**{"design/Bad_Name.md": "# Bad\n\nS.\n"}))
        self.assertIn("filename_not_kebab", kinds(f, "error"))
        self.assertEqual(paths(f), {"design/Bad_Name.md"})

    def test_exempt_names_are_not_reported(self):
        """KB-02"""
        ctx = self.ctx(**{"design/README.md": "# R\n\nS.\n",
                          "design/CLAUDE.md": "# C\n\nS.\n",
                          "design/MEMORY.md": "# M\n\nS.\n"})
        self.assertEqual(lint.check_filename_kebab(ctx), [])

    def test_loose_snake_case_file_is_exempt(self):
        """KB-03"""
        f = lint.check_filename_kebab(self.ctx(base=LOOSE))
        self.assertNotIn(".claude/memory/some_file.md", paths(f))
        self.assertEqual(f, [])

    def test_clean(self):
        """KB-04"""
        self.assert_clean()


# --- HD: check_h1 ------------------------------------------------------------
class CheckH1(CheckBase):
    CHECK = staticmethod(lint.check_h1)

    def test_missing_h1_is_error(self):
        """HD-01"""
        f = lint.check_h1(self.ctx(**{"design/nohead.md": "No heading line.\n\nMore.\n"}))
        self.assertIn("h1_missing", kinds(f, "error"))
        self.assertEqual(paths(f), {"design/nohead.md"})

    def test_index_is_skipped(self):
        """HD-02"""
        ctx = self.ctx(**{"design/INDEX.md": "No heading.\n\n- [good](good.md)\n"})
        self.assertEqual(lint.check_h1(ctx), [])

    def test_loose_file_without_h1_is_not_reported(self):
        """HD-03"""
        self.assertEqual(lint.check_h1(self.ctx(base=LOOSE)), [])

    def test_h1_after_frontmatter_counts(self):
        """HD-04"""
        ctx = self.ctx(**{"design/fm.md": "---\nname: fm\n---\n\n# Front\n\nSummary.\n"})
        self.assertEqual(lint.check_h1(ctx), [])

    def test_clean(self):
        """HD-05"""
        self.assert_clean()


# --- SM: check_summary -------------------------------------------------------
class CheckSummary(CheckBase):
    CHECK = staticmethod(lint.check_summary)

    def test_heading_straight_after_h1_is_warn(self):
        """SM-01"""
        f = lint.check_summary(self.ctx(**{"design/nosum.md": "# T\n\n## Section\n\nbody\n"}))
        self.assertIn("summary_missing", kinds(f, "warn"))
        self.assertEqual(paths(f), {"design/nosum.md"})

    def test_no_h1_produces_no_summary_finding(self):
        """SM-02"""
        ctx = self.ctx(**{"design/nohead.md": "No heading line.\n\nMore.\n"})
        self.assertEqual(lint.check_summary(ctx), [])

    def test_index_is_skipped(self):
        """SM-03"""
        ctx = self.ctx(**{"design/INDEX.md": "# Index\n\n## Docs\n\n- [good](good.md)\n"})
        self.assertEqual(lint.check_summary(ctx), [])

    def test_h1_with_nothing_after_it_is_warn(self):
        """SM-04"""
        f = lint.check_summary(self.ctx(**{"design/bare.md": "# Only A Title\n"}))
        self.assertIn("summary_missing", kinds(f, "warn"))

    def test_line_number_is_the_h1_line(self):
        """SM-05"""
        f = lint.check_summary(self.ctx(**{"design/nosum.md": "\n# Title\n\n## Section\n"}))
        self.assertEqual([x.line for x in f], [2])

    def test_clean(self):
        """SM-06"""
        self.assert_clean()


# --- BL: check_broken_links --------------------------------------------------
class CheckBrokenLinks(CheckBase):
    CHECK = staticmethod(lint.check_broken_links)

    def test_missing_target_is_error(self):
        """BL-01"""
        f = lint.check_broken_links(self.ctx(**{
            "design/good.md": "# Good\n\nSummary.\n\nSee [x](missing-xyz.md).\n"}))
        self.assertIn("broken_link", kinds(f, "error"))
        self.assertIn("missing-xyz.md", f[0].message)

    def test_external_and_anchor_targets_are_ignored(self):
        """BL-02"""
        ctx = self.ctx(**{"design/good.md": (
            "# Good\n\nSummary.\n\n[a](https://x.com) [b](http://x.com) "
            "[c](mailto:x@y.com) [d](tel:+61000) [e](#section)\n")})
        self.assertEqual(lint.check_broken_links(ctx), [])

    def test_link_inside_a_fence_is_ignored(self):
        """BL-03"""
        ctx = self.ctx(**{"design/good.md":
                          "# Good\n\nSummary.\n\n```\n[x](missing-xyz.md)\n```\n"})
        self.assertEqual(lint.check_broken_links(ctx), [])

    def test_broken_link_in_a_loose_surface_is_reported(self):
        """BL-04"""
        f = lint.check_broken_links(self.ctx(
            base=LOOSE, **{"CLAUDE.md": "See [x](missing-loose.md).\n"}))
        self.assertEqual(paths(f, "broken_link"), {"CLAUDE.md"})

    def test_resolving_link_out_of_the_docs_root_is_silent(self):
        """BL-05"""
        ctx = self.ctx(base=LOOSE, **{
            "design/good.md": "# Good\n\nSummary.\n\nSee [r](../README.md).\n"})
        self.assertEqual(lint.check_broken_links(ctx), [])

    def test_line_number_is_the_link_line(self):
        """BL-06"""
        f = lint.check_broken_links(self.ctx(**{
            "design/good.md": "# Good Doc\n\nSummary.\n\nSee [x](missing-xyz.md).\n"}))
        self.assertEqual([x.line for x in f], [5])

    def test_clean(self):
        """BL-07"""
        self.assert_clean()


# --- NI: check_not_indexed ---------------------------------------------------
class CheckNotIndexed(CheckBase):
    CHECK = staticmethod(lint.check_not_indexed)

    def test_unindexed_doc_is_warn(self):
        """NI-01"""
        f = lint.check_not_indexed(self.ctx(**{"design/lonely.md": "# Lonely\n\nS.\n"}))
        self.assertIn("not_indexed", kinds(f, "warn"))
        self.assertEqual(paths(f), {"design/lonely.md"})

    def test_indexed_doc_is_not_reported(self):
        """NI-02"""
        self.assertNotIn("design/good.md", paths(lint.check_not_indexed(self.ctx())))

    def test_index_itself_is_never_reported(self):
        """NI-03"""
        f = lint.check_not_indexed(self.ctx(**{"design/INDEX.md": "# Index\n\nCatalogue.\n"}))
        self.assertEqual(paths(f), {"design/good.md"})

    def test_indexing_is_per_root(self):
        """NI-04"""
        f = lint.check_not_indexed(self.ctx(base=TWO_ROOTS, **{
            "design/INDEX.md": ("# Index\n\nCatalogue.\n\n- [good](good.md)\n"
                                "- [other](../libraries/my-lib/docs/other.md)\n"),
            "libraries/my-lib/docs/INDEX.md": "# Index\n\nLibrary docs.\n"}))
        self.assertEqual(paths(f), {"libraries/my-lib/docs/other.md"})

    def test_index_link_inside_a_fence_does_not_count(self):
        """NI-05"""
        f = lint.check_not_indexed(self.ctx(**{
            "design/INDEX.md": "# Index\n\nCatalogue.\n\n```\n- [good](good.md)\n```\n"}))
        self.assertEqual(paths(f), {"design/good.md"})

    def test_clean(self):
        """NI-06"""
        self.assert_clean()


# --- OR: check_orphaned ------------------------------------------------------
class CheckOrphaned(CheckBase):
    CHECK = staticmethod(lint.check_orphaned)

    def test_doc_with_no_inbound_link_is_warn(self):
        """OR-01"""
        f = lint.check_orphaned(self.ctx(**{"design/lonely.md": "# Lonely\n\nS.\n"}))
        self.assertIn("orphaned", kinds(f, "warn"))
        self.assertEqual(paths(f), {"design/lonely.md"})

    def test_inbound_link_from_index_prevents_it(self):
        """OR-02"""
        self.assertNotIn("design/good.md", paths(lint.check_orphaned(self.ctx())))

    def test_inbound_link_from_another_doc_prevents_it(self):
        """OR-03"""
        f = lint.check_orphaned(self.ctx(**{
            "design/INDEX.md": "# Index\n\nCatalogue.\n\n- [b](b.md)\n",
            "design/b.md": "# B\n\nSummary.\n\n[to good](good.md)\n"}))
        self.assertNotIn("design/good.md", paths(f))

    def test_inbound_link_from_a_loose_surface_prevents_it(self):
        """OR-04"""
        f = lint.check_orphaned(self.ctx(base=LOOSE, **{
            "design/other.md": "# Other\n\nSummary.\n",
            "CLAUDE.md": "See [other](design/other.md).\n"}))
        self.assertNotIn("design/other.md", paths(f))

    def test_index_and_loose_files_are_never_orphaned(self):
        """OR-05"""
        reported = paths(lint.check_orphaned(self.ctx(base=LOOSE)))
        self.assertNotIn("design/INDEX.md", reported)
        self.assertFalse(reported & {"README.md", "CLAUDE.md",
                                     ".claude/memory/some_file.md"})

    def test_clean(self):
        """OR-06"""
        self.assert_clean()


# --- WP: check_was_phrasing --------------------------------------------------
class CheckWasPhrasing(CheckBase):
    CHECK = staticmethod(lint.check_was_phrasing)

    def test_trigger_phrase_is_advisory_with_line_number(self):
        """WP-01"""
        f = lint.check_was_phrasing(self.ctx(**{
            "design/good.md": "# Good Doc\n\nSummary.\n\nThis was formerly the only sauce.\n"}))
        self.assertIn("was_phrasing", kinds(f, "advisory"))
        self.assertEqual([(x.path, x.line) for x in f], [("design/good.md", 5)])
        self.assertIn("formerly", f[0].message)

    def test_matching_is_case_insensitive(self):
        """WP-02"""
        f = lint.check_was_phrasing(self.ctx(**{
            "design/good.md": "# Good Doc\n\nSummary.\n\nFORMERLY the only one.\n"}))
        self.assertIn("was_phrasing", kinds(f))

    def test_phrase_inside_a_fence_is_ignored(self):
        """WP-03"""
        f = lint.check_was_phrasing(self.ctx(**{
            "design/good.md": "# Good Doc\n\nSummary.\n\n```\nformerly the only one\n```\n"}))
        self.assertEqual(f, [])

    def test_matching_is_word_bounded(self):
        """WP-04"""
        self.assertIsNone(lint.WAS_RE.search("a reformerly coined word"))
        self.assertIsNotNone(lint.WAS_RE.search("a formerly coined word"))
        f = lint.check_was_phrasing(self.ctx(**{
            "design/good.md": "# Good Doc\n\nSummary.\n\nA reformerly coined word.\n"}))
        self.assertEqual(f, [])

    def test_every_pattern_is_matched_by_the_regex(self):
        """WP-05"""
        for phrase in lint.WAS_PATTERNS:
            with self.subTest(phrase=phrase):
                self.assertIsNotNone(lint.WAS_RE.search(f"text {phrase} text"))

    def test_phrase_in_a_loose_surface_is_reported(self):
        """WP-06"""
        f = lint.check_was_phrasing(self.ctx(
            base=LOOSE, **{"CLAUDE.md": "This was previously the rule.\n"}))
        self.assertEqual(paths(f, "was_phrasing"), {"CLAUDE.md"})

    def test_clean(self):
        """WP-07"""
        self.assert_clean()


# --- SC: lint() scope and counts ---------------------------------------------
class ScopeTests(TreeBase):
    BASE = SCOPED

    def test_unscoped_reports_every_file(self):
        """SC-01"""
        findings, _, _ = lint.lint(self.tree())
        self.assertEqual(paths(findings, "broken_link"), {"design/a.md", "design/b.md"})

    def test_file_scope_reports_only_that_file(self):
        """SC-02"""
        findings, n_files, n_roots = lint.lint(self.tree(), ["design/a.md"])
        self.assertTrue(findings, "file scope must not silently scan nothing")
        self.assertEqual(paths(findings), {"design/a.md"})
        self.assertEqual((n_files, n_roots), (1, 1))

    def test_scope_keeps_global_context(self):
        """SC-03 — a.md is linked by b.md, so scoping to a.md must not orphan it."""
        findings, _, _ = lint.lint(self.tree(), ["design/a.md"])
        self.assertNotIn("orphaned", kinds(findings))

    def test_directory_scope_reports_every_file_under_it(self):
        """SC-04"""
        findings, _, _ = lint.lint(self.tree(), ["design"])
        self.assertEqual(paths(findings, "broken_link"), {"design/a.md", "design/b.md"})

    def test_trailing_slash_scope_behaves_the_same(self):
        """SC-05"""
        root = self.tree()
        self.assertEqual(paths(lint.lint(root, ["design/"])[0]),
                         paths(lint.lint(root, ["design"])[0]))

    def test_n_roots_counts_only_roots_with_in_scope_files(self):
        """SC-06"""
        root = self.tree(base=TWO_ROOTS)
        self.assertEqual(lint.lint(root)[2], 2)
        self.assertEqual(lint.lint(root, ["design"])[2], 1)

    def test_scope_matching_nothing_is_empty(self):
        """SC-07"""
        self.assertEqual(lint.lint(self.tree(), ["no/such/place"]), ([], 0, 0))

    def test_unscoped_counts_the_whole_corpus(self):
        """SC-08"""
        _, n_files, n_roots = lint.lint(self.tree(base=LOOSE))
        self.assertEqual((n_files, n_roots), (5, 1))


# --- CL: CLI and output ------------------------------------------------------
class Cli(TreeBase):
    def run_cli(self, spec, *argv):
        root = self.tree(base=spec)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = lint.main(["--root", str(root), *argv])
        return code, buf.getvalue()

    def test_clean_corpus_exits_zero(self):
        """CL-01"""
        self.assertEqual(self.run_cli(CLEAN)[0], 0)

    def test_error_exits_one(self):
        """CL-02"""
        spec = {**CLEAN, "design/good.md": "# Good\n\nS.\n\n[x](missing.md)\n"}
        self.assertEqual(self.run_cli(spec)[0], 1)

    def test_warnings_alone_exit_zero(self):
        """CL-03"""
        spec = {**CLEAN, "design/lonely.md": "# Lonely\n\nSummary.\n"}
        code, out = self.run_cli(spec)
        self.assertEqual(code, 0)
        self.assertIn("not_indexed", out)

    def test_advisories_alone_exit_zero(self):
        """CL-04"""
        spec = {**CLEAN,
                "design/good.md": "# Good\n\nS.\n\nIt was formerly the only one.\n"}
        code, out = self.run_cli(spec)
        self.assertEqual(code, 0)
        self.assertIn("was_phrasing", out)

    def test_json_carries_findings_and_counts(self):
        """CL-05"""
        payload = json.loads(self.run_cli(MIXED, "--json")[1])
        summary = payload["summary"]
        self.assertEqual((summary["errors"], summary["warnings"], summary["advisory"]),
                         (1, 2, 1))
        self.assertEqual(len(payload["findings"]), 4)
        self.assertEqual(summary["files_scanned"], 3)
        self.assertEqual(summary["docs_roots"], 1)

    def test_json_orders_by_severity_then_path_and_line(self):
        """CL-06"""
        payload = json.loads(self.run_cli(MIXED, "--json")[1])
        order = [lint.SEV_ORDER[f["severity"]] for f in payload["findings"]]
        self.assertEqual(order, sorted(order))

    def test_render_human_groups_by_severity_and_summarises(self):
        """CL-07"""
        out = self.run_cli(MIXED)[1]
        self.assertIn("ERRORS (1)", out)
        self.assertIn("WARNINGS (2)", out)
        self.assertIn("ADVISORY (1)", out)
        self.assertIn("Scanned 3 files across 1 docs/ root(s)", out)

    def test_root_argument_scans_another_directory(self):
        """CL-08"""
        spec = {**SCOPED}
        out = self.run_cli(spec, "design/a.md")[1]
        self.assertIn("design/a.md", out)
        self.assertNotIn("design/b.md", out)

    def test_strict_is_not_an_option(self):
        """CL-09"""
        root = self.tree(base=CLEAN)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            lint.main(["--root", str(root), "--strict"])
        self.assertEqual(cm.exception.code, 2)


# --- XC: cross-cutting -------------------------------------------------------
class CrossCutting(TreeBase):
    def test_clean_corpus_has_no_findings(self):
        """XC-01"""
        self.assertEqual(lint.lint(self.tree())[0], [])

    def test_inject_then_restore(self):
        """XC-02"""
        root = self.tree()
        good = root / "design/good.md"
        original = good.read_text(encoding="utf-8")

        self.assertEqual(lint.lint(root)[0], [], "clean baseline")
        good.write_text(original + "\nSee [x](does-not-exist.md).\n", encoding="utf-8")
        self.assertIn("broken_link", kinds(lint.lint(root)[0]))
        good.write_text(original, encoding="utf-8")
        self.assertEqual(lint.lint(root)[0], [], "restored to clean")

    def test_every_check_is_named_in_the_plan(self):
        """XC-03"""
        plan = PLAN_PATH.read_text(encoding="utf-8")
        self.assertEqual([c.__name__ for c in lint.CHECKS if c.__name__ not in plan], [])

    def test_every_test_is_named_in_the_plan(self):
        """XC-04 — delegated to the test-plan-linter; uncovered cases are warns."""
        findings = plan_linter.check_test_plan(PLAN_PATH, [HERE], HERE)
        self.assertEqual([f"{f.check}: {f.message}" for f in findings
                          if f.severity == "error"], [])

    def test_finding_paths_are_repo_relative(self):
        """XC-05"""
        root = self.tree(base=MIXED)
        findings, _, _ = lint.lint(root)
        self.assertTrue(findings)
        for f in findings:
            self.assertFalse(Path(f.path).is_absolute())
            self.assertNotIn(str(root), f.path)

    def test_every_severity_is_known(self):
        """XC-06"""
        findings, _, _ = lint.lint(self.tree(base=MIXED))
        self.assertTrue(findings)
        self.assertTrue({f.severity for f in findings} <= set(lint.SEV_ORDER))

    @unittest.skipUnless((LIB_LINTER / "lint_library.py").is_file(),
                         "library-standards-linter is not deployed alongside")
    def test_missing_docs_agrees_with_the_library_linter(self):
        """XC-07 — the two linters must not drift on what a library is, or on how
        bad a missing docs/ is. This is the only cross-skill edge, and it lives in
        a test rather than in either linter."""
        sys.path.insert(0, str(LIB_LINTER))
        import lint_library  # noqa: E402

        root = self.tree(**{
            "libraries/my-lib/pyproject.toml": '[project]\nname = "my-lib"\n',
            "libraries/my-lib/README.md": "# my-lib\n\nA summary.\n"})
        mine = [f for f in lint.lint(root)[0] if f.check == "missing_docs"]
        theirs = [f for f in lint_library.lint(root, ["my-lib"])[0] if f.check == "missing_docs"]
        self.assertTrue(mine, "doc-convention-linter did not report the missing docs/")
        self.assertTrue(theirs, "library-standards-linter did not report the missing docs/")
        self.assertEqual({f.severity for f in mine}, {f.severity for f in theirs})


if __name__ == "__main__":
    unittest.main(verbosity=2)
