# Fixtures and Goldens

Last updated: 2026-01-26

Scope: Defines the canonical layout, naming, and contracts for **test fixtures** and **golden workspaces** used by the PTBL TestKit and validator. This doc describes *what must exist on disk* and *how tests discover and assert results*. It does NOT define schema contents (see `docs/20_SCHEMA_PACK.md`) and does NOT define diagnostic fields (see `docs/11_DIAGNOSTICS_CONTRACT.md`).

## If you only read one thing
- **Goldens** are *valid* workspaces that must pass schema + semantic validation. They are used to prevent regressions and to prove end-to-end behavior.
- **Fixtures** are targeted test inputs (often invalid) that must produce deterministic diagnostics with strict assertions (rule_id, tier, file, json_pointer, etc).
- Discovery is **filesystem-driven**: tests recurse directories and treat a folder as a “case” only when it contains an `expected.json` (or other declared expected artifact).
- Keep inputs **small and surgical**. Prefer many tiny cases over a few large ones.
- Determinism is non-negotiable: stable ordering, stable JSON output bytes, no timestamps, no random IDs, no machine-specific paths.

## Update log
- 2026-01-26: Initial version.

## Where these assets live

These assets live in the main repo (not inside `living-docs/`):

- `tests/goldens/`  
- `tests/fixtures/`

This doc lives at: `living-docs/docs/22_FIXTURES_AND_GOLDENS.md`

See also:
- TestKit front door: `docs/02_TESTKIT_EXECUTION_ORDER.md`
- Workspace layout canon: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- Semantic rules catalog: `docs/14_SEMANTIC_RULES_CATALOG.md`
- Regression snapshot rules: `docs/23_REGRESSION_SNAPSHOTS.md` (next)

## Quick definitions

### Fixture
A **fixture** is a minimal input designed to trigger a specific validation behavior. Most fixtures are invalid on purpose (schema, semantic, or policy tier).

Typical fixture case contains:
- `input.yaml` (or `raw.yaml`, `variant_a.yaml`, etc)
- `expected.json` describing the assertions (diagnostics, counts, rule_ids, pointers)
- optional `notes.md` explaining intent, the “why”, and what to tighten later

### Golden
A **golden** is a complete workspace that should be valid and remain valid across versions.

Typical golden case contains:
- `workspace/` with a small, realistic set of manifest files
- optional `notes.md` explaining what it proves
- tests assert: validates cleanly and optionally matches regression snapshots

## Folder layout (canonical)

### Goldens
```
tests/
  goldens/
    <archetype_slug>/
      small/
        workspace/
          ptbl-index.yaml
          app-core.yaml
          app-data.yaml
          ... (small = roughly 3 to 6 files)
        notes.md (optional)
      medium/
        workspace/
          ... (medium = roughly 15 to 25 files)
        notes.md (optional)
```

Archetype slugs should be stable and boring. Use lowercase snake case.

### Fixtures (main buckets)
```
tests/
  fixtures/
    negative/
      schema/
        <case_slug>/
          input.yaml
          expected.json
          notes.md (optional)
      semantic/
        <case_slug>/
          input.yaml
          expected.json
          notes.md (optional)
      policy/
        <case_slug>/
          input.yaml
          expected.json
          notes.md (optional)

    changeset/
      <category_slug>/
        <case_slug>/
          changeset.yaml
          workspace/ (optional, only if the case needs context)
          expected.json
          notes.md (optional)

    ambiguity_hunts/
      <case_slug>/
        variant_a.yaml
        variant_b.yaml
        notes.md
        expected.json (optional, only if you assert diagnostics; otherwise registry drives)

    real_failures/
      <source>/<id>/
        raw.yaml
        minimal.yaml
        expected.json
        notes.md
```

Notes:
- `expected.json` is the “case boundary” marker for most test discovery.
- Use `notes.md` whenever the case is not self-explanatory.

## How tests discover cases

The preferred pattern is:
- walk the tree under a known root
- treat any directory containing `expected.json` as a test case
- load one or more inputs from the same directory (convention-based)

This keeps the test suite scalable and avoids hand-maintained lists.

If a bucket needs a registry (example: ambiguity hunts), the registry must be canonical and deterministic, and the test must still resolve fixture directories from it.

## `expected.json` contract (minimum)

At minimum, `expected.json` should allow strict assertions that tie back to the diagnostics contract.

Minimum recommended fields:
- `case_id` or `name` (human friendly)
- `tier` (schema | semantic | policy)
- `expect_valid`: true/false (goldens set true; negatives set false)
- `diagnostics` assertions:
  - `rule_id` (must match exactly)
  - `severity` (if asserted)
  - `file` (relative path or manifest filename)
  - `json_pointer` (pointer to the failing location)
  - optional `message_contains` (small substring, avoid full messages unless stabilized)

The “diagnostics object shape” itself is defined in `docs/11_DIAGNOSTICS_CONTRACT.md`. This doc only defines what the fixture suite should assert and how.

## Determinism rules (hard requirements)

### Inputs
- No timestamps, UUIDs, or host-specific absolute paths.
- Avoid large blobs. Keep YAML minimal.
- Keep key order stable (YAML writer must not reorder).

### Outputs
- JSON must be byte-identical across runs on the same version.
- Sort diagnostics in a deterministic order (rule_id, file, pointer, message key).
- No random ordering from filesystem traversal. Always sort directory listings.

### Case IDs and names
- Use stable IDs and slugs. Do not renumber existing cases.
- When adding new cases, append, never reorder lists that are treated as canonical.

## Writing new goldens (guidelines)

Goldens should:
- be realistic enough to exercise resolver behavior (imports, refs, index)
- be minimal enough to understand without reading 20 files
- avoid optional flair fields that are likely to churn

A golden should always document:
- what it is proving (1 to 3 bullets)
- the “boundary” (what it intentionally does not cover)

If a golden starts failing because the schema changed intentionally:
- update the golden workspace
- update regression snapshots (if used)
- record the change in the pack changelog and in the golden notes

## Writing new negatives (guidelines)

Negatives should be surgical:
- one main failure per case (avoid cascading failures)
- assert the primary diagnostic you care about
- allow secondary diagnostics only if they are stable and required

Tier placement rule:
- **schema/**: wrong shape, wrong discriminator, wrong types, extra fields in closed objects
- **semantic/**: wrong refs, missing targets, cross-file consistency errors
- **policy/**: “allowed/disallowed” constraints that are not pure schema or semantic integrity

When a case could fit multiple tiers, pick the *earliest* tier that should catch it.

## Suggested “done” checklist for a new case

For each new fixture or golden:
- [ ] directory name is stable and descriptive
- [ ] input YAML is minimal and deterministic
- [ ] `expected.json` asserts: rule_id, tier, file, json_pointer
- [ ] optional `notes.md` explains intent
- [ ] test discovery finds it without adding hardcoded lists
- [ ] repeated runs produce identical output bytes

## Common mistakes to avoid
- Putting fixtures under `living-docs/` instead of `tests/fixtures/`
- Reusing a case slug for a different purpose
- Asserting full diagnostic messages that are likely to change
- Allowing non-deterministic ordering (filesystem order, dict iteration order)
- Making a “negative” that is actually valid but fails due to missing external context

## Relationship to Phase 4 batch work

Phase 4 batch tasks grow these assets over time:
- Goldens: expand by archetype and size until at least 20 exist
- Negatives: expand to 150+ with strict, tiered coverage
- Changesets: stress pack of 50 to 80 validate-only cases
- Ambiguity hunts: evidence pipeline plus pairs over time

Phase 4 reporting should remain non-blocking until the suite is big enough and stable enough to trust.

