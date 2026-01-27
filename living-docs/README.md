# PTBL Living Docs

Last updated: 2026-01-27

Scope: This folder stores the living Markdown docs that preserve context for humans and LLMs. It does NOT contain the validator code itself. Living docs are updated in small, reviewable commits.

## If you only read one thing
- Start here: `docs/01_ROUTING_GUIDE.md`
- Always-current snapshot: `docs/00_STATUS.md`
- TestKit front door: `docs/02_TESTKIT_EXECUTION_ORDER.md`
- Rust migration checklist: `docs/33_RUST_MIGRATION_TASKS.md`
- Every doc starts with the standard header block and an append-only Update log.
- Phase 4 batch progress (including validator mini-batches) is tracked in `docs/00_STATUS.md`.

## Update log
- 2026-01-27: Added docs/33_RUST_MIGRATION_TASKS.md and linked it from the front door as the Rust execution checklist.
- 2026-01-26: Clarified that Phase 4 mini-batch progress is tracked in docs/00_STATUS.md.
- 2026-01-24: Refreshed Task 1 outputs and added Phase 4 batch tracking pointers to the TestKit front door.

## Repo map
- `docs/`: living docs (canonical)
- `exports/docx/`: source DOCX exports (reference only)
- `templates/`: copy-paste templates and helper scripts

## Conventions
- Numbered filenames are for stable navigation.
- Use relative links.
- Keep docs short and link outward. Avoid giant all-in-one files.
