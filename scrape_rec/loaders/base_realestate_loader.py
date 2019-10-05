from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.items import RealEstateRentedApartmentItem
import scrape_rec.loaders.filters as filters
from scrape_rec.loaders.base_ad_loader import BaseAdLoader

to_int = Compose(TakeFirst(), filters.clean_whitespace, float, int)
to_lower = Compose(TakeFirst(), filters.lower_string)
number_to_bool = Compose(TakeFirst(), filters.number_to_bool)


class BaseRealEstateAdLoader(BaseAdLoader):
    default_item_class = RealEstateRentedApartmentItem
    default_output_processor = TakeFirst()

    surface_out = to_int
    number_of_rooms_out = to_int
    partitioning_out = to_lower
    building_year_out = to_lower
    neighborhood_out = to_lower
    floor_out = Compose(TakeFirst(), filters.lower_string, filters.floor_mapper)





