import datetime
from json import JSONEncoder


# 时间处理类
class JsonCustomEncoder(JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, value)
