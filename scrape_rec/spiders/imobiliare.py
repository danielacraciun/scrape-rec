import dateparser
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
        'partitioning': 'Compartimentare:',
        'surface': 'Suprafaţă utilă:',
        'building_year': 'An construcţie:',
        'floor': 'Etaj:',
        'number_of_rooms': 'Nr. camere:',
        'terrace': 'Nr. balcoane:',
        'parking': 'Nr. locuri parcare:',
    }
    convert_to_int = ['surface', 'number_of_rooms']
    title_xpath = '//h1/text()'
    description_xpath = '//div[@id="b_detalii_text"]/p//text()'
    date_xpath = '//span[@class="data-actualizare"]/text()'
    price_xpath = '//div[@itemprop="price"]/text()'
    currency_xpath = '//p[@itemprop="priceCurrency"]/text()'
    base_floors_mapping = {
        'Parter': 0,
        'Demisol': -1,
    }

    def is_product_url(self, url):
        return 'de-inchiriat' in url

    def get_attribute_values(self, response):
        attr_list = [
            item.strip().replace(':', '')
            for item in response.xpath('//ul[contains(@class, "lista-tabelara")]/li/text()').extract()
        ]
        value_list = response.xpath('//ul[contains(@class, "lista-tabelara")]/li/span/text()').extract()
        clean_value_list = []
        for value in value_list:
            if 'mp' in value:
                clean_value_list.append(value.split()[0])
                continue
            if 'etaj' in value.lower():
                clean_value_list.append(value.split()[1])
                continue
            clean_value_list.append(value)

        return {attr: val for attr, val in zip(attr_list, value_list)}

    def process_price(self, response):
        return (
            int(response.xpath(self.price_xpath).extract_first()), response.xpath(self.currency_xpath).extract_first()
        )

    def process_ad_date(self, ad_date):
        if not ad_date:
            return

        raw_date = ad_date.split(' ')[0].strip()
        return dateparser.parse(raw_date)

    def process_item_additional_fields(self, item, response):
        desc = item['description'].lower()

        item['terrace'] = (
            True if item.get('terrace') else any(word in desc for word in ['terasa', 'balcon', 'balcoane'])
        )
        item['parking'] = True if item.get('parking') else any(word in desc for word in ['parcare', 'garaj'])
        item['cellar'] = any(word in desc for word in ['pivnita', 'boxa'])

        item['source_offer'] = (
            'Agentie' if response.xpath('//div[contains(@class, "agentie")]').extract() else 'Proprietar'
        )

        return item
