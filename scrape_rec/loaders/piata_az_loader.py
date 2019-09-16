from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.loaders.base_loader import BaseAdLoader
from scrape_rec.loaders.filters import (
    take_first_splitter, lower_string, floor_mapper, clean_whitespace, missing_price_filter_with_currency,
    take_second_splitter, currency_mapper, piata_az_parse_date, number_to_bool
)
from scrape_rec.loaders.mappings import yesno_boolean_mapper


class PiataAZAdLoader(BaseAdLoader):
    number_of_rooms_out = Compose(TakeFirst(), take_first_splitter, int)
    price_out = Compose(TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_first_splitter, int)
    currency_out = Compose(
        TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_second_splitter, currency_mapper
    )
    floor_out = Compose(TakeFirst(), take_first_splitter, lower_string, floor_mapper)
    posted_date_out = Compose(TakeFirst(), piata_az_parse_date)
    parking_out = Compose(TakeFirst(), lambda kw: yesno_boolean_mapper.get(kw))
    terrace_out = number_to_bool
    source_offer_out = Compose(TakeFirst(), lower_string)
