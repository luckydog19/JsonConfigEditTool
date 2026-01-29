# JsonEditTool 设计文档

**版本**: v1.1.0  
**更新日期**: 2026-01-29

## 📋 目录

- [项目概述](#项目概述)
- [架构设计](#架构设计)
- [核心模块](#核心模块)
- [命令行接口](#命令行接口)
- [JSON格式支持](#json格式支持)
- [扩展字段机制](#扩展字段机制)
- [错误处理](#错误处理)
- [日志系统](#日志系统)
- [构建和部署](#构建和部署)

---

## 项目概述

### 项目目标

JsonEditTool 是一个命令行工具，用于快速修改 JSON 配置文件，特别适合：
- 批处理脚本自动化配置更新
- 部署流程中的配置文件修改
- CI/CD 流程中的配置管理
- 多环境配置文件维护

### 设计原则

1. **简单易用** - 命令行操作直观，学习成本低
2. **功能完整** - 支持增删改操作，满足常见需求
3. **灵活扩展** - 支持自定义字段，适应不同场景
4. **健壮可靠** - 完善的错误处理和日志记录
5. **高性能** - 单文件EXE，快速启动

---

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

### 模块依赖关系

```
main.py
  ├─ validator.py    (参数验证)
  ├─ json_editor.py  (JSON操作)
  └─ logger.py       (日志记录)
```

---

## 核心模块

### 1. main.py - 主程序

**职责：**
- 命令行参数解析
- 参数验证协调
- 操作流程控制
- 错误处理和返回码

**关键函数：**

```python
def parse_arguments():
    """解析命令行参数"""
    # 支持 --extra 参数（v1.1）
    parser.add_argument('--extra', action='append')
    
def parse_extra_fields(extra_list):
    """解析额外字段列表（v1.1新增）"""
    # 将 ["field1=value1", "field2=value2"] 
    # 转换为 {"field1": value1, "field2": value2}
    
def validate_params(args):
    """验证所有参数"""
    
def execute_operation(args, logger):
    """执行具体操作"""
```

### 2. json_editor.py - JSON编辑器

**职责：**
- JSON文件读取和保存
- 配置项的增删改操作
- 自动检测和处理两种JSON格式
- 支持额外字段（v1.1）

**关键类和方法：**

```python
class JSONEditor:
    def __init__(self, file_path, encoding, indent, create_backup):
        """初始化编辑器"""
        
    def load(self):
        """加载JSON文件，自动检测格式"""
        
    def save(self, data):
        """保存JSON文件"""
        
    def add_item(self, key, value, comment, extra_fields):
        """添加配置项（支持额外字段）"""
        
    def update_item(self, key, value, comment):
        """更新配置项"""
        
    def delete_item(self, key):
        """删除配置项"""
        
    def find_item_in_array(self, key):
        """在数组格式中查找配置项"""
        
    def find_item_in_object(self, key_path):
        """在对象格式中查找配置项"""
```

### 3. validator.py - 参数验证器

**职责：**
- 验证操作类型
- 验证文件路径（支持多种路径类型）
- 验证键名格式
- 验证编码格式
- 类型推断

**关键函数：**

```python
def validate_operation(operation):
    """验证操作类型"""
    
def validate_file_path(file_path, must_exist):
    """验证文件路径"""
    
def validate_key(key):
    """验证键名"""
    
def validate_encoding(encoding):
    """验证编码格式"""
    
def infer_value_type(value_str):
    """类型推断：字符串 → 实际类型"""
```

### 4. logger.py - 日志记录器

**职责：**
- 文件日志记录
- 控制台日志输出（可选）
- 日志格式化
- 静默模式支持（v1.1）

**关键类：**

```python
class Logger:
    def __init__(self, log_dir, log_level, silent):
        """初始化日志器
        
        Args:
            silent: 是否静默模式（v1.1新增）
        """
        
    def info(self, message):
        """记录INFO级别日志"""
        
    def error(self, message):
        """记录ERROR级别日志"""
        
    def warning(self, message):
        """记录WARNING级别日志"""
```

---

## 命令行接口

### 命令格式

```bash
JsonEditTool.exe <operation> <file> <key> [options]
```

### 操作类型

| 操作 | 说明 | 用法 |
|------|------|------|
| `update` | 修改现有配置项 | `update config.json key --value newvalue` |
| `add` | 添加新配置项 | `add config.json key --value value` |
| `delete` | 删除配置项 | `delete config.json key` |

### 参数设计

#### 位置参数

```python
operation  # 操作类型：update/add/delete
file       # JSON文件路径
key        # 配置项键名
```

#### 可选参数

```python
--value VALUE          # 配置项的值（update/add必需）
--comment COMMENT      # 配置项的注释
--extra FIELD=VALUE    # 额外字段（v1.1新增，可多次使用）
--encoding ENCODING    # 文件编码（默认utf-8）
--indent INDENT        # JSON缩进（默认4）
--backup               # 创建备份
--silent               # 静默模式（默认启用）
--verbose              # 详细模式（显示日志）
--version              # 版本信息
--help                 # 帮助信息
```

### 返回码设计

```python
ERROR_CODE = {
    'SUCCESS': 0,              # 成功
    'FILE_NOT_FOUND': 1,       # 文件不存在
    'JSON_FORMAT_ERROR': 2,    # JSON格式错误
    'ENCODING_ERROR': 3,       # 编码错误
    'KEY_NOT_FOUND': 4,        # 键不存在
    'INVALID_PARAMS': 5,       # 参数无效
    'PERMISSION_ERROR': 6,     # 权限不足
    'KEY_EXISTS': 7,           # 键已存在
    'INVALID_PATH': 8,         # 路径无效
    'DRIVE_NOT_EXIST': 9,      # 驱动器不存在
    'NETWORK_PATH_ERROR': 10,  # 网络路径错误
    'UNKNOWN_ERROR': 99        # 未知错误
}
```

---

## JSON格式支持

### 1. 对象格式（Object Format）

**结构：**
```json
{
    "parent": {
        "child": {
            "key": "child",
            "value": "value",
            "_comment": "comment",
            "custom_field": "custom_value"
        }
    }
}
```

**键名规则：**
- 使用点分路径：`parent.child`
- 支持多层嵌套：`level1.level2.level3`

**查找算法：**
```python
def find_item_in_object(self, key_path):
    keys = key_path.split('.')
    current = self.data
    
    for key in keys[:-1]:
        if key not in current:
            return None
        current = current[key]
    
    last_key = keys[-1]
    return current.get(last_key)
```

### 2. 数组格式（Array Format）

**结构：**
```json
[
    {
        "key": "Category/ItemName",
        "value": "value",
        "_comment": "comment",
        "custom_field": "custom_value"
    }
]
```

**键名规则：**
- 使用斜杠分隔：`Category/ItemName`
- 整个字符串作为key字段的值

**查找算法：**
```python
def find_item_in_array(self, key):
    for index, item in enumerate(self.data):
        if item.get('key') == key:
            return index, item
    return None, None
```

---

## 扩展字段机制

### 设计目标（v1.1新增）

允许用户为配置项添加任意自定义字段，不局限于固定的 `key`、`value`、`_comment` 三个字段。

### 实现方式

#### 1. 命令行参数

```bash
--extra field_name=field_value
```

可多次使用：
```bash
--extra type=int --extra min=0 --extra max=100
```

#### 2. 参数解析

```python
def parse_extra_fields(extra_list):
    """解析额外字段
    
    Args:
        extra_list: ["field1=value1", "field2=value2"]
        
    Returns:
        {"field1": value1, "field2": value2}
    """
    extra_fields = {}
    for item in extra_list:
        field_name, field_value = item.split('=', 1)
        # 类型推断
        parsed_value = Validator.infer_value_type(field_value)
        extra_fields[field_name] = parsed_value
    return extra_fields
```

#### 3. 添加到JSON

```python
def add_item(self, key, value, comment, extra_fields):
    # 基础字段
    new_item = {
        'key': key,
        'value': value,
        '_comment': comment
    }
    
    # 添加额外字段
    if extra_fields:
        for field_name, field_value in extra_fields.items():
            new_item[field_name] = field_value
    
    self.data.append(new_item)
```

### 使用示例

```bash
# 添加带类型元数据的配置
JsonEditTool.exe add config.json api.timeout --value 30 ^
    --extra type=int ^
    --extra unit=seconds ^
    --extra required=true

# 生成的JSON
{
    "api": {
        "timeout": {
            "key": "timeout",
            "value": 30,
            "_comment": "",
            "type": "int",
            "unit": "seconds",
            "required": true
        }
    }
}
```

---

## 错误处理

### 错误处理策略

1. **分层处理**
   - 底层模块抛出异常
   - 中间层捕获并转换
   - 顶层统一处理和记录

2. **友好提示**
   - 清晰的错误信息
   - 提供解决建议
   - 记录详细日志

3. **优雅降级**
   - 编码自动检测
   - 路径格式容错
   - 部分失败继续执行

### 错误处理示例

```python
try:
    editor.load()
except FileNotFoundError:
    logger.error(f"文件不存在: {file_path}")
    return ERROR_CODE['FILE_NOT_FOUND']
except json.JSONDecodeError as e:
    logger.error(f"JSON格式错误: {str(e)}")
    return ERROR_CODE['JSON_FORMAT_ERROR']
except UnicodeDecodeError:
    logger.error(f"编码错误: {str(e)}")
    return ERROR_CODE['ENCODING_ERROR']
except Exception as e:
    logger.exception(f"未知错误: {str(e)}")
    return ERROR_CODE['UNKNOWN_ERROR']
```

---

## 日志系统

### 日志级别

- **INFO** - 正常操作信息
- **WARNING** - 警告信息
- **ERROR** - 错误信息

### 日志输出

#### 文件日志
- 位置：`jsonedittoollogs/json_edit_tool_YYYYMMDD.log`
- 格式：`YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`
- 始终启用

#### 控制台日志
- v1.0：默认启用
- v1.1：默认禁用（静默模式）
- 使用 `--verbose` 参数启用

### 日志内容

```
2026-01-29 10:00:00 - INFO - ============================================================
2026-01-29 10:00:00 - INFO - 开始处理: update config.json server.port
2026-01-29 10:00:00 - INFO - 参数: value=8080, comment=端口号, encoding=utf-8
2026-01-29 10:00:00 - INFO - 规范化路径: config.json -> D:\App\config.json
2026-01-29 10:00:00 - INFO - 成功加载配置文件: D:\App\config.json
2026-01-29 10:00:00 - INFO - 执行修改操作: server.port
2026-01-29 10:00:00 - INFO - 值类型推断: 8080 (str) -> 8080 (int)
2026-01-29 10:00:00 - INFO - 旧值: 9000
2026-01-29 10:00:00 - INFO - 更新值: 8080
2026-01-29 10:00:00 - INFO - 保存配置文件成功: D:\App\config.json
2026-01-29 10:00:00 - INFO - 操作完成: update server.port
2026-01-29 10:00:00 - INFO - ============================================================
```

---

## 构建和部署

### 构建流程

```bash
# 1. 清理旧文件
rmdir /s /q build dist

# 2. 使用 PyInstaller 构建
python -m PyInstaller --onefile ^
    --name JsonEditTool ^
    --console ^
    --clean ^
    --noconfirm ^
    --hidden-import=logger ^
    --hidden-import=json_editor ^
    --hidden-import=validator ^
    --paths=src ^
    src\main.py

# 3. 输出到 dist\JsonEditTool.exe
```

### 部署方式

#### 1. 单文件部署
```bash
# 复制 EXE 到目标位置
copy dist\JsonEditTool.exe C:\Tools\

# 直接使用
C:\Tools\JsonEditTool.exe --help
```

#### 2. 添加到 PATH
```bash
# 将 dist 目录添加到系统 PATH
setx PATH "%PATH%;D:\Demo\JsonConfigEditTool\dist"
```

#### 3. 批处理集成
```batch
SET TOOL=D:\Tools\JsonEditTool.exe
%TOOL% update config.json key --value value
```

### 依赖管理

**运行时依赖：** 无（单文件EXE包含所有依赖）

**开发依赖：**
```
Python 3.8+
PyInstaller 5.0+
```

---

## 性能优化

### 1. 快速启动
- 单文件 EXE
- 无外部依赖
- 冷启动 < 1秒

### 2. 内存占用
- 小文件（< 1MB）：~20MB
- 大文件（> 10MB）：动态分配

### 3. 文件处理
- 一次性读取
- 内存操作
- 一次性写入

---

## 安全考虑

### 1. 路径安全
- 验证路径合法性
- 防止路径遍历
- 检查驱动器存在性

### 2. 文件操作
- 权限检查
- 备份机制
- 原子写入

### 3. 数据验证
- JSON格式验证
- 参数类型检查
- 编码验证

---

## 扩展性设计

### 1. 新增操作
```python
# 在 main.py 添加新操作
parser.add_argument('operation', choices=['update', 'add', 'delete', 'query'])

# 在 execute_operation 添加处理逻辑
elif args.operation == 'query':
    result = editor.query_item(args.key)
```

### 2. 新增格式支持
```python
# 在 json_editor.py 添加格式检测
def detect_format(self):
    if isinstance(self.data, list):
        self.format = 'array'
    elif isinstance(self.data, dict):
        self.format = 'object'
    elif self.is_yaml_format():
        self.format = 'yaml'
```

### 3. 新增验证规则
```python
# 在 validator.py 添加验证函数
@staticmethod
def validate_json_schema(data, schema):
    """JSON Schema 验证"""
```

---

## 测试策略

### 1. 单元测试
- 测试各个模块的独立功能
- 测试边界条件
- 测试异常处理

### 2. 集成测试
- 测试完整操作流程
- 测试多种JSON格式
- 测试路径类型

### 3. 批处理测试
- 测试批量操作
- 测试错误恢复
- 测试性能

---

## 未来规划

### v1.2.0
- [ ] `update` 操作支持修改额外字段
- [ ] 新增 `query` 操作，查询配置项的所有字段
- [ ] JSON Schema 验证
- [ ] 配置项导入/导出

### v1.3.0
- [ ] 额外字段支持嵌套对象和数组
- [ ] 批量操作支持
- [ ] 配置文件合并功能
- [ ] 交互式命令行模式

### v2.0.0
- [ ] GUI 图形界面
- [ ] 配置项搜索功能
- [ ] 历史版本管理
- [ ] 配置同步功能

---

**文档版本**: v1.1.0  
**最后更新**: 2026-01-29  
**维护者**: JsonEditTool Development Team
