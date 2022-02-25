import logging
import aiohttp
from aiohttp_retry import RetryClient


class LocationPipeline:

    API_ADDRESS_TEMPLATE = "https://photon.komoot.io/api?q={}, New Zealand"
    API_GEO_TEMPLATE = "https://photon.komoot.io/reverse?lon={0}&lat={1}"
    ERROR_STATUSES = {x for x in range(100, 600)} - {200}
    logger = logging.getLogger(__name__)

    def __init__(self):
        # photon api has a request limit of 7 per second
        # this limits the number of open requests at a time to 5
        connector = aiohttp.TCPConnector(limit=7)
        self.session = RetryClient(connector=connector)

    def close_spider(self, spider):
        self.session.close()

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
            new_location = await self.get_from_coordinates(location)
            item['store']['location'] = self.fill_in_missing_fields(location, new_location)

        elif location.get('address'):
            new_location = await self.get_from_address(location)
            item['store']['location'] = self.fill_in_missing_fields(location, new_location)

        else:
            raise Exception("Location address and coordinates not set")

        return item

    async def get_from_coordinates(self, location):
        url = LocationPipeline.API_GEO_TEMPLATE.format(location['longitude'], location['lattitude'])
        async with self.session.get(url) as resp:
            LocationPipeline.logger.info(f"Status code: {resp.status} for {resp.url}")
            if resp.status not in self.ERROR_STATUSES:
                return await resp.json(content_type=None)

    async def get_from_address(self, location):
        address = location['address']

        if location.get('region'):
            address += f", {location['region']}"
        if location.get('postcode'):
            address += f", {location['postcode']}"

        url = LocationPipeline.API_ADDRESS_TEMPLATE.format(address)
        async with self.session.get(url) as resp:
            LocationPipeline.logger.info(f"Status code: {resp.status} for {resp.url}")
            if resp.status not in self.ERROR_STATUSES:
                return await resp.json(content_type=None)

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
            location['postcode'] = int(location_properties.get('postcode'))

        if not location.get('region'):
            location['region'] = location_properties.get('state')

        return location
