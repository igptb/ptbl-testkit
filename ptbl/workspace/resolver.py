from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from ptbl.errors import (
    ResolverError,
    RESOLVE_LOCK_MISSING,
    RESOLVE_UNRESOLVED_IMPORT,
    RESOLVE_CYCLE,
    RESOLVE_CONFLICT,
    RESOLVE_PATH_TRAVERSAL,
    RESOLVE_SOURCE_UNSUPPORTED,
)
from ptbl.workspace.loader import Workspace


@dataclass(frozen=True)
class ResolvedItem:
    key: str
    kind: str  # module | registry | git | url
    locked: bool
    meta: Dict[str, Any]


def _is_within(child: Path, parent: Path) -> bool:
    child = child.resolve()
    parent = parent.resolve()
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _resolve_local_path(workspace: Workspace, rel_path: str) -> Path:
    """
    Full containment check: join to workspace.root, resolve, ensure it stays under root.
    Also rejects absolute paths.
    Accepts either:
      - modules/auth.ptbl
      - modules/auth   (auto adds .ptbl)
    """
    if not isinstance(rel_path, str) or not rel_path.strip():
        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, "Local import path must be a non-empty string")

    raw = rel_path.strip()

    # Normalize to a Path without touching filesystem
    p = Path(raw)

    # Reject absolute paths immediately (C:\..., \\server\share\..., /etc/...)
    if p.is_absolute():
        raise ResolverError(RESOLVE_PATH_TRAVERSAL, f"Absolute path not allowed: {raw}")

    # Allow omitting .ptbl extension
    if p.suffix == "":
        p = p.with_suffix(".ptbl")

    abs_path = (workspace.root / p).resolve()

    if not _is_within(abs_path, workspace.root):
        raise ResolverError(RESOLVE_PATH_TRAVERSAL, f"Path traversal detected: {raw}")

    return abs_path


def _entry_modules_from_app(workspace: Workspace) -> List[str]:
    entry = workspace.app.get("entry_modules", [])
    if entry is None:
        entry = []
    if not isinstance(entry, list) or not all(isinstance(x, str) for x in entry):
        raise ValueError("app.ptbl: entry_modules must be a list of strings")

    # Deterministic order
    return sorted(entry, key=lambda s: s.lower())


def resolve_workspace(workspace: Workspace, mode: str) -> List[ResolvedItem]:
    if mode not in ("dev", "repro"):
        raise ValueError("mode must be dev or repro")

    if mode == "repro" and workspace.lock is None:
        raise ResolverError(RESOLVE_LOCK_MISSING, "Repro mode requires lock.ptbl")

    lock_resolved: Dict[str, Any] = {}
    if workspace.lock is not None:
        lock_resolved = workspace.lock.get("resolved", {}) or {}
        if not isinstance(lock_resolved, dict):
            raise ValueError("lock.ptbl: resolved must be a mapping")

    entry_module_ids = _entry_modules_from_app(workspace)

    # Conflict detection for registry imports: name -> set(versions)
    registry_requested: Dict[str, Set[str]] = {}

    resolved_items: List[ResolvedItem] = []
    visited_modules: Set[str] = set()
    visiting_stack: List[str] = []

    def add_resolved(item: ResolvedItem) -> None:
        resolved_items.append(item)

    def dfs_module(module_id: str) -> None:
        if module_id in visiting_stack:
            cycle = " -> ".join(visiting_stack + [module_id])
            raise ResolverError(RESOLVE_CYCLE, f"Cycle detected: {cycle}")

        if module_id in visited_modules:
            return

        spec = workspace.modules.get(module_id)
        if spec is None:
            raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Missing module_id: {module_id}")

        visiting_stack.append(module_id)

        # Resolve imports first (depth-first), deterministic order already applied in loader
        for imp in spec.imports:
            if imp.source == "local":
                abs_path = _resolve_local_path(workspace, imp.path or "")

                # Map absolute module file path to module_id by matching loaded modules
                target_id: Optional[str] = None
                for mid, mspec in workspace.modules.items():
                    if mspec.file_path.resolve() == abs_path:
                        target_id = mid
                        break

                if target_id is None:
                    raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Local import not found: {imp.path}")

                dfs_module(target_id)

            elif imp.source == "registry":
                name = imp.name or ""
                version = imp.version or ""
                registry_requested.setdefault(name, set()).add(version)

                locked = (mode == "repro")
                if locked:
                    lock_key = f"registry:{name}"
                    lock_entry = lock_resolved.get(lock_key)
                    if not isinstance(lock_entry, dict):
                        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Missing lock entry for {lock_key}")
                    pinned = lock_entry.get("pinned_version")
                    if pinned != version:
                        raise ResolverError(
                            RESOLVE_CONFLICT,
                            f"Registry version mismatch for {name}: requested {version} but lock has {pinned}",
                        )

                add_resolved(
                    ResolvedItem(
                        key=f"registry:{name}@{version}",
                        kind="registry",
                        locked=locked,
                        meta={"name": name, "version": version},
                    )
                )

            elif imp.source == "git":
                # Stubbed: record it, require lock entry in repro mode
                locked = (mode == "repro")
                url = imp.url or ""
                ref = imp.ref

                if locked:
                    lock_key = f"git:{url}"
                    lock_entry = lock_resolved.get(lock_key)
                    if not isinstance(lock_entry, dict):
                        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Missing lock entry for {lock_key}")
                    if not isinstance(lock_entry.get("commit"), str) or not lock_entry.get("commit"):
                        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Lock entry missing commit for {lock_key}")

                add_resolved(
                    ResolvedItem(
                        key=f"git:{url}#{ref or 'unknown'}",
                        kind="git",
                        locked=locked,
                        meta={"url": url, "ref": ref},
                    )
                )

            elif imp.source == "url":
                locked = (mode == "repro")
                url = imp.url or ""

                if locked:
                    lock_key = f"url:{url}"
                    lock_entry = lock_resolved.get(lock_key)
                    if not isinstance(lock_entry, dict):
                        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Missing lock entry for {lock_key}")
                    if not isinstance(lock_entry.get("sha256"), str) or not lock_entry.get("sha256"):
                        raise ResolverError(RESOLVE_UNRESOLVED_IMPORT, f"Lock entry missing sha256 for {lock_key}")

                add_resolved(
                    ResolvedItem(
                        key=f"url:{url}",
                        kind="url",
                        locked=locked,
                        meta={"url": url},
                    )
                )

            else:
                raise ResolverError(RESOLVE_SOURCE_UNSUPPORTED, f"Unsupported source: {imp.source}")

        # Record module itself after imports
        add_resolved(
            ResolvedItem(
                key=f"module:{spec.module_id}",
                kind="module",
                locked=(mode == "repro"),
                meta={"module_id": spec.module_id, "file": str(spec.file_path)},
            )
        )

        visiting_stack.pop()
        visited_modules.add(module_id)

    # Walk all entry modules deterministically
    for mid in entry_module_ids:
        dfs_module(mid)

    # Registry conflict check: if any name has >1 requested version, error
    for name, versions in registry_requested.items():
        if len(versions) > 1:
            raise ResolverError(RESOLVE_CONFLICT, f"Registry version conflict for {name}: {sorted(versions)}")

    # Deduplicate items by (kind, key) deterministically, then sort deterministically
    seen: Set[tuple[str, str]] = set()
    unique: List[ResolvedItem] = []
    for item in resolved_items:
        k = (item.kind, item.key)
        if k in seen:
            continue
        seen.add(k)
        unique.append(item)

    unique_sorted = sorted(unique, key=lambda x: (x.kind, x.key.lower()))
    return unique_sorted
