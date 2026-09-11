#!/usr/bin/env python3
"""Unit tests for the library-standards-linter. Stdlib only (no pytest) so they
ship and run with the skill anywhere:
    python .claude/skills/library-standards-linter/tests.py

Every case is agreed in test-plan.md first; each test names its case ID in its
docstring, so the coverage trail reads in both directions. Each validator is
exercised in isolation against a synthetic library, plus integration tests over
lint(), the CLI, and the placeholder-satisfies-structure calibration."""
import ast
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
name = "evennia-lib"
version = "0.0.1"
description = "x"
readme = "README.md"
license = {text = "BSD-3-Clause"}
requires-python = ">=3.10"
dependencies = ["evennia", "evennia-logging-extension"]

[tool.setuptools.packages.find]
where = ["src"]
include = ["evennia_lib*"]
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


#: The pre-extension shim, kept so `LG-16` can assert what an un-migrated
#: library reports. Not a shape any library should still carry.
OLD_LOG_SHIM = '''\
"""Logging shim."""
import traceback

_LOG_FILENAME = "evennia_lib.log"
_VALID_LEVELS = ("INFO", "WARN", "ERROR")


def lib_log(message, level="INFO", trace=False):
    try:
        from evennia.utils import logger
    except ImportError:
        return
    if level not in _VALID_LEVELS:
        level = "INFO"
    logger.log_file(f"[{level}] {message}", filename=_LOG_FILENAME)
'''

LOG_SHIM = '''\
"""Logging shim."""

from evennia_logging_extension import make_logger

lib_log = make_logger("evennia_lib.log")
'''


CLAUDE_SECTIONS = ["What this project is", "Project status", "Where to read first",
                   "Load-bearing architectural principles", "Out of scope",
                   "Working conventions", "Documentation discipline (load-bearing)",
                   "Repository layout", "Tools and environment"]

CLAUDE_PRINCIPLES = (
    "1. **The library does not own game concepts.**\n"
    "2. **No FCM-specific assumptions.**\n"
    "3. **Test-first** — a case lands in `docs/test-plan.md`, then the test, then the code.\n")


def claude_md(sections=None, principles=CLAUDE_PRINCIPLES):
    """A CLAUDE.md with the nine standard sections; principles under section 4."""
    out = ["# evennia-lib\n"]
    for s in (CLAUDE_SECTIONS if sections is None else sections):
        out.append(f"## {s}\n")
        out.append(principles if s.startswith("Load-bearing")
                   else "1. `docs/test-plan.md`\n" if s.startswith("Where to read first")
                   else "Prose.\n")
    return "\n".join(out)


def compliant():
    """A fully-compliant synthetic library; tests/ and docs/archive/ via placeholders."""
    return {
        "libraries/evennia-lib/pyproject.toml": PYPROJECT,
        "libraries/evennia-lib/README.md": "# evennia-lib\n\nA summary.\n",
        "libraries/evennia-lib/CLAUDE.md": claude_md(),
        "libraries/evennia-lib/LICENSE": "BSD 3-Clause License ...\n",
        "libraries/evennia-lib/.gitignore": "venv/\n",
        "libraries/evennia-lib/runtests.py": "# runner\n",
        "libraries/evennia-lib/docs/INDEX.md": "# Index\n",
        "libraries/evennia-lib/docs/installing.md": INSTALLING,
        "libraries/evennia-lib/docs/interoperability.md":
            "# Interoperability\n\nSummary.\n\n## evennia-lib\n\nThis library.\n",
        "libraries/evennia-lib/docs/progress.md": "# Progress\n",
        "libraries/evennia-lib/docs/test-plan.md": TEST_PLAN,
        "libraries/evennia-lib/docs/archive/.gitkeep": "",
        "libraries/evennia-lib/src/evennia_lib/__init__.py": SPDX + '__version__ = "0.0.1"\n',
        "libraries/evennia-lib/src/evennia_lib/core.py":
            SPDX + "from .log import lib_log\n\n\ndef run():\n    lib_log('x')\n",
        "libraries/evennia-lib/src/evennia_lib/log.py": SPDX + LOG_SHIM,
        "libraries/evennia-lib/src/evennia_lib/tests.py": LIB_TESTS,
        "libraries/evennia-lib/tests/.gitkeep": "",
    }


SRC_FILES = ["libraries/evennia-lib/src/evennia_lib/__init__.py",
             "libraries/evennia-lib/src/evennia_lib/core.py",
             "libraries/evennia-lib/src/evennia_lib/log.py",
             "libraries/evennia-lib/src/evennia_lib/tests.py"]


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
    LibContext for evennia-lib, so each validator can be called in isolation."""

    def ctx(self, drop=(), **add):
        spec = compliant()
        for k in drop:
            spec.pop(k, None)
        spec.update(add)
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.LibContext(root / "libraries/evennia-lib", root)


class CheckRootFiles(ValidatorBase):
    def test_clean(self):
        """RF-01"""
        self.assertEqual(lib.check_root_files(self.ctx()), [])

    def test_missing_license_is_error(self):
        """RF-02"""
        f = lib.check_root_files(self.ctx(drop=["libraries/evennia-lib/LICENSE"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_gitignore_is_warn(self):
        """RF-03"""
        f = lib.check_root_files(self.ctx(drop=["libraries/evennia-lib/.gitignore"]))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("missing_file", kinds(f, "warn"))

    def test_each_required_file_has_its_documented_severity(self):
        """RF-04"""
        expected = {"pyproject.toml": "error", "README.md": "error", "CLAUDE.md": "error",
                    "LICENSE": "error", ".gitignore": "warn", "runtests.py": "warn"}
        for fn, severity in expected.items():
            with self.subTest(file=fn):
                f = lib.check_root_files(self.ctx(drop=[f"libraries/evennia-lib/{fn}"]))
                self.assertEqual(len(f), 1)
                self.assertEqual(f[0].severity, severity)
                self.assertIn(fn, f[0].message)

    def test_legacy_build_file_is_error(self):
        """RF-05"""
        for fn in ("setup.py", "setup.cfg", "requirements.txt"):
            with self.subTest(file=fn):
                f = lib.check_root_files(self.ctx(**{f"libraries/evennia-lib/{fn}": "x\n"}))
                self.assertIn("legacy_build_file", kinds(f, "error"))

    def test_venv_not_ignored_is_warn(self):
        """RF-06"""
        f = lib.check_root_files(self.ctx(**{"libraries/evennia-lib/.gitignore": "*.pyc\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("venv_not_ignored", kinds(f, "warn"))


_LOG_PATH = "libraries/evennia-lib/src/evennia_lib/log.py"


class CheckConstants(ValidatorBase):
    def test_clean(self):
        """CN-01"""
        self.assertEqual(lib.check_constants(self.ctx()), [])

    def test_constant_outside_config_is_warn(self):
        """CN-02"""
        f = lib.check_constants(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/core.py": SPDX + 'ARCHIVE_ALIAS = "archive"\n'}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("constant_outside_config", kinds(f, "warn"))
        self.assertIn("ARCHIVE_ALIAS", messages(f))
        self.assertIn("core.py", messages(f))

    def test_constants_in_config_are_clean(self):
        """CN-03"""
        f = lib.check_constants(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/config.py": SPDX + 'ARCHIVE_ALIAS = "archive"\n'}))
        self.assertEqual(f, [])

    def test_constants_in_tests_are_ignored(self):
        """CN-06"""
        f = lib.check_constants(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py": LIB_TESTS + 'FIXTURE_KEY = "x"\n'}))
        self.assertEqual(f, [])

    def test_constants_in_migrations_are_ignored(self):
        """CN-07"""
        f = lib.check_constants(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/migrations/__init__.py": "",
            "libraries/evennia-lib/src/evennia_lib/migrations/0001_initial.py":
                'DEPENDENCIES = ["evennia"]\n'}))
        self.assertEqual(f, [])

    def test_a_constant_in_the_shim_is_a_warn(self):
        """CN-10"""
        # The exemption is gone. This is what fails if anyone re-adds it.
        f = lib.check_constants(self.ctx(**{
            _LOG_PATH: SPDX + LOG_SHIM + '_LOG_FILENAME = "evennia_lib.log"\n'}))
        self.assertIn("constant_outside_config", kinds(f, "warn"))
        self.assertIn("_LOG_FILENAME", messages(f))

    def test_the_spec_binding_in_db_spec_is_exempt(self):
        """CN-11 — SPEC in db_spec.py is the cascade's discovery contract."""
        f = lib.check_constants(self.ctx(**{_SPEC_PATH: DB_SPEC}))
        self.assertEqual(f, [])

    def test_any_other_constant_in_db_spec_is_a_warn(self):
        """CN-12 — the exemption is the one name, not the file."""
        f = lib.check_constants(self.ctx(**{
            _SPEC_PATH: DB_SPEC + "DEFAULT_TIMEOUT = 5\n"}))
        self.assertIn("constant_outside_config", kinds(f, "warn"))
        self.assertIn("DEFAULT_TIMEOUT", messages(f))
        self.assertNotIn(":SPEC", messages(f))

    def test_lowercase_assignment_is_not_a_constant(self):
        """CN-09"""
        f = lib.check_constants(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/core.py": SPDX + 'alias = "archive"\nMixedCase = 1\n'}))
        self.assertEqual(f, [])


_CLAUDE_PATH = "libraries/evennia-lib/CLAUDE.md"
_INTEROP_PATH = "libraries/evennia-lib/docs/interoperability.md"
_INSTALLING_PATH = "libraries/evennia-lib/docs/installing.md"

INSTALLING = """# Installing

## 1. Install the package

## 2. Add the app

## 3. Declare the settings

### Required settings

| Setting | Does | Without it |

### Optional settings

| Setting | Default | Why |

## What is not checked for you

INSTALLED_APPS — leave the library out and ready() never runs.
"""


class CheckInstalling(ValidatorBase):
    def doc(self, text):
        return lib.check_installing(self.ctx(**{_INSTALLING_PATH: text}))

    def test_clean(self):
        """IN-01"""
        self.assertEqual(self.doc(INSTALLING), [])

    def test_too_few_numbered_steps_is_warn(self):
        """IN-02"""
        f = self.doc(INSTALLING.replace("## 2. Add the app", "## Add the app")
                               .replace("## 3. Declare the settings", "## Declare the settings"))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("installing_no_steps", kinds(f, "warn"))

    def test_no_required_settings_is_warn(self):
        """IN-03"""
        f = self.doc(INSTALLING.replace("### Required settings", "### Some settings"))
        self.assertIn("installing_no_required_settings", kinds(f, "warn"))

    def test_no_optional_settings_is_warn(self):
        """IN-04"""
        f = self.doc(INSTALLING.replace("### Optional settings", "### Other settings"))
        self.assertIn("installing_no_optional_settings", kinds(f, "warn"))

    def test_no_unchecked_section_is_warn(self):
        """IN-05"""
        f = self.doc(INSTALLING.replace("## What is not checked for you", "## Notes"))
        self.assertIn("installing_no_unchecked_section", kinds(f, "warn"))

    def test_stating_no_settings_satisfies_both(self):
        """IN-06"""
        f = self.doc(INSTALLING.replace("### Required settings", "### Settings")
                               .replace("### Optional settings", "")
                     + "\nThis library reads no settings.\n")
        self.assertNotIn("installing_no_required_settings", kinds(f))
        self.assertNotIn("installing_no_optional_settings", kinds(f))

    def test_missing_doc_is_silent(self):
        """IN-07"""
        self.assertEqual(lib.check_installing(self.ctx(drop=[_INSTALLING_PATH])), [])


def interop(entries):
    """An interoperability.md from `[(heading, body), …]`, in the order given."""
    return "# Interoperability\n\nPreamble.\n\n" + "\n".join(
        f"## {h}\n\n{b}\n" for h, b in entries)


class CheckInteroperability(ValidatorBase):
    def sibling_ctx(self, doc, siblings=("zz-other",)):
        """evennia-lib plus sibling library directories, so the corpus has more than one."""
        spec = compliant()
        spec[_INTEROP_PATH] = doc
        for s in siblings:
            spec[f"libraries/{s}/pyproject.toml"] = PYPROJECT.replace(
                'name = "evennia-lib"', f'name = "{s}"')
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.LibContext(root / "libraries/evennia-lib", root)

    def test_clean(self):
        """IO-01"""
        doc = interop([("evennia-lib", "This library."),
                       ("zz-other", "**No coupling.** Neither imports the other.")])
        self.assertEqual(lib.check_interoperability(self.sibling_ctx(doc)), [])

    def test_missing_sibling_is_warn(self):
        """IO-02"""
        doc = interop([("evennia-lib", "This library.")])
        f = lib.check_interoperability(self.sibling_ctx(doc))
        self.assertIn("interop_missing_sibling", kinds(f, "warn"))
        self.assertIn("zz-other", messages(f))

    def test_own_section_is_required(self):
        """IO-03"""
        doc = interop([("zz-other", "**No coupling.** Neither imports the other.")])
        f = lib.check_interoperability(self.sibling_ctx(doc))
        self.assertIn("interop_missing_sibling", kinds(f, "warn"))
        self.assertIn("evennia-lib", messages(f))

    def test_out_of_order_is_warn(self):
        """IO-04"""
        doc = interop([("zz-other", "**No coupling.** Neither imports the other."),
                       ("evennia-lib", "This library.")])
        f = lib.check_interoperability(self.sibling_ctx(doc))
        self.assertIn("interop_order", kinds(f, "warn"))

    def test_section_without_a_relationship_is_warn(self):
        """IO-05"""
        doc = interop([("evennia-lib", "This library."), ("zz-other", "")])
        f = lib.check_interoperability(self.sibling_ctx(doc))
        self.assertIn("interop_no_relationship", kinds(f, "warn"))
        self.assertIn("zz-other", messages(f))

    def test_own_section_needs_no_relationship(self):
        """IO-06"""
        doc = interop([("evennia-lib", "This library."),
                       ("zz-other", "**Hard dependency.** Imported unconditionally.")])
        f = lib.check_interoperability(self.sibling_ctx(doc))
        self.assertNotIn("interop_no_relationship", kinds(f))

    def test_non_library_headings_are_ignored(self):
        """IO-07"""
        doc = interop([("evennia-lib", "This library."),
                       ("zz-other", "**No coupling.** Neither imports the other."),
                       ("A note on threading", "Prose with no relationship in it.")])
        self.assertEqual(lib.check_interoperability(self.sibling_ctx(doc)), [])

    def test_missing_doc_is_silent(self):
        """IO-08"""
        ctx = self.ctx(drop=[_INTEROP_PATH])
        self.assertEqual(lib.check_interoperability(ctx), [])


class CheckClaudeMd(ValidatorBase):
    def fcm_ctx(self, **add):
        """The same tree under an `fcm-` name, so family-specific rules apply."""
        spec = compliant()
        spec = {k.replace("libraries/evennia-lib/", "libraries/fcm-lib/"): v
                for k, v in spec.items()}
        spec["libraries/fcm-lib/pyproject.toml"] = PYPROJECT.replace(
            'name = "evennia-lib"', 'name = "fcm-lib"')
        spec.update({k.replace("libraries/evennia-lib/", "libraries/fcm-lib/"): v
                     for k, v in add.items()})
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.LibContext(root / "libraries/fcm-lib", root)

    def test_clean(self):
        """CM-01"""
        self.assertEqual(lib.check_claude_md(self.ctx()), [])

    def test_missing_section_is_error(self):
        """CM-02"""
        short = [s for s in CLAUDE_SECTIONS if s != "Out of scope"]
        f = lib.check_claude_md(self.ctx(**{_CLAUDE_PATH: claude_md(short)}))
        self.assertIn("claude_md_section", kinds(f, "error"))
        self.assertIn("Out of scope", messages(f))

    def test_sections_out_of_order_is_error(self):
        """CM-03"""
        swapped = list(CLAUDE_SECTIONS)
        swapped[1], swapped[4] = swapped[4], swapped[1]
        f = lib.check_claude_md(self.ctx(**{_CLAUDE_PATH: claude_md(swapped)}))
        self.assertIn("claude_md_order", kinds(f, "error"))

    def test_extra_sections_are_fine(self):
        """CM-04"""
        padded = list(CLAUDE_SECTIONS)
        padded.insert(3, "The starting point")
        padded.append("Sibling libraries to reference")
        self.assertEqual(lib.check_claude_md(self.ctx(**{_CLAUDE_PATH: claude_md(padded)})), [])

    def test_missing_principle_is_warn(self):
        """CM-05"""
        f = lib.check_claude_md(self.ctx(**{
            _CLAUDE_PATH: claude_md(principles="1. **No FCM-specific assumptions.**\n")}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("claude_md_principle", kinds(f, "warn"))
        self.assertIn("game concepts", messages(f))

    def test_fcm_library_needs_neither_scope_principle(self):
        """CM-06"""
        f = lib.check_claude_md(self.fcm_ctx(**{
            _CLAUDE_PATH: claude_md(principles="1. **Test-first** — `docs/test-plan.md` first.\n")}))
        self.assertEqual(f, [])

    def test_fcm_library_still_needs_test_first(self):
        """CM-07"""
        f = lib.check_claude_md(self.fcm_ctx(**{
            _CLAUDE_PATH: claude_md(principles="1. **FCM concepts belong here.**\n")}))
        self.assertIn("claude_md_principle", kinds(f, "warn"))
        self.assertIn("Test-first", messages(f))

    def test_reading_order_without_test_plan_is_warn(self):
        """CM-09"""
        f = lib.check_claude_md(self.ctx(**{_CLAUDE_PATH: claude_md().replace("1. `docs/test-plan.md`", "1. README.md")}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("claude_md_reading_order", kinds(f, "warn"))

    def test_no_claude_md_is_silent(self):
        """CM-08"""
        self.assertEqual(lib.check_claude_md(self.ctx(drop=[_CLAUDE_PATH])), [])


_CORE_PATH = "libraries/evennia-lib/src/evennia_lib/core.py"
_CONFIG_PATH = "libraries/evennia-lib/src/evennia_lib/config.py"

ACCESSOR = SPDX + '''
def get_tick_seconds():
    from django.conf import settings

    return getattr(settings, "LIB_TICK_SECONDS", 60)
'''


class CheckSettingsAccess(ValidatorBase):
    def test_clean(self):
        """SA-01"""
        self.assertEqual(lib.check_settings_access(self.ctx()), [])

    def test_direct_read_outside_config_is_warn(self):
        """SA-02"""
        f = lib.check_settings_access(self.ctx(**{
            _CORE_PATH: SPDX + "def f():\n    return settings.LIB_TICK_SECONDS\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("settings_read_outside_config", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_getattr_read_outside_config_is_warn(self):
        """SA-03"""
        f = lib.check_settings_access(self.ctx(**{
            _CORE_PATH: SPDX + 'def f():\n    return getattr(settings, "LIB_X", 1)\n'}))
        self.assertIn("settings_read_outside_config", kinds(f, "warn"))

    def test_reads_inside_config_are_clean(self):
        """SA-04"""
        self.assertEqual(lib.check_settings_access(self.ctx(**{_CONFIG_PATH: ACCESSOR})), [])

    def test_module_scope_read_in_config_is_warn(self):
        """SA-05"""
        f = lib.check_settings_access(self.ctx(**{
            _CONFIG_PATH: SPDX + "TICK = settings.LIB_TICK_SECONDS\n"}))
        self.assertIn("settings_read_at_module_scope", kinds(f, "warn"))

    def test_module_scope_import_is_warn(self):
        """SA-06"""
        f = lib.check_settings_access(self.ctx(**{
            _CONFIG_PATH: SPDX + "from django.conf import settings\n\n\ndef get_x():\n"
                                 '    return getattr(settings, "LIB_X", 1)\n'}))
        self.assertIn("settings_import_at_module_scope", kinds(f, "warn"))

    def test_import_inside_a_function_is_clean(self):
        """SA-07"""
        f = lib.check_settings_access(self.ctx(**{_CONFIG_PATH: ACCESSOR}))
        self.assertNotIn("settings_import_at_module_scope", kinds(f))

    def test_tests_module_is_exempt(self):
        """SA-08"""
        f = lib.check_settings_access(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "from django.conf import settings\n\nX = settings.ANYTHING\n"}))
        self.assertEqual(f, [])

    def test_no_package_is_silent(self):
        """SA-09"""
        self.assertEqual(lib.check_settings_access(self.ctx(drop=SRC_FILES)), [])


_APPS_PATH = "libraries/evennia-lib/src/evennia_lib/apps.py"

VALIDATOR = SPDX + "\n\ndef check_settings():\n    pass\n"
APPS = SPDX + '''
from django.apps import AppConfig


class LibConfig(AppConfig):
    name = "evennia_lib"

    def ready(self):
        from .config import check_settings

        check_settings()
'''


class CheckBootValidation(ValidatorBase):
    def test_clean(self):
        """BV-01"""
        f = lib.check_boot_validation(self.ctx(**{
            _CONFIG_PATH: VALIDATOR, _APPS_PATH: APPS}))
        self.assertEqual(f, [])

    def test_uncalled_validator_is_error(self):
        """BV-02"""
        f = lib.check_boot_validation(self.ctx(**{
            _CONFIG_PATH: VALIDATOR,
            _APPS_PATH: APPS.replace("        check_settings()\n", "        pass\n")}))
        self.assertIn("settings_validator_uncalled", kinds(f, "error"))

    def test_no_validator_is_silent(self):
        """BV-03"""
        self.assertEqual(lib.check_boot_validation(self.ctx(**{_APPS_PATH: APPS})), [])

    def test_validator_outside_config_is_error(self):
        """BV-04"""
        f = lib.check_boot_validation(self.ctx(**{
            _CORE_PATH: VALIDATOR, _APPS_PATH: APPS}))
        self.assertIn("settings_validator_outside_config", kinds(f, "error"))

    def test_nonstandard_validator_name_is_warn(self):
        """BV-05"""
        f = lib.check_boot_validation(self.ctx(**{
            _CONFIG_PATH: VALIDATOR.replace("check_settings", "validate_settings"),
            _APPS_PATH: APPS.replace("check_settings", "validate_settings")}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("settings_validator_name", kinds(f, "warn"))

    def test_call_outside_ready_does_not_count(self):
        """BV-06"""
        f = lib.check_boot_validation(self.ctx(**{
            _CONFIG_PATH: VALIDATOR,
            _APPS_PATH: SPDX + "from .config import check_settings\n\ncheck_settings()\n"}))
        self.assertIn("settings_validator_uncalled", kinds(f, "error"))

    def test_no_package_is_silent(self):
        """BV-07"""
        self.assertEqual(lib.check_boot_validation(self.ctx(drop=SRC_FILES)), [])


class CheckEvenniaImports(ValidatorBase):
    def test_clean(self):
        """EI-01"""
        self.assertEqual(lib.check_evennia_imports(self.ctx()), [])

    def test_commented_import_is_clean(self):
        """EI-02"""
        f = lib.check_evennia_imports(self.ctx(**{
            _CORE_PATH: SPDX + "# Rows carry attributes through Evennia's own m2m tables.\n"
                               "from evennia.typeclasses.models import Attribute\n"}))
        self.assertEqual(f, [])

    def test_uncommented_import_is_warn(self):
        """EI-03"""
        f = lib.check_evennia_imports(self.ctx(**{
            _CORE_PATH: SPDX + "from evennia.typeclasses.models import Attribute\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("evennia_import_unexplained", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_plain_import_counts(self):
        """EI-04"""
        f = lib.check_evennia_imports(self.ctx(**{_CORE_PATH: SPDX + "import evennia\n"}))
        self.assertIn("evennia_import_unexplained", kinds(f, "warn"))

    def test_tests_module_is_exempt(self):
        """EI-05"""
        f = lib.check_evennia_imports(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py": LIB_TESTS + "import evennia\n"}))
        self.assertEqual(f, [])

    def test_an_import_in_the_shim_is_not_exempt(self):
        """EI-07"""
        # log.py imports evennia-logging-extension, which holds the Evennia
        # coupling. An Evennia import here is an exception like any other.
        f = lib.check_evennia_imports(self.ctx(**{
            _LOG_PATH: SPDX + "from evennia.utils import logger\n" + LOG_SHIM}))
        self.assertIn("evennia_import_unexplained", kinds(f, "warn"))
        self.assertIn("log.py", messages(f))

    def test_no_package_is_silent(self):
        """EI-06"""
        self.assertEqual(lib.check_evennia_imports(self.ctx(drop=SRC_FILES)), [])


class CheckObjectState(ValidatorBase):
    def test_clean(self):
        """OS-01"""
        self.assertEqual(lib.check_object_state(self.ctx()), [])

    def test_db_write_is_warn(self):
        """OS-02"""
        f = lib.check_object_state(self.ctx(**{
            _CORE_PATH: SPDX + "def f(obj):\n    obj.db.weight = 5\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("db_attribute_write", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_db_read_is_not_a_finding(self):
        """OS-03"""
        f = lib.check_object_state(self.ctx(**{
            _CORE_PATH: SPDX + "def f(obj):\n    return obj.db.weight\n"}))
        self.assertEqual(f, [])

    def test_tests_module_is_exempt(self):
        """OS-04"""
        f = lib.check_object_state(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "def f(obj):\n    obj.db.weight = 5\n"}))
        self.assertEqual(f, [])


class CheckBootSideEffects(ValidatorBase):
    def test_clean(self):
        """BS-01"""
        self.assertEqual(lib.check_boot_side_effects(self.ctx()), [])

    def test_makedirs_is_warn(self):
        """BS-02"""
        f = lib.check_boot_side_effects(self.ctx(**{
            _CORE_PATH: SPDX + "import os\n\n\ndef f(p):\n    os.makedirs(p)\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("creates_directories", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_path_mkdir_is_warn(self):
        """BS-03"""
        f = lib.check_boot_side_effects(self.ctx(**{
            _CORE_PATH: SPDX + "def f(p):\n    p.mkdir(parents=True)\n"}))
        self.assertIn("creates_directories", kinds(f, "warn"))

    def test_tests_module_is_exempt(self):
        """BS-04"""
        f = lib.check_boot_side_effects(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "import os\n\nos.makedirs('/tmp/x')\n"}))
        self.assertEqual(f, [])


_MODELS_PATH = "libraries/evennia-lib/src/evennia_lib/models.py"
_ROUTER_PATH = "libraries/evennia-lib/src/evennia_lib/db_router.py"
_TARGETING_PATH = "libraries/evennia-lib/src/evennia_lib/targeting.py"
_CONTRIB = "libraries/evennia-lib/src/evennia_lib/contrib"

_SPEC_PATH = "libraries/evennia-lib/src/evennia_lib/db_spec.py"

DB_SPEC = SPDX + (
    "from evennia_database_cascade import AliasSpec\n\n"
    'SPEC = AliasSpec(app_label="evennia_lib", alias="evennia_lib")\n')

PYPROJECT_CASCADE = PYPROJECT.replace(
    '"evennia-logging-extension"',
    '"evennia-logging-extension", "evennia-database-cascade"')

#: The cascade's own consumer shape — must never read as hand-written DATABASES doc.
INSTALLING_CASCADE = INSTALLING + """
```python
DATABASES, DATABASE_ROUTERS = configure(
    DATABASES, INSTALLED_APPS, GAME_DIR, os.environ
)
```
"""


class CheckDatabase(ValidatorBase):
    def test_no_models_is_silent(self):
        """DB-01"""
        self.assertEqual(lib.check_database(self.ctx()), [])

    def test_models_without_spec_is_warn(self):
        """DB-08"""
        f = lib.check_database(self.ctx(**{_MODELS_PATH: SPDX + "x = 1\n"}))
        self.assertIn("models_without_spec", kinds(f, "warn"))
        f = lib.check_database(self.ctx(**{
            _MODELS_PATH: SPDX + "x = 1\n", _SPEC_PATH: DB_SPEC,
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE}))
        self.assertNotIn("models_without_spec", kinds(f))

    def test_hand_rolled_router_is_error(self):
        """DB-09"""
        f = lib.check_database(self.ctx(**{_ROUTER_PATH: SPDX + "class R:\n    pass\n"}))
        self.assertIn("hand_rolled_router", kinds(f, "error"))
        # a router-shaped class in any other module reports the same
        f = lib.check_database(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/routing.py":
                SPDX + "class R:\n    def db_for_read(self, model, **hints):\n"
                       "        return None\n"}))
        self.assertIn("hand_rolled_router", kinds(f, "error"))
        # tests.py is exempt, as everywhere
        f = lib.check_database(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "\n\nclass FakeRouter:\n"
                            "    def db_for_read(self, model, **hints):\n"
                            "        return None\n"}))
        self.assertNotIn("hand_rolled_router", kinds(f))

    def test_hand_rolled_resolution_is_error(self):
        """DB-10"""
        f = lib.check_database(self.ctx(**{
            _CONFIG_PATH: SPDX + "import dj_database_url\n"}))
        self.assertIn("hand_rolled_resolution", kinds(f, "error"))
        f = lib.check_database(self.ctx(**{
            _CONFIG_PATH: SPDX + "import os\n\n\ndef lib_database(path):\n"
                                 "    return os.environ.get('DATABASE_URL_LIB')\n"}))
        self.assertIn("hand_rolled_resolution", kinds(f, "error"))
        # tests.py is exempt, as everywhere
        f = lib.check_database(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "\nimport os\n\nURL = os.environ.get('DATABASE_URL')\n"}))
        self.assertNotIn("hand_rolled_resolution", kinds(f))

    def test_spec_without_dependency_is_warn(self):
        """DB-11"""
        f = lib.check_database(self.ctx(**{_SPEC_PATH: DB_SPEC}))
        self.assertIn("cascade_dependency_undeclared", kinds(f, "warn"))

    def test_spec_importing_django_is_error(self):
        """DB-12"""
        f = lib.check_database(self.ctx(**{
            _SPEC_PATH: SPDX + "from django.conf import settings\n\nSPEC = None\n",
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE}))
        self.assertIn("db_spec_imports_django", kinds(f, "error"))

    def test_a_db_spec_binding_no_spec_is_a_warn(self):
        """DB-16 — discovery reads the SPEC attribute; a module without one declares nothing."""
        f = lib.check_database(self.ctx(**{
            _SPEC_PATH: SPDX + "from evennia_database_cascade import AliasSpec\n",
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE}))
        self.assertIn("db_spec_missing_spec", kinds(f, "warn"))
        f = lib.check_database(self.ctx(**{
            _SPEC_PATH: DB_SPEC,
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE}))
        self.assertNotIn("db_spec_missing_spec", kinds(f))

    def test_a_reexported_spec_still_counts_as_bound(self):
        """DB-17 — a SPEC imported into db_spec.py is found by discovery the same way."""
        f = lib.check_database(self.ctx(**{
            _SPEC_PATH: SPDX + "from .config import SPEC\n",
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE}))
        self.assertNotIn("db_spec_missing_spec", kinds(f))

    def test_installing_documenting_databases_is_warn(self):
        """DB-13"""
        for snippet in (
                '\n```python\nDATABASE_ROUTERS = ["evennia_lib.db_router.R"]\n```\n',
                '\n```python\nDATABASE_ROUTERS += ["evennia_lib.db_router.R"]\n```\n',
                '\n```python\nDATABASES["lib"] = lib_database(path)\n```\n'):
            with self.subTest(snippet=snippet):
                f = lib.check_database(self.ctx(**{_INSTALLING_PATH: INSTALLING + snippet}))
                self.assertIn("installing_documents_databases", kinds(f, "warn"))

    def test_the_cascade_itself_is_exempt(self):
        """DB-14"""
        # Its router.py and environ reads *are* the mechanism.
        ctx = self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/router.py":
                SPDX + "class CascadeRouter:\n    def db_for_read(self, model, **hints):\n"
                       "        return None\n",
            _CONFIG_PATH: SPDX + "import os\n\n\ndef common_url():\n"
                                 "    return os.environ.get('DATABASE_URL')\n"})
        ctx.name = "evennia-database-cascade"
        ctx.expected_pkg = "evennia_database_cascade"
        self.assertEqual(lib.check_database(ctx), [])

    def test_spec_with_dependency_is_clean(self):
        """DB-15"""
        f = lib.check_database(self.ctx(**{
            _MODELS_PATH: SPDX + "x = 1\n",
            _SPEC_PATH: DB_SPEC,
            "libraries/evennia-lib/pyproject.toml": PYPROJECT_CASCADE,
            _INSTALLING_PATH: INSTALLING_CASCADE}))
        self.assertEqual(f, [])


class CheckTargeting(ValidatorBase):
    def test_no_dependency_is_silent(self):
        """TG-01"""
        self.assertEqual(lib.check_targeting(self.ctx()), [])

    def test_dependency_without_module_is_warn(self):
        """TG-02"""
        f = lib.check_targeting(self.ctx(**{
            _CORE_PATH: SPDX + "from evennia_targeting import walk_contents\n"}))
        self.assertIn("targeting_module_missing", kinds(f, "warn"))

    def test_callable_outside_module_is_warn(self):
        """TG-03"""
        f = lib.check_targeting(self.ctx(**{
            _TARGETING_PATH: SPDX + "def p_ok(obj, caller):\n    return True\n",
            _CORE_PATH: SPDX + "def p_is_wielded(obj, caller):\n    return True\n"}))
        self.assertIn("targeting_callable_outside_module", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_callables_inside_module_are_clean(self):
        """TG-04"""
        f = lib.check_targeting(self.ctx(**{
            _TARGETING_PATH: SPDX + "def p_ok(obj, caller):\n    return True\n"
                                    "def op_not(p):\n    return p\n"}))
        self.assertEqual(f, [])

    def test_module_alone_binds_the_rule(self):
        """TG-05"""
        f = lib.check_targeting(self.ctx(**{
            _TARGETING_PATH: SPDX + "def p_ok(obj, caller):\n    return True\n",
            _CORE_PATH: SPDX + "def f_by_lock(name):\n    return name\n"}))
        self.assertIn("targeting_callable_outside_module", kinds(f, "warn"))

    def test_tests_module_is_exempt(self):
        """TG-06"""
        f = lib.check_targeting(self.ctx(**{
            _TARGETING_PATH: SPDX + "def p_ok(obj, caller):\n    return True\n",
            "libraries/evennia-lib/src/evennia_lib/tests.py":
                LIB_TESTS + "def p_fixture(obj, caller):\n    return True\n"}))
        self.assertEqual(f, [])


    def test_targeting_library_itself_is_excluded(self):
        """TG-07"""
        spec = {k.replace("libraries/evennia-lib/", "libraries/evennia-targeting/")
                 .replace("/evennia_lib/", "/evennia_targeting/"): v
                for k, v in compliant().items()}
        spec["libraries/evennia-targeting/src/evennia_targeting/predicates.py"] = (
            SPDX + "def p_not_exit(obj, caller):\n    return True\n")
        spec["libraries/evennia-targeting/src/evennia_targeting/__init__.py"] = (
            SPDX + "from evennia_targeting.predicates import p_not_exit\n")
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        ctx = lib.LibContext(root / "libraries/evennia-targeting", root)
        self.assertEqual(lib.check_targeting(ctx), [])


class CheckContrib(ValidatorBase):
    def test_no_contrib_is_silent(self):
        """CT-01"""
        self.assertEqual(lib.check_contrib(self.ctx()), [])

    def test_empty_contrib_is_warn(self):
        """CT-02"""
        f = lib.check_contrib(self.ctx(**{f"{_CONTRIB}/__init__.py": ""}))
        self.assertIn("contrib_empty", kinds(f, "warn"))

    def test_populated_contrib_is_clean(self):
        """CT-03"""
        f = lib.check_contrib(self.ctx(**{
            f"{_CONTRIB}/__init__.py": "", f"{_CONTRIB}/exits.py": SPDX + "x = 1\n"}))
        self.assertEqual(f, [])

    def test_core_importing_contrib_is_error(self):
        """CT-04"""
        f = lib.check_contrib(self.ctx(**{
            f"{_CONTRIB}/__init__.py": "", f"{_CONTRIB}/exits.py": SPDX + "x = 1\n",
            _CORE_PATH: SPDX + "from .contrib.exits import x\n"}))
        self.assertIn("core_imports_contrib", kinds(f, "error"))

    def test_contrib_importing_contrib_is_clean(self):
        """CT-05"""
        f = lib.check_contrib(self.ctx(**{
            f"{_CONTRIB}/__init__.py": "", f"{_CONTRIB}/exits.py": SPDX + "x = 1\n",
            f"{_CONTRIB}/doors.py": SPDX + "from .exits import x\n"}))
        self.assertEqual(f, [])


class CheckDocs(ValidatorBase):
    def test_clean(self):
        """DC-01"""
        self.assertEqual(lib.check_docs(self.ctx()), [])

    def test_missing_docs_dir_is_single_error(self):
        """DC-02"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/INDEX.md",
                                          "libraries/evennia-lib/docs/installing.md",
                                          "libraries/evennia-lib/docs/interoperability.md",
                                          "libraries/evennia-lib/docs/progress.md",
                                          "libraries/evennia-lib/docs/test-plan.md",
                                          "libraries/evennia-lib/docs/archive/.gitkeep"]))
        self.assertEqual(len(f), 1)
        self.assertEqual(kinds(f, "error"), {"missing_docs"})

    def test_missing_index_is_error(self):
        """DC-03"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/INDEX.md"]))
        self.assertIn("missing_file", kinds(f, "error"))

    def test_missing_progress_is_warn(self):
        """DC-04"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/progress.md"]))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("missing_file", kinds(f, "warn"))

    def test_missing_archive_is_warn(self):
        """DC-05"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/archive/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))

    def test_documentation_structure_md_forbidden(self):
        """DC-06"""
        f = lib.check_docs(self.ctx(**{"libraries/evennia-lib/docs/documentation-structure.md": "# no\n"}))
        self.assertIn("forbidden_meta_doc", kinds(f, "error"))

    def test_missing_interoperability_is_error(self):
        """DC-08"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/interoperability.md"]))
        self.assertIn("missing_file", kinds(f, "error"))
        self.assertIn("interoperability.md", messages(f))

    def test_missing_installing_is_error(self):
        """DC-07"""
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/installing.md"]))
        self.assertIn("missing_file", kinds(f, "error"))
        self.assertIn("installing.md", messages(f))
        # A differently-named install doc does not satisfy it: the standard names
        # one filename so a consumer running several libraries looks in the same
        # place each time.
        f = lib.check_docs(self.ctx(drop=["libraries/evennia-lib/docs/installing.md"],
                                    **{"libraries/evennia-lib/docs/installation.md": "# Installation\n"}))
        self.assertIn("missing_file", kinds(f, "error"))


class CheckTestPlan(ValidatorBase):
    """The adapter onto the test-plan-linter skill. The plan-vs-suite cases
    themselves live in that skill's own plan and suite."""

    PLAN = "libraries/evennia-lib/docs/test-plan.md"
    LIB_TESTS = "libraries/evennia-lib/src/evennia_lib/tests.py"

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
            self.assertEqual(x.library, "evennia-lib")
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
            drop=SRC_FILES, **{"libraries/evennia-lib/src/notes.txt": "not a package\n"}))
        self.assertIn("missing_package", kinds(f, "error"))

    def test_missing_version_is_warn(self):
        """SL-04"""
        f = lib.check_src_layout(self.ctx(**{"libraries/evennia-lib/src/evennia_lib/__init__.py": SPDX}))
        self.assertIn("missing_version", kinds(f, "warn"))


class CheckNaming(ValidatorBase):
    def test_clean(self):
        """NM-01"""
        self.assertEqual(lib.check_naming(self.ctx()), [])

    def renamed(self, name):
        """The compliant tree under a different library directory name."""
        spec = {k.replace("libraries/evennia-lib/", f"libraries/{name}/"): v
                for k, v in compliant().items()}
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.LibContext(root / "libraries" / name, root)

    def test_no_family_prefix_is_error(self):
        """NM-03"""
        f = lib.check_naming(self.renamed("some-lib"))
        self.assertIn("family_prefix", kinds(f, "error"))

    def test_fcm_prefix_is_accepted(self):
        """NM-04"""
        f = lib.check_naming(self.renamed("fcm-lib"))
        self.assertNotIn("family_prefix", kinds(f))

    def test_name_must_be_hyphenated_lowercase(self):
        """NM-05"""
        for name in ("evennia_lib", "evennia-Lib"):
            with self.subTest(name=name):
                f = lib.check_naming(self.renamed(name))
                self.assertIn("library_name_form", kinds(f, "error"))

    def test_mismatch_is_error(self):
        """NM-02"""
        ctx = self.ctx(drop=["libraries/evennia-lib/src/evennia_lib/__init__.py",
                             "libraries/evennia-lib/src/evennia_lib/core.py"],
                       **{"libraries/evennia-lib/src/wrong_name/__init__.py": SPDX})
        self.assertIn("naming_mismatch", kinds(lib.check_naming(ctx), "error"))


class CheckSpdx(ValidatorBase):
    def test_clean(self):
        """SP-01"""
        self.assertEqual(lib.check_spdx(self.ctx()), [])

    def test_missing_is_warn(self):
        """SP-02"""
        f = lib.check_spdx(self.ctx(**{"libraries/evennia-lib/src/evennia_lib/core.py": "x = 1\n"}))
        self.assertIn("missing_spdx", kinds(f, "warn"))

    def test_migrations_excluded(self):
        """SP-03"""
        f = lib.check_spdx(self.ctx(**{"libraries/evennia-lib/src/evennia_lib/migrations/0001.py": "x=1\n"}))
        self.assertEqual(f, [])

    def test_header_below_first_five_lines_is_missing(self):
        """SP-04"""
        buried = '"""doc"""\n' + "\n" * 8 + SPDX + "x = 1\n"
        f = lib.check_spdx(self.ctx(**{"libraries/evennia-lib/src/evennia_lib/core.py": buried}))
        self.assertIn("missing_spdx", kinds(f, "warn"))


class CheckTestsDir(ValidatorBase):
    def test_placeholder_passes(self):
        """TD-01"""
        self.assertEqual(lib.check_tests_dir(self.ctx()), [])

    def test_missing_is_warn_not_error(self):
        """TD-02"""
        f = lib.check_tests_dir(self.ctx(drop=["libraries/evennia-lib/tests/.gitkeep"]))
        self.assertIn("missing_dir", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())


    def test_incomplete_tests_dir_is_warn(self):
        """TD-03"""
        f = lib.check_tests_dir(self.ctx(**{
            "libraries/evennia-lib/tests/__init__.py": ""}))
        self.assertIn("tests_dir_incomplete", kinds(f, "warn"))
        self.assertIn("test_settings.py", messages(f))

    def test_placeholder_only_stays_clean(self):
        """TD-04"""
        self.assertNotIn("tests_dir_incomplete", kinds(lib.check_tests_dir(self.ctx())))

    def test_pytest_in_use_is_warn(self):
        """TD-05"""
        f = lib.check_tests_dir(self.ctx(**{"libraries/evennia-lib/conftest.py": ""}))
        self.assertIn("pytest_in_use", kinds(f, "warn"))


class CheckLogging(ValidatorBase):
    def test_clean(self):
        """LG-01"""
        self.assertEqual(lib.check_logging(self.ctx()), [])

    def test_missing_shim_is_warn_not_error(self):
        """LG-02"""
        f = lib.check_logging(self.ctx(drop=["libraries/evennia-lib/src/evennia_lib/log.py"]))
        self.assertIn("missing_log_shim", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())

    def test_shim_naming_no_log_file_is_warn(self):
        """LG-04"""
        f = lib.check_logging(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/log.py": SPDX + LOG_SHIM.replace('"evennia_lib.log"', '""')}))
        self.assertIn("log_shim_filename", kinds(f, "warn"))

    def test_stdlib_logging_outside_the_shim_is_warn(self):
        """LG-06"""
        f = lib.check_logging(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/core.py":
                SPDX + 'import logging\n\nlogger = logging.getLogger("evennia_lib")\n'}))
        self.assertIn("stdlib_logging", kinds(f, "warn"))
        self.assertIn("core.py", messages(f))

    def test_no_package_is_silent(self):
        """LG-08"""
        ctx = self.ctx(drop=SRC_FILES + ["libraries/evennia-lib/src/evennia_lib/log.py"])
        self.assertEqual(lib.check_logging(ctx), [])

    def test_function_not_named_for_the_library_is_warn(self):
        """LG-09"""
        # Read off the assignment target, not a `def`. If the extraction ever
        # regresses to FunctionDef-only this goes quiet rather than failing,
        # which is what LG-20 exists to prevent.
        f = lib.check_logging(self.ctx(**{
            _LOG_PATH: SPDX + LOG_SHIM.replace("lib_log = ", "zzz_log = ")}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("log_shim_function_name", kinds(f, "warn"))

    def test_shim_reexported_from_init_is_warn(self):
        """LG-13"""
        f = lib.check_logging(self.ctx(**{
            "libraries/evennia-lib/src/evennia_lib/__init__.py":
                SPDX + '__version__ = "0.0.1"\nfrom .log import lib_log\n'}))
        self.assertIn("log_shim_exported", kinds(f, "warn"))

    def test_unused_shim_is_warn(self):
        """LG-15"""
        f = lib.check_logging(self.ctx(**{_CORE_PATH: SPDX + "x = 1\n"}))
        self.assertEqual(kinds(f, "error"), set())
        self.assertIn("log_shim_unused", kinds(f, "warn"))
        # A module calling it clears the finding.
        f = lib.check_logging(self.ctx(**{
            _CORE_PATH: SPDX + "from .log import lib_log\n\n\ndef f():\n    lib_log('x')\n"}))
        self.assertNotIn("log_shim_unused", kinds(f))

    def test_shim_not_calling_make_logger_is_error(self):
        """LG-16"""
        # What an un-migrated library reports: a hand-rolled shim is a shim
        # through the wrong mechanism, and its lines go where nobody reads.
        f = lib.check_logging(self.ctx(**{
            _LOG_PATH: SPDX + OLD_LOG_SHIM}))
        self.assertIn("log_shim_mechanism", kinds(f, "error"))

    def test_undeclared_dependency_is_warn(self):
        """LG-17"""
        f = lib.check_logging(self.ctx(**{
            "libraries/evennia-lib/pyproject.toml":
                PYPROJECT.replace(
                    'dependencies = ["evennia", "evennia-logging-extension"]',
                    'dependencies = ["evennia"]')}))
        self.assertIn("log_dependency_undeclared", kinds(f, "warn"))
        self.assertEqual(kinds(f, "error"), set())

    def test_a_filename_from_an_accessor_is_clean(self):
        """LG-18"""
        # Whether the name is hardcoded or read from a setting is the
        # library's decision, and the extension has no opinion. The linter
        # must not read an accessor call as a missing filename.
        shim = ('"""Logging shim."""\n\n'
                "from evennia_logging_extension import make_logger\n\n"
                "from .config import get_log_filename\n\n"
                "lib_log = make_logger(get_log_filename())\n")
        f = lib.check_logging(self.ctx(**{_LOG_PATH: SPDX + shim}))
        self.assertNotIn("log_shim_filename", kinds(f))
        self.assertEqual(kinds(f, "error"), set())

    def test_the_extension_itself_is_exempt(self):
        """LG-19"""
        # It has no log.py because it *is* the mechanism, and a logger that
        # logs its own failures through itself is a cycle.
        ctx = self.ctx(drop=["libraries/evennia-lib/src/evennia_lib/log.py"])
        ctx.name = "evennia-logging-extension"
        ctx.expected_pkg = "evennia_logging_extension"
        self.assertEqual(lib.check_logging(ctx), [])

    def test_module_scope_log_import_in_config_is_warn(self):
        """LG-21"""
        # log.py may import config.py for a settable filename, so the reverse
        # import at module scope completes a cycle that resolves or crashes on
        # declaration order. Lazy imports inside functions are the idiom.
        config = "libraries/evennia-lib/src/evennia_lib/config.py"

        # Module scope: a finding.
        f = lib.check_logging(self.ctx(**{
            config: SPDX + "from .log import lib_log\n\nX = 1\n"}))
        self.assertIn("log_import_in_config_scope", kinds(f, "warn"))

        # Inside a function: clean.
        f = lib.check_logging(self.ctx(**{
            config: SPDX + "def check_settings():\n"
                           "    from .log import lib_log\n"
                           "    lib_log('checked')\n"}))
        self.assertNotIn("log_import_in_config_scope", kinds(f))

        # No import at all: clean — logging from config.py is optional.
        f = lib.check_logging(self.ctx(**{config: SPDX + "X = 1\n"}))
        self.assertNotIn("log_import_in_config_scope", kinds(f))

    def test_an_unreadable_shim_is_reported_not_skipped(self):
        """LG-20"""
        # "Cannot tell" is reported, never treated as clean. The list is the
        # point: an implementation that special-cases one shape and skips the
        # rest fails here rather than reporting a clean library.
        unreadable = {
            "a def where a binding belongs":
                '"""Shim."""\n\n\ndef lib_log(message, level="INFO", trace=False):\n    pass\n',
            "two public bindings":
                '"""Shim."""\n\nfrom evennia_logging_extension import make_logger\n\n'
                'lib_log = make_logger("evennia_lib.log")\n'
                'other_log = make_logger("other.log")\n',
            "no binding at all":
                '"""Shim."""\n\nfrom evennia_logging_extension import make_logger\n',
            "an empty file": "",
            "a file that does not parse": "def (broken\n",
        }
        for shape, source in unreadable.items():
            with self.subTest(shape=shape):
                f = lib.check_logging(self.ctx(**{_LOG_PATH: SPDX + source}))
                self.assertTrue(f, f"{shape} produced no findings — it read as clean")



class CheckMemorySurface(ValidatorBase):
    def test_clean(self):
        """MS-01"""
        self.assertEqual(lib.check_memory_surface(self.ctx()), [])

    def test_forbidden(self):
        """MS-02"""
        f = lib.check_memory_surface(self.ctx(**{"libraries/evennia-lib/.claude/memory/x.md": "x\n"}))
        self.assertIn("forbidden_memory", kinds(f, "warn"))


class CheckPyproject(ValidatorBase):
    PP = "libraries/evennia-lib/pyproject.toml"

    def test_clean(self):
        """PP-01"""
        self.assertEqual(lib.check_pyproject(self.ctx()), [])

    def test_wrong_license_is_error(self):
        """PP-02"""
        pp = PYPROJECT.replace('license = {text = "BSD-3-Clause"}', 'license = {text = "MIT"}')
        self.assertIn("license", kinds(lib.check_pyproject(self.ctx(**{self.PP: pp})), "error"))

    def test_name_mismatch_is_error(self):
        """PP-03"""
        pp = PYPROJECT.replace('name = "evennia-lib"', 'name = "other"')
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
    def lint(self, spec, scope=("evennia-lib",)):
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        return lib.lint(root, list(scope) if scope else scope)

    def test_compliant_is_clean(self):
        """DS-01"""
        findings, libs = self.lint(compliant())
        self.assertEqual(libs, ["evennia-lib"])
        self.assertEqual(findings, [])

    def test_discovery_skips_non_library_dirs(self):
        """DS-02"""
        spec = compliant()
        spec["libraries/fixture-repo/data.yaml"] = "x: 1\n"  # no pyproject -> not a library
        _, libs = self.lint(spec, scope=None)
        self.assertEqual(libs, ["evennia-lib"])

    def test_scope_restricts_to_named_libraries(self):
        """DS-03"""
        spec = compliant()
        spec["libraries/other-lib/pyproject.toml"] = PYPROJECT.replace('"evennia-lib"', '"other-lib"')
        _, libs = self.lint(spec, scope=None)
        self.assertEqual(libs, ["evennia-lib", "other-lib"])
        _, libs = self.lint(spec)
        self.assertEqual(libs, ["evennia-lib"])

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
            code = lib.main(["--root", str(root), "evennia-lib", *argv])
        return code, buf.getvalue()

    def test_clean_library_exits_zero(self):
        """CL-01"""
        code, out = self.run_cli(compliant())
        self.assertEqual(code, 0)
        self.assertIn("evennia-lib — OK", out)

    def test_error_exits_one(self):
        """CL-02"""
        spec = compliant()
        spec.pop("libraries/evennia-lib/LICENSE")
        self.assertEqual(self.run_cli(spec)[0], 1)

    def test_warnings_exit_zero_unless_strict(self):
        """CL-03"""
        spec = compliant()
        spec.pop("libraries/evennia-lib/.gitignore")
        self.assertEqual(self.run_cli(spec)[0], 0)
        self.assertEqual(self.run_cli(spec, "--strict")[0], 1)

    def test_json_output_carries_findings_and_counts(self):
        """CL-04"""
        spec = compliant()
        spec.pop("libraries/evennia-lib/LICENSE")
        spec.pop("libraries/evennia-lib/.gitignore")
        _, out = self.run_cli(spec, "--json")
        payload = json.loads(out)
        summary = payload["summary"]
        self.assertEqual(summary["libraries"], ["evennia-lib"])
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

    def emitted_findings(self, source=None):
        """Every finding name the linter can emit, read off its `ctx.F(...)` calls."""
        src = source or (HERE / "lint_library.py").read_text(encoding="utf-8")
        return {n.args[0].value for n in ast.walk(ast.parse(src))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "F" and n.args and isinstance(n.args[0], ast.Constant)}

    def test_every_finding_is_documented_in_the_skill(self):
        """XC-04"""
        skill = (HERE / "SKILL.md").read_text(encoding="utf-8")
        undocumented = sorted(n for n in self.emitted_findings() if n not in skill)
        self.assertEqual(undocumented, [])
        # Not vacuous: the same comparison against a SKILL.md missing one row fails.
        gutted = skill.replace("`stdlib_logging`", "`x`")
        self.assertIn("stdlib_logging",
                      {n for n in self.emitted_findings() if n not in gutted})

    def test_finding_paths_are_repo_relative(self):
        """XC-03"""
        spec = compliant()
        spec.pop("libraries/evennia-lib/LICENSE")
        tmp, root = build(spec)
        self.addCleanup(tmp.cleanup)
        findings, _ = lib.lint(root, ["evennia-lib"])
        self.assertTrue(findings)
        for f in findings:
            self.assertFalse(Path(f.path).is_absolute())
            self.assertNotIn(str(root), f.path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
