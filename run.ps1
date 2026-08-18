Clear-Host
Write-Host "======================================" -ForegroundColor Green
Write-Host "     NEXUS OPTIMIZER DEPLOYMENT       " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "[*] Downloading latest executable..." -ForegroundColor Cyan

# 1. Clear out any old cached executable
$exePath = "$env:TEMP\main.exe"
Remove-Item $exePath -Force -ErrorAction SilentlyContinue

# 2. Download the compiled executable directly from GitHub
$url = "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/dist/main.exe"
Invoke-WebRequest -Uri $url -OutFile $exePath

Write-Host "[+] Executable cached successfully. Launching..." -ForegroundColor Green
Start-Sleep -Seconds 1

# 3. Launch the executable with Administrator privileges
Start-Process -FilePath $exePath -Verb RunAs
