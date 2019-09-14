from unidecode import unidecode

from scrape_rec.db_wrapper import get_postgres_session, RealestateApartment


class NeighborhoodFinderPipeline(object):
    neighborhoods = [
        'andrei muresanu',
        'bulgaria',
        'buna ziua',
        'centru',
        'dambul rotund',
        'gara',
        'horea',
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
        'usamv',
    ]

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

        if item.get('parking') is None:
            item['parking'] = any(word in cleaned_desc for word in ['parcare', 'garaj'])

        if item.get('terrace') is None:
            item['terrace'] = any(word in cleaned_desc for word in ['terasa', 'balcon', 'balcoane'])

        if item.get('cellar') is None:
            item['cellar'] = any(word in cleaned_desc for word in ['pivnita', 'boxa'])

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
