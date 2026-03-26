"""
全局配置文件
包含数据库配置、API配置等全局设置
"""

# 数据库配置
DB_CONFIG = {
    "host": "qiyuan-test.mysql.polardb.rds.aliyuncs.com",
    "port": 3306,
    "user": "qiyuan_test",
    "password": "Cqca20230918!!!",
    "database": "qiyuan",
    "charset": "utf8mb4"
}

# API基础URL
BASE_URL = "https://qa-int.qiyuan.changan.com.cn"

# 默认手机号
DEFAULT_PHONE = "15922507735"

# 默认请求头模板
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "skipSign": "hyzh123456"
}

# Token缓存（避免频繁查询数据库）
_token_cache = {}


def get_token_cache_key(phone=None):
    """获取token缓存键"""
    return phone or DEFAULT_PHONE


def set_cached_token(phone, token):
    """设置token缓存"""
    cache_key = get_token_cache_key(phone)
    _token_cache[cache_key] = token


def get_cached_token(phone=None):
    """获取缓存的token"""
    cache_key = get_token_cache_key(phone)
    return _token_cache.get(cache_key)


def clear_token_cache(phone=None):
    """清除token缓存"""
    cache_key = get_token_cache_key(phone)
    if cache_key in _token_cache:
        del _token_cache[cache_key]