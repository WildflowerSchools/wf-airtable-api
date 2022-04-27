from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGeoAreaTargetCommunityFields(BaseModel):
    area_name: Optional[str] = Field(alias="Area Name")
    area_type: Optional[str] = Field(alias="Area Type")
    city_radius: Optional[int] = Field(alias="City Radius", default=30)
    polygon_coordinates: Optional[str] = Field(alias="Polygon Coordinates")
    hub_synced_record_id: Optional[str] = Field(alias="Associated Hub Synced Record ID")
    hub_name: Optional[str] = Field(alias="Associated Hub")
    target_community: Optional[str] = Field(alias="Target Community")
    target_community_name: Optional[str] = Field(alias="Target Community Name")
    target_community_synced_record_id: Optional[str] = Field(alias="Target Community Synced Record ID")
    latitude: Optional[float] = Field(alias="Latitude")
    longitude: Optional[float] = Field(alias="Longitude")
    geocode: Optional[str] = Field(alias="Geocode")

    # reusable validator
    _get_first_or_default_none = validator(
        "area_name",
        "area_type",
        "polygon_coordinates",
        "city_radius",
        "target_community",
        "target_community_name",
        "target_community_synced_record_id",
        "hub_name",
        "hub_synced_record_id",
        "latitude",
        "longitude",
        "geocode",
        pre=True,
        allow_reuse=True,
    )(get_first_or_default_none)


class AirtableGeoAreaTargetCommunityResponse(AirtableResponse):
    fields: AirtableGeoAreaTargetCommunityFields


class ListAirtableGeoAreaTargetCommunityResponse(ListAirtableResponse):
    __root__: list[AirtableGeoAreaTargetCommunityResponse]
