from urllib.parse import urlparse

from scrape_rec.loaders import OlxAdLoader
from scrape_rec.spiders.base_realestate import BaseRealEstateSpider


class OlxSpider(BaseRealEstateSpider):
    name = "olx"
    start_urls = [
        'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/1-camera/cluj-napoca/',
        'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/2-camere/cluj-napoca/',
        'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/3-camere/cluj-napoca/',
        'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/4-camere/cluj-napoca/'
    ]
    item_links_xpath = '//a[contains(@class, "detailsLink") and not(contains(@class, "detailsLinkPromoted"))]/@href'
    next_link_xpath = '//a[@data-cy="page-link-next"]/@href'

    attributes_mapping = {
        'partitioning': 'Compartimentare',
        'surface': 'Suprafata utila',
        'building_year': 'An constructie',
        'floor': 'Etaj',
        'source_offer': 'Oferit de',
    }

    title_xpath = '//h1/text()'
    description_xpath = '//div[@id="textContent"]/text()'
    date_xpath = '//em/text()'
    price_xpath = '//div[@class="price-label"]/strong/text()'
    currency_xpath = '//div[@class="price-label"]/strong/text()'

    item_loader_class = OlxAdLoader

    def is_product_url(self, url):
        return '/oferta/' in url

    def get_attribute_values(self, response):
        attr_table = response.css('table.item')
        return {
            attr.css('th::text').extract_first(): (
                    attr.css('td strong a::text') or attr.css('td strong::text')
            ).extract_first().strip()
            for attr in attr_table
        }

    def load_particular_fields(self, loader, response):
        urlpath = urlparse(response.meta['start_url']).path
        loader.add_value('number_of_rooms', urlpath.split('/')[3][0])

        return loader
