"""
JSONEditor模块的单元测试
"""

import os
import sys
import json
import unittest
import tempfile
import shutil

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from json_editor import JSONEditor


class TestJSONEditor(unittest.TestCase):
    """JSONEditor测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.test_dir = tempfile.mkdtemp()
        
        # 创建测试JSON文件
        self.test_file = os.path.join(self.test_dir, 'test_config.json')
        self.test_data = {
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
            },
            "database": {
                "name": {
                    "key": "name",
                    "value": "testdb",
                    "_comment": "数据库名称"
                }
            }
        }
        
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, indent=4)
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_load_file(self):
        """测试加载JSON文件"""
        editor = JSONEditor(self.test_file)
        data = editor.load()
        
        self.assertIsNotNone(data)
        self.assertIn('server', data)
        self.assertIn('database', data)
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        editor = JSONEditor('nonexistent.json')
        
        with self.assertRaises(FileNotFoundError):
            editor.load()
    
    def test_find_item(self):
        """测试查找配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        # 查找存在的项
        parent, key, item = editor.find_item('server.port')
        self.assertIsNotNone(parent)
        self.assertEqual(key, 'port')
        self.assertIsNotNone(item)
        self.assertEqual(item['value'], 8080)
        
        # 查找不存在的项
        parent, key, item = editor.find_item('server.nonexistent')
        self.assertIsNotNone(parent)
        self.assertEqual(key, 'nonexistent')
        self.assertIsNone(item)
    
    def test_update_item(self):
        """测试更新配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        # 更新值
        result = editor.update_item('server.port', 9000, '新端口')
        self.assertTrue(result)
        
        # 验证更新
        value = editor.get_value('server.port')
        self.assertEqual(value, 9000)
        
        # 保存并重新加载验证
        editor.save()
        editor2 = JSONEditor(self.test_file)
        editor2.load()
        value2 = editor2.get_value('server.port')
        self.assertEqual(value2, 9000)
    
    def test_update_nonexistent_item(self):
        """测试更新不存在的配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        with self.assertRaises(KeyError):
            editor.update_item('server.nonexistent', 'value')
    
    def test_add_item(self):
        """测试添加配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        # 添加新项
        result = editor.add_item('server.timeout', 30, '超时时间')
        self.assertTrue(result)
        
        # 验证添加
        value = editor.get_value('server.timeout')
        self.assertEqual(value, 30)
        
        # 保存并重新加载验证
        editor.save()
        editor2 = JSONEditor(self.test_file)
        editor2.load()
        value2 = editor2.get_value('server.timeout')
        self.assertEqual(value2, 30)
    
    def test_add_existing_item(self):
        """测试添加已存在的配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        with self.assertRaises(KeyError):
            editor.add_item('server.port', 9000)
    
    def test_add_nested_item(self):
        """测试添加嵌套配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        # 添加嵌套新项
        result = editor.add_item('cache.enabled', True, '启用缓存')
        self.assertTrue(result)
        
        # 验证添加
        value = editor.get_value('cache.enabled')
        self.assertEqual(value, True)
    
    def test_delete_item(self):
        """测试删除配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        # 删除项
        result = editor.delete_item('server.port')
        self.assertTrue(result)
        
        # 验证删除
        with self.assertRaises(KeyError):
            editor.get_value('server.port')
        
        # 保存并重新加载验证
        editor.save()
        editor2 = JSONEditor(self.test_file)
        editor2.load()
        with self.assertRaises(KeyError):
            editor2.get_value('server.port')
    
    def test_delete_nonexistent_item(self):
        """测试删除不存在的配置项"""
        editor = JSONEditor(self.test_file)
        editor.load()
        
        with self.assertRaises(KeyError):
            editor.delete_item('server.nonexistent')
    
    def test_save_with_backup(self):
        """测试保存时创建备份"""
        editor = JSONEditor(self.test_file, create_backup=True)
        editor.load()
        
        # 修改并保存
        editor.update_item('server.port', 9000)
        editor.save()
        
        # 检查备份文件是否存在
        backup_files = [f for f in os.listdir(self.test_dir) if f.startswith('test_config.json.bak')]
        self.assertGreater(len(backup_files), 0)


if __name__ == '__main__':
    unittest.main()
