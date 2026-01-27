# Generate requirements-ci.txt from the *current* (known-good) virtualenv.
# Run this from repo root inside your activated venv.
# Output is sorted to keep diffs stable.
#
# Usage (PowerShell):
#   .\.venv\Scripts\Activate.ps1
#   .\tools\gen_requirements_ci.ps1
#
# Then commit requirements-ci.txt.

$ErrorActionPreference = "Stop"

# Ensure we're at repo root (heuristic: tests/ exists)
if (-not (Test-Path ".\tests")) {
  throw "Run this from the repo root (expected .\tests\ to exist)."
}

# Make sure pytest imports (nice early failure if venv isn't active)
python -c "import pytest" | Out-Null

$lines = python -m pip freeze --exclude-editable
$sorted = $lines | Sort-Object
$sorted | Set-Content -Encoding ascii ".\requirements-ci.txt"

Write-Host ("Wrote requirements-ci.txt (" + $sorted.Count + " lines).") -ForegroundColor Green
