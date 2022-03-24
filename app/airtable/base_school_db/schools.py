from datetime import date, datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, validator

from app.airtable.attachment import AirtableAttachment
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none, get_first_or_default_dict


class AirtableSchoolFields(BaseModel):
    name: Optional[str] = Field(alias="Name")
    short_name: Optional[str] = Field(alias="Short Name")
    details: Optional[str] = Field(alias="Details")
    logo: Optional[AirtableAttachment] = Field(alias="Logo", default={})
    domain_name: Optional[str] = Field(alias="Email Domain")
    address: Optional[str] = Field(alias="Address")
    latitude: Optional[float] = Field(alias="Latitude")
    longitude: Optional[float] = Field(alias="Longitude")

    ages_served: Optional[list[str]] = Field(alias="Ages served")
    school_calendar: Optional[str] = Field(alias="School calendar")
    school_schedule: Optional[list[str]] = Field(alias="School schedule")
    school_phone: Optional[str] = Field(alias="School Phone")
    school_email: Optional[str] = Field(alias="School Email")
    website: Optional[AnyUrl] = Field(alias="Website")

    hub: Optional[str] = Field(alias="Hub")
    pod: Optional[str] = Field(alias="Pod")
    guides_entrepreneurs: Optional[list[str]] = Field(alias="Guides and Entrepreneurs")
    primary_contacts: Optional[list[str]] = Field(alias="Primary Contacts")
    all_educators: Optional[list[str]] = Field(alias="All Educator Record IDs")
    current_educators: Optional[list[str]] = Field(alias="Current Educator Record IDs")
    current_tls: Optional[list[str]] = Field(alias="Current TL Record IDs")
    founders: Optional[list[str]] = Field(alias="Founder Record IDs")

    status: Optional[str] = Field(alias="School Status")
    ssj_stage: Optional[str] = Field(alias="School Startup Stage")
    began_ssj_at: Optional[date] = Field(alias="Began Startup Journey")
    entered_planning_at: Optional[date] = Field(alias="Entered Planning")
    entered_startup_at: Optional[date] = Field(alias="Entered Startup")
    opened_at: Optional[date] = Field(alias="Opened")
    projected_open: Optional[date] = Field(alias="Projected Open")
    affiliation_status: Optional[str] = Field(alias="Affiliation status")
    affiliated_at: Optional[datetime] = Field(alias="Affiliation date")
    affiliation_agreement: Optional[AirtableAttachment] = Field(alias="Signed Affiliation Agreement", default={})
    nonprofit_status: Optional[str] = Field(alias="Nonprofit status")
    left_network_reason: Optional[str] = Field(alias="Left Network Reason")
    left_network_date: Optional[date] = Field(alias="Left Network Date")

    # reusable validator
    _get_first_or_default_none = validator(
        "hub",
        "pod",
        "address",
        "latitude",
        "longitude",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)

    _get_first_or_default_dict = validator(
        "affiliation_agreement",
        "logo",
        pre=True,
        allow_reuse=True)(get_first_or_default_dict)

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


class ListAirtableSchoolResponse(BaseModel):
    __root__: list[AirtableSchoolResponse]
