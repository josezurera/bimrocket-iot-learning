<#
.SYNOPSIS
Build lesson 1 MP4 video from Marp slides and Algieba TTS audio blocks.

.EXAMPLE
cd C:\Users\josez\bimrocket-iot-learning
.\scripts\build-lesson1-video.ps1

.EXAMPLE
.\scripts\build-lesson1-video.ps1 -Force
#>

[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptsDir = Split-Path -Parent $ScriptPath
$RepoRoot = Split-Path -Parent $ScriptsDir
$PythonScript = Join-Path $RepoRoot "scripts\build-lesson1-video.py"

if (-not (Test-Path -LiteralPath $PythonScript)) {
    Write-Error "Python script not found: $PythonScript"
}

Set-Location -LiteralPath $RepoRoot

$ArgsList = @($PythonScript)
if ($Force) {
    $ArgsList += "--force"
}

python @ArgsList
