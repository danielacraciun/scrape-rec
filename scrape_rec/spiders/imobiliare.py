from scrape_rec.loaders import ImobiliareAdLoader
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class ImobiliareRoSpider(BaseRealEstateSpider):
    name = "imobiliare_ro"
    start_urls = [
        'https://www.imobiliare.ro/inchirieri-apartamente/cluj-napoca',
        'https://www.imobiliare.ro/inchirieri-garsoniere/cluj-napoca',
    ]
    item_links_xpath = '//h2[@class="titlu-anunt hidden-xs"]/a/@href'
    next_link_xpath = '//a[@class="inainte butonpaginare"]/@href'

    attributes_mapping = {
        'partitioning': 'Compartimentare',
        'surface': 'Suprafaţă utilă',
        'building_year': 'An construcţie',
        'floor': 'Etaj',
        'number_of_rooms': 'Nr. camere',
        'terrace': 'Nr. balcoane',
        'parking': 'Nr. locuri parcare',
    }

    title_xpath = '//h1/text()'
    description_xpath = '//div[@id="b_detalii_text"]/p//text()'
    date_xpath = '//span[@class="data-actualizare"]/text()'
    price_xpath = '//div[@itemprop="price"]/text()'
    currency_xpath = '//p[@itemprop="priceCurrency"]/text()'

    item_loader_class = ImobiliareAdLoader

    def is_product_url(self, url):
        return 'de-inchiriat' in url

    def get_attribute_values(self, response):
        attr_list = [
            item.strip().replace(':', '')
            for item in response.xpath('//ul[contains(@class, "lista-tabelara")]/li/text()').extract()
        ]
        value_list = response.xpath('//ul[contains(@class, "lista-tabelara")]/li/span/text()').extract()
        return {attr: val for attr, val in zip(attr_list, value_list)}

    def load_particular_fields(self, loader, response):
        loader.add_xpath('description', '//div[@id="b_detalii_specificatii"]/p/text()')
        loader.add_value(
            'source_offer',
            'agentie' if response.xpath('//div[contains(@class, "agentie")]').extract() else 'proprietar'
        )
        return loader
