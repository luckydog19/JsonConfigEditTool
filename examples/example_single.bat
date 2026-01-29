@echo off
chcp 65001 >nul
REM Single File Modification Example
REM Demonstrates how to modify a single JSON config file

echo ============================================
echo JSON Config Editor - Single File Example
echo ============================================
echo.

REM Set tool path and config file path
set TOOL=..\dist\JsonEditTool.exe
set CONFIG=..\tests\sample_config.json

REM If tool doesn't exist, use Python
if not exist "%TOOL%" (
    echo [INFO] EXE not found, using Python
    set TOOL=python ..\src\main.py
)

echo [Example 1] Modify server port
%TOOL% update "%CONFIG%" server.port --value 9000 --comment "Modified port"
echo.

echo [Example 2] Modify database host
%TOOL% update "%CONFIG%" database.host --value "192.168.1.100" --comment "Production database"
echo.

echo [Example 3] Modify cache TTL
%TOOL% update "%CONFIG%" cache.ttl --value 7200 --comment "2 hours expiry"
echo.

echo ============================================
echo Example completed!
echo Check file: %CONFIG%
echo ============================================
pause
