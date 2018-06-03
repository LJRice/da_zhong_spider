import scrapy
from Intelligent.ShopItem import ShopItem
import time
import pymysql
import random
class ShopSpider(scrapy.Spider):
    name = "ShopSpider"
    start_urls = []
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="26651", db="da_zhong")
        self.cursor = self.conn.cursor()
        self.cursor.execute("select url from url_list where spider_date is NULL;")
        # self.conn.commit()
        self.url_list = self.cursor.fetchall()
        self.urln=0
        self.start_urls.append(self.url_list[0][0])
        self.cursor.close()
    def parse(self, response):
        item = ShopItem()
        # 爬取商店信息  8s/页
        wait_time = [6,7,8,9]
        now_url=self.url_list[self.urln][0]
        # handle_httpstatus_list=[403]
        self.cursor = self.conn.cursor()
        # print(now_url)
        now=0
        time.sleep(60)
        if response.status == 404:
            self.urln += 1
            next_shop = self.url_list[self.urln][0]
            yield scrapy.Request(next_shop, callback=self.parse, dont_filter=False, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'"})
        if response.status == 200 :
            item['place'] = response.xpath('//a[@class="city J-city"]/span[2]/text()').extract()
            if item['place']:
                item['place']=item['place'][0]+'-'
            else:
                item['place']=" -"
            for box in response.xpath('//div[@class="main"]'):
                item['shop_name'] = box.xpath('.//h1[@class="shop-name"]/text()').extract()
                if item['shop_name']:
                    item['shop_name']=item['shop_name'][0].strip()
                else:
                    item['shop_name']='not found'
                item['comment_num'] = box.xpath('.//span[@id="reviewCount"]/text()').extract()
                if item['comment_num']:
                    item['comment_num']=item['comment_num'][0].strip()
                else:
                    item['comment_num']='not found'
                item['avg_pay'] = box.xpath('.//span[@id="avgPriceTitle"]/text()').extract()
                if item['avg_pay']:
                    item['avg_pay']=item['avg_pay'][0].strip()
                else:
                    item['avg_pay']='not found'
                item['shop_type'] = box.xpath('.//p[@class="description"]/span[3]/text()').extract()
                if item['shop_type']:
                    item['shop_type']=item['shop_type'][0].strip()
                else:
                    item['shop_type']='not found'
                tmp_place = box.xpath('.//span[@itemprop="street-address"]/@title').extract()[0].strip()
                item['place'] = item['place'] + tmp_place
                item['taste'] =box.xpath('.//span[@id="comment_score"]/span[1]/text()').extract()
                if item['taste']:
                    item['taste']=item['taste'][0]
                else:
                    item['taste']='NULL'
                item['environment'] = box.xpath('.//span[@id="comment_score"]/span[2]/text()').extract()
                if item['environment']:
                    item['environment']=item['environment'][0]
                else:
                    item['environment']='NULL'
                item['service'] = box.xpath('.//span[@id="comment_score"]/span[3]/text()').extract()
                if item['service']:
                    item['service'] = item['service'][0]
                else:
                    item['service'] = 'NULL'
                item['open_time']=box.xpath('.//p[@class="info info-indent" and not(@id)]/span[2]/text()').extract()
                if item['open_time']:
                    item['open_time']=item['open_time'][0].strip()
                else:
                    item['open_time']='not found'
                item['phone']=box.xpath('.//span[@itemprop="tel"]/text()').extract()
                if item['phone']:
                    item['phone']=item['phone'][0]
                else:
                    item['phone']="NULL"
                self.cursor.execute("update url_list set spider_date='" + time.strftime("%Y-%m-%d",time.localtime()) + "' where url='"+now_url+"';")
                # print("update url_list set spider_date='" + time.strftime("%Y-%m-%d",time.localtime()) + "' where url='"+now_url+"';")
                self.conn.commit()
                self.cursor.close()
                wait = random.choice(wait_time)
                time.sleep(wait-5)
            yield item
        elif response.status == 403:
            now=1
            wait = random.choice(wait_time)
            time.sleep(wait-5)
            yield scrapy.Request(now_url, callback=self.parse, dont_filter=True,headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'"})
        if now==0:
            self.urln += 1
            next_shop = self.url_list[self.urln][0]
            yield scrapy.Request(next_shop, callback=self.parse, dont_filter=False, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'"})
