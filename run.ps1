Clear-Host
Write-Host "=========================================" -ForegroundColor Green
Write-Host "        NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[*] Fetching latest framework scripts..." -ForegroundColor Cyan

# Setup clean path environment variables
$tempDir = "$env:TEMP\nexus_working"
$managersDir = "$tempDir\managers"

# Create clean temporary directories
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force | Out-Null }
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
New-Item -ItemType Directory -Force -Path $managersDir | Out-Null

# Download all scripts directly into our working folder structure
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/main.py" -OutFile "$tempDir\main.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/engine.py" -OutFile "$tempDir\engine.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/managers/maintenance_manager.py" -OutFile "$managersDir\maintenance_manager.py"

Write-Host "[+] Scripts cached successfully. Launching console..." -ForegroundColor Green
Start-Sleep -Seconds 1

# Change directory and run the tool perfectly
cd $tempDir
python main.py
