import requests
from urllib import parse
from lxml import etree
from User_Agent_list import USER_AGENT_LIST
import random
import re
import json
from multiprocessing.dummy import Pool
import time

class DoubanSpider(object):
    """
    豆瓣电影排行榜
    方法：get
    返回数据：json
    url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100:90&action=&start=0&limit=20"
    type=11:电影类型编号
    interval_id=100:90  好于100%-90%的影片
    limit=20：每次限制查询20条数据
    start=0:从0开始查询，因为设置limit=20，即每页递增20
    https://movie.douban.com/j/chart/top_list?type=23&interval_id=90%3A80&action=&start=0&limit=20
    """

    def __init__(self):
        self.base_url = "https://movie.douban.com/j/chart/top_list?"
        self.type = {}
        self.film_list = []
        self.interval_id = input('请输入评价比(默认为100:90)：')
        self.limit = input('请输入每页数据最大条数(默认为20条)：')
        self.start = input('请输入从第几条数据开始(默认0)：')
        self.film_field = input('请输入电影类型(默认为爱情):')
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Cache-Control': 'max-age=0',
             'Connection': 'keep-alive',
             'Cookie': 'bid=QCzYuvAircU; douban-fav-remind=1; __utmz=30149280.1541491835.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="118282"; __yadk_uid=goG8DgcEotOvgLVkFpo62YJGQfenRmFh; _vwo_uuid_v2=DC409EDCFB3FD1246E5B6F8F39774E1E5|4e0afd21a1d0ded5b9a54535f2a5da57; __utmz=223695111.1541988512.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); gr_user_id=8f7c4822-c01e-41cd-9844-d02443148c9c; viewed="11614538_3354490_26857423_26880667_26836700"; ap_v=0,6.0; __utma=30149280.622363414.1540890569.1542114496.1543130795.6; __utma=223695111.915624189.1541988512.1541988512.1543130795.2; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1543132716%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=9be51f30c579227e.1541988471.3.1543134243.1543130846.',
             'Host': 'movie.douban.com',
             'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

    def send_request(self, url):
        print('[info]:正在抓取链接内容%s' % url)
        response = requests.get(url, headers= self.headers)
        return response.text

    def parse_response(self, response):
        file_list = json.loads(response)
        for film in file_list:
            fime_dict = {}
            fime_dict['title'] = film.get('title')
            fime_dict['rank'] = film.get('rank')
            fime_dict['score'] = film.get('score')
            fime_dict['release_date'] = film.get('release_date')
            fime_dict['vote_count'] = film.get('vote_count')
            fime_dict['actors'] = film.get('actors')
            fime_dict['types'] = film.get('types')
            fime_dict['regions'] = film.get('regions')
            fime_dict['actor_count'] = film.get('actor_count')
            fime_dict['rating'] = film.get('rating')
            fime_dict['cover_url'] = film.get('cover_url')
            fime_dict['url'] = film.get('url')
            self.film_list.append(fime_dict)
        with open("豆瓣电影排名_%s.json" % (self.film_field if self.film_field else '爱情'), 'w', encoding='utf-8') as f:
            json.dump(self.film_list, f, indent=4, separators=(',', ':'), ensure_ascii=False)


    def get_type(self):
        """获取电影类型对应的编号"""
        type_url = r'https://movie.douban.com/chart'
        response = requests.get(type_url, headers=self.headers)
        html = etree.HTML(response.content)
        types = html.xpath('//div[@class="types"]//a/@href')
        pattern = re.compile(r'.*type_name=(.*?)&type=(.*?)&')

        # 如果输入的电影类型存在，则返回编号
        for type_field in types:
            result = re.search(pattern, type_field)
            self.type[result.group(1)] = result.group(2)
        if self.film_field in self.type:
            return self.type[self.film_field]
        return self.type['爱情']

    def main(self):
        film_type = self.get_type()
        if not type:
            print('电影类型不存在')
            return
        start = int(self.start) if self.start else 0
        limit = int(self.limit) if self.start else 20
        pool = Pool()
        while True:
            query_data = {
                'type': film_type,
                'interval_id': self.interval_id if self.interval_id else '100:90',
                'action': '',
                'start': start,
                'limit': limit,
            }
            print(start)
            url = self.base_url + parse.urlencode(query_data)
            result = pool.apply_async(self.send_request, (url,), callback=self.parse_response)
            if len(result.get()) == 2:
                # 关闭线程池
                pool.close()
                # 让主线程等待所有子线程结束，主线程再退出
                pool.join()
                break

            start += 20
            time.sleep(1)


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main()
