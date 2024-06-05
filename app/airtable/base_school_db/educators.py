from typing import Optional, Union

from pydantic import field_validator, ConfigDict, Field, validator, RootModel

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

    individual_type: Optional[str] = Field("Educator", alias="Individual Type")
    primary_personal_email: Optional[str] = Field(None, alias="Primary Personal Email")
    other_personal_emails: Optional[str] = Field(None, alias="Other Personal Emails")
    primary_wildflower_email: Optional[str] = Field(None, alias="Primary Wildflower Email")
    wildflowerschools_email: Optional[str] = Field(None, alias="Wildflowerschools.org Email")

    first_name: Optional[str] = Field(None, alias="First Name")
    last_name: Optional[str] = Field(None, alias="Last Name")
    details: Optional[str] = Field(None, alias="Contact Form Details")
    home_address: Optional[str] = Field(None, alias="Home Address")

    stage: Optional[str] = Field(None, alias="Stage")
    status: Optional[str] = Field(None, alias="Status")

    assigned_partner: Optional[list[str]] = Field(None, alias="Assigned Partner")
    target_community: Optional[list[str]] = Field(None, alias="Target community for exploration")

    source: Optional[list[str]] = Field(None, alias="Source")
    source_other: Optional[str] = Field(None, alias="Source - Other")

    ssj_typeforms_start_a_school: Optional[list[str]] = Field(alias="SSJ Typeforms: Start a School", default=[])
    ssj_fillout_forms_get_involved: Optional[list[str]] = Field(alias="SSJ Fillout Forms: Get Involved", default=[])
    newsletters: Optional[list[str]] = Field(alias="Newsletter and Group Subscriptions", default=[])

    initial_interest_in_age_classrooms: Optional[list[str]] = Field(
        alias="Initial Interest in Classroom Levels", default=[]
    )
    initial_interest_in_governance_model: Optional[str] = Field(None, alias="Initial Interest in Governance Model")

    model_config = ConfigDict(populate_by_name=True)


class AirtableEducatorFields(CreateAirtableEducatorFields):
    full_name: Optional[str] = Field(None, alias="Full Name")
    # deprecated
    # all_contact_emails: Optional[list[str]] = Field(alias="All Contact Emails")

    email: Optional[str] = Field(None, alias="Contact Email")
    all_emails: Optional[list[str]] = Field(None, alias="All Emails")
    primary_personal_email: Optional[str] = Field(None, alias="Primary Personal Email")
    other_personal_emails: Optional[list[str]] = Field(None, alias="Other Personal Emails")
    primary_wildflower_email: Optional[str] = Field(None, alias="Primary Wildflower Email")
    wildflowerschools_email: Optional[str] = Field(None, alias="Wildflowerschools.org Email")

    current_roles: Optional[list[str]] = Field(None, alias="Current Role")
    montessori_certified: Optional[bool] = Field(alias="Montessori Certified", default=False)
    target_community_name: Optional[str] = Field(None, alias="Target Community Name")
    race_and_ethnicity: Optional[list[str]] = Field(None, alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(None, alias="Race & Ethnicity - Other")
    educational_attainment: Optional[str] = Field(None, alias="Educational Attainment")
    household_income: Optional[str] = Field(None, alias="Household Income")
    income_background: Optional[str] = Field(None, alias="Income Background")
    gender: Optional[str] = Field(None, alias="Gender")
    gender_other: Optional[str] = Field(None, alias="Gender - Other")
    lgbtqia_identifying: Optional[bool] = Field(None, alias="LGBTQIA")
    pronouns: Optional[str] = Field(None, alias="Pronouns")
    pronouns_other: Optional[str] = Field(None, alias="Pronouns - Other")
    visioning_album_complete: Optional[bool] = Field(alias="Visioning album complete", default=False)
    visioning_album: Optional[AirtableAttachment] = Field(alias="Visioning album", default={})

    hub: Optional[str] = Field(None, alias="Hub")
    hub_name: Optional[str] = Field(None, alias="Hub Name")

    educators_schools: Optional[list[Union[str, educators_schools_models.AirtableEducatorsSchoolsResponse]]] = Field(
        None, alias="Educators at Schools"
    )
    montessori_certifications: Optional[
        list[Union[str, airtable_montessori_certifications_models.AirtableMontessoriCertificationResponse]]
    ] = Field(None, alias="Montessori Certifications")
    languages: Optional[list[Union[str, airtable_languages_models.AirtableLanguageResponse]]] = Field(
        None, alias="Language Record IDs"
    )
    newsletters: Optional[list[Union[str, airtable_newsletters_models.AirtableNewsletterResponse]]] = Field(
        alias="Newsletter and Group Subscriptions", default=[]
    )
    model_config = ConfigDict(populate_by_name=True)

    @field_validator(
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
        mode="before",
    )
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator(
    #     "target_community_name",
    #     "household_income",
    #     "income_background",
    #     "gender",
    #     "gender_other",
    #     "lgbtqia_identifying",
    #     "pronouns",
    #     "pronouns_other",
    #     "race_and_ethnicity_other",
    #     "hub",
    #     "hub_name",
    #     pre=True,
    #     allow_reuse=True,
    # )(get_first_or_default_none)

    @field_validator("visioning_album", mode="before")
    def _get_first_or_default_dict(cls, v: Union[str, int, float]) -> Union[str, int, float, dict]:
        return get_first_or_default_dict(v)

    # _get_first_or_default_dict = validator("visioning_album", pre=True, allow_reuse=True)(get_first_or_default_dict)

    # deprecated
    # noinspection PyMethodParameters
    # @validator("all_contact_emails", pre=True)
    # def scrub_bad_contact_emails(cls, v):
    #     return list(filter(None, v))

    # noinspection PyMethodParameters
    @field_validator("all_emails", mode="before")
    @classmethod
    def split_all_emails(cls, v):
        return v.split(",") if v is not None else None

    # noinspection PyMethodParameters
    @field_validator("other_personal_emails", mode="before")
    @classmethod
    def split_other_personal_emails(cls, v):
        return v.split(",") if v is not None else None

    # noinspection PyMethodParameters
    @field_validator("lgbtqia_identifying", mode="before")
    @classmethod
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
        _records += list_airtable_guides_schools.root

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
        _records += list_airtable_montessori_certifications.root

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
        _records += list_language_certifications.root

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
        _records += list_airtable_newsletters.root

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


class ListAirtableEducatorResponse(RootModel):
    root: list[AirtableEducatorResponse]

    def load_relationships(self):
        for r in self.root:
            r.load_relationships()
