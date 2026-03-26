import pytest
import requests
from page import get_headers_with_token ,BASE_URL

class Test_Aiche_Page:
    def setup_method(self):

        print("开始测试")
        # 使用全局方法获取包含最新token的请求头
        self.headers_data = get_headers_with_token()

    # 购车全部车系展示
    def test_lovecar(self):

        url = f"{BASE_URL}/qy/carorder/index_one"
        test_data = {
                    "latitude":"fuLPKgOiQa3PesFKgU\/gNw==",
                    "longitude":"fuLPKgOiQa3PesFKgU\/gNw==",
                    "version":4
                    }

        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        # print(data)
        assert data.get("msg") == "操作成功"

    # 预约试驾
    def test_yuyue(self):
        url = f"{BASE_URL}/qy/carorder/saveDriveOrder"
        test_data = {
                    "seriesCode":"C236ICA2",
                    "dealerId":710,
                    "customerName":"测试",
                    "customerPhoneNo":"15922507735",
                    "referencePhone":"",
                    "type":0,
                    "source":0,
                    "testDriveTime":"",
                    "busSource":"",
                    "busSource2":""
                    }

        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

    # 大定创建订单
    def test_dadizhiding(self):
        url = f"{BASE_URL}/qy/carorder/createCarBigOrder"
        test_data = {
                    "busSource2":"",
                    "trainColourId":20847,
                    "source":"0",
                    "orderCenterNo":"JQYC14542",
                    "subId":"",
                    "orderCouponPrice":"",
                    "buyPersonalType":0,
                    "buyPersonalName":"测试",
                    "idType":"0",
                    "custCardNum":"500101198611223344",
                    "operator":"",
                    "buyPersonalPhone":"15922507735",
                    "carModelAttrInfoList":
                        [{
                        "carCode":"LB7",
                        "carModelId":1850,
                        "carSeriesId":15,
                        "modelAttrId":110426,
                        "trainCode":"C236ICA2",
                        "trainId":422
                        }],
                    "buyCarType":0,
                    "cashDiscountList":[],
                    "carOrderEquityList":[],
                    "giftPacksList":[],
                    "referencePhone":"",
                    "proExpertName":"",
                    "equity":[],
                    "seriesCode":"C236ICA2",
                    "policy": "",
                    "carConfigNameList":"[\"纯电版\",\"625旗舰型\",\"曜石黑\",\"幕夜黑\",\"19吋米其林舒适静音轮胎\",\"APA高级智能泊车系统订阅服务\"]",
                    "policy2":"[]",
                    "newListPolicy":[],
                    "busSource":"",
                    "modelAttrValueId":15045,
                    "freeJson":"{\"cash\":[{\"carModelAttrValueDiscountDetailQyList\":[{\"name\":\"现金优惠\",\"price\":3000}],\"name\":\"11月优惠\"}],\"optional\":[{\"text\":\"APA高级智能泊车系统订阅服务\",\"value\":1500}],\"color\":{\"text\":\"曜石黑\",\"value\":1000},\"interior\":{\"text\":\"幕夜黑\",\"value\":500}}",
                    "latitude":29.563628779108765,
                    "longitude":106.58770047704407,
                    "idNo":"500101198611223344"
                    }

        responses = requests.post(url=url, headers=self.headers_data, json=test_data)
        data = responses.json()
        print(data)
        assert data.get("msg") == "操作成功"

if __name__ == '__main__':
    pytest.main(['-s', 'test_lovecar.py'])

