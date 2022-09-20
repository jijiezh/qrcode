# -*-coding:utf-8-*-
import stomp
import time
from stomp.listener import ConnectionListener

default_topic = '/topic/demoTopic'
default_host = '172.18.8.63'
default_port = 61613
default_user = 'manbuzhe'
default_pwd = '20180725'

conn10 = stomp.Connection10([(default_host, default_port)])
class SampleListener(ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        for x in range(10):
            print(x)
            time.sleep(1)
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


# 订阅主题
def connect_and_subscribe():
    conn10.set_listener("myListener", SampleListener(conn10))
    conn10.connect(default_user, default_pwd, wait=True)
    conn10.subscribe(destination=default_topic, id="clientside_11", ack='auto')
    while True:
        pass
    conn10.disconnect()


if __name__ == '__main__':
    connect_and_subscribe()
