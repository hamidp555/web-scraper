import logging

from scrapy_redis import defaults
from scrapy_redis.spiders import RedisCrawlSpider

logger = logging.getLogger('basespider')


class BaseSpider(RedisCrawlSpider):

    # a callable which will be called for every Request extracted by rules
    def use_splash(self, request, response):
        logger.debug('adding splash meta')
        request.meta.update(
            splash={
                'endpoint': 'render.json',
                'magic_response': True,
                'args': {
                    'wait': 0.1,
                    'html': 1,
                    'iframes': 1,
                },
            }
        )
        return request

    def next_requests(self):
        """
        Returns a request to be scheduled or none.
        or close the spider if there is no request in redis qeueu
        '"""
        use_set = self.settings.getbool(
            'REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'",
                              found, self.redis_key)
        else:
            self.crawler.engine.close_spider(
                spider=self, reason='queue is empty, the spider close')
