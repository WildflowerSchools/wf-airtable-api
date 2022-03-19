from typing import Optional

from pydantic import BaseModel, Field, validator

from .response import AirtableResponse
from .validators import get_first_or_default_none


class AirtableLanguageFields(BaseModel):
    socio_economic_background_id: Optional[str] = Field(alias="Socio-economic Background")
    full_name: Optional[str] = Field(alias="Full Name")
    language: Optional[str] = Field(alias="Language | Language Other")
    language_dropdown: Optional[str] = Field(alias="Language")
    language_other: Optional[str] = Field(alias="Language - Other")
    is_primary_language: Optional[bool] = Field(alias="Is Primary Language")

    _get_first_or_default_none = validator(
        "socio_economic_background_id",
        "full_name",
        pre=True,
        allow_reuse=True)(get_first_or_default_none)


class AirtableLanguageResponse(AirtableResponse):
    fields: AirtableLanguageFields


class ListAirtableHubResponse(BaseModel):
    __root__: list[AirtableLanguageResponse]
