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
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

    # 我的历程
    def test_process(self):
        url = f"{BASE_URL}/api/usersProcessRecord/findList"
        test_data = {
            "pageNo": 0,
            "pageParams": {},
            "pageSize": 0
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

    # 我的-任务列表
    def test_taskcenter(self):
        url = f"{BASE_URL}/api/taskcenter/center/tasks"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

    # 我的积分
    def test_crmpoint(self):
        url = f"{BASE_URL}/my/crmPoint"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

    # 成长中心
    def test_growthcenter(self):
        url = f"{BASE_URL}/my/growUpCentre"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'Test_My_Page.py'])
