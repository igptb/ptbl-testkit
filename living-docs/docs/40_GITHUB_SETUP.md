# GitHub Setup

Last updated: 2026-01-26

Scope: How this repo is configured on GitHub and the minimum guardrails for reliable CI and review. This covers branch structure, protections, CI expectations, and the required checks. It does NOT teach Git basics.

## If you only read one thing
- Keep **one main branch** protected. Work happens on short-lived branches and merges via PR.
- CI must be the gate: **tests must pass** before merge.
- Never merge large doc changes without updating `docs/00_STATUS.md` and `TASKS.md`.
- Keep changes small and reviewable. One doc per PR is normal.

## Canon links
- Dev workflow: `docs/41_DEV_WORKFLOW.md`
- Lint and meta tests: `docs/21_LINT_AND_META_TESTS.md`
- Regression snapshots: `docs/23_REGRESSION_SNAPSHOTS.md`
- CLI contract: `docs/12_CLI_CONTRACT.md`
- Status: `docs/00_STATUS.md`

---

## 1) Repo model

### 1.1 Branches
- `main`: protected, always green
- Feature branches: short-lived, named by purpose, examples:
  - `living-docs/<topic>`
  - `phase4/<task>`
  - `bugfix/<rule_id>`

### 1.2 PRs
Use PRs for everything that changes shared files.

Minimum PR expectation:
- One clear objective
- Small diff
- Linked to status and tasks updates where relevant

---

## 2) Required GitHub settings

### 2.1 Branch protection (main)
Recommended settings:
- Require a pull request before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Dismiss stale approvals when new commits are pushed (optional but good)
- Restrict who can push to `main` (recommended)

### 2.2 Required status checks
Set required checks to match what your GitHub Actions workflow publishes.

At minimum:
- Lint (format + lint)
- Tests (pytest)
- Optional: snapshots check (if you split it)

Important:
- If you rename a workflow job, update the required checks list.

---

## 3) CI expectations

### 3.1 What CI must enforce
CI should fail the PR if any of these fail:
- Lint and meta tests (see `docs/21_LINT_AND_META_TESTS.md`)
- Unit tests
- Fixture tests
- Snapshot tests (if snapshots exist for that area)

### 3.2 What CI should not enforce (yet)
Avoid adding merge-blocking checks for work that is still being scaled, unless explicitly declared ready.

Example:
- Phase 4 goldens are not merge-blocking until 20 exist (tracked in `docs/00_STATUS.md`)

---

## 4) GitHub Actions layout (practical)

Recommended structure:
- Workflow triggers on PRs and on pushes to `main`
- Jobs:
  1) Setup Python
  2) Install dependencies
  3) Run lint
  4) Run tests

Example commands CI should run (adjust to your repo):
- `python -m pytest -q`
- If you have targeted suites, keep a single default that always runs

---

## 5) Labels and PR hygiene (optional but useful)

Useful labels:
- `living-docs`
- `contracts`
- `tests`
- `fixtures`
- `snapshots`
- `breaking-change` (rare, requires explicit approval)

PR checklist (minimum):
- [ ] Updated doc header dates for changed docs
- [ ] Updated `TASKS.md` if a doc moved from planned to complete
- [ ] Updated `docs/00_STATUS.md` if progress changed
- [ ] CI is green

---

## 6) Safe merging rules

### 6.1 Squash vs merge commits
Either is fine, but be consistent:
- Squash merge keeps history clean
- Merge commits preserve branch history

If you use squash merge:
- Make sure the squash commit message is meaningful

### 6.2 Never merge broken main
If main breaks:
- Stop new work
- Fix main first
- Document the incident briefly in `docs/00_STATUS.md` update log

---

## Update log
- 2026-01-26: Added GitHub setup and guardrails (branches, protections, CI checks, and PR hygiene).
