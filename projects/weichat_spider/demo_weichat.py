# coding:utf-8
import random
import requests
import json
import re
from selenium import webdriver
# driver = webdriver.Chrome()
search_url = r"https://mp.weixin.qq.com"
# with open(r"./cookies.txt", "r", encoding="utf-8") as f:
#     cookie = f.read()
#     # cokie_data = json.loads(cookie)
# cookies = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
# # # driver.add_cookie(cookie_dict=cokie_data)
cookie = {'tvfe_boss_uuid':'ebd8135a0e4928af', 'pgv_pvid': '368276864', 'pt2gguin': 'o0455062086', 'RK': 'XVpQ1OZURZ', 'ptcz': '0a3eff87bf7380a4d943bd608dd0bd3ebbb1c995c366e730582bbeca2f218c2e', 'pgv_pvi': '672316416', 'ua_id': 'iJXbZg4WDFyGMgfgAAAAADFArn5-WzAq-qOEoSQH5Hc=', 'mm_lang': 'zh_CN', 'o_cookie': '455062086', 'pac_uid': '1_455062086', 'ptui_loginuin': '455062086', 'noticeLoginFlag': '1', 'pgv_si': 's947469312', 'cert': 'ecf9c7ixYubl5Vs1ZQBNjqXImpJMcrbv', 'rewardsn': '', 'wxtokenkey': '777', 'uuid': '7dfc28f09d21f73af32951274a6c7f4d', 'ticket': 'f880ab1aca5fa7878be3550cdc23e019d8cf8029', 'ticket_id': 'gh_556ba6ff3b4b', 'data_bizuin': '3241764313', 'bizuin': '3230764266', 'data_ticket': 'xPoXBN+TaXQp2Vd5WDfAh+1/g1Is0WoMyl1u/uh97x2FxL/A3dGsOSuoCPFtJzK7', 'slave_sid': 'NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS', 'slave_user': 'gh_556ba6ff3b4b', 'xid': '3796e457aa50a788b43eafcfa571c442', 'openid2ticket_o2WU5wRKzSN4gKCXMCnPH9JGqJbY': 'cHS3AapsZVNwwuQBvbveXEIxtTf6pXk3rbb6JaFLpiU='}
header ={
    "HOST":"mp.weixin.qq.com",
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36"
    }
response = requests.get(search_url, headers= header,cookies= cookie)
# lists = search_response.json()
print(response.url)
token=re.findall(r'token=(\d+)',str(response.url))[0]
print(token)
# 构造查询参数
query_id = {
    "action":"search_biz",
    "token": 1651176410,
    "lang": "zh_CN",
    "f": "json",
    "ajax": 1,
    "random": random.random(),
    "query": "Python小屋",
    "begin": 0,
    "count": 5
}
"""
选中公众号后的参数
General
Request URL: https://mp.weixin.qq.com/cgi-bin/appmsg?token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.19913288608123603&action=list_ex&begin=0&count=5&query=&fakeid=MzI4MzM2MDgyMQ%3D%3D&type=9
Request Method: GET
Status Code: 200 OK
Remote Address: 183.192.196.190:443
Referrer Policy: no-referrer-when-downgrade

Response Headers
HTTP/1.1 200 OK
Connection: keep-alive
Cache-Control: no-cache, must-revalidate
Content-Type: application/json; charset=UTF-8
LogicRet: 0
RetKey: 14
Strict-Transport-Security: max-age=15552000
Set-Cookie: slave_user=gh_556ba6ff3b4b; Path=/; Secure; HttpOnly
Set-Cookie: slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; Path=/; Secure; HttpOnly
Set-Cookie: bizuin=3230764266; Path=/; Secure; HttpOnly
Content-Encoding: gzip
Content-Length: 1817

Request Headers
GET /cgi-bin/appmsg?token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.19913288608123603&action=list_ex&begin=0&count=5&query=&fakeid=MzI4MzM2MDgyMQ%3D%3D&type=9 HTTP/1.1
Host: mp.weixin.qq.com
Connection: keep-alive
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36
Referer: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1651176410
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: tvfe_boss_uuid=ebd8135a0e4928af; pgv_pvid=368276864; pt2gguin=o0455062086; RK=XVpQ1OZURZ; ptcz=0a3eff87bf7380a4d943bd608dd0bd3ebbb1c995c366e730582bbeca2f218c2e; pgv_pvi=672316416; ua_id=iJXbZg4WDFyGMgfgAAAAADFArn5-WzAq-qOEoSQH5Hc=; mm_lang=zh_CN; o_cookie=455062086; pac_uid=1_455062086; ptui_loginuin=455062086; noticeLoginFlag=1; pgv_si=s947469312; cert=ecf9c7ixYubl5Vs1ZQBNjqXImpJMcrbv; rewardsn=; wxtokenkey=777; uuid=7dfc28f09d21f73af32951274a6c7f4d; ticket=f880ab1aca5fa7878be3550cdc23e019d8cf8029; ticket_id=gh_556ba6ff3b4b; data_bizuin=3241764313; bizuin=3230764266; data_ticket=xPoXBN+TaXQp2Vd5WDfAh+1/g1Is0WoMyl1u/uh97x2FxL/A3dGsOSuoCPFtJzK7; slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; slave_user=gh_556ba6ff3b4b; xid=3796e457aa50a788b43eafcfa571c442; openid2ticket_o2WU5wRKzSN4gKCXMCnPH9JGqJbY=cHS3AapsZVNwwuQBvbveXEIxtTf6pXk3rbb6JaFLpiU=

Query String Parameters
token: 1651176410 # 需要替换成登陆的公众号token
lang: zh_CN
f: json
ajax: 1
random: 0.19913288608123603
action: list_ex
begin: 0
count: 5
query: 
fakeid: MzI4MzM2MDgyMQ==   # 搜索的公众号
type: 9

token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.19913288608123603&action=list_ex&begin=0&count=5&query=&fakeid=MzI4MzM2MDgyMQ%3D%3D&type=9

"""

"""
搜索公众号时的各种参数 
General
Request URL: https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.2733288582875857&query=Python%E5%B0%8F%E5%B1%8B&begin=0&count=5
Request Method: GET
Status Code: 200 OK
Remote Address: 120.204.16.168:443
Referrer Policy: no-referrer-when-downgrade

Response Headers
HTTP/1.1 200 OK
Connection: keep-alive
Cache-Control: no-cache, must-revalidate
Content-Type: application/json; charset=UTF-8
LogicRet: 0
RetKey: 14
Strict-Transport-Security: max-age=15552000
Set-Cookie: slave_user=gh_556ba6ff3b4b; Path=/; Secure; HttpOnly
Set-Cookie: slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; Path=/; Secure; HttpOnly
Set-Cookie: bizuin=3230764266; Path=/; Secure; HttpOnly
Content-Encoding: gzip
Content-Length: 750

Request Headers
GET /cgi-bin/searchbiz?action=search_biz&token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.2733288582875857&query=Python%E5%B0%8F%E5%B1%8B&begin=0&count=5 HTTP/1.1
Host: mp.weixin.qq.com
Connection: keep-alive
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36
Referer: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1651176410
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: tvfe_boss_uuid=ebd8135a0e4928af; pgv_pvid=368276864; pt2gguin=o0455062086; RK=XVpQ1OZURZ; ptcz=0a3eff87bf7380a4d943bd608dd0bd3ebbb1c995c366e730582bbeca2f218c2e; pgv_pvi=672316416; ua_id=iJXbZg4WDFyGMgfgAAAAADFArn5-WzAq-qOEoSQH5Hc=; mm_lang=zh_CN; o_cookie=455062086; pac_uid=1_455062086; ptui_loginuin=455062086; noticeLoginFlag=1; pgv_si=s947469312; cert=ecf9c7ixYubl5Vs1ZQBNjqXImpJMcrbv; rewardsn=; wxtokenkey=777; uuid=7dfc28f09d21f73af32951274a6c7f4d; ticket=f880ab1aca5fa7878be3550cdc23e019d8cf8029; ticket_id=gh_556ba6ff3b4b; data_bizuin=3241764313; bizuin=3230764266; data_ticket=xPoXBN+TaXQp2Vd5WDfAh+1/g1Is0WoMyl1u/uh97x2FxL/A3dGsOSuoCPFtJzK7; slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; slave_user=gh_556ba6ff3b4b; xid=3796e457aa50a788b43eafcfa571c442; openid2ticket_o2WU5wRKzSN4gKCXMCnPH9JGqJbY=cHS3AapsZVNwwuQBvbveXEIxtTf6pXk3rbb6JaFLpiU=

Query String Parameters
action: search_biz
token: 1651176410
lang: zh_CN
f: json
ajax: 1
random: 0.2733288582875857
query: Python小屋
begin: 0
count: 5
action=search_biz&token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.2733288582875857&query=Python%E5%B0%8F%E5%B1%8B&begin=0&count=5
"""

"""
下一页的各种参数
General
Request URL: https://mp.weixin.qq.com/cgi-bin/appmsg?token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.9104650017668006&action=list_ex&begin=5&count=5&query=&fakeid=MzI4MzM2MDgyMQ%3D%3D&type=9
Request Method: GET
Status Code: 200 OK
Remote Address: 183.192.196.190:443
Referrer Policy: no-referrer-when-downgrade

Response Headers
HTTP/1.1 200 OK
Connection: keep-alive
Cache-Control: no-cache, must-revalidate
Content-Type: application/json; charset=UTF-8
LogicRet: 0
RetKey: 14
Strict-Transport-Security: max-age=15552000
Set-Cookie: slave_user=gh_556ba6ff3b4b; Path=/; Secure; HttpOnly
Set-Cookie: slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; Path=/; Secure; HttpOnly
Set-Cookie: bizuin=3230764266; Path=/; Secure; HttpOnly
Content-Encoding: gzip
Content-Length: 1772

Request Headers
GET /cgi-bin/appmsg?token=1651176410&lang=zh_CN&f=json&ajax=1&random=0.9104650017668006&action=list_ex&begin=5&count=5&query=&fakeid=MzI4MzM2MDgyMQ%3D%3D&type=9 HTTP/1.1
Host: mp.weixin.qq.com
Connection: keep-alive
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36
Referer: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1651176410
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: tvfe_boss_uuid=ebd8135a0e4928af; pgv_pvid=368276864; pt2gguin=o0455062086; RK=XVpQ1OZURZ; ptcz=0a3eff87bf7380a4d943bd608dd0bd3ebbb1c995c366e730582bbeca2f218c2e; pgv_pvi=672316416; ua_id=iJXbZg4WDFyGMgfgAAAAADFArn5-WzAq-qOEoSQH5Hc=; mm_lang=zh_CN; o_cookie=455062086; pac_uid=1_455062086; ptui_loginuin=455062086; noticeLoginFlag=1; pgv_si=s947469312; cert=ecf9c7ixYubl5Vs1ZQBNjqXImpJMcrbv; rewardsn=; wxtokenkey=777; uuid=7dfc28f09d21f73af32951274a6c7f4d; ticket=f880ab1aca5fa7878be3550cdc23e019d8cf8029; ticket_id=gh_556ba6ff3b4b; data_bizuin=3241764313; bizuin=3230764266; data_ticket=xPoXBN+TaXQp2Vd5WDfAh+1/g1Is0WoMyl1u/uh97x2FxL/A3dGsOSuoCPFtJzK7; slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; slave_user=gh_556ba6ff3b4b; xid=3796e457aa50a788b43eafcfa571c442; openid2ticket_o2WU5wRKzSN4gKCXMCnPH9JGqJbY=cHS3AapsZVNwwuQBvbveXEIxtTf6pXk3rbb6JaFLpiU=

Query String Parameters
token: 1651176410
lang: zh_CN
f: json
ajax: 1
random: 0.9104650017668006
action: list_ex
begin: 5
count: 5
query: 
fakeid: MzI4MzM2MDgyMQ==
type: 9

"""

"""
结论
公众号的token和fakeid具有唯一性
下一页改变的参数为begin

"""

"""
登陆时的各种参数
General
Request URL: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1651176410
Request Method: GET
Status Code: 200 OK
Remote Address: 183.192.196.190:443
Referrer Policy: no-referrer-when-downgrade

Response Headers
HTTP/1.1 200 OK
Connection: keep-alive
Cache-Control: no-cache, must-revalidate
Content-Security-Policy-Report-Only: default-src 'self'; script-src https: 'unsafe-inline' 'unsafe-eval' *.qq.com *.weishi.com; object-src 'self' *.qq.com; style-src 'unsafe-inline' res.wx.qq.com; img-src data: http://mmbiz.qlogo.cn http://mmbiz.qpic.cn http://*.qq.com https://mmbiz.qlogo.cn https://mmbiz.qpic.cn https://*.qq.com http://mp.weixin.qq.com https://mp.weixin.qq.com; media-src 'self' *.qq.com; font-src res.wx.qq.com; frame-src http://*.qq.com https://*.qq.com; report-uri https://mp.weixin.qq.com/mp/fereport?action=csp_report
Content-Type: text/html; charset=UTF-8
LogicRet: 0
RetKey: 14
Strict-Transport-Security: max-age=15552000
Set-Cookie: slave_user=gh_556ba6ff3b4b; Path=/; Secure; HttpOnly
Set-Cookie: slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; Path=/; Secure; HttpOnly
Set-Cookie: bizuin=3230764266; Path=/; Secure; HttpOnly
Content-Encoding: gzip
Content-Length: 70779

Request Headers
GET /cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1651176410 HTTP/1.1
Host: mp.weixin.qq.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: tvfe_boss_uuid=ebd8135a0e4928af; pgv_pvid=368276864; pt2gguin=o0455062086; RK=XVpQ1OZURZ; ptcz=0a3eff87bf7380a4d943bd608dd0bd3ebbb1c995c366e730582bbeca2f218c2e; pgv_pvi=672316416; ua_id=iJXbZg4WDFyGMgfgAAAAADFArn5-WzAq-qOEoSQH5Hc=; mm_lang=zh_CN; o_cookie=455062086; pac_uid=1_455062086; ptui_loginuin=455062086; noticeLoginFlag=1; pgv_si=s947469312; cert=ecf9c7ixYubl5Vs1ZQBNjqXImpJMcrbv; rewardsn=; wxtokenkey=777; uuid=7dfc28f09d21f73af32951274a6c7f4d; ticket=f880ab1aca5fa7878be3550cdc23e019d8cf8029; ticket_id=gh_556ba6ff3b4b; data_bizuin=3241764313; bizuin=3230764266; data_ticket=xPoXBN+TaXQp2Vd5WDfAh+1/g1Is0WoMyl1u/uh97x2FxL/A3dGsOSuoCPFtJzK7; slave_sid=NW9xOWV6TkNTU2Y4bUs0WjFNbUFDNHRPcXpPbG0yaDIyeWI1R19OYVpzMWZuenk2Z3Z2R0k1dFBBTEtsVzgxYUdoVnFFS0hTMHZaMDZnaTRWZnB4eE8wQWdHUmJWRnR4dWlLOV96aFNEVDlCUjEwNnA5a0VtRGtuTDd4UXpQUmFlQVUweFhKaEpPTWxoTGRS; slave_user=gh_556ba6ff3b4b; xid=3796e457aa50a788b43eafcfa571c442; openid2ticket_o2WU5wRKzSN4gKCXMCnPH9JGqJbY=cHS3AapsZVNwwuQBvbveXEIxtTf6pXk3rbb6JaFLpiU=

Query String Parammeters
t: media/appmsg_edit
action: edit
type: 10
isMul: 1
isNew: 1
lang: zh_CN
token: 1651176410 # 登陆的公众号标识
"""


"""
{"app_msg_cnt":576,"app_msg_list":[{"aid":"2247487318_1","appmsgid":2247487318,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/xXrickrc6JTMacpr8KPx9SmqLFkPUSBuW9MP2uNYI54tXYIREk3uRk8526Rk5xFVyvx7FTlYScHEh0bHRHMP6kQ/0?wx_fmt=jpeg","digest":"编写爬虫程序之前，一定要对目标网站进行充分分析，能够看懂HTML代码是必备的一项技能。","itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzI4MzM2MDgyMQ==&mid=2247487318&idx=1&sn=b5aacc32bdd3c03d3b002bd3ca854312&chksm=eb8aa40cdcfd2d1ad48e81adbaafdd1c07314d1ba053cf2acf0d16732e830b1a4ceb0941ea5c#rd","title":"Python爬虫基础：常用HTML标签和Javascript入门","update_time":1534727025},{"aid":"2247487315_1","appmsgid":2247487315,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/xXrickrc6JTMnAoj36k4ao5Bzs0d4FPbQFQKJ1CIXSsic5PR7xCyrHyQljRMt54GVBsEpmszkzUicTFhic6lxpBDQA/0?wx_fmt=jpeg","digest":"内含上期题目答案。","itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzI4MzM2MDgyMQ==&mid=2247487315&idx=1&sn=9f245b9aeab2884ed051df7266429328&chksm=eb8aa409dcfd2d1fc68a4e01ee8e6b2abb9cf075f75b1e0bd3a111ab886fb59c4ae798a7eb20#rd","title":"1000道Python题库系列分享13（22道填空题）","update_time":1534555867},{"aid":"2247487310_1","appmsgid":2247487310,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/xXrickrc6JTOClutNDFLVicibtAzHgwLMJ3QicdOX6SSFN4yQopSbicceDMdXDd6T5dPbdibzCnJkiazWibuaZgvZeeqfw/0?wx_fmt=jpeg","digest":"遥遥领先的兔子回头看了看慢慢爬行的乌龟，非常地骄傲，于是就睡了一觉，结果醒来时发行乌龟已经快到终点了，只好急忙追赶，但是为时已晚，最终比赛结果是乌龟先到达了终点。","itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzI4MzM2MDgyMQ==&mid=2247487310&idx=1&sn=00f0fa782aafbfb7d78ef358e251611c&chksm=eb8aa414dcfd2d0297b81898b4e9bd0b16c1a120db980ec831c396371ec63a5df509a701630c#rd","title":"Python使用matplotlib绘制龟兔赛跑中兔子和乌龟的行走轨迹","update_time":1534284108},{"aid":"2247487304_1","appmsgid":2247487304,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/xXrickrc6JTOClutNDFLVicibtAzHgwLMJ3ORKEeia43dBEXiajwRfJhj51dh0MvKpiaLDgicu9hmgpQhQ3RbH1dIWLlw/0?wx_fmt=jpeg","digest":"问题描述：已有Excel文件，其中包含5列数据，要求在第3列前插入一列数据。","itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzI4MzM2MDgyMQ==&mid=2247487304&idx=1&sn=92530332caf40fc0ee802d8a922784ff&chksm=eb8aa412dcfd2d041b19a20445dd7d3f3b31fa688627e1d04e325f30b4295afab6687b6aba08#rd","title":"Python操作Excel文件：插入一列数据","update_time":1534231809},{"aid":"2247487299_1","appmsgid":2247487299,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/xXrickrc6JTNPb4UupDtdoKcIIibxoaySrpLFNVmQLEic57iaZib0H9zjBe3nHzRG5DnQWKNZbLFibknsEdC4O9ib4gsA/0?wx_fmt=jpeg","digest":"技术要点：1）使用pandas读取Excel多WorkSheet中的数据；2）使用pandas函数merge()横向合并DataFrame；3）柱状图与热力图的绘制。","itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzI4MzM2MDgyMQ==&mid=2247487299&idx=1&sn=f69b6a8a4c72c77ae94739c4d3a639e5&chksm=eb8aa419dcfd2d0f6128ccec68bb4af98f1e51e9510b3ea1e9d3ddeeb7455c502f4121f6312c#rd","title":"Python使用pandas读取Excel文件多个WorkSheet的数据并绘制柱状图和热力图","update_time":1534079590}],"base_resp":{"err_msg":"ok","ret":0}}

"""