# JSON配置文件修改工具

一个Windows平台下的JSON配置文件修改工具，支持通过BAT脚本调用，实现配置项的增删改操作。

## 功能特性

✅ **灵活的路径支持**
- 绝对路径：`D:\App\config.json`
- 相对路径：`.\configs\app.json`
- 网络路径：`\\server\share\config.json`
- 环境变量：`%APPDATA%\config.json`

✅ **完整的CRUD操作**
- 修改配置项（update）
- 添加配置项（add）
- 删除配置项（delete）

✅ **智能功能**
- 自动类型推断（数字、布尔、字符串）
- 支持嵌套路径（如：`server.port`）
- 同时修改value和_comment
- 完善的错误日志记录

✅ **易于使用**
- 命令行工具，简单易用
- 打包成单个exe文件
- 无需安装Python环境

## 快速开始

### 1. 使用预编译的exe文件

```batch
REM 修改配置
JsonEditTool.exe update config.json server.port --value 8080 --comment "服务器端口"

REM 添加配置
JsonEditTool.exe add config.json cache.enabled --value true --comment "启用缓存"

REM 删除配置
JsonEditTool.exe delete config.json old.setting
```

### 2. 从源码运行

```batch
REM 安装依赖（仅打包时需要）
pip install -r requirements.txt

REM 运行工具
python src\main.py update config.json server.port --value 8080
```

### 3. 打包成exe

```batch
REM 执行打包脚本
build.bat

REM 生成的exe位于 dist\JsonEditTool.exe
```

## 使用说明

### 命令格式

```
JsonEditTool.exe <操作类型> <JSON文件路径> <key> [选项]
```

### 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| 操作类型 | update/add/delete | 是 |
| JSON文件路径 | 配置文件路径 | 是 |
| key | 配置项键名（支持点分路径） | 是 |
| --value | 配置项的值 | update/add时必需 |
| --comment | 配置项的注释 | 否 |
| --encoding | 文件编码（默认utf-8） | 否 |
| --indent | JSON缩进（默认4） | 否 |
| --backup | 修改前创建备份 | 否 |

### 操作示例

#### 1. 修改配置项

```batch
REM 基本用法
JsonEditTool.exe update config.json server.port --value 8080

REM 带注释
JsonEditTool.exe update config.json server.host --value "0.0.0.0" --comment "监听所有网卡"

REM 绝对路径
JsonEditTool.exe update "D:\App\config.json" database.host --value "192.168.1.100"

REM 网络路径
JsonEditTool.exe update "\\server\share\prod.json" api.key --value "abc123"
```

#### 2. 添加配置项

```batch
REM 添加简单配置
JsonEditTool.exe add config.json cache.ttl --value 3600 --comment "缓存过期时间"

REM 添加嵌套配置
JsonEditTool.exe add config.json database.pool.maxSize --value 100 --comment "最大连接数"
```

#### 3. 删除配置项

```batch
REM 删除配置
JsonEditTool.exe delete config.json temp.data

REM 删除嵌套配置
JsonEditTool.exe delete config.json server.debug.enabled
```

### BAT脚本示例

#### 单文件修改

```batch
@echo off
set TOOL=D:\Tools\JsonEditTool.exe
set CONFIG=D:\App\config.json

%TOOL% update "%CONFIG%" server.port --value 8080
if %ERRORLEVEL% EQU 0 (
    echo 配置修改成功
) else (
    echo 配置修改失败
    exit /b 1
)
```

#### 批量修改多个文件

```batch
@echo off
set TOOL=JsonEditTool.exe

REM 修改Web应用配置
%TOOL% update "D:\WebApp\config.json" server.port --value 8080
echo [1/3] Web应用配置完成

REM 修改API服务配置
%TOOL% update "E:\API\settings.json" api.timeout --value 30
echo [2/3] API服务配置完成

REM 修改数据库配置
%TOOL% update "C:\DB\config.json" db.maxConn --value 100
echo [3/3] 数据库配置完成

echo 所有配置更新完成！
pause
```

## JSON配置文件格式

工具支持标准的JSON配置格式：

```json
{
  "server": {
    "port": {
      "key": "port",
      "value": 8080,
      "_comment": "服务器监听端口"
    },
    "host": {
      "key": "host",
      "value": "localhost",
      "_comment": "服务器地址"
    }
  }
}
```

使用点分路径访问：`server.port` 会定位到 `{"key": "port", "value": 8080, "_comment": "..."}`

## 错误代码

| 代码 | 说明 |
|------|------|
| 0 | 操作成功 |
| 1 | 文件不存在 |
| 2 | JSON格式错误 |
| 3 | 编码错误 |
| 4 | Key不存在 |
| 5 | 参数验证失败 |
| 6 | 权限不足 |
| 7 | 添加已存在的key |
| 8 | 无效路径 |
| 9 | 盘符不存在 |
| 10 | 网络路径不可达 |

## 日志

工具会在运行目录下的`logs`文件夹中生成日志文件：

```
logs/
  └── json_edit_tool_20260128.log
```

日志包含所有操作记录、错误信息和堆栈跟踪。

## 测试

运行单元测试：

```batch
REM 安装测试依赖
pip install pytest pytest-cov

REM 运行测试
pytest tests/

REM 查看覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 项目结构

```
JsonEditTool/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主程序入口
│   ├── json_editor.py       # JSON编辑核心
│   ├── logger.py            # 日志模块
│   └── validator.py         # 验证模块
├── tests/
│   ├── sample_config.json   # 示例配置
│   └── test_json_editor.py  # 单元测试
├── logs/                    # 日志目录
├── requirements.txt         # 依赖清单
├── build.bat               # 打包脚本
└── README.md               # 使用说明
```

## 技术栈

- Python 3.8+
- 标准库：json, logging, argparse, pathlib
- 打包工具：PyInstaller

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-01-28)
- ✨ 初始版本发布
- ✅ 支持增删改操作
- ✅ 支持多种路径类型
- ✅ 完整的日志记录
- ✅ 打包成独立exe

## 联系方式

如有问题或建议，请查看日志文件或联系开发团队。
