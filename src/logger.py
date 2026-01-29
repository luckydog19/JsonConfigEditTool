"""
日志管理模块
提供统一的日志记录功能，支持日志轮转和多级别输出
"""

import logging
import os
from datetime import datetime


class Logger:
    """日志管理器类"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """单例模式，确保全局只有一个Logger实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_dir='jsonedittoollogs', log_level=logging.INFO, silent=False):
        """
        初始化日志管理器
        
        Args:
            log_dir: 日志文件存储目录（默认：jsonedittoollogs）
            log_level: 日志级别（默认INFO）
            silent: 静默模式，不输出到控制台（默认False）
        """
        # 避免重复初始化
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.log_dir = log_dir
        self.log_level = log_level
        self.silent = silent
        
        # 创建日志目录
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print(f"Warning: Cannot create log directory: {e}")
        
        # 设置日志文件名（按日期）
        log_filename = f"json_edit_tool_{datetime.now().strftime('%Y%m%d')}.log"
        log_filepath = os.path.join(log_dir, log_filename)
        
        # 创建logger
        self.logger = logging.getLogger('JsonEditTool')
        self.logger.setLevel(log_level)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 设置日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # 创建文件handler（使用简单的FileHandler）
            try:
                file_handler = logging.FileHandler(
                    log_filepath,
                    mode='a',
                    encoding='utf-8'
                )
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Cannot create file handler: {e}")
            
            # 如果不是静默模式，添加控制台handler
            if not silent:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
    
    def info(self, message):
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def debug(self, message):
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def exception(self, message):
        """记录异常信息（包含堆栈跟踪）"""
        self.logger.exception(message)


# 创建全局logger实例
_global_logger = None


def get_logger(log_dir='jsonedittoollogs', log_level=logging.INFO, silent=False):
    """
    获取全局logger实例
    
    Args:
        log_dir: 日志目录（默认：jsonedittoollogs）
        log_level: 日志级别
        silent: 静默模式，不输出到控制台
        
    Returns:
        Logger实例
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger(log_dir, log_level, silent)
    return _global_logger
