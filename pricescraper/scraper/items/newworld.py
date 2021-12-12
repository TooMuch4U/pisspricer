# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose


def none_or_float(price):
    return None if price == '' else float(price)


class ItemAtPrice(scrapy.Item):
    price = scrapy.Field(input_processor=MapCompose(float))
    basePrice = scrapy.Field(input_processor=MapCompose(none_or_float))
    productId = scrapy.Field()
    url = scrapy.Field()
    productName = scrapy.Field()
    store = scrapy.Field()


class Store(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    address = scrapy.Field()
    openingHours = scrapy.Field(input_processor=str)
