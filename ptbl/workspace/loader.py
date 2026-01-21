from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ptbl.errors import ResolverError, RESOLVE_PATH_TRAVERSAL


@dataclass(frozen=True)
class ImportSpec:
    source: str  # local | git | registry | url
    path: Optional[str] = None      # for local
    name: Optional[str] = None      # for registry
    version: Optional[str] = None   # for registry
    url: Optional[str] = None       # for git/url
    ref: Optional[str] = None       # for git
    commit: Optional[str] = None    # for git (optional)
    raw: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ModuleSpec:
    module_id: str
    file_path: Path
    imports: Tuple[ImportSpec, ...]


@dataclass(frozen=True)
class Workspace:
    root: Path
    app_path: Path
    lock_path: Optional[Path]
    module_paths: Tuple[Path, ...]
    integration_paths: Tuple[Path, ...]

    app: Dict[str, Any]
    lock: Optional[Dict[str, Any]]
    modules: Dict[str, ModuleSpec]
    integrations: Dict[str, Dict[str, Any]]


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"PTBL/YAML must be a mapping at top level: {path}")
    return data


def _sorted_glob(dir_path: Path, pattern: str) -> List[Path]:
    if not dir_path.exists():
        return []
    return sorted([p for p in dir_path.glob(pattern) if p.is_file()], key=lambda p: str(p).lower())


def _validate_local_relpath(rel_path: str) -> None:
    p = Path(rel_path)

    # Reject absolute paths (C:\..., \\server\share\..., /etc/...)
    if p.is_absolute():
        raise ResolverError(RESOLVE_PATH_TRAVERSAL, f"Absolute local import path not allowed: {rel_path}")

    # Reject any '..' segment (basic traversal). Resolver will still do the full root containment check later.
    parts = p.parts
    if any(part == ".." for part in parts):
        raise ResolverError(RESOLVE_PATH_TRAVERSAL, f"Path traversal segment '..' not allowed: {rel_path}")

    # Reject empty or weird paths
    if rel_path.strip() == "":
        raise ResolverError(RESOLVE_PATH_TRAVERSAL, "Empty local import path not allowed")


def _parse_import(obj: Any) -> ImportSpec:
    if not isinstance(obj, dict):
        raise ValueError("import entry must be a mapping")

    source = obj.get("source")
    if source not in ("local", "git", "registry", "url"):
        raise ValueError("import.source must be one of: local, git, registry, url")

    raw = dict(obj)

    if source == "local":
        path = obj.get("path")
        if not isinstance(path, str) or not path:
            raise ValueError("local import requires non-empty string 'path'")

        _validate_local_relpath(path)
        return ImportSpec(source=source, path=path, raw=raw)

    if source == "registry":
        name = obj.get("name")
        version = obj.get("version")
        if not isinstance(name, str) or not name:
            raise ValueError("registry import requires non-empty string 'name'")
        if not isinstance(version, str) or not version:
            raise ValueError("registry import requires non-empty string 'version'")
        return ImportSpec(source=source, name=name, version=version, raw=raw)

    if source == "git":
        url = obj.get("url")
        ref = obj.get("ref")
        commit = obj.get("commit")
        if not isinstance(url, str) or not url:
            raise ValueError("git import requires non-empty string 'url'")
        if ref is not None and not isinstance(ref, str):
            raise ValueError("git import 'ref' must be string if present")
        if commit is not None and not isinstance(commit, str):
            raise ValueError("git import 'commit' must be string if present")
        return ImportSpec(source=source, url=url, ref=ref, commit=commit, raw=raw)

    if source == "url":
        url = obj.get("url")
        if not isinstance(url, str) or not url:
            raise ValueError("url import requires non-empty string 'url'")
        return ImportSpec(source=source, url=url, raw=raw)

    raise ValueError("unreachable")


def _parse_module(path: Path) -> ModuleSpec:
    data = _read_yaml(path)

    module_id = data.get("module_id")
    if not isinstance(module_id, str) or not module_id:
        raise ValueError(f"{path}: module_id must be a non-empty string")

    imports_raw = data.get("imports", [])
    if imports_raw is None:
        imports_raw = []
    if not isinstance(imports_raw, list):
        raise ValueError(f"{path}: imports must be a list")

    imports: List[ImportSpec] = []
    for item in imports_raw:
        imports.append(_parse_import(item))

    # Deterministic order inside module spec
    imports_sorted = sorted(
        imports,
        key=lambda i: (
            i.source or "",
            i.path or "",
            i.name or "",
            i.version or "",
            i.url or "",
            i.ref or "",
            i.commit or "",
        ),
    )

    return ModuleSpec(module_id=module_id, file_path=path, imports=tuple(imports_sorted))


def load_workspace(root: str | Path) -> Workspace:
    root_path = Path(root).resolve()

    app_path = root_path / "app.ptbl"
    lock_path = root_path / "lock.ptbl"
    modules_dir = root_path / "modules"
    integrations_dir = root_path / "integrations"

    module_paths = tuple(_sorted_glob(modules_dir, "*.ptbl"))
    integration_paths = tuple(_sorted_glob(integrations_dir, "*.ptbl"))

    app = _read_yaml(app_path)
    lock = _read_yaml(lock_path) if lock_path.exists() else None

    modules: Dict[str, ModuleSpec] = {}
    for p in module_paths:
        spec = _parse_module(p)
        if spec.module_id in modules:
            raise ValueError(f"Duplicate module_id '{spec.module_id}' in {p}")
        modules[spec.module_id] = spec

    integrations: Dict[str, Dict[str, Any]] = {}
    for p in integration_paths:
        integrations[p.stem] = _read_yaml(p)

    return Workspace(
        root=root_path,
        app_path=app_path,
        lock_path=lock_path if lock_path.exists() else None,
        module_paths=module_paths,
        integration_paths=integration_paths,
        app=app,
        lock=lock,
        modules=modules,
        integrations=integrations,
    )
