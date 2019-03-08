# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from gevent import monkey
from gevent.pool import Pool
from ..items import AqiSpidersItem
import time
import requests
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def get_url():
    urls = []
    response = requests.get('https://www.aqistudy.cn/historydata/')
    html = etree.HTML(response.content)
    # 获得城市链接
    city_links = html.xpath(r'//div[@class="all"]//a/@href')

    # 构造每个城市完整的链接
    city_links = ['https://www.aqistudy.cn/historydata/' + link for link in city_links]

    # 获取某个城市每月的完整链接
    for link in city_links:
        month_repsonse = requests.get(link)
        html = etree.HTML(month_repsonse.content)
        city_month_links = html.xpath(r'//tbody/tr/td/a/@href')
        city_month_links = ['https://www.aqistudy.cn/historydata/' + link for link in city_month_links]
        urls.append(city_month_links)
    print(urls)
    return urls


class AqistudySpider(CrawlSpider):
    name = 'aqistudy'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']
    page = LinkExtractor(allow=('monthdata.php?city=.*?'))
    rules = [Rule(page, callback='parse_data', follow=True)]

    def parse_data(self, response):
        print(self.page)
        html = etree.HTML(response.body)
        data_tr = html.xpath(r'//tbody/tr')
        for tr in data_tr:
            item = AqiSpidersItem()
            item['date'] = tr.xpath(r'//td[1]//text()')
            item['AQI'] = tr.xpath(r'//td[2]//text()')
            item['level'] = tr.xpath(r'//td[3]//text()')
            item['PM_2_5'] = tr.xpath(r'//td[4]//text()')
            item['PM_10'] = tr.xpath(r'//td[5]//text()')
            item['SO2'] = tr.xpath(r'//td[6]//text()')
            item['CO'] = tr.xpath(r'//td[7]//text()')
            item['NO2'] = tr.xpath(r'//td[8]//text()')
            item['O3_8h'] = tr.xpath(r'//td[9]//text()')
            print(item)
            yield item






