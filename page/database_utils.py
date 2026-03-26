"""
数据库工具类
提供数据库连接、token获取等通用方法
"""

import pymysql
from typing import Optional, Dict, Any
from .global_config import DB_CONFIG, DEFAULT_PHONE, set_cached_token, get_cached_token


class DatabaseUtils:
    """数据库工具类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化数据库工具
        
        Args:
            config: 数据库配置，如果为None则使用全局配置
        """
        self.config = config or DB_CONFIG
        self.connection = None
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.connection = pymysql.connect(**self.config)
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_latest_token(self, phone: str = DEFAULT_PHONE) -> Optional[str]:
        """
        从数据库获取用户最新的 token
        
        Args:
            phone: 手机号
            
        Returns:
            token 字符串，如果未找到则返回 None
        """
        # 先检查缓存
        cached_token = get_cached_token(phone)
        if cached_token:
            print(f"使用缓存的 token: {cached_token}")
            return cached_token
        
        # 连接数据库
        if not self.connect():
            return None
        
        try:
            cursor = self.connection.cursor()
            
            # 执行 SQL 查询 - 修复多行字符串格式
            sql = """
                SELECT * FROM sc_user_login_log 
                WHERE phone = %s AND data_state = 1 
                ORDER BY login_time DESC, id DESC 
                LIMIT 1
            """
            cursor.execute(sql, (phone,))
            
            # 获取查询结果
            result = cursor.fetchall()
            
            if result:
                # 获取列名以便正确提取 token
                columns = [desc[0] for desc in cursor.description]
                row_dict = dict(zip(columns, result[0]))
                
                # 尝试从不同可能的列名获取 token
                token = None
                for col_name in ['token', 'user_token', 'auth_token', 'data3']:
                    if col_name in row_dict and row_dict[col_name]:
                        token = row_dict[col_name]
                        break
                
                # 如果还是 None，尝试按索引获取（兼容旧版本）
                if not token and len(result[0]) > 2:
                    token = result[0][2]
                
                if token:
                    print(f"从数据库获取到 token: {token}")
                    
                    # 更新缓存
                    set_cached_token(phone, token)
                    
                    return token
                else:
                    print(f"找到记录但无法提取 token，可用列：{columns}")
                    return None
            else:
                print(f"未找到手机号 {phone} 的有效 token")
                return None
                
        except Exception as e:
            print(f"数据库查询错误：{e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            self.disconnect()
    
    def get_headers_with_token(self, phone: str = DEFAULT_PHONE) -> Dict[str, str]:
        """
        获取包含最新token的请求头
        
        Args:
            phone: 手机号
            
        Returns:
            包含token的请求头字典
        """
        from .global_config import DEFAULT_HEADERS
        
        token = self.get_latest_token(phone)
        headers = DEFAULT_HEADERS.copy()
        
        if token:
            headers["token"] = token
        else:
            # 如果获取token失败，使用默认token
            headers["token"] = "user:multi:token:ffffffff-9406-27fe-9406-27fe00000000:15922507735af2a3ecc2b124873b70b16675fbe4f90"
            print("使用默认token")
        
        return headers


# 创建全局实例
db_utils = DatabaseUtils()


def get_latest_token(phone: str = DEFAULT_PHONE) -> Optional[str]:
    """全局函数：获取最新token"""
    return db_utils.get_latest_token(phone)


def get_headers_with_token(phone: str = DEFAULT_PHONE) -> Dict[str, str]:
    """全局函数：获取包含token的请求头"""
    return db_utils.get_headers_with_token(phone)


def clear_token_cache(phone: str = DEFAULT_PHONE):
    """全局函数：清除token缓存"""
    from .global_config import clear_token_cache as clear_cache
    clear_cache(phone)
    print(f"已清除手机号 {phone} 的token缓存")