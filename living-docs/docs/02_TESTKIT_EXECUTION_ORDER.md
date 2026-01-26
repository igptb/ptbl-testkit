# PTBL TestKit v3.6: Phased Execution Order

Last updated: 2026-01-24

Scope: Sequences the full TestKit v3 checklist into execution phases. No checklist items are removed. This doc is the front door for the execution plan and links to canonical contracts and specs.

## If you only read one thing
- Single front door: the same loader, resolver, validator, canonicalizer, indexer, and changeset engine are used by CLI, CI, editors, and agents.
- Determinism by default: stable rule IDs, stable canonical output, stable index output, stable resolution behavior.
- Three-tier validation: schema then semantic then policy. Interactive mode runs schema + semantic. Commit mode runs all three tiers.
- Phase 4 work is executed in batches and is not merge-blocking until 20 goldens exist.
- Performance budgets and dogfooding are first-class. See `./50_PERFORMANCE_BUDGETS.md` and `./31_DOGFOODING_PLAN.md`.

## Update log
- 2026-01-24: Converted from `exports/docx/PTBL_TestKit_v3_6_Phased_Execution_Order.docx` (document date 2026-01-21). Added Phase 4 batch plan and tracking pointers.

## Phase 4 track: batch plan
This section is the practical plan you are executing to reach "100+ feels real" without chaos.
Track completion in `./00_STATUS.md`.

### Task 1: Golden workspace corpus
Goal: reach 10 archetypes x 2 sizes eventually, in batches.
- 1A: 4 archetypes x 2 sizes (8 goldens total)
  - Archetypes: SaaS CRUD + auth + billing; Data platform ingestion + transform + analytics; Security ops detections + playbooks + actions; Integrations-heavy app
  - Sizes: small (3 to 6 files), medium (15 to 25 files)
  - Deliverables: `tests/goldens/<archetype>/<size>/workspace/...`, `tests/test_goldens_validate.py`
- 1B: +3 archetypes x 2 sizes (6 more, total 14)
- 1C: +3 archetypes x 2 sizes (6 more, total 20)
Only after 20 goldens exist do we consider making any of this merge-blocking.

### Task 2: Negative suite expansion to 150+
- 2A: Convert existing near-misses into formal negative tree
- 2B: Add 30 negatives (15 schema, 10 semantic, 5 policy)
- 2C: Add 40 more
- 2D: Add 40 more aimed at hard edges

### Task 3: Variant coverage reporting
- 3A: reporting-only `coverage.json` (deterministic)
- 3B: `coverage.md` from `coverage.json`
- 3C: optional enforcement later

### Task 4: Changeset validation stress pack
- 4A: 20 fixtures (validate-only)
- 4B: +20 (total 40)
- 4C: +20 (total 60)

### Task 5: Ambiguity hunts evidence
- 5A: add 10 ambiguity pairs (reach 25)
- 5B: intent fingerprint evidence report (test-only)
- 5C: add 5 more pairs (reach 30)

### Task 6: Real LLM failure pipeline
- 6A: skeleton loader and structure
- 6B: add 10
- 6C: add 20
