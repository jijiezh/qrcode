# coding:utf-8
import requests as req
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED
import make_qrcode
import json

# https://restapi.amap.com/v3/weather/weatherInfo?city=110000&key=0b88a4341edd1b0d22a57556b3507272
url = 'https://restapi.amap.com/v3/weather/weatherInfo'
parms = {
    'city': '110000',
    'key': '0b88a4341edd1b0d22a57556b3507272'
}


def job_func():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    ret = req.get(url, params=parms)
    print(ret.json())
    qr_data = json.dumps(ret.json())
    make_qrcode.make_qrcode_img(qr_data)


job_func()

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_job(job_func, 'cron', hour='8,11,18', minute='30')
# scheduler.add_job(job_func, 'interval', seconds=5)
scheduler.start()
while True:
    time.sleep(1)
    if scheduler.state == STATE_STOPPED:
        break
