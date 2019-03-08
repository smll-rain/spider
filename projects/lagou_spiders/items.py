# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    positionName = scrapy.Field()
    name = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    salary = scrapy.Field()
    positionAdvantage = scrapy.Field()
    jobNature = scrapy.Field()
    createTime = scrapy.Field()
    companyId = scrapy.Field()
    companyShortName = scrapy.Field()
    companyFullName = scrapy.Field()
    companySize = scrapy.Field()
    industryField = scrapy.Field()
