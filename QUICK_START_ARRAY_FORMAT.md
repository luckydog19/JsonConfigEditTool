# 快速上手 - 数组格式配置文件

## 🚀 5分钟快速开始

### 前提条件
- ✅ Windows系统
- ✅ 已安装Python 3.8+（打包后不需要）
- ✅ 有需要修改的JSON配置文件

---

## 第一步：准备工具

### 方式1：使用EXE（推荐）
```batch
# 打包工具
cd d:\Demo\JsonEditTool
build.bat

# 复制到目标位置
copy dist\JsonEditTool.exe C:\NISServer\DB\
```

### 方式2：直接使用Python
```batch
# 确保在项目目录
cd d:\Demo\JsonEditTool

# 直接运行
python src\main.py --help
```

---

## 第二步：了解你的配置文件格式

### 你的配置文件是这种格式吗？
```json
[
  {
    "key": "Globle/UseConsul",
    "value": "false",
    "_comment": "是否启用Consul"
  },
  {
    "key": "Judge/ProcessHandleDeviceAutoContrbands",
    "value": true,
    "_comment": "自动处理违禁品"
  }
]
```

✅ 是的！这就是**数组格式**，工具完全支持！

---

## 第三步：第一个命令

### 示例：修改配置项

```batch
# 使用EXE
C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value true

# 或使用Python
python src\main.py update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value true
```

**命令说明：**
- `update` - 操作类型（修改）
- `"C:\NISServer\config.json"` - 配置文件路径
- `"Judge/ProcessHandleDeviceAutoContrbands"` - 配置项的key（注意是斜杠分隔）
- `--value true` - 新的值

---

## 第四步：在BAT脚本中使用

### 创建配置更新脚本

创建文件：`update_config.bat`

```batch
@echo off
REM NIS配置更新脚本

echo ========================================
echo NIS Configuration Update Script
echo ========================================
echo.

REM 定义工具和配置文件路径
set TOOL=C:\NISServer\DB\JsonEditTool.exe
set CONFIG=C:\NISServer\config.json

REM 定义配置值（可以从外部读取）
set Judge_ProcessHandleDeviceAutoContrbands=true
set Globle_UseConsul=false
set Globle_ConsulURI=http://127.0.0.1:8500

echo [1/3] Updating Judge/ProcessHandleDeviceAutoContrbands...
"%TOOL%" update "%CONFIG%" "Judge/ProcessHandleDeviceAutoContrbands" --value %Judge_ProcessHandleDeviceAutoContrbands%
if %ERRORLEVEL% EQU 0 (
    echo [OK] Success
) else (
    echo [ERROR] Failed
    goto :error
)

echo [2/3] Updating Globle/UseConsul...
"%TOOL%" update "%CONFIG%" "Globle/UseConsul" --value %Globle_UseConsul%
if %ERRORLEVEL% EQU 0 (
    echo [OK] Success
) else (
    echo [ERROR] Failed
    goto :error
)

echo [3/3] Updating Globle/ConsulURI...
"%TOOL%" update "%CONFIG%" "Globle/ConsulURI" --value "%Globle_ConsulURI%"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Success
) else (
    echo [ERROR] Failed
    goto :error
)

echo.
echo ========================================
echo All configurations updated successfully!
echo ========================================
pause
exit /b 0

:error
echo.
echo ========================================
echo Configuration update failed!
echo Please check the log file for details.
echo ========================================
pause
exit /b 1
```

---

## 第五步：常用操作

### 1. 修改配置（Update）
```batch
REM 基本语法
JsonEditTool.exe update <配置文件路径> <key> --value <新值>

REM 示例
JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true

REM 带注释
JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "启用自动处理"
```

### 2. 添加配置（Add）
```batch
REM 基本语法
JsonEditTool.exe add <配置文件路径> <key> --value <值>

REM 示例
JsonEditTool.exe add "C:\NISServer\config.json" "New/Config/Item" --value "test" --comment "新配置项"
```

### 3. 删除配置（Delete）
```batch
REM 基本语法
JsonEditTool.exe delete <配置文件路径> <key>

REM 示例
JsonEditTool.exe delete "C:\NISServer\config.json" "Old/Config/Item"
```

---

## 🎯 实战案例

### 案例1：根据环境变量更新配置

```batch
@echo off
REM 从环境变量或配置文件读取参数

REM 设置参数（可以从注册表、ini文件等读取）
set AUTO_HANDLE=true
set CONSUL_ENABLED=false
set API_URL=https://192.168.100.1:30006/SignalR

REM 批量更新
set TOOL=C:\NISServer\DB\JsonEditTool.exe
set CONFIG=C:\NISServer\config.json

"%TOOL%" update "%CONFIG%" "Judge/ProcessHandleDeviceAutoContrbands" --value %AUTO_HANDLE%
"%TOOL%" update "%CONFIG%" "Globle/UseConsul" --value %CONSUL_ENABLED%
"%TOOL%" update "%CONFIG%" "Globle/SignalRWebServer" --value "%API_URL%"

echo Configuration updated from environment variables!
```

### 案例2：部署脚本自动更新配置

```batch
@echo off
REM 自动化部署脚本

echo Starting deployment...

REM 检测环境（通过参数或其他方式）
set ENV=%1
if "%ENV%"=="" set ENV=dev

echo Deploying to %ENV% environment...

REM 根据环境设置不同的配置值
if "%ENV%"=="prod" (
    set AUTO_HANDLE=true
    set API_URL=https://prod.server.com/api
    set LOG_LEVEL=ERROR
) else if "%ENV%"=="test" (
    set AUTO_HANDLE=true
    set API_URL=https://test.server.com/api
    set LOG_LEVEL=WARN
) else (
    set AUTO_HANDLE=false
    set API_URL=http://dev.server.com:8080/api
    set LOG_LEVEL=DEBUG
)

REM 更新配置
JsonEditTool.exe update config.json "Judge/ProcessHandleDeviceAutoContrbands" --value %AUTO_HANDLE%
JsonEditTool.exe update config.json "API/Endpoint" --value "%API_URL%"
JsonEditTool.exe update config.json "System/LogLevel" --value "%LOG_LEVEL%"

echo Deployment to %ENV% completed!
```

---

## ⚠️ 重要提示

### 1. 路径包含空格必须用引号
```batch
# 正确 ✅
"C:\Program Files\My App\config.json"

# 错误 ❌
C:\Program Files\My App\config.json
```

### 2. Key使用斜杠分隔（不是点号）
```batch
# 数组格式使用斜杠 ✅
"Judge/ProcessHandleDeviceAutoContrbands"

# 对象格式使用点号 ✅
"server.port"

# 根据你的JSON格式选择正确的分隔符
```

### 3. 值包含特殊字符需要引号
```batch
# URL等包含特殊字符的值 ✅
--value "https://api.com:8080/v1?key=abc"

# 路径包含反斜杠 ✅
--value "C:\Program Files\App"

# 简单的布尔值和数字不需要引号 ✅
--value true
--value 123
```

### 4. 检查操作结果
```batch
JsonEditTool.exe update config.json "key" --value "value"

if %ERRORLEVEL% EQU 0 (
    echo Success!
) else (
    echo Failed! Check logs in src\logs\
    exit /b 1
)
```

---

## 🔍 故障排查

### 问题1：提示"配置项不存在"
**原因**：使用了`update`操作但key不存在  
**解决**：改用`add`操作

```batch
# 如果不确定是否存在，可以先尝试update，失败后再add
"%TOOL%" update "%CONFIG%" "key" --value "value"
if %ERRORLEVEL% NEQ 0 (
    "%TOOL%" add "%CONFIG%" "key" --value "value"
)
```

### 问题2：提示"配置项已存在"
**原因**：使用了`add`操作但key已存在  
**解决**：改用`update`操作

### 问题3：修改后值不对
**原因**：类型自动推断  
**说明**：
- `true`/`false` → 布尔值
- `123` → 数字
- `"text"` → 字符串

**解决**：如需字符串类型，请加引号：`--value "\"true\""`

### 问题4：找不到文件
**原因**：路径错误或权限不足  
**解决**：
1. 检查文件路径是否正确
2. 以管理员身份运行BAT脚本
3. 确保文件存在且可读写

---

## 📚 更多资源

### 详细文档
- **ARRAY_FORMAT_GUIDE.md** - 完整使用指南
- **UPGRADE_SUMMARY.md** - 升级说明
- **设计文档.md** - 技术设计文档

### 示例脚本
- `examples/example_array_format.bat` - 数组格式完整示例
- `examples/example_single.bat` - 单文件修改示例
- `examples/example_multi_files.bat` - 多文件批量修改

### 帮助命令
```batch
# 查看完整帮助
JsonEditTool.exe --help

# 查看版本
JsonEditTool.exe --version
```

### 日志文件
所有操作都会记录到：`src\logs\json_edit_tool_YYYYMMDD.log`

---

## ✅ 完成清单

学完本指南后，你应该能够：
- [x] 使用工具修改配置文件
- [x] 在BAT脚本中调用工具
- [x] 使用环境变量传递参数
- [x] 处理特殊字符和路径
- [x] 进行基本的错误处理
- [x] 查看日志排查问题

---

**需要帮助？**查看完整文档`ARRAY_FORMAT_GUIDE.md`或查看日志文件！

**准备好了吗？**现在就试试修改你的第一个配置吧！ 🚀
