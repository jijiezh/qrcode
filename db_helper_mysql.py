import pymysql

conn = pymysql.connect(
    host="10.11.131.124",
    user="root", password="root",
    database="py_db_platform",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor)
insert_sql = "insert into rt_weather_info(img_url, img_digits, img_content) values (%s, %s, %s)"


def write_db(self, data, info='插入天气数据'):
    try:
        with conn.cursor() as cursor:
            result = []
            for item in data:
                itemvs = tuple(item.values())
                result.append(itemvs)
            # 批量插入数据
            cursor.executemany(insert_sql, tuple(result))
            conn.commit()  # 提交请求， ********
    except Exception as e:
        print("********   %s  插入失败   ********" % self.web_site_desc)
        print(e)
    else:
        print('********   %s 保存成功   ********' % self.web_site_desc)
