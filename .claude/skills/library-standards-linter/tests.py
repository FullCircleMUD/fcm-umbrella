#!/usr/bin/env python3
"""Unit tests for the library-standards-linter. Stdlib only (no pytest) so they
ship and run with the skill anywhere:
    python .claude/skills/library-standards-linter/tests.py

Every case is agreed in test-plan.md first; each test names its case ID in its
docstring, so the coverage trail reads in both directions. Each validator is
exercised in isolation against a synthetic library, plus integration tests over
lint(), the CLI, and the placeholder-satisfies-structure calibration."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_library as lib  # noqa: E402

HERE = Path(__file__).resolve().parent
PLAN_PATH = HERE / "test-plan.md"

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

LIB_TESTS = SPDX + (
    "def test_wc_filters():\n    pass\n\n\n"
    "class WalkTests:\n    def test_wc_empty(self):\n        pass\n")


LOG_SHIM = '''\
"""Logging shim."""


def my_log(message, level="INFO", trace=False):
    try:
        from evennia.utils import logger
    except ImportError:
        return
    logger.log_file(f"[{level}] {message}", filename="my_lib.log")
'''


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
        "libraries/my-lib/src/my_lib/log.py": SPDX + LOG_SHIM,
        "libraries/my-lib/src/my_lib/tests.py": LIB_TESTS,
        "libraries/my-lib/tests/.gitkeep": "",
    }


SRC_FILES = ["libraries/my-lib/src/my_lib/__init__.py",
             "libraries/my-lib/src/my_lib/core.py",
             "libraries/my-lib/src/my_lib/log.py",
             "libraries/my-lib/src/my_lib/tests.py"]


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


def messages(findings):
    return " ".join(f.message for f in findings)


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
        """RF-01"""
        self.assertEqual(lib.check_root_files(self.ctx()), [])

    def test_missing_license_is_error(self):
        """RF-02"""
        f = lib.check_root_files(self.ctx(drop=["libraries/my-lib/LICENSE"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_gitignore_is_warn(self):
        """RF-03"""
        f = lib.check_root_files(self.ctx(drop=["libraries/my-lib/.gitignore"]))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("missing_file", kinds(f, "warn"))

    def test_each_required_file_has_its_documented_severity(self):
        """RF-04"""
        expected = {"pyproject.toml": "error", "README.md": "error", "CLAUDE.md": "error",
                    "LICENSE": "error", ".gitignore": "warn", "runtests.py": "warn"}
        for fn, severity in expected.items():
            with self.subTest(file=fn):
                f = lib.check_root_files(self.ctx(drop=[f"libraries/my-lib/{fn}"]))
                self.assertEqual(len(f), 1)
                self.assertEqual(f[0].severity, severity)
                self.assertIn(fn, f[0].message)


class CheckDocs(ValidatorBase):
    def test_clean(self):
        """DC-01"""
        self.assertEqual(lib.check_docs(self.ctx()), [])

    def test_missing_docs_dir_is_single_error(self):
        """DC-02"""
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/INDEX.md",
                                          "libraries/my-lib/docs/progress.md",
                                          "libraries/my-lib/docs/test-plan.md",
                                          "libraries/my-lib/docs/archive/.gitkeep"]))
        self.assertEqual(len(f), 1)
        self.assertEqual(kinds(f, "error"), {"missing_docs"})

    def test_missing_index_is_error(self):
        """DC-03"""
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/INDEX.md"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_progress_is_warn(self):
        """DC-04"""
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/progress.md"]))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("missing_file", kinds(f, "warn"))

    def test_missing_archive_is_warn(self):
        """DC-05"""
        f = lib.check_docs(self.ctx(drop=["libraries/my-lib/docs/archive/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))

    def test_documentation_structure_md_forbidden(self):
        """DC-06"""
        f = lib.check_docs(self.ctx(**{"libraries/my-lib/docs/documentation-structure.md": "# no\n"}))
        self.assertIn("forbidden_meta_doc", kinds(f, "error"))


class CheckTestPlan(ValidatorBase):
    """The adapter onto the test-plan-linter skill. The plan-vs-suite cases
    themselves live in that skill's own plan and suite."""

    PLAN = "libraries/my-lib/docs/test-plan.md"
    LIB_TESTS = "libraries/my-lib/src/my_lib/tests.py"

    def test_clean(self):
        """TP-01"""
        self.assertEqual(lib.check_test_plan(self.ctx()), [])

    def test_missing_plan_is_warn(self):
        """TP-02 — renamed to the library standard's `missing_file`."""
        f = lib.check_test_plan(self.ctx(drop=[self.PLAN]))
        self.assertIn("missing_file", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())

    def test_plan_findings_are_reported_under_the_library(self):
        """TP-19"""
        plan = TEST_PLAN.replace("`test_wc_filters`", "`test_gone`")
        f = lib.check_test_plan(self.ctx(**{self.PLAN: plan}))
        self.assertIn("test_plan_dangling_ref", kinds(f, "error"))
        for x in f:
            self.assertEqual(x.library, "my-lib")
            self.assertFalse(Path(x.path).is_absolute())

    def test_ghost_test_surfaces_as_an_error(self):
        """TP-20 — the reverse check reaches the library's own test modules."""
        f = lib.check_test_plan(self.ctx(**{
            self.LIB_TESTS: LIB_TESTS + "\n\ndef test_not_in_the_plan():\n    pass\n"}))
        self.assertIn("test_plan_ghost_test", kinds(f, "error"))
        self.assertIn("test_not_in_the_plan", messages(f))


class CheckSrcLayout(ValidatorBase):
    def test_clean(self):
        """SL-01"""
        self.assertEqual(lib.check_src_layout(self.ctx()), [])

    def test_missing_src_is_error(self):
        """SL-02"""
        f = lib.check_src_layout(self.ctx(drop=SRC_FILES))
        self.assertIn("missing_src", kinds(f, "error"))

    def test_no_package_under_src_is_error(self):
        """SL-03"""
        f = lib.check_src_layout(self.ctx(
            drop=SRC_FILES, **{"libraries/my-lib/src/notes.txt": "not a package\n"}))
        self.assertIn("missing_package", kinds(f, "error"))

    def test_missing_version_is_warn(self):
        """SL-04"""
        f = lib.check_src_layout(self.ctx(**{"libraries/my-lib/src/my_lib/__init__.py": SPDX}))
        self.assertIn("missing_version", kinds(f, "warn"))


class CheckNaming(ValidatorBase):
    def test_clean(self):
        """NM-01"""
        self.assertEqual(lib.check_naming(self.ctx()), [])

    def test_mismatch_is_error(self):
        """NM-02"""
        ctx = self.ctx(drop=["libraries/my-lib/src/my_lib/__init__.py",
                             "libraries/my-lib/src/my_lib/core.py"],
                       **{"libraries/my-lib/src/wrong_name/__init__.py": SPDX})
        self.assertIn("naming_mismatch", kinds(lib.check_naming(ctx), "error"))


class CheckSpdx(ValidatorBase):
    def test_clean(self):
        """SP-01"""
        self.assertEqual(lib.check_spdx(self.ctx()), [])

    def test_missing_is_warn(self):
        """SP-02"""
        f = lib.check_spdx(self.ctx(**{"libraries/my-lib/src/my_lib/core.py": "x = 1\n"}))
        self.assertIn("missing_spdx", kinds(f, "warn"))

    def test_migrations_excluded(self):
        """SP-03"""
        f = lib.check_spdx(self.ctx(**{"libraries/my-lib/src/my_lib/migrations/0001.py": "x=1\n"}))
        self.assertEqual(f, [])

    def test_header_below_first_five_lines_is_missing(self):
        """SP-04"""
        buried = '"""doc"""\n' + "\n" * 8 + SPDX + "x = 1\n"
        f = lib.check_spdx(self.ctx(**{"libraries/my-lib/src/my_lib/core.py": buried}))
        self.assertIn("missing_spdx", kinds(f, "warn"))


class CheckTestsDir(ValidatorBase):
    def test_placeholder_passes(self):
        """TD-01"""
        self.assertEqual(lib.check_tests_dir(self.ctx()), [])

    def test_missing_is_warn_not_error(self):
        """TD-02"""
        f = lib.check_tests_dir(self.ctx(drop=["libraries/my-lib/tests/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())


class CheckLogging(ValidatorBase):
    def test_clean(self):
        """LG-01"""
        self.assertEqual(lib.check_logging(self.ctx()), [])

    def test_missing_shim_is_warn_not_error(self):
        """LG-02"""
        f = lib.check_logging(self.ctx(drop=["libraries/my-lib/src/my_lib/log.py"]))
        self.assertIn("missing_log_shim", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())

    def test_shim_not_using_log_file_is_error(self):
        """LG-03"""
        f = lib.check_logging(self.ctx(**{
            "libraries/my-lib/src/my_lib/log.py":
                SPDX + 'import logging\n\n\ndef my_log(m):\n    print("my.log", m)\n'}))
        self.assertIn("log_shim_mechanism", kinds(f, "error"))

    def test_shim_naming_no_log_file_is_warn(self):
        """LG-04"""
        f = lib.check_logging(self.ctx(**{
            "libraries/my-lib/src/my_lib/log.py": SPDX + LOG_SHIM.replace('"my_lib.log"', '""')}))
        self.assertIn("log_shim_filename", kinds(f, "warn"))

    def test_shim_without_importerror_handling_is_warn(self):
        """LG-05"""
        stripped = LOG_SHIM.replace("    except ImportError:\n        return\n", "")
        stripped = stripped.replace("    try:\n", "")
        f = lib.check_logging(self.ctx(**{
            "libraries/my-lib/src/my_lib/log.py": SPDX + stripped}))
        self.assertIn("log_shim_fallback", kinds(f, "warn"))

    def test_stdlib_logging_outside_the_shim_is_warn(self):
        """LG-06"""
        f = lib.check_logging(self.ctx(**{
            "libraries/my-lib/src/my_lib/core.py":
                SPDX + 'import logging\n\nlogger = logging.getLogger("my_lib")\n'}))
        self.assertIn("stdlib_logging", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_the_shim_itself_may_mention_logging(self):
        """LG-07"""
        self.assertNotIn("stdlib_logging", kinds(lib.check_logging(self.ctx())))

    def test_no_package_is_silent(self):
        """LG-08"""
        ctx = self.ctx(drop=SRC_FILES + ["libraries/my-lib/src/my_lib/log.py"])
        self.assertEqual(lib.check_logging(ctx), [])


class CheckMemorySurface(ValidatorBase):
    def test_clean(self):
        """MS-01"""
        self.assertEqual(lib.check_memory_surface(self.ctx()), [])

    def test_forbidden(self):
        """MS-02"""
        f = lib.check_memory_surface(self.ctx(**{"libraries/my-lib/.claude/memory/x.md": "x\n"}))
        self.assertIn("forbidden_memory", kinds(f, "warn"))


class CheckPyproject(ValidatorBase):
    PP = "libraries/my-lib/pyproject.toml"

    def test_clean(self):
        """PP-01"""
        self.assertEqual(lib.check_pyproject(self.ctx()), [])

    def test_wrong_license_is_error(self):
        """PP-02"""
        pp = PYPROJECT.replace('license = {text = "BSD-3-Clause"}', 'license = {text = "MIT"}')
        self.assertIn("license", kinds(lib.check_pyproject(self.ctx(**{self.PP: pp})), "error"))

    def test_name_mismatch_is_error(self):
        """PP-03"""
        pp = PYPROJECT.replace('name = "my-lib"', 'name = "other"')
        self.assertIn("pyproject_name",
                      kinds(lib.check_pyproject(self.ctx(**{self.PP: pp})), "error"))

    def test_unparseable_is_error(self):
        """PP-04"""
        f = lib.check_pyproject(self.ctx(**{self.PP: "not = valid = toml ="}))
        self.assertEqual(kinds(f), {"pyproject_unparseable"})

    def test_absent_pyproject_is_not_reported_here(self):
        """PP-05 — check_root_files owns the absence."""
        self.assertEqual(lib.check_pyproject(self.ctx(drop=[self.PP])), [])

    def test_bare_string_license_accepted(self):
        """PP-06"""
        pp = PYPROJECT.replace('license = {text = "BSD-3-Clause"}', 'license = "BSD-3-Clause"')
        self.assertEqual(lib.check_pyproject(self.ctx(**{self.PP: pp})), [])

    def test_requires_python_missing_or_too_old_is_warn(self):
        """PP-07"""
        old = PYPROJECT.replace('requires-python = ">=3.10"', 'requires-python = ">=3.8"')
        self.assertIn("requires_python",
                      kinds(lib.check_pyproject(self.ctx(**{self.PP: old})), "warn"))
        gone = PYPROJECT.replace('requires-python = ">=3.10"\n', "")
        self.assertIn("requires_python",
                      kinds(lib.check_pyproject(self.ctx(**{self.PP: gone})), "warn"))

    def test_missing_build_system_is_warn(self):
        """PP-08"""
        pp = PYPROJECT.split("[project]", 1)[1]
        self.assertIn("build_system",
                      kinds(lib.check_pyproject(self.ctx(**{self.PP: "[project]" + pp})), "warn"))

    def test_packages_where_must_be_src(self):
        """PP-09"""
        pp = PYPROJECT.replace('where = ["src"]', 'where = ["."]')
        self.assertIn("packages_where",
                      kinds(lib.check_pyproject(self.ctx(**{self.PP: pp})), "warn"))


class Integration(unittest.TestCase):
    def lint(self, spec, scope=("my-lib",)):
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.lint(root, list(scope) if scope else scope)

    def test_compliant_is_clean(self):
        """DS-01"""
        findings, libs = self.lint(compliant())
        self.assertEqual(libs, ["my-lib"])
        self.assertEqual(findings, [])

    def test_discovery_skips_non_library_dirs(self):
        """DS-02"""
        spec = compliant()
        spec["libraries/fixture-repo/data.yaml"] = "x: 1\n"  # no pyproject -> not a library
        _, libs = self.lint(spec, scope=None)
        self.assertEqual(libs, ["my-lib"])

    def test_scope_restricts_to_named_libraries(self):
        """DS-03"""
        spec = compliant()
        spec["libraries/other-lib/pyproject.toml"] = PYPROJECT.replace('"my-lib"', '"other-lib"')
        _, libs = self.lint(spec, scope=None)
        self.assertEqual(libs, ["my-lib", "other-lib"])
        _, libs = self.lint(spec)
        self.assertEqual(libs, ["my-lib"])

    def test_root_without_libraries_dir_is_empty(self):
        """DS-04"""
        findings, libs = self.lint({"README.md": "# not a workspace\n"}, scope=None)
        self.assertEqual((findings, libs), ([], []))


class Cli(unittest.TestCase):
    def run_cli(self, spec, *argv):
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = lib.main(["--root", str(root), "my-lib", *argv])
        return code, buf.getvalue()

    def test_clean_library_exits_zero(self):
        """CL-01"""
        code, out = self.run_cli(compliant())
        self.assertEqual(code, 0)
        self.assertIn("my-lib — OK", out)

    def test_error_exits_one(self):
        """CL-02"""
        spec = compliant()
        spec.pop("libraries/my-lib/LICENSE")
        self.assertEqual(self.run_cli(spec)[0], 1)

    def test_warnings_exit_zero_unless_strict(self):
        """CL-03"""
        spec = compliant()
        spec.pop("libraries/my-lib/.gitignore")
        self.assertEqual(self.run_cli(spec)[0], 0)
        self.assertEqual(self.run_cli(spec, "--strict")[0], 1)

    def test_json_output_carries_findings_and_counts(self):
        """CL-04"""
        spec = compliant()
        spec.pop("libraries/my-lib/LICENSE")
        spec.pop("libraries/my-lib/.gitignore")
        _, out = self.run_cli(spec, "--json")
        payload = json.loads(out)
        summary = payload["summary"]
        self.assertEqual(summary["libraries"], ["my-lib"])
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["warnings"], 1)
        self.assertEqual(len(payload["findings"]), 2)


class CrossCutting(unittest.TestCase):
    """The linter's own coverage trail, checked the way it checks a library's."""

    def plan_names(self):
        rows, _ = lib.plan_linter.scan_test_plan(PLAN_PATH.read_text(encoding="utf-8"))
        return {n for _, cell, _ in rows for n in lib.plan_linter.ref_names(cell)}

    def test_every_check_is_named_in_the_plan(self):
        """XC-01"""
        plan = PLAN_PATH.read_text(encoding="utf-8")
        missing = [c.__name__ for c in lib.CHECKS if c.__name__ not in plan]
        self.assertEqual(missing, [])

    def test_every_test_is_named_in_the_plan(self):
        """XC-02 — the reverse check, applied to this suite."""
        defined = set(lib.plan_linter.scan_test_functions([HERE], HERE))
        self.assertEqual(sorted(defined - self.plan_names()), [])

    def test_finding_paths_are_repo_relative(self):
        """XC-03"""
        spec = compliant()
        spec.pop("libraries/my-lib/LICENSE")
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        findings, _ = lib.lint(root, ["my-lib"])
        self.assertTrue(findings)
        for f in findings:
            self.assertFalse(Path(f.path).is_absolute())
            self.assertNotIn(str(root), f.path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
