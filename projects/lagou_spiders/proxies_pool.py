from redis import StrictRedis
import requests

redis = StrictRedis(host='127.0.0.1', port=6379, db=3)
proxy = 'https://111.43.70.58:51547'
response = requests.get('https://www.baidu.com/', proxies={'https': proxy, 'http': proxy} )
# 采用列表模式存储，左进右出，即先进先出
if response.status_code == 200:
    # 左进 如果请求成功，则存入数据库
    redis.lpush('ippool', proxy)
# 右出
# get_proxy = redis.rpop('ippool')
# print(get_proxy.decode('utf-8'))