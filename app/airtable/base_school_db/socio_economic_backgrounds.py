from typing import Optional, Union

from pydantic import ConfigDict, Field, field_validator, RootModel

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CreateAirtableSocioEconomicBackgroundFields(BaseModel):
    educator: Optional[list[str]] = Field(None, alias="Educator")
    partner: Optional[list[str]] = Field(None, alias="Partner")
    race_and_ethnicity: Optional[list[str]] = Field(None, alias="Race & Ethnicity")
    race_and_ethnicity_other: Optional[str] = Field(None, alias="Race & Ethnicity - Other")
    educational_attainment: Optional[str] = Field(None, alias="Educational Attainment")
    household_income: Optional[str] = Field(None, alias="Household Income")
    income_background: Optional[str] = Field(None, alias="Income Background As Child")
    gender: Optional[str] = Field(None, alias="Gender")
    gender_other: Optional[str] = Field(None, alias="Gender - Other")
    lgbtqia_identifying: Optional[str] = Field(None, alias="LGBTQIA")
    pronouns: Optional[str] = Field(None, alias="Pronouns")
    pronouns_other: Optional[str] = Field(None, alias="Pronouns - Other")
    model_config = ConfigDict(populate_by_name=True)


class AirtableSocioEconomicBackgroundFields(CreateAirtableSocioEconomicBackgroundFields):
    educator_full_name: Optional[str] = Field(None, alias="Educator Full Name")
    partner_name: Optional[str] = Field(None, alias="Partner Name")
    languages: Optional[list[str]] = Field(None, alias="Languages")

    @field_validator("educator_full_name", "partner_name", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator("educator_full_name", "partner_name", pre=True, allow_reuse=True)(
    #     get_first_or_default_none
    # )


class AirtableSocioEconomicBackgroundResponse(AirtableResponse):
    fields: AirtableSocioEconomicBackgroundFields


class ListAirtableSocioEconomicBackgroundResponse(RootModel):
    root: list[AirtableSocioEconomicBackgroundResponse]
