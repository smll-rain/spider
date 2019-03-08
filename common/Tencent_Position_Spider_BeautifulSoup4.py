from bs4 import BeautifulSoup
import requests
from User_Agent_list import USER_AGENT_LIST
import random, re, csv
import time


class TencentPosition(object):
    """
    腾讯社招职位爬虫
    网页分析：
    https://hr.tencent.com/position.php?keywords=python&tid=0&lid=2218
    https://hr.tencent.com/position.php?keywords=python&tid=0&lid=2218&start=20#a
    keywords=python
    start=20:每页自增10
    存在的问题：因为采用一个列表存数据，如果数据量过大，中途被中断，会导致数据还未保存就丢失了
    如果采用每次保存的形式，会增加IO操作

    综合考虑：可没执行完1页就进行保存
    """

    def __init__(self):
        self.base_url = 'https://hr.tencent.com/position.php?'
        self.keywords = input('请输入职位关键字：')
        self.place = input('请输入城市：')
        self.start_page = int(input('请输入起始页码：'))
        self.end_page = int(input('请输入结束页码：'))
        self.page = 0
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": " gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.2.1193401785.1539267208; pgv_pvi=8207348736; _gcl_au=1.1.1094479715.1539267212; PHPSESSID=dpsb203mrf6k4s9bfg9nugpqc5; pgv_si=s2907344896",
            "Host": "hr.tencent.com",
            "Referer": "https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start=10",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(USER_AGENT_LIST)
        }
        self.data_list = []
        self.title_list = []
        self.title_write_count = 0
        self.city = {}

    def send_request(self, url=None, params=None):
        if not url:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            return response.content
        else:
            response = requests.get(url, headers=self.headers)
            return response.content

    def parse_response(self, response):
        soup = BeautifulSoup(response, 'lxml')
        titles = soup.find('tr', class_='h').find_all('td')
        datas = soup.find_all('tr', class_=re.compile('even|odd'))

        # 如果找不到数据，返回None
        if not datas:
            return None
        # 构建表题,只添加一次
        if not self.title_list:
            title_list = []
            for title in titles:
                title_list.append(title.string)
            title_list.append('链接')
            title_list.append('工作职责')
            title_list.append('工作要求')
            self.title_list.append(title_list)

        # 构建表内容
        for data in datas:
            # 获取行数据
            data_list = []
            data_td = data.find_all('td')
            data_td_a = data.find('a')
            data_list.append(data_td_a.string)
            data_list.append(data_td[1].string)
            data_list.append(data_td[2].string)
            data_list.append(data_td[3].string)
            data_list.append(data_td[4].string)
            # 获取链接
            detail_url = "https://hr.tencent.com/" + data_td_a['href']
            data_list.append(detail_url)

            # 详情页访问
            if data_td_a['href']:
                time.sleep(random.randint(1, 3))
                detail_data = self.send_request(url=detail_url)
                soup = BeautifulSoup(detail_data, 'lxml')
                ul = soup.find_all('ul', class_='squareli')
                data_list.append(ul[0])
                data_list.append(ul[1])

            # 去重
            if data_list not in self.data_list:
                self.data_list.append(data_list)
        return True

    def save_result(self):
        with open('腾讯社招_%s_职位信息.csv' % self.keywords, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 表题写入一次即可
            if self.title_write_count == 0:
                writer.writerows(self.title_list)
                self.title_write_count = 1
            writer.writerows(self.data_list)

    def set_city(self):
        if not self.city:
            response = requests.get('https://hr.tencent.com/position.php', headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')
            items = soup.find('div', id="additems").find_all('a')
            for item in items:
                # 城市名称
                city = item.string
                url = item.attrs.get('href')
                lid = re.findall(r'lid=(.*)', url)
                # 如果编号为空，或者编号不再字典里面，则对字典进行更新或添加
                if lid and lid not in self.city.values():
                    self.city[city] = lid[0]

    def main(self):
        # 发送请求前，先更新一下city字典
        self.set_city()
        for page in range(self.start_page, self.end_page + 1):
            query_params = {
                "keywords": self.keywords,
                "start": (page - 1) * 10,
                'lid': self.city.get(self.place)
            }

            # 设置访问时间间隔，以更接近浏览器的行为访问
            time.sleep(random.randint(1, 5))
            response = self.send_request(params=query_params)
            result = self.parse_response(response)
            # 如果获取的分析结果为空，则跳出循环
            if not result:
                print('抓取结束！')
                break
            print("[INFO]:正在抓取第%s页" % page)
            self.save_result()
            self.data_list = []


if __name__ == '__main__':
    spider = TencentPosition()
    spider.main()
