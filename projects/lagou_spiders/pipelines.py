# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo


class JobsSpidersPipeline(object):
    """连接mongodb数据库"""
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # 连接数据库
        client = pymongo.MongoClient(host, port)
        db = client[dbname]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
