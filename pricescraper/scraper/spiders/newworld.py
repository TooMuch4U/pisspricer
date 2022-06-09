from .foodstuffs import AbstractFoodstuffsSpider


class NewWorldSpider(AbstractFoodstuffsSpider):

    name = "newworld"

    def __init__(self, *args, **kwargs):
        super(NewWorldSpider, self).__init__(
            "New World",
            "https://www.newworld.co.nz",
            "https://6q1kn3c1gb-dsn.algolia.net",
            "/1/indexes/prod-online-nw-products-index/query",
            *args, **kwargs)
