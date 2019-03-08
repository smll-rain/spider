# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from ..items import SunshineHotlineItem
from urllib.parse import quote
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor


class HotlineRedisSpider(RedisCrawlSpider):
    name = 'hotline_redis'
    allowed_domains = ['sun0769.com']
    base_url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    # start_urls = [base_url + str(page)]
    redis_key = 'hotlineredisspider:start_urls'
    rules = [
        Rule(LinkExtractor(allow=r'"http://wz.sun0769.com/index.php/question/questionType?type=4')),
        Rule(LinkExtractor(allow=r"http://wz.sun0769.com/html/question/"), callback="parse_detail", follow=False)
    ]

    def parse(self, response):
        for link in response.xpath(r'//table//tr/td/a[@class="news14"]/@href'):
            print(link.extract())
            yield scrapy.Request(link.extract(),meta={'detail_url':link.extract()}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = SunshineHotlineItem()
        detail_url = response.meta.get('detail_url')
        item['detail_url'] = quote(detail_url,'utf-8')
        item["question"] = response.xpath('//div[@class="pagecenter p3"]//strong[@class="tgray14"]/text()').extract_first()
        item["detail"] = response.xpath('//div[@class="c1 text14_2"]/text()').extract_first()
        item["status"]= response.xpath('//div[@class="audit"]//span[@class="qgrn"]/text()').extract_first()
        item["asked_time"] = response.xpath('//div[@class="cright"]/p[@class="te12h"]/text()').extract_first()
        yield item
        # if not detail_url:
        #    return
