from typing import Optional

from pydantic import BaseModel, RootModel


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
    location_type: Optional[str] = None


class Place(BaseModel):
    address_components: Optional[list[AddressComponent]] = None
    formatted_address: Optional[str] = None
    geometry: Optional[Geometry] = None
    place_id: Optional[str] = None
    types: Optional[list[str]] = None

    def get_locality_component(self):
        for ac in self.address_components:
            if "locality" in ac.types:
                return ac

        return None

    def get_colloquial_area_component(self):
        for ac in self.address_components:
            if "colloquial_area" in ac.types:
                return ac

        return None

    def get_state_component(self):
        for ac in self.address_components:
            if "administrative_area_level_1" in ac.types:
                return ac

        return None

    def get_country_component(self):
        for ac in self.address_components:
            if "country" in ac.types:
                return ac

        return None


class ListPlace(RootModel):
    root: list[Place]
