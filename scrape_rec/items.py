from scrapy_jsonschema.item import JsonSchemaItem


def get_base_ad_json_schema():
    return {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Base ad listing',
        'description': 'Base ad item',
        'type': 'object',
        'properties': {
            'fingerprint': {
                'description': 'The unique identifier for a product',
                'type': 'string'
            },
            'title': {
                'description': 'Ad listing title',
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
                'description': 'The creation date of the listing',
            },
            'scraped_date': {
                'description': 'Date at which the item was scraped',
            },
            'description': {
                'description': 'Ad description',
                'type': 'string'
            },
            'source_website': {
                'description': 'The website of origin',
                'type': 'string'
            },
            'link': {
                'description': 'The link to the ad',
                'type': 'string'
            },
        },
        'required': ['fingerprint', 'title', 'description', 'price', 'currency', 'scraped_date']
    }


def get_real_estate_ad_json_schema():
    schema = get_base_ad_json_schema()
    schema['title'] = 'Real estate rented apartment item'
    schema['description'] = 'An listing for an apartment for rent'
    schema['properties'].update({
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
        'source_offer': {
            'description': 'Type of owner',
            'type': 'string'
        },
        'neighborhood': {
            'description': 'The area',
            'type': 'string'
        },
    })

    return schema


class AdItem(JsonSchemaItem):
    jsonschema = get_base_ad_json_schema()


class RealEstateRentedApartmentItem(JsonSchemaItem):
    jsonschema = get_real_estate_ad_json_schema()
