@echo off
chcp 65001 >nul
REM User Script - Fixed Version
REM Purpose: Modify config.json with proper syntax

echo ============================================
echo Modify Config.json - Fixed Script
echo ============================================
echo.

REM ============================================
REM Method 1: Use variables WITHOUT quotes
REM ============================================
echo [Method 1] Variables without quotes:
echo.

SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

echo Variables set:
echo   Comment=%Comment%
echo   Judge_ProcessHandleDeviceAutoContrbands=%Judge_ProcessHandleDeviceAutoContrbands%
echo.

REM Test with local file first
SET CONFIG_FILE=C:\NISServer\config.json

REM Create directory if not exists
if not exist C:\NISServer mkdir C:\NISServer

REM Create initial config if not exists
if not exist "%CONFIG_FILE%" (
    echo [INFO] Creating initial config file...
    echo [ > "%CONFIG_FILE%"
    echo   { >> "%CONFIG_FILE%"
    echo     "key": "Globle/UseConsul", >> "%CONFIG_FILE%"
    echo     "value": true, >> "%CONFIG_FILE%"
    echo     "_comment": "Sample config" >> "%CONFIG_FILE%"
    echo   } >> "%CONFIG_FILE%"
    echo ] >> "%CONFIG_FILE%"
    echo [OK] Initial config created
    echo.
)

REM Try to add the new key
echo [Step 1] Trying to ADD new key...
C:\NISServer\DB\JsonEditTool.exe add "%CONFIG_FILE%" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"

if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Key might already exist, trying UPDATE instead...
    C:\NISServer\DB\JsonEditTool.exe update "%CONFIG_FILE%" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
)

echo.
echo ============================================
REM ============================================
REM Method 2: Direct command with literal values
REM ============================================
echo [Method 2] Direct command:
echo.

C:\NISServer\DB\JsonEditTool.exe update "%CONFIG_FILE%" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)"

echo.
echo ============================================
echo [RESULT] Final config content:
echo ============================================
type "%CONFIG_FILE%"
echo ============================================
echo.

pause
