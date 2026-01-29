@echo off
chcp 65001 >nul

echo ============================================
echo Simple Test - Correct Variable Usage
echo ============================================
echo.

REM CORRECT: No quotes in variable assignment
SET VALUE=false
SET COMMENT=测试注释内容

echo [INFO] Variables (without quotes in assignment):
echo VALUE=%VALUE%
echo COMMENT=%COMMENT%
echo.

REM Test command (add quotes around %COMMENT% in command)
echo [TEST] Running command...
echo Command: python src\main.py add tests\test_array_config.json "Test/Simple" --value %VALUE% --comment "%COMMENT%"
echo.

python src\main.py add tests\test_array_config.json "Test/SimpleTest" --value %VALUE% --comment "%COMMENT%"

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Command executed successfully
) else (
    echo [FAILED] Command failed with exit code: %ERRORLEVEL%
)

echo.
pause
