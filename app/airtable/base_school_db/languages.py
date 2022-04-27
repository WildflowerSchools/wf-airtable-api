from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CertificationStatus(str, Enum):
    CERTIFIED = "Certified"
    NOT_IN_TRAINING = "Not in Training"
    PAUSED = "Paused"
    TRAINING = "Training"


class CreateAirtableLanguageFields(BaseModel):
    socio_economic_background: Optional[list[str]] = Field(alias="Socio-economic Background")
    language_dropdown: Optional[str] = Field(alias="Language")
    language_other: Optional[str] = Field(alias="Language - Other")
    is_primary_language: Optional[bool] = Field(alias="Is Primary Language")

    class Config:
        allow_population_by_field_name = True


class AirtableLanguageFields(CreateAirtableLanguageFields):
    educator_full_name: Optional[str] = Field(alias="Educator Full Name")
    language: Optional[str] = Field(alias="Language | Language Other")

    _get_first_or_default_none = validator("educator_full_name", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtableLanguageResponse(AirtableResponse):
    fields: AirtableLanguageFields


class ListAirtableLanguageResponse(BaseModel):
    __root__: list[AirtableLanguageResponse]
