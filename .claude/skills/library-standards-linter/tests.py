#!/usr/bin/env python3
"""Unit tests for the library-standards-linter. Stdlib only (no pytest) so they
ship and run with the skill anywhere:
    python .claude/skills/library-standards-linter/tests.py

Each validator is exercised in isolation against a synthetic library, plus
integration tests over lint() and the placeholder-satisfies-structure calibration."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_library as lib  # noqa: E402

SPDX = "# SPDX-License-Identifier: BSD-3-Clause\n"

PYPROJECT = """\
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "my-lib"
version = "0.0.1"
description = "x"
readme = "README.md"
license = {text = "BSD-3-Clause"}
requires-python = ">=3.10"
dependencies = ["evennia"]

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_lib*"]
"""


TEST_PLAN = """# Test plan

| Prefix | Covers |
|---|---|
| `WC` | `walk_contents` |

## WC — `walk_contents`

| ID | Case | Test function |
|---|---|---|
| WC-01 | Filters by predicate | `test_wc_filters` |
| WC-02 | Empty source returns [] | `WalkTests.test_wc_empty` |
"""


def compliant():
    """A fully-compliant synthetic library; tests/ and docs/archive/ via placeholders."""
    return {
        "libraries/my-lib/pyproject.toml": PYPROJECT,
        "libraries/my-lib/README.md": "# my-lib\n\nA summary.\n",
        "libraries/my-lib/CLAUDE.md": "# my-lib\n",
        "libraries/my-lib/LICENSE": "BSD 3-Clause License ...\n",
        "libraries/my-lib/.gitignore": "venv/\n",
        "libraries/my-lib/runtests.py": "# runner\n",
        "libraries/my-lib/docs/INDEX.md": "# Index\n",
        "libraries/my-lib/docs/progress.md": "# Progress\n",
        "libraries/my-lib/docs/test-plan.md": TEST_PLAN,
        "libraries/my-lib/docs/archive/.gitkeep": "",
        "libraries/my-lib/src/my_lib/__init__.py": SPDX + '__version__ = "0.0.1"\n',
        "libraries/my-lib/src/my_lib/core.py": SPDX + "x = 1\n",
        "libraries/my-lib/src/my_lib/tests.py": SPDX + (
            "def test_wc_filters():\n    pass\n\n\n"
            "class WalkTests:\n    def test_wc_empty(self):\n        pass\n"),
        "libraries/my-lib/tests/.gitkeep": "",
    }


def build(spec):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for relpath, content in spec.items():
        f = root / relpath
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    return tmp, root


def kinds(findings, severity=None):
    return {f.check for f in findings if severity is None or f.severity == severity}


class ValidatorBase(unittest.TestCase):
    """Builds a tree (compliant by default, mutated by **changes) and returns a
    LibContext for my-lib, so each validator can be called in isolation."""

    def ctx(self, drop=(), **add):
        spec = compliant()
        for k in drop:
            spec.pop(k, None)
        spec.update(add)
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.LibContext(root / "libraries/my-lib", root)


class CheckRootFiles(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_root_files(self.ctx()), [])

    def test_missing_license_is_error(self):
        f = lib.check_root_files(self.ctx(drop=["libraries/my-lib/LICENSE"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_gitignore_is_warn(self):
        f = lib.check_root_files(self.ctx(drop=["libraries/my-lib/.gitignore"]))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("missing_file", kinds(f, "warn"))


class CheckDocs(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_docs(self.ctx()), [])

    def test_missing_index_is_error(self):
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/INDEX.md"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_archive_is_warn(self):
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/archive/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))

    def test_documentation_structure_md_forbidden(self):
        f = lib.check_docs(self.ctx(**{"libraries/my-lib/docs/documentation-structure.md": "# no\n"}))
        self.assertIn("forbidden_meta_doc", kinds(f, "error"))


class CheckTestPlan(ValidatorBase):
    PLAN = "libraries/my-lib/docs/test-plan.md"

    def test_clean(self):
        self.assertEqual(lib.check_test_plan(self.ctx()), [])

    def test_missing_plan_is_warn(self):
        f = lib.check_test_plan(self.ctx(drop=[self.PLAN]))
        self.assertIn("missing_file", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())

    def test_uncovered_case_is_warn(self):
        plan = TEST_PLAN.replace("`test_wc_filters`", "")
        f = lib.check_test_plan(self.ctx(**{self.PLAN: plan}))
        self.assertIn("test_plan_uncovered", kinds(f, "warn"))
        self.assertIn("WC-01", f[0].message)

    def test_dangling_reference_is_error(self):
        plan = TEST_PLAN.replace("`test_wc_filters`", "`test_gone`")
        f = lib.check_test_plan(self.ctx(**{self.PLAN: plan}))
        self.assertIn("test_plan_dangling_ref", kinds(f, "error"))
        self.assertIn("test_gone", f[0].message)

    def test_no_test_function_column_is_warn(self):
        plan = TEST_PLAN.replace("| ID | Case | Test function |", "| ID | Case | Notes |")
        f = lib.check_test_plan(self.ctx(**{self.PLAN: plan}))
        self.assertIn("test_plan_no_column", kinds(f, "warn"))

    def test_non_case_tables_are_ignored(self):
        """The prefix-legend table has no Test function column and no case IDs."""
        rows, saw = lib.scan_test_plan(TEST_PLAN)
        self.assertEqual([r[0] for r in rows], ["WC-01", "WC-02"])
        self.assertTrue(saw)

    def test_qualified_reference_resolves_to_last_segment(self):
        self.assertEqual(lib._ref_names("`WalkTests.test_wc_empty`"), ["test_wc_empty"])

    def test_several_references_in_one_cell(self):
        self.assertEqual(lib._ref_names("`test_a`, `test_b`"), ["test_a", "test_b"])


class CheckSrcLayout(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_src_layout(self.ctx()), [])

    def test_missing_version_is_warn(self):
        f = lib.check_src_layout(self.ctx(**{"libraries/my-lib/src/my_lib/__init__.py": SPDX}))
        self.assertIn("missing_version", kinds(f, "warn"))


class CheckNaming(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_naming(self.ctx()), [])

    def test_mismatch_is_error(self):
        ctx = self.ctx(drop=["libraries/my-lib/src/my_lib/__init__.py",
                             "libraries/my-lib/src/my_lib/core.py"],
                       **{"libraries/my-lib/src/wrong_name/__init__.py": SPDX})
        self.assertIn("naming_mismatch", kinds(lib.check_naming(ctx), "error"))


class CheckSpdx(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_spdx(self.ctx()), [])

    def test_missing_is_warn(self):
        f = lib.check_spdx(self.ctx(**{"libraries/my-lib/src/my_lib/core.py": "x = 1\n"}))
        self.assertIn("missing_spdx", kinds(f, "warn"))

    def test_migrations_excluded(self):
        f = lib.check_spdx(self.ctx(**{"libraries/my-lib/src/my_lib/migrations/0001.py": "x=1\n"}))
        self.assertEqual(f, [])


class CheckTestsDir(ValidatorBase):
    def test_placeholder_passes(self):
        self.assertEqual(lib.check_tests_dir(self.ctx()), [])

    def test_missing_is_warn_not_error(self):
        f = lib.check_tests_dir(self.ctx(drop=["libraries/my-lib/tests/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())


class CheckMemorySurface(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_memory_surface(self.ctx()), [])

    def test_forbidden(self):
        f = lib.check_memory_surface(self.ctx(**{"libraries/my-lib/.claude/memory/x.md": "x\n"}))
        self.assertIn("forbidden_memory", kinds(f, "warn"))


class CheckPyproject(ValidatorBase):
    def test_clean(self):
        self.assertEqual(lib.check_pyproject(self.ctx()), [])

    def test_wrong_license_is_error(self):
        pp = PYPROJECT.replace('license = {text = "BSD-3-Clause"}', 'license = {text = "MIT"}')
        self.assertIn("license", kinds(lib.check_pyproject(
            self.ctx(**{"libraries/my-lib/pyproject.toml": pp})), "error"))

    def test_name_mismatch_is_error(self):
        pp = PYPROJECT.replace('name = "my-lib"', 'name = "other"')
        self.assertIn("pyproject_name", kinds(lib.check_pyproject(
            self.ctx(**{"libraries/my-lib/pyproject.toml": pp})), "error"))

    def test_unparseable_is_error(self):
        self.assertIn("pyproject_unparseable", kinds(lib.check_pyproject(
            self.ctx(**{"libraries/my-lib/pyproject.toml": "not = valid = toml ="})), "error"))


class Integration(unittest.TestCase):
    def lint(self, spec):
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.lint(root, ["my-lib"])

    def test_compliant_is_clean(self):
        findings, libs = self.lint(compliant())
        self.assertEqual(libs, ["my-lib"])
        self.assertEqual(findings, [])

    def test_discovery_skips_non_library_dirs(self):
        spec = compliant()
        spec["libraries/fixture-repo/data.yaml"] = "x: 1\n"  # no pyproject -> not a library
        _, root = build(spec)
        self.addCleanup(lambda: None)
        _, libs = lib.lint(root, None)
        self.assertEqual(libs, ["my-lib"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
