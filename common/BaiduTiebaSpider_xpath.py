# -*- coding: utf-8 -*-
from lxml import etree
# 获取每页的url：//div[@class='threadlist_lz clearfix']/div/a/@href
import requests
from User_Agent_list import USER_AGENT_LIST
import random
import time


class BaiduTiebaSpider(object):
    """
    百度贴吧

    """

    def __init__(self):
        self.base_url = 'http://tieba.baidu.com/f?'
        self.kw = input('请输入贴吧主题：')
        self.start_page = int(input('请输入起始页：'))
        self.end_page = int(input('请输入结束页：'))
        self.headers = random.choice(USER_AGENT_LIST)
        self.detail_url_total_list = []

    def send_request(self, url, params=None):
        """只负责发送请求"""
        response = requests.get(url, params=params)
        return response

    def parse_page(self, response):
        """
        只负责详情页的分析
        楼层类：l_post j_l_post l_post_bright
        楼层作者类：d_author
        楼层图片类：d_post_content j_d_post_content  clearfix
             表情图标类：BDE_Smiley
             图片类：BDE_Image
        """
        html = etree.HTML(response.content)
        detail_url_list = html.xpath(r"//div[@class='threadlist_lz clearfix']/div/a/@href")
        if detail_url_list in self.detail_url_total_list:
            return True
        else:
            self.detail_url_total_list.append(detail_url_list)
        for detail_url in detail_url_list:
            url = 'http://tieba.baidu.com' + detail_url
            response = self.send_request(url)
            self.parse_image(response)

    def parse_image(self, response):
        """
        //img[@class="BDE_Image"]
        """
        html = response.content
        html = etree.HTML(html)
        image_url_list = html.xpath(r'//img[@class="BDE_Image"]/@src')
        for image_url in image_url_list:
            if not image_url:
                break
            filename = image_url[-44:]
            print("[info]正在请求图片链接：%s" % image_url)
            response = self.send_request(image_url)
            print("[info]正在保存图片：%s" % filename)
            self.save_page(response, filename)
            time.sleep(random.randint(1,5))

    def save_page(self, response, filename):
        with open('../dataset/baidu_tieba/%s' % filename, 'wb') as f:
            f.write(response.content)

    def main(self):
        # 获取每页贴吧所有吧友发帖的url
        for page in range(self.start_page, self.end_page):
            query_dict = {
                'kw': self.kw,
                'pn': (page-1) * 50
            }
            print("[info]正在抓取第%s页" % query_dict.get('pn'))
            response = self.send_request(self.base_url, params=query_dict)
            flag = self.parse_page(response)
            if flag:
                print('爬取结束')
                break


if __name__ == '__main__':
    spider = BaiduTiebaSpider()
    spider.main()
