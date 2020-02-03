import treq
import json

from scrapy.exceptions import NotConfigured
from twisted.internet import defer


class WebserviceWriter(object):

    def __init__(self, crawler):
        webservice_url = crawler.settings.get('WEBSERVICE_PIPELINE_URL', None)
        if not webservice_url:
            raise NotConfigured
        self.webservice_url = webservice_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """
        Pipeline's main method. Uses inlineCallbacks to do
        asynchronous REST requests
        """
        try:
            # Create a json representation of this item
            data = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")
            yield treq.post(self.webservice_url, data, timeout=5)
        finally:
            defer.returnValue(item)
