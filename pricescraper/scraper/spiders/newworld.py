import scrapy
import json
import requests
from ..items.newworld import ItemAtPrice, Store
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, SelectJmes

NW_BEER_AND_WINE_PAGE_URL = 'https://www.newworld.co.nz/shop/category/beer-cider-and-wine?ps=50'


class NewWorldSpider(scrapy.Spider):
    name = 'newworld'
    allowed_domains = ['newworld.co.nz']
    start_urls = ['https://www.newworld.co.nz/']
    api_url = "https://www.newworld.co.nz/CommonApi"
    # dictionary to map UserItem fields to Jmes query paths
    item_price_jmes_paths = {
        'basePrice': 'ProductDetails.MultiBuyBasePrice',
        'price': 'ProductDetails.PricePerItem',
        'productId': 'productId',
        'productName': 'productName'
    }
    store_jmes_paths = {
        'name': 'name',
        'id': 'id',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'address': 'address',
        'openingHours': 'openingHours'
    }

    def parse(self, response, **kwargs):
        # get the ID of all New World stores from API
        stores_json = requests.get(f"{self.api_url}/Store/GetStoreList").json()

        # iterate over each store
        for store in stores_json['stores']:
            # check the store can be accessed
            if not store.get('onboardingMode'):

                # create an ItemLoader to populate a StoreItem item
                loader = ItemLoader(item=Store())
                loader.default_output_processor = TakeFirst()

                # iterate over each store json field an populate a store item
                for (field, path) in self.store_jmes_paths.items():
                    loader.add_value(field, SelectJmes(path)(store))

                yield response.follow(
                    NW_BEER_AND_WINE_PAGE_URL,
                    callback=self.parse_beer_wine_page,
                    cookies={"STORE_ID_V2": store['id'],
                             "eCom_STORE_ID": store['id']},
                    meta={'store': loader.load_item()},
                    dont_filter=True)

    def parse_beer_wine_page(self, response):
        products = response.css(
            'div.l-columns__column.l-columns__column--one-l.l-columns__column--one-half-m.u-margin-bottom-x2')

        for product in products:
            # get the items json
            data_text = product.css(
                'div.js-product-card-footer.fs-product-card__footer-container::attr(data-options)').get()
            item_json = json.loads(data_text)

            # create an ItemLoader to populate an ItemAtPrice item
            loader = ItemLoader(item=ItemAtPrice(), selector=product)
            loader.default_output_processor = TakeFirst()

            # iterate over each item json field an populate
            for (field, path) in self.item_price_jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(item_json))

            # populate url and store fields
            loader.add_css('url', 'a.fs-product-card__details.u-color-black.u-no-text-decoration.u-cursor::attr(href)')
            loader.add_value('store', response.meta.get('store'))

            loaded_item = loader.load_item()
            yield loaded_item

        next_page = response.css('a.fs-pagination__btn--next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_beer_wine_page)


