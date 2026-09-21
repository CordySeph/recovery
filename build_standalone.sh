#!/bin/bash
# 🚀 Build Standalone Executable for Data Recovery Tool
# Creates a single standalone executable file that runs without Python installed.

set -e

echo "================================================================="
echo "📦 Building Standalone Universal Data Recovery Executable..."
echo "================================================================="

# 1. Check/Install PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "[*] PyInstaller not found. Installing PyInstaller..."
    python3 -m pip install pyinstaller
fi

# 2. Build standalone binary
echo "[*] Compiling recover.py into standalone executable..."
pyinstaller --clean --onefile --collect-all recovery_engine --name recover recover.py

echo ""
echo "================================================================="
echo "🎉 BUILD SUCCESSFUL!"
echo "================================================================="
echo "📁 Standalone Executable File is located at: dist/recover"
echo ""
echo "👉 คุณสามารถคัดลอกไฟล์ 'dist/recover' ไปใส่ Flash Drive และนำไปเปิดใช้งาน"
echo "   บนเครื่องอื่นได้ทันทีโดยไม่ต้องติดตั้ง Python!"
echo ""
echo "   วิธีรันบนเครื่องปลายทาง:"
echo "   sudo ./recover"
echo "================================================================="
