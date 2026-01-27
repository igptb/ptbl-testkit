# Curated parity fixture set

Last updated: 2026-01-27

Scope: This file defines the curated fixture set used for Rust parity during the migration.

## If you only read one thing
The canonical curated set is the list in `tests/parity_baseline/fixtures.json`.

During the migration:
- The frozen Python oracle outputs live under `tests/parity_baseline/python/<baseline_version>/...`
- The parity harness compares Rust output to that frozen oracle.
- Schema-tier diagnostic message wording is allowed to differ. Structure and IDs must match.

## Why this exists
We want a small, stable, high-signal fixture set to gate every Rust micro-task.
The set starts at 10 fixtures and grows later if needed.
