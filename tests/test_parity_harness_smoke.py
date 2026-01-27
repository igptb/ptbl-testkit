"""Smoke test for parity harness.

This test intentionally uses Python as the "rust" side so it can run
before Rust exists. It validates that:
  - baseline oracle loads
  - harness runs end-to-end
  - normalization and diff logic work

Once Rust exists, keep this test, but add a second smoke that runs Rust
on 1 fixture (or switch this one to Rust and keep a Python-as-Rust test separately).
"""

from __future__ import annotations

from tests.parity_harness import load_fixtures, repo_root_from_here, build_config, run_parity
import argparse


def test_parity_harness_smoke_python_as_rust():
    repo_root = repo_root_from_here()
    fixtures_path = repo_root / "tests" / "parity_baseline" / "fixtures.json"
    fixtures = load_fixtures(fixtures_path)

    # Pick 1 fixture to keep this fast and stable.
    fixture_id = fixtures[0]["id"]

    ns = argparse.Namespace(
        fixtures=[fixture_id],
        modes=["interactive"],
        oracle="baseline",
        schemas_dir="schemas/ptbl/2.6.19",
        max_diagnostics=200,
        baseline_version=None,
        ignore_validator_version=True,
        check_determinism=False,
        write_artifacts=False,
        rust_cmd=None,
        use_python_as_rust=True,
    )
    cfg = build_config(ns)

    rc = run_parity(
        fixtures=fixtures,
        fixture_ids=[fixture_id],
        modes=["interactive"],
        cfg=cfg,
    )
    assert rc == 0
