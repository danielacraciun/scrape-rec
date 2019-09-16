import dateparser

from scrape_rec.loaders.mappings import currency_map, floors_mapping


def clean_whitespace(s):
    return s.strip()


def lower_string(s):
    return s.lower()


def multiline_joiner(values):
    return ''.join(map(clean_whitespace, values))


def take_first_splitter(value):
    return value.split()[0] if ' ' in value else value


def take_second_splitter(value):
    return value.split()[1] if ' ' in value else value


def take_last_splitter(value):
    return value.split()[-1] if ' ' in value else value


def imobiliare_splitter(value):
    first_part = value.split('/')[0]
    return take_second_splitter(first_part.strip())


def currency_mapper(value):
    return currency_map.get(value) if value in currency_map.keys() else value


def floor_mapper(value):
    return floors_mapping.get(value) if value in floors_mapping.keys() else int(value)


def parse_date(value):
    if not value:
        return

    return dateparser.parse(value)


def piata_az_parse_date(value):
    return dateparser.parse(value, date_formats=['%d.%m.%Y %H:%M'])


def storia_parse_date(value):
    return parse_date(value.split(':')[1])


def olx_parse_date(value):
    return parse_date(value.split(' ', 1)[1].strip())


def number_to_bool(value):
    return int(value) > 0


def missing_price_filter(value, currency=False):
    price_value = take_first_splitter(value)
    try:
        int(price_value.strip())
    except:
        return '0 EUR' if currency else 0

    return value


def missing_price_filter_with_currency(value):
    return missing_price_filter(value, currency=True)
