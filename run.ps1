Clear-Host
Write-Host "=========================================" -ForegroundColor Green
Write-Host "        NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[*] Fetching latest framework scripts..." -ForegroundColor Cyan

# Define download destinations
$mainPath = "$env:TEMP\main.py"
$enginePath = "$env:TEMP\engine.py"
$maintPath = "$env:TEMP\maintenance_manager.py"

# Download your files directly from your repository
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/main.py" -OutFile $mainPath
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/engine.py" -OutFile $enginePath

# Create the managers folder inside TEMP so python can find it
New-Item -ItemType Directory -Force -Path "$env:TEMP\managers" | Out-Null
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/nexus_optimizer/managers/maintenance_manager.py" -OutFile $maintPath

Write-Host "[+] Scripts cached successfully. Launching console..." -ForegroundColor Green
time.sleep 1

# Execute the application
cd $env:TEMP
python main.py
