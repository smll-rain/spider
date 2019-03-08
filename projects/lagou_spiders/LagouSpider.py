# -*- coding: UTF-8 -*-
import json
import requests
import time
from gevent.pool import Pool
from gevent.monkey import patch_all
import csv
from lxml import etree

patch_all()


class LagouSpider(object):
    def __init__(self):
        self.headers = {
            "Cookie": "_ga=GA1.2.648121662.1540282185; user_trace_token=20181023160944-0022c75c-d69b-11e8-80a4-5254005c3644; LGUID=20181023160944-0022cfc9-d69b-11e8-80a4-5254005c3644; JSESSIONID=ABAAABAAAIAACBI840BBC34E8DCDC8991AE72E1535D51B6; _gid=GA1.2.1541069417.1543887253; index_location_city=%E6%B7%B1%E5%9C%B3; WEBTJ-ID=20181204100339-16776f4e1dc2c9-0218dfb99f0d35-6313363-921600-16776f4e1dd87e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221671bca9b041cb-06ec179635988e-8383268-921600-1671bca9b051118%22%2C%22%24device_id%22%3A%221671bca9b041cb-06ec179635988e-8383268-921600-1671bca9b051118%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543890249,1543890455,1543890469,1543897512; LGSID=20181204122513-9840213d-f77c-11e8-89ec-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DX8L1TN0bMABXUKkV3mkPkrx_490wfElRATQ-STo84nOEeh1BZelA73c-GYdOimostIb1DQXlNhoxU7_nsXxMYa%26wd%3D%26eqid%3De3bdea1700004ac2000000065c060187; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2798853.html; TG-TRACK-CODE=index_search; SEARCH_ID=6573bb783bf4475fb233e702eb66381a; LGRID=20181204122530-a268aa6c-f77c-11e8-8cb7-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543897530",
            "Host": "www.lagou.com",
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'}
        self.post_data = {'first': 'false', 'kd': 'Python数据分析'}  # 这是请求网址的一些参数
        self.t = time.strftime('%Y%m%d %H_%M_%S', time.localtime(time.time()))
        self.writer = csv.writer(
            open('职位信息_%s_拉勾网_%s.csv' % (self.post_data.get('kd'), self.t), 'w', encoding='utf-8', newline=''))
        self.flag = False
        self.detail_url = "https://www.lagou.com/jobs/"

    def get_proxy(self):
        """随机获取代理IP"""
        PROXY_POOL_URL = 'http://localhost:5555/random'
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def send_requests(self, url, page):
        proxy = self.get_proxy()
        if page > 1:
            self.post_data['first'] = 'true'
        proxies = {'htts': 'https://' + proxy, 'htt': 'http://' + proxy}
        requests.packages.urllib3.disable_warnings()
        try:
            response = requests.post(url + str(page), data=self.post_data, headers=self.headers, verify=False,
                                     proxies=proxies)
            clientIp = json.loads(response.text).get('clientIp')
            while clientIp:
                time.sleep(0.001)
                response = self.send_requests(url, page)
                pagesize = json.loads(response.content.decode('utf-8')).get('content').get('pageSize')
                if pagesize:
                    break
            pageNo = json.loads(response.content).get('content').get('pageNo')
            if str(pageNo) == "0":
                self.flag = True
            print('[Info]正在爬取第%s页' % page)
            print(response.content)
            return response
        except Exception as e:
            print(e)
            self.send_requests(url, page)

    def get_response(self, response):
        content_next = json.loads(response.content)
        company_info = content_next.get('content').get('positionResult').get('result')
        positions_list = []
        if company_info:
            # 构造文本信息，一条职位一条信息
            for p in company_info:
                position_list = [p['createTime'], p['city'], p['district'], p['companyFullName'], p['companyId'],
                                 p['companyLabelList'], p['companyShortName'], p['companySize'], p['industryField'],
                                 p['businessZones'],
                                 p['financeStage'], p['industryField'], p['firstType'], p['positionName'],
                                 p['positionId'],
                                 p['positionLables'], p['salary'], p['workYear'], p['education'],
                                 p['positionAdvantage'],
                                 p['secondType'], p['thirdType']]
                positions_list.append(position_list)
            self.save_data(positions_list)

    def save_data(self, data):
        # 存为csv格式
        self.writer.writerows(data)

    def get_pagesize(self, response):
        content = json.loads(response.text)  # loads()暂时可以理解为把json格式转为字典格式，而dumps()则是相反的
        pagesize = content.get('content').get('pageSize')  # 获取页面总数
        return pagesize

    def main(self):
        # 创建协程
        pool = Pool(10)

        # 构造表头，并写入文件
        title = ['createTime', 'city', 'district', 'companyFullName', 'companyId',
                 'companyLabelList', 'companyShortName', 'companySize', 'industryField', 'businessZones',
                 'financeStage', 'industryField', 'firstType', 'positionName', 'positionId', 'positionLables',
                 'salary', 'workYear', 'education', 'positionAdvantage', 'secondType', 'thirdType']

        self.writer.writerow(title)

        # 设置爬取的热门城市
        cityList = [u'深圳', u'广州', u'北京', u'上海', u'杭州', u'成都', u'南京', u'武汉', u'西安', u'厦门', u'长沙', u'苏州', u'天津',
                    u'郑州']
        for city in cityList:
            print('爬取%s' % city)

            # 获取页面总页数
            url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false&pn='.format(
                city)
            total_count = None
            while not total_count:
                response = pool.apply_async(self.send_requests, (url, 1)).get()
                time.sleep(1)
                total_count = json.loads(response.content).get('content').get('positionResult').get('totalCount')
                if total_count:
                    break
            total_count = int(float(total_count) / 15) + 2  # 取整时需加1，range边界需再加1，如条数19，取整后为1
            print('总页数%s' % total_count)
            for page in range(1, total_count):
                # 判断当前页面的页码项是否为0，即是否无职位信息

                if self.flag:
                    self.flag = False
                    break
                # 异步非阻塞多协程处理
                pool.apply_async(self.send_requests, (url, page), callback=self.get_response)
                time.sleep(1)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.main()
    print('爬取结束！')
