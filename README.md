# JsonEditTool - JSON 配置文件编辑工具

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个强大而灵活的命令行工具，用于快速修改 JSON 配置文件，特别适合批处理脚本和自动化部署场景。

## ✨ 主要特性

- 🎯 **简单易用** - 命令行操作，支持增删改
- 🔧 **灵活扩展** - 支持添加任意自定义字段（v1.1新增）
- 📁 **双格式支持** - 同时支持数组格式和对象格式的JSON
- 🌍 **多路径支持** - 相对路径、绝对路径、网络路径、环境变量路径
- 🔄 **自动类型推断** - 智能识别字符串、数字、布尔值
- 🔇 **静默模式** - 默认静默执行，适合批处理脚本
- 📝 **完整日志** - 所有操作记录到日志文件
- 🌐 **中文友好** - 完整支持中文路径和中文内容

## 🚀 快速开始

### 安装

#### 方式1：使用编译好的 EXE（推荐）
```bash
# 1. 下载 dist\JsonEditTool.exe
# 2. 将其放到任意目录或添加到系统 PATH
# 3. 直接使用
JsonEditTool.exe --help
```

#### 方式2：从源码构建
```bash
# 克隆或下载项目
cd D:\Demo\JsonConfigEditTool

# 安装依赖（仅Python运行时需要）
pip install -r requirements.txt

# 构建EXE
build.bat
```

### 基本用法

```bash
# 修改配置项
JsonEditTool.exe update config.json server.port --value 8080 --comment "服务器端口"

# 添加配置项
JsonEditTool.exe add config.json cache.enabled --value true --comment "启用缓存"

# 添加带额外字段的配置项（v1.1新增）
JsonEditTool.exe add config.json api.timeout --value 30 ^
    --extra type=int ^
    --extra unit=seconds ^
    --extra required=true

# 删除配置项
JsonEditTool.exe delete config.json old.key
```

## 📖 核心功能

### 1. Update - 修改配置项

修改现有配置项的值和注释。

```bash
# 基本用法
JsonEditTool.exe update config.json server.port --value 9000

# 修改值和注释
JsonEditTool.exe update config.json db.host --value "192.168.1.100" --comment "数据库地址"

# 支持点分路径（对象格式）
JsonEditTool.exe update config.json server.database.pool --value 20

# 支持斜杠分隔（数组格式）
JsonEditTool.exe update config.json "Judge/ProcessHandle" --value true
```

### 2. Add - 添加配置项

添加新的配置项到JSON文件。

```bash
# 基本添加
JsonEditTool.exe add config.json new.feature --value true --comment "新功能开关"

# 添加带额外字段（v1.1新增）
JsonEditTool.exe add config.json db.pool --value 10 ^
    --comment "连接池大小" ^
    --extra min=5 ^
    --extra max=20 ^
    --extra type=mysql
```

**生成的JSON：**
```json
{
    "db": {
        "pool": {
            "key": "pool",
            "value": 10,
            "_comment": "连接池大小",
            "min": 5,
            "max": 20,
            "type": "mysql"
        }
    }
}
```

### 3. Delete - 删除配置项

从JSON文件中删除配置项。

```bash
JsonEditTool.exe delete config.json old.setting
```

## 🎯 高级功能

### 额外字段支持（v1.1新增）

使用 `--extra` 参数可以为配置项添加任意自定义字段，不再局限于 `key`、`value`、`_comment`。

```bash
# 添加元数据
JsonEditTool.exe add config.json api.endpoint --value "https://api.example.com" ^
    --comment "API端点" ^
    --extra timeout=30 ^
    --extra retry=3 ^
    --extra auth=required ^
    --extra version=v2

# 添加功能开关
JsonEditTool.exe add features.json payment.alipay --value true ^
    --comment "支付宝支付" ^
    --extra feature_name=alipay ^
    --extra since=2026-01-01 ^
    --extra experimental=false

# 数组格式也支持额外字段
JsonEditTool.exe add config.json "Feature/NewModule" --value true ^
    --extra module=feature ^
    --extra priority=high
```

**详细文档：** [EXTRA_FIELDS_GUIDE.md](EXTRA_FIELDS_GUIDE.md)

### 静默模式

v1.1版本默认启用静默模式，不输出INFO日志到控制台，适合批处理脚本。

```bash
# 默认静默执行（无控制台输出）
JsonEditTool.exe update config.json key --value value

# 需要查看详细日志时
JsonEditTool.exe update config.json key --value value --verbose
```

### 路径支持

```bash
# 相对路径
JsonEditTool.exe update config.json key --value value

# 绝对路径
JsonEditTool.exe update "D:\MyApp\config.json" key --value value

# 网络路径
JsonEditTool.exe update "\\server\share\config.json" key --value value

# 环境变量路径
JsonEditTool.exe update "%APPDATA%\MyApp\settings.json" key --value value
```

### 数据类型推断

工具会自动推断值的类型：

```bash
# 整数
--value 123          → 123 (int)

# 浮点数
--value 3.14         → 3.14 (float)

# 布尔值
--value true         → true (bool)
--value false        → false (bool)

# 字符串
--value "hello"      → "hello" (string)
```

### 备份功能

```bash
# 修改前自动创建备份
JsonEditTool.exe update config.json key --value value --backup
```

## 📋 命令行参数

### 通用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--value` | 配置项的值（update/add必需） | `--value 8080` |
| `--comment` | 配置项的注释 | `--comment "端口号"` |
| `--extra` | 额外字段（可多次使用） | `--extra type=int` |
| `--encoding` | 文件编码（默认utf-8） | `--encoding gbk` |
| `--indent` | JSON缩进空格数（默认4） | `--indent 2` |
| `--backup` | 修改前创建备份 | `--backup` |
| `--silent` | 静默模式（默认启用） | `--silent` |
| `--verbose` | 详细模式（显示日志） | `--verbose` |
| `--version` | 显示版本信息 | `--version` |
| `--help` | 显示帮助信息 | `--help` |

## 📦 批处理脚本示例

### 简单示例

```batch
@echo off
SET TOOL=JsonEditTool.exe
SET CONFIG=C:\MyApp\config.json

REM 更新服务器配置
%TOOL% update %CONFIG% server.port --value 8080 --comment "Web端口"
%TOOL% update %CONFIG% server.host --value "0.0.0.0" --comment "监听地址"

REM 启用功能
%TOOL% update %CONFIG% features.cache --value true --comment "启用缓存"

echo 配置更新完成！
pause
```

### 带错误处理的示例

```batch
@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

SET TOOL=JsonEditTool.exe
SET CONFIG=C:\MyApp\config.json

echo 开始更新配置...

REM 更新端口
%TOOL% update %CONFIG% server.port --value 9000
if !ERRORLEVEL! NEQ 0 (
    echo [错误] 更新端口失败
    pause
    exit /b 1
)

REM 添加新配置（带额外字段）
%TOOL% add %CONFIG% api.timeout --value 30 ^
    --extra type=int ^
    --extra unit=seconds

if !ERRORLEVEL! NEQ 0 (
    echo [错误] 添加配置失败
    pause
    exit /b 1
)

echo [成功] 所有配置更新完成！
pause
```

## 🔧 JSON 格式支持

### 对象格式（Object Format）

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

**使用点分路径：**
```bash
JsonEditTool.exe update config.json server.port --value 9000
```

### 数组格式（Array Format）

```json
[
    {
        "key": "Judge/ProcessHandle",
        "value": true,
        "_comment": "处理开关"
    }
]
```

**使用斜杠分隔：**
```bash
JsonEditTool.exe update config.json "Judge/ProcessHandle" --value false
```

## 📝 日志

所有操作都会记录到日志文件：

```
工具所在目录\jsonedittoollogs\json_edit_tool_YYYYMMDD.log
```

日志内容包括：
- 操作时间和类型
- 文件路径
- 修改的键值
- 操作结果
- 错误信息（如有）

## 🐛 错误代码

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 文件不存在 |
| 2 | JSON格式错误 |
| 3 | 编码错误 |
| 4 | 键不存在 |
| 5 | 参数无效 |
| 6 | 权限不足 |
| 7 | 键已存在（add操作） |
| 99 | 未知错误 |

## 📚 相关文档

- [CHANGELOG.md](CHANGELOG.md) - 版本更新记录
- [EXTRA_FIELDS_GUIDE.md](EXTRA_FIELDS_GUIDE.md) - 额外字段功能详细指南
- [DESIGN.md](DESIGN.md) - 设计文档
- [examples/](examples/) - 示例脚本集合

## 🔄 版本历史

### v1.1.0 (2026-01-29) - 当前版本
- ✨ 新增 `--extra` 参数支持任意额外字段
- ✨ 默认启用静默模式
- 🐛 修复 logger 初始化问题
- 📝 完善文档和示例

### v1.0.0 (2026-01-28)
- 🎉 初始版本发布
- ✅ 支持 update/add/delete 操作
- ✅ 支持双格式 JSON
- ✅ 支持多种路径类型

**完整更新日志：** [CHANGELOG.md](CHANGELOG.md)

## 💡 使用技巧

1. **变量使用**：BAT脚本中使用变量时，不要在赋值时加引号
   ```batch
   SET VALUE=true           # ✅ 正确
   SET VALUE="true"         # ❌ 错误
   ```

2. **包含空格的值**：使用时加引号
   ```batch
   --comment "%COMMENT%"    # ✅ 正确
   ```

3. **路径包含空格**：整个路径加引号
   ```batch
   JsonEditTool.exe update "D:\My App\config.json" key --value value
   ```

4. **静默执行**：默认就是静默的，适合自动化脚本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 支持

- 问题反馈：提交 Issue
- 功能建议：提交 Feature Request
- 使用帮助：查看文档或提交 Issue

---

**版本**: v1.1.0  
**更新日期**: 2026-01-29  
**项目地址**: D:\Demo\JsonConfigEditTool
