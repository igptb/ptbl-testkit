"""PTBL parity harness (Python oracle vs Rust)

Purpose:
  - Compare Rust validator JSON output to the frozen Python baseline outputs
    under tests/parity_baseline/.
  - Normalize only what we allow to differ during migration:
      * schema-tier diagnostic message text (tier == "schema")
      * (optionally) validator_version while Rust is under development

This file is used both as a CLI tool and as a library from tests.

Typical usage (once Rust CLI exists):
  python tests/parity_harness.py --fixtures neg_schema_invalid --modes interactive --oracle baseline \
    --rust-cmd '["cargo","run","-q","-p","ptbl_cli","--","validate","{root}","--mode","{mode}","--format","json","--schemas-dir","{schemas_dir}","--max-diagnostics","{max_diagnostics}"]'

Until Rust exists, you can self-test the harness by running Python as the "rust" side:
  python tests/parity_harness.py --fixtures neg_schema_invalid --modes interactive --oracle baseline --use-python-as-rust
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


TIER_RANK = {"schema": 0, "semantic": 1, "policy": 2}
SEV_RANK = {"error": 0, "warning": 1, "info": 2}


@dataclass(frozen=True)
class ParityConfig:
    repo_root: Path
    schemas_dir: Path
    max_diagnostics: int
    oracle: str  # "baseline" | "live"
    baseline_version: str
    ignore_validator_version: bool
    check_determinism: bool
    write_artifacts: bool
    rust_cmd_template: Optional[List[str]]  # list of tokens with placeholders
    use_baseline_as_rust: bool


def repo_root_from_here() -> Path:
    # tests/parity_harness.py -> repo root
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def stable_dir_sha256(root: Path) -> str:
    """Stable content hash of a directory tree.
    Hash includes relative path + NUL + file bytes for each file, in sorted path order.
    """
    h = hashlib.sha256()
    if not root.exists():
        raise FileNotFoundError(root)
    for p in sorted([p for p in root.rglob("*") if p.is_file()], key=lambda x: x.as_posix()):
        rel = p.relative_to(root).as_posix().encode("utf-8")
        h.update(rel)
        h.update(b"\x00")
        h.update(p.read_bytes())
        h.update(b"\x00")
    return h.hexdigest()


def load_fixtures(fixtures_json_path: Path) -> List[Dict[str, Any]]:
    data = read_json(fixtures_json_path)
    fixtures = data.get("fixtures", [])
    if not isinstance(fixtures, list):
        raise ValueError("fixtures.json missing 'fixtures' list")
    return fixtures


def detect_baseline_version(baseline_root: Path) -> str:
    py_root = baseline_root / "python"
    if not py_root.exists():
        raise FileNotFoundError(f"Missing baseline python folder: {py_root}")
    versions = [p.name for p in py_root.iterdir() if p.is_dir()]
    if len(versions) != 1:
        raise ValueError(f"Expected exactly 1 baseline version folder under {py_root}, found: {versions}")
    return versions[0]


def python_cmd_template() -> List[str]:
    # Matches ptbl/cli.py usage.
    return [
        sys.executable,
        "-m",
        "ptbl.cli",
        "validate",
        "{root}",
        "--mode",
        "{mode}",
        "--format",
        "json",
        "--schemas-dir",
        "{schemas_dir}",
        "--max-diagnostics",
        "{max_diagnostics}",
    ]


def parse_rust_cmd(arg: Optional[str], use_python_as_rust: bool) -> Optional[List[str]]:
    if use_python_as_rust:
        return python_cmd_template()

    if arg is None:
        return None

    s = arg.strip()
    if s.startswith("["):
        # JSON array of tokens
        try:
            tokens = json.loads(s)
        except Exception as e:
            raise ValueError(f"--rust-cmd JSON parse failed: {e}") from e
        if not isinstance(tokens, list) or not all(isinstance(t, str) for t in tokens):
            raise ValueError("--rust-cmd must be a JSON array of strings")
        return tokens

    # Fallback: treat as a single shell command string.
    # On Windows this can be convenient, but quoting rules can be surprising.
    # We keep this as an escape hatch.
    return [s]


def run_validator_cmd(
    cmd_template: List[str],
    *,
    root: Path,
    mode: str,
    schemas_dir: Path,
    max_diagnostics: int,
    cwd: Path,
) -> Dict[str, Any]:
    # Substitute placeholders into a list of tokens
    tokens: List[str] = []
    for t in cmd_template:
        tokens.append(
            t.format(
                root=str(root),
                mode=mode,
                schemas_dir=str(schemas_dir),
                max_diagnostics=str(max_diagnostics),
            )
        )

    # If the template is a single string (shell fallback), run with shell=True
    if len(tokens) == 1 and (" " in tokens[0] or "\t" in tokens[0]):
        cp = subprocess.run(
            tokens[0],
            cwd=str(cwd),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    else:
        cp = subprocess.run(
            tokens,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

    if cp.returncode not in (0, 1):
        raise RuntimeError(
            "Validator command failed unexpectedly.\n"
            f"Return code: {cp.returncode}\n"
            f"STDERR:\n{cp.stderr}"
        )

    try:
        return json.loads(cp.stdout)
    except Exception as e:
        raise RuntimeError(
            "Validator did not emit valid JSON.\n"
            f"STDOUT (first 2000 chars):\n{cp.stdout[:2000]}\n"
            f"STDERR (first 2000 chars):\n{cp.stderr[:2000]}"
        ) from e


def normalize_result(raw: Dict[str, Any], *, ignore_validator_version: bool) -> Dict[str, Any]:
    """Normalize a validation result for parity comparison."""
    obj = json.loads(json.dumps(raw))  # deep copy

    if ignore_validator_version and "validator_version" in obj:
        obj["validator_version"] = "<ignored>"

    # Normalize schema-tier message text
    diags = obj.get("diagnostics", [])
    if isinstance(diags, list):
        for d in diags:
            if isinstance(d, dict) and d.get("tier") == "schema":
                if "message" in d:
                    d["message"] = "<schema_message>"

    # Deterministic sort of diagnostics (using normalized message)
    def diag_key(d: Dict[str, Any]) -> Tuple[int, int, str, str, str, str]:
        tier = str(d.get("tier", ""))
        sev = str(d.get("severity", ""))
        return (
            TIER_RANK.get(tier, 99),
            SEV_RANK.get(sev, 99),
            str(d.get("file", "")),
            str(d.get("path", "")),
            str(d.get("rule_id", "")),
            str(d.get("message", "")),
        )

    if isinstance(diags, list):
        obj["diagnostics"] = sorted([d for d in diags if isinstance(d, dict)], key=diag_key)

    # Deterministic sort of fix_actions if present
    fixes = obj.get("fix_actions", [])
    if isinstance(fixes, list):
        def fix_key(f: Dict[str, Any]) -> Tuple[str, str, str, str]:
            return (
                str(f.get("op", "")),
                str(f.get("file", "")),
                str(f.get("json_pointer", "")),
                str(f.get("reason_rule_id", "")),
            )
        obj["fix_actions"] = sorted([f for f in fixes if isinstance(f, dict)], key=fix_key)

    return obj


def first_diff_path(a: Any, b: Any, path: str = "") -> Optional[str]:
    """Return the first differing JSON path, or None if equal."""
    if type(a) != type(b):
        return path or "$"

    if isinstance(a, dict):
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        if a_keys != b_keys:
            return (path or "$") + f".<keys differ a={sorted(a_keys)} b={sorted(b_keys)}>"
        for k in sorted(a.keys()):
            p = f"{path}.{k}" if path else f"$.{k}"
            d = first_diff_path(a[k], b[k], p)
            if d is not None:
                return d
        return None

    if isinstance(a, list):
        if len(a) != len(b):
            return (path or "$") + f".<len differ a={len(a)} b={len(b)}>"
        for i, (x, y) in enumerate(zip(a, b)):
            p = f"{path}[{i}]" if path else f"$[{i}]"
            d = first_diff_path(x, y, p)
            if d is not None:
                return d
        return None

    if a != b:
        return path or "$"

    return None


def load_oracle_baseline(
    cfg: ParityConfig, fixture_id: str, mode: str
) -> Dict[str, Any]:
    path = (
        cfg.repo_root
        / "tests"
        / "parity_baseline"
        / "python"
        / cfg.baseline_version
        / fixture_id
        / f"{mode}.json"
    )
    if not path.exists():
        raise FileNotFoundError(f"Missing baseline oracle file: {path}")
    return read_json(path)


def run_live_python_oracle(
    cfg: ParityConfig, fixture_root: Path, mode: str
) -> Dict[str, Any]:
    cmd = python_cmd_template()
    return run_validator_cmd(
        cmd,
        root=fixture_root,
        mode=mode,
        schemas_dir=cfg.schemas_dir,
        max_diagnostics=cfg.max_diagnostics,
        cwd=cfg.repo_root,
    )


def run_rust_candidate(
    cfg: ParityConfig,
    fixture_id: str,
    fixture_root: Path,
    mode: str,
) -> Dict[str, Any]:
    if cfg.use_baseline_as_rust:
        # Harness self-test mode: treat baseline oracle output as the Rust candidate.
        return load_oracle_baseline(cfg, fixture_id, mode)

    if cfg.rust_cmd_template is None:
        raise ValueError(
            "Rust command not configured. Provide --rust-cmd. (Tip: --use-python-as-rust makes the Rust side read baseline artifacts for a quick self-test.)"
        )
    return run_validator_cmd(
        cfg.rust_cmd_template,
        root=fixture_root,
        mode=mode,
        schemas_dir=cfg.schemas_dir,
        max_diagnostics=cfg.max_diagnostics,
        cwd=cfg.repo_root,
    )


def compare_one(
    cfg: ParityConfig,
    fixture: Dict[str, Any],
    mode: str,
    *,
    artifacts_root: Optional[Path],
) -> Tuple[bool, str]:
    fixture_id = fixture["id"]
    fixture_root = cfg.repo_root / fixture["fixture_root"]

    # Optional fixture hash check (warn only)
    try:
        got = stable_dir_sha256(fixture_root)
        expected = fixture.get("content_sha256", "")
        if expected and got != expected:
            print(
                f"Warning: fixture content hash differs for {fixture_id}. "
                f"baseline={expected} current={got}"
            )
    except Exception as e:
        print(f"Warning: could not hash fixture {fixture_id}: {e}")

    if cfg.oracle == "baseline":
        oracle_raw = load_oracle_baseline(cfg, fixture_id, mode)
    else:
        oracle_raw = run_live_python_oracle(cfg, fixture_root, mode)

    rust_raw = run_rust_candidate(cfg, fixture_id, fixture_root, mode)

    if cfg.check_determinism:
        rust_raw_2 = run_rust_candidate(cfg, fixture_id, fixture_root, mode)
        if json.dumps(rust_raw, sort_keys=True) != json.dumps(rust_raw_2, sort_keys=True):
            return False, f"{fixture_id}:{mode} rust output is not deterministic across two runs"

    oracle = normalize_result(oracle_raw, ignore_validator_version=cfg.ignore_validator_version)
    rust = normalize_result(rust_raw, ignore_validator_version=cfg.ignore_validator_version)

    diff = first_diff_path(oracle, rust)
    if diff is None:
        if cfg.write_artifacts and artifacts_root is not None:
            write_json(artifacts_root / fixture_id / f"{mode}_oracle.normalized.json", oracle)
            write_json(artifacts_root / fixture_id / f"{mode}_rust.normalized.json", rust)
        return True, f"{fixture_id}:{mode} OK"

    # Write artifacts on failure for debugging
    if artifacts_root is not None:
        write_json(artifacts_root / fixture_id / f"{mode}_oracle.raw.json", oracle_raw)
        write_json(artifacts_root / fixture_id / f"{mode}_rust.raw.json", rust_raw)
        write_json(artifacts_root / fixture_id / f"{mode}_oracle.normalized.json", oracle)
        write_json(artifacts_root / fixture_id / f"{mode}_rust.normalized.json", rust)

    # Include a small value preview for the first differing path
    preview = ""
    try:
        preview = f" (first diff at {diff})"
    except Exception:
        pass
    return False, f"{fixture_id}:{mode} MISMATCH{preview}"


def run_parity(
    *,
    fixtures: Sequence[Dict[str, Any]],
    fixture_ids: Sequence[str],
    modes: Sequence[str],
    cfg: ParityConfig,
) -> int:
    selected = [f for f in fixtures if f.get("id") in set(fixture_ids)] if fixture_ids else list(fixtures)
    if not selected:
        print("No fixtures selected.")
        return 2

    # Set up artifacts output
    artifacts_root = None
    if cfg.write_artifacts:
        ts = os.environ.get("PTBL_PARITY_RUN_ID") or __import__("datetime").datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        artifacts_root = cfg.repo_root / "tests" / "parity_runs" / ts

    any_fail = False
    for fx in selected:
        fx_modes = fx.get("modes", ["interactive", "commit"])
        for m in modes:
            if m not in fx_modes:
                continue
            ok, msg = compare_one(cfg, fx, m, artifacts_root=artifacts_root)
            print(msg)
            if not ok:
                any_fail = True

    return 1 if any_fail else 0


def build_config(args: argparse.Namespace) -> ParityConfig:
    repo_root = repo_root_from_here()

    baseline_root = repo_root / "tests" / "parity_baseline"
    baseline_version = args.baseline_version or detect_baseline_version(baseline_root)

    schemas_dir = Path(args.schemas_dir)
    if not schemas_dir.is_absolute():
        schemas_dir = repo_root / schemas_dir

    rust_cmd_template = parse_rust_cmd(args.rust_cmd, args.use_python_as_rust)

    return ParityConfig(
        repo_root=repo_root,
        schemas_dir=schemas_dir,
        max_diagnostics=args.max_diagnostics,
        oracle=args.oracle,
        baseline_version=baseline_version,
        ignore_validator_version=args.ignore_validator_version,
        check_determinism=args.check_determinism,
        write_artifacts=args.write_artifacts,
        rust_cmd_template=rust_cmd_template,
        use_baseline_as_rust=args.use_python_as_rust,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", nargs="*", default=[], help="Fixture IDs to run (default: all curated)")
    p.add_argument("--modes", nargs="*", default=["interactive", "commit"], help="Modes: interactive commit")
    p.add_argument("--oracle", choices=["baseline", "live"], default="baseline", help="Oracle source")
    p.add_argument("--schemas-dir", default="schemas/ptbl/2.6.19", help="Schemas directory")
    p.add_argument("--max-diagnostics", type=int, default=200, help="Max diagnostics")
    p.add_argument("--baseline-version", default=None, help="Override baseline version folder name")
    p.add_argument("--ignore-validator-version", action="store_true", default=True, help="Ignore validator_version field")
    p.add_argument("--no-ignore-validator-version", dest="ignore_validator_version", action="store_false")
    p.add_argument("--check-determinism", action="store_true", default=False, help="Run Rust twice and require identical output")
    p.add_argument("--write-artifacts", action="store_true", default=True, help="Write debug artifacts to tests/parity_runs/")
    p.add_argument("--no-write-artifacts", dest="write_artifacts", action="store_false")
    p.add_argument("--rust-cmd", default=None, help="Rust command template as JSON array of tokens, or a shell string")
    p.add_argument("--use-python-as-rust", action="store_true", default=False, help="Self-test: run Python as Rust side")
    args = p.parse_args(list(argv) if argv is not None else None)

    cfg = build_config(args)

    fixtures_path = cfg.repo_root / "tests" / "parity_baseline" / "fixtures.json"
    fixtures = load_fixtures(fixtures_path)

    # Validate modes
    modes = []
    for m in args.modes:
        if m not in ("interactive", "commit"):
            raise ValueError(f"Invalid mode: {m}")
        modes.append(m)

    return run_parity(
        fixtures=fixtures,
        fixture_ids=args.fixtures,
        modes=modes,
        cfg=cfg,
    )


if __name__ == "__main__":
    raise SystemExit(main())
