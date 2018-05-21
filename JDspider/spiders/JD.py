# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from JDspider.items import JDSpiderItem
import scrapy
import re
import json
import csv


class JDSpider(Spider):
    name = "JDSpider"
    # start_urls = ['https://list.jd.com/list.html?cat=1320,5019,12215']
    start_urls = []
    there = input('请输入要爬取的产品名称：')
    with open(there + '.csv', 'w', newline="") as f:  #根据输入的搜索字段生成csv文件
        fieldnames = ['平台', 'link', '品牌', '产品', '型号', '类别', '价格', '总评价数', '好评率', '好评数', '中评数', '差评数',
                      '追评数', '晒图数', '标题', '产品ID', '抓取时间']
        write = csv.DictWriter(f, fieldnames=fieldnames)
        write.writeheader()
    for i in range(1, 2):  # 根据需求设置页数
        #url = 'https://list.jd.com/list.html?cat=1320,5019,12215&page=' + str(i) + '&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
        url = 'http://search.jd.com/Search?keyword=' + there +'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=''&page=' + str(i) + '&s=1&click=0'
        #url = 'https://search.jd.com/Search?keyword=牛奶&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=' + str(i) + '&s=57&click=0'
        start_urls.append(url)

    # def parse_name(self, response):
    #     item1 = response.meta['item']
    #     sel = Selector(response.body)  # Xpath选择器
    #     print(sel)
    #     bad = sel.xpath('//div[@class="w"]')
    #     # '//li[@class="gl-item"]'
    #     print(bad)
    #     qwe = bad.xpath('/html/body/div[7]/div/div[2]/div[1]/text()').extract()
    #     print(qwe)
    #     a = str(response.body).split('(')
    #     yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_name)

    def parse_price(self, response):
        import time
        item1 = response.meta['item']
        a = str(response.body).split('(')
        b = a[1]
        c = b.split(');')
        temp1 = c[0]
        js = json.loads(temp1)
        item1['price'] = js[0]['p']   #获取产品价格
        time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item1['datetime'] = time    #获取当前时间
        column0 = [item1['platform'], item1['link'], item1['brand'], item1['product'], item1['model'],
                   item1['category'], item1['price'], item1['allcount'], item1['goodrate'], item1['goodcount'],
                   item1['generalcount'], item1['poorcount'], item1['aftercount'], item1['showcount'], item1['title'],
                   item1['project_id'], item1['datetime']]
        bll = []
        bll.append(column0)
        with open(self.there+'.csv', 'a+', newline="") as f:
            # f.write()
            writer = csv.writer(f)
            writer.writerows(bll)  #写入csv文件
            return item1
            # print(column0)
            # cll = bll.append(column0)
            # print(cll)
            # all = str(cll)
            # print(all)
            # bll = str(cll).split("']")
            # print(bll)
            # with open('tset.csv', 'w+') as f:
            #     dw = csv.DictWriter(f, bll[0])
            #     dw.writeheader()
            #     for row in bll:
            #         dw.writerow(row)
            # fieldnames = ['first_name', 'last_name']
            # head = csv.DictWriter(f, fieldnames=fieldnames)
            # head.writeheader()
        # url = 'https://item.jd.com/' + item1['project_id'] + '.html'
        # yield scrapy.Request(url, meta={'item': item1}, callback=self.excel_write)

    def parse_getCommentnum(self, response):
        item1 = response.meta['item']
        a = re.sub(r"\\xcd\\xf2+", r"", str(response.body)[2:-1])
        js = json.loads(a)
        item1['poorcount'] = js['CommentsCount'][0]['PoorCount']  #获取各种评价数量
        item1['generalcount'] = js['CommentsCount'][0]['GeneralCount']
        item1['goodcount'] = js['CommentsCount'][0]['GoodCount']
        item1['aftercount'] = js['CommentsCount'][0]['AfterCount']
        item1['showcount'] = js['CommentsCount'][0]['ShowCount']
        item1['allcount'] = js['CommentsCount'][0]['CommentCount']
        item1['goodrate'] = js['CommentsCount'][0]['GoodRate']
        num = item1['project_id']  # 获取商品ID
        s1 = re.findall("\d+", str(num))[0]
        # 价格requesturl
        url = "https://p.3.cn/prices/mgets?callback=jQuery6116480&type=1&area=1_72_2799_0&pdtk=&pduid=1526375186851325533471&pdpin=&pin=null&pdbp=0&skuIds=J_" + s1
        # url = 'https://item.jd.com/' + item1['ID'] + '.html'
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_price)

    def parse_detail(self, response):
        # pass
        item1 = response.meta['item']
        # if re.search(r'com', item1['link']):
        sel = Selector(response)  # Xpath选择器
        # 获取各种产品信息
        category = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[1]/a/text()').extract()).split("'", 2)
        # print(category)
        model = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[9]/text()').extract()).split("'", 2)
        # print(model)
        brand = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract()).split("'", 2)
        # print(brand)
        product = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract()).split("'", 2)
        # print(product)
        # 将产品信息放入item1
        item1['model'] = model[1]
        item1['brand'] = brand[1]
        item1['product'] = product[1] + self.there
        item1['category'] = category[1]
        # if sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract() == None:
        #     b = item1['title'][0]
        #     print(b)
        #     item1['brand'] = b
        # else:
        # brand = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract()).split("'", 2)
        # #print(brand)
        # if brand == '[]':
        #     b = item1['title'][0]
        #     print(b)
        #     item1['brand'] = b
        #     #print(brand)
        # else:
        #     item1['brand'] = brand[1]
        #
        # if sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract() == None:
        #     p = str(sel.xpath('.div/div[@id="item ellipsis"]/text()').extract())
        #     print(p)
        #     item1['product'] = p + self.there
        # else:
        #     product = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract()).split("'", 2)
        #     #print(product[1] + self.there)
        #     item1['product'] = product[1] + self.there
        #
        # if sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[9]/text()').extract() == None:
        #     m = str(sel.xpath('.div/div[@id="item ellipsis"]/text()').extract())
        #     print(m)
        #     item1['model'] = m
        # else:
        #     model = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[9]/text()').extract()).split("'", 2)
        #     # print(model[1])
        #     item1['model'] = model[1]
        #
        # if str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[1]/a/text()').extract()) == ['']:
        #     item1['category'] = '全球购没有分类'
        # else:
        #     category = str(sel.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[1]/a/text()').extract()).split("'", 2)
        #     item1['category'] = category[1]
        # if response.url[:18] == 'https://item.jd.hk':
        # if re.search(r"https://item.jd.hk", response.url):  #判断是否为全球购
        #     goods = sel.xpath('//div[@class="shopName"]')
        #     temp = str(goods.xpath('./strong/span/a/text()').extract())[2:-2]
        #     if temp == '':
        #         item1['shop_name'] = '全球购：' + 'JD全球购'  #判断是否JD自营
        #     else:
        #         item1['shop_name'] = '全球购：' + temp
        #     # print('全球购：'+ item1['shop_name'])
        #
        # else:
        #     goods = sel.xpath('//div[@class="J-hove-wrap EDropdown fr"]')
        #     item1['shop_name'] = str(goods.xpath('./div/div[@class="name"]/a/text()').extract())[2:-2]
        #     if item1['shop_name'] == '':       #是否JD自营
        #         item1['shop_name'] = '京东自营'
        #     # print(item1['shop_name'])

        url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + item1['project_id']
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_getCommentnum)

    def parse(self, response):  # 解析搜索页
        # print(response.text)
        sel = Selector(response)  # Xpath选择器
        goods = sel.xpath('//li[@class="gl-item"]')
        print(goods)
        for good in goods:
            item1 = JDSpiderItem()

            temp1 = str(good.xpath('./div/div[@class="p-name p-name-type-2"]/a/em/text()').extract())
           #print(temp1)
            pattern = re.compile("[\u4e00-\u9fa5]+.+\w")   # 匹配商品名称
            good_name = re.search(pattern, temp1)
            # print(str(good_name.group()))
            # brand = str(good_name).split(',')
            # product = str(good_name).split(',')
            item1['title'] = good_name.group()  #得到标题
            item1['subtitle'] = ''   #没有副标题
            # item1['brand'] = brand[2]
            # item1['product'] = product[2] + self.there

            #print(item1)
            # if re.search(r"https://item.jd.hk", response.url):
            #     continue
            #print(str(good.xpath('./div/div[@class="p-img"]/a/@href').extract()))
            a = str(good.xpath('./div/div[@class="p-img"]/a/@href').extract())[2:-2]
            if re.search(r'https://ccc-x.jd.com', a):       # 判断当前url是否符合，不符合则进行修改
                continue
            if re.search(r'https:', a):
                item1['link'] = a
            else:
                item1['link'] = 'https:' + a
            # if re.search(r'http', a):
            #     item1['link'] = a
            # elif re.search(r'https://ccc-x.jd.com', a):
            #     continue
            # else:
            #     item1['link'] = 'https:' + a
            # https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xNjM3MDk5MzE0Ni5odG1s&log=rTX8qIKNmZj2al4qo8OE4NyAAkYC6LbYXR2D6uMnMvWBcWrpePdaqVcb7YwzZd1-LLMEhhUF6huSgxuQ6pV4AV48jzJRwrfvKdkRz1R4MRMtIC1nBl95wDYvb_v0aNnFMuIlRzjiJeqgU0jXCnjdJamwUXwbAR6LU5oeFJt5ufQAH1-SSA_L2dOVstPSyLOMLkh0-YNQ0XGXb6KzCa3H7roGWJlwkYw_mffzm6qKNHljMEYIh5Wk_T1APCAkW22VxheYV9QHp6fYUn-EE7_zyQL4Lx6Kv2OYbQX8msynCla8gawatKE7tGFwH6W-WRKCmryLnVJkBNevzI0wu5k8SVUveAVduYTIULFjgMSeK6nNiS35WUIwzWiHjuFYI6pEU8ex1PdL2l0Baut_VVk7Yfr-323nm5L9HrHoJaBTPbluXiA7tRL_tB6v4CnBpfHo&v=404
            print(item1['link'])
            a = item1['link'][20:]
            b = str(a).split(".html")
            # print(b)
            item1['project_id'] = b[0] # 拿到商品ID

            q = str(item1['link']).split('.', 2)
            if q[1] == 'jd':
                item1['platform'] = '京东'  # 判断平台
            #item1['ID'] = good.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()
            # a = good.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()
            # print(len(a))
            # item1['ID'] = good.xpath('//div/ul/li/@data-sku').extract()
            #i = 1
            # while (i < 30):
            #     j = 2
            #     while (j <= (i / j)):
            #         b = a
            #     i = i + 1
            # for i in a[::-1]:
            #     item1['ID'] = i
            # 判断是否为全球购
            if good.xpath('./div/div[@class="p-name"]/a/em/span/text()').extract() == ['全球购']:
                item1['link'] = 'https://item.jd.hk/' + item1['ID'] + '.html'
            # url = item1['link'] + "#comments-list"
            url = item1['link']
            yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_detail)
