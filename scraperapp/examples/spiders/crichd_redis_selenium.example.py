# -*- coding: utf-8 -*-
import scrapy
import datetime
import socket
import logging

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scraperapp.items import ScraperItem
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisCrawlSpider


logger = logging.getLogger('crichdspider')


class CrichdSpider(RedisCrawlSpider):
    name = 'crichd_redis'
    allowed_domains = ['hd.crichd.com', 'crichd.com',
                       'pl.topperformance.xyz', 'watch.crichd.to']
    redis_key = 'crichd_redis:start_urls'

    RAW_ASSET_XPATH = "//td[contains(text(), 'Game Name:')]/following-sibling::td[1]/h3/text()"
    RAW_CATEGORY_XPATH = "//td[contains(text(), 'Sports Name:')]/following-sibling::td[1]/text()"
    DATE_XPATH = "//td[contains(text(), 'Date:')]/following-sibling::td[1]/text()"
    START_TIME_XPATH = "//td[contains(text(), 'Start Time:')]/following-sibling::td[1]/text()"
    END_TIME_XPATH = "//td[contains(text(), 'End Time:')]/following-sibling::td[1]/text()"

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[child::h2[@class='gametitle']]"),
             callback='parse_item',
             follow=True,
             process_request='_process_request'),
    )

    # a callable which will be called for every Request extracted by this rule
    def _process_request(self, request, response):
        logger.debug("selenium request is created for {}".format(request.url))
        request.meta.update(
            webdriver_settings={
                'wait_time': 5,
                'wait_until': EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe'))
            }
        )
        return request

    def _extract_urls(self, iframe_body):
        soup = BeautifulSoup(iframe_body, 'lxml')
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return urls

    def parse_item(self, response):
        logger.debug("parsing {} to extract item".format(response.url))
        l = ItemLoader(item=ScraperItem(), response=response)

        # capture viewing location url
        l.add_value('viewing_location_url', response.url)

        # capture hosting site urls
        urls = self._extract_urls(
            response.request.meta.get('iframe_body', None))
        l.add_value('hosting_site_urls', urls)

        l.add_xpath('raw_asset', self.RAW_ASSET_XPATH, MapCompose(str.strip))
        l.add_xpath('raw_category', self.RAW_CATEGORY_XPATH,
                    MapCompose(str.strip))

        l.add_xpath('date', self.DATE_XPATH)
        l.add_xpath('start_time', self.START_TIME_XPATH)
        l.add_xpath('end_time', self.END_TIME_XPATH)

        # hosue keeping fields
        l.add_value('scrape_date', datetime.datetime.now().isoformat())
        l.add_value('spider', self.settings.get('BOT_NAME'))
        l.add_value('project', self.name)

        logger.debug("item extracted for {}".format(response.url))
        return l.load_item()
