@echo off
chcp 65001 >nul
REM Complete Function Test Script
REM Test all core functionality

echo ============================================
echo JSON Config Editor - Full Function Test
echo ============================================
echo.

REM Set tool path
set TOOL=python src\main.py
set TEST_CONFIG=tests\test_temp.json

REM Create test config file
echo [PREPARE] Creating test config file...
echo { > %TEST_CONFIG%
echo   "server": { >> %TEST_CONFIG%
echo     "port": { >> %TEST_CONFIG%
echo       "key": "port", >> %TEST_CONFIG%
echo       "value": 8080, >> %TEST_CONFIG%
echo       "_comment": "Server Port" >> %TEST_CONFIG%
echo     } >> %TEST_CONFIG%
echo   } >> %TEST_CONFIG%
echo } >> %TEST_CONFIG%
echo [OK] Test config file created
echo.

REM Test 1: Update operation
echo [TEST 1] Testing update operation...
%TOOL% update %TEST_CONFIG% server.port --value 9000 --comment "Modified port" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Update operation successful
) else (
    echo [FAIL] Update operation failed
    goto :error
)
echo.

REM Test 2: Add operation
echo [TEST 2] Testing add operation...
%TOOL% add %TEST_CONFIG% server.host --value "localhost" --comment "Server address" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Add operation successful
) else (
    echo [FAIL] Add operation failed
    goto :error
)
echo.

REM Test 3: Add nested config
echo [TEST 3] Testing nested config addition...
%TOOL% add %TEST_CONFIG% database.host --value "127.0.0.1" --comment "Database host" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Nested config added successfully
) else (
    echo [FAIL] Nested config addition failed
    goto :error
)
echo.

REM Test 4: Type inference
echo [TEST 4] Testing type inference...
%TOOL% add %TEST_CONFIG% cache.enabled --value true --comment "Cache switch" >nul 2>&1
%TOOL% add %TEST_CONFIG% cache.ttl --value 3600 --comment "Cache TTL" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Type inference test successful
) else (
    echo [FAIL] Type inference test failed
    goto :error
)
echo.

REM Test 5: Delete operation
echo [TEST 5] Testing delete operation...
%TOOL% delete %TEST_CONFIG% cache.ttl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Delete operation successful
) else (
    echo [FAIL] Delete operation failed
    goto :error
)
echo.

REM Test 6: Backup function
echo [TEST 6] Testing backup function...
%TOOL% update %TEST_CONFIG% server.port --value 8888 --backup >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backup function test successful
) else (
    echo [FAIL] Backup function test failed
    goto :error
)
echo.

REM Test 7: Absolute path
echo [TEST 7] Testing absolute path...
set ABS_PATH=%CD%\%TEST_CONFIG%
%TOOL% update "%ABS_PATH%" server.port --value 7777 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Absolute path test successful
) else (
    echo [FAIL] Absolute path test failed
    goto :error
)
echo.

REM Test 8: Error handling
echo [TEST 8] Testing error handling...
%TOOL% update nonexistent.json key --value value >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [OK] Error handling works correctly
) else (
    echo [FAIL] Error handling abnormal
    goto :error
)
echo.

REM Show final result
echo [RESULT] Final config file content:
echo ----------------------------------------
type %TEST_CONFIG%
echo ----------------------------------------
echo.

REM Cleanup
echo [CLEANUP] Removing test files...
del %TEST_CONFIG% >nul 2>&1
del %TEST_CONFIG%.bak.* >nul 2>&1
echo [OK] Cleanup completed
echo.

echo ============================================
echo All Tests Passed!
echo ============================================
echo.
echo Log files location: src\logs\
pause
exit /b 0

:error
echo.
echo ============================================
echo Tests Failed!
echo ============================================
echo Please check log file: src\logs\json_edit_tool_*.log
echo.
REM Cleanup
del %TEST_CONFIG% >nul 2>&1
del %TEST_CONFIG%.bak.* >nul 2>&1
pause
exit /b 1
