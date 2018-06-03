import scrapy
from Intelligent.ShopItem import CommentItem
import pymysql
import time
import random
class CommentSpider(scrapy.Spider):
    name = "CommentSpider"
    start_urls=[]
    def __init__(self):
        self.conn=pymysql.connect(host="localhost",user="root",passwd="26651",db="da_zhong")
        self.cursor=self.conn.cursor()
        #筛选爬取url，筛除已爬完的url以及不适用代码中爬取规则的url
        self.cursor.execute("select url,comment_nowpage,shop_name from url_list where (comment_nowpage !='RULE_ERROR' and comment_nowpage !='FINISHED') order by rand();")
        self.url_list=self.cursor.fetchall()
        self.urln=0
        # print("1111")
        # print(self.url_list)
        self.start_urls.append(self.url_list[0][0]+"/review_all"+self.url_list[0][1])
        self.cursor.close()
    def parse(self, response):
        item=CommentItem()
        # items=[]
        now_url = self.url_list[self.urln][0]
        wait_time=[9,7,8]
        self.cursor = self.conn.cursor()
        # handle_httpstatus_list = [403]
        got_data=False
        rule_error=False
        try:
            item['shop_name']=response.xpath("//div[@class='review-list-header']/h1/a/@title").extract()
            item['city']=response.xpath('//a[@class="city J-city"]/span[2]/text()').extract()
            if item['city']:
                item['city']=item['city'][0]
            else:
                item['city']='False'
            if item['shop_name']:
                item['shop_name']=item['shop_name'][0]
            else:
                item['shop_name']='False'
            print(item['shop_name'])
            if response.status == 200:
                for box in response.xpath('//div[@class="reviews-items"]/ul/li'):
                    got_data=True
                    rule_error=False
                    all_dishes = ''
                    split_str='sml-str'
                    # sml-rank-stars sml-str40 star     4星
                    item['star']=box.xpath('.//div[@class="review-rank"]/span[1]/@class').extract()
                    if item['star']:
                        item['star']=item['star'][0]
                        item['star']=item['star'].partition(split_str)[2]   # 得到 40 star
                        item['star']=item['star'][:3] #得到40
                        if item['star']!='':
                            item['star']=str(int(item['star'])/10)  # 得到4
                    else:
                        item['star']='not found'
                    tmp_name=box.xpath('.//a[@class="name"]/text()').extract()
                    if not tmp_name:
                        tmp_name=box.xpath('.//span[@class="name"]/text()').extract()
                    if tmp_name:
                        item['author']=tmp_name[0].strip()
                    item['avg_pay']=box.xpath('.//span[@class="score"]/span[4]/text()').extract()
                    if item['avg_pay']:
                        item['avg_pay']=item['avg_pay'][0].strip()
                    else:
                        item['avg_pay']='NULL'
                    item['taste']=box.xpath('.//span[@class="score"]/span[@class="item"][1]/text()').extract()
                    if item['taste']:
                        item['taste']=item['taste'][0].strip()
                    else:
                        item['taste']='not found'
                    item['environment']=box.xpath('.//span[@class="score"]/span[@class="item"][2]/text()').extract()
                    if item['environment']:
                        item['environment']=item['environment'][0].strip()
                    else:
                        item['environment']='not found'
                    item['service']=box.xpath('.//span[@class="score"]/span[@class="item"][3]/text()').extract()
                    if item['service']:
                        item['service']=item['service'][0].strip()
                    else:
                        item['service']='not found'
                    tmp = box.xpath('.//div[@class="review-words"]')
                    if not tmp:
                        tmp=box.xpath('.//div[@class="review-words Hide"]')
                    if tmp:
                        item['comment']=tmp.xpath('string(.)').extract()[0].strip()
                    else:
                        item['comment']="error"
                    # item['comment']=''.join(str(item['comment']).split('\\')).replace('\\','@')
                    item['like_dishes']=box.xpath('.//div[@class="review-recommend"]/a/text()').extract()
                    item['like_dishes']=list(set(item['like_dishes']))
                    for dish in item['like_dishes']:
                        all_dishes+=dish+' '
                    item['like_dishes']=all_dishes
                    item['date']=box.xpath('.//span[@class="time"]/text()').extract()[0].strip()
                    item['album'] = ''
                    for pic in box.xpath('.//div[@class="review-pictures"]/ul/li'):
                        img_url=pic.xpath('./a/img/@data-big').extract()[0]
                        item['album']=item['album']+img_url+'+'
                    yield item
                sql = "update url_list set comment_date='" + time.strftime("%Y-%m-%d",time.localtime()) + "' where url='" + now_url + "';"
                self.cursor.execute(sql)
                print(sql)
                self.conn.commit()
                wait = random.choice(wait_time)

                if not got_data:
                    print("Spider Fail:NOT FOUND!")
                    #RULE_ERROR 表示网页不适用上面的爬取规则
                    rule_error=True
                    sql="update url_list set comment_nowpage='RULE_ERROR' where url='" + now_url + "';"
                    self.cursor.execute(sql)
                    print(sql)
                    self.conn.commit()
                next_url=response.xpath("//a[@class='NextPage']/@href").extract()
                if next_url and rule_error==False:
                    # time.sleep(wait)
                    next_url=next_url[0]
                    nextpage = response.xpath("//a[@class='NextPage']/@data-pg").extract()[0]
                    #更新数据库中的当前页
                    self.cursor.execute("update url_list set comment_nowpage='/p" +nextpage+ "'where url='" + now_url + "';")
                    self.conn.commit()
                    yield scrapy.Request("http://www.dianping.com"+next_url,callback=self.parse,dont_filter=False)
                else:
                    #更新数据库：已爬完所有页数
                    if got_data:
                        self.cursor.execute("update url_list set comment_nowpage='FINISHED'" + "where url='" + now_url + "';")
                        self.conn.commit()
                        print("FINISHED!!!")
                    # time.sleep(60)
                    self.urln += 1
                    yield scrapy.Request(self.url_list[self.urln][0]+"/review_more"+self.url_list[self.urln][1],callback=self.parse,dont_filter=False)
                self.cursor.close()
            else:
                yield scrapy.Request(self.url_list[self.urln][0] + "/review_more" + self.url_list[self.urln][1],callback=self.parse, dont_filter=False)
                self.cursor.close()
        except Exception as e:
            print("异常")
            print(e)