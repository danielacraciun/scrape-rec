from urllib.parse import urlparse

import dateparser
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class PiataAZSpider(BaseRealEstateSpider):
    name = "piata_az"
    start_urls = [
        'https://www.piata-az.ro/imobiliare/apartamente-de-inchiriat/cluj-napoca',
        'https://www.piata-az.ro/imobiliare/garsoniere-de-inchiriat/cluj-napoca',
    ]
    item_links_xpath = '//a[@class="announcement__description__title"]/@href'
    next_link_xpath = '//li[@class="pagination__right"]/a/@href'
    attributes_mapping = {
        'source_offer': 'Pers. fizica sau agentie',
        'partitioning': 'compartimentare',
        'surface': 'suprafata',
        'floor': 'etaj',
        'number_of_rooms': 'camere',
        'building_year': 'an constructie',
        'parking': 'parcare',
        'terrace': 'balcoane',
    }
    convert_to_int = ['number_of_rooms', 'surface', 'floor']
    title_xpath = '//h1/text()'
    description_xpath = '//div[@class="offer-details__description"]/text()'
    date_xpath = '//div[@class="announcement-detail__date-time pull-right"]/span/text()'
    price_xpath = '//div[@class="sidebar--details__top__price"]/strong/text()'
    currency_xpath = '//div[@class="sidebar--details__top__price"]/b/text()'
    base_floors_mapping = {
        'parter': 0,
        'demisol': -1,
        'mansarda': 99,
    }
    currency_mapping = {
        'euro': 'EUR',
        'EURO': 'EUR',
        'lei': 'RON',
        'LEI': 'RON',
    }

    def process_price(self, response):
        price = response.xpath(self.price_xpath).extract_first()
        currency = response.xpath(self.currency_xpath).extract_first()

        if not price:
            return 0, 'EUR'

        try:
            integer_price = int(price.strip())
        except:
            self.logger.error(f'This might be an exchange request: {price}')
            return 0, 'EUR'

        return integer_price, (self.currency_mapping.get(currency.strip()) if currency else 'EUR')

    def is_product_url(self, url):
        return not ('imobiliare' in url)

    def get_attribute_values(self, response):
        attr_list = response.xpath('//div/ul/li/div/b/text()').extract()
        value_list = response.xpath('//div/ul/li/div/text()').extract()
        clean_value_list = []
        for value in value_list:
            if 'mp' in value:
                clean_value_list.append(value.split()[0])
                continue
            if 'etaj' in value.lower():
                clean_value_list.append(value.split()[1].lower())
                continue
            clean_value_list.append(value)
        return {attr: val for attr, val in zip(attr_list, clean_value_list)}

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        return dateparser.parse(ad_date, date_formats=['%d.%m.%Y %H:%M'])

    def process_item_additional_fields(self, item, response):
        desc = item['description'].lower()
        if not item.get('terrace'):
            item['terrace'] = any(word in desc for word in ['terasa', 'balcon', 'balcoane'])
        else:
            item['terrace'] = True if int(item['terrace']) > 0 else False
        if not item.get('parking'):
            item['parking'] = any(word in desc for word in ['parcare', 'garaj'])
        else:
            item['parking'] = item['parking'] == 'da'

        item['cellar'] = any(word in desc for word in ['pivnita', 'boxa'])

        urlpath = urlparse(response.meta['start_url']).path
        if not item.get('number_of_rooms') and 'garsoniere' in urlpath:
            item['number_of_rooms'] = 1

        return item
