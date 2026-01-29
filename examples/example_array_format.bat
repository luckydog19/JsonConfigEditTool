@echo off
chcp 65001 >nul
REM Array Format Config Example
REM Demonstrates working with array-based JSON config files

echo ============================================
echo JSON Config Editor - Array Format Example
echo ============================================
echo.

set TOOL=..\dist\JsonEditTool.exe
set CONFIG=..\tests\test_array_config.json

if not exist "%TOOL%" (
    echo [INFO] EXE not found, using Python
    set TOOL=python ..\src\main.py
)

echo Configuration file: %CONFIG%
echo.

REM Example 1: Update existing item with slash separator
echo [Example 1] Update item with slash separator
%TOOL% update "%CONFIG%" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "Enable auto contraband handling"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Updated successfully
) else (
    echo [FAIL] Update failed
)
echo.

REM Example 2: Add new item with special characters in key
echo [Example 2] Add item with special characters in key
%TOOL% add "%CONFIG%" "Network/API:Endpoint" --value "https://api.server.com:8443/v1" --comment "API endpoint with port"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Added successfully
) else (
    echo [WARN] Add failed (may already exist)
)
echo.

REM Example 3: Update value with URL containing special characters
echo [Example 3] Update value with URL (special characters)
%TOOL% update "%CONFIG%" "Globle/ConsulURI" --value "http://192.168.1.100:8500/v1/kv?token=abc123" --comment "Consul URI with query params"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Updated successfully
) else (
    echo [FAIL] Update failed
)
echo.

REM Example 4: Using environment variable in command
set Judge_ProcessHandleDeviceAutoContrbands=false
echo [Example 4] Using environment variable
echo   Variable: Judge_ProcessHandleDeviceAutoContrbands = %Judge_ProcessHandleDeviceAutoContrbands%
%TOOL% update "%CONFIG%" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "Updated from environment variable"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Updated successfully
) else (
    echo [FAIL] Update failed
)
echo.

REM Example 5: Delete an item
echo [Example 5] Delete item
%TOOL% delete "%CONFIG%" "Test/URL:Port"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Deleted successfully
) else (
    echo [WARN] Delete failed (may not exist)
)
echo.

echo ============================================
echo Examples completed!
echo Check file: %CONFIG%
echo ============================================
pause
