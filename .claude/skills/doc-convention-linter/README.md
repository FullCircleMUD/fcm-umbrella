# doc-convention-linter · v1.0.0 (created 2026-06-19)

## Purpose
**The mechanical half of the FCM documentation audit.** A deterministic linter that surfaces the
*machine-decidable* documentation problems — a library with no `docs/`, a docs root with no `INDEX.md`,
broken relative links, docs missing from their `INDEX`, orphaned docs, non-kebab-case filenames,
missing H1 / summary blocks, and "document what WAS" trigger phrases. Structure is checked before its
contents, so an absent `docs/` or `INDEX.md` is reported rather than silently skipping everything under
it. No model in the loop: same input always gives the same findings. It deliberately stops where
judgment begins (surface-fit, graduation, cross-ref *quality*, legitimate "use X not Y" exceptions) —
that half belongs to the `doc-convention-auditor` agent, which consumes this linter's `--json` output.

## Provenance — internally created
Original to FCM (not vendored). Pure Python standard library — no third-party dependencies, so it runs
anywhere Python 3 does and ships complete with its own tests.

## What's in the folder
- `SKILL.md` — the model/user-facing contract: what it checks, how to run it, how to read the output.
- `lint.py` — the linter. The corpus globs, exempt filenames, and trigger phrases are constants at the
  top; each check is a `Context -> list[Finding]` function in the `CHECKS` list.
- `test-plan.md` — every case the linter commits to covering, and the test function covering it. Any
  behavioural change starts here, not in the code.
- `tests.py` — stdlib `unittest`, one class per check: every helper, every check in isolation, the
  scope filter, the CLI, and an inject/restore round-trip. Each test names its case ID in its
  docstring. Zero dependencies beyond the sibling `test-plan-linter`, imported for the self-check only.

## How it works
`lint.py` discovers the whole doc corpus, reads it once into a shared `Context`, then runs each check.
Findings carry `check`, `severity` (`error` / `warn` / `advisory`), `path`, `line`, `message`.
Scoping (a directory or a single file) narrows the *report* while analysis stays global, so corpus-wide
checks (orphaned, not-indexed, inbound links) remain correct. Exit code is non-zero when any `error`
exists, so it doubles as a git pre-commit / CI gate over the same script. Warnings and advisories never
fail the run: an advisory is a judgment call for a human or the auditor agent, and a legitimate one
("use X, not Y") can never be cleared, so gating a commit on it would only teach people to suppress it.

## Running the tests
```bash
python .claude/skills/doc-convention-linter/tests.py
```
Run it after any change to `lint.py`. The check set is data (`CHECKS`), so adding a check means adding a
case to `test-plan.md`, a function, and a test — in that order.

## Deploying
Copy the `doc-convention-linter/` folder into a project's `.claude/skills/`. Adjust the corpus globs at
the top of `lint.py` to match that project's doc layout. No dependencies beyond Python 3.
