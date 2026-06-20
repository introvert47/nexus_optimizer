Clear-Host
Write-Host "=========================================" -ForegroundColor Green
Write-Host "        NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[*] Fetching latest framework scripts..." -ForegroundColor Cyan

$tempDir = "$env:TEMP\nexus_flat"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force | Out-Null }
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# Download everything into the flat folder
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/main.py" -OutFile "$tempDir\main.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/engine.py" -OutFile "$tempDir\engine.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/managers/maintenance_manager.py" -OutFile "$tempDir\maintenance_manager.py"

# Clean up the file lines so they don't look for a managers folder structure
(Get-Content "$tempDir\main.py") -replace "from managers.maintenance_manager import MaintenanceManager", "from maintenance_manager import MaintenanceManager" | Set-Content "$tempDir\main.py"

Write-Host "[+] Scripts cached successfully. Launching console..." -ForegroundColor Green
Start-Sleep -Seconds 1

cd $tempDir
python main.py
