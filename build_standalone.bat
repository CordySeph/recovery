@echo off
REM =================================================================
REM 🚀 Build Standalone Executable for Data Recovery Tool (Windows)
REM Creates a single standalone executable file that runs without Python installed.
REM =================================================================

setlocal enabledelayedexpansion

echo =================================================================
echo 📦 Building Standalone Universal Data Recovery Executable for Windows...
echo =================================================================

REM 1. Check/Install PyInstaller
where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] PyInstaller not found. Installing PyInstaller via pip...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [!] Failed to install PyInstaller. Please ensure Python and pip are in PATH.
        exit /b 1
    )
)

REM 2. Build standalone binary
echo [*] Compiling recover.py into standalone Windows executable (dist\recover.exe)...
pyinstaller --clean --onefile --collect-all recovery_engine --name recover recover.py

if %errorlevel% neq 0 (
    echo [!] Build failed!
    exit /b 1
)

echo.
echo =================================================================
echo 🎉 BUILD SUCCESSFUL!
echo =================================================================
echo 📁 Standalone Executable File is located at: dist\recover.exe
echo.
echo 👉 คุณสามารถคัดลอกไฟล์ "dist\recover.exe" ไปใส่ Flash Drive และนำไปเปิดใช้งาน
echo    บนเครื่อง Windows อื่นได้ทันทีโดยไม่ต้องติดตั้ง Python!
echo.
echo    วิธีรันบนเครื่องปลายทาง (เปิด CMD หรือ PowerShell ด้วย Run as Administrator):
echo    recover.exe \\.\PhysicalDrive1 --all -o D:\recovered_data
echo =================================================================
pause
