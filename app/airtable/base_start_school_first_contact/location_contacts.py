from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableLocationContactFields(BaseModel):
    location: Optional[str] = Field(alias="Location")
    location_type: Optional[str] = Field(alias="Location Type")
    city_radius: Optional[int] = Field(alias="City Radius")
    first_contact_email: Optional[str] = Field(alias="First Contact Email")
    assigned_rse: Optional[str] = Field(alias="Assigned RSE")
    assigned_rse_name: Optional[str] = Field(alias="Assigned RSE Name")
    hub: Optional[str] = Field(alias="Hub")
    hub_name: Optional[str] = Field(alias="Hub Name")
    latitude: Optional[float] = Field(alias="Latitude")
    longitude: Optional[float] = Field(alias="Longitude")

    # reusable validator
    _get_first_or_default_none = validator(
        "assigned_rse",
        "assigned_rse_name",
        "hub",
        "hub_name",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)


class AirtableLocationContactResponse(AirtableResponse):
    fields: AirtableLocationContactFields


class ListAirtableLocationContactResponse(ListAirtableResponse):
    __root__: list[AirtableLocationContactResponse]
