import pytest
import requests

from page import BASE_URL, get_headers_with_token

class Test_My_Page:
    def setup_method(self):
        print("开始测试")
        # 使用全局方法获取包含最新token的请求头
        self.headers_data = get_headers_with_token()
    # 获取用户信息
    def test_my_userinfo(self):
        url = f"{BASE_URL}/user/v2/getInfo"
        test_data = {
        }
        responses = requests.get(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'Test_My_Page.py'])
