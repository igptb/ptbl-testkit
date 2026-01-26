# Routing Guide

Last updated: 2026-01-24

Scope: This doc routes humans and LLMs to the correct living doc fast. It does NOT restate every spec. If you are writing or changing behavior, this guide tells you where the canonical contract lives.

## If you only read one thing
- Read order matters: start with current truth, then execution plan, then canon specs.
- Canon docs define contracts. Generated reports are derived artifacts.
- If you are unsure where a change belongs, use the "Where does this change go" table below.
- If you are debugging, follow the triage protocol. Do not jump straight into random tests.

## Read order
1) `./00_STATUS.md` (what is true right now)
2) `./02_TESTKIT_EXECUTION_ORDER.md` (what we are executing)
3) `./20_SCHEMA_PACK.md` (schema canon, once created)

## Canon vs derived
Canon docs (contracts that win conflicts):
- `./10_WORKSPACE_LAYOUT_SPEC.md`
- `./11_DIAGNOSTICS_CONTRACT.md`
- `./12_CLI_CONTRACT.md`
- `./13_CHANGESET_SEMANTICS.md`
- `./14_SEMANTIC_RULES_CATALOG.md`
- `./15_FIX_ACTIONS_SPEC.md`
- `./20_SCHEMA_PACK.md`

Derived docs (reports, evidence, generated artifacts):
- coverage reports
- ambiguity reports
- snapshot outputs
- any files under `tests/_out/` or `artifacts/`

Rule: if a derived artifact disagrees with a canon contract, update the canon doc or the generator. Do not patch around it in downstream tooling.

## Start here if
- You want to know what is done and what is next: `./00_STATUS.md`
- You want the big execution plan and phase order: `./02_TESTKIT_EXECUTION_ORDER.md`
- You want to understand the folder structure and file types: `./10_WORKSPACE_LAYOUT_SPEC.md`
- You got a validation failure and need to interpret it: `./11_DIAGNOSTICS_CONTRACT.md`
- You want to run validation locally or in CI: `./12_CLI_CONTRACT.md`
- You are editing via changesets and need exact semantics: `./13_CHANGESET_SEMANTICS.md`
- You are adding or changing a semantic rule: `./14_SEMANTIC_RULES_CATALOG.md`
- You want the fix actions vocabulary for auto repair: `./15_FIX_ACTIONS_SPEC.md`
- You need schema truth, dependencies, and allowed shapes: `./20_SCHEMA_PACK.md`
- You are working on fixtures, goldens, and how tests discover them: `./22_FIXTURES_AND_GOLDENS.md`
- You are dealing with snapshots or deterministic bytes: `./23_REGRESSION_SNAPSHOTS.md`
- You are changing repo practices, PR checklist, or how work is done: `./41_DEV_WORKFLOW.md`
- You are making a tradeoff decision that must not be lost: `./42_DECISIONS.md`

## Where does this change go
| You are changing | Update this canon doc first |
|---|---|
| File and folder layout, naming, discovery rules | `./10_WORKSPACE_LAYOUT_SPEC.md` |
| Diagnostic fields, rule_id format, json_pointer paths, locations | `./11_DIAGNOSTICS_CONTRACT.md` |
| CLI flags, exit codes, JSON output format, modes | `./12_CLI_CONTRACT.md` |
| Changeset operations, pointer rules, determinism, validation scope | `./13_CHANGESET_SEMANTICS.md` |
| Semantic rule definitions, rule IDs, rule tiers, invariants | `./14_SEMANTIC_RULES_CATALOG.md` |
| Fix action names, payload shapes, apply semantics | `./15_FIX_ACTIONS_SPEC.md` |
| Schema structure, refs, closed objects, defaults, dependency graph | `./20_SCHEMA_PACK.md` |
| Lint rules, schema meta tests, shape invariants | `./21_LINT_AND_META_TESTS.md` |
| Fixture formats, expected.json conventions, goldens layout | `./22_FIXTURES_AND_GOLDENS.md` |
| Snapshot rules, byte stability guarantees, regeneration procedure | `./23_REGRESSION_SNAPSHOTS.md` |

## Triage protocol for bugs and failures
1) Confirm current state: read `./00_STATUS.md`
2) Identify validation tier: schema vs semantic vs policy
3) Confirm the expected diagnostic shape: `./11_DIAGNOSTICS_CONTRACT.md`
4) Find the relevant rule or invariant:
   - schema problems: `./20_SCHEMA_PACK.md`
   - semantic problems: `./14_SEMANTIC_RULES_CATALOG.md`
   - policy problems: `./21_LINT_AND_META_TESTS.md` and policy section in the schema pack
5) Check the relevant fixtures and their expected outputs: `./22_FIXTURES_AND_GOLDENS.md`
6) If outputs differ by bytes, check snapshot rules: `./23_REGRESSION_SNAPSHOTS.md`
7) If you had to make a non-obvious call, record it: `./42_DECISIONS.md`

## Do not do this
- Do not add a new doc without adding a route to it here.
- Do not change diagnostics fields without updating `./11_DIAGNOSTICS_CONTRACT.md` first.
- Do not change CLI output without updating `./12_CLI_CONTRACT.md` first.
- Do not treat ambiguity evidence as canonical behavior. It is evidence only.
- Do not make Phase 4 merge blocking before the golden suite reaches 20.

## Update log
- 2026-01-24: Created routing guide for LLM-first navigation and change routing.
