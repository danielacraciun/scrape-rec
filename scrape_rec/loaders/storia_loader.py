from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.loaders.base_realestate_loader import BaseRealEstateAdLoader
from scrape_rec.loaders.filters import (
    clean_whitespace, missing_price_filter_with_currency, take_second_splitter, take_first_splitter, currency_mapper,
    storia_parse_date
)


class StoriaAdLoader(BaseRealEstateAdLoader):
    posted_date_out = Compose(TakeFirst(), storia_parse_date)
    price_out = Compose(TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_first_splitter, int)
    currency_out = Compose(
        TakeFirst(), clean_whitespace, missing_price_filter_with_currency, take_second_splitter, currency_mapper
    )
