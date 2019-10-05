from scrape_rec.loaders import BaseRealEstateAdLoader
from scrape_rec.spiders.base_ad import BaseAdSpider


class BaseRealEstateSpider(BaseAdSpider):

    item_loader_class = BaseRealEstateAdLoader

    def get_attribute_values(self, response):
        super().get_attribute_values(response)
