@echo off
chcp 65001 >nul
REM ============================================
REM User Script - CORRECT VERSION
REM Purpose: Add/Update Judge/ProcessHandleDeviceAutoContrbands
REM ============================================

echo ============================================
echo Config Modification Script (CORRECT)
echo ============================================
echo.

REM ============================================
REM CRITICAL: Variable assignment WITHOUT quotes!
REM ============================================
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

echo [INFO] Variables set (no quotes in assignment):
echo   Judge_ProcessHandleDeviceAutoContrbands = %Judge_ProcessHandleDeviceAutoContrbands%
echo   Comment = %Comment%
echo.

REM ============================================
REM Configuration
REM ============================================
SET TOOL=C:\NISServer\DB\JsonEditTool.exe
SET CONFIG=C:\NISServer\config.json
SET KEY=Judge/ProcessHandleDeviceAutoContrbands

REM ============================================
REM Check if tool exists
REM ============================================
echo [1/3] Checking tool...
if not exist "%TOOL%" (
    echo [WARNING] Tool not found at: %TOOL%
    echo [INFO] Using Python version instead...
    REM Change to project directory first
    cd /d "d:\Demo\JsonEditTool"
    SET TOOL=python src\main.py
    echo [INFO] Changed to project directory: d:\Demo\JsonEditTool
)
echo [OK] Tool: %TOOL%
echo.

REM ============================================
REM Check if config exists
REM ============================================
echo [2/3] Checking config file...
if not exist "%CONFIG%" (
    echo [WARNING] Config not found at: %CONFIG%
    echo [INFO] Creating test config...
    mkdir C:\NISServer 2>nul
    echo [ > "%CONFIG%"
    echo   { >> "%CONFIG%"
    echo     "key": "Globle/UseConsul", >> "%CONFIG%"
    echo     "value": true, >> "%CONFIG%"
    echo     "_comment": "Test config" >> "%CONFIG%"
    echo   } >> "%CONFIG%"
    echo ] >> "%CONFIG%"
    echo [OK] Test config created
) else (
    echo [OK] Config found
)
echo.

REM ============================================
REM Execute command
REM IMPORTANT: Add quotes around %Comment% in the command!
REM ============================================
echo [3/3] Updating config...
echo.
echo Command:
echo   %TOOL% update "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
echo.

%TOOL% update "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo [SUCCESS] Config updated successfully!
    echo ============================================
    echo Key: %KEY%
    echo Value: %Judge_ProcessHandleDeviceAutoContrbands%
    echo Comment: %Comment%
    echo ============================================
) else (
    echo.
    echo ============================================
    echo [FAILED] Update failed!
    echo ============================================
    echo Exit code: %ERRORLEVEL%
    echo.
    echo Trying ADD command instead...
    echo ============================================
    %TOOL% add "%CONFIG%" "%KEY%" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
    
    if %ERRORLEVEL% EQU 0 (
        echo [SUCCESS] Config added successfully!
    ) else (
        echo [FAILED] Both update and add failed!
        echo Please check:
        echo   1. Tool exists at: %TOOL%
        echo   2. Config file is valid JSON
        echo   3. Config file permissions
    )
)

echo.
echo [RESULT] Final config content:
echo ----------------------------------------
type "%CONFIG%"
echo ----------------------------------------
echo.

pause
