# JsonEditTool 版本更新日志

## v1.1.0 (2026-01-29)

### 🎉 新增功能

#### 1. 额外字段支持（--extra参数）
- ✅ `add`操作现在支持添加任意额外字段
- ✅ 可通过`--extra field_name=field_value`添加自定义字段
- ✅ 支持多次使用`--extra`参数添加多个字段
- ✅ 自动类型推断（字符串、数字、布尔值）
- ✅ 同时支持数组格式和对象格式

**使用示例：**
```bash
# 添加单个额外字段
JsonEditTool.exe add config.json api.timeout --value 30 --extra unit=seconds

# 添加多个额外字段
JsonEditTool.exe add config.json db.pool --value 10 ^
    --extra min=5 ^
    --extra max=20 ^
    --extra type=mysql
```

**生成的JSON：**
```json
{
    "api": {
        "timeout": {
            "key": "timeout",
            "value": 30,
            "_comment": "",
            "unit": "seconds"
        }
    },
    "db": {
        "pool": {
            "key": "pool",
            "value": 10,
            "_comment": "",
            "min": 5,
            "max": 20,
            "type": "mysql"
        }
    }
}
```

#### 2. 默认静默模式
- ✅ 默认启用静默模式，不输出INFO日志到控制台
- ✅ 日志仍会写入`jsonedittoollogs`文件夹
- ✅ 错误信息始终输出到控制台
- ✅ 如需查看详细日志，使用`--verbose`参数

**行为变化：**
```bash
# 静默执行（默认，无控制台输出）
JsonEditTool.exe update config.json key --value value

# 详细模式（显示所有日志）
JsonEditTool.exe update config.json key --value value --verbose
```

### 🐛 Bug修复
- ✅ 修复了在使用`--help`等参数时logger未初始化导致的崩溃问题
- ✅ 修复了finally块中访问未定义变量的问题

### 📝 文档更新
- ✅ 新增 `EXTRA_FIELDS_GUIDE.md` - 额外字段功能详细指南
- ✅ 新增 `examples/add_with_extra_fields.bat` - 额外字段使用示例脚本
- ✅ 更新帮助文档，添加`--extra`参数说明和示例

---

## v1.0.0 (2026-01-28)

### 🎉 初始版本

#### 核心功能
- ✅ 支持JSON配置文件的增、删、改操作
- ✅ 支持两种JSON格式：
  - 数组格式：`[{key, value, _comment}, ...]`
  - 对象格式：`{key: {key, value, _comment}}`
- ✅ 支持点分路径（如`server.port`）
- ✅ 支持斜杠分隔的key（如`Judge/ProcessHandle`）

#### 路径支持
- ✅ 相对路径
- ✅ 绝对路径
- ✅ 网络路径（UNC路径）
- ✅ 环境变量路径

#### 数据类型
- ✅ 自动类型推断（字符串、整数、浮点数、布尔值）
- ✅ 支持中文和特殊字符
- ✅ 多种编码支持（UTF-8、GBK、GB2312等）

#### 命令行参数
- `--value` - 配置项的值
- `--comment` - 配置项的注释
- `--encoding` - 文件编码（默认utf-8）
- `--indent` - JSON缩进（默认4）
- `--backup` - 创建备份文件
- `--silent` - 静默模式（v1.1改为默认启用）

#### 错误处理
- ✅ 详细的错误代码
- ✅ 友好的错误提示
- ✅ 完整的日志记录

#### 日志功能
- ✅ 文件日志记录
- ✅ 控制台日志输出
- ✅ 日志目录：`jsonedittoollogs`

---

## 计划功能（未来版本）

### v1.2.0 (计划中)
- [ ] `update`操作支持修改额外字段
- [ ] 新增`query`操作，查询配置项的所有字段
- [ ] 支持JSON Schema验证
- [ ] 支持配置项导入/导出

### v1.3.0 (计划中)
- [ ] 额外字段支持嵌套对象和数组
- [ ] 支持批量操作
- [ ] 支持配置文件合并
- [ ] 交互式命令行模式

### v2.0.0 (远期规划)
- [ ] GUI图形界面
- [ ] 配置项搜索功能
- [ ] 配置历史版本管理
- [ ] 配置同步功能

---

## 升级指南

### 从v1.0升级到v1.1

#### ⚠️ 行为变化
1. **静默模式成为默认**：升级后，工具默认不再输出INFO日志到控制台。如果您的脚本依赖日志输出，请添加`--verbose`参数。

**v1.0行为：**
```bash
JsonEditTool.exe update config.json key --value value
# 输出：大量INFO日志
```

**v1.1行为：**
```bash
# 默认静默
JsonEditTool.exe update config.json key --value value
# 输出：无（除非出错）

# 需要日志时
JsonEditTool.exe update config.json key --value value --verbose
# 输出：大量INFO日志
```

#### ✅ 新功能使用
使用新的`--extra`参数添加额外字段：
```bash
JsonEditTool.exe add config.json newkey --value test --extra type=string
```

#### 🔄 兼容性
- ✅ 完全向后兼容v1.0的所有功能
- ✅ 现有脚本无需修改即可继续使用
- ✅ JSON文件格式保持不变

---

## 贡献者

感谢所有为JsonEditTool做出贡献的开发者！

---

## 许可证

MIT License

---

## 联系方式

- 问题反馈：提交Issue
- 功能建议：提交Feature Request
- 文档改进：提交Pull Request
