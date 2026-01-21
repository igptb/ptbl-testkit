from pathlib import Path
import pytest

from ptbl.errors import (
    ResolverError,
    RESOLVE_LOCK_MISSING,
    RESOLVE_CYCLE,
    RESOLVE_CONFLICT,
    RESOLVE_PATH_TRAVERSAL,
)
from ptbl.workspace.loader import load_workspace
from ptbl.workspace.resolver import resolve_workspace


def test_deterministic_resolution_chain():
    ws = load_workspace(Path("fixtures/phase1/chain"))
    first = resolve_workspace(ws, mode="dev")
    for _ in range(20):
        again = resolve_workspace(ws, mode="dev")
        assert again == first


def test_repro_mode_requires_lock():
    ws = load_workspace(Path("fixtures/phase1/no_lock"))
    with pytest.raises(ResolverError) as exc:
        resolve_workspace(ws, mode="repro")
    assert exc.value.rule_id == RESOLVE_LOCK_MISSING


def test_cycle_detected():
    ws = load_workspace(Path("fixtures/phase1/cycle"))
    with pytest.raises(ResolverError) as exc:
        resolve_workspace(ws, mode="dev")
    assert exc.value.rule_id == RESOLVE_CYCLE


def test_conflict_detected():
    ws = load_workspace(Path("fixtures/phase1/conflict"))
    with pytest.raises(ResolverError) as exc:
        resolve_workspace(ws, mode="dev")
    assert exc.value.rule_id == RESOLVE_CONFLICT


def test_path_traversal_rejected_in_loader():
    # Path traversal is rejected during load_workspace() because imports are parsed there.
    with pytest.raises(ResolverError) as exc:
        load_workspace(Path("fixtures/phase1/path_traversal"))
    assert exc.value.rule_id == RESOLVE_PATH_TRAVERSAL


def test_diamond_dedupes_shared_dependency():
    # This assumes your diamond fixture uses module ids: a, b, c, d
    ws = load_workspace(Path("fixtures/phase1/diamond"))
    result = resolve_workspace(ws, mode="dev")

    d_entries = [r for r in result if r.key == "module:d"]
    assert len(d_entries) == 1
