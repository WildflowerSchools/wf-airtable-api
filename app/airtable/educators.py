from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from .attachment import AirtableAttachment
from .educators_schools import AirtableEducatorsSchoolsResponse
from .languages import AirtableLanguageResponse
from .montessori_certifications import AirtableMontessoriCertificationResponse
from .response import AirtableResponse
from .validators import get_first_or_default_none, get_first_or_default_dict


class AirtableEducatorFields(BaseModel):
    full_name: Optional[str] = Field(alias="Full Name")
    first_name: Optional[str] = Field(alias="First Name")
    last_name: Optional[str] = Field(alias="Last Name")
    email: Optional[list[str]] = Field(alias="Contact Email")
    details: Optional[str] = Field(alias="Details")
    home_address: Optional[str] = Field(alias="Home Address")

    educators_schools: Optional[list[
        Union[str, AirtableEducatorsSchoolsResponse]]] = Field(alias="Educators at Schools")
    montessori_certifications: Optional[list[
        Union[str, AirtableMontessoriCertificationResponse]]] = Field(alias="Montessori Certifications")
    languages: Optional[list[
        Union[str, AirtableLanguageResponse]]] = Field(alias="Language Record IDs")

    target_community: Optional[list[str]] = Field(alias="Target Community Name")
    stage: Optional[str] = Field(alias="Stage")
    assigned_partner_id: Optional[list[str]] = Field(alias="Assigned Partner")
    visioning_album_complete: Optional[bool] = Field(alias="Visioning album complete")
    visioning_album: Optional[AirtableAttachment] = Field(alias="Visioning album", default={})
    current_roles: Optional[list[str]] = Field(alias="Current Role")
    source: Optional[list[str]] = Field(alias="Source")
    source_other: Optional[str] = Field(alias="Source - Other")
    race_and_ethnicity: Optional[list[str]] = Field(alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(alias="Race & Ethnicity - Other")
    educational_attainment: Optional[str] = Field(alias="Educational Attainment")
    income_background: Optional[str] = Field(alias="Income Background")
    gender: Optional[str] = Field(alias="Gender")
    lgbtqia_identifying: Optional[bool] = Field(alias="LGBTQIA")
    pronouns: Optional[str] = Field(alias="Pronouns")
    montessori_certified: Optional[bool] = Field(alias="Montessori Certified")

    _get_first_or_default_none = validator(
        "income_background",
        "gender",
        "lgbtqia_identifying",
        "pronouns",
        "race_and_ethnicity_other",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)

    _get_first_or_default_dict = validator(
        "visioning_album",
        pre=True,
        allow_reuse=True)(get_first_or_default_dict)

    @validator("lgbtqia_identifying", pre=True)
    def normalize_lgbtqia(cls, v):
        return v == "TRUE"

    @validator("educators_schools")
    def load_educators_schools_relationship(cls, value):
        from .client import AirtableClient
        airtable_client = AirtableClient()

        loaded_educators_schools = value.copy()
        for ii, educator_school in enumerate(loaded_educators_schools):
            if isinstance(educator_school, str):
                raw = airtable_client.get_educator_school_by_id(educator_school)
                loaded_educators_schools[ii] = AirtableEducatorsSchoolsResponse.parse_obj(raw)

        return loaded_educators_schools

    @validator("montessori_certifications")
    def load_montessori_certifications_relationship(cls, value):
        from .client import AirtableClient
        airtable_client = AirtableClient()

        loaded_montessori_certifications = value.copy()
        for ii, montessori_certification in enumerate(loaded_montessori_certifications):
            if isinstance(montessori_certification, str):
                raw = airtable_client.get_montessori_education_by_id(montessori_certification)
                loaded_montessori_certifications[ii] = AirtableMontessoriCertificationResponse.parse_obj(raw)

        return loaded_montessori_certifications

    @validator("languages")
    def load_languages_relationship(cls, value):
        from .client import AirtableClient
        airtable_client = AirtableClient()

        loaded_languages = value.copy()
        for ii, language in enumerate(loaded_languages):
            if isinstance(language, str):
                raw = airtable_client.get_language_by_id(language)
                loaded_languages[ii] = AirtableLanguageResponse.parse_obj(raw)

        return loaded_languages


class AirtableEducatorResponse(AirtableResponse):
    fields: AirtableEducatorFields


class ListAirtableEducatorResponse(BaseModel):
    __root__: list[AirtableEducatorResponse]
