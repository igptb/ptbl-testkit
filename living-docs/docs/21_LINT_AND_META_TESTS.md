# Lint and Meta Tests

Last updated: 2026-01-26

Scope: Defines the purpose, contracts, and expected behavior of **lint checks** and **meta tests** for the PTBL TestKit repo. This doc focuses on preventing schema drift, ambiguity, and determinism regressions. It does NOT define the full semantic validation rules (see the semantic rules catalog) and it does NOT define policy rules.

## If you only read one thing
- Meta tests and lint exist to stop schema debt from compounding: once the repo accepts ambiguous or loose structure, you cannot safely tighten it later.
- Treat PTBL blueprints as **machine-consumed contracts for LLMs**, so schema ambiguity directly causes hallucinations and non-determinism.
- Any new lint rule must be: deterministic, stable-ID, and backed by at least one test (or fixture + test) that proves it fires.
- Meta tests should be cheap and always-on in CI. If a meta test is flaky, it is worse than useless.

## Canon links
- Status (what is complete, what is next): `docs/00_STATUS.md`
- Routing guide (where to put things): `docs/01_ROUTING_GUIDE.md`
- Workspace layout spec: `docs/10_WORKSPACE_LAYOUT_SPEC.md`
- Diagnostics contract: `docs/11_DIAGNOSTICS_CONTRACT.md`
- Semantic rules catalog: `docs/14_SEMANTIC_RULES_CATALOG.md`
- Schema pack canon: `docs/20_SCHEMA_PACK.md`

---

## Why lint and meta tests exist

### The core problem they prevent
Schemas and validation logic tend to degrade over time through:
- Accidental openness (missing `additionalProperties: false`, unbounded `object` shapes)
- Dual identity (map key and internal `uid` disagree, or both exist and drift)
- Stringly references (free-form strings instead of validated UID/ref semantics)
- Optional UIDs becoming permanent (backwards compatibility trap)
- Version drift (docs say v2.6.19 but code silently accepts a different shape)
- Non-deterministic ordering (unordered map iteration, unstable diagnostics ordering)

Lint and meta tests are the guard rails that catch these issues early.

### Two layers, two jobs
**Lint**
- Fast, rule-based checks over repo structure, schemas, fixtures, and code conventions.
- Usually produces human-readable diagnostics with rule IDs.
- Often run locally before committing and also in CI.

**Meta tests**
- Automated tests (pytest) that assert invariants about the repo and schema pack.
- Must be deterministic and merge-blocking.
- Prefer tight assertions that fail loudly and predictably.

---

## Definitions

### Lint rule
A lint rule is a deterministic check with:
- A stable `rule_id`
- A clear trigger condition
- A consistent diagnostic payload (aligned with the diagnostics contract, if lint emits diagnostics)

### Meta invariant
A meta invariant is an always-true statement about the repo, for example:
- “All schemas are closed (no open objects) except approved bag primitives.”
- “The schema pack has exactly N canonical schema files and they are consistent.”
- “No schema has both map-key identity and a duplicate `uid` field for the same object.”

---

## Lint contracts

### Rule IDs
- Use stable IDs.
- Recommended prefix: `LINT_...`
- One rule ID should have one meaning. If meaning changes, create a new ID.

### Determinism
Lint output must be deterministic:
- Stable ordering of findings (sort by file path, then rule ID, then location)
- No timestamps
- No random ordering
- No reliance on OS directory iteration order

### Severity
Keep lint severities simple:
- `error`: must fix before merge
- `warning`: allowed but visible (use sparingly)
- `info`: usually off by default

### What lint should cover
The “high value” targets:
- Schema hygiene:
  - closed objects by default
  - no unintended `additionalProperties: true`
  - consistent `$id` and `$ref` style
  - discriminator and oneOf usage rules
- Identity and references:
  - single identity strategy (no duplicate UID sources)
  - refs validated by type (no stringly refs)
- Version alignment:
  - schema pack version referenced consistently across docs, tooling, and fixtures when versioned output is embedded
- Repo hygiene:
  - forbidden file patterns committed (large artifacts, secrets, OS noise)
  - required docs present (front doors, contracts)

### What lint should NOT cover
- Anything subjective or “style-only” (move to policy tier if needed).
- Anything that requires network calls.
- Anything that is slow or flaky.

---

## Meta tests contracts

### Properties of a good meta test
- Cheap: seconds, not minutes
- Deterministic: byte-identical outputs on repeat runs
- Self-contained: no dependence on external services
- Specific failure: the assertion tells you exactly what to fix

### Meta tests we expect in this repo
This section is a contract, not a claim about current implementation names. If file names differ, keep the same intent.

#### Schema pack invariants
- Schemas load successfully as JSON.
- The schema set is complete (expected files exist).
- All schemas that must be closed are closed.
- No schema violates PTBL “single identity” rules (example: map key equals UID, do not duplicate UID fields).
- `$ref` targets resolve within the pack (no broken internal references).

#### Determinism invariants
- Any generated meta artifact (coverage reports, ambiguity reports, snapshots) is byte-identical across multiple runs.
- Diagnostics ordering is stable.

#### Fixture invariants
- Every negative fixture has an `expected.json` with required asserted fields.
- Fixture discovery is deterministic.

---

## Where these checks live

### Recommended layout (target)
- Lint entrypoint:
  - `ptbl_lint.py` at repo root, or a module entrypoint like `ptbl/lint/__main__.py`
- Meta tests:
  - `tests/test_meta_*.py` (schema pack invariants)
  - `tests/test_lint_*.py` (lint rule unit tests, if applicable)
- Lint rule implementation:
  - `ptbl/lint/` (preferred), or `ptbl/validate/` if shared utilities exist

If your repo currently uses different paths, keep the **contracts** but adjust routing in `docs/01_ROUTING_GUIDE.md`.

---

## How to run (local)

### 1) Run the full test suite
```powershell
python -m pytest -q
```

### 2) Run only meta tests
If your repo follows the recommended naming:
```powershell
python -m pytest -q tests/test_meta_*.py
```

### 3) Run lint
Common patterns you might have:
```powershell
python .\ptbl_lint.py --help
python .\ptbl_lint.py
```

If you do not know the entrypoint, search for it:
```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "ptbl_lint" -List
```

---

## Adding a new lint rule (workflow)

1) Create a new stable `LINT_...` rule ID.
2) Define the trigger precisely (what files and what condition).
3) Implement the rule with deterministic iteration and stable output.
4) Add a test:
   - Either a unit test over a minimal fixture directory
   - Or a meta test that asserts the repo invariant
5) Document the rule in this doc:
   - Add it under “Lint rule catalog” below.
6) Wire it into the lint entrypoint so it runs by default (if merge-blocking).

---

## Lint rule catalog (starter)

This catalog should grow over time. Only list rules that exist (or are explicitly committed as TODO with an owner).

### LINT_SCHEMA_CLOSED_OBJECTS
- Intent: Prevent open objects except for explicitly allowed bag primitives.
- Trigger: Any schema object node missing `additionalProperties: false` where closure is required.
- Determinism: Traverse schemas in stable order; report paths sorted.
- Tests: Meta test that scans the schema pack and asserts closure rules.

### LINT_DUAL_IDENTITY_FORBIDDEN
- Intent: Enforce single identity strategy to avoid drift.
- Trigger: A schema allows both map-key identity and a duplicated `uid` field (or multiple UID sources) for the same object.
- Tests: Meta test scanning schema definitions.

### LINT_REF_SEMANTICS_VALIDATED
- Intent: Stop stringly references.
- Trigger: A field documented as a UID/ref is represented as a free string without validation constraints.
- Tests: Meta test, plus at least one negative fixture proving failure.

---

## CI expectations

### Merge-blocking checks (recommended minimum)
- `pytest` must pass
- Meta tests must pass
- Lint must pass (at least error-level lint)

If CI uses a single job, that is fine, but the policy remains: these checks gate merges.

---

## Update log
- 2026-01-26: Created lint and meta tests contract doc (scope, invariants, determinism requirements, and starter rule catalog).
