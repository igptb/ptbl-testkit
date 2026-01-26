Title: Dogfooding Plan
Last updated: 2026-01-26
Scope: How we will dogfood PTBL and the TestKit by using the same blueprint workflow we expect users and LLM agents to follow. This doc covers process, guardrails, and milestones. It does NOT define product requirements for Prompt.Build itself.

If you only read one thing, read this section:
- Dogfooding means: PTBL is the source of truth, the validator is the gate, and changesets are the only allowed edit primitive once a workspace is created.
- Start with a small, boring target: keep dogfooding about determinism and workflow, not features.
- Every dogfood run must produce reproducible artifacts (validator outputs, reports, and snapshots) and must be runnable from a clean checkout.
- The goal is to generate evidence, not opinions: byte-stable outputs, stable rule IDs, and a clear audit trail.

Update log (append-only):
- 2026-01-26: Initial version (living doc).

---

# Dogfooding Plan

## Why dogfood
Dogfooding is how we prove the core promise: an LLM can make changes safely because the blueprint format is unambiguous and the engine is deterministic.

It also forces early answers to questions we will otherwise postpone forever:
- What is the smallest “real” workspace we can validate end to end?
- What contracts must exist for an automated agent loop to work reliably?
- Where does ambiguity or drift show up in practice?

## What we will dogfood
We dogfood two things, in this order.

1) The blueprint workflow
- Prompt or edit a PTBL workspace.
- Validate.
- If invalid, fix via a changeset.
- Revalidate until green.
- Produce artifacts (reports, snapshots).

2) The repo-operational workflow
- Small batches.
- Update living docs after each batch.
- Keep checks green on PRs.

## Principles and guardrails
### Determinism-first
- The same input workspace must yield the same validator outputs and reports.
- If output changes, it must be explained by a committed change to inputs, schemas, rules, or tooling version.

### Changesets are the only mutation mechanism
Once a workspace exists, any edit should be representable as a changeset.
- Humans may edit files manually during development, but the “official” edit path we test is changeset apply.
- This keeps the workflow aligned with eventual agent automation.

### No silent widening of schema
- Do not “make it pass” by loosening schemas.
- If a real need appears, capture it as evidence (fixtures, ambiguity case, rule), then decide via the Decisions log.

### Evidence artifacts are first-class
Every dogfood batch should add or refresh at least one of:
- regression snapshots
- coverage reports
- ambiguity reports
- fixture packs (goldens, negatives, changesets)

## Milestones
### Milestone A: Blueprint loop is boring and reliable
Definition of done:
- A small workspace can be validated, fixed, and revalidated via changesets.
- Diagnostics are stable and actionable.

Artifacts expected:
- deterministic validator JSON output
- snapshots that lock those bytes

### Milestone B: Dogfood workspace corpus exists
Definition of done:
- A set of “golden” workspaces exists and is stable.
- The corpus exercises key schema variants without becoming merge-blocking too early.

Artifacts expected:
- goldens under `tests/goldens/`
- a test that validates all goldens

### Milestone C: Evidence pipeline is automatic
Definition of done:
- Reports generate in CI and are deterministic.
- Drift is visible immediately.

Artifacts expected:
- `tests/_out/*.json` and `tests/_out/*.md` (or `artifacts/*`), generated and verified by tests

## Concrete dogfood targets
Start with these targets, in increasing complexity.

1) TestKit itself, as a “product”
- The living docs are already a dogfood surface area.
- We treat docs as part of the system contract.

2) A minimal PTBL workspace that models the validator tool
- A workspace that describes the validator package and its expected contracts.
- The output is not a compiled product, it is validation evidence plus docs.

3) Incrementally add “platform slices”
Examples:
- CLI surface area
- diagnostics and fix actions
- import resolver behavior

The point is to grow complexity without breaking determinism.

## How this connects to other living docs
- Architecture boundaries: see `docs/30_ARCHITECTURE.md`
- Changeset rules: see `docs/13_CHANGESET_SEMANTICS.md`
- Diagnostics contract: see `docs/11_DIAGNOSTICS_CONTRACT.md`
- Fix actions contract: see `docs/15_FIX_ACTIONS_SPEC.md`
- Regression snapshots: see `docs/23_REGRESSION_SNAPSHOTS.md`
- Schema canon: see `docs/20_SCHEMA_PACK.md`

## How to run dogfood loops locally
A “dogfood loop” is one of these patterns.

1) Validate-only loop
- edit workspace
- run validator
- confirm deterministic outputs

2) Auto-repair loop
- generate a changeset for the error
- apply changeset
- revalidate
- confirm fix actions are correct and minimal

Keep each loop small enough that it can be reviewed and reverted easily.
