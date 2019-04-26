# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateRentedApartmentItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    partitioning = scrapy.Field()
    surface = scrapy.Field()
    building_year = scrapy.Field()
    floor = scrapy.Field()
    number_of_rooms = scrapy.Field()
    terrace = scrapy.Field()
    parking = scrapy.Field()
    cellar = scrapy.Field()
    posted_date = scrapy.Field()
    source_website = scrapy.Field()
    source_offer = scrapy.Field()
    neighborhood = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()