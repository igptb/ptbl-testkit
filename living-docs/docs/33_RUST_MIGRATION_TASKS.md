# Rust Migration Tasks: Python Validator Pack to Rust

Last updated: 2026-01-27

Scope: Execution checklist to migrate the PTBL Phase 2 validator pack from Python to Rust in small, reviewable steps with parity gates. This doc is the task tracker. It is not the design doc (see `docs/32_RUST_MIGRATION_PLAN.md`).

## If you only read one thing
- Python stays as the oracle until Rust is feature-complete and passes parity on the full curated suite.
- Every Rust micro-task must end with: build OK, tests OK, parity OK on 1 to 5 fixtures chosen for that task.
- We allow schema error wording to change in Rust. We do not require byte-identical schema error text.
- Schemas are loaded from disk during migration to avoid rebuild friction. Embedding can come later.
- Rust is built as a library plus a CLI wrapper so PTB can call it in-process later.
- TestKit Phase 4 mini-batches (Task 5D onward) resume after Rust cutover so outputs do not drift mid-stream.

## Decisions and answers (from the 7 questions)

### 1) Keep Python while adding Rust
Decision: keep all Python validator files in place during the migration. Rust code is added alongside. After cutover, archive Python validator code first, delete later.

### 2) Continue TestKit after migration
Decision: after Rust cutover, resume TestKit remaining tasks (Task 5 mini-batch D onward, plus everything else) using Rust as the validator.

### 3) Micro-task testing responsibility
Decision: every Rust micro-task is considered done only after it compiles and passes targeted tests and parity checks for the fixtures tied to that task.

### 4) Schema error wording parity
Decision: choose option (2). Preserve structure, IDs, paths, ordering, truncation behavior, but allow schema error message wording to change and become the new canon under a major version bump.

### 5) Architecture choices
Decisions:
- Schema error wording parity: allow new canon.
- Schema pack access: load schemas from disk during migration (optional embed later).
- Rust shape: library plus CLI wrapper.
- Parity harness: keep a temporary Python parity harness until cutover.

### 6) Tracking and doc updates
Decision: create this checklist doc and update status, README, TASKS, and the TestKit execution order doc with a Rust migration note and the gating rules.

### 7) Impact on the v2.6.19 schema pack and schema tooling scripts
Decision: the v2.6.19 JSON schema files do not change because of this migration. The schema tooling Python scripts (lint, meta tests, regression tests) remain for now. We will convert them later, as a final migration track, broken into small tasks.

## Parity gates (definition of done for any task)
For a task checkbox to be marked complete, all must be true:
- `cargo build` passes
- `cargo test` passes
- parity harness passes on the fixture set for this task (1 to 5 fixtures)
- output is deterministic across repeated runs (same inputs, same outputs)

## Repo layout target
- Python validator remains in current location during migration (oracle baseline).
- Rust lives under a new workspace folder (example: `rust/` or `crates/`).
- Schemas remain in the existing schema pack folder and are loaded from disk.

---

## Task checklist (execute one micro-task at a time)

### Phase 0: Baseline and parity harness
- [x] 0.1 Freeze a Python baseline run for a curated set of fixtures (store the JSON outputs as baseline artifacts)
	- Baseline artifacts: tests/parity_baseline/python/10.4+v10_4_c (see tests/parity_baseline/fixtures.json)
- [x] 0.2 Write `docs/33_RUST_MIGRATION_TASKS.md` parity rules section into code comments or a small `rust/README.md` for developers
	- Added: rust/README.md (developer parity rules and manual diff steps until parity harness exists)
- [x] 0.3 Implement a parity harness that runs Python and Rust validators on the same fixture and diffs normalized JSON
- [x] 0.4 Define the curated parity fixture set (start with 10, grow later)

### Phase 1: Rust workspace scaffolding and CI
- [x] 1.1 Create Rust workspace (library crate plus CLI crate)
- [x] 1.2 Add rustfmt and clippy defaults
- [x] 1.3 Add CI job for Rust (build, test, fmt, clippy)
- [ ] 1.4 Add a single command to run Rust validator locally (document it)

### Phase 2: Diagnostics contract and determinism utilities
- [ ] 2.1 Port diagnostics data model (structs) and JSON serialization
- [ ] 2.2 Port JSON pointer helpers
- [ ] 2.3 Implement deterministic ordering for diagnostics and lists
- [ ] 2.4 Implement truncation and max diagnostics behavior

### Phase 3: Workspace scanning and path normalization
- [ ] 3.1 Port workspace YAML discovery and ignore rules
- [ ] 3.2 Normalize paths to workspace-relative POSIX style
- [ ] 3.3 Implement workspace fingerprint (match baseline or define new stable algorithm and document it)

### Phase 4: YAML loading and safety checks
- [ ] 4.1 BOM detection and decode behavior
- [ ] 4.2 YAML safety scan (aliases, merges, tags, depth, size limits) with diagnostics
- [ ] 4.3 Parse YAML into a generic value form used by schema validation and pointers
- [ ] 4.4 Multi-document detection behavior
- [ ] 4.5 Alias usage signal behavior

### Phase 5: Schema pack access, schema detection, schema validation
- [ ] 5.1 Load schema pack from disk and validate all JSON schema files load cleanly
- [ ] 5.2 Build schema `$id` index
- [ ] 5.3 Port schema detection logic and parity-test it
- [ ] 5.4 Implement unknown schema diagnostic
- [ ] 5.5 Implement ambiguous kind diagnostic
- [ ] 5.6 Implement schema validation using a Rust JSON Schema engine and normalize results to the diagnostics contract

### Phase 6: Validator pipeline wiring (schema-only first)
- [ ] 6.1 Implement Rust pipeline: load docs then schema validate
- [ ] 6.2 Expose schema-only CLI command with stable JSON output
- [ ] 6.3 Implement interactive mode gate (schema + semantic)
- [ ] 6.4 Implement commit mode gate (schema + semantic + policy)

### Phase 7: Rule engine and rule catalog
- [ ] 7.1 Port rule metadata and rule trait interface (stable rule_id enforcement)
- [ ] 7.2 Port rule catalog builder and tier grouping
- [ ] 7.3 Parity-test rule catalog enumeration (IDs, tiers, deterministic order)

### Phase 8: Port semantic rules (one rule per task)
- [ ] 8.1 SEM_PTBL_VERSION_MISMATCH
- [ ] 8.2 SEM_UID_DUPLICATE
- [ ] 8.3 SEM_MODULE_NAME_UID_CONSISTENCY
- [ ] 8.4 SEM_APP_UID_MISMATCH
- [ ] 8.5 SEM_APP_NAME_UID_CONSISTENCY
- [ ] 8.6 SEM_APP_REQUIRES_IMPORTS
- [ ] 8.7 SEM_IMPORT_REF_FORMAT
- [ ] 8.8 SEM_IMPORT_ALIAS_DUPLICATE
- [ ] 8.9 SEM_IMPORT_LOCAL_NOT_FOUND
- [ ] 8.10 SEM_IMPORT_CYCLE
- [ ] 8.11 SEM_ENUM_REF_NOT_FOUND
- [ ] 8.12 SEM_LOCK_VERSION_MISMATCH
- [ ] 8.13 SEM_LOCK_MANIFEST_VERSION_SYNC
- [ ] 8.14 SEM_CHANGESET_OP_SHAPE_INVALID
- [ ] 8.15 SEM_CHANGESET_REFERENCES_VALID
- [ ] 8.16 SEM_CHANGESET_OVERLAPPING_OPS
- [ ] 8.17 SEM_YAML_MULTI_DOCUMENT
- [ ] 8.18 SEM_YAML_ALIAS_USED

### Phase 9: Port policy rules (one rule per task)
- [ ] 9.1 POL_MISSING_OWNER
- [ ] 9.2 POL_GIT_UNPINNED
- [ ] 9.3 POL_INTEGRITY_MISSING
- [ ] 9.4 POL_LOCK_STALE
- [ ] 9.5 POL_DEPRECATED_USAGE

### Phase 10: Repair engine (fix actions) in Rust
- [ ] 10.1 Port FixAction parsing and deterministic grouping
- [ ] 10.2 Implement JSON pointer navigation and mutation utilities
- [ ] 10.3 Implement replace op
- [ ] 10.4 Implement add op
- [ ] 10.5 Implement remove op
- [ ] 10.6 Implement rename_key op
- [ ] 10.7 Implement move op (or explicitly keep unimplemented and document why)
- [ ] 10.8 Deterministic YAML write behavior
- [ ] 10.9 End-to-end repair loop test (validate, apply fixes, validate again)

### Phase 11: Reports (coverage and ambiguity evidence)
- [ ] 11.1 Port coverage.json generator
- [ ] 11.2 Port coverage.md generator
- [ ] 11.3 Port ambiguity evidence report generator and tests

### Phase 12: Cutover to Rust and archive Python validator
- [ ] 12.1 Expand parity harness to the full curated suite and pass
- [ ] 12.2 Make Rust CLI the primary validator entry point
- [ ] 12.3 Archive Python validator code (keep for a short grace period)
- [ ] 12.4 Remove Python validator after stable cutover
- [ ] 12.5 Resume TestKit Phase 4 mini-batches starting at Task 5 mini-batch D using Rust

### Phase 13: Post-cutover track, schema tooling scripts (later)
- [ ] 13.1 Port schema pack loader and `$id` indexer to Rust
- [ ] 13.2 Port lint rule framework and deterministic ordering
- [ ] 13.3 Port first 3 to 5 lint rules
- [ ] 13.4 Port meta tests runner
- [ ] 13.5 Port regression snapshot generator
- [ ] 13.6 Add CI gates for Rust tooling
- [ ] 13.7 Archive and then remove Python tooling scripts

## Update log
- 2026-01-27: Completed 1.3 (GitHub Actions rust + python-parity-smoke green).
- 2026-01-27: Completed 1.2 by passing cargo fmt --check and cargo clippy -D warnings on the Rust workspace.
- 2026-01-27: Completed 0.3 and 0.4 (parity harness smoke green; curated set fixture roots present on disk).
- 2026-01-27: Completed 1.1 (Rust workspace builds and cargo test is green).
- 2026-01-27: Completed Task 0.2 by adding rust/README.md (developer-facing parity rules for Rust migration).
- 2026-01-27: Completed Task 0.1 by freezing Python parity baseline outputs for 10 curated snapshot fixtures under tests/parity_baseline/.
- 2026-01-27: Created this execution checklist and locked decisions for Rust migration gates and packaging shape.