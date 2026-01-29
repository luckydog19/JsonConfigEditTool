@echo off
chcp 65001 >nul
REM User Script Test - Array Format JSON

echo ============================================
echo Testing User Script with Array Format JSON
echo ============================================
echo.

REM Set variables (DO NOT use quotes in variable assignment!)
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

echo [INFO] Variables:
echo Comment=%Comment%
echo Judge_ProcessHandleDeviceAutoContrbands=%Judge_ProcessHandleDeviceAutoContrbands%
echo.

REM Create test config if not exists
if not exist "C:\NISServer\config.json" (
    echo [INFO] Creating test config file...
    mkdir C:\NISServer 2>nul
    echo [ > C:\NISServer\config.json
    echo   { >> C:\NISServer\config.json
    echo     "key": "Globle/UseConsul", >> C:\NISServer\config.json
    echo     "value": true, >> C:\NISServer\config.json
    echo     "_comment": "Test config" >> C:\NISServer\config.json
    echo   } >> C:\NISServer\config.json
    echo ] >> C:\NISServer\config.json
    echo [OK] Test config created
    echo.
)

echo [TEST 1] Using ADD command with variables:
echo Command: python src\main.py add "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
python src\main.py add "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
echo Exit code: %ERRORLEVEL%
echo.

echo [TEST 2] Check if key exists:
python src\main.py update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Key exists, use UPDATE command
    echo.
    echo [TEST 3] Using UPDATE command:
    python src\main.py update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "%Comment%"
) else (
    echo [INFO] Key does not exist, ADD was correct
)
echo.

echo [RESULT] Final config content:
echo ----------------------------------------
type "C:\NISServer\config.json"
echo ----------------------------------------
echo.

pause
