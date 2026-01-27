"""Curated parity fixture set invariants.

This test codifies the current expectation that the curated parity set is 10 fixtures.
If you intentionally grow the set, change the expected count and update
tests/parity_baseline/CURATED_SET.md.
"""

from __future__ import annotations

from pathlib import Path

from tests.parity_harness import load_fixtures, repo_root_from_here


def test_curated_parity_set_has_expected_count_and_unique_ids():
    repo_root = repo_root_from_here()
    fixtures_path = repo_root / "tests" / "parity_baseline" / "fixtures.json"
    fixtures = load_fixtures(fixtures_path)

    assert len(fixtures) == 10, "Curated parity set should start at 10 fixtures"
    ids = [f["id"] for f in fixtures]
    assert len(ids) == len(set(ids)), "Fixture IDs must be unique"

    # Basic shape checks
    for f in fixtures:
        assert "fixture_root" in f
        fx_root = repo_root / f["fixture_root"]
        assert fx_root.exists(), f"fixture_root missing on disk: {fx_root}"
