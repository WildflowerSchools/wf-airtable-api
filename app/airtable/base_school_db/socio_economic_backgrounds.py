from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CreateAirtableSocioEconomicBackgroundFields(BaseModel):
    educator: Optional[list[str]] = Field(alias="Educator")
    partner: Optional[list[str]] = Field(alias="Partner")
    race_and_ethnicity: Optional[list[str]] = Field(alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(alias="Race & Ethnicity - Other")
    educational_attainment: Optional[str] = Field(alias="Educational Attainment")
    household_income: Optional[str] = Field(alias="Household Income")
    income_background: Optional[str] = Field(alias="Income Background As Child")
    gender: Optional[str] = Field(alias="Gender")
    gender_other: Optional[str] = Field(alias="Gender - Other")
    lgbtqia_identifying: Optional[str] = Field(alias="LGBTQIA", default=False)
    pronouns: Optional[str] = Field(alias="Pronouns")
    pronouns_other: Optional[str] = Field(alias="Pronouns - Other")

    class Config:
        allow_population_by_field_name = True


class AirtableSocioEconomicBackgroundFields(CreateAirtableSocioEconomicBackgroundFields):
    educator_full_name: Optional[str] = Field(alias="Educator Full Name")
    partner_name: Optional[str] = Field(alias="Partner Name")
    languages: Optional[list[str]] = Field(alias="Languages")

    _get_first_or_default_none = validator(
        "educator_full_name",
        "partner_name",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)


class AirtableSocioEconomicBackgroundResponse(AirtableResponse):
    fields: AirtableSocioEconomicBackgroundFields


class ListAirtableHubResponse(BaseModel):
    __root__: list[AirtableSocioEconomicBackgroundResponse]
