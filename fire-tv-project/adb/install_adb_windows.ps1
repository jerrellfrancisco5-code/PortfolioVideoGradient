# Installs the already-downloaded Android Platform Tools on Windows.
# Run in PowerShell:  powershell -ExecutionPolicy Bypass -File .\install_adb_windows.ps1
# Looks for the zip or extracted folder in Downloads, puts adb in C:\platform-tools,
# adds that folder to your user PATH, and verifies adb runs.

$ErrorActionPreference = "Stop"
$dl   = Join-Path $env:USERPROFILE "Downloads"
$dest = "C:\platform-tools"

$zip    = Get-ChildItem $dl -Filter "platform-tools*.zip" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$folder = Get-ChildItem $dl -Directory -Filter "platform-tools*" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($zip) {
    Write-Host "Extracting $($zip.FullName) ..."
    $tmp = Join-Path $env:TEMP "pt_extract"
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    Expand-Archive -Path $zip.FullName -DestinationPath $tmp -Force
    $src = Get-ChildItem $tmp -Recurse -Filter "adb.exe" | Select-Object -First 1
} elseif ($folder) {
    Write-Host "Using extracted folder $($folder.FullName) ..."
    $src = Get-ChildItem $folder.FullName -Recurse -Filter "adb.exe" | Select-Object -First 1
} else {
    Write-Host "No platform-tools zip or folder found in $dl"
    Write-Host "Download it from https://developer.android.com/tools/releases/platform-tools and run this again."
    exit 1
}

if (-not $src) { Write-Host "adb.exe not found inside the download."; exit 1 }

$srcDir = $src.DirectoryName
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Copy-Item $srcDir $dest -Recurse
Write-Host "Installed to $dest"

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$dest*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$dest", "User")
    Write-Host "Added $dest to your user PATH (new terminals will see it)."
}
$env:Path += ";$dest"

Write-Host ""
& "$dest\adb.exe" version
Write-Host ""
Write-Host "adb is ready. Next, on the TV find the IP under Settings > My Fire TV > About > Network, then run:"
Write-Host "    adb connect <TV-IP>:5555"
Write-Host "and press Allow on the TV screen."
