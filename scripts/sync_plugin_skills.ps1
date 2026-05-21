# Copy canonical skill into the marketplace plugin bundle (release-time only).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Src = Join-Path $Root ".claude\skills\ros2-doctor"
$Dest = Join-Path $Root "plugins\ros2-doctor\skills\ros2-doctor"

if (-not (Test-Path $Src)) {
    Write-Error "Canonical skill not found at $Src"
}

if (Test-Path $Dest) {
    Remove-Item -Recurse -Force $Dest
}
New-Item -ItemType Directory -Force -Path (Split-Path $Dest) | Out-Null
Copy-Item -Recurse $Src $Dest
Write-Host "Synced $Src -> $Dest"
