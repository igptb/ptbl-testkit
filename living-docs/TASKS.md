# Living Docs Task List

Last updated: 2026-01-27

Scope: Track creation and conversion of the living Markdown docs. This list is the single checklist to tick off per doc. It does NOT contain the doc content itself.

## If you only read one thing
- Do not start a doc without the standard header block and Update log.
- Keep `docs/` flat.
- Every doc must link to neighbors (at least: "see also" links).
- Prefer a short front door doc that links outward over a giant all-in-one file.

## Update log
- 2026-01-27: Added docs/33_RUST_MIGRATION_TASKS.md (Rust migration execution checklist) and marked it complete.
- 2026-01-26: Updated docs/00_STATUS.md and docs/02_TESTKIT_EXECUTION_ORDER.md to reflect validator mini-batch progress through v10_4_c.
- 2026-01-26: Added docs/42_DECISIONS.md and marked it complete.
- 2026-01-26: Added docs/41_DEV_WORKFLOW.md (batch discipline and no-regression rules) and marked it complete.
- 2026-01-26: Added docs/40_GITHUB_SETUP.md and marked it complete.
- 2026-01-26: Added docs/32_RUST_MIGRATION_PLAN.md and marked it complete.
- 2026-01-26: Added docs/31_DOGFOODING_PLAN.md and marked it complete.
- 2026-01-26: Added docs/15_FIX_ACTIONS_SPEC.md and marked it complete.
- 2026-01-26: Added docs/30_ARCHITECTURE.md and marked it complete.
- 2026-01-26: Added docs/23_REGRESSION_SNAPSHOTS.md and marked it complete.
- 2026-01-26: Added docs/22_FIXTURES_AND_GOLDENS.md and marked it complete.
- 2026-01-26: Added docs/21_LINT_AND_META_TESTS.md and marked it complete.
- 2026-01-26: Added docs/14_SEMANTIC_RULES_CATALOG.md and marked it complete.
- 2026-01-26: Added docs/13_CHANGESET_SEMANTICS.md and marked it complete.
- 2026-01-26: Added docs/12_CLI_CONTRACT.md and marked it complete.
- 2026-01-26: Added docs/11_DIAGNOSTICS_CONTRACT.md and marked it complete.
- 2026-01-24: Added `docs/10_WORKSPACE_LAYOUT_SPEC.md` and marked it complete.
- 2026-01-24: Converted core schema documentation into `docs/20_SCHEMA_PACK.md` and marked it complete.
- 2026-01-24: Added `docs/01_ROUTING_GUIDE.md` and marked it complete.
- 2026-01-24: Marked TestKit front door conversion as complete and added its split docs.

---

## 0) Repo and navigation bootstrap

- [x] Create folder tree: `docs/`, `exports/docx/`, `templates/`
- [x] Create `TASKS.md` (this file)
- [x] Create `README.md` (front door)
- [x] Create `CHANGELOG.md` (release index)
- [x] Keep `CHANGELOG-v2_6_19.md` as historical release notes (do not edit except for links)

---

## 1) Convert and split source docs

### 1.1 TestKit execution order (done)
- [x] `docs/02_TESTKIT_EXECUTION_ORDER.md` (front door, from `exports/docx/PTBL_TestKit_v3_6_Phased_Execution_Order.docx`)
  - [x] Extract Dogfooding into `docs/31_DOGFOODING_PLAN.md`
  - [x] Extract Performance Budgets into `docs/50_PERFORMANCE_BUDGETS.md`

### 1.2 Core schema documentation (schema canon)
- [x] `docs/20_SCHEMA_PACK.md` (from `exports/docx/PTBL_Core_Schema_Documentation_v2_6_19.docx`)

---

## 2) Core living docs (contracts and navigation)

- [ ] `docs/00_STATUS.md` (exists, but fill out more as we go)
- [x] `docs/01_ROUTING_GUIDE.md`
- [x] `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- [x] `docs/11_DIAGNOSTICS_CONTRACT.md`
- [x] `docs/12_CLI_CONTRACT.md`
- [x] `docs/13_CHANGESET_SEMANTICS.md`
- [x] `docs/14_SEMANTIC_RULES_CATALOG.md`
- [x] `docs/15_FIX_ACTIONS_SPEC.md`
- [x] `docs/21_LINT_AND_META_TESTS.md`
- [x] `docs/22_FIXTURES_AND_GOLDENS.md`
- [x] `docs/23_REGRESSION_SNAPSHOTS.md`
- [x] `docs/30_ARCHITECTURE.md`
- [x] `docs/31_DOGFOODING_PLAN.md` (exists)
- [x] `docs/32_RUST_MIGRATION_PLAN.md`
- [x] `docs/33_RUST_MIGRATION_TASKS.md`
- [x] `docs/40_GITHUB_SETUP.md`
- [x] `docs/41_DEV_WORKFLOW.md`
- [x] `docs/42_DECISIONS.md`

---

## 3) Optional later

- [ ] `docs/51_SECURITY_MODEL.md`
- [ ] `docs/52_CHATBOT_ORCHESTRATION_SPEC.md`
