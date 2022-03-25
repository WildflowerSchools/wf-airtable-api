from typing import Optional

from pydantic import BaseModel


class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: list[str]


class LatLngLiteral(BaseModel):
    lat: float
    lng: float

    def as_tuple(self):
        return tuple([self.lat, self.lng])


class Bounds(BaseModel):
    northeast: LatLngLiteral
    southwest: LatLngLiteral


class Geometry(BaseModel):
    location: LatLngLiteral
    viewport: Bounds
    location_type: Optional[str]


class Place(BaseModel):
    address_components: Optional[list[AddressComponent]]
    formatted_address: Optional[str]
    geometry: Optional[Geometry]
    place_id: Optional[str]
    types: Optional[list[str]]

    def get_locality_component(self):
        for ac in self.address_components:
            if 'locality' in ac.types:
                return ac

        return None

    def get_colloquial_area_component(self):
        for ac in self.address_components:
            if 'colloquial_area' in ac.types:
                return ac

        return None

    def get_state_component(self):
        for ac in self.address_components:
            if 'administrative_area_level_1' in ac.types:
                return ac

        return None

    def get_country_component(self):
        for ac in self.address_components:
            if 'country' in ac.types:
                return ac

        return None


class ListPlace(BaseModel):
    __root__: list[Place]
