@echo off
chcp 65001 >nul
REM Add and Delete Operation Examples
REM Demonstrates how to add new config items and delete existing ones

echo ============================================
echo JSON Config Editor - Add and Delete Examples
echo ============================================
echo.

set TOOL=..\dist\JsonEditTool.exe
set CONFIG=..\tests\sample_config.json

if not exist "%TOOL%" (
    set TOOL=python ..\src\main.py
)

echo [Example 1] Add new config item
%TOOL% add "%CONFIG%" server.timeout --value 30 --comment "Request timeout (seconds)"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Added successfully: server.timeout = 30
) else (
    echo [FAIL] Add failed (may already exist)
)
echo.

echo [Example 2] Add nested config item
%TOOL% add "%CONFIG%" logging.level --value "INFO" --comment "Log level"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Added successfully: logging.level = INFO
) else (
    echo [FAIL] Add failed
)
echo.

echo [Example 3] Delete config item
%TOOL% delete "%CONFIG%" server.debug
if %ERRORLEVEL% EQU 0 (
    echo [OK] Deleted successfully: server.debug
) else (
    echo [WARNING] Delete failed or item not found
)
echo.

echo ============================================
echo Operations completed!
echo Check file: %CONFIG%
echo ============================================
pause
