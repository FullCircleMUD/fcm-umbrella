# `.claude/` — infrastructure skeleton (umbrella, canonical reference)

This is the **umbrella repo's** `.claude/` — the single canonical coordination layer for the whole
FCM project. Always launch Claude from the umbrella root so this layer is authoritative; each
sub-repo's own `CLAUDE.md` and skills still load on demand as you work inside it.

## What each folder/file is for

| Path | Purpose |
|---|---|
| `settings.json` | Live, committed config — `$schema`, the `SessionStart` memory hook, and the permission profile. Travels to every machine. |
| `settings.local.json` | Machine-local overrides (holds the absolute `autoMemoryDirectory`). **Gitignored** — never committed. |
| `rules/` | Auto-firing rule files (`paths:` glob). Keep at the umbrella; globs reach sub-repo files. |
| `skills/` | Cross-project skills, always available from the umbrella. Repo-specific skills live in that sub-repo's own `.claude/skills/`. |
| `agents/` | Subagent definitions — discovered only from the launch dir, so they must live here. |
| `agent-memory/` | Committed agent working memory. |
| `agent-memory-local/` | Machine-local agent memory. **Gitignored.** |
| `output-styles/` | Output-style definitions. |
| `hooks/` | Hook scripts (e.g. `ensure-repo-memory.mjs`), wired in `settings.json`. |
| `memory/` | Portable, version-controlled Claude auto-memory (added by memory-setup). `MEMORY.md` is the index. |

## Discovery rule of thumb

Skills and `CLAUDE.md` follow you down into sub-repos; **agents, settings, rules, and memory stay at
the umbrella top.** That asymmetry is why you always launch from the umbrella.
