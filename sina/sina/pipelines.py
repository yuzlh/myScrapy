# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaPipeline(object):

    def process_item(self, item, spider):
        # 保存到txt文件中
        header = item['header']
        fileName = header + ".txt"
        if(fileName.endswith('.txt')):
            with open(item['subFilePath'] + '/' + fileName, 'a') as f:
                f.write(item['content'])

        return item
