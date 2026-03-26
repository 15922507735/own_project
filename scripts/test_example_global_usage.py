"""
示例：如何使用全局数据库连接和token获取方法
"""

import pytest
import requests
from page import (
    get_headers_with_token,  # 获取包含token的请求头
    get_latest_token,        # 获取最新token
    BASE_URL,                # 基础URL
    clear_token_cache,       # 清除token缓存
    db_utils                 # 数据库工具实例
)


class TestExampleGlobalUsage:
    """示例测试类：展示全局方法的使用"""
    
    def setup_method(self):
        """测试前准备"""
        print("[SETUP] 开始测试")
        # 方法1：直接获取包含token的请求头
        self.headers = get_headers_with_token()
        print(f"[SUCCESS] 获取到的请求头: {self.headers}")
    
    def test_get_token_directly(self):
        """测试直接获取token"""
        print("\n[TEST] 测试直接获取token")
        
        # 方法2：直接获取token
        token = get_latest_token()
        print(f"[SUCCESS] 直接获取的token: {token}")
        
        # 验证token格式
        assert token is not None, "token不能为空"
        assert "user:multi:token:" in token, "token格式不正确"
    
    def test_use_cached_token(self):
        """测试使用缓存的token"""
        print("\n[TEST] 测试token缓存功能")
        
        # 第一次获取token（会查询数据库）
        token1 = get_latest_token()
        print(f"[SUCCESS] 第一次获取token: {token1}")
        
        # 第二次获取token（使用缓存）
        token2 = get_latest_token()
        print(f"[SUCCESS] 第二次获取token: {token2}")
        
        # 两次获取的token应该相同
        assert token1 == token2, "缓存功能异常"
    
    def test_clear_cache_and_refresh(self):
        """测试清除缓存并重新获取token"""
        print("\n[TEST] 测试清除缓存功能")
        
        # 获取当前token
        original_token = get_latest_token()
        print(f"[SUCCESS] 原始token: {original_token}")
        
        # 清除缓存
        clear_token_cache()
        print("[SUCCESS] 缓存已清除")
        
        # 重新获取token（会重新查询数据库）
        new_token = get_latest_token()
        print(f"[SUCCESS] 重新获取的token: {new_token}")
        
        # 验证token不为空
        assert new_token is not None, "重新获取的token不能为空"
    
    def test_api_with_global_token(self):
        """测试使用全局token调用API"""
        print("\n[TEST] 测试API调用")
        
        # 使用全局方法获取请求头
        headers = get_headers_with_token()
        
        # 调用API
        url = f"{BASE_URL}/article/list"
        test_data = {
            "begRow": 0,
            "isPage": True,
            "pageNo": 0,
            "pageSize": 0,
            "queryParams": {}
        }
        
        response = requests.post(url=url, headers=headers, json=test_data)
        data = response.json()
        
        print(f"[SUCCESS] API响应: {data}")
        
        # 验证响应
        assert response.status_code == 200, "API请求失败"
        assert data.get("msg") == "操作成功", "API响应消息不正确"
    
    def test_custom_phone_number(self):
        """测试使用不同手机号获取token"""
        print("\n[TEST] 测试自定义手机号")
        
        # 使用不同的手机号
        custom_phone = "15922507735"  # 可以修改为其他手机号
        
        # 获取该手机号的token
        token = get_latest_token(custom_phone)
        print(f"[SUCCESS] 手机号 {custom_phone} 的token: {token}")
        
        # 验证token不为空
        assert token is not None, "自定义手机号的token不能为空"
    
    def test_database_utils_instance(self):
        """测试直接使用数据库工具实例"""
        print("\n[TEST] 测试数据库工具实例")
        
        # 直接使用全局数据库工具实例
        token = db_utils.get_latest_token()
        print(f"[SUCCESS] 使用db_utils获取的token: {token}")
        
        # 验证token
        assert token is not None, "使用db_utils获取的token不能为空"


class TestAdvancedUsage:
    """高级用法示例"""
    
    def test_create_custom_db_utils(self):
        """测试创建自定义数据库工具实例"""
        print("\n[TEST] 测试自定义数据库工具")
        
        from page import DatabaseUtils
        
        # 创建自定义配置的数据库工具
        custom_config = {
            "host": "qiyuan-test.mysql.polardb.rds.aliyuncs.com",
            "port": 3306,
            "user": "qiyuan_test",
            "password": "Cqca20230918!!!",
            "database": "qiyuan",
            "charset": "utf8mb4"
        }
        
        custom_db_utils = DatabaseUtils(custom_config)
        token = custom_db_utils.get_latest_token()
        
        print(f"[SUCCESS] 自定义数据库工具获取的token: {token}")
        assert token is not None, "自定义数据库工具获取的token不能为空"
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n[TEST] 测试错误处理")
        
        # 测试无效手机号
        invalid_phone = "00000000000"
        token = get_latest_token(invalid_phone)
        
        if token is None:
            print("[SUCCESS] 无效手机号正确处理：返回None")
        else:
            print(f"[WARNING] 无效手机号返回了token: {token}")


if __name__ == "__main__":
    # 运行示例测试
    pytest.main([__file__, "-v", "-s"])