# coding:utf-8
import random
import requests
import re
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import os


class WeichatSpider:
    """
    注意事项：
       因是登陆公众号抓取，速度不宜过快，容易被封号；
       不建议采用多进程多协程模式，同一个账号如果同一时间访问不同页面，不符合正常人访问网页的习惯。

    存在的问题：
       1.视频部分未进行处理；
       2.部分图片抓取失败；
       3.多余的广告内容以及链接过多，导致页面臃肿
       4.部分网页格式不一致，导致无法抓取。

    临时解决方案：
        可通过页面上的原文链接查看缺失的内容
    """

    def __init__(self, weichat_name):
        """初始化所需参数"""
        self.cookie = {}
        self.header = {
                       "HOST": "mp.weixin.qq.com",
                       "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ("
                                     "KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36 "
                      }
        self.token = None
        self.fakeid = None
        self.article_count = None
        self.weichat_name = weichat_name
        self.count = 0
        self.browser = webdriver.Chrome()
        self.host_url = r"https://mp.weixin.qq.com"
        self.search_url = r"https://mp.weixin.qq.com/cgi-bin/searchbiz?"
        self.appmsg_url = r"https://mp.weixin.qq.com/cgi-bin/appmsg?"

    def __del__(self):
        self.browser.close()

    def get_cookie(self):
        # 需换成获取网页的cookie
        """处理登陆的cookie文件"""
        with open(r"./cookie.txt", "r", encoding="utf-8") as f:
            cookie_content = f.read()
            split_content = cookie_content.split(";")
            for key_value in split_content:
                key, value = key_value.replace(" ", "").split("=", maxsplit=1)
                self.cookie[key] = value

    def get_token_fakeid(self):
        """获取登陆公众号的token值，目标公众号的唯一标志fakeid值"""

        response = requests.get(self.host_url, headers=self.header, cookies=self.cookie)
        # 获取登陆的微信公众号token值
        self.token = re.findall(r'token=(\d+)', str(response.url))[0]
        # 构造查询参数
        query_id = {
            "action": "search_biz",
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
            "random": random.random(),
            "query": self.weichat_name,
            "begin": 0,
            "count": 5
        }
        # 获取公众号的fakeid
        search_result = requests.get(self.search_url, headers=self.header, cookies=self.cookie, params=query_id)
        chat_list = search_result.json().get("list")[0]
        self.fakeid = chat_list.get("fakeid")

    def get_article_count(self):
        """获取公众号文章总数"""
        query_id_data = {
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
            "random": random.random(),
            "action": "list_ex",
            "query": self.weichat_name,
            "begin": 0,
            "count": 5,
            "fakeid": self.fakeid,
            "type": 9
        }

        appmsg_result = requests.get(self.appmsg_url, headers=self.header, cookies=self.cookie, params=query_id_data)
        json_result = appmsg_result.json()
        self.article_count = json_result.get("app_msg_cnt")

    def get_page_list(self):
        """获取每页文章列表"""
        for page in [pages for pages in range(self.article_count+1) if pages % 5 == 0]:
            # 构造每页参数
            query_id_data = {
                "token": self.token,
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
                "random": random.random(),
                "action": "list_ex",
                "query": self.weichat_name,
                "begin": page,
                "count": 5,
                "fakeid": self.fakeid,
                "type": 9
            }
            # 构造每页链接
            appmsg_result = requests.get(self.appmsg_url, headers=self.header,
                                         cookies=self.cookie, params=query_id_data)
            json_result = appmsg_result.json()
            # 获取每页列表
            article_list = json_result.get("app_msg_list")
            self.download_article(article_list)

    def save_article_link(self, link):
        """保存文章链接"""
        if not  os.path.exists("./%s" % self.weichat_name):
            os.mkdir("./%s" % self.weichat_name)
        link_path = "./%s/link.txt" % self.weichat_name
        with open(link_path, "a+") as f_link:
            f_link.write(link)
            f_link.write("\n")

    def download_img(self, p_children, f):
        """下载文章图片"""
        for p1 in p_children.items():
            img_link = p1.attr("data-src")
            if img_link:
                respone = requests.get(img_link)
                self.count += 1
                if not os.path.exists("./%s/images" % self.weichat_name):
                    os.mkdir("./%s/images" % self.weichat_name)
                images_path = "./%s/images/img%s.png" % (self.weichat_name, self.count)
                with open(images_path, "wb") as f_img:
                    time.sleep(random.randint(3, 5))
                    f_img.write(respone.content)
                    img_path = """<p style="text-align: center"><img style="margin: 0 auto;
                    " src="%s" _width="410px"/></p>""" % (
                            "./images/img%s.png" % self.count)
                    f.write(img_path)

    def download_article(self, article_list):
        for article in next(article_list):
            title = article.get("title")
            link = article.get("link")
            update_time = article.get("update_time")
            write_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(update_time))
            self.save_article_link(link)
            self.browser.get(link)
            time.sleep(random.randint(5, 10))
            # 获取网页源码
            html = self.browser.page_source
            if html:
                doc = pq(html)
                article_title = doc("#activity-name")
                # author = doc("#meta_content")
                article_content1 = doc("#js_content")
                p_list = article_content1.children()
                error_flag = False
                # 存在不规则符号时，无法创建文件，故需进一步处理
                try:
                    article_title_try = re.sub(r"[\\/|*?:<>\"]", "", article_title.text())
                    if not os.path.exists("./%s" % self.weichat_name):
                        os.mkdir("./%s" % self.weichat_name)
                    article_path = "./%s/%s.html" % (self.weichat_name, article_title_try)
                    with open( article_path, "w+", encoding="utf-8") as f:
                        pass
                except:
                    error_flag = True
                finally:
                    if error_flag:
                        num = random.randint(1, 1000)
                        while True:
                            if not os.path.exists("./%s/%s.html" % (self.weichat_name, num)):
                                break
                        article_title_try = "错误文件%d" % num
                    article_path = "./%s/%s.html" % (self.weichat_name,article_title_try)
                    with open(article_path, "w+", encoding="utf-8") as f:
                        f.write(str("<p>文章标题：%s</p>" % title))
                        f.write("\n")
                        f.write(str("<p>原文链接：%s</p>" % link))
                        f.write("\n")
                        f.write(str("<p>发布时间：%s</p>" % write_time))
                        f.write("\n")
                        for p in p_list.items():
                            if "<img" not in str(p):
                                f.write(str(p))
                                f.write("\n")
                            else:
                                p_children = p.children()
                                self.download_img(p_children, f)


def main():
    weichat_name = input("请输入公众号名称：")
    spider = WeichatSpider(weichat_name)
    spider.get_cookie()
    spider.get_token_fakeid()
    spider.get_article_count()
    spider.get_page_list()



if __name__ == '__main__':
    main()
