from ..items.pisspricer import FullItem, Item, Location, Store, ItemPrice


class FoodstuffsItemTransformPipeline:

    def process_item(self, item, _):
        new_item = FullItem()
        new_item['itemPrice'] = self.create_item_price(item)
        new_item['store'] = self.create_store(item)
        new_item['item'] = self.create_item(item)
        return new_item

    @staticmethod
    def create_item(item):
        new_item = Item()
        new_item['name'] = item['productName']
        if item.get('image'):
            new_item['image'] = item.get('image')
        if item.get('packSize'):
            new_item['packSize'] = item.get('packSize')
        if item.get('volume'):
            new_item['volumeEach'] = item.get('volume')
        return new_item

    @staticmethod
    def create_item_price(item):
        item_price = ItemPrice()
        if not item.get('basePrice'):
            item_price['price'] = item['price']
        else:
            item_price['salePrice'] = item['price']
            item_price['price'] = item['basePrice']
            if item_price['salePrice'] == item_price['price']:
                del item_price['salePrice']
        item_price['internalSku'] = item['productId']
        return item_price

    @staticmethod
    def create_store(item):
        store = Store()
        store['location'] = FoodstuffsItemTransformPipeline.create_location(item)
        store['name'] = item['store']['name']
        store['internalId'] = item['store']['id']
        store['url'] = item['store']['id']  # url is a required field
        return store

    @staticmethod
    def create_location(item):
        location = Location()
        location['longitude'] = item['store']['longitude']
        location['lattitude'] = item['store']['latitude']
        location['address'] = item['store']['address']
        return location
