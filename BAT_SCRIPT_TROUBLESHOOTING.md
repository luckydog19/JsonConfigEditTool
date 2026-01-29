# BAT脚本故障排查指南

## 问题现象

执行脚本后没有创建预期的配置内容。

## 🔍 常见问题和解决方案

### 问题 1: 引号使用错误 ❌

**错误示例:**
```batch
SET Judge_ProcessHandleDeviceAutoContrbands="false"
```

**问题说明:**
- 这样设置的变量值是 `"false"`（包含引号）
- 传递给工具时会被当作字符串 `"false"`，而不是布尔值 `false`

**正确做法:** ✅
```batch
SET Judge_ProcessHandleDeviceAutoContrbands=false
```

---

### 问题 2: add vs update 命令

**问题说明:**
- `add` 命令：只能添加**不存在**的key
- `update` 命令：只能修改**已存在**的key
- 如果key已存在，使用 `add` 会失败

**解决方案 1: 先检查再操作** ✅
```batch
REM 尝试更新，如果失败则添加
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "说明" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo Key不存在，执行添加...
    C:\NISServer\DB\JsonEditTool.exe add "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "说明"
)
```

**解决方案 2: 直接使用update（推荐）** ✅
```batch
REM update命令会自动处理不存在的情况（如果程序支持）
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "说明"
```

---

### 问题 3: 路径不存在

**问题说明:**
- 如果 `C:\NISServer\config.json` 不存在，操作会失败
- 如果 `C:\NISServer\DB\JsonEditTool.exe` 不存在，命令无法执行

**解决方案:** ✅
```batch
REM 检查工具是否存在
if not exist "C:\NISServer\DB\JsonEditTool.exe" (
    echo [ERROR] JsonEditTool.exe not found!
    echo Please copy JsonEditTool.exe to C:\NISServer\DB\
    pause
    exit /b 1
)

REM 检查配置文件是否存在
if not exist "C:\NISServer\config.json" (
    echo [ERROR] config.json not found at C:\NISServer\
    pause
    exit /b 1
)
```

---

### 问题 4: 特殊字符处理

**问题说明:**
- 中文注释包含特殊字符（括号、逗号等）
- 可能导致命令行解析错误

**解决方案:** ✅
```batch
REM 使用双引号包裹包含特殊字符的内容
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)

REM 在命令中使用时也要加引号
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false --comment "%Comment%"
```

---

## ✅ 完整的正确脚本示例

### 示例 1: 基本用法（推荐）

```batch
@echo off
chcp 65001 >nul

echo Modifying config.json...

REM 直接执行，简单明了
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value false ^
    --comment "分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)"

if %ERRORLEVEL% EQU 0 (
    echo [OK] Config updated successfully
) else (
    echo [ERROR] Failed to update config
    pause
    exit /b 1
)

pause
```

### 示例 2: 使用变量

```batch
@echo off
chcp 65001 >nul

REM 注意：变量赋值时不要加引号
SET VALUE=false
SET COMMENT=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)

echo Modifying config with variables...
echo Value: %VALUE%
echo Comment: %COMMENT%
echo.

C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value %VALUE% ^
    --comment "%COMMENT%"

pause
```

### 示例 3: 完整的健壮脚本

```batch
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo Config.json Modification Script
echo ============================================
echo.

REM Configuration
SET TOOL=C:\NISServer\DB\JsonEditTool.exe
SET CONFIG=C:\NISServer\config.json
SET KEY=Judge/ProcessHandleDeviceAutoContrbands
SET VALUE=false
SET COMMENT=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)

REM Check tool exists
echo [1/4] Checking tool...
if not exist "%TOOL%" (
    echo [ERROR] JsonEditTool.exe not found at: %TOOL%
    echo Please build and copy the tool first
    pause
    exit /b 1
)
echo [OK] Tool found

REM Check config exists
echo [2/4] Checking config file...
if not exist "%CONFIG%" (
    echo [ERROR] config.json not found at: %CONFIG%
    pause
    exit /b 1
)
echo [OK] Config file found

REM Backup config (optional)
echo [3/4] Creating backup...
copy "%CONFIG%" "%CONFIG%.backup.%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul
echo [OK] Backup created

REM Update config
echo [4/4] Updating config...
"%TOOL%" update "%CONFIG%" "%KEY%" --value %VALUE% --comment "%COMMENT%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo [SUCCESS] Config updated successfully!
    echo ============================================
    echo Key: %KEY%
    echo Value: %VALUE%
    echo ============================================
) else (
    echo.
    echo ============================================
    echo [FAILED] Config update failed!
    echo ============================================
    echo Exit code: %ERRORLEVEL%
    echo Check log file at: C:\NISServer\DB\logs\
    echo ============================================
)

pause
```

---

## 🧪 调试技巧

### 1. 显示实际执行的命令

```batch
REM 显示完整命令（用于调试）
echo Command to execute:
echo C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %VALUE% --comment "%COMMENT%"
echo.
pause

REM 然后再实际执行
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %VALUE% --comment "%COMMENT%"
```

### 2. 检查变量值

```batch
SET Judge_ProcessHandleDeviceAutoContrbands=false
echo Variable value: [%Judge_ProcessHandleDeviceAutoContrbands%]
echo Variable length: 
echo %Judge_ProcessHandleDeviceAutoContrbands% | find /v "" | find /c ""
```

### 3. 查看错误码

```batch
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false

echo Exit code: %ERRORLEVEL%
if %ERRORLEVEL% EQU 0 echo Success
if %ERRORLEVEL% EQU 1 echo File not found or permission denied
if %ERRORLEVEL% EQU 2 echo Key already exists (for add command)
if %ERRORLEVEL% EQU 3 echo Key not found (for update/delete command)
```

### 4. 重定向输出查看详细信息

```batch
REM 保存输出到文件
C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value false > output.txt 2>&1

REM 查看输出
type output.txt
pause
```

---

## 📋 快速检查清单

执行脚本前，请确认：

- [ ] JsonEditTool.exe 存在于 `C:\NISServer\DB\`
- [ ] config.json 存在于 `C:\NISServer\`
- [ ] config.json 是有效的JSON数组格式
- [ ] 变量赋值时没有使用引号（除非值本身需要引号）
- [ ] 命令中的路径使用了双引号
- [ ] 命令中的注释参数使用了双引号（如果包含空格或特殊字符）
- [ ] 使用了正确的命令（add 或 update）

---

## 🔧 测试工具

创建一个测试脚本来验证环境：

```batch
@echo off
chcp 65001 >nul

echo ============================================
echo Environment Test Script
echo ============================================
echo.

echo [TEST 1] Check tool exists
if exist "C:\NISServer\DB\JsonEditTool.exe" (
    echo [OK] Tool found
) else (
    echo [FAIL] Tool not found
)

echo [TEST 2] Check config exists
if exist "C:\NISServer\config.json" (
    echo [OK] Config found
) else (
    echo [FAIL] Config not found
)

echo [TEST 3] Test tool help command
C:\NISServer\DB\JsonEditTool.exe --help
if %ERRORLEVEL% EQU 0 (
    echo [OK] Tool runs correctly
) else (
    echo [FAIL] Tool execution failed
)

echo [TEST 4] Test variable assignment
SET TEST_VAR=false
echo Variable TEST_VAR=%TEST_VAR%
if "%TEST_VAR%"=="false" (
    echo [OK] Variable assignment correct
) else (
    echo [FAIL] Variable value unexpected: [%TEST_VAR%]
)

echo.
echo ============================================
echo Test completed
echo ============================================
pause
```

---

## 💡 最佳实践建议

1. **始终使用绝对路径**
   ```batch
   C:\NISServer\DB\JsonEditTool.exe update "C:\NISServer\config.json" ...
   ```

2. **关键路径加引号**
   ```batch
   "C:\Program Files\MyApp\config.json"
   ```

3. **先测试后部署**
   - 在测试环境先运行
   - 确认无误后再部署到生产环境

4. **创建备份**
   ```batch
   copy config.json config.json.backup
   ```

5. **记录日志**
   ```batch
   C:\NISServer\DB\JsonEditTool.exe update ... >> operation.log 2>&1
   ```

6. **错误处理**
   ```batch
   if %ERRORLEVEL% NEQ 0 (
       echo Error occurred, check logs
       pause
       exit /b %ERRORLEVEL%
   )
   ```

---

## 📞 仍然有问题？

1. 检查日志文件：`C:\NISServer\DB\logs\json_edit_tool_*.log`
2. 运行测试脚本：`user_script_fixed.bat`
3. 手动测试单个命令
4. 检查JSON文件格式是否正确

---

**更新时间**: 2026-01-28  
**版本**: 1.0
