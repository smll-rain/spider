# coding=utf-8

import re
import requests
from User_Agent_list import USER_AGENT_LIST
import random


class NeihanSpider(object):
    """
    http: //www.neihan8.com/article/list_5_1 .html
    内涵段子抓取

    """
    def send_request(self, url, headers):
        response = requests.get(url, headers=headers)
        return response

    def parse_request(self, response):
        # 获取目标内容
        content = response.content.decode('gb18030')
        # 'gb2312' codec can't decode byte 0x84 in position 42485: illegal multibyte sequence 解决方法
        # 因为一些字符导致的解码失败，比如一些神奇的表情或者泰国文字
        # 使用一种范围更大的字符编码进行解码应该就可以了。
        # 根据谷歌结果得知使用gb18030即可，修改代码后成功解码无报错
        # 获取标题
        pattern = re.compile(r'<li class="piclist.*?<a.*?>(.*?)</a>.*?<div class="f18 mb20">(.*?)</div>', re.S)

        # pattern = re.compile(r'<div class="f18 mb20">(.*?)</div>', re.S)
        content_list = re.findall(pattern, content)
        return content_list

    def save_file(self, content, page):
        # 对每个目标内容进行格式化
        pattern_sub = re.compile(r'\u3000|&.*?;|\s|<p>', re.S)
        pattern_format = re.compile(r'<br/>|</p>', re.S)
        with open('neihanduanzi.txt', 'a', encoding='gbk') as f:
            f.write('\n')
            f.write('\n')
            f.write(("第%s页" % page).center(100, '='))
            f.write('\n')
            i = 1
            for title, text in content:
                re_text = re.sub(pattern_sub, '', text)
                format_text = re.sub(pattern_format, '\n', re_text, re.S)
                f.write('%s.'% i + re.sub(r'<.*?>','', title))
                f.write('\n')
                f.write(format_text)
                f.write('\n')
                i += 1


def main(start_page, end_page):
    spider = NeihanSpider()
    for page in range(start_page, end_page+1):
        url = r'https://www.neihan8.com/article/list_5_%s.html' % page
        headers = {
            "User-Agent": random.choice(USER_AGENT_LIST)
        }
        response = spider.send_request(url, headers)
        content = spider.parse_request(response)
        spider.save_file(content, page)


if __name__ == '__main__':
    main(11, 12)


