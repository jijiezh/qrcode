import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def show():
    """打印当前日期时间"""
    print(datetime.datetime.now())

scheduler = BlockingScheduler()  # 阻塞调度器，会阻塞当前进程
scheduler.add_job(show, 'interval', seconds=3)
scheduler.start()