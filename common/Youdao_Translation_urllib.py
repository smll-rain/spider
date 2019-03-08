from urllib import request, parse
import time
import json
import hashlib


class YoudaoTranslation:
    """
    有道翻译器
    分析网页
    Request URL: http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
    Request Method: POST

    headers:

    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Content-Length: 218   # 变动值
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Cookie: OUTFOX_SEARCH_USER_ID_NCOO=837989913.345146; _ga=GA1.2.1695229506.1539162379; OUTFOX_SEARCH_USER_ID="-2066732723@10.168.11.12"; LAST_LOGIN=8982531; JSESSIONID=aaa09ubkBj74XgR0JkhCw; ___rl__test__cookies=1542013492853 # 改变 时间戳
    Host: fanyi.youdao.com
    Origin: http://fanyi.youdao.com
    Referer: http://fanyi.youdao.com/
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
    X-Requested-With: XMLHttpRequest

    form Data:
    i: 我们  # 查询内容
    from: AUTO
    to: AUTO
    smartresult: dict
    client: fanyideskweb
    salt: 1542013492859 # 改变 时间戳
    sign: 162ac327c77f8ddfed059e591f22a879
         75df60be8a514bdf443689588d51151f
         # 改变
    doctype: json
    version: 2.1
    keyfrom: fanyi.web
    action: FY_BY_CLICKBUTTION
    typoResult: false

    """

    def send_request(self, text):
        # API
        base_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

        t = int(time.time() * 1000)
        # 构造头部
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   # 'Accept-Encoding': 'gzip, deflate',  # 注释，以防编码出问题
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   'Content-Length': '218',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=837989913.345146; _ga=GA1.2.1695229506.1539162379; OUTFOX_SEARCH_USER_ID="-2066732723@10.168.11.12"; LAST_LOGIN=8982531; JSESSIONID=aaa09ubkBj74XgR0JkhCw; ___rl__test__cookies=%s' % t,
                   'Host': 'fanyi.youdao.com',
                   'Origin': 'http://fanyi.youdao.com',
                   'Referer': 'http://fanyi.youdao.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}
        # 构造时间戳和加密签证sign
        """
        return {salt: t, sign: n.md5("fanyideskweb" + e + t + "sr_3(QOHT)L2dx#uuGR@r")} 加密方法
        t是时间戳， e通过查找js文件，找不出是什么，只能靠猜了：比如说一般会用什么进行加密和解密
        假设e是翻译字段，通过加密后跟原来的签证左对比，如果一致，则说明假设成立
        salt: 1542016545138
        sign: fda3fa978cf3cc70115b8653acccf4db
        t = '1542016545138'
        e = '北京'
        md5 = hashlib.md5()
        strs = "fanyideskweb" + e + t + "sr_3(QOHT)L2dx#uuGR@r"
        md5.update(strs.encode('utf-8'))
        print(md5.hexdigest())
        加密结果与浏览器给出的一致，破解成功
        """
        md5 = hashlib.md5()
        strs = "fanyideskweb" + text + str(t) + "sr_3(QOHT)L2dx#uuGR@r"
        md5.update(strs.encode('utf-8'))
        sign = md5.hexdigest()

        # 构造发送数据
        form_dict = {
            'i': text,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': t,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'false',
        }

        # 查询参数转换为url编码
        form_data = parse.urlencode(form_dict)

        # 更新header的文本长度
        headers['Content-Length'] = len(form_data)
        # 构造响应对象
        request_obj = request.Request(base_url, data=form_data.encode(), headers=headers)

        response = request.urlopen(request_obj)

        html = response.read()

        json_data = json.loads(html)
        print(json_data['translateResult'][0][0]['tgt'])

    def main(self):
        while True:
            text = input("请输入翻译内容(支持任意语言，按0退出)：")
            if text == '0':
                break
            self.send_request(text)


if __name__ == '__main__':
    youdao = YoudaoTranslation()
    youdao.main()