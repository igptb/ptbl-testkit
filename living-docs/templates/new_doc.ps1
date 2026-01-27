<# 
Creates a new living-docs Markdown file using templates/DOC_HEADER_TEMPLATE.md.

Usage (from repo root):
  pwsh -File living-docs/templates/new_doc.ps1 -Name "docs/16_SOMETHING.md" -Title "Something"

Notes:
- Writes the file relative to repo root.
- Will NOT overwrite an existing file.
- Ensures directories exist.
#>

param(
  [Parameter(Mandatory=$true)]
  [string]$Name,

  [Parameter(Mandatory=$false)]
  [string]$Title = ""
)

$ErrorActionPreference = "Stop"

# Resolve repo root as the parent of this script's directory (templates/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")

$TemplatePath = Join-Path $RepoRoot "living-docs\templates\DOC_HEADER_TEMPLATE.md"
if (!(Test-Path $TemplatePath)) {
  throw "Template not found: $TemplatePath"
}

# Normalize path separators and remove leading .\ if present
$RelPath = $Name.Trim()
$RelPath = $RelPath -replace "^[.\\\/]+",""
$OutPath = Join-Path $RepoRoot $RelPath

if (Test-Path $OutPath) {
  throw "Refusing to overwrite existing file: $OutPath"
}

# Ensure destination directory exists
$OutDir = Split-Path -Parent $OutPath
if ($OutDir -and !(Test-Path $OutDir)) {
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
}

# Read template
$Content = Get-Content -Raw -Path $TemplatePath

# Stamp date
$Today = (Get-Date).ToString("yyyy-MM-dd")
$Content = $Content -replace "<YYYY-MM-DD>", $Today

# Title replace (optional)
if ($Title.Trim().Length -gt 0) {
  $EscTitle = [regex]::Escape("<TITLE>")
  $Content = [regex]::Replace($Content, $EscTitle, $Title.Trim(), 1)
}

# Create file (UTF8 without BOM to keep diffs clean)
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OutPath, $Content, $Utf8NoBom)

Write-Host "Created: $OutPath"
