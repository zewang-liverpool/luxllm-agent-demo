param(
    [switch]$Apply,
    [string]$Destination = "archive/legacy-untracked-20260711"
)

$ErrorActionPreference = "Stop"
$Root = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$ArchiveRoot = [System.IO.Path]::GetFullPath((Join-Path $Root $Destination))
$RootPrefix = $Root.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
$ArchivePrefix = $ArchiveRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

if (-not $ArchivePrefix.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Archive destination must remain inside the repository: $ArchiveRoot"
}

$Files = @(git -C $Root ls-files --others --exclude-standard)
if ($LASTEXITCODE -ne 0) {
    throw "git ls-files failed"
}

Write-Host "Untracked files found: $($Files.Count)"
Write-Host "Archive destination: $ArchiveRoot"

if (-not $Apply) {
    $Files | ForEach-Object { Write-Host "  $_" }
    Write-Host "Dry run only. Re-run with -Apply after reviewing the list."
    exit 0
}

New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null
$Manifest = Join-Path $ArchiveRoot "manifest.txt"
$Files | Set-Content -Encoding utf8 $Manifest

foreach ($RelativePath in $Files) {
    $Source = [System.IO.Path]::GetFullPath((Join-Path $Root $RelativePath))
    $Target = [System.IO.Path]::GetFullPath((Join-Path $ArchiveRoot $RelativePath))
    if (-not $Source.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Source escaped repository root: $Source"
    }
    if (-not $Target.StartsWith($ArchivePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Target escaped archive root: $Target"
    }
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        continue
    }
    $TargetParent = Split-Path -Parent $Target
    New-Item -ItemType Directory -Path $TargetParent -Force | Out-Null
    Move-Item -LiteralPath $Source -Destination $Target
}

Write-Host "Archived $($Files.Count) files. Manifest: $Manifest"
