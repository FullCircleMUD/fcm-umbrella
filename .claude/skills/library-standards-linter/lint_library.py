#!/usr/bin/env python3
"""library-standards-linter — deterministic checks against library-standards.md.

No model is in the loop: same input -> same output. This is the mechanical half of
the library-standards audit. It checks the *machine-decidable* subset of
`design/library-standards.md` for each reusable library under `libraries/` and is
meant to be composed into agentic workflows (a future library-standards-auditor
ingests `--json` and adjudicates declared divergences), called directly from a
Claude session, or wired into CI.

Structure: each library is read once into a `LibContext`, then every check is a
single-purpose `LibContext -> list[Finding]` validator in the `CHECKS` list — each
independently unit-tested. Add or remove a check by editing that list.

Calibration: structural folders the standard expects (`tests/`, `docs/archive/`)
are checked at *folder-presence* level — a placeholder (`.gitkeep` or a short
README explaining why) satisfies them; the linter does not demand their internal
contents. `examples/` is optional. Whether a gap is a sanctioned divergence (e.g.
a pure-Python library with no Evennia test infra) is left to the judgment layer:
the linter surfaces the deviation; the accepted resolutions are "add the structure
(placeholder OK)" or "document the divergence in the library's CLAUDE.md".
`docs/test-plan.md` is delegated to the sibling `test-plan-linter` skill, which
owns every plan-vs-suite rule; this module only supplies the paths and wraps the
findings.

Run from the umbrella root:  python .claude/skills/library-standards-linter/lint_library.py
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path

# The test-plan checks live in their own skill so any linter can use them; a gap
# fixed there is fixed for every consumer. Imported as a sibling skill.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "test-plan-linter"))
import lint_test_plan as plan_linter  # noqa: E402

# A library under libraries/ is any directory carrying a pyproject.toml. This
# excludes auxiliary repos (test-content / fixture repos) which are not bound by
# the standards (per library-standards.md).
LIBRARIES_DIR = "libraries"

SPDX = "SPDX-License-Identifier: BSD-3-Clause"
SPDX_SKIP_DIRS = {"migrations", "__pycache__"}

# The two families. `evennia-*` is game-agnostic; `fcm-*` embeds FCM's concepts
# deliberately. The prefix is a claim about who can use the library.
FAMILY_PREFIXES = ("evennia-", "fcm-")
LIBRARY_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# A constant is an UPPER_SNAKE module-level name, optionally private. This is
# what excludes `__version__` and any ordinary lower-case module variable.
CONSTANT_NAME = re.compile(r"^_?[A-Z][A-Z0-9_]*$")
CONSTANT_SKIP_DIRS = {"migrations", "__pycache__"}
# tests.py lives inside the package by Django convention, but its constants are
# scaffolding rather than library surface.
CONSTANT_SKIP_FILES = {"tests.py"}
CONSTANT_HOME = "config.py"
# The bounded exemption: log.py may declare these two and nothing else.
LOG_SHIM_CONSTANTS = ("_LOG_FILENAME", "_VALID_LEVELS")
SHIM_ARGS = ("message", "level", "trace")
SHIM_LEVELS = ("INFO", "WARN", "ERROR")
# log_file already prefixes a UTC timestamp; a second stamps every line twice.
SHIM_TIMESTAMP = re.compile(r"\bdatetime\b|\bstrftime\b|\btime\.time\b")


def _library_words(name):
    """The words in a library name — `evennia-message-bus` -> evennia, message, bus."""
    return [w for w in re.split(r"[-_]", name.lower()) if w]


def _names_the_library(token, words):
    """True when `token` is one of `words`, or an unambiguous stem of one.

    The stem rule is what lets `shard_log` stand for `evennia-shards` while
    still refusing `ms_log` and `wb_log`. Four characters is the floor: below
    it a "stem" is an abbreviation, which the standard bans because it reads
    fine to whoever picked it and to nobody afterwards.
    """
    if token in words:
        return True
    return any((token.startswith(w) or w.startswith(token))
               and min(len(token), len(w)) >= 4 for w in words)


def _shim_function(tree):
    """The shim's single public module-level function, or None if unclear."""
    fns = [n for n in tree.body
           if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
    return fns[0] if len(fns) == 1 else None


class Finding:
    __slots__ = ("check", "severity", "library", "path", "message")

    def __init__(self, check, severity, library, path, message):
        self.check = check
        self.severity = severity      # "error" | "warn"
        self.library = library
        self.path = path              # repo-relative str
        self.message = message

    def as_dict(self):
        return {"check": self.check, "severity": self.severity, "library": self.library,
                "path": self.path, "message": self.message}


# --- helpers -----------------------------------------------------------------
def rel(p: Path, root: Path):
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def head(path: Path, n=5):
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            return "".join(next(f, "") for _ in range(n))
    except OSError:
        return ""


def _resolve_pkg(src: Path):
    """The single package directory under src/ (a dir with __init__.py), or None."""
    if not src.is_dir():
        return None
    pkgs = [d for d in sorted(src.iterdir())
            if d.is_dir() and (d / "__init__.py").exists()]
    return pkgs[0] if pkgs else None


def _load_pyproject(pp: Path):
    """Return (parsed_dict_or_None, error_str_or_None)."""
    if not pp.exists():
        return None, None
    try:
        return tomllib.loads(pp.read_text(encoding="utf-8")), None
    except (tomllib.TOMLDecodeError, OSError) as e:
        return None, str(e)


class LibContext:
    """One library read once, shared by every check."""

    def __init__(self, libdir: Path, root: Path):
        self.libdir = libdir
        self.root = root
        self.name = libdir.name
        self.expected_pkg = self.name.replace("-", "_")
        self.src = libdir / "src"
        self.pkg = _resolve_pkg(self.src)
        self.pyproject_path = libdir / "pyproject.toml"
        self.pyproject, self.pyproject_error = _load_pyproject(self.pyproject_path)

    def F(self, check, severity, path: Path, message):
        return Finding(check, severity, self.name, rel(path, self.root), message)


# --- checks (each: LibContext -> list[Finding], independently unit-testable) --
def check_root_files(ctx):
    out = []
    for fn, sev in [("pyproject.toml", "error"), ("README.md", "error"),
                    ("CLAUDE.md", "error"), ("LICENSE", "error"),
                    (".gitignore", "warn"), ("runtests.py", "warn")]:
        if not (ctx.libdir / fn).exists():
            out.append(ctx.F("missing_file", sev, ctx.libdir / fn, f"missing {fn}"))
    return out


def _module_constants(path: Path):
    """`([(name, node)], tree)` for a module's top-level constants, in file order.

    Parsed rather than grepped: `tree.body` is *only* module scope, so a
    constant-looking name inside a function or a docstring cannot match. An
    unparseable file yields nothing — a syntax error is not this check's to
    report.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return [], None
    found = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        for t in targets:
            if isinstance(t, ast.Name) and CONSTANT_NAME.match(t.id):
                found.append((t.id, node))
    return found, tree


def _check_log_shim(ctx, path, constants, tree):
    """The bounded exemption: exactly the two names, at the top of the file."""
    out = []
    extra = [name for name, _ in constants if name not in LOG_SHIM_CONSTANTS]
    if extra:
        out.append(ctx.F(
            "log_shim_extra_constant", "error", path,
            f"log.py declares {', '.join(extra)} — its exemption is exactly "
            f"{' and '.join(LOG_SHIM_CONSTANTS)}. Everything else belongs in "
            f"{CONSTANT_HOME}"))
    if not constants or tree is None:
        return out
    # Only the module docstring and `import traceback` may precede them.
    for node in tree.body[:tree.body.index(constants[0][1])]:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            continue
        if isinstance(node, ast.Import) and [a.name for a in node.names] == ["traceback"]:
            continue
        out.append(ctx.F(
            "log_shim_constant_placement", "warn", path,
            "log.py has something above its constants other than the module "
            "docstring and `import traceback`. The two names sit at the top so "
            "anyone looking for them finds them without reading the file"))
        break
    return out


def check_constants(ctx):
    """Every module-level constant lives in config.py; log.py is bounded-exempt.

    Encodes *Where constants are declared* in library-standards.md. Reports
    `constant_outside_config` (warn) for a constant declared anywhere but
    `config.py`, `log_shim_extra_constant` (error) for a name in `log.py`
    outside `{_LOG_FILENAME, _VALID_LEVELS}`, and `log_shim_constant_placement`
    (warn) where anything but `import traceback` sits above them.

    `tests.py` and `migrations/` are out of scope — the first is scaffolding
    that lives in the package by Django convention, the second is generated.
    """
    if ctx.pkg is None:
        return []
    out, stray = [], []
    for f in sorted(ctx.pkg.rglob("*.py")):
        if CONSTANT_SKIP_DIRS & set(f.parts) or f.name in CONSTANT_SKIP_FILES:
            continue
        if f.name == CONSTANT_HOME:
            continue
        constants, tree = _module_constants(f)
        if f.name == "log.py":
            out += _check_log_shim(ctx, f, constants, tree)
            continue
        stray += [(f, name) for name, _ in constants]

    if stray:
        shown = ", ".join(f"{rel(f, ctx.root)}:{name}" for f, name in stray[:6])
        more = f" (+{len(stray) - 6} more)" if len(stray) > 6 else ""
        out.append(ctx.F(
            "constant_outside_config", "warn", ctx.pkg,
            f"{len(stray)} module-level constant(s) declared outside "
            f"{CONSTANT_HOME}: {shown}{more}. One file holds them all, so a "
            f"session about to declare one finds the existing name first"))
    return out


# CLAUDE.md's nine standard sections, in the order the standard fixes. Extra
# sections between them are allowed and common — only these are checked.
CLAUDE_SECTIONS = ("What this project is", "Project status", "Where to read first",
                   "Load-bearing architectural principles", "Out of scope",
                   "Working conventions", "Documentation discipline (load-bearing)",
                   "Repository layout", "Tools and environment")
# (label, pattern) for the principles section 4 must carry. An `fcm-*` library
# carries only the third: the standard has it state that the two scope
# principles deliberately do not apply, and a mention either way reads the same
# to a linter, so checking them would be guessing.
CLAUDE_PRINCIPLES = (
    ("does not own game concepts", re.compile(r"own game concepts", re.I), False),
    ("No FCM-specific assumptions", re.compile(r"FCM-specific assumptions", re.I), False),
    ("Test-first", re.compile(r"test-first|test-plan\.md", re.I), True),
)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def check_claude_md(ctx):
    """CLAUDE.md's nine sections and its section-4 principles.

    See design/library-standards.md § CLAUDE.md structure. A missing CLAUDE.md
    is `check_root_files`' finding, not this one — two findings for one absent
    file is noise.
    """
    path = ctx.libdir / "CLAUDE.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    found = SECTION_RE.findall(text)
    out = []

    missing = [s for s in CLAUDE_SECTIONS if s not in found]
    if missing:
        out.append(ctx.F("claude_md_section", "error", path,
                         f"CLAUDE.md is missing section(s): {', '.join(missing)}. The nine "
                         f"standard sections are what lets a session find the same thing in "
                         f"the same place across the libraries"))

    present = [s for s in CLAUDE_SECTIONS if s in found]
    if present != sorted(present, key=lambda s: found.index(s)):
        out.append(ctx.F("claude_md_order", "error", path,
                         "CLAUDE.md's standard sections are out of order. Extra sections "
                         "between them are fine; the required nine keep their sequence"))

    body = text.split("## Load-bearing architectural principles", 1)
    if len(body) == 2:
        section = re.split(r"^## ", body[1], maxsplit=1, flags=re.M)[0]
        fcm = ctx.name.startswith("fcm-")
        for label, pattern, applies_to_fcm in CLAUDE_PRINCIPLES:
            if fcm and not applies_to_fcm:
                continue
            if not pattern.search(section):
                out.append(ctx.F(
                    "claude_md_principle", "warn", path,
                    f"the principles section does not state `{label}` — one of the "
                    f"{'principle an `fcm-*` library carries' if fcm else 'three every '
                    '`evennia-*` library carries'}"))
    return out


# The three relationships a sibling section may declare. "No known issues" on its
# own is not one of them — that is the void the document exists to remove.
INTEROP_RELATIONSHIPS = re.compile(
    r"hard dependency|optional integration|no coupling", re.I)


def check_interoperability(ctx):
    """`docs/interoperability.md` against the actual contents of `libraries/`.

    The one check that reads the corpus rather than the library alone, because
    "every sibling" is a fact about the directory. Its absence is
    `check_docs`' finding, not this one.
    """
    path = ctx.libdir / "docs" / "interoperability.md"
    if not path.exists():
        return []

    expected = [d.name for d in discover(ctx.root, None)]
    if not expected:
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = SECTION_RE.findall(text)
    covered = [s for s in sections if s in expected]
    out = []

    missing = [name for name in expected if name not in covered]
    if missing:
        out.append(ctx.F(
            "interop_missing_sibling", "warn", path,
            f"interoperability.md has no section for {', '.join(missing)}. It covers every "
            f"library in libraries/ including itself, so a reader gets a definite statement "
            f"from either side rather than inferring from silence"))

    if covered != sorted(covered):
        out.append(ctx.F(
            "interop_order", "warn", path,
            "interoperability.md's sibling sections are not in alphabetical order. One "
            "template, no permutations — the copies are meant to be readable side by side"))

    # Split on every heading, so each section's body is what follows its own.
    bodies = dict(zip(sections, re.split(r"^##\s+.+?\s*$", text, flags=re.M)[1:]))
    for name in covered:
        # The library's own entry says "This library." and nothing else, so it
        # has no relationship to declare.
        if name == ctx.name:
            continue
        if not INTEROP_RELATIONSHIPS.search(bodies.get(name, "")):
            out.append(ctx.F(
                "interop_no_relationship", "warn", path,
                f"the {name} section names no relationship. It opens with one of hard "
                f"dependency, optional integration or no coupling, then the considerations "
                f"or an explicit clearance — an empty section is the void the document "
                f"exists to remove"))
    return out


INSTALLING_STEP = re.compile(r"^##\s+\d+\.", re.M)
INSTALLING_PARTS = (
    ("installing_no_required_settings", re.compile(r"required settings", re.I),
     "names no required settings — name, what it does, and what happens without it"),
    ("installing_no_optional_settings", re.compile(r"optional settings", re.I),
     "names no optional settings — name, default, and why the default is what it is"),
)
# A library with no settings says so in one line rather than dropping the section.
INSTALLING_NO_SETTINGS = re.compile(r"no settings", re.I)
INSTALLING_UNCHECKED = re.compile(r"not checked for you", re.I)


def check_installing(ctx):
    """`docs/installing.md`'s contents — see § The installation document.

    `check_docs` owns the file's absence; this owns what is in it. Without the
    split, renaming an existing document to `installing.md` turns the linter
    green while the document still fails the standard.
    """
    path = ctx.libdir / "docs" / "installing.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    out = []

    if len(INSTALLING_STEP.findall(text)) < 3:
        out.append(ctx.F(
            "installing_no_steps", "warn", path,
            "installing.md has no numbered step list. A consumer works down it in order — "
            "install the package, add the app, declare the settings, mix in the typeclasses "
            "— one step per heading, each carrying the code to paste"))

    states_none = INSTALLING_NO_SETTINGS.search(text)
    for check, pattern, complaint in INSTALLING_PARTS:
        if not states_none and not pattern.search(text):
            out.append(ctx.F(check, "warn", path, f"installing.md {complaint}"))

    if not INSTALLING_UNCHECKED.search(text):
        out.append(ctx.F(
            "installing_no_unchecked_section", "warn", path,
            "installing.md has no `what is not checked for you` section — the mistakes "
            "check_settings() cannot catch, so a consumer knows where the safety net ends. "
            "INSTALLED_APPS is always one of them"))
    return out


def _package_modules(ctx, extra_skip=()):
    """Every library source file a code rule applies to, with its AST.

    `tests.py` and `migrations/` are out of scope throughout: the first exists
    to emulate a running game, the second is generated.
    """
    for f in sorted(ctx.pkg.rglob("*.py")):
        if CONSTANT_SKIP_DIRS & set(f.parts) or f.name in CONSTANT_SKIP_FILES:
            continue
        if f.name in extra_skip:
            continue
        tree = _parse(f)
        if tree is not None:
            yield f, tree


def _aggregate(ctx, check, sites, message):
    """One finding per library, naming up to six sites."""
    if not sites:
        return []
    shown = ", ".join(f"{rel(f, ctx.root)}:{line}" for f, line in sites[:6])
    more = f" (+{len(sites) - 6} more)" if len(sites) > 6 else ""
    return [ctx.F(check, "warn", ctx.pkg, f"{len(sites)} {message}: {shown}{more}")]


def check_evennia_imports(ctx):
    """Evennia is imported in log.py; elsewhere the import says why.

    See § Importing Evennia. The comment is looked for on the line above, which
    is where the standard's example puts it — a reader landing on the import
    should see the reason without hunting for it.
    """
    if ctx.pkg is None:
        return []
    sites = []
    for f, tree in _package_modules(ctx, extra_skip=("log.py",)):
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            elif isinstance(node, ast.Import):
                module = node.names[0].name if node.names else ""
            else:
                continue
            if module.split(".")[0] != "evennia":
                continue
            above = lines[node.lineno - 2].strip() if node.lineno >= 2 else ""
            # The SPDX header is a comment and sits above the first import in
            # every file, so it would silence exactly the import most likely to
            # need explaining.
            if not above.startswith("#") or SPDX in above:
                sites.append((f, node.lineno))
    return _aggregate(
        ctx, "evennia_import_unexplained", sites,
        "Evennia import(s) outside log.py with no comment saying why that module needs "
        "the engine. The narrower the coupling, the more of the library runs without an "
        "engine — and an import with no comment is an open question, not a settled one")


def check_object_state(ctx):
    """A library sets its own attributes by assignment, never through `.db`.

    See § Reading and writing object state. `.db` goes through the
    AttributeHandler and never reaches an AttributeProperty's `at_set()`, so a
    validated property accepts through `.db` whatever it would refuse by
    assignment.
    """
    if ctx.pkg is None:
        return []
    sites = []
    for f, tree in _package_modules(ctx):
        for node in ast.walk(tree):
            targets = (node.targets if isinstance(node, ast.Assign)
                       else [node.target] if isinstance(node, (ast.AnnAssign, ast.AugAssign))
                       else [])
            for t in targets:
                # obj.db.<name> = … — the write is what the standard names; a
                # read through .db is ordinary Evennia.
                if (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Attribute)
                        and t.value.attr == "db"):
                    sites.append((f, node.lineno))
    return _aggregate(
        ctx, "db_attribute_write", sites,
        "write(s) through `.db`. A library sets its own attributes by assignment, because "
        "`.db` never reaches the descriptor — an unvalidated property is one commit away "
        "from a validated one, and every `.db` write is then silently wrong")


def check_boot_side_effects(ctx):
    """A library creates no directories in the consumer's gamedir.

    See § Consumer-authored config. Where a consumer's modules sit is theirs to
    decide; a library that creates a folder takes the decision away and leaves
    something behind in a repo it does not own.
    """
    if ctx.pkg is None:
        return []
    sites = []
    for f, tree in _package_modules(ctx):
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr in ("makedirs", "mkdir")):
                sites.append((f, node.lineno))
    return _aggregate(
        ctx, "creates_directories", sites,
        "director(y/ies) created by library code. Config the consumer authors is named by a "
        "setting and read from where they put it — a library that creates the folder decides "
        "for them and leaves something behind in a repo it does not own")


SETTINGS_VALIDATOR = "check_settings"
# Two libraries call theirs validate_settings; the standard names one function so
# every library's boot check is found in the same place under the same name.
SETTINGS_VALIDATOR_ALIASES = ("check_settings", "validate_settings")


def check_boot_validation(ctx):
    """`check_settings()` lives in config.py and is called from `ready()`.

    See § Reading settings. The inverse — a library with required settings and no
    validator at all — is not decidable here: the linter cannot know which of a
    library's settings are required.
    """
    if ctx.pkg is None:
        return []
    out, found = [], []
    for f in sorted(ctx.pkg.rglob("*.py")):
        if CONSTANT_SKIP_DIRS & set(f.parts) or f.name in CONSTANT_SKIP_FILES:
            continue
        tree = _parse(f)
        if tree is None:
            continue
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in SETTINGS_VALIDATOR_ALIASES:
                found.append((f, node.name))
    if not found:
        return []

    for f, name in found:
        if f.name != CONSTANT_HOME:
            out.append(ctx.F(
                "settings_validator_outside_config", "error", f,
                f"`{name}` is defined in {f.name}, not {CONSTANT_HOME}. One function, one "
                f"place, in every library — four guard clauses in a row beat four one-line "
                f"checks scattered across modules"))
        if name != SETTINGS_VALIDATOR:
            out.append(ctx.F(
                "settings_validator_name", "warn", f,
                f"the boot validator is `{name}`; the standard names it "
                f"`{SETTINGS_VALIDATOR}`, so it is found under one name in every library"))

    apps = ctx.pkg / "apps.py"
    tree = _parse(apps) if apps.exists() else None
    called = False
    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "ready":
                called = any(
                    isinstance(c, ast.Call) and (
                        (isinstance(c.func, ast.Name) and c.func.id in SETTINGS_VALIDATOR_ALIASES)
                        or (isinstance(c.func, ast.Attribute)
                            and c.func.attr in SETTINGS_VALIDATOR_ALIASES))
                    for c in ast.walk(node))
                if called:
                    break
    if not called:
        names = ", ".join(sorted({n for _, n in found}))
        out.append(ctx.F(
            "settings_validator_uncalled", "error", apps,
            f"`{names}` is defined but never called from AppConfig.ready(). A validator "
            f"nothing calls looks like validation and performs none — the misconfigured "
            f"instance starts cleanly and fails later, somewhere that says nothing about "
            f"the setting"))
    return out


def _is_settings_read(node):
    """`settings.NAME` or `getattr(settings, …)` — both bypass an accessor."""
    if isinstance(node, ast.Attribute):
        return isinstance(node.value, ast.Name) and node.value.id == "settings"
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "getattr" and node.args
            and isinstance(node.args[0], ast.Name) and node.args[0].id == "settings")


def check_settings_access(ctx):
    """Settings are read through a named accessor in config.py, and read late.

    See § Reading settings. The linter sees only the reads that exist, so an
    accessor that is *missing* for a setting the library ought to read is the
    judgment layer's to spot.
    """
    if ctx.pkg is None:
        return []
    out, stray = [], []
    for f in sorted(ctx.pkg.rglob("*.py")):
        if CONSTANT_SKIP_DIRS & set(f.parts) or f.name in CONSTANT_SKIP_FILES:
            continue
        tree = _parse(f)
        if tree is None:
            continue

        if f.name != CONSTANT_HOME:
            reads = sum(1 for n in ast.walk(tree) if _is_settings_read(n))
            if reads:
                stray.append((f, reads))
        else:
            # In the right file and still evaluated at import time, which is the
            # failure the rule exists to prevent. Elsewhere the read is already
            # reported as outside its accessor.
            if any(_is_settings_read(n) for node in tree.body
                   if isinstance(node, (ast.Assign, ast.AnnAssign))
                   for n in ast.walk(node)):
                out.append(ctx.F(
                    "settings_read_at_module_scope", "warn", f,
                    "config.py reads a setting at module scope. The read belongs inside the "
                    "accessor — at module scope it runs when the library is first imported, "
                    "which can be while the consumer's settings module is still executing"))

        if any(isinstance(n, ast.ImportFrom) and n.module == "django.conf"
               and any(a.name == "settings" for a in n.names) for n in tree.body):
            out.append(ctx.F(
                "settings_import_at_module_scope", "warn", f,
                "`from django.conf import settings` at module scope. The standard puts it "
                "inside the function, for the same import-timing reason the read is deferred"))

    if stray:
        shown = ", ".join(f"{rel(f, ctx.root)}({n})" for f, n in stray[:6])
        more = f" (+{len(stray) - 6} more)" if len(stray) > 6 else ""
        out.append(ctx.F(
            "settings_read_outside_config", "warn", ctx.pkg,
            f"{sum(n for _, n in stray)} settings read(s) outside {CONSTANT_HOME}: {shown}"
            f"{more}. Each setting gets a named accessor there, and a direct read is what "
            f"raises AttributeError for the consumer who declared nothing"))
    return out


def check_docs(ctx):
    docs = ctx.libdir / "docs"
    if not docs.is_dir():
        return [ctx.F("missing_docs", "error", docs, "missing docs/ directory")]
    out = []
    if not (docs / "INDEX.md").exists():
        out.append(ctx.F("missing_file", "error", docs / "INDEX.md", "missing docs/INDEX.md"))
    # The filename is part of the standard, not just the content: a consumer
    # running several of our libraries looks in the same place each time, so an
    # install doc under any other name does not satisfy this.
    if not (docs / "installing.md").exists():
        out.append(ctx.F("missing_file", "error", docs / "installing.md",
                          "missing docs/installing.md — the numbered install steps, the required "
                          "and optional settings, and what is not checked for you"))
    # Required so a reader deciding whether two libraries can be co-installed gets
    # a definite statement from either side rather than inferring from silence.
    if not (docs / "interoperability.md").exists():
        out.append(ctx.F("missing_file", "error", docs / "interoperability.md",
                          "missing docs/interoperability.md — this library against every "
                          "sibling, each either a stated consideration or an explicit clearance"))
    if not (docs / "progress.md").exists():
        out.append(ctx.F("missing_file", "warn", docs / "progress.md", "missing docs/progress.md"))
    if not (docs / "archive").is_dir():
        out.append(ctx.F("missing_dir", "warn", docs / "archive",
                          "missing docs/archive/ (a placeholder dir is fine)"))
    if (docs / "documentation-structure.md").exists():
        out.append(ctx.F("forbidden_meta_doc", "error", docs / "documentation-structure.md",
                          "docs/documentation-structure.md must not exist — libraries follow the "
                          "umbrella's conventions (the reduced-set standard), not a per-repo copy"))
    return out


# --- test-plan (delegated to the test-plan-linter skill) ---------------------
# That linter reports a missing plan as `test_plan_missing`; under the library
# standard an absent required doc is a `missing_file`, so it is renamed here.
CHECK_RENAMES = {"test_plan_missing": "missing_file"}


def check_test_plan(ctx):
    docs = ctx.libdir / "docs"
    if not docs.is_dir():
        return []                                   # already reported by check_docs
    roots = [p for p in (ctx.pkg, ctx.libdir / "tests") if p]
    return [ctx.F(CHECK_RENAMES.get(f.check, f.check), f.severity,
                  ctx.root / f.path, f.message)
            for f in plan_linter.check_test_plan(docs / "test-plan.md", roots, ctx.root)]


def check_src_layout(ctx):
    if not ctx.src.is_dir():
        return [ctx.F("missing_src", "error", ctx.src, "missing src/ directory")]
    if ctx.pkg is None:
        return [ctx.F("missing_package", "error", ctx.src,
                      "no package (a dir with __init__.py) under src/")]
    init = ctx.pkg / "__init__.py"
    if "__version__" not in init.read_text(encoding="utf-8", errors="replace"):
        return [ctx.F("missing_version", "warn", init,
                      "no __version__ in the package __init__.py")]
    return []


def check_naming(ctx):
    out = []
    if not ctx.name.startswith(FAMILY_PREFIXES):
        out.append(ctx.F(
            "family_prefix", "error", ctx.libdir,
            f"'{ctx.name}' carries neither family prefix. The prefix states what the code "
            f"is allowed to know — {' or '.join(p.rstrip('-') for p in FAMILY_PREFIXES)} — "
            f"and a library without one has not answered the question"))
    if not LIBRARY_NAME.match(ctx.name):
        out.append(ctx.F(
            "library_name_form", "error", ctx.libdir,
            f"'{ctx.name}' is not hyphenated lowercase. The repo name and the PyPI "
            f"distribution name are the same string, so it carries the constraints of both"))
    if ctx.pkg is not None and ctx.pkg.name != ctx.expected_pkg:
        out.append(ctx.F("naming_mismatch", "error", ctx.pkg,
                         f"src package '{ctx.pkg.name}' should be '{ctx.expected_pkg}' "
                         "(underscored form of the repo name)"))
    return out


def check_spdx(ctx):
    if ctx.pkg is None:
        return []
    missing = [f for f in sorted(ctx.pkg.rglob("*.py"))
               if not (SPDX_SKIP_DIRS & set(f.parts)) and SPDX not in head(f)]
    if not missing:
        return []
    shown = ", ".join(rel(f, ctx.root) for f in missing[:6])
    more = f" (+{len(missing) - 6} more)" if len(missing) > 6 else ""
    return [ctx.F("missing_spdx", "warn", ctx.pkg,
                  f"{len(missing)} source file(s) missing the SPDX header "
                  f"`# {SPDX}`: {shown}{more}")]


def check_tests_dir(ctx):
    if (ctx.libdir / "tests").is_dir():
        return []
    return [ctx.F("missing_dir", "warn", ctx.libdir / "tests",
                  "no tests/ directory — add it (a placeholder is fine) or document a "
                  "divergence in CLAUDE.md (e.g. a pure-Python library)")]


def _parse(path: Path):
    """The module's AST, or None where it cannot be read or parsed."""
    try:
        return ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return None


def _check_shim_interface(ctx, shim: Path, source: str):
    """The shim's public function: named for the library, with the fixed signature."""
    tree = _parse(shim)
    if tree is None:
        return []
    out = []

    fn = _shim_function(tree)
    if fn is not None:
        words = _library_words(ctx.name)
        stem = fn.name[:-4] if fn.name.endswith("_log") else fn.name
        if not fn.name.endswith("_log") or not all(
                _names_the_library(part, words) for part in stem.split("_") if part):
            out.append(ctx.F(
                "log_shim_function_name", "warn", shim,
                f"the shim's function is `{fn.name}` — it should be named for the library "
                f"({'/'.join(words)}) plus `_log`, in full words. A reader tracing a log line "
                f"back uses that name to tell whose it is, and an abbreviation reads fine only "
                f"to whoever picked it"))
        if tuple(a.arg for a in fn.args.args) != SHIM_ARGS:
            out.append(ctx.F(
                "log_shim_signature", "warn", shim,
                f"`{fn.name}` takes {tuple(a.arg for a in fn.args.args)} — the shim's signature "
                f"is {SHIM_ARGS}. It is copied between libraries, so a changed one means a copy "
                f"was edited rather than adapted"))

    for name, node in _module_constants(shim)[0]:
        if name != "_VALID_LEVELS":
            continue
        try:
            value = ast.literal_eval(node.value)
        except ValueError:
            break
        if tuple(value) != SHIM_LEVELS:
            out.append(ctx.F(
                "log_shim_levels", "warn", shim,
                f"_VALID_LEVELS is {tuple(value)} — the shim's levels are {SHIM_LEVELS}. A "
                f"fourth level is one the rest of the corpus cannot be grepped for"))
        break
    return out


def check_logging(ctx):
    """The logging shim — see design/library-standards.md § Logging.

    Every library logs to a file of its own through ``log.py``, a lazy wrapper
    over Evennia's ``logger.log_file``. Only the mechanically decidable parts
    are checked here: that the shim exists, that it uses that mechanism, that
    it degrades outside an Evennia engine, and that no other module has fallen
    back to stdlib ``logging`` — records nobody sees, which is the failure the
    shim exists to prevent.
    """
    if ctx.pkg is None:
        return []
    out = []
    shim = ctx.pkg / "log.py"
    if not shim.exists():
        out.append(ctx.F("missing_log_shim", "warn", shim,
                         "no log.py — a library logs to a file of its own through the shim "
                         "(copy a sibling's and rename); or document a divergence in CLAUDE.md"))
    else:
        source = shim.read_text(encoding="utf-8", errors="replace")
        if "log_file" not in source:
            out.append(ctx.F("log_shim_mechanism", "error", shim,
                             "log.py does not call Evennia's `logger.log_file` — that is the "
                             "mechanism that puts lines in the instance's LOG_DIR"))
        if not re.search(r"""["'][\w.-]+\.log["']""", source):
            out.append(ctx.F("log_shim_filename", "warn", shim,
                             "log.py names no `<library>.log` file — lines would land in the "
                             "main server log rather than one of the library's own"))
        if "ImportError" not in source:
            out.append(ctx.F("log_shim_fallback", "warn", shim,
                             "log.py does not handle ImportError — the shim must be a silent "
                             "no-op outside an Evennia engine, so tests need no log directory"))
        if not ("format_exc" in source and "NoneType: None" in source):
            out.append(ctx.F("log_shim_trace", "warn", shim,
                             "log.py does not both call `traceback.format_exc()` and suppress the "
                             "`NoneType: None` it returns outside an except block — without the "
                             "suppression every trace=True call from outside one logs noise"))
        if SHIM_TIMESTAMP.search(source):
            out.append(ctx.F("log_shim_timestamp", "warn", shim,
                             "log.py stamps a time of its own — `logger.log_file` already "
                             "prefixes one in UTC, so a second stamps every line twice and the "
                             "file stops reading against server.log"))
        out += _check_shim_interface(ctx, shim, source)

    init = ctx.pkg / "__init__.py"
    if init.exists():
        tree = _parse(init)
        if tree is not None and any(
                isinstance(n, ast.ImportFrom) and n.module == "log" and n.level
                for n in tree.body):
            out.append(ctx.F("log_shim_exported", "warn", init,
                             "__init__.py re-exports the log shim — it is internal, and a "
                             "consumer importing it depends on something the standard does not "
                             "offer them"))

    stdlib = [f for f in sorted(ctx.pkg.rglob("*.py"))
              if f.name not in ("log.py", "tests.py")
              and not (SPDX_SKIP_DIRS & set(f.parts))
              and "logging.getLogger" in f.read_text(encoding="utf-8", errors="replace")]
    if stdlib:
        shown = ", ".join(rel(f, ctx.root) for f in stdlib[:6])
        more = f" (+{len(stdlib) - 6} more)" if len(stdlib) > 6 else ""
        out.append(ctx.F("stdlib_logging", "warn", ctx.pkg,
                         f"stdlib logging.getLogger used outside the shim: {shown}{more} — "
                         "with no handler configured those records reach nobody"))
    return out


def check_memory_surface(ctx):
    mem = ctx.libdir / ".claude" / "memory"
    if not mem.exists():
        return []
    return [ctx.F("forbidden_memory", "warn", mem,
                  "library carries its own memory surface — memory is a project-level "
                  "concern held once, at the umbrella")]


def check_pyproject(ctx):
    if ctx.pyproject_error:
        return [ctx.F("pyproject_unparseable", "error", ctx.pyproject_path,
                      f"could not parse pyproject.toml: {ctx.pyproject_error}")]
    if ctx.pyproject is None:
        return []  # absence already reported by check_root_files
    out = []
    proj = ctx.pyproject.get("project", {})
    if proj.get("name") != ctx.name:
        out.append(ctx.F("pyproject_name", "error", ctx.pyproject_path,
                         f"[project] name '{proj.get('name')}' should match the repo dir '{ctx.name}'"))
    lic = proj.get("license")
    lic_text = lic.get("text") if isinstance(lic, dict) else lic
    if lic_text != "BSD-3-Clause":
        out.append(ctx.F("license", "error", ctx.pyproject_path,
                         f"license should be BSD-3-Clause, found {lic_text!r}"))
    rpy = proj.get("requires-python")
    if not rpy:
        out.append(ctx.F("requires_python", "warn", ctx.pyproject_path,
                         "missing requires-python (should be >=3.10)"))
    else:
        m = re.search(r">=\s*3\.(\d+)", rpy)
        if not m or int(m.group(1)) < 10:
            out.append(ctx.F("requires_python", "warn", ctx.pyproject_path,
                             f"requires-python should allow >=3.10, found {rpy!r}"))
    if "build-system" not in ctx.pyproject:
        out.append(ctx.F("build_system", "warn", ctx.pyproject_path, "missing [build-system] table"))
    where = (ctx.pyproject.get("tool", {}).get("setuptools", {})
             .get("packages", {}).get("find", {}).get("where"))
    if where != ["src"]:
        out.append(ctx.F("packages_where", "warn", ctx.pyproject_path,
                         f'[tool.setuptools.packages.find] where should be ["src"], found {where!r}'))
    return out


CHECKS = [
    check_root_files, check_docs, check_test_plan, check_src_layout, check_naming,
    check_spdx, check_tests_dir, check_logging, check_constants, check_claude_md,
    check_interoperability, check_installing, check_settings_access, check_boot_validation, check_evennia_imports,
    check_object_state, check_boot_side_effects, check_memory_surface, check_pyproject,
]


def check_library(libdir: Path, root: Path):
    ctx = LibContext(libdir, root)
    return [f for chk in CHECKS for f in chk(ctx)]


# --- discovery + driver ------------------------------------------------------
def discover(root: Path, scope):
    libdir = root / LIBRARIES_DIR
    if not libdir.is_dir():
        return []
    libs = [d for d in sorted(libdir.iterdir())
            if d.is_dir() and (d / "pyproject.toml").exists()]
    if scope:
        wanted = {s.rstrip("/").split("/")[-1] for s in scope}
        libs = [d for d in libs if d.name in wanted]
    return libs


def lint(root: Path, scope):
    libs = discover(root, scope)
    findings = [f for lib in libs for f in check_library(lib, root)]
    return findings, [l.name for l in libs]


# --- output ------------------------------------------------------------------
SEV_ORDER = {"error": 0, "warn": 1}


def render_human(findings, libs):
    out = []
    by_lib = {name: [] for name in libs}
    for f in findings:
        by_lib.setdefault(f.library, []).append(f)
    for name in libs:
        group = sorted(by_lib.get(name, []), key=lambda f: (SEV_ORDER[f.severity], f.check))
        e = sum(f.severity == "error" for f in group)
        w = sum(f.severity == "warn" for f in group)
        status = "OK" if not group else f"{e} error, {w} warn"
        out.append(f"\n{name} — {status}")
        out.append("-" * (len(name) + len(status) + 3))
        for f in group:
            out.append(f"  [{f.severity}] {f.check}: {f.message}")
            out.append(f"      {f.path}")
    total_e = sum(f.severity == "error" for f in findings)
    total_w = sum(f.severity == "warn" for f in findings)
    out.append(f"\nChecked {len(libs)} librar{'y' if len(libs) == 1 else 'ies'}: "
               f"{total_e} error, {total_w} warn.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic FCM library-standards linter.")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("scope", nargs="*", help="optional library names to restrict the check")
    ap.add_argument("--json", action="store_true", help="emit JSON findings")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero on warnings too (default: errors only)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    findings, libs = lint(root, args.scope)

    if args.json:
        print(json.dumps({
            "findings": [f.as_dict() for f in
                         sorted(findings, key=lambda f: (f.library, SEV_ORDER[f.severity], f.check))],
            "summary": {
                "libraries": libs,
                "errors": sum(f.severity == "error" for f in findings),
                "warnings": sum(f.severity == "warn" for f in findings),
            },
        }, indent=2))
    else:
        print(render_human(findings, libs))

    fail = any(f.severity == "error" for f in findings)
    if args.strict:
        fail = fail or any(f.severity == "warn" for f in findings)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
