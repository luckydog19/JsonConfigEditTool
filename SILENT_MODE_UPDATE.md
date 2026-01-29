# 静默模式更新说明

## 📋 更新内容

根据您的需求，已完成以下修改：

### 1. ✅ 添加静默模式
- 新增 `--silent` 参数
- 静默模式下不输出INFO日志到控制台
- 所有日志仍会写入日志文件

### 2. ✅ 修改日志目录名称
- 原日志目录：`logs`
- 新日志目录：**`jsonedittoollogs`**

### 3. ✅ 日志文件位置
根据执行方式不同，日志文件位置如下：

| 执行方式 | 日志目录位置 |
|---------|-------------|
| EXE版本 | `C:\NISServer\DB\jsonedittoollogs\` |
| Python开发 | `d:\Demo\JsonEditTool\src\jsonedittoollogs\` |
| Python打包测试 | `d:\Demo\JsonEditTool\jsonedittoollogs\` |

日志文件名格式：`json_edit_tool_YYYYMMDD.log`

例如：`json_edit_tool_20260128.log`

---

## 🚀 使用方法

### 静默模式命令

#### 基本用法
```batch
JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "注释" --silent
```

#### Python版本
```batch
python src\main.py update "config.json" "key" --value "value" --comment "注释" --silent
```

---

### 输出对比

#### ❌ 非静默模式（默认）
```
2026-01-28 15:02:28 - INFO - ============================================================
2026-01-28 15:02:28 - INFO - 开始处理: update C:\NISServer\config.json Judge/ProcessHandleDeviceAutoContrbands
2026-01-28 15:02:28 - INFO - 参数: value=true, comment=..., encoding=utf-8
2026-01-28 15:02:28 - INFO - 规范化路径: C:\NISServer\config.json -> C:\NISServer\config.json
2026-01-28 15:02:28 - INFO - 成功加载配置文件: C:\NISServer\config.json
2026-01-28 15:02:28 - INFO - 执行修改操作: Judge/ProcessHandleDeviceAutoContrbands
... (更多日志)
操作成功: update Judge/ProcessHandleDeviceAutoContrbands
```

#### ✅ 静默模式（--silent）
```
(无输出，执行完成立即返回)
```

**日志仍然会写入到日志文件中！**

---

## 📝 修改的文件

### 1. `src/logger.py`
- 修改 `__init__` 方法，添加 `silent` 参数
- 修改 `get_logger` 函数，添加 `silent` 参数
- 静默模式下不添加控制台Handler
- 修改默认日志目录为 `jsonedittoollogs`
- 改用简单的 `FileHandler` 替代 `TimedRotatingFileHandler`（更稳定）

### 2. `src/main.py`
- 添加 `--silent` 命令行参数
- 修改日志目录为 `jsonedittoollogs`
- 在静默模式下：
  - 不输出INFO日志到控制台
  - 不输出成功提示信息
  - 不输出"使用 --help 查看帮助"等提示
  - **错误信息仍会输出**（便于故障排查）

### 3. `simple_update.bat`
- 添加 `--silent` 参数到命令中
- 更新提示信息

### 4. `build.bat`
- 添加 `--hidden-import` 参数确保所有模块被打包
- 添加 `--paths=src` 参数指定模块搜索路径

---

## 🎯 静默模式特性

| 项目 | 非静默模式 | 静默模式 |
|------|-----------|---------|
| INFO日志 | ✅ 控制台 + 文件 | ❌ 仅文件 |
| 成功提示 | ✅ 显示 | ❌ 不显示 |
| 错误信息 | ✅ 显示 | ✅ 显示 |
| 日志文件 | ✅ 写入 | ✅ 写入 |
| 返回码 | ✅ 0=成功 | ✅ 0=成功 |

---

## 💡 使用场景

### 适合静默模式的场景：
1. ✅ 批处理脚本中调用
2. ✅ 定时任务/计划任务
3. ✅ 自动化脚本
4. ✅ 后台服务调用
5. ✅ 不需要实时查看日志的场景

### 适合非静默模式的场景：
1. ✅ 手动运行，需要实时反馈
2. ✅ 调试和故障排查
3. ✅ 学习和了解工具工作流程
4. ✅ 交互式使用

---

## 🧪 测试验证

### 测试1：静默模式不输出
```batch
cd d:\Demo\JsonEditTool
python src\main.py update tests\test_array_config.json "Globle/UseConsul" --value false --silent
```

**预期结果：** 无任何控制台输出，命令立即返回

### 测试2：日志文件记录
```batch
# 执行上述命令后，查看日志文件
type src\jsonedittoollogs\json_edit_tool_20260128.log
```

**预期结果：** 日志文件中有完整的操作记录

### 测试3：错误仍会输出
```batch
python src\main.py update nonexistent.json "key" --value "value" --silent
```

**预期结果：** 输出错误信息到控制台

---

## 📋 更新后的脚本示例

### 示例1：简单静默更新

```batch
@echo off
chcp 65001 >nul

REM 静默更新配置
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value true ^
    --comment "分组判图没有程处理违禁品关" ^
    --silent

REM 检查返回码
if %ERRORLEVEL% EQU 0 (
    echo Config updated successfully
) else (
    echo Config update failed: %ERRORLEVEL%
)
```

### 示例2：批量静默更新

```batch
@echo off
chcp 65001 >nul

echo Starting batch update...

REM 更新配置1（静默）
C:\NISServer\DB\JsonEditTool.exe update "config1.json" "key1" --value "value1" --silent
if %ERRORLEVEL% NEQ 0 echo [FAILED] config1.json

REM 更新配置2（静默）
C:\NISServer\DB\JsonEditTool.exe update "config2.json" "key2" --value "value2" --silent
if %ERRORLEVEL% NEQ 0 echo [FAILED] config2.json

REM 更新配置3（静默）
C:\NISServer\DB\JsonEditTool.exe update "config3.json" "key3" --value "value3" --silent
if %ERRORLEVEL% NEQ 0 echo [FAILED] config3.json

echo Batch update completed!
```

### 示例3：带日志查看的静默脚本

```batch
@echo off
chcp 65001 >nul

SET TOOL=C:\NISServer\DB\JsonEditTool.exe
SET LOG_DIR=C:\NISServer\DB\jsonedittoollogs
SET LOG_FILE=%LOG_DIR%\json_edit_tool_%date:~0,4%%date:~5,2%%date:~8,2%.log

echo Updating config (silent mode)...

REM 静默更新
%TOOL% update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --silent

REM 显示结果
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Config updated
    echo.
    echo Last 5 log entries:
    powershell -Command "Get-Content '%LOG_FILE%' -Tail 5"
) else (
    echo [FAILED] Update failed
    echo.
    echo Error log:
    powershell -Command "Get-Content '%LOG_FILE%' | Select-String 'ERROR' | Select-Object -Last 3"
)
```

---

## 🔧 重新打包

修改后需要重新打包：

```batch
cd d:\Demo\JsonEditTool
build.bat
copy dist\JsonEditTool.exe C:\NISServer\DB\
```

---

## 📊 日志文件示例

日志文件内容示例（`jsonedittoollogs/json_edit_tool_20260128.log`）：

```
2026-01-28 15:03:20 - INFO - ============================================================
2026-01-28 15:03:20 - INFO - 开始处理: update C:\NISServer\config.json Judge/ProcessHandleDeviceAutoContrbands
2026-01-28 15:03:20 - INFO - 参数: value=true, comment=分组判图..., encoding=utf-8
2026-01-28 15:03:20 - INFO - 规范化路径: C:\NISServer\config.json -> C:\NISServer\config.json
2026-01-28 15:03:20 - INFO - 成功加载配置文件: C:\NISServer\config.json
2026-01-28 15:03:20 - INFO - 执行修改操作: Judge/ProcessHandleDeviceAutoContrbands
2026-01-28 15:03:20 - INFO - 值类型推断: true (str) -> True (bool)
2026-01-28 15:03:20 - INFO - 旧值: False
2026-01-28 15:03:20 - INFO - 更新值: true
2026-01-28 15:03:20 - INFO - 更新注释: 分组判图没有程处理违禁品关...
2026-01-28 15:03:20 - INFO - 保存配置文件成功: C:\NISServer\config.json
2026-01-28 15:03:20 - INFO - 操作完成: update Judge/ProcessHandleDeviceAutoContrbands
2026-01-28 15:03:20 - INFO - ============================================================
```

---

## ✅ 验证清单

打包和部署后，请验证：

- [ ] 运行 `JsonEditTool.exe --help` 能看到 `--silent` 参数
- [ ] 使用 `--silent` 参数时无控制台输出
- [ ] 日志目录名称为 `jsonedittoollogs`
- [ ] 日志文件正常创建和写入
- [ ] 错误情况下仍有错误信息输出
- [ ] 返回码正确（0=成功，非0=失败）

---

## 🎉 总结

所有修改已完成！主要特性：

1. ✅ **静默模式**：使用 `--silent` 参数完全静默执行
2. ✅ **日志目录改名**：`logs` → `jsonedittoollogs`
3. ✅ **日志正常记录**：所有操作都会记录到日志文件
4. ✅ **错误仍会显示**：关键错误信息不会被隐藏
5. ✅ **向后兼容**：不使用 `--silent` 时行为与之前一致

---

**更新时间**: 2026-01-28  
**版本**: 2.0
