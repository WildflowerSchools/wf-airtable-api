from typing import Optional, Union

from pydantic import Field, field_validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse, ListAirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableGeoAreaContactFields(BaseModel):
    area_name: Optional[str] = Field(None, alias="Area Name")
    area_type: Optional[str] = Field(None, alias="Area Type")
    city_radius: Optional[int] = Field(alias="City Radius", default=30)
    polygon_coordinates: Optional[str] = Field(None, alias="Polygon Coordinates")
    first_contact_email: Optional[str] = Field(None, alias="First Contact Email")
    assigned_rse: Optional[str] = Field(None, alias="Assigned RSE")
    assigned_rse_synced_record_id: Optional[str] = Field(None, alias="Assigned RSE Synced Record ID")
    assigned_rse_name: Optional[str] = Field(None, alias="Assigned RSE Name")
    # hub: Optional[str] = Field(None, alias="Hub")
    # hub_synced_record_id: Optional[str] = Field(None, alias="Hub Synced Record ID")
    # hub_name: Optional[str] = Field(None, alias="Hub Name")
    sendgrid_template_id: Optional[str] = Field(None, alias="Sendgrid Template ID")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    geocode: Optional[str] = Field(None, alias="Geocode")
    marketing_source: Optional[str] = Field(None, alias="Marketing Source")
    # auto_response_email_template_ids: Optional[list[str]] = Field(alias="Auto-Response Email Template IDs")

    @field_validator(
        "area_name",
        "area_type",
        "polygon_coordinates",
        "city_radius",
        "assigned_rse",
        "assigned_rse_synced_record_id",
        "assigned_rse_name",
        # "hub",
        # "hub_synced_record_id",
        # "hub_name",
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
    #     "assigned_rse",
    #     "assigned_rse_synced_record_id",
    #     "assigned_rse_name",
    #     "hub",
    #     "hub_synced_record_id",
    #     "hub_name",
    #     "latitude",
    #     "longitude",
    #     "geocode",
    #     pre=True,
    #     allow_reuse=True,
    # )(get_first_or_default_none)


class AirtableGeoAreaContactResponse(AirtableResponse):
    fields: AirtableGeoAreaContactFields


class ListAirtableGeoAreaContactResponse(ListAirtableResponse):
    root: list[AirtableGeoAreaContactResponse]
