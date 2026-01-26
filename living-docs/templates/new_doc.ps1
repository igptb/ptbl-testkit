param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][string]$Title
)

$today = "2026-01-24"

$content = @"
# $Title

Last updated: $today

Scope: <what this doc covers, and what it does NOT cover>

## If you only read one thing
- TODO: Fill this doc.

## Update log
- $today: Created skeleton.
"@

New-Item -ItemType File -Force -Path $Path | Out-Null
Set-Content -Path $Path -Value $content -Encoding utf8
Write-Host "Created $Path"
