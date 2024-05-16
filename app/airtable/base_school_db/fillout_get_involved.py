from datetime import datetime
from typing import Optional

from pydantic import Field

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse


class CreateAirtableSSJFilloutGetInvolved(BaseModel):
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="Last Name")
    email: str = Field(alias="Email")
    contact_type: str = Field(alias="Contact Type")
    is_montessori_certified: bool = Field(alias="Is Montessori Certified", default=False)
    is_seeking_montessori_certification: bool = Field(alias="Is Seeking Montessori Certification", default=False)
    montessori_certification_certifier_1: Optional[str] = Field(alias="Montessori Certification Certifier 1")
    montessori_certification_year_1: Optional[int] = Field(alias="Montessori Certification Year 1")
    montessori_certification_level_1: Optional[str] = Field(alias="Montessori Certification Level 1")
    montessori_certification_certifier_2: Optional[str] = Field(alias="Montessori Certification Certifier 2")
    montessori_certification_year_2: Optional[int] = Field(alias="Montessori Certification Year 2")
    montessori_certification_level_2: Optional[str] = Field(alias="Montessori Certification Level 2")
    montessori_certification_certifier_3: Optional[str] = Field(alias="Montessori Certification Certifier 3")
    montessori_certification_year_3: Optional[int] = Field(alias="Montessori Certification Year 3")
    montessori_certification_level_3: Optional[str] = Field(alias="Montessori Certification Level 3")
    montessori_certification_certifier_4: Optional[str] = Field(alias="Montessori Certification Certifier 4")
    montessori_certification_year_4: Optional[int] = Field(alias="Montessori Certification Year 4")
    montessori_certification_level_4: Optional[str] = Field(alias="Montessori Certification Level 4")
    city: str = Field(alias="City")
    state: str = Field(alias="State")
    country: Optional[str] = Field(alias="Country")
    age_classrooms_interested_in_offering: Optional[str] = Field(alias="Age Classrooms Interested In Offering")
    educator_interests: Optional[str] = Field(alias="Educator Interests")
    educator_interests_other: Optional[str] = Field(alias="Educator Interests Other")
    community_member_interest: Optional[str] = Field(alias="Community Member Interest")
    community_member_support_finding_teachers: bool = Field(alias="Community Member Support Finding Teachers", default=False)
    community_member_community_info: Optional[str] = Field(alias="Community Member Community Info")
    community_member_self_info: Optional[str] = Field(alias="Community Member Self Info")
    socio_economic_race_and_ethnicity: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity")
    socio_economic_race_and_ethnicity_other: Optional[str] = Field(alias="Socio-Economic: Race & Ethnicity Other")
    socio_economic_pronouns: Optional[str] = Field(alias="Socio-Economic: Pronouns")
    socio_economic_pronouns_other: Optional[str] = Field(alias="Socio-Economic: Pronouns Other")
    socio_economic_gender: Optional[str] = Field(alias="Socio-Economic: Gender")
    socio_economic_gender_other: Optional[str] = Field(alias="Socio-Economic: Gender Other")
    socio_economic_household_income: Optional[str] = Field(alias="Socio-Economic: Household Income")
    socio_economic_primary_language: Optional[str] = Field(alias="Socio-Economic: Primary Language")
    socio_economic_primary_language_other: Optional[str] = Field(alias="Socio-Economic: Primary Language Other")
    message: str = Field(alias="Message")
    receive_communications: bool = Field(alias="Receive Communications", default=False)
    source: Optional[str] = Field(alias="Source")
    entry_date: datetime = Field(alias="Entry Date")

    class Config:
        allow_population_by_field_name = True


class AirtableSSJFilloutGetInvolvedFields(CreateAirtableSSJFilloutGetInvolved):
    response_id: str = Field(alias="Response ID")
    created_at: datetime = Field(alias="Created At")

    class Config:
        allow_population_by_field_name = True


class AirtableSSJFilloutGetInvolvedResponse(AirtableResponse):
    fields: AirtableSSJFilloutGetInvolvedFields