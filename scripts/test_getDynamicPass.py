import pytest
import requests

class Test_GetDynamicPass:
    headers = {
        "Content-Type": "application/json",
        "skipSign": "hyzh123456",
        "x-gray": "1"
    }
    # 获取图形验证码
    def test_getGraphicsCode(self):
        url = "https://qa-int.qiyuan.changan.com.cn/user/getGraphics"
        test_data = {
            "channel": "",
            "graphicsKey": "",
            "imgCode": "",
            "imgCodeSign": 0,
            "isApp": 0,
            "phone": "15922507735",
            "temporaryToken": "",
            "vertifyCode": ""
        }
        responses = requests.post(url, headers=self.headers, json=test_data)
        data = responses.json()
        print(f"获取图形验证码响应结果：{data}")
        assert data.get("msg") == "操作成功"

    # 获取手机登录验证码
    # def test_getDynamicPass(self):
    #     url = "https://qa-int.qiyuan.changan.com.cn/user/getDynamicPass"
    #     test_data = {
    # "channel": "",
    # "graphicsKey": "",
    # "imgCode": "",
    # "imgCodeSign": 0,
    # "isApp": 0,
    # "phone": "15922507735",
    # "temporaryToken": "",
    # "vertifyCode": ""
    # }
    #     response = requests.post(url, headers=self.headers, json=test_data)
    #     data = response.json()
    #     print(f"获取验证码响应结果：{data}")
    #     assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'Test_GetDynamicPass.py'])
