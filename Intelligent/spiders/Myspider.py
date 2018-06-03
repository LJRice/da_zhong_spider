import scrapy
from Intelligent.ShopItem import UrlItem
import time


class Myspider(scrapy.Spider):
    # spider名字
    name = "Myspider"
    # 允许访问的域
    # allowed_domains = ["http://www.dianping.com/"]
    # 爬取起点
    g = 0
    r = 0
    place = 152
    now_page=1
    start_urls = [('http://www.dianping.com/search/category/%d/10/' % (place))]
    # 爬取函数
    def parse(self, response):
        # 实例一个容器对象
        item = UrlItem()
        # 爬取到的商家url
        item['url_list']={}
        # 爬取商店链接组  8s/页
        if response.status==200:
            self.now_page+=1
            for box in response.xpath('//div[@id="shop-all-list"]//li[@class]'):
                item['shop_name']=box.xpath('.//h4/text()').extract()[0].strip()
                url=box.xpath('.//a[@data-hippo-type="shop"]/@href').extract()[0]
                item['url_list'][item['shop_name']]=url
                yield item
            # 跟进urls
            next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
            if next_url:
                # 返回url
                next_url = next_url[0]
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=False)
            else:
                self.now_page=1
                if self.place<200:
                    self.place+=1
                next_purl=('http://www.dianping.com/search/category/%d/10' % (self.place,))
                yield scrapy.Request(next_purl,callback=self.parse,dont_filter=False)
        else:
            now_purl = ('http://www.dianping.com/search/category/%d/10/p%d' % (self.place,self.now_page))
            print("try again:"+now_purl)
            yield scrapy.Request(now_purl,callback=self.parse,dont_filter=True)

