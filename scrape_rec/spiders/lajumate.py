from scrape_rec.loaders import LajumateAdLoader
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class LajumateSpider(BaseRealEstateSpider):
    name = "lajumate"
    start_urls = [
        'https://lajumate.ro/anunturi_apartamente-de-inchiriat_in-cluj-napoca-cj.html',
        'https://lajumate.ro/anunturi_garsoniere-de-inchiriat_in-cluj-napoca-cj.html',
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

    title_xpath = '//h1/text()'
    description_xpath = '//p[@itemprop="description"]/text()'
    date_xpath = '//span[@id="date"]/text()'
    price_xpath = '//span[@id="price"]/text()'
    currency_xpath = '//span[@id="price"]/text()'
    source_offer_xpath = '//div[@class="account_right"]/span/text()'

    item_loader_class = LajumateAdLoader

    def is_product_url(self, url):
        return 'anunturi' not in url

    def get_attribute_values(self, response):
        attr_list = response.xpath('//div[@id="extra-fields"]/div/span/text()').extract()
        value_list = []
        for header_no in range(2, 7):
            values_header = response.xpath(f'//div[@id="extra-fields"]/div/h{header_no}/text()').extract()
            value_list += values_header
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def load_particular_fields(self, loader, response):
        loader.add_xpath('source_offer', self.source_offer_xpath)
        return loader
