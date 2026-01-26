# Dev Workflow

Last updated: 2026-01-26

Scope: How we work in this repo day to day. This covers how to create small, safe changes, how to keep living docs consistent, and what must be updated after each task. It does NOT teach Git fundamentals, and it does NOT define any validator contracts (those live in the contract docs).

## If you only read one thing
- Keep changes small. One doc per batch is normal.
- Every doc edit must also update: the doc's Update log, `TASKS.md`, and `docs/00_STATUS.md`.
- Never delete checkmarks or completed items. Only append new updates and mark new items complete.
- Always run the relevant tests before pushing. CI must stay green.

## Canon links
- GitHub setup: `docs/40_GITHUB_SETUP.md`
- Routing guide: `docs/01_ROUTING_GUIDE.md`
- Lint and meta tests: `docs/21_LINT_AND_META_TESTS.md`
- Regression snapshots: `docs/23_REGRESSION_SNAPSHOTS.md`
- Status: `docs/00_STATUS.md`

---

## 1) Working style (non-negotiables)

### 1.1 Small batches
A batch should be one of:
- Create 1 new living doc
- Convert 1 source doc into MD (and optionally split)
- Add 1 new test suite or fixture batch

If a change touches many files, split it into multiple batches.

### 1.2 No checklist regressions
Never:
- Uncheck a completed task
- Remove completed docs from `docs/00_STATUS.md`
- Rewrite history in Update logs

Only:
- Add new lines
- Mark new items complete
- Add new sections as needed

### 1.3 Update logs are append-only, newest first
For this repo, Update logs are append-only, but we place the newest entry at the top of the list. Do not reorder older entries.

---

## 2) The standard batch sequence

For any batch, do these steps in order.

### Step A: Create or edit the primary doc(s)
- Create the new doc file under `docs/`
- Paste the standard header block
- Fill content
- Add an Update log entry with today's date

### Step B: Update the navigation state
Update these two files after every batch:
1) `TASKS.md`
- Mark the doc complete (checkbox)
- Add a new Update log entry (newest first)

2) `docs/00_STATUS.md`
- Add a new Update log entry (newest first)
- Move the doc from Next to Completed if applicable
- Update the "Next milestone" or "Next batch" lines if the plan changed

### Step C: Run checks locally
Run the smallest set of checks that are relevant, plus a quick sanity check:

Recommended minimum:
- Docs batch: no tests required, but make sure Markdown renders cleanly and links are correct
- Validator batch: `python -m pytest -q`

If snapshots are involved:
- Run the snapshot tests documented in `docs/23_REGRESSION_SNAPSHOTS.md`

### Step D: Commit, push, PR
- Commit with a clear message
- Push your branch
- Open or update a PR

See: `docs/40_GITHUB_SETUP.md`

---

## 3) Commit rules

### 3.1 Commit message shape
Prefer:
- `docs: add 41_DEV_WORKFLOW`
- `docs: update diagnostics contract`
- `tests: add changeset fixtures batch 4B`

Avoid:
- `updates`
- `fixes`
- anything vague

### 3.2 One purpose per commit (usually)
If a batch is one doc, one commit is fine. If a batch is code + fixtures + docs, split into 2 to 3 commits maximum.

---

## 4) PR checklist (copy-paste)

Before you merge:
- [ ] The primary doc(s) have correct header and Update log
- [ ] `TASKS.md` is updated and does not regress any completed tasks
- [ ] `docs/00_STATUS.md` matches reality (Completed vs Next)
- [ ] Links in the new doc resolve (relative links)
- [ ] CI is green

---

## 5) File rules (to avoid drift)

### 5.1 Keep `docs/` flat
No nested folders under `docs/`. Numbering is the navigation system.

### 5.2 One doc owns one contract
If you need to change a contract, change the single owning doc, then update other docs by linking, not duplicating.

### 5.3 Prefer "front doors" over giant files
If a doc grows too long:
- Keep a short front door doc
- Split detailed content into neighboring docs
- Keep links in both directions

---

## 6) Hand-off rule for generated artifacts

If a batch produces generated outputs (reports, snapshots, zips):
- Document where they live
- Document how to reproduce them
- Ensure generation is deterministic

See: `docs/23_REGRESSION_SNAPSHOTS.md`

---

## Update log
- 2026-01-26: Added day to day workflow: batch sequence, no checklist regressions, and PR checklist.
