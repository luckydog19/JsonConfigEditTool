# 数组格式JSON配置文件使用指南

## 概述

工具现已全面支持两种JSON配置文件格式：

### 1. **数组格式**（Array Format）
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

### 2. **对象格式**（Object Format）
```json
{
  "server": {
    "port": {
      "key": "port",
      "value": 8080,
      "_comment": "服务器端口"
    }
  }
}
```

## 数组格式特性

### ✅ 支持的Key格式

1. **斜杠分隔** - `Judge/ProcessHandleDeviceAutoContrbands`
2. **带冒号** - `Network/API:Endpoint`
3. **点分路径** - `System.Config.Item`
4. **中文字符** - `系统/配置项`
5. **组合使用** - `App/Server:Port-8080`

### ✅ 支持的Value类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 字符串 | `"hello"` | 普通文本 |
| 布尔值 | `true` / `false` | 自动类型推断 |
| 数字 | `123` / `3.14` | 整数或浮点数 |
| URL | `"https://api.com:8080/v1?key=abc"` | 包含特殊字符 |
| 路径 | `"C:\\Program Files\\App"` | Windows路径 |
| 空值 | `null` | NULL值 |

### ✅ 支持的特殊字符

**Key中支持：**
- 斜杠 `/`
- 冒号 `:`
- 连字符 `-`
- 下划线 `_`
- 点号 `.`
- 中文字符

**Value中支持：**
- 所有可打印字符
- URL特殊字符：`://`, `?`, `&`, `=`, `%`
- 路径分隔符：`\`, `/`
- 引号（需要转义）：`\"`

**Comment中支持：**
- 任意文本（包括中文、标点、表情符号等）

## 使用示例

### 命令行方式

#### 1. 修改配置（Update）
```batch
JsonEditTool.exe update "C:\NISServer\config.json" "Judge/ProcessHandleDeviceAutoContrbands" --value true --comment "启用自动处理"
```

#### 2. 添加配置（Add）
```batch
JsonEditTool.exe add "C:\NISServer\config.json" "New/Config:Item" --value "test" --comment "新配置项"
```

#### 3. 删除配置（Delete）
```batch
JsonEditTool.exe delete "C:\NISServer\config.json" "Old/Config:Item"
```

### BAT脚本方式

#### 示例1：使用环境变量
```batch
@echo off
set Judge_ProcessHandleDeviceAutoContrbands=true

C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Judge/ProcessHandleDeviceAutoContrbands" ^
    --value %Judge_ProcessHandleDeviceAutoContrbands% ^
    --comment "从环境变量更新"
```

#### 示例2：批量修改多个配置
```batch
@echo off
setlocal enabledelayedexpansion

set TOOL=C:\NISServer\DB\JsonEditTool.exe
set CONFIG=C:\NISServer\config.json

REM 定义配置项
set "CONFIG_1=Globle/UseConsul true 启用Consul"
set "CONFIG_2=Globle/ConsulURI http://127.0.0.1:8500 Consul地址"
set "CONFIG_3=Judge/ProcessHandleDeviceAutoContrbands false 禁用自动处理"

REM 批量更新
for /L %%i in (1,1,3) do (
    for /F "tokens=1,2,* delims= " %%a in ("!CONFIG_%%i!") do (
        echo Updating: %%a
        "%TOOL%" update "%CONFIG%" "%%a" --value %%b --comment "%%c"
        if !ERRORLEVEL! NEQ 0 (
            echo [ERROR] Failed to update %%a
        )
    )
)

echo All updates completed!
pause
```

#### 示例3：带特殊字符的值
```batch
@echo off
set API_URL=https://192.168.100.1:30006/SignalR?token=abc123

C:\NISServer\DB\JsonEditTool.exe update ^
    "C:\NISServer\config.json" ^
    "Globle/SignalRWebServer" ^
    --value "%API_URL%" ^
    --comment "SignalR服务器地址（包含端口和令牌）"
```

### 特殊字符处理技巧

#### 1. 包含空格的值
使用引号包裹：
```batch
--value "C:\Program Files\My App"
```

#### 2. 包含引号的值
在BAT中使用转义：
```batch
--value "He said \"Hello\""
```

#### 3. 包含百分号的值
在BAT中使用双百分号：
```batch
--value "完成度: 100%%"
```

#### 4. 多行注释
使用分号或逗号分隔：
```batch
--comment "第一行说明；第二行说明；第三行说明"
```

## 实际应用场景

### 场景1：NIS服务器配置管理
```batch
@echo off
REM NIS服务器配置更新脚本

set TOOL=C:\NISServer\DB\JsonEditTool.exe
set CONFIG=C:\NISServer\config.json

REM 从配置文件或注册表读取参数
set UseConsul=false
set ConsulURI=http://127.0.0.1:8500
set AutoHandle=true
set SignalRServer=https://192.168.100.1:30006/SignalR

REM 更新配置
"%TOOL%" update "%CONFIG%" "Globle/UseConsul" --value %UseConsul%
"%TOOL%" update "%CONFIG%" "Globle/ConsulURI" --value "%ConsulURI%"
"%TOOL%" update "%CONFIG%" "Judge/ProcessHandleDeviceAutoContrbands" --value %AutoHandle%
"%TOOL%" update "%CONFIG%" "Globle/SignalRWebServer" --value "%SignalRServer%"

echo Configuration updated successfully!
```

### 场景2：自动化部署脚本
```batch
@echo off
REM 自动化部署：根据环境更新配置

set ENV=%1
if "%ENV%"=="" set ENV=dev

if "%ENV%"=="prod" (
    set API_URL=https://prod.api.server.com:443/v1
    set AUTO_HANDLE=true
    set LOG_LEVEL=ERROR
) else (
    set API_URL=http://dev.api.server.com:8080/v1
    set AUTO_HANDLE=false
    set LOG_LEVEL=DEBUG
)

REM 更新配置
JsonEditTool.exe update config.json "API/Endpoint" --value "%API_URL%"
JsonEditTool.exe update config.json "Judge/AutoHandle" --value %AUTO_HANDLE%
JsonEditTool.exe update config.json "System/LogLevel" --value "%LOG_LEVEL%"

echo Deployed to %ENV% environment!
```

## 错误处理

### 常见错误及解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `配置项不存在` | Key不存在 | 使用`add`而不是`update` |
| `配置项已存在` | Key已存在 | 使用`update`而不是`add` |
| `文件不存在` | 路径错误 | 检查文件路径是否正确 |
| `JSON格式错误` | 文件损坏 | 手动修复或恢复备份 |
| `权限不足` | 无写权限 | 以管理员身份运行 |

### 日志查看
所有操作都会记录日志到：`src\logs\json_edit_tool_YYYYMMDD.log`

## 最佳实践

### 1. 使用备份功能
```batch
JsonEditTool.exe update config.json "key" --value "value" --backup
```

### 2. 验证操作结果
```batch
JsonEditTool.exe update config.json "key" --value "value"
if %ERRORLEVEL% NEQ 0 (
    echo Update failed! Check logs.
    exit /b 1
)
```

### 3. 使用变量管理配置
```batch
REM 集中定义配置
set CONFIG_FILE=C:\NISServer\config.json
set TOOL=C:\NISServer\DB\JsonEditTool.exe

REM 使用变量
"%TOOL%" update "%CONFIG_FILE%" "key" --value "value"
```

### 4. 添加错误处理和日志
```batch
@echo off
setlocal enabledelayedexpansion

set LOG_FILE=update_%date:~0,4%%date:~5,2%%date:~8,2%.log

echo [%time%] Starting config update... >> %LOG_FILE%

"%TOOL%" update "%CONFIG%" "key" --value "value" 2>> %LOG_FILE%
if !ERRORLEVEL! EQU 0 (
    echo [%time%] Success >> %LOG_FILE%
) else (
    echo [%time%] Failed >> %LOG_FILE%
)
```

## 注意事项

⚠️ **重要提示：**

1. **引号使用**：路径和包含特殊字符的值必须用引号包裹
2. **编码问题**：确保BAT文件和JSON文件编码一致（推荐UTF-8）
3. **权限问题**：修改系统目录下的文件可能需要管理员权限
4. **备份策略**：修改重要配置前建议开启`--backup`选项
5. **类型推断**：`true`/`false`会自动转换为布尔值，如需字符串请用引号

## 更新日志

**2026-01-28 - v1.0**
- ✅ 支持数组格式JSON配置文件
- ✅ 支持斜杠分隔的key
- ✅ 支持key和value中的特殊字符
- ✅ 自动检测并适配JSON格式
- ✅ 完善的错误处理和日志记录

## 技术支持

如有问题，请查看：
1. 日志文件：`src\logs\json_edit_tool_*.log`
2. 帮助信息：`JsonEditTool.exe --help`
3. 示例脚本：`examples\example_array_format.bat`
