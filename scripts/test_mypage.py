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
        responses = requests.get(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':