from urllib.parse import urljoin
from ..services.pisspricer import PisspricerAdmin
from ..services.environment import Environment
from ..services.summarisation import Summarisation
import logging
from scrapy.exporters import PythonItemExporter
from aiohttp import ClientSession
from scrapy.exceptions import DropItem


class SavePipeline:

    logger = logging.getLogger(__name__)
    ERROR_STATUSES = {x for x in range(100, 600)} - {200, 201}

    def __init__(self):
        pisspricer = PisspricerAdmin()
        self.api_base_url = Environment()[Environment.BASE_URL_KEY]
        self.session = ClientSession()
        self._set_auth(pisspricer)
        self.summary = Summarisation()

    def _set_auth(self, pisspricer):
        self.session.headers.update(pisspricer.auth_headers)

    def _re_auth(self):
        self.logger.info('Re-authing')
        pisspricer = PisspricerAdmin()
        pisspricer.login()
        self._set_auth(pisspricer)

    def _get_exporter(self, **kwargs):
        return PythonItemExporter(binary=False, **kwargs)

    async def process_item(self, item, spider):
        # todod make async
        url = urljoin(self.api_base_url, f'brands/{spider.brand_id}/fullitem')

        # export item to json body
        ie = self._get_exporter()
        body = ie.export_item(item)

        self.logger.debug(f"Putting item: {body}")
        retry = True
        try_count = 0
        while retry and try_count <= 1:
            retry = False
            try_count += 1

            async with await self.session.put(url, json=body) as res:

                if res.status == 401:
                    # try again
                    self._re_auth()
                    self.logger.debug(f"401 status, trying again: {body}")
                    retry = True

                elif res.status not in [200, 201]:
                    self.logger.error(f"Error from pisspricer api: {res.reason}. \nItem: {item}")
                    self.summary.log_fail(spider.brand_id, res.status, res.reason, body)
                    return item
                else:
                    res_data = await res.json()
                    self.logger.info(f"Successfully saved item: {res_data}")
                    self.summary.log_success(spider.brand_id, res_data)
                    return item

        return item
