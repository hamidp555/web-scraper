# -*- coding: utf-8 -*-
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule

from scraperapp.items import ScraperItem
from scraperapp.spiders.base_spider import BaseSpider

logger = logging.getLogger('streamsports')


class StreamSportsSpider(BaseSpider):
    name = 'streamsports'
    allowed_domains = ['streamsports.to']
    redis_key = 'streamsports:start_urls'

    EVENT_LINK_XPATH = \
        "//table[contains(@class,'ssports_table')]/tbody/tr/descendant::td[4]/descendant::a[1]"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=EVENT_LINK_XPATH),
             callback='parse_item',
             process_request='use_splash',
             follow=True),
    )

    def parse_item(self, response):
        logger.debug("parsing {} to extract item".format(response.url))
        loader = ItemLoader(item=ScraperItem(), response=response)

        # capture viewing location url
        loader.add_value('viewing_location_url', response.url)

        # capture hosting site urls
        iframes = response.data['childFrames']
        urls = []
        for iframe in iframes:
            urls.append(iframe['requestedUrl'])
        loader.add_value('hosting_site_urls', urls)
        loader.add_xpath('hosting_site_urls',
                    "//table[contains(@class, 'ssports_table')]//tr//a/@hre")

        info_loader = loader.nested_xpath(
            "//div[contains(@class, 'ssports_match_info')]")
        info_loader.add_xpath(
            'raw_asset', "div[@class='ssports_row']//h2/text()")
        info_loader.add_xpath(
            'raw_category', "ul[@class='ssports_list']/descendant::li[1]/span/a/text()")
        info_loader.add_xpath(
            'date', "ul[@class='ssports_list']/descendant::li[3]/span/text()")

        logger.debug("item extracted for {}".format(response.url))
        return loader.load_item()
