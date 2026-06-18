---
name: Upcoming — rebuild FCM world in YAML using evennia-world-builder
description: Starting 2026-05-08, FCM world content gets rebuilt as YAML driven through the evennia-world-builder library; real-world edge cases will surface library gaps to fix
type: project
originSessionId: e12138e1-0b05-4f0f-9c0c-f751f175704b
---
Starting 2026-05-08, the user is rebuilding the existing FullCircleMUD world content as YAML files consumed by the `evennia-world-builder` library at `/Users/timbaird/Documents/FCM/libraries/evennia-world-builder/`.

**Why:** the library is v0 feature-complete as of 2026-05-07 — full pipeline (Reader → Definitions → Finder → Loader → Validator → Builder) with `contents:` and `exits:` recursion, cross-file `location:` / `destination:` cross-refs (in-build map + DB tag-search fallback), file-level `incoming_exits:` registry for cross-file rebuild dependency restoration, three-pass build (rooms → exits → dependency restore), async wrap via `run_async` so long deployments don't block the reactor. 293 unit tests + multi-scenario live smoke. Now exercising it against real content.

**How to apply:**
- Real-world authoring will surface edge cases the synthetic test fixtures didn't reach. Expect gaps around: FCM-specific typeclass behaviour, scale (dozens-to-hundreds of files vs. 3 in test), authoring ergonomics at scale, `incoming_exits:` maintenance burden, integration with hooks/scripts the game expects post-build.
- Per the project's "synthetic content first" principle, when a real-content edge case bites, capture it as a new synthetic fixture in the library's tests before fixing — keeps regression coverage forever.
- The library is in `libraries/evennia-world-builder/`; the test-content repo is `libraries/evennia-world-builder-test-yaml/`. The actual FCM world content will likely live in a separate content repo (config TBD when that work begins).
- Per existing Company Scope memory, FCM is marketing-focused and game-repo changes need board approval. Library/content work is upstream of that — confirm with user if any of this work is actually expected to touch `src/game/` directly.
