from typing import Optional, Union

from pydantic import ConfigDict, Field, field_validator, RootModel

from app.airtable.base_model import BaseModel
from app.airtable.response import AirtableResponse
from app.airtable.validators import get_first_or_default_none


class CreateAirtableMontessoriCertificationFields(BaseModel):
    educator: Optional[list[str]] = Field(None, alias="Educator")
    year_certified: Optional[int] = Field(None, alias="Year Certified")
    certification_levels: Optional[list[str]] = Field(None, alias="Certification Levels")
    certifier: Optional[str] = Field(None, alias="Certifier")
    certifier_other: Optional[str] = Field(None, alias="Certifier - Other")
    certification_status: Optional[str] = Field(None, alias="Certification Status")
    model_config = ConfigDict(populate_by_name=True)


class AirtableMontessoriCertificationFields(CreateAirtableMontessoriCertificationFields):
    educator_full_name: Optional[str] = Field(None, alias="Educator Full Name")

    @field_validator("educator_full_name", mode="before")
    def _get_first_or_default_none(cls, v: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        return get_first_or_default_none(v)

    # _get_first_or_default_none = validator("educator_full_name", pre=True, allow_reuse=True)(get_first_or_default_none)


class AirtableMontessoriCertificationResponse(AirtableResponse):
    fields: AirtableMontessoriCertificationFields


class ListAirtableMontessoriCertificationResponse(RootModel):
    root: list[AirtableMontessoriCertificationResponse]
