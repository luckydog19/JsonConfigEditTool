@echo off
chcp 65001 >nul
REM Multi-file Batch Modification Example
REM Demonstrates batch modification of JSON configs in different locations

setlocal enabledelayedexpansion

echo ============================================
echo JSON Config Editor - Multi-file Batch Example
echo ============================================
echo.

REM Set tool path
set TOOL=..\dist\JsonEditTool.exe
if not exist "%TOOL%" (
    set TOOL=python ..\src\main.py
)

REM Define multiple config file paths (examples)
set "CONFIG1=..\tests\sample_config.json"
set "CONFIG2=D:\App\config.json"
set "CONFIG3=E:\Projects\settings.json"

echo Preparing batch modification...
echo.

REM Modify config file 1
echo [1/3] Modifying test config...
%TOOL% update "%CONFIG1%" server.port --value 8080 --comment "Web service port"
if !ERRORLEVEL! EQU 0 (
    echo    [OK] Success
) else (
    echo    [FAIL] Failed
)
echo.

REM Modify config file 2 (if exists)
if exist "%CONFIG2%" (
    echo [2/3] Modifying app config...
    %TOOL% update "%CONFIG2%" api.endpoint --value "https://api.example.com"
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Success
    ) else (
        echo    [FAIL] Failed
    )
) else (
    echo [2/3] Skip (file not found): %CONFIG2%
)
echo.

REM Modify config file 3 (if exists)
if exist "%CONFIG3%" (
    echo [3/3] Modifying project config...
    %TOOL% update "%CONFIG3%" database.maxConn --value 100
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Success
    ) else (
        echo    [FAIL] Failed
    )
) else (
    echo [3/3] Skip (file not found): %CONFIG3%
)
echo.

echo ============================================
echo Batch modification completed!
echo ============================================
pause
