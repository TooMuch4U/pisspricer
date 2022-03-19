import base64
import json
import requests
from urllib.parse import urljoin

from .brand import AbstractBrandSpider
from ..items.newworld import ItemAtPrice, Store
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, SelectJmes
from ..services.images import process_response_content
from ..services.pisspricer import PisspricerAdmin
from ..pipelines.foodstuffs_transform import FoodstuffsItemTransformPipeline


BEER_AND_WINE_PATH = '/shop/category/beer-cider-and-wine?ps=50'


class AbstractFoodstuffsSpider(AbstractBrandSpider):

    # dictionary to map Item fields to jmes json query paths
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

    def __init__(self, pisspricer_brand_name, base_url, *args, **kwargs):
        super(AbstractFoodstuffsSpider, self).__init__(pisspricer_brand_name, *args, **kwargs)

        # set constants
        self.allowed_domains = [base_url.lstrip("https://"), 'fsimg.co.nz']
        self.start_urls = [base_url]
        self.api_url = urljoin(base_url, "/CommonApi")

        # get skus that have an image set
        pisspricer = PisspricerAdmin()
        self.skus_with_image = pisspricer.get_existing_image_set(self.brand_id)

    def parse(self, response, **kwargs):
        # get the ID of all New World stores from API
        stores_json = requests.get(f"{self.api_url}/Store/GetStoreList").json()

        # iterate over each store
        for store in stores_json['stores']:
            # check the store can be accessed
            on_boarding = store.get('onboardingMode')
            delivery = store.get('delivery')
            click_and_collect = store.get('clickAndCollect')
            if (not on_boarding) and (delivery or click_and_collect):

                # create an ItemLoader to populate a StoreItem item
                loader = ItemLoader(item=Store())
                loader.default_output_processor = TakeFirst()

                # iterate over each store json field an populate a store item
                for (field, path) in self.store_jmes_paths.items():
                    loader.add_value(field, SelectJmes(path)(store))

                yield response.follow(
                    urljoin(self.api_url, BEER_AND_WINE_PATH),
                    callback=self.parse_beer_wine_page,
                    cookies=self.get_store_cookies(store),
                    meta={'store': loader.load_item()},
                    dont_filter=True)

    @staticmethod
    def get_store_cookies(store):
        return {"STORE_ID_V2": store['id'], "eCom_STORE_ID": store['id']}

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

            # volume or pack size
            size = loader.get_css('p.u-color-half-dark-grey::text')
            if len(size) > 0:
                size = size[0]
                if "ml" in size:
                    loader.add_value('volume', size.rstrip("ml"))
                elif "pk" in size:
                    loader.add_value('packSize', size.rstrip("pk"))

            # get image if its new, else load item
            if self._image_already_exists(item_json[self.item_price_jmes_paths['productId']]):
                yield self.load_item(loader)
            else:
                image_url = product.css('div.fs-product-card__product-image').attrib['data-src-s']

                yield response.follow(
                    image_url,
                    callback=self.load_image,
                    meta={'item_loader': loader},
                    dont_filter=True)

        store = response.meta.get('store')
        next_page = response.css('a.fs-pagination__btn--next').attrib.get('href')
        if next_page is not None:
            yield response.follow(
                next_page,
                callback=self.parse_beer_wine_page,
                dont_filter=True,
                meta={'store': store},
                cookies=self.get_store_cookies(store))

    def load_image(self, response):
        loader = response.meta.get('item_loader')

        # process image and encode as base64 string
        image_file = process_response_content(response.body)
        image = base64.b64encode(image_file)

        # add image to loader and load item
        loader.add_value('image', image)
        yield self.load_item(loader)

    def load_item(self, loader):
        loaded_item = loader.load_item()
        self.logger.debug(f"Item loaded: {loaded_item.get('productName')}")
        transformed_item = FoodstuffsItemTransformPipeline().process_item(loaded_item, self)
        return transformed_item

    def _image_already_exists(self, internal_sku):
        """ Checks if the image already exists on pisspricer """
        return internal_sku in self.skus_with_image
