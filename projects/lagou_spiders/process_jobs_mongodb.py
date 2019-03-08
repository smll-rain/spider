# -*- coding: utf-8 -*-

import json
import redis
import pymongo


def main():
    # 指定Redis数据库信息
    rediscli = redis.Redis(host='127.0.0.1', port=6379, db=1)
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='127.0.0.1', port=27017)

    # 创建数据库名
    db = mongocli['jobs']
    # 创建表名
    sheet = db['lagou_data']

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["LagouSpider:items"])

        item = json.loads(data)
        sheet.insert(item)

        try:
            print(u"Processing: %(name)s <%(link)s>" % item)
        except KeyError:
            print (u"Error procesing: %r" % item)


if __name__ == '__main__':
    main()