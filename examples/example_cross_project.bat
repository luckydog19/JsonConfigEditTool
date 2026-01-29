@echo off
chcp 65001 >nul
REM Cross-project Config Sync Example
REM Demonstrates syncing the same configs to multiple projects

setlocal enabledelayedexpansion

echo ============================================
echo JSON Config Editor - Cross-project Sync Example
echo ============================================
echo.

set TOOL=..\dist\JsonEditTool.exe
if not exist "%TOOL%" (
    set TOOL=python ..\src\main.py
)

REM Config values to sync
set DB_HOST=192.168.1.100
set DB_PORT=3306
set API_TIMEOUT=30

echo Configuration info:
echo - Database host: %DB_HOST%
echo - Database port: %DB_PORT%
echo - API timeout: %API_TIMEOUT% seconds
echo.

REM Define project config file list
set "PROJECT_A=D:\ProjectA\config.json"
set "PROJECT_B=E:\ProjectB\settings.json"
set "PROJECT_C=C:\ProjectC\app.json"

echo Starting config sync to all projects...
echo.

REM Iterate through all projects
for %%P in ("%PROJECT_A%" "%PROJECT_B%" "%PROJECT_C%") do (
    if exist %%P (
        echo Updating: %%~P
        
        REM Update database config
        %TOOL% update %%P database.host --value %DB_HOST% --comment "Database host" >nul 2>&1
        if !ERRORLEVEL! NEQ 0 (
            %TOOL% add %%P database.host --value %DB_HOST% --comment "Database host" >nul 2>&1
        )
        
        %TOOL% update %%P database.port --value %DB_PORT% --comment "Database port" >nul 2>&1
        if !ERRORLEVEL! NEQ 0 (
            %TOOL% add %%P database.port --value %DB_PORT% --comment "Database port" >nul 2>&1
        )
        
        REM Update API config
        %TOOL% update %%P api.timeout --value %API_TIMEOUT% --comment "API timeout" >nul 2>&1
        if !ERRORLEVEL! NEQ 0 (
            %TOOL% add %%P api.timeout --value %API_TIMEOUT% --comment "API timeout" >nul 2>&1
        )
        
        echo [OK] Completed
    ) else (
        echo [WARNING] Skip (file not found): %%~P
    )
    echo.
)

echo ============================================
echo Config sync completed!
echo ============================================
pause
