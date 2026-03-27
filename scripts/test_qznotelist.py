import requests
import pytest
from page import get_headers_with_token, BASE_URL

class Test_QzNotelist:
    def setup_method(self):

        print("开始测试")
        """测试前准备：获取最新的 token"""
        self.headers_data = get_headers_with_token()

    # 我创建的圈子列表
    def test_myqznotelist(self):
        url = f"{BASE_URL}/qzNotes/myQzNotesList"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'test_qznotelist.py'])


