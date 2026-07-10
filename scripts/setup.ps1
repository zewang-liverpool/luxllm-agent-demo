param(
    [string]$PythonExe = "py",
    [string]$PythonVersion = "-3.11"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root ".venv"

if (-not (Test-Path (Join-Path $Venv "Scripts\python.exe"))) {
    $arguments = @()
    if ($PythonVersion) {
        $arguments += $PythonVersion
    }
    $arguments += @("-m", "venv", $Venv)
    & $PythonExe @arguments
}

$VenvPython = Join-Path $Venv "Scripts\python.exe"
& $VenvPython -m pip install --upgrade "pip==23.1.2"
& $VenvPython -m pip install -r (Join-Path $Root "requirements-dev.txt")

Write-Host "Environment ready: $VenvPython"
Write-Host "Next: & '$VenvPython' scripts/smoke_test.py"
