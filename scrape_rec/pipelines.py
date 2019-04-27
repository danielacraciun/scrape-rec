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
        if not(item.get('posted_date')):
            return

        entry = RealestateApartment(
            fingerprint=item.get('fingerprint'),
            title=item.get('title'),
            description=item.get('description'),
            posted_date=item.get('posted_date'),
            partitioning=item.get('partitioning'),
            surface=item.get('surface'),
            building_year=item.get('building_year'),
            floor=item.get('floor'),
            number_of_rooms=item.get('number_of_rooms'),
            terrace=item.get('terrace'),
            parking=item.get('parking'),
            cellar=item.get('cellar'),
            source_website=item.get('source_website'),
            source_offer=item.get('source_offer'),
            neightbourhood=item.get('neightbourhood'),
        ) 

        self.session.add(entry)  
        self.session.commit()

        return item
