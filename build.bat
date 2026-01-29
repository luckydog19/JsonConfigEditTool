@echo off
chcp 65001 >nul
REM JSON Config Editor - Build Script

echo ============================================
echo JSON Config Editor - Build Script
echo ============================================
echo.

REM Check Python installation
echo [INFO] Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found, please install Python 3.8+
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo [1/5] Checking dependencies...
python -m pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] PyInstaller not found, installing...
    python -m pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install PyInstaller
        echo [INFO] Try running: python -m pip install --upgrade pip
        pause
        exit /b 1
    )
    echo [OK] PyInstaller installed successfully
) else (
    echo [OK] PyInstaller already installed
)
echo.

echo [2/5] Cleaning old build files...
if exist build (
    echo [INFO] Removing build directory...
    rmdir /s /q build
)
if exist dist (
    echo [INFO] Removing dist directory...
    rmdir /s /q dist
)
if exist __pycache__ (
    rmdir /s /q __pycache__
)
if exist src\__pycache__ (
    rmdir /s /q src\__pycache__
)
if exist JsonEditTool.spec (
    echo [INFO] Removing old spec file...
    del JsonEditTool.spec
)
echo [OK] Cleanup completed
echo.

echo [3/5] Building executable...
echo [INFO] This may take a few minutes...
python -m PyInstaller --onefile ^
    --name JsonEditTool ^
    --console ^
    --clean ^
    --noconfirm ^
    --hidden-import=logger ^
    --hidden-import=json_editor ^
    --hidden-import=validator ^
    --paths=src ^
    src\main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed! Please check error messages above
    echo.
    echo Common issues:
    echo   1. Missing dependencies - run: python -m pip install -r requirements.txt
    echo   2. Antivirus blocking - temporarily disable it
    echo   3. Insufficient permissions - run as administrator
    echo.
    pause
    exit /b 1
)
echo [OK] Build completed
echo.

echo [4/5] Verifying build result...
if not exist dist\JsonEditTool.exe (
    echo [ERROR] EXE file not found in dist directory
    pause
    exit /b 1
)
echo [OK] EXE file created successfully
echo.

echo [5/5] Testing executable...
dist\JsonEditTool.exe --version
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] EXE test failed, but file was created
)
echo.

echo ============================================
echo Build Successful!
echo ============================================
echo.
echo Executable location: dist\JsonEditTool.exe
echo.
echo File information:
dir dist\JsonEditTool.exe | find "JsonEditTool.exe"
echo.
echo ============================================
echo Usage Examples:
echo ============================================
echo   dist\JsonEditTool.exe --help
echo   dist\JsonEditTool.exe update config.json server.port --value 8080
echo   dist\JsonEditTool.exe add settings.json new.key --value "test"
echo   dist\JsonEditTool.exe delete config.json old.key
echo ============================================
echo.
echo [TIP] You can copy JsonEditTool.exe to any location
echo       or add it to your system PATH
echo.

pause
