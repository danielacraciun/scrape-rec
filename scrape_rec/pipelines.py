from unidecode import unidecode

from scrape_rec.utils import get_postgres_session, RealestateApartment


class NeighborhoodFinderPipeline(object):
    neighborhoods = [
        'andrei muresanu',
        'bulgaria',
        'buna ziua',
        'centru',
        'dambul rotund',
        'gara',
        'horea'
        'manastur',
        'grigorescu',
        'gruia',
        'iris',
        'intre lacuri',
        'marasti',
        'someseni',
        'zorilor',
        'sopor',
        'faget',
        'borhanci',
        'becas',
        'expo transilvania',
        'iulius',
        'vivo',
        'polus',
        'floresti',
        'viteazu',
        'sigma',
        'piata unirii',
        'dorobantilor',
        'the office',
        'plopilor',
        'calea turzii',
        'baciu',
        'gheorgheni',
        'interservisan',
        'ultracentral',
        'europa',
        'muzeului',
        'calea baciului',
        'titulescu',
    ]

    def process_item(self, item, spider):
        for neighborhood in self.neighborhoods:
            if neighborhood in unidecode(item['title'].lower()):
                item['neighborhood'] = neighborhood
                return item

        for neighborhood in self.neighborhoods:
            if neighborhood in unidecode(item['description'].lower()):
                item['neighborhood'] = neighborhood
                return item

        item['neighborhood'] = 'not found'

        return item


class PostgresPipeline(object):

    def __init__(self):
        self.session = get_postgres_session()

    def process_item(self, item, spider):
        fingerprint_filer = self.session.query(RealestateApartment).filter_by(
            fingerprint=item['fingerprint'])
        if fingerprint_filer.all():
            spider.logger.info('Already scraped item {}'.format(item['fingerprint']))
            return item

        spider.logger.info('New item found {}'.format(item['fingerprint']))

        entry = RealestateApartment(**item) 

        self.session.add(entry)  
        self.session.commit()

        spider.logger.info('New item saved in postgres {}'.format(item['fingerprint']))

        return item
