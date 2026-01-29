# Python模块错误修复指南

## 🚨 错误现象

```
ModuleNotFoundError: No module named 'logger'
[PYT-27140:ERROR] Failed to execute script 'main' due to unhandled exception!
```

## 🔍 根本原因

当使用Python版本运行工具时（`python src\main.py`），如果**当前工作目录不在项目根目录**，Python将无法找到 `src` 目录下的模块（`logger.py`, `json_editor.py` 等）。

### 问题场景

```batch
REM 在 C:\WINDOWS\system32 或其他目录执行
python src\main.py update config.json key --value value
```

**结果：** Python在当前目录查找 `src\main.py`，即使找到了，`main.py` 中的 `from logger import get_logger` 也会失败，因为Python无法找到同级的 `logger.py`。

---

## ✅ 解决方案

### 方案 1：切换到项目目录（推荐）

```batch
@echo off
chcp 65001 >nul

REM 保存原始目录
set OLDDIR=%CD%

REM 切换到项目目录
cd /d "d:\Demo\JsonEditTool"

REM 运行Python脚本（现在能找到模块了）
python src\main.py update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "注释"

REM 返回原始目录
cd /d "%OLDDIR%"

pause
```

### 方案 2：使用绝对路径和PYTHONPATH

```batch
@echo off
chcp 65001 >nul

REM 设置Python模块搜索路径
set PYTHONPATH=d:\Demo\JsonEditTool\src

REM 使用绝对路径运行
python "d:\Demo\JsonEditTool\src\main.py" update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "注释"

pause
```

### 方案 3：使用EXE版本（最简单）

```batch
@echo off
chcp 65001 >nul

REM 直接使用打包好的EXE，无需担心模块问题
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value true ^
    --comment "注释"

pause
```

---

## 🎯 完整的健壮脚本

### 自动检测并选择最佳方式

```batch
@echo off
chcp 65001 >nul
setlocal

echo Updating configuration...

REM Configuration
SET TOOL_EXE=C:\NISServer\DB\JsonEditTool.exe
SET TOOL_SRC=d:\Demo\JsonEditTool
SET CONFIG=C:\NISServer\config.json
SET KEY=Judge/ProcessHandleDeviceAutoContrbands
SET VALUE=true
SET COMMENT=分组判图没有程处理违禁品关

REM ============================================
REM Method 1: Try EXE first (no module issues)
REM ============================================
if exist "%TOOL_EXE%" (
    echo [1] Using EXE version
    "%TOOL_EXE%" update "%CONFIG%" "%KEY%" --value %VALUE% --comment "%COMMENT%"
    goto :result
)

REM ============================================
REM Method 2: Use Python with proper directory
REM ============================================
echo [2] Using Python version

REM Check if project exists
if not exist "%TOOL_SRC%\src\main.py" (
    echo [ERROR] Project not found at: %TOOL_SRC%
    pause
    exit /b 1
)

REM Save and change directory
set OLDDIR=%CD%
cd /d "%TOOL_SRC%"
echo [INFO] Working directory: %TOOL_SRC%

REM Execute
python src\main.py update "%CONFIG%" "%KEY%" --value %VALUE% --comment "%COMMENT%"

REM Restore directory
cd /d "%OLDDIR%"

:result
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Config updated
) else (
    echo [FAILED] Exit code: %ERRORLEVEL%
)

endlocal
pause
```

---

## 📋 问题诊断检查清单

如果遇到模块错误，按以下步骤检查：

### 1. 确认文件结构

```
d:\Demo\JsonEditTool\
├── src\
│   ├── main.py
│   ├── logger.py
│   ├── json_editor.py
│   └── validator.py
└── ...
```

**检查命令：**
```batch
dir d:\Demo\JsonEditTool\src\*.py
```

### 2. 确认当前工作目录

在脚本中添加：
```batch
echo Current directory: %CD%
pause
```

### 3. 测试Python能否找到模块

```batch
cd /d "d:\Demo\JsonEditTool"
python -c "import sys; sys.path.insert(0, 'src'); from logger import get_logger; print('OK')"
```

如果输出 `OK`，说明模块能正常导入。

### 4. 查看Python搜索路径

```batch
cd /d "d:\Demo\JsonEditTool"
python -c "import sys; print('\n'.join(sys.path))"
```

---

## 🛠️ 已为您创建的修复脚本

我已经创建了以下修复版本的脚本：

### 1. **simple_update.bat** ⭐ 推荐
- 简单易用
- 自动检测使用EXE或Python
- 自动切换到正确目录

### 2. **user_config_update.bat**
- 功能完整
- 包含备份、错误处理
- 详细的日志输出

### 3. **correct_user_script.bat** (已修复)
- 原有脚本的修复版本
- 添加了目录切换逻辑

---

## 💡 最佳实践

### 1. 优先使用EXE版本

```batch
REM 打包工具
cd d:\Demo\JsonEditTool
build.bat

REM 复制到目标位置
copy dist\JsonEditTool.exe C:\NISServer\DB\

REM 使用（无需担心模块问题）
C:\NISServer\DB\JsonEditTool.exe update ...
```

### 2. 使用Python时始终切换目录

```batch
cd /d "d:\Demo\JsonEditTool"
python src\main.py ...
```

### 3. 使用绝对路径

```batch
SET TOOL_DIR=d:\Demo\JsonEditTool
cd /d "%TOOL_DIR%"
python src\main.py ...
```

---

## 🧪 测试脚本

创建 `test_module.bat` 来测试：

```batch
@echo off
echo Testing module import...

cd /d "d:\Demo\JsonEditTool"

python -c "from src.logger import get_logger; print('logger: OK')"
python -c "from src.json_editor import JSONEditor; print('json_editor: OK')"
python -c "from src.validator import Validator; print('validator: OK')"

echo.
echo If all show OK, modules can be imported correctly.
pause
```

---

## 📊 错误对比

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `No module named 'logger'` | 工作目录不对 | `cd /d "项目目录"` |
| `No module named 'src'` | 使用了错误的导入 | 检查 `main.py` 导入语句 |
| `File not found: src\main.py` | 路径不存在 | 确认项目路径正确 |

---

## 🚀 立即使用

### 快速修复（3步）

#### 步骤1：使用简单脚本
```batch
cd d:\Demo\JsonEditTool
simple_update.bat
```

#### 步骤2：或者手动修改您的脚本
在 `python src\main.py` 之前添加：
```batch
cd /d "d:\Demo\JsonEditTool"
```

#### 步骤3：或者打包使用EXE
```batch
cd d:\Demo\JsonEditTool
build.bat
copy dist\JsonEditTool.exe C:\NISServer\DB\
```

---

## ✅ 验证修复

运行修复后的脚本，应该看到：

```
Updating configuration...
[INFO] Using Python version
[INFO] Working directory: d:\Demo\JsonEditTool

2026-01-28 XX:XX:XX - INFO - ============================================================
2026-01-28 XX:XX:XX - INFO - 开始处理: update C:\NISServer\config.json ...
...
操作成功: update Judge/ProcessHandleDeviceAutoContrbands
```

**没有** `ModuleNotFoundError` 错误！

---

**更新时间**: 2026-01-28  
**版本**: 1.0
