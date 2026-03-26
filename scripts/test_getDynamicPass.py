import base64
import pytest
import requests
import ddddocr
import io
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import hashlib
import json

class Test_GetDynamicPass:
    headers = {
        "Content-Type": "application/json",
        "skipSign": "hyzh123456",
    }
    
    # 创建OCR客户端实例，用于识别图形验证码
    @pytest.fixture(scope="class")
    def ocr_client(self):
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr
    
    # def get_rsa_public_key(self):
    #     """获取RSA公钥"""
    #     # 尝试常见的RSA公钥接口
    #     endpoints = [
    #         "/user/getRsa",
    #         "/api/user/getRsa",
    #         "/api/common/getRsaKey",
    #         "/user/getPublicKey",
    #         "/api/password/getPublicKey",
    #         "/api/password/getRsaKey",
    #         "/password/getPublicKey",
    #         "/password/getRsaKey"
    #     ]
    #
    #     for endpoint in endpoints:
    #         try:
    #             url = f"https://qa-int.qiyuan.changan.com.cn{endpoint}"
    #             response = requests.post(url, headers=self.headers, json={"phone": "15922507735"})
    #             if response.status_code == 200:
    #                 data = response.json()
    #                 if data.get("code") == 0 and data.get("data"):
    #                     public_key = data.get("data", {}).get("publicKey") or data.get("data", {}).get("rsaKey")
    #                     if public_key:
    #                         print(f"获取到RSA公钥: {public_key[:50]}...")
    #                         return public_key
    #         except:
    #             continue
    #
    #     # 如果无法获取公钥，返回None
    #     print("无法获取RSA公钥")
    #     return None
    #
    # def encrypt_password(self, password, public_key=None):
    #     """使用RSA加密密码"""
    #     if not public_key:
    #         # 如果无法获取公钥，尝试使用简单的Base64编码（NES加密的一种简单实现）
    #         print("警告：无法获取RSA公钥，使用Base64编码作为NES加密")
    #         # 这里将"NES"理解为"Network Encoding Scheme"，使用Base64编码
    #         encoded = base64.b64encode(password.encode()).decode()
    #         print(f"密码NES加密(Base64): {password} -> {encoded}")
    #         return encoded
    #
    #     try:
    #         # 如果公钥是字符串格式，需要添加头尾
    #         if not public_key.startswith("-----BEGIN"):
    #             public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    #
    #         # 加载公钥
    #         rsa_key = RSA.import_key(public_key)
    #         cipher = PKCS1_v1_5.new(rsa_key)
    #
    #         # 加密密码
    #         encrypted = cipher.encrypt(password.encode())
    #
    #         # Base64编码
    #         encrypted_base64 = base64.b64encode(encrypted).decode()
    #         print(f"密码RSA加密成功: {password} -> {encrypted_base64[:30]}...")
    #         return encrypted_base64
    #
    #     except Exception as e:
    #         print(f"密码RSA加密失败: {e}")
    #         # 如果RSA加密失败，使用Base64编码作为备选
    #         encoded = base64.b64encode(password.encode()).decode()
    #         print(f"密码NES加密(Base64): {password} -> {encoded}")
    #         return encoded




    # 获取图形验证码 并识别验证码
    @pytest.fixture(scope="class")
    def graphics_data(self, ocr_client):
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
        print(f"\n获取图形验证码响应结果：{data}")

        graphics_value = data.get("data", {}).get("graphicsValue")
        graphics_key = data.get("data", {}).get("graphicsKey")
        assert graphics_value is not None, "获取图形验证码失败"

        img_bytes = base64.b64decode(graphics_value)
        img_code = ocr_client.classification(img_bytes)
        print(f"\nOCR识别结果: {img_code}")

        return {
            "graphicsValue": graphics_value,
            "graphicsKey": graphics_key,
            "imgCode": img_code
        }

    def test_getGraphicsCode(self, graphics_data):
        print(f"\n获取到的graphicsValue: {graphics_data['graphicsValue'][:50]}...")
        print(f"graphicsKey: {graphics_data['graphicsKey']}")
        print(f"OCR识别验证码: {graphics_data['imgCode']}")
        assert graphics_data is not None

    def test_getDynamicPass(self, graphics_data):
        graphics_value = graphics_data["graphicsValue"]

        img_data = base64.b64decode(graphics_value)
        print(f"\n验证码图片大小: {len(img_data)} 字节")

        assert graphics_value is not None

    # 获取手机短信验证码，传入上面获取的图形验证码
    def test_getDynamicPassCode(self, graphics_data):
        url = "https://qa-int.qiyuan.changan.com.cn/user/getDynamicPass"
        test_data = {
                "channel": "",
                "dynamicPassword": "",
                "graphicsKey": graphics_data.get("graphicsKey", ""),
                "imgCode": graphics_data.get("imgCode", ""),
                "imgCodeSign": 0,
                "isApp": 0,
                "phone": "15922507735",
                "temporaryToken": "",
                "vertifyCode": ""
            }
        response = requests.post(url, headers=self.headers, json=test_data)
        print(f"\n获取手机短信验证码响应结果：{response.text}")
        data = response.json()
        print(f"\n获取手机短信验证码响应结果：{data}")
        assert data.get("code") == 0

    # 手机号短信验证码登录，传入图形验证码和手机短信验证码
    # def test_phoneLogin(self, graphics_data):
    #     url = "https://qa-int.qiyuan.changan.com.cn/user/login"
    #     test_data = {
    #         "code": "",
    #         "dynamicPassword": "439409",
    #         "graphicsKey": graphics_data.get("graphicsKey", ""),
    #         "imgCode": graphics_data.get("imgCode", ""),
    #         "iosOrAndroid": 0,
    #         "isApp": 0,
    #         "lastCity": "",
    #         "lastProvince": "",
    #         "openType": "",
    #         "parentId": "",
    #         "parentLink": "",
    #         "parentType": 0,
    #         "password": "",
    #         "phone": "15922507735",
    #         "rid": "string",
    #         "temporaryToken": "string",
    #         "ydToken": "string"
    #     }
    #     response = requests.post(url, headers=self.headers, json=test_data)
    #     print(f"\n手机号短信验证码登录响应结果：{response.text}")
    #     data = response.json()
    #     print(f"\n手机号短信验证码登录响应结果：{data}")
    #     assert data.get("code") == 0

    # 使用账号密码登录-输入账号密码和验证码登录
    # def test_login(self, graphics_data):
    #     url = "https://qa-int.qiyuan.changan.com.cn/api/password/passwordLogin"
    #
    #     # 获取RSA公钥
    #     public_key = self.get_rsa_public_key()
    #
    #     # 加密密码
    #     encrypted_password = self.encrypt_password("Aa123456", public_key)
    #
    #     img_code = graphics_data.get("imgCode", "")
    #     print(f"\n使用OCR识别验证码登录: {img_code}")
    #     print(f"使用加密密码: {encrypted_password}")
    #
    #     test_data = {
    #         "code": "",
    #         "dynamicPassword": "",
    #         "graphicsKey": graphics_data.get("graphicsKey", ""),
    #         "imgCode": img_code,
    #         "iosOrAndroid": 0,
    #         "isApp": 0,
    #         "lastCity": "",
    #         "lastProvince": "",
    #         "openType": "",
    #         "parentId": "",
    #         "parentLink": "",
    #         "parentType": 0,
    #         "password": encrypted_password,
    #         "phone": "15922507735",
    #         "rid": "",
    #         "temporaryToken": "",
    #         "ydToken": ""
    #     }
    #     responses = requests.post(url, headers=self.headers, json=test_data)
    #     print(f"登录响应结果：{responses.text}")
    #     data = responses.json()
    #     print(f"登录响应结果：{data}")
    #
    #     if data.get("msg") == "操作成功":
    #         print("✅ 登录成功！")
    #         assert True
    #     else:
    #         print(f"❌ 登录失败: {data.get('msg')}")
    #         if public_key:
    #             print("注意：已尝试RSA加密，登录失败可能是其他原因")
    #         else:
    #             print("注意：无法获取RSA公钥，使用NES加密(Base64)")

if __name__ == '__main__':
    pytest.main(['-s', __file__])