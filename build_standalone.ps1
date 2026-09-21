# 🚀 Build Standalone Executable for Data Recovery Tool (PowerShell)
# Creates a single standalone executable file that runs without Python installed.

$ErrorActionPreference = "Stop"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "📦 Building Standalone Universal Data Recovery Executable for Windows..." -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Check/Install PyInstaller
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "[*] PyInstaller not found. Installing PyInstaller via pip..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

# 2. Build standalone binary
Write-Host "[*] Compiling recover.py into standalone Windows executable (dist\recover.exe)..." -ForegroundColor Green
pyinstaller --clean --onefile --collect-all recovery_engine --name recover recover.py

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "🎉 BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "📁 Standalone Executable File is located at: dist\recover.exe" -ForegroundColor White
Write-Host ""
Write-Host "👉 คุณสามารถคัดลอกไฟล์ 'dist\recover.exe' ไปใส่ Flash Drive และนำไปเปิดใช้งาน" -ForegroundColor Gray
Write-Host "   บนเครื่อง Windows อื่นได้ทันทีโดยไม่ต้องติดตั้ง Python!" -ForegroundColor Gray
Write-Host ""
Write-Host "   วิธีรันบนเครื่องปลายทาง (เปิด PowerShell ด้วย Run as Administrator):" -ForegroundColor Yellow
Write-Host "   .\recover.exe \\.\PhysicalDrive1 --all -o D:\recovered_data" -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
