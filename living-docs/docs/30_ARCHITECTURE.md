# Architecture

Last updated: 2026-01-26

Scope: High-level architecture map for the PTBL TestKit and validator stack. This doc defines component boundaries, data flow, and what is considered a contract surface. It does NOT define schema details, individual rules, or CLI flags in depth.

## If you only read one thing
- The system is built around a single principle: **deterministic inputs produce deterministic outputs**.
- Validation is layered and ordered: **loader/resolver -> schema -> semantic -> policy**. Earlier layers must be clean and predictable.
- Outputs are contracts: **diagnostics JSON**, optional **fix_actions**, and deterministic **reports** (coverage, ambiguity evidence).
- Everything else is implementation detail. If it is not documented as a contract, it can change.

## Canon links
- Routing guide: `docs/01_ROUTING_GUIDE.md`
- Workspace layout: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- CLI contract: `docs/12_CLI_CONTRACT.md`
- Changeset semantics: `docs/13_CHANGESET_SEMANTICS.md`
- Semantic rules catalog: `docs/14_SEMANTIC_RULES_CATALOG.md`
- Lint and meta tests: `docs/21_LINT_AND_META_TESTS.md`
- Fixtures and goldens: `docs/22_FIXTURES_AND_GOLDENS.md`
- Regression snapshots: `docs/23_REGRESSION_SNAPSHOTS.md`
- Schema pack canon: `docs/20_SCHEMA_PACK.md`
- Status: `docs/00_STATUS.md`

---

## System goal

Given a workspace (a set of PTBL manifests and related files), the system must:
1) Load and resolve the workspace deterministically
2) Validate it in ordered tiers
3) Emit stable diagnostics and deterministic reports
4) Optionally suggest deterministic fix actions (evidence only, unless explicitly contract-bound)

---

## Inputs and outputs

### Inputs
- Workspace root directory (see `docs/10_WORKSPACE_LAYOUT_SPEC.md`)
- PTBL schema pack (v2.6.19 canon, see `docs/20_SCHEMA_PACK.md`)
- Optional: changeset file (see `docs/13_CHANGESET_SEMANTICS.md`)
- Optional: policy config (if policy tier is enabled)

### Primary outputs (contract surfaces)
- Diagnostics JSON list (see `docs/11_DIAGNOSTICS_CONTRACT.md`)
- Deterministic reports (examples):
  - Variant coverage report
  - Ambiguity evidence report
- Regression snapshots (tests only, see `docs/23_REGRESSION_SNAPSHOTS.md`)

### Secondary outputs (not always contract-bound)
- Human-readable CLI output (only stable if declared stable in `docs/12_CLI_CONTRACT.md`)
- Developer debug logs (never treated as contract)

---

## Component map

This section names the components and defines their responsibilities.

### 1) Workspace loader
Responsibility:
- Discover workspace files
- Read manifest text
- Produce an internal representation for validation

Hard requirements:
- Deterministic file discovery and ordering
- No implicit environment dependencies

See: `docs/10_WORKSPACE_LAYOUT_SPEC.md`

### 2) Import resolver
Responsibility:
- Resolve import references to concrete files
- Enforce import rules and boundaries
- Provide a stable resolved workspace graph

Hard requirements:
- Deterministic resolution order
- Stable error reporting for missing targets and cycles

### 3) Schema validator (tier: schema)
Responsibility:
- Validate each document against the correct JSON schema
- Report schema failures in a stable, contract-compliant way

Hard requirements:
- Correct schema selection per document type
- Stable JSON pointer reporting
- No “best effort” coercion

See: `docs/20_SCHEMA_PACK.md`, `docs/11_DIAGNOSTICS_CONTRACT.md`

### 4) Semantic validator (tier: semantic)
Responsibility:
- Validate cross-field and cross-file meaning that JSON Schema does not cover
- Enforce reference integrity, identity rules, determinism rules, and invariants

Hard requirements:
- Rules are named and cataloged
- Rule IDs are stable and never recycled

See: `docs/14_SEMANTIC_RULES_CATALOG.md`

### 5) Policy validator (tier: policy)
Responsibility:
- Enforce deployment, security, and operational policy constraints that are environment or org specific

Hard requirements:
- Clear separation from semantic tier
- Explicit toggles (policy is not silently “always on”)

### 6) Diagnostics builder
Responsibility:
- Convert validator findings into a stable diagnostics list
- Apply stable sorting and stable formatting rules

Hard requirements:
- Output must comply with the diagnostics contract
- Deterministic ordering and serialization

See: `docs/11_DIAGNOSTICS_CONTRACT.md`

### 7) Fix actions (optional contract)
Responsibility:
- Provide structured “next edits” that an agent or tool can apply
- Only treated as a contract if documented in `docs/15_FIX_ACTIONS_SPEC.md`

Hard requirements:
- No free-form strings as the primary mechanism
- Deterministic and patch-applicable structure

See: `docs/15_FIX_ACTIONS_SPEC.md` (to be written)

### 8) Deterministic report generators (tests and evidence)
Responsibility:
- Produce deterministic reports from fixtures and runs
- Support coverage tracking and ambiguity evidence

Hard requirements:
- Deterministic bytes
- Reproducible in CI

See: `docs/21_LINT_AND_META_TESTS.md`, `docs/23_REGRESSION_SNAPSHOTS.md`

---

## End-to-end data flow

High-level flow:

1) CLI entrypoint receives a workspace root
2) Loader reads and indexes files
3) Resolver builds a resolved workspace graph
4) Schema tier validates each document
5) Semantic tier validates cross-document invariants
6) Policy tier validates organization constraints (if enabled)
7) Diagnostics builder emits stable diagnostics JSON
8) Optional: report generators emit deterministic reports
9) Tests compare outputs to snapshots or expected JSON

---

## Determinism boundaries

To keep determinism real:
- No nondeterministic sources in outputs (timestamps, machine paths, random IDs)
- Stable ordering for everything
- Stable serialization rules for JSON outputs
- Version strings are controlled and bumping versions triggers snapshot refresh

See: `docs/23_REGRESSION_SNAPSHOTS.md`

---

## Non-goals (for now)
- No runtime “canonicalizer” that rewrites user manifests automatically
- No promise that pretty CLI output is stable unless explicitly stated
- No environment-specific behavior without declaring it in the policy tier contract

---

## Future components (planned, not assumed)
These may exist later, but they are not relied on as current contracts unless linked docs exist.

- Canonicalizer (normalizes equivalent shapes)
- Changeset apply engine (not just validate)
- Incremental rebuild planner
- Deterministic code emitters and packaging

---

## Update log
- 2026-01-26: Added high-level architecture map, component boundaries, and end-to-end flow.
