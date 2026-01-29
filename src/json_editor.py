"""
JSON编辑器核心模块
提供JSON配置文件的读取、修改、保存功能
支持两种格式：
1. 数组格式：[{key, value, _comment}, ...]
2. 对象格式：{key: {key, value, _comment}, ...}
"""

import json
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime


class JSONEditor:
    """JSON配置文件编辑器"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8', indent: int = 4, create_backup: bool = False):
        """
        初始化JSON编辑器
        
        Args:
            file_path: JSON文件路径
            encoding: 文件编码
            indent: JSON缩进空格数
            create_backup: 是否创建备份
        """
        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self.create_backup = create_backup
        self.data = None
        self.is_array_format = False  # 标记是否为数组格式
    
    def load(self) -> Union[Dict, List]:
        """
        加载JSON文件
        
        Returns:
            JSON数据（字典或列表）
            
        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON格式错误
            UnicodeDecodeError: 编码错误
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"文件不存在: {self.file_path}")
        
        # 尝试使用指定编码读取
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as f:
                self.data = json.load(f)
            
            # 检测格式
            if isinstance(self.data, list):
                self.is_array_format = True
            
            return self.data
        except UnicodeDecodeError:
            # 尝试其他编码
            for alt_encoding in ['utf-8-sig', 'gbk', 'gb2312', 'latin-1']:
                if alt_encoding == self.encoding:
                    continue
                try:
                    with open(self.file_path, 'r', encoding=alt_encoding) as f:
                        self.data = json.load(f)
                    
                    # 检测格式
                    if isinstance(self.data, list):
                        self.is_array_format = True
                    
                    # 更新编码
                    self.encoding = alt_encoding
                    return self.data
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
            # 所有编码都失败
            raise UnicodeDecodeError(
                self.encoding, b'', 0, 1,
                f"无法使用任何已知编码读取文件: {self.file_path}"
            )
    
    def save(self, data: Optional[Union[Dict, List]] = None) -> bool:
        """
        保存JSON文件
        
        Args:
            data: 要保存的数据（如果为None则使用self.data）
            
        Returns:
            是否保存成功
            
        Raises:
            ValueError: 数据为空
            IOError: 写入失败
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有数据可保存")
        
        # 创建备份
        if self.create_backup and os.path.exists(self.file_path):
            backup_path = f"{self.file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            shutil.copy2(self.file_path, backup_path)
        
        # 保存文件
        try:
            with open(self.file_path, 'w', encoding=self.encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=self.indent)
            return True
        except Exception as e:
            raise IOError(f"保存文件失败: {str(e)}")
    
    def find_item_in_array(self, key: str) -> Tuple[Optional[int], Optional[Dict]]:
        """
        在数组格式中查找配置项
        
        Args:
            key: 配置项的key字段值（支持斜杠分隔，如 "Judge/ProcessHandleDeviceAutoContrbands"）
            
        Returns:
            (索引, 配置项) 如果未找到则返回(None, None)
        """
        if not isinstance(self.data, list):
            return None, None
        
        for index, item in enumerate(self.data):
            if isinstance(item, dict) and item.get('key') == key:
                return index, item
        
        return None, None
    
    def find_item_in_object(self, key_path: str) -> Tuple[Optional[Dict], Optional[str], Optional[Dict]]:
        """
        在对象格式中根据点分路径查找配置项
        
        Args:
            key_path: 点分路径，如 "server.port"
            
        Returns:
            (父节点, 最后一个键名, 找到的配置项) 如果未找到则返回(None, None, None)
        """
        if not isinstance(self.data, dict):
            return None, None, None
        
        keys = key_path.split('.')
        current = self.data
        parent = None
        
        # 遍历路径
        for i, key in enumerate(keys):
            if not isinstance(current, dict):
                return None, None, None
            
            # 最后一个键
            if i == len(keys) - 1:
                if key in current:
                    return current, key, current[key]
                else:
                    return current, key, None
            
            # 中间键
            if key not in current:
                return None, None, None
            
            parent = current
            current = current[key]
        
        return None, None, None
    
    def update_item(self, key: str, value: Any, comment: Optional[str] = None) -> bool:
        """
        更新配置项
        
        Args:
            key: 配置项的key（数组格式）或点分路径（对象格式）
            value: 新值
            comment: 新注释（可选）
            
        Returns:
            是否更新成功
        """
        if self.is_array_format:
            # 数组格式
            index, item = self.find_item_in_array(key)
            
            if index is None or item is None:
                raise KeyError(f"配置项不存在: {key}")
            
            # 更新值和注释
            item['value'] = value
            if comment is not None:
                item['_comment'] = comment
            
            return True
        else:
            # 对象格式
            parent, last_key, item = self.find_item_in_object(key)
            
            if parent is None or last_key is None:
                raise KeyError(f"配置项不存在: {key}")
            
            if item is None:
                raise KeyError(f"配置项不存在: {key}")
            
            # 检查是否为标准配置项结构
            if isinstance(item, dict) and 'key' in item and 'value' in item:
                # 标准结构：{key, value, _comment}
                item['value'] = value
                if comment is not None:
                    item['_comment'] = comment
            else:
                # 简单结构：直接是值
                # 转换为标准结构
                parent[last_key] = {
                    'key': last_key,
                    'value': value,
                    '_comment': comment if comment is not None else ''
                }
            
            return True
    
    def add_item(self, key: str, value: Any, comment: Optional[str] = None, extra_fields: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加配置项
        
        Args:
            key: 配置项的key（数组格式）或点分路径（对象格式）
            value: 值
            comment: 注释（可选）
            extra_fields: 额外字段（可选），例如 {"type": "string", "enabled": true}
            
        Returns:
            是否添加成功
        """
        if self.is_array_format:
            # 数组格式
            index, item = self.find_item_in_array(key)
            
            if index is not None:
                raise KeyError(f"配置项已存在: {key}")
            
            # 添加新配置项（基础字段）
            new_item = {
                'key': key,
                'value': value,
                '_comment': comment if comment is not None else ''
            }
            
            # 添加额外字段
            if extra_fields:
                for field_name, field_value in extra_fields.items():
                    new_item[field_name] = field_value
            
            self.data.append(new_item)
            
            return True
        else:
            # 对象格式
            keys = key.split('.')
            current = self.data
            
            # 遍历或创建路径
            for i, k in enumerate(keys[:-1]):
                if k not in current:
                    current[k] = {}
                elif not isinstance(current[k], dict):
                    raise ValueError(f"路径冲突: {'.'.join(keys[:i+1])} 不是对象")
                current = current[k]
            
            # 最后一个键
            last_key = keys[-1]
            if last_key in current:
                raise KeyError(f"配置项已存在: {key}")
            
            # 添加配置项（标准结构+额外字段）
            current[last_key] = {
                'key': last_key,
                'value': value,
                '_comment': comment if comment is not None else ''
            }
            
            # 添加额外字段
            if extra_fields:
                for field_name, field_value in extra_fields.items():
                    current[last_key][field_name] = field_value
            
            return True
    
    def delete_item(self, key: str) -> bool:
        """
        删除配置项
        
        Args:
            key: 配置项的key（数组格式）或点分路径（对象格式）
            
        Returns:
            是否删除成功
        """
        if self.is_array_format:
            # 数组格式
            index, item = self.find_item_in_array(key)
            
            if index is None:
                raise KeyError(f"配置项不存在: {key}")
            
            # 删除配置项
            del self.data[index]
            
            return True
        else:
            # 对象格式
            parent, last_key, item = self.find_item_in_object(key)
            
            if parent is None or last_key is None:
                raise KeyError(f"配置项不存在: {key}")
            
            if item is None:
                raise KeyError(f"配置项不存在: {key}")
            
            # 删除配置项
            del parent[last_key]
            
            return True
    
    def get_value(self, key: str) -> Any:
        """
        获取配置项的值
        
        Args:
            key: 配置项的key（数组格式）或点分路径（对象格式）
            
        Returns:
            配置项的值
        """
        if self.is_array_format:
            # 数组格式
            _, item = self.find_item_in_array(key)
            
            if item is None:
                raise KeyError(f"配置项不存在: {key}")
            
            return item.get('value')
        else:
            # 对象格式
            _, _, item = self.find_item_in_object(key)
            
            if item is None:
                raise KeyError(f"配置项不存在: {key}")
            
            # 如果是标准结构，返回value字段
            if isinstance(item, dict) and 'value' in item:
                return item['value']
            
            # 否则返回整个item
            return item
