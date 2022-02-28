import scrapy
from pydispatch import dispatcher
from scrapy import signals
from abc import ABC
from scrapy.exporters import PythonItemExporter

from ..services.pisspricer import PisspricerAdmin
from ..services.summarisation import Summarisation
from ..items.pisspricer import FullItem, Item, ItemPrice, Store, Location


class AbstractBrandSpider(scrapy.Spider, ABC):

    def __init__(self, brand_name, *args, **kwargs):
        super(AbstractBrandSpider, self).__init__(*args, **kwargs)
        pisspricer = PisspricerAdmin()
        self.brand_name = brand_name
        self.brand_id = pisspricer.get_brand_id(self.brand_name)
        Summarisation().log_start(self.brand_id)
        dispatcher.connect(self.on_close, signals.spider_closed)
        dispatcher.connect(self.on_item_dropped, signals.item_dropped)
        dispatcher.connect(self.on_item_error, signals.item_error)
        dispatcher.connect(self.on_spider_error, signals.spider_error)

    @staticmethod
    def on_item_dropped(item: scrapy.item, response, exception, spider):
        message = f"Response: {response}\n\nItem pipeline drop: {exception}"
        item_json = PythonItemExporter(binary=False).export_item(item)
        Summarisation().log_fail(spider.brand_id, 0, message, item_json)

    @staticmethod
    def on_item_error(item: scrapy.item, response, spider, failure):
        message = f"Response: {response}\n\nItem pipeline error: {failure}"
        item_json = PythonItemExporter(binary=False).export_item(item)
        Summarisation().log_fail(spider.brand_id, 0, message, item_json)

    @staticmethod
    def on_spider_error(failure, response, spider):
        message = f"Response: {response}\n\nSpider error: {failure}"
        item = FullItem()
        item["itemPrice"] = ItemPrice()
        item["item"] = Item()
        item["store"] = Store()
        item["store"]["location"] = Location()
        item_json = PythonItemExporter(binary=False).export_item(item)
        Summarisation().log_fail(spider.brand_id, 0, message, item_json)

    def on_close(self):
        Summarisation().log_end(self.brand_id)
