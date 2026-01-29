@echo off
chcp 65001 >nul
setlocal

REM ============================================
REM Config Update Script - PRODUCTION VERSION
REM Purpose: Update Judge/ProcessHandleDeviceAutoContrbands
REM ============================================

echo ============================================
echo Config Modification Script
echo ============================================
echo.

REM ============================================
REM Configuration - Modify these values as needed
REM ============================================
REM IMPORTANT: Do NOT add quotes in variable assignment!
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=true

REM Tool and config paths
SET TOOL_EXE=C:\NISServer\DB\JsonEditTool.exe
SET TOOL_SRC=D:\Demo\JsonConfigEditTool
SET CONFIG=C:\NISServer\config.json
SET KEY=Judge/ProcessHandleDeviceAutoContrbands

echo [INFO] Configuration:
echo   Key: %KEY%
echo   Value: %Judge_ProcessHandleDeviceAutoContrbands%
echo   Comment: %Comment%
echo.

REM ============================================
REM Determine which tool to use
REM ============================================
echo [1/4] Checking tool...
if exist "%TOOL_EXE%" (
    echo [OK] Using EXE: %TOOL_EXE%
    SET "TOOL_CMD=%TOOL_EXE%"
    SET USE_PYTHON=0
) else (
    echo [WARNING] EXE not found at: %TOOL_EXE%
    echo [INFO] Using Python version instead
    
    REM Check if project directory exists
    if not exist "%TOOL_SRC%" (
        echo [ERROR] Project directory not found: %TOOL_SRC%
        echo Please update TOOL_SRC in this script
        pause
        exit /b 1
    )
    
    REM Save current directory
    set ORIGINAL_DIR=%CD%
    
    REM Change to project directory
    cd /d "%TOOL_SRC%"
    echo [INFO] Working directory: %TOOL_SRC%
    
    SET "TOOL_CMD=python src\main.py"
    SET USE_PYTHON=1
)
echo.

REM ============================================
REM Check if config exists
REM ============================================
echo [2/4] Checking config file...
if not exist "%CONFIG%" (
    echo [WARNING] Config not found at: %CONFIG%
    echo [INFO] Creating initial config...
    
    REM Create directory
    mkdir C:\NISServer 2>nul
    
    REM Create initial JSON array config
    (
        echo [
        echo   {
        echo     "key": "Globle/UseConsul",
        echo     "value": false,
        echo     "_comment": "Initial config"
        echo   }
        echo ]
    ) > "%CONFIG%"
    
    if exist "%CONFIG%" (
        echo [OK] Initial config created
    ) else (
        echo [ERROR] Failed to create config file
        pause
        exit /b 1
    )
) else (
    echo [OK] Config file found
)
echo.

REM ============================================
REM Backup config (optional)
REM ============================================
echo [3/4] Creating backup...
set BACKUP_FILE=%CONFIG%.backup.%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_FILE=%BACKUP_FILE: =0%
copy "%CONFIG%" "%BACKUP_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backup created: %BACKUP_FILE%
) else (
    echo [WARNING] Backup failed, continuing anyway...
)
echo.

REM ============================================
REM Execute update
REM ============================================
echo [4/4] Updating configuration...
echo.
echo Command: %TOOL_CMD% update "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
echo.

REM Execute the command (quotes around %Comment% are critical!)
%TOOL_CMD% update "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"

set EXIT_CODE=%ERRORLEVEL%

REM Restore original directory if using Python
if %USE_PYTHON% EQU 1 (
    cd /d "%ORIGINAL_DIR%"
)

REM ============================================
REM Check result
REM ============================================
if %EXIT_CODE% EQU 0 (
    echo.
    echo ============================================
    echo [SUCCESS] Configuration updated successfully!
    echo ============================================
    echo.
    echo Details:
    echo   File: %CONFIG%
    echo   Key: %KEY%
    echo   Value: %Judge_ProcessHandleDeviceAutoContrbands%
    echo   Comment: %Comment%
    echo ============================================
) else (
    echo.
    echo ============================================
    echo [FAILED] Update failed!
    echo ============================================
    echo Exit code: %EXIT_CODE%
    echo.
    echo Trying ADD command instead...
    echo.
    
    REM Try ADD if UPDATE failed (key might not exist)
    if %USE_PYTHON% EQU 1 (
        cd /d "%TOOL_SRC%"
    )
    
    %TOOL_CMD% add "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
    
    if %USE_PYTHON% EQU 1 (
        cd /d "%ORIGINAL_DIR%"
    )
    
    if %ERRORLEVEL% EQU 0 (
        echo [SUCCESS] Key added successfully!
    ) else (
        echo [FAILED] Both UPDATE and ADD failed!
        echo.
        echo Troubleshooting:
        echo   1. Verify tool path is correct
        echo   2. Check config.json is valid JSON array format
        echo   3. Verify file permissions
        echo   4. Check logs at: %TOOL_SRC%\src\logs\
        echo.
        pause
        exit /b %ERRORLEVEL%
    )
)

echo.
echo [INFO] Final config content:
echo ----------------------------------------
type "%CONFIG%"
echo ----------------------------------------
echo.

endlocal
pause
