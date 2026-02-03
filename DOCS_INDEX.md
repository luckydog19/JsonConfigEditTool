# 文档导航

欢迎使用 JsonEditTool！根据您的需求选择相应的文档：

## 🚀 快速导航

| 我想... | 阅读文档 | 说明 |
|---------|---------|------|
| **快速上手** | [QUICKSTART.md](QUICKSTART.md) | 5分钟快速入门教程 |
| **了解功能** | [README.md](README.md) | 完整功能说明和使用指南 |
| **使用额外字段** | [EXTRA_FIELDS_GUIDE.md](EXTRA_FIELDS_GUIDE.md) | v1.1新功能详细说明 |
| **了解架构** | [DESIGN.md](DESIGN.md) | 设计文档和技术细节 |
| **查看更新** | [CHANGELOG.md](CHANGELOG.md) | 版本历史和更新记录 |
| **项目总结** | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目迁移和整理总结 |

## 📖 文档说明

### 1. README.md - 主文档 ⭐
**适合**: 所有用户  
**内容**:
- 项目介绍和特性
- 安装和快速开始
- 完整的功能说明
- 命令行参数详解
- 批处理脚本示例
- 常见问题解答

### 2. QUICKSTART.md - 快速开始 🚀
**适合**: 新用户  
**内容**:
- 5分钟快速入门
- 基本操作演示
- 常见场景示例
- 重要注意事项

### 3. EXTRA_FIELDS_GUIDE.md - 额外字段指南 ✨
**适合**: 需要扩展配置的用户  
**内容**:
- 额外字段功能说明（v1.1新增）
- 详细使用示例
- 实际应用场景
- 批处理脚本示例

### 4. DESIGN.md - 设计文档 🏗️
**适合**: 开发者和维护者  
**内容**:
- 架构设计
- 核心模块说明
- JSON格式处理
- 扩展机制
- 性能和安全考虑

### 5. CHANGELOG.md - 变更记录 📋
**适合**: 关注版本更新的用户  
**内容**:
- 版本更新历史
- 新功能说明
- Bug修复记录
- 未来规划

### 6. PROJECT_SUMMARY.md - 项目总结 📊
**适合**: 项目维护者  
**内容**:
- 项目迁移记录
- 文档整理说明
- 目录结构
- 验证清单

## 🎯 使用场景

### 场景1：我是新用户，想快速开始使用
```
推荐阅读顺序：
1. README.md（了解基本功能）
2. QUICKSTART.md（快速上手）
3. 根据需要参考 EXTRA_FIELDS_GUIDE.md
```

### 场景2：我想在批处理中使用
```
推荐阅读：
1. QUICKSTART.md（第4部分：常见场景）
2. README.md（第6部分：批处理脚本示例）
3. examples/ 目录下的示例脚本
```

### 场景3：我想使用额外字段功能
```
推荐阅读：
1. EXTRA_FIELDS_GUIDE.md（完整指南）
2. README.md（第4部分：高级功能）
```

### 场景4：我是开发者，想了解实现细节
```
推荐阅读顺序：
1. DESIGN.md（架构和设计）
2. src/main.py（源代码）
3. CHANGELOG.md（版本历史）
```

### 场景5：我想贡献代码或报告问题
```
推荐阅读：
1. DESIGN.md（了解架构）
2. README.md（功能说明）
3. CHANGELOG.md（当前版本）
```

## 📁 其他资源

### 示例脚本
查看 `examples/` 目录：
- `add_with_extra_fields.bat` - 额外字段使用示例
- 其他批处理脚本示例

### 测试文件
查看 `tests/` 目录：
- `sample_config.json` - 对象格式示例
- `test_array_config.json` - 数组格式示例

### 源代码
查看 `src/` 目录：
- `main.py` - 主程序
- `json_editor.py` - JSON编辑器
- `validator.py` - 参数验证
- `logger.py` - 日志记录

## 💡 文档约定

- ✅ 表示功能已实现
- ❌ 表示已删除或不推荐
- ⭐ 表示重要文档
- 🚀 表示快速入门
- ✨ 表示新功能
- 📋 表示列表或记录

## 🔄 文档更新

文档随版本更新而更新。当前文档版本对应：

**工具版本**: v1.1.0  
**文档更新日期**: 2026-01-29

## 📞 获取帮助

如果文档无法解决您的问题：

1. **查看命令行帮助**
   ```bash
   JsonEditTool.exe --help
   ```

2. **查看日志文件**
   ```bash
   type jsonedittoollogs\json_edit_tool_20260129.log
   ```

3. **提交 Issue**
   - 描述问题
   - 提供日志
   - 说明使用环境

---

**祝您使用愉快！** 🎉
