Clear-Host
Write-Host "======================================" -ForegroundColor Green
Write-Host "     NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "[*] Downloading latest executable..." -ForegroundColor Cyan

# 1. Clear out any old cached executable
$exePath = "$env:TEMP\main.exe"
Remove-Item $exePath -Force -ErrorAction SilentlyContinue

# 2. Download compiled executable directly from GitHub root
$url = "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/main.exe"
Invoke-WebRequest -Uri $url -OutFile $exePath

Write-Host "[+] Executable cached successfully. Launching..." -ForegroundColor Green
Start-Sleep -Seconds 1

# 3. Launch with Administrator privileges
Start-Process -FilePath $exePath -Verb RunAs
