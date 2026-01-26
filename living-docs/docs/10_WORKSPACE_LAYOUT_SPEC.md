# Workspace Layout Spec

Last updated: 2026-01-24

Scope: Canonical folder and file layout for the PTBL TestKit and validator repo, including where fixtures, goldens, snapshots, and generated reports live. This doc does NOT define schema meaning or rule logic.

## If you only read one thing
- Keep paths stable. Tests and tools depend on these locations. Do not rename folders without updating the docs and tests.
- Separate source from generated outputs. Generated artifacts go under `tests/_out/` (or `artifacts/` if you later standardize there).
- Fixtures are organized by intent: negative fixtures, changesets, ambiguity hunts, real failures.
- Goldens are organized by archetype and size and must validate cleanly.

## Repository root layout

This spec assumes a single repo root (for example: `ptbl-testkit/`). The living docs folder can live inside the repo root.

Recommended top-level layout:

- `ptbl/`  
  Python package for the validator and related utilities.
- `tests/`  
  Test suite, fixtures, goldens, snapshots, and generated test outputs.
- `living-docs/`  
  The living Markdown docs set (this is what you are editing now).
- `scripts/` (optional)  
  Helper scripts if you want to separate them from `ptbl/`.
- `artifacts/` (optional)  
  Build artifacts if you want a single non-test output directory later.

## Living docs layout

Inside `living-docs/`:

- `README.md`  
  Front door and map.
- `TASKS.md`  
  Checklist for doc creation and conversion.
- `docs/`  
  Flat doc folder. All living docs live here.
- `exports/docx/`  
  Original or exported Word documents that were converted into Markdown.
- `templates/`  
  Header template and helper scripts to create new docs quickly.

Rule: keep `docs/` flat. Use numbering and strong titles to avoid nesting.

## Validator and TestKit code layout

Inside `ptbl/` (conceptual, not exhaustive):
- `ptbl/cli.py`  
  CLI entrypoints and version string.
- `ptbl/validate/`  
  Validation logic, report generators, and shared utilities.

Rule: do not place test-only utilities in random locations. Prefer a clear home such as `ptbl/validate/` for generators that are invoked by tests.

## Tests layout

Inside `tests/`:

### Fixtures
All instance fixtures live under `tests/fixtures/`:

- `tests/fixtures/negative/`  
  Negative cases. Organized by tier:
  - `schema/`
  - `semantic/`
  - `policy/`

- `tests/fixtures/changeset/`  
  Changeset fixtures grouped by category.

- `tests/fixtures/ambiguity_hunts/`  
  Paired fixtures that are both valid, but intended to have equivalent meaning.

- `tests/fixtures/real_failures/`  
  Real LLM failures harvested over time, organized by source and case id.

Convention for fixture case directories:
- Each case directory should contain the minimum inputs plus an `expected.json` (or similar) that asserts:
  - rule_id
  - tier
  - json_pointer
  - file path

### Goldens
Goldens live under `tests/goldens/`:

- `tests/goldens/<archetype>/<size>/workspace/`

Where:
- `<archetype>` is a stable identifier (snake_case).
- `<size>` is `small` or `medium` (and later maybe `large`).

Rule: goldens must validate cleanly and remain stable. They are not negative fixtures.

### Snapshots
Snapshots live under `tests/snapshots/`.

Rule: snapshots are committed only if you are intentionally locking down deterministic bytes for diagnostics or outputs. If you are not locking bytes, do not introduce snapshots.

### Generated test outputs
Generated files produced during tests should go under:

- `tests/_out/`

Examples:
- `tests/_out/coverage.json`
- `tests/_out/ambiguity_report.json`
- `tests/_out/ambiguity_report.md`

Rule: treat `tests/_out/` as generated and ignore it in git unless you explicitly decide to commit an output for a specific reason.

## Git ignore recommendations

These are typical ignore targets:
- `tests/_out/`
- `__pycache__/`
- `.pytest_cache/`
- local virtualenv folders

Rule: never ignore canonical docs or fixtures. Only ignore generated outputs and local environment noise.

## Update log
- 2026-01-24: Created workspace layout spec for the validator repo and living docs folder.
