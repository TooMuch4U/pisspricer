from .foodstuffs import AbstractFoodstuffsSpider


class NewWorldSpider(AbstractFoodstuffsSpider):

    name = "newworld"

    def __init__(self, *args, **kwargs):
        super(NewWorldSpider, self).__init__("New World", "https://www.newworld.co.nz", *args, **kwargs)
