import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from urllib import parse
import time
from gevent.pool import Pool
from gevent.monkey import patch_all
patch_all()


class LagouSpider(object):
    """
    Request URL: https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
    Request Method: POST

    headers

    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Content-Length: 61
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Cookie: _ga=GA1.2.648121662.1540282185; user_trace_token=20181023160944-0022c75c-d69b-11e8-80a4-5254005c3644; LGUID=20181023160944-0022cfc9-d69b-11e8-80a4-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221671bca9b041cb-06ec179635988e-8383268-921600-1671bca9b051118%22%2C%22%24device_id%22%3A%221671bca9b041cb-06ec179635988e-8383268-921600-1671bca9b051118%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAAADEAAFIC6E4129FB8076EFC8F35692CBEEC71DE; _gid=GA1.2.1284664483.1542984546; LGSID=20181123224909-ef040289-ef2e-11e8-b8fc-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D68bMzOTJ3ApCk4frw2uQmzvLF9dagZnHvRHUftA7M5zAGiMGLocxcO6NvsizBIbxi9vN5fRfnIFu_PNdjUriWa%26wd%3D%26eqid%3D8cc39abb0000eec8000000065bf81358; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4818572.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542359466,1542595150,1542640966,1542984546; X_HTTP_TOKEN=a46b992d41da9a42430b65613da78fbf; TG-TRACK-CODE=index_search; _gat=1; LGRID=20181123225012-150389f0-ef2f-11e8-b8fc-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542984610; SEARCH_ID=1c1cf164f7024f069869c48100924ac2
    Host: www.lagou.com
    Origin: https://www.lagou.com
    Referer: https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36
    X-Anit-Forge-Code: 0
    X-Anit-Forge-Token: None
    X-Requested-With: XMLHttpRequest

    Form Data
    first: true
    pn: 1
    kd: python数据分析

    results: 15条职位信息
    content[positionResult][result]

    """

    def __init__(self):
        self.base_url = r'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        # self.headers = {
        #     'Accept': 'application/json, text/javascript, */*; q=0.01',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'Connection': 'keep-alive',
        #     'Content-Length': '61',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'Cookie':parse.urlencode(self.get_cookies()),
        #     'Host': 'www.lagou.com',
        #     'Origin': 'https://www.lagou.com',
        #     'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        #     'User-Agent': random.choice(USER_AGENT_LIST),
        #     'X-Anit-Forge-Code': '0',
        #     'X-Anit-Forge-Token': 'None',
        #     'X-Requested-With': 'XMLHttpRequest'
        # }

        self.headers = {
            "Cookie": "user_trace_token=20171010163413-cb524ef6-ad95-11e7-85a7-525400f775ce; LGUID=20171010163413-cb52556e-ad95-11e7-85a7-525400f775ce; JSESSIONID=ABAAABAABEEAAJAA71D0768F83E77DA4F38A5772BDFF3E6; _gat=1; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUsjkuPdu00000PW4pNb00000LCecjM.THL0oUhY1x60UWY4rj0knj03rNqbusK15yDLnWfkuWN-nj0sn103rHm0IHdDPbmzPjI7fHn3f1m3PDnsnH9anDFArH6LrHm3PHcYf6K95gTqFhdWpyfqn101n1csPHnsPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HDLP1Rv%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26ie%3Dutf8%26f%3D8%26ch%3D2%26tn%3D98010089_dg%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rqlang%3Dcn%26oe%3Dutf8; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; _putrc=347EB76F858577F7; login=true; unick=%E6%9D%8E%E5%87%AF%E6%97%8B; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=63; TG-TRACK-CODE=index_search; _gid=GA1.2.1110077189.1507624453; _ga=GA1.2.1827851052.1507624453; LGSID=20171011082529-afc7b124-ae1a-11e7-87db-525400f775ce; LGRID=20171011082545-b94d70d5-ae1a-11e7-87db-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507444213,1507624453,1507625209,1507681531; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507681548; SEARCH_ID=e420ce4ae5a7496ca8acf3e7a5490dfc; index_location_city=%E5%8C%97%E4%BA%AC",
            "Host": "www.lagou.com",
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'}
        self.keywords = '数据分析师'
        self.start_page = int(input('请输入起始页码：'))
        self.end_page = int(input('请输入结束页码：'))
        self.page = 1
        self.jobs = {}
        # self.cookies = self.get_cookies()

    def get_cookies(self):
        url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%EF%BC%9F'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        cookies_dict = {}
        cookies = driver.get_cookies()
        driver.close()
        for item in cookies:
            cookies_dict[item["name"]] = item["value"]
        return cookies_dict

    def get_proxy(self):
        PROXY_POOL_URL = 'http://localhost:5555/random'
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def send_request(self, form_data):
        try:
            time.sleep(0.001)
            get_proxy = self.get_proxy()
            proxy = {'https': 'https://' + get_proxy, 'http': 'http://' + get_proxy}
            response = requests.post(self.base_url, data=form_data, headers=self.headers, proxies=proxy)
            if response.status_code == 200 and not response:
                return response.content
        except Exception as e:
            print('链接错误%s' % form_data)
            return None

    def parse_response(self, response):
        json_dict = json.loads(response.decode('utf-8'))
        jobs_list = json_dict.get('content').get('positionResult').get('result')
        for job in jobs_list:
            json_dict_job = {
                # 岗位信息
                'positionName': job.get('positionName'),
                'workYear': job.get('workYear'),
                'education': job.get('education'),
                'city': job.get('city'),
                'district': job.get('district'),
                'salary': job.get('salary'),
                'positionAdvantage': job.get('positionAdvantage'),
                'jobNature': job.get('jobNature'),
                'createTime': job.get('createTime'),
                # 公司信息
                'companyId': job.get('companyId'),
                'companyShortName': job.get('companyShortName'),
                'companyFullName': job.get('companyFullName'),
                'companySize': job.get('companySize'),
                'industryField': job.get('industryField')
            }
            key = '%s_%s_%s' % (job.get('companyShortName'), job.get('positionName'), job.get('companyId'))
            self.jobs[key] = json_dict_job
        self.save_result()

    def save_result(self):
        with open('拉勾网_{}_职位信息{}-{}页.json'.format(self.keywords, self.start_page, self.end_page), 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=4, separators=(',', ': '),ensure_ascii=False)

    def main(self):
        pool = Pool(10)
        for page in range(self.start_page, self.end_page + 1):
            self.page = page
            data = {
                "first": "false" if page > 1 else "true",
                "pn": self.page,
                "kd": self.keywords
            }

            # 更新请求头文字长度
            form_data = parse.urlencode(data)
            self.headers['Content-Length'] = str(len(form_data))
            pool.apply_async(self.send_request, (data,), callback=self.parse_response)
            time.sleep(1)
        # pool.join()

            
if __name__ == '__main__':
    spider = LagouSpider()
    spider.main()
