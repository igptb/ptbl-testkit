# Fix Actions Spec

Last updated: 2026-01-26

Scope: Defines the contract for machine-applied "fix actions" emitted by the validator. This doc specifies the data model, determinism rules, and safety constraints. It does NOT define UI workflows, LLM prompting strategy, or any apply-engine implementation details beyond the minimum needed for interoperability.

## If you only read one thing
- Fix actions are **structured patches**, not free-form advice. They must be applicable by a dumb applier.
- Fix actions are **optional**: the validator can emit diagnostics without any fix actions.
- Fix actions must be **deterministic** for a given input workspace and validator version.
- Fix actions must be **safe by default**: no execution, no network, no touching files outside the workspace root.

## Canon links
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- Changeset semantics: `docs/13_CHANGESET_SEMANTICS.md`
- Regression snapshots: `docs/23_REGRESSION_SNAPSHOTS.md`
- Workspace layout: `docs/10_WORKSPACE_LAYOUT_SPEC.md`

---

## 1) Why fix actions exist

Diagnostics answer: "What is wrong?"
Fix actions answer: "What edit should be made to get to green?"

They exist so:
- Humans can apply fixes quickly
- Agents can auto-repair deterministically (validate -> emit fixes -> apply -> revalidate)
- Tools can build safe, repeatable repair loops without inventing edits

Fix actions are evidence, not magic. If the validator cannot specify a safe deterministic edit, it should emit no fix action.

---

## 2) Contract surface

### Where fix actions live
Fix actions are emitted alongside diagnostics in the validator output.

- Diagnostics: **required** contract (see `docs/11_DIAGNOSTICS_CONTRACT.md`)
- Fix actions: **optional** contract

If present, fix actions must be machine-readable and stable.

### Relationship to diagnostics
Each fix action should reference the diagnostic(s) it intends to fix using `diagnostic_id` or by stable matching fields (rule_id + file + json_pointer).

If your diagnostics contract does not include `diagnostic_id`, use stable referencing:
- `rule_id`
- `file`
- `json_pointer`

---

## 3) Data model

This spec uses JSON-style shapes. YAML is allowed as a serialization format, but the structure must match.

### Top-level shape
```json
{
  "pack_version": "10.4",
  "workspace_root": ".",
  "fix_actions": [ ... ]
}
```

Fields:
- `pack_version` (string, required): validator/pack version used to generate fixes
- `workspace_root` (string, required): path root used for relative file addressing
- `fix_actions` (array, required): list of fix action objects

### Fix action object
```json
{
  "id": "FIX_000123",
  "title": "Short human label",
  "severity": "error",
  "targets": [
    {
      "file": "app/app-core.yaml",
      "json_pointer": "/app/name",
      "rule_id": "SEM_IDENTITY_SINGLE_SOURCE"
    }
  ],
  "ops": [ ... ],
  "notes": "Optional short note",
  "confidence": "high"
}
```

Fields:
- `id` (string, required): stable within one run; deterministic across runs if possible
- `title` (string, required): short label, no long prose
- `severity` (enum string, required): `error` | `warning` | `info` (match diagnostics severities where possible)
- `targets` (array, required): what this action is meant to fix
- `ops` (array, required): patch operations (see below)
- `notes` (string, optional): small explanation
- `confidence` (enum string, optional): `high` | `medium` | `low`

Determinism rule:
- If `id` cannot be stable across runs, it must still be deterministic for a given input ordering and must not include timestamps/randomness.

---

## 4) Patch operations

Patch ops must be:
- Deterministic
- Bounded (no wildcard "search the internet" behavior)
- Workspace-scoped (no edits outside workspace root)

### Operation types (minimal set)
This minimal set is enough to support most deterministic repairs.

#### 4.1 Replace value
```json
{
  "op": "replace_value",
  "file": "app/app-core.yaml",
  "json_pointer": "/app/name",
  "value": "my_app"
}
```

#### 4.2 Add value (insert into object)
```json
{
  "op": "add_value",
  "file": "app/app-core.yaml",
  "json_pointer": "/app",
  "key": "expression_language",
  "value": "cel"
}
```

#### 4.3 Remove key
```json
{
  "op": "remove_key",
  "file": "app/app-core.yaml",
  "json_pointer": "/app",
  "key": "deprecated_field"
}
```

#### 4.4 Insert into array (append or at index)
```json
{
  "op": "insert_array_item",
  "file": "app/app-core.yaml",
  "json_pointer": "/app/modules",
  "value": { "uid": "mod_1", "ref": "..." },
  "index": 0
}
```
Rules:
- If `index` is omitted, append.
- Array ordering must be deterministic and consistent with workspace ordering rules.

#### 4.5 Replace array item (by index)
```json
{
  "op": "replace_array_item",
  "file": "app/app-core.yaml",
  "json_pointer": "/app/modules",
  "index": 2,
  "value": { "uid": "mod_3", "ref": "..." }
}
```

#### 4.6 Rename key (object)
```json
{
  "op": "rename_key",
  "file": "app/app-core.yaml",
  "json_pointer": "/app",
  "from": "old_name",
  "to": "new_name"
}
```

---

## 5) Preconditions and safety

Each op may include a precondition to avoid applying edits to the wrong structure.

### Precondition object (optional)
```json
{
  "expects": {
    "type": "string",
    "equals": "old_value"
  }
}
```

Supported checks (minimal):
- `type` (string): expected JSON type
- `equals`: exact match
- `exists` (bool): expect presence or absence

If a precondition fails, the applier must:
- Not apply that op
- Emit an apply error in a deterministic format (out of scope here)

---

## 6) Determinism requirements

Fix actions must:
- Not include timestamps, absolute paths, random IDs, or nondeterministic ordering
- Use stable ordering for:
  - `fix_actions` list
  - `ops` list within each fix
- Be stable with respect to:
  - file ordering
  - rule ordering
  - JSON pointer ordering

Recommended ordering:
1) Sort by `severity` (error, warning, info)
2) Then by `targets[0].file`
3) Then by `targets[0].json_pointer`
4) Then by `rule_id`
5) Then by `title`

---

## 7) Interaction with changesets

Fix actions are conceptually compatible with the changeset format documented in `docs/13_CHANGESET_SEMANTICS.md`.

Two acceptable patterns:
- Emit fix actions and let a separate step convert them into a changeset
- Emit fix actions directly in the same operation vocabulary as changesets

Constraint:
- Do not create two divergent patch languages without documenting the bridge.

---

## 8) Tests and snapshots

Fix actions must be covered by tests before being considered a real contract.

Minimum test expectations:
- Deterministic bytes for a fixed input fixture
- Stable ordering
- No nondeterministic fields
- Snapshot coverage for representative fixes

See: `docs/23_REGRESSION_SNAPSHOTS.md`

---

## 9) Non-goals
- No auto-apply engine is required by this spec
- No attempt to "guess intent" beyond deterministic edit rules
- No LLM-generated free-form patches as part of the contract

---

## Update log
- 2026-01-26: Added fix actions contract, data model, patch ops, and determinism/safety constraints.
