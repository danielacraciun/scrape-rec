from scrape_rec.loaders.base_ad_loader import BaseAdLoader
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class DummySpider(BaseRealEstateSpider):
    name = 'dummy'
    start_urls = ['https://dum.my/ads']
    item_links_xpath = '//div[@class="individual-ad"]/@href'
    next_link_xpath = '//div[@class="next-page"]/@href'

    attributes_mapping = {
        'surface': 'Surface',
        'floor': 'Floor',
        'number_of_rooms': 'Rooms',
    }

    title_xpath = '//h1/text()'
    description_xpath = '//div[@class="description"]/text()'
    date_xpath = '//div[@class="date"]/text()'
    price_xpath = '//div[@class="price"]/text()'
    currency_xpath = '//div[@class="price"]/text()'

    item_loader_class = BaseAdLoader

    def get_attribute_values(self, response):
        attr_list = response.xpath('//li[@class="prop"]/text()').extract()
        value_list = response.xpath('//li[@class="prop_value"]/text()').extract()
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def load_particular_fields(self, loader, response):
        loader.add_xpath('description', '//div[@class="alt-description"]/text()')
