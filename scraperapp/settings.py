# -*- coding: utf-8 -*-

# Scrapy settings for scraperapp project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scraperapp'

SPIDER_MODULES = ['scraperapp.spiders']
NEWSPIDER_MODULE = 'scraperapp.spiders'

# Defaults for high performance
# See http://doc.scrapy.org/en/latest/topics/broad-crawls.html
LOG_LEVEL = "DEBUG"
DOWNLOAD_TIMEOUT = 15

# The maximum limit for Twisted Reactor thread pool size, default is 10
REACTOR_THREADPOOL_MAXSIZE = 20
# AJAXCRAWL_ENABLED = True

# An integer that is used to adjust the priority
# of a Request based on its depth.
DEPTH_PRIORITY = 0

# Whether the Retry middleware will be enabled, default is True
RETRY_ENABLED = True

# selenium middleware settings
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = '/usr/bin/chromedriver'
# SELENIUM_DRIVER_ARGUMENTS = \
# ['--headless', '--no-sandbox', '--ignore-certificate-errors']

# measuring latencies and throughput
LATENCIES_INTERVAL = 5
EXTENSIONS = {
    'scraperapp.extensions.Latencies': 500,
}

WEBSERVICE_PIPELINE_URL = '/api/v1/crawl/result'
SPLASH_URL = 'http://sps-web-splash:8050'

# Crawl responsibly
# by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scraperapp (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# a random high number
CONCURRENT_REQUESTS_PER_DOMAIN = 1000000
# set to zero to diable CONCURRENT_REQUESTS_PER_IP
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'scraperapp.middlewares.SeleniumSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# Low orders are closer to the engine,
# high orders are closer to the downloader.
DOWNLOADER_MIDDLEWARES = {
    # 'scraperapp.middlewares.SeleniumDownloaderMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scraperapp.extensions.Latencies': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scraperapp.pipelines.TidyUp': 300,
    'scrapy_redis.pipelines.RedisPipeline': 301,
    # 'scraperapp.pipelines.WebserviceWriter': 800,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# use if enabled HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
# DEPTH_LIMIT = 5


# SCRAPY REDIS CONFIG #
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_CLASS = 'scraperapp.utils.SplashAwareRFPDupeFilter'

# Default requests serializer is pickle, but it can be changed to any module
# with loads and dumps functions. Note that pickle is not compatible between
# python versions.
# Caveat: In python 3.x, the serializer must return strings keys and support
# bytes as values. Because of this reason the json or msgpack module will not
# work by default. In python 2.x there is no such issue and you can use
# 'json' or 'msgpack' as serializers.
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# Don't cleanup redis queues, allows to pause/resume crawls.
# SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# Alternative queues.
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# Max idle time to prevent the spider from
# being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at
# the first time (because the queue is empty).
# SCHEDULER_IDLE_BEFORE_CLOSE = 10

# Store scraped item in redis for post-processing.
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }

# The item pipeline serializes and stores the items in this redis key.
# REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
# REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
REDIS_URL = 'redis://:redispassword@redis-master.default.svc.cluster.local:6379'

# Custom redis client parameters (i.e.: socket timeout, etc.)
# REDIS_PARAMS  = {}
# Use custom redis client class.
# REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# If True, it uses redis' ``SPOP`` operation. You have to use the ``SADD``
# command to add URLs to the redis queue. This could be useful if you
# want to avoid duplicates in your start urls list and the order of
# processing does not matter.
# REDIS_START_URLS_AS_SET = False

# Default start urls key for RedisSpider and RedisCrawlSpider.
# REDIS_START_URLS_KEY = '%(name)s:start_urls'

# Use other encoding than utf-8 for redis.
# REDIS_ENCODING = 'latin1'
