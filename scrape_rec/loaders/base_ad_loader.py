from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

from scrape_rec.items import AdItem
import scrape_rec.loaders.filters as filters

to_int = Compose(TakeFirst(), filters.clean_whitespace, float, int)
to_lower = Compose(TakeFirst(), filters.lower_string)
number_to_bool = Compose(TakeFirst(), filters.number_to_bool)


class BaseAdLoader(ItemLoader):
    default_item_class = AdItem
    default_output_processor = TakeFirst()

    title_out = Compose(TakeFirst(), filters.clean_whitespace, filters.lower_string)
    description_out = Compose(filters.multiline_joiner, filters.lower_string)
    posted_date_out = Compose(TakeFirst(), filters.parse_date)
    price_out = Compose(TakeFirst(), filters.clean_whitespace, filters.missing_price_filter, int)
    currency_out = Compose(TakeFirst(), filters.clean_whitespace, filters.currency_mapper)
