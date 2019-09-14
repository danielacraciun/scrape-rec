from urllib.parse import urlparse

from scrape_rec.loaders import PiataAZAdLoader
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

    title_xpath = '//h1/text()'
    description_xpath = '//div[@class="offer-details__description"]/text()'
    date_xpath = '//div[@class="announcement-detail__date-time pull-right"]/span/text()'
    price_xpath = '//div[@class="sidebar--details__top__price"]/strong/text()'
    currency_xpath = '//div[@class="sidebar--details__top__price"]/b/text()'

    item_loader_class = PiataAZAdLoader

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

    def load_particular_fields(self, loader, response):
        urlpath = urlparse(response.meta['start_url']).path
        if 'garsoniere' in urlpath:
            loader.add_value('number_of_rooms', 1)

        return loader
