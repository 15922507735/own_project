import requests
import pytest
from page import get_headers_with_token, BASE_URL

class Test_QzNotesSpecialDetails:
    def setup_method(self):

        print("开始测试")
        """测试前准备：获取最新的 token"""
        self.headers_data = get_headers_with_token()

# 圈子-帖子专题详情
    def test_qzNotesSpecialDetails(self):
        url = f"{BASE_URL}/qzNotes/qzNotesSpecialDetails"

        test_data = {
            "ids": "203"
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'test_qzNotesSpecialDetails.py'])

