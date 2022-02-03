import requests
from urllib.parse import urljoin
from .singleton import Singleton
from .environment import Environment


class PisspricerAdmin(metaclass=Singleton):

    def __init__(self):

        env = Environment()
        email = env[env.EMAIL_KEY]

        login_json = {"email": email, "password": env[env.PASSWORD_KEY]}
        res = requests.post(urljoin(env[env.BASE_URL_KEY], 'users/login'), json=login_json)

        if not res.ok:
            raise Exception(f"Login to Pisspricer API failed. Email: '{email}'")
        res_json = res.json()
        token = res_json["authToken"]
        self.auth_headers = {"X-Authorization": token}
