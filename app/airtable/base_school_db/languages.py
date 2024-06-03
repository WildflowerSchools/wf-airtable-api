from enum import Enum
from typing import Optional, Union

from pydantic import ConfigDict, Field, field_validator, RootModel

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CertificationStatus(str, Enum):
    CERTIFIED = "Certified"
    NOT_IN_TRAINING = "Not in Training"
    PAUSED = "Paused"
    TRAINING = "Training"


class CreateAirtableLanguageFields(BaseModel):
    socio_economic_background: Optional[list[str]] = Field(None, alias="Socio-economic Background")
    language_dropdown: Optional[str] = Field(None, alias="Language")
    language_other: Optional[str] = Field(None, alias="Language - Other")
    is_primary_language: Optional[bool] = Field(None, alias="Is Primary Language")
    model_config = ConfigDict(populate_by_name=True)


class AirtableLanguageFields(CreateAirtableLanguageFields):
    educator_full_name: Optional[str] = Field(None, alias="Educator Full Name")
    language: Optional[str] = Field(None, alias="Language | Language Other")

    @field_validator("educator_full_name", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator("educator_full_name", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtableLanguageResponse(AirtableResponse):
    fields: AirtableLanguageFields


class ListAirtableLanguageResponse(RootModel):
    root: list[AirtableLanguageResponse]
