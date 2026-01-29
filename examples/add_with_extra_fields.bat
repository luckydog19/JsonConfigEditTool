@echo off
chcp 65001 >nul
REM ========================================
REM 添加带额外字段的配置项示例
REM ========================================

SET TOOL_DIR=%~dp0..
SET TOOL_EXE=%TOOL_DIR%\dist\JsonEditTool.exe
SET CONFIG_FILE=C:\YourApp\config.json

REM ========================================
REM 示例1: 添加带类型和启用状态的配置
REM ========================================
echo 示例1: 添加API配置...
"%TOOL_EXE%" add "%CONFIG_FILE%" "api.timeout" ^
    --value 30 ^
    --comment "API超时时间" ^
    --extra type=int ^
    --extra unit=seconds ^
    --extra enabled=true

if %ERRORLEVEL% EQU 0 (
    echo [成功] 已添加 api.timeout
) else (
    echo [失败] 错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

REM ========================================
REM 示例2: 添加带版本和废弃标记的配置
REM ========================================
echo.
echo 示例2: 添加数据库连接池配置...
"%TOOL_EXE%" add "%CONFIG_FILE%" "db.pool.size" ^
    --value 10 ^
    --comment "连接池大小" ^
    --extra min=5 ^
    --extra max=20 ^
    --extra version=2.0 ^
    --extra deprecated=false

if %ERRORLEVEL% EQU 0 (
    echo [成功] 已添加 db.pool.size
) else (
    echo [失败] 错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

REM ========================================
REM 示例3: 添加带优先级和分类的配置
REM ========================================
echo.
echo 示例3: 添加缓存配置...
"%TOOL_EXE%" add "%CONFIG_FILE%" "cache.redis.host" ^
    --value "127.0.0.1" ^
    --comment "Redis主机地址" ^
    --extra priority=high ^
    --extra category=cache ^
    --extra required=true ^
    --extra env=production

if %ERRORLEVEL% EQU 0 (
    echo [成功] 已添加 cache.redis.host
) else (
    echo [失败] 错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

REM ========================================
REM 示例4: 数组格式 - 添加带额外字段的配置
REM ========================================
echo.
echo 示例4: 数组格式添加配置...
"%TOOL_EXE%" add "%CONFIG_FILE%" "Feature/NewModule" ^
    --value true ^
    --comment "新模块功能开关" ^
    --extra module=feature ^
    --extra since=1.5.0 ^
    --extra experimental=false

if %ERRORLEVEL% EQU 0 (
    echo [成功] 已添加 Feature/NewModule
) else (
    echo [失败] 错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo 所有配置添加完成！
echo ========================================
pause
