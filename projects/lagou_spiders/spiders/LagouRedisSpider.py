# -*- coding: utf-8 -*-
import json
from http.cookiejar import CookieJar
from urllib import parse
import uuid
from urllib.request import HTTPCookieProcessor, build_opener

from scrapy_redis.spiders import RedisSpider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..items import JobsSpidersItem
from scrapy.conf import settings
from ..User_Agent_list import random_user_agent


import requests


def get_cookies():
    url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%EF%BC%9F'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    cookies_dict = {}
    cookies = driver.get_cookies()
    for item in cookies:
        cookies_dict[item["name"]] = item["value"]
    return cookies_dict


class LagouRedisSpider(RedisSpider):
    name = 'LagouRedisSpider'
    allowed_domains = ['lagou.com']
    redis_key = 'lagouredisspider:start_urls'
    base_url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    keywords = '数据分析'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '61',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        "User-Agent": random_user_agent()
    }

    # 使用无界面浏览器获取cookies，默认cookies
    cookies = get_cookies()
    # if not cookies:
    #     cookies = {
    #         'JSESSIONID': uuid.uuid4(),
    #         'user_trace_token': uuid.uuid4()}
    page = 10

    def parse(self, response):
        for page in range(self.page+1):
            print('page：%s' % page)
            data = {
                "first": 'false' if self.page >1 else 'true',
                "pn": str(page),
                "kd": self.keywords
            }
            self.headers['Content-Length'] = str(len(parse.urlencode(data)))
            yield scrapy.FormRequest(self.base_url, formdata=data, meta={'data':data}, callback=self.parse, cookies=self.cookies, headers=self.headers)

        json_dict = json.loads(response.text)
        print(response.meta['data'])
        if not json_dict:
            return
        jobs_list = json_dict.get('content').get('positionResult').get('result')

        for job in jobs_list:
            item = JobsSpidersItem()
            # 岗位信息
            item['positionName'] = job.get('positionName')
            item['workYear'] = job.get('workYear')
            item['education'] = job.get('education')
            item['city'] = job.get('city')
            item['district'] = job.get('district')
            item['salary'] = job.get('salary')
            item['positionAdvantage'] = job.get('positionAdvantage')
            item['jobNature'] = job.get('jobNature')
            item['createTime'] = job.get('createTime')
            # 公司信息
            item['companyId'] = job.get('companyId')
            item['companyShortName'] = job.get('companyShortName')
            item['companyFullName'] = job.get('companyFullName')
            item['companySize'] = job.get('companySize')
            item['industryField'] = job.get('industryField')
            yield item

