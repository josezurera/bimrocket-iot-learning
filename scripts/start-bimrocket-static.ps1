param(
    [string]$BimrocketRoot
)

$ErrorActionPreference = "Stop"

$courseRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$workspaceRoot = Split-Path $courseRoot -Parent

if ([string]::IsNullOrWhiteSpace($BimrocketRoot)) {
    $BimrocketRoot = Join-Path $workspaceRoot "bimrocket"
}

$webappRoot = Join-Path $BimrocketRoot "bimrocket-webapp\src\main\webapp"
$appFile = Join-Path $webappRoot "app.html"

if (-not (Test-Path $appFile)) {
    throw "No encuentro BIMROCKET en $webappRoot. Puedes pasar otra ruta con -BimrocketRoot C:\ruta\a\bimrocket"
}

Write-Host "Arrancando BIMROCKET estático..."
Write-Host "URL: http://127.0.0.1:8000/app.html"
Write-Host "Pulsa Ctrl+C para detenerlo."
Write-Host ""

Set-Location $webappRoot
python -m http.server 8000 --bind 127.0.0.1
