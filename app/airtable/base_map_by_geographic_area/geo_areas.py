from typing import Optional

from pydantic import Field, validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGeoAreaFields(BaseModel):
    area_name: Optional[str] = Field(alias="Geographic Area")
    area_type: Optional[str] = Field(alias="Area Type")
    city_radius: Optional[int] = Field(alias="City Radius", default=30)
    polygon_coordinates: Optional[str] = Field(alias="Polygon Coordinates")
    assigned_rse: Optional[str] = Field(alias="Assigned RSE")
    assigned_rse_synced_record_id: Optional[str] = Field(alias="Assigned RSE Synced Record ID")
    assigned_rse_name: Optional[str] = Field(alias="Assigned RSE Name")
    hub_synced_record_id: Optional[str] = Field(alias="Hub Synced Record ID")
    hub_name: Optional[str] = Field(alias="Associated Hub Name")
    latitude: Optional[float] = Field(alias="Latitude")
    longitude: Optional[float] = Field(alias="Longitude")
    geocode: Optional[str] = Field(alias="Geocode")
    auto_response_email_templates: Optional[list[str]] = Field(alias="Auto-Response Email Templates")

    # reusable validator
    _get_first_or_default_none = validator(
        "assigned_rse",
        "assigned_rse_synced_record_id",
        "assigned_rse_name",
        "hub_synced_record_id",
        "hub_name",
        pre=True,
        allow_reuse=True,
    )(get_first_or_default_none)


class AirtableGeoAreaResponse(AirtableResponse):
    fields: AirtableGeoAreaFields


class ListAirtableGeoAreaResponse(ListAirtableResponse):
    __root__: list[AirtableGeoAreaResponse]
