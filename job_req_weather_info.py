# coding:utf-8
import requests as req
import time
import make_qrcode
import json
from db_helper_mysql import write_db


# 查询实时天气
class AMap_WeatherInfo(object):

    def __init__(self):
        self.web_site = 'amap'
        self.web_site_desc = '实时天气'
        self.web_site_url = 'https://restapi.amap.com/v3/weather/weatherInfo'
        self.weather_city = '110000'
        self.access_key = "0b88a4341edd1b0d22a57556b3507272"

    # 1. 发请求
    def send_request(self):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        ret = req.get(self.web_site_url, params={
            'city': self.weather_city,
            'key': self.access_key
        })
        # .content.decode('utf-8')

        qr_data = json.dumps(ret.json(), ensure_ascii=False)
        return qr_data

    # 2. 生成二维码
    def make_qrcode_img(self, qr_data):
        return make_qrcode.make_qrcode_img(qr_data)

    # 3. 保存到数据库
    def write_db_many(self, data):
        return write_db(self,data)

    # 4.调度
    def run(self):
        # 1. 发请求
        data = self.send_request()
        # 2.解析
        img_data = self.make_qrcode_img(data)
        # 3.存储
        self.write_db_many(img_data)


if __name__ == '__main__':
    AMap_WeatherInfo().run()
