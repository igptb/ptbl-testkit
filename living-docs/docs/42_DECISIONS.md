# Decisions

Last updated: 2026-01-26

Scope: Append-only log of significant decisions for PTBL TestKit and the PTBL validator toolchain. This is the place to record "we decided X, not Y, because Z" so humans and LLMs do not re-open settled choices. This doc does NOT duplicate detailed specs or contracts. It links to the owning docs.

## If you only read one thing
- This file is append-only. Newest entries go at the top.
- Only record decisions that change architecture, contracts, rules, or long-term workflow.
- Each entry must include: date, decision, rationale, alternatives considered, and the docs it impacts.
- If a decision changes a contract, update the contract doc and reference it here.

## Canon links
- Status: `docs/00_STATUS.md`
- Routing guide: `docs/01_ROUTING_GUIDE.md`
- Architecture: `docs/30_ARCHITECTURE.md`
- Rust migration plan: `docs/32_RUST_MIGRATION_PLAN.md`
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- Lint and meta tests: `docs/21_LINT_AND_META_TESTS.md`

---

## Template for a new decision (copy-paste)

### DEC-YYYY-MM-DD-<short_slug>
Date: YYYY-MM-DD  
Status: Accepted | Rejected | Superseded  
Decision: <one sentence>  

Context
- <what problem were we solving?>

Rationale
- <why this decision?>

Alternatives considered
- A) <option>
- B) <option>

Consequences
- <what this enables or constrains>
- <follow-up work, if any>

Impacted docs
- `docs/..`
- `docs/..`

---

## Decision log (newest first)

### DEC-2026-01-26-doc_headers_and_logs
Date: 2026-01-26  
Status: Accepted  
Decision: All living docs must use a standard header block and an append-only Update log with newest entries at the top.

Context
- We need docs that are easy for humans and LLMs to navigate, and hard to drift.

Rationale
- A consistent header makes it trivial to orient in any file.
- Newest-first logs make current changes visible without scrolling.

Alternatives considered
- A) No standard template, let authors choose
- B) Update logs oldest-first

Consequences
- Every new doc and edit follows the same structure.
- Docs remain comparable and easy to diff.

Impacted docs
- `docs/00_STATUS.md`
- `TASKS.md`
- All files under `docs/`

### DEC-2026-01-26-contracts_are_the_guardrails
Date: 2026-01-26  
Status: Accepted  
Decision: Contracts are the source of truth, and migrations or refactors must preserve contract outputs unless explicitly changed.

Context
- We are planning a Rust migration and long-term evolution of the validator.

Rationale
- PTBL’s value depends on determinism and stable outputs.
- Snapshots and contracts prevent accidental regressions.

Alternatives considered
- A) Allow behavior to drift during migration
- B) Treat implementation as the source of truth

Consequences
- Contract docs and regression snapshots become merge gates as they mature.
- Any intentional contract change must be documented and versioned.

Impacted docs
- `docs/11_DIAGNOSTICS_CONTRACT.md`
- `docs/12_CLI_CONTRACT.md`
- `docs/23_REGRESSION_SNAPSHOTS.md`
- `docs/32_RUST_MIGRATION_PLAN.md`
