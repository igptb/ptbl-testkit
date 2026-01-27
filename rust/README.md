# Rust Validator Migration: Parity Rules for Developers

Last updated: 2026-01-27

Scope: Developer-facing rules for the Rust validator migration. This file defines what must stay stable while we port the Python validator pack to Rust, and how to check parity task by task.

## If you only read one thing
- Python remains the oracle until Rust is feature-complete and passes parity on the curated fixture set.
- Every micro-task ends with: build OK, tests OK, parity OK for 1 to 5 fixtures tied to that task.
- Schema error wording is allowed to change in Rust. Structure and meaning must remain stable.

## Folder pointers
- Task tracker: `docs/33_RUST_MIGRATION_TASKS.md`
- Frozen Python oracle outputs: `tests/parity_baseline/`
- Current Python validator entrypoint: `python -m ptbl.cli`

## What must match between Python and Rust
These are contract requirements, not suggestions.

### A) Diagnostics structure
For each diagnostic emitted by Rust, the following fields must match Python (for the same input):
- rule_id
- tier (schema, semantic, policy)
- severity
- file path (workspace-relative, POSIX style)
- JSON pointer path formatting
- ordering of diagnostics (deterministic sort)
- truncation behavior and max limits

### B) What is allowed to differ
- Schema validation message wording may differ between Python and Rust, because different JSON Schema engines generate different text.
- Any field that is explicitly tagged as "message" in schema-tier errors may change text, but it must still point to the correct location and rule_id.

### C) Determinism rules
- Running Rust on the same workspace twice must produce byte-identical JSON output.
- Sorting must be explicit. Never rely on filesystem order, hash map order, or YAML parser iteration order.

## Parity gates for every micro-task
A task checkbox can be marked complete only if all are true:
1) `cargo build` succeeds
2) `cargo test` succeeds
3) Parity passes for the fixtures selected for that task (1 to 5 fixtures)
4) Output is deterministic across repeated runs

## How to run the frozen Python oracle outputs
The baseline outputs live under:
- `tests/parity_baseline/python/10.4+v10_4_c/`

Each fixture folder contains:
- `interactive.json`
- `commit.json`

Use these as the ground truth while Rust is incomplete.

## How to compare results before the parity harness exists
Until Task 0.3 is implemented, you can do a manual compare.

### Step 1: Run Python and capture output
Run the Python validator on the same fixture workspace and save JSON output to a temp folder.

### Step 2: Run Rust and capture output
Run the Rust CLI (once it exists) on the same fixture workspace and save JSON output to a temp folder.

### Step 3: Compare on Windows
Use `fc` for a quick byte compare:
- `fc /b rust.json python.json`

Or use PowerShell for a readable diff:
- `Compare-Object (Get-Content python.json) (Get-Content rust.json)`

If the diff is large, inspect:
- rule_id
- file path normalization
- pointer formatting
- ordering and truncation

## Notes for the upcoming parity harness (Task 0.3)
- The harness should normalize only what we allow to differ (schema message text).
- Everything else must be compared strictly.
- The harness must print the first mismatch with enough context to reproduce quickly.
