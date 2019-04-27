from itertools import takewhile

import dateparser
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class StoriaSpider(BaseRealEstateSpider):
    name = "storia"
    start_urls = ['https://www.storia.ro/inchiriere/apartament/cluj/cluj-napoca/cluj-napoca/',]
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
    ground_floor = 'Parter'
    price_xpath = '//div[@class="css-c0ipkw-AdHeader"]/text()'

    def get_attribute_values(self, response):
        attr_list = [
            item.strip().replace(':', '')
            for item in response.xpath('//section[@class="section-overview"]//ul/li/text()').extract()
        ]
        value_list = response.xpath('//section[@class="section-overview"]//ul/li/strong/text()').extract()
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def process_price(self, price):
        price = ''.join(takewhile(lambda x: x.isdigit(), ''.join(price.split())))

        return int(price) if price else 0, 'EUR'

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        raw_date = ad_date.split(':')[0]
        return dateparser.parse(raw_date)
