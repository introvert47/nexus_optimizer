Clear-Host
Write-Host "=========================================" -ForegroundColor Green
Write-Host "        NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[*] Fetching latest framework scripts..." -ForegroundColor Cyan

# Define download destinations inside Windows Temp directory
$mainPath = "$env:TEMP\main.py"
$enginePath = "$env:TEMP\engine.py"
$maintPath = "$env:TEMP\maintenance_manager.py"

# Download your main files directly from your repository
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/main.py" -OutFile $mainPath
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/engine.py" -OutFile $enginePath

# Create the managers folder inside TEMP so python can locate it natively
New-Item -ItemType Directory -Force -Path "$env:TEMP\managers" | Out-Null
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/managers/maintenance_manager.py" -OutFile $maintPath

Write-Host "[+] Scripts cached successfully. Launching console..." -ForegroundColor Green
Start-Sleep -Seconds 1

# Execute the application setup
cd $env:TEMP
python main.py
