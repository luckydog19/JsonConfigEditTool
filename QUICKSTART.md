# 快速开始指南

## 🚀 5分钟上手 JsonEditTool

### 第一步：获取工具

#### 方式1：使用编译好的 EXE（推荐）
```bash
# 从 dist 目录获取
D:\Demo\JsonConfigEditTool\dist\JsonEditTool.exe
```

#### 方式2：从源码构建
```bash
cd D:\Demo\JsonConfigEditTool
build.bat
```

### 第二步：准备测试文件

创建一个测试配置文件 `test_config.json`:

```json
{
    "server": {
        "port": {
            "key": "port",
            "value": 8080,
            "_comment": "服务器端口"
        },
        "host": {
            "key": "host",
            "value": "localhost",
            "_comment": "服务器地址"
        }
    }
}
```

### 第三步：基本操作

#### 1. 修改配置
```bash
# 修改端口号
JsonEditTool.exe update test_config.json server.port --value 9000

# 修改端口号并添加注释
JsonEditTool.exe update test_config.json server.port --value 9000 --comment "新端口号"
```

#### 2. 添加配置
```bash
# 添加新配置项
JsonEditTool.exe add test_config.json server.debug --value true --comment "调试模式"

# 添加带额外字段的配置（v1.1新增）
JsonEditTool.exe add test_config.json api.timeout --value 30 ^
    --comment "API超时时间" ^
    --extra type=int ^
    --extra unit=seconds
```

#### 3. 删除配置
```bash
JsonEditTool.exe delete test_config.json server.debug
```

### 第四步：查看结果

```bash
# 查看修改后的文件
type test_config.json

# 查看日志
type jsonedittoollogs\json_edit_tool_20260129.log
```

## 💡 常见场景

### 场景1：批量更新配置

创建脚本 `update_config.bat`:

```batch
@echo off
SET TOOL=JsonEditTool.exe
SET CONFIG=config.json

echo 更新服务器配置...
%TOOL% update %CONFIG% server.port --value 8080
%TOOL% update %CONFIG% server.host --value "0.0.0.0"

echo 更新数据库配置...
%TOOL% update %CONFIG% db.host --value "192.168.1.100"
%TOOL% update %CONFIG% db.port --value 3306

echo 配置更新完成！
pause
```

### 场景2：添加完整配置

```batch
@echo off
SET TOOL=JsonEditTool.exe
SET CONFIG=config.json

REM 添加API配置（带完整元数据）
%TOOL% add %CONFIG% api.endpoint --value "https://api.example.com" ^
    --comment "API端点" ^
    --extra timeout=30 ^
    --extra retry=3 ^
    --extra auth=required

REM 添加缓存配置
%TOOL% add %CONFIG% cache.redis --value "127.0.0.1:6379" ^
    --comment "Redis地址" ^
    --extra ttl=3600 ^
    --extra enabled=true

echo 配置添加完成！
```

### 场景3：环境配置切换

```batch
@echo off
SET TOOL=JsonEditTool.exe
SET CONFIG=config.json

REM 切换到生产环境
echo 切换到生产环境...
%TOOL% update %CONFIG% env.mode --value "production"
%TOOL% update %CONFIG% db.host --value "prod-db.example.com"
%TOOL% update %CONFIG% debug.enabled --value false

echo 环境切换完成！
```

## 🎯 高级功能

### 静默模式（默认）

```bash
# 默认静默执行（无控制台输出）
JsonEditTool.exe update config.json key --value value

# 需要看详细日志时
JsonEditTool.exe update config.json key --value value --verbose
```

### 备份功能

```bash
# 修改前自动备份
JsonEditTool.exe update config.json key --value value --backup
```

### 不同路径类型

```bash
# 相对路径
JsonEditTool.exe update config.json key --value value

# 绝对路径
JsonEditTool.exe update "D:\MyApp\config.json" key --value value

# 网络路径
JsonEditTool.exe update "\\server\share\config.json" key --value value

# 环境变量
JsonEditTool.exe update "%APPDATA%\MyApp\config.json" key --value value
```

## 📝 数组格式示例

如果你的JSON是数组格式：

```json
[
    {
        "key": "Judge/ProcessHandle",
        "value": true,
        "_comment": "处理开关"
    }
]
```

使用方法：

```bash
# 修改（使用斜杠分隔）
JsonEditTool.exe update config.json "Judge/ProcessHandle" --value false

# 添加（也支持额外字段）
JsonEditTool.exe add config.json "Feature/NewModule" --value true ^
    --comment "新模块" ^
    --extra priority=high
```

## ⚠️ 注意事项

### 1. 变量使用（重要！）

**错误示例**:
```batch
SET VALUE="true"         # ❌ 错误：引号会成为值的一部分
```

**正确示例**:
```batch
SET VALUE=true           # ✅ 正确
--value %VALUE%          # ✅ 正确

SET COMMENT=这是注释     # ✅ 正确
--comment "%COMMENT%"    # ✅ 包含空格时使用引号
```

### 2. 路径空格

```bash
# 路径包含空格时，整个路径加引号
JsonEditTool.exe update "D:\My Application\config.json" key --value value
```

### 3. 中文支持

```bash
# 批处理脚本开头添加
@echo off
chcp 65001 >nul

# 然后正常使用中文
JsonEditTool.exe update config.json key --value "中文值" --comment "中文注释"
```

## 🔍 错误处理

### 检查返回码

```batch
JsonEditTool.exe update config.json key --value value

if %ERRORLEVEL% EQU 0 (
    echo [成功] 配置已更新
) else (
    echo [失败] 错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)
```

### 常见错误码

- `0` - 成功
- `1` - 文件不存在
- `2` - JSON格式错误
- `4` - 键不存在（update操作）
- `7` - 键已存在（add操作）

## 📚 更多资源

- **完整文档**: [README.md](README.md)
- **设计文档**: [DESIGN.md](DESIGN.md)
- **额外字段指南**: [EXTRA_FIELDS_GUIDE.md](EXTRA_FIELDS_GUIDE.md)
- **变更记录**: [CHANGELOG.md](CHANGELOG.md)
- **示例脚本**: [examples/](examples/)

## 💬 获取帮助

```bash
# 查看帮助
JsonEditTool.exe --help

# 查看版本
JsonEditTool.exe --version
```

---

现在你已经掌握了 JsonEditTool 的基本使用！🎉
