import json
import requests
from urllib.parse import urljoin
from ..services.pisspricer import PisspricerAdmin
from ..services.environment import Environment
import logging
from scrapy.exporters import PythonItemExporter


class SavePipeline:

    def __init__(self):
        pisspricer = PisspricerAdmin()
        self.api_base_url = Environment()[Environment.BASE_URL_KEY]
        self.session = requests.Session()
        self.session.headers.update(pisspricer.auth_headers)

    def _get_exporter(self, **kwargs):
        return PythonItemExporter(binary=False, **kwargs)

    def process_item(self, item, spider):
        url = urljoin(self.api_base_url, f'brands/{spider.brand_id}/fullitem')
        ie = self._get_exporter()
        body = ie.export_item(item)

        logging.debug(f"Putting item: {body}")

        res = self.session.put(url, json=body)
        if res.status_code not in [200, 201]:
            logging.error(f"Error from pisspricer api: {res.reason}")
        return item
