from .foodstuffs import AbstractFoodstuffsSpider


class PaknsaveSpider(AbstractFoodstuffsSpider):

    name = "paknsave"

    def __init__(self, *args, **kwargs):
        super(PaknsaveSpider, self).__init__("PAK'nSAVE", "https://www.paknsave.co.nz", *args, **kwargs)
