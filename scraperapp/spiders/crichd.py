# -*- coding: utf-8 -*-
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule

from bs4 import BeautifulSoup
from scraperapp.items import ScraperItem
from scraperapp.spiders.base_spider import BaseSpider
from scrapy_redis.utils import bytes_to_str
from scrapy_splash import SplashRequest

logger = logging.getLogger('BaseSpider')


class CrichdSpider(BaseSpider):
    name = 'crichd'
    allowed_domains = ['hd.crichd.com', 'crichd.com',
                       'pl.topperformance.xyz', 'watch.crichd.to']
    redis_key = 'crichd:start_urls'

    RAW_ASSET_XPATH = "//td[contains(text(), 'Game Name:')]/following-sibling::td[1]/h3/text()"
    RAW_CATEGORY_XPATH = "//td[contains(text(), 'Sports Name:')]/following-sibling::td[1]/text()"
    DATE_XPATH = "//td[contains(text(), 'Date:')]/following-sibling::td[1]/text()"
    START_TIME_XPATH = "//td[contains(text(), 'Start Time:')]/following-sibling::td[1]/text()"
    END_TIME_XPATH = "//td[contains(text(), 'End Time:')]/following-sibling::td[1]/text()"

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[child::h2[@class='gametitle']]"),
             callback='parse_item',
             process_request='use_splash',
             follow=True),
    )

    def use_splash(self, request, response):
        request = super().use_splash(request, response)
        request.meta.update(dont_redirect=True)
        return request

    def _extract_urls(self, html):
        soup = BeautifulSoup(html, 'lxml')
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return urls

    # extract items from response
    def parse_item(self, response):
        logger.debug("parsing {} to extract item".format(response.url))
        loader = ItemLoader(item=ScraperItem(), response=response)

        # capture viewing location url
        loader.add_value('viewing_location_url', response.url)

        # capture hosting site urls
        iframes = response.data['childFrames']
        urls = []
        for iframe in iframes:
            urls = [*urls, *self._extract_urls(iframe['html'])]
        loader.add_value('hosting_site_urls', urls)

        loader.add_xpath('raw_asset', self.RAW_ASSET_XPATH,
                         MapCompose(str.strip))
        loader.add_xpath('raw_category', self.RAW_CATEGORY_XPATH,
                         MapCompose(str.strip))

        loader.add_xpath('date', self.DATE_XPATH)
        loader.add_xpath('start_time', self.START_TIME_XPATH)
        loader.add_xpath('end_time', self.END_TIME_XPATH)

        logger.debug("item extracted for {}".format(response.url))
        return loader.load_item()
