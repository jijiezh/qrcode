from flask import Flask
from flask_cors import CORS
from flask import request
import json
from json_time_formatter import JsonCustomEncoder
from db_helper_mysql import conn
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args

    dict = ImmutableMultiDict(data).to_dict()
    return dict.get('page'), dict.get('limit')


@app.route('/weatherinfo/queryone', methods=['GET', 'POST'])
def articles_query_one():
    results = {
        'data': []
        , 'code': 0
        , 'msg': ''
    }

    squery_sql = [""" select * from rt_weather_info t """]
    squery_sql.append(""" where t.is_used = '0' """)
    squery_sql.append(""" order by t.create_time desc limit 1""")

    base_query_sql = ''.join(squery_sql)
    try:
        with conn.cursor() as cursor:
            print(base_query_sql)
            cursor.execute(base_query_sql)
            results['data'] = cursor.fetchall()
            results['code'] = 0
        print("Success:  fetch data !")
    except Exception as e:
        print("Error: unable to fetch data,For reason: s%" %e)

    return json.dumps(results, cls=JsonCustomEncoder, ensure_ascii=False)


# http://127.0.0.1:5000/test?pagesize=15&pageindex=1
CORS(app, resources=r'/*')


@app.route('/weatherinfo/querylist', methods=['GET', 'POST'])
def articles_query_page():
    results = {
        'data': []
        , 'code': 0
        , 'count': 0
        , 'msg': ''
    }
    pageindex, pagesize = request_parse(request)
    pageindex = 1 if pageindex is None else pageindex
    pagesize = 100 if pagesize is None else pagesize

    # pageindex = int(pageindex) if int(pageindex) < 1 else 1
    offset = int(pagesize) * (int(pageindex) - 1)

    squery_sql = [""" select * from rt_weather_info t """]
    squery_sql.append(""" where t.is_used = '0' """)
    squery_sql.append(""" order by t.create_time desc """)

    base_query_sql = ''.join(squery_sql)
    try:
        with conn.cursor() as cursor:
            page_query_sql = base_query_sql + """ limit %d offset %d """ % (int(pagesize), offset)

            print(page_query_sql)
            cursor.execute(page_query_sql)
            results['data'] = cursor.fetchall()

            count_query_sql = """select count(1) as rcount from (""" + base_query_sql + """) as tmp"""
            cursor.execute(count_query_sql)
            results['count'] = cursor.fetchone()['rcount']
            results['code'] = 0
        print(results)
    except Exception as e:
        print("Error: unable to fetch data,For reason: s%", e)

    return json.dumps(results, cls=JsonCustomEncoder, ensure_ascii=False)
