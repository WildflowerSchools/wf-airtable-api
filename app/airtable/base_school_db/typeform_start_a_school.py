from datetime import datetime
from typing import Optional, Union

from pydantic import ConfigDict, Field, field_validator

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_provided


class CreateAirtableSSJTypeformStartASchool(BaseModel):
    educator: Optional[list[str]] = Field([], alias="Educator")
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="Last Name")
    email: str = Field(alias="Email")
    is_montessori_certified: bool = Field(alias="Is Montessori Certified", default=False)
    is_seeking_montessori_certification: bool = Field(alias="Is Seeking Montessori Certification", default=False)
    montessori_certification_certifier: Optional[str] = Field(None, alias="Montessori Certification Certifier")
    montessori_certification_year: Optional[int] = Field(None, alias="Montessori Certification Year")
    montessori_certification_levels: Optional[str] = Field(None, alias="Montessori Certification Levels")
    school_location_city: str = Field(alias="School Location: City")
    school_location_state: str = Field(alias="School Location: State")
    school_location_country: Optional[str] = Field(None, alias="School Location: Country")
    school_location_community: Optional[str] = Field(None, alias="School Location: Community")
    contact_location_city: str = Field(alias="Contact Location: City")
    contact_location_state: str = Field(alias="Contact Location: State")
    contact_location_country: Optional[str] = Field(None, alias="Contact Location: Country")
    has_interest_in_joining_another_school: bool = Field(alias="Has Interest in Joining Another School", default=False)
    is_willing_to_move: bool = Field(alias="Is Willing to Move", default=False)
    age_classrooms_interested_in_offering: Optional[str] = Field(None, alias="Age Classrooms Interested In Offering")
    is_interested_in_charter: bool = Field(alias="Is Interested in Charter", default=False)
    socio_economic_race_and_ethnicity: Optional[str] = Field(None, alias="Socio-Economic: Race & Ethnicity")
    socio_economic_race_and_ethnicity_other: Optional[str] = Field(None, alias="Socio-Economic: Race & Ethnicity Other")
    socio_economic_lgbtqia_identifying: Optional[str] = Field(None, alias="Socio-Economic: LGBTQIA Identifying")
    socio_economic_pronouns: Optional[str] = Field(None, alias="Socio-Economic: Pronouns")
    socio_economic_pronouns_other: Optional[str] = Field(None, alias="Socio-Economic: Pronouns Other")
    socio_economic_gender: Optional[str] = Field(None, alias="Socio-Economic: Gender")
    socio_economic_gender_other: Optional[str] = Field(None, alias="Socio-Economic: Gender Other")
    socio_economic_household_income: Optional[str] = Field(None, alias="Socio-Economic: Household Income")
    socio_economic_primary_language: Optional[str] = Field(None, alias="Socio-Economic: Primary Language")
    message: str = Field(alias="Message")
    equity_reflection: Optional[str] = Field(None, alias="Equity Reflection")
    receive_communications: bool = Field(alias="Receive Communications", default=False)
    source: Optional[str] = Field(None, alias="Source")
    entry_date: datetime = Field(alias="Entry Date")
    model_config = ConfigDict(populate_by_name=True)

    # @field_validator("educator", mode="before")
    # def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
    #     return get_first_or_default_provided(v)


class AirtableSSJTypeformStartASchoolFields(CreateAirtableSSJTypeformStartASchool):
    response_id: str = Field(alias="Response ID")
    created_at: datetime = Field(alias="Created At")
    model_config = ConfigDict(populate_by_name=True)


class AirtableSSJTypeformStartASchoolResponse(AirtableResponse):
    fields: AirtableSSJTypeformStartASchoolFields
