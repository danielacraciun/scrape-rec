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
        'gheorgheni',
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
    ]

    def process_item(self, item, spider):
        for neighborhood in self.neighborhoods:
            if neighborhood in item['title'].lower():
                item['neighborhood'] = neighborhood
                return item

        for neighborhood in self.neighborhoods:
            if neighborhood in item['description'].lower():
                item['neighborhood'] = neighborhood
                return item

        item['neighborhood'] = 'not found'

        return item


class PostgresPipeline(object):

    def __init__(self):
        self.session = get_postgres_session()

    def process_item(self, item, spider):
        # TODO: Move this in validation schema
        if not item.get('posted_date'):
            return

        # TODO: don't add if already exists for double check in case redis fails

        entry = RealestateApartment(**item) 

        self.session.add(entry)  
        self.session.commit()

        return item
