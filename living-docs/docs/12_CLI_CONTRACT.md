# CLI Contract

Last updated: 2026-01-26

Scope: Defines the canonical command surface, exit codes, and output formats for the PTBL validator CLI. This is a hard contract for CI, editor integrations, and agentic workflows. This doc does NOT define schema meaning or semantic rule behavior.

## If you only read one thing
- The CLI is an API. Keep flags, exit codes, and JSON output stable.
- Default behavior is deterministic. Same inputs must produce byte-identical JSON diagnostics output.
- Exit codes are meaningful and must not drift. CI depends on them.
- Never print secrets. Redact paths and values only if required, but do it deterministically.
- Output has two layers: a minimal JSON result wrapper and a list of Diagnostic objects (see `docs/11_DIAGNOSTICS_CONTRACT.md`).

## Canon links
- Diagnostics object and determinism rules: `docs/11_DIAGNOSTICS_CONTRACT.md`
- Workspace layout and output locations: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Changeset format rules: `docs/13_CHANGESET_SEMANTICS.md`

## Command name and entrypoint

The canonical command name is:

- `ptbl`

Implementations may also support `python -m ptbl` as an equivalent entrypoint, but `ptbl` is the contract name for docs, CI, and tooling.

## Global flags

These flags must behave consistently for all subcommands:

- `--version`
  - Prints the single pack version string and exits with code 0.
  - Must not print extra text in machine contexts. If you want a human-friendly line, add `--format text`.

- `--help`
  - Prints help and exits with code 0.

- `--format (json|text)`
  - Selects output format.
  - Default is `text` for interactive use.
  - For CI and tooling, recommend `--format json`.

- `--cwd <path>`
  - Treat this as the workspace root. If absent, use the current working directory.
  - Output paths (like `tests/_out/...`) are relative to this root.

## Exit code contract

Exit codes must be stable and consistent across platforms.

- `0`: success, and no diagnostics with `severity=error`.
- `1`: validation failed, at least one diagnostic with `severity=error`.
- `2`: usage error (bad flags, missing arguments, unknown command).
- `3`: runtime error (uncaught exception, IO failure, internal bug).

Rule: schema, semantic, and policy errors all map to exit code 1. Tier does not change exit code.

## Subcommands

### 1) `ptbl validate`

Purpose: Validate a workspace or a specific file set.

#### Usage
- `ptbl validate`
- `ptbl validate --root <path>`
- `ptbl validate --files <path> --files <path> ...`

#### Options
- `--root <path>`
  - Workspace root. If absent, use `--cwd` (or current directory).
- `--files <path>`
  - Validate only these workspace-relative paths. Repeatable.
- `--tier (schema|semantic|policy|all)`
  - Default: `all`.
  - If `schema` is selected, only schema diagnostics are emitted.
  - If `semantic` is selected, schema must still run first for parsing and shape, but only semantic diagnostics are emitted.
  - Same rule for `policy`.
- `--fail-fast`
  - Stop after the first error diagnostic is produced.
  - Determinism rule: the first diagnostic must still be deterministic based on the global sort order.
- `--strict`
  - Treat warnings as errors for exit code purposes.
  - Contract: when strict is enabled, any `warning` behaves like `error` for exit code. The diagnostic severity field stays `warning`.
- `--out <path>`
  - If `--format json`, write the JSON result to this path.
  - If absent, JSON goes to stdout.

#### Text output contract (default)
Text output is for humans. It may include summaries, but it must remain deterministic in ordering.

Recommended layout:
- Summary line: total errors, warnings, infos
- Then each diagnostic on its own block:
  - `[TIER] [SEVERITY] RULE_ID file:json_pointer`
  - `message`
  - Optional: related files

#### JSON output contract
When `--format json` is used, output must be a single JSON object:

```json
{
  "ok": false,
  "validator_version": "X.Y.Z",
  "diagnostics": []
}
```

Rules:
- Keys must be in stable order.
- `diagnostics` must already be deterministically sorted.
- No extra stdout text. If you need logging, send to stderr.

### 2) `ptbl lint`

Purpose: Run fast static checks that are not full validation. This is typically a policy-tier surface that is safe to run frequently.

#### Usage
- `ptbl lint`
- `ptbl lint --root <path>`

#### Options
- `--root <path>` same semantics as validate.
- `--format (json|text)` same semantics.

#### Exit codes
Same as validate.

### 3) `ptbl report`

Purpose: Generate deterministic reports used by the TestKit, such as variant coverage or ambiguity reports.

This command is optional. If you do not expose it, you must provide equivalent Python entrypoints invoked by tests.

#### Suggested usage
- `ptbl report coverage --out tests/_out/coverage.json`
- `ptbl report ambiguity --out tests/_out/ambiguity_report.json --out-md tests/_out/ambiguity_report.md`

#### Determinism rules
Reports must be byte-identical across runs given the same inputs.

## Machine consumption rules

When integrating the CLI in CI or agentic loops:
- Use `--format json` and capture stdout exactly.
- Do not parse text output.
- Depend only on:
  - exit code
  - JSON wrapper fields
  - diagnostic contract fields

## Error handling rules

- Usage errors must exit 2 and print help or a clear error message to stderr.
- Runtime errors must exit 3 and print a minimal, non-secret stack trace to stderr.
- When exiting 3, do not emit partial JSON to stdout unless you are explicitly in a "best effort" mode (not recommended for the contract).

## Backwards compatibility policy

- Adding a new optional field in JSON output is allowed if it is stable and does not break consumers.
- Renaming or removing fields is not allowed in the same major version.
- Changing exit codes is not allowed without an explicit major version bump and migration plan.

## Update log
- 2026-01-26: Created the canonical CLI contract (commands, flags, exit codes, and output rules).
