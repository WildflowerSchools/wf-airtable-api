from typing import Optional, Union

from pydantic import Field, field_validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGeoAreaTargetCommunityFields(BaseModel):
    area_name: Optional[str] = Field(None, alias="Area Name")
    area_type: Optional[str] = Field(None, alias="Area Type")
    city_radius: Optional[int] = Field(alias="City Radius", default=30)
    polygon_coordinates: Optional[str] = Field(None, alias="Polygon Coordinates")
    hub_synced_record_id: Optional[str] = Field(None, alias="Associated Hub Synced Record ID")
    hub_name: Optional[str] = Field(None, alias="Associated Hub")
    target_community: Optional[str] = Field(None, alias="Target Community")
    target_community_name: Optional[str] = Field(None, alias="Target Community Name")
    target_community_synced_record_id: Optional[str] = Field(None, alias="Target Community Synced Record ID")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    geocode: Optional[str] = Field(None, alias="Geocode")

    @field_validator(
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
        mode="before",
    )
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # reusable validator
    # _get_first_or_default_none = validator(
    #     "area_name",
    #     "area_type",
    #     "polygon_coordinates",
    #     "city_radius",
    #     "target_community",
    #     "target_community_name",
    #     "target_community_synced_record_id",
    #     "hub_name",
    #     "hub_synced_record_id",
    #     "latitude",
    #     "longitude",
    #     "geocode",
    #     pre=True,
    #     allow_reuse=True,
    # )(get_first_or_default_none)


class AirtableGeoAreaTargetCommunityResponse(AirtableResponse):
    fields: AirtableGeoAreaTargetCommunityFields


class ListAirtableGeoAreaTargetCommunityResponse(ListAirtableResponse):
    root: list[AirtableGeoAreaTargetCommunityResponse]
