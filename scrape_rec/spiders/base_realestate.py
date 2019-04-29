from datetime import datetime
from itertools import takewhile

import scrapy
from scrapy.utils.request import request_fingerprint

from scrape_rec.items import RealEstateRentedApartmentItem


class BaseRealEstateSpider(scrapy.Spider):

    def get_attribute_values(self, response):
        raise NotImplementedError

    def process_title(self, title):
        return title

    def process_description(self, description):
        return description

    def process_ad_date(self, ad_date):
        return ad_date

    def process_price(self, price):
        return int(price), 'EUR'

    def process_item_additional_fields(self, item, response):
        return item

    def process_link(self, response):
        item = RealEstateRentedApartmentItem()
        item['source_website'] = self.name
        item['link'] = response.url

        item['fingerprint'] = request_fingerprint(response.request)

        title = response.xpath(self.title_xpath).extract_first().strip()
        title = self.process_title(title)
        item['title'] = title

        description = ''.join(map(lambda line: line.strip(), response.xpath(self.description_xpath).extract()))
        description = self.process_description(description)
        item['description'] = description

        ad_date = None
        if self.date_xpath:
            ad_date = response.xpath(self.date_xpath).extract_first().strip()
            ad_date = self.process_ad_date(ad_date)
        if not ad_date:
            ad_date = datetime.now()
        item['posted_date'] = ad_date

        price = response.xpath(self.price_xpath).extract_first()
        item['price'], item['currency'] = self.process_price(price)

        available_attributes = self.get_attribute_values(response)
        for attr, site_value in self.attributes_mapping.items():
            value = available_attributes.get(site_value)
            if attr == 'floor' and value in self.base_floors_mapping.keys():
                value = self.base_floors_mapping.get(value)
            elif value and attr in self.convert_to_int:
                value = int(''.join(takewhile(str.isdigit, value)))

            if value:
                item[attr] = value

        # in order to extract additional fields
        item = self.process_item_additional_fields(item, response)
        yield item

    def parse(self, response):
        links = response.xpath(self.item_links_xpath).extract()
        for link in links:
            yield response.follow(link, callback=self.process_link)

        next_link = response.xpath(self.next_link_xpath).extract_first()
        yield response.follow(next_link, dont_filter=True, meta={'dont_cache': True})
