import requests
import pytest
from page import get_headers_with_token, BASE_URL

class Test_charging_station:
    def setup_method(self):

        print("开始测试")
        """测试前准备：获取最新的 token"""
        self.headers_data = get_headers_with_token()

    # 用户充电桩信息
    def test_charging_station(self):
        url = f"{BASE_URL}/api/chargingStation/info"
        test_data = {
        }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"


    # 充电桩订单列表
    # def test_charging_station_order(self):
    #     url = f"{BASE_URL}/api/chargingStation/order/list"
    #     test_data = {
    #         "currentPageNo": 0,
    #         "stubId": "string",
    #         "totalCount": 0,
    #         "userType": 0
    #     }
    #     responses = requests.post(url=url, headers=self.headers_data, json=test_data)
    #     data = responses.json()
    #     print(data)
    #     assert data.get("msg") == "操作成功"
