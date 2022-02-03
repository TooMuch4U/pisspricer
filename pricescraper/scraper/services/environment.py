from .singleton import Singleton
from os.path import join, dirname
from dotenv import load_dotenv
import os


class Environment(metaclass=Singleton):

    EMAIL_KEY = 'pisspricer.email'
    PASSWORD_KEY = 'pisspricer.password'
    BASE_URL_KEY = 'pisspricer.url'
    REQUIRED = [EMAIL_KEY, PASSWORD_KEY, BASE_URL_KEY]

    def __init__(self):
        dotenv_path = join(dirname(__file__), '../../.env')
        load_dotenv(dotenv_path)
        self._env_items = dict(os.environ.items())

        # check for missing env variables
        missing = self.REQUIRED - self._env_items.keys()
        if any(missing):
            raise Exception(f'Missing environment variables: {", ".join(missing)}')

    def __getitem__(self, key):
        return self._env_items[key]
