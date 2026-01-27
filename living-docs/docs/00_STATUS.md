# Status

Last updated: 2026-01-27

Scope: Always-current snapshot of TestKit and validator progress, plus the state of the living docs.

## If you only read one thing
- TestKit v3.6 source plan says Phase 0 and Phase 1 are complete as of 2026-01-21. Phase 2 is the next milestone.
- Living docs: TestKit front door is converted to Markdown and split docs exist for budgets and dogfooding.
- Phase 4 track is executed in batches. Tick them off here as they complete.
- Schema canon: `docs/20_SCHEMA_PACK.md` is the reference for the v2.6.19 schema pack.

## Update log
- 2026-01-27: CI green for rust + python parity smoke.
- 2026-01-27: Rust scaffold hardening: cargo fmt --check and cargo clippy -D warnings are green.
- 2026-01-27: Rust migration Phase 1 underway (parity gates green; Rust workspace builds).
- 2026-01-27: Rust migration Task 0.2 completed; added rust/README.md with parity rules and manual compare steps until the parity harness is implemented.
- 2026-01-27: Rust migration Phase 0 started; Task 0.1 frozen Python parity baseline outputs (10 curated snapshots) under tests/parity_baseline/.
- 2026-01-27: Started Rust migration execution using docs/33_RUST_MIGRATION_TASKS.md. Python remains the oracle until Rust cutover; TestKit mini-batch D resumes after cutover.
- 2026-01-26: Updated Phase 4 batch tracking to reflect validator progress through v10_4_c (mini-batches A to C complete; 20 ambiguity pairs total).
- 2026-01-26: Added docs/42_DECISIONS.md (append-only decision log template + initial entries).
- 2026-01-26: Added docs/41_DEV_WORKFLOW.md (batch discipline and no-regression rules).
- 2026-01-26: Added docs/40_GITHUB_SETUP.md (GitHub guardrails and CI expectations).
- 2026-01-26: Added docs/32_RUST_MIGRATION_PLAN.md (Rust/Python ownership split and migration sequencing).
- 2026-01-26: Added docs/31_DOGFOODING_PLAN.md (dogfooding milestones and guardrails).
- 2026-01-26: Added docs/15_FIX_ACTIONS_SPEC.md (fix actions contract).
- 2026-01-26: Added docs/30_ARCHITECTURE.md (architecture map and boundaries).
- 2026-01-26: Added docs/23_REGRESSION_SNAPSHOTS.md.
- 2026-01-26: Added docs/22_FIXTURES_AND_GOLDENS.md.
- 2026-01-26: Added docs/21_LINT_AND_META_TESTS.md (lint + meta tests contracts).
- 2026-01-26: Added docs/14_SEMANTIC_RULES_CATALOG.md
- 2026-01-26: Added docs/13_CHANGESET_SEMANTICS.md (changeset semantics).
- 2026-01-26: Added docs/12_CLI_CONTRACT.md (CLI contract).
- 2026-01-26: Added docs/11_DIAGNOSTICS_CONTRACT.md (diagnostics contract).
- 2026-01-24: Created `docs/10_WORKSPACE_LAYOUT_SPEC.md` (workspace layout canon).
- 2026-01-24: Converted core schema documentation into `docs/20_SCHEMA_PACK.md` (schema canon).
- 2026-01-24: Added routing guide and updated living docs completion list.
- 2026-01-24: Updated after converting TestKit plan and adding Phase 4 batch tracking.

## TestKit execution status (from the v3.6 plan)

### Completed
- Phase 0: Repository and CI skeleton (complete 2026-01-21)
- Phase 1: Workspace loader and resolver contracts (complete 2026-01-21)

### Next milestone
- Phase 2: Validator core with rule catalog and stable diagnostics

## Phase 4 track status (batch execution plan)

These are not merge-blocking until the golden suite reaches 20.

### Task 1: Golden workspace corpus
- [x] 1A: 8 goldens (4 archetypes x 2 sizes)
- [ ] 1B: +6 goldens (3 archetypes x 2 sizes, total 14)
- [ ] 1C: +6 goldens (3 archetypes x 2 sizes, total 20)

### Task 2: Negative suite to 150+
- [ ] 2A: Convert existing near-misses into formal negative tree
- [x] 2B: Add 30 negatives (15 schema, 10 semantic, 5 policy)
- [ ] 2C: Add 40 negatives (15 schema, 15 semantic, 10 policy)
- [ ] 2D: Add 40 negatives (hard edges)

### Task 3: Variant coverage reporting
- [x] 3A: Reporting-only `coverage.json` (deterministic)
- [ ] 3B: Human-readable `coverage.md` from `coverage.json`
- [ ] 3C: Optional enforcement later (not now)

### Task 4: Changeset validation stress pack
- [x] 4A: 20 changeset fixtures (validate-only)
- [ ] 4B: +20 fixtures (total 40)
- [ ] 4C: +20 fixtures (total 60)

### Task 5: Ambiguity hunts evidence
Target: reach 25 ambiguity pairs (Task 5A) before we do any evidence-quality improvements (Mini-batch F).
- [ ] 5A: Add 10 ambiguity pairs (reach 25)
  - [x] Mini-batch A (v10_4_a): Scaffold intent fingerprint evidence pipeline + raise budget to 25
  - [x] Mini-batch B (v10_4_b): +3 ambiguity pairs (total 17)
  - [x] Mini-batch C (v10_4_c): +3 ambiguity pairs (total 20)
  - [ ] Mini-batch D (v10_4_d): +3 ambiguity pairs (total 23)
  - [ ] Mini-batch E (v10_4_e): +2 ambiguity pairs (total 25)
  - [ ] Mini-batch F (v10_4): Improve fingerprint normalization rules + final release version (no suffix)
- [x] 5B: Add intent fingerprint evidence report (test-only)
- [ ] 5C: Add 5 more ambiguity pairs (reach 30)
- Latest validator pack: ptbl_phase2_validator_v10_4_c.zip

### Task 6: Real LLM failure pipeline
- [ ] 6A: Skeleton loader and structure
- [ ] 6B: Add 10 real failures
- [ ] 6C: Add 20 more real failures

## Next batch to run
- Current focus: Rust migration execution (see docs/33_RUST_MIGRATION_TASKS.md).
- Rust migration in progress: parity harness + curated parity gates are green; Rust workspace scaffold builds. Next: Phase 1 hardening (fmt, clippy) and first real Rust parity tasks. Python validator pack remains v10_4_c. fmt + clippy are green.

## Living docs status

### Completed
- `docs/33_RUST_MIGRATION_TASKS.md`
- `docs/42_DECISIONS.md`
- `docs/41_DEV_WORKFLOW.md`
- `docs/40_GITHUB_SETUP.md`
- `docs/32_RUST_MIGRATION_PLAN.md`
- `docs/31_DOGFOODING_PLAN.md`
- `docs/15_FIX_ACTIONS_SPEC.md`
- `docs/30_ARCHITECTURE.md`
- `docs/23_REGRESSION_SNAPSHOTS.md`
- `docs/22_FIXTURES_AND_GOLDENS.md`
- `docs/21_LINT_AND_META_TESTS.md`
- `docs/14_SEMANTIC_RULES_CATALOG.md`
- `docs/13_CHANGESET_SEMANTICS.md`
- `docs/12_CLI_CONTRACT.md`
- `docs/11_DIAGNOSTICS_CONTRACT.md`
- `docs/01_ROUTING_GUIDE.md`
- `docs/02_TESTKIT_EXECUTION_ORDER.md`
- `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- `docs/20_SCHEMA_PACK.md`
- `docs/31_DOGFOODING_PLAN.md`
- `docs/50_PERFORMANCE_BUDGETS.md`

### In progress
- `docs/00_STATUS.md` (this file is continuously updated)

### Next

