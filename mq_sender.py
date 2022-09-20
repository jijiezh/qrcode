# -*-coding:utf-8-*-
import stomp
import time

default_topic = '/topic/demoTopic'
default_host = '172.18.8.63'
default_port = 61613
default_user = 'manbuzhe'
default_pwd = '20180725'


def send_to_topic(msg):
    conn = stomp.Connection10([(default_host, default_port)])
    conn.connect(default_user, default_pwd, wait=True)
    for i in range(10):
        conn.send(body='topic: 测试信息1...',destination=default_topic)
        time.sleep(5)
    conn.disconnect()


if __name__ == '__main__':
    send_to_topic("11111")
