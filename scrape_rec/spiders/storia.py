import re
from itertools import takewhile

import dateparser
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class StoriaSpider(BaseRealEstateSpider):
    name = "storia"
    start_urls = ['https://www.storia.ro/inchiriere/apartament/cluj/cluj-napoca/cluj-napoca/?search%5Border%5D=created_at_first%3Adesc',]
    item_links_xpath = '//h3/a[@data-featured-name="listing_no_promo"]/@href'
    next_link_xpath = '//a[@data-dir="next"]/@href'
    attributes_mapping = {
        'partitioning': 'Compartimentare',
        'surface': 'Suprafata utila (m²)',
        'building_year': 'Anul constructiei',
        'floor': 'Etaj',
        'number_of_rooms': 'Numarul de camere',
    }
    convert_to_int = ['surface', 'floor', 'number_of_rooms']
    title_xpath = '//h1/text()'
    description_xpath = '//section[@class="section-description"]//text()'
    date_xpath = '//div[contains(text(), "Data publicarii")]/text()'   
    base_floors_mapping = {
        'Parter': 0,
        'Demisol': -1,
    }

    price_regex = re.compile(r'\"price\":\"(\d+)\"')

    def is_product_url(self, url):
        return '/oferta/' in url

    def get_attribute_values(self, response):
        attr_list = [
            item.strip().replace(':', '')
            for item in response.xpath('//section[@class="section-overview"]//ul/li/text()').extract()
        ]
        value_list = response.xpath('//section[@class="section-overview"]//ul/li/strong/text()').extract()
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def process_price(self, response):
        price_script = ''.join(response.xpath(
            "//script[contains(text(), '\"price\"')]/text()").getall())
        if not price_script:
            self.logger.warning(
                'Price script could not be extracted {}'.format(response.url))
            return 0, 'EUR'

        price_match = self.price_regex.search(price_script)
        if not price_match:
            self.logger.error(
                'Price regex failed {}'.format(response.url))
            return 0, 'EUR'

        return int(price_match.group(1)), 'EUR'

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        raw_date = ad_date.split(':')[0]
        return dateparser.parse(raw_date)

    def process_item_additional_fields(self, item, response):
        desc = item['description'].lower()
        item['terrace'] = any(word in desc for word in ['terasa', 'balcon', 'balcoane'])
        item['parking'] = any(word in desc for word in ['parcare', 'garaj'])
        item['cellar'] = any(word in desc for word in ['pivnita', 'boxa'])

        item['source_offer'] = response.xpath(
            '//div[@class="css-asr5zc-AdAgency-className"]/ul/li/text()').extract_first().strip()

        return item