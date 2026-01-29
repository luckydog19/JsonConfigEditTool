"""
参数验证模块
提供路径验证、参数验证、类型推断等功能
"""

import os
import re
from pathlib import Path
from typing import Any, Tuple


class Validator:
    """参数验证器类"""
    
    # 有效的操作类型
    VALID_OPERATIONS = ['update', 'add', 'delete']
    
    # Windows非法文件名字符
    INVALID_PATH_CHARS = ['<', '>', ':', '"', '|', '?', '*']
    
    @staticmethod
    def validate_operation(operation: str) -> Tuple[bool, str]:
        """
        验证操作类型
        
        Args:
            operation: 操作类型字符串
            
        Returns:
            (是否有效, 错误信息)
        """
        if not operation:
            return False, "操作类型不能为空"
        
        operation = operation.lower()
        if operation not in Validator.VALID_OPERATIONS:
            return False, f"无效的操作类型: {operation}。有效操作: {', '.join(Validator.VALID_OPERATIONS)}"
        
        return True, ""
    
    @staticmethod
    def validate_file_path(file_path: str, must_exist: bool = False) -> Tuple[bool, str]:
        """
        验证文件路径
        
        Args:
            file_path: 文件路径
            must_exist: 是否必须存在
            
        Returns:
            (是否有效, 错误信息)
        """
        if not file_path:
            return False, "文件路径不能为空"
        
        # 检查路径长度（Windows限制）
        if len(file_path) > 260:
            return False, f"文件路径过长（超过260字符）: {len(file_path)}"
        
        # 展开环境变量
        expanded_path = os.path.expandvars(file_path)
        expanded_path = os.path.expanduser(expanded_path)
        
        # 检查是否为JSON文件
        if not expanded_path.lower().endswith('.json'):
            return False, f"文件必须是.json格式: {file_path}"
        
        # 规范化路径
        try:
            normalized_path = os.path.normpath(expanded_path)
        except Exception as e:
            return False, f"路径格式错误: {str(e)}"
        
        # 检查路径遍历攻击
        if '..' in normalized_path:
            # 获取绝对路径后再检查
            abs_path = os.path.abspath(normalized_path)
            # 这里可以添加白名单检查（可选）
            # 暂时允许，但记录警告
            pass
        
        # 如果路径必须存在
        if must_exist:
            if not os.path.exists(normalized_path):
                return False, f"文件不存在: {normalized_path}"
            
            if not os.path.isfile(normalized_path):
                return False, f"路径不是文件: {normalized_path}"
            
            # 检查文件是否可读写
            if not os.access(normalized_path, os.R_OK):
                return False, f"文件不可读: {normalized_path}"
            
            if not os.access(normalized_path, os.W_OK):
                return False, f"文件不可写: {normalized_path}"
        else:
            # 检查父目录是否存在
            parent_dir = os.path.dirname(normalized_path)
            if parent_dir and not os.path.exists(parent_dir):
                return False, f"父目录不存在: {parent_dir}"
        
        # 检查盘符是否存在（仅Windows）
        if os.name == 'nt':
            drive = os.path.splitdrive(normalized_path)[0]
            if drive and not os.path.exists(drive + os.sep):
                return False, f"盘符不存在: {drive}"
        
        return True, ""
    
    @staticmethod
    def normalize_path(file_path: str) -> str:
        """
        规范化文件路径
        
        Args:
            file_path: 原始文件路径
            
        Returns:
            规范化后的绝对路径
        """
        # 展开环境变量
        expanded_path = os.path.expandvars(file_path)
        expanded_path = os.path.expanduser(expanded_path)
        
        # 转换为绝对路径
        abs_path = os.path.abspath(expanded_path)
        
        # 规范化路径分隔符
        normalized_path = os.path.normpath(abs_path)
        
        return normalized_path
    
    @staticmethod
    def validate_key(key: str) -> Tuple[bool, str]:
        """
        验证配置项key
        支持多种分隔符格式：
        - 点分路径（对象格式）: server.port
        - 斜杠路径（数组格式）: Judge/ProcessHandleDeviceAutoContrbands
        
        Args:
            key: 配置项键名
            
        Returns:
            (是否有效, 错误信息)
        """
        if not key:
            return False, "配置项key不能为空"
        
        # 检查长度限制
        if len(key) > 255:
            return False, f"配置项key过长（超过255字符）: {len(key)}"
        
        # 支持的字符：字母、数字、点号、斜杠、下划线、连字符、冒号、中文字符
        # 允许更广泛的字符以支持各种命名约定
        # 只排除明显的控制字符和特殊符号
        invalid_chars = ['\0', '\n', '\r', '\t', '<', '>', '|', '?', '*', '"']
        for char in invalid_chars:
            if char in key:
                return False, f"配置项key包含非法字符: {repr(char)}"
        
        # 不能以点号或斜杠开头或结尾（除非是绝对路径）
        if key.startswith('.') or key.endswith('.'):
            return False, f"配置项key不能以点号开头或结尾: {key}"
        
        if key.endswith('/'):
            return False, f"配置项key不能以斜杠结尾: {key}"
        
        # 不能有连续的点号或斜杠
        if '..' in key or '//' in key:
            return False, f"配置项key不能包含连续的分隔符: {key}"
        
        return True, ""
    
    @staticmethod
    def validate_value(value: Any) -> Tuple[bool, str]:
        """
        验证配置值（基本验证）
        
        Args:
            value: 配置值
            
        Returns:
            (是否有效, 错误信息)
        """
        # 值可以为None
        if value is None:
            return True, ""
        
        # 检查类型是否为JSON支持的类型
        valid_types = (str, int, float, bool, list, dict, type(None))
        if not isinstance(value, valid_types):
            return False, f"值类型不支持: {type(value).__name__}"
        
        return True, ""
    
    @staticmethod
    def infer_value_type(value_str: str) -> Any:
        """
        从字符串推断值类型
        
        Args:
            value_str: 字符串值
            
        Returns:
            推断后的Python对象
        """
        if not isinstance(value_str, str):
            return value_str
        
        # 去除首尾空格
        value_str = value_str.strip()
        
        # null/None
        if value_str.lower() in ['null', 'none']:
            return None
        
        # 布尔值
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        # 整数
        try:
            if '.' not in value_str and 'e' not in value_str.lower():
                return int(value_str)
        except ValueError:
            pass
        
        # 浮点数
        try:
            return float(value_str)
        except ValueError:
            pass
        
        # 默认为字符串
        return value_str
    
    @staticmethod
    def validate_encoding(encoding: str) -> Tuple[bool, str]:
        """
        验证编码格式
        
        Args:
            encoding: 编码名称
            
        Returns:
            (是否有效, 错误信息)
        """
        import codecs
        
        try:
            codecs.lookup(encoding)
            return True, ""
        except LookupError:
            return False, f"不支持的编码格式: {encoding}"
