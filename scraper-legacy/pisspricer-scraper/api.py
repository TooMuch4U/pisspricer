import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from urllib.parse import urljoin

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.getenv('pisspricer.url')
email = os.environ.get('pisspricer.email')
password = os.environ.get('pisspricer.password')

res = requests.post(urljoin(url, '/users/login'), json={"email": email, "password": password})

if not res.ok:
    raise Exception(f"Login to API failed ('{email}', '{password}', '{url}')")
res_json = res.json()
token = res_json["authToken"]
headers = {"X-Authorization": token}
