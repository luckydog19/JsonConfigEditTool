# 额外字段功能使用指南

## 概述

从v1.1版本开始，JsonEditTool支持在使用`add`操作时添加**任意额外字段**，不再局限于固定的`key`、`value`、`_comment`三个字段。

## 功能特性

✅ 支持添加任意数量的额外字段  
✅ 支持多种数据类型（字符串、数字、布尔值、数组、对象）  
✅ 自动进行类型推断  
✅ 同时支持数组格式和对象格式的JSON  

---

## 基本用法

### 语法格式

```bash
JsonEditTool.exe add <文件路径> <键名> --value <值> [--comment <注释>] [--extra <字段名>=<字段值>] ...
```

### 参数说明

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|---------|------|
| `--value` | 配置项的值 | ✅ 必需 | `--value "test"` |
| `--comment` | 配置项的注释 | ❌ 可选 | `--comment "说明"` |
| `--extra` | 额外字段（可多次使用） | ❌ 可选 | `--extra type=string` |

---

## 使用示例

### 示例1：添加单个额外字段

```bash
JsonEditTool.exe add config.json api.timeout ^
    --value 30 ^
    --comment "API超时时间" ^
    --extra unit=seconds
```

**生成的JSON（对象格式）：**
```json
{
    "api": {
        "timeout": {
            "key": "timeout",
            "value": 30,
            "_comment": "API超时时间",
            "unit": "seconds"
        }
    }
}
```

---

### 示例2：添加多个额外字段

```bash
JsonEditTool.exe add config.json db.pool ^
    --value 10 ^
    --comment "数据库连接池" ^
    --extra min=5 ^
    --extra max=20 ^
    --extra type=mysql ^
    --extra version=8.0
```

**生成的JSON（对象格式）：**
```json
{
    "db": {
        "pool": {
            "key": "pool",
            "value": 10,
            "_comment": "数据库连接池",
            "min": 5,
            "max": 20,
            "type": "mysql",
            "version": 8.0
        }
    }
}
```

---

### 示例3：数组格式添加额外字段

```bash
JsonEditTool.exe add config.json Feature/NewModule ^
    --value true ^
    --comment "新模块功能开关" ^
    --extra module=feature ^
    --extra priority=high ^
    --extra since=1.5.0
```

**生成的JSON（数组格式）：**
```json
[
    {
        "key": "Feature/NewModule",
        "value": true,
        "_comment": "新模块功能开关",
        "module": "feature",
        "priority": "high",
        "since": "1.5.0"
    }
]
```

---

### 示例4：布尔值和数字类型

```bash
JsonEditTool.exe add config.json cache.config ^
    --value redis ^
    --comment "缓存配置" ^
    --extra enabled=true ^
    --extra ttl=3600 ^
    --extra priority=1 ^
    --extra distributed=false
```

**类型推断规则：**
- `true`/`false` → 布尔值
- `123`、`3.14` → 数字
- 其他 → 字符串

---

## 实际应用场景

### 场景1：配置项元数据管理

为每个配置项添加类型、范围、版本等元数据：

```bash
JsonEditTool.exe add app.json server.port ^
    --value 8080 ^
    --comment "服务器端口" ^
    --extra type=int ^
    --extra min=1024 ^
    --extra max=65535 ^
    --extra required=true ^
    --extra env=production
```

### 场景2：功能开关配置

添加功能开关并记录启用时间和版本：

```bash
JsonEditTool.exe add features.json payment.alipay ^
    --value true ^
    --comment "支付宝支付开关" ^
    --extra feature_name=alipay_payment ^
    --extra enabled_since=2026-01-01 ^
    --extra version=2.0 ^
    --extra experimental=false
```

### 场景3：API配置管理

添加API配置并记录超时、重试等信息：

```bash
JsonEditTool.exe add api.json external.weather ^
    --value "https://api.weather.com" ^
    --comment "天气API地址" ^
    --extra timeout=10 ^
    --extra retry=3 ^
    --extra cache=true ^
    --extra auth=required
```

### 场景4：数据库连接配置

添加数据库配置并记录连接池信息：

```bash
JsonEditTool.exe add db.json master.host ^
    --value "192.168.1.100" ^
    --comment "主库地址" ^
    --extra port=3306 ^
    --extra pool_min=10 ^
    --extra pool_max=100 ^
    --extra charset=utf8mb4 ^
    --extra ssl=true
```

---

## 批处理脚本示例

### 完整配置初始化脚本

```batch
@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

SET TOOL=JsonEditTool.exe
SET CONFIG=config.json

REM 添加服务器配置
%TOOL% add %CONFIG% server.host --value "0.0.0.0" ^
    --comment "监听地址" ^
    --extra type=string --extra required=true

%TOOL% add %CONFIG% server.port --value 8080 ^
    --comment "监听端口" ^
    --extra type=int --extra min=1024 --extra max=65535

REM 添加数据库配置
%TOOL% add %CONFIG% db.host --value "localhost" ^
    --comment "数据库地址" ^
    --extra type=string --extra env=production

%TOOL% add %CONFIG% db.pool --value 20 ^
    --comment "连接池大小" ^
    --extra min=5 --extra max=100 --extra type=int

REM 添加功能开关
%TOOL% add %CONFIG% features.cache --value true ^
    --comment "缓存功能" ^
    --extra module=cache --extra since=1.0 --extra stable=true

echo 配置初始化完成！
pause
```

---

## 注意事项

### 1. 字段名命名规范

- ✅ 推荐：使用小写字母和下划线：`cache_size`、`max_retry`
- ✅ 推荐：使用驼峰命名：`cacheSize`、`maxRetry`
- ❌ 避免：使用空格或特殊字符

### 2. 值的格式

- 字符串：直接输入，如 `--extra name=test`
- 数字：直接输入，如 `--extra count=100`
- 布尔值：使用 `true` 或 `false`，如 `--extra enabled=true`
- 包含空格的字符串：需要引号，如 `--extra desc="this is a test"`

### 3. 类型推断

工具会自动进行类型推断：
- `"123"` → `123` (整数)
- `"3.14"` → `3.14` (浮点数)
- `"true"` → `true` (布尔值)
- `"false"` → `false` (布尔值)
- 其他 → 字符串

如果需要强制保持字符串类型，暂不支持（未来版本可能添加）。

### 4. 字段顺序

额外字段会按照命令行参数的顺序添加到JSON中（在`key`、`value`、`_comment`之后）。

---

## 错误处理

### 格式错误

```bash
REM ❌ 错误：缺少等号
--extra type string

REM ✅ 正确
--extra type=string
```

### 参数验证

如果`--extra`格式错误，工具会返回错误：

```
错误: --extra参数格式错误，应为 field_name=field_value: type string
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.1 | 2026-01-29 | 添加`--extra`参数支持任意额外字段 |
| v1.0 | 2026-01-28 | 初始版本，仅支持`key`、`value`、`_comment` |

---

## 常见问题

### Q1：可以添加多少个额外字段？

**A：** 没有数量限制，可以根据需要添加任意数量的额外字段。

### Q2：额外字段支持嵌套对象吗？

**A：** 当前版本不支持。额外字段的值只能是简单类型（字符串、数字、布尔值）。嵌套对象支持计划在未来版本中添加。

### Q3：update操作支持修改额外字段吗？

**A：** 当前版本的`update`操作只能修改`value`和`_comment`。如需修改额外字段，需要先删除再重新添加（计划在未来版本改进）。

### Q4：如何删除额外字段？

**A：** 当前版本不支持单独删除额外字段。如需删除，请先删除整个配置项，然后重新添加不包含该字段的配置。

---

## 总结

通过`--extra`参数，您可以灵活地为配置项添加各种元数据和扩展信息，使配置文件更加结构化和易于管理。这在大型项目的配置管理中非常有用。

如有问题或建议，请参考项目文档或联系开发团队。
