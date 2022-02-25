"""
Items that model what is used by pisspricer api
"""

import scrapy
from itemloaders.processors import MapCompose


class FullItem(scrapy.Item):
    itemPrice = scrapy.Field()
    item = scrapy.Field()
    store = scrapy.Field()


class ItemPrice(scrapy.Item):
    price = scrapy.Field()
    salePrice = scrapy.Field()
    internalSku = scrapy.Field()


class Item(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    stdDrinks = scrapy.Field()
    alcoholContent = scrapy.Field()
    volumeEach = scrapy.Field()
    packSize = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()


class Location(scrapy.Item):
    lattitude = scrapy.Field()
    longitude = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()
    region = scrapy.Field()


class Store(scrapy.Item):
    name = scrapy.Field()
    internalId = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
