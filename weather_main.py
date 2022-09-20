import time

from flask_server import app
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from job_req_weather_info import AMap_WeatherInfo
from gevent import pywsgi

# 任务配置类
class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'req_weather_info',  # 任务id
            'func': 'weather_main:dojob_req_weatherinfo',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'interval',  # 任务执行类型，定时器
            'hours': 3,
            'replace_existing': True
        }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SCHEDULER_API_ENABLED = True


# 定义任务执行程序
def dojob_req_weatherinfo():
    print("Start schedule job at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    AMap_WeatherInfo().run()


if __name__ == '__main__':
    app.config.from_object(SchedulerConfig())
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表载入实例flask
    scheduler.start()  # 启动任务计划

    # app.run(host='127.0.0.1', port=5000, use_reloader=False)
    server = pywsgi.WSGIServer(('127.0.0.1',5000),app)
    server.serve_forever()