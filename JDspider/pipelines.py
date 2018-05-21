# -*- coding: utf-8 -*-
from Sql import Sql
from JDspider.items import JDSpiderItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 插入数据库Pipeline
class JdspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JDSpiderItem):
            platform = item['platform']
            link = item['link']
            brand = item['brand']
            product = item['product']
            model = item['model']
            category = item['category']
            price = item['price']
            allcount = item['allcount']
            goodrate = item['goodrate']
            goodcount = item['goodcount']
            generalcount = item['generalcount']
            poorcount = item['poorcount']
            aftercount = item['aftercount']
            showcount = item['showcount']
            title = item['title']
            subtitle = item['subtitle']
            project_id = item['project_id']
            datetime = item['datetime']

            Sql.insert_JD_name(platform, link, brand, product, model,
        category, price, allcount, goodrate, goodcount,
        generalcount, poorcount, aftercount, showcount, title,
        subtitle, project_id, datetime)
        return item

# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host = settings["MYSQL_HOST"],
#             db = settings["MYSQL_DBNAME"],
#             user = settings["MYSQL_USER"],
#             passwd = settings["MYSQL_PASSWORD"],
#             charset='utf8',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
#
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         #使用twisted将mysql插入变成异步执行
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider) #处理异常
#
#     def handle_error(self, failure, item, spider):
#         #处理异步插入的异常
#         print (failure)
#
#     def do_insert(self, cursor, item):
#         #执行具体的插入
#         #根据不同的item 构建不同的sql语句并插入到mysql中
#         insert_sql, params = item.get_insert_sql()
#         cursor.execute(insert_sql, params)


