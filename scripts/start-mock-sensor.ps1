$ErrorActionPreference = "Stop"

$courseRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$sensorRoot = Join-Path $courseRoot "examples\mock-sensor"
$serverFile = Join-Path $sensorRoot "server.py"

if (-not (Test-Path $serverFile)) {
    throw "No encuentro el sensor simulado en $serverFile"
}

Write-Host "Arrancando sensor REST simulado..."
Write-Host "URL: http://127.0.0.1:8001/api/rooms/A-101"
Write-Host "Pulsa Ctrl+C para detenerlo."
Write-Host ""

Set-Location $sensorRoot
python server.py
