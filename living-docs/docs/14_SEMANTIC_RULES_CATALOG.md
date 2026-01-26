# Semantic Rules Catalog

Last updated: 2026-01-26

Scope: Canonical catalog format and conventions for semantic validation rules. This doc defines what qualifies as a semantic rule, how rule IDs are named, what metadata a rule must expose, and how rules should be tested and documented. This doc does NOT redefine schema validity rules (schema tier) and does NOT define policy rules (policy tier).

## If you only read one thing
- Semantic rules validate meaning and integrity that JSON Schema cannot express, such as referential integrity and cross-file consistency.
- Every semantic rule must have a stable `rule_id`, a clear trigger condition, deterministic diagnostics ordering, and a minimal set of asserted fields in tests.
- Do not add “soft” semantic checks that drift. If it is subjective, it belongs in policy tier or not at all.
- The rule catalog is a contract for humans, LLMs, and CI. If it is not in the catalog, it is not a supported rule.

## Canon links
- Diagnostics contract (fields, ordering, determinism): `docs/11_DIAGNOSTICS_CONTRACT.md`
- CLI contract (exit codes, outputs): `docs/12_CLI_CONTRACT.md`
- Workspace layout and identity (UIDs, paths): `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Changeset semantics (op targeting, pointers): `docs/13_CHANGESET_SEMANTICS.md`

## Definitions

### What is a semantic rule?
A semantic rule checks correctness that is:
- Not enforceable in JSON Schema (or would be impractical to encode)
- Based on parsed meaning, relationships, or invariants across objects or files
- Deterministic, mechanical, and objective

Examples of semantic concerns:
- A referenced UID must exist in the workspace
- An import target must resolve to an actual file
- A changeset op references a file_uid that exists (unless add_file)
- A discriminator implies a required structure that schema cannot fully enforce across linked objects

### What is not semantic?
Not semantic:
- “This name is ugly” or “this is not idiomatic” (policy tier)
- Style and formatting preferences (policy tier)
- Raw schema validation such as missing required fields (schema tier)

## Rule ID conventions

### Prefixes
Use a fixed tier prefix:
- `SEM_` for semantic rules
- `SCHEMA_` for schema-level rules (usually emitted by schema validator layer)
- `POL_` for policy rules

### Naming
- IDs must be stable and never reused for a different meaning.
- Use uppercase snake case with a short noun phrase.
- Prefer a single “primary failure” meaning per rule.

Good:
- `SEM_IMPORT_TARGET_EXISTS`
- `SEM_CHANGESET_REFERENCES_VALID`

Avoid:
- Overloaded names like `SEM_VALIDATION_ERROR`
- Versioned IDs like `SEM_IMPORT_TARGET_EXISTS_V2`

### Stability policy
- Once shipped, `rule_id` meaning is immutable.
- If meaning must change, create a new `rule_id` and deprecate the old one in this catalog.

## Required rule metadata (contract)

Every semantic rule must document:
- `rule_id`: stable ID
- `title`: short human name
- `scope`: what inputs it inspects (single file, cross-file, workspace-wide)
- `trigger`: clear condition that causes a diagnostic
- `tier`: must be semantic
- `default_severity`: recommended default
- `diagnostic_fields`: which fields are always populated (see diagnostics contract)
- `test_coverage`: where tests live and what they assert
- `fix_actions`: optional, but if present must be deterministic and safe

## Determinism requirements

### Ordering
- Rules must run in a deterministic order.
- Within a rule, discovered violations must be emitted in deterministic order.
  - Sort by `file` then `json_pointer` then `rule_id`, unless another stable ordering is explicitly documented.

### No randomness, no time
Rules must not depend on:
- Current time
- Randomness
- Non-deterministic iteration of maps without sorting

### Stable text
- Diagnostic messages must be stable.
- Avoid embedding variable data that can reorder, such as unordered set prints.

## How to add a new semantic rule

1) Assign a new `rule_id` using the conventions above.
2) Decide the minimum objective invariant you are enforcing.
3) Implement the rule with deterministic iteration and stable output.
4) Add tests:
   - Add negative fixtures that trigger the rule
   - Ensure expected assertions include at least: `rule_id`, `tier`, `file`, and `json_pointer` when applicable
5) Add a catalog entry in this doc (see template below).
6) If the rule is user-facing in CLI output, ensure CLI contract alignment.

## Testing requirements

### Fixture-based tests
For each semantic rule, prefer fixture-driven tests:
- Fixtures live under a deterministic tree such as `tests/fixtures/negative/semantic/...`
- Each case includes:
  - an input file or workspace snippet
  - `expected.json` that asserts the key diagnostic fields

Minimum assertions recommended:
- `rule_id`
- `tier`
- `severity`
- `file`
- `json_pointer` (when a precise location exists)

### Avoid fragile assertions
Avoid asserting:
- Full diagnostic message text, unless it is explicitly treated as a contract
- Exact ordering across unrelated rules, unless ordering is itself being tested

## Catalog entry template

Copy and fill this block when adding a new rule:

### <RULE_ID>
- Title: <short name>
- Tier: semantic
- Scope: <single file | cross-file | workspace-wide>
- Trigger: <objective condition that causes the diagnostic>
- Default severity: <error | warning | info>
- Diagnostic fields:
  - file: <always | when applicable>
  - json_pointer: <always | when applicable>
  - locations: <always | optional>
  - details: <optional, deterministic>
- Tests:
  - Fixtures: <path(s)>
  - Test runner: <test file(s)>
  - Assertions: <list of asserted fields>
- Fix actions:
  - <none | describe deterministic fix actions if any>

## Catalog

This catalog starts small and is expanded as rules are implemented. Add entries only when a rule exists in code or fixtures.

### SEM_CHANGESET_REFERENCES_VALID
- Title: Changeset references are valid
- Tier: semantic
- Scope: workspace-wide
- Trigger: A changeset operation references a missing file UID, an invalid JSON pointer, or a non-existent target location under the op’s rules.
- Default severity: error
- Diagnostic fields:
  - file: always (changeset file if applicable, otherwise workspace-level)
  - json_pointer: when applicable (points into changeset op location or target pointer)
  - details: optional and deterministic (op index, op type)
- Tests:
  - Fixtures: `tests/fixtures/changeset/...`
  - Test runner: `tests/test_changeset_fixtures.py`
  - Assertions: rule_id, tier, file, json_pointer, severity
- Fix actions:
  - None by default. If added later, must be deterministic and validate-only safe.

## Update log
- 2026-01-26: Created the semantic rules catalog contract and initial entry template.
