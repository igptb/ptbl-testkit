# Living Docs Task List

Last updated: 2026-01-24

Scope: Track creation and conversion of the living Markdown docs that preserve context for LLMs and humans. This list is the single checklist to tick off per doc. It does NOT contain the doc content itself.

## If you only read one thing
- Do not start a doc without the standard header block and Update log.
- Keep docs/ flat. Root is only for README, CHANGELOG, TASKS.
- Every doc must link to its neighbors (at least: "see also" links).
- Prefer short front door docs that link outward over giant all-in-one files.

## Update log
- 2026-01-24: Created initial checklist for the living-doc set.

---

## 0) Repo and navigation bootstrap (do first)

- [x] Create folder tree: docs/, exports/docx/, templates/
- [x] Create TASKS.md (this file)
- [x] Create README.md (repo purpose + doc map + start-here link)
- [x] Create CHANGELOG.md (release index)
- [x] Create placeholder CHANGELOG-v2_6_19.md (keep existing content here)

---

## 1) Convert and split source docs (highest priority)

### 1.1 TestKit execution order (FIRST)
- [ ] docs/02_TESTKIT_EXECUTION_ORDER.md (front door, from exports/docx/PTBL_TestKit_v3_6_Phased_Execution_Order.docx)
  - [ ] Add Doc map linking to contract docs
  - [ ] Keep phase list and completion gates, but link out to canonical specs
  - [ ] Extract Dogfooding into docs/31_DOGFOODING_PLAN.md (canonical)
  - [ ] Extract Performance Budgets into docs/50_PERFORMANCE_BUDGETS.md (optional but recommended)

### 1.2 Core schema documentation (schema canon)
- [ ] docs/20_SCHEMA_PACK.md (from exports/docx/PTBL_Core_Schema_Documentation_v2_6_19.docx)

### 1.3 Release changelog indexing
- [ ] Ensure CHANGELOG.md indexes all releases and links to detailed notes
- [ ] Ensure docs/42_DECISIONS.md includes the versioning and release policy

---

## 2) Core living docs (contracts and navigation)

- [ ] docs/00_STATUS.md
- [ ] docs/01_ROUTING_GUIDE.md
- [ ] docs/10_WORKSPACE_LAYOUT_SPEC.md
- [ ] docs/11_DIAGNOSTICS_CONTRACT.md
- [ ] docs/12_CLI_CONTRACT.md
- [ ] docs/13_CHANGESET_SEMANTICS.md
- [ ] docs/14_SEMANTIC_RULES_CATALOG.md
- [ ] docs/15_FIX_ACTIONS_SPEC.md
- [ ] docs/21_LINT_AND_META_TESTS.md
- [ ] docs/22_FIXTURES_AND_GOLDENS.md
- [ ] docs/23_REGRESSION_SNAPSHOTS.md
- [ ] docs/30_ARCHITECTURE.md
- [ ] docs/31_DOGFOODING_PLAN.md
- [ ] docs/32_RUST_MIGRATION_PLAN.md
- [ ] docs/40_GITHUB_SETUP.md
- [ ] docs/41_DEV_WORKFLOW.md
- [ ] docs/42_DECISIONS.md

---

## 3) Optional later (only when the core set is stable)

- [ ] docs/50_PERFORMANCE_BUDGETS.md
- [ ] docs/51_SECURITY_MODEL.md
- [ ] docs/52_CHATBOT_ORCHESTRATION_SPEC.md
