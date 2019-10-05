from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.loaders.base_realestate_loader import BaseRealEstateAdLoader
from scrape_rec.loaders.filters import (
    multiline_joiner, clean_whitespace, missing_price_filter_with_currency, take_second_splitter, take_first_splitter,
    currency_mapper, olx_parse_date
)


class OlxAdLoader(BaseRealEstateAdLoader):
    posted_date_out = Compose(multiline_joiner, olx_parse_date)
    price_out = Compose(TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_first_splitter, int)
    currency_out = Compose(
        TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_second_splitter, currency_mapper
    )
    surface_out = Compose(TakeFirst(), take_first_splitter, int)
