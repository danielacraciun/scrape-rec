import scrapy
from scrapy_jsonschema.item import JsonSchemaItem


class RealEstateRentedApartmentItem(JsonSchemaItem):
    jsonschema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Realestate apartment item',
        'description': 'An apartment for rent in Cluj',
        'type': 'object',
        'properties': {
            'fingerprint': {
                'description': 'The unique identifier for a product',
                'type': 'string'
            },
            'title': {
                'description': 'Apartment listing title',
                'type': 'string'
            },
            'price': {
                'type': 'number',
                'minimum': 0,
                'exclusiveMinimum': True
            },
            'currency': {
                'description': 'The creation date of the listing or if not found the scrape date',
                'type': 'string',
                'pattern': 'EUR|RON|USD'
            },
            'posted_date': {
                'description': 'The creation date of the listing or if not found the scrape date',
            },
            'description': {
                'description': 'Apartment description',
                'type': 'string'
            },
            'partitioning': {
                'description': 'Apartment sections',
                'type': 'string'
            },
            'surface': {
                'description': 'Surface in mp^2',
                'type': 'integer',
                'minimum': 0
            },
            'building_year': {
                'description': 'The building construction date',
                'type': 'string'
            },
            'floor': {
                'description': 'Obvious',
                'type': 'integer',
            },
            'number_of_rooms': {
                'description': 'Obvious',
                'type': 'integer',
                'minimum': 0
            },
            'terrace': {
                'description': 'Has or not terrace',
                'type': 'boolean'
            },
            'parking': {
                'description': 'Has or not parking',
                'type': 'boolean'
            },
            'cellar': {
                'description': 'Has or not cellar',
                'type': 'boolean'
            },
            'source_website': {
                'description': 'The website of origin',
                'type': 'string'
            },
            'source_offer': {
                'description': 'Type of owner',
                'type': 'string'
            },
            'neighborhood': {
                'description': 'The area',
                'type': 'string'
            },
        },
        'required': ['fingerprint', 'title', 'price', 'posted_date']
    }
