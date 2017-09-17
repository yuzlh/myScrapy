# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaItem(scrapy.Item):
    # 大类的标题 和 url
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    # 子类的标题 和 子url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    # 子类目录存储路径
    subFilePath = scrapy.Field()

    # 子类下的子链接
    sonUrls = scrapy.Field()

    # 文章标题和内容
    header = scrapy.Field()
    content = scrapy.Field()
