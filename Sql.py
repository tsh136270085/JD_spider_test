# -*- coding: utf-8 -*-
import pymysql.connections
import pymysql.cursors

# 数据库连接参数
MYSQL_HOSTS = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "JD_test"

connect = pymysql.Connect(
    host=MYSQL_HOSTS,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    database=MYSQL_DB,
    charset="utf8"
)

cursor = connect.cursor()
# # 插入数据
class Sql:
    @classmethod
    def insert_JD_name(cls, platform, link, brand, product, model,
                       category, price, allcount, goodrate, goodcount,
                       generalcount, poorcount, aftercount, showcount, title,
                       subtitle, project_id, datetime):
        sql = "INSERT INTO jd_name (platform, link, brand, product , model, category , price , allcount," \
              "goodrate, goodcount, generalcount, poorcount, aftercount, showcount, title, subtitle, project_id, datetime) " \
              "VALUES ( %(platform)s, %(link)s, %(brand)s, %(product)s, %(model)s" \
              ", %(category)s,  %(price)s, %(allcount)s, %(goodrate)s, %(goodcount)s, %(generalcount)s, %(poorcount)s, %(aftercount)s" \
              ", %(showcount)s, %(title)s, %(subtitle)s, %(project_id)s, %(datetime)s)"
        value = {
            'platform': platform,
            'link': link,
            'brand': brand,
            'product': product,
            'model': model,
            'category': category,
            'price': price,
            'allcount': allcount,
            'goodrate': goodrate,
            'goodcount': goodcount,
            'generalcount': generalcount,
            'poorcount': poorcount,
            'aftercount': aftercount,
            'showcount': showcount,
            'title': title,
            'subtitle': subtitle,
            'project_id': project_id,
            'datetime': datetime,
        }
        cursor.execute(sql, value)
        connect.commit()
        # print('成功插入', cursor.rowcount, '条数据')
