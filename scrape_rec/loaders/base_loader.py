from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.items import RealEstateRentedApartmentItem
from scrape_rec.loaders.filters import (
    clean_whitespace, lower_string, number_to_bool, multiline_joiner, parse_date, missing_price_filter,
    currency_mapper, floor_mapper
)

to_int = Compose(TakeFirst(), clean_whitespace, float, int)
to_lower = Compose(TakeFirst(), lower_string)
number_to_bool = Compose(TakeFirst(), number_to_bool)


class BaseAdLoader(ItemLoader):
    default_item_class = RealEstateRentedApartmentItem
    default_output_processor = TakeFirst()

    surface_out = to_int
    number_of_rooms_out = to_int
    partitioning_out = to_lower
    building_year_out = to_lower
    neighborhood_out = to_lower

    title_out = Compose(TakeFirst(), clean_whitespace, lower_string)
    description_out = Compose(multiline_joiner, lower_string)
    posted_date_out = Compose(TakeFirst(), parse_date)
    price_out = Compose(TakeFirst(), clean_whitespace, missing_price_filter, int)
    currency_out = Compose(TakeFirst(), clean_whitespace, currency_mapper)
    floor_out = Compose(TakeFirst(), lower_string, floor_mapper)





