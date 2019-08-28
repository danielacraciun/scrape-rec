from urllib.parse import urlparse

import dateparser
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class LajumateSpider(BaseRealEstateSpider):
    name = "lajumate"
    start_urls = [
        'https://lajumate.ro/anunturi_apartamente-de-inchiriat_in-cluj-napoca-cj.html',
    ]
    item_links_xpath = '//a[contains(@class, "main_items")]/@href'
    next_link_xpath = '//link[@rel="next"]/@href'
    attributes_mapping = {
        'neighborhood': 'Zona',
        'partitioning': 'Compartimentare',
        'surface': 'Suprafața utilă (m²)',
        'building_year': 'An finalizare construcție',
        'floor': 'Etaj',
        'number_of_rooms': 'Număr camere',
    }
    convert_to_int = ['surface', 'floor', 'number_of_rooms']
    title_xpath = '//h1/text()'
    description_xpath = '//p[@itemprop="description"]/text()'
    date_xpath = '//span[@id="date"]/text()'
    price_xpath = '//span[@id="price"]/text()'
    base_floors_mapping = {
        'parter': 0,
        'demisol': -1,
    }

    def is_product_url(self, url):
        return '/oferta/' in url

    def get_attribute_values(self, response):
        attr_list = response.xpath('//div[@id="extra-fields"]/div/span/text()').extract()
        value_list = []
        for header_no in range(2, 7):
            values_header = response.xpath(f'//div[@id="extra-fields"]/div/h{header_no}/text()').extract()
            value_list += values_header
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        return dateparser.parse(ad_date)

    def process_price(self, response):
        full_price = response.xpath(self.price_xpath).extract_first().split(' ')
        return int(full_price[0]), full_price[1]

    def process_item_additional_fields(self, item, response):
        desc = item['description'].lower()
        item['terrace'] = any(word in desc for word in ['terasa', 'balcon', 'balcoane'])
        item['parking'] = any(word in desc for word in ['parcare', 'garaj'])
        item['cellar'] = any(word in desc for word in ['pivnita', 'boxa'])

        return item
