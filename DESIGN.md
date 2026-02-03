# JsonEditTool 设计文档

**版本**: v1.1.0  
**更新日期**: 2026-01-29

## 项目概述

JsonEditTool 是一个命令行工具，用于快速修改 JSON 配置文件，特别适合批处理脚本和自动化部署场景。

### 设计目标

- **简单易用** - 命令行操作直观，学习成本低
- **功能完整** - 支持增删改操作，满足常见需求
- **灵活扩展** - 支持自定义字段，适应不同场景
- **健壮可靠** - 完善的错误处理和日志记录
- **高性能** - 单文件EXE，快速启动

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────┐
│         命令行接口 (main.py)             │
│  - 参数解析                              │
│  - 参数验证                              │
│  - 操作调度                              │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    ├─ Validator      │  参数验证
    ├─ JSONEditor     │  JSON操作
    └─ Logger         │  日志记录
             │
    ┌────────┴────────┐
    │   JSON 文件      │
    │ - 数组格式       │
    │ - 对象格式       │
    └─────────────────┘
```

### 核心模块

1. **main.py** - 主程序入口，参数解析和流程控制
2. **json_editor.py** - JSON文件读写和操作
3. **validator.py** - 参数验证和类型推断
4. **logger.py** - 日志记录（支持静默模式）

## JSON格式支持

### 对象格式

```json
{
    "server": {
        "port": {
            "key": "port",
            "value": 8080,
            "_comment": "服务器端口",
            "type": "int",
            "min": 1024,
            "max": 65535
        }
    }
}
```

**键名规则**: 点分路径，如 `server.port`

### 数组格式

```json
[
    {
        "key": "Judge/ProcessHandle",
        "value": true,
        "_comment": "处理开关",
        "module": "judge",
        "priority": "high"
    }
]
```

**键名规则**: 斜杠分隔，如 `Judge/ProcessHandle`

## 扩展字段机制（v1.1）

### 设计目标

允许用户为配置项添加任意自定义字段，扩展配置元数据。

### 实现方式

```bash
# 命令行参数
--extra field_name=field_value

# 可多次使用
--extra type=int --extra min=0 --extra max=100
```

### 使用示例

```bash
JsonEditTool.exe add config.json api.timeout --value 30 ^
    --comment "API超时" ^
    --extra type=int ^
    --extra unit=seconds ^
    --extra required=true
```

**生成的JSON**:
```json
{
    "api": {
        "timeout": {
            "key": "timeout",
            "value": 30,
            "_comment": "API超时",
            "type": "int",
            "unit": "seconds",
            "required": true
        }
    }
}
```

## 命令行接口

### 命令格式

```bash
JsonEditTool.exe <operation> <file> <key> [options]
```

### 操作类型

- `update` - 修改现有配置项
- `add` - 添加新配置项
- `delete` - 删除配置项

### 关键参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--value` | 配置项的值 | `--value 8080` |
| `--comment` | 配置项的注释 | `--comment "端口号"` |
| `--extra` | 额外字段（v1.1） | `--extra type=int` |
| `--encoding` | 文件编码 | `--encoding utf-8` |
| `--indent` | JSON缩进 | `--indent 4` |
| `--backup` | 创建备份 | `--backup` |
| `--silent` | 静默模式（默认） | `--silent` |
| `--verbose` | 详细模式 | `--verbose` |

### 返回码

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 文件不存在 |
| 2 | JSON格式错误 |
| 3 | 编码错误 |
| 4 | 键不存在 |
| 5 | 参数无效 |
| 6 | 权限不足 |
| 7 | 键已存在 |
| 99 | 未知错误 |

## 错误处理

### 分层处理

1. 底层模块抛出异常
2. 中间层捕获并转换
3. 顶层统一处理和记录

### 友好提示

- 清晰的错误信息
- 提供解决建议
- 记录详细日志

## 日志系统

### 日志级别

- **INFO** - 正常操作信息
- **WARNING** - 警告信息
- **ERROR** - 错误信息

### 日志输出

#### 文件日志
- 位置: `jsonedittoollogs/json_edit_tool_YYYYMMDD.log`
- 始终启用

#### 控制台日志
- v1.1默认禁用（静默模式）
- 使用 `--verbose` 参数启用

## 构建和部署

### 构建流程

```bash
# 使用 PyInstaller 构建单文件 EXE
python -m PyInstaller --onefile ^
    --name JsonEditTool ^
    --console ^
    --clean ^
    --hidden-import=logger ^
    --hidden-import=json_editor ^
    --hidden-import=validator ^
    --paths=src ^
    src\main.py
```

### 部署方式

1. **单文件部署** - 直接复制 EXE 到目标位置
2. **添加到 PATH** - 加入系统环境变量
3. **批处理集成** - 在脚本中调用

## 性能特性

- **快速启动** - 单文件 EXE，冷启动 < 1秒
- **低内存** - 小文件处理 ~20MB
- **高效处理** - 一次性读写，内存操作

## 安全考虑

- **路径验证** - 防止路径遍历攻击
- **权限检查** - 验证文件读写权限
- **备份机制** - 支持修改前备份
- **数据验证** - JSON格式和类型检查

## 扩展性

### 易于添加新功能

- 新增操作类型
- 新增格式支持
- 新增验证规则
- 新增输出格式

## 未来规划

### v1.2.0
- `update` 操作支持修改额外字段
- 新增 `query` 操作
- JSON Schema 验证

### v1.3.0
- 额外字段支持嵌套对象
- 批量操作
- 配置文件合并

### v2.0.0
- GUI 图形界面
- 配置项搜索
- 历史版本管理

---

**文档版本**: v1.1.0  
**最后更新**: 2026-01-29
