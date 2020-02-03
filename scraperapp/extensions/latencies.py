
from scrapy import signals
from scrapy.exceptions import NotConfigured
from twisted.internet import task
from time import time


class Latencies(object):

    def __init__(self, crawler):
        self.crawler = crawler

        self.interval = crawler.settings.getfloat('LATENCIES_INTERVAL')
        if not self.interval:
            raise NotConfigured

        cs = crawler.signals
        cs.connect(self._spider_opened, signal=signals.spider_opened)
        cs.connect(self._spider_closed, signal=signals.spider_closed)
        cs.connect(self._request_scheduled, signal=signals.request_scheduled)
        cs.connect(self._response_received, signal=signals.response_received)
        cs.connect(self._item_scraped, signal=signals.item_scraped)

        self.latency, self.proc_latency, self.items = 0, 0, 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # Sent when the engine schedules a Request, to be downloaded later.
    # The signal does not support returning deferreds from their handlers.
    def _request_scheduled(self, request, spider):
        request.meta['schedule_time'] = time()

    # Sent when the engine receives a new Response from the downloader.
    # This signal does not support returning deferreds from their handlers.
    def _response_received(self, response, request, spider):
        request.meta['received_time'] = time()

    # Sent when an item has been scraped, after it has passed all the Item Pipeline stages (without being dropped).
    # This signal supports returning deferreds from their handlers.
    def _item_scraped(self, item, response, spider):
        self.latency += time() - response.meta['schedule_time']
        self.proc_latency += time() - response.meta['received_time']
        self.items += 1

    # Sent after a spider has been closed
    # This signal supports returning deferreds from their handlers.
    def _spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        if self.task.running:
            self.task.stop()

    # Sent after a spider has been opened
    # This signal supports returning deferreds from their handlers.
    def _spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def _log(self, spider):
        irate = float(self.items) / self.interval
        latency = self.latency / self.items if self.items else 0
        proc_latency = self.proc_latency / self.items if self.items else 0
        spider.logger.info(("Scraped %d items at %.1f items/s, avg latency: "
                            "%.2f s and avg time in pipelines: %.2f s") %
                           (self.items, irate, latency, proc_latency))
        self.latency, self.proc_latency, self.items = 0, 0, 0
