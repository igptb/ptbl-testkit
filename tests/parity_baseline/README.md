# Parity baseline (Python oracle)

Last updated: 2026-01-27

Scope: Frozen Python JSON outputs used as the oracle baseline while migrating the validator to Rust.

## If you only read one thing
- During migration, Python is the oracle. Rust output is compared against these baseline JSON files.
- `workspace_fingerprint` is normalized to `__FINGERPRINT__` to avoid machine-dependent drift.

## Files
- `fixtures.json`: curated fixture list and metadata
- `python/10.4+v10_4_c/<fixture_id>/{interactive.json,commit.json}`: canonical baseline outputs

## How to use
- For any Rust micro-task, pick 1 to 5 fixture IDs from `fixtures.json`.
- Run Python validator and Rust validator on the same fixture root and compare JSON after applying the same normalizations.
