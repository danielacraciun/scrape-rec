from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.loaders.base_realestate_loader import BaseRealEstateAdLoader
from scrape_rec.loaders.filters import (
    take_first_splitter, imobiliare_splitter, take_last_splitter, parse_date, lower_string, floor_mapper,
    number_to_bool
)


class ImobiliareAdLoader(BaseRealEstateAdLoader):
    floor_out = Compose(TakeFirst(), imobiliare_splitter, lower_string, floor_mapper)
    posted_date_out = Compose(TakeFirst(), take_last_splitter, parse_date)
    surface_out = Compose(TakeFirst(), take_first_splitter, int)
    parking_out = Compose(TakeFirst(), number_to_bool)
    terrace_out = Compose(TakeFirst(), number_to_bool)
