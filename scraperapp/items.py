# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScraperItem(Item):
    # Primary fields
    viewing_location_url = Field()
    hosting_site_urls = Field()
    raw_asset = Field()  # teams playing against each other
    raw_category = Field()  # category like soccer
    date = Field()
    start_time = Field()
    end_time = Field()

    # Housekeeping fields
    project = Field()
    spider = Field()
    scrape_date = Field()
