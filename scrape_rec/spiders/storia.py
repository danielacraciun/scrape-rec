from scrape_rec.loaders import StoriaAdLoader
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class StoriaSpider(BaseRealEstateSpider):
    name = "storia"
    start_urls = [
        'https://www.storia.ro/inchiriere/apartament/cluj/cluj-napoca/cluj-napoca/?search%5Border%5D=created_at_first%3Adesc',
    ]
    item_links_xpath = '//h3/a[@data-featured-name="listing_no_promo"]/@href'
    next_link_xpath = '//a[@data-dir="next"]/@href'

    attributes_mapping = {
        'partitioning': 'Compartimentare',
        'surface': 'Suprafata utila (m²)',
        'building_year': 'Anul constructiei',
        'floor': 'Etaj',
        'number_of_rooms': 'Numarul de camere',
    }

    title_xpath = '//h1/text()'
    description_xpath = '//section[@class="section-description"]/div//text()'
    date_xpath = '//div[contains(text(), "Data publicarii")]/text()'
    price_xpath = '//header/div/div/div/text()'
    currency_xpath = '//header/div/div/div/text()'

    item_loader_class = StoriaAdLoader

    def is_product_url(self, url):
        return '/oferta/' in url

    def get_attribute_values(self, response):
        attr_list = [
            item.strip().replace(':', '')
            for item in response.xpath('//section[@class="section-overview"]//ul/li/text()').extract()
        ]
        value_list = response.xpath('//section[@class="section-overview"]//ul/li/strong/text()').extract()
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def load_particular_fields(self, loader, response):
        loader.add_value(
            'source_offer',
            'agentie' if response.xpath('//div[ul[li[contains(text(), "Agentie")]]]//text()').get() else 'proprietar'
        )
        return loader
