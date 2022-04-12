from typing import Optional, Union

from pydantic import BaseModel, Field, validator

from . import montessori_certifications as airtable_montessori_certifications_models, \
    languages as airtable_languages_models, \
    educators_schools as airtable_educators_schools_models, \
    newsletters as airtable_newsletters_models
from app.airtable.attachment import AirtableAttachment
from .languages import AirtableLanguageResponse
from .montessori_certifications import AirtableMontessoriCertificationResponse
from .newsletters import AirtableNewsletterResponse
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none, get_first_or_default_dict


class CreateAirtableEducatorFields(BaseModel):
    first_name: Optional[str] = Field(alias="First Name")
    last_name: Optional[str] = Field(alias="Last Name")
    details: Optional[str] = Field(alias="Details")
    home_address: Optional[str] = Field(alias="Home Address")

    stage: Optional[str] = Field(alias="Stage")
    assigned_partner: Optional[list[str]] = Field(alias="Assigned Partner")
    target_community: Optional[list[str]] = Field(alias="Target community for exploration")

    source: Optional[list[str]] = Field(alias="Source")
    source_other: Optional[str] = Field(alias="Source - Other")

    ssj_typeforms_start_a_school: Optional[list[str]] = Field(alias="SSJ Typeforms: Start a School")
    newsletters: Optional[list[str]] = Field(alias="Newsletter and Group Subscriptions")

    class Config:
        allow_population_by_field_name = True


class AirtableEducatorFields(CreateAirtableEducatorFields):
    full_name: Optional[str] = Field(alias="Full Name")
    email: Optional[list[str]] = Field(alias="Contact Email")
    current_roles: Optional[list[str]] = Field(alias="Current Role")
    montessori_certified: Optional[bool] = Field(alias="Montessori Certified", default=False)
    target_community_name: Optional[str] = Field(alias="Target Community Name")
    race_and_ethnicity: Optional[list[str]] = Field(alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(alias="Race & Ethnicity - Other")
    educational_attainment: Optional[str] = Field(alias="Educational Attainment")
    household_income: Optional[str] = Field(alias="Household Income")
    income_background: Optional[str] = Field(alias="Income Background")
    gender: Optional[str] = Field(alias="Gender")
    gender_other: Optional[str] = Field(alias="Gender - Other")
    lgbtqia_identifying: Optional[bool] = Field(alias="LGBTQIA", default=False)
    pronouns: Optional[str] = Field(alias="Pronouns")
    pronouns_other: Optional[str] = Field(alias="Pronouns - Other")
    visioning_album_complete: Optional[bool] = Field(alias="Visioning album complete", default=False)
    visioning_album: Optional[AirtableAttachment] = Field(alias="Visioning album", default={})

    hub: Optional[str] = Field(alias="Hub")
    hub_name: Optional[str] = Field(alias="Hub Name")

    educators_schools: Optional[list[
        Union[str, airtable_educators_schools_models.AirtableEducatorsSchoolsResponse]]] = Field(alias="Educators at Schools")
    montessori_certifications: Optional[list[
        Union[str, AirtableMontessoriCertificationResponse]]] = Field(alias="Montessori Certifications")
    languages: Optional[list[
        Union[str, AirtableLanguageResponse]]] = Field(alias="Language Record IDs")
    newsletters: Optional[list[
        Union[str, AirtableNewsletterResponse]]] = Field(alias="Newsletter and Group Subscriptions", default=[])

    class Config:
        allow_population_by_field_name = True

    _get_first_or_default_none = validator(
        "target_community_name",
        "household_income",
        "income_background",
        "gender",
        "lgbtqia_identifying",
        "pronouns",
        "race_and_ethnicity_other",
        "hub",
        "hub_name",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)

    _get_first_or_default_dict = validator(
        "visioning_album",
        pre=True,
        allow_reuse=True)(get_first_or_default_dict)

    # noinspection PyMethodParameters
    @validator("lgbtqia_identifying", pre=True)
    def normalize_lgbtqia(cls, v):
        return v == "TRUE"

    # noinspection PyMethodParameters
    @validator("educators_schools")
    def load_educators_schools_relationship(cls, value):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        educators_schools = value.copy()
        _ids = []
        _records = []
        for id_or_record in educators_schools:
            if isinstance(id_or_record, airtable_educators_schools_models.AirtableEducatorsSchoolsResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_guides_schools = airtable_client.list_educator_schools_by_ids(educator_school_ids=_ids)
        _records += list_airtable_guides_schools.__root__

        return _records

    # noinspection PyMethodParameters
    @validator("montessori_certifications")
    def load_montessori_certifications_relationship(cls, value):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        montessori_certifications = value.copy()
        _ids = []
        _records = []
        for id_or_record in montessori_certifications:
            if isinstance(id_or_record, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_montessori_certifications = airtable_client.list_montessori_certifications_by_ids(
            montessori_certification_ids=_ids)
        _records += list_airtable_montessori_certifications.__root__

        return _records

    # noinspection PyMethodParameters
    @validator("languages")
    def load_languages_relationship(cls, value):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        languages = value.copy()
        _ids = []
        _records = []
        for id_or_record in languages:
            if isinstance(id_or_record, airtable_languages_models.AirtableLanguageResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_language_certifications = airtable_client.list_languages_by_ids(language_ids=_ids)
        _records += list_language_certifications.__root__

        return _records

    # noinspection PyMethodParameters
    @validator("newsletters")
    def load_newsletters_relationship(cls, value):
        from ..client import AirtableClient
        airtable_client = AirtableClient()

        newsletters = value.copy()
        _ids = []
        _records = []
        for id_or_record in newsletters:
            if isinstance(id_or_record, airtable_newsletters_models.AirtableNewsletterResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_newsletters = airtable_client.list_newsletters_by_ids(newsletter_ids=_ids)
        _records += list_airtable_newsletters.__root__

        return _records


class AirtableEducatorResponse(AirtableResponse):
    fields: AirtableEducatorFields


class ListAirtableEducatorResponse(BaseModel):
    __root__: list[AirtableEducatorResponse]
