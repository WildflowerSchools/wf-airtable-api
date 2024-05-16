from typing import Optional, Union

from pydantic import Field, validator

from . import (
    educators_schools as educators_schools_models,
    montessori_certifications as airtable_montessori_certifications_models,
    languages as airtable_languages_models,
    newsletters as airtable_newsletters_models,
)
from app.airtable.attachment import AirtableAttachment
from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none, get_first_or_default_dict


class CreateAirtableEducatorFields(BaseModel):
    # deprecated
    # contact: Optional[list[str]] = Field(alias="Contact Info")

    primary_personal_email: Optional[str] = Field(alias="Primary Personal Email")
    other_personal_emails: Optional[str] = Field(alias="Other Personal Emails")
    primary_wildflower_email: Optional[str] = Field(alias="Primary Wildflower Email")
    wildflowerschools_email: Optional[str] = Field(alias="Wildflowerschools.org Email")

    first_name: Optional[str] = Field(alias="First Name")
    last_name: Optional[str] = Field(alias="Last Name")
    details: Optional[str] = Field(alias="Contact Form Details")
    home_address: Optional[str] = Field(alias="Home Address")

    stage: Optional[str] = Field(alias="Stage")
    assigned_partner: Optional[list[str]] = Field(alias="Assigned Partner")
    target_community: Optional[list[str]] = Field(alias="Target community for exploration")

    source: Optional[list[str]] = Field(alias="Source")
    source_other: Optional[str] = Field(alias="Source - Other")

    ssj_typeforms_start_a_school: Optional[list[str]] = Field(alias="SSJ Typeforms: Start a School", default=[])
    ssj_fillout_forms_get_involved: Optional[list[str]] = Field(alias="SSJ Fillout Forms: Get Involved", default=[])
    newsletters: Optional[list[str]] = Field(alias="Newsletter and Group Subscriptions", default=[])

    initial_interest_in_age_classrooms: Optional[list[str]] = Field(alias="Initial Interest in Classroom Levels", default=[])
    initial_interest_in_governance_model: Optional[str] = Field(alias="Initial Interest in Governance Model")

    class Config:
        allow_population_by_field_name = True


class AirtableEducatorFields(CreateAirtableEducatorFields):
    full_name: Optional[str] = Field(alias="Full Name")
    # deprecated
    # all_contact_emails: Optional[list[str]] = Field(alias="All Contact Emails")

    email: Optional[str] = Field(alias="Contact Email")
    all_emails: Optional[list[str]] = Field(alias="All Emails")
    primary_personal_email: Optional[str] = Field(alias="Primary Personal Email")
    other_personal_emails: Optional[list[str]] = Field(alias="Other Personal Emails")
    primary_wildflower_email: Optional[str] = Field(alias="Primary Wildflower Email")
    wildflowerschools_email: Optional[str] = Field(alias="Wildflowerschools.org Email")

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
    lgbtqia_identifying: Optional[bool] = Field(alias="LGBTQIA")
    pronouns: Optional[str] = Field(alias="Pronouns")
    pronouns_other: Optional[str] = Field(alias="Pronouns - Other")
    visioning_album_complete: Optional[bool] = Field(alias="Visioning album complete", default=False)
    visioning_album: Optional[AirtableAttachment] = Field(alias="Visioning album", default={})

    hub: Optional[str] = Field(alias="Hub")
    hub_name: Optional[str] = Field(alias="Hub Name")

    educators_schools: Optional[list[Union[str, educators_schools_models.AirtableEducatorsSchoolsResponse]]] = Field(
        alias="Educators at Schools"
    )
    montessori_certifications: Optional[
        list[Union[str, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse]]
    ] = Field(alias="Montessori Certifications")
    languages: Optional[list[Union[str, airtable_languages_models.AirtableLanguageResponse]]] = Field(
        alias="Language Record IDs"
    )
    newsletters: Optional[list[Union[str, airtable_newsletters_models.AirtableNewsletterResponse]]] = Field(
        alias="Newsletter and Group Subscriptions", default=[]
    )

    class Config:
        allow_population_by_field_name = True

    _get_first_or_default_none = validator(
        "target_community_name",
        "household_income",
        "income_background",
        "gender",
        "gender_other",
        "lgbtqia_identifying",
        "pronouns",
        "pronouns_other",
        "race_and_ethnicity_other",
        "hub",
        "hub_name",
        pre=True,
        allow_reuse=True,
    )(get_first_or_default_none)

    _get_first_or_default_dict = validator("visioning_album", pre=True, allow_reuse=True)(get_first_or_default_dict)

    # deprecated
    # noinspection PyMethodParameters
    # @validator("all_contact_emails", pre=True)
    # def scrub_bad_contact_emails(cls, v):
    #     return list(filter(None, v))

    # noinspection PyMethodParameters
    @validator("all_emails", pre=True)
    def split_all_emails(cls, v):
        return v.split(",") if v is not None else None

    # noinspection PyMethodParameters
    @validator("other_personal_emails", pre=True)
    def split_other_personal_emails(cls, v):
        return v.split(",") if v is not None else None

    # noinspection PyMethodParameters
    @validator("lgbtqia_identifying", pre=True)
    def normalize_lgbtqia(cls, v):
        if v == "TRUE":
            return True
        elif v == "FALSE":
            return False
        else:
            return None

    def load_educators_schools_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        _ids = []
        _records = []

        if self.educators_schools is None:
            return _records

        for id_or_record in self.educators_schools:
            if isinstance(id_or_record, educators_schools_models.AirtableEducatorsSchoolsResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_guides_schools = airtable_client.list_educator_schools_by_ids(educator_school_ids=_ids)
        _records += list_airtable_guides_schools.__root__

        self.educators_schools = _records
        return _records

    def load_montessori_certifications_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        _ids = []
        _records = []

        if self.montessori_certifications is None:
            return _records

        for id_or_record in self.montessori_certifications:
            if isinstance(
                id_or_record, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse
            ):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_montessori_certifications = airtable_client.list_montessori_certifications_by_ids(
            montessori_certification_ids=_ids
        )
        _records += list_airtable_montessori_certifications.__root__

        return _records

    def load_languages_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        _ids = []
        _records = []

        if self.languages is None:
            return _records

        for id_or_record in self.languages:
            if isinstance(id_or_record, airtable_languages_models.AirtableLanguageResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_language_certifications = airtable_client.list_languages_by_ids(language_ids=_ids)
        _records += list_language_certifications.__root__

        self.languages = _records
        return _records

    def load_newsletters_relationship(self):
        from ..client import AirtableClient

        airtable_client = AirtableClient()

        _ids = []
        _records = []

        if self.newsletters is None:
            return _records

        for id_or_record in self.newsletters:
            if isinstance(id_or_record, airtable_newsletters_models.AirtableNewsletterResponse):
                _records.append(id_or_record)
            elif isinstance(id_or_record, str):
                _ids.append(id_or_record)

        list_airtable_newsletters = airtable_client.list_newsletters_by_ids(newsletter_ids=_ids)
        _records += list_airtable_newsletters.__root__

        self.newsletters = _records
        return _records

    def load_relationships(self):
        self.load_educators_schools_relationship()
        self.load_montessori_certifications_relationship()
        self.load_languages_relationship()
        self.load_newsletters_relationship()


class AirtableEducatorResponse(AirtableResponse):
    fields: AirtableEducatorFields

    def load_relationships(self):
        self.fields.load_relationships()


class ListAirtableEducatorResponse(BaseModel):
    __root__: list[AirtableEducatorResponse]

    def load_relationships(self):
        for r in self.__root__:
            r.load_relationships()
