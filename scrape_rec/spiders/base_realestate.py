from datetime import datetime

import scrapy
from scrapy.utils.request import request_fingerprint

from scrape_rec.loaders import BaseAdLoader
from scrape_rec.utils import get_all_urls_from_httpcache


class BaseRealEstateSpider(scrapy.Spider):

    item_loader_class = BaseAdLoader

    def get_attribute_values(self, response):
        raise NotImplementedError

    def is_product_url(self, url):
        raise NotImplementedError

    def load_particular_fields(self, loader, response):
        return loader

    def start_requests(self):
        if hasattr(self, 'httpcache_only'):
            for index, url in enumerate(get_all_urls_from_httpcache(self.name)):
                if self.is_product_url(url):
                    self.logger.info(
                        'Processing {} url from cache {}'.format(index, url))
                    yield scrapy.Request(url, callback=self.process_link)
        else:
            yield from super().start_requests()

    def process_link(self, response):
        item_loader_class = self.item_loader_class
        loader = item_loader_class(selector=response)

        loader.add_xpath('title', self.title_xpath)
        loader.add_xpath('description', self.description_xpath)

        loader.add_value('source_website', self.name)
        loader.add_value('link', response.url)
        loader.add_value('fingerprint', request_fingerprint(response.request))
        loader.add_value('scraped_date', datetime.now())

        loader.add_xpath('posted_date', self.date_xpath)
        loader.add_xpath('price', self.price_xpath)
        loader.add_xpath('currency', self.currency_xpath)

        available_attributes = self.get_attribute_values(response)
        for attr, site_value in self.attributes_mapping.items():
            value = available_attributes.get(site_value)
            loader.add_value(attr, value)

        loader = self.load_particular_fields(loader, response)
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
