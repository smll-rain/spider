# coding:utf-8
import random
import requests
import re
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import os
search_url = r"https://mp.weixin.qq.com"
# 处理cookie
cookie ={}
with open(r"./cookie.txt", "r", encoding="utf-8") as f:
    cookie_content = f.read()
    split_content = cookie_content.split(";")
    for key_value in split_content:
        key, value = key_value.replace(" ", "").split("=", maxsplit=1)
        cookie[key] = value

header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36"
}
response = requests.get(search_url, headers=header, cookies=cookie)
# 获取登陆的微信公众号token值
token = re.findall(r'token=(\d+)', str(response.url))[0]

weichat_name = input("请输入查找的公众号名称：")
# 构造查询参数
query_id = {
    "action": "search_biz",
    "token": token,
    "lang": "zh_CN",
    "f": "json",
    "ajax": 1,
    "random": random.random(),
    "query": weichat_name,
    "begin": 0,
    "count": 5
}
# 查询链接
search_url = r"https://mp.weixin.qq.com/cgi-bin/searchbiz?"
search_result = requests.get(search_url, headers=header, cookies=cookie, params=query_id)
chat_list = search_result.json().get("list")[0]
fakeid = chat_list.get("fakeid")
query_id_data = {
    "token": token,
    "lang": "zh_CN",
    "f": "json",
    "ajax": 1,
    "random": random.random(),
    "action": "list_ex",
    "query": weichat_name,
    "begin": 0,
    "count": 5,
    "query": "",
    "fakeid": fakeid,
    "type": 9
}

appmsg_url = r"https://mp.weixin.qq.com/cgi-bin/appmsg?"
appmsg_result = requests.get(appmsg_url, headers=header, cookies=cookie, params=query_id_data)
json_result = appmsg_result.json()
article_count = json_result.get("app_msg_cnt")
article_list = json_result.get("app_msg_list")
for article in article_list:
    article.get("title")
    article.get("link")
    article.get("update_time")

# 翻页
browser = webdriver.Chrome()
count = 0
for page in [pages for pages in range(article_count+1) if pages % 5 ==0]:
    # 构造每页参数
    query_id_data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1,
        "random": random.random(),
        "action": "list_ex",
        "query": weichat_name,
        "begin": page,
        "count": 5,
        "query": "",
        "fakeid": fakeid,
        "type": 9
    }
    # 构造每页链接
    appmsg_result = requests.get(appmsg_url, headers=header, cookies=cookie, params=query_id_data)
    json_result = appmsg_result.json()
    # 获取每页列表
    article_list = json_result.get("app_msg_list")
    # 获取每页的文章标题、文件链接和更新时间
    for article in article_list:
        title = article.get("title")
        link = article.get("link")
        update_time = article.get("update_time")
        article_result = requests.get(link, headers=header, cookies=cookie)
        write_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(update_time))
        with open("./articles/link.txt", "a+") as f_link:
            f_link.write(link)
            f_link.write("\n")
        print(link)
        browser.get(link)
        time.sleep(random.randint(5, 10))
        # 获取网页源码
        html = browser.page_source
        if html:
            doc = pq(html)
            article_title = doc("#activity-name")
            author = doc("#meta_content")
            article_content1 = doc("#js_content")
            p_list = article_content1.children()
            error_flag = False
            try:
                article_title_try = article_title.text()
                with open("./articles/%s.html" % article_title_try, "w+", encoding="utf-8") as f:
                    pass
            except:
                error_flag = True
            finally:
                if error_flag:
                    num = random.randint(1, 1000)
                    while True:
                        if not os.path.exists("./article/%s.html" % num):
                            break
                    article_title_try = "错误文件%d" % num
                with open("./articles/%s.html" % article_title_try, "w+", encoding="utf-8") as f:
                    f.write(str("<p>文章标题：%s</p>" % title))
                    f.write("\n")
                    f.write(str("<p>原文链接：%s</p>" % link))
                    f.write("\n")
                    f.write(str("<p>发布时间：%s</p>" % write_time))
                    f.write("\n")
                    for p in p_list.items():
                        if p.attr("style"):
                            if "background-color" not in p.attr("style") or "rgb(51, 51, 51)" not in p.attr("style"):
                                if "<img" not in str(p):
                                    f.write(str(p))
                                    f.write("\n")
                                else:
                                    p_children = p.children()
                                    for p1 in p_children.items():
                                        img_link = p1.attr("data-src")
                                        if img_link:
                                            respone = requests.get(img_link)
                                            count += 1
                                            with open("./articles/images/img%s.png" % count, "wb") as f_img:
                                                time.sleep(random.randint(3,5))
                                                f_img.write(respone.content)
                                                img_path = """<p style="text-align: center"><img style="margin: 0 auto;" src="%s" _width="410px"/></p>""" % (
                                                            "./images/img%s.png" % count)
                                                f.write(img_path)
browser.close()



