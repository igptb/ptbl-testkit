# Changeset Semantics

Last updated: 2026-01-26

Scope: Defines the canonical semantics for PTBL changesets: file identity, JSON Pointer targeting, operation types, determinism rules, and what “valid” means. This doc is the contract for changeset fixtures and validator checks. This doc does NOT define the apply engine implementation details beyond deterministic requirements.

## If you only read one thing
- A changeset is designed so a dumb deterministic program can apply it. No LLM required.
- Changesets must be validate-only by default. The validator checks structure and referential integrity, not “does this edit look good.”
- Targeting is by `file_uid` (stable) and `json_pointer` (RFC 6901). Never by fuzzy paths or free text.
- Operation ordering and conflicts must be deterministic. Same inputs must produce the same diagnostics in the same order.
- Use closed, typed operations only. No “arbitrary patch” blobs.

## Canon links
- Diagnostics shape and ordering: `docs/11_DIAGNOSTICS_CONTRACT.md`
- CLI contract and exit codes: `docs/12_CLI_CONTRACT.md`
- Workspace file identity rules: `docs/10_WORKSPACE_LAYOUT_SPEC.md`

## Core concepts

### What a changeset is
A changeset is a list of explicit edit operations against a workspace snapshot. Each operation targets:
- a specific file (by `file_uid`)
- a specific location (by `json_pointer`)
- a specific mutation type (insert, replace, delete, rename, add file, delete file, etc.)

### Why changesets exist
- Deterministic editing: edits can be applied and reviewed mechanically.
- Reduced blast radius: operations are scoped and auditable.
- Stable agent loop: LLM proposes changeset, validator checks it, applier executes it, validator rechecks.

## Identity and targeting

### File identity
A changeset MUST target files by stable UID:

- `file_uid`: the canonical identity for a file inside a workspace.
- Do not target by file path alone. Paths can change via rename operations.

If you still store `path` on an op for convenience:
- treat it as informational only
- validate it matches the current file_uid mapping when possible
- never use it as the primary key

### JSON Pointer targeting
All in-file operations use RFC 6901 JSON Pointers.
- Root is `/`
- Array indices use numeric segments: `/items/0/name`
- Pointer segments must be properly escaped:
  - `~` is `~0`
  - `/` is `~1`

YAML is treated as JSON-like after parsing. Pointers reference the parsed structure, not raw text.

## Changeset object shape (conceptual)

The exact JSON schema is defined in the schema pack. This doc defines semantics.

Minimum fields:
- `changeset_uid` (string, stable)
- `target_workspace_uid` (string or omitted if “current workspace”)
- `ops` (array of operation objects)

Semantics:
- `ops` is ordered.
- The applier processes ops in order.
- If an op fails, the applier must stop deterministically at that op (fail-fast), unless an explicit batch mode is defined.

## Operation types

All ops MUST be one of the typed operations below. No open-ended op types.

### 1) `set_value`
Sets (replaces or creates) a value at `json_pointer`.

Fields:
- `type`: `set_value`
- `file_uid`
- `json_pointer`
- `value` (any JSON value)

Semantics:
- If the pointer exists, replace the value.
- If the pointer does not exist but the parent exists and is a map, create the key.
- If the pointer does not exist because an intermediate node is missing, this is an error.

### 2) `delete_value`
Deletes a key from a map or an element from an array.

Fields:
- `type`: `delete_value`
- `file_uid`
- `json_pointer`

Semantics:
- Map delete: remove the key.
- Array delete: remove the element and shift remaining indices.
- Deleting a non-existent pointer is an error.

### 3) `insert_into_array`
Inserts an element into an array.

Fields:
- `type`: `insert_into_array`
- `file_uid`
- `json_pointer` (must point to an array)
- `index` (integer, 0..len)
- `value`

Semantics:
- Insert at index.
- Index may equal len to append.
- If pointer is not an array, error.

### 4) `move_value`
Moves a value from one pointer to another within the same file.

Fields:
- `type`: `move_value`
- `file_uid`
- `from_pointer`
- `to_pointer`

Semantics:
- Read value at `from_pointer`, delete it, then set at `to_pointer`.
- Both pointers must be valid for their intended operations.
- If `from_pointer` does not exist, error.

### 5) `rename_file`
Renames a file’s path, preserving identity.

Fields:
- `type`: `rename_file`
- `file_uid`
- `new_path` (workspace-relative, forward slashes)

Semantics:
- The file UID stays the same.
- `new_path` must not collide with an existing path.
- Path normalization must be deterministic.

### 6) `add_file`
Adds a new file.

Fields:
- `type`: `add_file`
- `file_uid` (new UID)
- `path`
- `content` (string, typically YAML)

Semantics:
- `file_uid` must not already exist.
- `path` must not already exist.
- `content` is treated as raw text; parsing happens after apply.

### 7) `delete_file`
Deletes a file.

Fields:
- `type`: `delete_file`
- `file_uid`

Semantics:
- File must exist.
- Deleting a missing file is an error.

## Determinism rules

### Sorting and diagnostics
- The changeset validator must emit diagnostics in deterministic order (see diagnostics contract).
- When validating ops, process `ops` in order.
- If you choose to also emit “aggregate” diagnostics, those must be placed deterministically after op-specific diagnostics.

### Conflict handling (deterministic)
The validator should detect common conflicts deterministically:
- Two ops writing the same pointer in the same file.
- Delete then set on the same pointer.
- Rename file then operate on old path by path-based targeting (if path fields exist).

Rule: prefer correctness and determinism over clever merging. When in doubt, error.

### Apply failure point
If apply is implemented:
- Stop at the first failing op.
- Report the failing op index deterministically in diagnostics details, if exposed.

## Validation semantics (what is checked)

The changeset validator SHOULD check:
- Operation type is one of the allowed set.
- `file_uid` exists (unless `add_file`).
- Pointers are valid RFC 6901.
- Pointer targets exist or are creatable under the op’s rules.
- Cross-file references inside ops are valid when applicable.
- No path traversal or absolute paths in `new_path` or `path`.

The changeset validator SHOULD NOT check:
- Business logic correctness.
- Style preferences beyond policy-tier checks.
- Whether a value “looks reasonable.”

## Security and safety guardrails
- Reject absolute paths, drive letters, and `..` segments.
- Reject writing outside workspace root.
- Avoid echoing file contents into diagnostics.
- If content is large, cap diagnostic details deterministically.

## Recommended fixture layout
For the TestKit stress pack:

- `tests/fixtures/changeset/<category>/<case>/changeset.json`
- `tests/fixtures/changeset/<category>/<case>/expected.json`
- `tests/fixtures/changeset/<category>/<case>/notes.md`

`expected.json` should assert at least:
- `rule_id`
- `tier`
- `severity`
- `file` and `json_pointer` when relevant

## Update log
- 2026-01-26: Created the canonical changeset semantics contract (ops, targeting, validation, determinism).
