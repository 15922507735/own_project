import requests
import pytest
from page import get_headers_with_token, BASE_URL

# 定义签到测试类
class Test_CheckIn:

    def setup_method(self):
        print("开始测试")
        """测试前准备：获取最新的 token"""
        self.headers_data = get_headers_with_token()

    # 签到测试
    def test_check_in(self):
        url = f"{BASE_URL}/user/getCheckInStatusListV2"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        
        # 检查响应消息，处理已签到的情况
        msg = data.get("msg")
        if msg == "操作成功":
            print("✅ 签到成功")
            assert True
        elif msg == "今天您已签到":
            print("✅ 今天已经签到过，接口正常")
            assert True
        else:
            print(f"❌ 签到失败: {msg}")
            assert False, f"签到接口返回错误: {msg}"

        print("接口正常")

if __name__ == '__main__':
    pytest.main(['-s', 'test_getCheckIn.py'])