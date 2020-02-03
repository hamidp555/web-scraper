# -*- coding: utf-8 -*-
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule

from scraperapp.items import ScraperItem
from scraperapp.spiders.base_spider import BaseSpider

logger = logging.getLogger('hulksport')


class HulkSportSpider(BaseSpider):
    name = 'hulksport'
    allowed_domains = ['hulksport.com', 'livesport.best']
    redis_key = 'hulksport:start_urls'
    TITLE_XPATH = "//div[contains(@class,'panel-heading')]//text()"

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[descendant::*[normalize-space(text())='WATCH']]"),
             callback='parse_item',
             process_request='use_splash',
             follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='card']/descendant::a"),
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

        texts = loader.get_xpath(self.TITLE_XPATH)
        loader.add_value('raw_asset', texts[0])
        loader.add_value('raw_category', texts[1])

        logger.debug("item extracted for {}".format(response.url))
        return loader.load_item()
