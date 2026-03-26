"""
Page软件包
包含页面操作、数据库工具、全局配置等模块
"""

from .global_config import *
from .database_utils import *

__all__ = [
    # 全局配置
    'DB_CONFIG',
    'BASE_URL', 
    'DEFAULT_PHONE',
    'DEFAULT_HEADERS',
    'get_token_cache_key',
    'set_cached_token',
    'get_cached_token',
    'clear_token_cache',
    
    # 数据库工具
    'DatabaseUtils',
    'db_utils',
    'get_latest_token',
    'get_headers_with_token',
    'clear_token_cache'
]