from .foodstuffs import AbstractFoodstuffsSpider


class PaknsaveSpider(AbstractFoodstuffsSpider):

    name = "paknsave"

    def __init__(self, *args, **kwargs):
        super(PaknsaveSpider, self).__init__(
            "PAK'nSAVE",
            "https://www.paknsave.co.nz",
            "https://6q1kn3c1gb-dsn.algolia.net",
            "/1/indexes/prod-online-pns-products-index/query",
            *args, **kwargs)