import scrapy
import json
import requests


class NewWorldSpider(scrapy.Spider):
    name = 'newworld'
    allowed_domains = ['newworld.co.nz']
    start_urls = ['https://www.newworld.co.nz/']
    api_url = "https://www.newworld.co.nz/CommonApi"

    def parse(self, response):
        # get the ID of all New World stores from API
        stores_json = requests.get(f"{self.api_url}/Store/GetStoreList").json()

        beer_wine_page = "https://www.newworld.co.nz/shop/category/beer-cider-and-wine?ps=50"

        # iterate over each store
        for store in stores_json['stores']:
            # check the store can be accessed
            if not store['onboardingMode']:
                yield response.follow(beer_wine_page,
                                      callback=self.parse_beer_wine_page,
                                      cookies={"STORE_ID_V2": store['id'],
                                               "eCom_STORE_ID": store['id']},
                                      meta=store,
                                      dont_filter=True)

    def parse_beer_wine_page(self, response):
        products = response.css(
            'div.l-columns__column.l-columns__column--one-l.l-columns__column--one-half-m.u-margin-bottom-x2')
        for product in products:
            data_text = product.css(
                'div.js-product-card-footer.fs-product-card__footer-container::attr(data-options)').get()
            data = json.loads(data_text)
            name = data['productName']
            price = data['ProductDetails']['PricePerItem']
            if data['ProductDetails']['PriceMode'] != 'ea':
                raise Exception("wrong price mode")
            sale = data['ProductDetails']['ClubCardPriceText'] == 'Club Deal'
            yield {
                'name': name,
                'price': price,
                'store': response.meta['name']
            }

        next_page = response.css('a.fs-pagination__btn--next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_beer_wine_page)


