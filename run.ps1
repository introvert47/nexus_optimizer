Clear-Host
Write-Host "=========================================" -ForegroundColor Green
Write-Host "        NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[*] Fetching latest framework scripts..." -ForegroundColor Cyan

# 1. Clear out any old cached files completely
Remove-Item "$env:TEMP\main.py", "$env:TEMP\engine.py", "$env:TEMP\managers" -Recurse -Force -ErrorAction SilentlyContinue

# 2. Create the clean managers subdirectory
New-Item -ItemType Directory -Force -Path "$env:TEMP\managers" | Out-Null

# 3. Download the clean files directly into the Windows Temp environment
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/main.py" -OutFile "$env:TEMP\main.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/engine.py" -OutFile "$env:TEMP\engine.py"
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/managers/maintenance_manager.py" -OutFile "$env:TEMP\managers\maintenance_manager.py"

Write-Host "[+] Scripts cached successfully. Launching console..." -ForegroundColor Green
Start-Sleep -Seconds 1

# 4. Jump into the folder and execute
cd $env:TEMP
python main.py
