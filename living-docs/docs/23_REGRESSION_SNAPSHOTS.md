# Regression Snapshots

Last updated: 2026-01-26

Scope: Defines what “regression snapshots” are in this repo, what must be snapshotted, how snapshots are generated, and the determinism rules that make them trustworthy. This doc does NOT define semantic rules, fixtures, or lint rules themselves. It defines snapshot policy and workflow.

## If you only read one thing
- A regression snapshot is a **byte-stable, golden reference** for outputs we promise to keep deterministic (diagnostics JSON, reports, normalized artifacts).
- Snapshots are merge-blocking only when the underlying output is intended to be stable. Otherwise, use a non-blocking report artifact first.
- All snapshot generation must be reproducible: same inputs, same tool version, same output bytes.
- Never “fix” a failing snapshot by re-recording blindly. First confirm the change is intentional, then update snapshot with a logged reason.

## Canon links
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- CLI contract: `docs/12_CLI_CONTRACT.md`
- Changeset semantics: `docs/13_CHANGESET_SEMANTICS.md`
- Lint and meta tests: `docs/21_LINT_AND_META_TESTS.md`
- Fixtures and goldens: `docs/22_FIXTURES_AND_GOLDENS.md`
- Schema pack canon: `docs/20_SCHEMA_PACK.md`
- Status: `docs/00_STATUS.md`

---

## What is a regression snapshot

A regression snapshot is a stored expected output that protects:
- Determinism (ordering, stable formatting, stable field shapes)
- Backwards compatibility of the validator’s outward-facing contracts
- Non-regression for known tricky cases

Snapshots exist to answer:
- “Did the validator output change?”
- “If yes, was the change intentional and documented?”

### Snapshot vs fixtures
- **Fixtures** are inputs (YAML/JSON files) that represent test cases.
- **Snapshots** are expected outputs produced from fixtures or from deterministic generators.

---

## What we snapshot in this repo (target set)

Only snapshot outputs that are intended to be stable contracts.

### A) Diagnostics JSON outputs
When running the validator on selected fixtures and goldens, snapshot:
- JSON diagnostics list for each fixture (or a merged combined file), including:
  - rule_id
  - tier
  - severity
  - file
  - json_pointer
  - message (if message is stable)
  - fix_actions (if stable and documented)

If message text is not stable yet, snapshot a minimized representation.

### B) Deterministic reports
Snapshot or produce deterministic artifacts for:
- Variant coverage reports (if present)
- Ambiguity evidence reports (if present)
- Any other deterministic meta-report that is intended to be stable

### C) CLI surface outputs (only if stable)
If the CLI has a stable machine-readable output mode (recommended), snapshot:
- `--format json` output for a small set of representative runs

Do NOT snapshot human-oriented “pretty” output unless you enforce stable formatting.

---

## Where snapshots live (recommended)

Keep snapshots under:
- `tests/snapshots/`

Common patterns:
- `tests/snapshots/diagnostics/<case_id>.json`
- `tests/snapshots/reports/coverage.json`
- `tests/snapshots/reports/ambiguity_report.json`

If you already use a different structure, keep it consistent and document it here.

---

## Determinism rules (non-negotiable)

Snapshots only work if outputs are deterministic.

### Ordering
- Sort diagnostics by:
  1) file path
  2) json_pointer
  3) rule_id
  4) severity (stable order)
- For any list in output JSON, define a stable sort rule.

### Formatting
- JSON must be serialized deterministically:
  - stable key ordering (sort keys)
  - fixed indentation
  - normalized newline (`\n`)
  - no trailing whitespace
- No timestamps in snapshot outputs.
- No machine-specific paths (absolute paths) in snapshot outputs.

### Version embedding
If outputs embed a `validator_version` or `pack_version`, then:
- Version bumps require snapshot refresh.
- Snapshot refresh must be an explicit step and logged as “version bump only” if no logic changed.

---

## Snapshot update workflow

### When a snapshot test fails
1) Identify which output changed and why.
2) Decide whether change is:
   - Bug fix (good)
   - Intentional contract change (needs doc update)
   - Accidental nondeterminism (must fix implementation)
3) Only then update snapshots.

### Acceptable reasons to update snapshots
- Version bump that is intentionally embedded in output
- Intentional contract change that is documented in the relevant contract doc
- Fixing a bug that produced incorrect output

### Unacceptable reasons
- “It’s easier to re-record”
- “It seems fine”
- “It passed locally once”

---

## How to run snapshot tests (local)

This repo may implement snapshots in different ways. These are the recommended commands.

### Run snapshot-related tests
```powershell
python -m pytest -q tests -k snapshot
```

### (If implemented) Regenerate snapshots
Use an explicit regeneration command, never an implicit one.

Possible patterns:
```powershell
python -m pytest -q --snapshot-update
python .\tools\regen_snapshots.py
```

If your repo doesn’t yet have a regeneration tool, add one when snapshots become merge-blocking.

---

## What should be merge-blocking now vs later

### Merge-blocking now (recommended)
- Diagnostics JSON structure snapshots for a small fixed set of fixtures
- Deterministic report outputs that we claim are deterministic

### Later (once stable)
- Wider snapshot coverage across more fixtures
- CLI pretty output snapshots (only if you truly want stable text output)

---

## Minimal “starter pack” for regression snapshots (actionable plan)

1) Pick 10 representative fixtures:
   - mix of schema, semantic, and policy negatives
   - at least 2 ambiguity cases (if treated as report-only)
   - at least 2 goldens (one small, one medium)

2) Create a single test that:
   - runs validator deterministically
   - writes output JSON in a fixed format
   - compares to `tests/snapshots/...`

3) Add a regen script guarded by:
   - explicit flag
   - prints changed files
   - fails if used in CI unless explicitly allowed

4) Document all of this in this doc and in `docs/21_LINT_AND_META_TESTS.md`.

---

## Update log
- 2026-01-26: Created regression snapshots policy and workflow doc (what to snapshot, determinism rules, and update workflow).
