from scrapy.exceptions import DropItem
import pymysql

class ShopPipeline(object):
    def __init__(self):
        # 连接数据库
        self.conn=pymysql.connect(host="localhost",user="root",passwd="26651",charset='utf8mb4')
        self.conn.query("create database if not exists da_zhong ")
        self.conn.query("use da_zhong")

    # 处理数据
    def process_item(self,item, spider):
        if spider.name=="Myspider":
            self.conn.query("create table if not exists url_list (shop_name varchar(100) not null,url varchar(200),spider_date date,comment_nowpage varchar(100),primary key(shop_name))")
            key=item['shop_name']
            # for key in item['url_list'].keys():
            cursor = self.conn.cursor()
            cursor.execute("insert into url_list (shop_name,url,comment_nowpage) values('"+key+"','"+item['url_list'][key]+"','/p1');")
            cursor.close()
            self.conn.commit()
        if spider.name=="ShopSpider":
            self.conn.query("create table if not exists shop_data (shop_name varchar(100) not null,comment_num varchar(100),avg_pay varchar(100),taste varchar(100),environment varchar(100),service varchar(100),place varchar(100),phone varchar(100),shop_type varchar(100),open_time varchar(100),primary key(shop_name))")
            cursor = self.conn.cursor()
            # insert into shop_data values(   ,   ,  )
            cursor.execute('insert into shop_data values(\''+item['shop_name']+'\',\''+item['comment_num']+'\',\''+item['avg_pay']+'\',\''+item['taste']+'\',\''+item['environment']+'\',\''+item['service']+'\',\''+item['place']+'\',\''+item['phone']+'\',\''+item['shop_type']+'\',\''+item['open_time']+'\')')
            cursor.close()
            self.conn.commit()
        if spider.name=="CommentSpider":
            # comment="".join(str(item['comment']).split())
            # print(comment)
            self.conn.query("create table if not exists comment(shop_name varchar(100) not null,author varchar(100) not null,avg_pay varchar(100),taste varchar(100),environment varchar(100),service varchar(100),comment varchar(3000),like_dishes varchar(300),date varchar(100),img_url varchar(1000),city varchar(100),star varchar(10),primary key(author,shop_name,city))")
            cursor=self.conn.cursor()
            cursor.execute('insert into comment values("'+item['shop_name']+'","'+item['author']+'","'+item['avg_pay']+'","'+item['taste']+'","'+item['environment']+'","'+item['service']+'","'+item['comment']+'","'+item['like_dishes']+'","'+item['date']+'","'+str(item['album'])+'","'+item['city']+'","'+item['star']+'");')
            cursor.close()
            self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.close()