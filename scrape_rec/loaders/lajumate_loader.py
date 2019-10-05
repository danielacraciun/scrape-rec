from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.loaders.base_realestate_loader import BaseRealEstateAdLoader
from scrape_rec.loaders.filters import (
    take_first_splitter, lower_string, floor_mapper, clean_whitespace, missing_price_filter_with_currency,
    take_second_splitter, currency_mapper
)


class LajumateAdLoader(BaseRealEstateAdLoader):
    price_out = Compose(TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_first_splitter, int)
    currency_out = Compose(
        TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_second_splitter, currency_mapper
    )
    floor_out = Compose(TakeFirst(), take_first_splitter, lower_string, floor_mapper)
    source_offer_out = Compose(TakeFirst(), lower_string)
