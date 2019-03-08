from urllib import request, parse
import time
import json


class TranslateSpider:
    """腾讯翻译器"""

    def send_request(self, text):
        """发送请求"""
        base_url = 'https://fanyi.qq.com/api/translate'

        # 构造请求头
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',  # 加入会导致编码解码错误
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '287',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'tvfe_boss_uuid=0b624c658acfa3db; pgv_pvid=7459925917; pgv_pvi=835309568; pt2gguin=o0455062086; RK=0cpQkMZ1H5; ptcz=d9c175405b4e716acb9e272913ab534c1ade6e00d9360ec9f21bd8164e7c7227; o_cookie=455062086; pac_uid=1_455062086; fy_guid=18fdd8bb-7231-4cd2-b784-7071ed3ecc62; ts_refer=www.baidu.com/link; ts_uid=7106458059; gr_user_id=79f3203e-8a85-4868-9182-3f104255dd06; grwng_uid=c5294e2e-b7c6-46ff-9f54-89b01e484b6e; qtv=7abda9def3b6732d; qtk=7E+s++9JwcFmOuuGy5QYe+bGrRnhluyMaGqMEd+tXlWVBCLIa3yX52CEC/0BTWCQRreVQcYCV6GsuVpSenGgSOVXCEFRUyFEBRlpAcuccGfO7VJjKRsJN8jlNKUgNETSA7kq/RcMvJcM4pIqFQ6P7g==; pgv_info=ssid=s4725150400; ts_last=fanyi.qq.com/; openCount=1; 9c118ce09a6fa3f4_gr_session_id=0b7f8a04-1da6-4d53-a3b8-0d710464f643; 9c118ce09a6fa3f4_gr_session_id_0b7f8a04-1da6-4d53-a3b8-0d710464f643=true',
            'Host': 'fanyi.qq.com',
            'Origin': 'https://fanyi.qq.com',
            'Referer': 'https://fanyi.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 构造时间戳
        t = int(time.time()*1000)

        # 构造发送数据
        # 发送的字符串，需要多查几次，找到规律：哪些是不变的，哪些是变化的
        form_dict = {'source': 'auto',
                     'target': 'en',
                     'sourceText': text,
                     'qtv': '7abda9def3b6732d',
                     'qtk': '7E+s++9JwcFmOuuGy5QYe+bGrRnhluyMaGqMEd+tXlWVBCLIa3yX52CEC/0BTWCQRreVQcYCV6GsuVpSenGgSOVXCEFRUyFEBRlpAcuccGfO7VJjKRsJN8jlNKUgNETSA7kq/RcMvJcM4pIqFQ6P7g==',
                     'sessionUuid': 'translate_uuid{}'.format(t)
                     }
        # 转换成url编码
        form_data = parse.urlencode(form_dict)

        # 更新文本长度
        headers['Content-Length'] = len(form_data)

        # 构造request对象
        request_obj = request.Request(base_url, data=form_data.encode(), headers=headers)
        response = request.urlopen(request_obj)

        # 响应格式处理
        html = response.read()
        json_data = json.loads(html)
        print(json_data['translate']['records'][0]['targetText'])

    def main(self):
        while True:
            text = input("请输入翻译的文字(支持任何语言,按0退出)：")
            if text == '0':
                break
            self.send_request(text)


if __name__ == '__main__':
    translate = TranslateSpider()
    translate.main()


