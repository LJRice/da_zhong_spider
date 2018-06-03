import scrapy

class UrlItem(scrapy.Item):
    # 获取列表
    url_list = scrapy.Field()
    # 商店名称
    shop_name=scrapy.Field()


class ShopItem(scrapy.Item):
    # 商店名称
    shop_name=scrapy.Field()
    # 评论数目
    comment_num=scrapy.Field()
    # 人均消费
    avg_pay=scrapy.Field()
    # 口味
    taste=scrapy.Field()
    # 环境
    environment=scrapy.Field()
    # 服务
    service=scrapy.Field()
    # 地址
    place=scrapy.Field()
    # 电话
    phone=scrapy.Field()
    # 商店分类
    shop_type = scrapy.Field()
    # 营业时间
    open_time = scrapy.Field()
    # 评论
    # comment=scrapy.Field()
    # 图片组
    # imglist=scrapy.Field()
    #图片存储地址
    # img_path=scrapy.Field()

class CommentItem (scrapy.Item):
    #商店名字
    shop_name=scrapy.Field()
    # 商店城市
    city=scrapy.Field()
    # 星级
    star=scrapy.Field()
    # 评论人
    author=scrapy.Field()
    # 评论人均
    avg_pay=scrapy.Field()
    # 口味
    taste=scrapy.Field()
    # 环境
    environment=scrapy.Field()
    # 服务
    service=scrapy.Field()
    # 评价内容
    comment=scrapy.Field()
    # 喜欢的菜
    like_dishes=scrapy.Field()
    # 图片
    img_url=scrapy.Field()
    # 评价日期
    date=scrapy.Field()
    # 相册
    album=scrapy.Field()
    #用户id
    user_id=scrapy.Field()