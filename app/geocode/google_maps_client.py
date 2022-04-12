from typing import Optional

from cachetools import cached, TTLCache
import googlemaps

from app import const

from .geocode_models import ListPlace, Place
from ..utils.singleton import Singleton


class GoogleMapsAPI(metaclass=Singleton):
    def __init__(self, api_key=const.GOOGLE_CLOUD_API_KEY):
        self.client_api = googlemaps.Client(key=api_key)

    @cached(cache=TTLCache(maxsize=256, ttl=60 * 60 * 24 * 31))  # Cache for a month
    def geocode_address(self, address) -> Optional[Place]:
        response = self.client_api.geocode(address)
        if len(response) > 0:
            return ListPlace.parse_obj(response).__root__[0]

        return None
