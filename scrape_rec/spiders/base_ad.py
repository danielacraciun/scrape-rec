from datetime import datetime

import scrapy
from scrapy.utils.request import request_fingerprint

from scrape_rec.loaders.base_ad_loader import BaseAdLoader


class BaseAdSpider(scrapy.Spider):

    # Fields that can be found in a structured way in the individual ad page
    # an entry usually looks like {'base_field': 'website_field ...}
    attributes_mapping = {}
    item_loader_class = BaseAdLoader

    # Mandatory XPaths
    item_links_xpath = ''
    next_link_xpath = ''

    title_xpath = ''
    description_xpath = ''
    date_xpath = ''
    price_xpath = ''
    currency_xpath = ''

    def get_attribute_values(self, response):
        """
        Takes a response as an arguments, and usually parses an individual ad page
        in order to extract structured data
        """
        raise NotImplementedError

    def load_particular_fields(self, loader, response):
        """
        Optional method to implement, takes an ItemLoader and a response and
        tries to attach any data the generic processing method might have missed
        :param loader:
        :param response:
        :return:
        """
        return

    def process_link(self, response):
        item_loader_class = self.item_loader_class
        loader = item_loader_class(selector=response)

        loader.add_value('source_website', self.name)
        loader.add_value('link', response.url)
        loader.add_value('fingerprint', request_fingerprint(response.request))
        loader.add_value('scraped_date', datetime.now())

        loader.add_xpath('title', self.title_xpath)
        loader.add_xpath('description', self.description_xpath)
        loader.add_xpath('posted_date', self.date_xpath)
        loader.add_xpath('price', self.price_xpath)
        loader.add_xpath('currency', self.currency_xpath)

        available_attributes = self.get_attribute_values(response)

        for attr, site_value in self.attributes_mapping.items():
            value = available_attributes.get(site_value)
            loader.add_value(attr, value)

        self.load_particular_fields(loader, response)
        yield loader.load_item()

    def parse(self, response):
        links = response.xpath(self.item_links_xpath).extract()
        for link in links:
            yield response.follow(link, callback=self.process_link, meta={'start_url': response.url})

        next_link = response.xpath(self.next_link_xpath).extract_first()
        if not next_link:
            self.logger.error(
                'Invalid next listing page xpath {}'.format(response.url))
            return

        yield response.follow(
            next_link, dont_filter=True, meta={'dont_cache': True}
        )
