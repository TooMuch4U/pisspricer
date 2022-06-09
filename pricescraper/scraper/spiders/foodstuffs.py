import base64
import json
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse
import re

from .brand import AbstractBrandSpider
from ..items.newworld import ItemAtPrice
from ..items.pisspricer import Item, ItemPrice, FullItem, Store, Location
from scrapy.loader import ItemLoader
from scrapy import Request
from itemloaders.processors import TakeFirst, SelectJmes
from ..services.images import process_response_content
from ..services.pisspricer import PisspricerAdmin
from ..pipelines.foodstuffs_transform import FoodstuffsItemTransformPipeline


MOBILE_CATEGORIES_PATH = '/prod/mobile/v1/products/category'
MOBILE_API_HEADERS = {
  'Host': '6q1kn3c1gb-dsn.algolia.net',
  'User-Agent': 'clubcard/257 CFNetwork/1331.0.7 Darwin/21.4.0',
  'x-algolia-api-key': '5c9ca0c058cbd3170b9a73605b1cc46c',
  'Accept': '*/*',
  'Accept-Language': 'en-AU,en;q=0.9',
  'x-algolia-application-id': '6Q1KN3C1GB',
  'Content-Type': 'application/json'
}
MOBILE_API_PAYLOAD = {
    "query": "",
    "facets": [
        "category1SI",
        "brand",
        "onPromotion",
        "si_marketinginitiatives"
    ],
    "attributesToHighlight": [],
    "sortFacetValuesBy": "alpha",
    "maxValuesPerFacet": 1000,
    "hitsPerPage": 100,
    "facetFilters": [
        [
            "category1SI:Beer & Cider Awards",
            "category1SI:Beer & Cider",
            "category1SI:Wine"
        ]
    ]
}
MOBILE_API_PAYLOAD_WITH_CAT_TEMPLATE = {
    "query": "",
    "facets": [
        "category1SI",
        "brand",
        "onPromotion",
        "si_marketinginitiatives"
    ],
    "attributesToHighlight": [],
    "sortFacetValuesBy": "alpha",
    "maxValuesPerFacet": 1000,
    "hitsPerPage": 100,
    "facetFilters": [
    ]
}


class AbstractFoodstuffsSpider(AbstractBrandSpider):

    # dictionary to map Item fields to jmes json query paths
    item_jmes_paths = {
        'name': "join(' ', [brand, DisplayName])",
        'brand': "brand",
        'category': 'category1',
    }

    store_jmes_paths = {
        'name': 'name',
        'internalId': 'id',
        'url': 'id'
    }

    location_jmes_paths = {
        'lattitude': 'latitude',
        'longitude': 'longitude',
        'address': 'address'
    }

    def __init__(self, pisspricer_brand_name, base_url, base_mobile_api_url, mobile_items_path, *args, **kwargs):
        super(AbstractFoodstuffsSpider, self).__init__(pisspricer_brand_name, *args, **kwargs)

        # set constants
        self.allowed_domains = [urlparse(base_url).netloc, urlparse(base_mobile_api_url).netloc, 'fsimg.co.nz']
        self.web_api_url = urljoin(base_url, "/CommonApi")
        self.mobile_api_url = base_mobile_api_url
        self.mobile_items_path = mobile_items_path
        self.start_urls = [f"{self.web_api_url}/Store/GetStoreList"]
        self.store_dict = dict()

        # get skus that have an image set
        pisspricer = PisspricerAdmin()
        self.skus_with_image = pisspricer.get_existing_image_set(self.brand_id)

    def parse(self, response, **kwargs):
        # get the ID of all New World stores from API
        stores_json = json.loads(response.text)

        # iterate over each store
        for store in stores_json['stores']:
            # check the store can be accessed
            on_boarding = store.get('onboardingMode')
            delivery = store.get('delivery')
            click_and_collect = store.get('clickAndCollect')
            # if (not on_boarding) and (delivery or click_and_collect):

            # iterate over each location field
            location_loader = ItemLoader(item=Location())
            location_loader.default_output_processor = TakeFirst()
            for (field, path) in self.location_jmes_paths.items():
                location_loader.add_value(field, SelectJmes(path)(store))

            # create an ItemLoader to populate a StoreItem item
            store_loader = ItemLoader(item=Store())
            store_loader.default_output_processor = TakeFirst()
            for (field, path) in self.store_jmes_paths.items():
                store_loader.add_value(field, SelectJmes(path)(store))
            store_loader.add_value('location', location_loader.load_item())

            store_item = store_loader.load_item()
            self.store_dict[store_item['internalId'].replace('-', '')] = store_item

        categories = self.get_categories()
        for category1, sub_cats in categories:
            for category2 in sub_cats:
                yield self.create_item_request(category1, category2)

    @staticmethod
    def get_store_cookies(store):
        return {"STORE_ID_V2": store['id'], "eCom_STORE_ID": store['id']}

    def parse_mobile_query_response(self, response):
        resp_json = json.loads(response.text)
        n_hits = resp_json['nbHits']
        if n_hits > 1000:
            hi = "jio"
        for item_json in resp_json['hits']:

            # create an ItemLoader to populate an Item
            item_loader = ItemLoader(item=Item())
            item_loader.default_output_processor = TakeFirst()

            # iterate over each item json field and populate
            for (field, path) in self.item_jmes_paths.items():
                item_loader.add_value(field, SelectJmes(path)(item_json))

            # volume
            size = item_json.get('netContentDisplay', "")
            matched_volume = re.compile('[0-9]+ml', re.IGNORECASE).match(size)
            if matched_volume:
                item_loader.add_value('volumeEach', matched_volume.group().rstrip("ml"))

            # pack size
            matched_pack_size = re.compile('[0-9]+(( ?x)|(pk))', re.IGNORECASE).match(size)
            if matched_pack_size:
                pack_size = matched_pack_size.group().rstrip("pk").rstrip("x").rstrip("X").rstrip(" ")
                item_loader.add_value('packSize', pack_size)

            # barcodes
            barcodes_str = item_json.get("barcodes")
            item_loader.add_value('barcodes', barcodes_str.split(','))

            # internal id
            internal_id = item_json.get("objectID")

            # get image if its new, else load item
            image_url = self.get_image_url(internal_id)
            if self._image_already_exists(image_url):
                for item in self.load_item_prices(item_loader, item_json, internal_id):
                    yield item
            else:
                yield response.follow(
                    image_url,
                    callback=self.load_image,
                    meta={'item_loader': item_loader, 'item_json': item_json, 'internal_id': internal_id},
                    dont_filter=True)

        page = resp_json['page']
        n_pages = resp_json['nbPages']
        if (page + 1) < n_pages:
            category1 = response.meta.get('category1')
            category2 = response.meta.get('category2')
            yield self.create_item_request(category1, category2, page=page + 1)

    def create_item_request(self, category1, category2, page=None):
        body = MOBILE_API_PAYLOAD_WITH_CAT_TEMPLATE
        body['facetFilters'] = [[f"category1SI:{category1}"], [f"category2SI:{category2}"]]
        if page is not None:
            body['page'] = page
        return Request(
            urljoin(self.mobile_api_url, self.mobile_items_path),
            callback=self.parse_mobile_query_response,
            headers=MOBILE_API_HEADERS,
            body=json.dumps(body),
            method='POST',
            dont_filter=True,
            meta={'category1': category1, 'category2': category2, 'page': page}
        )

    @staticmethod
    def get_image_url(internal_id):
        stripped_id = re.compile('[0-9]+-EA').match(internal_id).group().rstrip("-EA")
        return f"https://a.fsimg.co.nz/product/retail/fan/image/400x400/{stripped_id}.png"

    def load_item_prices(self, item_loader, item_json, internal_id):
        for store_id_str, price_str in item_json['prices'].items():
            item_price_loader = ItemLoader(item=ItemPrice())
            item_price_loader.default_output_processor = TakeFirst()
            item_price_loader.add_value('price', float(price_str))
            item_price_loader.add_value('internalSku', internal_id)
            # todo: sale price
            store = self.store_dict[store_id_str]

            full_item_loader = ItemLoader(item=FullItem())
            full_item_loader.default_output_processor = TakeFirst()
            full_item_loader.add_value('itemPrice', item_price_loader.load_item())
            full_item_loader.add_value('store', store)
            full_item_loader.add_value('item', item_loader.load_item())
            full_item = full_item_loader.load_item()
            self.logger.debug(f"Item loaded: {full_item.get('item').get('name')}")

            yield full_item

    def load_image(self, response):
        loader = response.meta.get('item_loader')

        # process image and encode as base64 string
        image_file = process_response_content(response.body)
        image = base64.b64encode(image_file)

        # add image to loader and load item
        loader.add_value('image', image)
        for item in self.load_item_prices(loader, response.meta.get('item_json'), response.meta.get('internal_id')):
            yield item

    def load_item(self, loader):
        loaded_item = loader.load_item()
        self.logger.debug(f"Item loaded: {loaded_item.get('productName')}")
        transformed_item = FoodstuffsItemTransformPipeline().process_item(loaded_item, self)
        return transformed_item

    def _image_already_exists(self, internal_sku):
        """ Checks if the image already exists on pisspricer """
        return internal_sku in self.skus_with_image

    @staticmethod
    def get_categories() -> list:
        cat_json = requests.get(urljoin("https://api-prod.prod.fsniwaikato.kiwi", MOBILE_CATEGORIES_PATH),
                                params={"storeId": "81f807e9-1879-484c-b27e-ded56245c6a4"}
                                ).json()
        wine = "Wine"
        beer_cider = "Beer & Cider"
        beer_wine_children = next(filter(lambda cat: cat['name'] == "Beer, Cider & Wine", cat_json))['children']
        beer_children = next(filter(lambda cat: cat['name'] == beer_cider, beer_wine_children))['children']
        wine_children = next(filter(lambda cat: cat['name'] == wine, beer_wine_children))['children']
        return [
            (wine, [cat['name'] for cat in wine_children]),
            (beer_cider, [cat['name'] for cat in beer_children])
        ]
