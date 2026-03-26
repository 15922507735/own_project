import pytest
import requests
from page import get_headers_with_token, BASE_URL

# 定义测试数据
pinglun_test_data = [
    {
        "commentId": 0,
        "imgs": "",
        "qzNotesId": 29802,
        "type": 0
    },
    {
        "commentId": 0,
        "imgs": "",
        "qzNotesId": 29802,
        "type": 0
    },
    {
        "commentId": 0,
        "imgs": "",
        "qzNotesId": 29802,
        "type": 0
    }
]

class Test_Faxian_Page:
    
    def setup_method(self):
        """测试前准备：获取最新的 token"""
        print("开始测试")
        # 使用全局方法获取包含最新 token 的请求头
        self.headers_data = get_headers_with_token()
        print(f"当前使用的 token: {self.headers_data.get('token')}")


    # 资讯列表
    def test_faxian_zixun(self):
        url = f"{BASE_URL}/article/list"
        test_data = {
                    "begRow": 0,
                    "isPage": True,
                    "pageNo": 0,
                    "pageSize": 0,
                    "queryParams": {}
                    }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 广告位置
    def test_faxian_guanggaoweizhi(self):
        url = f"{BASE_URL}/ads/list"
        test_data = {"positionId":"53"}
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 活动列表
    def test_faxian_huodong(self):
        url = f"{BASE_URL}/activity/list"
        test_data = {
                    "queryParams":
                         {
                            "provinceCode":"",
                            "cityCode":"",
                            "activityStatus":5
                          },
                    "pageNo":1,
                    "pageSize":20}
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"
    
    # 推荐列表
    def test_faxian_tuijian(self):
        url = f"{BASE_URL}/recommend/list"
        test_data = {
                    "pageNo":1,
                    "pageSize":20
                    }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 社区
    def test_faxian_shequ(self):
        url = f"{BASE_URL}/qz/v2/squareDetailPageList"
        test_data = {"queryParams":{"business":"NEWEST"},"pageNo":1,"pageSize":10}
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 专题
    def test_faxian_zhuti(self):
        url = f"{BASE_URL}/article/articleSpecials"
        test_data = {}
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 看车全部车型数据展示
    def test_faxian_keche(self):
        url = f"{BASE_URL}/qy/carorder/index_one"
        test_data = {
                    "latitude":"fuLPKgOiQa3PesFKgU/gNw==",
                    "longitude":"fuLPKgOiQa3PesFKgU/gNw==",
                    "version":4
                    }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 单车系数据展示
    def test_faxian_danchexi(self):
        url = f"{BASE_URL}/qy/carorder/only_car_index"
        test_data = {
                    "seriesCode":"C798",
                    "modelId":0,
                    "latitude":"",
                    "version":4,
                    "longitude":""
                    }
        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 圈子 - 评论帖子（参数化测试）
    @pytest.mark.parametrize("test_case", pinglun_test_data, ids=lambda x: f"type_{x['type']}")
    def test_faxian_pinglun(self, test_case):
        """参数化测试：分别测试不同类型的评论"""
        url = f"{BASE_URL}/qzNotes/commentSub"
        request_data = {
                "commentId": test_case.get("commentId"),
                "content": test_case.get("content"),
                "imgs": test_case.get("imgs"),
                "qzNotesId": test_case.get("qzNotesId"),
                "type": test_case.get("type")
                }
        responses = requests.post(url=url, headers=self.headers_data, json=request_data)
        data = responses.json()
        print(f"\n测试数据：{test_case}")
        print(f"响应结果：{data}")
        if data.get("msg") == "对不起，该内容你已经评论过啦":
            responses = requests.post(url=url, headers=self.headers_data, json=request_data)
            data = responses.json()

        assert data.get("msg") == "操作成功"


if __name__ == '__main__':
    pytest.main(['-s', 'test_faxian_zixun.py'])