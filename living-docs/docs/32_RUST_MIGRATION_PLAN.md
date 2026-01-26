# Rust Migration Plan

Last updated: 2026-01-26

Scope: Defines what moves to Rust, what stays in Python, and the sequencing and success criteria for migrating PTBL’s core to Rust without breaking contracts. This doc is a plan and contract map, not an implementation guide.

## If you only read one thing
- Rust owns the deterministic, performance-critical core. Python stays as orchestration and glue.
- Do not migrate by rewriting everything. Migrate by **locking contracts** and swapping implementations behind the same interfaces.
- The validator/diagnostics outputs are contracts. Migration must preserve them byte-for-byte unless an intentional contract change is documented.
- Migration is staged: begin with loader/resolver and validation engine, then incremental planning and emitters, leaving LLM orchestration in Python.

## Canon links
- Architecture map: `docs/30_ARCHITECTURE.md`
- Workspace layout: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- CLI contract: `docs/12_CLI_CONTRACT.md`
- Semantic rules catalog: `docs/14_SEMANTIC_RULES_CATALOG.md`
- Regression snapshots: `docs/23_REGRESSION_SNAPSHOTS.md`
- Status: `docs/00_STATUS.md`

---

## 1) Migration principles

### 1.1 Preserve contracts first
Before migrating a component, confirm:
- Input expectations are documented
- Output formats are documented
- Tests exist to lock behavior (snapshots where appropriate)

### 1.2 Determinism beats features
If a migration risks nondeterminism, pause and fix determinism first. PTBL’s value prop is deterministic compilation and validation.

### 1.3 Swap behind stable interfaces
Rust replaces Python implementation behind stable entrypoints:
- CLI stays stable
- JSON output stays stable
- Rule IDs stay stable

### 1.4 Keep one source of truth for rules
Rule identifiers and rule semantics must not fork across languages. Choose one representation:
- Rust implements rules, while Python only calls Rust
- Or a shared catalog definition used to generate stubs (later)

---

## 2) Ownership split: Rust core vs Python glue

### 2.1 Rust core owns
These are the components where Rust provides correctness and performance wins, and where determinism matters most.

- Workspace loader + import resolver (file discovery, import graph, lock semantics)
- Schema + semantic + policy validation engine (including rule execution pipeline)
- IR builder + dependency graph for compilation
- Changeset apply engine (deterministic patch operations)
- Incremental rebuild planner (scoped diffs, dependency invalidation)
- Deterministic code emitters/scaffolders
- Artifact packaging (zip/tar generation, manifest emission)

### 2.2 Python owns
Python remains the control plane for developer velocity and agent orchestration.

- Orchestration and glue (CLI wrapper if helpful, task runner)
- LLM / chat orchestrator pipeline (prompting, tool selection)
- Prompt templates and policy config for agents
- Thin wrappers for Rust core (CLI calls, subprocess, or FFI later)
- Dev tooling utilities and test harness

---

## 3) Target end-state interfaces

### 3.1 Rust core entrypoints
Provide at least one stable interface:
- A Rust CLI binary that accepts workspace root + flags
- Optional: a library API for embedding

Recommended baseline:
- `ptbl-core validate <workspace> --format json`
- `ptbl-core resolve <workspace> --format json`
- `ptbl-core apply-changeset <workspace> <changeset> --dry-run --format json`

### 3.2 Python orchestration contracts
Python should treat Rust core as an external deterministic tool:
- Run Rust core
- Parse JSON outputs
- Decide next agent steps (if any)
- Never re-implement validation logic in Python once Rust is authoritative

---

## 4) Sequencing plan (phased)

### Phase A: Lock the contracts
Goal: make migration safe.

Deliverables:
- Snapshot tests that lock diagnostics JSON shape and ordering
- A small fixed corpus of fixtures/goldens used for parity checks
- A “parity runner” script that can compare Python vs Rust outputs

Exit criteria:
- Contract docs are complete enough for migration
- Parity test harness exists (even if Rust not implemented yet)

### Phase B: Loader + resolver in Rust
Goal: move the most IO-heavy deterministic step first.

Deliverables:
- Rust implementation of workspace scanning and import resolution
- JSON output of resolved graph (for debugging and determinism checks)

Exit criteria:
- Deterministic output matching Python behavior (or documented improvement)
- Performance measurable on medium workspaces

### Phase C: Schema validation in Rust
Goal: migrate schema-tier validation first.

Deliverables:
- Rust schema validator emitting diagnostics in exact contract format

Exit criteria:
- Byte-identical diagnostics for schema-tier cases (snapshots)
- No regressions on fixtures and goldens

### Phase D: Semantic + policy in Rust
Goal: migrate rule engine and catalog.

Deliverables:
- Rust rule runner using the same stable rule IDs
- Fully contract-compliant diagnostics output

Exit criteria:
- Parity on representative semantic fixtures
- Documented deltas only where previous behavior was wrong

### Phase E: Changeset apply engine + incremental planning
Goal: enable deterministic edits and fast rebuild loops.

Deliverables:
- Changeset apply engine in Rust
- Incremental rebuild planner (scope invalidation + dependency graph)

Exit criteria:
- Deterministic apply behavior validated by fixtures
- Measurable performance wins on repeated edits

### Phase F: Deterministic emitters + packaging
Goal: compilation outputs become stable and fast.

Deliverables:
- Deterministic scaffold generation and packaging
- Build artifacts reproducible across machines

Exit criteria:
- Artifact-level regression snapshots and reproducibility checks

---

## 5) Parity, testing, and regression strategy

### 5.1 Parity mode
Run the same workspace through both implementations and compare:
- Diagnostics list (normalized, then byte-stable)
- Report artifacts (coverage/ambiguity evidence), if present
- Exit codes and severity aggregation

### 5.2 Snapshot policy
Snapshots are the guardrails:
- If output is a contract, snapshot it
- If output is not a contract, do not snapshot it

See: `docs/23_REGRESSION_SNAPSHOTS.md`

---

## 6) Performance goals (practical)

This doc does not set strict budgets. It sets direction:
- Loader/resolver should scale to large workspaces without Python overhead
- Semantic validation should reduce per-file latency and improve p95 and p99
- Incremental edits should revalidate only what changed plus dependencies

If you later formalize budgets, link them here.

---

## 7) Risks and mitigations

### Risk: Two implementations diverge
Mitigation:
- Keep Rust as “source of truth” once migrated
- Keep parity tests for a while during transition

### Risk: Rule catalog drifts
Mitigation:
- Single rule ID registry
- Tests that fail on unknown or duplicated rule IDs

### Risk: Lost developer velocity
Mitigation:
- Keep Python orchestration and testing fast
- Move core first, not the whole stack

---

## Update log
- 2026-01-26: Created Rust migration plan: ownership split, target interfaces, sequencing, and parity strategy.
