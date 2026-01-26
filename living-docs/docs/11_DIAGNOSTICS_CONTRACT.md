# Diagnostics Contract

Last updated: 2026-01-26

Scope: Defines the canonical shape and determinism rules for validator diagnostics, across schema, semantic, and policy tiers. This is a hard contract for CLI output, tests, editor integrations, and any auto-repair loop. This doc does NOT define the content of each semantic rule. See `docs/14_SEMANTIC_RULES_CATALOG.md`.

## If you only read one thing
- Diagnostics are an API contract. Keep them stable. Never rename fields or change meanings casually.
- Every diagnostic must include: `rule_id`, `tier`, `severity`, `message`, `file`, and `json_pointer`.
- Ordering must be deterministic so snapshot tests can lock bytes. Sort by `(file, json_pointer, tier, severity, rule_id, message)`.
- Rule IDs are stable identifiers. Once shipped, do not change or reuse them.
- Fix actions are optional but if present they must be machine-applicable and validated. They must never be "best effort" free text.

## Canon links
- Routing: `docs/01_ROUTING_GUIDE.md`
- Workspace paths and where outputs live: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Semantic rule list and meanings: `docs/14_SEMANTIC_RULES_CATALOG.md`
- Fix actions vocabulary: `docs/15_FIX_ACTIONS_SPEC.md`
- CLI output formats and exit codes: `docs/12_CLI_CONTRACT.md`

## Terminology
- **Diagnostic**: One reportable issue (error, warning, info) produced by validation.
- **Tier**:
  - `schema`: JSON Schema validation shape failures.
  - `semantic`: cross-field and cross-file integrity rules.
  - `policy`: repo or product policy rules (style, lint, constraints that are not pure schema or semantic integrity).
- **Location**: Optional structured positions for humans (line, column), in addition to the required machine pointer `json_pointer`.
- **Fix action**: Optional structured instruction that a deterministic applier could perform to repair an issue.

## The Diagnostic object (canonical)

### Required fields

Every diagnostic MUST include these fields:

- `rule_id` (string)
  - Stable identifier for the check that produced this diagnostic.
  - Format: `SCHEMA_*`, `SEM_*`, `POL_*` prefixes are recommended.
  - Examples:
    - `SCHEMA_YAML_INVALID`
    - `SEM_CHANGESET_REFERENCES_VALID`
    - `POL_WORKSPACE_NO_OPEN_OBJECTS`

- `tier` (string enum)
  - One of: `schema`, `semantic`, `policy`.

- `severity` (string enum)
  - One of: `error`, `warning`, `info`.
  - Rule: any `error` must cause overall validation failure for that run mode (see CLI contract).

- `message` (string)
  - Human-readable, concise, actionable.
  - Must not include secrets.
  - Should not include unstable data like timestamps or memory addresses.

- `file` (string)
  - Workspace-relative path using forward slashes.
  - Example: `apps/my_app/app-core.yaml`

- `json_pointer` (string)
  - RFC 6901 JSON Pointer to the specific failing node in the parsed document.
  - Root is `/`.
  - For YAML sources, the pointer refers to the YAML parsed as a JSON-like structure.
  - Must be stable for deterministic output.

### Optional but recommended fields

These fields SHOULD be included when available and stable:

- `code` (string)
  - Short machine-friendly code, often the same as `rule_id` or a sub-code.
  - If used, keep stable.

- `details` (object)
  - Structured extra context for debugging.
  - Must be deterministic in key ordering when serialized.
  - Do not put large payloads here.

- `related_files` (array of strings)
  - Other files relevant to this error, workspace-relative.

- `locations` (array of objects)
  - 1 or more human-friendly locations.
  - Use when you can map pointers to a line/column reliably.
  - Each location object:

```json
{
  "path": "apps/my_app/app-core.yaml",
  "start_line": 12,
  "start_col": 5,
  "end_line": 12,
  "end_col": 22
}
```

- `fix_actions` (array of objects)
  - Proposed deterministic repairs.
  - Must be validated against `docs/15_FIX_ACTIONS_SPEC.md` once that doc exists.
  - Must be safe, minimal, and reproducible.

## Rule ID stability and naming

### Stability rules
- Rule IDs are stable across releases.
- Do not change the meaning of an existing `rule_id`.
- If behavior changes materially, create a new rule ID and deprecate the old one in the rule catalog.
- Never reuse a retired rule ID for a different rule.

### Recommended naming convention
- Schema tier: `SCHEMA_*`
- Semantic tier: `SEM_*`
- Policy tier: `POL_*`

Within each tier:
- Use an all-caps noun phrase.
- Keep it specific.
- Prefer positive phrasing for invariants (example: `SEM_IMPORT_TARGET_EXISTS`).

## Determinism requirements

### Ordering
Diagnostics MUST be returned in a deterministic order. Sort by this stable key tuple:

1) `file` (lexicographic)
2) `json_pointer` (lexicographic)
3) `tier` (schema, semantic, policy)
4) `severity` (error, warning, info)
5) `rule_id`
6) `message`

If two diagnostics still collide, add a final tie-breaker such as a stable hash of the diagnostic object with keys sorted.

### Serialization
If diagnostics are serialized to JSON:
- Use stable key ordering.
- Use consistent whitespace policy in snapshot tests (define in snapshot doc).
- Never include unstable fields (timestamps, elapsed_ms, random ids) in snapshot-locked outputs.

## Minimum output contract (batch result)

Many callers want a “validation result” wrapper. If you expose a wrapper object, keep it minimal and stable:

```json
{
  "ok": false,
  "validator_version": "X.Y.Z",
  "diagnostics": [ /* list of Diagnostic objects */ ]
}
```

Rules:
- `validator_version` must match the pack version policy.
- `diagnostics` must already be sorted deterministically.

## Example diagnostics

### Example: schema-tier error

```json
{
  "rule_id": "SCHEMA_VALIDATION_FAILED",
  "tier": "schema",
  "severity": "error",
  "message": "Field must be a string.",
  "file": "apps/my_app/app-core.yaml",
  "json_pointer": "/app/name"
}
```

### Example: semantic-tier error with related file

```json
{
  "rule_id": "SEM_IMPORT_TARGET_EXISTS",
  "tier": "semantic",
  "severity": "error",
  "message": "Import target does not exist.",
  "file": "apps/my_app/app-core.yaml",
  "json_pointer": "/imports/0/target",
  "related_files": ["modules/common/module.yaml"]
}
```

### Example: policy-tier warning with fix action

```json
{
  "rule_id": "POL_FIELD_ORDER_STYLE",
  "tier": "policy",
  "severity": "warning",
  "message": "Fields are not in canonical order.",
  "file": "apps/my_app/app-core.yaml",
  "json_pointer": "/",
  "fix_actions": [
    {
      "type": "reorder_keys",
      "path": "apps/my_app/app-core.yaml",
      "json_pointer": "/",
      "order": ["app", "imports", "modules", "policies"]
    }
  ]
}
```

## Guardrails
- No secrets: do not echo credential values in messages or details.
- Keep messages short and actionable.
- Do not mix tiers: schema failures are schema, even if they block semantic validation.
- If you must stop early (fail-fast mode), still return a deterministic subset.

## Update log
- 2026-01-26: Created the canonical diagnostics contract (shape, stability, determinism, and examples).
