from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.airtable.response import AirtableResponse


class CreateAirtableSSJTypeformStartASchool(BaseModel):
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="Last Name")
    email: str = Field(alias="Email")
    is_montessori_certified: bool = Field(alias="Is Montessori Certified", default=False)
    montessori_certification_year: Optional[int] = Field(alias="Montessori Certification Year")
    montessori_certification_levels: Optional[str] = Field(alias="Montessori Certification Levels")
    school_location_city: str = Field(alias="School Location: City")
    school_location_state: str = Field(alias="School Location: State")
    school_location_country: Optional[str] = Field(alias="School Location: Country")
    school_location_community: Optional[str] = Field(alias="School Location: Community")
    contact_location_city: str = Field(alias="Contact Location: City")
    contact_location_state: str = Field(alias="Contact Location: State")
    contact_location_country: Optional[str] = Field(alias="Contact Location: Country")
    age_classrooms_interested_in_offering: str = Field(alias="Age Classrooms Interested In Offering")
    socio_economic_race_and_ethnicity: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity")
    socio_economic_race_and_ethnicity_other: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity Other")
    socio_economic_gender: Optional[str] = Field(alias="Socio-Economic: Gender")
    socio_economic_gender_other: Optional[str] = Field(alias="Socio-Economic: Gender Other")
    socio_economic_household_income: Optional[str] = Field(alias="Socio-Economic: Household Income")
    socio_economic_primary_language: Optional[str] = Field(alias="Socio-Economic: Primary Language")
    message: str = Field(alias="Message")
    receive_newsletter: bool = Field(alias="Receive Newsletter", default=False)
    receive_event_invitations: bool = Field(alias="Receive Event Invitations", default=False)

    class Config:
        allow_population_by_field_name = True


class AirtableSSJTypeformStartASchoolFields(CreateAirtableSSJTypeformStartASchool):
    response_id: str = Field(alias="Response ID")
    created_at: datetime = Field(alias="Created At")

    class Config:
        allow_population_by_field_name = True


class AirtableSSJTypeformStartASchoolResponse(AirtableResponse):
    fields: AirtableSSJTypeformStartASchoolFields
