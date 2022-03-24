from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class AirtableSocioEconomicBackgroundCoreFields(BaseModel):
    race_and_ethnicity: Optional[list[str]] = Field(alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(alias="Race & Ethnicity - Other")
    educational_attainment = Optional[str] = Field(alias="Educational Attainment")
    income_background = Optional[str] = Field(alias="Income Background")
    gender = Optional[str] = Field(alias="Gender")
    lgbtqia_identifying = Optional[bool] = Field(alias="LGBTQIA")
    pronouns = Optional[str] = Field(alias="Pronouns")


class AirtableSocioEconomicBackgroundFields(AirtableSocioEconomicBackgroundCoreFields):
    educator_id: Optional[str] = Field(alias="Educator")
    partner_id: Optional[str] = Field(alias="Partner")
    educator_full_name: Optional[str] = Field(alias="Educator Full Name")
    partner_name: Optional[str] = Field(alias="Partner Name")
    language_ids = Optional[list[str]] = Field(alias="Languages")

    _get_first_or_default_none = validator("educator_id", "partner_id", pre=True,
                                           allow_reuse=True)(get_first_or_default_none)


class AirtableSocioEconomicBackgroundResponse(AirtableResponse):
    fields: AirtableSocioEconomicBackgroundFields


class ListAirtableHubResponse(BaseModel):
    __root__: list[AirtableSocioEconomicBackgroundResponse]
