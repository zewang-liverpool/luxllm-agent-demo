param(
    [string]$PythonExe = "py",
    [string]$PythonVersion = "-3.11"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$VenvPython = Join-Path $Venv "Scripts\python.exe"

function Test-PythonCommand {
    param(
        [string]$Executable,
        [string[]]$Arguments = @()
    )
    try {
        & $Executable @Arguments --version *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

function Invoke-Checked {
    param(
        [string]$Executable,
        [string[]]$Arguments
    )
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Executable $($Arguments -join ' ')"
    }
}

if ((Test-Path $VenvPython) -and -not (Test-PythonCommand -Executable $VenvPython)) {
    Write-Warning "Existing .venv is broken or points to a missing Python installation; rebuilding it."
    Remove-Item -LiteralPath $Venv -Recurse -Force
}

if (-not (Test-Path $VenvPython)) {
    $candidates = @()
    if ($PythonVersion) {
        $candidates += ,@($PythonExe, $PythonVersion)
    }
    else {
        $candidates += ,@($PythonExe)
    }
    if ($PythonExe -eq "py") {
        foreach ($version in @("-3.12", "-3.11", "-3.10")) {
            if ($version -ne $PythonVersion) {
                $candidates += ,@("py", $version)
            }
        }
    }

    $selected = $null
    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        $args = @($candidate | Select-Object -Skip 1)
        if (Test-PythonCommand -Executable $exe -Arguments $args) {
            $selected = $candidate
            break
        }
    }
    if ($null -eq $selected) {
        throw "No supported Python 3.10-3.12 interpreter was found. Install Python or pass -PythonExe and -PythonVersion."
    }

    $selectedExe = $selected[0]
    $selectedArgs = @($selected | Select-Object -Skip 1)
    Write-Host "Creating .venv with: $selectedExe $($selectedArgs -join ' ')"
    Invoke-Checked -Executable $selectedExe -Arguments @($selectedArgs + @("-m", "venv", $Venv))
    if (-not (Test-PythonCommand -Executable $VenvPython)) {
        throw "Virtual environment creation failed: $Venv"
    }
}

Invoke-Checked -Executable $VenvPython -Arguments @("-m", "pip", "install", "--upgrade", "pip==23.1.2")
Invoke-Checked -Executable $VenvPython -Arguments @("-m", "pip", "install", "-r", (Join-Path $Root "requirements-dev.txt"))

Write-Host "Environment ready: $VenvPython"
Write-Host "Next: & '$VenvPython' scripts/smoke_test.py"
