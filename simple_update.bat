@echo off
chcp 65001 >nul

REM ============================================
REM Simple Config Update Script (Silent Mode)
REM ============================================

echo Updating Judge/ProcessHandleDeviceAutoContrbands...

REM Variables (NO quotes!)
SET VALUE=true
SET COMMENT=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)

REM Check if EXE exists
if exist "C:\NISServer\DB\JsonEditTool.exe" (
    echo [INFO] Using EXE version (silent mode)
    C:\NISServer\DB\JsonEditTool.exe update ^
        "C:\NISServer\config.json" ^
        "Judge/ProcessHandleDeviceAutoContrbands" ^
        --value %VALUE% ^
        --comment "%COMMENT%" ^
        --silent
) else (
    echo [INFO] Using Python version (silent mode)
    REM Save current directory
    set OLDDIR=%CD%
    
    REM Change to project directory
    cd /d "D:\Demo\JsonConfigEditTool"
    
    REM Run Python script with --silent flag
    python src\main.py update ^
        "C:\NISServer\config.json" ^
        "Judge/ProcessHandleDeviceAutoContrbands" ^
        --value %VALUE% ^
        --comment "%COMMENT%" ^
        --silent
    
    REM Return to original directory
    cd /d "%OLDDIR%"
)

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Config updated
) else (
    echo [FAILED] Update failed, exit code: %ERRORLEVEL%
)

echo.
pause
