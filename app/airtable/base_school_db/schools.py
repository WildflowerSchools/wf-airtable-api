from datetime import date
from typing import Optional, Union

from pydantic import HttpUrl, Field, field_validator, RootModel

from app.airtable.attachment import AirtableAttachment
from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none, get_first_or_default_dict


class AirtableSchoolFields(BaseModel):
    name: Optional[str] = Field(None, alias="Name")
    short_name: Optional[str] = Field(None, alias="Short Name")
    details: Optional[str] = Field(None, alias="Details")
    logo: Optional[AirtableAttachment] = Field(alias="Logo", default={})
    domain_name: Optional[str] = Field(None, alias="Email Domain")
    address: Optional[str] = Field(None, alias="Address")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    organizational_unit: Optional[str] = Field(None, alias="Google Workspace Org Unit Path")

    ages_served: Optional[list[str]] = Field(None, alias="Ages served")
    school_calendar: Optional[str] = Field(None, alias="School calendar")
    school_schedule: Optional[list[str]] = Field(None, alias="School schedule")
    school_phone: Optional[str] = Field(None, alias="School Phone")
    school_email: Optional[str] = Field(None, alias="School Email")
    website: Optional[HttpUrl] = Field(None, alias="Website")

    hub: Optional[str] = Field(None, alias="Hub")
    hub_name: Optional[str] = Field(None, alias="Hub Name")
    # pod: Optional[str] = Field(None, alias="Pod")
    # pod_name: Optional[str] = Field(None, alias="Pod Name")
    guides_entrepreneurs: Optional[list[str]] = Field(None, alias="Guides and Entrepreneurs")
    primary_contacts: Optional[list[str]] = Field(None, alias="Primary Contacts")
    all_educators: Optional[list[str]] = Field(None, alias="All Educator Record IDs")
    current_educators: Optional[list[str]] = Field(None, alias="Current Educator Record IDs")
    current_tls: Optional[list[str]] = Field(None, alias="Current TL Record IDs")
    founders: Optional[list[str]] = Field(None, alias="Founder Record IDs")

    status: Optional[str] = Field(None, alias="School Status")
    ssj_stage: Optional[str] = Field(None, alias="School Startup Stage")
    began_ssj_at: Optional[date] = Field(None, alias="Began Startup Journey")
    entered_planning_at: Optional[date] = Field(None, alias="Entered Planning")
    entered_startup_at: Optional[date] = Field(None, alias="Entered Startup")
    opened_at: Optional[date] = Field(None, alias="Opened")
    projected_open: Optional[date] = Field(None, alias="Projected Open")
    affiliation_status: Optional[str] = Field(None, alias="Affiliation status")
    affiliated_at: Optional[date] = Field(None, alias="Affiliation date")
    affiliation_agreement: Optional[AirtableAttachment] = Field(alias="Signed Affiliation Agreement", default={})
    nonprofit_status: Optional[str] = Field(None, alias="Nonprofit status")
    left_network_reason: Optional[str] = Field(None, alias="Left Network Reason")
    left_network_date: Optional[date] = Field(None, alias="Left Network Date")

    @field_validator("hub", "hub_name", "address", "latitude", "longitude", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    @field_validator("affiliation_agreement", "logo", mode="before")
    def _get_first_or_default_dict(cls, v: Union[str, int, float]) -> Union[str, int, float, dict]:
        return get_first_or_default_dict(v)

    #
    # # reusable validator
    # _get_first_or_default_none = validator(
    #     "hub", "hub_name", "pod", "pod_name", "address", "latitude", "longitude", pre=True, allow_reuse=True
    # )(get_first_or_default_none)
    #
    # _get_first_or_default_dict = validator("affiliation_agreement", "logo", pre=True, allow_reuse=True)(
    #     get_first_or_default_dict
    # )

    def get_logo_url(self, default=None):
        if isinstance(self.logo, AirtableAttachment):
            return self.logo.url
        else:
            return default

    def get_affiliation_agreement_url(self, default=None):
        if isinstance(self.affiliation_agreement, AirtableAttachment):
            return self.affiliation_agreement.url
        else:
            return default


class AirtableSchoolResponse(AirtableResponse):
    fields: AirtableSchoolFields


class ListAirtableSchoolResponse(RootModel):
    root: list[AirtableSchoolResponse]
