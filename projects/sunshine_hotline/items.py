# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SunshineHotlineItem(scrapy.Item):
    # define the fields for your item here like:
    question = scrapy.Field()
    detail = scrapy.Field()
    status = scrapy.Field()
    asked_time = scrapy.Field()
    detail_url = scrapy.Field()
