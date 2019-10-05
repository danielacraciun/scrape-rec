from unidecode import unidecode

from scrape_rec.keywords import keywords, amenities
from scrape_rec.db_wrapper import get_postgres_session, RealestateApartment
from scrape_rec.settings import CURRENT_CITY


class NeighborhoodFinderPipeline(object):

    neighborhoods = keywords[CURRENT_CITY]['neighborhoods']

    def process_item(self, item, spider):
        if item.get('neighborhood'):
            return item
        cleaned_title = unidecode(item['title'])
        for neighborhood in self.neighborhoods:
            if neighborhood in cleaned_title:
                item['neighborhood'] = neighborhood
                return item

        cleaned_desc = unidecode(item['description'])
        for neighborhood in self.neighborhoods:
            if neighborhood in cleaned_desc:
                item['neighborhood'] = neighborhood
                return item

        item['neighborhood'] = 'not found'
        return item


class DescriptionAnalysePipeline(object):
    def process_item(self, item, spider):
        cleaned_desc = unidecode(item['description'])
        for amenity in amenities:
            if item.get(amenity) is None:
                item[amenity] = any(word in cleaned_desc for word in keywords[CURRENT_CITY][amenity])
        return item


class PostgresPipeline(object):

    def __init__(self):
        self.session = get_postgres_session()

    def process_item(self, item, spider):
        fingerprint_filter = self.session.query(RealestateApartment).filter_by(
            title=item['title'])

        if fingerprint_filter.all():
            spider.logger.info('Already scraped item {}'.format(item['title']))
            return item

        spider.logger.info('New item found {}'.format(item['fingerprint']))

        entry = RealestateApartment(**item) 

        try:
            self.session.add(entry)
            self.session.commit()
            spider.logger.info('New item saved in postgres {}'.format(item['fingerprint']))
        except:
            self.session.rollback()

        return item
