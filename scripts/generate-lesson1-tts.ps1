<#
.SYNOPSIS
Generate all missing TTS WAV files for lesson 1 using Gemini TTS.

.DESCRIPTION
This script is a PowerShell wrapper around scripts/generate_tts_gemini.py.

It expects GEMINI_API_KEY to be already set in the current PowerShell session:

    $env:GEMINI_API_KEY="YOUR_API_KEY"

By default it skips WAV files that already exist, so it is safe to run after
successfully generating block 01. It will continue with the missing blocks.

.EXAMPLE
cd C:\Users\josez\bimrocket-iot-learning
$env:GEMINI_API_KEY="YOUR_API_KEY"
.\scripts\generate-lesson1-tts.ps1

.EXAMPLE
# Regenerate everything, including existing WAV files
.\scripts\generate-lesson1-tts.ps1 -Force

.EXAMPLE
# Regenerate only block 03
.\scripts\generate-lesson1-tts.ps1 -Only 03 -Force
#>

[CmdletBinding()]
param(
    [switch]$Force,

    [ValidatePattern('^\d{1,2}$')]
    [string]$Only
)

$ErrorActionPreference = "Stop"

$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptsDir = Split-Path -Parent $ScriptPath
$RepoRoot = Split-Path -Parent $ScriptsDir
$PythonScript = Join-Path $RepoRoot "scripts\generate_tts_gemini.py"

if (-not $env:GEMINI_API_KEY) {
    Write-Error "GEMINI_API_KEY is not set. Run: `$env:GEMINI_API_KEY=`"YOUR_API_KEY`""
}

if (-not (Test-Path -LiteralPath $PythonScript)) {
    Write-Error "Python script not found: $PythonScript"
}

Set-Location -LiteralPath $RepoRoot

$ArgsList = @($PythonScript)

if ($Only) {
    $ArgsList += @("--only", $Only.PadLeft(2, "0"))
}

if ($Force) {
    $ArgsList += "--force"
}

Write-Host "Generating lesson 1 TTS audio..." -ForegroundColor Cyan
Write-Host "Repository: $RepoRoot"
Write-Host "Voice: Algieba"

python @ArgsList

Write-Host ""
Write-Host "Done. Audio folder:" -ForegroundColor Green
Write-Host (Join-Path $RepoRoot "slides\leccion-01\tts\audio")
