import requests
from urllib.parse import urljoin
from .singleton import Singleton
from .environment import Environment


class PisspricerAdmin(metaclass=Singleton):

    def __init__(self):
        self.auth_headers = None
        self.login()

    def login(self):
        env = Environment()
        email = env[env.EMAIL_KEY]

        login_json = {"email": email, "password": env[env.PASSWORD_KEY]}
        res = requests.post(urljoin(env[env.BASE_URL_KEY], 'users/login'), json=login_json)

        if not res.ok:
            raise Exception(f"Login to Pisspricer API failed. Email: '{email}'")
        res_json = res.json()
        token = res_json["authToken"]
        self.auth_headers = {"X-Authorization": token}

    def get_brand_id(self, name):
        url = urljoin(Environment()[Environment.BASE_URL_KEY], 'brands')
        res = requests.get(url, headers=self.auth_headers)
        for brand in res.json():
            if brand['name'] == name:
                return brand['brandId']
        raise Exception(f"Brand with name '{name}' doesn't exist")

    def get_existing_image_set(self, brand_id):
        """ Takes a brand ID and returns a set of internal id's that have an image already
        :param brand_id: Id of brand for the internal id's
        :return: Set of internal id's
        """
        url = urljoin(Environment()[Environment.BASE_URL_KEY], f'brands/{brand_id}/items')
        res = requests.get(url, headers=self.auth_headers)
        internal_skus_with_image = set()
        for item in res.json():
            if item["hasImage"] == 1:
                internal_skus_with_image.add(item["internalSku"])
        return internal_skus_with_image
