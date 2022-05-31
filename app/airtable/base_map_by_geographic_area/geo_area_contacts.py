from typing import Optional

from pydantic import Field, validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGeoAreaContactFields(BaseModel):
    area_name: Optional[str] = Field(alias="Area Name")
    area_type: Optional[str] = Field(alias="Area Type")
    city_radius: Optional[int] = Field(alias="City Radius", default=30)
    polygon_coordinates: Optional[str] = Field(alias="Polygon Coordinates")
    first_contact_email: Optional[str] = Field(alias="First Contact Email")
    assigned_rse: Optional[str] = Field(alias="Assigned RSE")
    assigned_rse_synced_record_id: Optional[str] = Field(alias="Assigned RSE Synced Record ID")
    assigned_rse_name: Optional[str] = Field(alias="Assigned RSE Name")
    hub: Optional[str] = Field(alias="Hub")
    hub_synced_record_id: Optional[str] = Field(alias="Hub Synced Record ID")
    hub_name: Optional[str] = Field(alias="Hub Name")
    sendgrid_template_id: Optional[str] = Field(alias="Sendgrid Template ID")
    latitude: Optional[float] = Field(alias="Latitude")
    longitude: Optional[float] = Field(alias="Longitude")
    geocode: Optional[str] = Field(alias="Geocode")

    # reusable validator
    _get_first_or_default_none = validator(
        "area_name",
        "area_type",
        "polygon_coordinates",
        "city_radius",
        "assigned_rse",
        "assigned_rse_synced_record_id",
        "assigned_rse_name",
        "hub",
        "hub_synced_record_id",
        "hub_name",
        "latitude",
        "longitude",
        "geocode",
        pre=True,
        allow_reuse=True,
    )(get_first_or_default_none)


class AirtableGeoAreaContactResponse(AirtableResponse):
    fields: AirtableGeoAreaContactFields


class ListAirtableGeoAreaContactResponse(ListAirtableResponse):
    __root__: list[AirtableGeoAreaContactResponse]
