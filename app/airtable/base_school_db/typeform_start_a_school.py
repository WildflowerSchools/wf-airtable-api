from datetime import datetime
from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse


class CreateAirtableSSJTypeformStartASchool(BaseModel):
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="Last Name")
    email: str = Field(alias="Email")
    is_montessori_certified: bool = Field(alias="Is Montessori Certified", default=False)
    is_seeking_montessori_certification: bool = Field(alias="Is Seeking Montessori Certification", default=False)
    montessori_certification_certifier: Optional[str] = Field(alias="Montessori Certification Certifier")
    montessori_certification_year: Optional[int] = Field(alias="Montessori Certification Year")
    montessori_certification_levels: Optional[str] = Field(alias="Montessori Certification Levels")
    school_location_city: str = Field(alias="School Location: City")
    school_location_state: str = Field(alias="School Location: State")
    school_location_country: Optional[str] = Field(alias="School Location: Country")
    school_location_community: Optional[str] = Field(alias="School Location: Community")
    contact_location_city: str = Field(alias="Contact Location: City")
    contact_location_state: str = Field(alias="Contact Location: State")
    contact_location_country: Optional[str] = Field(alias="Contact Location: Country")
    has_interest_in_joining_another_school: bool = Field(alias="Has Interest in Joining Another School", default=False)
    is_willing_to_move: bool = Field(alias="Is Willing to Move", default=False)
    age_classrooms_interested_in_offering: Optional[str] = Field(alias="Age Classrooms Interested In Offering")
    socio_economic_race_and_ethnicity: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity")
    socio_economic_race_and_ethnicity_other: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity Other")
    socio_economic_lgbtqia_identifying: Optional[str] = Field(alias="Socio-Economic: LGBTQIA Identifying")
    socio_economic_pronouns: Optional[str] = Field(alias="Socio-Economic: Pronouns")
    socio_economic_pronouns_other: Optional[str] = Field(alias="Socio-Economic: Pronouns Other")
    socio_economic_gender: Optional[str] = Field(alias="Socio-Economic: Gender")
    socio_economic_gender_other: Optional[str] = Field(alias="Socio-Economic: Gender Other")
    socio_economic_household_income: Optional[str] = Field(alias="Socio-Economic: Household Income")
    socio_economic_primary_language: Optional[str] = Field(alias="Socio-Economic: Primary Language")
    message: str = Field(alias="Message")
    equity_reflection: Optional[str] = Field(alias="Equity Reflection")
    receive_communications: bool = Field(alias="Receive Communications", default=False)
    source: Optional[str] = Field(alias="Source")
    entry_date: datetime = Field(alias="Entry Date")

    class Config:
        allow_population_by_field_name = True


class AirtableSSJTypeformStartASchoolFields(CreateAirtableSSJTypeformStartASchool):
    response_id: str = Field(alias="Response ID")
    created_at: datetime = Field(alias="Created At")

    class Config:
        allow_population_by_field_name = True


class AirtableSSJTypeformStartASchoolResponse(AirtableResponse):
    fields: AirtableSSJTypeformStartASchoolFields
