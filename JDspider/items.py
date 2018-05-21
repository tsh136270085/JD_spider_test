# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 商品信息item
class JDSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    platform = scrapy.Field()
    link = scrapy.Field()
    brand = scrapy.Field()
    product = scrapy.Field()
    model = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    allcount = scrapy.Field()
    monsale = scrapy.Field()
    goodrate = scrapy.Field()
    goodcount = scrapy.Field()
    generalcount = scrapy.Field()
    poorcount = scrapy.Field()
    aftercount = scrapy.Field()
    showcount = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    project_id = scrapy.Field()
    datetime = scrapy.Field()




    # ID = scrapy.Field()  # 商品ID
    # name = scrapy.Field()  # 商品名字
    # commentcount = scrapy.Field()  # 评论人数
    # shop_name = scrapy.Field()  # 店家名字
    # price = scrapy.Field()  # 价钱
    # link = scrapy.Field()  #链接
    # # commentVersion = scrapy.Field()
    # poorcount = scrapy.Field()  #差评
    # generalcount = scrapy.Field()  #中评
    # goodcount = scrapy.Field()  #好评
    # aftercount = scrapy.Field()  #追评
    # showcount = scrapy.Field()  #晒图

