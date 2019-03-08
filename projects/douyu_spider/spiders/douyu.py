# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import DouyuSpidersItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyu.com', 'rpic.douyucdn.cn']
    page = 1
    url = 'https://www.douyu.com/gapi/rkc/directory/1_8/'
    start_urls = [url + str(page)]

    def parse(self, response):
        datas = json.loads(response.body).get('data').get('rl')
        for data in datas:
            item = DouyuSpidersItem()
            item['name'] = data.get('nn')
            item['image_url'] = data.get('rs1')

            yield item

        self.page += 1
        if not datas:
            return
        yield scrapy.Request(self.url + str(self.page), callback=self.parse)
        # datas = json.loads(response).get('rl')
        # for data in datas:
        #     print(data)

