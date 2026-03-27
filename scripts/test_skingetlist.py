import requests
import pytest
from page import get_headers_with_token, BASE_URL

class Test_Skingetlist:
    def setup_method(self):
        print("开始测试")
        """测试前准备：获取最新的 token"""
        self.headers_data = get_headers_with_token()

    # 获取皮肤列表
    def test_skingetlist(self):
        url = f"{BASE_URL}/skin/getList"

        test_data = {
            "deviceId": "48209A3B-7E07-4DFF-A69D-E73E585FB7C2",
            "skinId": 9,
            "userId": 9944686
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'test_skingetlist.py'])
