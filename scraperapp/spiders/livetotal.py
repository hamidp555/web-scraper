# -*- coding: utf-8 -*-
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule

from scraperapp.items import ScraperItem
from scraperapp.spiders.base_spider import BaseSpider

logger = logging.getLogger('livetotal')


class LiveTotalSpider(BaseSpider):
    name = 'livetotal'
    allowed_domains = ['livetotal.net', 'livetotal.tv']
    redis_key = 'livetotal:start_urls'

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'panel-group')]/div//a"),
             callback='parse_item',
             process_request='use_splash',
             follow=True),
    )

    def use_splash(self, request, response):
        request = super().use_splash(request, response)
        request.meta.update(dont_redirect=True)
        return request

    def parse_item(self, response):
        loader = ItemLoader(item=ScraperItem(), response=response)

        # capture viewing location url
        loader.add_value('viewing_location_url', response.url)

        # capture hosting site urls
        iframes = response.data['childFrames']
        urls = []
        for iframe in iframes:
            urls.append(iframe['requestedUrl'])
        loader.add_value('hosting_site_urls', urls)
        loader.add_xpath('raw_asset', "//h1")

        logger.debug("item extracted for {}".format(response.url))
        return loader.load_item()
