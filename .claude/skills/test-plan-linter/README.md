# test-plan-linter · v1.0.0 (created 2026-08-30)

## Purpose
**One test plan, checked against the suite that covers it.** A deterministic linter that reads a plan's
case tables and the test modules those cases claim, and reports where the two disagree. It is
repo-shape agnostic by design — a caller passes a plan path and the directories holding its tests — so
any linter or test suite can use it, and a gap fixed here is fixed for every consumer. No model in the
loop: same input always gives the same findings.

The plan and the suite must agree **in both directions**: every case names a test that exists (forward),
and every test is named by a case (reverse). An uncovered case is the normal test-first in-progress
state (warn); the ways the two disagree are errors.

## Provenance — internally created
Original to FCM (not vendored). Pure Python standard library — no third-party dependencies, so it runs
anywhere Python 3.10+ does and ships complete with its own tests.

## What's in the folder
- `SKILL.md` — the model/user-facing contract: what it checks, how to run it, how to call it.
- `lint_test_plan.py` — the linter. `scan_test_plan` reads the plan, `scan_test_functions` reads the
  suite, `check_test_plan` compares them and returns `Finding` objects.
- `test-plan.md` — every case this linter covers and the test function covering it.
- `tests.py` — the suite. Stdlib `unittest`, no pytest.

## Consumers
- `library-standards-linter` — calls it for each library's `docs/test-plan.md`, passing the package and
  `tests/` directories as the test roots, and renames `test_plan_missing` to its own `missing_file`.

Import it as a sibling skill:

```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "test-plan-linter"))
import lint_test_plan as plan_linter

findings = plan_linter.check_test_plan(plan_path, test_roots, root)
```

Each `Finding` carries `check`, `severity`, `path` and `message`; `CHECK_NAMES` is the full set of
checks it can emit, and a consumer wrapping findings in its own type can rename them.

## Calibration
A test function is a `test_*` def in a `tests.py` / `test_*.py` module, found by **parsing** the module
rather than pattern-matching it — test source inside a fixture string is data, not a test. Helpers,
fixtures and `setUp` are not tests; the standalone Django test infrastructure (`test_settings.py`,
`urls.py`, `conftest.py`) is excluded by name; `migrations/` and `__pycache__/` are skipped. A module
that does not parse is skipped rather than stopping the run.

A case row carrying `[TBD` is an error — an open decision is resolved before the plan passes. A plan
that needs to write the marker without raising one escapes it with a backslash: `\[TBD]`.

## Running the tests
```bash
python .claude/skills/test-plan-linter/tests.py
```
Run it after any change to `lint_test_plan.py`. XC-03 runs the linter over this skill's own plan and
suite, so the linter is its own first consumer.
