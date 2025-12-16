import os
import logging
import threading
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pathlib import Path

from constants import base_dir


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogOutput(Enum):
    """日志输出类型枚举"""
    CONSOLE = "console"
    FILE = "file"
    BOTH = "both"


class Logger:
    """全局单例日志管理器"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        # 只在配置变更时使用锁，日志记录时不需要
        self._config_lock = threading.Lock()
        self._logger = logging.getLogger('TooMuchLeft')
        self._logger.setLevel(logging.DEBUG)
        
        # 默认配置
        self._log_level = LogLevel.INFO
        self._log_output = LogOutput.CONSOLE
        self._log_dir = os.path.join(base_dir, 'logs')
        self._current_log_file = None
        self._current_date = None
        
        # 确保日志目录存在
        Path(self._log_dir).mkdir(parents=True, exist_ok=True)
        
        # 初始化日志配置
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志器"""
        # 清除现有的处理器
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
        
        # 创建格式器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 根据输出类型添加处理器
        if self._log_output in [LogOutput.CONSOLE, LogOutput.BOTH]:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self._log_level.value)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
        
        if self._log_output in [LogOutput.FILE, LogOutput.BOTH]:
            self._setup_file_handler(formatter)
    
    def _setup_file_handler(self, formatter):
        """设置文件处理器"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 如果日期变化，创建新的日志文件
        if self._current_date != today:
            self._current_date = today
            self._current_log_file = os.path.join(self._log_dir, f"TooMuchLeft_{today}.log")
        
        file_handler = logging.FileHandler(self._current_log_file, encoding='utf-8')
        file_handler.setLevel(self._log_level.value)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
    
    def set_level(self, level: Union[LogLevel, str]):
        """设置日志级别"""
        with self._config_lock:
            if isinstance(level, str):
                level = LogLevel[level.upper()]
            self._log_level = level
            self._logger.setLevel(level.value)
            
            # 更新所有处理器的级别
            for handler in self._logger.handlers:
                handler.setLevel(level.value)
    
    def set_output(self, output: Union[LogOutput, str]):
        """设置日志输出类型"""
        with self._config_lock:
            if isinstance(output, str):
                output = LogOutput[output.upper()]
            self._log_output = output
            self._setup_logger()
    
    def set_log_dir(self, log_dir: str):
        """设置日志目录"""
        with self._config_lock:
            self._log_dir = log_dir
            Path(self._log_dir).mkdir(parents=True, exist_ok=True)
            self._setup_logger()
    
    def debug(self, message: str):
        """记录调试信息"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """记录一般信息"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告信息"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """记录错误信息"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误信息"""
        self._logger.critical(message)
    
    def exception(self, message: str):
        """记录异常信息（包含堆栈跟踪）"""
        self._logger.exception(message)
    
    def get_current_log_file(self) -> Optional[str]:
        """获取当前日志文件路径"""
        return self._current_log_file
    
    def get_log_level(self) -> LogLevel:
        """获取当前日志级别"""
        return self._log_level
    
    def get_log_output(self) -> LogOutput:
        """获取当前日志输出类型"""
        return self._log_output


# 创建全局日志实例
logger = Logger()