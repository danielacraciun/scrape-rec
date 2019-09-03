import dateparser
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class PiataAZSpider(BaseRealEstateSpider):
    name = "piata_az"
    start_urls = [
        'https://www.piata-az.ro/imobiliare/garsoniere-de-inchiriat/cluj-napoca',
        'https://www.piata-az.ro/imobiliare/apartamente-de-inchiriat/cluj-napoca'
    ]
    item_links_xpath = '//a[@class="announcement__description__title"]/@href'
    next_link_xpath = '//li[@class="pagination__right"]/a/@href'
    attributes_mapping = {
        'source_offer': 'Pers. Fizica Sau Agentie',
        'partitioning': 'Compartimentare',
        'surface': 'Suprafata',
        'floor': 'Etaj',
        'number_of_rooms': 'Camere',
        'building_year': 'An Constructie',
        'parking': 'Parcare',
        'terrace': 'Balcoane',
    }
    convert_to_int = ['surface', 'floor', 'number_of_rooms']
    title_xpath = '//h1/text()'
    description_xpath = '//div[@class="offer-details__description"]/text()'
    date_xpath = '//div[@class="announcement-detail__date-time pull-right"]/span/text()'
    price_xpath = '//div[@class="sidebar--details__top__price"]/strong/text()'
    currency_xpath = '//div[@class="sidebar--details__top__price"]/b/text()'
    base_floors_mapping = {
        'parter': 0,
        'demisol': -1,
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
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        return dateparser.parse(ad_date)

    def process_item_additional_fields(self, item, response):
        desc = item['description'].lower()
        if not item.get('terrace'):
            item['terrace'] = any(word in desc for word in ['terasa', 'balcon', 'balcoane'])
        if not item.get('parking'):
            item['parking'] = any(word in desc for word in ['parcare', 'garaj'])
        item['cellar'] = any(word in desc for word in ['pivnita', 'boxa'])

        return item
