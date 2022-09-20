# import sys
import json
import requests as req
from logger import logging

corpid = "wwa59760080dff45bc"
corpsecret = "9dtSBlIDif43GMe-CXGWhxRJj0EmVNkxoBvB9MH8PtE"
agentid = "1000002"
token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + \
            "&corpsecret=" + corpsecret


def get_token(url):
    r = req.get(url)
    token_value = list(r.json().values())[2]
    return token_value


token = get_token(token_url)
msg_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
msg_to = "ZhangJiJie"  # sys.argv[1]
msg_body = "Default Message!"  # sys.argv[2] + "\n\n" +sys.argv[3]


# 消息发送的必要信息改为获取命令行的参数，以便在 zabbix使用宏来代替消息内容等信息。


def send_msg(send_data):
    s_msg = send_data
    if isinstance(send_data, list) or isinstance(send_data, dict):
        s_msg = json.dumps(send_data, ensure_ascii=False)
    post_body = {
        "touser": msg_to,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": s_msg
        },
        "safe": 0
    }
    post = req.post(msg_url, data=json.dumps(post_body))
    print("Send 企业微信：" + post.text)
    logging.info('msg_to:' + msg_to + ';msg:' + post.text+';msg_content:'+s_msg)
# send_msg(post_body)
