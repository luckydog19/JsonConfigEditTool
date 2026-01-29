# BAT脚本变量使用指南

## 🚨 核心问题：引号的正确使用

### ❌ 错误用法（您的脚本中的问题）

```batch
SET Comment="分组判图没有程处理违禁品关..."
SET Judge_ProcessHandleDeviceAutoContrbands="false"

python src\main.py add "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment %Comment%
```

**问题分析：**
1. 变量赋值时包含了引号 → 变量值变成 `"false"` 而不是 `false`
2. 命令行中 `%Comment%` 没有加引号 → 空格和特殊字符会导致参数分割错误
3. 实际执行的命令变成：
   ```
   python ... --value "false" --comment "分组判图..." "，正常的分组流程)"
   ```
   参数被错误分割了！

---

### ✅ 正确用法

```batch
REM 1. 变量赋值时：不要加引号！
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

REM 2. 使用变量时：在命令中该加引号的地方加引号
python src\main.py add "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands% --comment "%Comment%"
```

**为什么正确：**
1. 变量值干净，没有多余的引号：`Comment=分组判图...`
2. 命令中给 `%Comment%` 加了引号 → 整个注释被当作一个参数
3. 实际执行的命令：
   ```
   python ... --value false --comment "分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)"
   ```
   参数正确！

---

## 📋 引号使用规则总结

### 规则 1：变量赋值

| 场景 | 写法 | 说明 |
|------|------|------|
| ✅ 正确 | `SET VAR=value` | 不加引号，值干净 |
| ✅ 正确 | `SET VAR=value with spaces` | 即使有空格也不加引号 |
| ❌ 错误 | `SET VAR="value"` | 引号会成为值的一部分 |
| ❌ 错误 | `SET VAR='value'` | 单引号也会成为值的一部分 |

**示例：**
```batch
REM 正确
SET NAME=John
SET PATH=C:\Program Files\MyApp
SET COMMENT=这是一段包含空格和逗号，以及括号（）的文本

REM 错误
SET NAME="John"              → 变量值变成: "John"
SET PATH="C:\Program Files"  → 变量值变成: "C:\Program Files"
```

---

### 规则 2：变量使用

| 场景 | 是否需要引号 | 示例 |
|------|-------------|------|
| 值不包含空格 | 不需要 | `--value %PORT%` |
| 值可能包含空格 | **需要** | `--comment "%COMMENT%"` |
| 路径 | **需要** | `"%CONFIG_FILE%"` |
| 文件名可能有空格 | **需要** | `"%FILE_PATH%"` |

**示例：**
```batch
SET PORT=8080
SET COMMENT=This is a long comment with spaces
SET CONFIG=C:\Program Files\App\config.json

REM 正确的使用
python tool.py --port %PORT%                        ← 不需要引号
python tool.py --comment "%COMMENT%"                ← 需要引号（有空格）
python tool.py --config "%CONFIG%"                  ← 需要引号（路径可能有空格）
```

---

## 🎯 针对您的场景的完整示例

### 场景：修改 Judge/ProcessHandleDeviceAutoContrbands 配置

#### ✅ 正确脚本

```batch
@echo off
chcp 65001 >nul

REM ============================================
REM 步骤1: 定义变量（不要加引号！）
REM ============================================
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

REM ============================================
REM 步骤2: 执行命令（注释参数加引号！）
REM ============================================
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value %Judge_ProcessHandleDeviceAutoContrbands% ^
    --comment "%Comment%"

if %ERRORLEVEL% EQU 0 (
    echo Success!
) else (
    echo Failed!
)

pause
```

---

#### ❌ 错误脚本（不要这样写）

```batch
@echo off

REM 错误1: 变量赋值时加了引号
SET Comment="分组判图没有程处理违禁品关..."
SET Judge_ProcessHandleDeviceAutoContrbands="false"

REM 错误2: 命令中注释没加引号
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value %Judge_ProcessHandleDeviceAutoContrbands% ^
    --comment %Comment%

pause
```

**为什么错误：**
1. `Comment` 的值变成了 `"分组判图..."`（包含引号）
2. 命令行解析时，空格和特殊字符会导致参数被错误分割
3. 工具收到的参数是错乱的

---

## 🔍 调试技巧

### 技巧 1：查看变量实际值

```batch
SET Comment=测试内容
echo Variable value: [%Comment%]
pause
```

输出应该是：`Variable value: [测试内容]`
如果是：`Variable value: ["测试内容"]` 说明有问题！

---

### 技巧 2：显示实际执行的命令

```batch
SET VALUE=false
SET COMMENT=测试注释

REM 先显示命令，不执行
echo About to execute:
echo JsonEditTool.exe update "config.json" "key" --value %VALUE% --comment "%COMMENT%"
pause

REM 确认后再执行
JsonEditTool.exe update "config.json" "key" --value %VALUE% --comment "%COMMENT%"
```

---

### 技巧 3：测试变量是否包含引号

```batch
SET TEST="value"
if "%TEST%"=="""value""" (
    echo ERROR: Variable contains unwanted quotes!
    echo Please remove quotes from assignment
) else (
    echo OK: Variable is clean
)
```

---

## 📝 快速参考卡片

### 常见值类型的处理

| 值类型 | 赋值 | 使用 |
|--------|------|------|
| 布尔值 | `SET VAR=true` | `--value %VAR%` |
| 数字 | `SET PORT=8080` | `--value %PORT%` |
| 简单字符串 | `SET NAME=test` | `--value %NAME%` |
| 包含空格的字符串 | `SET MSG=hello world` | `--value "%MSG%"` |
| 路径 | `SET PATH=C:\App` | `"%PATH%"` |
| URL | `SET URL=http://example.com` | `--value %URL%` |
| 中文 | `SET TEXT=测试` | `--value "%TEXT%"` |
| 包含特殊字符 | `SET CMT=a,b(c)` | `--comment "%CMT%"` |

---

## 🚀 实战示例集合

### 示例 1：修改布尔值

```batch
@echo off
SET VALUE=false
JsonEditTool.exe update "config.json" "enable.debug" --value %VALUE%
```

---

### 示例 2：修改带中文注释的配置

```batch
@echo off
chcp 65001 >nul
SET COMMENT=启用调试模式，生产环境请设置为false
JsonEditTool.exe update "config.json" "debug" --value true --comment "%COMMENT%"
```

---

### 示例 3：修改URL配置

```batch
@echo off
SET URL=https://api.example.com:8080/v1/endpoint?key=abc
SET COMMENT=API接口地址
JsonEditTool.exe update "config.json" "api.endpoint" --value %URL% --comment "%COMMENT%"
```

---

### 示例 4：批量修改多个配置

```batch
@echo off
chcp 65001 >nul

REM 定义所有变量
SET HOST=192.168.1.100
SET PORT=8080
SET TIMEOUT=30
SET COMMENT1=服务器地址
SET COMMENT2=服务器端口
SET COMMENT3=超时时间（秒）

REM 批量执行
JsonEditTool.exe update "config.json" "server.host" --value %HOST% --comment "%COMMENT1%"
JsonEditTool.exe update "config.json" "server.port" --value %PORT% --comment "%COMMENT2%"
JsonEditTool.exe update "config.json" "server.timeout" --value %TIMEOUT% --comment "%COMMENT3%"

echo All configs updated!
pause
```

---

### 示例 5：使用环境变量

```batch
@echo off
REM 从外部获取值（比如Jenkins、用户输入等）
SET /P USER_VALUE="Enter value (true/false): "
SET /P USER_COMMENT="Enter comment: "

JsonEditTool.exe update "config.json" "my.key" --value %USER_VALUE% --comment "%USER_COMMENT%"
```

---

## ⚠️ 常见错误和解决方案

### 错误 1：参数被分割

**现象：**
```
错误: 无法识别的参数 "正常的分组流程)"
```

**原因：** 注释参数没有用引号包裹

**解决：**
```batch
REM 错误
--comment %COMMENT%

REM 正确
--comment "%COMMENT%"
```

---

### 错误 2：布尔值变成字符串

**现象：**
```json
{
    "key": "test",
    "value": "\"false\"",   ← 变成了字符串 "false"
    "_comment": "..."
}
```

**原因：** 变量赋值时加了引号

**解决：**
```batch
REM 错误
SET VALUE="false"

REM 正确
SET VALUE=false
```

---

### 错误 3：路径找不到

**现象：**
```
Error: File not found: C:\Program
```

**原因：** 路径包含空格，但使用时没加引号

**解决：**
```batch
SET PATH=C:\Program Files\App\config.json

REM 错误
JsonEditTool.exe update %PATH% ...

REM 正确
JsonEditTool.exe update "%PATH%" ...
```

---

## 📚 总结

### 核心规则（必须记住）

1. **变量赋值：不要加引号**
   ```batch
   SET VAR=value      ← 正确
   SET VAR="value"    ← 错误
   ```

2. **变量使用：根据内容决定是否加引号**
   ```batch
   %VAR%              ← 简单值，不需要
   "%VAR%"            ← 包含空格/特殊字符，需要
   ```

3. **路径：始终加引号**
   ```batch
   "%PATH%"           ← 始终加引号，防止路径包含空格
   ```

4. **注释：始终加引号**
   ```batch
   --comment "%COMMENT%"   ← 始终加引号，注释通常包含空格
   ```

---

## 🎯 您的最终脚本

```batch
@echo off
chcp 65001 >nul

REM 变量定义（不加引号！）
SET Comment=分组判图没有程处理违禁品关，true就开启(根据站点总品创建成的)，false为关闭(不处理违禁品，正常的分组流程)
SET Judge_ProcessHandleDeviceAutoContrbands=false

REM 执行命令（注释加引号！）
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value %Judge_ProcessHandleDeviceAutoContrbands% ^
    --comment "%Comment%"

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Config updated
) else (
    echo [FAILED] Update failed, exit code: %ERRORLEVEL%
)

pause
```

---

**记住这一点，就不会出错了：**
> 赋值不要引号，使用看情况！

---

**更新时间**: 2026-01-28  
**版本**: 1.0
