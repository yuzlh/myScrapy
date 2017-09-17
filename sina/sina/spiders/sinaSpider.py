# -*- coding: utf-8 -*-
import scrapy
from sina.items import SinaItem

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaspiderSpider(scrapy.Spider):
    name = 'sinaSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []

        # 大类url和标题的匹配规则
        parentUrls = response.xpath(
            '//div[@id="tab01"]/div/h3/a/@href').extract()
        parentTitle = response.xpath(
            '//div[@id="tab01"]/div/h3/a/text()').extract()

        # 子类的url和标题的匹配规则
        subUrls = response.xpath(
            '//div[@id="tab01"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath(
            '//div[@id="tab01"]/div/ul/li/a/text()').extract()

        for i in range(len(parentUrls)):
            parentFilePath = "./Data/" + parentTitle[i]
            if(not os.path.exists(parentFilePath)):
                os.makedirs(parentFilePath)

            for j in range(len(subUrls)):
                item = SinaItem()

                # 保存大类的urls和title
                item['parentUrls'] = parentUrls[i]
                item['parentTitle'] = parentTitle[i]

                is_belong = subUrls[j].startswith(item['parentUrls'])
                if (is_belong):
                    subFilePath = parentFilePath + '/' + subTitle[j]
                    if (not os.path.exists(subFilePath)):
                        os.makedirs(subFilePath)

                item['subUrls'] = subUrls[j]
                item['subTitle'] = subTitle[j]
                item['subFilePath'] = subFilePath
                # print subFilePath

                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['subUrls'], meta={'meta_item': item}, callback = self.parse_item)

    # 根据子类返回的url发送请求
    def parse_item(self,response):
        meta_item = response.meta['meta_item']

        #获取子类里的所有链接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for x in range(0, len(sonUrls)):
            # is_belong = None
            # if((sonUrls[x].find('.shtml') or sonUrls[x].find('.html')) != -1):
                # is_belong = sonUrls[x].startswith(meta_item['parentUrls'])
                # print is_belong

            is_belong = (sonUrls[x].endswith('.shtml') or sonUrls[x].find('.html')) and sonUrls[x].startswith(meta_item['parentUrls'])
            if(is_belong):
                item = SinaItem()
                item['parentTitle'] = meta_item['parentTitle']
                item['parentUrls'] = meta_item['parentUrls']
                item['subUrls'] = meta_item['subUrls']
                item['subTitle'] = meta_item['subTitle']
                item['subFilePath'] = meta_item['subFilePath']
                item['sonUrls'] = sonUrls[x]
                items.append(item)
        for item in items:
            yield scrapy.Request(url = item['sonUrls'], meta = {'meta_item_detail': item}, callback = self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['meta_item_detail']

        content = ''
        header = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()
        contentList = response.xpath('//div[@id="artibody"]/p/text() | //div[@id="articleContent"]/p/text()').extract()

        for i in contentList:
            content += i
        if(len(header) != 0):
            item['header'] = header[0]
        item['content'] = content
        print header[0]

        yield item