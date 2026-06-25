$ErrorActionPreference = "Stop"

$courseRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$workspaceRoot = Split-Path $courseRoot -Parent
$defaultBimrocketRoot = Join-Path $workspaceRoot "bimrocket"

function Test-CommandAvailable {
    param([Parameter(Mandatory = $true)][string]$Name)

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        Write-Host "[ERROR] No encuentro '$Name' en el PATH." -ForegroundColor Red
        return $false
    }

    Write-Host "[OK] $Name -> $($command.Source)" -ForegroundColor Green
    return $true
}

$ok = $true
$ok = (Test-CommandAvailable "git") -and $ok
$ok = (Test-CommandAvailable "python") -and $ok

if (Test-Path $defaultBimrocketRoot) {
    Write-Host "[OK] Repositorio BIMROCKET encontrado en $defaultBimrocketRoot" -ForegroundColor Green
} else {
    Write-Host "[ERROR] No encuentro BIMROCKET en $defaultBimrocketRoot" -ForegroundColor Red
    Write-Host "Clónalo junto al curso con:"
    Write-Host "  git clone https://github.com/bimrocket/bimrocket.git"
    $ok = $false
}

if ($ok) {
    Write-Host ""
    Write-Host "Entorno listo para continuar el curso." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Falta preparar algo antes de continuar." -ForegroundColor Yellow
exit 1
