import base64
import pytest
import requests
import ddddocr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../page')
from page.test_login_data_driven import Test_DataDriven


class Test_GetDynamicPass:
    headers = {
        "Content-Type": "application/json",
        "skipSign": "hyzh123456",
        "x-gray": "1"
    }

    @pytest.fixture(scope="class")
    def test_data(self, test_data):
        """从Excel加载测试数据"""
        data_loader = Test_DataDriven()
        test_data = data_loader.load_test_data()
        print(f"\n从Excel加载了 {len(test_data)} 条测试数据")
        return test_data

    @pytest.fixture(scope="class")
    def ocr_client(self):
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr

    def get_rsa_public_key(self):
        """获取RSA公钥"""
        # 尝试常见的RSA公钥接口
        endpoints = [
            "/user/getRsa",
            "/api/user/getRsa",
            "/api/common/getRsaKey",
            "/user/getPublicKey",
            "/api/password/getPublicKey",
            "/api/password/getRsaKey",
            "/password/getPublicKey",
            "/password/getRsaKey"
        ]

        for endpoint in endpoints:
            try:
                url = f"https://qa-int.qiyuan.changan.com.cn{endpoint}"
                response = requests.post(url, headers=self.headers, json={"phone": "15922507735"})
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0 and data.get("data"):
                        public_key = data.get("data", {}).get("publicKey") or data.get("data", {}).get("rsaKey")
                        if public_key:
                            print(f"获取到RSA公钥: {public_key[:50]}...")
                            return public_key
            except:
                continue

        # 如果无法获取公钥，返回None
        print("无法获取RSA公钥")
        return None

    def encrypt_password(self, password, public_key=None):
        """使用RSA加密密码"""
        if not public_key:
            # 如果无法获取公钥，尝试使用简单的Base64编码（NES加密的一种简单实现）
            # print("警告：无法获取RSA公钥，使用Base64编码作为NES加密")
            # 这里将"NES"理解为"Network Encoding Scheme"，使用Base64编码
            encoded = base64.b64encode(password.encode()).decode()
            # print(f"密码NES加密(Base64): {password} -> {encoded}")
            return encoded

        try:
            # 如果公钥是字符串格式，需要添加头尾
            if not public_key.startswith("-----BEGIN"):
                public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

            # 加载公钥
            rsa_key = RSA.import_key(public_key)
            cipher = PKCS1_v1_5.new(rsa_key)

            # 加密密码
            encrypted = cipher.encrypt(password.encode())

            # Base64编码
            encrypted_base64 = base64.b64encode(encrypted).decode()
            # print(f"密码RSA加密成功: {password} -> {encrypted_base64[:30]}...")
            return encrypted_base64

        except Exception as e:
            print(f"密码RSA加密失败: {e}")
            # 如果RSA加密失败，使用Base64编码作为备选
            encoded = base64.b64encode(password.encode()).decode()
            # print(f"密码AES加密(Base64): {password} -> {encoded}")
            return encoded

    def encrypt_password_aes(self, password, key=None):
        """使用AES加密密码"""
        try:
            # 如果没有提供密钥，使用默认密钥（16字节）
            if key is None:
                key = b'ThisIsA16ByteKey'  # 16字节密钥用于AES-128
            
            # 生成随机的初始化向量（IV）
            iv = get_random_bytes(16)
            
            # 创建AES加密器
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # 对密码进行填充，使其长度为16字节的倍数
            padded_password = pad(password.encode(), AES.block_size)
            
            # 加密密码
            encrypted = cipher.encrypt(padded_password)
            
            # 将IV和加密后的数据组合，并进行Base64编码
            encrypted_data = iv + encrypted
            encrypted_base64 = base64.b64encode(encrypted_data).decode()
            
            # print(f"密码AES加密成功: {password} -> {encrypted_base64[:50]}...")
            return encrypted_base64
            
        except Exception as e:
            print(f"密码AES加密失败: {e}")
            # 如果AES加密失败，使用Base64编码作为备选
            encoded = base64.b64encode(password.encode()).decode()
            # print(f"密码Base64编码: {password} -> {encoded}")
            return encoded

    @pytest.fixture(scope="class")
    def graphics_data(self, ocr_client, test_data):
        url = "https://qa-int.qiyuan.changan.com.cn/user/getGraphics"
        
        phone = test_data[0].get('phone') if test_data else "15922507735"
        
        test_data_request = {
            "channel": "",
            "graphicsKey": "",
            "imgCode": "",
            "imgCodeSign": 0,
            "isApp": 0,
            "phone": phone,
            "temporaryToken": "",
            "vertifyCode": ""
        }
        responses = requests.post(url, headers=self.headers, json=test_data_request)
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
            "imgCode": img_code,
            "phone": phone
        }
    # 说明：使用OCR识别验证码登录测试
    def test_getgraphicscode(self, graphics_data):
        print(f"\n获取到的graphicsValue: {graphics_data['graphicsValue'][:50]}...")
        print(f"graphicsKey: {graphics_data['graphicsKey']}")
        print(f"OCR识别验证码: {graphics_data['imgCode']}")
        assert graphics_data is not None

    def test_getdynamicpass(self, graphics_data):
        graphics_value = graphics_data["graphicsValue"]

        img_data = base64.b64decode(graphics_value)
        print(f"\n验证码图片大小: {len(img_data)} 字节")

        assert graphics_value is not None

    @pytest.mark.parametrize('test_case', [
        {'phone': '15922507735', 'password': 'Aa123456'},
        {'phone': '18908323900', 'password': 'Aa123456'},
        {'phone': '15200909383', 'password': 'Fq202412301@'}
    ])
    def test_login_data_driven(self, ocr_client, test_case):
        """数据驱动登录测试"""
        url = "https://qa-int.qiyuan.changan.com.cn/api/password/passwordLogin"
        
        phone = test_case['phone']
        password = test_case['password']
        
        graphics_req = {
            "channel": "",
            "graphicsKey": "",
            "imgCode": "",
            "imgCodeSign": 0,
            "isApp": 0,
            "phone": phone,
            "temporaryToken": "",
            "vertifyCode": ""
        }
        graphic_response = requests.post(
            "https://qa-int.qiyuan.changan.com.cn/user/getGraphics",
            headers=self.headers,
            json=graphics_req
        )
        graphic_data = graphic_response.json()
        graphics_value = graphic_data.get("data", {}).get("graphicsValue")
        graphics_key = graphic_data.get("data", {}).get("graphicsKey")
        
        img_bytes = base64.b64decode(graphics_value)
        img_code = ocr_client.classification(img_bytes)
        
        encrypted_password = self.encrypt_password_aes(password)
        
        print(f"\n{'='*50}")
        print(f"测试手机号: {phone}")
        print(f"测试密码: {password}")
        print(f"验证码: {img_code}")
        
        login_data = {
            "code": "",
            "dynamicPassword": "",
            "graphicsKey": graphics_key,
            "imgCode": img_code,
            "iosOrAndroid": 0,
            "isApp": 0,
            "lastCity": "",
            "lastProvince": "",
            "openType": "",
            "parentId": "",
            "parentLink": "",
            "parentType": 0,
            "password": encrypted_password,
            "phone": phone,
            "rid": "",
            "temporaryToken": "",
            "ydToken": ""
        }
        
        response = requests.post(url, headers=self.headers, json=login_data)
        result = response.json()
        
        if result.get("msg") == "操作成功":
            print("✅ 登录成功！")
        else:
            print(f"❌ 登录失败: {result.get('msg')}")
        
        print(f"{'='*50}")


if __name__ == '__main__':
    pytest.main(['-s', __file__])