import requests
from urllib.parse import urljoin
from ..services.pisspricer import PisspricerAdmin
from ..services.environment import Environment
from ..services.summarisation import Summarisation
import logging
from scrapy.exporters import PythonItemExporter


class SavePipeline:

    logger = logging.getLogger(__name__)

    def __init__(self):
        pisspricer = PisspricerAdmin()
        self.api_base_url = Environment()[Environment.BASE_URL_KEY]
        self.session = requests.Session()
        self.session.headers.update(pisspricer.auth_headers)
        self.summary = Summarisation()

    def _get_exporter(self, **kwargs):
        return PythonItemExporter(binary=False, **kwargs)

    def process_item(self, item, spider):
        url = urljoin(self.api_base_url, f'brands/{spider.brand_id}/fullitem')

        # export item to json body
        ie = self._get_exporter()
        body = ie.export_item(item)

        self.logger.debug(f"Putting item: {body}")
        res = self.session.put(url, json=body)

        if res.status_code not in [200, 201]:
            self.logger.error(f"Error from pisspricer api: {res.reason}. \nItem: {item}")
            self.summary.log_fail(spider.brand_id, res.status_code, res.reason, body)
        else:
            self.logger.info(f"Successfully saved item: {res.json()}")
            self.summary.log_success(spider.brand_id, res.json())

        return item
