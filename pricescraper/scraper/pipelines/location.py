import logging
from aiohttp_retry import RetryClient, ExponentialRetry
from async_lru import alru_cache
from scrapy.exceptions import DropItem
from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectorError, ClientOSError
import asyncio

from ..services.ratelimiter import RateLimiter


class LocationPipeline:

    API_ADDRESS_TEMPLATE = "https://photon.komoot.io/api?q={}, New Zealand"
    API_GEO_TEMPLATE = "https://photon.komoot.io/reverse?lon={0}&lat={1}"
    ERROR_STATUSES = {x for x in range(100, 600)} - {200}
    logger = logging.getLogger(__name__)

    def __init__(self):
        retry_options = ExponentialRetry(attempts=3, statuses=self.ERROR_STATUSES, start_timeout=1)
        self.session = RateLimiter(RetryClient(retry_options=retry_options))

    async def process_item(self, item, _):
        location = item['store']['location']

        if all([
            location.get('longitude'),
            location.get('lattitude'),
            location.get('region'),
            location.get('postcode'),
            location.get('address')
        ]):
            return item

        if location.get('lattitude') and location.get('longitude'):
            new_location = await self.get_from_coordinates(location['longitude'], location['lattitude'])
            item['store']['location'] = self.fill_in_missing_fields(location, new_location)

        elif location.get('address'):
            new_location = await self.get_from_address(location)
            item['store']['location'] = self.fill_in_missing_fields(location, new_location)

        else:
            raise Exception("Location address and coordinates not set")

        return item

    @alru_cache(maxsize=32)
    async def get_from_coordinates(self, lng, lat):
        url = LocationPipeline.API_GEO_TEMPLATE.format(lng, lat)
        attempt_count = 0
        while True:
            attempt_count += 1
            try:
                async with await self.session.get(url) as resp:
                    LocationPipeline.logger.info(f"Status code: {resp.status} for {resp.url}")
                    if resp.status not in self.ERROR_STATUSES:
                        return await resp.json(content_type=None)
                    raise DropItem(f"Location api returned status code {resp.status} for {url}")
            except (ServerDisconnectedError, ClientConnectorError, ClientOSError) as err:
                print("Oops, the server connection was dropped on ", url, ": ", err)
                await asyncio.sleep(10)
                if attempt_count > 3:
                    raise err

    async def get_from_address(self, location):
        # TODO: This method needs updated to use the same syntax as the get_from_coordinates method when it gets used
        raise Exception("TODO: This method needs updated to use the same syntax as the get_from_coordinates method when it gets used")
        address = location['address']

        if location.get('region'):
            address += f", {location['region']}"
        if location.get('postcode'):
            address += f", {location['postcode']}"

        url = LocationPipeline.API_ADDRESS_TEMPLATE.format(address)
        resp = await self.session.get(url)
        LocationPipeline.logger.info(f"Status code: {resp.status} for {resp.url}")
        if resp.status not in self.ERROR_STATUSES:
            return await resp.json(content_type=None)
        raise DropItem(f"Location api returned status code {resp.status} for {url}")

    @staticmethod
    def fill_in_missing_fields(location, new_location):
        LocationPipeline.logger.debug(f"Location api returned {new_location}")

        new_location_json = new_location.get('features')[0]
        location_properties = new_location_json.get('properties')

        if not location.get('lattitude'):
            coords = new_location_json.get('geometry').get('coordinates')
            location['lattitude'] = coords[0]
            location['longitude'] = coords[1]
        else:
            if not location.get('address'):
                new_address = f"{location_properties.get('housenumber')} {location_properties.get('street')}"
                location['address'] = new_address

        if not location.get('postcode'):
            postcode = int_if_possible(location_properties.get('postcode'))
            if postcode == "NTL 0110":
                postcode = 110
            location['postcode'] = postcode

        if not location.get('region'):
            location['region'] = location_properties.get('state')

        return location


def int_if_possible(field):
    if field.isdigit():
        return int(field)
    return field
