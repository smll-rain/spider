# -*- coding: utf-8 -*-
import random
# Scrapy settings for lagou_spiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from .User_Agent_list import random_user_agent

BOT_NAME = 'lagou_spiders'

SPIDER_MODULES = ['lagou_spiders.spiders']
NEWSPIDER_MODULE = 'lagou_spiders.spiders'

USER_AGENT = random_user_agent()
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lagou_spiders (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 1(重要). 使用了scrapy_redis的去重组件，在redis数据库里做去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2(重要). 使用了scrapy_redis的调度器，在redis里分配请求
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 3(重要). 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True
# 4(重要). 通过配置RedisPipeline将item写入key为 spider.name : items 的redis的list中，供后面的分布式处理item
# 这个已经由 scrapy-redis 实现，不需要我们写代码，直接使用即可
ITEM_PIPELINES = {
    # 'lagou_spiders.pipelines.JobsSpidersPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400
}
# 5(重要). 指定redis数据库的连接参数
# # REDIS_HOST = '47.107.112.222'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 1
}
# 等价于 REDIS_URL = 'redis://127.0.0.1:6379/1'
# mongodb数据库配置
# MONGODB 主机环回地址127.0.0.1
# MONGODB_HOST = '127.0.0.1'
# # 端口号，默认是27017
# MONGODB_PORT = 27017
# # 设置数据库名称
# MONGODB_DBNAME = 'lagou'
# # 存放本次数据的表名称
# MONGODB_DOCNAME = 'lagou_position'
# # 6.如果不启用则按scrapy默认的策略(优先级)
# #  -1. 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式。
# # SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# #  -2. 可选的 按先进先出排序（FIFO）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
#  -3. 可选的 按后进先出排序（LIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.randint(1, 3)
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lagou_spiders.middlewares.JobsSpidersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'lagou_spiders.middlewares.JobsSpidersDownloaderMiddleware': 543,
    # 'lagou_spiders.middlewares.MyUserAgentMiddleware': 400,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'lagou_spiders.pipelines.JobsSpidersPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
